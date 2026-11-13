#include "trek/host/session_owner.h"

#include "abi_admission.h"
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
#include <thread>
#include <type_traits>
#include <string_view>
#include <utility>
#include <variant>

namespace trek::host {
namespace {

constinit std::atomic<std::uint64_t> last_generation{0};

std::uint64_t next_generation() noexcept
{
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

    struct Save { Generation generation;std::string slot;std::promise<Result> reply; };
    struct Load { Generation generation;SlotAddress address;bool had_active;std::promise<Result> reply; };
    struct Dispatch { Generation generation; detail::GatewayRequest request; std::promise<OperationResult> reply; };
#ifdef TREK_HOST_GATEWAY_TESTING
    struct TestVisit { Generation generation; std::function<void(F04Session*)> visit; std::promise<Result> reply; };
    using Request = std::variant<Check, PreparePlayer, BindPlayer, Save, Load, Dispatch, TestVisit>;
#else
    using Request = std::variant<Check, PreparePlayer, BindPlayer, Save, Load, Dispatch>;
#endif
    enum class Binding { UNBOUND, RESOLVING, BOUND, INVALID };

    std::recursive_mutex mutex;
    std::condition_variable_any work;
    State state = State::CLOSED;
    Generation generation;
    std::shared_ptr<const detail::ActiveCampaign> campaign;
    Binding binding = Binding::UNBOUND;
    F04Ref player{};
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
        if (binding == Binding::INVALID) {
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
        if (request.selection.campaign_.lock() != campaign) {
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
        if(binding!=Binding::BOUND){request.reply.set_value({Error::PRINCIPAL_UNBOUND,{}});return;}
        state=State::SAVING;
        const auto id=persistent_id;const auto expected_player=player;
        lock.unlock();
        Error error=Error::PERSISTENCE_FAILED;
        try {
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
        std::string id;std::uint64_t next=0;
        try {
            auto prepared=store.prepare(request.address);
            marker=std::make_shared<const detail::ActiveCampaign>();id=prepared.campaign;
            next=next_generation();
            if(!next)error=Error::INTERNAL_ERROR;
            else {
                auto outcome=session.stage(prepared,restored);error=outcome.error;
                if(outcome.domain_code==F04_DENIED)error=Error::IDENTITY_MISMATCH;
                else if(outcome.domain_code==F04_SAVE)error=Error::SAVE_CORRUPT;
            }
        }catch(const detail::StorageFailure& e){error=e.error;}catch(...){error=Error::PERSISTENCE_FAILED;}
        lock.lock();
        if(state==State::CLOSING)error=Error::GENERATION_EXPIRED;
        if(error==Error::OK) {
            // All allocation, Core validation and scope renewal finished before
            // this mutex-protected publication. No old request survives the swap.
            auto outcome=session.commit_stage();error=outcome.error;
            if(error==Error::OK) {
                invalidate();campaign=std::move(marker);persistent_id=std::move(id);
                provenance=Provenance::KNOWN_LOCAL;generation=Generation(next);player=restored;binding=Binding::BOUND;state=State::ACTIVE;
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
    if (impl_->closing) {
        return impl_->close_result;
    }
    if (impl_->state == State::CLOSED) {
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
    } else if(generation!=Generation{})return ready(Error::GENERATION_EXPIRED);
    if(impl_->requests.size()==Impl::max_requests)return ready(Error::CAPACITY_LIMIT);
    Impl::Load request{generation,std::move(address),active,{}};auto result=request.reply.get_future();
    impl_->requests.emplace_back(std::move(request));if(!active)impl_->state=State::LOADING;
    impl_->work.notify_one();return result;
}
InspectionResult SessionOwner::inspect(const StorageConfig& config)
{
    return detail::SlotStore(config).inspect([](const detail::PreparedSlot& prepared){
        const auto* sha=detail::bridge::core_sha();
        if(!sha || std::string_view(sha)!=TREK_HOST_CORE_SHA)return Error::SAVE_INCOMPATIBLE;
        F04Session* candidate=nullptr;F04Ref player{};
        auto code=detail::bridge::restore(prepared,&candidate,player);
        if(candidate)detail::bridge::destroy(candidate);
        return code==F04_OK?Error::OK:code==F04_DENIED?Error::IDENTITY_MISMATCH:Error::SAVE_CORRUPT;
    });
}

PlayerResult SessionOwner::current_player(Generation generation) const
{
    std::lock_guard lock(impl_->mutex);
    if (const auto error = impl_->admission(generation); error != Error::OK) {
        return {error, std::nullopt};
    }
    switch (impl_->binding) {
    case Impl::Binding::BOUND: return {Error::OK, PlayerIdentity{generation, impl_->player.id}};
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

} // namespace trek::host
