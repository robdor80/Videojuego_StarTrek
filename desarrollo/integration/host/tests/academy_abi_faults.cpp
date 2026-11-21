#include "academy_interface.h"
#include "f10/academy_campaign.h"
#include "f10/academy_player_binding.h"
#include "test_support.h"

#include <semaphore>

namespace {
using namespace trek::host;
using namespace trek::host::detail;
using test::require;
constexpr auto payload = R"({"display_name":"Aren"})";
std::binary_semaphore entered{0}, resume{0};
void pause_bind() { entered.release(); resume.acquire(); }
void fail_bind() { throw std::runtime_error("Injected bind interruption"); }

AcademyCandidateView real_world(SessionOwner& owner)
{
    auto intent = AcademyCandidateFactory::begin(owner);
    auto creation = AcademyCandidateFactory::create(owner, intent, payload).get();
    require(creation.error == Error::OK, "private B02 retry");
    auto inspected = AcademyCandidateFactory::inspect(owner, creation.receipt).get();
    require(inspected.error == Error::OK && inspected.candidate, "real Core inspect");
    auto view = *inspected.candidate;
    require(view.person_count == 1 && view.creation_fact_count == 1 && view.population_count == 0,
            "product facade duplicated PERSON/fact or granted a naval population");
    return view;
}

void retry_and_gates()
{
    SessionOwner owner;
    set_academy_fault(AcademyFault::BEFORE_PUBLICATION);
    auto failed = AcademyInterface::create_bound(owner, 1, payload).get();
    require(failed.error == Error::INTERNAL_ERROR && owner.snapshot().state == State::CLOSED,
            "failed stage published campaign");
    set_academy_fault(AcademyFault::NONE);
    set_academy_bind_test_hook(fail_bind);
    auto interrupted = AcademyInterface::create_bound(owner, 1, payload).get();
    require(interrupted.error == Error::INTERNAL_ERROR && !interrupted.candidate,
            "failed bind reported BOUND");
    const auto generation = owner.snapshot().generation;
    require(owner.current_player(generation).error == Error::PRINCIPAL_UNBOUND, "failed bind exposed player");
    require(owner.save(generation, "alpha").get().error != Error::OK, "failed bind saved");
    require(AcademyInterface::query(owner, generation).get().error == Error::PRINCIPAL_UNBOUND,
            "failed bind exposed candidate ficha");
    const auto before = real_world(owner);
    set_academy_bind_test_hook(nullptr);
    auto result = AcademyInterface::create_bound(owner, 1, payload).get();
    require(result.error == Error::OK && result.candidate && result.candidate->person == before.person,
            "retry did not reuse the same PERSON");
    require(owner.current_player(result.generation).player->person_id == before.person, "H03 person differs");
    require(owner.query_view(result.generation).get().error == Error::ACCESS_DENIED &&
            owner.submit_order(result.generation, {}).get().error == Error::ACCESS_DENIED &&
            owner.query_order(result.generation, 1).get().error == Error::ACCESS_DENIED &&
            owner.cancel_order(result.generation, 1, 1).get().error == Error::ACCESS_DENIED &&
            owner.institutional_command(result.generation).get().error == Error::ACCESS_DENIED,
            "product binding admitted one of five F05 operations");
    const auto after = real_world(owner);
    require(after.revision == before.revision && after.person == before.person &&
            after.background == before.background, "binding or F05 mutated Core");
}

void close_during_bind()
{
    SessionOwner owner;
    set_academy_bind_test_hook(pause_bind);
    auto creation = AcademyInterface::create_bound(owner, 1, payload);
    require(entered.try_acquire_for(std::chrono::seconds(10)), "bind hook timeout");
    auto closed = owner.close();
    require(owner.snapshot().generation == Generation{}, "close did not revoke immediately");
    resume.release();
    auto result = creation.get();
    require(result.error == Error::GENERATION_EXPIRED && !result.candidate, "late BOUND after close");
    require(closed.get().error == Error::OK, "close failed");
    set_academy_bind_test_hook(nullptr);
    require(AcademyInterface::create_bound(owner, 1, payload).get().error == Error::GENERATION_EXPIRED,
            "retired creation key reactivated");
    auto fresh = AcademyInterface::create_bound(owner, 2, payload).get();
    require(fresh.error == Error::OK, "new explicit creation failed");
    real_world(owner);
}
} // namespace

int main()
{
    retry_and_gates();
    close_during_bind();
}
