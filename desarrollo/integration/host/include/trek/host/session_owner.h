#pragma once

#include <cstdint>
#include <future>
#include <memory>
#include <optional>
#include <string>
#include <vector>

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
namespace detail { class AbiAdmission; }

// Internal C++ interface for HOST modules.
enum class State { CLOSED, OPENING, ACTIVE, SAVING, LOADING, FAILED, FAILED_RECOVERABLE, CLOSING };

enum class Error {
    OK, INVALID_ARGUMENT, SESSION_CLOSED, BUSY_STATE, WRONG_THREAD,
    GENERATION_EXPIRED, CAPACITY_LIMIT, DOMAIN_REJECTED, INTERNAL_ERROR,
    PRINCIPAL_UNBOUND, ACCESS_DENIED, SCOPE_INVALID, REVISION_STALE, IDEMPOTENCY_CONFLICT,
    SAVE_INCOMPATIBLE, SAVE_UNTRUSTED, PERSISTENCE_FAILED, PUBLICATION_UNCERTAIN,
    SAVE_CORRUPT, IDENTITY_MISMATCH, PATH_REJECTED, SERVICE_UNAVAILABLE
};

class Generation {
public:
    Generation() = default;
    bool operator==(const Generation&) const = default;

private:
    friend class SessionOwner;
    friend class detail::AbiAdmission;
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

enum class Provenance { CREATED_LOCALLY, KNOWN_LOCAL, IMPORTED_UNVERIFIED, REJECTED };
struct SlotAddress {
    std::string campaign; // 32 lowercase hex digits, obtained from campaign_id().
    std::string slot;     // 1..32 lowercase ASCII letters/digits/underscore.
    std::uint64_t version = 0; // 0 selects newest confirmed; explicit previous version allowed.
};
struct SlotInspection {
    SlotAddress address;
    Provenance provenance = Provenance::REJECTED;
    Error reason = Error::SAVE_CORRUPT;
    std::uint32_t format = 0;
    bool compatible = false;
    bool recoverable = false; // Complete envelope and isolated Core validation succeeded.
};
struct InspectionResult {
    Error error = Error::OK;
    std::vector<SlotInspection> slots;
};
struct StorageConfig { std::string root; }; // Existing authorized private absolute directory, UTF-8.

// Native HOST projections, semantic version 1. IDs are data, never credentials.
struct CampaignView {
    Generation generation;
    std::uint64_t revision = 0, now = 0, person = 0, ship = 0;
};
struct OrderIntent {
    std::uint64_t recipient = 0, station = 0;
    std::uint64_t key = 0, expected_revision = 0, deadline = 0, cause = 0;
    std::uint32_t operation = 0; // F04Op; F05 decides supported operations.
};
struct OrderReceipt {
    std::uint64_t request = 0, order = 0, task = 0, attempt = 0, result = 0, event = 0, revision = 0;
    std::uint32_t state = 0, code = 0;
};
struct ExecutionResult {
    std::uint64_t id = 0, executor = 0, input_revision = 0, tick = 0;
    std::uint32_t performed = 0, code = 0, core_outcome = 0, core_rejection = 0;
    std::uint64_t core_revision_before = 0, core_revision_after = 0, stream = 0, value = 0;
    std::uint32_t consumed_random = 0;
};
struct OrderView {
    Generation generation;
    OrderReceipt receipt;
    std::uint64_t issuer = 0, recipient = 0, ship = 0, station = 0;
    std::uint64_t key = 0, deadline = 0, cause = 0, input_revision = 0;
    std::uint32_t operation = 0;
    std::optional<ExecutionResult> execution;
};
struct OperationResult {
    Error error = Error::OK;
    Generation generation;
    std::uint64_t correlation_id = 0; // Transport correlation only; never F05 key.
    std::optional<CampaignView> campaign;
    std::optional<OrderView> order;
    std::optional<OrderReceipt> receipt;
};

class PlayerBootstrap;

class SessionOwner final {
public:
    TREK_HOST_API SessionOwner();
    TREK_HOST_API explicit SessionOwner(StorageConfig storage);
    TREK_HOST_API ~SessionOwner();

    SessionOwner(const SessionOwner&) = delete;
    SessionOwner& operator=(const SessionOwner&) = delete;

    TREK_HOST_API std::future<Result> open(PopulationConfig config);
    TREK_HOST_API std::shared_future<Result> close();
    TREK_HOST_API Snapshot snapshot() const;
    TREK_HOST_API std::string campaign_id(Generation generation) const;
    TREK_HOST_API Provenance campaign_provenance(Generation generation) const;
    TREK_HOST_API std::future<Result> save(Generation generation, std::string slot);
    // CLOSED requires an empty Generation. ACTIVE requires its exact generation.
    TREK_HOST_API std::future<Result> restore(Generation generation, SlotAddress address);
    TREK_HOST_API static InspectionResult inspect(const StorageConfig& storage);

    // A generation-bound liveness check for internal HOST components.
    TREK_HOST_API std::future<Result> check_active(Generation generation);

    // Resolves the sole local principal of this owner. The copied ID is for
    // projection; later operations must resolve authority on the owner again.
    TREK_HOST_API PlayerResult current_player(Generation generation) const;

    TREK_HOST_API std::future<OperationResult> query_view(Generation, std::uint64_t correlation_id = 0);
    TREK_HOST_API std::future<OperationResult> submit_order(Generation, OrderIntent, std::uint64_t correlation_id = 0);
    TREK_HOST_API std::future<OperationResult> query_order(Generation, std::uint64_t order, std::uint64_t correlation_id = 0);
    TREK_HOST_API std::future<OperationResult> cancel_order(Generation, std::uint64_t order,
                                                        std::uint64_t expected_revision, std::uint64_t correlation_id = 0);
    TREK_HOST_API std::future<OperationResult> institutional_command(Generation, std::uint64_t correlation_id = 0);

private:
    friend class PlayerBootstrap;
    friend class detail::AbiAdmission;
#ifdef TREK_HOST_GATEWAY_TESTING
    friend class GatewayTestAccess;
#endif
    struct Impl;
    std::unique_ptr<Impl> impl_;
};

} // namespace trek::host

#undef TREK_HOST_API
