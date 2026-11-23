#include "native_session.h"

#include "f05_player_binding.h"
#include "f04_host_persistence.h"
#ifdef F11_HOST_READ_ONLY
#include "f11_host_reader.h"
#endif

#ifdef TREK_HOST_PERSISTENCE_TESTING
namespace trek::host::detail { void persistence_test_observe(F04Session*,bool); }
#endif
namespace trek::host::detail::bridge {

std::uint32_t persistent_identity(F04Session* session,PersistentIdentity& identity,F04Ref& player) noexcept
{
    identity={};player={};F05PlayerBinding binding{};
    auto code=f05_player_binding(session,&binding);if(code!=F04_OK)return code;
    if(!binding.record || !binding.person.id)return F04_DENIED;
    identity={binding.person.id,binding.record,binding.input_revision,binding.tick};player=binding.person;return F04_OK;
}
std::uint32_t snapshot(F04Session* session,const std::filesystem::path& path,const CampaignId& id) noexcept
{
    try {
#ifdef TREK_HOST_PERSISTENCE_TESTING
        persistence_test_observe(session,true);
#endif
        auto text=path.u8string();return f04_history_snapshot(session,reinterpret_cast<const char*>(text.c_str()),id.data(),id.size());}
    catch(...){return F04_SAVE;}
}
std::uint32_t restore(const PreparedSlot& slot,F04Session** out,F04Ref& player) noexcept
{
    *out=nullptr;player={};F04Session* candidate=nullptr;
    const auto* expected = std::get_if<PersistentIdentity>(&slot.identity);
    if (!expected) return F04_SAVE;
    try {
        auto code=f04_create(1,"miranda",&candidate);
        if(code!=F04_OK)return code;
        auto text=slot.history->path().u8string();code=f04_history_open(candidate,reinterpret_cast<const char*>(text.c_str()));
        PersistentIdentity actual{};CampaignId id{};F04Ref resolved{};
        if(code==F04_OK)code=f04_history_identity(candidate,id.data(),id.size());
        if(code==F04_OK && id!=decode_campaign(slot.campaign))code=F04_DENIED;
        if(code==F04_OK)code=persistent_identity(candidate,actual,resolved);
        if(code==F04_OK && actual!=*expected)code=F04_DENIED;
        if(code==F04_OK){
#ifdef TREK_HOST_PERSISTENCE_TESTING
            persistence_test_observe(candidate,false);
#endif
            *out=candidate;player=resolved;return F04_OK;}
        f04_destroy(candidate);return code;
    } catch(...) {if(candidate)f04_destroy(candidate);return F04_SAVE;}
}

const char* core_sha() noexcept
{
    return f04_core_sha();
}

std::uint32_t create(const PopulationConfig& config, F04Session** session) noexcept
{
    const F04PopulationConfig population{
        config.ship_identity, config.seed, config.crew,
        config.residents, config.passengers, config.maximum
    };
    constexpr std::uint32_t f04_abi = 1;
    return f04_create_population(f04_abi, config.class_id.c_str(), &population, session);
}

std::uint32_t probe(F04Session* session) noexcept
{
#ifdef TREK_HOST_PERSISTENCE_TESTING
    storage_test_event("probe");
#endif
    F04PopulationStats stats{};
    return f04_population_stats(session, &stats);
}

std::uint32_t destroy(F04Session* session) noexcept
{
    return f04_destroy(session);
}

std::uint32_t resolve_person(F04Session* session, std::uint64_t person_id,
                             F04Ref& person, std::uint64_t& revision) noexcept
{
    person = {};
    revision = 0;
    F04Handles handles{};
    if (const auto code = f04_handles(session, &handles); code != F04_OK) {
        return code;
    }
    F04Person view{};
    if (const auto code = f04_person(session, handles.captain, person_id, &view); code != F04_OK) {
        return code;
    }
    F04Stats stats{};
    if (const auto code = f04_stats(session, &stats); code != F04_OK) {
        return code;
    }
    person = {handles.ship.scope, view.id};
    revision = stats.revision;
    return F04_OK;
}

std::uint32_t bind_player(F04Session* session, F04Ref person, std::uint64_t revision) noexcept
{
    return f05_bind_player(session, person, revision);
}

#ifdef F11_HOST_READ_ONLY
namespace {
Outcome read_error(std::uint32_t code) noexcept
{
    switch (code) {
    case F04_SCOPE: return {Error::SCOPE_INVALID, code};
    case F04_THREAD: return {Error::WRONG_THREAD, code};
    case F11_UNCOMMISSIONED: return {Error::DOMAIN_REJECTED, code};
    case F04_DENIED:
    case F04_ARGUMENT: // An unknown event and another person's event disclose the same result.
    case F11_IDENTITY: return {Error::ACCESS_DENIED, code};
    default: return {Error::INTERNAL_ERROR, code};
    }
}
} // namespace

Outcome institutional_read(F04Session* session, F04Ref player, const InstitutionalRequest& request,
                           std::optional<InstitutionalViewV1>& view) noexcept
{
    view.reset();
    F05PlayerBinding binding{};
    const auto binding_code = f05_player_binding(session, &binding);
    if (binding_code != F04_OK) return read_error(binding_code);
    if (!binding.record || binding.person.id != player.id) return {Error::ACCESS_DENIED};
    if (binding.person.scope != player.scope) return {Error::SCOPE_INVALID};

    if (request.kind == InstitutionalKind::CAREER) {
        f11_host::Career career{};
        const auto code = f11_host::career(session, binding.person, &career);
        if (code != F04_OK) return read_error(code);
        view = InstitutionalViewV1{career.world_revision,
            CareerViewV1{career.rank_event, career.rank, career.service_status}};
        return {};
    }

    if (!request.event_id) return {Error::INVALID_ARGUMENT};
    f11_host::Promotion promotion{};
    const auto code = f11_host::promotion(session, binding.person, request.event_id, &promotion);
    if (code != F04_OK) return read_error(code);
    // The reader carries the original commit revision. Read the current Core
    // revision on the same owner turn, without touching time or history.
    F04Stats stats{};
    if (const auto status = f04_stats(session, &stats); status != F04_OK) return read_error(status);
    view = InstitutionalViewV1{stats.revision, PromotionViewV1{promotion.promotion_event,
        promotion.effective_tick, promotion.original_revision, promotion.from_rank, promotion.to_rank}};
    return {};
}
#else
Outcome institutional_read(F04Session*, F04Ref, const InstitutionalRequest&,
                           std::optional<InstitutionalViewV1>& view) noexcept
{
    view.reset();
    return {Error::SERVICE_UNAVAILABLE};
}
#endif

} // namespace trek::host::detail::bridge
