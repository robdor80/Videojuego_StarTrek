#include "f10/academy_player_binding.h"
#include "player_bootstrap.h"
#include "test_support.h"

#include <bit>
#include <filesystem>
#include <iomanip>
#include <iostream>

#ifdef TREK_HOST_ACADEMY_TESTING
#include "f10/academy_campaign.h"
#include "slot_store.h"

#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <semaphore>
#endif

namespace fs = std::filesystem;

#ifdef TREK_HOST_ACADEMY_TESTING
namespace trek::host::detail {
struct AcademyPersistenceTest {
    static void mutate(AcademyCampaign& candidate, const fs::path& destination, std::string_view mode)
    {
        using namespace corerpg;
        using test::require;
        auto& world = candidate.world_;
        auto& random = candidate.random_;
        auto& clock = candidate.timeline_;
        auto& catalog = candidate.catalog_;
        const auto remove_person_definition = [&] {
            auto checkpoint = CampaignPersistence::capture(world, random, clock);
            const auto removed = std::erase_if(checkpoint.campaign.definitions, [&](const auto& binding) {
                return binding.entity == candidate.person_;
            });
            ++checkpoint.campaign.revision;
            require(removed == 1 && CampaignPersistence::restore(checkpoint, world, random, clock, {}, &catalog) ==
                        CampaignArchiveStatus::success, "Remove PERSON definition");
        };

        if (mode == "advanced") {
            const auto event = world.create_entity();
            require(event.is_valid() && world.add_relation({event, RelationKind{201}, candidate.person_}) ==
                        RelationChange::applied, "Add independent Core history fact");
            require(clock.advance(world, random, 31).status == TimelineStatus::completed, "Advance Core timeline");
            (void)random.stream(7).next();
            copy_history(candidate.history_pin_->path(), destination);
            HistoryArchive archive;
            WorldState previous;
            RandomStreams previous_rng{0};
            Timeline previous_clock;
            require(HistoryPersistence::recover(destination, archive, previous, previous_rng, previous_clock,
                                                &catalog) == HistoryStatus::success, "Recover source archive for fixture");
            const std::array selected{HistorySelection{event, 0, 30}};
            require(HistoryPersistence::consolidate(archive, world, random, clock, selected, 30, &catalog) ==
                        HistoryStatus::success && archive.segments().size() == 1, "Consolidate real Core history");
        } else {
            if (mode == "missing-person") {
                remove_person_definition();
            } else if (mode == "duplicate-person") {
                candidate.create_entity("person");
            } else if (mode == "wrong-subject") {
                require(world.remove_relation({candidate.creation_fact_, RelationKind{2}, candidate.person_}) ==
                            RelationChange::applied &&
                        world.add_relation({candidate.creation_fact_, RelationKind{2}, candidate.campus_}) ==
                            RelationChange::applied, "Change creation fact subject");
            } else if (mode == "background") {
                const auto edges = world.relations_from(candidate.creation_fact_);
                const auto edge = std::ranges::find(edges, RelationKind{4}, &EntityRelation::kind);
                require(edge != edges.end(), "Find canonical background edge");
                const auto removed = *edge;
                require(world.remove_relation(removed) == RelationChange::applied, "Remove canonical background");
            } else {
                require(mode == "admitted" || mode == "legacy", "Unknown mutation");
                const auto version = SemanticVersion::parse("2.0.0").value();
                const auto schema = SemanticVersion::parse("0.1.0").value();
                const auto pack = PackId::parse("startrek.academy").value();
                const auto def = DefinitionId::parse(mode == "admitted"
                    ? "startrek.academy:starfleet_academy/v2/admitted"
                    : "startrek.academy:starfleet_academy/v1/person").value();
                std::vector<ContentDefinitionInput> definitions;
                for (const auto& definition : catalog.definitions()) definitions.emplace_back(definition);
                definitions.emplace_back(ResourceDefinition{def, *ResourceKind::parse("event")});
                const auto altered = ContentCatalog::create({ContentPackInput{
                    ContentManifest{pack, version, schema, schema}, std::move(definitions)}});
                require(altered.succeeded(), "Construct incompatible fixture catalog");
                EntityId entity;
                if (mode == "legacy") {
                    entity = candidate.person_;
                    remove_person_definition();
                } else entity = world.create_entity();
                require(world.bind_definition(entity, *altered.catalog(), def) == DefinitionBindingChange::applied,
                        "Bind unsupported academic definition");
            }
            HistoryArchive damaged;
            require(HistoryPersistence::migrate(destination, candidate.history_.campaign_id(), world, random, clock, damaged) ==
                        HistoryStatus::success, "Publish self-consistent Core archive for negative test");
        }
        std::cout << world.revision() << ' ' << clock.now() << '\n';
        if (mode == "advanced") std::cout << candidate.inspect_checkpoint().checkpoint_digest << '\n';
    }
};
}
#endif

namespace {
using namespace test;
using namespace trek::host::detail;

StorageConfig storage(const fs::path& root)
{
    const auto utf8 = fs::absolute(root).make_preferred().u8string();
    return {std::string(utf8.begin(), utf8.end())};
}

AcademyCreationResult create(SessionOwner& owner)
{
    const auto intent = AcademyCandidateFactory::begin(owner);
    require(bool(intent), "Missing B02 intent");
    const auto created = AcademyCandidateFactory::create(owner, intent,
        R"({"display_name":"Nara T\u2019Var \u00e9"})").get();
    require(created.error == Error::OK && created.receipt, "B02 creation failed");
    expect(owner.save(created.generation, "alpha").get(), Error::PRINCIPAL_UNBOUND);
    expect(AcademyPlayerBinding::bind(owner, created.generation, created.receipt).get(), Error::OK);
    return created;
}

void denied(SessionOwner& owner, Generation generation)
{
    for (const auto& result : {owner.query_view(generation, 1).get(), owner.submit_order(generation, {}, 2).get(),
                               owner.query_order(generation, 1, 3).get(), owner.cancel_order(generation, 1, 0, 4).get(),
                               owner.institutional_command(generation, 5).get()}) {
        require(result.error == Error::ACCESS_DENIED && !result.campaign && !result.order && !result.receipt,
                "Restored Academy reached naval gateway");
    }
}

AcademyCandidateView view_of(SessionOwner& owner, Generation generation)
{
    const auto view = AcademyPlayerBinding::inspect(owner, generation).get();
    require(view.error == Error::OK && view.candidate, "Bound Academy inspection failed");
    const auto& candidate = *view.candidate;
    require(candidate.campaign_id == owner.campaign_id(generation) && candidate.creation_fact != 0 &&
                candidate.person_count == 1 && candidate.creation_fact_count == 1 &&
                candidate.population_count == 0 && candidate.display_name == "Nara T’Var é" &&
                candidate.checkpoint_digest.size() == 64 && !candidate.background.empty(),
            "Lost validated candidate state");
    const auto player = owner.current_player(generation);
    require(player.error == Error::OK && player.player && player.player->generation == generation &&
                player.player->person_id == candidate.person, "H03 did not project the restored PERSON");
    require(PlayerBootstrap::prepare(owner, generation, candidate.person).get().error == Error::ACCESS_DENIED,
            "Naval bootstrap accepted an Academy candidate");
    denied(owner, generation);
    return candidate;
}

void print_view(SessionOwner& owner, Generation generation)
{
    const auto view = view_of(owner, generation);
    // The generation is opaque application data. Compare its ABI representation
    // across processes to ensure the test also detects a restarted counter.
    std::cout << view.campaign_id << '\n' << std::bit_cast<std::uint64_t>(generation) << '\n'
              << view.history_generation << ' ' << view.history_segments << '\n'
              << view.person << ' ' << view.creation_fact << ' ' << view.revision << ' ' << view.tick << ' '
              << view.clock << ' ' << view.person_count << ' ' << view.creation_fact_count << ' ' << view.population_count << '\n'
              << std::quoted(view.display_name) << '\n' << view.source_digest << '\n'
              << view.catalog_digest << '\n' << view.checkpoint_digest << '\n';
    for (const auto& fact : view.background) std::cout << fact << '\n';
}

void write(const StorageConfig& config)
{
    SessionOwner owner(config);
    const auto created = create(owner);
    const auto before = view_of(owner, created.generation);
    expect(owner.save(created.generation, "../alpha").get(), Error::PATH_REJECTED);
    expect(owner.save(created.generation, "alpha").get(), Error::OK);
    require(view_of(owner, created.generation).checkpoint_digest == before.checkpoint_digest, "SAVE changed the live Core");
    print_view(owner, created.generation);
    expect(owner.close().get(), Error::OK);
}

void read(const StorageConfig& config, const SlotAddress& address, Generation old, bool resave)
{
    SessionOwner owner(config);
    expect(owner.restore(old, address).get(), Error::GENERATION_EXPIRED);
    const auto loaded = owner.restore({}, address).get();
    expect(loaded, Error::OK);
    const auto generation = loaded.generation;
    require(generation != old && owner.current_player(old).error == Error::GENERATION_EXPIRED &&
                owner.campaign_provenance(generation) == Provenance::KNOWN_LOCAL, "Restored an old generation or profile");
    expect(owner.restore(generation, address).get(), Error::BUSY_STATE);
    require(!AcademyCandidateFactory::begin(owner), "RESTORE enabled a second B02 creation");
    if (resave) expect(owner.save(generation, "alpha").get(), Error::OK);
    print_view(owner, generation);
    expect(owner.close().get(), Error::OK);
    require(owner.current_player(generation).error == Error::GENERATION_EXPIRED, "Closed projection still authorized");
}

void naval(const StorageConfig& config)
{
    SessionOwner owner(config);
    const auto generation = open(owner);
    const auto selection = PlayerBootstrap::prepare(owner, generation, 4).get();
    require(selection.error == Error::OK && selection.selection, "Prepare naval player");
    require(PlayerBootstrap::bind(owner, generation, *selection.selection, selection.revision).get().error == Error::OK,
            "Bind naval player");
    expect(owner.save(generation, "alpha").get(), Error::OK);
    std::cout << owner.campaign_id(generation) << '\n';
    expect(owner.close().get(), Error::OK);
}

void mixed(const StorageConfig& config, const std::string& academy_id, const std::string& naval_id)
{
    SessionOwner owner(config);
    SlotAddress academy{academy_id, "alpha", 0, CampaignKind::ACADEMY};
    SlotAddress ship{naval_id, "alpha", 0, CampaignKind::NAVAL};
    auto wrong = academy;
    wrong.kind = CampaignKind::NAVAL;
    expect(owner.restore({}, wrong).get(), Error::SAVE_INCOMPATIBLE);
    closed(owner);
    wrong = ship;
    wrong.kind = CampaignKind::ACADEMY;
    expect(owner.restore({}, wrong).get(), Error::SAVE_INCOMPATIBLE);
    closed(owner);
    const auto loaded = owner.restore({}, ship).get();
    expect(loaded, Error::OK);
    require(owner.query_view(loaded.generation).get().error == Error::OK, "Naval v1 gateway regression");
    expect(owner.restore(loaded.generation, academy).get(), Error::BUSY_STATE);
    academy.kind = CampaignKind::AUTO;
    expect(owner.restore(loaded.generation, academy).get(), Error::SAVE_INCOMPATIBLE);
    require(owner.query_view(loaded.generation).get().error == Error::OK, "Failed LOAD replaced active naval session");
    expect(owner.close().get(), Error::OK);
    expect(owner.restore({}, academy).get(), Error::OK);
}

void reject(const StorageConfig& config, const SlotAddress& address, std::string_view reason)
{
    const auto expected = reason == "incompatible" ? Error::SAVE_INCOMPATIBLE :
                          reason == "untrusted" ? Error::SAVE_UNTRUSTED :
                          reason == "path" ? Error::PATH_REJECTED :
                          reason == "identity" ? Error::IDENTITY_MISMATCH : Error::SAVE_CORRUPT;
    SessionOwner owner(config);
    expect(owner.restore({}, address).get(), expected);
    closed(owner);
    const auto slots = SessionOwner::inspect(config);
    require(slots.error == Error::OK, "Inspection could not enumerate rejected slot");
    bool seen = false;
    for (const auto& slot : slots.slots) {
        if (slot.address.campaign != address.campaign || slot.address.slot != address.slot ||
            (address.version && slot.address.version != address.version) || slot.reason != expected) continue;
        require(!slot.recoverable && slot.provenance ==
                    (expected == Error::SAVE_UNTRUSTED ? Provenance::IMPORTED_UNVERIFIED : Provenance::REJECTED),
                "Inspection incorrectly authorized rejected slot");
        seen = true;
    }
    require(seen, "Expected error or slot was missing from inspection");
}

void inspect(const StorageConfig& config, const std::string& academy_id, const std::string& naval_id)
{
    const auto found = SessionOwner::inspect(config);
    require(found.error == Error::OK, "Mixed root inspection failed");
    bool academy = false, ship = false;
    for (const auto& slot : found.slots) {
        require(slot.compatible && slot.recoverable && slot.provenance == Provenance::KNOWN_LOCAL,
                "Local valid slot was rejected");
        if (slot.address.campaign == academy_id)
            academy |= slot.address.kind == CampaignKind::ACADEMY && slot.format == 2;
        if (slot.address.campaign == naval_id)
            ship |= slot.address.kind == CampaignKind::NAVAL && slot.format == 1;
    }
    require(academy && ship, "Inspection failed to distinguish formats");
}

void rebind(const StorageConfig& config)
{
    SessionOwner owner(config);
    const auto created = create(owner);
    const auto campaign = owner.campaign_id(created.generation);
    expect(owner.save(created.generation, "alpha").get(), Error::OK);
    expect(owner.close().get(), Error::OK);
    const auto loaded = owner.restore({}, {campaign, "alpha"}).get();
    expect(loaded, Error::OK);
    expect(AcademyPlayerBinding::bind(owner, created.generation, created.receipt).get(), Error::GENERATION_EXPIRED);
    expect(AcademyPlayerBinding::bind(owner, loaded.generation, created.receipt).get(), Error::SCOPE_INVALID);
    require(AcademyCandidateFactory::inspect(owner, created.receipt).get().error == Error::SCOPE_INVALID,
            "Recovered campaign reused B02 receipt");
    (void)view_of(owner, loaded.generation);
}

#ifdef TREK_HOST_ACADEMY_TESTING
void interrupted(const StorageConfig& config, const SlotAddress& address, std::string_view point)
{
    SessionOwner owner(config);
    const auto loaded = owner.restore({}, address).get();
    expect(loaded, Error::OK);
    const auto before = view_of(owner, loaded.generation);
    storage_test_hook([&](const char* name) {
        if (point == "crash" && std::string_view(name) == "before_publish") std::_Exit(73);
        if (name == point) throw std::runtime_error("Injected H04 interruption");
    });
    const auto result = owner.save(loaded.generation, "alpha").get();
    storage_test_hook({});
    const auto uncertain = point == "after_publish" || point == "before_ack";
    expect(result, uncertain ? Error::PUBLICATION_UNCERTAIN : Error::PERSISTENCE_FAILED);
    require(view_of(owner, loaded.generation).checkpoint_digest == before.checkpoint_digest,
            "Interrupted SAVE modified the live state");
    expect(owner.close().get(), Error::OK);
}

void close_during_restore(const StorageConfig& config, const SlotAddress& address)
{
    using namespace std::chrono_literals;
    std::binary_semaphore staged(0), resume(0);
    SessionOwner owner(config);
    storage_test_hook([&](const char* name) {
        if (std::string_view(name) == "after_copy") {
            staged.release();
            resume.acquire();
        }
    });
    auto pending = owner.restore({}, address);
    const auto paused = staged.try_acquire_for(10s);
    const auto stopping = owner.close();
    resume.release();
    const auto result = pending.get();
    expect(stopping.get(), Error::OK);
    storage_test_hook({});
    require(paused, "Could not pause restore in staging");
    expect(result, Error::GENERATION_EXPIRED);
    closed(owner);
    const auto next = owner.restore({}, address).get();
    expect(next, Error::OK);
    (void)view_of(owner, next.generation);
}
#endif
}

int main(int argc, char** argv)
try {
    if (argc < 3) return 2;
    const std::string_view mode = argv[1];
    const auto config = storage(fs::path(argv[2]));
    if (mode == "write") write(config);
    else if (mode == "naval") naval(config);
    else if (mode == "rebind") rebind(config);
    else {
        if (argc < 5) return 2;
        if (mode == "mixed") mixed(config, argv[3], argv[4]);
        else if (mode == "inspect") inspect(config, argv[3], argv[4]);
        else {
            SlotAddress address{argv[3], argv[4], 0, CampaignKind::ACADEMY};
            if (mode == "close") {
#ifdef TREK_HOST_ACADEMY_TESTING
                close_during_restore(config, address);
#else
                return 2;
#endif
            } else {
                if (argc != 7) return 2;
                address.version = std::stoull(argv[5]);
                if (mode == "resume" || mode == "read")
                    read(config, address, std::bit_cast<Generation>(std::uint64_t(std::stoull(argv[6]))), mode == "resume");
                else if (mode == "reject") reject(config, address, argv[6]);
#ifdef TREK_HOST_ACADEMY_TESTING
                else if (mode == "fault") interrupted(config, address, argv[6]);
                else {
                    const auto prepared = SlotStore(config).prepare(address);
                    auto candidate = AcademyCampaign::restore(prepared);
                    AcademyPersistenceTest::mutate(*candidate, fs::absolute(argv[6]), mode);
                }
#else
                else return 2;
#endif
            }
        }
    }
    return 0;
} catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
}
#ifdef TREK_HOST_ACADEMY_TESTING
catch (const StorageFailure& error) {
    std::cerr << "Storage error " << static_cast<int>(error.error) << '\n';
    return 1;
}
#endif
