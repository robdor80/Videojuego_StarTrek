#include "F02CampaignSubsystem.h"
#include "Modules/ModuleManager.h"
#include "HAL/PlatformProcess.h"
#include "Misc/Paths.h"

namespace { void* BridgeHandle=nullptr; bool Ready=false; }
bool F02BridgeReady() { return Ready; }
class FF02CoreLabModule : public FDefaultGameModuleImpl {
    virtual void StartupModule() override {
        const FString Path=FPaths::Combine(FPaths::ProjectDir(),TEXT("Binaries/Win64/TrekF02Bridge.dll"));
        BridgeHandle=FPlatformProcess::GetDllHandle(*Path);
        if (!BridgeHandle) { UE_LOG(LogTemp,Error,TEXT("F02: missing native bridge %s"),*Path); return; }
        // Check exports before calling an unrecognized DLL through its import table.
        if (!FPlatformProcess::GetDllExport(BridgeHandle,TEXT("f02_abi_version")) ||
            !FPlatformProcess::GetDllExport(BridgeHandle,TEXT("f02_core_sha"))) return;
        Ready=f02_abi_version()==1 && FCStringAnsi::Strcmp(f02_core_sha(),
            "4f282863737bcd8f5add401202a9e1064c133672")==0;
        UE_LOG(LogTemp,Display,TEXT("F02 bridge compatible=%d; Core SHA=%s"),Ready,ANSI_TO_TCHAR(f02_core_sha()));
    }
    virtual void ShutdownModule() override {
        Ready=false;
        if (BridgeHandle) FPlatformProcess::FreeDllHandle(BridgeHandle);
        BridgeHandle=nullptr;
    }
};
IMPLEMENT_PRIMARY_GAME_MODULE(FF02CoreLabModule,F02CoreLab,"F02CoreLab");
