#pragma once

#include "trek/host/academy_abi.h"

// Kept independent of Unreal so product SDK checks can exercise the loader's
// exact negotiation policy without loading the engine.
struct FHostAcademyApi
{
    TrekHostCode Availability = TREK_HOST_SERVICE_UNAVAILABLE;
    decltype(&trek_host_academy_submit) Submit = nullptr;
    decltype(&trek_host_academy_poll) Poll = nullptr;

    template <typename FResolve>
    static FHostAcademyApi Negotiate(FResolve Resolve)
    {
        const auto Version = reinterpret_cast<decltype(&trek_host_academy_version)>(
            Resolve("trek_host_academy_version"));
        const auto Submit = reinterpret_cast<decltype(&trek_host_academy_submit)>(
            Resolve("trek_host_academy_submit"));
        const auto Poll = reinterpret_cast<decltype(&trek_host_academy_poll)>(
            Resolve("trek_host_academy_poll"));
        if (!Version || !Submit || !Poll)
        {
            return {};
        }
        const auto AvailableVersion = Version();
        if (AvailableVersion == 0)
        {
            return {};
        }
        if (AvailableVersion != TREK_HOST_ACADEMY_VERSION)
        {
            return {TREK_HOST_ABI_MISMATCH};
        }
        return {TREK_HOST_OK, Submit, Poll};
    }
};
