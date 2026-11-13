#pragma once

#include "trek/host/session_owner.h"

#include <stdexcept>
#include <string_view>

namespace test {
using namespace trek::host;

inline void require(bool condition, const char* message)
{
    if (!condition) {
        throw std::runtime_error(message);
    }
}

inline void expect(Result result, Error error)
{
    if (result.error != error) {
        throw std::runtime_error("Expected HOST error " + std::to_string(static_cast<int>(error))
                                 + ", received " + std::to_string(static_cast<int>(result.error)));
    }
    if (error != Error::OK) {
        require(result.generation == Generation{}, "Error exposed a generation");
    }
}

inline PopulationConfig population()
{
    return {"miranda", 65001, 404, 8, 2, 1, 16};
}

inline Generation open(SessionOwner& owner)
{
    const auto result = owner.open(population()).get();
    expect(result, Error::OK);
    require(result.generation != Generation{}, "Open did not assign a generation");
    const auto snapshot = owner.snapshot();
    require(snapshot.state == State::ACTIVE && snapshot.generation == result.generation,
            "Open did not publish an active session");
    return result.generation;
}

inline void closed(SessionOwner& owner)
{
    const auto snapshot = owner.snapshot();
    require(snapshot.state == State::CLOSED && snapshot.generation == Generation{},
            "Owner did not return to CLOSED");
}

struct Case {
    std::string_view name;
    void (*run)();
};

void run_player_case(std::string_view name);

} // namespace test
