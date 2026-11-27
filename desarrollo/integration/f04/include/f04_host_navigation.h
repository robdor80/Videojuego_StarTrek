#pragma once

#include "f04_bridge.h"
#include "trek/host/navigation.h"

// C++ bridge private to the native HOST composition.
namespace trek::host::nav_bridge {
F04_API std::uint32_t create(const char*, const F04PopulationConfig&,
                             const NavalBootstrap&, F04Session**) noexcept;
F04_API std::uint32_t read(F04Session*, F04Ref, NavigationView&) noexcept;
#ifdef F04_HOST_NAVIGATION_TESTING
F04_API std::uint32_t revoke_chart(F04Session*, F04Ref) noexcept;
#endif
}
