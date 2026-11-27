#include "route_solver.h"
#include "nav_chart_data.h"

#include <algorithm>
#include <map>
#include <queue>
#include <string_view>

namespace trek::host::detail {
namespace {
bool same_destination(std::string_view a, std::string_view b) {
    const auto fold = [](char c) { return c >= 'A' && c <= 'Z' ? c + ('a' - 'A') : c; };
    return std::ranges::equal(a, b, [&](char x, char y) { return fold(x) == fold(y); });
}

int uncertainty(const ChartEdge& edge) {
    const auto confidence = edge.confidence == "HIGH" ? 0 :
        edge.confidence == "MEDIUM" ? 1 : edge.confidence == "LOW" ? 2 : 3;
    return confidence + (edge.distance_ly ? 0 : 1);
}
}

const char* chart_publication() noexcept { return chart_data::publication; }

NavigationStatus solve_route(const NavigationView& view, const RouteIntent& intent,
                             std::vector<ChartPlace>& candidates, RouteProposal& proposal) {
    if (!view.location) return NavigationStatus::LOCATION_UNKNOWN;
    if (view.revision.chart.empty()) return NavigationStatus::CHART_UNAVAILABLE;
    const auto profile = std::ranges::find_if(chart_data::profiles,
        [&](const auto& p) { return p.id == intent.profile; });
    if (profile == std::ranges::end(chart_data::profiles)) return NavigationStatus::INVALID_PROFILE;

    const ChartPlace* destination = nullptr;
    for (const auto& place : view.places) {
        if (place.id == intent.destination) {
            destination = &place;
            break;
        }
        if (same_destination(place.name, intent.destination)) candidates.push_back(place);
    }
    if (!destination && candidates.empty()) return NavigationStatus::DESTINATION_UNKNOWN_OR_REDACTED;
    if (!destination && candidates.size() > 1) return NavigationStatus::CLARIFICATION_REQUIRED;
    const auto goal = destination ? destination->id : candidates.front().id;
    candidates.clear();
    const auto& origin = view.location->id;
    if (std::ranges::find(view.places, origin, &ChartPlace::id) == view.places.end())
        return NavigationStatus::NO_KNOWN_ROUTE;

    struct Arrival {
        double score = 0;
        const ChartEdge* edge = nullptr;
        std::string_view previous;
    };
    using Frontier = std::pair<double, std::string_view>;
    std::priority_queue<Frontier, std::vector<Frontier>, std::greater<>> frontier;
    std::map<std::string_view, Arrival> arrivals;
    arrivals.emplace(origin, Arrival{});
    frontier.emplace(0, origin);
    while (!frontier.empty()) {
        const auto [score, from] = frontier.top();
        frontier.pop();
        if (score != arrivals.at(from).score) continue;
        if (from == goal) break;
        for (const auto& edge : view.edges) {
            if (!edge.traversal.empty()) continue;
            std::string_view to;
            if (edge.origin == from) to = edge.destination;
            else if (!edge.directional && edge.destination == from) to = edge.origin;
            else continue;
            // Travel time, hazards, political exposure and support have no inputs in this publication.
            const double next = score + 1 + profile->uncertainty_weight * uncertainty(edge);
            const auto existing = arrivals.find(to);
            if (existing != arrivals.end() && existing->second.score <= next) continue;
            arrivals.insert_or_assign(to, Arrival{next, &edge, from});
            frontier.emplace(next, to);
        }
    }
    if (!arrivals.contains(goal)) return NavigationStatus::NO_KNOWN_ROUTE;

    proposal.revision = view.revision;
    proposal.destination = goal;
    proposal.profile = intent.profile;
    for (std::string_view at = goal; at != origin;) {
        const auto& arrival = arrivals.at(at);
        auto leg = *arrival.edge;
        if (leg.origin != arrival.previous) std::swap(leg.origin, leg.destination);
        proposal.legs.push_back(std::move(leg));
        at = arrival.previous;
    }
    std::ranges::reverse(proposal.legs);
    // Bounds and ranges cannot be added as point estimates. Keep their authored
    // relation and confidence on each leg even when there is no aggregate.
    if (!proposal.legs.empty() && std::ranges::all_of(proposal.legs, [](const auto& leg) {
        return leg.distance_ly && (leg.distance_relation == "exact" || leg.distance_relation == "approximate");
    })) {
        double distance = 0;
        for (const auto& leg : proposal.legs) distance += *leg.distance_ly;
        proposal.distance_ly = distance;
    }
    return NavigationStatus::OK;
}
}
