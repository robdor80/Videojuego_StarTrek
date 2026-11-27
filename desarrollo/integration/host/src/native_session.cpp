#include "native_session.h"

#include "f05_orders.h"

#include <atomic>
#include <exception>
#include <string_view>

namespace trek::host::detail {
#ifdef TREK_HOST_GATEWAY_TESTING
void gateway_test_after_bind();
void gateway_test_after_dispatch(F04Session*, std::uint32_t&);
void gateway_test_after_clock(F04Session*);
#endif
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
    if (session_ || reserved_ || staged_ || academy_) {
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

Outcome NativeSession::commit_academy(std::unique_ptr<AcademyCampaign> staged) noexcept
{
    if (!staged || reserved_ || session_ || staged_ || academy_) return {Error::INTERNAL_ERROR};
    bool available = false;
    if (!campaign_reserved.compare_exchange_strong(available, true)) return {Error::BUSY_STATE};
    reserved_ = true;
    academy_ = std::move(staged);
    return {};
}

Outcome NativeSession::probe() const noexcept
{
    if (academy_) return {};
    return normalize(bridge::probe(session_));
}

Outcome NativeSession::resolve_person(std::uint64_t person_id, F04Ref& person,
                                      std::uint64_t& revision) const noexcept
{
    return normalize_identity(bridge::resolve_person(session_, person_id, person, revision));
}

Outcome NativeSession::bind_player(F04Ref person, std::uint64_t revision) noexcept
{
    const auto outcome = normalize_identity(bridge::bind_player(session_, person, revision));
#ifdef TREK_HOST_GATEWAY_TESTING
    gateway_test_after_bind();
#endif
    return outcome;
}

Outcome NativeSession::dispatch(F04Ref player, const GatewayRequest& request, OperationResult& reply) noexcept
{
    if (request.operation == GatewayOp::INSTITUTIONAL) return {Error::SERVICE_UNAVAILABLE};
    auto code = bridge::dispatch(session_, player, request, reply);
#ifdef TREK_HOST_GATEWAY_TESTING
    gateway_test_after_dispatch(session_, code);
#endif
    return normalize_identity(code);
}

Outcome NativeSession::events(F04Ref player, std::uint64_t order, std::uint64_t after,
                              NativeEventPage& page) noexcept
{
    if (academy_ || !session_) return {Error::ACCESS_DENIED};
    return normalize_identity(bridge::events(session_, player, order, after, page));
}

Outcome NativeSession::advance(F04Ref player, const ClockIntent& request,
                              NativeClockReport& report) noexcept
{
    report = {};
    if (academy_ || !session_) return {Error::SERVICE_UNAVAILABLE};
    const auto outcome = normalize_identity(bridge::advance(session_, player, request, report));
#ifdef TREK_HOST_GATEWAY_TESTING
    gateway_test_after_clock(session_);
#endif
    return outcome;
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
    if (academy_) return {Error::SAVE_INCOMPATIBLE};
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
    academy_.reset();
    if (reserved_) {
        reserved_ = false;
        campaign_reserved.store(false);
    }
    return {};
}

} // namespace trek::host::detail
