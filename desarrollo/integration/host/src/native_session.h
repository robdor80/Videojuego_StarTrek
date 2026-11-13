#pragma once

#include "f04_bridge.h"
#include "trek/host/session_owner.h"

#include <optional>

namespace trek::host::detail {

struct Outcome {
    Error error = Error::OK;
    std::optional<std::uint32_t> domain_code = std::nullopt;
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
    Outcome probe() const noexcept;
    Outcome resolve_person(std::uint64_t person_id, F04Ref& person, std::uint64_t& revision) const noexcept;
    Outcome bind_player(F04Ref person, std::uint64_t revision) noexcept;

private:
    F04Session* session_ = nullptr;
    bool reserved_ = false;
};

namespace bridge {
const char* core_sha() noexcept;
std::uint32_t create(const PopulationConfig& config, F04Session** session) noexcept;
std::uint32_t probe(F04Session* session) noexcept;
std::uint32_t destroy(F04Session* session) noexcept;
std::uint32_t resolve_person(F04Session* session, std::uint64_t person_id,
                             F04Ref& person, std::uint64_t& revision) noexcept;
std::uint32_t bind_player(F04Session* session, F04Ref person, std::uint64_t revision) noexcept;
}

} // namespace trek::host::detail
