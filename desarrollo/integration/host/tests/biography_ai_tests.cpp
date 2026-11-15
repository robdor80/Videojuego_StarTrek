#include "f10/biography_evidence.h"
#include "f10/openai_biography.h"
#include <jsoncons/json.hpp>
#include <atomic>
#include <cstdlib>
#include <iostream>
#include <thread>
#include <type_traits>
using namespace trek::f10;
using namespace trek::host::ai;
using Json = jsoncons::json;
using namespace std::chrono_literals;
#define CHECK(x) do { if (!(x)) throw std::runtime_error("IA02 check at line " + std::to_string(__LINE__)); } while(false)
// Compile product sources without the historical privileged test constructor.
static_assert(std::is_final_v<OpenAiBiographyEvaluator>);
static_assert(!std::is_constructible_v<BiographyValidator, const BiographyAuthority&, SemanticEvaluator&, std::string, std::string>);
static_assert(!std::is_constructible_v<RegisteredBiographyAuthority, std::vector<RegisteredBiographySource>, std::vector<BiographyClaimEvidence>, std::shared_ptr<SemanticEvaluator>>);
namespace {
struct Keys final : CredentialStore {
    bool missing{};
    Error read(std::string& key) override { key = missing ? "" : "offline-fixture-key"; return missing ? Error::MISSING_KEY : Error::OK; }
    Error write(std::string_view) override { return Error::UNSUPPORTED_PLATFORM; }
};
struct Fake final : Transport {
    std::atomic<unsigned> calls{};
    std::atomic<bool> hold{}, started{};
    HttpResponse answer;
    Json sent;
    HttpResponse post(std::string_view body, std::string_view, std::chrono::steady_clock::time_point deadline,
                      std::stop_token stop, std::size_t) override {
        sent = Json::parse(body); ++calls; started = true;
        while (hold && !stop.stop_requested() && std::chrono::steady_clock::now() < deadline) std::this_thread::sleep_for(1ms);
        if (stop.stop_requested()) return {Error::CANCELLED};
        if (std::chrono::steady_clock::now() >= deadline) return {Error::TIMEOUT};
        return answer;
    }
};
HttpResponse response(std::string text = R"({"verdict":"COHERENT","issues":[]})", std::string model = "gpt-6-luna") {
    auto body = Json::parse(R"({"status":"completed","output":[{"type":"message","role":"assistant","status":"completed","content":[{"type":"output_text","text":""}]}]})");
    body["model"] = model; body["output"][0]["content"][0]["text"] = text;
    return {Error::OK, 200, body.to_string(), "application/json"};
}
Json draft() {
    return Json::parse(R"({"display_name":"Daniel Torres","species_id":"human","age_or_birth_date":20,
      "adult_equivalent_status":true,"origin":"Tierra","citizenship_context":"pendiente",
      "culture_context":"civil","appearance_profile":"descripción","prior_education":["estudios generales"],
      "prior_experience":["trabajo civil; interés por astronomía"],
      "prior_activities_and_hobbies":[{"name":"karate","started_at_or_age":8,"ended_at_or_current":"current"}],
      "initial_long_term_objective":"entrar en la Academia"})");
}
struct Fixture {
    // Source/claim fixtures are deliberately NOT product evidence or approval of real background.
    std::shared_ptr<Keys> keys = std::make_shared<Keys>();
    std::shared_ptr<Fake> http = std::make_shared<Fake>();
    std::shared_ptr<Service> service;
    std::shared_ptr<OpenAiBiographyEvaluator> adapter;
    BiographyContext context{"starfleet_academy","tng_ds9_voyager",2383,"","private-campaign",1,"private-profile"};
    Json data = draft();
    std::shared_ptr<RegisteredBiographyAuthority> authority;
    std::unique_ptr<BiographyValidator> validator;
    explicit Fixture(bool complex = false, std::chrono::milliseconds timeout = 2s) {
        Config config; config.timeout = timeout;
        http->answer = response(R"({"verdict":"COHERENT","issues":[]})", complex ? "gpt-6.1-sol" : "gpt-6-luna");
        service = std::make_shared<Service>(config, http, keys);
        adapter = std::make_shared<OpenAiBiographyEvaluator>(service, complex ? OpenAiBiographyEvaluator::Route::EXPLICIT_COMPLEX : OpenAiBiographyEvaluator::Route::HABITUAL);
        compose();
    }
    void compose(bool sources_available = true) {
        auto assessed = BiographyValidator{}.evaluate(data.to_string(), context);
        std::vector<RegisteredBiographySource> sources{RegisteredBiographyAuthority::initial_background_source()};
        std::vector<BiographyClaimEvidence> evidence;
        if (sources_available && assessed.objective.binding()) {
            for (const auto& issue : assessed.objective.issues()) {
                BiographySourceIdentity source{"fixture-" + std::to_string(sources.size()), "test-1", "offline-fixture", BiographyEvidenceOrigin::APPROVED_RULE};
                BiographyEvidenceClaim claim{issue.code, std::string(issue.field)};
                sources.push_back({source, {claim}});
                evidence.push_back({source, claim, *assessed.objective.binding(), BiographyEvidenceDecision::SUPPORTED});
            }
        }
        authority = std::make_shared<RegisteredBiographyAuthority>(std::move(sources), std::move(evidence), adapter);
        validator = std::make_unique<BiographyValidator>(authority);
    }
    BiographyEvaluation finish() {
        auto result = validator->evaluate(data.to_string(), context);
        const auto until = std::chrono::steady_clock::now() + 4s;
        while (result.semantic == SemanticStatus::REVIEW_REQUIRED && result.objective.status() == ObjectiveStatus::OBJECTIVE_VALID && std::chrono::steady_clock::now() < until) {
            std::this_thread::sleep_for(1ms);
            result = validator->evaluate(data.to_string(), context);
        }
        return result;
    }
    void wait_started() {
        const auto until = std::chrono::steady_clock::now() + 2s;
        while (!http->started && std::chrono::steady_clock::now() < until) std::this_thread::sleep_for(1ms);
        CHECK(http->started);
    }
};
void coherent() {
    Fixture f;
    const auto raw = f.data.to_string();
    auto first = f.validator->evaluate(raw, f.context);
    CHECK(first.semantic == SemanticStatus::REVIEW_REQUIRED && !first.receipt);
    auto result = f.finish();
    CHECK(result.semantic == SemanticStatus::VALID && result.receipt && result.feedback.empty());
    CHECK(f.validator->eligible(*result.receipt, raw, f.context));
    CHECK(f.http->calls == 1 && raw == f.data.to_string());
    CHECK(f.finish().semantic == SemanticStatus::VALID && f.http->calls == 1);
    const auto& sent = f.http->sent;
    CHECK(sent.at("model") == Json("gpt-6-luna"));
    CHECK(sent.at("text").at("format").at("strict") == Json(true));
    CHECK(sent.at("store") == Json(false) && !sent.contains("tools"));
    const auto body = sent.to_string();
    CHECK(body.find("private-campaign") == std::string::npos && body.find("private-profile") == std::string::npos);
    CHECK(body.find("offline-fixture-key") == std::string::npos);
    f.adapter->cancel();
    CHECK(!f.validator->eligible(*result.receipt, raw, f.context));
    Fixture complex(true);
    CHECK(complex.finish().semantic == SemanticStatus::VALID);
    CHECK(complex.http->sent.at("model") == Json("gpt-6.1-sol"));
}
void objective() {
    Fixture f;
    f.data["age_or_birth_date"] = 17;
    CHECK(f.finish().objective.status() == ObjectiveStatus::CHANGES_REQUIRED && f.http->calls == 0);
    f.data = draft(); f.data["prior_activities_and_hobbies"][0]["started_at_or_age"] = 21;
    CHECK(f.finish().objective.status() == ObjectiveStatus::CHANGES_REQUIRED && f.http->calls == 0);
    f.data = draft(); f.compose(false);
    auto pending = f.finish();
    CHECK(pending.objective.status() == ObjectiveStatus::REVIEW_REQUIRED && !pending.receipt && f.http->calls == 0);
    for (auto code : {IssueCode::ORIGIN_EVIDENCE_REQUIRED, IssueCode::CITIZENSHIP_EVIDENCE_REQUIRED,
                      IssueCode::EDUCATION_EVIDENCE_REQUIRED, IssueCode::EXPERIENCE_EVIDENCE_REQUIRED,
                      IssueCode::PROFILE_EVIDENCE_REQUIRED}) {
        bool found = false;
        for (const auto& issue : pending.objective.issues()) found |= issue.code == code;
        CHECK(found);
    }
    f.data["certifications"] = "médico especialista";
    pending = f.finish();
    bool missing = false;
    for (const auto& issue : pending.objective.issues()) missing |= issue.code == IssueCode::CERTIFICATION_EVIDENCE_REQUIRED;
    CHECK(missing && f.http->calls == 0);
}
void findings() {
    for (bool contradiction : {false, true}) {
        Fixture f;
        if (contradiction) { f.data["prior_experience"] = "Quince años como capitán y estudios simultáneos a tiempo completo"; f.compose(); }
        Json reply;
        reply["verdict"] = contradiction ? "CHANGES_REQUIRED" : "COHERENT";
        reply["issues"] = Json::array();
        Json issue;
        issue["field"] = "prior_experience";
        issue["kind"] = contradiction ? "CONTRADICTION" : "SUGGESTION";
        issue["reason"] = contradiction ? "La duración del mando y los estudios contradicen la edad y la condición de aspirante." : "La astronomía es una afición, sin competencia profesional acreditada.";
        issue["suggested_correction"] = "Aclara la cronología y distingue la afición de una certificación.";
        reply["issues"].push_back(issue);
        f.http->answer = response(reply.to_string());
        const auto before = f.data.to_string();
        const auto result = f.finish();
        CHECK(result.semantic == (contradiction ? SemanticStatus::CHANGES_REQUIRED : SemanticStatus::VALID));
        CHECK(result.receipt.has_value() == !contradiction && result.feedback.size() == 1);
        CHECK(result.feedback[0].reason == issue.at("reason").as<std::string>());
        CHECK(before == f.data.to_string());
    }
}
void failures() {
    for (auto text : {"{", "{}", R"({"verdict":"APPROVED","issues":[]})", R"({"verdict":"CHANGES_REQUIRED","issues":[]})",
         R"({"verdict":"COHERENT","issues":[],"approved":true})",
         R"({"verdict":"COHERENT","issues":[{"field":"permissions","kind":"SUGGESTION","reason":"x","suggested_correction":"x"}]})",
         R"({"verdict":"COHERENT","issues":[{"field":"prior_experience","kind":"CONTRADICTION","reason":"x","suggested_correction":"x"}]})"}) {
        Fixture f; f.http->answer = response(text);
        auto result = f.finish();
        CHECK(result.semantic == SemanticStatus::REVIEW_UNAVAILABLE && !result.receipt && result.feedback.empty());
        CHECK(f.http->calls == 1 && f.finish().semantic == SemanticStatus::REVIEW_UNAVAILABLE && f.http->calls == 1);
    }
    for (int status : {401,429,500,503}) {
        Fixture f; f.http->answer = {Error::OK,status,"{}","application/json"};
        CHECK(f.finish().semantic == SemanticStatus::REVIEW_UNAVAILABLE);
        CHECK(f.adapter->error() == (status == 401 ? Error::INVALID_CREDENTIAL : status == 429 ? Error::RATE_LIMIT : Error::CONNECTION));
    }
    for (bool refusal : {false,true}) {
        Fixture f;
        f.http->answer.body = refusal ? R"({"model":"gpt-6-luna","status":"completed","output":[{"type":"message","content":[{"type":"refusal"}]}]})" : R"({"model":"gpt-6-luna","status":"incomplete","output":[]})";
        CHECK(f.finish().semantic == SemanticStatus::REVIEW_UNAVAILABLE);
        CHECK(f.adapter->error() == (refusal ? Error::REFUSAL : Error::INCOMPLETE));
    }
    for (auto model : {"other-model", "gpt-6-luna-old"}) {
        Fixture f; f.http->answer = response(R"({"verdict":"COHERENT","issues":[]})", model);
        CHECK(f.finish().semantic == SemanticStatus::REVIEW_UNAVAILABLE);
    }
    Fixture no_model; auto body = Json::parse(no_model.http->answer.body); body.erase("model"); no_model.http->answer.body = body.to_string();
    CHECK(no_model.finish().semantic == SemanticStatus::REVIEW_UNAVAILABLE);
    Fixture no_key; no_key.keys->missing = true;
    CHECK(no_key.finish().semantic == SemanticStatus::REVIEW_UNAVAILABLE && no_key.http->calls == 0);
    CHECK(no_key.adapter->error() == Error::MISSING_KEY);
    Fixture timeout(false, 100ms); timeout.http->hold = true;
    CHECK(timeout.finish().semantic == SemanticStatus::REVIEW_UNAVAILABLE && timeout.adapter->error() == Error::TIMEOUT);
}
void provenance() {
    Fixture f;
    auto accepted = f.finish(); CHECK(accepted.receipt);
    const auto canonical = f.data.to_string();
    const auto bound = *accepted.objective.binding();
    ReviewRequest request{canonical, bound, &f.context};
    auto genuine = f.adapter->review(request);
    CHECK(f.authority->verify(request, genuine) == DomainDecision::ACCEPTED);
    auto unregistered = RegisteredBiographyAuthority({}, {});
    CHECK(unregistered.verify(request, genuine) == DomainDecision::UNVERIFIED);
    for (int mutation = 0; mutation != 9; ++mutation) {
        auto forged = genuine;
        switch (mutation) {
        case 0: forged.reviewer = "simulated"; break;
        case 1: forged.reviewer_version = "old"; break;
        case 2: forged.review_ref += "-fabricated"; break;
        case 3: forged.binding.draft_sha256[0] ^= 1; break;
        case 4: forged.binding.context_sha256[0] ^= 1; break;
        case 5: forged.binding.ruleset += "-old"; break;
        case 6: forged.binding.policy += "-old"; break;
        case 7: forged.completion = ReviewCompletion::INCOMPLETE; break;
        case 8: forged.findings.push_back({FindingKind::SUGGESTION,"prior_experience","fabricated","fabricated"}); break;
        }
        CHECK(f.authority->verify(request, forged) == DomainDecision::UNVERIFIED);
    }
    std::string other = "{}";
    CHECK(f.authority->verify({other, bound, &f.context}, genuine) == DomainDecision::UNVERIFIED);
    f.adapter->cancel();
    CHECK(f.authority->verify(request, genuine) == DomainDecision::UNVERIFIED);
    CHECK(!f.validator->eligible(*accepted.receipt, canonical, f.context));
}
void replacement() {
    Fixture f; f.http->hold = true;
    auto first = f.validator->evaluate(f.data.to_string(), f.context);
    f.wait_started();
    const auto previous = *first.objective.binding();
    f.data["display_name"] = "Otro borrador";
    f.compose(); // New trusted objective fixture, never reuses the old evidence.
    auto pending = f.validator->evaluate(f.data.to_string(), f.context);
    CHECK(pending.semantic == SemanticStatus::REVIEW_REQUIRED && !pending.receipt);
    CHECK(*pending.objective.binding() != previous);
    f.http->hold = false;
    auto current = f.finish();
    CHECK(current.semantic == SemanticStatus::VALID && current.receipt && f.http->calls == 2);
    CHECK(f.validator->eligible(*current.receipt, f.data.to_string(), f.context));
    auto stale_evidence = ReviewEvidence{previous, ReviewCompletion::COMPLETE,
        std::string(OpenAiBiographyEvaluator::identity), std::string(OpenAiBiographyEvaluator::version), "ia02-1", {}};
    CHECK(f.authority->verify({f.data.to_string(), previous, &f.context}, stale_evidence) == DomainDecision::UNVERIFIED);
}
void stale() {
    for (int change = 0; change < 7; ++change) {
        Fixture f; f.http->hold = true;
        auto first = f.validator->evaluate(f.data.to_string(), f.context);
        CHECK(first.semantic == SemanticStatus::REVIEW_REQUIRED); f.wait_started();
        const auto old_binding = *first.objective.binding();
        switch (change) {
        case 0: f.data["display_name"] = "Editado"; break;
        case 1: f.data["species_id"] = "vulcan"; break;
        case 2: f.context.campaign += "-new"; break;
        case 3: ++f.context.generation; break;
        case 4: f.context.profile += "-new"; break;
        case 5: f.adapter->cancel(); break;
        case 6: f.context.generation = 0; break;
        }
        auto changed = f.validator->evaluate(f.data.to_string(), f.context);
        CHECK(!changed.receipt);
        // Changes 0..4 invalidate objective snapshot; cancellation requires a fresh operation.
        if (change < 5) CHECK(changed.objective.status() != ObjectiveStatus::OBJECTIVE_VALID);
        auto forged = ReviewEvidence{old_binding, ReviewCompletion::COMPLETE, std::string(OpenAiBiographyEvaluator::identity), std::string(OpenAiBiographyEvaluator::version), "ia02-1", {}};
        CHECK(f.authority->verify({f.data.to_string(), old_binding, &f.context}, forged) == DomainDecision::UNVERIFIED);
        f.adapter->cancel();
    }
}
}
int main() {
    try {
        // No real secret is read or printed. Isolate the simulated MISSING_KEY case.
#ifdef _WIN32
        _putenv_s("OPENAI_API_KEY", "");
#else
        unsetenv("OPENAI_API_KEY");
#endif
        coherent(); objective(); findings(); failures(); provenance(); replacement(); stale();
        std::cout << "PASS IA02 offline product adapter; no network or Core writes\n";
    } catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 1; }
}
