#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"
#include "HAL/PlatformProcess.h"
#include "Misc/Paths.h"
#include "f05_orders.h"
#include "f05_core_revision.h"
namespace {void* Bridge=nullptr;bool Ready=false;}
bool F05BridgeReady(){return Ready;}
class FF05OrdersLabModule : public FDefaultGameModuleImpl {
 virtual void StartupModule() override {
  Bridge=FPlatformProcess::GetDllHandle(*FPaths::Combine(FPaths::ProjectDir(),TEXT("Binaries/Win64/TrekF04Bridge.dll")));
  if(Bridge && FPlatformProcess::GetDllExport(Bridge,TEXT("f05_submit")) && FPlatformProcess::GetDllExport(Bridge,TEXT("f04_core_sha")) && FPlatformProcess::GetDllExport(Bridge,TEXT("f05_delegate")) && FPlatformProcess::GetDllExport(Bridge,TEXT("f05_evaluate")) && FPlatformProcess::GetDllExport(Bridge,TEXT("f05_ai_finish")) && FPlatformProcess::GetDllExport(Bridge,TEXT("f05_ai_apply")))
   Ready=FCStringAnsi::Strcmp(f04_core_sha(),F05_EXPECTED_CORE_SHA)==0;
  UE_LOG(LogTemp,Display,TEXT("F05 P01/P02/P03/P04 bridge ready=%d Core=%s"),Ready,ANSI_TO_TCHAR(F05_EXPECTED_CORE_SHA));
 }
 virtual void ShutdownModule() override {Ready=false;if(Bridge)FPlatformProcess::FreeDllHandle(Bridge);Bridge=nullptr;}
};
IMPLEMENT_PRIMARY_GAME_MODULE(FF05OrdersLabModule,F05OrdersLab,"F05OrdersLab");
