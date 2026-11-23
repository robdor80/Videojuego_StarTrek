#include <corerpg/content_catalog.hpp>
#include <corerpg/history.hpp>

#include <array>
#include <filesystem>
#include <iostream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

namespace {
using namespace corerpg;
using namespace std::string_view_literals;

constexpr auto pack = "startrek.academy"sv;
constexpr auto campus_def = "startrek.academy:starfleet_academy/v1/campus"sv;
constexpr auto cohort_def = "startrek.academy:starfleet_academy/v1/cohort"sv;
constexpr auto person_def = "startrek.academy:starfleet_academy/v1/person"sv;
constexpr auto fact_def = "startrek.academy:starfleet_academy/v1/candidate_created"sv;
constexpr auto biography = "Name: Talia. Civilian studies prior to applying."sv;
constexpr auto fixture_campaign = HistoryCampaignId{0x41, 0x43};
constexpr auto academy_year = RelationKind{(UINT64_C(1) << 48) | 2383};
constexpr auto candidate_of = RelationKind{2};
constexpr auto subject = RelationKind{3};
constexpr auto creation_tick = RelationKind{(UINT64_C(6) << 48) | 31};
constexpr auto length_field = UINT64_C(4) << 48;
constexpr auto byte_field = UINT64_C(5) << 48;
constexpr auto byte_mask = (UINT64_C(1) << 48) - 1;
constexpr auto campus = EntityId{1};
constexpr auto cohort = EntityId{2};
constexpr auto cadet = EntityId{3};
constexpr auto candidate = EntityId{4};
constexpr auto fact = EntityId{5};

void require(bool ok, std::string_view message) {
    if (!ok) throw std::runtime_error(std::string(message));
}

auto catalog(bool academy) {
    const auto v = *SemanticVersion::parse("0.1.0");
    std::vector<ContentDefinitionInput> definitions;
    if (academy) {
        for (auto [id, kind] : std::array{
                 std::pair{campus_def, "campus"sv}, std::pair{cohort_def, "cohort"sv},
                 std::pair{person_def, "person"sv}, std::pair{fact_def, "event"sv}}) {
            definitions.emplace_back(ResourceDefinition{*DefinitionId::parse(id), *ResourceKind::parse(kind)});
        }
    }
    return ContentCatalog::create({ContentPackInput{ContentManifest{*PackId::parse(pack), v, v, v},
                                                    std::move(definitions)}});
}

void bind(WorldState& world, const ContentCatalog& content, EntityId id, std::string_view definition) {
    require(world.bind_definition(id, content, *DefinitionId::parse(definition)) ==
                DefinitionBindingChange::applied, "definition binding");
}

void edge(WorldState& world, EntityId from, RelationKind kind, EntityId to) {
    require(world.add_relation({from, kind, to}) == RelationChange::applied, "relation");
}

void base_campus(WorldState& world, const ContentCatalog& content) {
    require(world.create_entity() == campus && world.create_entity() == cohort, "campus/cohort IDs");
    bind(world, content, campus, campus_def);
    bind(world, content, cohort, cohort_def);
    edge(world, campus, academy_year, campus);
    require(world.place_entity(cohort, campus) == ContainmentChange::applied, "locate cohort in campus");
    require(world.declare_population(cohort, 2) == PopulationChange::applied, "declare cohort");
    const auto result = world.materialize_population(cohort, 1);
    require(result.status == MaterializationStatus::applied && result.first == cadet && result.count == 1,
            "materialize test background cadet");
    bind(world, content, cadet, person_def);
}

// Structural sample for the pin experiment. The text has no review receipt or approval.
void stage_sample(WorldState& world, const ContentCatalog& content) {
    require(world.create_entity() == candidate && world.create_entity() == fact, "subject/fact IDs");
    bind(world, content, candidate, person_def);
    bind(world, content, fact, fact_def);
    edge(world, candidate, candidate_of, campus);
    edge(world, fact, subject, candidate);
    edge(world, fact, creation_tick, fact);
    edge(world, fact, RelationKind{length_field | biography.size()}, fact);
    for (std::size_t i = 0; i < biography.size(); ++i) {
        const auto encoded = (static_cast<std::uint64_t>(i) << 8) |
                             static_cast<unsigned char>(biography[i]);
        edge(world, fact, RelationKind{byte_field | encoded}, fact);
    }
}

void verify_sample(const WorldState& world) {
    require(world.entity_count() == 5 && world.definition_of(candidate) &&
                world.definition_of(candidate)->value() == person_def, "stable PERSON definition/ID");
    require(world.definition_of(fact) && world.definition_of(fact)->value() == fact_def &&
                world.has_relation({fact, subject, candidate}) &&
                world.has_relation({fact, creation_tick, fact}), "creation history");
    require(world.has_relation({campus, academy_year, campus}) &&
                world.has_relation({candidate, candidate_of, campus}), "campus and epoch");
    require(world.population_of(cohort) == PopulationRecord{cohort, 2, 1} &&
                world.population_origin(cadet) == cohort && !world.population_origin(candidate),
            "candidate did not spend a cadet place");
    require(world.has_relation({fact, RelationKind{length_field | biography.size()}, fact}), "text size");
    std::string text;
    for (const auto& relation : world.relations_from(fact)) {
        const auto value = relation.kind.value();
        if ((value & ~byte_mask) != byte_field) continue;
        require(relation.target == fact && ((value & byte_mask) >> 8) == text.size(), "canonical text order");
        text.push_back(static_cast<char>(value & 0xff));
    }
    require(text == biography, "exact restored biography");
}

auto snapshot(const WorldState& world, const RandomStreams& random, const Timeline& time) {
    auto result = CampaignPersistence::serialize(CampaignPersistence::capture(world, random, time));
    require(result.status == CampaignArchiveStatus::success, "serialize Core checkpoint");
    return std::move(result.bytes);
}

void write(const std::filesystem::path& path, const ContentCatalog& content) {
    WorldState live;
    RandomStreams random{42};
    Timeline time;
    HistoryArchive history;
    base_campus(live, content);
    require(time.advance(live, random, 31).status == TimelineStatus::completed, "clock");
    (void)random.stream(7).next();
    const auto before = snapshot(live, random, time);
    const auto exhausted = live.materialize_population(cohort, 2);
    require(exhausted.status == MaterializationStatus::insufficient_latent &&
                snapshot(live, random, time) == before, "over-capacity materialization left state intact");
    require(HistoryPersistence::migrate(path, fixture_campaign, live, random, time, history) ==
                HistoryStatus::success, "initial checkpoint");
    auto staged = live;
    stage_sample(staged, content);
    verify_sample(staged);
    for (auto fault : {HistoryFault::after_checkpoint, HistoryFault::before_manifest, HistoryFault::before_publish}) {
        require(HistoryPersistence::publish(history, staged, random, time, {}, fault) ==
                    HistoryStatus::injected_failure, "pre-publication injection");
        require(history.generation() == 1 && snapshot(live, random, time) == before, "live rollback");
        HistoryArchive reopened;
        WorldState restored;
        RandomStreams restored_rng{0};
        Timeline restored_time;
        require(HistoryPersistence::recover(path, reopened, restored, restored_rng, restored_time, &content) ==
                    HistoryStatus::success, "recover before commit");
        require(reopened.generation() == 1 && snapshot(restored, restored_rng, restored_time) == before,
                "durable rollback restored original entity count, revision, facts, population, RNG and clock");
    }
    require(HistoryPersistence::publish(history, staged, random, time) == HistoryStatus::success &&
                history.generation() == 2, "publish Core history");
    std::cout << "write: capacity rejection and three pre-publication faults preserved generation 1; "
                 "published one structural PERSON and one fact in generation 2\n";
}

void read(const std::filesystem::path& path, const ContentCatalog& content, bool damaged) {
    WorldState live;
    RandomStreams random{50};
    Timeline time;
    HistoryArchive history;
    require(live.create_entity() == campus, "preexisting world");
    const auto before = snapshot(live, random, time);
    if (damaged) {
        require(HistoryPersistence::recover(path, history, live, random, time, &content) ==
                    HistoryStatus::integrity_error, "tampered Core root rejected");
        require(history.generation() == 0 && snapshot(live, random, time) == before,
                "tampered root left destinations intact");
        std::cout << "reject: altered manifest rejected without swapping recovery destinations\n";
        return;
    }
    const auto foreign = catalog(false);
    require(foreign.succeeded(), "empty incompatible catalog");
    require(HistoryPersistence::recover(path, history, live, random, time, foreign.catalog()) ==
                HistoryStatus::invalid_projection, "wrong catalog rejected");
    require(history.generation() == 0 && snapshot(live, random, time) == before, "wrong catalog left destinations intact");

    const auto missing = path / "not-an-archive";
    require(HistoryPersistence::recover(missing, history, live, random, time, &content) != HistoryStatus::success &&
                snapshot(live, random, time) == before, "missing archive left destinations intact");
    require(HistoryPersistence::recover(path, history, live, random, time, &content) ==
                HistoryStatus::success, "recover candidate checkpoint");
    require(history.generation() == 2 && history.campaign_id() == fixture_campaign &&
                history.locate(candidate, live.entity_count()) == HistoryLocation::resident, "history scope and generation");
    verify_sample(live);
    RandomStreams reference{42};
    (void)reference.stream(7).next();
    require(time.now() == 31 && random.master_seed() == 42 &&
                random.stream(7).next() == reference.stream(7).next(), "restored campaign clock and RNG");
    std::cout << "read: PERSON=4, candidate fact=5, cohort=2/1, tick=31 and biography preserved; incompatible archive rejected\n";
}
} // namespace

int main(int argc, char** argv) {
    try {
        require(argc == 3, "usage: academy_core_feasibility write|read|reject archive-path");
        const auto content = catalog(true);
        require(content.succeeded(), "Academy catalog");
        const std::string_view mode = argv[1];
        if (mode == "write") write(argv[2], *content.catalog());
        else if (mode == "read" || mode == "reject") read(argv[2], *content.catalog(), mode == "reject");
        else require(false, "unknown mode");
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
