#include "F02CampaignSubsystem.h"
#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Engine/GameInstance.h"
#include "Engine/Engine.h"
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
        GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World);
        Game=NewObject<UGameInstance>(); Game->AddToRoot();
        World->SetGameInstance(Game);
        Host=NewObject<UF02CampaignSubsystem>(Game); Host->AddToRoot(); Host->OpenLab();
    }
    ~FLab() {
        Host->CloseLab(); Host->RemoveFromRoot();
        World->DestroyWorld(false); GEngine->DestroyWorldContext(World); Game->RemoveFromRoot();
    }
};
struct FAdditionalVisualWorld {
    UWorld* World=nullptr;
    explicit FAdditionalVisualWorld(UGameInstance* Game) {
        const auto Values=UWorld::InitializationValues().AllowAudioPlayback(false)
            .RequiresHitProxies(false).CreatePhysicsScene(false).CreateNavigation(false)
            .CreateAISystem(false).ShouldSimulatePhysics(false).SetTransactional(false);
        World=UWorld::CreateWorld(EWorldType::Game,false,NAME_None,nullptr,true,
            ERHIFeatureLevel::Num,&Values);
        GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World);
        World->SetGameInstance(Game);
    }
    ~FAdditionalVisualWorld() {
        World->DestroyWorld(false); GEngine->DestroyWorldContext(World);
    }
};
constexpr auto Flags=EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF02WorldScopedRepresentation,"F02.Core.WorldScopedRepresentation",Flags)
bool FF02WorldScopedRepresentation::RunTest(const FString&) {
    FLab Lab;
    FAdditionalVisualWorld Other(Lab.Game);
    const FString Id=Lab.Host->DiagnosticId();
    TArray<uint8> Before,After;
    if (!TestTrue(TEXT("Capture before visual overlap"),Lab.Host->Save(Before))) return false;
    auto* First=Lab.Host->Represent(Lab.World);
    auto* Second=Lab.Host->Represent(Other.World);
    if (!TestNotNull(TEXT("First world Actor"),First) ||
        !TestNotNull(TEXT("Second world Actor"),Second)) return false;
    const bool Distinct=TestTrue(TEXT("Overlapping worlds have distinct Actors"),First!=Second);
    const bool CorrectWorld=TestTrue(TEXT("Requested second world owns returned Actor"),Second->GetWorld()==Other.World);
    if (!Distinct || !CorrectWorld) return false;
    TestTrue(TEXT("First world retains its live Actor"),IsValid(First) && First->GetWorld()==Lab.World);
    TestEqual(TEXT("First world logical identity"),First->LogicalId,Id);
    TestEqual(TEXT("Second world logical identity"),Second->LogicalId,Id);
    TestTrue(TEXT("Repeated first-world request is idempotent"),Lab.Host->Represent(Lab.World)==First);
    TestTrue(TEXT("Repeated second-world request is idempotent"),Lab.Host->Represent(Other.World)==Second);
    TestTrue(TEXT("Destroy only first-world Actor"),First->Destroy());
    TestTrue(TEXT("Second-world Actor survives first-world unload"),IsValid(Second));
    auto* Recreated=Lab.Host->Represent(Lab.World);
    if (!TestNotNull(TEXT("Recreated first-world Actor"),Recreated)) return false;
    TestTrue(TEXT("Recreation belongs to requested first world"),Recreated->GetWorld()==Lab.World && Recreated!=Second);
    TestEqual(TEXT("Recreation preserves logical identity"),Recreated->LogicalId,Id);
    TestTrue(TEXT("Second world still reuses its own Actor"),Lab.Host->Represent(Other.World)==Second);
    TestTrue(TEXT("Capture after visual overlap"),Lab.Host->Save(After));
    TestTrue(TEXT("Visual lifecycle leaves Core state and RNG byte-identical"),Before==After);
    if (!TestTrue(TEXT("Restore shared logical world"),Lab.Host->Load(Before))) return false;
    TestFalse(TEXT("Restore invalidates first-world binding"),IsValid(Recreated));
    TestFalse(TEXT("Restore invalidates second-world binding"),IsValid(Second));
    auto* LoadedFirst=Lab.Host->Represent(Lab.World);
    auto* LoadedSecond=Lab.Host->Represent(Other.World);
    if (!TestNotNull(TEXT("First-world Actor after restore"),LoadedFirst) ||
        !TestNotNull(TEXT("Second-world Actor after restore"),LoadedSecond)) return false;
    TestTrue(TEXT("Restored bindings remain world-scoped"),LoadedFirst!=LoadedSecond &&
        LoadedFirst->GetWorld()==Lab.World && LoadedSecond->GetWorld()==Other.World);
    TestEqual(TEXT("First identity after restore"),LoadedFirst->LogicalId,Id);
    TestEqual(TEXT("Second identity after restore"),LoadedSecond->LogicalId,Id);
    TestTrue(TEXT("Capture after restore and representation"),Lab.Host->Save(After));
    TestTrue(TEXT("Restored Core state and RNG remain unchanged"),Before==After);
    Lab.Host->CloseLab();
    TestFalse(TEXT("Closing Host clears first-world Actor"),IsValid(LoadedFirst));
    TestFalse(TEXT("Closing Host clears second-world Actor"),IsValid(LoadedSecond));
    UE_LOG(LogTemp,Display,TEXT("F02 EVIDENCE WorldScopedRepresentation: EntityId=%s two-world overlap/reuse/recreate/restore/close verified"),*Id);
    return true;
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
