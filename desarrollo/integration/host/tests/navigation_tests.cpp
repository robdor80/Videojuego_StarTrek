#include "test_support.h"
#include "f04_host_navigation.h"
#include "gateway_test_access.h"
#include "navigation/route_solver.h"
#include "player_bootstrap.h"
#include "slot_store.h"

#include <corerpg/campaign_persistence.hpp>
#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>

using namespace test;
namespace fs = std::filesystem;
namespace {
using S = NavigationStatus;

NavalBootstrap chart() {
    return {"bajor", SessionOwner::naval_chart_publication(), {
        {0, true, true, {"deep_space_9", "trill", "ferenginar", "bajoran_wormhole_alpha",
                        "bajoran_wormhole_gamma"},
         {"bajor_deep_space_9_local", "bajor_trill", "deep_space_9_bajoran_wormhole",
          "bajoran_wormhole_traversal", "bajor_cardassia_prime"}},
        {1, false, true, {"bajor", "trill"}, {}},
    }};
}

struct Fixture {
    fs::path root;
    SessionOwner owner;
    Generation generation;

    explicit Fixture(fs::path path) : root(std::move(path)), owner(StorageConfig{root.string()}) {}
    void open(NavalBootstrap bootstrap, std::uint64_t ordinal = 0, bool bind = true,
              std::uint64_t ship = 65001) {
        auto config = population();
        config.ship_identity = ship;
        auto opened = owner.open_naval(config, std::move(bootstrap)).get();
        expect(opened, Error::OK);
        generation = opened.generation;
        if (!bind) return;
        visit([&](F04Session* session) {
            F04Handles handles{};
            require(f04_handles(session, &handles) == F04_OK, "Bootstrap handles");
            F04Person selected{};
            std::uint64_t written = 0, total = 0;
            require(f04_manifest_page(session, handles.captain, ordinal, &selected, 1, &written, &total)
                == F04_OK && written == 1, "Resolve bootstrap person");
            person = selected.id;
        });
        const auto selected = PlayerBootstrap::prepare(owner, generation, person).get();
        require(selected.error == Error::OK && selected.selection, "Prepare player");
        require(PlayerBootstrap::bind(owner, generation, *selected.selection, selected.revision).get().error ==
                Error::OK, "Bind player");
    }

    void visit(std::function<void(F04Session*)> use) {
        expect(GatewayTestAccess::visit(owner, generation, std::move(use)).get(), Error::OK);
    }
    NavigationView view() {
        auto result = owner.query_navigation(generation).get();
        require(result.error == Error::OK && result.view, "Navigation read");
        return std::move(*result.view);
    }
    NavigationResult propose(std::string destination, std::string profile = "safest") {
        return owner.propose_route(generation, {std::move(destination), std::move(profile), view().revision}).get();
    }
    RouteProposal proposal(std::string destination = "deep_space_9") {
        auto result = propose(std::move(destination));
        require(result.error == Error::OK && result.status == S::OK && result.proposal &&
                result.proposal->reference, "Route not issued");
        return std::move(*result.proposal);
    }
    void stale(std::uint64_t reference) {
        auto result = owner.validate_route(generation, reference).get();
        require(result.error == Error::REVISION_STALE && !result.proposal && !result.view &&
                result.candidates.empty(), "Stale route exposed");
    }
    std::vector<std::uint8_t> bytes() {
        std::vector<std::uint8_t> archive;
        visit([&](F04Session* session) {
            std::uint64_t size = 0;
            auto save = f04_save;
            auto code = save(session, nullptr, 0, &size);
            if (code == F04_SAVE) {
                save = f04_history_export_active;
                code = save(session, nullptr, 0, &size);
            }
            require(code == F04_CAPACITY && size, "Archive size");
            archive.resize(static_cast<std::size_t>(size));
            require(save(session, archive.data(), size, &size) == F04_OK, "Read canonical archive");
        });
        return archive;
    }
    SlotAddress save(std::string slot = "nav") {
        const auto campaign = owner.campaign_id(generation);
        expect(owner.save(generation, slot).get(), Error::OK);
        return {campaign, std::move(slot), 1};
    }
    void restore(const SlotAddress& slot) {
        const auto before = generation;
        auto restored = owner.restore(generation, slot).get();
        expect(restored, Error::OK);
        generation = restored.generation;
        require(before != generation, "Restore reused generation");
    }

    std::uint64_t person = 0;
};

void denied(const NavigationResult& result, S status) {
    require(result.error == Error::OK && result.status == status && !result.proposal &&
            !result.view && result.candidates.empty(), "Unexpected domain rejection");
}

void run(std::string name, Fixture& f) {
    if (name == "01") {
        f.open({});
        const auto legacy = f.save();
        f.restore(legacy);
        const auto view = f.view();
        require(!view.location && view.places.empty() && view.edges.empty() &&
                view.revision.chart.empty(), "Legacy acquired an invented origin or chart");
        denied(f.propose("earth"), S::LOCATION_UNKNOWN);
        expect(f.owner.close().get(), Error::OK);
        NavalBootstrap published_without_origin{std::nullopt, SessionOwner::naval_chart_publication(),
            {{0, false, true, {"earth"}, {}}}};
        f.open(std::move(published_without_origin));
        const auto published = f.view();
        require(!published.location && published.places.size() == 1, "Chart invented an initial origin");
        denied(f.propose("earth"), S::LOCATION_UNKNOWN);
    } else if (name == "02") {
        f.open({"bajor", std::nullopt, {{0, true, false, {}, {}}}});
        auto view = f.view();
        require(view.location && view.location->id == "bajor" && view.location->type == "planet" &&
                view.revision.chart.empty(), "Explicit origin did not project independently of chart");
        denied(f.propose("Bajor"), S::CHART_UNAVAILABLE);
        auto bytes = corerpg::CampaignPersistence::deserialize(f.bytes());
        require(bytes.snapshot.has_value(), "Decode native origin archive");
        const auto& campaign = bytes.snapshot->campaign;
        auto place = std::ranges::find_if(campaign.definitions, [](const auto& d) {
            return d.definition_id == "trek.f04:nav_place_bajor";
        });
        require(place != campaign.definitions.end() &&
                std::ranges::any_of(campaign.containment, [&](const auto& containment) {
                    return containment.container == place->entity;
                }), "Origin absent from Core containment");
        f.restore(f.save());
        require(f.view().location->id == "bajor", "Origin lost to restore");
    } else if (name == "03") {
        f.open(chart());
        const auto view = f.view();
        require(view.revision.chart == SessionOwner::naval_chart_publication() && view.places.size() == 6 &&
                view.edges.size() == 4 &&
                std::ranges::none_of(view.edges, [](const auto& edge) { return edge.id == "bajor_cardassia_prime"; }),
                "Unpublished, ungranted or dangling edge exposed");
        f.restore(f.save());
        const auto restored = f.view();
        require(restored.places.size() == view.places.size() && restored.edges.size() == view.edges.size() &&
                restored.revision.chart == view.revision.chart, "Publication/grants lost on restore");
    } else if (name == "04") {
        f.open(chart(), 1);
        auto view = f.view();
        require(!view.location && view.places.size() == 2 && view.edges.empty(), "Cross-observer knowledge leak");
        expect(f.owner.close().get(), Error::OK);
        f.open(chart());
        auto route = f.proposal();
        f.visit([&](F04Session* session) {
            F04Handles handles{};
            require(f04_handles(session, &handles) == F04_OK &&
                    nav_bridge::revoke_chart(session, {handles.ship.scope, f.person}) == F04_OK, "Core revocation");
        });
        view = f.view();
        require(view.location && view.revision.chart.empty() && view.places.empty() && view.edges.empty(),
                "Chart remained visible after revocation");
        f.stale(route.reference);
        denied(f.propose("deep_space_9"), S::CHART_UNAVAILABLE);
        f.restore(f.save());
        require(f.view().revision.chart.empty(), "Restore refreshed revoked knowledge");
        expect(f.owner.close().get(), Error::OK);
        f.open(chart(), 1);
        f.visit([&](F04Session* session) {
            F04Handles handles{};
            F04Stats stats{};
            require(f04_handles(session, &handles) == F04_OK && f04_stats(session, &stats) == F04_OK,
                    "Departure authority");
            F04Request request{handles.captain, stats.revision, F04_DEPART, 0, f.person, 0, 0, 0, 1};
            F04Result result{};
            require(f04_execute(session, &request, &result) == F04_OK, "Crew departure");
        });
        const auto former = f.owner.query_navigation(f.generation).get();
        require(former.error == Error::ACCESS_DENIED && !former.view, "Former crew retained navigation access");
    } else if (name == "05") {
        f.open(chart());
        auto view = f.view();
        // The published chart has no homonyms. Add a second visible name in
        // this detached projection to exercise the production resolver.
        view.places.push_back({"test_visible_alias", "Nombre compartido", "planet", {}, {}});
        const RouteIntent intent{"nombre compartido", "safest", view.revision};
        std::vector<ChartPlace> candidates;
        RouteProposal proposal;
        // An explicit ID takes precedence. Use a display name distinct from IDs.
        for (auto& place : view.places)
            if (place.id == "bajor") place.name = "Nombre compartido";
        require(detail::solve_route(view, intent, candidates, proposal) == S::CLARIFICATION_REQUIRED &&
                candidates.size() == 2, "Visible homonyms did not require clarification");
        view.places.pop_back();
        candidates.clear();
        require(detail::solve_route(view, intent, candidates, proposal) == S::OK && candidates.empty() &&
                proposal.destination == "bajor", "Missing homonym influenced resolution");
    } else if (name == "06") {
        f.open(chart());
        denied(f.propose("Cardassia Prime"), S::DESTINATION_UNKNOWN_OR_REDACTED);
        denied(f.propose("does_not_exist"), S::DESTINATION_UNKNOWN_OR_REDACTED);
    } else if (name == "07") {
        f.open(chart());
        for (auto profile : {"fastest", "safest", "avoid_hostile_space", "prefer_starbase_support", "silent_or_low_contact"}) {
            auto result = f.propose("TRILL", profile);
            require(result.error == Error::OK && result.proposal && result.proposal->profile == profile &&
                    result.proposal->legs.size() == 1 && result.proposal->legs.front().id == "bajor_trill" &&
                    result.proposal->distance_ly == 30 && result.proposal->profile_data_incomplete,
                    "Profile/authored distance/edge mismatch");
        }
        const auto route = f.proposal("bajoran_wormhole_alpha");
        require(route.legs.size() == 2 && route.legs.back().origin == "deep_space_9", "Known two-leg path missing");
        denied(f.propose("trill", "invented"), S::INVALID_PROFILE);
    } else if (name == "08") {
        f.open(chart());
        denied(f.propose("ferenginar"), S::NO_KNOWN_ROUTE);
        denied(f.propose("bajoran_wormhole_gamma"), S::NO_KNOWN_ROUTE);
    } else if (name == "09") {
        f.open(chart());
        const auto route = f.proposal();
        require(!route.eta && !route.distance_ly && route.legs.size() == 1 && !route.legs.front().distance_ly &&
                !f.view().location->z_ly, "Invented distance, z or ETA");
    } else if (name == "10") {
        f.open(chart());
        const auto before = f.bytes();
        const auto route = f.proposal();
        require(f.owner.validate_route(f.generation, route.reference).get().proposal.has_value(), "Live reference");
        denied(f.propose("unknown"), S::DESTINATION_UNKNOWN_OR_REDACTED);
        denied(f.propose("ferenginar"), S::NO_KNOWN_ROUTE);
        require(before == f.bytes(), "Read/proposal/rejection altered canonical Core archive");
    } else if (name == "11") {
        auto unavailable = chart();
        unavailable.chart_publication = "other-publication";
        expect(f.owner.open_naval(population(), unavailable).get(), Error::INVALID_ARGUMENT);
        closed(f.owner);
        f.open(chart());
        const auto route = f.proposal();
        auto incorrect = route.revision;
        incorrect.chart += "changed";
        auto denied = f.owner.propose_route(f.generation, {"trill", "fastest", incorrect}).get();
        require(denied.error == Error::REVISION_STALE && !denied.proposal, "Wrong chart version accepted");
        const auto tick = f.owner.advance_clock(f.generation,
            {1, route.revision.core, route.revision.tick, route.revision.tick + 1, 1}).get();
        require(tick.error == Error::OK, "Core tick did not advance");
        f.stale(route.reference);
        denied = f.owner.propose_route(f.generation, {"trill", "fastest", route.revision}).get();
        require(denied.error == Error::REVISION_STALE && !denied.proposal, "Old tick accepted");
    } else if (name == "12") {
        f.open(chart());
        const auto before_save = f.proposal();
        const auto slot = f.save();
        f.stale(before_save.reference);
        const auto before_restore = f.proposal();
        const auto generation = f.generation;
        f.restore(slot);
        f.stale(before_restore.reference);
        require(f.owner.validate_route(generation, before_restore.reference).get().error == Error::GENERATION_EXPIRED,
                "Restore kept old generation");
        const auto before_close = f.proposal();
        expect(f.owner.close().get(), Error::OK);
        f.open(chart(), 1, true, 65002);
        f.stale(before_close.reference);
    } else if (name == "13") {
        f.open(chart());
        const auto before = f.bytes();
        auto decoded = corerpg::CampaignPersistence::deserialize(before);
        require(decoded.snapshot.has_value(), "Decode for semantic corruption test");
        auto& snapshot = decoded.snapshot->campaign;
        const auto definition = std::ranges::find_if(snapshot.definitions, [](const auto& row) {
            return row.definition_id == "trek.f04:nav_chart";
        });
        require(definition != snapshot.definitions.end(), "Persisted chart record");
        auto stamp = std::ranges::find(snapshot.relations, definition->entity, &corerpg::EntityRelation::source);
        require(stamp != snapshot.relations.end(), "Persisted chart stamp");
        snapshot.relations.erase(stamp);
        const auto altered = corerpg::CampaignPersistence::serialize(*decoded.snapshot);
        require(altered.status == corerpg::CampaignArchiveStatus::success, "Core-valid corruption fixture");
        f.visit([&](F04Session* session) {
            require(f04_load(session, altered.bytes.data(), altered.bytes.size()) == F04_SAVE,
                    "F04 accepted chart with invalid stamp");
        });
        require(before == f.bytes(), "Rejected Core archive changed campaign");
        auto healthy = f.save("healthy");
        auto damaged = f.save("damaged");
        const auto current = f.root / "campaigns" / damaged.campaign / "slots" / "damaged" / "v1" / "history" / "CURRENT";
        require(fs::is_regular_file(current), "History CURRENT missing");
        std::ofstream(current, std::ios::binary | std::ios::trunc) << "damaged";
        require(f.owner.restore(f.generation, damaged).get().error != Error::OK && f.bytes() == before,
                "Broken history replaced active campaign");
        f.restore(healthy);
        require(f.bytes() == before && f.view().location->id == "bajor", "Verified history changed canonical state");
    } else if (name == "14") {
        f.open(chart(), 0, false);
        require(f.owner.query_navigation(f.generation).get().error == Error::PRINCIPAL_UNBOUND,
                "Unbound HOST exposed navigation");
        expect(f.owner.close().get(), Error::OK);
        f.open(chart());
        const auto before = f.bytes();
        const auto view = f.view();
        const auto route = f.proposal("trill");
        require(route.revision.tick == view.revision.tick && f.view().location->id == view.location->id &&
                f.view().revision == view.revision && f.bytes() == before, "Proposal moved ship or advanced time");
    } else throw std::runtime_error("Unknown CN2 case");
}
}

namespace trek::host::detail {
void gateway_test_after_bind() {}
void gateway_test_after_clock(F04Session*) {}
void gateway_test_after_dispatch(F04Session*, std::uint32_t&) {}
}

int main(int argc, char** argv) {
    try {
        require(argc == 3, "Usage: navigation_tests case root");
        auto root = fs::absolute(argv[2]) / detail::new_campaign_id();
        fs::create_directories(root);
        fs::permissions(root, fs::perms::owner_all, fs::perm_options::replace);
        Fixture fixture(root);
        run(argv[1], fixture);
        std::cout << "PASS CN2-" << argv[1] << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
