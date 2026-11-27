#pragma once

#include "trek/host/session_owner.h"

#include <variant>

namespace trek::host::detail {

struct CareerViewV1 {
    std::uint64_t rank_event_id = 0;
    std::uint32_t rank = 0, service_status = 0;
};

struct PromotionViewV1 {
    std::uint64_t event_id = 0, effective_tick = 0, original_revision = 0;
    std::uint32_t from_rank = 0, to_rank = 0;
};

struct InstitutionalViewV1 {
    std::uint64_t world_revision = 0;
    std::variant<CareerViewV1, PromotionViewV1> facts;
};

struct InstitutionalResult {
    Error error = Error::OK;
    Generation generation;
    std::uint64_t correlation_id = 0;
    std::optional<InstitutionalViewV1> view;
    std::uint64_t persistence_epoch = 0;
};

// Local native projection. Only SessionOwner selects the observer and subject.
class InstitutionalQueries final {
public:
    static std::future<InstitutionalResult> career(SessionOwner&, Generation,
                                                   std::uint64_t correlation = 0);
    static std::future<InstitutionalResult> promotion(SessionOwner&, Generation,
                                                      std::uint64_t event_id, std::uint64_t correlation = 0);
    // Check immediately before using a previously received view.
    static bool is_current(const SessionOwner&, const InstitutionalResult&);
};

enum class InstitutionalKind { CAREER, PROMOTION };
struct InstitutionalRequest {
    InstitutionalKind kind;
    std::uint64_t event_id, correlation;
};

} // namespace trek::host::detail
