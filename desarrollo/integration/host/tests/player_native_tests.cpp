#include "player_bootstrap.h"
#include "test_support.h"

#include "f05_initiative.h"

#include <barrier>
#include <iostream>
#include <thread>
#include <type_traits>

namespace {
using namespace test;

// Individuals materialized by the native F04 population fixture. These are
// test inputs from trusted creation, independent of the future Academy flow.
constexpr std::uint64_t player_id = 4;
constexpr std::uint64_t other_id = 5;
constexpr std::uint64_t resident_id = 11;

struct BindRevisions {
    std::uint64_t before;
    std::uint64_t after;
};

BindRevisions one_core_bind(std::uint64_t id);

template<class... Args>
concept CanResolvePlayer = requires(const SessionOwner& owner, Args... args) {
    owner.current_player(args...);
};

template<class Owner>
concept HasPublicBind = requires(Owner& owner, Generation generation, F04Ref actor) {
    owner.bind_player(generation, actor);
};

static_assert(CanResolvePlayer<Generation>);
static_assert(!CanResolvePlayer<Generation, F04Ref>);
static_assert(!CanResolvePlayer<Generation, std::uint64_t, bool, unsigned>);
static_assert(!HasPublicBind<SessionOwner>);
static_assert(!std::is_default_constructible_v<PlayerSelection>);
static_assert(!std::is_constructible_v<PlayerSelection, F04Ref>);

PlayerSelectionResult prepare(SessionOwner& owner, Generation generation, std::uint64_t id = player_id)
{
    auto result = PlayerBootstrap::prepare(owner, generation, id).get();
    require(result.error == Error::OK && result.selection && !result.domain_code,
            "Trusted creation did not resolve a PERSON");
    return result;
}

BindPlayerResult bind(SessionOwner& owner, Generation generation, const PlayerSelectionResult& selected)
{
    return PlayerBootstrap::bind(owner, generation, *selected.selection, selected.revision).get();
}

void expect_bind(BindPlayerResult result, Error error,
                 std::optional<std::uint32_t> domain_code = std::nullopt)
{
    require(result.error == error && result.domain_code == domain_code,
            "Wrong HOST or raw Core bind code");
}

void expect_player(const SessionOwner& owner, Generation generation, Error error,
                   std::uint64_t id = 0)
{
    const auto result = owner.current_player(generation);
    require(result.error == error, "Wrong player lookup status");
    if (error == Error::OK) {
        require(result.player && result.player->generation == generation && result.player->person_id == id,
                "Wrong bound player or generation");
    } else {
        require(!result.player, "Denial exposed player data");
    }
}

void expect_revision(SessionOwner& owner, Generation generation, std::uint64_t before)
{
    const auto after = prepare(owner, generation).revision;
    std::cout << "Core revision " << before << " -> " << after << '\n';
    require(after == before, "Unexpected Core mutation");
}

void first_bind()
{
    SessionOwner owner;
    const auto generation = open(owner);
    const auto selected = prepare(owner, generation);
    expect_bind(bind(owner, generation, selected), Error::OK);
    expect_player(owner, generation, Error::OK, player_id);
    const auto snapshot = owner.snapshot();
    require(snapshot.state == State::ACTIVE && snapshot.generation == generation,
            "Bind changed the H02 session");
    expect(owner.close().get(), Error::OK);
}

void unbound()
{
    SessionOwner owner;
    const auto generation = open(owner);
    const auto before = prepare(owner, generation).revision;
    expect_player(owner, generation, Error::PRINCIPAL_UNBOUND);
    expect_revision(owner, generation, before);
    expect(owner.check_active(generation).get(), Error::OK);
}

void client_boundary()
{
    SessionOwner owner;
    const auto generation = open(owner);
    // Even with the current generation, the consumer can only ask for the
    // owner's player. The compile-time checks cover unsupported actor inputs.
    expect_player(owner, generation, Error::PRINCIPAL_UNBOUND);
    const auto selected = prepare(owner, generation);
    expect_bind(bind(owner, generation, selected), Error::OK);
    const auto before = prepare(owner, generation).revision;
    expect_player(owner, generation, Error::OK, player_id);
    expect_revision(owner, generation, before);
}

void replay()
{
    SessionOwner owner;
    const auto generation = open(owner);
    const auto selected = prepare(owner, generation);
    expect_bind(bind(owner, generation, selected), Error::OK);
    const auto committed = prepare(owner, generation).revision;
    require(committed > selected.revision, "First bind did not commit");
    expect_bind(bind(owner, generation, selected), Error::OK);
    expect_player(owner, generation, Error::OK, player_id);
    expect_revision(owner, generation, committed);
}

void conflict()
{
    SessionOwner owner;
    const auto generation = open(owner);
    expect_bind(bind(owner, generation, prepare(owner, generation)), Error::OK);
    const auto other = prepare(owner, generation, other_id);
    expect_bind(bind(owner, generation, other), Error::IDEMPOTENCY_CONFLICT, F05_IDEMPOTENCY_CONFLICT);
    expect_revision(owner, generation, other.revision);
    expect_player(owner, generation, Error::OK, player_id);
}

void foreign_campaign()
{
    SessionOwner owner;
    const auto first = open(owner);
    const auto foreign = prepare(owner, first);
    expect(owner.close().get(), Error::OK);

    const auto second = open(owner);
    const auto local = prepare(owner, second);
    require(local.revision == foreign.revision, "Fixture revisions do not collide");
    expect_bind(bind(owner, second, foreign), Error::SCOPE_INVALID);
    expect_player(owner, second, Error::PRINCIPAL_UNBOUND);
    expect_revision(owner, second, local.revision);
    expect_bind(bind(owner, second, local), Error::OK);
}

void expired()
{
    SessionOwner owner;
    const auto first = open(owner);
    const auto selection = prepare(owner, first);
    expect_bind(bind(owner, first, selection), Error::OK);
    const auto close = owner.close();
    expect_player(owner, first, Error::GENERATION_EXPIRED);
    expect_bind(bind(owner, first, selection), Error::GENERATION_EXPIRED);
    expect(close.get(), Error::OK);

    const auto second = open(owner);
    const auto before = prepare(owner, second).revision;
    expect_player(owner, first, Error::GENERATION_EXPIRED);
    expect_bind(bind(owner, first, selection), Error::GENERATION_EXPIRED);
    const auto stale = PlayerBootstrap::prepare(owner, first, player_id).get();
    require(stale.error == Error::GENERATION_EXPIRED && !stale.selection && stale.revision == 0,
            "Expired prepare leaked a selection");
    expect_revision(owner, second, before);
}

void concurrent()
{
    SessionOwner owner;
    const auto generation = open(owner);
    const auto first = prepare(owner, generation);
    const auto second = prepare(owner, generation, other_id);
    std::barrier start(2);
    BindPlayerResult a{};
    std::jthread producer([&] {
        start.arrive_and_wait();
        a = bind(owner, generation, first);
    });
    start.arrive_and_wait();
    const auto b = bind(owner, generation, second);
    producer.join();
    const bool first_won = a.error == Error::OK;
    expect_bind(first_won ? a : b, Error::OK);
    expect_bind(first_won ? b : a, Error::IDEMPOTENCY_CONFLICT, F05_IDEMPOTENCY_CONFLICT);
    expect_player(owner, generation, Error::OK, first_won ? player_id : other_id);
    const auto committed = prepare(owner, generation).revision;
    require(committed > first.revision, "Concurrent bind did not commit");
    expect_bind(bind(owner, generation, first_won ? first : second), Error::OK);
    expect_revision(owner, generation, committed);
    expect(owner.close().get(), Error::OK);
    require(committed == one_core_bind(first_won ? player_id : other_id).after,
            "Concurrent requests committed more than one F05 bind");
}

void stale_revision()
{
    SessionOwner owner;
    const auto generation = open(owner);
    const auto selected = prepare(owner, generation);
    require(selected.revision > 0, "Fixture did not initialize the Core revision");
    expect_bind(PlayerBootstrap::bind(owner, generation, *selected.selection, selected.revision - 1).get(),
                Error::REVISION_STALE, F04_STALE);
    expect_player(owner, generation, Error::PRINCIPAL_UNBOUND);
    expect_revision(owner, generation, selected.revision);
    expect_bind(bind(owner, generation, prepare(owner, generation)), Error::OK);
}

void invalid_person()
{
    SessionOwner owner;
    const auto generation = open(owner);
    const auto before = prepare(owner, generation).revision;
    const auto ship = PlayerBootstrap::prepare(owner, generation, 1).get();
    require(ship.error == Error::SCOPE_INVALID && ship.domain_code == F04_SCOPE &&
            !ship.selection && ship.revision == 0, "Ship was accepted as PERSON");
    const auto resident = prepare(owner, generation, resident_id);
    expect_bind(bind(owner, generation, resident), Error::ACCESS_DENIED, F04_DENIED);
    expect_player(owner, generation, Error::PRINCIPAL_UNBOUND);
    expect_revision(owner, generation, before);
    expect_bind(bind(owner, generation, prepare(owner, generation)), Error::OK);
}

BindRevisions one_core_bind(std::uint64_t id)
{
    // Independently measure the revision change of one real F05 bind.
    F04Session* session = nullptr;
    const auto config = population();
    const F04PopulationConfig native{config.ship_identity, config.seed, config.crew,
                                     config.residents, config.passengers, config.maximum};
    require(f04_create_population(1, config.class_id.c_str(), &native, &session) == F04_OK,
            "Could not open the Core revision oracle");
    std::unique_ptr<F04Session, decltype(&f04_destroy)> core(session, f04_destroy);
    F04Handles handles{};
    F04Stats before{}, after{};
    require(f04_handles(core.get(), &handles) == F04_OK && f04_stats(core.get(), &before) == F04_OK,
            "Core revision oracle setup failed");
    require(f05_bind_player(core.get(), {handles.ship.scope, id}, before.revision) == F04_OK &&
            f04_stats(core.get(), &after) == F04_OK, "Core revision oracle bind failed");
    require(after.entities == before.entities + 1 && after.revision > before.revision,
            "A single F05 bind did not create exactly one record");
    return {before.revision, after.revision};
}

void updated_revision()
{
    const auto [before, after] = one_core_bind(player_id);
    SessionOwner owner;
    const auto generation = open(owner);
    const auto selected = prepare(owner, generation);
    expect_bind(bind(owner, generation, selected), Error::OK);
    require(selected.revision == before, "Unexpected initial revision");
    expect_revision(owner, generation, after);
}

void reopen_campaign()
{
    SessionOwner owner;
    const auto first = open(owner);
    expect_bind(bind(owner, first, prepare(owner, first)), Error::OK);
    expect(owner.close().get(), Error::OK);

    auto config = population();
    ++config.ship_identity;
    const auto second = owner.open(config).get();
    expect(second, Error::OK);
    require(second.generation != first, "A new campaign reused the generation");
    expect_player(owner, second.generation, Error::PRINCIPAL_UNBOUND);
    expect_bind(bind(owner, second.generation, prepare(owner, second.generation)), Error::OK);
    expect_player(owner, second.generation, Error::OK, player_id);
    expect_player(owner, first, Error::GENERATION_EXPIRED);
}

void validation_failure()
{
    SessionOwner owner;
    const auto generation = open(owner);
    const auto selected = prepare(owner, generation);
    expect_bind(bind(owner, generation, selected), Error::OK);
    const auto committed = prepare(owner, generation).revision;
    const auto bad = PlayerBootstrap::prepare(owner, generation, UINT64_MAX).get();
    require(bad.error == Error::SCOPE_INVALID && bad.domain_code == F04_SCOPE &&
            !bad.selection && bad.revision == 0, "Validation leaked an invalid selection");
    expect_player(owner, generation, Error::OK, player_id);
    expect_revision(owner, generation, committed);
    expect(owner.check_active(generation).get(), Error::OK);
}

constexpr Case cases[]{
    {"hi01_first_bind", first_bind},
    {"hi02_unbound", unbound},
    {"hi03_client_boundary", client_boundary},
    {"hi04_replay", replay},
    {"hi05_conflict", conflict},
    {"hi06_foreign_campaign", foreign_campaign},
    {"hi07_expired", expired},
    {"hi08_concurrent", concurrent},
    {"hi10_stale", stale_revision},
    {"hi11_invalid_person", invalid_person},
    {"hi12_revision", updated_revision},
    {"hi13_reopen", reopen_campaign},
    {"hi19_validation", validation_failure},
};
} // namespace

void test::run_player_case(std::string_view name)
{
    for (const auto& scenario : cases) {
        if (scenario.name == name) {
            scenario.run();
            return;
        }
    }
    throw std::runtime_error("Unknown native HOST test");
}
