#include <trek/host/ai/service.h>
#include <cstdlib>
#include <algorithm>
#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#include <wincred.h>
#endif
namespace trek::host::ai {
namespace {
bool valid_key(std::string_view key) {
    return !key.empty() && key.size() <= 2048 &&
        std::all_of(key.begin(), key.end(), [](unsigned char c) { return c > 32 && c < 127; });
}
class Shared final : public CredentialStore {
public:
    Error read(std::string& key) override {
        key.clear();
#ifdef _WIN32
        PCREDENTIALW credential{};
        if (!CredReadW(L"PersonalRPG/OpenAI/APIKey/v1", CRED_TYPE_GENERIC, 0, &credential))
            return GetLastError() == ERROR_NOT_FOUND ? Error::MISSING_KEY : Error::CREDENTIAL_STORAGE;
        key.assign(reinterpret_cast<char*>(credential->CredentialBlob), credential->CredentialBlobSize);
        SecureZeroMemory(credential->CredentialBlob, credential->CredentialBlobSize);
        CredFree(credential);
        if (!valid_key(key)) { key.clear(); return Error::INVALID_CREDENTIAL; }
        return Error::OK;
#else
        return Error::UNSUPPORTED_PLATFORM;
#endif
    }
    Error write(std::string_view key) override {
        if (!valid_key(key)) return Error::INVALID_CREDENTIAL;
#ifdef _WIN32
        CREDENTIALW credential{};
        credential.Type = CRED_TYPE_GENERIC;
        credential.TargetName = const_cast<wchar_t*>(L"PersonalRPG/OpenAI/APIKey/v1");
        credential.CredentialBlobSize = static_cast<DWORD>(key.size());
        credential.CredentialBlob = reinterpret_cast<LPBYTE>(const_cast<char*>(key.data()));
        credential.Persist = CRED_PERSIST_LOCAL_MACHINE; // Same Windows user, across logons/apps.
        credential.UserName = const_cast<wchar_t*>(L"OpenAI");
        return CredWriteW(&credential, 0) ? Error::OK : Error::CREDENTIAL_STORAGE;
#else
        return Error::UNSUPPORTED_PLATFORM;
#endif
    }
};
}
std::shared_ptr<CredentialStore> shared_credentials() { return std::make_shared<Shared>(); }
CredentialStatus credential_status(CredentialStore& store) noexcept {
    CredentialStatus result;
    try {
        std::string key;
        result.storage_error = store.read(key);
        result.shared = result.storage_error == Error::OK && valid_key(key);
        const char* env = std::getenv("OPENAI_API_KEY");
        result.environment = env && valid_key(env);
    } catch (...) { result.storage_error = Error::CREDENTIAL_STORAGE; }
    return result;
}
Error register_key(CredentialStore& store, std::string_view key) noexcept {
    if (!valid_key(key)) return Error::INVALID_CREDENTIAL;
    try { return store.write(key); } catch (...) { return Error::CREDENTIAL_STORAGE; }
}
Error import_environment_key(CredentialStore& store) noexcept {
    const char* key = std::getenv("OPENAI_API_KEY");
    return key && *key ? register_key(store, key) : Error::MISSING_KEY;
}
}
