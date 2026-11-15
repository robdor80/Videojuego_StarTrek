#include <trek/host/ai/service.h>
#include <algorithm>
#include <array>
#include <condition_variable>
#include <mutex>
#include <limits>
#include <thread>
#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#include <winhttp.h>
#else
#include <curl/curl.h>
#endif
namespace trek::host::ai {
namespace {
using Clock = std::chrono::steady_clock;
#ifdef _WIN32
struct Handle {
    HINTERNET value{};
    ~Handle() { if (value) WinHttpCloseHandle(value); }
};
// All WinHTTP calls and handle closure belong to the HOST worker. Pending IO is
// asynchronous; context/buffer stay alive through the final HANDLE_CLOSING callback.
struct AsyncRequest {
    HINTERNET handle{};
    std::mutex mutex;
    std::condition_variable changed;
    DWORD event{}, error{}, transferred{};
    bool registered{}, closing{};
    std::array<char, 4096> buffer{};
    static void CALLBACK callback(HINTERNET, DWORD_PTR context, DWORD status, void* info, DWORD length) noexcept {
        if (!context) return;
        auto& self = *reinterpret_cast<AsyncRequest*>(context);
        std::lock_guard lock(self.mutex);
        switch (status) {
        case WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE:
        case WINHTTP_CALLBACK_STATUS_HEADERS_AVAILABLE:
            self.event = status; break;
        case WINHTTP_CALLBACK_STATUS_READ_COMPLETE:
            self.transferred = length; self.event = status; break;
        case WINHTTP_CALLBACK_STATUS_REQUEST_ERROR:
            self.error = static_cast<WINHTTP_ASYNC_RESULT*>(info)->dwError; break;
        case WINHTTP_CALLBACK_STATUS_HANDLE_CLOSING:
            self.closing = true; break;
        default: return;
        }
        self.changed.notify_all();
    }
    Error initialize() {
        DWORD_PTR context = reinterpret_cast<DWORD_PTR>(this);
        if (!WinHttpSetOption(handle, WINHTTP_OPTION_CONTEXT_VALUE, &context, sizeof(context))) return Error::CONNECTION;
        registered = WinHttpSetStatusCallback(handle, callback,
            WINHTTP_CALLBACK_FLAG_ALL_COMPLETIONS | WINHTTP_CALLBACK_FLAG_HANDLES, 0) != WINHTTP_INVALID_STATUS_CALLBACK;
        return registered ? Error::OK : Error::CONNECTION;
    }
    Error wait(DWORD expected, Clock::time_point deadline, std::stop_token stop) {
        std::unique_lock lock(mutex);
        while (event != expected && !error && !stop.stop_requested() && Clock::now() < deadline)
            changed.wait_until(lock, std::min(deadline, Clock::now() + std::chrono::milliseconds(10)));
        if (stop.stop_requested()) return Error::CANCELLED;
        if (Clock::now() >= deadline || error == ERROR_WINHTTP_TIMEOUT) return Error::TIMEOUT;
        if (error) return Error::CONNECTION;
        event = 0;
        return Error::OK;
    }
    ~AsyncRequest() {
        if (!handle) return;
        WinHttpCloseHandle(handle);
        if (registered) {
            std::unique_lock lock(mutex);
            changed.wait(lock, [this] { return closing; });
        }
    }
};
bool accepted(BOOL result) { return result || GetLastError() == ERROR_IO_PENDING; }
#else
struct CurlState {
    std::string body;
    std::size_t limit;
    Clock::time_point deadline;
    std::stop_token stop;
    bool oversized{};
};
size_t receive(char* data, size_t size, size_t count, void* context) noexcept {
    auto& state = *static_cast<CurlState*>(context);
    if (size && count > std::numeric_limits<size_t>::max() / size) return 0;
    const auto bytes = size * count;
    if (bytes > state.limit - state.body.size()) { state.oversized = true; return 0; }
    try { state.body.append(data, bytes); return bytes; } catch (...) { return 0; }
}
int progress(void* context, curl_off_t, curl_off_t, curl_off_t, curl_off_t) noexcept {
    const auto& state = *static_cast<CurlState*>(context);
    return state.stop.stop_requested() || Clock::now() >= state.deadline;
}
#endif
class Https final : public Transport {
public:
    HttpResponse post(std::string_view body, std::string_view key, Clock::time_point deadline,
                      std::stop_token stop, std::size_t limit) override {
        if (stop.stop_requested()) return {Error::CANCELLED};
        const auto remaining = std::chrono::duration_cast<std::chrono::milliseconds>(deadline - Clock::now()).count();
        if (remaining <= 0) return {Error::TIMEOUT};
#ifdef _WIN32
        Handle session{WinHttpOpen(L"StarTrekHost/IA01", WINHTTP_ACCESS_TYPE_AUTOMATIC_PROXY,
                                  WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, WINHTTP_FLAG_ASYNC)};
        if (!session.value) return {Error::CONNECTION};
        WinHttpSetTimeouts(session.value, static_cast<int>(remaining), static_cast<int>(remaining),
                           static_cast<int>(remaining), static_cast<int>(remaining));
        Handle connection{WinHttpConnect(session.value, L"api.openai.com", INTERNET_DEFAULT_HTTPS_PORT, 0)};
        if (!connection.value) return {Error::CONNECTION};
        AsyncRequest request;
        auto raw = WinHttpOpenRequest(connection.value, L"POST", L"/v1/responses", nullptr,
                                      WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, WINHTTP_FLAG_SECURE);
        if (!raw) return {Error::CONNECTION};
        request.handle = raw;
        if (auto error = request.initialize(); error != Error::OK) return {error};
        DWORD redirect = WINHTTP_OPTION_REDIRECT_POLICY_NEVER;
        if (!WinHttpSetOption(raw, WINHTTP_OPTION_REDIRECT_POLICY, &redirect, sizeof(redirect))) return {Error::CONNECTION};
        const std::string narrow = "Content-Type: application/json\r\nAuthorization: Bearer " + std::string(key) + "\r\n";
        std::wstring headers(narrow.begin(), narrow.end());
        auto failure = [&]() -> HttpResponse {
            if (stop.stop_requested()) return {Error::CANCELLED};
            if (Clock::now() >= deadline || GetLastError() == ERROR_WINHTTP_TIMEOUT) return {Error::TIMEOUT};
            return {Error::CONNECTION};
        };
        if (!accepted(WinHttpSendRequest(raw, headers.c_str(), static_cast<DWORD>(headers.size()),
            const_cast<char*>(body.data()), static_cast<DWORD>(body.size()), static_cast<DWORD>(body.size()),
            reinterpret_cast<DWORD_PTR>(&request)))) return failure();
        if (auto e = request.wait(WINHTTP_CALLBACK_STATUS_SENDREQUEST_COMPLETE, deadline, stop); e != Error::OK) return {e};
        if (!accepted(WinHttpReceiveResponse(raw, nullptr))) return failure();
        if (auto e = request.wait(WINHTTP_CALLBACK_STATUS_HEADERS_AVAILABLE, deadline, stop); e != Error::OK) return {e};
        DWORD status{}, bytes = sizeof(status);
        if (!WinHttpQueryHeaders(raw, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
                                 WINHTTP_HEADER_NAME_BY_INDEX, &status, &bytes, WINHTTP_NO_HEADER_INDEX)) return failure();
        wchar_t content[256]{}; bytes = sizeof(content);
        if (!WinHttpQueryHeaders(raw, WINHTTP_QUERY_CONTENT_TYPE, WINHTTP_HEADER_NAME_BY_INDEX,
                                 content, &bytes, WINHTTP_NO_HEADER_INDEX)) content[0] = L'\0';
        HttpResponse result{Error::OK, static_cast<int>(status)};
        for (auto p = content; *p; ++p) result.content_type.push_back(static_cast<char>(*p));
        for (;;) {
            if (!accepted(WinHttpReadData(raw, request.buffer.data(), static_cast<DWORD>(request.buffer.size()), nullptr))) return failure();
            if (auto e = request.wait(WINHTTP_CALLBACK_STATUS_READ_COMPLETE, deadline, stop); e != Error::OK) return {e};
            const DWORD received = request.transferred;
            if (!received) break;
            if (received > limit - result.body.size()) return {Error::SIZE_LIMIT};
            result.body.append(request.buffer.data(), received);
        }
        return result;
#else
        // Initialization is process-wide and thread safe. No global cleanup while other clients may use curl.
        static const auto initialized = curl_global_init(CURL_GLOBAL_DEFAULT);
        if (initialized != CURLE_OK) return {Error::CONNECTION};
        auto curl = std::unique_ptr<CURL, decltype(&curl_easy_cleanup)>(curl_easy_init(), curl_easy_cleanup);
        if (!curl) return {Error::CONNECTION};
        CurlState state{{}, limit, deadline, stop};
        curl_slist* list = nullptr;
        list = curl_slist_append(list, "Content-Type: application/json");
        if (!list) return {Error::INTERNAL};
        const std::string auth = "Authorization: Bearer " + std::string(key);
        auto* appended = curl_slist_append(list, auth.c_str());
        if (!appended) { curl_slist_free_all(list); return {Error::INTERNAL}; }
        list = appended;
        auto headers = std::unique_ptr<curl_slist, decltype(&curl_slist_free_all)>(list, curl_slist_free_all);
        auto* c = curl.get();
        curl_easy_setopt(c, CURLOPT_URL, "https://api.openai.com/v1/responses");
        curl_easy_setopt(c, CURLOPT_HTTPHEADER, headers.get());
        curl_easy_setopt(c, CURLOPT_POST, 1L);
        curl_easy_setopt(c, CURLOPT_POSTFIELDS, body.data());
        curl_easy_setopt(c, CURLOPT_POSTFIELDSIZE_LARGE, static_cast<curl_off_t>(body.size()));
        curl_easy_setopt(c, CURLOPT_TIMEOUT_MS, static_cast<long>(remaining));
        curl_easy_setopt(c, CURLOPT_CONNECTTIMEOUT_MS, static_cast<long>(std::min<long long>(remaining, 10000)));
        curl_easy_setopt(c, CURLOPT_NOSIGNAL, 1L);
        curl_easy_setopt(c, CURLOPT_FOLLOWLOCATION, 0L);
        curl_easy_setopt(c, CURLOPT_PROTOCOLS_STR, "https");
        curl_easy_setopt(c, CURLOPT_SSL_VERIFYPEER, 1L);
        curl_easy_setopt(c, CURLOPT_SSL_VERIFYHOST, 2L);
        curl_easy_setopt(c, CURLOPT_WRITEFUNCTION, receive);
        curl_easy_setopt(c, CURLOPT_WRITEDATA, &state);
        curl_easy_setopt(c, CURLOPT_NOPROGRESS, 0L);
        curl_easy_setopt(c, CURLOPT_XFERINFOFUNCTION, progress);
        curl_easy_setopt(c, CURLOPT_XFERINFODATA, &state);
        auto code = curl_easy_perform(c);
        if (stop.stop_requested()) return {Error::CANCELLED};
        if (Clock::now() >= deadline || code == CURLE_OPERATION_TIMEDOUT) return {Error::TIMEOUT};
        if (state.oversized) return {Error::SIZE_LIMIT};
        if (code != CURLE_OK) return {Error::CONNECTION};
        long status{}; char* content{};
        curl_easy_getinfo(c, CURLINFO_RESPONSE_CODE, &status);
        curl_easy_getinfo(c, CURLINFO_CONTENT_TYPE, &content);
        return {Error::OK, static_cast<int>(status), std::move(state.body), content ? content : ""};
#endif
    }
};
}
std::shared_ptr<Transport> https_transport() { return std::make_shared<Https>(); }
}
