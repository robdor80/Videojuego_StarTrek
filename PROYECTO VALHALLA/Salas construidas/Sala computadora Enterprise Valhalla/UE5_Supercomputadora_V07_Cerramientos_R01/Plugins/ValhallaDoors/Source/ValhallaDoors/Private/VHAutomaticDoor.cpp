#include "VHAutomaticDoor.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Engine/World.h"
#include "Engine/OverlapResult.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/SpectatorPawn.h"

AVHAutomaticDoor::AVHAutomaticDoor() {
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
void AVHAutomaticDoor::ConfigureSensors() {
 const float Height=FMath::Max(OpeningHeight,180.f);
 ApproachSensor->SetRelativeLocation(FVector(0,0,Height/2));
 ApproachSensor->SetBoxExtent(FVector(ProximityDepth,OpeningWidth/2+55,Height/2+15));
 OccupancySensor->SetRelativeLocation(FVector(0,0,Height/2));
 OccupancySensor->SetBoxExtent(FVector(65,OpeningWidth/2+15,Height/2+15));
}
void AVHAutomaticDoor::OnConstruction(const FTransform& T) {Super::OnConstruction(T);ConfigureSensors();ResetClosed();}
void AVHAutomaticDoor::BeginPlay() {Super::BeginPlay();ConfigureSensors();ResetClosed();}
void AVHAutomaticDoor::ResetClosed() {
 ConfigureSensors();
 OpenFraction=0;TimeWithoutDemand=0;bRequestedOpen=false;bSafetyReopen=false;bManualCloseRequested=false;PreviousNearby.Empty();
 RequestedActor.Reset();OpeningRequester.Reset();IntentGrace.Empty();
 LastBlockingMesh.Reset();LastBlockingNormal=FVector::ZeroVector;LastPenetrationDepth=0;bLastStartPenetrating=false;
 LeftLeaf->SetRelativeLocation(LeftClosedLocation);RightLeaf->SetRelativeLocation(RightClosedLocation);
 LeftLeaf->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);RightLeaf->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
 DoorState=(bSecurityLocked||!bDestinationConstructed||!bExternalAccessAllowed)?EVHDoorState::Blocked:EVHDoorState::Closed;
}
TArray<AActor*> AVHAutomaticDoor::QueryPawns(const UBoxComponent* Sensor) const {
 TArray<AActor*> Found;if(!GetWorld()||!Sensor)return Found;
 TArray<FOverlapResult> Hits;
 FCollisionQueryParams Params(SCENE_QUERY_STAT(VHDoorOccupants),false,this);
 GetWorld()->OverlapMultiByObjectType(Hits,Sensor->GetComponentLocation(),Sensor->GetComponentQuat(),
  FCollisionObjectQueryParams(ECC_Pawn),FCollisionShape::MakeBox(Sensor->GetScaledBoxExtent()),Params);
 for(const FOverlapResult& Hit:Hits) {AActor* A=Hit.GetActor();if(IsValid(A)&&A->IsA<APawn>()&&!A->IsA<ASpectatorPawn>())Found.AddUnique(A);}
 return Found;
}
bool AVHAutomaticDoor::IsDoorwayOccupied() const {return QueryPawns(OccupancySensor).Num()>0;}
bool AVHAutomaticDoor::CanActorUseDoor_Implementation(AActor* Requester) const {return bExternalAccessAllowed&&IsValid(Requester)&&Requester->IsA<APawn>()&&!Requester->IsA<ASpectatorPawn>();}
bool AVHAutomaticDoor::EvaluateAccess(AActor* Requester,FName& Reason) const {
 if(!IsValid(Requester)||!Requester->IsA<APawn>()||Requester->IsA<ASpectatorPawn>()){Reason=TEXT("UnsupportedRequester");return false;}
 if(!bDestinationConstructed){Reason=TEXT("DestinationNotConstructed");return false;}
 if(bSecurityLocked){Reason=TEXT("SecurityLocked");return false;}
 if(!CanActorUseDoor(Requester)){Reason=TEXT("PermissionDenied");return false;}
 Reason=TEXT("Granted");return true;
}
bool AVHAutomaticDoor::RequestOpen(AActor* Requester) {
 FName Reason;const bool Granted=EvaluateAccess(Requester,Reason);OnAccessEvaluated.Broadcast(Requester,Granted,Reason);
 if(Granted){bRequestedOpen=true;RequestedActor=Requester;bManualCloseRequested=false;TimeWithoutDemand=0;}
 return Granted;
}
void AVHAutomaticDoor::RequestClose(){bRequestedOpen=false;bManualCloseRequested=true;TimeWithoutDemand=CloseDelay;}
void AVHAutomaticDoor::SetSecurityLocked(bool Locked){bSecurityLocked=Locked;if(Locked)bRequestedOpen=false;}
void AVHAutomaticDoor::SetDestinationConstructed(bool Built){bDestinationConstructed=Built;if(!Built)bRequestedOpen=false;}
void AVHAutomaticDoor::SetExternalAccessAllowed(bool Allowed){bExternalAccessAllowed=Allowed;if(!Allowed)bRequestedOpen=false;}
void AVHAutomaticDoor::SetEmergencyHoldOpen(bool Hold){bEmergencyHoldOpen=Hold;TimeWithoutDemand=0;}
void AVHAutomaticDoor::ChangeState(EVHDoorState State){if(State!=DoorState){EVHDoorState Old=DoorState;DoorState=State;OnDoorStateChanged.Broadcast(Old,State);}}
void AVHAutomaticDoor::Tick(float Dt){Super::Tick(Dt);AdvanceDoor(Dt);DrawIntentDebug();}
FVector AVHAutomaticDoor::LeafLocationAtFraction(bool Left,float Fraction) const {
 const float F=FMath::Clamp(Fraction,0.f,1.f);
 const FVector Closed=Left?LeftClosedLocation:RightClosedLocation;
 const FVector Travel=bUseConfiguredTravel?(Left?LeftTravel:RightTravel):FVector(0,Left?-TravelDistance:TravelDistance,0);
 const FVector Offset=bUseConfiguredTravel?(Left?LeftClearanceOffset:RightClearanceOffset):FVector::ZeroVector;
 if(Offset.IsNearlyZero())return Closed+Travel*F;
 const float C=FMath::Clamp(ClearanceFraction,.05f,.95f);
 return Closed+Offset*FMath::Min(F/C,1.f)+Travel*FMath::Max((F-C)/(1-C),0.f);
}
float AVHAutomaticDoor::FractionAtLeafLocation(bool Left) const {
 const FVector Closed=Left?LeftClosedLocation:RightClosedLocation;
 const FVector P=(Left?LeftLeaf:RightLeaf)->GetRelativeLocation()-Closed;
 const FVector Travel=bUseConfiguredTravel?(Left?LeftTravel:RightTravel):FVector(0,Left?-TravelDistance:TravelDistance,0);
 const FVector Offset=bUseConfiguredTravel?(Left?LeftClearanceOffset:RightClearanceOffset):FVector::ZeroVector;
 if(Offset.IsNearlyZero())return Travel.IsNearlyZero()?OpenFraction:FMath::Clamp(FVector::DotProduct(P,Travel)/Travel.SizeSquared(),0.f,1.f);
 const float C=FMath::Clamp(ClearanceFraction,.05f,.95f);
 const float Sliding=Travel.IsNearlyZero()?0:FVector::DotProduct(P-Offset,Travel)/Travel.SizeSquared();
 if(Sliding>0)return C+(1-C)*FMath::Clamp(Sliding,0.f,1.f);
 return C*FMath::Clamp(FVector::DotProduct(P,Offset)/Offset.SizeSquared(),0.f,1.f);
}
void AVHAutomaticDoor::AdvanceDoor(float Dt) {
 if(Dt<=0||!GetWorld())return;
 const auto Nearby=QueryPawns(ApproachSensor);TSet<TWeakObjectPtr<AActor>> Now;
 FName RequestReason;
 const bool RequestedAuthorized=bRequestedOpen&&RequestedActor.IsValid()&&EvaluateAccess(RequestedActor.Get(),RequestReason);
 bool Demand=(bEmergencyHoldOpen&&bDestinationConstructed)||bSafetyReopen||RequestedAuthorized;
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
  if(DoorState==EVHDoorState::Closing){ClosingReversalCount++;}
  Demand=true;
 }
 bool Opening=false;
 if(Demand){TimeWithoutDemand=0;Opening=true;}
 else {
  TimeWithoutDemand+=Dt;
  FName ContinuationReason;
  const bool CompleteOpening=DoorState==EVHDoorState::Opening&&OpeningRequester.IsValid()&&EvaluateAccess(OpeningRequester.Get(),ContinuationReason);
  if(TimeWithoutDemand<CloseDelay){if(!CompleteOpening)return;Opening=true;}
 }
 float Target=FMath::Clamp(OpenFraction+(Opening?1.f:-1.f)*Dt/FMath::Max(MovementDuration,.05f),0.f,1.f);
 if(bUseConfiguredTravel&&(!LeftClearanceOffset.IsNearlyZero()||!RightClearanceOffset.IsNearlyZero())){
  const float C=FMath::Clamp(ClearanceFraction,.05f,.95f);
  if((OpenFraction<C&&Target>C)||(OpenFraction>C&&Target<C))Target=C;
 }
 if(FMath::IsNearlyEqual(Target,OpenFraction)) {ChangeState(Target>.999f?EVHDoorState::Open:((bSecurityLocked||!bDestinationConstructed||!bExternalAccessAllowed)?EVHDoorState::Blocked:EVHDoorState::Closed));return;}
 ChangeState(Opening?EVHDoorState::Opening:EVHDoorState::Closing);
 FHitResult LHit,RHit;
 LeftLeaf->SetRelativeLocation(LeafLocationAtFraction(true,Target),true,&LHit);
 RightLeaf->SetRelativeLocation(LeafLocationAtFraction(false,Target),true,&RHit);
 if(LHit.bBlockingHit||RHit.bBlockingHit) {
  const FHitResult& H=LHit.bBlockingHit?LHit:RHit;auto* HitMesh=Cast<UStaticMeshComponent>(H.GetComponent());LastBlockingMesh=HitMesh&&HitMesh->GetStaticMesh()?HitMesh->GetStaticMesh()->GetPathName():(H.GetComponent()?H.GetComponent()->GetName():TEXT("Unknown"));LastBlockingNormal=H.ImpactNormal;LastPenetrationDepth=H.PenetrationDepth;bLastStartPenetrating=H.bStartPenetrating;
  const float LF=LeftLeaf->GetStaticMesh()?FractionAtLeafLocation(true):Target;
  const float RF=RightLeaf->GetStaticMesh()?FractionAtLeafLocation(false):Target;
  OpenFraction=Opening?FMath::Min(LF,RF):FMath::Max(LF,RF);
  if(!Opening){ClosingReversalCount++;bSafetyReopen=true;TimeWithoutDemand=0;ChangeState(EVHDoorState::Opening);}
  else ChangeState(EVHDoorState::Blocked);
  return;
 }
 OpenFraction=Target;
 if(Target>=.999f){bSafetyReopen=false;ChangeState(EVHDoorState::Open);}else if(Target<=.001f)ChangeState((bSecurityLocked||!bDestinationConstructed||!bExternalAccessAllowed)?EVHDoorState::Blocked:EVHDoorState::Closed);
}
