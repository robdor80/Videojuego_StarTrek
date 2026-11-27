#pragma once

#include "trek/host/navigation.h"

namespace trek::host::detail {
const char* chart_publication() noexcept;
NavigationStatus solve_route(const NavigationView&, const RouteIntent&,
                             std::vector<ChartPlace>& candidates, RouteProposal& proposal);
}
