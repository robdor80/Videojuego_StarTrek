#include "academy_campaign.h"
#include "fixed_candidate_data.h"
#include "../slot_store.h"

#include <jsoncons/json.hpp>
#include <jsoncons/json_cursor.hpp>
#include <jsoncons/utility/unicode_traits.hpp>

#include <algorithm>
#ifdef TREK_HOST_ACADEMY_TESTING
#include <atomic>
#endif
#include <stdexcept>
#include <utility>

namespace trek::host::detail {
namespace {
using namespace corerpg;
using namespace std::string_view_literals;
using Json = jsoncons::json;

constexpr auto pack = "startrek.academy"sv;
constexpr auto catalog_root = "startrek.academy:starfleet_academy/v2"sv;
constexpr auto definition_prefix = "startrek.academy:starfleet_academy/v2/"sv;
constexpr auto policy_hash = "df7f7a564cb1cb8dd989b5e70672db8d14ac0e7f9e8587c8d5a49afd3769a27b"sv;
constexpr auto source_path =
    "source/s04_fixed_player_protagonist/2.0.0/s04_player_khan_vulcan_male/1.0.0/"sv;

constexpr RelationKind candidate_for{1}, subject{2}, source{3}, background{4},
    species{5}, mother_species{6}, father_species{7}, paternal_ancestor{8};
constexpr std::uint64_t field_shift = 48;
constexpr std::uint64_t field_mask = (UINT64_C(1) << field_shift) - 1;
constexpr std::uint64_t campaign_field = UINT64_C(1) << field_shift;
constexpr std::uint64_t name_field = UINT64_C(2) << field_shift;
constexpr std::uint64_t tick_field = UINT64_C(3) << field_shift;
constexpr std::size_t name_limit = 96;

#ifdef TREK_HOST_ACADEMY_TESTING
std::atomic<AcademyFault> test_fault{AcademyFault::NONE};
#endif

void require(bool ok)
{
    if (!ok) throw std::logic_error("Inconsistent F10 Academy campaign");
}

void require_source(bool ok)
{
    if (!ok) throw UnapprovedAcademySource{};
}

std::string hex(const HistoryHash& hash)
{
    constexpr std::string_view digits = "0123456789abcdef";
    std::string output;
    output.reserve(hash.size() * 2);
    for (auto byte : hash) {
        output.push_back(digits[byte >> 4]);
        output.push_back(digits[byte & 15]);
    }
    return output;
}

struct CanonicalProfile {
    std::string digest;
    std::string species, mother_species, father_species, ancestor;
    std::vector<std::string> facts;
};

std::string code(const Json& input)
{
    if (input.is_bool()) return input.as<bool>() ? "true" : "false";
    auto value = input.is_number() ? std::to_string(input.as<int>()) : input.as<std::string>();
    std::ranges::transform(value, value.begin(), [](unsigned char ch) -> char {
        return ch >= 'A' && ch <= 'Z' ? static_cast<char>(ch + ('a' - 'A')) : static_cast<char>(ch);
    });
    return value;
}

CanonicalProfile approved_profile()
{
    require_source(hex(academy_digest(fixed_candidate_data::policy)) == policy_hash);
    auto policy = Json::parse(fixed_candidate_data::policy);
    auto contract_bytes = fixed_candidate_data::s04_contract;
    auto biography_bytes = fixed_candidate_data::s04_biography;
#ifdef TREK_HOST_ACADEMY_TESTING
    if (test_fault == AcademyFault::SOURCE_VERSION) policy["source"]["s04_contract"]["version"] = "9.0.0";
    if (test_fault == AcademyFault::SOURCE_DIGEST) policy["source"]["s04_contract"]["sha256"] = std::string(64, '0');
    if (test_fault == AcademyFault::SOURCE_BYTES) biography_bytes.remove_suffix(1);
#endif
    require_source(policy.at("contract_id") == "f10_fixed_candidate_factory" &&
                   policy.at("schema_version") == "2.0.0" && policy.at("owner") == "F10" &&
                   policy.at("catalog") == catalog_root && policy.at("scenario") == "starfleet_academy" &&
                   policy.at("validation").at("mode") == "DETERMINISTIC_AUTHOR_APPROVED_SOURCE");

    const auto contract_hash = hex(academy_digest(contract_bytes));
    const auto biography_hash = hex(academy_digest(biography_bytes));
    const auto& contract_ref = policy.at("source").at("s04_contract");
    const auto& biography_ref = policy.at("source").at("s04_biography");
    require_source(contract_ref.at("sha256") == contract_hash && biography_ref.at("sha256") == biography_hash);
    const auto contract = Json::parse(contract_bytes);
    const auto biography = Json::parse(biography_bytes);
    require_source(contract.at("contract_id") == contract_ref.at("id") &&
                   contract.at("schema_version") == contract_ref.at("version") &&
                   biography.at("profile_id") == biography_ref.at("id") &&
                   biography.at("schema_version") == biography_ref.at("version"));

    const auto& campaign = contract.at("campaign");
    const auto& selection = contract.at("selection");
    const auto& identity = biography.at("identity");
    const auto& parentage = contract.at("parentage");
    const auto& family = biography.at("family");
    const auto& mother = family.at("mother");
    const auto& father = family.at("father");
    const auto& formation = biography.at("formation");
    const auto& education = contract.at("education");
    require_source(campaign.at("start_year") == 2383 && policy.at("start_year") == 2383 &&
                   campaign.at("setting") == "starfleet_academy" &&
                   campaign.at("start_month_day") == "AUTHOR_UNDECIDED" &&
                   biography.at("first_campaign_year") == 2383 &&
                   selection.at("allowed_species_ids").size() == 1 &&
                   selection.at("allowed_species_ids").at(0) == "human_vulcan_hybrid" &&
                   identity.at("species_id") == selection.at("allowed_species_ids").at(0) &&
                   identity.at("sex") == "male" && selection.at("sex") == identity.at("sex") &&
                   identity.at("age_at_admission_earth_years") == 45 &&
                   selection.at("age_at_academy_entry_years") == identity.at("age_at_admission_earth_years") &&
                   mother.at("species") == "vulcan" && father.at("species") == "human" &&
                   father.at("descendant_of") == "khan_noonien_singh" &&
                   parentage.at("mother_species") == mother.at("species") &&
                   parentage.at("father_species") == father.at("species") &&
                   parentage.at("father_direct_descendant_of") == father.at("descendant_of") &&
                   identity.at("birth_exact_date").is_null() && identity.at("place_of_birth").is_null() &&
                   mother.at("name").is_null() && father.at("name").is_null() &&
                   formation.at("university_degrees").is_null() && formation.at("certificates").is_null() &&
                   formation.at("music_instruments").is_null() &&
                   education.at("previous_starfleet_service") == false &&
                   education.at("prior_commission") == false &&
                   formation.at("starfleet_commission") == false && formation.at("starfleet_clearance") == false);

    CanonicalProfile profile{hex(academy_digest(std::string(policy_hash) + contract_hash + biography_hash)),
                             code(identity.at("species_id")), code(mother.at("species")),
                             code(father.at("species")), code(father.at("descendant_of")), {}};
    auto fact = [&](std::string_view field, const Json& value) {
        profile.facts.push_back("background/" + std::string(field) + "/" + code(value));
    };
    fact("sex", identity.at("sex"));
    fact("academy_entry_age_earth_years", identity.at("age_at_admission_earth_years"));
    fact("application_year", campaign.at("start_year"));
    fact("approximate_birth_year", identity.at("birth_year_approx"));
    fact("approximate_apparent_human_age", identity.at("apparent_human_age_years_approx"));
    fact("maternal_mentorship", mother.at("role"));
    fact("family_culture", parentage.at("culture"));
    fact("fictional_inherited_expression", family.at("gene_expression").at("type"));
    fact("slow_aging", contract.at("biology").at("slow_aging"));
    fact("vulcan_mental_discipline", contract.at("training").at("vulcan_mental_discipline"));
    const auto& application = contract.at("admission");
    fact("declares_khan_lineage", application.at("declares_khan_lineage"));
    fact("declares_exceptional_traits", application.at("declares_exceptional_traits"));
    fact("requests_merit_assessment", application.at("requests_merit_based_assessment"));
    const auto& traits = biography.at("capability_seeds");
    for (auto field : {"strength", "reflexes", "resilience", "emotional_mastery", "anger", "musical_practice"})
        fact(field, traits.at(field));
    const auto& arts = contract.at("training").at("martial_mastery");
    require_source(arts.size() == 4 && traits.at("martial_skills").size() == arts.size());
    for (std::size_t i = 0; i < arts.size(); ++i) {
        const auto art = code(arts.at(i));
        require_source(code(traits.at("martial_skills").at(i)) == art + "_master");
        fact("martial_mastery", arts.at(i));
    }
    fact("vocation", education.at("primary_vocation"));
    for (const auto& interest : education.at("strong_interest").array_range()) fact("interest", interest);
    for (const auto& interest : education.at("artistic_interests").array_range()) fact("interest", interest);
    for (const auto& stage : biography.at("life_stages").array_range()) fact("life_stage", stage.at("stage"));
    profile.facts.emplace_back("background/prior_career/civilian");
    profile.facts.emplace_back("background/prior_starfleet_service/absent");
    return profile;
}

std::string id(std::string_view path)
{
    return std::string(definition_prefix) + std::string(path);
}

ContentCatalog make_catalog(const CanonicalProfile& profile)
{
    const auto pack_version = SemanticVersion::parse("2.0.0").value();
    const auto core_content_version = SemanticVersion::parse("0.1.0").value();
    std::vector<ContentDefinitionInput> definitions;
    auto define = [&](std::string_view path, std::string_view kind) {
        auto definition = DefinitionId::parse(id(path));
        auto resource = ResourceKind::parse(kind);
        require(definition && resource);
        definitions.emplace_back(ResourceDefinition{std::move(*definition), std::move(*resource)});
    };
    define("campus", "campus");
    define("person", "person");
    define("candidate_created", "event");
    define(std::string(source_path) + profile.digest, "source");
    for (const auto* value : {&profile.species, &profile.mother_species, &profile.father_species})
        define("species/" + *value, "species");
    define("ancestry/" + profile.ancestor, "historical_reference");
    for (const auto& fact : profile.facts) define(fact, "biographical_fact");
    auto result = ContentCatalog::create({ContentPackInput{
        ContentManifest{*PackId::parse(pack), pack_version, core_content_version, core_content_version}, std::move(definitions)}});
    require(result.succeeded());
    return *result.catalog();
}

std::string catalog_digest(const ContentCatalog& catalog)
{
    auto inventory = std::string(academy_catalog_version) + "\nCore schema 0.1.0\n";
    for (const auto& definition : catalog.definitions()) {
        inventory.append(definition.id().value()).append(" ").append(definition.kind().value()).append("\n");
    }
    return academy_digest_hex(inventory);
}

bool canonical_background(std::vector<std::string> actual, const CanonicalProfile& profile)
{
    auto expected = profile.facts;
    expected.emplace_back("species/" + profile.species);
    expected.emplace_back("mother/species/" + profile.mother_species);
    expected.emplace_back("father/species/" + profile.father_species);
    expected.emplace_back("paternal/ancestry/" + profile.ancestor);
    std::ranges::sort(actual);
    std::ranges::sort(expected);
    return actual == expected;
}

Error history_error(HistoryStatus result, Error otherwise)
{
    switch (result) {
    case HistoryStatus::success: return Error::OK;
    case HistoryStatus::unsupported_version: return Error::SAVE_INCOMPATIBLE;
    case HistoryStatus::limit_exceeded: return Error::CAPACITY_LIMIT;
    default: return otherwise;
    }
}

void link(WorldState& world, EntityId from, RelationKind kind, EntityId to)
{
    require(world.add_relation({from, kind, to}) == RelationChange::applied);
}

// The Core pin persists typed relations and definition bindings. These two
// bounded UTF-8 fields use ordered bytes, scoped to the v2 catalog.
void write_text(WorldState& world, EntityId entity, std::uint64_t field, std::string_view text)
{
    for (std::size_t i = 0; i < text.size(); ++i) {
        const auto byte = static_cast<unsigned char>(text[i]);
        link(world, entity, RelationKind{field | (static_cast<std::uint64_t>(i) << 8) | byte}, entity);
    }
}

std::string read_text(const WorldState& world, EntityId entity, std::uint64_t field, std::size_t limit)
{
    std::string value;
    for (const auto& relation : world.relations_from(entity)) {
        const auto kind = relation.kind.value();
        if ((kind & ~field_mask) != field) continue;
        require(relation.target == entity && ((kind & field_mask) >> 8) == value.size() && value.size() < limit);
        value.push_back(static_cast<char>(kind & 0xff));
    }
    require(!value.empty());
    return value;
}

bool forbidden_name_char(char32_t ch)
{
    return ch < 0x20 || (ch >= 0x7f && ch <= 0x9f) || ch == 0xad || ch == 0x61c ||
           ch == 0x180e || (ch >= 0x200b && ch <= 0x200f) || (ch >= 0x2028 && ch <= 0x202e) ||
           (ch >= 0x2060 && ch <= 0x206f) || ch == 0xfeff || ch == 0xfffe || ch == 0xffff;
}

bool name_space(char32_t ch)
{
    return ch == 0x20 || ch == 0xa0 || ch == 0x1680 || (ch >= 0x2000 && ch <= 0x200a) ||
           ch == 0x202f || ch == 0x205f || ch == 0x3000;
}

bool valid_name(std::string_view name)
{
    if (name.empty() || name.size() > name_limit) return false;
    std::u32string codepoints;
    const auto result = jsoncons::unicode_traits::convert(name.data(), name.size(), codepoints);
    return result.ec == jsoncons::unicode_traits::unicode_errc{} && !codepoints.empty() &&
           !name_space(codepoints.front()) && !name_space(codepoints.back()) &&
           std::ranges::none_of(codepoints, forbidden_name_char);
}
} // namespace

#ifdef TREK_HOST_ACADEMY_TESTING
void set_academy_fault(AcademyFault fault) noexcept { test_fault.store(fault); }
void academy_fail_at(AcademyFault fault)
{
    if (test_fault == fault) throw std::runtime_error("Injected failure staging F10 Academy campaign");
}
#endif

std::optional<std::string> academy_display_name(std::string_view payload)
{
    using Event = jsoncons::staj_event_type;
    if (payload.empty() || payload.size() > academy_payload_limit) return std::nullopt;
    try {
        jsoncons::json_options options;
        options.allow_comments(false).max_nesting_depth(2);
        jsoncons::json_string_cursor cursor(payload, options);
        if (cursor.current().event_type() != Event::begin_object) return std::nullopt;
        cursor.next();
        if (cursor.current().event_type() != Event::key || cursor.current().get<std::string_view>() != "display_name")
            return std::nullopt;
        cursor.next();
        if (cursor.current().event_type() != Event::string_value) return std::nullopt;
        auto name = cursor.current().get<std::string>();
        cursor.next();
        if (cursor.current().event_type() != Event::end_object) return std::nullopt;
        cursor.next();
        cursor.check_done();
        if (cursor.done() && valid_name(name)) return name;
    } catch (const jsoncons::ser_error&) {
        return std::nullopt;
    }
    return std::nullopt;
}

HistoryHash academy_digest(std::string_view bytes)
{
    return HistoryPersistence::hash({reinterpret_cast<const std::uint8_t*>(bytes.data()), bytes.size()});
}

std::string academy_digest_hex(std::string_view bytes)
{
    return hex(academy_digest(bytes));
}

AcademySnapshotIdentity academy_identity(const AcademyCandidateView& view, std::string profile)
{
    return {{view.person, view.creation_fact, std::move(profile), view.source_digest, view.catalog_digest,
             academy_digest_hex(view.display_name)}, view.revision, view.clock};
}

AcademyCampaign::AcademyCampaign(ContentCatalog catalog, std::uint64_t seed)
    : catalog_(std::move(catalog)), catalog_digest_(catalog_digest(catalog_)), random_(seed) {}

EntityId AcademyCampaign::create_entity(std::string_view definition)
{
    const auto* resource = catalog_.find_by_value(id(definition));
    require(resource != nullptr);
    const auto entity = world_.create_entity();
    require(entity.is_valid() &&
            world_.bind_definition(entity, catalog_, resource->id()) == DefinitionBindingChange::applied);
    return entity;
}

std::unique_ptr<AcademyCampaign> AcademyCampaign::stage(std::string_view campaign, std::string_view name)
{
    const auto profile = approved_profile();
    auto seed = UINT64_C(0);
    const auto hash = academy_digest(campaign);
    for (std::size_t i = 0; i < sizeof(seed); ++i) seed = (seed << 8) | hash[i];
    auto staged = std::unique_ptr<AcademyCampaign>(new AcademyCampaign(make_catalog(profile), seed));
#ifdef TREK_HOST_ACADEMY_TESTING
    academy_fail_at(AcademyFault::CATALOG);
#endif
    auto& world = staged->world_;
    const auto campus = staged->campus_ = staged->create_entity("campus");
    const auto person = staged->person_ = staged->create_entity("person");
    write_text(world, person, name_field, name);
#ifdef TREK_HOST_ACADEMY_TESTING
    academy_fail_at(AcademyFault::PERSON);
#endif
    const auto event = staged->creation_fact_ = staged->create_entity("candidate_created");
    write_text(world, campus, campaign_field, campaign);
    link(world, person, candidate_for, campus);
    link(world, event, subject, person);
    link(world, event, RelationKind{tick_field | staged->timeline_.now()}, event);
    link(world, event, source, staged->create_entity(std::string(source_path) + profile.digest));
    link(world, person, species, staged->create_entity("species/" + profile.species));
    link(world, person, mother_species, staged->create_entity("species/" + profile.mother_species));
    link(world, person, father_species, staged->create_entity("species/" + profile.father_species));
    link(world, person, paternal_ancestor, staged->create_entity("ancestry/" + profile.ancestor));
    for (const auto& fact : profile.facts) link(world, event, background, staged->create_entity(fact));
#ifdef TREK_HOST_ACADEMY_TESTING
    academy_fail_at(AcademyFault::FACT);
#endif
    const auto checkpoint = CampaignPersistence::capture(world, staged->random_, staged->timeline_);
    require(CampaignPersistence::validate(checkpoint) == CampaignArchiveStatus::success);
#ifdef TREK_HOST_ACADEMY_TESTING
    const auto archive = CampaignPersistence::serialize(checkpoint);
    require(archive.status == CampaignArchiveStatus::success &&
            CampaignPersistence::load(archive.bytes, world, staged->random_, staged->timeline_, {},
                                      &staged->catalog_) == CampaignArchiveStatus::success);
    academy_fail_at(AcademyFault::HISTORY);
#endif
    return staged;
}

Error AcademyCampaign::snapshot(const std::filesystem::path& destination, const HistoryCampaignId& campaign) const
{
    HistoryArchive archive;
    if (!history_pin_) {
        return history_error(HistoryPersistence::migrate(destination, campaign, world_, random_, timeline_, archive),
                             Error::PERSISTENCE_FAILED);
    }

    // Core has no archive export operation. Branch the immutable recovered tree
    // and extend it using the pinned API, preserving its segments and frontier.
    copy_history(history_pin_->path(), destination);
    WorldState checkpoint;
    RandomStreams rng{0};
    Timeline clock;
    const auto recovered = HistoryPersistence::recover(destination, archive, checkpoint, rng, clock, &catalog_);
    if (recovered != HistoryStatus::success) return history_error(recovered, Error::SAVE_CORRUPT);
    if (archive.campaign_id() != campaign) return Error::IDENTITY_MISMATCH;
    return history_error(HistoryPersistence::publish(archive, world_, random_, timeline_), Error::PERSISTENCE_FAILED);
}

std::unique_ptr<AcademyCampaign> AcademyCampaign::restore(const PreparedSlot& slot)
{
    const auto* expected = std::get_if<AcademySnapshotIdentity>(&slot.identity);
    if (!expected) throw StorageFailure{Error::SAVE_INCOMPATIBLE};
    const auto canonical = approved_profile();
    auto restored = std::unique_ptr<AcademyCampaign>(new AcademyCampaign(make_catalog(canonical), 0));
    if (expected->anchor.catalog_digest != restored->catalog_digest_ || expected->anchor.source_digest != canonical.digest)
        throw StorageFailure{Error::SAVE_INCOMPATIBLE};

    auto& archive = restored->history_;
    const auto status = HistoryPersistence::recover(slot.history->path(), archive, restored->world_,
                                                    restored->random_, restored->timeline_, &restored->catalog_);
    if (status != HistoryStatus::success) throw StorageFailure{history_error(status, Error::SAVE_CORRUPT)};
    if (archive.campaign_id() != decode_campaign(slot.campaign)) throw StorageFailure{Error::IDENTITY_MISMATCH};

    // Archived role entities would hide a second candidate or change the meaning
    // of the live anchors. Generic Core facts may remain in older segments.
    for (HistoryPage page; archive.archived_count() != 0;) {
        page = HistoryPersistence::query(archive, page.next, HistoryLimits{}.max_page);
        if (page.status != HistoryStatus::success) throw StorageFailure{history_error(page.status, Error::SAVE_CORRUPT)};
        for (const auto& fact : page.facts) {
            if (fact.definition.empty()) continue;
            const auto* definition = restored->catalog_.find_by_value(fact.definition);
            if (!definition || definition->kind().value() == "person" || definition->kind().value() == "campus" ||
                definition->kind().value() == "event") throw StorageFailure{Error::IDENTITY_MISMATCH};
        }
        if (!page.more) break;
    }

    try {
        for (auto entity : HistoryPersistence::bound_entities(restored->world_)) {
            const auto* definition = restored->world_.definition_of(entity);
            require(definition != nullptr);
            const auto name = definition->value();
            if (name == id("campus")) {
                require(!restored->campus_.is_valid());
                restored->campus_ = entity;
            } else if (name == id("person")) {
                require(!restored->person_.is_valid());
                restored->person_ = entity;
            } else if (name == id("candidate_created")) {
                require(!restored->creation_fact_.is_valid());
                restored->creation_fact_ = entity;
            }
        }
        const auto view = restored->inspect();
        if (view.campaign_id != slot.campaign || view.source_digest != canonical.digest ||
            !canonical_background(view.background, canonical) ||
            academy_identity(view, expected->anchor.profile) != *expected)
            throw StorageFailure{Error::IDENTITY_MISMATCH};
    } catch (const std::logic_error&) {
        throw StorageFailure{Error::IDENTITY_MISMATCH};
    }
    restored->history_pin_ = slot.history;
    return restored;
}

AcademyCandidateView AcademyCampaign::inspect() const
{
    AcademyCandidateView result;
    auto path = [&](EntityId entity) {
        const auto* definition = world_.definition_of(entity);
        require(definition != nullptr && catalog_.contains(*definition) && definition->value().starts_with(definition_prefix));
        return definition->value().substr(definition_prefix.size());
    };
    require(path(campus_) == "campus" && path(person_) == "person" && path(creation_fact_) == "candidate_created" &&
            world_.has_relation({person_, candidate_for, campus_}) &&
            world_.has_relation({creation_fact_, subject, person_}) && !world_.population_origin(person_) &&
            std::ranges::count(world_.relations_from(person_), candidate_for, &EntityRelation::kind) == 1 &&
            std::ranges::count(world_.relations_from(creation_fact_), subject, &EntityRelation::kind) == 1);

    result.campaign_id = read_text(world_, campus_, campaign_field, 32);
    result.display_name = read_text(world_, person_, name_field, name_limit);
    result.person = person_.value();
    result.creation_fact = creation_fact_.value();
    result.revision = world_.revision();
    result.clock = timeline_.now();
    result.catalog_digest = catalog_digest_;
    result.population_count = world_.populations().size();
    for (auto entity : HistoryPersistence::bound_entities(world_)) {
        const auto definition = path(entity);
        result.person_count += definition == "person";
        result.creation_fact_count += definition == "candidate_created";
    }
    bool has_tick = false;
    for (const auto& edge : world_.relations_from(creation_fact_)) {
        if (edge.kind == source) {
            const auto ref = path(edge.target);
            require(result.source_digest.empty() && ref.starts_with(source_path));
            result.source_digest = ref.substr(source_path.size());
        } else if (edge.kind == background) {
            result.background.emplace_back(path(edge.target));
        } else if ((edge.kind.value() & ~field_mask) == tick_field) {
            require(edge.target == creation_fact_ && !has_tick);
            has_tick = true;
            result.tick = edge.kind.value() & field_mask;
        }
    }
    for (const auto& edge : world_.relations_from(person_)) {
        if (edge.kind == species) result.background.emplace_back(path(edge.target));
        if (edge.kind == mother_species) result.background.emplace_back("mother/" + std::string(path(edge.target)));
        if (edge.kind == father_species) result.background.emplace_back("father/" + std::string(path(edge.target)));
        if (edge.kind == paternal_ancestor) result.background.emplace_back("paternal/" + std::string(path(edge.target)));
    }
    require(result.campaign_id.size() == 32 && valid_name(result.display_name) && result.source_digest.size() == 64 &&
            result.person_count == 1 && result.creation_fact_count == 1 && result.population_count == 0 &&
            has_tick && result.tick <= result.clock);
    return result;
}

AcademyCandidateView AcademyCampaign::inspect_checkpoint() const
{
    auto view = inspect();
    const auto serialized = CampaignPersistence::serialize(CampaignPersistence::capture(world_, random_, timeline_));
    require(serialized.status == CampaignArchiveStatus::success);
    view.checkpoint_digest = hex(HistoryPersistence::hash(serialized.bytes));
    view.history_generation = history_.generation();
    view.history_segments = history_.segments().size();
    return view;
}

} // namespace trek::host::detail
