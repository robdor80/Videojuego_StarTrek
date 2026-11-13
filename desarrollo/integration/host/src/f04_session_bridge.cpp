#include "native_session.h"

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

} // namespace trek::host::detail::bridge
