#include "F02CampaignSubsystem.h"
#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "HAL/FileManager.h"
#include "Misc/Paths.h"
#include "Async/Async.h"

namespace {
struct FLab {
    UWorld* World=nullptr;
    UGameInstance* Game=nullptr;
    UF02CampaignSubsystem* Host=nullptr;
    FLab() {
        const auto Values=UWorld::InitializationValues().AllowAudioPlayback(false)
            .RequiresHitProxies(false).CreatePhysicsScene(false).CreateNavigation(false)
            .CreateAISystem(false).ShouldSimulatePhysics(false).SetTransactional(false);
        World=UWorld::CreateWorld(EWorldType::Game,false,NAME_None,nullptr,true,
            ERHIFeatureLevel::Num,&Values);
        Game=NewObject<UGameInstance>(); Game->AddToRoot();
        Host=NewObject<UF02CampaignSubsystem>(Game); Host->AddToRoot(); Host->OpenLab();
    }
    ~FLab() {
        Host->CloseLab(); Host->RemoveFromRoot();
        World->DestroyWorld(false); Game->RemoveFromRoot();
    }
};
constexpr auto Flags=EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF02ActorLifecycle,"F02.Core.ActorLifecycle",Flags)
bool FF02ActorLifecycle::RunTest(const FString&) {
    FLab Lab;
    TestTrue(TEXT("Core ready"),Lab.Host->Exists());
    const FString Id=Lab.Host->DiagnosticId();
    auto* First=Lab.Host->Represent(Lab.World);
    if (!TestNotNull(TEXT("First real Actor"),First)) return false;
    TestEqual(TEXT("Logical identifier displayed"),First->LogicalId,Id);
    TestTrue(TEXT("Repeated representation does not duplicate Actor"),First==Lab.Host->Represent(Lab.World));
    TestTrue(TEXT("Destroy Actor"),First->Destroy());
    TestTrue(TEXT("Core survives Actor destruction"),Lab.Host->Exists());
    auto* Second=Lab.Host->Represent(Lab.World);
    if (!TestNotNull(TEXT("Recreated Actor"),Second)) return false;
    TestTrue(TEXT("Different visual object"),Second!=First);
    TestEqual(TEXT("Same logical identity"),Second->LogicalId,Id);
    TestTrue(TEXT("Core action"),Lab.Host->Place());
    const FString Dir=FPaths::Combine(FPaths::ProjectSavedDir(),TEXT("F02Evidence"));
    IFileManager::Get().MakeDirectory(*Dir,true);
    const FString Path=FPaths::Combine(Dir,FGuid::NewGuid().ToString()+TEXT(".save"));
    if (!TestTrue(TEXT("Real disk save"),Lab.Host->WriteSave(Path))) return false;
    TestFalse(TEXT("Existing save is never overwritten"),Lab.Host->WriteSave(Path));
    if (!TestTrue(TEXT("Real disk load"),Lab.Host->ReadSave(Path))) return false;
    TestFalse(TEXT("Old visual binding invalidated"),IsValid(Second));
    auto* Third=Lab.Host->Represent(Lab.World);
    if (!TestNotNull(TEXT("Actor after load"),Third)) return false;
    TestEqual(TEXT("Identity after load"),Third->LogicalId,Id);
    Third->Destroy(); TestTrue(TEXT("Entity after second unload"),Lab.Host->Exists());
    auto* Fourth=Lab.Host->Represent(Lab.World);
    if (!TestNotNull(TEXT("Actor recreated after load"),Fourth)) return false;
    TestEqual(TEXT("Identity after load and recreation"),Fourth->LogicalId,Id);
    UE_LOG(LogTemp,Display,TEXT("F02 EVIDENCE ActorLifecycle: EntityId=%s destroy/recreate/disk/reload passed"),*Id);
    return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF02CorruptLoad,"F02.Core.CorruptLoad",Flags)
bool FF02CorruptLoad::RunTest(const FString&) {
    FLab Lab; TestTrue(TEXT("Place"),Lab.Host->Place());
    auto* Actor=Lab.Host->Represent(Lab.World); TArray<uint8> Before,After;
    if (!TestTrue(TEXT("Capture"),Lab.Host->Save(Before)) || Before.IsEmpty()) return false;
    auto Bad=Before; Bad[Bad.Num()/2]^=0x7f;
    TestFalse(TEXT("Corrupt save rejected"),Lab.Host->Load(Bad));
    TestTrue(TEXT("Actor preserved"),IsValid(Actor) && Actor==Lab.Host->Represent(Lab.World));
    TestTrue(TEXT("Capture after rejection"),Lab.Host->Save(After));
    TestTrue(TEXT("World and RNG byte-identical"),Before==After);
    return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF02Projection,"F02.Core.Projection",Flags)
bool FF02Projection::RunTest(const FString&) {
    FLab Lab; TArray<uint8> Before,After;
    TestTrue(TEXT("Save"),Lab.Host->Save(Before));
    TestTrue(TEXT("ObserverView hides fixture secret"),Lab.Host->VerifyProjection());
    TestTrue(TEXT("Save after projection"),Lab.Host->Save(After));
    TestTrue(TEXT("Read-only projection"),Before==After); return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF02HostRecovery,"F02.Core.HostRecovery",Flags)
bool FF02HostRecovery::RunTest(const FString&) {
    FLab Lab; TestTrue(TEXT("Place"),Lab.Host->Place());
    auto* Actor=Lab.Host->Represent(Lab.World); const auto Id=Lab.Host->DiagnosticId();
    TArray<uint8> Saved; if (!TestTrue(TEXT("Save"),Lab.Host->Save(Saved))) return false;
    Lab.Host->CloseLab(); TestFalse(TEXT("Closed Host fails safely"),Lab.Host->Exists());
    TestFalse(TEXT("Closed Host cannot represent"),Lab.Host->Represent(Lab.World)!=nullptr);
    TestFalse(TEXT("Stale Actor removed"),IsValid(Actor));
    TestTrue(TEXT("New session"),Lab.Host->OpenLab()); TestTrue(TEXT("Restore"),Lab.Host->Load(Saved));
    auto* Recovered=Lab.Host->Represent(Lab.World);
    if (TestNotNull(TEXT("Recovered Actor"),Recovered)) TestEqual(TEXT("Recovered identity"),Recovered->LogicalId,Id);
    return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF02Thread,"F02.Core.ThreadAffinity",Flags)
bool FF02Thread::RunTest(const FString&) {
    FLab Lab; TArray<uint8> Before,After; TestTrue(TEXT("Save"),Lab.Host->Save(Before));
    const bool Rejected=Async(EAsyncExecution::Thread,[Host=Lab.Host]() {
        TArray<uint8> Bytes;
        return !Host->Exists() && !Host->Place() && !Host->Save(Bytes) && !Host->OpenLab();
    }).Get();
    TestTrue(TEXT("Worker cannot access campaign"),Rejected);
    TestTrue(TEXT("Save after worker"),Lab.Host->Save(After));
    TestTrue(TEXT("No side effects"),Before==After); return true;
}
#endif
