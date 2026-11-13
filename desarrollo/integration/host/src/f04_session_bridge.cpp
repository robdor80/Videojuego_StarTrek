#include "native_session.h"

#include "f05_initiative.h"

namespace trek::host::detail::bridge {

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

} // namespace trek::host::detail::bridge
