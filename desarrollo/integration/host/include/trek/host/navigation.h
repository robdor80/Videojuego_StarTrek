#pragma once

#include <cstdint>
#include <optional>
#include <string>
#include <vector>

namespace trek::host {

// Trusted native campaign authoring. Crew ordinals are zero-based and resolved
// during bootstrap. The publication ID includes the revision of its source data.
struct ChartKnowledge {
    std::uint64_t crew_ordinal = 0;
    bool knows_own_location = false;
    bool knows_chart = false;
    std::vector<std::string> places, edges;
};
struct NavalBootstrap {
    std::optional<std::string> origin;
    std::optional<std::string> chart_publication;
    std::vector<ChartKnowledge> observers;
};

struct ChartPlace {
    std::string id, name, type;
    std::optional<double> z_ly;
    std::vector<std::string> sources;
};
struct ChartEdge {
    std::string id, origin, destination, confidence, distance_relation, derivation, traversal;
    std::vector<std::string> sources;
    std::optional<double> distance_ly;
    bool directional = false;
};
struct NavigationRevision {
    std::uint64_t core = 0, position = 0, knowledge = 0, tick = 0;
    std::string chart;
    bool operator==(const NavigationRevision&) const = default;
};
struct NavigationView {
    NavigationRevision revision;
    std::optional<ChartPlace> location;
    std::vector<ChartPlace> places;
    std::vector<ChartEdge> edges;
};
struct RouteIntent {
    std::string destination, profile;
    NavigationRevision expected;
};
struct RouteProposal {
    std::uint64_t reference = 0;
    NavigationRevision revision;
    std::string destination, profile;
    std::vector<ChartEdge> legs;
    std::optional<double> distance_ly, eta;
    bool profile_data_incomplete = true;
};
enum class NavigationStatus {
    OK, LOCATION_UNKNOWN, CHART_UNAVAILABLE, DESTINATION_UNKNOWN_OR_REDACTED,
    CLARIFICATION_REQUIRED, NO_KNOWN_ROUTE, INVALID_PROFILE
};
} // namespace trek::host
