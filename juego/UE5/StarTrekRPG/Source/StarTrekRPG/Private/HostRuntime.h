#pragma once

#include "CoreMinimal.h"
#include "Async/Future.h"
#include "Modules/ModuleManager.h"
#include "trek/host/host_abi.h"

struct FHostApi
{
    decltype(&trek_host_create) Create = nullptr;
    decltype(&trek_host_destroy) Destroy = nullptr;
    decltype(&trek_host_status) Status = nullptr;
    decltype(&trek_host_submit) Submit = nullptr;
    decltype(&trek_host_poll) Poll = nullptr;
    decltype(&trek_host_discard) Discard = nullptr;
};

class FStarTrekRPGModule final : public FDefaultGameModuleImpl
{
public:
    static FStarTrekRPGModule& Get();
    const FHostApi* GetHostApi() const { return Host ? &Api : nullptr; }
    void RetireClient(TrekHostClient* Client);

    virtual bool SupportsDynamicReloading() override { return false; }
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;

private:
    FHostApi Api;
    void* Bridge = nullptr;
    void* Host = nullptr;
    TArray<TFuture<void>> Retiring;
};

const TCHAR* HostCodeName(TrekHostCode Code);
const TCHAR* HostStateName(uint32 State);
