#pragma once

#include <cstdint>
#include <future>
#include <memory>
#include <optional>
#include <string>

#if defined(TREK_HOST_STATIC_TEST)
# define TREK_HOST_API
#elif defined(_WIN32)
# if defined(TREK_HOST_BUILD)
#  define TREK_HOST_API __declspec(dllexport)
# else
#  define TREK_HOST_API __declspec(dllimport)
# endif
#else
# define TREK_HOST_API __attribute__((visibility("default")))
#endif

namespace trek::host {

// Internal C++ interface for HOST modules.
enum class State { CLOSED, OPENING, ACTIVE, SAVING, LOADING, FAILED, FAILED_RECOVERABLE, CLOSING };

enum class Error {
    OK, INVALID_ARGUMENT, SESSION_CLOSED, BUSY_STATE, WRONG_THREAD,
    GENERATION_EXPIRED, CAPACITY_LIMIT, DOMAIN_REJECTED, INTERNAL_ERROR,
    PRINCIPAL_UNBOUND, ACCESS_DENIED, SCOPE_INVALID, REVISION_STALE, IDEMPOTENCY_CONFLICT
};

class Generation {
public:
    Generation() = default;
    bool operator==(const Generation&) const = default;

private:
    friend class SessionOwner;
    explicit Generation(std::uint64_t value) : value_(value) {}
    std::uint64_t value_ = 0;
};

struct PopulationConfig {
    std::string class_id;
    std::uint64_t ship_identity = 0;
    std::uint64_t seed = 0;
    std::uint64_t crew = 0;
    std::uint64_t residents = 0;
    std::uint64_t passengers = 0;
    std::uint64_t maximum = 0;
};

struct Result {
    Error error = Error::OK;
    Generation generation;
};

struct Snapshot {
    State state;
    Generation generation;
};

struct PlayerIdentity {
    Generation generation;
    std::uint64_t person_id;
};

struct PlayerResult {
    Error error;
    std::optional<PlayerIdentity> player;
};

class PlayerBootstrap;

class SessionOwner final {
public:
    TREK_HOST_API SessionOwner();
    TREK_HOST_API ~SessionOwner();

    SessionOwner(const SessionOwner&) = delete;
    SessionOwner& operator=(const SessionOwner&) = delete;

    TREK_HOST_API std::future<Result> open(PopulationConfig config);
    TREK_HOST_API std::shared_future<Result> close();
    TREK_HOST_API Snapshot snapshot() const;

    // A generation-bound liveness check for internal HOST components.
    TREK_HOST_API std::future<Result> check_active(Generation generation);

    // Resolves the sole local principal of this owner. The copied ID is for
    // projection; later operations must resolve authority on the owner again.
    TREK_HOST_API PlayerResult current_player(Generation generation) const;

private:
    friend class PlayerBootstrap;
    struct Impl;
    std::unique_ptr<Impl> impl_;
};

} // namespace trek::host

#undef TREK_HOST_API
