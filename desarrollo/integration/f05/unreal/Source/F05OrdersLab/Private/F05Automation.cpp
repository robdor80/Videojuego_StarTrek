#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"
#include "f05_orders.h"
#include "f05_delegation.h"
bool F05BridgeReady();
#if WITH_DEV_AUTOMATION_TESTS
namespace {
constexpr auto Flags=EAutomationTestFlags::EditorContext|EAutomationTestFlags::EngineFilter;
struct Campaign {
 F04Session* Session=nullptr;F04Handles H{};
 ~Campaign(){if(Session)f04_destroy(Session);}
 bool Open(){return IsInGameThread() && F05BridgeReady() && f04_create(1,"miranda",&Session)==F04_OK && f04_handles(Session,&H)==F04_OK;}
 uint64 Revision(){F04Stats S{};return f04_stats(Session,&S)==F04_OK?S.revision:MAX_uint64;}
 uint32 Op(F04Ref Actor,uint32 Kind,uint64 Target=0,uint64 Aux=0,uint64 End=0){
  F04Request Q{Actor,Revision(),Kind,0,Target,Aux,0,End,50501};F04Result R{};return f04_execute(Session,&Q,&R);
 }
 bool Ready(){return Op(H.head,F04_ASSIGN,H.sensors,H.ensign.id)==F04_OK && Op(H.head,F04_DUTY,H.ensign.id,H.sensors,28800)==F04_OK && Op(H.ensign,F04_MOVE,H.sensors)==F04_OK;}
 F05OrderRequest Request(){return {H.captain,H.ensign,H.ship,{H.ship.scope,H.sensors},1,Revision(),100,50501,F04_SCAN,0};}
 bool Save(TArray<uint8>& Out){uint64 N=0;if(f04_save(Session,nullptr,0,&N)!=F04_CAPACITY || N>MAX_int32)return false;Out.SetNumUninitialized(int32(N));return f04_save(Session,Out.GetData(),N,&N)==F04_OK;}
 bool Load(const TArray<uint8>& In){return f04_load(Session,In.GetData(),In.Num())==F04_OK && f04_handles(Session,&H)==F04_OK;}
};
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05Lifecycle,"F05.P01.LifecycleAndRecovery",Flags)
bool FF05Lifecycle::RunTest(const FString&) {
 Campaign C;if(!TestTrue(TEXT("Audited DLL and existing F04 campaign"),C.Open() && C.Ready()))return false;
 auto Q=C.Request();F05Receipt R{};
 TestEqual(TEXT("Issue"),f05_submit(C.Session,&Q,&R),uint32(F04_OK));TestEqual(TEXT("Issued"),R.state,uint32(F05_ISSUED));
 TestEqual(TEXT("Receive"),f05_receive(C.Session,C.H.ensign,C.Revision(),R.order,&R),uint32(F04_OK));
 TArray<uint8> Pending,Future,Restored;TestTrue(TEXT("Save accepted task"),C.Save(Pending));
 TestEqual(TEXT("Execute real F04_SCAN"),f05_execute_order(C.Session,C.H.ensign,C.Revision(),R.order,&R),uint32(F04_OK));
 F05ResultView Result{};TestEqual(TEXT("True Core result"),f05_result(C.Session,C.H.captain,R.order,&Result),uint32(F04_OK));
 TestTrue(TEXT("Roll, not a fabricated sensor contact"),Result.performed==1 && Result.consumed_random==1 && Result.value>=1 && Result.value<=100);
 TestTrue(TEXT("Save future"),C.Save(Future));TestTrue(TEXT("Restore pending"),C.Load(Pending));
 TestEqual(TEXT("Resume"),f05_execute_order(C.Session,C.H.ensign,C.Revision(),R.order,&R),uint32(F04_OK));C.Save(Restored);
 TestTrue(TEXT("Identical future and RNG"),Restored==Future);
 f05_execute_order(C.Session,C.H.ensign,0,R.order,&R);C.Save(Restored);TestTrue(TEXT("Replay has no second effect"),Restored==Future);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05Negative,"F05.P01.Negatives",Flags)
bool FF05Negative::RunTest(const FString&) {
 Campaign C;if(!TestTrue(TEXT("Ready"),C.Open() && C.Ready()))return false;
 auto Q=C.Request();Q.issuer=C.H.ensign;F05Receipt R{};TestEqual(TEXT("No command by skill"),f05_submit(C.Session,&Q,&R),uint32(F04_DENIED));
 Q=C.Request();Q.key=2;Q.recipient=C.H.doctor;TestEqual(TEXT("Wrong qualification"),f05_submit(C.Session,&Q,&R),uint32(F04_QUALIFICATION));
 Q=C.Request();Q.key=3;Q.operation=F04_BRIDGE;TestEqual(TEXT("Unsupported explicit refusal"),f05_submit(C.Session,&Q,&R),uint32(F05_UNSUPPORTED));
 TArray<uint8> A,B;C.Save(A);++Q.cause;TestEqual(TEXT("Key conflict"),f05_submit(C.Session,&Q,&R),uint32(F05_IDEMPOTENCY_CONFLICT));C.Save(B);TestTrue(TEXT("Conflict unchanged"),A==B);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05Visual,"F05.P01.WorldAndActorIndependence",Flags)
bool FF05Visual::RunTest(const FString&) {
 Campaign C;if(!TestTrue(TEXT("Ready"),C.Open() && C.Ready()))return false;
 auto Q=C.Request();F05Receipt R{};f05_submit(C.Session,&Q,&R);f05_receive(C.Session,C.H.ensign,C.Revision(),R.order,&R);
 TArray<uint8> A,B;C.Save(A);
 const auto WorldValues=UWorld::InitializationValues().AllowAudioPlayback(false).CreatePhysicsScene(false).CreateNavigation(false).CreateAISystem(false);
 UWorld* World=UWorld::CreateWorld(EWorldType::Game,false,NAME_None,nullptr,true,ERHIFeatureLevel::Num,&WorldValues);
 if(!TestNotNull(TEXT("Disposable UWorld"),World))return false;
 AActor* Marker=World->SpawnActor<AActor>();TestNotNull(TEXT("Presentation marker"),Marker);
 if(Marker)Marker->Destroy();World->DestroyWorld(false);C.Save(B);TestTrue(TEXT("Actor and world removal preserve order"),A==B);
 TestEqual(TEXT("Execute offscreen"),f05_execute_order(C.Session,C.H.ensign,C.Revision(),R.order,&R),uint32(F04_OK));TestEqual(TEXT("Completed"),R.state,uint32(F05_COMPLETED));return true;
}

namespace {
bool DelegationReady(Campaign& C){return C.Open() && C.Ready() && C.Op(C.H.captain,F04_ASSIGN,C.H.bridge,C.H.watch.id)==F04_OK && C.Op(C.H.captain,F04_DUTY,C.H.watch.id,C.H.bridge,28800)==F04_OK;}
uint32 Grant(Campaign& C,F05DelegationView& D,uint32 Mode=F05_DELEGATED_AUTONOMOUS){
 F05DelegationRequest Q{C.H.captain,C.H.watch,C.H.ship,{C.H.ship.scope,C.H.sensors},C.H.ensign,1000,C.Revision(),0,80,50201,0,F04_SENSORS,F04_SCAN,Mode,0};
 uint32 Code=f05_delegate(C.Session,&Q,&D);if(Code)return Code;
 F05DelegationChange Change{C.H.captain,D.id,1001,C.Revision(),50202,F05_ACTIVE,Mode};return f05_change_delegation(C.Session,&Change,&D);
}
uint32 DelegatedOrder(Campaign& C,uint64 D,F05Receipt& R){auto Q=C.Request();Q.issuer=C.H.watch;Q.deadline=80;return f05_submit_delegated(C.Session,&Q,D,&R);}
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05DelegationRevocation,"F05.P02.DelegationRevocationRecovery",Flags)
bool FF05DelegationRevocation::RunTest(const FString&){
 Campaign C;if(!TestTrue(TEXT("Real F04 campaign"),DelegationReady(C)))return false;
 F05DelegationView D{};F05Receipt R{};TestEqual(TEXT("Grant"),Grant(C,D),uint32(F04_OK));TestEqual(TEXT("Issue"),DelegatedOrder(C,D.id,R),uint32(F04_OK));
 TestEqual(TEXT("Accept without effect"),f05_receive(C.Session,C.H.ensign,C.Revision(),R.order,&R),uint32(F04_OK));
 TArray<uint8> Pending,Future,Restored;TestTrue(TEXT("Save pending delegation and task"),C.Save(Pending));
 F05DelegationChange Change{C.H.captain,D.id,1002,C.Revision(),50203,F05_REVOKED,F05_DELEGATED_AUTONOMOUS};TestEqual(TEXT("Revoke"),f05_change_delegation(C.Session,&Change,&D),uint32(F04_OK));
 TestEqual(TEXT("Reject pending effect"),f05_execute_order(C.Session,C.H.ensign,C.Revision(),R.order,&R),uint32(F04_REVOKED));
 F05ResultView Result{};TestEqual(TEXT("Result"),f05_result(C.Session,C.H.captain,R.order,&Result),uint32(F04_OK));TestEqual(TEXT("No Core scan"),Result.performed,uint32(0));C.Save(Future);
 TestTrue(TEXT("Restore"),C.Load(Pending));Change.actor=C.H.captain;Change.expected_revision=C.Revision();f05_change_delegation(C.Session,&Change,&D);f05_execute_order(C.Session,C.H.ensign,C.Revision(),R.order,&R);C.Save(Restored);TestTrue(TEXT("Exact revoked future"),Future==Restored);
 f05_execute_order(C.Session,C.H.ensign,0,R.order,&R);C.Save(Restored);TestTrue(TEXT("Retry unchanged"),Future==Restored);return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05DelegationModes,"F05.P02.ModesAndLimits",Flags)
bool FF05DelegationModes::RunTest(const FString&){
 Campaign C;if(!TestTrue(TEXT("Ready"),DelegationReady(C)))return false;F05DelegationView D{};F05Receipt R{};
 TestEqual(TEXT("Proposal grant"),Grant(C,D,F05_PROPOSAL_REQUIRES_APPROVAL),uint32(F04_OK));TestEqual(TEXT("Propose order"),DelegatedOrder(C,D.id,R),uint32(F04_OK));TArray<uint8> A,B;C.Save(A);
 TestEqual(TEXT("Requires approval"),f05_receive(C.Session,C.H.ensign,C.Revision(),R.order,&R),uint32(F04_REVIEW));C.Save(B);TestTrue(TEXT("Proposal has no effect"),A==B);
 const uint64 Order=R.order;
 TestEqual(TEXT("No self approval"),f05_approve_order(C.Session,C.H.watch,C.Revision(),R.order,1,&R),uint32(F04_DENIED));
 TestEqual(TEXT("Captain approval"),f05_approve_order(C.Session,C.H.captain,C.Revision(),Order,1,&R),uint32(F04_OK));
 TestEqual(TEXT("Accept approved"),f05_receive(C.Session,C.H.ensign,C.Revision(),R.order,&R),uint32(F04_OK));TestEqual(TEXT("Actual Core scan"),f05_execute_order(C.Session,C.H.ensign,C.Revision(),R.order,&R),uint32(F04_OK));
 F05DelegationRequest Q{C.H.watch,C.H.head,C.H.ship,{C.H.ship.scope,C.H.sensors},C.H.ensign,1003,C.Revision(),0,80,50201,D.id,F04_SENSORS,F04_SCAN,F05_DELEGATED_AUTONOMOUS,0};
 TestEqual(TEXT("Explicit subdelegation rejection"),f05_delegate(C.Session,&Q,&D),uint32(F05_UNSUPPORTED));return true;
}
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FF05DelegationChain,"F05.P02.ExpiryAndChainOfCommand",Flags)
bool FF05DelegationChain::RunTest(const FString&){
 Campaign C;if(!TestTrue(TEXT("Ready"),DelegationReady(C)))return false;F05DelegationView D{};F05Receipt R{};TestEqual(TEXT("Grant"),Grant(C,D),uint32(F04_OK));TestEqual(TEXT("Issue"),DelegatedOrder(C,D.id,R),uint32(F04_OK));f05_receive(C.Session,C.H.ensign,C.Revision(),R.order,&R);
 TestEqual(TEXT("Revoke original command appointment"),C.Op(C.H.captain,F04_REVOKE,D.origin),uint32(F04_OK));TestEqual(TEXT("F04 succession cannot rescue revoked origin"),f05_execute_order(C.Session,C.H.ensign,C.Revision(),R.order,&R),uint32(F04_REVOKED));
 Campaign E;if(!TestTrue(TEXT("Independent expiry campaign"),DelegationReady(E)))return false;Grant(E,D);DelegatedOrder(E,D.id,R);f05_receive(E.Session,E.H.ensign,E.Revision(),R.order,&R);uint64 N=0;TestEqual(TEXT("Core clock"),f04_advance(E.Session,80,4096,&N),uint32(F04_OK));TestEqual(TEXT("Exact expiry"),f05_execute_order(E.Session,E.H.ensign,E.Revision(),R.order,&R),uint32(F04_EXPIRED));return true;
}
#endif
