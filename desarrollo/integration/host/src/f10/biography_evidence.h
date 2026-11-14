#pragma once

#include "biography_validation.h"

namespace trek::f10 {

enum class BiographyEvidenceOrigin { UNREGISTERED, APPROVED_RULE, WORLD_FACT_READ, VALIDATED_INITIAL_BACKGROUND };
enum class BiographyEvidenceDecision { INSUFFICIENT, SUPPORTED, CONTRADICTED, NOT_APPLICABLE };

struct BiographyEvidenceClaim {
    IssueCode code;
    std::string field;
    bool operator==(const BiographyEvidenceClaim&) const = default;
};

struct BiographySourceIdentity {
    std::string id;
    std::string version; // Approved source version or current world revision.
    std::string issuer;
    BiographyEvidenceOrigin origin{BiographyEvidenceOrigin::UNREGISTERED};
    bool operator==(const BiographySourceIdentity&) const = default;
};

struct RegisteredBiographySource {
    BiographySourceIdentity identity;
    std::vector<BiographyEvidenceClaim> claims;
};

struct BiographyClaimEvidence {
    BiographySourceIdentity source;
    BiographyEvidenceClaim claim;
    ReviewBinding binding;
    BiographyEvidenceDecision decision{BiographyEvidenceDecision::INSUFFICIENT};
    bool revoked{};
};

// Owned snapshot for trusted F10 composition. A source attests the entire issue
// for the exact canonical draft, including all entries in a collection field.
// Use a new authority and validator when source registrations or evidence change.
// Neither vector may be populated from player input or evaluator output.
class RegisteredBiographyAuthority final : public BiographyAuthority {
public:
    RegisteredBiographyAuthority(std::vector<RegisteredBiographySource> sources,
                                 std::vector<BiographyClaimEvidence> evidence);

    // Register alongside other trusted sources to enable this per-evaluation
    // attestation and let the same registry apply contradictions or revocations.
    [[nodiscard]] static RegisteredBiographySource initial_background_source();
    [[nodiscard]] bool resolves(BiographyIssue, const ReviewRequest&, const BiographyContext&) const override;
    [[nodiscard]] DomainDecision verify(const ReviewRequest&, const ReviewEvidence&) const override;

private:
    friend class BiographyValidator;
    [[nodiscard]] bool resolves(BiographyIssue, const ReviewRequest&, const BiographyContext&,
                                const BiographyClaimEvidence* evaluated) const;
    const std::vector<RegisteredBiographySource> sources_;
    const std::vector<BiographyClaimEvidence> evidence_;
};

} // namespace trek::f10
