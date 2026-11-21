#pragma once
#include "f10/academy_identity.h"
#include "trek/host/session_owner.h"
#include <array>
#include <filesystem>
#include <functional>
#include <memory>
#include <utility>
#include <variant>

namespace trek::host::detail {
using CampaignId = std::array<std::uint8_t,16>;
struct PersistentIdentity {
    std::uint64_t person=0, record=0, revision=0, tick=0;
    bool operator==(const PersistentIdentity&) const = default;
};
using SlotIdentity = std::variant<PersistentIdentity, AcademySnapshotIdentity>;
std::string new_campaign_id();
CampaignId decode_campaign(const std::string&);
bool valid_slot(const std::string&);
struct StorageFailure { Error error; };
// Pins every path component. Linux operations use the pinned directory descriptor;
// Windows handles deny deletion/rename and reject all reparse points.
class PinnedDirectory final {
public:
    explicit PinnedDirectory(const std::filesystem::path&);
    ~PinnedDirectory();
    std::filesystem::path path() const;
private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};
struct PreparedSlot {
    std::shared_ptr<PinnedDirectory> history;
    SlotIdentity identity;
    std::string campaign;
};
// Private keyset position. Empty slot marks a completed campaign; version 0
// marks a completed slot. An entirely empty position starts a fresh walk.
struct SlotPosition {
    std::string campaign, slot;
    std::uint64_t version = 0;
    bool operator==(const SlotPosition&) const = default;
};
struct SlotPage {
    InspectionResult inspection;
    std::optional<SlotPosition> next;
};
// Branch an existing archive into a new, private snapshot destination.
void copy_history(const std::filesystem::path& source, const std::filesystem::path& destination);
class SlotStore final {
public:
    explicit SlotStore(StorageConfig config) : config_(std::move(config)) {}
    bool configured() const noexcept { return !config_.root.empty(); }
    Error save(const std::string& campaign,const std::string& slot,SlotIdentity identity,
               const std::function<Error(const std::filesystem::path&)>& snapshot,
               const std::function<Error(const PreparedSlot&)>& verify) const;
    PreparedSlot prepare(SlotAddress address) const;
    InspectionResult inspect(const std::function<Error(const PreparedSlot&)>& verify = {},
                             std::size_t limit = 10000) const;
    SlotPage inspect_page(const SlotPosition& after,
                         const std::function<Error(const PreparedSlot&)>& verify) const;
private:
    StorageConfig config_;
};
#if defined(TREK_HOST_PERSISTENCE_TESTING) || defined(TREK_HOST_ACADEMY_TESTING)
void storage_test_hook(std::function<void(const char*)> hook);
void storage_test_event(const char*);
#endif
} // namespace trek::host::detail
