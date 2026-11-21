#pragma once

#include <cstdint>
#include <string>
#include <string_view>

namespace trek::host::detail {

inline constexpr std::string_view academy_catalog_version = "startrek.academy:starfleet_academy/v2 2.0.0";
inline constexpr std::string_view academy_source_version =
    "s04_fixed_player_protagonist/2.0.0/s04_player_khan_vulcan_male/1.0.0";

struct AcademyAnchor {
    std::uint64_t person = 0, creation_fact = 0;
    std::string profile, source_digest, catalog_digest, name_digest;
    bool operator==(const AcademyAnchor&) const = default;
};

struct AcademySnapshotIdentity {
    AcademyAnchor anchor;
    std::uint64_t revision = 0, clock = 0;
    bool operator==(const AcademySnapshotIdentity&) const = default;
};

std::string academy_digest_hex(std::string_view bytes);

} // namespace trek::host::detail
