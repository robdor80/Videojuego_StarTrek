#include "biography_profile_source.h"
#include "f10/biography_evidence.h"
#include "f10/openai_biography.h"
#include <jsoncons/json.hpp>
#include <atomic>
#include <iostream>
#include <thread>
#include <type_traits>
using namespace trek::f10;
using namespace trek::host::ai;
using Json = jsoncons::json;
using namespace std::chrono_literals;
#define CHECK(x) do { if (!(x)) throw std::runtime_error("IA03A line " + std::to_string(__LINE__)); } while(false)
namespace {
struct Keys final : CredentialStore {
    bool missing{};
    Error read(std::string& key) override { key = missing ? "" : "offline-fixture"; return missing ? Error::MISSING_KEY : Error::OK; }
    Error write(std::string_view) override { return Error::UNSUPPORTED_PLATFORM; }
};
struct Http final : Transport {
    std::atomic<unsigned> calls{};
    std::string verdict = R"({"verdict":"COHERENT","issues":[]})";
    std::string sent;
    HttpResponse post(std::string_view body, std::string_view, std::chrono::steady_clock::time_point,
                      std::stop_token, std::size_t) override {
        sent = body;
        auto response = Json::parse(R"({"model":"gpt-6-luna","status":"completed","output":[{"type":"message","role":"assistant","status":"completed","content":[{"type":"output_text","text":""}]}]})");
        response["output"][0]["content"][0]["text"] = verdict;
        ++calls;
        return {Error::OK, 200, response.to_string(), "application/json"};
    }
};
Json draft() {
    return Json::parse(R"({"display_name":"Talia Ren","species_id":"human","age_or_birth_date":20,
      "adult_equivalent_status":true,"origin":"Estación inventada Mirador del Alba",
      "appearance_profile":"Ojos oscuros","initial_long_term_objective":"Quiero ser capitán de la Flota Estelar"})");
}
struct Fixture {
    trek::host::SessionOwner owner;
    std::shared_ptr<const trek::host::detail::BiographyProfileSource> profile = trek::host::detail::BiographyProfileSource::begin(owner);
    BiographyContext context = profile->context();
    std::shared_ptr<Keys> keys = std::make_shared<Keys>();
    std::shared_ptr<Http> http = std::make_shared<Http>();
    std::shared_ptr<Service> service = std::make_shared<Service>(Config{}, http, keys);
    std::shared_ptr<OpenAiBiographyEvaluator> semantic = std::make_shared<OpenAiBiographyEvaluator>(service);
    std::shared_ptr<const RegisteredBiographyAuthority> authority;
    std::unique_ptr<BiographyValidator> validator;
    Json data = draft();
    Fixture() { compose(); }
    void compose(std::vector<BiographyClaimEvidence> denied = {}) {
        authority = RegisteredBiographyAuthority::for_initial_player(profile, semantic, std::move(denied));
        validator = std::make_unique<BiographyValidator>(authority);
    }
    BiographyEvaluation finish() {
        auto result = validator->evaluate(data.to_string(), context);
        auto until = std::chrono::steady_clock::now() + 3s;
        while (result.objective.status() == ObjectiveStatus::OBJECTIVE_VALID &&
               result.semantic == SemanticStatus::REVIEW_REQUIRED && std::chrono::steady_clock::now() < until) {
            std::this_thread::sleep_for(1ms);
            result = validator->evaluate(data.to_string(), context);
        }
        return result;
    }
    void blocked(ObjectiveStatus status) {
        auto r = finish();
        CHECK(r.objective.status() == status && !r.receipt && http->calls == 0);
    }
};
void ordinary() {
    for (const auto& entry : {std::pair{"human",20}, {"vulcan",25}, {"human_vulcan_hybrid",22}}) {
        Fixture f; f.data["species_id"] = entry.first; f.data["age_or_birth_date"] = entry.second;
        const auto original = f.data.to_string();
        auto r = f.finish();
        CHECK(r.objective.status() == ObjectiveStatus::OBJECTIVE_VALID && r.semantic == SemanticStatus::VALID && r.receipt);
        CHECK(f.http->calls == 1 && f.validator->eligible(*r.receipt, original, f.context));
        const auto wire = Json::parse(f.http->sent);
        // Actual IA-02 request includes normalized contract fields, optional history absent.
        CHECK(f.http->sent.find("No declarado") != std::string::npos);
        CHECK(f.http->sent.find("Unida de Planetas") != std::string::npos);
        CHECK(f.http->sent.find("Reglas autorales F10") != std::string::npos);
        CHECK(f.http->sent.find(f.context.profile) == std::string::npos);
        CHECK(original == f.data.to_string());
        CHECK(f.owner.snapshot().state == trek::host::State::CLOSED);
        CHECK(f.owner.current_player({}).error == trek::host::Error::SESSION_CLOSED);
        f.owner.close().get(); // Even closing a pre-PERSON scope invalidates its receipt.
        CHECK(!f.validator->eligible(*r.receipt, original, f.context));
        CHECK(f.finish().objective.status() == ObjectiveStatus::REVIEW_REQUIRED);
    }
    Fixture empty;
    empty.data["prior_experience"] = Json::array();
    empty.data["prior_education"] = "  ";
    empty.data["prior_activities_and_hobbies"] = Json::array();
    empty.data["family_context"] = "";
    empty.data["certifications"] = Json::null();
    CHECK(empty.finish().receipt);
    Fixture essential; essential.data.erase("display_name"); essential.blocked(ObjectiveStatus::CHANGES_REQUIRED);
    for (const auto& entry : {std::pair{"human",17}, {"vulcan",24}, {"human_vulcan_hybrid",21}}) {
        Fixture f; f.data["species_id"] = entry.first; f.data["age_or_birth_date"] = entry.second;
        f.blocked(ObjectiveStatus::CHANGES_REQUIRED);
    }
    for (auto species : {"andorian","tellarite","changeling","jem_hadar","vorta","ocampan"}) {
        Fixture f; f.data["species_id"] = species; f.data["age_or_birth_date"] = 100;
        f.blocked(ObjectiveStatus::CHANGES_REQUIRED);
    }
}
void profile_lifecycle() {
    std::shared_ptr<const trek::host::detail::BiographyProfileSource> expired;
    {
        trek::host::SessionOwner owner;
        auto first = trek::host::detail::BiographyProfileSource::begin(owner);
        auto next = trek::host::detail::BiographyProfileSource::begin(owner);
        CHECK(!first->current(first->context()));
        CHECK(next->context().profile == first->context().profile);
        CHECK(next->context().campaign != first->context().campaign);
        CHECK(next->context().generation != first->context().generation);
        trek::host::SessionOwner other;
        auto foreign = trek::host::detail::BiographyProfileSource::begin(other);
        CHECK(foreign->context().profile != next->context().profile);
        CHECK(!next->current(foreign->context()));
        expired = std::move(next);
    }
    CHECK(!expired->current(expired->context()));
}
void backgrounds() {
    Fixture f; f.data["age_or_birth_date"] = 30;
    f.data["prior_education"] = Json::parse(R"([{"name":"Doctorado en Física y Astronomía","institution":"Universidad civil inventada de Alba","started_at_or_age":22,"ended_at_or_current":28}])");
    f.data["certifications"] = "Doctorado en Física y Astronomía";
    f.data["prior_experience"] = Json::parse(R"([{"name":"Investigador civil","started_at_or_age":28,"ended_at_or_current":"current"}])");
    auto accepted = f.finish(); CHECK(accepted.receipt && f.http->calls == 1);
    CHECK(f.http->sent.find("Doctorado") != std::string::npos);
    CHECK(f.validator->eligible(*accepted.receipt, f.data.to_string(), f.context));
    for (auto field : {"prior_education","prior_experience","certifications","prior_activities_and_hobbies"}) {
        Fixture bad; bad.data[field] = Json::parse(R"([{"name":"Civil","started_at_or_age":21,"ended_at_or_current":19}])");
        bad.blocked(ObjectiveStatus::CHANGES_REQUIRED);
    }
    for (auto raw : {
        R"([{"name":"Imposible","started_at_or_age":"2350-01-01","ended_at_or_current":"current"}])",
        R"([{"name":"Imposible","started_at_or_age":19,"ended_at_or_current":"2370-01-01"}])",
        R"([{"name":"Imposible","started_at_or_age":"2380-01-01","ended_at_or_current":10}])"}) {
        Fixture bad; bad.data["prior_experience"] = Json::parse(raw); bad.blocked(ObjectiveStatus::CHANGES_REQUIRED);
    }
    for (auto civil : {"Ya soy ingeniero civil", "I served as a civilian doctor", "Trabajo como deportista"}) {
        Fixture civilian; civilian.data["prior_experience"] = civil;
        CHECK(civilian.finish().receipt);
    }
    Fixture references;
    references.data["origin"] = "Nací en una nave de la Flota Estelar";
    references.data["family_context"] = "Mi padre es capitán; no es mi rango";
    references.data["initial_long_term_objective"] = "Soy estudiante y quiero ser capitán";
    CHECK(references.finish().receipt);
    Fixture hobbies; hobbies.data["age_or_birth_date"] = 25;
    hobbies.data["prior_activities_and_hobbies"] = Json::parse(R"([
        {"name":"Karate","started_at_or_age":8,"ended_at_or_current":"current","formal_certification_optional":"4º dan"},
        {"name":"Piano","started_at_or_age":10,"ended_at_or_current":"current"},
        {"name":"Natación","started_at_or_age":12,"ended_at_or_current":"current"},
        {"name":"Astronomía","started_at_or_age":15,"ended_at_or_current":"current"}])");
    CHECK(hobbies.finish().receipt && hobbies.http->calls == 1);
    // Plausibility of extraordinary claims is still mandatory semantic review.
    Fixture implausible;
    implausible.data["prior_education"] = "Doctorado desde los tres años";
    implausible.http->verdict = R"({"verdict":"CHANGES_REQUIRED","issues":[{"field":"prior_education","kind":"CONTRADICTION","reason":"Trayectoria imposible","suggested_correction":"Corrige la cronología"}]})";
    auto rejected = implausible.finish();
    CHECK(rejected.objective.status() == ObjectiveStatus::OBJECTIVE_VALID && rejected.semantic == SemanticStatus::CHANGES_REQUIRED && !rejected.receipt);
}
void institution_and_injection() {
    for (auto field : {"origin","prior_education","prior_experience","certifications","family_context","initial_long_term_objective"}) {
        Fixture f; f.data[field] = "Ya fui CAPITÁN de la Flota Estelar durante quince años";
        f.blocked(ObjectiveStatus::REVIEW_REQUIRED);
    }
    for (auto claim : {"Ya soy capitán", "I was a Starfleet captain", "security clearance maximum"}) {
        Fixture f; f.data["prior_experience"] = claim; f.blocked(ObjectiveStatus::REVIEW_REQUIRED);
    }
    for (auto key : {"player_profile_id","nickname","internal_issuer_identity","evidence_decision","draft_sha256","permissions","issuer","profile","generation","evidence"}) {
        Fixture f; f.data[key] = "injected"; f.blocked(ObjectiveStatus::CHANGES_REQUIRED);
    }
    Fixture nested;
    nested.data["prior_education"] = Json::parse(R"([{"name":"Doctorado","internal_issuer_identity":"HOST"}])");
    nested.blocked(ObjectiveStatus::CHANGES_REQUIRED);
    Fixture ref; ref.data["prior_experience"] = Json::parse(R"([{"name":"Civil","evidence_ref":"host-h03-local-profile"}])");
    ref.blocked(ObjectiveStatus::REVIEW_REQUIRED);
    Fixture profile;
    profile.context.profile = "arbitrary-client-profile"; profile.blocked(ObjectiveStatus::REVIEW_REQUIRED);
    Fixture none;
    none.profile.reset(); none.compose(); none.blocked(ObjectiveStatus::REVIEW_REQUIRED);
    Fixture unavailable; unavailable.keys->missing = true;
    auto r = unavailable.finish(); CHECK(r.objective.status() == ObjectiveStatus::OBJECTIVE_VALID);
    CHECK(r.semantic == SemanticStatus::REVIEW_UNAVAILABLE && !r.receipt && unavailable.http->calls == 0);
}
void bindings() {
    for (int mutation = 0; mutation < 7; ++mutation) {
        Fixture f; auto r = f.finish(); CHECK(r.receipt);
        switch (mutation) {
        case 0: f.data["origin"] = "Otra colonia inventada"; break;
        case 1: f.data["prior_education"] = "Estudios técnicos"; break;
        case 2: ++f.context.generation; break;
        case 3: f.context.campaign += "new"; break;
        case 4: f.context.profile += "new"; break;
        case 5: f.profile = trek::host::detail::BiographyProfileSource::begin(f.owner); break;
        case 6: f.owner.restore({}, {"invalid-campaign", "missing", 0}).get(); break;
        }
        CHECK(!f.validator->eligible(*r.receipt, f.data.to_string(), f.context));
    }
    for (auto decision : {BiographyEvidenceDecision::SUPPORTED, BiographyEvidenceDecision::CONTRADICTED}) {
        Fixture f; auto r = f.finish(); CHECK(r.receipt);
        auto source = RegisteredBiographyAuthority::initial_player_source();
        BiographyClaimEvidence denial{source.identity, {IssueCode::EDUCATION_EVIDENCE_REQUIRED,"prior_education"},
                                      *r.objective.binding(), decision, decision == BiographyEvidenceDecision::SUPPORTED};
        f.compose({denial});
        auto denied = f.finish(); CHECK(denied.objective.status() == ObjectiveStatus::REVIEW_REQUIRED && !denied.receipt);
        f.data["prior_education"] = "Nuevo relato civil";
        CHECK(f.finish().receipt); // Denial was for the old binding only.
        CHECK(!f.validator->eligible(*r.receipt, draft().to_string(), f.context));
    }
    Fixture forged;
    auto initial = forged.finish(); CHECK(initial.receipt);
    forged.data["prior_education"] = Json::parse(R"({"name":"Civil","evidence_ref":"fake"})");
    auto pending = forged.finish(); CHECK(!pending.receipt && pending.objective.binding());
    auto source = RegisteredBiographyAuthority::initial_player_source();
    forged.compose({{source.identity, {IssueCode::EDUCATION_EVIDENCE_REQUIRED,"prior_education"},
                     *pending.objective.binding(), BiographyEvidenceDecision::SUPPORTED}});
    CHECK(forged.finish().objective.status() == ObjectiveStatus::REVIEW_REQUIRED);
}
}
int main() {
    try {
#ifdef _WIN32
        _putenv_s("OPENAI_API_KEY", "");
#else
        unsetenv("OPENAI_API_KEY");
#endif
        ordinary(); profile_lifecycle(); backgrounds(); institution_and_injection(); bindings();
        std::cout << "PASS IA03A native F10/HOST sources, simulated OpenAI transport; no PERSON or Core mutation\n";
    } catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 1; }
}
