#pragma once

#include <array>
#include <cstdint>
#include <memory>
#include <optional>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

namespace trek::f10 {

// Internal C++ boundary. Context is supplied from the owning activation, never
// decoded from the draft. Generation and profile are rechecked before future use.
struct BiographyContext {
    std::string scenario;
    std::string era;
    int start_year{};
    std::string start_date; // Empty under the current year-only policy.
    std::string campaign;
    std::uint64_t generation{};
    std::string profile;
    bool operator==(const BiographyContext&) const = default;
};

enum class ObjectiveStatus { CHANGES_REQUIRED, REVIEW_REQUIRED, OBJECTIVE_VALID };
enum class SemanticStatus { NOT_REQUESTED, REVIEW_REQUIRED, REVIEW_UNAVAILABLE, CHANGES_REQUIRED, VALID };

enum class IssueCode {
    INVALID_DRAFT, INVALID_CAMPAIGN_CONTEXT, UNEXPECTED_FIELD, FORBIDDEN_AUTHORITY_FIELD,
    MISSING_REQUIRED_FIELD, MALFORMED_FIELD, UNKNOWN_SPECIES, UNSUPPORTED_BIRTH_VALUE,
    BIRTH_AFTER_CAMPAIGN_YEAR, AGE_OUTSIDE_CALENDAR, NON_ADULT_DECLARED, PRIOR_ACTIVITY_AGE_CONFLICT,
    CHRONOLOGY_CONFLICT, CONTEXT_NOT_DECIDED, BELOW_PLAYABLE_AGE, PLAYABLE_AGE_UNDECIDED,
    SPECIAL_MATURITY_RULE_REQUIRED, DLC_DELTA_UNAVAILABLE, MATURITY_EVIDENCE_REQUIRED, PROFILE_EVIDENCE_REQUIRED,
    ORIGIN_EVIDENCE_REQUIRED, CITIZENSHIP_EVIDENCE_REQUIRED, EDUCATION_EVIDENCE_REQUIRED,
    EXPERIENCE_EVIDENCE_REQUIRED, CERTIFICATION_EVIDENCE_REQUIRED, TECH_AVAILABILITY_REVIEW,
    TECH_UNAVAILABLE, UNKNOWN_TECHNOLOGY, ACTIVITY_BUDGET_REVIEW, SEMANTIC_CONTRADICTION, SEMANTIC_SUGGESTION,
    SEMANTIC_CHANGES_REQUIRED, SEMANTIC_REVIEW_UNAVAILABLE
};

[[nodiscard]] std::string_view code_name(IssueCode) noexcept;

struct BiographyIssue {
    IssueCode code;
    std::string_view field; // Always a predefined field, never text copied from a draft or response.
    bool operator==(const BiographyIssue&) const = default;
};

using Digest = std::array<std::uint8_t, 32>;

struct ReviewBinding {
    Digest draft_sha256{};
    Digest context_sha256{};
    std::string ruleset;
    std::string policy;
    bool operator==(const ReviewBinding&) const = default;
};

struct ReviewRequest {
    std::string_view canonical_draft;
    const ReviewBinding& binding;
};

enum class FindingKind { SUGGESTION, CONTRADICTION };
struct ReviewFinding {
    FindingKind kind;
    std::string field;
};

enum class ReviewCompletion { UNAVAILABLE, INCOMPLETE, COMPLETE };
struct ReviewEvidence {
    ReviewBinding binding;
    ReviewCompletion completion{ReviewCompletion::UNAVAILABLE};
    std::string reviewer;
    std::string reviewer_version;
    std::string review_ref;
    std::vector<ReviewFinding> findings;
};

class SemanticEvaluator {
public:
    virtual ~SemanticEvaluator() = default;
    // Synchronous, local port. The request views are borrowed for this call.
    // Returned findings are proposals. The registered domain authority must verify them.
    virtual ReviewEvidence review(const ReviewRequest&) = 0;
};

enum class DomainDecision { UNVERIFIED, CORRECTIONS, ACCEPTED };
class BiographyAuthority {
public:
    virtual ~BiographyAuthority() = default;
    // Resolve only a rule with missing evidence. Deterministic rejection cannot
    // go through this port. Authority must inspect trusted, draft-specific facts.
    virtual bool resolves(BiographyIssue, const ReviewRequest&, const BiographyContext&) const = 0;
    virtual DomainDecision verify(const ReviewRequest&, const ReviewEvidence&) const = 0;
};

class BiographyValidator;

class ObjectiveAssessment final {
public:
    [[nodiscard]] ObjectiveStatus status() const noexcept { return status_; }
    [[nodiscard]] const std::vector<BiographyIssue>& issues() const noexcept { return issues_; }

private:
    friend class BiographyValidator;
    ObjectiveStatus status_{ObjectiveStatus::CHANGES_REQUIRED};
    std::vector<BiographyIssue> issues_;
    ReviewBinding binding_;
};

class BiographyReceipt final {
public:
    BiographyReceipt(const BiographyReceipt&) = delete;
    BiographyReceipt& operator=(const BiographyReceipt&) = delete;
    BiographyReceipt(BiographyReceipt&&) noexcept = default;
    BiographyReceipt& operator=(BiographyReceipt&&) noexcept = default;

private:
    friend class BiographyValidator;
#ifdef TREK_F10_BIOGRAPHY_TESTING
    friend struct BiographyReceiptTestAccess;
#endif
    BiographyReceipt(std::weak_ptr<const int> issuer, BiographyContext context,
                     ReviewEvidence evidence, std::string canonical_draft)
        : issuer_(std::move(issuer)), context_(std::move(context)), evidence_(std::move(evidence)),
          canonical_draft_(std::move(canonical_draft)) {}
    std::weak_ptr<const int> issuer_;
    BiographyContext context_;
    ReviewEvidence evidence_;
    std::string canonical_draft_;
};

struct BiographyEvaluation {
    ObjectiveAssessment objective;
    SemanticStatus semantic{SemanticStatus::NOT_REQUESTED};
    std::vector<BiographyIssue> semantic_issues;
    std::optional<BiographyReceipt> receipt;
};

class BiographyValidator final {
public:
    BiographyValidator();
    BiographyValidator(const BiographyValidator&) = delete;
    BiographyValidator& operator=(const BiographyValidator&) = delete;

#ifdef TREK_F10_BIOGRAPHY_TESTING
    // This constructor is compiled exclusively in the test executable.
    BiographyValidator(const BiographyAuthority&, SemanticEvaluator&, std::string reviewer,
                        std::string reviewer_version);
#endif

    [[nodiscard]] BiographyEvaluation evaluate(std::string_view draft, const BiographyContext&) const;
    // Future commit must call with the current activation and draft on the owner
    // thread. This check neither writes Core nor consumes an intent.
    [[nodiscard]] bool eligible(const BiographyReceipt&, std::string_view draft,
                                const BiographyContext& current) const;

private:
    const BiographyAuthority* authority_{};
    SemanticEvaluator* evaluator_{};
    std::string reviewer_;
    std::string reviewer_version_;
    std::string ruleset_;
    std::string policy_;
    std::shared_ptr<const int> issuer_;
};

} // namespace trek::f10
