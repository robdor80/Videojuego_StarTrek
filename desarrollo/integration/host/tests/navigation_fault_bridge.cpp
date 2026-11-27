#include "native_session.h"

namespace trek::host::detail::bridge {
// The legacy lifecycle fault executable has no actual campaign or chart.
std::uint32_t create(const PopulationConfig&, F04Session**) noexcept;

std::uint32_t create(const PopulationConfig& config, const NavalBootstrap& bootstrap, F04Session** session) noexcept
{
    if (bootstrap.origin || bootstrap.chart_publication || !bootstrap.observers.empty())
        return F04_ARGUMENT;
    return create(config, session);
}

std::uint32_t read_navigation(F04Session*, F04Ref, NavigationView&) noexcept
{
    return F04_DENIED;
}
}
