// H02/H03 fault executable substitutes the bridge. Its historical oracles stay intact.
#include "native_session.h"
namespace trek::host::detail::bridge {
std::uint32_t dispatch(F04Session*, F04Ref, const GatewayRequest&, OperationResult&) noexcept
{
    return F04_INTERNAL;
}

// Test-only bridge denies H08 reads: historical lifecycle fault tests should
// not require F05/Core linkage or a fabricated authoritative event.
std::uint32_t events(F04Session*, F04Ref, std::uint64_t, std::uint64_t,
                     NativeEventPage& page) noexcept
{
    page = {};
    return F04_INTERNAL;
}
// The H02/H03 fake bridge must never make a second clock or invent activity.
std::uint32_t advance(F04Session*, F04Ref, const ClockIntent&, NativeClockReport& report) noexcept
{
    report = {};
    return F04_INTERNAL;
}
}
