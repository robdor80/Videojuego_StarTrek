#include "biography_evidence.h"
#include "biography_rules_data.h"

#include <corerpg/history.hpp>
#include <jsoncons/json.hpp>
#include <jsoncons/json_cursor.hpp>

#include <algorithm>
#include <charconv>
#include <chrono>
#include <set>
#include <stdexcept>
#include <utility>

namespace trek::f10 {
namespace {
using Json = jsoncons::json;
using namespace std::string_view_literals;

constexpr auto max_draft_bytes = 65536U;
constexpr auto max_findings = 32U;
constexpr auto ruleset_version = "f10-biography/4"sv;
constexpr std::string_view adult_field = "adult_equivalent_status";
constexpr std::string_view birth_field = "age_or_birth_date";
constexpr std::string_view activities_field = "prior_activities_and_hobbies";
constexpr std::string_view education_field = "prior_education";
constexpr std::string_view experience_field = "prior_experience";
constexpr std::string_view certifications_field = "certifications";
constexpr std::string_view species_field = "species_id";

const Json& rules() {
    static const auto data = Json::parse(detail::biography_rules_json);
    return data;
}

std::string_view text(const Json& value) {
    if (!value.is_string() || value.tag() == jsoncons::semantic_tag::bigdec ||
        value.tag() == jsoncons::semantic_tag::bigint) return {};
    return value.as_string_view();
}

bool contains(const Json& list, std::string_view value) {
    return std::ranges::any_of(list.array_range(), [=](const Json& item) { return text(item) == value; });
}

bool opaque_id(std::string_view value) {
    return !value.empty() && value.size() <= 128 && std::ranges::all_of(value, [](char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') ||
               c == '_' || c == '-' || c == '.' || c == ':';
    });
}

bool nonblank(std::string_view value) {
    return value.find_first_not_of(" \t\r\n") != std::string_view::npos;
}

bool forbidden(std::string_view key) {
    static constexpr std::array extra = {
        "player_profile_id"sv, "nickname"sv, "campaign_refs"sv, "valid"sv, "approved"sv,
        "authorized"sv, "verified"sv, "is_admin"sv, "semantic_review_approved"sv, "objective_valid"sv,
        "objective_gate"sv, "semantic_gate"sv, "review_decision"sv, "internal_provenance"sv,
        "reviewer_identity_and_version"sv, "permission"sv, "permissions"sv, "qualification"sv,
        "qualifications"sv, "skill_points"sv, "attribute_points"sv, "character_level"sv,
        "professional_f11_character_id"sv, "trusted"sv, "source_version_or_world_revision"sv,
        "evidence_decision"sv, "rule_or_fact_source_id"sv, "internal_issuer_identity"sv,
        "draft_sha256"sv, "context_sha256"sv, "security_clearance"sv
    };
    return contains(rules().at("forbidden"), key) || std::ranges::find(extra, key) != extra.end();
}

bool has_authority_field(const Json& value) {
    if (value.is_object()) {
        return std::ranges::any_of(value.object_range(), [](const auto& item) {
            return forbidden(item.key()) || has_authority_field(item.value());
        });
    }
    if (value.is_array()) return std::ranges::any_of(value.array_range(), has_authority_field);
    return false;
}

std::optional<Json> parse_draft(std::string_view draft) {
    if (draft.empty() || draft.size() > max_draft_bytes) return std::nullopt;
    try {
        jsoncons::json_options options;
        options.max_nesting_depth(12).lossless_number(true).allow_comments(false);
        jsoncons::json_string_cursor cursor(draft, options);
        std::vector<std::set<std::string>> keys;
        while (!cursor.done()) {
            const auto& event = cursor.current();
            switch (event.event_type()) {
            case jsoncons::staj_event_type::begin_object:
                keys.emplace_back();
                break;
            case jsoncons::staj_event_type::key:
                if (!keys.back().insert(event.get<std::string>()).second) return std::nullopt;
                break;
            case jsoncons::staj_event_type::end_object:
                keys.pop_back();
                break;
            default:
                break;
            }
            cursor.next();
        }
        const auto parsed = Json::parse(draft, options);
        if (parsed.is_object()) return parsed;
    } catch (const jsoncons::ser_error&) {
        return std::nullopt;
    }
    return std::nullopt;
}

std::string canonical(const Json& value) {
    // jsoncons::json sorts object keys. Preserve decimal lexemes rather than
    // round through double when binding the exact submitted content.
    jsoncons::json_options options;
    options.bignum_format(jsoncons::bignum_format_kind::raw);
    std::string bytes;
    value.dump(bytes, options);
    return bytes;
}

Digest digest(std::string_view bytes) {
    // Reuse the pinned SHA-256 implementation as a pure byte function.
    return corerpg::HistoryPersistence::hash(
        {reinterpret_cast<const std::uint8_t*>(bytes.data()), bytes.size()});
}

Digest context_digest(const BiographyContext& context) {
    Json data(jsoncons::json_object_arg);
    data["scenario"] = context.scenario;
    data["era"] = context.era;
    data["year"] = context.start_year;
    data["date"] = context.start_date;
    data["campaign"] = context.campaign;
    data["generation"] = context.generation;
    data["profile"] = context.profile;
    return digest(canonical(data));
}

bool valid_context(const BiographyContext& context) {
    const auto& approved = rules().at("scenario");
    return context.scenario == text(approved.at("scenario_id")) &&
           context.era == text(approved.at("era_id")) &&
           context.start_year == approved.at("approved_start_year").as<int>() &&
           context.start_date.empty() && opaque_id(context.campaign) && context.generation != 0 &&
           opaque_id(context.profile);
}

const std::string& ruleset_identity() {
    static const std::string identity = std::string(ruleset_version) + ":" +
        std::string(text(rules().at("maturity_policy"))) + ":" + std::string(text(rules().at("sources_sha256")));
    return identity;
}

const std::string& review_policy() {
    static const std::string identity = std::string(text(rules().at("policy"))) + ":" +
        std::string(text(rules().at("evidence_policy")));
    return identity;
}

ReviewBinding bind_review(std::string_view canonical_draft, const BiographyContext& context) {
    return {digest(canonical_draft), context_digest(context), ruleset_identity(), review_policy()};
}

std::optional<int> date_year(std::string_view value) {
    if (value.size() != 10 || value[4] != '-' || value[7] != '-') return std::nullopt;
    const auto number = [](std::string_view part) {
        if (!std::ranges::all_of(part, [](char c) { return c >= '0' && c <= '9'; })) return 0;
        int result{};
        std::from_chars(part.data(), part.data() + part.size(), result);
        return result;
    };
    const auto year = number(value.substr(0, 4));
    const auto month = number(value.substr(5, 2));
    const auto day = number(value.substr(8, 2));
    const std::chrono::year_month_day date{std::chrono::year(year), std::chrono::month(month), std::chrono::day(day)};
    if (year > 0 && date.ok()) return year;
    return std::nullopt;
}

bool exact_integer(const Json& value) {
    using T = jsoncons::json_type;
    return value.type() == T::int64 || value.type() == T::uint64;
}

bool content_value(const Json& value) {
    if (value.is_string()) return nonblank(text(value));
    return (value.is_array() || value.is_object()) && !value.empty();
}

std::string_view static_field(std::string_view field) {
    for (const auto key : {"required", "optional"}) {
        for (const auto& value : rules().at(key).array_range()) {
            if (text(value) == field) return text(value);
        }
    }
    return {};
}

struct Checks {
    std::vector<BiographyIssue> errors;
    std::vector<BiographyIssue> pending;
    bool personal_background_plausible{};

    void reject(IssueCode rule, std::string_view field) { add(errors, {rule, field}); }
    void defer(IssueCode rule, std::string_view field) { add(pending, {rule, field}); }

private:
    static void add(std::vector<BiographyIssue>& issues, BiographyIssue issue) {
        if (std::ranges::find(issues, issue) == issues.end()) issues.push_back(issue);
    }
};

void check_evidence_ref(const Json& value, std::string_view field, Checks& checks) {
    if (value.is_object() && value.contains("evidence_ref") &&
        !opaque_id(text(value.at("evidence_ref")))) {
        checks.reject(IssueCode::MALFORMED_FIELD, field);
    }
}

struct BiographicalAge {
    const Json* age{};
    std::string_view birthday;
    std::optional<int> birth_year;
};

BiographicalAge validate_birth(const Json& draft, const BiographyContext& context, Checks& checks) {
    if (!draft.contains(birth_field)) return {};
    const auto& value = draft.at(birth_field);
    if (exact_integer(value) && value.is_uint64()) {
        // No upper lifespan is implied by the supported birth-date format.
        if (value.as<std::uint64_t>() >= static_cast<std::uint64_t>(context.start_year)) {
            checks.defer(IssueCode::AGE_OUTSIDE_CALENDAR, birth_field);
        }
        return {&value, {}, {}};
    }
    const auto birthday = text(value);
    const auto year = date_year(birthday);
    if (!year) {
        checks.reject(IssueCode::UNSUPPORTED_BIRTH_VALUE, birth_field);
        return {};
    }
    if (*year > context.start_year) checks.reject(IssueCode::BIRTH_AFTER_CAMPAIGN_YEAR, birth_field);
    if (*year == context.start_year) checks.defer(IssueCode::CONTEXT_NOT_DECIDED, birth_field);
    return {nullptr, birthday, year};
}

void validate_playable_maturity(const Json& draft, const BiographicalAge& age,
                                const BiographyContext& context, Checks& checks) {
    if (!draft.contains(species_field)) return;
    const auto id = text(draft.at(species_field));
    const auto& species = rules().at("species");
    if (!species.contains(id)) {
        checks.reject(IssueCode::UNKNOWN_SPECIES, species_field);
        return;
    }

    const auto& rule = species.at(id);
    if (rule.at("delta_dlc").as<bool>()) checks.reject(IssueCode::DLC_DELTA_UNAVAILABLE, species_field);
    const auto& minimum = rule.at("minimum");
    if (minimum.is_null()) {
        checks.defer(IssueCode::SPECIAL_MATURITY_RULE_REQUIRED, species_field);
        return;
    }

    const auto floor = minimum.as<int>();
    if (age.age && age.age->as<std::uint64_t>() < static_cast<std::uint64_t>(floor)) {
        checks.reject(IssueCode::BELOW_PLAYABLE_AGE, birth_field);
    } else if (age.birth_year && *age.birth_year <= context.start_year) {
        // Under the approved year-only policy, the whole threshold year needs review.
        const auto age_reached_in_campaign_year = context.start_year - *age.birth_year;
        if (age_reached_in_campaign_year < floor) checks.reject(IssueCode::BELOW_PLAYABLE_AGE, birth_field);
        if (age_reached_in_campaign_year == floor) checks.defer(IssueCode::PLAYABLE_AGE_UNDECIDED, birth_field);
    }
    checks.defer(IssueCode::MATURITY_EVIDENCE_REQUIRED, adult_field);
}

struct Moment {
    std::optional<std::uint64_t> age;
    std::string_view date;
    std::optional<int> year;
};

struct ActivityPeriod {
    Moment start;
    Moment end;
    bool ongoing;
};

Moment validate_moment(const Json& entry, std::string_view key, bool end, const BiographicalAge& age,
                       const BiographyContext& context, std::string_view field, Checks& checks) {
    if (!entry.contains(key)) return {};
    const auto& value = entry.at(key);
    const auto contradiction = field == activities_field ? IssueCode::PRIOR_ACTIVITY_AGE_CONFLICT :
                                                           IssueCode::CHRONOLOGY_CONFLICT;
    if (exact_integer(value) && value.is_uint64()) {
        const auto years = value.as<std::uint64_t>();
        if ((age.age && years > age.age->as<std::uint64_t>()) ||
            (age.birth_year && *age.birth_year <= context.start_year &&
             years > static_cast<std::uint64_t>(context.start_year - *age.birth_year))) {
            checks.reject(contradiction, field);
        } else if (age.birth_year && *age.birth_year <= context.start_year &&
                   years == static_cast<std::uint64_t>(context.start_year - *age.birth_year)) {
            checks.defer(IssueCode::CONTEXT_NOT_DECIDED, field);
        }
        return {years, {}, {}};
    }
    const auto date = text(value);
    if (end && date == "current") return {};
    const auto year = date_year(date);
    if (year) {
        if (*year > context.start_year || (!age.birthday.empty() && date < age.birthday)) {
            checks.reject(contradiction, field);
        } else if (*year == context.start_year) {
            checks.defer(IssueCode::CONTEXT_NOT_DECIDED, field);
        }
        return {{}, date, year};
    }
    const bool looks_like_date = date.size() == 10 && date[4] == '-' && date[7] == '-';
    if (exact_integer(value)) checks.reject(contradiction, field);
    else if (looks_like_date || !nonblank(date)) checks.reject(IssueCode::MALFORMED_FIELD, field);
    // Other nonempty text may describe a time without specifying a machine-readable date.
    return {};
}

void validate_technology(const Json& entry, const Moment& start, std::string_view field, Checks& checks) {
    if (!entry.contains("technology_ref") && !entry.contains("technology_profile_ref")) return;
    if (!entry.contains("technology_ref") || !opaque_id(text(entry.at("technology_ref"))) ||
        (entry.contains("technology_profile_ref") && !opaque_id(text(entry.at("technology_profile_ref"))))) {
        checks.reject(IssueCode::MALFORMED_FIELD, field);
        return;
    }
    const auto capability = text(entry.at("technology_ref"));
    const auto profile_id = entry.contains("technology_profile_ref") ?
        text(entry.at("technology_profile_ref")) : std::string_view{};
    const auto& profiles = rules().at("technology").array_range();
    if (!std::ranges::any_of(profiles, [=](const Json& p) { return p.at("capabilities").contains(capability); })) {
        checks.defer(IssueCode::UNKNOWN_TECHNOLOGY, field);
        return;
    }
    // The matrix describes Starfleet shipboard capability. Only apply a
    // negative rule to an explicit claim in its own profile and date range.
    for (const auto& profile : profiles) {
        if (text(profile.at("id")) != profile_id || !start.year) continue;
        const auto& years = profile.at("year_range");
        if (*start.year < years.at(0).as<int>() || *start.year > years.at(1).as<int>()) {
            checks.defer(IssueCode::TECH_AVAILABILITY_REVIEW, field);
            return;
        }
        const auto& capabilities = profile.at("capabilities");
        if (capabilities.contains(capability) && text(capabilities.at(capability)) == "unavailable" &&
            !entry.contains("evidence_ref")) {
            checks.reject(IssueCode::TECH_UNAVAILABLE, field);
            return;
        }
    }
    checks.defer(IssueCode::TECH_AVAILABILITY_REVIEW, field);
}

std::optional<ActivityPeriod> validate_entry(const Json& entry, const BiographicalAge& age,
                                             const BiographyContext& context, std::string_view field, Checks& checks) {
    if (!entry.is_object()) {
        if (!nonblank(text(entry))) checks.reject(IssueCode::MALFORMED_FIELD, field);
        return std::nullopt;
    }
    if (entry.empty()) checks.reject(IssueCode::MALFORMED_FIELD, field);
    check_evidence_ref(entry, field, checks);
    if (field == activities_field && entry.contains("category") &&
        !contains(rules().at("activity_categories"), text(entry.at("category")))) {
        checks.reject(IssueCode::MALFORMED_FIELD, field);
    }
    const auto start = validate_moment(entry, "started_at_or_age", false, age, context, field, checks);
    const auto end = validate_moment(entry, "ended_at_or_current", true, age, context, field, checks);
    if ((start.age && end.age && *start.age > *end.age) ||
        (!start.date.empty() && !end.date.empty() && start.date > end.date)) {
        checks.reject(field == activities_field ? IssueCode::PRIOR_ACTIVITY_AGE_CONFLICT :
                                                 IssueCode::CHRONOLOGY_CONFLICT, field);
    }
    if (entry.contains("formal_certification_optional")) {
        if (content_value(entry.at("formal_certification_optional"))) {
            checks.defer(IssueCode::CERTIFICATION_EVIDENCE_REQUIRED, field);
        } else {
            checks.reject(IssueCode::MALFORMED_FIELD, field);
        }
    }
    validate_technology(entry, start, field, checks);
    if (field != activities_field || !entry.contains("name") || !nonblank(text(entry.at("name")))) {
        return std::nullopt;
    }
    // Attest only the checkable timeline of a personal activity. Additional
    // claims about training, certification, access or competition need review.
    static constexpr std::array personal_fields = {
        "name"sv, "activity_id"sv, "category"sv, "started_at_or_age"sv, "ended_at_or_current"sv,
        "typical_frequency"sv,
    };
    if (!std::ranges::all_of(entry.object_range(), [](const auto& member) {
            return std::ranges::find(personal_fields, member.key()) != personal_fields.end();
        })) return std::nullopt;
    if (entry.contains("typical_frequency") && !nonblank(text(entry.at("typical_frequency")))) {
        return std::nullopt;
    }
    const bool ongoing = entry.contains("ended_at_or_current") && text(entry.at("ended_at_or_current")) == "current";
    if ((start.age && (ongoing || end.age)) ||
        (!start.date.empty() && age.birth_year && (ongoing || !end.date.empty()))) {
        return ActivityPeriod{start, end, ongoing};
    }
    return std::nullopt;
}

bool has_checkable_activity_budget(std::vector<ActivityPeriod>& periods) {
    if (periods.empty()) return false;
    const bool by_age = periods.front().start.age.has_value();
    if (std::ranges::any_of(periods, [=](const ActivityPeriod& period) {
            return period.start.age.has_value() != by_age;
        })) return false;
    std::ranges::sort(periods, [=](const ActivityPeriod& a, const ActivityPeriod& b) {
        return by_age ? a.start.age < b.start.age : a.start.date < b.start.date;
    });
    // Time markers alone cannot establish a combined budget for overlapping
    // activities. Even equal bounds might denote overlap at this precision.
    for (std::size_t i = 1; i < periods.size(); ++i) {
        const auto& previous = periods[i - 1];
        const auto& next = periods[i];
        if (previous.ongoing ||
            (by_age ? previous.end.age >= next.start.age : previous.end.date >= next.start.date)) return false;
    }
    return true;
}

void validate_history(const Json& draft, std::string_view field, IssueCode evidence,
                      const BiographicalAge& age, const BiographyContext& context, Checks& checks) {
    if (!draft.contains(field)) return;
    const auto& value = draft.at(field);
    std::vector<ActivityPeriod> periods;
    const auto check_entry = [&](const Json& item) {
        if (const auto period = validate_entry(item, age, context, field, checks)) periods.push_back(*period);
    };
    if (value.is_array()) {
        for (const auto& item : value.array_range()) check_entry(item);
    } else {
        check_entry(value);
    }
    if (field == activities_field) {
        checks.personal_background_plausible = periods.size() == (value.is_array() ? value.size() : 1) &&
                                               has_checkable_activity_budget(periods);
    }
    checks.defer(evidence, field);
}

Checks objective_checks(const Json& draft, const BiographyContext& context) {
    Checks checks;
    for (const auto& item : draft.object_range()) {
        const auto key = item.key();
        const auto field = static_field(key);
        if (forbidden(key) || has_authority_field(item.value())) {
            checks.reject(IssueCode::FORBIDDEN_AUTHORITY_FIELD, field.empty() ? "draft" : field);
        } else if (field.empty()) {
            checks.reject(IssueCode::UNEXPECTED_FIELD, "draft");
        }
    }
    for (const auto& value : rules().at("required").array_range()) {
        const auto field = text(value);
        if (!draft.contains(field)) checks.reject(IssueCode::MISSING_REQUIRED_FIELD, field);
    }
    const auto check_shape = [&](const Json& names) {
        for (const auto& value : names.array_range()) {
            const auto field = text(value);
            if (field == birth_field || field == adult_field || !draft.contains(field)) continue;
            const auto& item = draft.at(field);
            const bool textual = field == "display_name" || field == species_field;
            if (textual ? !nonblank(text(item)) : !content_value(item)) {
                checks.reject(IssueCode::MALFORMED_FIELD, field);
            }
        }
    };
    check_shape(rules().at("required"));
    check_shape(rules().at("optional"));
    if (draft.contains(adult_field)) {
        const auto& adult = draft.at(adult_field);
        if (!adult.is_bool()) checks.reject(IssueCode::MALFORMED_FIELD, adult_field);
        else if (!adult.as<bool>()) checks.reject(IssueCode::NON_ADULT_DECLARED, adult_field);
    }
    const auto age = validate_birth(draft, context, checks);
    validate_playable_maturity(draft, age, context, checks);
    for (const auto field : {"origin", "citizenship_context"}) {
        if (draft.contains(field)) check_evidence_ref(draft.at(field), field, checks);
    }
    validate_history(draft, activities_field, IssueCode::ACTIVITY_BUDGET_REVIEW, age, context, checks);
    validate_history(draft, education_field, IssueCode::EDUCATION_EVIDENCE_REQUIRED, age, context, checks);
    validate_history(draft, experience_field, IssueCode::EXPERIENCE_EVIDENCE_REQUIRED, age, context, checks);
    validate_history(draft, certifications_field, IssueCode::CERTIFICATION_EVIDENCE_REQUIRED, age, context, checks);
    checks.defer(IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin");
    checks.defer(IssueCode::CITIZENSHIP_EVIDENCE_REQUIRED, "citizenship_context");
    checks.defer(IssueCode::PROFILE_EVIDENCE_REQUIRED, "player_profile");
    return checks;
}

bool evidence_claim(BiographyIssue issue) {
    const bool history_field = issue.field == education_field || issue.field == experience_field ||
                               issue.field == activities_field || issue.field == certifications_field;
    switch (issue.code) {
    case IssueCode::PROFILE_EVIDENCE_REQUIRED: return issue.field == "player_profile";
    case IssueCode::ORIGIN_EVIDENCE_REQUIRED: return issue.field == "origin";
    case IssueCode::CITIZENSHIP_EVIDENCE_REQUIRED: return issue.field == "citizenship_context";
    case IssueCode::EDUCATION_EVIDENCE_REQUIRED: return issue.field == education_field;
    case IssueCode::EXPERIENCE_EVIDENCE_REQUIRED: return issue.field == experience_field;
    case IssueCode::ACTIVITY_BUDGET_REVIEW: return issue.field == activities_field;
    case IssueCode::CERTIFICATION_EVIDENCE_REQUIRED:
    case IssueCode::TECH_AVAILABILITY_REVIEW: return history_field;
    default: return false;
    }
}

constexpr BiographyIssue personal_activity_claim{IssueCode::ACTIVITY_BUDGET_REVIEW, activities_field};

bool background_prerequisite(BiographyIssue issue) {
    return issue.code == IssueCode::AGE_OUTSIDE_CALENDAR ||
           issue.code == IssueCode::SPECIAL_MATURITY_RULE_REQUIRED ||
           issue.code == IssueCode::PLAYABLE_AGE_UNDECIDED ||
           issue.code == IssueCode::CONTEXT_NOT_DECIDED;
}

bool source_origin(BiographyEvidenceOrigin origin) {
    switch (origin) {
    case BiographyEvidenceOrigin::UNREGISTERED: return false;
    case BiographyEvidenceOrigin::APPROVED_RULE:
    case BiographyEvidenceOrigin::WORLD_FACT_READ:
    case BiographyEvidenceOrigin::VALIDATED_INITIAL_BACKGROUND: return true;
    }
    return false;
}

} // namespace

std::string_view code_name(IssueCode code) noexcept {
    switch (code) {
    case IssueCode::INVALID_DRAFT: return "INVALID_DRAFT";
    case IssueCode::INVALID_CAMPAIGN_CONTEXT: return "INVALID_CAMPAIGN_CONTEXT";
    case IssueCode::UNEXPECTED_FIELD: return "UNEXPECTED_FIELD";
    case IssueCode::FORBIDDEN_AUTHORITY_FIELD: return "FORBIDDEN_AUTHORITY_FIELD";
    case IssueCode::MISSING_REQUIRED_FIELD: return "MISSING_REQUIRED_FIELD";
    case IssueCode::MALFORMED_FIELD: return "MALFORMED_FIELD";
    case IssueCode::UNKNOWN_SPECIES: return "UNKNOWN_SPECIES";
    case IssueCode::UNSUPPORTED_BIRTH_VALUE: return "UNSUPPORTED_BIRTH_VALUE";
    case IssueCode::BIRTH_AFTER_CAMPAIGN_YEAR: return "BIRTH_AFTER_CAMPAIGN_YEAR";
    case IssueCode::AGE_OUTSIDE_CALENDAR: return "AGE_OUTSIDE_CALENDAR";
    case IssueCode::NON_ADULT_DECLARED: return "NON_ADULT_DECLARED";
    case IssueCode::PRIOR_ACTIVITY_AGE_CONFLICT: return "PRIOR_ACTIVITY_AGE_CONFLICT";
    case IssueCode::CHRONOLOGY_CONFLICT: return "CHRONOLOGY_CONFLICT";
    case IssueCode::CONTEXT_NOT_DECIDED: return "CONTEXT_NOT_DECIDED";
    case IssueCode::BELOW_PLAYABLE_AGE: return "BELOW_PLAYABLE_AGE";
    case IssueCode::PLAYABLE_AGE_UNDECIDED: return "PLAYABLE_AGE_UNDECIDED";
    case IssueCode::SPECIAL_MATURITY_RULE_REQUIRED: return "SPECIAL_MATURITY_RULE_REQUIRED";
    case IssueCode::DLC_DELTA_UNAVAILABLE: return "DLC_DELTA_UNAVAILABLE";
    case IssueCode::MATURITY_EVIDENCE_REQUIRED: return "MATURITY_EVIDENCE_REQUIRED";
    case IssueCode::PROFILE_EVIDENCE_REQUIRED: return "PROFILE_EVIDENCE_REQUIRED";
    case IssueCode::ORIGIN_EVIDENCE_REQUIRED: return "ORIGIN_EVIDENCE_REQUIRED";
    case IssueCode::CITIZENSHIP_EVIDENCE_REQUIRED: return "CITIZENSHIP_EVIDENCE_REQUIRED";
    case IssueCode::EDUCATION_EVIDENCE_REQUIRED: return "EDUCATION_EVIDENCE_REQUIRED";
    case IssueCode::EXPERIENCE_EVIDENCE_REQUIRED: return "EXPERIENCE_EVIDENCE_REQUIRED";
    case IssueCode::CERTIFICATION_EVIDENCE_REQUIRED: return "CERTIFICATION_EVIDENCE_REQUIRED";
    case IssueCode::TECH_AVAILABILITY_REVIEW: return "TECH_AVAILABILITY_REVIEW";
    case IssueCode::TECH_UNAVAILABLE: return "TECH_UNAVAILABLE";
    case IssueCode::UNKNOWN_TECHNOLOGY: return "UNKNOWN_TECHNOLOGY";
    case IssueCode::ACTIVITY_BUDGET_REVIEW: return "ACTIVITY_BUDGET_REVIEW";
    case IssueCode::SEMANTIC_CONTRADICTION: return "SEMANTIC_CONTRADICTION";
    case IssueCode::SEMANTIC_SUGGESTION: return "SEMANTIC_SUGGESTION";
    case IssueCode::SEMANTIC_CHANGES_REQUIRED: return "SEMANTIC_CHANGES_REQUIRED";
    case IssueCode::SEMANTIC_REVIEW_UNAVAILABLE: return "SEMANTIC_REVIEW_UNAVAILABLE";
    }
    return {};
}

RegisteredBiographyAuthority::RegisteredBiographyAuthority(std::vector<RegisteredBiographySource> sources,
                                                           std::vector<BiographyClaimEvidence> evidence)
    : sources_(std::move(sources)), evidence_(std::move(evidence)) {
    std::set<std::string_view> source_ids;
    for (const auto& source : sources_) {
        const auto& id = source.identity;
        if (!opaque_id(id.id) || !opaque_id(id.version) || !opaque_id(id.issuer) || !source_origin(id.origin) ||
            !source_ids.insert(id.id).second || source.claims.empty()) {
            throw std::invalid_argument("Invalid F10 evidence source registration");
        }
        for (const auto& claim : source.claims) {
            if (!evidence_claim({claim.code, claim.field}) ||
                (claim.code == IssueCode::PROFILE_EVIDENCE_REQUIRED && id.origin != BiographyEvidenceOrigin::APPROVED_RULE)) {
                throw std::invalid_argument("Unsupported F10 evidence claim scope");
            }
        }
    }
}

RegisteredBiographySource RegisteredBiographyAuthority::initial_background_source() {
    const auto& policy = rules().at("initial_background");
    return {{std::string(text(policy.at("id"))), std::string(text(policy.at("version"))), "F10",
             BiographyEvidenceOrigin::VALIDATED_INITIAL_BACKGROUND},
            {{personal_activity_claim.code, std::string(personal_activity_claim.field)}}};
}

bool RegisteredBiographyAuthority::resolves(BiographyIssue issue, const ReviewRequest& request,
                                            const BiographyContext& context) const {
    return resolves(issue, request, context, nullptr);
}

bool RegisteredBiographyAuthority::resolves(BiographyIssue issue, const ReviewRequest& request,
                                            const BiographyContext& context,
                                            const BiographyClaimEvidence* evaluated) const {
    if (sources_.empty() || (evidence_.empty() && !evaluated) || !evidence_claim(issue) ||
        request.canonical_draft.empty() || request.canonical_draft.size() > max_draft_bytes || !valid_context(context) ||
        request.binding != bind_review(request.canonical_draft, context)) return false;

    const auto registered = [&](const BiographyClaimEvidence& evidence) {
        return BiographyIssue{evidence.claim.code, evidence.claim.field} == issue &&
               evidence.binding == request.binding &&
               std::ranges::any_of(sources_, [&](const RegisteredBiographySource& source) {
                   return source.identity == evidence.source &&
                          std::ranges::find(source.claims, evidence.claim) != source.claims.end();
               });
    };
    bool supported = evaluated && !evaluated->revoked &&
                     evaluated->decision == BiographyEvidenceDecision::SUPPORTED && registered(*evaluated);
    const auto native_background = text(rules().at("initial_background").at("id"));
    for (const auto& evidence : evidence_) {
        if (!registered(evidence)) continue;
        if (evidence.revoked) return false;
        switch (evidence.decision) {
        case BiographyEvidenceDecision::SUPPORTED:
            // Only the native evaluation may assert support under the built-in source ID.
            if (evidence.source.id != native_background) supported = true;
            break;
        case BiographyEvidenceDecision::CONTRADICTED: return false;
        case BiographyEvidenceDecision::INSUFFICIENT:
        case BiographyEvidenceDecision::NOT_APPLICABLE:
            break;
        default: return false;
        }
    }
    return supported;
}

DomainDecision RegisteredBiographyAuthority::verify(const ReviewRequest&, const ReviewEvidence&) const {
    // Future F10 domain verification requires an approved provider and a trusted
    // record of the evaluation. Self-declared reviewer strings cannot supply it.
    return DomainDecision::UNVERIFIED;
}

BiographyValidator::BiographyValidator()
    : BiographyValidator(std::make_shared<RegisteredBiographyAuthority>(
          std::vector{RegisteredBiographyAuthority::initial_background_source()}, std::vector<BiographyClaimEvidence>{})) {}

BiographyValidator::BiographyValidator(std::shared_ptr<const RegisteredBiographyAuthority> authority)
    : registered_authority_(std::move(authority)), issuer_(std::make_shared<const int>(0)) {}

#ifdef TREK_F10_BIOGRAPHY_TESTING
BiographyValidator::BiographyValidator(const BiographyAuthority& authority, SemanticEvaluator& evaluator,
                                       std::string reviewer, std::string reviewer_version)
    : BiographyValidator(nullptr) {
    test_authority_ = &authority;
    evaluator_ = &evaluator;
    reviewer_ = std::move(reviewer);
    reviewer_version_ = std::move(reviewer_version);
}
#endif

BiographyEvaluation BiographyValidator::evaluate(std::string_view draft, const BiographyContext& context) const {
    BiographyEvaluation result;
    const BiographyContext frozen_context = context;
    if (!valid_context(frozen_context)) {
        result.objective.issues_.push_back({IssueCode::INVALID_CAMPAIGN_CONTEXT, "campaign_context"});
        return result;
    }
    const auto parsed = parse_draft(draft);
    if (!parsed) {
        result.objective.issues_.push_back({IssueCode::INVALID_DRAFT, "draft"});
        return result;
    }
    auto checks = objective_checks(*parsed, frozen_context);
    if (!checks.errors.empty()) {
        result.objective.issues_ = std::move(checks.errors);
        return result;
    }
    auto bytes = canonical(*parsed);
    if (bytes.size() > max_draft_bytes) {
        result.objective.issues_.push_back({IssueCode::INVALID_DRAFT, "draft"});
        return result;
    }
    const auto& binding = result.objective.binding_.emplace(bind_review(bytes, frozen_context));
    const ReviewRequest request{bytes, binding};
    const BiographyAuthority* authority = registered_authority_.get();
#ifdef TREK_F10_BIOGRAPHY_TESTING
    if (test_authority_) authority = test_authority_;
#endif
    if (authority) {
        // Preserve every pending issue if the domain resolver fails partway.
        try {
            std::optional<BiographyClaimEvidence> personal_background;
            if (registered_authority_ && checks.personal_background_plausible &&
                std::ranges::none_of(checks.pending, background_prerequisite)) {
                auto source = RegisteredBiographyAuthority::initial_background_source();
                personal_background.emplace(BiographyClaimEvidence{
                    std::move(source.identity), std::move(source.claims.front()), binding,
                    BiographyEvidenceDecision::SUPPORTED});
            }
            for (const auto& issue : checks.pending) {
                // An evidence provider cannot supply missing policy or set the campaign date.
                const bool use_personal_background = issue == personal_activity_claim && personal_background.has_value();
                if (issue.code == IssueCode::SPECIAL_MATURITY_RULE_REQUIRED ||
                    issue.code == IssueCode::PLAYABLE_AGE_UNDECIDED ||
                    !(use_personal_background
                          ? registered_authority_->resolves(issue, request, frozen_context, &*personal_background)
                          : authority->resolves(issue, request, frozen_context))) {
                    result.objective.issues_.push_back(issue);
                }
            }
        } catch (...) {
            result.objective.issues_ = std::move(checks.pending);
        }
    } else {
        result.objective.issues_ = std::move(checks.pending);
    }
    result.objective.status_ = result.objective.issues_.empty() ?
        ObjectiveStatus::OBJECTIVE_VALID : ObjectiveStatus::REVIEW_REQUIRED;

    const auto unavailable = [&result] {
        result.semantic = SemanticStatus::REVIEW_UNAVAILABLE;
        result.semantic_issues = {{IssueCode::SEMANTIC_REVIEW_UNAVAILABLE, "semantic_validation"}};
    };
    if (!evaluator_ || !authority) {
        unavailable();
        return result;
    }
    if (result.objective.status_ != ObjectiveStatus::OBJECTIVE_VALID) {
        result.semantic = SemanticStatus::REVIEW_REQUIRED;
        return result;
    }

    ReviewEvidence evidence;
    DomainDecision decision = DomainDecision::UNVERIFIED;
    try {
        evidence = evaluator_->review(request);
        if (evidence.completion != ReviewCompletion::COMPLETE || evidence.binding != binding ||
            evidence.reviewer != reviewer_ || evidence.reviewer_version != reviewer_version_ ||
            !opaque_id(evidence.reviewer) || !opaque_id(evidence.reviewer_version) ||
            !opaque_id(evidence.review_ref) || evidence.findings.size() > max_findings) {
            unavailable();
            return result;
        }
        for (const auto& finding : evidence.findings) {
            if (static_field(finding.field).empty() ||
                (finding.kind != FindingKind::CONTRADICTION && finding.kind != FindingKind::SUGGESTION)) {
                unavailable();
                return result;
            }
        }
        decision = authority->verify(request, evidence);
    } catch (...) {
        unavailable();
        return result;
    }

    if (decision != DomainDecision::ACCEPTED && decision != DomainDecision::CORRECTIONS) {
        unavailable();
        return result;
    }
    bool contradiction = false;
    for (const auto& finding : evidence.findings) {
        const bool conflicts = finding.kind == FindingKind::CONTRADICTION;
        contradiction |= conflicts;
        result.semantic_issues.push_back({
            conflicts ? IssueCode::SEMANTIC_CONTRADICTION : IssueCode::SEMANTIC_SUGGESTION,
            static_field(finding.field)});
    }
    if (contradiction || decision == DomainDecision::CORRECTIONS) {
        result.semantic = SemanticStatus::CHANGES_REQUIRED;
        if (!contradiction) {
            result.semantic_issues.push_back({IssueCode::SEMANTIC_CHANGES_REQUIRED, "semantic_validation"});
        }
        return result;
    }
    result.semantic = SemanticStatus::VALID;
    result.receipt = BiographyReceipt(issuer_, frozen_context, std::move(evidence), std::move(bytes));
    return result;
}

bool BiographyValidator::eligible(const BiographyReceipt& receipt, std::string_view draft,
                                  const BiographyContext& current) const {
    if (receipt.issuer_.lock() != issuer_ || receipt.context_ != current || !valid_context(current) ||
        receipt.evidence_.binding.ruleset != ruleset_identity() ||
        receipt.evidence_.binding.policy != review_policy()) return false;
    const auto parsed = parse_draft(draft);
    return parsed && canonical(*parsed) == receipt.canonical_draft_;
}

} // namespace trek::f10
