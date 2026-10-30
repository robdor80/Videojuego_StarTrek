#include "F03CampaignSubsystem.h"
#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Engine/GameInstance.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Misc/Paths.h"
#include "HAL/FileManager.h"
#include "Async/Async.h"
namespace {
struct FWorld {
    UWorld* World=nullptr;
    UF03CampaignSubsystem* Host=nullptr;
    FWorld(UGameInstance* Game,UF03CampaignSubsystem* InHost):Host(InHost) {
        const auto Values=UWorld::InitializationValues().AllowAudioPlayback(false).RequiresHitProxies(false)
            .CreatePhysicsScene(false).CreateNavigation(false).CreateAISystem(false).ShouldSimulatePhysics(false).SetTransactional(false);
        World=UWorld::CreateWorld(EWorldType::Game,false,NAME_None,nullptr,true,ERHIFeatureLevel::Num,&Values);
        GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World); World->SetGameInstance(Game);
    }
    ~FWorld() { Host->Dematerialize(World); World->DestroyWorld(false); GEngine->DestroyWorldContext(World); }
};
struct FLab {
    UGameInstance* Game=NewObject<UGameInstance>();
    UF03CampaignSubsystem* Host=nullptr;
    FLab() { Game->AddToRoot(); Host=NewObject<UF03CampaignSubsystem>(Game); Host->AddToRoot(); Host->OpenLab(); }
    ~FLab() { Host->CloseLab(); Host->RemoveFromRoot(); Game->RemoveFromRoot(); }
};
bool Romulan(const TArray<F03Fact>& Facts) { for(const auto& F:Facts) if(F.classification==2) return true; return false; }
constexpr auto Flags=EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF03Identity,"F03.Core.IdentityLodWorlds",Flags)
bool FF03Identity::RunTest(const FString&) {
    FLab Lab; FWorld First(Lab.Game,Lab.Host),Second(Lab.Game,Lab.Host);
    TArray<uint8> Before,After; if(!TestTrue(TEXT("Save before visual changes"),Lab.Host->Save(Before))) return false;
    auto* A=Lab.Host->Represent(First.World,2,0); auto* B=Lab.Host->Represent(Second.World,2,1);
    if(!TestNotNull(TEXT("First marker"),A) || !TestNotNull(TEXT("Second marker"),B)) return false;
    TestTrue(TEXT("Distinct per UWorld"),A!=B && A->GetWorld()==First.World && B->GetWorld()==Second.World);
    TestEqual(TEXT("Same logical identity"),A->LogicalId,B->LogicalId);
    const FString Id=A->LogicalId;
    TestTrue(TEXT("LOD reuses entity and Actor"),Lab.Host->Represent(First.World,2,1)==A);
    TestNull(TEXT("Hidden entity cannot be materialized by guessed id"),Lab.Host->Represent(First.World,3));
    TestTrue(TEXT("Desmaterialize"),A->Destroy());
    A=Lab.Host->Represent(First.World,2,0); if(!TestNotNull(TEXT("Recreate"),A)) return false;
    TestEqual(TEXT("Recreated identity"),A->LogicalId,Id); TestTrue(TEXT("Other world survives"),IsValid(B));
    Lab.Host->Save(After); TestTrue(TEXT("Visual cycle leaves Core and RNG byte identical"),Before==After);
    F03Stats State{}; TestTrue(TEXT("Stats"),Lab.Host->Stats(State)); TestEqual(TEXT("No logical duplicate"),State.entities,uint64(8));
    TestTrue(TEXT("Load"),Lab.Host->Load(Before)); TestFalse(TEXT("First binding invalidated"),IsValid(A)); TestFalse(TEXT("Second binding invalidated"),IsValid(B));
    A=Lab.Host->Represent(First.World,2); B=Lab.Host->Represent(Second.World,2);
    if(!TestNotNull(TEXT("Restored first"),A) || !TestNotNull(TEXT("Restored second"),B)) return false;
    TestEqual(TEXT("Persisted identity"),A->LogicalId,Id); Lab.Host->CloseLab();
    TestFalse(TEXT("Close destroys first"),IsValid(A)); TestFalse(TEXT("Close destroys second"),IsValid(B)); return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF03Offscreen,"F03.Core.Offscreen",Flags)
bool FF03Offscreen::RunTest(const FString&) {
    FLab Lab; FWorld World(Lab.Game,Lab.Host);
    auto* Primary=Lab.Host->Represent(World.World,1); if(!TestNotNull(TEXT("Primary only"),Primary)) return false;
    TestTrue(TEXT("Authorized route"),Lab.Host->ScheduleRoute());
    TestTrue(TEXT("Advance without secondary Actor"),Lab.Host->Advance(20));
    auto* Ship=Lab.Host->Represent(World.World,2); if(!TestNotNull(TEXT("Materialize result"),Ship)) return false;
    TestEqual(TEXT("Core arrival represented"),Ship->Location,2);
    TestTrue(TEXT("Unload secondary"),Ship->Destroy()); TestTrue(TEXT("Remaining route offscreen"),Lab.Host->Advance(100));
    Ship=Lab.Host->Represent(World.World,2); if(!TestNotNull(TEXT("Rematerialize result"),Ship)) return false;
    TestEqual(TEXT("Core return represented"),Ship->Location,1);
    F03Stats Before{},After{}; Lab.Host->Stats(Before); Lab.Host->Advance(100); Lab.Host->Stats(After);
    TestEqual(TEXT("Exactly four terminal events"),After.finished,uint64(4));
    TestEqual(TEXT("Replay has no mutation"),After.revision,Before.revision);
    TestEqual(TEXT("Primary persists"),Primary->Location,1); return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF03Knowledge,"F03.Core.Knowledge",Flags)
bool FF03Knowledge::RunTest(const FString&) {
    FLab Lab; TArray<F03Fact> First,Second; TArray<uint8> Before,After;
    Lab.Host->Save(Before); Lab.Host->View(1,First); Lab.Host->View(2,Second);
    TestFalse(TEXT("Primary cannot see Romulan"),Romulan(First)); TestFalse(TEXT("Secondary cannot see Romulan"),Romulan(Second));
    TestFalse(TEXT("No acquisition before arrival"),Lab.Host->Acquire(2,1));
    TestFalse(TEXT("No arbitrary channel"),Lab.Host->Acquire(2,99));
    TestFalse(TEXT("No arbitrary observer"),Lab.Host->View(3,First));
    Lab.Host->Save(After); TestTrue(TEXT("Queries and denials do not mutate"),Before==After);
    Lab.Host->ScheduleRoute(); Lab.Host->Advance(20); TestTrue(TEXT("Direct authorized observation"),Lab.Host->Acquire(2,1));
    Lab.Host->View(1,First); Lab.Host->View(2,Second);
    TestFalse(TEXT("Isolation"),Romulan(First)); TestTrue(TEXT("Acquired classification"),Romulan(Second));
    const int32 N=First.Num(); TestTrue(TEXT("Report"),Lab.Host->Acquire(1,2)); Lab.Host->View(1,First);
    TestEqual(TEXT("Only existence transferred"),First.Num(),N+1); TestFalse(TEXT("No classification leak in report"),Romulan(First));
    TestTrue(TEXT("Revoke host permission"),Lab.Host->SetPermission(false));
    TestFalse(TEXT("Revocation denies read"),Lab.Host->View(2,Second)); TestFalse(TEXT("Revocation denies mutation"),Lab.Host->Acquire(2,1)); return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF03Recovery,"F03.Core.Recovery",Flags)
bool FF03Recovery::RunTest(const FString&) {
    FLab Lab; FWorld World(Lab.Game,Lab.Host); Lab.Host->ScheduleRoute(); Lab.Host->Advance(20); Lab.Host->Acquire(2,1); Lab.Host->Acquire(1,2);
    auto* Old=Lab.Host->Represent(World.World,2); if(!TestNotNull(TEXT("Before close"),Old)) return false;
    const FString Id=Old->LogicalId;
    const FString Dir=FPaths::Combine(FPaths::ProjectSavedDir(),TEXT("F03Evidence")); IFileManager::Get().MakeDirectory(*Dir,true);
    const FString File=FPaths::Combine(Dir,FGuid::NewGuid().ToString()+TEXT(".f03"));
    TArray<uint8> Saved,Future,Recovered; Lab.Host->Save(Saved);
    TestTrue(TEXT("Real file save"),Lab.Host->WriteSave(File)); TestFalse(TEXT("Never overwrite prior save"),Lab.Host->WriteSave(File));
    Lab.Host->Advance(100); Lab.Host->Save(Future); Lab.Host->CloseLab(); TestFalse(TEXT("Session fully closed"),IsValid(Old));
    TestTrue(TEXT("New logical session"),Lab.Host->OpenLab()); TestTrue(TEXT("Load file"),Lab.Host->ReadSave(File)); Lab.Host->Save(Recovered);
    TestTrue(TEXT("Full archive identical"),Saved==Recovered);
    TArray<F03Fact> Facts; Lab.Host->View(2,Facts); TestTrue(TEXT("Knowledge preserved"),Romulan(Facts));
    auto* Marker=Lab.Host->Represent(World.World,2); if(!TestNotNull(TEXT("Recovered marker"),Marker)) return false;
    TestEqual(TEXT("Identity persists"),Marker->LogicalId,Id); TestEqual(TEXT("Arrival persists"),Marker->Location,2);
    Lab.Host->Advance(100); Lab.Host->Save(Recovered); TestTrue(TEXT("Pending events and RNG reproduce future"),Future==Recovered);
    TestEqual(TEXT("Loaded route result projected"),Marker->Location,1); return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF03Failure,"F03.Core.SafeFailure",Flags)
bool FF03Failure::RunTest(const FString&) {
    FLab Lab; FWorld World(Lab.Game,Lab.Host); auto* A=Lab.Host->Represent(World.World,2);
    if(!TestNotNull(TEXT("Initial visual"),A)) return false;
    TArray<uint8> Before,After,Bad; Lab.Host->ScheduleRoute(); Lab.Host->Save(Before); Bad=Before; Bad.Last()^=128;
    TestFalse(TEXT("Corrupt archive rejected"),Lab.Host->Load(Bad)); Bad=Before; Bad[8]=99;
    TestFalse(TEXT("Incompatible archive rejected"),Lab.Host->Load(Bad));
    Lab.Host->Save(After); TestTrue(TEXT("Valid state preserved"),Before==After); TestTrue(TEXT("Valid Actor preserved"),IsValid(A));
    TestTrue(TEXT("Advance"),Lab.Host->Advance(20)); Lab.Host->Save(Before);
    TestFalse(TEXT("Backwards time rejected"),Lab.Host->Advance(19)); Lab.Host->Save(After);
    TestTrue(TEXT("Negative temporal operation is safe"),Before==After); return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF03Thread,"F03.Core.ThreadAuthority",Flags)
bool FF03Thread::RunTest(const FString&) {
    FLab Lab; TArray<uint8> Before,After; if(!TestTrue(TEXT("Live campaign before worker"),Lab.Host->Save(Before))) return false;
    const bool Denied=Async(EAsyncExecution::Thread,[Host=Lab.Host]() {
        F03Stats State{}; TArray<uint8> Bytes;
        return !Host->Stats(State) && !Host->OpenLab() && !Host->Advance(20) && !Host->ScheduleRoute() && !Host->Save(Bytes);
    }).Get();
    TestTrue(TEXT("Worker denied"),Denied); Lab.Host->Save(After); TestTrue(TEXT("No side effect"),Before==After); return true;
}
#endif
