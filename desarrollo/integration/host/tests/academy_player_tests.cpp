#include "f10/academy_player_binding.h"
#include "player_bootstrap.h"
#include "test_support.h"

#include <chrono>
#include <iostream>
#include <semaphore>
#include <type_traits>

namespace {
using namespace test;
using namespace trek::host::detail;
using namespace std::chrono_literals;

constexpr std::string_view name = R"({"display_name":"Aren"})";
constexpr std::string_view other_name = R"({"display_name":"T'Var"})";

static_assert(!std::is_invocable_v<decltype(&AcademyPlayerBinding::bind), SessionOwner&, Generation, std::uint64_t>);

AcademyIntent begin(SessionOwner& owner)
{
    auto intent = AcademyCandidateFactory::begin(owner);
    require(bool(intent), "B02 did not issue an Academy intent");
    return intent;
}

AcademyCreationResult create(SessionOwner& owner, const AcademyIntent& intent)
{
    auto result = AcademyCandidateFactory::create(owner, intent, name).get();
    require(result.error == Error::OK && result.generation != Generation{} && result.receipt,
            "B02 did not publish a candidate");
    return result;
}

AcademyCandidateView inspect(SessionOwner& owner, const AcademyCreationResult& created)
{
    auto result = AcademyCandidateFactory::inspect(owner, created.receipt).get();
    require(result.error == Error::OK && result.candidate, "B02 receipt did not match the live Core");
    return std::move(*result.candidate);
}

std::future<Result> bind(SessionOwner& owner, const AcademyCreationResult& created)
{
    return AcademyPlayerBinding::bind(owner, created.generation, created.receipt);
}

void expect_player(SessionOwner& owner, Generation generation, std::uint64_t person)
{
    const auto result = owner.current_player(generation);
    require(result.error == Error::OK && result.player && result.player->generation == generation &&
                result.player->person_id == person,
            "H03 did not project the B02 Core PERSON in its generation");
}

void expect_no_player(SessionOwner& owner, Generation generation, Error error)
{
    const auto result = owner.current_player(generation);
    require(result.error == error && !result.player, "H03 exposed a player without a live binding");
}

void expect_same_world(const AcademyCandidateView& before, const AcademyCandidateView& after)
{
    require(before.person != 0 && before.creation_fact != 0 && before.person_count == 1 &&
                before.creation_fact_count == 1 && before.population_count == 0,
            "B02 did not start with a single candidate and no population places");
    require(after.campaign_id == before.campaign_id && after.person == before.person &&
                after.creation_fact == before.creation_fact && after.revision == before.revision &&
                after.tick == before.tick && after.person_count == 1 && after.creation_fact_count == 1 &&
                after.population_count == 0 && after.display_name == before.display_name &&
                after.source_digest == before.source_digest && after.background == before.background,
            "H03 or the naval gateway changed the Academy WorldState");
}

void expect_denied(const OperationResult& result, std::uint64_t correlation)
{
    require(result.error == Error::ACCESS_DENIED && result.generation == Generation{} &&
                result.correlation_id == correlation && !result.campaign && !result.order && !result.receipt,
            "Naval gateway did not deny the Academy operation at the HOST boundary");
}

void binding()
{
    SessionOwner owner;
    const auto created = create(owner, begin(owner));
    const auto before = inspect(owner, created);
    expect_no_player(owner, created.generation, Error::PRINCIPAL_UNBOUND);
    const auto bound = bind(owner, created).get();
    expect(bound, Error::OK);
    require(bound.generation == created.generation && owner.campaign_id(bound.generation) == before.campaign_id,
            "H03 changed the B02 activation");
    expect_player(owner, created.generation, before.person);
    expect_same_world(before, inspect(owner, created));
}

void naval_gateway()
{
    SessionOwner owner;
    const auto created = create(owner, begin(owner));
    const auto before = inspect(owner, created);
    expect(bind(owner, created).get(), Error::OK);
    const auto generation = created.generation;
    expect_player(owner, generation, before.person);
    OrderIntent order;
    order.recipient = before.person;
    order.expected_revision = before.revision;
    order.key = 1;
    expect_denied(owner.query_view(generation, 11).get(), 11);
    expect_denied(owner.submit_order(generation, order, 12).get(), 12);
    expect_denied(owner.query_order(generation, 1, 13).get(), 13);
    expect_denied(owner.cancel_order(generation, 1, before.revision, 14).get(), 14);
    expect_denied(owner.institutional_command(generation, 15).get(), 15);
    expect_player(owner, generation, before.person);
    expect_same_world(before, inspect(owner, created));
}

void replay()
{
    SessionOwner owner;
    const auto intent = begin(owner);
    const auto created = create(owner, intent);
    const auto before = inspect(owner, created);
    expect(bind(owner, created).get(), Error::OK);
    const auto retried = create(owner, intent);
    require(retried.receipt == created.receipt, "B02 replaced the receipt after H03 binding");
    const auto rebound = bind(owner, retried).get();
    expect(rebound, Error::OK);
    require(rebound.generation == created.generation, "Replay changed the generation");
    expect_player(owner, created.generation, before.person);
    expect_same_world(before, inspect(owner, created));
}

void foreign_scope()
{
    SessionOwner foreign;
    const auto foreign_created = create(foreign, begin(foreign));
    const auto foreign_world = inspect(foreign, foreign_created);
    expect(foreign.close().get(), Error::OK);

    SessionOwner owner;
    const auto old = create(owner, begin(owner));
    expect(owner.close().get(), Error::OK);
    const auto created = create(owner, begin(owner));
    const auto before = inspect(owner, created);
    const auto generation = created.generation;
    require(foreign_world.campaign_id != before.campaign_id && foreign_world.person == before.person,
            "Fixture must exercise equal Core ordinals in different campaigns");

    expect(AcademyPlayerBinding::bind(owner, generation, foreign_created.receipt).get(), Error::SCOPE_INVALID);
    expect(AcademyPlayerBinding::bind(owner, generation, {}).get(), Error::SCOPE_INVALID);
    expect_no_player(owner, generation, Error::PRINCIPAL_UNBOUND);
    expect(bind(owner, created).get(), Error::OK);
    expect(AcademyPlayerBinding::bind(owner, generation, foreign_created.receipt).get(), Error::SCOPE_INVALID);
    expect(AcademyPlayerBinding::bind(owner, generation, old.receipt).get(), Error::SCOPE_INVALID);
    expect(bind(owner, old).get(), Error::GENERATION_EXPIRED);
    for (auto id : {before.person, before.creation_fact}) {
        const auto selection = PlayerBootstrap::prepare(owner, generation, id).get();
        require(selection.error == Error::ACCESS_DENIED && !selection.selection,
                "Naval bootstrap accepted an Academy PERSON or fact as a selector");
    }
    expect_player(owner, generation, before.person);
    expect_same_world(before, inspect(owner, created));
    expect(owner.close().get(), Error::OK);

    const auto naval_generation = open(foreign);
    expect(AcademyPlayerBinding::bind(foreign, naval_generation, created.receipt).get(), Error::SCOPE_INVALID);
    expect_no_player(foreign, naval_generation, Error::PRINCIPAL_UNBOUND);
}

void projection()
{
    SessionOwner owner;
    const auto created = create(owner, begin(owner));
    const auto before = inspect(owner, created);
    expect(bind(owner, created).get(), Error::OK);
    expect(owner.check_active(created.generation).get(), Error::OK);
    expect_player(owner, created.generation, before.person);
    expect_denied(owner.institutional_command(created.generation, 1).get(), 1);
    expect(owner.save(created.generation, "test").get(), Error::SAVE_INCOMPATIBLE);
    expect(owner.restore(created.generation, {before.campaign_id, "test", 0}).get(), Error::SAVE_INCOMPATIBLE);
    expect_same_world(before, inspect(owner, created));

    expect(owner.close().get(), Error::OK);
    expect_no_player(owner, created.generation, Error::GENERATION_EXPIRED);
    expect(bind(owner, created).get(), Error::GENERATION_EXPIRED);
    const auto next = create(owner, begin(owner));
    require(next.generation != created.generation, "A new campaign reused the closed generation");
    expect_no_player(owner, next.generation, Error::PRINCIPAL_UNBOUND);
}

void concurrent_binding()
{
    SessionOwner owner, other_owner;
    const auto intent = begin(owner);
    const auto other_intent = begin(other_owner);
    const auto created = create(owner, intent);
    const auto before = inspect(owner, created);
    std::future<Result> first, second;
    std::future<AcademyCreationResult> repeated, substitute, profile;
    std::promise<void> ready;
    const auto start = ready.get_future().share();
    auto submit = [&](auto operation) {
        return std::async(std::launch::async, [start, operation] {
            start.get();
            return operation();
        });
    };
    first = submit([&] { return bind(owner, created).get(); });
    second = submit([&] { return bind(owner, created).get(); });
    repeated = submit([&] { return create(owner, intent); });
    substitute = submit([&] { return AcademyCandidateFactory::create(owner, intent, other_name).get(); });
    profile = submit([&] { return AcademyCandidateFactory::create(owner, other_intent, name).get(); });
    ready.set_value();
    for (auto* response : {&first, &second}) {
        const auto bound = response->get();
        expect(bound, Error::OK);
        require(bound.generation == created.generation, "Concurrent binding changed the generation");
    }
    require(repeated.get().receipt == created.receipt, "Concurrent creation produced another receipt");
    const auto conflict = substitute.get();
    require(conflict.error == Error::IDEMPOTENCY_CONFLICT && !conflict.receipt,
            "Concurrent creation replaced the candidate");
    const auto denied = profile.get();
    require(denied.error == Error::SCOPE_INVALID && !denied.receipt, "A foreign profile took over the campaign");
    expect_player(owner, created.generation, before.person);
    expect_same_world(before, inspect(owner, created));
}

#ifdef TREK_HOST_ACADEMY_TESTING
std::binary_semaphore bind_validated(0), resume_bind(0);

struct PauseBind {
    PauseBind()
    {
        set_academy_bind_test_hook([] {
            bind_validated.release();
            resume_bind.acquire();
        });
    }

    ~PauseBind()
    {
        set_academy_bind_test_hook(nullptr);
        resume_bind.release();
    }
};

void close_during_binding()
{
    SessionOwner owner;
    const auto created = create(owner, begin(owner));
    std::future<Result> in_flight;
    std::shared_future<Result> closed_result;
    {
        PauseBind pause;
        in_flight = bind(owner, created);
        require(bind_validated.try_acquire_for(5s), "Owner did not reach Academy bind publication");
        expect_no_player(owner, created.generation, Error::PRINCIPAL_UNBOUND);
        auto queued = bind(owner, created);
        closed_result = owner.close();
        expect_no_player(owner, created.generation, Error::GENERATION_EXPIRED);
        expect(bind(owner, created).get(), Error::GENERATION_EXPIRED);
        require(queued.wait_for(0s) == std::future_status::ready, "Close did not revoke the queued binding immediately");
        expect(queued.get(), Error::GENERATION_EXPIRED);
        require(AcademyCandidateFactory::inspect(owner, created.receipt).get().error == Error::SCOPE_INVALID,
                "Close left the B02 receipt active");
    }
    expect(in_flight.get(), Error::GENERATION_EXPIRED);
    expect(closed_result.get(), Error::OK);
    closed(owner);
    const auto next = create(owner, begin(owner));
    expect_no_player(owner, next.generation, Error::PRINCIPAL_UNBOUND);
    expect(bind(owner, created).get(), Error::GENERATION_EXPIRED);
    expect(bind(owner, next).get(), Error::OK);
    expect_player(owner, next.generation, inspect(owner, next).person);
}

void retry_after_failure()
{
    SessionOwner owner;
    const auto created = create(owner, begin(owner));
    const auto before = inspect(owner, created);
    set_academy_bind_test_hook([] { throw std::runtime_error("Injected Academy bind failure"); });
    const auto failed = bind(owner, created).get();
    set_academy_bind_test_hook(nullptr);
    expect(failed, Error::INTERNAL_ERROR);
    expect_no_player(owner, created.generation, Error::PRINCIPAL_UNBOUND);
    expect_same_world(before, inspect(owner, created));
    expect(bind(owner, created).get(), Error::OK);
    expect_player(owner, created.generation, before.person);
    expect_same_world(before, inspect(owner, created));
}
#endif
} // namespace

int main(int argc, char** argv)
try {
    if (argc != 2) return 2;
    for (const auto& test_case : {
        Case{"b03t_01", binding}, Case{"b03t_02", naval_gateway}, Case{"b03t_03a", replay},
        Case{"b03t_03b", foreign_scope}, Case{"b03t_03d", projection}, Case{"b03t_03e", concurrent_binding},
#ifdef TREK_HOST_ACADEMY_TESTING
        Case{"b03t_03c", close_during_binding}, Case{"b03t_bind_retry", retry_after_failure},
#endif
    }) {
        if (argv[1] == test_case.name) {
            test_case.run();
            return 0;
        }
    }
    return 2;
} catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
}
