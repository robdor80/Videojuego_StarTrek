#include "native_session.h"

#include "f05_orders.h"

#include <atomic>
#include <exception>
#include <string_view>

namespace trek::host::detail {
namespace {

// The reservation covers initialization and any failed destruction.
constinit std::atomic_bool campaign_reserved{false};

Outcome normalize(std::uint32_t code) noexcept
{
    switch (code) {
    case F04_OK: return {};
    case F04_ARGUMENT: return {Error::INVALID_ARGUMENT, code};
    case F04_THREAD: return {Error::WRONG_THREAD, code};
    case F04_CAPACITY: return {Error::CAPACITY_LIMIT, code};
    case F04_INTERNAL: return {Error::INTERNAL_ERROR, code};
    default: return {Error::DOMAIN_REJECTED, code};
    }
}

Outcome normalize_identity(std::uint32_t code) noexcept
{
    switch (code) {
    case F04_SCOPE: return {Error::SCOPE_INVALID, code};
    case F04_DENIED: return {Error::ACCESS_DENIED, code};
    case F04_REVIEW:
    case F04_STALE: return {Error::REVISION_STALE, code};
    case F05_IDEMPOTENCY_CONFLICT: return {Error::IDEMPOTENCY_CONFLICT, code};
    default: return normalize(code);
    }
}

} // namespace

NativeSession::~NativeSession() noexcept
{
    if (session_ || reserved_ || staged_) {
        std::terminate();
    }
}

Outcome NativeSession::open(const PopulationConfig& config) noexcept
{
    bool available = false;
    if (!campaign_reserved.compare_exchange_strong(available, true)) {
        return {Error::BUSY_STATE};
    }
    reserved_ = true;

    const auto* sha = bridge::core_sha();
    if (!sha || std::string_view(sha) != TREK_HOST_CORE_SHA) {
        return {Error::INTERNAL_ERROR};
    }
    const auto created = normalize(bridge::create(config, &session_));
    if (created.error != Error::OK) {
        return created;
    }
    if (!session_) {
        return {Error::INTERNAL_ERROR};
    }
    return probe();
}

Outcome NativeSession::probe() const noexcept
{
    return normalize(bridge::probe(session_));
}

Outcome NativeSession::resolve_person(std::uint64_t person_id, F04Ref& person,
                                      std::uint64_t& revision) const noexcept
{
    return normalize_identity(bridge::resolve_person(session_, person_id, person, revision));
}

Outcome NativeSession::bind_player(F04Ref person, std::uint64_t revision) noexcept
{
    return normalize_identity(bridge::bind_player(session_, person, revision));
}

Outcome NativeSession::persistent_identity(PersistentIdentity& identity,F04Ref& player) const noexcept
{
    return normalize(bridge::persistent_identity(session_,identity,player));
}
Outcome NativeSession::snapshot(const std::filesystem::path& path,const CampaignId& id) noexcept
{
    return normalize(bridge::snapshot(session_,path,id));
}
Outcome NativeSession::stage(const PreparedSlot& slot,F04Ref& player) noexcept
{
    if(staged_)return {Error::BUSY_STATE};
    const auto* sha=bridge::core_sha();if(!sha || std::string_view(sha)!=TREK_HOST_CORE_SHA)return {Error::INTERNAL_ERROR};
    const auto result=normalize(bridge::restore(slot,&staged_,player));
    if(result.error==Error::OK)staged_pin_=slot.history;
    return result;
}
Outcome NativeSession::discard_stage() noexcept
{
    if(staged_){auto result=normalize(bridge::destroy(staged_));if(result.error!=Error::OK)return result;staged_=nullptr;}
    staged_pin_.reset();return {};
}
Outcome NativeSession::commit_stage() noexcept
{
    if(!staged_)return {Error::INTERNAL_ERROR};
    if(!reserved_) {
        bool available=false;
        if(!campaign_reserved.compare_exchange_strong(available,true))return {Error::BUSY_STATE};
        reserved_=true;
    }
    if(session_){auto result=normalize(bridge::destroy(session_));if(result.error!=Error::OK)return result;}
    session_=staged_;staged_=nullptr;history_pin_=std::move(staged_pin_);return {};
}
Outcome NativeSession::close() noexcept
{
    const auto stage_result=discard_stage();if(stage_result.error!=Error::OK)return stage_result;
    if (session_) {
        const auto destroyed = normalize(bridge::destroy(session_));
        if (destroyed.error != Error::OK) {
            return destroyed;
        }
        session_ = nullptr;
    }
    history_pin_.reset();
    if (reserved_) {
        reserved_ = false;
        campaign_reserved.store(false);
    }
    return {};
}

} // namespace trek::host::detail
