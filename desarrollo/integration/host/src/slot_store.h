#pragma once
#include "trek/host/session_owner.h"
#include <array>
#include <filesystem>
#include <functional>
#include <memory>
#include <utility>

namespace trek::host::detail {
using CampaignId = std::array<std::uint8_t,16>;
struct PersistentIdentity {
    std::uint64_t person=0, record=0, revision=0, tick=0;
    bool operator==(const PersistentIdentity&) const = default;
};
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
    PersistentIdentity identity;
    std::string campaign;
};
class SlotStore final {
public:
    explicit SlotStore(StorageConfig config) : config_(std::move(config)) {}
    Error save(const std::string& campaign,const std::string& slot,PersistentIdentity identity,
               const std::function<Error(const std::filesystem::path&)>& snapshot,
               const std::function<Error(const PreparedSlot&)>& verify) const;
    PreparedSlot prepare(SlotAddress address) const;
    InspectionResult inspect(const std::function<Error(const PreparedSlot&)>& verify = {}) const;
private:
    StorageConfig config_;
};
#ifdef TREK_HOST_PERSISTENCE_TESTING
void storage_test_hook(std::function<void(const char*)> hook);
void storage_test_event(const char*);
#endif
} // namespace trek::host::detail
