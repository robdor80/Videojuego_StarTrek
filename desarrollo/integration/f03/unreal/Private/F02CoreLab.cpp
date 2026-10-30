#include "F02CampaignSubsystem.h"
#include "F03CampaignSubsystem.h"
#include "f03_core_revision.h"
#include "Modules/ModuleManager.h"
#include "HAL/PlatformProcess.h"
#include "Misc/Paths.h"
namespace { void* F02Handle=nullptr; void* F03Handle=nullptr; bool Ready2=false,Ready3=false; }
bool F02BridgeReady() { return Ready2; }
bool F03BridgeReady() { return Ready3; }
class FF02CoreLabModule : public FDefaultGameModuleImpl {
    virtual void StartupModule() override {
        F02Handle=FPlatformProcess::GetDllHandle(*FPaths::Combine(FPaths::ProjectDir(),TEXT("Binaries/Win64/TrekF02Bridge.dll")));
        F03Handle=FPlatformProcess::GetDllHandle(*FPaths::Combine(FPaths::ProjectDir(),TEXT("Binaries/Win64/TrekF03Bridge.dll")));
        if(F02Handle && FPlatformProcess::GetDllExport(F02Handle,TEXT("f02_abi_version")) &&
            FPlatformProcess::GetDllExport(F02Handle,TEXT("f02_core_sha")))
            Ready2=f02_abi_version()==1 && FCStringAnsi::Strcmp(f02_core_sha(),"4f282863737bcd8f5add401202a9e1064c133672")==0;
        if(F03Handle && FPlatformProcess::GetDllExport(F03Handle,TEXT("f03_abi_version")) &&
            FPlatformProcess::GetDllExport(F03Handle,TEXT("f03_core_sha")))
            Ready3=f03_abi_version()==1 && FCStringAnsi::Strcmp(f03_core_sha(),F03_EXPECTED_CORE_SHA)==0;
        UE_LOG(LogTemp,Display,TEXT("F03 module Core compatible=%d expected=%s; F02 regression compatible=%d"),Ready3,ANSI_TO_TCHAR(F03_EXPECTED_CORE_SHA),Ready2);
    }
    virtual void ShutdownModule() override {
        Ready2=Ready3=false;
        if(F02Handle) FPlatformProcess::FreeDllHandle(F02Handle); if(F03Handle) FPlatformProcess::FreeDllHandle(F03Handle);
        F02Handle=F03Handle=nullptr;
    }
};
IMPLEMENT_PRIMARY_GAME_MODULE(FF02CoreLabModule,F02CoreLab,"F02CoreLab");
