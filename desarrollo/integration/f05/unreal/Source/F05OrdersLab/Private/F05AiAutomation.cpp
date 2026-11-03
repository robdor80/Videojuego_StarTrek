#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "f05_ai.h"
bool F05BridgeReady();
#if WITH_DEV_AUTOMATION_TESTS
namespace {
constexpr auto AiFlags=EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter;
struct AiCampaign {
 F04Session* S=nullptr;F04Handles H{};uint64 Need=0,Duty=0,Key=40000;
 ~AiCampaign(){if(S)f04_destroy(S);}
 uint64 Revision(){F04Stats V{};return f04_stats(S,&V)==F04_OK?V.revision:MAX_uint64;}
 bool Op(F04Ref Who,uint32 Kind,uint64 Target,uint64 Aux=0,uint64 End=0,uint32 Value=0){F04Request Q{Who,Revision(),Kind,Value,Target,Aux,0,End,50401};F04Result R{};if(f04_execute(S,&Q,&R)!=F04_OK)return false;if(Kind==F04_DUTY)Duty=R.record;return true;}
 bool Open(){
  if(!F05BridgeReady() || f04_create(1,"miranda",&S)!=F04_OK || f04_handles(S,&H)!=F04_OK)return false;
  if(!Op(H.head,F04_ASSIGN,H.sensors,H.ensign.id) || !Op(H.head,F04_DUTY,H.ensign.id,H.sensors,28800) || !Op(H.ensign,F04_MOVE,H.sensors))return false;
  if(f05_bind_player(S,H.doctor,Revision())!=F04_OK)return false;
  F05ScanNeedRequest Q{H.captain,Duty,Key++,Revision(),0,80,50401};F05NeedView N{};
  if(f05_scan_need(S,&Q,&N)!=F04_OK)return false;Need=N.id;
  for(auto Actor:{H.captain,H.ensign}){uint64 B=0;if(f05_brief_need(S,H.captain,Actor,Revision(),Need,Key++,50402,&B)!=F04_OK)return false;}return true;
 }
 bool Begin(F05AiContext& C){F05AiRequest Q{H.captain,Need,Key++,Revision(),70,F05_AI_FAST,0};return f05_ai_begin(S,&Q,&C)==F04_OK;}
 // Controlled v1 provider fixture; no HTTP, credentials or generation in UE.
 uint32 Reply(const F05AiContext& C,F05AiView& V,uint32 Error=0,bool Corrupt=false){
  FString Body=Corrupt?TEXT("{broken"):FString::Printf(TEXT("{\"version\":1,\"actor\":%llu,\"request\":%llu,\"projection\":%llu,\"revision\":%llu,\"issued_at\":%llu,\"expires\":%llu,\"intent\":\"scan\",\"actions\":[{\"operation\":\"F04_SCAN\",\"parameters\":{}}],\"needs_clarification\":false,\"insufficient_data\":false,\"explanation\":\"Untrusted advice\",\"trace\":\"ue-simulated\"}"),C.actor,C.request,C.projection,C.revision,C.issued_at,C.expires);
  FTCHARToUTF8 Utf8(*Body);return f05_ai_finish(S,H.captain,C.request,Utf8.Get(),uint64(Utf8.Length()),Error,&V);
 }
 bool Evaluate(F04Ref Actor,F05DecisionView& D){F05Evaluation Q{Actor,Need,Key++,Revision(),32,0};return f05_evaluate(S,&Q,&D)==F04_OK;}
 bool Save(TArray<uint8>& Out){uint64 N=0;if(f04_save(S,nullptr,0,&N)!=F04_CAPACITY || N>MAX_int32)return false;Out.SetNumUninitialized(int32(N));return f04_save(S,Out.GetData(),N,&N)==F04_OK;}
 bool Load(const TArray<uint8>& In){return f04_load(S,In.GetData(),In.Num())==F04_OK && f04_handles(S,&H)==F04_OK;}
};
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05AIValidation,"F05.P04.AIProposalValidation",AiFlags)
bool FF05AIValidation::RunTest(const FString&){
 AiCampaign C;if(!TestTrue(TEXT("Real F04/P03"),C.Open()))return false;F05AiContext Context{};F05AiView V{};
 TestTrue(TEXT("Authorized context"),C.Begin(Context) && Context.complete && Context.need==C.Need);
 TestEqual(TEXT("Strict corrupt response"),C.Reply(Context,V,0,true),uint32(F04_OK));TestEqual(TEXT("Rejected"),V.status,uint32(F05_AI_REJECTED));TestEqual(TEXT("No order"),V.order,uint64(0));
 TestTrue(TEXT("New request"),C.Begin(Context));TestEqual(TEXT("Valid simulated response"),C.Reply(Context,V),uint32(F04_OK));TestEqual(TEXT("Candidate"),V.status,uint32(F05_AI_VALID));TestEqual(TEXT("Still no order"),V.order,uint64(0));
 TestEqual(TEXT("Explicit Host handoff"),f05_ai_apply(C.S,C.H.captain,Context.request,&V),uint32(F04_OK));TestTrue(TEXT("Real P01 order"),V.order!=0);
 F05OrderView Order{};f05_order(C.S,C.H.captain,V.order,&Order);TestTrue(TEXT("Proposal is not execution"),Order.receipt.state==F05_ISSUED && !Order.receipt.task && !Order.receipt.result);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05AIStale,"F05.P04.StaleAuthorityAndFallback",AiFlags)
bool FF05AIStale::RunTest(const FString&){
 AiCampaign C;if(!TestTrue(TEXT("Ready"),C.Open()))return false;
 F05AiContext Context{};F05AiView V{};C.Begin(Context);
 TestTrue(TEXT("Authority change while provider responds"),C.Op(C.H.doctor,F04_MEDICAL,C.H.captain.id,0,60,F04_SICK));
 C.Reply(Context,V);TestEqual(TEXT("Stale response"),V.status,uint32(F05_AI_STALE));TestEqual(TEXT("No unauthorized order"),V.order,uint64(0));
 AiCampaign Offline;if(!TestTrue(TEXT("Independent offline campaign"),Offline.Open()))return false;Offline.Begin(Context);
 Offline.Reply(Context,V,F05_AI_TIMEOUT);TestEqual(TEXT("Timeout fallback"),V.status,uint32(F05_AI_FALLBACK));
 F05DecisionView D{};TestTrue(TEXT("P03 captain continues without AI"),Offline.Evaluate(Offline.H.captain,D));uint64 Order=D.order;
 TestTrue(TEXT("P03 operator receives"),Offline.Evaluate(Offline.H.ensign,D));TestTrue(TEXT("P03 operator executes"),Offline.Evaluate(Offline.H.ensign,D));
 F05ResultView R{};TestEqual(TEXT("True Core effect"),f05_result(Offline.S,Offline.H.captain,Order,&R),uint32(F04_OK));TestEqual(TEXT("Performed"),R.performed,uint32(1));return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05AIRecovery,"F05.P04.OffscreenRecoveryAndSafety",AiFlags)
bool FF05AIRecovery::RunTest(const FString&){
 AiCampaign C;if(!TestTrue(TEXT("Ready"),C.Open()))return false;F05AiContext Context{};F05AiView V{};C.Begin(Context);C.Reply(Context,V);
 UWorld* World=UWorld::CreateWorld(EWorldType::Game,false);if(!TestNotNull(TEXT("Isolated UWorld"),World))return false;
 World->InitializeNewWorld(UWorld::InitializationValues().AllowAudioPlayback(false).CreatePhysicsScene(false).CreateNavigation(false).CreateAISystem(false));
 AActor* Marker=World->SpawnActor<AActor>();TestNotNull(TEXT("Disposable Actor"),Marker);if(Marker)Marker->Destroy();World->DestroyWorld(false);
 TestEqual(TEXT("Apply offscreen"),f05_ai_apply(C.S,C.H.captain,Context.request,&V),uint32(F04_OK));uint64 Order=V.order;
 F05DecisionView D{};C.Evaluate(C.H.ensign,D);C.Evaluate(C.H.ensign,D);TArray<uint8> Future,Replay;C.Save(Future);
 TestTrue(TEXT("Recover"),C.Load(Future));TestEqual(TEXT("Replay accepted intent"),f05_ai_apply(C.S,C.H.captain,Context.request,&V),uint32(F04_OK));C.Reply(Context,V);C.Save(Replay);
 TestTrue(TEXT("No second effect or overwritten Core result"),Future==Replay);F05ResultView R{};f05_result(C.S,C.H.captain,Order,&R);TestTrue(TEXT("Actual retained Core result"),R.performed && R.consumed_random);return true;
}
#endif
