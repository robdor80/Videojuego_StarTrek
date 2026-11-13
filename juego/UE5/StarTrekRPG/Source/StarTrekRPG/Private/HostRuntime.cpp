#include "HostRuntime.h"

#include "Async/Async.h"
#include "HAL/PlatformProcess.h"
#include "Misc/Paths.h"
#include "Modules/ModuleManager.h"

DEFINE_LOG_CATEGORY_STATIC(LogStarTrekHost, Log, All);

namespace
{
static_assert(sizeof(TrekHostRequest) == 80 && sizeof(TrekHostCompletion) == 120);
static_assert(sizeof(TrekHostStatus) == 24 && STRUCT_OFFSET(TrekHostCompletion, output) == 72);

template <typename T>
T Resolve(void* Dll, const TCHAR* Name)
{
    return reinterpret_cast<T>(FPlatformProcess::GetDllExport(Dll, Name));
}
}

FStarTrekRPGModule& FStarTrekRPGModule::Get()
{
    return FModuleManager::GetModuleChecked<FStarTrekRPGModule>(TEXT("StarTrekRPG"));
}

void FStarTrekRPGModule::StartupModule()
{
    const FString Dir = FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectDir(), TEXT("Binaries/Win64")));
    Bridge = FPlatformProcess::GetDllHandle(*FPaths::Combine(Dir, TEXT("TrekF04Bridge.dll")));
    if (Bridge)
    {
        Host = FPlatformProcess::GetDllHandle(*FPaths::Combine(Dir, TEXT("TrekHost.dll")));
    }
    if (Host)
    {
        const auto Version = Resolve<decltype(&trek_host_abi_version)>(Host, TEXT("trek_host_abi_version"));
        Api.Create = Resolve<decltype(Api.Create)>(Host, TEXT("trek_host_create"));
        Api.Destroy = Resolve<decltype(Api.Destroy)>(Host, TEXT("trek_host_destroy"));
        Api.Status = Resolve<decltype(Api.Status)>(Host, TEXT("trek_host_status"));
        Api.Submit = Resolve<decltype(Api.Submit)>(Host, TEXT("trek_host_submit"));
        Api.Poll = Resolve<decltype(Api.Poll)>(Host, TEXT("trek_host_poll"));
        Api.Discard = Resolve<decltype(Api.Discard)>(Host, TEXT("trek_host_discard"));
        if (Version && Version() == TREK_HOST_ABI_VERSION && Api.Create && Api.Destroy &&
            Api.Status && Api.Submit && Api.Poll && Api.Discard)
        {
            UE_LOG(LogStarTrekHost, Display, TEXT("H06 HOST ABI %u loaded with TrekF04Bridge"), Version());
            return;
        }
    }
    ShutdownModule();
    UE_LOG(LogStarTrekHost, Warning, TEXT("HOST unavailable: prepare the Win64 Release libraries and ABI v1."));
}

void FStarTrekRPGModule::RetireClient(TrekHostClient* Client)
{
    check(IsInGameThread() && Client && Api.Destroy);
    Retiring.RemoveAllSwap([](const TFuture<void>& Task) { return Task.IsReady(); });
    const auto Destroy = Api.Destroy;
    Retiring.Add(Async(EAsyncExecution::Thread, [Destroy, Client]() { Destroy(Client); }));
}

void FStarTrekRPGModule::ShutdownModule()
{
    // Final DLL unload barrier. GameInstance and world teardown never join.
    for (TFuture<void>& Task : Retiring)
    {
        Task.Wait();
    }
    Retiring.Reset();
    Api = {};
    if (Host)
    {
        FPlatformProcess::FreeDllHandle(Host);
        Host = nullptr;
    }
    if (Bridge)
    {
        FPlatformProcess::FreeDllHandle(Bridge);
        Bridge = nullptr;
    }
}

const TCHAR* HostCodeName(TrekHostCode Code)
{
    switch (Code)
    {
    case TREK_HOST_OK: return TEXT("OK");
    case TREK_HOST_INVALID_ARGUMENT: return TEXT("INVALID_ARGUMENT");
    case TREK_HOST_SESSION_CLOSED: return TEXT("SESSION_CLOSED");
    case TREK_HOST_BUSY_STATE: return TEXT("BUSY_STATE");
    case TREK_HOST_WRONG_THREAD: return TEXT("WRONG_THREAD");
    case TREK_HOST_GENERATION_EXPIRED: return TEXT("GENERATION_EXPIRED");
    case TREK_HOST_CAPACITY_LIMIT: return TEXT("CAPACITY_LIMIT");
    case TREK_HOST_DOMAIN_REJECTED: return TEXT("DOMAIN_REJECTED");
    case TREK_HOST_INTERNAL_ERROR: return TEXT("INTERNAL_ERROR");
    case TREK_HOST_PRINCIPAL_UNBOUND: return TEXT("PRINCIPAL_UNBOUND");
    case TREK_HOST_ACCESS_DENIED: return TEXT("ACCESS_DENIED");
    case TREK_HOST_SCOPE_INVALID: return TEXT("SCOPE_INVALID");
    case TREK_HOST_REVISION_STALE: return TEXT("REVISION_STALE");
    case TREK_HOST_IDEMPOTENCY_CONFLICT: return TEXT("IDEMPOTENCY_CONFLICT");
    case TREK_HOST_SAVE_INCOMPATIBLE: return TEXT("SAVE_INCOMPATIBLE");
    case TREK_HOST_SAVE_UNTRUSTED: return TEXT("SAVE_UNTRUSTED");
    case TREK_HOST_PERSISTENCE_FAILED: return TEXT("PERSISTENCE_FAILED");
    case TREK_HOST_PUBLICATION_UNCERTAIN: return TEXT("PUBLICATION_UNCERTAIN");
    case TREK_HOST_SAVE_CORRUPT: return TEXT("SAVE_CORRUPT");
    case TREK_HOST_IDENTITY_MISMATCH: return TEXT("IDENTITY_MISMATCH");
    case TREK_HOST_PATH_REJECTED: return TEXT("PATH_REJECTED");
    case TREK_HOST_SERVICE_UNAVAILABLE: return TEXT("SERVICE_UNAVAILABLE");
    case TREK_HOST_ABI_MISMATCH: return TEXT("ABI_MISMATCH");
    case TREK_HOST_RETRY: return TEXT("RETRY");
    case TREK_HOST_PENDING: return TEXT("PENDING");
    case TREK_HOST_UNKNOWN_TICKET: return TEXT("UNKNOWN_TICKET");
    default: return TEXT("UNKNOWN_ERROR");
    }
}

const TCHAR* HostStateName(uint32 State)
{
    switch (State)
    {
    case TREK_HOST_CLOSED: return TEXT("CLOSED");
    case TREK_HOST_OPENING: return TEXT("OPENING");
    case TREK_HOST_ACTIVE: return TEXT("ACTIVE");
    case TREK_HOST_SAVING: return TEXT("SAVING");
    case TREK_HOST_LOADING: return TEXT("LOADING");
    case TREK_HOST_FAILED: return TEXT("FAILED");
    case TREK_HOST_FAILED_RECOVERABLE: return TEXT("FAILED_RECOVERABLE");
    case TREK_HOST_CLOSING: return TEXT("CLOSING");
    default: return TEXT("UNKNOWN");
    }
}

IMPLEMENT_PRIMARY_GAME_MODULE(FStarTrekRPGModule, StarTrekRPG, "StarTrekRPG");
