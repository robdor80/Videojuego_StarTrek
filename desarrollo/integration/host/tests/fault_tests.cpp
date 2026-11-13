#include "native_session.h"
#include "player_bootstrap.h"
#include "test_support.h"

#include "f05_orders.h"

#include <atomic>
#include <chrono>
#include <iostream>
#include <semaphore>
#include <thread>

namespace {
using namespace test;
using namespace std::chrono_literals;

enum class Mode {
    normal, bad_sha, fail_create, fail_probe, pause_create, pause_probe,
    pause_destroy, fail_destroy, fail_destroy_once, pause_bind
};

std::atomic mode{Mode::normal};
std::atomic_int creates{0};
std::atomic_int destroys{0};
std::atomic_int probes{0};
std::atomic_int live{0};
std::atomic_int wrong_thread{0};
std::atomic_int binds{0};
std::atomic_int player_records{0};
std::atomic_uint bind_failure{F04_OK};
std::binary_semaphore entered{0};
std::binary_semaphore resume{0};

void wait_in_bridge() noexcept
{
    entered.release();
    if (!resume.try_acquire_for(5s)) {
        std::terminate();
    }
}

void await_bridge()
{
    require(entered.try_acquire_for(5s), "Worker did not reach bridge");
}

// Only this executable uses a replacement bridge. Each fake session is owned
// by its creating worker and all callers are checked against that thread.
} // namespace

struct F04Session {
    std::thread::id owner = std::this_thread::get_id();
    std::uint64_t revision = 1;
    std::uint64_t player = 0;
};

namespace trek::host::detail::bridge {

const char* core_sha() noexcept
{
    return mode == Mode::bad_sha ? "unapproved-core" : TREK_HOST_CORE_SHA;
}

std::uint32_t create(const PopulationConfig&, F04Session** session) noexcept
{
    ++creates;
    if (mode == Mode::pause_create) {
        wait_in_bridge();
    }
    if (mode == Mode::fail_create) {
        return F04_INTERNAL;
    }
    *session = new F04Session;
    ++live;
    return F04_OK;
}

std::uint32_t probe(F04Session* session) noexcept
{
    ++probes;
    if (session->owner != std::this_thread::get_id()) {
        ++wrong_thread;
        return F04_THREAD;
    }
    if (mode == Mode::pause_probe) {
        wait_in_bridge();
    }
    return mode == Mode::fail_probe ? F04_INTERNAL : F04_OK;
}

std::uint32_t destroy(F04Session* session) noexcept
{
    ++destroys;
    if (session->owner != std::this_thread::get_id()) {
        ++wrong_thread;
        return F04_THREAD;
    }
    if (mode == Mode::pause_destroy) {
        wait_in_bridge();
    }
    auto once = Mode::fail_destroy_once;
    if (mode.compare_exchange_strong(once, Mode::normal) || mode == Mode::fail_destroy) {
        return F04_THREAD;
    }
    delete session;
    --live;
    return F04_OK;
}

std::uint32_t resolve_person(F04Session* session, std::uint64_t person_id,
                             F04Ref& person, std::uint64_t& revision) noexcept
{
    if (session->owner != std::this_thread::get_id()) {
        ++wrong_thread;
        return F04_THREAD;
    }
    person = {1, person_id};
    revision = session->revision;
    return F04_OK;
}

std::uint32_t bind_player(F04Session* session, F04Ref person, std::uint64_t) noexcept
{
    if (session->owner != std::this_thread::get_id()) {
        ++wrong_thread;
        return F04_THREAD;
    }
    ++binds;
    if (const auto code = bind_failure.load(); code != F04_OK) {
        return code;
    }
    if (session->player == 0) {
        session->player = person.id;
        ++session->revision;
        ++player_records;
    }
    // Model a commit that finished before the F05 call returns to HOST.
    if (mode == Mode::pause_bind) {
        wait_in_bridge();
    }
    return F04_OK;
}

} // namespace trek::host::detail::bridge

namespace {
void initialization()
{
    SessionOwner owner;
    mode = Mode::bad_sha;
    expect(owner.open(population()).get(), Error::INTERNAL_ERROR);
    require(creates == 0 && destroys == 0 && live == 0, "SHA mismatch reached F04 create");
    closed(owner);

    mode = Mode::fail_create;
    expect(owner.open(population()).get(), Error::INTERNAL_ERROR);
    require(creates == 1 && destroys == 0 && live == 0, "Failure before acquisition leaked");
    closed(owner);

    mode = Mode::fail_probe;
    expect(owner.open(population()).get(), Error::INTERNAL_ERROR);
    require(creates == 2 && destroys == 1 && live == 0, "Partial initialization leaked");
    closed(owner);

    mode = Mode::normal;
    open(owner);
    expect(owner.close().get(), Error::OK);
    require(creates == 3 && destroys == 2 && live == 0, "Wrong lifetime counts");
}

void incompatible()
{
    SessionOwner owner;
    mode = Mode::pause_create;
    auto opening = owner.open(population());
    await_bridge();
    require(owner.snapshot().state == State::OPENING, "Expected OPENING");
    expect(owner.open(population()).get(), Error::BUSY_STATE);
    expect(owner.check_active({}).get(), Error::BUSY_STATE);
    const auto closed_during_open = owner.close();
    require(owner.snapshot().state == State::CLOSING, "Close did not stop opening admission");
    expect(owner.open(population()).get(), Error::BUSY_STATE);
    expect(owner.check_active({}).get(), Error::BUSY_STATE);
    mode = Mode::normal;
    resume.release();
    expect(opening.get(), Error::BUSY_STATE);
    expect(closed_during_open.get(), Error::OK);
    closed(owner);
    require(creates == 1 && destroys == 1 && live == 0, "Canceled opening leaked");

    const auto generation = open(owner);
    mode = Mode::pause_destroy;
    const auto closing = owner.close();
    await_bridge();
    const auto same_close = owner.close();
    const auto snapshot = owner.snapshot();
    require(snapshot.state == State::CLOSING && snapshot.generation == Generation{},
            "Close left an active generation during destruction");
    expect(owner.open(population()).get(), Error::BUSY_STATE);
    expect(owner.check_active(generation).get(), Error::GENERATION_EXPIRED);
    mode = Mode::normal;
    resume.release();
    expect(closing.get(), Error::OK);
    expect(same_close.get(), Error::OK);
    require(creates == 2 && destroys == 2 && live == 0, "Double close destroyed twice");
}

void pending()
{
    SessionOwner owner;
    const auto generation = open(owner);
    mode = Mode::pause_probe;
    auto running = owner.check_active(generation);
    await_bridge();
    std::future<Result> queued[32];
    for (auto& request : queued) {
        request = owner.check_active(generation);
    }
    expect(owner.check_active(generation).get(), Error::CAPACITY_LIMIT);
    auto closing = owner.close();
    for (auto& request : queued) {
        expect(request.get(), Error::GENERATION_EXPIRED);
    }
    require(probes == 2 && destroys == 0, "Close overlapped Core work or executed pending checks");
    mode = Mode::normal;
    resume.release();
    expect(running.get(), Error::GENERATION_EXPIRED);
    expect(closing.get(), Error::OK);
    require(probes == 2 && destroys == 1 && live == 0, "Pending checks reached the bridge");
}

void failed_destroy()
{
    SessionOwner owner;
    const auto generation = open(owner);
    mode = Mode::fail_destroy;
    expect(owner.close().get(), Error::WRONG_THREAD);
    require(owner.snapshot().state == State::FAILED && live == 1, "Failed destroy lost its session");
    expect(owner.check_active(generation).get(), Error::GENERATION_EXPIRED);
    expect(owner.open(population()).get(), Error::BUSY_STATE);
    SessionOwner other;
    expect(other.open(population()).get(), Error::BUSY_STATE);
    require(creates == 1 && destroys == 1, "Failure released the process reservation");

    mode = Mode::normal;
    expect(owner.close().get(), Error::OK);
    closed(owner);
    open(other);
    expect(other.close().get(), Error::OK);
    require(creates == 2 && destroys == 3 && live == 0, "Retry did not destroy the original session");
}

void failed_active_probe()
{
    SessionOwner owner;
    const auto generation = open(owner);
    mode = Mode::fail_probe;
    expect(owner.check_active(generation).get(), Error::INTERNAL_ERROR);
    require(owner.snapshot().state == State::FAILED && live == 1,
            "A failed liveness probe did not suspend the session");
    expect(owner.check_active(generation).get(), Error::GENERATION_EXPIRED);
    expect(owner.close().get(), Error::OK);
    closed(owner);
}

void shutdown_retry()
{
    {
        SessionOwner owner;
        open(owner);
        mode = Mode::fail_destroy_once;
    }
    require(creates == 1 && destroys == 2 && live == 0, "Shutdown did not retry on the owner");
    SessionOwner next;
    open(next);
    expect(next.close().get(), Error::OK);
}

PlayerSelectionResult select_player(SessionOwner& owner, Generation generation)
{
    auto result = PlayerBootstrap::prepare(owner, generation, 4).get();
    require(result.error == Error::OK && result.selection, "Fake bridge selection failed");
    return result;
}

void close_during_bind()
{
    SessionOwner owner;
    const auto generation = open(owner);
    const auto selection = select_player(owner, generation);
    mode = Mode::pause_bind;
    auto running = PlayerBootstrap::bind(owner, generation, *selection.selection, selection.revision);
    await_bridge();
    const auto resolving = owner.current_player(generation);
    require(resolving.error == Error::PRINCIPAL_UNBOUND && !resolving.player,
            "HOST published the player before F05 returned");
    auto queued = PlayerBootstrap::bind(owner, generation, *selection.selection, selection.revision);
    auto pending_selection = PlayerBootstrap::prepare(owner, generation, 5);
    const auto closing = owner.close();
    const auto snapshot = owner.snapshot();
    require(snapshot.state == State::CLOSING && snapshot.generation == Generation{},
            "Close left the generation active");
    const auto denied = owner.current_player(generation);
    require(denied.error == Error::GENERATION_EXPIRED && !denied.player,
            "Close left player access active");
    require(queued.get().error == Error::GENERATION_EXPIRED, "Close kept queued bind");
    const auto canceled = pending_selection.get();
    require(canceled.error == Error::GENERATION_EXPIRED && !canceled.selection && canceled.revision == 0,
            "Close kept queued selection");
    require(player_records == 1 && binds == 1 && destroys == 0, "F05 or destroy overlapped the in-flight bind");
    mode = Mode::normal;
    resume.release();
    const auto stale = running.get();
    require(stale.error == Error::GENERATION_EXPIRED && !stale.domain_code,
            "Late F05 success escaped invalidation");
    expect(closing.get(), Error::OK);
    const auto next = open(owner);
    const auto unbound = owner.current_player(next);
    require(unbound.error == Error::PRINCIPAL_UNBOUND && !unbound.player && destroys == 1 &&
            player_records == 1 && binds == 1, "Close published a late result or reused the binding");
}

void bind_failure_without_mutation()
{
    SessionOwner owner;
    const auto generation = open(owner);
    const auto selection = select_player(owner, generation);
    for (const auto failure : {F04_SCOPE, F04_INTERNAL, F04_QUALIFICATION}) {
        bind_failure = failure;
        const auto result = PlayerBootstrap::bind(owner, generation, *selection.selection,
                                                  selection.revision).get();
        const auto mapped = failure == F04_SCOPE ? Error::SCOPE_INVALID
                          : failure == F04_INTERNAL ? Error::INTERNAL_ERROR : Error::DOMAIN_REJECTED;
        require(result.error == mapped && result.domain_code == failure, "Core failure code was lost");
        const auto unbound = owner.current_player(generation);
        require(unbound.error == Error::PRINCIPAL_UNBOUND && !unbound.player &&
                select_player(owner, generation).revision == selection.revision && player_records == 0,
                "Failed F05 call published a player or wrote Core");
    }
    require(owner.snapshot().state == State::ACTIVE, "F05 failure closed a healthy session");
    bind_failure = F04_OK;
    const auto result = PlayerBootstrap::bind(owner, generation, *selection.selection, selection.revision).get();
    require(result.error == Error::OK && player_records == 1, "Explicit retry failed");
    mode = Mode::fail_probe;
    expect(owner.check_active(generation).get(), Error::INTERNAL_ERROR);
    const auto expired = owner.current_player(generation);
    require(expired.error == Error::GENERATION_EXPIRED && !expired.player && owner.snapshot().state == State::FAILED,
            "H02 failure kept the H03 binding alive");
}

void incompatible_core_binding()
{
    SessionOwner owner;
    const auto generation = open(owner);
    const auto selection = select_player(owner, generation);
    bind_failure = F05_IDEMPOTENCY_CONFLICT;
    const auto result = PlayerBootstrap::bind(owner, generation, *selection.selection, selection.revision).get();
    require(result.error == Error::IDEMPOTENCY_CONFLICT && result.domain_code == F05_IDEMPOTENCY_CONFLICT,
            "Preexisting Core conflict was lost");
    const auto denied = owner.current_player(generation);
    require(denied.error == Error::ACCESS_DENIED && !denied.player, "Inconsistent binding allowed access");
    const auto retry = PlayerBootstrap::bind(owner, generation, *selection.selection, selection.revision).get();
    require(retry.error == Error::ACCESS_DENIED && !retry.domain_code && binds == 1 && player_records == 0,
            "An invalid binding allowed another mutation");
    expect(owner.check_active(generation).get(), Error::OK);
}

constexpr Case cases[]{
    {"initialization", initialization},
    {"hc06_incompatible_states", incompatible},
    {"pending", pending},
    {"failed_destroy", failed_destroy},
    {"failed_active_probe", failed_active_probe},
    {"shutdown_retry", shutdown_retry},
    {"hi09_close_during_bind", close_during_bind},
    {"hi11_bind_failure", bind_failure_without_mutation},
    {"hi19_incompatible_core_binding", incompatible_core_binding},
};
} // namespace

int main(int argc, char** argv)
{
    try {
        if (argc == 2) {
            for (const auto& scenario : cases) {
                if (scenario.name == argv[1]) {
                    scenario.run();
                    require(live == 0 && wrong_thread == 0, "Bridge leaked or was used from the wrong thread");
                    std::cout << "PASS " << scenario.name << '\n';
                    return 0;
                }
            }
        }
        throw std::runtime_error("Unknown HOST fault test");
    } catch (const std::exception& error) {
        std::cerr << "FAIL " << error.what() << '\n';
        return 1;
    }
}
