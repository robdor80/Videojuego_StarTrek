#include "STAutomaticDoor.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/SpectatorPawn.h"
#include "Components/BoxComponent.h"
#include "DrawDebugHelpers.h"

FSTDoorIntentEvaluation ASTAutomaticDoor::EvaluatePassageIntent(AActor* Requester) const {
 FSTDoorIntentEvaluation E;E.DoorwayOccupied=IsDoorwayOccupied();FName AccessReason;
 E.Authorized=EvaluateAccess(Requester,AccessReason);
 if(!IsValid(Requester)||!Requester->IsA<APawn>()||Requester->IsA<ASpectatorPawn>()){E.Reason=TEXT("UnsupportedRequester");return E;}
 const FTransform T=GetActorTransform();const FVector P=T.InverseTransformPosition(Requester->GetActorLocation());
 float Radius=0,HalfHeight=0;Requester->GetSimpleCollisionCylinder(Radius,HalfHeight);
 const FVector Center=ApproachSensor->GetRelativeLocation(),Ext=ApproachSensor->GetUnscaledBoxExtent();
 E.Nearby=FMath::Abs(P.X-Center.X)<=Ext.X+Radius&&FMath::Abs(P.Y-Center.Y)<=Ext.Y+Radius&&FMath::Abs(P.Z-Center.Z)<=Ext.Z+HalfHeight;
 if(!E.Nearby)return E;
 if(!bUsePassageIntent){E.HasIntent=true;E.Reason=TEXT("LegacyProximity");return E;}
 // Explicit use is a separate trusted input; EvaluateAccess still decides permission.
 if(bRequestedOpen&&RequestedActor.Get()==Requester){E.HasIntent=true;E.Reason=TEXT("ExplicitRequest");return E;}
 const float HalfLane=OpeningWidth*.5f-Radius-FMath::Max(PathClearance,0.f);
 if(HalfLane<0){E.Reason=TEXT("CapsuleTooWide");return E;}
 const FVector V=T.InverseTransformVectorNoScale(Requester->GetVelocity());const float Speed=V.Size2D();
 if(Speed>=FMath::Max(MovingSpeedThreshold,1.f)) {
  if(P.X*V.X>=0||FMath::Abs(V.X)<FMath::Max(MinNormalSpeed,1.f)||FMath::Abs(V.X)/Speed<FMath::Clamp(MinNormalFraction,0.f,1.f)){E.Reason=TEXT("ParallelOrDeparting");return E;}
  E.CrossingSeconds=-P.X/V.X;E.CrossingLateralCm=P.Y+V.Y*E.CrossingSeconds;
  // A fixed time horizon alone would detect a very slow pawn only after its capsule
  // already touches the shut leaves. Keep a minimum anticipation distance, while
  // still requiring real normal approach and a capsule-clear predicted crossing.
  if(E.CrossingSeconds<0||(E.CrossingSeconds>FMath::Max(PredictionHorizon,.1f)&&FMath::Abs(P.X)>FMath::Max(SlowApproachDistance,0.f))){E.Reason=TEXT("CrossingTooLate");return E;}
  E.HasIntent=FMath::Abs(E.CrossingLateralCm)<=HalfLane;E.Reason=E.HasIntent?TEXT("PredictedThresholdCrossing"):TEXT("TrajectoryMissesOpening");return E;
 }
 if(FMath::Abs(P.Y)>HalfLane||FMath::Abs(P.X)>FMath::Max(StationaryMaxDistance,0.f)){E.Reason=TEXT("StoppedOutsideEntryLane");return E;}
 const FVector Facing=T.InverseTransformVectorNoScale(Requester->GetActorForwardVector()).GetSafeNormal2D();
 const bool FacesDoor=(-FMath::Sign(P.X)*Facing.X)>=FMath::Clamp(StationaryFacingDot,0.f,1.f);
 const bool ClearEntry=FMath::Abs(P.X)<=FMath::Max(ClearEntryDistance,0.f)&&FMath::Abs(P.Y)<=HalfLane*FMath::Clamp(ClearEntryWidthFraction,0.f,1.f);
 E.HasIntent=FacesDoor||ClearEntry;E.Reason=ClearEntry?TEXT("StationaryClearEntry"):(FacesDoor?TEXT("StationaryFacingDoor"):TEXT("StoppedFacingAway"));return E;
}
bool ASTAutomaticDoor::UpdatePassageIntent(AActor* Pawn,float Dt) {
 if(!bUsePassageIntent)return true;
 const FSTDoorIntentEvaluation E=EvaluatePassageIntent(Pawn);
 float& Grace=IntentGrace.FindOrAdd(Pawn);
 if(E.HasIntent&&E.Nearby)Grace=FMath::Clamp(IntentGraceSeconds,0.f,1.f);
 else Grace=FMath::Max(0.f,Grace-Dt);
 return E.Nearby&&(E.HasIntent||Grace>0);
}
void ASTAutomaticDoor::DrawIntentDebug() const {
 if(!bDrawIntentDebug||!GetWorld())return;
 DrawDebugBox(GetWorld(),ApproachSensor->GetComponentLocation(),ApproachSensor->GetScaledBoxExtent(),ApproachSensor->GetComponentQuat(),FColor::Cyan,false,0,0,1);
 DrawDebugBox(GetWorld(),OccupancySensor->GetComponentLocation(),OccupancySensor->GetScaledBoxExtent(),OccupancySensor->GetComponentQuat(),FColor::Orange,false,0,0,2);
 for(AActor* P:QueryPawns(ApproachSensor)) {
  const auto E=EvaluatePassageIntent(P);const FColor C=E.DoorwayOccupied?FColor::Magenta:(!E.Authorized?FColor::Red:(E.HasIntent?FColor::Green:FColor::Silver));
  DrawDebugDirectionalArrow(GetWorld(),P->GetActorLocation(),P->GetActorLocation()+P->GetVelocity()*.3f,15,C,false,0,0,3);
  DrawDebugString(GetWorld(),P->GetActorLocation()+FVector(0,0,110),FString::Printf(TEXT("P=%d I=%d A=%d O=%d %s"),E.Nearby,E.HasIntent,E.Authorized,E.DoorwayOccupied,*E.Reason.ToString()),nullptr,C,0,true);
 }
}
