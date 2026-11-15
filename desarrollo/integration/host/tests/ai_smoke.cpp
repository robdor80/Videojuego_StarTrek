#include <trek/host/ai/service.h>
#include <cstdlib>
#include <iostream>
using namespace trek::host::ai;
int main(int argc, char** argv) {
    if (argc != 2 || std::string_view(argv[1]) != "--live-openai" ) return 2;
    const char* key = std::getenv("OPENAI_API_KEY");
    if (!key || !*key) { std::cout << "MISSING_KEY (no call)\n"; return 3; }
    // This smoke deliberately uses the environment rather than the Windows shared entry.
    struct Environment final : CredentialStore {
        Error read(std::string& out) override { out = std::getenv("OPENAI_API_KEY"); return Error::OK; }
        Error write(std::string_view) override { return Error::UNSUPPORTED_PLATFORM; }
    };
    Config config; config.max_calls = 1; config.max_output_tokens = 128;
    Service service(config, https_transport(), std::make_shared<Environment>());
    Request request;
    request.instructions = "Return the JSON object with ok equal to true. Technical connectivity test.";
    request.input = "Test";
    request.json_schema = R"({"type":"object","properties":{"ok":{"type":"boolean","enum":[true]}},"required":["ok"],"additionalProperties":false})";
    auto operation = service.submit(std::move(request));
    const auto result = operation.result.get(); // Console smoke only, never Unreal Game Thread.
    std::cout << diagnostic(result.error) << " HTTP=" << result.http_status << '\n';
    return result.error == Error::OK ? 0 : 1;
}
