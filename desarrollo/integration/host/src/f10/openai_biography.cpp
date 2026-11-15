#include "openai_biography.h"
#include "biography_rules_data.h"
#include <jsoncons/json.hpp>
#include <algorithm>
#include <stdexcept>

namespace trek::f10 {
namespace {
using Json = jsoncons::json;
const Json& rules() {
    static const auto value = Json::parse(detail::biography_rules_json);
    return value;
}
bool allowed_field(std::string_view field) {
    for (auto key : {"required", "optional"})
        for (const auto& item : rules().at(key).array_range())
            if (item.as_string_view() == field) return true;
    return false;
}
Json schema() {
    auto result = Json::parse(R"({"type":"object","additionalProperties":false,
      "required":["verdict","issues"],"properties":{
      "verdict":{"type":"string","enum":["COHERENT","CHANGES_REQUIRED"]},
      "issues":{"type":"array","maxItems":16,"items":{"type":"object","additionalProperties":false,
      "required":["field","kind","reason","suggested_correction"],"properties":{
      "field":{"type":"string","enum":[]},
      "kind":{"type":"string","enum":["CONTRADICTION","SUGGESTION"]},
      "reason":{"type":"string","minLength":1,"maxLength":512},
      "suggested_correction":{"type":"string","minLength":1,"maxLength":512}}}}}})");
    const auto& limits = rules().at("semantic").at("limits");
    auto& issues = result["properties"]["issues"];
    issues["maxItems"] = limits.at("issues");
    for (auto name : {"reason", "suggested_correction"})
        issues["items"]["properties"][name]["maxLength"] = limits.at("explanation_characters");
    auto& fields = result["properties"]["issues"]["items"]["properties"]["field"]["enum"];
    for (auto key : {"required", "optional"})
        for (const auto& field : rules().at(key).array_range()) fields.push_back(field);
    return result;
}
}
OpenAiBiographyEvaluator::OpenAiBiographyEvaluator(std::shared_ptr<host::ai::Service> service, Route route)
    : service_(std::move(service)),
      route_(route == Route::HABITUAL ? "FAST_LANGUAGE" : "REASONING_LANGUAGE") {
    if (!service_) throw std::invalid_argument("F10 requires shared AI service");
    model_ = service_->route_model(route_);
    if (model_.empty()) throw std::invalid_argument("F10 requires configured AI route");
}
OpenAiBiographyEvaluator::~OpenAiBiographyEvaluator() { cancel(); }
void OpenAiBiographyEvaluator::cancel() noexcept {
    if (operation_) operation_->cancel();
    operation_.reset(); record_.reset(); context_.reset(); canonical_.clear();
    error_ = host::ai::Error::CANCELLED;
}
ReviewEvidence OpenAiBiographyEvaluator::review(const ReviewRequest& request) {
    using namespace host::ai;
    if (!request.context) return {};
    if (record_ && (canonical_ != request.canonical_draft || record_->binding != request.binding ||
                    context_ != *request.context)) cancel();
    if (!record_) {
        canonical_ = request.canonical_draft;
        context_ = *request.context; // No borrowed views survive this call.
        record_ = ReviewEvidence{request.binding, ReviewCompletion::UNAVAILABLE,
            std::string(identity), std::string(version), "ia02-" + std::to_string(++serial_), {}};
        error_ = Error::INTERNAL;
        try {
            const auto draft = Json::parse(canonical_);
            Json input;
            input["biography"] = draft;
            input["campaign"]["scenario"] = context_->scenario;
            input["campaign"]["era"] = context_->era;
            input["campaign"]["start_year"] = context_->start_year;
            input["campaign"]["start_month_day"] = "UNDECIDED_BY_AUTHOR";
            // Campaign/profile IDs and generation bind locally; they are unnecessary on the wire.
            input["species_restrictions"] = rules().at("species").at(draft.at("species_id").as_string_view());
            input["species_public_profile"] = rules().at("semantic_species").at(draft.at("species_id").as_string_view());
            input["ruleset"] = request.binding.ruleset;
            input["policy"] = request.binding.policy;
            input["evaluator_version"] = version;
            Request outgoing;
            outgoing.route = route_;
            outgoing.instructions = rules().at("semantic").at("instructions_es").as<std::string>();
            if (request.binding.ruleset.ends_with(":initial-player/0.1.0"))
                outgoing.instructions += "\n" + rules().at("initial_player").at("semantic_instructions_es").as<std::string>();
            outgoing.input = input.to_string();
            outgoing.json_schema = schema().to_string();
            outgoing.require_model_identity = true;
            operation_.emplace(service_->submit(std::move(outgoing)));
            record_->completion = ReviewCompletion::PENDING;
            error_ = Error::OK;
        } catch (...) { error_ = Error::INTERNAL; }
        return *record_;
    }
    if (!operation_ || operation_->result.wait_for(std::chrono::milliseconds(0)) != std::future_status::ready)
        return *record_;
    try {
        auto result = operation_->result.get(); // Ready only; Service owns the sole worker.
        operation_.reset();
        record_->completion = ReviewCompletion::UNAVAILABLE;
        error_ = result.error;
        if (result.error != Error::OK) return *record_;
        error_ = Error::MALFORMED;
        if (result.model != model_ || result.text.size() > rules().at("semantic").at("limits").at("response_bytes").as<std::size_t>()) return *record_;
        const auto parsed = Json::parse(result.text); // Service already checked strict schema.
        const auto verdict = parsed.at("verdict").as<std::string>();
        bool contradiction = false;
        std::vector<ReviewFinding> findings;
        for (const auto& issue : parsed.at("issues").array_range()) {
            const auto kind = issue.at("kind").as<std::string>();
            auto field = issue.at("field").as<std::string>();
            auto reason = issue.at("reason").as<std::string>();
            auto correction = issue.at("suggested_correction").as<std::string>();
            if (!allowed_field(field) || (kind != "CONTRADICTION" && kind != "SUGGESTION") ||
                reason.find_first_not_of(" \t\r\n") == std::string::npos ||
                correction.find_first_not_of(" \t\r\n") == std::string::npos || findings.size() >= rules().at("semantic").at("limits").at("issues").as<std::size_t>()) return *record_;
            const bool conflict = kind == "CONTRADICTION";
            contradiction |= conflict;
            findings.push_back({conflict ? FindingKind::CONTRADICTION : FindingKind::SUGGESTION,
                                std::move(field), std::move(reason), std::move(correction)});
        }
        if ((verdict != "COHERENT" && verdict != "CHANGES_REQUIRED") ||
            contradiction != (verdict == "CHANGES_REQUIRED")) return *record_;
        record_->findings = std::move(findings);
        record_->completion = ReviewCompletion::COMPLETE;
        error_ = Error::OK;
    } catch (...) {
        operation_.reset(); record_->completion = ReviewCompletion::UNAVAILABLE;
        error_ = Error::MALFORMED;
    }
    return *record_;
}
DomainDecision OpenAiBiographyEvaluator::verify(const ReviewRequest& request, const ReviewEvidence& evidence) const {
    if (!record_ || !context_ || !request.context || *request.context != *context_ ||
        canonical_ != request.canonical_draft || evidence != *record_ ||
        evidence.binding != request.binding || evidence.completion != ReviewCompletion::COMPLETE ||
        evidence.reviewer != identity || evidence.reviewer_version != version ||
        service_->route_model(route_) != model_ || error_ != host::ai::Error::OK) return DomainDecision::UNVERIFIED;
    for (const auto& finding : evidence.findings) {
        if (!allowed_field(finding.field) || (finding.kind != FindingKind::CONTRADICTION &&
            finding.kind != FindingKind::SUGGESTION)) return DomainDecision::UNVERIFIED;
    }
    return std::ranges::any_of(evidence.findings, [](const auto& f) { return f.kind == FindingKind::CONTRADICTION; })
        ? DomainDecision::CORRECTIONS : DomainDecision::ACCEPTED;
}
}
