#include "f10/academy_candidate_factory.h"
#include "player_bootstrap.h"
#include "test_support.h"

#include <algorithm>
#include <iostream>
#include <type_traits>

#if defined(TREK_HOST_ACADEMY_TESTING)
#include "biography_profile_source.h"
#include "f10/academy_campaign.h"
#endif

namespace {
using namespace test;
using namespace trek::host::detail;
using namespace std::string_view_literals;

constexpr auto name = R"({"display_name":"Sarek Ríos"})"sv;
constexpr auto another_name = R"({"display_name":"Aren T’Var"})"sv;

struct Candidate {
    SessionOwner owner;
    AcademyIntent intent = AcademyCandidateFactory::begin(owner);

    AcademyCreationResult submit(std::string_view payload = name)
    {
        require(bool(intent), "HOST did not issue an attempt");
        return AcademyCandidateFactory::create(owner, intent, payload).get();
    }

    AcademyCandidateView inspect(const AcademyCreationResult& result)
    {
        require(result.error == Error::OK && result.receipt && result.generation != Generation{},
                ("Academy creation failed: " + std::to_string(static_cast<int>(result.error))).c_str());
        const auto inspected = AcademyCandidateFactory::inspect(owner, result.receipt).get();
        require(inspected.error == Error::OK && inspected.candidate.has_value(), "Core receipt could not be verified");
        return *inspected.candidate;
    }

    void rejected(std::string_view payload, Error error = Error::INVALID_ARGUMENT)
    {
        const auto result = submit(payload);
        require(result.error == error && !result.receipt && result.generation == Generation{}, "Expected rejection");
        closed(owner);
    }
};

void has(const AcademyCandidateView& view, std::string_view fact)
{
    require(std::ranges::find(view.background, fact) != view.background.end(),
            ("Core fact absent: " + std::string(fact)).c_str());
}

void same_world(const AcademyCandidateView& a, const AcademyCandidateView& b)
{
    require(a.campaign_id == b.campaign_id && a.person == b.person && a.creation_fact == b.creation_fact &&
            a.source_digest == b.source_digest && a.revision == b.revision && a.tick == b.tick &&
            a.display_name == b.display_name && a.background == b.background &&
            a.person_count == b.person_count && a.creation_fact_count == b.creation_fact_count &&
            a.population_count == b.population_count, "Core state changed");
}

void canonical()
{
    Candidate fixture;
    const auto result = fixture.submit();
    const auto view = fixture.inspect(result);
    require(view.display_name == "Sarek Ríos", "Name was lost");
    require(view.campaign_id == fixture.owner.campaign_id(result.generation) &&
            fixture.owner.campaign_provenance(result.generation) == Provenance::CREATED_LOCALLY,
            "Core identity did not match the HOST campaign");
    for (auto fact : {"species/human_vulcan_hybrid", "background/sex/male",
         "background/academy_entry_age_earth_years/45", "background/application_year/2383",
         "background/approximate_birth_year/2338", "background/approximate_apparent_human_age/30",
         "mother/species/vulcan", "father/species/human", "paternal/ancestry/khan_noonien_singh",
         "background/strength/exceptional_real", "background/reflexes/exceptional_real",
         "background/resilience/exceptional_real", "background/martial_mastery/kung_fu",
         "background/martial_mastery/karate", "background/martial_mastery/aikido",
         "background/martial_mastery/suus_mahna", "background/vocation/science",
         "background/interest/astronomy", "background/interest/astrophysics", "background/interest/music",
         "background/emotional_mastery/advanced_learned_not_suppressed",
         "background/prior_career/civilian", "background/prior_starfleet_service/absent"}) has(view, fact);
}

void new_campaign()
{
    Candidate fixture;
    const auto first = fixture.submit();
    const auto a = fixture.inspect(first);
    expect(fixture.owner.close().get(), Error::OK);
    const auto expired_intent = fixture.intent;
    fixture.intent = AcademyCandidateFactory::begin(fixture.owner);
    require(expired_intent != fixture.intent, "New campaign reused an intent");
    const auto second = fixture.submit(another_name);
    const auto b = fixture.inspect(second);
    require(a.campaign_id != b.campaign_id && first.generation != second.generation && first.receipt != second.receipt,
            "Campaign-qualified identity was reused");
    require(b.display_name == "Aren T’Var" && a.background == b.background && a.source_digest == b.source_digest,
            "Canonical archetype changed between campaigns");
    require(a.person_count == 1 && b.person_count == 1, "Exactly one Core PERSON in each separate world");
}

void replay()
{
    Candidate fixture;
    auto first = AcademyCandidateFactory::create(fixture.owner, fixture.intent, name);
    auto queued = AcademyCandidateFactory::create(fixture.owner, fixture.intent, name);
    const auto one = first.get();
    const auto two = queued.get();
    const auto initial = fixture.inspect(one);
    auto escaped = fixture.submit(R"( { "display_name": "Sarek R\u00edos" } )");
    require(one.receipt == two.receipt && two.receipt == escaped.receipt &&
            AcademyCandidateFactory::begin(fixture.owner) == fixture.intent && one.generation == two.generation,
            "Same intent and decoded name did not replay its receipt");
    same_world(initial, fixture.inspect(two));
    same_world(initial, fixture.inspect(escaped));
    require(initial.person_count == 1 && initial.creation_fact_count == 1, "Replay duplicated Core records");
}

void conflict()
{
    Candidate fixture;
    const auto first = fixture.submit();
    const auto before = fixture.inspect(first);
    const auto result = fixture.submit(another_name);
    require(result.error == Error::IDEMPOTENCY_CONFLICT && !result.receipt && result.generation == Generation{},
            "Changed name reused the committed attempt");
    same_world(before, fixture.inspect(first));
}

void immutable_fields()
{
    Candidate fixture;
    for (auto extra : {R"("species_id":"human")", R"("species_id":"vulcan")", R"("age":20)",
                       R"("sex":"female")", R"("parentage":{"father":"vulcan"})",
                       R"("khan_lineage":false)", R"("biography":"alternative")"}) {
        fixture.rejected(std::string(R"({"display_name":"Aren",)") + extra + "}");
    }
}

void authority_fields()
{
    Candidate fixture;
    for (auto field : {"person_id", "campaign_id", "generation", "source_digest", "issuer", "approval", "scope",
                       "candidate_commit_receipt", "semantic_receipt", "rank", "profile_id", "cadet_slot"}) {
        fixture.rejected(std::string(R"({"display_name":"Aren",")") + field + R"(":true})");
    }
    for (auto payload : {R"({})", R"({"display_name":[]})", R"({"display_name":""})",
                         R"({"display_name":"Aren","display_name":"Second"})",
                         R"({"display_name":"Aren"} garbage)", R"({"display_name":"Aren"}{})",
                         R"({"display_name":"Aren\n"})", R"({"display_name":" Aren"})",
                         R"({"display_name":"\u3000"})", R"({"display_name":"\u202eAren"})",
                         R"json({"display_name":"Aren"} /* comment */)json"}) fixture.rejected(payload);
    fixture.rejected(std::string(R"({"display_name":")") + std::string(97, 'a') + R"("})");
    fixture.rejected(std::string(R"({"display_name":")") + "\xc0\xaf" + R"("})");
    fixture.rejected(std::string(1025, 'a'));
    const auto result = fixture.submit(std::string(R"({"display_name":")") + std::string(96, 'a') + R"("})");
    require(fixture.inspect(result).display_name.size() == 96, "UTF-8 byte limit rejected its inclusive boundary");
}

void unknowns()
{
    Candidate fixture;
    const auto view = fixture.inspect(fixture.submit());
    for (auto field : {"birthplace", "birth_date", "parents_names", "degree", "certificate", "teacher",
                       "instrument", "generations_between", "mutation", "diploma", "birth_planet"}) {
        require(std::ranges::none_of(view.background, [&](const auto& fact) { return fact.find(field) != std::string::npos; }),
                "An unspecified biographical value escaped into the Core");
    }
}

void core_candidate()
{
    Candidate fixture;
    const auto result = fixture.submit();
    const auto view = fixture.inspect(result);
    require(view.person != 0 && view.creation_fact != 0 && view.person != view.creation_fact &&
            view.person_count == 1 && view.creation_fact_count == 1 && view.revision > 0 &&
            view.population_count == 0 && view.tick == 0, "Expected one person and one initial fact");
    require(view.source_digest == "19317d97ef8f8e14483e544f0f7babab5c312f8c6f64c832ad47fb4936d35bc8",
            "Core did not bind the approved authoring digest");
    expect(fixture.owner.check_active(result.generation).get(), Error::OK);
}

void offline()
{
    Candidate fixture;
    const auto view = fixture.inspect(fixture.submit());
    require(view.creation_fact_count == 1, "Fixed candidate could not be created with plain SessionOwner");
}

void foreign_or_expired()
{
    Candidate fixture;
    Candidate foreign;
    auto denied = AcademyCandidateFactory::create(foreign.owner, fixture.intent, name).get();
    require(denied.error == Error::SCOPE_INVALID && !denied.receipt, "Foreign HOST intent obtained authority");
    closed(fixture.owner);
    closed(foreign.owner);
    expect(fixture.owner.close().get(), Error::OK);
    require(fixture.submit().error == Error::SCOPE_INVALID, "Closed pending attempt remained active");
    const auto stale = fixture.intent;
    fixture.intent = AcademyCandidateFactory::begin(fixture.owner);
    require(AcademyCandidateFactory::create(fixture.owner, stale, name).get().error == Error::SCOPE_INVALID,
            "Expired generation replaced the next attempt");
    require(!AcademyCandidateFactory::inspect(fixture.owner, {}).get().candidate,
            "Missing receipt resolved a Core PERSON");
    closed(fixture.owner);
}

void permissions()
{
    SessionOwner naval;
    Candidate fixture;
    const auto naval_generation = open(naval);
    require(!AcademyCandidateFactory::begin(naval), "A naval session issued an Academy attempt");
    fixture.rejected(name, Error::BUSY_STATE);
    expect(naval.check_active(naval_generation).get(), Error::OK);
    expect(naval.close().get(), Error::OK);

    const auto created = fixture.submit();
    const auto before = fixture.inspect(created);
    const auto generation = created.generation;
    const auto fails_unbound = [](const OperationResult& result) {
        require(result.error == Error::PRINCIPAL_UNBOUND && !result.campaign && !result.order && !result.receipt,
                "Academy candidate obtained naval authority");
    };
    fails_unbound(fixture.owner.query_view(generation).get());
    fails_unbound(fixture.owner.submit_order(generation, {}).get());
    fails_unbound(fixture.owner.institutional_command(generation).get());
    require(fixture.owner.current_player(generation).error == Error::PRINCIPAL_UNBOUND, "Automatic H03 binding");
    expect(fixture.owner.save(generation, "test").get(), Error::SAVE_INCOMPATIBLE);
    expect(fixture.owner.restore(generation, {before.campaign_id, "test", 0}).get(), Error::SAVE_INCOMPATIBLE);
    expect(naval.open(population()).get(), Error::BUSY_STATE);
    require(before.population_count == 0 && before.creation_fact_count == 1, "Candidacy consumed a place");
    same_world(before, fixture.inspect(created));
}

void receipt_resolution()
{
    Candidate fixture;
    Candidate foreign;
    const auto created = fixture.submit();
    const auto view = fixture.inspect(created);
    require(AcademyCandidateFactory::inspect(foreign.owner, created.receipt).get().error == Error::SCOPE_INVALID,
            "Foreign receipt selected a PERSON");
    for (auto id : {view.person, view.creation_fact, UINT64_C(0), UINT64_MAX}) {
        require(PlayerBootstrap::prepare(fixture.owner, created.generation, id).get().error == Error::ACCESS_DENIED,
                "Naval bootstrap resolved an Academy entity using a numeric selector");
    }
    expect(fixture.owner.close().get(), Error::OK);
    auto second = foreign.submit();
    foreign.inspect(second);
    require(AcademyCandidateFactory::inspect(foreign.owner, created.receipt).get().error == Error::SCOPE_INVALID &&
            AcademyCandidateFactory::inspect(fixture.owner, created.receipt).get().error == Error::SCOPE_INVALID,
            "Retired receipt selected a PERSON");
}

#if defined(TREK_HOST_ACADEMY_TESTING)
void bad_source()
{
    Candidate fixture;
    for (auto fault : {AcademyFault::SOURCE_VERSION, AcademyFault::SOURCE_DIGEST, AcademyFault::SOURCE_BYTES}) {
        set_academy_fault(fault);
        fixture.rejected(name, Error::DOMAIN_REJECTED);
    }
    set_academy_fault(AcademyFault::NONE);
    canonical();
}

void legacy_scope()
{
    static_assert(!std::is_convertible_v<trek::f10::BiographyReceipt, AcademyIntent>);
    static_assert(!std::is_convertible_v<trek::f10::BiographyReceipt, AcademyReceipt>);
    SessionOwner owner;
    const auto profile = BiographyProfileSource::begin(owner);
    require(profile && profile->current(profile->context()), "Missing native historical scope");
    const auto intent = AcademyCandidateFactory::begin(owner);
    require(bool(intent), "Missing v2 intent");
    require(!profile->current(profile->context()), "Historical scope remained active after beginning the v2 flow");
    const auto next_legacy = BiographyProfileSource::begin(owner);
    require(next_legacy && next_legacy->current(next_legacy->context()), "Legacy workflow cannot start again");
    require(AcademyCandidateFactory::create(owner, intent, name).get().error == Error::SCOPE_INVALID,
            "Superseded v2 intent obtained authority");
    closed(owner);
}

void failed_publication()
{
    Candidate fixture;
    for (auto fault : {AcademyFault::CATALOG, AcademyFault::PERSON, AcademyFault::FACT,
                       AcademyFault::HISTORY, AcademyFault::BEFORE_PUBLICATION}) {
        set_academy_fault(fault);
        fixture.rejected(name, Error::INTERNAL_ERROR);
        require(fixture.owner.campaign_id({}).empty() &&
                fixture.owner.current_player({}).error == Error::SESSION_CLOSED,
                "An incomplete campaign was visible");
        require(AcademyCandidateFactory::begin(fixture.owner) == fixture.intent,
                "Rollback lost the original attempt");
        SessionOwner naval;
        open(naval);
        expect(naval.close().get(), Error::OK);
    }
    set_academy_fault(AcademyFault::NONE);
    const auto created = fixture.submit();
    const auto view = fixture.inspect(created);
    require(view.person_count == 1 && view.creation_fact_count == 1 && view.population_count == 0,
            "Retry after rollback/verified Core archive duplicated the creation");
}
#endif
} // namespace

int main(int argc, char** argv)
try {
    if (argc != 2) return 2;
    for (const auto& test_case : {
        Case{"b02_01", canonical}, Case{"b02_02", new_campaign}, Case{"b02_03", replay}, Case{"b02_04", conflict},
        Case{"b02_05", immutable_fields}, Case{"b02_06", authority_fields}, Case{"b02_08", unknowns},
        Case{"b02_09", core_candidate}, Case{"b02_10", offline}, Case{"b02_11", foreign_or_expired},
        Case{"b02_13", permissions}, Case{"b02_15", receipt_resolution},
#if defined(TREK_HOST_ACADEMY_TESTING)
        Case{"b02_07", bad_source}, Case{"b02_11_legacy", legacy_scope}, Case{"b02_12", failed_publication},
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
