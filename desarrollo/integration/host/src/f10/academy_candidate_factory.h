#pragma once

#include "trek/host/session_owner.h"

#include <string_view>

#if defined(TREK_HOST_STATIC_TEST)
# define TREK_HOST_CANDIDATE_API
#elif defined(_WIN32)
# if defined(TREK_HOST_BUILD)
#  define TREK_HOST_CANDIDATE_API __declspec(dllexport)
# else
#  define TREK_HOST_CANDIDATE_API __declspec(dllimport)
# endif
#else
# define TREK_HOST_CANDIDATE_API __attribute__((visibility("default")))
#endif

namespace trek::host::detail {

struct AcademyCreationIntent;
struct AcademyCreationReceipt;
using AcademyIntent = std::shared_ptr<const AcademyCreationIntent>;
using AcademyReceipt = std::shared_ptr<const AcademyCreationReceipt>;

struct AcademyCreationResult {
    Error error = Error::OK;
    Generation generation;
    AcademyReceipt receipt;
};

struct AcademyCandidateView {
    std::string campaign_id, display_name, source_digest;
    std::uint64_t person = 0, creation_fact = 0, revision = 0, tick = 0;
    std::size_t person_count = 0, creation_fact_count = 0, population_count = 0;
    std::vector<std::string> background;
};

struct AcademyCandidateResult {
    Error error = Error::OK;
    std::optional<AcademyCandidateView> candidate;
};

// Private entry point for native HOST composition. Only the JSON payload comes
// from the caller's editable input. Keep intent and receipt inside HOST.
class AcademyCandidateFactory final {
public:
    TREK_HOST_CANDIDATE_API static AcademyIntent begin(SessionOwner&);
    TREK_HOST_CANDIDATE_API static std::future<AcademyCreationResult> create(
        SessionOwner&, const AcademyIntent&, std::string_view payload);
    TREK_HOST_CANDIDATE_API static std::future<AcademyCandidateResult> inspect(
        SessionOwner&, const AcademyReceipt&);
};

} // namespace trek::host::detail

#undef TREK_HOST_CANDIDATE_API
