#pragma once

#include "f04_bridge.h"
#include "trek/host/session_owner.h"

#include <utility>

#if defined(TREK_HOST_STATIC_TEST)
# define TREK_HOST_BOOTSTRAP_API
#elif defined(_WIN32)
# if defined(TREK_HOST_BUILD)
#  define TREK_HOST_BOOTSTRAP_API __declspec(dllexport)
# else
#  define TREK_HOST_BOOTSTRAP_API __declspec(dllimport)
# endif
#else
# define TREK_HOST_BOOTSTRAP_API __attribute__((visibility("default")))
#endif

namespace trek::host {
namespace detail {
// Identity of a newly opened local campaign for this activation. H04 will
// supply durable campaign identity from the admitted slot.
struct ActiveCampaign final {};
}

class PlayerSelection final {
private:
    friend class SessionOwner;
    PlayerSelection(const std::shared_ptr<const detail::ActiveCampaign>& campaign, F04Ref person)
        : campaign_(campaign), person_(person) {}

    std::weak_ptr<const detail::ActiveCampaign> campaign_;
    F04Ref person_;
};

struct PlayerSelectionResult {
    Error error;
    std::optional<std::uint32_t> domain_code = std::nullopt;
    std::optional<PlayerSelection> selection = std::nullopt;
    std::uint64_t revision = 0;
};

struct BindPlayerResult {
    Error error;
    std::optional<std::uint32_t> domain_code = std::nullopt;
};

// Private C++ entry point for the trusted local character creation flow.
// created_person is an output of that flow. Never forward client payloads
// here or expose this header to UI, Blueprint, NPC or AI adapters.
class PlayerBootstrap final {
public:
    TREK_HOST_BOOTSTRAP_API static std::future<PlayerSelectionResult> prepare(
        SessionOwner& owner, Generation generation, std::uint64_t created_person);
    TREK_HOST_BOOTSTRAP_API static std::future<BindPlayerResult> bind(
        SessionOwner& owner, Generation generation, const PlayerSelection& selection,
        std::uint64_t expected_revision);
};

} // namespace trek::host

#undef TREK_HOST_BOOTSTRAP_API
