#include "F04CampaignSubsystem.h"
#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"
#include "Engine/GameInstance.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "Async/Async.h"
#include "EngineUtils.h"
namespace {
constexpr auto Flags=EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter;
struct Lab {
 UGameInstance* Game=NewObject<UGameInstance>();UF04CampaignSubsystem* Host=nullptr;
 Lab(){Game->AddToRoot();Host=NewObject<UF04CampaignSubsystem>(Game);Host->AddToRoot();Host->OpenLab();}
 ~Lab(){Host->CloseLab();Host->RemoveFromRoot();Game->RemoveFromRoot();}
 bool Duty(){return Host->Intent(4,F04_ASSIGN,12,5)==F04_OK && Host->Intent(4,F04_DUTY,5,12,0,28800)==F04_OK;}
};
struct World {
 UWorld* W=nullptr;UF04CampaignSubsystem* Host=nullptr;
 World(Lab& L):Host(L.Host){const auto V=UWorld::InitializationValues().AllowAudioPlayback(false).RequiresHitProxies(false).CreatePhysicsScene(false).CreateNavigation(false).CreateAISystem(false).ShouldSimulatePhysics(false).SetTransactional(false);
 W=UWorld::CreateWorld(EWorldType::Game,false,NAME_None,nullptr,true,ERHIFeatureLevel::Num,&V);GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(W);W->SetGameInstance(L.Game);}
 ~World(){Host->Dematerialize(W);W->DestroyWorld(false);GEngine->DestroyWorldContext(W);}
};
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF04Actors,"F04.Core.RealWorldsActors",Flags)
bool FF04Actors::RunTest(const FString&){
 Lab L;World A(L),B(L);TestTrue(TEXT("Core watch"),L.Duty());TArray<uint8> Before,After;L.Host->Save(Before);
 auto* One=L.Host->Represent(A.W,5);auto* Two=L.Host->Represent(B.W,5);
 if(!TestNotNull(TEXT("First real Actor"),One)||!TestNotNull(TEXT("Second real Actor"),Two))return false;
 TestTrue(TEXT("World isolation"),One!=Two && One->GetWorld()==A.W && Two->GetWorld()==B.W);
 TestEqual(TEXT("Same stable identity"),One->LogicalId,Two->LogicalId);TestTrue(TEXT("Core watch projection"),One->OnDuty);
 TestTrue(TEXT("Reuse"),One==L.Host->Represent(A.W,5));TestNull(TEXT("Unknown identity"),L.Host->Represent(A.W,999));
 L.Host->Dematerialize(A.W);TestFalse(TEXT("Unloaded Actor"),IsValid(One));One=L.Host->Represent(A.W,5);TestNotNull(TEXT("Recreated"),One);
 L.Host->Save(After);TestTrue(TEXT("Visual lifecycle does not mutate Core"),Before==After);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF04Recovery,"F04.Core.NewSessionRecovery",Flags)
bool FF04Recovery::RunTest(const FString&){
 Lab L;World W(L);TestTrue(TEXT("Duty"),L.Duty());TestEqual(TEXT("Move intention"),L.Host->Intent(5,F04_MOVE,12),uint32(F04_OK));
 TestEqual(TEXT("Pending task"),L.Host->Intent(5,F04_QUEUE,0,0,10,20,F04_SCAN),uint32(F04_OK));
 auto* Old=L.Host->Represent(W.W,5);if(!TestNotNull(TEXT("Old Actor"),Old))return false;
 const FString Id=Old->LogicalId;TArray<uint8> Before,Future,Restored;L.Host->Save(Before);L.Host->Advance(100);L.Host->Save(Future);
 L.Host->CloseLab();TestFalse(TEXT("Destroyed session bindings"),IsValid(Old));TestTrue(TEXT("New session"),L.Host->OpenLab());TestTrue(TEXT("Load"),L.Host->Load(Before));L.Host->Save(Restored);TestTrue(TEXT("Archive preserved"),Restored==Before);
 auto* New=L.Host->Represent(W.W,5);if(!TestNotNull(TEXT("New Actor"),New))return false;TestEqual(TEXT("Persistent identity"),New->LogicalId,Id);
 TestTrue(TEXT("Resume no Actors required"),L.Host->Advance(100));L.Host->Save(Restored);TestTrue(TEXT("Deterministic future"),Restored==Future);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF04Authority,"F04.Core.AuthorityAndMedical",Flags)
bool FF04Authority::RunTest(const FString&){
 Lab L;TestTrue(TEXT("Duty"),L.Duty());TestEqual(TEXT("No captain technical privilege"),L.Host->Intent(3,F04_SCAN),uint32(F04_QUALIFICATION));
 TestEqual(TEXT("Ensign no command"),L.Host->Intent(5,F04_BRIDGE),uint32(F04_DENIED));TestEqual(TEXT("Head own department"),L.Host->Intent(4,F04_ASSIGN,12,5),uint32(F04_OK));
 TestEqual(TEXT("Head other department denied"),L.Host->Intent(4,F04_ASSIGN,13,11),uint32(F04_SCOPE));TestEqual(TEXT("Watch authority changes alert"),L.Host->Intent(6,F04_BRIDGE,0,0,0,0,2),uint32(F04_OK));
 F04Stats Alert{};L.Host->Stats(Alert);TestEqual(TEXT("Authoritative yellow alert"),Alert.alert,uint64(2));
 TestEqual(TEXT("Captain safety limit"),L.Host->Intent(3,F04_IMPOSSIBLE),uint32(F04_SAFETY));TestEqual(TEXT("Medical relief"),L.Host->Intent(7,F04_MEDICAL,3,0,0,100,F04_SICK),uint32(F04_OK));
 F04Stats S{};L.Host->Stats(S);TestEqual(TEXT("Normal succession"),S.commander,uint64(6));TestEqual(TEXT("Doctor no command"),L.Host->Intent(7,F04_BRIDGE),uint32(F04_DENIED));
 L.Host->Advance(100);L.Host->Stats(S);TestEqual(TEXT("Captain recovers"),S.commander,uint64(3));return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF04Vacancy,"F04.Core.AbsenceReliefOffscreen",Flags)
bool FF04Vacancy::RunTest(const FString&){
 Lab L;World W(L);TestTrue(TEXT("Duty"),L.Duty());uint64 Duty=0; // Locate the created duty through its returned record in a fresh scenario.
 L.Host->CloseLab();L.Host->OpenLab();L.Host->Intent(4,F04_ASSIGN,12,5);L.Host->Intent(4,F04_DUTY,5,12,0,28800,0,42,&Duty);
 auto* Actor=L.Host->Represent(W.W,5);if(!TestNotNull(TEXT("Actor"),Actor))return false;
 L.Host->Intent(4,F04_ABSENCE,5,0,0,200,F04_SICK);TestFalse(TEXT("Authoritative unavailable"),Actor->Available);F04Stats S{};L.Host->Stats(S);TestEqual(TEXT("Recognized gap"),S.vacancies,uint64(3));
 L.Host->Dematerialize(W.W);TestEqual(TEXT("Existing relief"),L.Host->Intent(4,F04_RELIEF,Duty,8),uint32(F04_OK));L.Host->Advance(100);
 auto* Relief=L.Host->Represent(W.W,8);if(!TestNotNull(TEXT("Represent existing relief"),Relief))return false;TestTrue(TEXT("Offscreen state projected"),Relief->OnDuty);L.Host->Stats(S);TestEqual(TEXT("No synthetic crew"),S.crew,uint64(7));return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF04Failure,"F04.Core.SafeLoadAndThread",Flags)
bool FF04Failure::RunTest(const FString&){
 Lab L;World W(L);auto* Actor=L.Host->Represent(W.W,5);TArray<uint8> Before,After,Bad;L.Host->Save(Before);Bad=Before;Bad.Last()^=128;
 TestFalse(TEXT("Bad load"),L.Host->Load(Bad));L.Host->Save(After);TestTrue(TEXT("Atomic load failure"),Before==After);TestTrue(TEXT("Actor preserved"),IsValid(Actor));
 const bool Denied=Async(EAsyncExecution::Thread,[Host=L.Host](){F04Stats S{};return !Host->Stats(S) && Host->Intent(3,F04_BRIDGE)==F04_THREAD && !Host->Advance(20);}).Get();TestTrue(TEXT("Owner thread authority"),Denied);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF04Population,"F04.Core.LargePopulationSelectiveActors",Flags)
bool FF04Population::RunTest(const FString&){
 Lab L;World A(L),B(L);F04PopulationConfig Config{65001,404,1800,400,0,0};
 TestTrue(TEXT("Valhalla Core population"),L.Host->OpenPopulation("valhalla",Config));
 F04Stats S{};L.Host->Stats(S);TestEqual(TEXT("Fleet"),S.crew,uint64(1800));TestEqual(TEXT("Residents"),S.civilians,uint64(400));
 int32 Count=0;for(TActorIterator<AF04CrewMarker> It(A.W);It;++It)++Count;
 TestEqual(TEXT("No automatic crew Actors"),Count,0);
 auto* One=L.Host->Represent(A.W,2202);auto* Two=L.Host->Represent(B.W,2202);
 if(!TestNotNull(TEXT("Last civilian identity"),One)||!TestNotNull(TEXT("Second world"),Two))return false;
 TestEqual(TEXT("Core identity"),One->CorePersonId,uint64(2202));TestTrue(TEXT("World isolation"),One!=Two);
 L.Host->Dematerialize(A.W);TestFalse(TEXT("Actor released"),IsValid(One));L.Host->Stats(S);
 TestEqual(TEXT("Logical civilian retained"),S.civilians,uint64(400));
 TArray<uint8> Before,After;L.Host->Save(Before);TestTrue(TEXT("Restore large campaign"),L.Host->Load(Before));L.Host->Save(After);
 TestTrue(TEXT("Identities persist"),Before==After);TestNotNull(TEXT("Represent after recovery"),L.Host->Represent(A.W,2202));return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF04Sutherland,"F04.Core.SutherlandOrganizationSelectiveActors",Flags)
bool FF04Sutherland::RunTest(const FString&){
 Lab L;World A(L),B(L);F04PopulationConfig Config{65001,404,130,0,0,0};
 TestTrue(TEXT("130 persistent identities"),L.Host->OpenPopulation("miranda",Config));
 TestTrue(TEXT("Explicit equipment-specific profile"),L.Host->InstallOrganization(F04_SUTHERLAND_SCIENCE,F04_SUTHERLAND_EQUIPMENT));
 F04OrganizationStats Organization{};L.Host->Organization(Organization);
 TestEqual(TEXT("130 vacant posts; no invented crew"),Organization.vacant,uint64(130));
 TestTrue(TEXT("Explicit synthetic fixture on existing people"),L.Host->BootstrapOrganizationFixture());
 TestTrue(TEXT("Alpha reference"),L.Host->PlanAlpha(28800));TestTrue(TEXT("Core clock"),L.Host->Advance(28800));
 L.Host->Organization(Organization);TestEqual(TEXT("Seven departments"),Organization.departments,uint64(7));
 TestEqual(TEXT("32 sections"),Organization.sections,uint64(32));TestEqual(TEXT("53 actual workers"),Organization.on_duty,uint64(53));
 int32 Count=0;for(TActorIterator<AF04CrewMarker> It(A.W);It;++It)++Count;
 TestEqual(TEXT("Organization does not create 130 Actors"),Count,0);
 TArray<F04Position> Positions;TestTrue(TEXT("Core relation projection"),L.Host->Positions(Positions));
 uint32 First=0,Security=0;for(const auto& Position:Positions){if(Position.section==2)First=static_cast<uint32>(Position.person);if(Position.section==21 && Position.ordinal==1)Security=static_cast<uint32>(Position.person);}
 auto* FirstActor=L.Host->Represent(A.W,First);auto* SecurityActor=L.Host->Represent(A.W,Security);
 if(!TestNotNull(TEXT("First officer"),FirstActor)||!TestNotNull(TEXT("Security chief"),SecurityActor))return false;
 TestTrue(TEXT("Two identities, both on duty"),FirstActor!=SecurityActor && FirstActor->OnDuty && SecurityActor->OnDuty);
 TestEqual(TEXT("First officer also watch officer"),L.Host->Intent(First,F04_BRIDGE,0,0,0,0,2),uint32(F04_OK));
 TestEqual(TEXT("Tactical console does not confer ship command"),L.Host->Intent(Security,F04_BRIDGE),uint32(F04_DENIED));
 TArray<uint8> Before,After;L.Host->Save(Before);L.Host->Dematerialize(A.W);L.Host->Save(After);
 TestTrue(TEXT("Actor removal preserves organization"),Before==After);TestTrue(TEXT("Load complete organization"),L.Host->Load(Before));
 L.Host->Save(After);TestTrue(TEXT("Exact archive"),Before==After);auto* Recovered=L.Host->Represent(B.W,Security);
 if(!TestNotNull(TEXT("Selective recovery in another world"),Recovered))return false;
 TestTrue(TEXT("Same identity and watch"),Recovered->CorePersonId==Security && Recovered->OnDuty);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF04Intrepid,"F04.Core.IntrepidOrganizationOffscreen",Flags)
bool FF04Intrepid::RunTest(const FString&){
 Lab L;World A(L),B(L);F04PopulationConfig Config{66001,404,160,0,0,0};
 TestTrue(TEXT("160 persistent people"),L.Host->OpenPopulation("intrepid",Config));
 TestTrue(TEXT("Install reusable profile"),L.Host->InstallOrganization(F04_INTREPID_EXPLORATION,F04_INTREPID_EQUIPMENT));
 TestTrue(TEXT("Existing identities only"),L.Host->BootstrapOrganizationFixture());
 TestTrue(TEXT("Alpha"),L.Host->PlanAlpha(28800));TestTrue(TEXT("Core time without player"),L.Host->Advance(28800));
 F04OrganizationStats Org{};L.Host->Organization(Org);
 TestEqual(TEXT("160 posts"),Org.positions,uint64(160));TestEqual(TEXT("7 departments"),Org.departments,uint64(7));
 TestEqual(TEXT("34 sections"),Org.sections,uint64(34));TestEqual(TEXT("64 workers"),Org.on_duty,uint64(64));
 TestEqual(TEXT("No Alpha gaps"),Org.alpha_deficit,uint64(0));TestEqual(TEXT("Separate operations and communications"),Org.continuous_covered,uint64(7));
 int32 Count=0;for(TActorIterator<AF04CrewMarker> It(A.W);It;++It)++Count;TestEqual(TEXT("No 160 automatic Actors"),Count,0);
 TArray<F04Position> Positions;L.Host->Positions(Positions);uint32 First=0,Security=0;
 for(const auto& P:Positions){if(P.section==2)First=static_cast<uint32>(P.person);if(P.section==23 && P.ordinal==1)Security=static_cast<uint32>(P.person);}
 TestEqual(TEXT("First is also watch officer"),L.Host->Intent(First,F04_BRIDGE,0,0,0,0,2),uint32(F04_OK));
 TestEqual(TEXT("Tactical function grants no command"),L.Host->Intent(Security,F04_BRIDGE),uint32(F04_DENIED));
 auto* Marker=L.Host->Represent(A.W,Security);if(!TestNotNull(TEXT("One selective Actor"),Marker))return false;
 TestTrue(TEXT("Same identity on duty"),Marker->CorePersonId==Security && Marker->OnDuty);
 TArray<uint8> Before,After,Future;L.Host->Save(Before);L.Host->Dematerialize(A.W);L.Host->Save(After);
 TestTrue(TEXT("No visual authority"),Before==After);L.Host->Advance(57600);L.Host->Save(Future);
 L.Host->CloseLab();L.Host->OpenLab();TestTrue(TEXT("Restore complete Intrepid in new session"),L.Host->Load(Before));L.Host->Save(After);
 TestTrue(TEXT("Exact archive"),Before==After);auto* Recovered=L.Host->Represent(B.W,Security);
 if(!TestNotNull(TEXT("New UWorld projection"),Recovered))return false;
 TestTrue(TEXT("Identity and duty persist"),Recovered->CorePersonId==Security && Recovered->OnDuty);
 L.Host->Dematerialize(B.W);L.Host->Advance(57600);L.Host->Save(After);TestTrue(TEXT("Same future without player or Actors"),After==Future);
 L.Host->Organization(Org);TestEqual(TEXT("Duty ended on Core clock"),Org.on_duty,uint64(0));return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF04Sovereign,"F04.Core.SovereignThreeWatchesOffscreen",Flags)
bool FF04Sovereign::RunTest(const FString&){
 Lab L;World A(L),B(L);F04PopulationConfig Config{67001,404,700,0,0,0};
 TestTrue(TEXT("700 Core identities"),L.Host->OpenPopulation("sovereign",Config));
 TestTrue(TEXT("Sovereign profile3"),L.Host->InstallOrganization(F04_SOVEREIGN_MULTIMISSION,F04_SOVEREIGN_EQUIPMENT));
 TestTrue(TEXT("Explicit existing people fixture"),L.Host->BootstrapOrganizationFixture());
 TestTrue(TEXT("28 days, reference then rotation"),L.Host->PlanWatches(0,28*86400,false,true));
 TArray<F04ServiceCoverage> Coverage;TestTrue(TEXT("Entire horizon coverage query"),L.Host->ServiceCoverage(0,28*86400,Coverage));
 TestEqual(TEXT("Eight independent services"),Coverage.Num(),8);for(const auto& C:Coverage)TestTrue(TEXT("No critical gap in entire horizon"),C.covered==1);
 int32 Count=0;for(TActorIterator<AF04CrewMarker> It(A.W);It;++It)++Count;TestEqual(TEXT("No 700 automatic Actors"),Count,0);
 F04OrganizationStats Org{};L.Host->Organization(Org);TestEqual(TEXT("Gamma100"),Org.on_duty,uint64(100));
 F04Stats State{};L.Host->Stats(State);TestTrue(TEXT("Captain legitimately relieved"),State.commander!=3 && State.commander!=0);
 auto* Officer=L.Host->Represent(A.W,static_cast<uint32>(State.commander));if(!TestNotNull(TEXT("One selective guard Actor"),Officer))return false;
 TestTrue(TEXT("Actual guard is on duty"),Officer->OnDuty);TestTrue(TEXT("Alpha boundary"),L.Host->Advance(28800));
 L.Host->Organization(Org);TestEqual(TEXT("Alpha230"),Org.on_duty,uint64(230));L.Host->Stats(State);TestEqual(TEXT("Captain Alpha"),State.commander,uint64(3));
 TestTrue(TEXT("Beta boundary"),L.Host->Advance(57600));L.Host->Organization(Org);TestEqual(TEXT("Beta150"),Org.on_duty,uint64(150));
 L.Host->Dematerialize(A.W);TArray<uint8> Before,Future,After;L.Host->Save(Before);
 TestTrue(TEXT("Universe continues without player or Actors"),L.Host->Advance(28*86400-1));L.Host->Save(Future);
 TestTrue(TEXT("Schema4 recovery"),L.Host->Load(Before));L.Host->Save(After);TestTrue(TEXT("Exact archive"),After==Before);
 L.Host->Stats(State);auto* Recovered=L.Host->Represent(B.W,static_cast<uint32>(State.commander));if(!TestNotNull(TEXT("Reconstructed selective Actor"),Recovered))return false;
 TestTrue(TEXT("Same watch"),Recovered->OnDuty);L.Host->Dematerialize(B.W);L.Host->Advance(28*86400-1);L.Host->Save(After);
 TestTrue(TEXT("Same offscreen future"),After==Future);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF04Odyssey,"F04.Core.OdysseyThreeWatchesOffscreen",Flags)
bool FF04Odyssey::RunTest(const FString&){
 Lab L;World A(L),B(L);F04PopulationConfig Config{68001,404,1600,0,0,0};
 TestTrue(TEXT("1600 Core identities"),L.Host->OpenPopulation("odyssey",Config));
 TestTrue(TEXT("Odyssey profile4"),L.Host->InstallOrganization(F04_ODYSSEY_MULTIMISSION,F04_ODYSSEY_EQUIPMENT));
 TestTrue(TEXT("Explicit existing people fixture"),L.Host->BootstrapOrganizationFixture());
 TestTrue(TEXT("28 days, reference then rotation"),L.Host->PlanWatches(0,28*86400,false,true));
 TArray<F04ServiceCoverage> Coverage;TestTrue(TEXT("Entire horizon coverage query"),L.Host->ServiceCoverage(0,28*86400,Coverage));
 TestEqual(TEXT("Eight independent services"),Coverage.Num(),8);for(const auto& C:Coverage)TestTrue(TEXT("No critical gap in entire horizon"),C.covered==1);
 int32 Count=0;for(TActorIterator<AF04CrewMarker> It(A.W);It;++It)++Count;TestEqual(TEXT("No 1600 automatic Actors"),Count,0);
 F04OrganizationStats Org{};L.Host->Organization(Org);TestEqual(TEXT("Gamma205"),Org.on_duty,uint64(205));
 F04Stats State{};L.Host->Stats(State);TestTrue(TEXT("Captain legitimately relieved"),State.commander!=3 && State.commander!=0);
 auto* Officer=L.Host->Represent(A.W,static_cast<uint32>(State.commander));if(!TestNotNull(TEXT("One selective guard Actor"),Officer))return false;
 TestTrue(TEXT("Actual guard is on duty"),Officer->OnDuty);TestTrue(TEXT("Alpha boundary"),L.Host->Advance(28800));
 L.Host->Organization(Org);TestEqual(TEXT("Alpha500"),Org.on_duty,uint64(500));L.Host->Stats(State);TestEqual(TEXT("Captain Alpha"),State.commander,uint64(3));
 TestTrue(TEXT("Beta boundary"),L.Host->Advance(57600));L.Host->Organization(Org);TestEqual(TEXT("Beta330"),Org.on_duty,uint64(330));
 L.Host->Dematerialize(A.W);TArray<uint8> Before,Future,After;L.Host->Save(Before);
 TestTrue(TEXT("Universe continues without player or Actors"),L.Host->Advance(28*86400-1));L.Host->Save(Future);
 TestTrue(TEXT("Schema4 recovery"),L.Host->Load(Before));L.Host->Save(After);TestTrue(TEXT("Exact archive"),After==Before);
 L.Host->Stats(State);auto* Recovered=L.Host->Represent(B.W,static_cast<uint32>(State.commander));if(!TestNotNull(TEXT("Reconstructed selective Actor"),Recovered))return false;
 TestTrue(TEXT("Same watch"),Recovered->OnDuty);L.Host->Dematerialize(B.W);L.Host->Advance(28*86400-1);L.Host->Save(After);
 TestTrue(TEXT("Same offscreen future"),After==Future);return true;
}
#endif
