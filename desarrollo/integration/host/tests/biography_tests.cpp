#include "f10/biography_evidence.h"
#include "biography_rules_data.h"

#include <jsoncons/json.hpp>
#include <iostream>
#include <stdexcept>
#include <type_traits>

namespace trek::f10 {
struct BiographyReceiptTestAccess {
    static void change_ruleset(BiographyReceipt& receipt, std::string previous_ruleset) {
        receipt.evidence_.binding.ruleset = std::move(previous_ruleset);
    }
};
}

namespace {
using namespace trek::f10;
using Json = jsoncons::json;

void check(bool ok, std::string_view label) {
    if (!ok) throw std::runtime_error(std::string(label));
}

BiographyContext context() {
    return {"starfleet_academy", "tng_ds9_voyager", 2383, "", "campaign-a", 1, "local-profile"};
}

Json draft() {
    return Json::parse(R"({
        "display_name":"Talia Ren","species_id":"human","age_or_birth_date":20,
        "adult_equivalent_status":true,"origin":"local origin","citizenship_context":"to review",
        "culture_context":"civilian","appearance_profile":"description",
        "prior_education":["general studies"],"prior_experience":["civilian work"],
        "prior_activities_and_hobbies":[{"name":"karate","started_at_or_age":8,"ended_at_or_current":"current"}],
        "initial_long_term_objective":"apply to Starfleet Academy"
    })");
}

Json maturity_draft(std::string_view species) {
    auto data = draft();
    data["species_id"] = species;
    data["prior_activities_and_hobbies"] = "Reading";
    return data;
}

bool issue(const BiographyEvaluation& result, IssueCode code, std::string_view field) {
    for (const auto* list : {&result.objective.issues(), &result.semantic_issues}) {
        for (const auto& item : *list) if (item.code == code && item.field == field) return true;
    }
    return false;
}

void diagnostics(const BiographyEvaluation& result) {
    for (const auto* list : {&result.objective.issues(), &result.semantic_issues}) {
        for (const auto& item : *list) std::cerr << code_name(item.code) << ' ' << item.field << '\n';
    }
}

void rejected(const BiographyEvaluation& result, IssueCode code, std::string_view field) {
    const auto correct = result.objective.status() == ObjectiveStatus::CHANGES_REQUIRED &&
                         result.semantic == SemanticStatus::NOT_REQUESTED && !result.receipt &&
                         issue(result, code, field);
    if (!correct) diagnostics(result);
    check(correct, code_name(code));
}

// These two controls are linked only in the test target.
struct Evaluator final : SemanticEvaluator {
    enum Mode { GOOD, DOWN, PARTIAL, THROW, FOREIGN, WRONG_VERSION, WRONG_POLICY, WRONG_RULESET,
                WRONG_CONTEXT, WRONG_DRAFT, CONTRADICTION, ADVICE, PRIVATE_FIELD, BAD_TRACE };
    Mode mode{GOOD};
    unsigned calls{};
    BiographyContext* advance_generation{};
    std::string seen;
    ReviewBinding request_binding;

    ReviewEvidence review(const ReviewRequest& request) override {
        ++calls;
        if (advance_generation) ++advance_generation->generation;
        seen.assign(request.canonical_draft);
        request_binding = request.binding;
        ReviewEvidence evidence{request.binding, ReviewCompletion::COMPLETE, "fixture-local", "test-1", "review-17", {}};
        switch (mode) {
        case GOOD: break;
        case DOWN: evidence.completion = ReviewCompletion::UNAVAILABLE; break;
        case PARTIAL: evidence.completion = ReviewCompletion::INCOMPLETE; break;
        case THROW: throw std::runtime_error("private service output");
        case FOREIGN: evidence.reviewer = "other"; break;
        case WRONG_VERSION: evidence.reviewer_version = "test-0"; break;
        case WRONG_POLICY: evidence.binding.policy = "old"; break;
        case WRONG_RULESET: evidence.binding.ruleset = "f10-biography/1:previous"; break;
        case WRONG_CONTEXT: evidence.binding.context_sha256[0] ^= 1; break;
        case WRONG_DRAFT: evidence.binding.draft_sha256[0] ^= 1; break;
        case CONTRADICTION: evidence.findings = {{FindingKind::CONTRADICTION, "prior_education"}}; break;
        case ADVICE: evidence.findings = {{FindingKind::SUGGESTION, "prior_education"}}; break;
        case PRIVATE_FIELD: evidence.findings = {{FindingKind::SUGGESTION, "private service output"}}; break;
        case BAD_TRACE: evidence.review_ref = "private service output"; break;
        }
        return evidence;
    }
};

struct Authority final : BiographyAuthority {
    bool has_evidence{true};
    bool objective_throws{};
    bool semantic_throws{};
    DomainDecision decision{DomainDecision::ACCEPTED};
    mutable unsigned verified{};

    bool resolves(BiographyIssue missing, const ReviewRequest&, const BiographyContext&) const override {
        if (objective_throws && missing.code == IssueCode::PROFILE_EVIDENCE_REQUIRED) {
            throw std::runtime_error("private resolver output");
        }
        return has_evidence;
    }

    DomainDecision verify(const ReviewRequest&, const ReviewEvidence&) const override {
        ++verified;
        if (semantic_throws) throw std::runtime_error("private verifier output");
        return decision;
    }
};

struct Fixture {
    Authority authority;
    Evaluator evaluator;
    BiographyValidator validator{authority, evaluator, "fixture-local", "test-1"};
};

void production() {
    const BiographyValidator validator;
    const auto raw = draft().to_string();
    const auto result = validator.evaluate(raw, context());
    if (result.semantic != SemanticStatus::REVIEW_UNAVAILABLE) diagnostics(result);
    check(result.objective.status() == ObjectiveStatus::REVIEW_REQUIRED &&
          result.semantic == SemanticStatus::REVIEW_UNAVAILABLE && !result.receipt &&
          !issue(result, IssueCode::MATURITY_EVIDENCE_REQUIRED, "adult_equivalent_status") &&
          issue(result, IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin"), "product pending for actual biographical sources");
    check(draft().to_string() == raw, "draft unchanged");
    static_assert(!std::is_default_constructible_v<BiographyReceipt>);
    static_assert(!std::is_copy_constructible_v<BiographyReceipt>);
}

void fields() {
    Fixture f;
    auto data = draft();
    data.erase("origin");
    rejected(f.validator.evaluate(data.to_string(), context()), IssueCode::MISSING_REQUIRED_FIELD, "origin");
    for (const auto key : {"nickname", "manual_skill_point_allocation", "person_id", "validated_creation_ref",
                           "admission_authorized", "academy_population_slot_id", "rank", "authority_grant_id",
                           "permissions", "trusted"}) {
        data = draft();
        data[key] = true;
        rejected(f.validator.evaluate(data.to_string(), context()), IssueCode::FORBIDDEN_AUTHORITY_FIELD, "draft");
    }
    data = draft();
    data["prior_experience"] = Json::parse(R"([{"issuer":"admiral","validated_creation_ref":"fake"}])");
    rejected(f.validator.evaluate(data.to_string(), context()), IssueCode::FORBIDDEN_AUTHORITY_FIELD, "prior_experience");
    check(f.evaluator.calls == 0, "rejected client data must not reach evaluator");
}

void species() {
    BiographyValidator validator;
    auto data = draft();
    for (const auto id : {"invented_alien", "../human", "borg_assimilated_character"}) {
        data["species_id"] = id;
        rejected(validator.evaluate(data.to_string(), context()), IssueCode::UNKNOWN_SPECIES, "species_id");
    }
    data["species_id"] = "human";
    data["adult_equivalent_status"] = false;
    rejected(validator.evaluate(data.to_string(), context()), IssueCode::NON_ADULT_DECLARED, "adult_equivalent_status");
    data["species_id"] = "el_aurian";
    data["adult_equivalent_status"] = true;
    data["age_or_birth_date"] = 2600;
    check(issue(validator.evaluate(data.to_string(), context()), IssueCode::AGE_OUTSIDE_CALENDAR, "age_or_birth_date"),
          "earlier than the supported date format is pending, without a species lifespan cap");
}

void playable_age() {
    const BiographyValidator validator;
    // The F10 reference regression independently pins all author-approved values.
    const auto embedded = Json::parse(detail::biography_rules_json);
    const auto& catalog = embedded.at("species");
    check(catalog.size() == 25, "25 native species");
    unsigned numeric = 0;
    for (const auto& entry : catalog.object_range()) {
        const auto& rule = entry.value();
        if (rule.at("minimum").is_null()) continue;
        ++numeric;
        auto data = maturity_draft(entry.key());
        const auto floor = rule.at("minimum").as<int>();
        data["age_or_birth_date"] = floor - 1;
        auto result = validator.evaluate(data.to_string(), context());
        rejected(result, IssueCode::BELOW_PLAYABLE_AGE, "age_or_birth_date");

        data["age_or_birth_date"] = floor;
        result = validator.evaluate(data.to_string(), context());
        if (rule.at("delta_dlc").as<bool>()) {
            rejected(result, IssueCode::DLC_DELTA_UNAVAILABLE, "species_id");
            check(!issue(result, IssueCode::BELOW_PLAYABLE_AGE, "age_or_birth_date"), entry.key());
            continue;
        }
        check(result.objective.status() == ObjectiveStatus::REVIEW_REQUIRED && !result.receipt &&
              !issue(result, IssueCode::MATURITY_EVIDENCE_REQUIRED, "adult_equivalent_status") &&
              issue(result, IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin"), entry.key());
        data["age_or_birth_date"] = 1200;
        result = validator.evaluate(data.to_string(), context());
        check(result.objective.status() == ObjectiveStatus::REVIEW_REQUIRED &&
              !issue(result, IssueCode::MATURITY_EVIDENCE_REQUIRED, "adult_equivalent_status"), entry.key());
    }
    check(numeric == 22, "22 numeric age floors");

    for (const auto& [id, floor] : {std::pair{"human", 18}, {"vulcan", 25}, {"andorian", 20}, {"ocampan", 2}}) {
        check(catalog.at(id).at("minimum").as<int>() == floor, id);
    }
}

void maturity_dates() {
    Fixture f;
    auto data = maturity_draft("human");
    data["age_or_birth_date"] = "2366-01-01";
    rejected(f.validator.evaluate(data.to_string(), context()), IssueCode::BELOW_PLAYABLE_AGE, "age_or_birth_date");
    for (const auto birthday : {"2365-01-01", "2365-05-18", "2365-12-31"}) {
        data["age_or_birth_date"] = birthday;
        const auto result = f.validator.evaluate(data.to_string(), context());
        check(result.objective.status() == ObjectiveStatus::REVIEW_REQUIRED &&
              result.semantic == SemanticStatus::REVIEW_REQUIRED && !result.receipt && f.evaluator.calls == 0 &&
              issue(result, IssueCode::PLAYABLE_AGE_UNDECIDED, "age_or_birth_date"), birthday);
    }
    data["age_or_birth_date"] = "2364-12-31";
    auto result = f.validator.evaluate(data.to_string(), context());
    check(result.objective.status() == ObjectiveStatus::OBJECTIVE_VALID && result.receipt &&
          result.semantic == SemanticStatus::VALID && f.evaluator.calls == 1 &&
          !issue(result, IssueCode::MATURITY_EVIDENCE_REQUIRED, "adult_equivalent_status"),
          "age past the minimum has no additional adulthood gate");
    data["age_or_birth_date"] = 18;
    result = f.validator.evaluate(data.to_string(), context());
    check(result.objective.status() == ObjectiveStatus::OBJECTIVE_VALID && result.receipt &&
          result.semantic == SemanticStatus::VALID && f.evaluator.calls == 2 &&
          !issue(result, IssueCode::MATURITY_EVIDENCE_REQUIRED, "adult_equivalent_status"),
          "declared age at minimum passes age check without invented evidence");
}

void restricted_species() {
    Fixture f;
    for (const auto id : {"changeling", "jem_hadar", "vorta"}) {
        auto data = maturity_draft(id);
        for (const auto age : {1, 18, 1200}) {
            data["age_or_birth_date"] = age;
            const auto result = f.validator.evaluate(data.to_string(), context());
            check(result.objective.status() == ObjectiveStatus::REVIEW_REQUIRED &&
                  result.semantic == SemanticStatus::REVIEW_REQUIRED && !result.receipt &&
                  result.objective.issues() ==
                      std::vector<BiographyIssue>{{IssueCode::SPECIAL_MATURITY_RULE_REQUIRED, "species_id"}}, id);
        }
    }
    for (const auto id : {"hirogen", "kazon", "ocampan", "talaxian", "vidiian"}) {
        auto data = maturity_draft(id);
        for (const Json& age : {Json(1200), Json("2350-01-01")}) {
            data["age_or_birth_date"] = age;
            rejected(f.validator.evaluate(data.to_string(), context()), IssueCode::DLC_DELTA_UNAVAILABLE, "species_id");
        }
    }
    check(f.evaluator.calls == 0 && f.authority.verified == 0, "unavailable species never reach semantic review");
}

void chronology() {
    BiographyValidator validator;
    auto data = draft();
    for (const auto invalid : {"2383-02-29", "2363-08-32", "0000-01-01"}) {
        data["age_or_birth_date"] = invalid;
        rejected(validator.evaluate(data.to_string(), context()), IssueCode::UNSUPPORTED_BIRTH_VALUE, "age_or_birth_date");
    }
    data["age_or_birth_date"] = true;
    rejected(validator.evaluate(data.to_string(), context()), IssueCode::UNSUPPORTED_BIRTH_VALUE, "age_or_birth_date");
    data["age_or_birth_date"] = -1;
    rejected(validator.evaluate(data.to_string(), context()), IssueCode::UNSUPPORTED_BIRTH_VALUE, "age_or_birth_date");
    data["age_or_birth_date"] = "2384-01-01";
    rejected(validator.evaluate(data.to_string(), context()), IssueCode::BIRTH_AFTER_CAMPAIGN_YEAR, "age_or_birth_date");
    data["age_or_birth_date"] = "2364-02-29";
    data["prior_experience"] = Json::parse(R"([{"started_at_or_age":"2364-02-28"}])");
    rejected(validator.evaluate(data.to_string(), context()), IssueCode::CHRONOLOGY_CONFLICT, "prior_experience");
    data = draft();
    for (const auto activity : {R"([{"started_at_or_age":21}])", R"([{"started_at_or_age":8,"ended_at_or_current":3}])"}) {
        data["prior_activities_and_hobbies"] = Json::parse(activity);
        rejected(validator.evaluate(data.to_string(), context()), IssueCode::PRIOR_ACTIVITY_AGE_CONFLICT,
                 "prior_activities_and_hobbies");
    }
    data = draft();
    data["prior_education"] = Json::parse(R"([{"started_at_or_age":"2383-12-31"}])");
    check(issue(validator.evaluate(data.to_string(), context()), IssueCode::CONTEXT_NOT_DECIDED, "prior_education"),
          "month/day is undecided");
}

void evidence() {
    BiographyValidator validator;
    auto data = draft();
    data["citizenship_context"] = "Federation citizen";
    data["certifications"] = Json::parse(R"([{"name":"command_qualified","evidence_ref":"made-up"}])");
    auto result = validator.evaluate(data.to_string(), context());
    check(result.objective.status() == ObjectiveStatus::REVIEW_REQUIRED && !result.receipt &&
          issue(result, IssueCode::CITIZENSHIP_EVIDENCE_REQUIRED, "citizenship_context") &&
          issue(result, IssueCode::CERTIFICATION_EVIDENCE_REQUIRED, "certifications"), "claims require evidence");
    data["prior_activities_and_hobbies"] = Json::parse(R"([{"formal_certification_optional":"black_belt_1_dan"}])");
    check(issue(validator.evaluate(data.to_string(), context()), IssueCode::CERTIFICATION_EVIDENCE_REQUIRED,
                "prior_activities_and_hobbies"), "hobby certification requires evidence");
    data["prior_education"] = Json::parse(
        R"([{"started_at_or_age":"2370-01-01","technology_ref":"quantum_torpedoes","technology_profile_ref":"tng_2364_2370"}])");
    rejected(validator.evaluate(data.to_string(), context()), IssueCode::TECH_UNAVAILABLE, "prior_education");
    data["prior_education"] = Json::parse(
        R"([{"started_at_or_age":"2370-01-01","technology_ref":"quantum_torpedoes","technology_profile_ref":"tng_2364_2370","evidence_ref":"unverified-exception"}])");
    check(issue(validator.evaluate(data.to_string(), context()), IssueCode::TECH_AVAILABILITY_REVIEW, "prior_education"),
          "exception claim requires evidence review");
}

void context_case() {
    BiographyValidator validator;
    auto current = context();
    current.start_date = "2383-09-01";
    rejected(validator.evaluate(draft().to_string(), current), IssueCode::INVALID_CAMPAIGN_CONTEXT, "campaign_context");
    current = context();
    current.start_year = 2384;
    rejected(validator.evaluate(draft().to_string(), current), IssueCode::INVALID_CAMPAIGN_CONTEXT, "campaign_context");
    current = context();
    current.generation = 0;
    rejected(validator.evaluate(draft().to_string(), current), IssueCode::INVALID_CAMPAIGN_CONTEXT, "campaign_context");
}

void malformed() {
    BiographyValidator validator;
    const auto raw = draft().to_string();
    for (const auto input : {"null", "[]", "{", R"({"x":1,"\u0078":2})", "{/*comment*/}", R"({"x":1,})"}) {
        rejected(validator.evaluate(input, context()), IssueCode::INVALID_DRAFT, "draft");
    }
    rejected(validator.evaluate(raw + "{}", context()), IssueCode::INVALID_DRAFT, "draft");
    auto invalid_utf8 = raw;
    invalid_utf8.replace(invalid_utf8.find("Talia"), 1, 1, static_cast<char>(0xFF));
    rejected(validator.evaluate(invalid_utf8, context()), IssueCode::INVALID_DRAFT, "draft");
    rejected(validator.evaluate(std::string(65537, 'x'), context()), IssueCode::INVALID_DRAFT, "draft");
    rejected(validator.evaluate("{\"nested\":" + std::string(20, '[') + "0" + std::string(20, ']') + "}", context()),
             IssueCode::INVALID_DRAFT, "draft");
}

void conjunction() {
    Fixture f;
    const auto raw = draft().to_string();
    f.authority.has_evidence = false;
    auto result = f.validator.evaluate(raw, context());
    check(result.objective.status() == ObjectiveStatus::REVIEW_REQUIRED &&
          result.semantic == SemanticStatus::REVIEW_REQUIRED && f.evaluator.calls == 0 && !result.receipt,
          "objective pending blocks review");
    f.authority.has_evidence = true;
    f.authority.decision = DomainDecision::UNVERIFIED;
    result = f.validator.evaluate(raw, context());
    check(result.objective.status() == ObjectiveStatus::OBJECTIVE_VALID &&
          result.semantic == SemanticStatus::REVIEW_UNAVAILABLE && !result.receipt, "evaluator cannot approve");
    f.authority.decision = DomainDecision::ACCEPTED;
    result = f.validator.evaluate(raw, context());
    check(result.objective.status() == ObjectiveStatus::OBJECTIVE_VALID && result.semantic == SemanticStatus::VALID &&
          result.receipt && f.validator.eligible(*result.receipt, raw, context()), "both controlled gates, same draft");
}

void review() {
    Fixture f;
    const auto raw = draft().to_string();
    f.evaluator.mode = Evaluator::CONTRADICTION;
    auto result = f.validator.evaluate(raw, context());
    check(result.semantic == SemanticStatus::CHANGES_REQUIRED && !result.receipt &&
          issue(result, IssueCode::SEMANTIC_CONTRADICTION, "prior_education"), "unresolved contradiction");
    f.evaluator.mode = Evaluator::ADVICE;
    result = f.validator.evaluate(raw, context());
    check(result.semantic == SemanticStatus::VALID && result.receipt &&
          issue(result, IssueCode::SEMANTIC_SUGGESTION, "prior_education") && f.evaluator.seen == raw,
          "suggestion does not rewrite");
    f.authority.decision = DomainDecision::CORRECTIONS;
    result = f.validator.evaluate(raw, context());
    check(result.semantic == SemanticStatus::CHANGES_REQUIRED && !result.receipt &&
          issue(result, IssueCode::SEMANTIC_CHANGES_REQUIRED, "semantic_validation"), "domain correction");
}

void stale() {
    Fixture f;
    const auto raw = draft().to_string();
    auto valid = f.validator.evaluate(raw, context());
    check(valid.receipt.has_value(), "fixture receipt");
    check(f.validator.eligible(*valid.receipt, "\n " + raw + " ", context()), "JSON whitespace is canonicalized");
    for (const auto field : {"display_name", "species_id", "age_or_birth_date", "prior_education", "prior_experience"}) {
        auto changed = draft();
        changed[field] = "edited";
        check(!f.validator.eligible(*valid.receipt, changed.to_string(), context()), "edited draft cannot reuse receipt");
    }
    auto current = context();
    ++current.generation;
    check(!f.validator.eligible(*valid.receipt, raw, current), "expired generation");
    current = context();
    current.campaign = "campaign-b";
    check(!f.validator.eligible(*valid.receipt, raw, current), "foreign campaign");
    current = context();
    current.profile = "another-profile";
    check(!f.validator.eligible(*valid.receipt, raw, current), "different player profile");
    current = context();
    current.start_date = "2383-01-01";
    check(!f.validator.eligible(*valid.receipt, raw, current), "different campaign date");
    Fixture other;
    check(!other.validator.eligible(*valid.receipt, raw, context()), "foreign authority instance");
    BiographyValidator product;
    check(!product.eligible(*valid.receipt, raw, context()), "test receipt cannot enter product");
    check(f.evaluator.request_binding.ruleset.starts_with(
              "f10-biography/4:f10_species_playable_maturity_policy/0.1.0:"), "bound maturity policy version");
    auto previous_ruleset = f.evaluator.request_binding.ruleset;
    previous_ruleset.back() = previous_ruleset.back() == '0' ? '1' : '0';
    BiographyReceiptTestAccess::change_ruleset(*valid.receipt, std::move(previous_ruleset));
    check(!f.validator.eligible(*valid.receipt, raw, context()), "same issuer rejects a previous policy content digest");

    auto precise = raw;
    precise.insert(precise.size() - 1, R"(,"medical_background":{"detail":1.00000000000000000001})");
    auto precision_result = f.validator.evaluate(precise, context());
    check(precision_result.receipt.has_value(), "exact numeric data can be reviewed");
    precise.replace(precise.find("00001"), 5, "00002");
    check(!f.validator.eligible(*precision_result.receipt, precise, context()),
          "changes beyond double precision invalidate the receipt");

    auto during_review = context();
    f.evaluator.advance_generation = &during_review;
    const auto late = f.validator.evaluate(raw, during_review);
    check(late.receipt && !f.validator.eligible(*late.receipt, raw, during_review) &&
          f.validator.eligible(*late.receipt, raw, context()),
          "a review that returns after renewal remains bound to the earlier activation");
}

void evidence_stale() {
    Fixture f;
    for (const auto mode : {Evaluator::FOREIGN, Evaluator::WRONG_VERSION, Evaluator::WRONG_POLICY,
             Evaluator::WRONG_RULESET, Evaluator::WRONG_CONTEXT, Evaluator::WRONG_DRAFT}) {
        f.evaluator.mode = mode;
        const auto result = f.validator.evaluate(draft().to_string(), context());
        check(result.semantic == SemanticStatus::REVIEW_UNAVAILABLE && !result.receipt &&
              f.authority.verified == 0, "stale or foreign evidence rejected before domain decision");
    }
}

struct InternalEvidence {
    Json data = draft();
    BiographyContext campaign = context();
    BiographySourceIdentity background{"f10.history", "1", "f10.domain",
                                       BiographyEvidenceOrigin::VALIDATED_INITIAL_BACKGROUND};
    BiographySourceIdentity profile{"f10.profile", "1", "f10.domain", BiographyEvidenceOrigin::APPROVED_RULE};
    std::vector<RegisteredBiographySource> sources{
        {background, {{IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin"},
                      {IssueCode::CITIZENSHIP_EVIDENCE_REQUIRED, "citizenship_context"},
                      {IssueCode::EDUCATION_EVIDENCE_REQUIRED, "prior_education"},
                      {IssueCode::EXPERIENCE_EVIDENCE_REQUIRED, "prior_experience"},
                      {IssueCode::ACTIVITY_BUDGET_REVIEW, "prior_activities_and_hobbies"}}},
        {profile, {{IssueCode::PROFILE_EVIDENCE_REQUIRED, "player_profile"}}},
    };

    ReviewBinding binding() const {
        const auto result = BiographyValidator{}.evaluate(data.to_string(), campaign);
        check(result.objective.binding().has_value(), "exact internal binding");
        return *result.objective.binding();
    }

    std::vector<BiographyClaimEvidence> support() const {
        const auto exact = binding();
        std::vector<BiographyClaimEvidence> records;
        for (const auto& source : sources) {
            for (const auto& claim : source.claims) {
                records.push_back({source.identity, claim, exact, BiographyEvidenceDecision::SUPPORTED});
            }
        }
        return records;
    }

    BiographyEvaluation evaluate(std::vector<BiographyClaimEvidence> records) const {
        const BiographyValidator validator(std::make_shared<RegisteredBiographyAuthority>(sources, std::move(records)));
        return validator.evaluate(data.to_string(), campaign);
    }
};

void registered_sources() {
    InternalEvidence f;
    f.data["origin"] = Json::parse(R"({"name":"fictional origin","evidence_ref":"f10.history"})");
    const auto missing = f.evaluate({});
    check(issue(missing, IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin") && !missing.receipt,
          "registered ID in player text is insufficient");

    const auto records = f.support();
    const auto accepted = f.evaluate(records);
    check(accepted.objective.status() == ObjectiveStatus::OBJECTIVE_VALID &&
          accepted.objective.issues().empty() &&
          accepted.semantic == SemanticStatus::REVIEW_UNAVAILABLE && !accepted.receipt,
          "declared age passes; other trusted sources still require semantic review");

    const auto unavailable = BiographyValidator{}.evaluate(f.data.to_string(), f.campaign);
    check(issue(unavailable, IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin") &&
          unavailable.semantic == SemanticStatus::REVIEW_UNAVAILABLE && !unavailable.receipt, "authority absent");

    const RegisteredBiographyAuthority authority(f.sources, records);
    const auto raw = f.data.to_string();
    const auto exact = f.binding();
    const ReviewRequest request{raw, exact};
    const BiographyIssue origin{IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin"};
    check(authority.resolves(origin, request, f.campaign), "current source attestation");
    check(!authority.resolves(origin, {"{}", exact}, f.campaign), "binding cannot substitute a different draft");
    auto old = exact;
    old.policy += ":old";
    check(!authority.resolves(origin, {raw, old}, f.campaign), "authority rejects obsolete request policy");
    ReviewEvidence forged{exact, ReviewCompletion::COMPLETE, "f10.domain", "1", "guess", {}};
    check(authority.verify(request, forged) == DomainDecision::UNVERIFIED,
          "matching strings and binding do not authenticate a semantic review");

    for (const auto key : {"source_version_or_world_revision", "evidence_decision", "reviewer_identity_and_version"}) {
        auto injected = f.data;
        injected["origin"][key] = "forged";
        rejected(BiographyValidator{}.evaluate(injected.to_string(), f.campaign),
                 IssueCode::FORBIDDEN_AUTHORITY_FIELD, "origin");
    }
    ++f.campaign.generation;
    check(issue(f.evaluate(records), IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin"), "previous generation");
    --f.campaign.generation;
    f.campaign.profile = "other-profile";
    check(issue(f.evaluate(records), IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin"), "previous profile");
    f.campaign = context();
    f.campaign.campaign = "other-campaign";
    check(issue(f.evaluate(records), IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin"), "previous campaign");
    f.campaign = context();
    f.data["display_name"] = "Edited";
    check(issue(f.evaluate(records), IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin"), "previous draft");
}

void evidence_conflicts() {
    InternalEvidence f;
    const auto records = f.support();
    const auto pending_origin = [&](std::vector<BiographyClaimEvidence> evidence) {
        const auto result = f.evaluate(std::move(evidence));
        return result.objective.status() == ObjectiveStatus::REVIEW_REQUIRED && !result.receipt &&
               issue(result, IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin");
    };
    auto invalid = records;
    invalid.front().source.id = "unregistered";
    check(pending_origin(invalid), "unregistered source");
    invalid = records;
    invalid.front().source.issuer = "forged";
    check(pending_origin(invalid), "issuer does not match registry");
    invalid = records;
    invalid.front().source.origin = BiographyEvidenceOrigin::WORLD_FACT_READ;
    check(pending_origin(invalid), "origin does not match registry");
    invalid = records;
    invalid.front().source.version = "older-revision";
    check(pending_origin(invalid), "source version does not match registry");
    invalid = records;
    invalid.front().binding.ruleset += ":older";
    check(pending_origin(invalid), "obsolete ruleset");
    invalid = records;
    invalid.front().binding.policy += ":older";
    check(pending_origin(invalid), "obsolete review policy");
    invalid = records;
    invalid.front().source = f.profile;
    check(pending_origin(invalid), "registered source outside its claim scope");
    invalid = records;
    invalid.front().decision = BiographyEvidenceDecision::INSUFFICIENT;
    check(pending_origin(invalid), "insufficient evidence");
    invalid.front().decision = BiographyEvidenceDecision::NOT_APPLICABLE;
    check(pending_origin(invalid), "inapplicable evidence");
    invalid = records;
    invalid.front().revoked = true;
    invalid.push_back(records.front());
    check(pending_origin(invalid), "revocation wins over support");

    f.sources.push_back({{"f10.fact", "12", "f10.reader", BiographyEvidenceOrigin::WORLD_FACT_READ},
                         {records.front().claim}});
    auto conflict = records.front();
    conflict.source = f.sources.back().identity;
    conflict.decision = BiographyEvidenceDecision::CONTRADICTED;
    invalid = records;
    invalid.push_back(conflict);
    check(pending_origin(invalid), "registered contradiction wins over support");
    std::swap(invalid.front(), invalid.back());
    check(pending_origin(invalid), "conflict independent of source order");
    invalid.front().source.version = "11";
    check(!pending_origin(invalid), "obsolete conflict ignored");
}

void evidence_policy() {
    InternalEvidence f;
    check(f.binding().policy.ends_with(":f10_h06_p06a3_evidence_semantic_boundary/0.1.0"),
          "bound evidence policy");
    for (const auto& claim : {BiographyEvidenceClaim{IssueCode::MATURITY_EVIDENCE_REQUIRED, "adult_equivalent_status"},
                              {IssueCode::PLAYABLE_AGE_UNDECIDED, "age_or_birth_date"},
                              {IssueCode::SPECIAL_MATURITY_RULE_REQUIRED, "species_id"},
                              {IssueCode::DLC_DELTA_UNAVAILABLE, "species_id"},
                              {IssueCode::CONTEXT_NOT_DECIDED, "prior_education"},
                              {IssueCode::ORIGIN_EVIDENCE_REQUIRED, "citizenship_context"}}) {
        bool refused = false;
        try {
            const RegisteredBiographyAuthority authority({{f.background, {claim}}}, {});
        } catch (const std::invalid_argument&) {
            refused = true;
        }
        check(refused, "unsupported claim capability");
    }
    f.sources.push_back(f.sources.front());
    bool duplicate_refused = false;
    try {
        const RegisteredBiographyAuthority authority(f.sources, {});
    } catch (const std::invalid_argument&) {
        duplicate_refused = true;
    }
    check(duplicate_refused, "ambiguous registration");

    auto authority = std::make_shared<RegisteredBiographyAuthority>(std::vector<RegisteredBiographySource>{},
                                                                    std::vector<BiographyClaimEvidence>{});
    const BiographyValidator validator(authority);
    auto data = maturity_draft("ocampan");
    data["age_or_birth_date"] = 2;
    auto result = validator.evaluate(data.to_string(), context());
    rejected(result, IssueCode::DLC_DELTA_UNAVAILABLE, "species_id");
    check(!result.objective.binding(), "deterministic rejection is not sent to trusted sources");
    data["species_id"] = "changeling";
    check(issue(validator.evaluate(data.to_string(), context()), IssueCode::SPECIAL_MATURITY_RULE_REQUIRED, "species_id"),
          "special species stays pending");
    data["species_id"] = "human";
    data["age_or_birth_date"] = "2365-06-15";
    check(issue(validator.evaluate(data.to_string(), context()), IssueCode::PLAYABLE_AGE_UNDECIDED, "age_or_birth_date"),
          "threshold year stays pending");
}

void personal_background() {
    const BiographyValidator validator;
    auto data = draft();
    const auto check_personal = [&](const Json& candidate) {
        const auto result = validator.evaluate(candidate.to_string(), context());
        check(result.objective.status() == ObjectiveStatus::REVIEW_REQUIRED &&
              !issue(result, IssueCode::ACTIVITY_BUDGET_REVIEW, "prior_activities_and_hobbies") &&
              result.semantic == SemanticStatus::REVIEW_UNAVAILABLE && !result.receipt,
              "only checkable personal background is supported");
        for (const BiographyIssue unresolved : {
                 BiographyIssue{IssueCode::ORIGIN_EVIDENCE_REQUIRED, "origin"},
                 {IssueCode::CITIZENSHIP_EVIDENCE_REQUIRED, "citizenship_context"},
                 {IssueCode::EDUCATION_EVIDENCE_REQUIRED, "prior_education"},
                 {IssueCode::EXPERIENCE_EVIDENCE_REQUIRED, "prior_experience"},
                 {IssueCode::PROFILE_EVIDENCE_REQUIRED, "player_profile"}}) {
            check(issue(result, unresolved.code, unresolved.field), unresolved.field);
        }
    };
    check_personal(data); // Human, 20, karate from age eight.
    data["prior_activities_and_hobbies"] = Json::parse(R"([
        {"name":"Astronomy","category":"academic_interest","started_at_or_age":16,"ended_at_or_current":"current"},
        {"name":"Karate","category":"martial_art","started_at_or_age":8,"ended_at_or_current":14}
    ])");
    check_personal(data);
    data["age_or_birth_date"] = "2363-04-15";
    data["prior_activities_and_hobbies"] = Json::parse(R"([
        {"name":"Astronomy","started_at_or_age":"2375-06-01","ended_at_or_current":"2380-02-05"}
    ])");
    check_personal(data);
    const BiographyValidator unavailable(nullptr);
    const auto result = unavailable.evaluate(data.to_string(), context());
    check(issue(result, IssueCode::ACTIVITY_BUDGET_REVIEW, "prior_activities_and_hobbies") && !result.receipt,
          "no background source when the authority is absent");
}

void background_boundaries() {
    const BiographyValidator validator;
    auto data = draft();
    const auto budget_pending = [&](const Json& candidate) {
        auto result = validator.evaluate(candidate.to_string(), context());
        check(result.objective.status() == ObjectiveStatus::REVIEW_REQUIRED && !result.receipt &&
              issue(result, IssueCode::ACTIVITY_BUDGET_REVIEW, "prior_activities_and_hobbies"),
              "unchecked activity timeline remains pending");
        return result;
    };
    for (const auto raw : {
             R"("Karate since childhood")",
             R"([{"name":"Karate","started_at_or_age":8}])",
             R"([{"name":"Karate","started_at_or_age":8,"ended_at_or_current":"long ago"}])",
             R"([{"name":"Karate","started_at_or_age":"2370-01-01","ended_at_or_current":"current"}])",
             R"([{"name":"Karate","started_at_or_age":8,"ended_at_or_current":13},{"name":"Music","started_at_or_age":12,"ended_at_or_current":"current"}])",
             R"([{"name":"Karate","started_at_or_age":8,"ended_at_or_current":"current"},"Unverified experience"])",
             R"([{"name":"Training","started_at_or_age":8,"ended_at_or_current":"current","training_context":"Starfleet"}])",
             R"([{"name":"Training","started_at_or_age":8,"ended_at_or_current":"current","evidence_ref":"f10_h06_p06a5_initial_background_policy"}])",
         }) {
        data["prior_activities_and_hobbies"] = Json::parse(raw);
        budget_pending(data);
    }
    data = draft();
    data["prior_activities_and_hobbies"][0]["formal_certification_optional"] = "first dan";
    check(issue(budget_pending(data), IssueCode::CERTIFICATION_EVIDENCE_REQUIRED, "prior_activities_and_hobbies"),
          "practice cannot accredit a certification");
    data = draft();
    data["prior_activities_and_hobbies"][0]["started_at_or_age"] = 21;
    rejected(validator.evaluate(data.to_string(), context()), IssueCode::PRIOR_ACTIVITY_AGE_CONFLICT,
             "prior_activities_and_hobbies");
    data = draft();
    data["prior_experience"] = "I captained a Starfleet ship";
    data["certifications"] = "Medical specialist";
    auto result = validator.evaluate(data.to_string(), context());
    check(issue(result, IssueCode::EXPERIENCE_EVIDENCE_REQUIRED, "prior_experience") &&
          issue(result, IssueCode::CERTIFICATION_EVIDENCE_REQUIRED, "certifications") && !result.receipt,
          "institutional text and certification await trusted sources");
    data["prior_experience"] = Json::parse(R"([{"name":"Starfleet","security_clearance":"maximum"}])");
    rejected(validator.evaluate(data.to_string(), context()), IssueCode::FORBIDDEN_AUTHORITY_FIELD, "prior_experience");
    data = draft();
    data["age_or_birth_date"] = "2365-08-01";
    check(issue(budget_pending(data), IssueCode::PLAYABLE_AGE_UNDECIDED, "age_or_birth_date"), "ambiguous 2383 age");
    data["age_or_birth_date"] = 100;
    for (const auto species : {"changeling", "jem_hadar", "vorta"}) {
        data["species_id"] = species;
        check(issue(budget_pending(data), IssueCode::SPECIAL_MATURITY_RULE_REQUIRED, "species_id"), species);
    }
    for (const auto species : {"hirogen", "kazon", "ocampan", "talaxian", "vidiian"}) {
        data["species_id"] = species;
        rejected(validator.evaluate(data.to_string(), context()), IssueCode::DLC_DELTA_UNAVAILABLE, "species_id");
    }
}

void background_provenance() {
    const auto source = RegisteredBiographyAuthority::initial_background_source();
    check(source.identity.id == "f10_h06_p06a5_initial_background_policy" && source.identity.version == "0.1.0" &&
          source.identity.issuer == "F10" && source.identity.origin == BiographyEvidenceOrigin::VALIDATED_INITIAL_BACKGROUND,
          "versioned F10 source");
    auto data = draft();
    auto campaign = context();
    const auto assessed = BiographyValidator{}.evaluate(data.to_string(), campaign);
    check(assessed.objective.binding().has_value(), "checked draft binding");
    auto revoked = BiographyClaimEvidence{source.identity, source.claims.front(), *assessed.objective.binding(),
                                          BiographyEvidenceDecision::SUPPORTED, true};
    const BiographyValidator validator(std::make_shared<RegisteredBiographyAuthority>(
        std::vector{source}, std::vector{revoked}));
    const auto activity_pending = [&](const BiographyValidator& composed) {
        const auto result = composed.evaluate(data.to_string(), campaign);
        check(!result.receipt, "internal source cannot grant a receipt");
        return issue(result, IssueCode::ACTIVITY_BUDGET_REVIEW, "prior_activities_and_hobbies");
    };
    check(activity_pending(validator), "revocation overrides the generated atestation");
    ++campaign.generation;
    check(!activity_pending(validator), "new generation is evaluated independently");
    --campaign.generation;
    data["prior_activities_and_hobbies"][0].erase("ended_at_or_current");
    check(activity_pending(validator), "changed unsupported draft cannot inherit plausibility");
    auto replayed = revoked;
    replayed.revoked = false;
    replayed.binding = *BiographyValidator{}.evaluate(data.to_string(), campaign).objective.binding();
    const BiographyValidator injected(std::make_shared<RegisteredBiographyAuthority>(
        std::vector{source}, std::vector{replayed}));
    check(activity_pending(injected), "snapshot cannot supply a positive result under the native source ID");
    data = draft();
    auto stale_source = source;
    stale_source.identity.version = "0.0.9";
    const BiographyValidator old(std::make_shared<RegisteredBiographyAuthority>(
        std::vector{stale_source}, std::vector<BiographyClaimEvidence>{}));
    check(activity_pending(old), "stale source registration cannot authenticate the native result");
}

void failure() {
    Fixture f;
    const auto raw = draft().to_string();
    f.authority.objective_throws = true;
    const auto pending = f.validator.evaluate(raw, context());
    check(!pending.receipt && f.evaluator.calls == 0 &&
          issue(pending, IssueCode::PROFILE_EVIDENCE_REQUIRED, "player_profile"), "resolver failure preserves pending issues");
    f.authority.objective_throws = false;
    for (const auto mode : {Evaluator::DOWN, Evaluator::PARTIAL, Evaluator::THROW, Evaluator::GOOD}) {
        f.evaluator.mode = mode;
        f.authority.semantic_throws = mode == Evaluator::GOOD;
        const auto result = f.validator.evaluate(raw, context());
        check(result.semantic == SemanticStatus::REVIEW_UNAVAILABLE && !result.receipt, "service failure closes gate");
    }
    const auto first = f.evaluator.request_binding;
    f.authority.semantic_throws = false;
    const auto result = f.validator.evaluate(raw, context());
    check(result.receipt && f.evaluator.request_binding == first && f.evaluator.seen == raw, "retry preserves input");
}

void privacy() {
    Fixture f;
    for (const auto mode : {Evaluator::PRIVATE_FIELD, Evaluator::BAD_TRACE}) {
        f.evaluator.mode = mode;
        const auto result = f.validator.evaluate(draft().to_string(), context());
        check(!result.receipt && result.semantic_issues ==
              std::vector<BiographyIssue>{{IssueCode::SEMANTIC_REVIEW_UNAVAILABLE, "semantic_validation"}},
              "untrusted messages do not leave the trust boundary");
    }
    auto data = draft();
    data["private medical details"] = "private input";
    rejected(f.validator.evaluate(data.to_string(), context()), IssueCode::UNEXPECTED_FIELD, "draft");
}

} // namespace

int main(int argc, char** argv) {
    try {
        check(argc == 2, "expected case name");
        const std::pair<std::string_view, void(*)()> cases[] = {
            {"production", production}, {"fields", fields}, {"species", species},
            {"playable_age", playable_age}, {"maturity_dates", maturity_dates}, {"restricted_species", restricted_species},
            {"chronology", chronology}, {"evidence", evidence}, {"context", context_case},
            {"malformed", malformed}, {"conjunction", conjunction}, {"review", review},
            {"stale", stale}, {"evidence_stale", evidence_stale}, {"registered_sources", registered_sources},
            {"evidence_conflicts", evidence_conflicts}, {"evidence_policy", evidence_policy},
            {"personal_background", personal_background}, {"background_boundaries", background_boundaries},
            {"background_provenance", background_provenance},
            {"failure", failure}, {"privacy", privacy}
        };
        for (const auto& [name, run] : cases) {
            if (name == argv[1]) {
                run();
                std::cout << "PASS " << name << '\n';
                return 0;
            }
        }
        check(false, "unknown case");
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 1;
    }
}
