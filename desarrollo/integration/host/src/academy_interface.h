#pragma once

#include "f10/academy_candidate_factory.h"

namespace trek::host::detail {

struct AcademyInterfaceResult {
    Error error = Error::OK;
    Generation generation;
    std::optional<AcademyCandidateView> candidate;
    std::vector<SlotInspection> slots;
};

// Private composition, never exported as a caller-controlled receipt or ID.
class AcademyInterface final {
public:
    static std::future<AcademyInterfaceResult> create_bound(SessionOwner&, std::uint64_t key, std::string payload);
    static std::future<AcademyInterfaceResult> query(SessionOwner&, Generation);
    static std::future<AcademyInterfaceResult> slots(SessionOwner&, Generation);
};

} // namespace trek::host::detail
