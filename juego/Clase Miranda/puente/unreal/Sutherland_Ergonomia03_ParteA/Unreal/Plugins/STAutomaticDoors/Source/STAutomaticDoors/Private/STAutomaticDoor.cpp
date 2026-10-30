#include "STAutomaticDoor.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Engine/World.h"
#include "Engine/OverlapResult.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/SpectatorPawn.h"

ASTAutomaticDoor::ASTAutomaticDoor() {
 PrimaryActorTick.bCanEverTick=true;
 DoorRoot=CreateDefaultSubobject<USceneComponent>(TEXT("DoorRoot"));SetRootComponent(DoorRoot);
 LeftLeaf=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("LeftLeaf"));LeftLeaf->SetupAttachment(DoorRoot);
 RightLeaf=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("RightLeaf"));RightLeaf->SetupAttachment(DoorRoot);
 for(UStaticMeshComponent* Leaf:{LeftLeaf.Get(),RightLeaf.Get()}) {
  Leaf->SetMobility(EComponentMobility::Movable);Leaf->SetCollisionProfileName(TEXT("BlockAllDynamic"));
  Leaf->SetSimulatePhysics(false);Leaf->SetGenerateOverlapEvents(false);
 }
 ApproachSensor=CreateDefaultSubobject<UBoxComponent>(TEXT("ApproachSensor"));ApproachSensor->SetupAttachment(DoorRoot);
 OccupancySensor=CreateDefaultSubobject<UBoxComponent>(TEXT("OccupancySensor"));OccupancySensor->SetupAttachment(DoorRoot);
 for(UBoxComponent* Sensor:{ApproachSensor.Get(),OccupancySensor.Get()}) {
  Sensor->SetCollisionEnabled(ECollisionEnabled::NoCollision);Sensor->SetHiddenInGame(true);
 }
 ConfigureSensors();
}
void ASTAutomaticDoor::ConfigureSensors() {
 const float Height=FMath::Max(OpeningHeight,180.f);
 ApproachSensor->SetRelativeLocation(FVector(0,0,Height/2));
 ApproachSensor->SetBoxExtent(FVector(ProximityDepth,OpeningWidth/2+55,Height/2+15));
 OccupancySensor->SetRelativeLocation(FVector(0,0,Height/2));
 OccupancySensor->SetBoxExtent(FVector(65,OpeningWidth/2+15,Height/2+15));
}
void ASTAutomaticDoor::OnConstruction(const FTransform& T) {Super::OnConstruction(T);ConfigureSensors();ResetClosed();}
void ASTAutomaticDoor::BeginPlay() {Super::BeginPlay();ConfigureSensors();ResetClosed();}
void ASTAutomaticDoor::ResetClosed() {
 ConfigureSensors();
 OpenFraction=0;TimeWithoutDemand=0;bRequestedOpen=false;bSafetyReopen=false;bManualCloseRequested=false;PreviousNearby.Empty();
 RequestedActor.Reset();OpeningRequester.Reset();IntentGrace.Empty();
 LeftLeaf->SetRelativeLocation(LeftClosedLocation);RightLeaf->SetRelativeLocation(RightClosedLocation);
 LeftLeaf->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);RightLeaf->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
 DoorState=ESTDoorState::Closed;
}
TArray<AActor*> ASTAutomaticDoor::QueryPawns(const UBoxComponent* Sensor) const {
 TArray<AActor*> Found;if(!GetWorld()||!Sensor)return Found;
 TArray<FOverlapResult> Hits;
 FCollisionQueryParams Params(SCENE_QUERY_STAT(STDoorOccupants),false,this);
 GetWorld()->OverlapMultiByObjectType(Hits,Sensor->GetComponentLocation(),Sensor->GetComponentQuat(),
  FCollisionObjectQueryParams(ECC_Pawn),FCollisionShape::MakeBox(Sensor->GetScaledBoxExtent()),Params);
 for(const FOverlapResult& Hit:Hits) {AActor* A=Hit.GetActor();if(IsValid(A)&&A->IsA<APawn>()&&!A->IsA<ASpectatorPawn>())Found.AddUnique(A);}
 return Found;
}
bool ASTAutomaticDoor::IsDoorwayOccupied() const {return QueryPawns(OccupancySensor).Num()>0;}
bool ASTAutomaticDoor::CanActorUseDoor_Implementation(AActor* Requester) const {return bExternalAccessAllowed&&IsValid(Requester)&&Requester->IsA<APawn>()&&!Requester->IsA<ASpectatorPawn>();}
bool ASTAutomaticDoor::EvaluateAccess(AActor* Requester,FName& Reason) const {
 if(!IsValid(Requester)||!Requester->IsA<APawn>()||Requester->IsA<ASpectatorPawn>()){Reason=TEXT("UnsupportedRequester");return false;}
 if(!bDestinationConstructed){Reason=TEXT("DestinationNotConstructed");return false;}
 if(bSecurityLocked){Reason=TEXT("SecurityLocked");return false;}
 if(!CanActorUseDoor(Requester)){Reason=TEXT("PermissionDenied");return false;}
 Reason=TEXT("Granted");return true;
}
bool ASTAutomaticDoor::RequestOpen(AActor* Requester) {
 FName Reason;const bool Granted=EvaluateAccess(Requester,Reason);OnAccessEvaluated.Broadcast(Requester,Granted,Reason);
 if(Granted){bRequestedOpen=true;RequestedActor=Requester;bManualCloseRequested=false;TimeWithoutDemand=0;}
 return Granted;
}
void ASTAutomaticDoor::RequestClose(){bRequestedOpen=false;bManualCloseRequested=true;TimeWithoutDemand=CloseDelay;}
void ASTAutomaticDoor::SetSecurityLocked(bool Locked){bSecurityLocked=Locked;if(Locked)bRequestedOpen=false;}
void ASTAutomaticDoor::SetDestinationConstructed(bool Built){bDestinationConstructed=Built;if(!Built)bRequestedOpen=false;}
void ASTAutomaticDoor::SetExternalAccessAllowed(bool Allowed){bExternalAccessAllowed=Allowed;if(!Allowed)bRequestedOpen=false;}
void ASTAutomaticDoor::ChangeState(ESTDoorState State){if(State!=DoorState){ESTDoorState Old=DoorState;DoorState=State;OnDoorStateChanged.Broadcast(Old,State);}}
void ASTAutomaticDoor::Tick(float Dt){Super::Tick(Dt);AdvanceDoor(Dt);DrawIntentDebug();}
void ASTAutomaticDoor::AdvanceDoor(float Dt) {
 if(Dt<=0||!GetWorld())return;
 const auto Nearby=QueryPawns(ApproachSensor);TSet<TWeakObjectPtr<AActor>> Now;
 FName RequestReason;
 const bool RequestedAuthorized=bRequestedOpen&&RequestedActor.IsValid()&&EvaluateAccess(RequestedActor.Get(),RequestReason);
 bool Demand=bSafetyReopen||RequestedAuthorized;
 if(RequestedAuthorized)OpeningRequester=RequestedActor;
 for(AActor* Pawn:Nearby) {
  Now.Add(Pawn);FName Reason;bool Granted=EvaluateAccess(Pawn,Reason);
  if(!PreviousNearby.Contains(Pawn))OnAccessEvaluated.Broadcast(Pawn,Granted,Reason);
  const bool Intent=UpdatePassageIntent(Pawn,Dt);
  if(Granted&&Intent&&bProximityEnabled&&!bManualCloseRequested){Demand=true;OpeningRequester=Pawn;}
 }
 for(auto It=IntentGrace.CreateIterator();It;++It)if(!It.Key().IsValid()||!Now.Contains(It.Key()))It.RemoveCurrent();
 if(Nearby.IsEmpty())bManualCloseRequested=false;
 PreviousNearby=MoveTemp(Now);bRequestedOpen=false;
 const bool Occupied=IsDoorwayOccupied();
 if(Occupied&&OpenFraction>0) {
  if(DoorState==ESTDoorState::Closing){ClosingReversalCount++;}
  Demand=true;
 }
 bool Opening=false;
 if(Demand){TimeWithoutDemand=0;Opening=true;}
 else {
  TimeWithoutDemand+=Dt;
  FName ContinuationReason;
  const bool CompleteOpening=DoorState==ESTDoorState::Opening&&OpeningRequester.IsValid()&&EvaluateAccess(OpeningRequester.Get(),ContinuationReason);
  if(TimeWithoutDemand<CloseDelay){if(!CompleteOpening)return;Opening=true;}
 }
 const float Target=FMath::Clamp(OpenFraction+(Opening?1.f:-1.f)*Dt/FMath::Max(MovementDuration,.05f),0.f,1.f);
 if(FMath::IsNearlyEqual(Target,OpenFraction)) {ChangeState(Target>.999f?ESTDoorState::Open:ESTDoorState::Closed);return;}
 ChangeState(Opening?ESTDoorState::Opening:ESTDoorState::Closing);
 FHitResult LHit,RHit;
 LeftLeaf->SetRelativeLocation(LeftClosedLocation+FVector(0,-TravelDistance*Target,0),true,&LHit);
 RightLeaf->SetRelativeLocation(RightClosedLocation+FVector(0,TravelDistance*Target,0),true,&RHit);
 if(LHit.bBlockingHit||RHit.bBlockingHit) {
  const float LF=FMath::Clamp((LeftClosedLocation.Y-LeftLeaf->GetRelativeLocation().Y)/FMath::Max(TravelDistance,.01f),0.f,1.f);
  const float RF=FMath::Clamp((RightLeaf->GetRelativeLocation().Y-RightClosedLocation.Y)/FMath::Max(TravelDistance,.01f),0.f,1.f);
  OpenFraction=Opening?FMath::Min(LF,RF):FMath::Max(LF,RF);
  if(!Opening){ClosingReversalCount++;bSafetyReopen=true;TimeWithoutDemand=0;ChangeState(ESTDoorState::Opening);}
  else ChangeState(ESTDoorState::Obstructed);
  return;
 }
 OpenFraction=Target;
 if(Target>=.999f){bSafetyReopen=false;ChangeState(ESTDoorState::Open);}else if(Target<=.001f)ChangeState(ESTDoorState::Closed);
}
