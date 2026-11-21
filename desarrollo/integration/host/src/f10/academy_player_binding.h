#pragma once

#include "academy_candidate_factory.h"

#if defined(TREK_HOST_STATIC_TEST)
# define TREK_HOST_ACADEMY_BINDING_API
#elif defined(_WIN32)
# if defined(TREK_HOST_BUILD)
#  define TREK_HOST_ACADEMY_BINDING_API __declspec(dllexport)
# else
#  define TREK_HOST_ACADEMY_BINDING_API __declspec(dllimport)
# endif
#else
# define TREK_HOST_ACADEMY_BINDING_API __attribute__((visibility("default")))
#endif

namespace trek::host::detail {

// Private H03 entry point for native HOST composition, using only B02 authority.
class AcademyPlayerBinding final {
public:
    TREK_HOST_ACADEMY_BINDING_API static std::future<Result> bind(
        SessionOwner&, Generation, const AcademyReceipt&);
    TREK_HOST_ACADEMY_BINDING_API static std::future<AcademyCandidateResult> inspect(
        SessionOwner&, Generation);
};

#ifdef TREK_HOST_ACADEMY_TESTING
void set_academy_bind_test_hook(void (*hook)()) noexcept;
#endif

} // namespace trek::host::detail

#undef TREK_HOST_ACADEMY_BINDING_API
