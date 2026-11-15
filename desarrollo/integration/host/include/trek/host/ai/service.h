#pragma once
#include <chrono>
#include <cstddef>
#include <future>
#include <filesystem>
#include <map>
#include <memory>
#include <stop_token>
#include <string>
#include <string_view>

#if defined(TREK_HOST_STATIC_TEST)
#define TREK_AI_API
#elif defined(_WIN32)
#ifdef TREK_HOST_BUILD
#define TREK_AI_API __declspec(dllexport)
#else
#define TREK_AI_API __declspec(dllimport)
#endif
#else
#define TREK_AI_API __attribute__((visibility("default")))
#endif

namespace trek::host::ai {
enum class Error {
    OK, CONFIGURATION, MISSING_KEY, INVALID_CREDENTIAL, CREDENTIAL_STORAGE,
    UNSUPPORTED_PLATFORM, MODEL_UNAVAILABLE, HTTP_ERROR, CONNECTION,
    QUOTA, RATE_LIMIT, TIMEOUT, CANCELLED, INCOMPLETE, MALFORMED,
    REFUSAL, CAPACITY, SIZE_LIMIT, INTERNAL
};
TREK_AI_API std::string_view diagnostic(Error) noexcept; // Fixed codes only; safe to log.
TREK_AI_API bool retryable(Error) noexcept; // Caller decides; service never retries.
struct Result {
    Error error{Error::OK};
    int http_status{};
    std::string text; // Untrusted candidate, never authority. Empty on every failure.
    std::string model;
};
struct Config {
    std::string fast_model{"gpt-6-luna"}, reasoning_model{"gpt-6.1-sol"};
    std::string reasoning_effort{"low"};
    std::map<std::string, std::string> routes{
        {"FAST_LANGUAGE", "fast"}, {"REASONING_LANGUAGE", "reasoning"},
        {"DIALOGUE", "fast"}, {"COMPUTER_ANALYSIS", "fast"}, {"NARRATIVE_SUMMARY", "fast"}};
    std::chrono::milliseconds timeout{20000};
    std::size_t max_request_bytes{65536}, max_response_bytes{131072}, max_output_bytes{32768};
    unsigned max_output_tokens{1024}, max_pending{8}, max_calls{200};
};
// Bounded JSON document; invalid configuration never falls back silently.
TREK_AI_API Error parse_config(std::string_view json, Config& out) noexcept;
TREK_AI_API Error load_config(const std::filesystem::path&, Config& out) noexcept;
struct Request {
    std::string route{"FAST_LANGUAGE"};
    std::string instructions; // Trusted HOST task policy only, never player text.
    std::string input; // Authorized context/player data, separated from internal instructions.
    std::string json_schema; // Optional strict schema; no remote references.
    bool require_model_identity{}; // Consumers may require the response model to match the configured route.
};
// Internal HOST credential port. Do not expose read() or keys to Blueprint.
class CredentialStore {
public:
    virtual ~CredentialStore() = default;
    virtual Error read(std::string& key) = 0;
    virtual Error write(std::string_view key) = 0;
};
inline constexpr std::string_view shared_credential_identity = "PersonalRPG/OpenAI/APIKey/v1";
TREK_AI_API std::shared_ptr<CredentialStore> shared_credentials();
struct CredentialStatus { bool shared{}, environment{}; Error storage_error{Error::OK}; };
TREK_AI_API CredentialStatus credential_status(CredentialStore&) noexcept;
TREK_AI_API Error register_key(CredentialStore&, std::string_view) noexcept;
TREK_AI_API Error import_environment_key(CredentialStore&) noexcept; // Explicit future wizard action.
struct HttpResponse {
    Error error{Error::OK};
    int status{};
    std::string body, content_type;
};
class Transport {
public:
    virtual ~Transport() = default;
    // Implementations must honor deadline/cancellation and bound received bytes.
    virtual HttpResponse post(std::string_view body, std::string_view key,
        std::chrono::steady_clock::time_point deadline, std::stop_token,
        std::size_t max_response_bytes) = 0;
};
TREK_AI_API std::shared_ptr<Transport> https_transport();
struct Operation {
    std::future<Result> result;
    std::stop_source cancellation;
    void cancel() noexcept { cancellation.request_stop(); }
};
// One bounded worker; no Core references, callbacks, world state or persistence.
// Same-toolchain internal C++ API, not a new Unreal binary ABI.
class TREK_AI_API Service final {
public:
    explicit Service(Config = {}, std::shared_ptr<Transport> = https_transport(),
                     std::shared_ptr<CredentialStore> = shared_credentials());
    ~Service(); // Cancel + join on HOST shutdown worker, never on Game Thread.
    Service(const Service&) = delete;
    Service& operator=(const Service&) = delete;
    Operation submit(Request); // Immediate; poll future with wait_for(0) from future adapter.
    [[nodiscard]] std::string route_model(std::string_view route) const;
    void shutdown() noexcept; // Nonblocking cancellation; rejects further submissions.
private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
};
}
