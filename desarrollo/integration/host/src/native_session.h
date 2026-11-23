#pragma once

#include "f04_bridge.h"
#include "f10/academy_campaign.h"
#include "trek/host/session_owner.h"

#include <optional>
#include "slot_store.h"
#include "gateway.h"

namespace trek::host::detail {

struct Outcome {
    Error error = Error::OK;
    std::optional<std::uint32_t> domain_code = std::nullopt;
};

struct NativeEventPage {
    EventNotice events[16]{};
    std::uint64_t written = 0;
    bool more = false;
};

// Called exclusively by the owner thread, including destruction.
class NativeSession final {
public:
    NativeSession() = default;
    ~NativeSession() noexcept;

    NativeSession(const NativeSession&) = delete;
    NativeSession& operator=(const NativeSession&) = delete;

    Outcome open(const PopulationConfig& config) noexcept;
    Outcome close() noexcept;
    Outcome commit_academy(std::unique_ptr<AcademyCampaign>) noexcept;
    const AcademyCampaign* academy() const noexcept { return academy_.get(); }
    Outcome persistent_identity(PersistentIdentity& identity,F04Ref& player) const noexcept;
    Outcome snapshot(const std::filesystem::path&,const CampaignId&) noexcept;
    Outcome stage(const PreparedSlot&,F04Ref& player) noexcept;
    Outcome discard_stage() noexcept;
    Outcome commit_stage() noexcept;
    Outcome probe() const noexcept;
    Outcome resolve_person(std::uint64_t person_id, F04Ref& person, std::uint64_t& revision) const noexcept;
    Outcome bind_player(F04Ref person, std::uint64_t revision) noexcept;
    Outcome dispatch(F04Ref player, const GatewayRequest&, OperationResult&) noexcept;
    // Revalidates the F05-bound local principal on each authorized source read.
    Outcome events(F04Ref player, std::uint64_t order, std::uint64_t after,
                   NativeEventPage& page) noexcept;
#ifdef TREK_HOST_GATEWAY_TESTING
    void test_visit(const std::function<void(F04Session*)>& visit) { visit(session_); }
#endif

private:
    std::unique_ptr<AcademyCampaign> academy_;
    F04Session* session_ = nullptr;
    bool reserved_ = false;
    F04Session* staged_ = nullptr;
    std::shared_ptr<PinnedDirectory> history_pin_,staged_pin_;
};

namespace bridge {
std::uint32_t dispatch(F04Session*, F04Ref, const GatewayRequest&, OperationResult&) noexcept;
std::uint32_t events(F04Session*, F04Ref, std::uint64_t order,
                     std::uint64_t after, NativeEventPage& page) noexcept;
const char* core_sha() noexcept;
std::uint32_t persistent_identity(F04Session*,PersistentIdentity&,F04Ref&) noexcept;
std::uint32_t snapshot(F04Session*,const std::filesystem::path&,const CampaignId&) noexcept;
std::uint32_t restore(const PreparedSlot&,F04Session**,F04Ref&) noexcept;
std::uint32_t create(const PopulationConfig& config, F04Session** session) noexcept;
std::uint32_t probe(F04Session* session) noexcept;
std::uint32_t destroy(F04Session* session) noexcept;
std::uint32_t resolve_person(F04Session* session, std::uint64_t person_id,
                             F04Ref& person, std::uint64_t& revision) noexcept;
std::uint32_t bind_player(F04Session* session, F04Ref person, std::uint64_t revision) noexcept;
}

} // namespace trek::host::detail
