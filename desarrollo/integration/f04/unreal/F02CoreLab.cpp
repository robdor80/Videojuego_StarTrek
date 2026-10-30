#include "F02CampaignSubsystem.h"
#include "F03CampaignSubsystem.h"
#include "F04CampaignSubsystem.h"
#include "f03_core_revision.h"
#include "f04_core_revision.h"
#include "Modules/ModuleManager.h"
#include "HAL/PlatformProcess.h"
#include "Misc/Paths.h"
namespace { void* H2=nullptr;void* H3=nullptr;void* H4=nullptr;bool R2=false,R3=false,R4=false; }
bool F02BridgeReady(){return R2;}bool F03BridgeReady(){return R3;}bool F04BridgeReady(){return R4;}
class FF02CoreLabModule:public FDefaultGameModuleImpl {
 virtual void StartupModule()override{
  auto Load=[](const TCHAR* Name){return FPlatformProcess::GetDllHandle(*FPaths::Combine(FPaths::ProjectDir(),TEXT("Binaries/Win64"),Name));};
  H2=Load(TEXT("TrekF02Bridge.dll"));H3=Load(TEXT("TrekF03Bridge.dll"));H4=Load(TEXT("TrekF04Bridge.dll"));
  if(H2 && FPlatformProcess::GetDllExport(H2,TEXT("f02_abi_version")) && FPlatformProcess::GetDllExport(H2,TEXT("f02_core_sha")))R2=f02_abi_version()==1 && FCStringAnsi::Strcmp(f02_core_sha(),"4f282863737bcd8f5add401202a9e1064c133672")==0;
  if(H3 && FPlatformProcess::GetDllExport(H3,TEXT("f03_abi_version")) && FPlatformProcess::GetDllExport(H3,TEXT("f03_core_sha")))R3=f03_abi_version()==1 && FCStringAnsi::Strcmp(f03_core_sha(),F03_EXPECTED_CORE_SHA)==0;
  if(H4 && FPlatformProcess::GetDllExport(H4,TEXT("f04_create")) && FPlatformProcess::GetDllExport(H4,TEXT("f04_core_sha")))R4=FCStringAnsi::Strcmp(f04_core_sha(),F04_EXPECTED_CORE_SHA)==0;
  UE_LOG(LogTemp,Display,TEXT("F04 isolated lab compatible F02=%d F03=%d F04=%d Core=%s"),R2,R3,R4,ANSI_TO_TCHAR(F04_EXPECTED_CORE_SHA));
 }
 virtual void ShutdownModule()override{R2=R3=R4=false;for(void* H:{H2,H3,H4})if(H)FPlatformProcess::FreeDllHandle(H);H2=H3=H4=nullptr;}
};
IMPLEMENT_PRIMARY_GAME_MODULE(FF02CoreLabModule,F02CoreLab,"F02CoreLab");
