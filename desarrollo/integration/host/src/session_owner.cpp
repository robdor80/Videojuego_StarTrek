#include "trek/host/session_owner.h"

#include "abi_admission.h"
#include "academy_interface.h"
#include "biography_profile_source.h"
#include "f10/academy_player_binding.h"
#include "native_session.h"
#include "player_bootstrap.h"
#ifdef TREK_HOST_GATEWAY_TESTING
#include "gateway_test_access.h"
#endif

#include <atomic>
#include <condition_variable>
#include <cstdio>
#include <deque>
#include <exception>
#include <limits>
#include <mutex>
#include <optional>
#include <random>
#include <stdexcept>
#include <thread>
#include <type_traits>
#include <string_view>
#include <utility>
#include <variant>

namespace trek::host {
namespace detail {
struct AcademyCreationIntent {
    Generation generation;
    std::string campaign, profile;
    // The private object itself is the only key for the one creation intent
    // of this campaign. The campaign ID also identifies it for future storage.
};

struct AcademyCreationReceipt {
    AcademyIntent intent;
    corerpg::HistoryHash editable_digest;
    std::string source_digest;
    std::uint64_t person, creation_fact, revision, tick;
};
} // namespace detail

namespace {

#ifdef TREK_HOST_ACADEMY_TESTING
constinit std::atomic<void (*)()> academy_bind_test_hook{nullptr};
#endif

detail::AcademyCandidateResult inspect_academy_receipt(const detail::AcademyCampaign& academy,
                                                       const detail::AcademyCreationReceipt& receipt)
{
    auto view = academy.inspect();
    if (view.campaign_id != receipt.intent->campaign || view.source_digest != receipt.source_digest ||
        detail::academy_digest(view.display_name) != receipt.editable_digest ||
        view.person != receipt.person || view.creation_fact != receipt.creation_fact ||
        view.revision < receipt.revision || view.tick != receipt.tick) {
        return {Error::IDENTITY_MISMATCH, {}};
    }
    return {Error::OK, std::move(view)};
}

std::uint64_t next_generation() noexcept
{
    // Tokens include a process-specific starting point. The durable binding
    // reconstructs ownership without accepting generations from the slot.
    static std::atomic<std::uint64_t> last_generation{[]() noexcept {
        try {
            std::random_device random;
            return std::uniform_int_distribution<std::uint64_t>{
                1, std::numeric_limits<std::uint64_t>::max() / 2}(random);
        } catch (...) {
            return std::numeric_limits<std::uint64_t>::max();
        }
    }()};
    auto previous = last_generation.load();
    while (previous != std::numeric_limits<std::uint64_t>::max()) {
        if (last_generation.compare_exchange_weak(previous, previous + 1)) {
            return previous + 1;
        }
    }
    return 0;
}

template<class Reply = Result>
std::future<Reply> ready(Error error)
{
    std::promise<Reply> reply;
    auto future = reply.get_future();
    reply.set_value(Reply{error, {}});
    return future;
}

void report_failure(const char* operation, detail::Outcome outcome) noexcept
{
    if (outcome.domain_code) {
        std::fprintf(stderr, "TrekHost: %s failed (F04/F05 code %u)\n",
                     operation, static_cast<unsigned>(*outcome.domain_code));
    }
}

Error verify_academy_slot(const detail::PreparedSlot& slot)
{
    try {
        auto candidate = detail::AcademyCampaign::restore(slot);
        return Error::OK;
    } catch (const detail::StorageFailure& failure) {
        return failure.error;
    } catch (const detail::UnapprovedAcademySource&) {
        return Error::SAVE_INCOMPATIBLE;
    } catch (...) {
        return Error::PERSISTENCE_FAILED;
    }
}

Error verify_slot(const detail::PreparedSlot& prepared)
{
    if (std::holds_alternative<detail::AcademySnapshotIdentity>(prepared.identity))
        return verify_academy_slot(prepared);
    const auto* sha = detail::bridge::core_sha();
    if (!sha || std::string_view(sha) != TREK_HOST_CORE_SHA) return Error::SAVE_INCOMPATIBLE;
    F04Session* candidate = nullptr;
    F04Ref player{};
    const auto code = detail::bridge::restore(prepared, &candidate, player);
    if (candidate) detail::bridge::destroy(candidate);
    return code == F04_OK ? Error::OK : code == F04_DENIED ? Error::IDENTITY_MISMATCH : Error::SAVE_CORRUPT;
}

} // namespace

struct SessionOwner::Impl {
    struct Open {
        PopulationConfig config;
        std::shared_ptr<const detail::ActiveCampaign> campaign;
        std::promise<Result> reply;
    };

    struct Check {
        Generation generation;
        std::promise<Result> reply;
    };

    struct PreparePlayer {
        Generation generation;
        std::uint64_t person_id;
        std::promise<PlayerSelectionResult> reply;
    };

    struct BindPlayer {
        Generation generation;
        PlayerSelection selection;
        std::uint64_t revision;
        std::promise<BindPlayerResult> reply;
    };

    struct CreateAcademy {
        detail::AcademyIntent intent;
        std::string payload;
        std::promise<detail::AcademyCreationResult> reply;
    };

    struct InspectAcademy {
        Generation generation;
        detail::AcademyReceipt receipt;
        std::promise<detail::AcademyCandidateResult> reply;
    };

    struct BindAcademy {
        Generation generation;
        detail::AcademyReceipt receipt;
        std::promise<Result> reply;
    };
    struct InspectBoundAcademy {
        Generation generation;
        std::promise<detail::AcademyCandidateResult> reply;
    };
    struct CreateBoundAcademy {
        detail::AcademyIntent intent;
        std::string payload;
        std::promise<detail::AcademyInterfaceResult> reply;
    };
    struct QueryAcademy {
        Generation generation;
        std::promise<detail::AcademyInterfaceResult> reply;
    };
    struct InspectSlots {
        Generation generation;
        std::promise<detail::AcademyInterfaceResult> reply;
    };

    struct Save { Generation generation;std::string slot;std::promise<Result> reply; };
    struct Load { Generation generation;SlotAddress address;bool had_active;std::promise<Result> reply; };
    struct Dispatch { Generation generation; detail::GatewayRequest request; std::promise<OperationResult> reply; };
#ifdef TREK_HOST_GATEWAY_TESTING
    struct TestVisit { Generation generation; std::function<void(F04Session*)> visit; std::promise<Result> reply; };
    using Request = std::variant<Check, PreparePlayer, BindPlayer, Save, Load, Dispatch,
                                 CreateAcademy, InspectAcademy, BindAcademy, InspectBoundAcademy,
                                 CreateBoundAcademy, QueryAcademy, InspectSlots, TestVisit>;
#else
    using Request = std::variant<Check, PreparePlayer, BindPlayer, Save, Load, Dispatch,
                                 CreateAcademy, InspectAcademy, BindAcademy, InspectBoundAcademy,
                                 CreateBoundAcademy, QueryAcademy, InspectSlots>;
#endif
    enum class Binding { UNBOUND, RESOLVING, BOUND, INVALID };

    std::recursive_mutex mutex;
    std::condition_variable_any work;
    State state = State::CLOSED;
    Generation generation;
    std::shared_ptr<const detail::ActiveCampaign> campaign;
    std::shared_ptr<const int> biography_activation;
    std::string local_profile;
    detail::AcademyIntent academy_intent;
    detail::AcademyReceipt academy_receipt;
    // One bounded product retry record. The high-water key survives invalidation;
    // the weak intent cannot keep a retired activation authorized.
    std::uint64_t academy_product_key = 0;
    std::string academy_product_payload;
    std::weak_ptr<const detail::AcademyCreationIntent> academy_product_intent;
    Binding binding = Binding::UNBOUND;
    F04Ref player{};
    std::shared_ptr<const detail::AcademyAnchor> academy_player;
    bool stopping = false;
    std::optional<Open> opening;
    std::optional<std::promise<Result>> closing;
    std::shared_future<Result> close_result;
    std::deque<Request> requests;
    static constexpr std::size_t max_requests = 32;
    detail::SlotStore store;
    std::string persistent_id;
    Provenance provenance=Provenance::REJECTED;
    std::thread owner;

    explicit Impl(StorageConfig config) : store(std::move(config)),owner([this] { run(); }) {}

    ~Impl()
    {
        if (std::this_thread::get_id() == owner.get_id()) {
            std::terminate();
        }
        {
            std::lock_guard lock(mutex);
            stopping = true;
            if (state != State::CLOSED) {
                state = State::CLOSING;
                invalidate();
            }
        }
        work.notify_one();
        owner.join();
    }

    // Caller holds mutex. Complete queued work before the session can be destroyed.
    void invalidate()
    {
        academy_player.reset();
        academy_receipt.reset();
        academy_intent.reset();
        biography_activation.reset();
        generation = {};
        campaign.reset();
        binding = Binding::UNBOUND;
        player = {};
        persistent_id.clear();
        provenance=Provenance::REJECTED;
        for (auto& request : requests) {
            std::visit([](auto& item) {
                if constexpr (std::is_same_v<std::decay_t<decltype(item)>, Dispatch>)
                    item.reply.set_value({Error::GENERATION_EXPIRED, {}, item.request.correlation});
                else item.reply.set_value({Error::GENERATION_EXPIRED, {}});
            }, request);
        }
        requests.clear();
    }

    Error admission(Generation requested) const noexcept
    {
        if (requested == Generation{}) {
            if (state == State::CLOSED) {
                return Error::SESSION_CLOSED;
            }
            return state == State::ACTIVE ? Error::INVALID_ARGUMENT : Error::BUSY_STATE;
        }
        if (requested != generation) {
            return Error::GENERATION_EXPIRED;
        }
        return state == State::ACTIVE ? Error::OK : Error::BUSY_STATE;
    }

    template<class Reply, class Item>
    std::future<Reply> enqueue(Item request)
    {
        std::lock_guard lock(mutex);
        auto reject = [&](Error error) {
            if constexpr (std::is_same_v<Item, Dispatch>) {
                std::promise<Reply> promise;
                auto future = promise.get_future();
                promise.set_value({error, {}, request.request.correlation});
                return future;
            } else return ready<Reply>(error);
        };
        if (const auto error = admission(request.generation); error != Error::OK) {
            return reject(error);
        }
        if constexpr (std::is_same_v<Item, Dispatch>) {
            if (binding != Binding::BOUND)
                return reject(binding == Binding::INVALID ? Error::ACCESS_DENIED : Error::PRINCIPAL_UNBOUND);
        }
        if (requests.size() == max_requests) {
            return reject(Error::CAPACITY_LIMIT);
        }
        auto reply = request.reply.get_future();
        requests.emplace_back(std::move(request));
        work.notify_one();
        return reply;
    }

    void finish_open(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session, Open request)
    {
        if (state == State::CLOSING) {
            request.reply.set_value({Error::BUSY_STATE, {}});
            return;
        }

        std::string id;
        try {id=detail::new_campaign_id();}catch(...){state=State::CLOSED;request.reply.set_value({Error::INTERNAL_ERROR,{}});return;}
        lock.unlock();
        auto outcome = session.open(request.config);
        lock.lock();
        if (outcome.error == Error::OK && state == State::OPENING) {
            const auto next = next_generation();
            if (next != 0) {
                generation = Generation(next);
                campaign = std::move(request.campaign);
                persistent_id=std::move(id);
                provenance=Provenance::CREATED_LOCALLY;
                state = State::ACTIVE;
                request.reply.set_value({Error::OK, generation});
                return;
            }
            outcome.error = Error::INTERNAL_ERROR;
        }

        if (outcome.error != Error::OK) {
            report_failure("open", outcome);
        }
        if (state == State::OPENING) {
            state = State::FAILED;
        }
        lock.unlock();
        const auto cleanup = session.close();
        lock.lock();
        if (cleanup.error != Error::OK) {
            report_failure("open cleanup", cleanup);
        }
        // An admitted close owns the final state, even when open already cleaned up.
        if (state == State::FAILED) {
            state = cleanup.error == Error::OK ? State::CLOSED : State::FAILED;
        }
        const auto error = outcome.error == Error::OK ? Error::BUSY_STATE : outcome.error;
        request.reply.set_value({error, {}});
    }

    Error academy_admission(const detail::AcademyIntent& intent) const noexcept
    {
        if (!intent || intent != academy_intent || intent->profile != local_profile) return Error::SCOPE_INVALID;
        if (state == State::CLOSED || state == State::OPENING) return Error::OK;
        return admission(intent->generation);
    }

    Error academy_receipt_admission(Generation requested, const detail::AcademyReceipt& receipt) const noexcept
    {
        if (const auto error = admission(requested); error != Error::OK) return error;
        if (!receipt || receipt != academy_receipt || receipt->intent->generation != requested ||
            academy_admission(receipt->intent) != Error::OK || receipt->intent->campaign != persistent_id) {
            return Error::SCOPE_INVALID;
        }
        return Error::OK;
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session, CreateAcademy& request)
    {
        auto fail = [&](Error error) { request.reply.set_value({error, {}, {}}); };
        if (const auto error = academy_admission(request.intent); error != Error::OK) { fail(error); return; }
        if (state == State::ACTIVE) {
            try {
                if (!academy_receipt || !session.academy()) { fail(Error::INTERNAL_ERROR); return; }
                const auto name = detail::academy_display_name(request.payload);
                if (!name || detail::academy_digest(*name) != academy_receipt->editable_digest) {
                    fail(Error::IDEMPOTENCY_CONFLICT);
                    return;
                }
                request.reply.set_value({Error::OK, generation, academy_receipt});
            } catch (...) { fail(Error::INTERNAL_ERROR); }
            return;
        }

        state = State::OPENING;
        lock.unlock();
        Error error = Error::OK;
        std::unique_ptr<detail::AcademyCampaign> staged;
        detail::AcademyReceipt receipt;
        std::string id;
        try {
            const auto name = detail::academy_display_name(request.payload);
            if (!name) {
                error = Error::INVALID_ARGUMENT;
            } else {
                staged = detail::AcademyCampaign::stage(request.intent->campaign, *name);
                auto view = staged->inspect();
                if (view.campaign_id != request.intent->campaign || view.display_name != *name)
                    throw std::logic_error("F10 staged identity mismatch");
                id = std::move(view.campaign_id);
                receipt = std::make_shared<const detail::AcademyCreationReceipt>(detail::AcademyCreationReceipt{
                    request.intent, detail::academy_digest(*name), std::move(view.source_digest),
                    view.person, view.creation_fact, view.revision, view.tick});
#ifdef TREK_HOST_ACADEMY_TESTING
                detail::academy_fail_at(detail::AcademyFault::BEFORE_PUBLICATION);
#endif
            }
        } catch (const detail::UnapprovedAcademySource&) {
            error = Error::DOMAIN_REJECTED;
        } catch (...) {
            error = Error::INTERNAL_ERROR;
        }
        lock.lock();
        if (state != State::OPENING || request.intent != academy_intent) {
            fail(Error::GENERATION_EXPIRED);
            return;
        }
        if (error == Error::OK) error = session.commit_academy(std::move(staged)).error;
        if (error != Error::OK) {
            state = State::CLOSED;
            fail(error);
            return;
        }

        // The Core world and all receipt data were prepared on this thread.
        // The remaining moves publish one complete activation under the mutex.
        biography_activation.reset();
        generation = request.intent->generation;
        persistent_id = std::move(id);
        provenance = Provenance::CREATED_LOCALLY;
        academy_receipt = std::move(receipt);
        state = State::ACTIVE;
        request.reply.set_value({Error::OK, generation, academy_receipt});
    }

    void execute(std::unique_lock<std::recursive_mutex>&, detail::NativeSession& session, InspectAcademy& request)
    {
        if (const auto error = academy_receipt_admission(request.generation, request.receipt); error != Error::OK) {
            request.reply.set_value({error, {}});
            return;
        }
        if (!session.academy()) {
            request.reply.set_value({Error::SCOPE_INVALID, {}});
            return;
        }
        try {
            request.reply.set_value(inspect_academy_receipt(*session.academy(), *request.receipt));
        } catch (...) {
            request.reply.set_value({Error::INTERNAL_ERROR, {}});
        }
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session, BindAcademy& request)
    {
        auto fail = [&](Error error) { request.reply.set_value({error, {}}); };
        if (const auto error = academy_receipt_admission(request.generation, request.receipt); error != Error::OK) {
            fail(error);
            return;
        }
        const auto* academy = session.academy();
        if (!academy || (binding != Binding::UNBOUND && !academy_player)) {
            fail(Error::IDENTITY_MISMATCH);
            return;
        }

        // Core reads stay on this thread. Close can revoke the scope during validation.
        const auto prior = academy_player;
        lock.unlock();
        Error validation;
        std::shared_ptr<const detail::AcademyAnchor> resolved;
        try {
            auto inspected = inspect_academy_receipt(*academy, *request.receipt);
            validation = inspected.error;
            if (inspected.candidate) {
                auto anchor = detail::academy_identity(*inspected.candidate, request.receipt->intent->profile).anchor;
                if (prior && *prior != anchor) validation = Error::IDENTITY_MISMATCH;
                else if (!prior) resolved = std::make_shared<const detail::AcademyAnchor>(std::move(anchor));
            }
#ifdef TREK_HOST_ACADEMY_TESTING
            if (auto hook = academy_bind_test_hook.load()) hook();
#endif
        } catch (const std::logic_error&) {
            validation = Error::IDENTITY_MISMATCH;
        } catch (...) {
            validation = Error::INTERNAL_ERROR;
        }
        lock.lock();
        if (const auto error = academy_receipt_admission(request.generation, request.receipt); error != Error::OK) {
            fail(error);
            return;
        }
        if (validation != Error::OK) {
            fail(validation);
            return;
        }
        if (binding == Binding::UNBOUND) {
            academy_player = std::move(resolved);
            binding = Binding::BOUND;
        }
        request.reply.set_value({Error::OK, request.generation});
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session,
                 InspectBoundAcademy& request)
    {
        const auto* academy = session.academy();
        const auto anchor = academy_player;
        if (!academy || !anchor || binding != Binding::BOUND) {
            request.reply.set_value({Error::PRINCIPAL_UNBOUND, {}});
            return;
        }
        lock.unlock();
        detail::AcademyCandidateResult result{Error::INTERNAL_ERROR, {}};
        try {
            auto view = academy->inspect_checkpoint();
            if (detail::academy_identity(view, anchor->profile).anchor == *anchor)
                result = {Error::OK, std::move(view)};
            else result.error = Error::IDENTITY_MISMATCH;
        } catch (...) {}
        lock.lock();
        if (const auto error = admission(request.generation); error != Error::OK) result = {error, {}};
        if (result.candidate && result.candidate->campaign_id != persistent_id)
            result = {Error::IDENTITY_MISMATCH, {}};
        request.reply.set_value(std::move(result));
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session,
                 CreateBoundAcademy& request)
    {
        // Compose the existing B02/B03 handlers on this same worker. Their local
        // promises are completed synchronously by execute; get never waits for
        // queued work. No observation or polling is needed to advance the bind.
        CreateAcademy create{request.intent, std::move(request.payload), {}};
        auto created_reply = create.reply.get_future();
        execute(lock, session, create);
        auto created = created_reply.get();
        if (created.error != Error::OK) {
            request.reply.set_value({created.error, {}});
            return;
        }
        BindAcademy bind{created.generation, std::move(created.receipt), {}};
        auto bound_reply = bind.reply.get_future();
        execute(lock, session, bind);
        const auto bound = bound_reply.get();
        if (bound.error != Error::OK) {
            // Keep B02's private receipt for an idempotent retry. Only a
            // confirmed binding may be queried or persisted. CLOSE revokes it.
            request.reply.set_value({bound.error, {}});
            return;
        }
        QueryAcademy query{bound.generation, std::move(request.reply)};
        execute(lock, session, query);
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session,
                 QueryAcademy& request)
    {
        InspectBoundAcademy inspect{request.generation, {}};
        auto reply = inspect.reply.get_future();
        execute(lock, session, inspect);
        auto result = reply.get();
        request.reply.set_value({result.error, result.error == Error::OK ? request.generation : Generation{},
                                 std::move(result.candidate)});
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession&, InspectSlots& request)
    {
        const auto expected = request.generation;
        lock.unlock();
        auto inspected = store.inspect(verify_slot, 64);
        lock.lock();
        if (generation != expected || (state != State::ACTIVE && state != State::CLOSED))
            inspected = {Error::GENERATION_EXPIRED, {}};
        if (inspected.error != Error::OK) inspected.slots.clear();
        request.reply.set_value({inspected.error, inspected.error == Error::OK ? expected : Generation{},
                                 {}, std::move(inspected.slots)});
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session, Check& check)
    {
        lock.unlock();
        const auto outcome = session.probe();
        if (outcome.error != Error::OK) {
            report_failure("liveness check", outcome);
        }
        lock.lock();
        const auto current = admission(check.generation);
        const auto result = current == Error::OK ? outcome.error : current;
        if (current == Error::OK && outcome.error != Error::OK) {
            invalidate();
            state = State::FAILED;
        }
        check.reply.set_value({result, result == Error::OK ? check.generation : Generation{}});
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session,
                 PreparePlayer& request)
    {
        if (session.academy() || binding == Binding::INVALID) {
            request.reply.set_value({Error::ACCESS_DENIED, {}});
            return;
        }
        F04Ref person{};
        std::uint64_t revision = 0;
        lock.unlock();
        const auto outcome = session.resolve_person(request.person_id, person, revision);
        lock.lock();
        if (const auto error = admission(request.generation); error != Error::OK) {
            request.reply.set_value({error, {}});
        } else if (outcome.error != Error::OK) {
            request.reply.set_value({outcome.error, outcome.domain_code});
        } else {
            request.reply.set_value({Error::OK, {}, PlayerSelection(campaign, person), revision});
        }
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session, BindPlayer& request)
    {
        if (session.academy() || request.selection.campaign_.lock() != campaign) {
            request.reply.set_value({Error::SCOPE_INVALID, {}});
            return;
        }
        if (binding == Binding::INVALID) {
            request.reply.set_value({Error::ACCESS_DENIED, {}});
            return;
        }

        const auto person = request.selection.person_;
        const bool first = binding == Binding::UNBOUND;
        if (first) {
            binding = Binding::RESOLVING;
        }
        // Close can invalidate immediately while F05 runs. It destroys the
        // Core only after this owner finishes the already-dispatched call.
        lock.unlock();
        const auto outcome = session.bind_player(person, request.revision);
        lock.lock();
        if (const auto error = admission(request.generation); error != Error::OK) {
            request.reply.set_value({error, {}});
            return;
        }
        if (outcome.error == Error::OK) {
            player = person;
            binding = Binding::BOUND;
        } else if (first) {
            binding = outcome.error == Error::IDEMPOTENCY_CONFLICT ? Binding::INVALID : Binding::UNBOUND;
        }
        request.reply.set_value({outcome.error, outcome.domain_code});
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session, Save& request)
    {
        const auto* academy = session.academy();
        if (academy && !store.configured()) { request.reply.set_value({Error::SAVE_INCOMPATIBLE, {}}); return; }
        if(binding!=Binding::BOUND){request.reply.set_value({Error::PRINCIPAL_UNBOUND,{}});return;}
        const auto id=persistent_id;const auto expected_player=player;
        const auto anchor=academy_player;
        state=State::SAVING;
        lock.unlock();
        Error error=Error::PERSISTENCE_FAILED;
        try {
            if (academy) {
                const auto view=academy->inspect();
                if (!anchor || view.campaign_id!=id) error=Error::IDENTITY_MISMATCH;
                else {
                    auto identity=detail::academy_identity(view,anchor->profile);
                    if (identity.anchor!=*anchor) error=Error::IDENTITY_MISMATCH;
                    else error=store.save(id,request.slot,std::move(identity),
                        [&](const auto& path) { return academy->snapshot(path,detail::decode_campaign(id)); },
                        verify_academy_slot);
                }
            } else {
                detail::PersistentIdentity identity{};F04Ref resolved{};
                auto outcome=session.persistent_identity(identity,resolved);
                if(outcome.error!=Error::OK || resolved.scope!=expected_player.scope || resolved.id!=expected_player.id)error=Error::IDENTITY_MISMATCH;
                else error=store.save(id,request.slot,identity,
                    [&](const auto& path){return session.snapshot(path,detail::decode_campaign(id)).error;},
                    [&](const detail::PreparedSlot& prepared){
                        F04Ref verified{};auto result=session.stage(prepared,verified);
                        auto cleanup=session.discard_stage();
                        return cleanup.error==Error::OK?result.error:cleanup.error;
                    });
            }
        }catch(const detail::StorageFailure& e){error=e.error;}catch(...){error=Error::PERSISTENCE_FAILED;}
        lock.lock();
        if(state==State::SAVING)state=State::ACTIVE;
        if(generation!=request.generation)error=Error::GENERATION_EXPIRED;
        request.reply.set_value({error,error==Error::OK?generation:Generation{}});
    }

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session, Dispatch& request)
    {
        auto fail = [&](Error error) {
            request.reply.set_value({error, {}, request.request.correlation});
        };
        if (const auto error = admission(request.generation); error != Error::OK) { fail(error); return; }
        if (binding != Binding::BOUND) {
            fail(binding == Binding::INVALID ? Error::ACCESS_DENIED : Error::PRINCIPAL_UNBOUND); return;
        }
        if (session.academy()) {
            fail(Error::ACCESS_DENIED);
            return;
        }
        const auto principal = player;
        OperationResult reply;
        lock.unlock();
        const auto outcome = session.dispatch(principal, request.request, reply);
        report_failure("gateway", outcome); // Raw code remains in private native diagnostics.
        lock.lock();
        if (const auto error = admission(request.generation); error != Error::OK) { fail(error); return; }
        if (outcome.error != Error::OK) { fail(outcome.error); return; }
        reply.generation = request.generation;
        reply.correlation_id = request.request.correlation;
        if (reply.campaign) reply.campaign->generation = request.generation;
        if (reply.order) reply.order->generation = request.generation;
        request.reply.set_value(std::move(reply));
    }

#ifdef TREK_HOST_GATEWAY_TESTING
    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session, TestVisit& request)
    {
        lock.unlock();
        Error error = Error::OK;
        try { session.test_visit(request.visit); } catch (...) { error = Error::INTERNAL_ERROR; }
        lock.lock();
        if (const auto current = admission(request.generation); current != Error::OK) error = current;
        request.reply.set_value({error,error == Error::OK ? request.generation : Generation{}});
    }
#endif

    void execute(std::unique_lock<std::recursive_mutex>& lock, detail::NativeSession& session, Load& request)
    {
        if(state==State::CLOSING){request.reply.set_value({Error::GENERATION_EXPIRED,{}});return;}
        state=State::LOADING;
        lock.unlock();
        Error error=Error::PERSISTENCE_FAILED;F04Ref restored{};
        std::shared_ptr<const detail::ActiveCampaign> marker;
        std::unique_ptr<detail::AcademyCampaign> staged_academy;
        std::shared_ptr<const detail::AcademyAnchor> restored_anchor;
        std::string restored_profile;
        std::string id;std::uint64_t next=0;
        try {
            auto prepared=store.prepare(request.address);
            id=prepared.campaign;
            next=next_generation();
            if(!next)error=Error::INTERNAL_ERROR;
            else if (const auto* identity=std::get_if<detail::AcademySnapshotIdentity>(&prepared.identity)) {
                staged_academy=detail::AcademyCampaign::restore(prepared);
                restored_anchor=std::make_shared<const detail::AcademyAnchor>(identity->anchor);
                restored_profile=identity->anchor.profile;
                error=Error::OK;
            }
            else {
                marker=std::make_shared<const detail::ActiveCampaign>();
                auto outcome=session.stage(prepared,restored);error=outcome.error;
                if(outcome.domain_code==F04_DENIED)error=Error::IDENTITY_MISMATCH;
                else if(outcome.domain_code==F04_SAVE)error=Error::SAVE_CORRUPT;
            }
        }catch(const detail::StorageFailure& e){error=e.error;}
         catch(const detail::UnapprovedAcademySource&){error=Error::SAVE_INCOMPATIBLE;}
         catch(...){error=Error::PERSISTENCE_FAILED;}
        lock.lock();
        if(state==State::CLOSING)error=Error::GENERATION_EXPIRED;
        if(error==Error::OK) {
            // All allocation, Core validation and scope renewal finished before
            // this mutex-protected publication. No old request survives the swap.
            auto outcome=staged_academy ? session.commit_academy(std::move(staged_academy)) : session.commit_stage();
            error=outcome.error;
            if(error==Error::OK) {
                invalidate();campaign=std::move(marker);persistent_id=std::move(id);
                if (restored_anchor) {
                    academy_player=std::move(restored_anchor);
                    local_profile=std::move(restored_profile);
                } else player=restored;
                provenance=Provenance::KNOWN_LOCAL;generation=Generation(next);binding=Binding::BOUND;state=State::ACTIVE;
            }
        }
        if(error!=Error::OK) {
            lock.unlock();auto cleanup=session.discard_stage();lock.lock();
            if(cleanup.error!=Error::OK)error=cleanup.error;
            if(state==State::LOADING)state=request.had_active?State::ACTIVE:State::CLOSED;
        }
        request.reply.set_value({error,error==Error::OK?generation:Generation{}});
    }

    void run()
    {
        detail::NativeSession session;
        std::unique_lock lock(mutex);
        for (;;) {
            work.wait(lock, [this] { return stopping || opening || closing || !requests.empty(); });
            if (opening) {
                auto request = std::move(*opening);
                opening.reset();
                finish_open(lock, session, std::move(request));
                continue;
            }
            if (closing || stopping) {
                lock.unlock();
                auto outcome = session.close();
                if (outcome.error != Error::OK) {
                    report_failure("close", outcome);
                }
                lock.lock();
                state = outcome.error == Error::OK ? State::CLOSED : State::FAILED;
                if (closing) {
                    closing->set_value({outcome.error, {}});
                    closing.reset();
                    close_result = {};
                }
                if (stopping && outcome.error == Error::OK) {
                    return;
                }
                if (stopping) {
                    // The real bridge can only refuse a null or wrong-thread destroy.
                    // Retry once on this owner, then fail closed if its invariant is broken.
                    lock.unlock();
                    outcome = session.close();
                    if (outcome.error != Error::OK) {
                        report_failure("shutdown retry", outcome);
                        std::terminate();
                    }
                    return;
                }
                continue;
            }

            // Admission and invalidation use this same mutex. Only requests
            // of the active generation can remain in the queue.
            auto request = std::move(requests.front());
            requests.pop_front();
            std::visit([&](auto& item) { execute(lock, session, item); }, request);
        }
    }
};

detail::AbiAdmission::AbiAdmission(SessionOwner& owner)
    : owner_(owner), lock_(owner.impl_->mutex, std::try_to_lock) {}

std::uint64_t detail::AbiAdmission::token(Generation generation) noexcept
{
    return generation.value_;
}

std::string_view detail::AbiAdmission::campaign() const noexcept
{
    return owner_.impl_->persistent_id;
}

SessionOwner::SessionOwner() : SessionOwner(StorageConfig{}) {}
SessionOwner::SessionOwner(StorageConfig storage) : impl_(std::make_unique<Impl>(std::move(storage))) {}
SessionOwner::~SessionOwner() = default;

std::future<Result> SessionOwner::open(PopulationConfig config)
{
    std::lock_guard lock(impl_->mutex);
    if (impl_->state != State::CLOSED) {
        return ready(Error::BUSY_STATE);
    }
    if (config.class_id.empty() || config.class_id.find('\0') != std::string::npos) {
        return ready(Error::INVALID_ARGUMENT);
    }
    impl_->biography_activation.reset();
    impl_->academy_intent.reset();
    Impl::Open request{std::move(config), std::make_shared<const detail::ActiveCampaign>(), {}};
    auto reply = request.reply.get_future();
    impl_->opening.emplace(std::move(request));
    impl_->state = State::OPENING;
    impl_->work.notify_one();
    return reply;
}

std::shared_future<Result> SessionOwner::close()
{
    std::lock_guard lock(impl_->mutex);
    impl_->biography_activation.reset();
    if (impl_->closing) {
        return impl_->close_result;
    }
    if (impl_->state == State::CLOSED) {
        impl_->academy_intent.reset();
        return ready(Error::OK).share();
    }
    std::promise<Result> reply;
    impl_->close_result = reply.get_future().share();
    impl_->closing.emplace(std::move(reply));
    impl_->state = State::CLOSING;
    impl_->invalidate();
    impl_->work.notify_one();
    return impl_->close_result;
}

Snapshot SessionOwner::snapshot() const
{
    std::lock_guard lock(impl_->mutex);
    return {impl_->state, impl_->generation};
}

std::future<Result> SessionOwner::check_active(Generation generation)
{
    return impl_->enqueue<Result>(Impl::Check{generation, {}});
}

std::future<OperationResult> SessionOwner::query_view(Generation generation, std::uint64_t correlation)
{
    return impl_->enqueue<OperationResult>(Impl::Dispatch{generation,{detail::GatewayOp::VIEW,{},0,0,correlation},{}});
}
std::future<OperationResult> SessionOwner::submit_order(Generation generation, OrderIntent intent, std::uint64_t correlation)
{
    return impl_->enqueue<OperationResult>(Impl::Dispatch{generation,{detail::GatewayOp::SUBMIT,intent,0,0,correlation},{}});
}
std::future<OperationResult> SessionOwner::query_order(Generation generation, std::uint64_t order, std::uint64_t correlation)
{
    return impl_->enqueue<OperationResult>(Impl::Dispatch{generation,{detail::GatewayOp::ORDER,{},order,0,correlation},{}});
}
std::future<OperationResult> SessionOwner::cancel_order(Generation generation, std::uint64_t order,
    std::uint64_t revision, std::uint64_t correlation)
{
    return impl_->enqueue<OperationResult>(Impl::Dispatch{generation,{detail::GatewayOp::CANCEL,{},order,revision,correlation},{}});
}
std::future<OperationResult> SessionOwner::institutional_command(Generation generation, std::uint64_t correlation)
{
    return impl_->enqueue<OperationResult>(Impl::Dispatch{generation,{detail::GatewayOp::INSTITUTIONAL,{},0,0,correlation},{}});
}
#ifdef TREK_HOST_GATEWAY_TESTING
std::future<Result> GatewayTestAccess::visit(SessionOwner& owner, Generation generation, std::function<void(F04Session*)> visit)
{
    return owner.impl_->enqueue<Result>(SessionOwner::Impl::TestVisit{generation,std::move(visit),{}});
}
#endif

std::string SessionOwner::campaign_id(Generation generation) const
{
    std::lock_guard lock(impl_->mutex);
    return impl_->admission(generation)==Error::OK?impl_->persistent_id:std::string{};
}
Provenance SessionOwner::campaign_provenance(Generation generation) const
{
    std::lock_guard lock(impl_->mutex);
    return impl_->admission(generation)==Error::OK?impl_->provenance:Provenance::REJECTED;
}
std::future<Result> SessionOwner::save(Generation generation,std::string slot)
{
    if(!detail::valid_slot(slot))return ready(Error::PATH_REJECTED);
    return impl_->enqueue<Result>(Impl::Save{generation,std::move(slot),{}});
}
std::future<Result> SessionOwner::restore(Generation generation,SlotAddress address)
{
    std::lock_guard lock(impl_->mutex);
    const bool active=impl_->state==State::ACTIVE;
    if(impl_->state!=State::CLOSED) {
        if(auto error=impl_->admission(generation);error!=Error::OK)return ready(error);
        if (impl_->academy_receipt || impl_->academy_player)
            return ready(impl_->store.configured()?Error::BUSY_STATE:Error::SAVE_INCOMPATIBLE);
        if (address.kind==CampaignKind::ACADEMY) return ready(Error::BUSY_STATE);
        address.kind=CampaignKind::NAVAL;
    } else if(generation!=Generation{})return ready(Error::GENERATION_EXPIRED);
    if(impl_->requests.size()==Impl::max_requests)return ready(Error::CAPACITY_LIMIT);
    impl_->academy_intent.reset();
    Impl::Load request{generation,std::move(address),active,{}};auto result=request.reply.get_future();
    impl_->biography_activation.reset();
    impl_->requests.emplace_back(std::move(request));if(!active)impl_->state=State::LOADING;
    impl_->work.notify_one();return result;
}
InspectionResult SessionOwner::inspect(const StorageConfig& config)
{
    return detail::SlotStore(config).inspect(verify_slot);
}

PlayerResult SessionOwner::current_player(Generation generation) const
{
    std::lock_guard lock(impl_->mutex);
    if (const auto error = impl_->admission(generation); error != Error::OK) {
        return {error, std::nullopt};
    }
    switch (impl_->binding) {
    case Impl::Binding::BOUND: {
        const auto person = impl_->academy_player ? impl_->academy_player->person : impl_->player.id;
        return {Error::OK, PlayerIdentity{generation, person}};
    }
    case Impl::Binding::INVALID: return {Error::ACCESS_DENIED, std::nullopt};
    default: return {Error::PRINCIPAL_UNBOUND, std::nullopt};
    }
}

std::future<PlayerSelectionResult> PlayerBootstrap::prepare(
    SessionOwner& owner, Generation generation, std::uint64_t created_person)
{
    return owner.impl_->enqueue<PlayerSelectionResult>(
        SessionOwner::Impl::PreparePlayer{generation, created_person, {}});
}

std::future<BindPlayerResult> PlayerBootstrap::bind(
    SessionOwner& owner, Generation generation, const PlayerSelection& selection,
    std::uint64_t expected_revision)
{
    return owner.impl_->enqueue<BindPlayerResult>(
        SessionOwner::Impl::BindPlayer{generation, selection, expected_revision, {}});
}

std::future<detail::AcademyInterfaceResult> detail::AcademyInterface::create_bound(
    SessionOwner& owner, std::uint64_t key, std::string payload)
{
    auto& impl = *owner.impl_;
    std::lock_guard lock(impl.mutex);
    const auto reject = [](Error error) { return ready<AcademyInterfaceResult>(error); };
    if (!key || !academy_display_name(payload)) return reject(Error::INVALID_ARGUMENT);
    if (impl.requests.size() == SessionOwner::Impl::max_requests) return reject(Error::CAPACITY_LIMIT);
    AcademyIntent intent;
    if (key < impl.academy_product_key) return reject(Error::GENERATION_EXPIRED);
    if (key == impl.academy_product_key) {
        intent = impl.academy_product_intent.lock();
        if (!intent || intent != impl.academy_intent) return reject(Error::GENERATION_EXPIRED);
        if (payload != impl.academy_product_payload) return reject(Error::IDEMPOTENCY_CONFLICT);
        if (const auto error = impl.academy_admission(intent); error != Error::OK) return reject(error);
    } else {
        if (impl.state != State::CLOSED) return reject(Error::BUSY_STATE);
        intent = AcademyCandidateFactory::begin(owner);
        if (!intent) return reject(Error::INTERNAL_ERROR);
    }
    SessionOwner::Impl::CreateBoundAcademy request{intent, payload, {}};
    auto future = request.reply.get_future();
    impl.requests.emplace_back(std::move(request));
    impl.academy_product_key = key;
    impl.academy_product_payload = std::move(payload);
    impl.academy_product_intent = intent;
    if (impl.state == State::CLOSED) impl.state = State::OPENING;
    impl.work.notify_one();
    return future;
}

std::future<detail::AcademyInterfaceResult> detail::AcademyInterface::query(SessionOwner& owner, Generation generation)
{
    return owner.impl_->enqueue<AcademyInterfaceResult>(SessionOwner::Impl::QueryAcademy{generation, {}});
}

std::future<detail::AcademyInterfaceResult> detail::AcademyInterface::slots(SessionOwner& owner, Generation generation)
{
    auto& impl = *owner.impl_;
    std::lock_guard lock(impl.mutex);
    if (generation != impl.generation) return ready<AcademyInterfaceResult>(Error::GENERATION_EXPIRED);
    if (impl.state != State::CLOSED && impl.state != State::ACTIVE)
        return ready<AcademyInterfaceResult>(Error::BUSY_STATE);
    if (impl.requests.size() == SessionOwner::Impl::max_requests)
        return ready<AcademyInterfaceResult>(Error::CAPACITY_LIMIT);
    SessionOwner::Impl::InspectSlots request{generation, {}};
    auto future = request.reply.get_future();
    impl.requests.emplace_back(std::move(request));
    impl.work.notify_one();
    return future;
}

detail::AcademyIntent detail::AcademyCandidateFactory::begin(SessionOwner& owner)
{
    std::lock_guard lock(owner.impl_->mutex);
    auto& impl = *owner.impl_;
    if (impl.stopping) return {};
    if (impl.academy_intent && impl.academy_admission(impl.academy_intent) == Error::OK) return impl.academy_intent;
    if (impl.state != State::CLOSED) return {};

    auto campaign = detail::new_campaign_id();
    (void)detail::decode_campaign(campaign);
    if (impl.local_profile.empty()) impl.local_profile = detail::new_campaign_id();
    const auto next = next_generation();
    if (!next) return {};
    auto intent = std::make_shared<const AcademyCreationIntent>(
        AcademyCreationIntent{Generation(next), std::move(campaign), impl.local_profile});
    impl.biography_activation.reset();
    impl.academy_intent = std::move(intent);
    return impl.academy_intent;
}

std::future<detail::AcademyCreationResult> detail::AcademyCandidateFactory::create(
    SessionOwner& owner, const AcademyIntent& intent, std::string_view payload)
{
    auto& impl = *owner.impl_;
    std::lock_guard lock(impl.mutex);
    if (const auto error = impl.academy_admission(intent); error != Error::OK)
        return ready<AcademyCreationResult>(error);
    if (payload.empty() || payload.size() > academy_payload_limit)
        return ready<AcademyCreationResult>(Error::INVALID_ARGUMENT);
    if (impl.requests.size() == SessionOwner::Impl::max_requests)
        return ready<AcademyCreationResult>(Error::CAPACITY_LIMIT);
    SessionOwner::Impl::CreateAcademy request{intent, std::string(payload), {}};
    auto future = request.reply.get_future();
    impl.requests.emplace_back(std::move(request));
    impl.work.notify_one();
    return future;
}

std::future<detail::AcademyCandidateResult> detail::AcademyCandidateFactory::inspect(
    SessionOwner& owner, const AcademyReceipt& receipt)
{
    auto& impl = *owner.impl_;
    std::lock_guard lock(impl.mutex);
    if (!receipt || receipt != impl.academy_receipt) return ready<AcademyCandidateResult>(Error::SCOPE_INVALID);
    return impl.enqueue<AcademyCandidateResult>(
        SessionOwner::Impl::InspectAcademy{receipt->intent->generation, receipt, {}});
}

std::future<Result> detail::AcademyPlayerBinding::bind(
    SessionOwner& owner, Generation generation, const AcademyReceipt& receipt)
{
    return owner.impl_->enqueue<Result>(SessionOwner::Impl::BindAcademy{generation, receipt, {}});
}

std::future<detail::AcademyCandidateResult> detail::AcademyPlayerBinding::inspect(SessionOwner& owner, Generation generation)
{
    return owner.impl_->enqueue<detail::AcademyCandidateResult>(
        SessionOwner::Impl::InspectBoundAcademy{generation, {}});
}

#ifdef TREK_HOST_ACADEMY_TESTING
void detail::set_academy_bind_test_hook(void (*hook)()) noexcept
{
    academy_bind_test_hook.store(hook);
}
#endif

} // namespace trek::host

std::shared_ptr<const trek::host::detail::BiographyProfileSource>
trek::host::detail::BiographyProfileSource::begin(SessionOwner& owner) {
    std::lock_guard lock(owner.impl_->mutex);
    if (owner.impl_->state != State::CLOSED || owner.impl_->stopping) return {};
    if (owner.impl_->local_profile.empty()) owner.impl_->local_profile = detail::new_campaign_id();
    const auto generation = next_generation();
    if (!generation) return {};
    auto activation = std::make_shared<const int>(0);
    auto source = std::shared_ptr<const BiographyProfileSource>(new BiographyProfileSource(
        {"starfleet_academy", "tng_ds9_voyager", 2383, "", detail::new_campaign_id(),
         generation, owner.impl_->local_profile}, activation));
    owner.impl_->academy_intent.reset();
    owner.impl_->biography_activation = std::move(activation);
    return source;
}
