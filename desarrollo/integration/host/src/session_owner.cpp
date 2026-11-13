#include "trek/host/session_owner.h"

#include "native_session.h"

#include <atomic>
#include <condition_variable>
#include <cstdio>
#include <deque>
#include <exception>
#include <limits>
#include <mutex>
#include <optional>
#include <thread>
#include <utility>

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

std::future<Result> ready(Error error)
{
    std::promise<Result> reply;
    auto future = reply.get_future();
    reply.set_value({error, {}});
    return future;
}

void report_failure(const char* operation, detail::Outcome outcome) noexcept
{
    if (outcome.domain_code) {
        std::fprintf(stderr, "TrekHost: %s failed (F04 code %u)\n",
                     operation, static_cast<unsigned>(*outcome.domain_code));
    }
}

} // namespace

struct SessionOwner::Impl {
    struct Open {
        PopulationConfig config;
        std::promise<Result> reply;
    };

    struct Check {
        Generation generation;
        std::promise<Result> reply;
    };

    std::mutex mutex;
    std::condition_variable work;
    State state = State::CLOSED;
    Generation generation;
    bool stopping = false;
    std::optional<Open> opening;
    std::optional<std::promise<Result>> closing;
    std::shared_future<Result> close_result;
    std::deque<Check> checks;
    static constexpr std::size_t max_checks = 32;
    std::thread owner;

    Impl() : owner([this] { run(); }) {}

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
        for (auto& check : checks) {
            check.reply.set_value({Error::GENERATION_EXPIRED, {}});
        }
        checks.clear();
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

    void finish_open(std::unique_lock<std::mutex>& lock, detail::NativeSession& session, Open request)
    {
        if (state == State::CLOSING) {
            request.reply.set_value({Error::BUSY_STATE, {}});
            return;
        }

        lock.unlock();
        auto outcome = session.open(request.config);
        lock.lock();
        if (outcome.error == Error::OK && state == State::OPENING) {
            const auto next = next_generation();
            if (next != 0) {
                generation = Generation(next);
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

    void run()
    {
        detail::NativeSession session;
        std::unique_lock lock(mutex);
        for (;;) {
            work.wait(lock, [this] { return stopping || opening || closing || !checks.empty(); });
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

            auto check = std::move(checks.front());
            checks.pop_front();
            const auto error = admission(check.generation);
            if (error != Error::OK) {
                check.reply.set_value({error, {}});
                continue;
            }
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
    }
};

SessionOwner::SessionOwner() : impl_(std::make_unique<Impl>()) {}
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
    Impl::Open request{std::move(config), {}};
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
    std::lock_guard lock(impl_->mutex);
    const auto error = impl_->admission(generation);
    if (error != Error::OK) {
        return ready(error);
    }
    if (impl_->checks.size() == Impl::max_checks) {
        return ready(Error::CAPACITY_LIMIT);
    }
    Impl::Check check{generation, {}};
    auto reply = check.reply.get_future();
    impl_->checks.push_back(std::move(check));
    impl_->work.notify_one();
    return reply;
}

} // namespace trek::host
