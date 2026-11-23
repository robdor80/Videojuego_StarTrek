#pragma once
#include "biography_validation.h"
#include <trek/host/ai/service.h>

namespace trek::f10 {
// Internal HOST composition only, same toolchain. One owner thread per draft/session.
// No public way to register a completed review or substitute a SemanticEvaluator.
class OpenAiBiographyEvaluator final : public SemanticEvaluator {
public:
    enum class Route { HABITUAL, EXPLICIT_COMPLEX };
    explicit OpenAiBiographyEvaluator(std::shared_ptr<host::ai::Service>, Route = Route::HABITUAL);
    ~OpenAiBiographyEvaluator() override;
    ReviewEvidence review(const ReviewRequest&) override;
    // Owner MUST call on edit/context change, session close, cancellation or policy reload.
    // Re-evaluation also invalidates a different binding before it can be used.
    void cancel() noexcept;
    [[nodiscard]] host::ai::Error error() const noexcept { return error_; }
    static constexpr std::string_view identity = "openai.responses.f10";
    static constexpr std::string_view version = "ia02.1";
private:
    friend class RegisteredBiographyAuthority;
    friend class BiographyValidator;
    DomainDecision verify(const ReviewRequest&, const ReviewEvidence&) const;
    std::shared_ptr<host::ai::Service> service_;
    std::string route_, model_, canonical_;
    std::optional<BiographyContext> context_;
    std::optional<host::ai::Operation> operation_;
    std::optional<ReviewEvidence> record_;
    host::ai::Error error_{host::ai::Error::OK};
    std::uint64_t serial_{};
};
}
