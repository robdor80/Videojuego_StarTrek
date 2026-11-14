#include "biography_validation.h"
#include "biography_rules_data.h"

#include <corerpg/history.hpp>
#include <jsoncons/json.hpp>
#include <jsoncons/json_cursor.hpp>

#include <algorithm>
#include <charconv>
#include <chrono>
#include <set>
#include <utility>

namespace trek::f10 {
namespace {
using Json = jsoncons::json;
using namespace std::string_view_literals;

constexpr auto max_draft_bytes = 65536U;
constexpr auto max_findings = 32U;
constexpr auto ruleset_version = "f10-biography/1"sv;
constexpr std::string_view adult_field = "adult_equivalent_status";
constexpr std::string_view birth_field = "age_or_birth_date";
constexpr std::string_view activities_field = "prior_activities_and_hobbies";
constexpr std::string_view education_field = "prior_education";
constexpr std::string_view experience_field = "prior_experience";
constexpr std::string_view certifications_field = "certifications";

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
        "professional_f11_character_id"sv, "trusted"sv
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

struct Moment {
    std::optional<std::uint64_t> age;
    std::string_view date;
    std::optional<int> year;
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

void validate_entry(const Json& entry, const BiographicalAge& age, const BiographyContext& context,
                    std::string_view field, Checks& checks) {
    if (!entry.is_object()) {
        if (!nonblank(text(entry))) checks.reject(IssueCode::MALFORMED_FIELD, field);
        return;
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
}

void validate_history(const Json& draft, std::string_view field, IssueCode evidence,
                      const BiographicalAge& age, const BiographyContext& context, Checks& checks) {
    if (!draft.contains(field)) return;
    const auto& value = draft.at(field);
    if (value.is_array()) {
        for (const auto& item : value.array_range()) validate_entry(item, age, context, field, checks);
    } else {
        validate_entry(value, age, context, field, checks);
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
            const bool textual = field == "display_name" || field == "species_id";
            if (textual ? !nonblank(text(item)) : !content_value(item)) {
                checks.reject(IssueCode::MALFORMED_FIELD, field);
            }
        }
    };
    check_shape(rules().at("required"));
    check_shape(rules().at("optional"));
    if (draft.contains("species_id") && !contains(rules().at("species"), text(draft.at("species_id")))) {
        checks.reject(IssueCode::UNKNOWN_SPECIES, "species_id");
    }
    if (draft.contains(adult_field)) {
        const auto& adult = draft.at(adult_field);
        if (!adult.is_bool()) checks.reject(IssueCode::MALFORMED_FIELD, adult_field);
        else if (!adult.as<bool>()) checks.reject(IssueCode::NON_ADULT_DECLARED, adult_field);
    }
    const auto age = validate_birth(draft, context, checks);
    for (const auto field : {"origin", "citizenship_context"}) {
        if (draft.contains(field)) check_evidence_ref(draft.at(field), field, checks);
    }
    validate_history(draft, activities_field, IssueCode::ACTIVITY_BUDGET_REVIEW, age, context, checks);
    validate_history(draft, education_field, IssueCode::EDUCATION_EVIDENCE_REQUIRED, age, context, checks);
    validate_history(draft, experience_field, IssueCode::EXPERIENCE_EVIDENCE_REQUIRED, age, context, checks);
    validate_history(draft, certifications_field, IssueCode::CERTIFICATION_EVIDENCE_REQUIRED, age, context, checks);
    checks.defer(IssueCode::MATURITY_RULE_REQUIRED, adult_field);
    checks.defer(IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin");
    checks.defer(IssueCode::CITIZENSHIP_EVIDENCE_REQUIRED, "citizenship_context");
    checks.defer(IssueCode::PROFILE_EVIDENCE_REQUIRED, "player_profile");
    return checks;
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
    case IssueCode::MATURITY_RULE_REQUIRED: return "MATURITY_RULE_REQUIRED";
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

BiographyValidator::BiographyValidator()
    : ruleset_(std::string(ruleset_version) + ":" + std::string(text(rules().at("sources_sha256")))),
      policy_(text(rules().at("policy"))), issuer_(std::make_shared<const int>(0)) {}

#ifdef TREK_F10_BIOGRAPHY_TESTING
BiographyValidator::BiographyValidator(const BiographyAuthority& authority, SemanticEvaluator& evaluator,
                                       std::string reviewer, std::string reviewer_version)
    : BiographyValidator() {
    authority_ = &authority;
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
    auto& binding = result.objective.binding_;
    binding = {digest(bytes), context_digest(frozen_context), ruleset_, policy_};
    const ReviewRequest request{bytes, binding};
    if (authority_) {
        // Preserve every pending issue if the domain resolver fails partway.
        try {
            for (const auto& issue : checks.pending) {
                if (!authority_->resolves(issue, request, frozen_context)) result.objective.issues_.push_back(issue);
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
    if (!evaluator_ || !authority_) {
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
        decision = authority_->verify(request, evidence);
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
        receipt.evidence_.binding.ruleset != ruleset_ || receipt.evidence_.binding.policy != policy_) return false;
    const auto parsed = parse_draft(draft);
    return parsed && canonical(*parsed) == receipt.canonical_draft_;
}

} // namespace trek::f10
