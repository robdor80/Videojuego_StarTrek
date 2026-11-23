#pragma once

#include "CoreMinimal.h"
#include "Async/Future.h"
#include "Modules/ModuleManager.h"
#include "HostAcademyExports.h"

struct FHostApi
{
    ~FHostApi();

    void* Bridge = nullptr;
    void* Host = nullptr;
    FHostAcademyApi Academy;
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
    TSharedPtr<const FHostApi, ESPMode::ThreadSafe> GetHostApi() const { return Api; }
    static void RetireClient(TSharedPtr<const FHostApi, ESPMode::ThreadSafe> Api,
                             TrekHostClient* Client, TFuture<TrekHostClient*> Creating);

    virtual bool SupportsDynamicReloading() override { return false; }
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;

private:
    TSharedPtr<const FHostApi, ESPMode::ThreadSafe> Api;
};

const TCHAR* HostCodeName(TrekHostCode Code);
const TCHAR* HostStateName(uint32 State);
