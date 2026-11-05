#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "Engine/World.h"
#include "Engine/Engine.h"
#include "GameFramework/Actor.h"
#include "f05_initiative.h"
bool F05BridgeReady();
#if WITH_DEV_AUTOMATION_TESTS
namespace {
constexpr auto InitiativeFlags=EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter;
struct InitiativeCampaign {
 F04Session* Session=nullptr;F04Handles H{};uint64 Need=0,Duty=0;
 ~InitiativeCampaign(){if(Session)f04_destroy(Session);}
 uint64 Revision(){F04Stats S{};return f04_stats(Session,&S)==F04_OK?S.revision:MAX_uint64;}
 bool Op(F04Ref Actor,uint32 Kind,uint64 Target,uint64 Aux=0,uint64 End=0){
  F04Request Q{Actor,Revision(),Kind,0,Target,Aux,0,End,50301};F04Result R{};
  if(f04_execute(Session,&Q,&R)!=F04_OK)return false;if(Kind==F04_DUTY)Duty=R.record;return true;
 }
 bool Open(bool PlayerOperator=false){
  if(!IsInGameThread() || !F05BridgeReady() || f04_create(1,"miranda",&Session)!=F04_OK || f04_handles(Session,&H)!=F04_OK)return false;
  if(!Op(H.head,F04_ASSIGN,H.sensors,H.ensign.id) || !Op(H.head,F04_DUTY,H.ensign.id,H.sensors,28800) || !Op(H.ensign,F04_MOVE,H.sensors))return false;
  if(f05_bind_player(Session,PlayerOperator?H.ensign:H.doctor,Revision())!=F04_OK)return false;
  F05ScanNeedRequest Q{H.captain,Duty,10000,Revision(),0,80,50301};F05NeedView N{};
  if(f05_scan_need(Session,&Q,&N)!=F04_OK)return false;Need=N.id;return true;
 }
 bool Brief(F04Ref To,uint64 Key){uint64 Communication=0;return f05_brief_need(Session,H.captain,To,Revision(),Need,Key,50302,&Communication)==F04_OK && Communication!=0;}
 uint32 Evaluate(F04Ref Who,uint64 Key,F05DecisionView& Out){F05Evaluation Q{Who,Need,Key,Revision(),32,0};return f05_evaluate(Session,&Q,&Out);}
 bool Save(TArray<uint8>& Out){uint64 N=0;if(f04_save(Session,nullptr,0,&N)!=F04_CAPACITY || N>MAX_int32)return false;Out.SetNumUninitialized(int32(N));return f04_save(Session,Out.GetData(),N,&N)==F04_OK;}
 bool Load(const TArray<uint8>& In){return f04_load(Session,In.GetData(),In.Num())==F04_OK && f04_handles(Session,&H)==F04_OK;}
};
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05NPCInitiative,"F05.P03.NPCInitiativeAndOrders",InitiativeFlags)
bool FF05NPCInitiative::RunTest(const FString&) {
 InitiativeCampaign C;if(!TestTrue(TEXT("Actual F04 duty and authorized obligation"),C.Open() && C.Brief(C.H.captain,10001) && C.Brief(C.H.ensign,10002)))return false;
 F05DecisionView D{};TestEqual(TEXT("NPC captain evaluates"),C.Evaluate(C.H.captain,20001,D),uint32(F04_OK));
 TestTrue(TEXT("Detection, decision and P01 order are distinct"),D.need==C.Need && D.detection && D.id && D.order && D.decision==F05_ISSUE_ORDER);
 const uint64 Order=D.order;F05OrderView O{};f05_order(C.Session,C.H.captain,Order,&O);TestTrue(TEXT("Issued is not executed"),O.receipt.state==F05_ISSUED && !O.receipt.task);
 TestEqual(TEXT("NPC receives via P01"),C.Evaluate(C.H.ensign,20002,D),uint32(F04_OK));
 TestEqual(TEXT("NPC executes via P01"),C.Evaluate(C.H.ensign,20003,D),uint32(F04_OK));
 F05ResultView R{};TestEqual(TEXT("Authoritative Core result"),f05_result(C.Session,C.H.captain,Order,&R),uint32(F04_OK));
 TestTrue(TEXT("Real Core stream, no fabricated contacts"),R.performed==1 && R.consumed_random==1 && R.stream==0xF0401 && R.value>=1 && R.value<=100);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05NPCAuthorityKnowledge,"F05.P03.AuthorityAndKnowledge",InitiativeFlags)
bool FF05NPCAuthorityKnowledge::RunTest(const FString&) {
 InitiativeCampaign C;if(!TestTrue(TEXT("Player identity persisted"),C.Open(true)))return false;
 F05DecisionView D{};C.Evaluate(C.H.captain,20001,D);TestTrue(TEXT("Unbriefed even captain does not know"),D.decision==F05_CLARIFY && !D.need && !D.order);
 TestTrue(TEXT("Report only to operator"),C.Brief(C.H.ensign,10001));C.Evaluate(C.H.captain,20002,D);TestEqual(TEXT("No automatic shared knowledge"),D.decision,uint32(F05_CLARIFY));
 TestTrue(TEXT("XO explicitly briefed"),C.Brief(C.H.watch,10002));C.Evaluate(C.H.watch,20003,D);TestTrue(TEXT("XO proposal has no unauthorized order"),D.decision==F05_PROPOSE && !D.order);
 TestTrue(TEXT("Captain explicitly briefed"),C.Brief(C.H.captain,10003));C.Evaluate(C.H.captain,20004,D);const uint64 Order=D.order;
 C.Evaluate(C.H.ensign,20005,D);TestEqual(TEXT("Absent player never auto accepts"),D.decision,uint32(F05_WAIT_PLAYER));
 F05OrderView O{};TestEqual(TEXT("Pending order"),f05_order(C.Session,C.H.captain,Order,&O),uint32(F04_OK));TestTrue(TEXT("No task, attempt or effect"),O.receipt.state==F05_ISSUED && !O.receipt.task && !O.receipt.result);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05NPCOffscreen,"F05.P03.OffscreenPersistenceAndRecovery",InitiativeFlags)
bool FF05NPCOffscreen::RunTest(const FString&) {
 InitiativeCampaign C;if(!TestTrue(TEXT("Ready"),C.Open() && C.Brief(C.H.captain,10001) && C.Brief(C.H.ensign,10002)))return false;
 TArray<uint8> Initial,WithWorld,Offscreen,Replay;TestTrue(TEXT("Save initial"),C.Save(Initial));
 const auto WorldValues=UWorld::InitializationValues().AllowAudioPlayback(false).CreatePhysicsScene(false).CreateNavigation(false).CreateAISystem(false);
 UWorld* World=UWorld::CreateWorld(EWorldType::Game,false,NAME_None,nullptr,true,ERHIFeatureLevel::Num,&WorldValues);if(!TestNotNull(TEXT("Isolated UWorld"),World))return false;
 GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(World);
 AActor* Marker=World->SpawnActor<AActor>();TestNotNull(TEXT("Disposable presentation only"),Marker);
 F05DecisionView D{};C.Evaluate(C.H.captain,20001,D);const uint64 Order=D.order;C.Evaluate(C.H.ensign,20002,D);C.Evaluate(C.H.ensign,20003,D);C.Save(WithWorld);
 if(Marker)TestTrue(TEXT("Destroy disposable Actor"),Marker->Destroy());World->DestroyWorld(false);GEngine->DestroyWorldContext(World);
 TestTrue(TEXT("Restore without world or Actors"),C.Load(Initial));C.Evaluate(C.H.captain,20001,D);TestEqual(TEXT("Stable order ID"),D.order,Order);
 C.Evaluate(C.H.ensign,20002,D);F05Evaluation Execute{C.H.ensign,C.Need,20003,C.Revision(),32,0};
 TestEqual(TEXT("Native offscreen execution"),f05_evaluate(C.Session,&Execute,&D),uint32(F04_OK));C.Save(Offscreen);
 TestTrue(TEXT("Same inputs/seed/revision exact Core future"),WithWorld==Offscreen);
 TestTrue(TEXT("Recover completed campaign"),C.Load(Offscreen));Execute.actor=C.H.ensign;
 TestEqual(TEXT("Replay recovered decision"),f05_evaluate(C.Session,&Execute,&D),uint32(F04_OK));C.Save(Replay);TestTrue(TEXT("No repeated events or effect"),Replay==Offscreen);return true;
}
#endif
