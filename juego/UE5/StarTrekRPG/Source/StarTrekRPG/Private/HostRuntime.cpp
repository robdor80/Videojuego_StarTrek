#include "HostRuntime.h"

#include "Async/Async.h"
#include "HAL/PlatformProcess.h"
#include "Misc/Paths.h"
#include "Modules/ModuleManager.h"
#include "Windows/WindowsHWrapper.h"

DEFINE_LOG_CATEGORY_STATIC(LogStarTrekHost, Log, All);

namespace
{
static_assert(sizeof(TrekHostRequest) == 80 && sizeof(TrekHostCompletion) == 120);
static_assert(sizeof(TrekHostStatus) == 24 && STRUCT_OFFSET(TrekHostCompletion, output) == 72);
static_assert(TREK_HOST_ACADEMY_VERSION == 2 && sizeof(TrekHostAcademyRequest) == 48);
static_assert(sizeof(TrekHostAcademyView) == 240 && sizeof(TrekHostSlotMetadata) == 104);
static_assert(sizeof(TrekHostAcademyCompletion) == 6696 && STRUCT_OFFSET(TrekHostAcademyCompletion, output) == 32);

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

FHostApi::~FHostApi()
{
    if (Host)
    {
        FPlatformProcess::FreeDllHandle(Host);
    }
    if (Bridge)
    {
        FPlatformProcess::FreeDllHandle(Bridge);
    }
}

void FStarTrekRPGModule::StartupModule()
{
    const FString Dir = FPaths::ConvertRelativePathToFull(FPaths::Combine(FPaths::ProjectDir(), TEXT("Binaries/Win64")));
    auto Loaded = MakeShared<FHostApi, ESPMode::ThreadSafe>();
    Loaded->Bridge = FPlatformProcess::GetDllHandle(*FPaths::Combine(Dir, TEXT("TrekF04Bridge.dll")));
    if (Loaded->Bridge)
    {
        Loaded->Host = FPlatformProcess::GetDllHandle(*FPaths::Combine(Dir, TEXT("TrekHost.dll")));
    }
    if (void* Host = Loaded->Host)
    {
        const auto Version = Resolve<decltype(&trek_host_abi_version)>(Host, TEXT("trek_host_abi_version"));
        Loaded->Create = Resolve<decltype(Loaded->Create)>(Host, TEXT("trek_host_create"));
        Loaded->Destroy = Resolve<decltype(Loaded->Destroy)>(Host, TEXT("trek_host_destroy"));
        Loaded->Status = Resolve<decltype(Loaded->Status)>(Host, TEXT("trek_host_status"));
        Loaded->Submit = Resolve<decltype(Loaded->Submit)>(Host, TEXT("trek_host_submit"));
        Loaded->Poll = Resolve<decltype(Loaded->Poll)>(Host, TEXT("trek_host_poll"));
        Loaded->Discard = Resolve<decltype(Loaded->Discard)>(Host, TEXT("trek_host_discard"));
        if (Version && Version() == TREK_HOST_ABI_VERSION && Loaded->Create && Loaded->Destroy &&
            Loaded->Status && Loaded->Submit && Loaded->Poll && Loaded->Discard)
        {
            // A retirement task can outlive ShutdownModule. Keep the code of
            // its callable resident even in the modular Win64 Editor.
            HMODULE CodeModule = nullptr;
            if (!::GetModuleHandleExW(GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS | GET_MODULE_HANDLE_EX_FLAG_PIN,
                                     reinterpret_cast<LPCWSTR>(&LogStarTrekHost), &CodeModule))
            {
                UE_LOG(LogStarTrekHost, Error, TEXT("HOST unavailable: could not retain the game module during teardown."));
                return;
            }
            Loaded->Academy = FHostAcademyApi::Negotiate([Host](const char* Name)
            {
                return FPlatformProcess::GetDllExport(Host, ANSI_TO_TCHAR(Name));
            });
            UE_LOG(LogStarTrekHost, Display, TEXT("H06 HOST ABI %u loaded with TrekF04Bridge; Academy v%u: %s"),
                TREK_HOST_ABI_VERSION, TREK_HOST_ACADEMY_VERSION, HostCodeName(Loaded->Academy.Availability));
            Api = Loaded;
            return;
        }
    }
    UE_LOG(LogStarTrekHost, Warning, TEXT("HOST unavailable: prepare the Win64 Release libraries and ABI v1."));
}

void FStarTrekRPGModule::RetireClient(TSharedPtr<const FHostApi, ESPMode::ThreadSafe> Api,
                                    TrekHostClient* Client, TFuture<TrekHostClient*> Creating)
{
    check(IsInGameThread() && Api && (Client || Creating.IsValid()));
    Async(EAsyncExecution::Thread, [Api = MoveTemp(Api), Client, Creating = MoveTemp(Creating)]() mutable
    {
        TrekHostClient* Retiring = Client ? Client : Creating.Get();
        if (Retiring)
        {
            Api->Destroy(Retiring);
        }
    });
}

void FStarTrekRPGModule::ShutdownModule()
{
    // Active clients and retirement tasks retain both DLLs. Their last
    // reference releases the libraries only after native destruction returns.
    Api.Reset();
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
