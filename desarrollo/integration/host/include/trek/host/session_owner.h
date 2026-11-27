#pragma once

#include <cstdint>
#include <future>
#include <memory>
#include <optional>
#include <string>
#include <vector>

#include "trek/host/navigation.h"

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
namespace detail {
class AbiAdmission;
class BiographyProfileSource;
class AcademyCandidateFactory;
class AcademyPlayerBinding;
class AcademyInterface;
class InstitutionalQueries;
}

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
    friend class detail::AcademyCandidateFactory;
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

struct NavigationResult {
    Error error = Error::OK;
    Generation generation;
    NavigationStatus status = NavigationStatus::OK;
    std::optional<NavigationView> view;
    std::optional<RouteProposal> proposal;
    std::vector<ChartPlace> candidates;
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
enum class CampaignKind { AUTO, NAVAL, ACADEMY };
struct SlotAddress {
    std::string campaign; // 32 lowercase hex digits, obtained from campaign_id().
    std::string slot;     // 1..32 lowercase ASCII letters/digits/underscore.
    std::uint64_t version = 0; // 0 selects newest confirmed; explicit previous version allowed.
    CampaignKind kind = CampaignKind::AUTO; // Native callers may require a particular reader.
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

// H08-P02 native-only events. No C ABI or Unreal client is added here.
// IDs/state are filtered projections of a real F05 event page, not authority.
enum class EventSource : std::uint32_t { F05_ORDER = 1 };
struct EventNotice {
    EventSource source = EventSource::F05_ORDER;
    std::uint64_t id = 0, previous = 0, order = 0, tick = 0;
    std::uint32_t state = 0, code = 0;
    bool operator==(const EventNotice&) const = default;
};
struct EventSubscriptionResult {
    Error error = Error::OK;
    Generation generation;
    std::uint64_t subscription = 0, correlation_id = 0;
};
struct EventBatchResult {
    Error error = Error::OK;
    Generation generation;
    std::uint64_t subscription = 0, correlation_id = 0;
    std::vector<EventNotice> events;
    bool more = false, resync_required = false;
};

// H08-P04: presentation-only projections. No Core authority, F11 issuer,
// public C ABI or Unreal endpoint; acknowledgements reuse H08-P02.
enum class NotificationLevel : std::uint32_t { INFO, SUCCESS, WARNING, ERROR };
enum class NotificationKind : std::uint32_t {
    ORDER_ISSUED = 1, ORDER_ACCEPTED, ORDER_EXECUTING, ORDER_COMPLETED,
    ORDER_FAILED, ORDER_REFUSED, ORDER_CANCELLED
};
struct NotificationNotice {
    EventSource source = EventSource::F05_ORDER;
    NotificationKind kind = NotificationKind::ORDER_ISSUED;
    NotificationLevel level = NotificationLevel::INFO;
    std::uint64_t source_event_id = 0;
    std::uint64_t previous_event_id = 0;
    std::uint64_t order = 0, core_tick = 0;
    std::string title, body; // Safe, localized presentation, no raw Core details.
    bool operator==(const NotificationNotice&) const = default;
};
struct NotificationBatchResult {
    Error error = Error::OK;
    Generation generation;
    std::uint64_t subscription = 0, correlation_id = 0;
    std::string campaign_id; // Non-secret H04 identity for stable source deduplication.
    std::vector<NotificationNotice> items;
    bool more = false, resync_required = false;
};

// H08-P03: explicit, bounded campaign-clock intent on the trusted native
// HOST interface. The timeline and scheduled work belong exclusively to Core.
struct ClockLimits {
    static constexpr std::uint64_t max_span_seconds = 600;
    static constexpr std::uint64_t max_tasks = 128;
};
struct ClockIntent {
    std::uint64_t intent_id = 0; // Monotonic within one session generation; not a credential.
    std::uint64_t expected_revision = 0;
    std::uint64_t expected_now = 0;
    std::uint64_t horizon = 0; // Absolute Core campaign seconds, never wall time.
    std::uint64_t task_budget = 0; // 1..128; Core's own maximum remains unchanged.
};
struct ClockResult {
    Error error = Error::OK;
    Generation generation;
    std::uint64_t correlation_id = 0;
    std::uint64_t before_tick = 0, after_tick = 0;
    std::uint64_t before_revision = 0, after_revision = 0;
    std::uint64_t processed = 0;
    bool more_due = false; // F04_CAPACITY: partial committed advance, NOT a failure.
    bool replayed = false; // Identical intent already observed, Core not called again.
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
    // Explicit native bootstrap. The existing open and C ABI use no origin or chart.
    TREK_HOST_API std::future<Result> open_naval(PopulationConfig config, NavalBootstrap bootstrap);
    TREK_HOST_API static const char* naval_chart_publication() noexcept;
    TREK_HOST_API std::future<NavigationResult> query_navigation(Generation);
    TREK_HOST_API std::future<NavigationResult> propose_route(Generation, RouteIntent);
    TREK_HOST_API std::future<NavigationResult> validate_route(Generation, std::uint64_t reference);
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

    // F05-only initial H08-P02 subscription. HOST resolves the observer;
    // clients supply no actor or scope. All Core reads run on the owner thread.
    TREK_HOST_API std::future<EventSubscriptionResult> subscribe_order_events(
        Generation, std::uint64_t order, std::uint64_t correlation_id = 0);
    TREK_HOST_API std::future<EventBatchResult> poll_order_events(
        Generation, std::uint64_t subscription, std::uint64_t correlation_id = 0);
    // One-to-one presentation of the SAME authorized F05 source stream.
    // No new subscriptions, no new acknowledgement semantics, no F11 emission.
    TREK_HOST_API std::future<NotificationBatchResult> poll_order_notifications(
        Generation, std::uint64_t subscription, std::uint64_t correlation_id = 0);
    TREK_HOST_API std::future<Result> ack_order_events(
        Generation, std::uint64_t subscription, std::uint64_t presented_event_id);

    // A single explicit, monotonic, generation-bound request. No automatic
    // real-time progression, background scheduler or mutation from NPC/AI/UE.
    TREK_HOST_API std::future<ClockResult> advance_clock(
        Generation, ClockIntent, std::uint64_t correlation_id = 0);

private:
    friend class PlayerBootstrap;
    friend class detail::BiographyProfileSource;
    friend class detail::AcademyCandidateFactory;
    friend class detail::AcademyPlayerBinding;
    friend class detail::AcademyInterface;
    friend class detail::InstitutionalQueries;
    friend class detail::AbiAdmission;
#ifdef TREK_HOST_GATEWAY_TESTING
    friend class GatewayTestAccess;
#endif
    struct Impl;
    std::unique_ptr<Impl> impl_;
};

} // namespace trek::host

#undef TREK_HOST_API
