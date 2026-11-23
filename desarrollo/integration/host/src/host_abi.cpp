#include "trek/host/host_abi.h"
#include "trek/host/academy_abi.h"

#include "abi_admission.h"
#include "institutional_queries.h"
#include "trek/host/institutional_abi.h"
#include "academy_interface.h"
#include "f10/academy_campaign.h"
#include "trek/host/session_owner.h"
#include "f05_orders.h"

#include <array>
#include <chrono>
#include <cstddef>
#include <cstring>
#include <limits>
#include <string>
#include <string_view>
#include <type_traits>
#include <utility>
#include <variant>
#include <jsoncons/json.hpp>

using namespace trek::host;
using detail::AbiAdmission;

static_assert(sizeof(void*) == 8);
static_assert(sizeof(TrekHostText) == 16 && sizeof(TrekHostRequest) == 80);
static_assert(sizeof(TrekHostStatus) == 24 && sizeof(TrekHostCompletion) == 120);
static_assert(offsetof(TrekHostRequest, input) == 16 && offsetof(TrekHostCompletion, output) == 72);
static_assert(std::is_trivial_v<TrekHostRequest> && std::is_standard_layout_v<TrekHostRequest>);
static_assert(std::is_trivial_v<TrekHostCompletion> && std::is_standard_layout_v<TrekHostCompletion>);
static_assert(sizeof(TrekHostAcademyRequest) == 48 && sizeof(TrekHostAcademyView) == 240);
static_assert(sizeof(TrekHostSlotMetadata) == 104 && sizeof(TrekHostAcademyCompletion) == 6696);

namespace {

TrekHostCode encode(Error error)
{
    switch (error) {
    case Error::OK: return TREK_HOST_OK;
    case Error::INVALID_ARGUMENT: return TREK_HOST_INVALID_ARGUMENT;
    case Error::SESSION_CLOSED: return TREK_HOST_SESSION_CLOSED;
    case Error::BUSY_STATE: return TREK_HOST_BUSY_STATE;
    case Error::WRONG_THREAD: return TREK_HOST_WRONG_THREAD;
    case Error::GENERATION_EXPIRED: return TREK_HOST_GENERATION_EXPIRED;
    case Error::CAPACITY_LIMIT: return TREK_HOST_CAPACITY_LIMIT;
    case Error::DOMAIN_REJECTED: return TREK_HOST_DOMAIN_REJECTED;
    case Error::INTERNAL_ERROR: return TREK_HOST_INTERNAL_ERROR;
    case Error::PRINCIPAL_UNBOUND: return TREK_HOST_PRINCIPAL_UNBOUND;
    case Error::ACCESS_DENIED: return TREK_HOST_ACCESS_DENIED;
    case Error::SCOPE_INVALID: return TREK_HOST_SCOPE_INVALID;
    case Error::REVISION_STALE: return TREK_HOST_REVISION_STALE;
    case Error::IDEMPOTENCY_CONFLICT: return TREK_HOST_IDEMPOTENCY_CONFLICT;
    case Error::SAVE_INCOMPATIBLE: return TREK_HOST_SAVE_INCOMPATIBLE;
    case Error::SAVE_UNTRUSTED: return TREK_HOST_SAVE_UNTRUSTED;
    case Error::PERSISTENCE_FAILED: return TREK_HOST_PERSISTENCE_FAILED;
    case Error::PUBLICATION_UNCERTAIN: return TREK_HOST_PUBLICATION_UNCERTAIN;
    case Error::SAVE_CORRUPT: return TREK_HOST_SAVE_CORRUPT;
    case Error::IDENTITY_MISMATCH: return TREK_HOST_IDENTITY_MISMATCH;
    case Error::PATH_REJECTED: return TREK_HOST_PATH_REJECTED;
    case Error::SERVICE_UNAVAILABLE: return TREK_HOST_SERVICE_UNAVAILABLE;
    }
    return TREK_HOST_INTERNAL_ERROR;
}

uint32_t encode(State state)
{
    switch (state) {
    case State::CLOSED: return TREK_HOST_CLOSED;
    case State::OPENING: return TREK_HOST_OPENING;
    case State::ACTIVE: return TREK_HOST_ACTIVE;
    case State::SAVING: return TREK_HOST_SAVING;
    case State::LOADING: return TREK_HOST_LOADING;
    case State::FAILED: return TREK_HOST_FAILED;
    case State::FAILED_RECOVERABLE: return TREK_HOST_FAILED_RECOVERABLE;
    case State::CLOSING: return TREK_HOST_CLOSING;
    }
    return TREK_HOST_FAILED;
}

static_assert(F05_ISSUED == int(TREK_HOST_ISSUED) && F05_ACCEPTED == int(TREK_HOST_ACCEPTED) &&
              F05_EXECUTING == int(TREK_HOST_EXECUTING) && F05_COMPLETED == int(TREK_HOST_COMPLETED) &&
              F05_FAILED == int(TREK_HOST_ORDER_FAILED) && F05_REFUSED == int(TREK_HOST_REFUSED) &&
              F05_CANCELLED == int(TREK_HOST_CANCELLED));

bool valid_text(TrekHostText text, uint32_t limit)
{
    return text.reserved == 0 && text.size <= limit &&
           (text.size == 0 || (text.data && !std::memchr(text.data, '\0', text.size)));
}

std::string copy(TrekHostText text)
{
    return text.size ? std::string(text.data, text.size) : std::string{};
}

using Reply = std::variant<std::future<Result>, std::shared_future<Result>, std::future<OperationResult>,
                           std::future<detail::AcademyInterfaceResult>, std::future<detail::InstitutionalResult>>;

struct Pending {
    Reply reply;
    uint64_t ticket = 0;
    uint64_t key = 0;
    uint32_t operation = 0;
    Generation generation;
    bool academy = false;
    bool institutional = false;
    uint64_t correlation = 0;
};

void project(TrekHostCompletion& out, const OperationResult& result, const Pending& pending)
{
    if (result.campaign) {
        const auto& view = *result.campaign;
        out.output.view = {view.revision, view.now, view.person, view.ship};
    }
    const auto* order = result.order ? &*result.order : nullptr;
    const auto* receipt = order ? &order->receipt : (result.receipt ? &*result.receipt : nullptr);
    if (receipt) {
        const auto* execution = order && order->execution ? &*order->execution : nullptr;
        out.output.order = {receipt->order, order ? order->key : pending.key, receipt->revision,
                            receipt->result, execution ? execution->value : 0,
                            receipt->state, execution ? execution->performed : 0};
    }
}

} // namespace

struct TrekHostClient {
    explicit TrekHostClient(StorageConfig config) : owner(std::move(config)) {}

    Pending* find(uint64_t ticket)
    {
        for (auto& slot : pending) {
            if (slot.ticket == ticket) return &slot;
        }
        return nullptr;
    }

    SessionOwner owner;
    std::array<Pending, TREK_HOST_ABI_MAX_PENDING + 1> pending{};
    uint64_t last_ticket = 0;
};

extern "C" {

uint32_t TREK_HOST_ABI_CALL trek_host_abi_version(void)
{
    return TREK_HOST_ABI_VERSION;
}

TrekHostCode TREK_HOST_ABI_CALL trek_host_create(uint32_t version, const char* root,
                                               uint32_t root_size, TrekHostClient** out)
try {
    if (!out) return TREK_HOST_INVALID_ARGUMENT;
    *out = nullptr;
    if (version != TREK_HOST_ABI_VERSION) return TREK_HOST_ABI_MISMATCH;
    const TrekHostText path{root, root_size, 0};
    if (!valid_text(path, TREK_HOST_ABI_MAX_ROOT_BYTES)) return TREK_HOST_INVALID_ARGUMENT;
    *out = new TrekHostClient(StorageConfig{copy(path)});
    return TREK_HOST_OK;
} catch (...) {
    return TREK_HOST_INTERNAL_ERROR;
}

void TREK_HOST_ABI_CALL trek_host_destroy(TrekHostClient* client)
{
    delete client;
}

TrekHostCode TREK_HOST_ABI_CALL trek_host_status(TrekHostClient* client, TrekHostStatus* out)
try {
    if (!client || !out) return TREK_HOST_INVALID_ARGUMENT;
    if (out->size != sizeof(*out)) return TREK_HOST_ABI_MISMATCH;
    const AbiAdmission guard(client->owner);
    if (!guard) return TREK_HOST_RETRY;
    const auto snapshot = client->owner.snapshot();
    const auto principal = client->owner.current_player(snapshot.generation);
    *out = {sizeof(*out), encode(snapshot.state), AbiAdmission::token(snapshot.generation),
            encode(principal.error), TREK_HOST_SERVICE_UNAVAILABLE};
    return TREK_HOST_OK;
} catch (...) {
    return TREK_HOST_INTERNAL_ERROR;
}

TrekHostCode TREK_HOST_ABI_CALL trek_host_submit(TrekHostClient* client, const TrekHostRequest* request,
                                               uint64_t* ticket)
try {
    if (!ticket) return TREK_HOST_INVALID_ARGUMENT;
    *ticket = 0;
    if (!client || !request) return TREK_HOST_INVALID_ARGUMENT;
    if (request->size != sizeof(*request)) return TREK_HOST_ABI_MISMATCH;
    const auto op = request->operation;
    if (op < TREK_HOST_OPEN || op > TREK_HOST_RESTORE) return TREK_HOST_INVALID_ARGUMENT;
    if ((op == TREK_HOST_OPEN || op == TREK_HOST_CLOSE) && request->generation != 0)
        return TREK_HOST_INVALID_ARGUMENT;

    auto* slot = op == TREK_HOST_CLOSE ? &client->pending.back() : client->find(0);
    if (!slot || (op != TREK_HOST_CLOSE && slot == &client->pending.back()) || slot->ticket ||
        client->last_ticket == std::numeric_limits<uint64_t>::max())
        return TREK_HOST_CAPACITY_LIMIT;

    // Prepare the bounded input copies before locking admission.
    PopulationConfig population;
    SlotAddress address;
    std::string save_slot;
    if (op == TREK_HOST_OPEN) {
        const auto& p = request->input.population;
        if (!valid_text(p.class_id, 64) || p.class_id.size == 0) return TREK_HOST_INVALID_ARGUMENT;
        population = {copy(p.class_id), p.ship_identity, p.seed, p.crew,
                      p.residents, p.passengers, p.maximum};
    } else if (op == TREK_HOST_SAVE) {
        if (!valid_text(request->input.slot, 32)) return TREK_HOST_PATH_REJECTED;
        save_slot = copy(request->input.slot);
    } else if (op == TREK_HOST_RESTORE) {
        const auto& a = request->input.restore;
        if (!valid_text(a.campaign, 32) || !valid_text(a.slot, 32)) return TREK_HOST_PATH_REJECTED;
        address = {copy(a.campaign), copy(a.slot), a.version};
    }

    const AbiAdmission guard(client->owner);
    if (!guard) return TREK_HOST_RETRY;
    const auto current = client->owner.snapshot().generation;
    if (op != TREK_HOST_OPEN && op != TREK_HOST_CLOSE &&
        request->generation != AbiAdmission::token(current))
        return TREK_HOST_GENERATION_EXPIRED;

    const auto next = client->last_ticket + 1;
    Reply reply;
    uint64_t key = 0;
    switch (op) {
    case TREK_HOST_OPEN:
        reply = client->owner.open(std::move(population));
        break;
    case TREK_HOST_CLOSE:
        reply = client->owner.close();
        break;
    case TREK_HOST_QUERY_VIEW:
        reply = client->owner.query_view(current, next);
        break;
    case TREK_HOST_SUBMIT_SCAN: {
        const auto& q = request->input.scan;
        key = q.key;
        reply = client->owner.submit_order(current, {q.recipient, q.station, q.key,
            q.expected_revision, q.deadline, q.cause, F04_SCAN}, next);
        break;
    }
    case TREK_HOST_QUERY_ORDER:
        reply = client->owner.query_order(current, request->input.order.id, next);
        break;
    case TREK_HOST_CANCEL_ORDER:
        reply = client->owner.cancel_order(current, request->input.order.id,
            request->input.order.expected_revision, next);
        break;
    case TREK_HOST_SAVE:
        reply = client->owner.save(current, std::move(save_slot));
        break;
    case TREK_HOST_RESTORE:
        reply = client->owner.restore(current, std::move(address));
        break;
    }
    const auto generation = op == TREK_HOST_OPEN || op == TREK_HOST_CLOSE ? Generation{} : current;
    *slot = {std::move(reply), next, key, op, generation};
    *ticket = client->last_ticket = next;
    return TREK_HOST_OK;
} catch (...) {
    return TREK_HOST_INTERNAL_ERROR;
}

TrekHostCode TREK_HOST_ABI_CALL trek_host_poll(TrekHostClient* client, uint64_t ticket,
                                             TrekHostCompletion* out)
try {
    if (!client || !out || !ticket) return TREK_HOST_INVALID_ARGUMENT;
    if (out->size != sizeof(*out)) return TREK_HOST_ABI_MISMATCH;
    auto* slot = client->find(ticket);
    if (!slot) return TREK_HOST_UNKNOWN_TICKET;
    if (slot->academy || slot->institutional) return TREK_HOST_ABI_MISMATCH;

    const AbiAdmission guard(client->owner);
    if (!guard) return TREK_HOST_RETRY;
    const auto snapshot = client->owner.snapshot();
    TrekHostCompletion completion{};
    completion.size = sizeof(completion);
    completion.operation = slot->operation;
    completion.ticket = ticket;
    completion.code = TREK_HOST_INTERNAL_ERROR;

    const bool ready = std::visit([&](auto& future) {
        if (future.wait_for(std::chrono::seconds(0)) != std::future_status::ready) return false;
        try {
            const auto result = future.get();
            completion.code = encode(result.error);
            if (result.error != Error::OK) {
                if (slot->generation != Generation{} && slot->generation != snapshot.generation)
                    completion.code = TREK_HOST_GENERATION_EXPIRED;
                return true;
            }
            if (result.generation != snapshot.generation ||
                (slot->operation == TREK_HOST_CLOSE && snapshot.state != State::CLOSED)) {
                completion.code = TREK_HOST_GENERATION_EXPIRED;
                return true;
            }
            completion.generation = AbiAdmission::token(result.generation);
            if constexpr (std::is_same_v<std::decay_t<decltype(result)>, OperationResult>) {
                project(completion, result, *slot);
            } else if (slot->operation == TREK_HOST_OPEN || slot->operation == TREK_HOST_RESTORE) {
                const auto campaign = guard.campaign();
                if (campaign.size() != TREK_HOST_ABI_CAMPAIGN_BYTES) {
                    completion.generation = 0;
                    completion.code = TREK_HOST_INTERNAL_ERROR;
                } else {
                    std::memcpy(completion.campaign, campaign.data(), campaign.size());
                }
            }
        } catch (const std::future_error&) {
            // A broken promise has no usable domain result.
        }
        return true;
    }, slot->reply);
    if (!ready) return TREK_HOST_PENDING;
    *slot = {};
    *out = completion;
    return TREK_HOST_OK;
} catch (...) {
    return TREK_HOST_INTERNAL_ERROR;
}

TrekHostCode TREK_HOST_ABI_CALL trek_host_discard(TrekHostClient* client, uint64_t ticket)
{
    if (!client || !ticket) return TREK_HOST_INVALID_ARGUMENT;
    auto* slot = client->find(ticket);
    if (!slot) return TREK_HOST_UNKNOWN_TICKET;
    *slot = {};
    return TREK_HOST_OK;
}

uint32_t TREK_HOST_ABI_CALL trek_host_institutional_version(void)
{
    return TREK_HOST_INSTITUTIONAL_VERSION;
}

TrekHostCode TREK_HOST_ABI_CALL trek_host_institutional_current(
    TrekHostClient* client, uint64_t generation, uint64_t epoch)
try {
    if (!client) return TREK_HOST_INVALID_ARGUMENT;
    const AbiAdmission guard(client->owner);
    if (!guard) return TREK_HOST_RETRY;
    const auto current = client->owner.snapshot().generation;
    if (!generation || generation != AbiAdmission::token(current)) return TREK_HOST_GENERATION_EXPIRED;
    detail::InstitutionalResult result;
    result.generation = current;
    result.persistence_epoch = epoch;
    result.view.emplace();
    return detail::InstitutionalQueries::is_current(client->owner, result) ? TREK_HOST_OK : TREK_HOST_GENERATION_EXPIRED;
} catch (...) { return TREK_HOST_INTERNAL_ERROR; }

TrekHostCode TREK_HOST_ABI_CALL trek_host_institutional_submit(
    TrekHostClient* client, const TrekHostInstitutionalRequest* request, uint64_t* ticket)
try {
    if (!ticket) return TREK_HOST_INVALID_ARGUMENT;
    *ticket = 0;
    if (!client || !request) return TREK_HOST_INVALID_ARGUMENT;
    if (request->size != sizeof(*request) || request->version != TREK_HOST_INSTITUTIONAL_VERSION)
        return TREK_HOST_ABI_MISMATCH;
    if (request->reserved || (request->operation != TREK_HOST_CAREER && request->operation != TREK_HOST_PROMOTION) ||
        (request->operation == TREK_HOST_CAREER && request->event_id) ||
        (request->operation == TREK_HOST_PROMOTION && !request->event_id)) return TREK_HOST_INVALID_ARGUMENT;
    auto* slot = client->find(0);
    if (!slot || slot == &client->pending.back() || client->last_ticket == UINT64_MAX) return TREK_HOST_CAPACITY_LIMIT;
    const AbiAdmission guard(client->owner);
    if (!guard) return TREK_HOST_RETRY;
    const auto current = client->owner.snapshot().generation;
    if (request->generation != AbiAdmission::token(current)) return TREK_HOST_GENERATION_EXPIRED;
    const auto next = client->last_ticket + 1;
    auto reply = request->operation == TREK_HOST_CAREER
        ? detail::InstitutionalQueries::career(client->owner, current, request->correlation)
        : detail::InstitutionalQueries::promotion(client->owner, current, request->event_id, request->correlation);
    *slot = {std::move(reply), next, 0, request->operation, current, false, true, request->correlation};
    *ticket = client->last_ticket = next;
    return TREK_HOST_OK;
} catch (...) { return TREK_HOST_INTERNAL_ERROR; }

TrekHostCode TREK_HOST_ABI_CALL trek_host_institutional_poll(
    TrekHostClient* client, uint64_t ticket, TrekHostInstitutionalCompletion* out)
try {
    if (!client || !out || !ticket) return TREK_HOST_INVALID_ARGUMENT;
    if (out->size != sizeof(*out)) return TREK_HOST_ABI_MISMATCH;
    auto* slot = client->find(ticket);
    if (!slot) return TREK_HOST_UNKNOWN_TICKET;
    if (!slot->institutional) return TREK_HOST_ABI_MISMATCH;
    const AbiAdmission guard(client->owner);
    if (!guard) return TREK_HOST_RETRY;
    auto& future = std::get<std::future<detail::InstitutionalResult>>(slot->reply);
    if (future.wait_for(std::chrono::seconds(0)) != std::future_status::ready) return TREK_HOST_PENDING;
    TrekHostInstitutionalCompletion completion{};
    completion.size = sizeof(completion);
    completion.ticket = ticket;
    completion.operation = slot->operation;
    completion.correlation = slot->correlation;
    completion.code = TREK_HOST_INTERNAL_ERROR;
    try {
        const auto result = future.get();
        completion.code = encode(result.error);
        if (result.error == Error::OK && !detail::InstitutionalQueries::is_current(client->owner, result))
            completion.code = TREK_HOST_GENERATION_EXPIRED;
        if (completion.code == TREK_HOST_OK) {
            completion.generation = AbiAdmission::token(result.generation);
            completion.epoch = result.persistence_epoch;
            completion.world_revision = result.view->world_revision;
            std::visit([&](const auto& facts) {
                using T = std::decay_t<decltype(facts)>;
                if constexpr (std::is_same_v<T, detail::CareerViewV1>) {
                    completion.event_id = facts.rank_event_id;
                    completion.rank = facts.rank;
                    completion.service_status = facts.service_status;
                } else {
                    completion.event_id = facts.event_id;
                    completion.effective_tick = facts.effective_tick;
                    completion.original_revision = facts.original_revision;
                    completion.from_rank = facts.from_rank;
                    completion.to_rank = facts.to_rank;
                }
            }, result.view->facts);
        }
    } catch (...) { completion.code = TREK_HOST_INTERNAL_ERROR; }
    *slot = {};
    *out = completion;
    return TREK_HOST_OK;
} catch (...) { return TREK_HOST_INTERNAL_ERROR; }

uint32_t TREK_HOST_ABI_CALL trek_host_academy_version(void)
{
    return TREK_HOST_ACADEMY_VERSION;
}

TrekHostCode TREK_HOST_ABI_CALL trek_host_academy_submit(
    TrekHostClient* client, const TrekHostAcademyRequest* request, uint64_t* ticket)
try {
    if (!ticket) return TREK_HOST_INVALID_ARGUMENT;
    *ticket = 0;
    if (!client || !request) return TREK_HOST_INVALID_ARGUMENT;
    if (request->size != sizeof(*request) || request->version != TREK_HOST_ACADEMY_VERSION)
        return TREK_HOST_ABI_MISMATCH;
    if (request->reserved || request->operation < TREK_HOST_ACADEMY_CREATE ||
        request->operation > TREK_HOST_ACADEMY_SLOTS) return TREK_HOST_INVALID_ARGUMENT;
    const bool create = request->operation == TREK_HOST_ACADEMY_CREATE;
    std::string payload;
    if (create) {
        if (request->generation || !request->creation_key || !request->display_name.size ||
            !valid_text(request->display_name, TREK_HOST_ACADEMY_NAME_BYTES)) return TREK_HOST_INVALID_ARGUMENT;
        jsoncons::json input;
        input["display_name"] = copy(request->display_name);
        payload = input.to_string();
        if (!detail::academy_display_name(payload)) return TREK_HOST_INVALID_ARGUMENT;
    } else if ((request->operation == TREK_HOST_ACADEMY_QUERY && request->creation_key) ||
               (request->operation == TREK_HOST_ACADEMY_SLOTS && request->slot_cursor > UINT32_MAX) ||
               request->display_name.data || request->display_name.size ||
               request->display_name.reserved) return TREK_HOST_INVALID_ARGUMENT;

    auto* slot = client->find(0);
    if (!slot || slot == &client->pending.back() ||
        client->last_ticket == std::numeric_limits<uint64_t>::max()) return TREK_HOST_CAPACITY_LIMIT;
    const AbiAdmission guard(client->owner);
    if (!guard) return TREK_HOST_RETRY;
    const auto current = client->owner.snapshot().generation;
    if (!create && request->generation != AbiAdmission::token(current)) return TREK_HOST_GENERATION_EXPIRED;
    const auto next = client->last_ticket + 1;
    std::future<detail::AcademyInterfaceResult> reply;
    switch (request->operation) {
    case TREK_HOST_ACADEMY_CREATE:
        reply = detail::AcademyInterface::create_bound(client->owner, request->creation_key, std::move(payload));
        break;
    case TREK_HOST_ACADEMY_QUERY:
        reply = detail::AcademyInterface::query(client->owner, current);
        break;
    case TREK_HOST_ACADEMY_SLOTS:
        reply = detail::AcademyInterface::slots(client->owner, current, static_cast<uint32_t>(request->slot_cursor));
        break;
    }
    *slot = {std::move(reply), next, 0, request->operation, create ? Generation{} : current, true};
    *ticket = client->last_ticket = next;
    return TREK_HOST_OK;
} catch (const jsoncons::ser_error&) {
    return TREK_HOST_INVALID_ARGUMENT;
} catch (...) {
    return TREK_HOST_INTERNAL_ERROR;
}

TrekHostCode TREK_HOST_ABI_CALL trek_host_academy_poll(
    TrekHostClient* client, uint64_t ticket, TrekHostAcademyCompletion* out)
try {
    if (!client || !out || !ticket) return TREK_HOST_INVALID_ARGUMENT;
    if (out->size != sizeof(*out)) return TREK_HOST_ABI_MISMATCH;
    auto* slot = client->find(ticket);
    if (!slot) return TREK_HOST_UNKNOWN_TICKET;
    if (!slot->academy || slot->institutional) return TREK_HOST_ABI_MISMATCH;
    const AbiAdmission guard(client->owner);
    if (!guard) return TREK_HOST_RETRY;
    auto& future = std::get<std::future<detail::AcademyInterfaceResult>>(slot->reply);
    if (future.wait_for(std::chrono::seconds(0)) != std::future_status::ready) return TREK_HOST_PENDING;
    TrekHostAcademyCompletion completion{};
    completion.size = sizeof(completion);
    completion.ticket = ticket;
    completion.operation = slot->operation;
    completion.code = TREK_HOST_INTERNAL_ERROR;
    try {
        auto result = future.get();
        const auto snapshot = client->owner.snapshot();
        completion.code = encode(result.error);
        if ((result.error == Error::OK && result.generation != snapshot.generation) ||
            (result.error == Error::OK && slot->operation == TREK_HOST_ACADEMY_SLOTS &&
             result.catalog_epoch != guard.catalog_epoch()) ||
            (result.error != Error::OK && slot->generation != Generation{} && slot->generation != snapshot.generation))
            completion.code = TREK_HOST_GENERATION_EXPIRED;
        if (completion.code == TREK_HOST_OK) {
            completion.generation = AbiAdmission::token(result.generation);
            if (slot->operation == TREK_HOST_ACADEMY_SLOTS) {
                if (result.slots.size() > TREK_HOST_ACADEMY_MAX_SLOTS) throw std::logic_error("Slot limit");
                completion.output.slots.count = static_cast<uint32_t>(result.slots.size());
                completion.output.slots.next_cursor = result.next_cursor;
                for (std::size_t i = 0; i < result.slots.size(); ++i) {
                    const auto& source = result.slots[i];
                    auto& row = completion.output.slots.entries[i];
                    if (source.address.campaign.size() != 32 || source.address.slot.size() > 32)
                        throw std::logic_error("Slot metadata bounds");
                    row.version = source.address.version;
                    row.kind = source.address.kind == CampaignKind::ACADEMY ? TREK_HOST_KIND_ACADEMY :
                               source.address.kind == CampaignKind::NAVAL ? TREK_HOST_KIND_NAVAL : TREK_HOST_KIND_UNKNOWN;
                    row.format = source.format;
                    row.provenance = static_cast<uint32_t>(source.provenance);
                    row.reason = encode(source.reason);
                    row.compatible = source.compatible;
                    row.recoverable = source.recoverable;
                    std::memcpy(row.campaign, source.address.campaign.data(), source.address.campaign.size());
                    std::memcpy(row.slot, source.address.slot.data(), source.address.slot.size());
                }
            } else {
                if (!result.candidate) throw std::logic_error("Missing bound candidate");
                const auto& source = *result.candidate;
                if (source.campaign_id.size() != 32 || source.display_name.size() > TREK_HOST_ACADEMY_NAME_BYTES ||
                    source.source_digest.size() != 64) throw std::logic_error("Candidate bounds");
                auto& view = completion.output.candidate;
                view.person = source.person;
                view.creation_fact = source.creation_fact;
                view.revision = source.revision;
                view.tick = source.tick;
                view.kind = TREK_HOST_KIND_ACADEMY;
                view.candidate_state = TREK_HOST_CANDIDATE;
                std::memcpy(view.campaign, source.campaign_id.data(), source.campaign_id.size());
                std::memcpy(view.display_name, source.display_name.data(), source.display_name.size());
                std::memcpy(view.source_digest, source.source_digest.data(), source.source_digest.size());
            }
        }
    } catch (...) {
        completion.code = TREK_HOST_INTERNAL_ERROR;
    }
    if (completion.code != TREK_HOST_OK) {
        completion.generation = 0;
        completion.output = {};
    }
    *slot = {};
    *out = completion;
    return TREK_HOST_OK;
} catch (...) {
    return TREK_HOST_INTERNAL_ERROR;
}

} // extern "C"
