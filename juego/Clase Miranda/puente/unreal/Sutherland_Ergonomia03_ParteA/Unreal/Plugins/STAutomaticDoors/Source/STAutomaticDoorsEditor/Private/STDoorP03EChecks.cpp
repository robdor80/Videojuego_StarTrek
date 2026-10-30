#include "STAutomaticDoorTestLibrary.h"
#include "STAutomaticDoor.h"
#include "Components/StaticMeshComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Engine/World.h"
#include "AssetCompilingManager.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"

bool USTAutomaticDoorTestLibrary::SetValidationVelocity(ACharacter* P,FVector V) {
 if(!P||!P->HasAnyFlags(RF_Transient))return false;auto* C=P->GetCharacterMovement();
 P->SetActorTickEnabled(true);C->bRunPhysicsWithNoController=true;C->bUpdateOnlyIfRendered=false;
 C->SetUpdatedComponent(P->GetCapsuleComponent());C->Activate(true);C->SetComponentTickEnabled(true);
 if(C->MovementMode==MOVE_None)C->SetMovementMode(MOVE_Walking);
 C->bOrientRotationToMovement=false;C->bUseControllerDesiredRotation=false;
 C->MaxWalkSpeed=600;C->GroundFriction=0;C->BrakingDecelerationWalking=0;C->BrakingFrictionFactor=0;C->Velocity=V;return true;
}
FString USTAutomaticDoorTestLibrary::RunP03EIntentChecks(ASTAutomaticDoor* D) {
 if(!D)return TEXT("{\"error\":\"No D01\"}");
 FAssetCompilingManager::Get().FinishAllCompilation();D->LeftLeaf->RecreatePhysicsState();D->RightLeaf->RecreatePhysicsState();auto* W=D->GetWorld();
 const bool Built=D->bDestinationConstructed,Locked=D->bSecurityLocked,Allowed=D->bExternalAccessAllowed,Enabled=D->bUsePassageIntent,Proximity=D->bProximityEnabled;
 D->bDestinationConstructed=true;D->bSecurityLocked=false;D->bExternalAccessAllowed=true;D->bUsePassageIntent=true;D->bProximityEnabled=true;
 FActorSpawnParameters SP;SP.ObjectFlags=RF_Transient;SP.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 auto* P=W->SpawnActor<ACharacter>(ACharacter::StaticClass(),FTransform(D->GetActorLocation()+FVector(0,0,1000)),SP);
 P->GetCapsuleComponent()->SetCapsuleSize(35,90);P->GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));
 const FTransform T=D->GetActorTransform();auto O=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Cases;
 float MaxFraction=0;int Blocks=0;float MinApproachFraction=1;
 auto Put=[&](FVector V){P->SetActorLocation(T.TransformPosition(V),false);};
 auto Velocity=[&](FVector V){P->GetCharacterMovement()->Velocity=T.TransformVectorNoScale(V);};
 auto Prepare=[&](FVector Position,float Yaw=0){Put(FVector(-350,230,100));Velocity(FVector::ZeroVector);D->bDestinationConstructed=true;D->bSecurityLocked=false;D->bExternalAccessAllowed=true;D->bUsePassageIntent=true;D->bProximityEnabled=true;D->ResetClosed();Put(Position);P->SetActorRotation(FRotator(0,D->GetActorRotation().Yaw+Yaw,0));MaxFraction=0;Blocks=0;MinApproachFraction=1;};
 auto Run=[&](FVector V,float Seconds,bool Move=true){
  for(int I=0;I<FMath::CeilToInt(Seconds*60);I++){
   Velocity(V);D->AdvanceDoor(1.f/60);MaxFraction=FMath::Max(MaxFraction,D->OpenFraction);
   FVector Local=T.InverseTransformPosition(P->GetActorLocation());if(FMath::Abs(Local.X)<65)MinApproachFraction=FMath::Min(MinApproachFraction,D->OpenFraction);
   if(Move){FHitResult H;P->SetActorLocation(P->GetActorLocation()+T.TransformVectorNoScale(V)/60,true,&H);if(H.bBlockingHit)Blocks++;}
  }
 };
 auto Check=[&](const TCHAR* Name,bool Pass){const auto E=D->EvaluatePassageIntent(P);auto C=MakeShared<FJsonObject>();C->SetStringField(TEXT("name"),Name);C->SetBoolField(TEXT("pass"),Pass);C->SetNumberField(TEXT("fraction"),D->OpenFraction);C->SetNumberField(TEXT("max_fraction"),MaxFraction);C->SetNumberField(TEXT("blocked_character_steps"),Blocks);C->SetBoolField(TEXT("raw_intent"),E.HasIntent);C->SetBoolField(TEXT("authorized"),E.Authorized);C->SetBoolField(TEXT("occupied"),E.DoorwayOccupied);C->SetStringField(TEXT("reason"),E.Reason.ToString());Cases.Add(MakeShared<FJsonValueObject>(C));};
 Prepare(FVector(-330,0,100));Run(FVector(450,0,0),1.25f);Check(TEXT("frontal_450cm_s_crosses_without_stopping"),T.InverseTransformPosition(P->GetActorLocation()).X>150&&Blocks==0&&MinApproachFraction>.4f);
 Prepare(FVector(330,0,100),180);Run(FVector(-600,0,0),.85f);Check(TEXT("reverse_frontal_600cm_s_anticipated"),T.InverseTransformPosition(P->GetActorLocation()).X<-150&&Blocks==0&&MinApproachFraction>.4f);
 Prepare(FVector(110,0,100),180);Run(FVector(-20,0,0),11);Check(TEXT("very_slow_frontal_does_not_get_stuck_outside_time_horizon"),T.InverseTransformPosition(P->GetActorLocation()).X<-100&&Blocks==0);
 Prepare(FVector(100,-30,100),90);Run(FVector(0,20,0),1.4f);Check(TEXT("slow_parallel_inside_clear_entry_does_not_open"),MaxFraction==0&&Blocks==0);
 Prepare(FVector(130,-210,100),90);D->bUsePassageIntent=false;Run(FVector(0,180,0),2.34f);float LegacyMax=MaxFraction;
 Prepare(FVector(130,-210,100),90);Run(FVector(0,180,0),2.34f);O->SetNumberField(TEXT("parallel_legacy_max_fraction"),LegacyMax);O->SetNumberField(TEXT("parallel_intent_max_fraction"),MaxFraction);Check(TEXT("same_parallel_path_legacy_opens_new_stays_closed"),LegacyMax>.999f&&MaxFraction==0&&Blocks==0);
 Prepare(FVector(130,210,100),-90);Run(FVector(0,-180,0),2.34f);Check(TEXT("parallel_reverse_direction_stays_closed"),MaxFraction==0&&Blocks==0);
 Prepare(FVector(-130,-35,100),90);Run(FVector(0,140,0),.5f);Check(TEXT("parallel_inside_short_corridor_stays_closed"),MaxFraction==0&&Blocks==0);
 Prepare(FVector(-300,-60,100));Run(FVector(350,70,0),1.16f);Check(TEXT("diagonal_inside_crosses_without_exact_facing"),T.InverseTransformPosition(P->GetActorLocation()).X>90&&Blocks==0);
 Prepare(FVector(300,120,100),90);Run(FVector(-350,-140,0),1.16f);Check(TEXT("diagonal_outside_crosses_without_exact_facing"),T.InverseTransformPosition(P->GetActorLocation()).X<-90&&Blocks==0);
 Prepare(FVector(210,-50,100),90);Run(FVector(0,180,0),.3f);bool ParallelClosed=MaxFraction==0;Run(FVector(-400,0,0),1);Check(TEXT("parallel_turns_into_entry_and_crosses"),ParallelClosed&&Blocks==0&&T.InverseTransformPosition(P->GetActorLocation()).X<-150);
 Prepare(FVector(-180,0,100));Run(FVector::ZeroVector,1,false);Check(TEXT("stationary_facing_from_inside_opens"),D->OpenFraction>.999f);
 Prepare(FVector(180,0,100),180);Run(FVector::ZeroVector,1,false);Check(TEXT("stationary_facing_from_outside_opens"),D->OpenFraction>.999f);
 Prepare(FVector(180,0,100));Run(FVector::ZeroVector,1,false);Check(TEXT("stopped_facing_away_outside_entry_does_not_open"),MaxFraction==0);
 Prepare(FVector(90,0,100));Run(FVector::ZeroVector,1,false);Check(TEXT("stationary_clear_entry_can_open_without_continuous_motion"),D->OpenFraction>.999f);
 Prepare(FVector(180,120,100),180);Run(FVector::ZeroVector,1,false);Check(TEXT("stopped_lateral_outside_entry_lane_stays_closed"),MaxFraction==0);
 Prepare(FVector(180,0,100),180);Run(FVector(200,0,0),.8f);Check(TEXT("departing_character_does_not_open"),MaxFraction==0&&Blocks==0);
 Prepare(FVector(330,36,100),180);Run(FVector(-250,0,0),1.85f);Check(TEXT("near_opening_edge_valid_path_passes"),T.InverseTransformPosition(P->GetActorLocation()).X<-100&&Blocks==0);
 Prepare(FVector(300,70,100),180);Run(FVector(-280,0,0),.4f);Check(TEXT("trajectory_misses_capsule_clear_opening_stays_closed"),MaxFraction==0&&Blocks==0);
 Prepare(FVector(200,166,100),180);Run(FVector(-150,0,0),.3f);Check(TEXT("sensor_lateral_edge_does_not_open_by_proximity"),MaxFraction==0);
 Prepare(FVector(180,0,100),180);Run(FVector::ZeroVector,1,false);const int Reversals=D->ClosingReversalCount;
 for(int I=0;I<20;I++){float Dot=I%2?.57f:.53f;P->SetActorRotation(FRotator(0,D->GetActorRotation().Yaw+FMath::RadiansToDegrees(FMath::Acos(-Dot)),0));Run(FVector(0,I%2?14:16,0),.05f,false);}
 Check(TEXT("orientation_and_low_speed_jitter_do_not_oscillate"),D->OpenFraction>.999f&&D->ClosingReversalCount==Reversals);
 P->SetActorRotation(FRotator(0,D->GetActorRotation().Yaw,0));Run(FVector::ZeroVector,3,false);Check(TEXT("intent_expiry_and_delay_close_without_permanent_hold"),D->OpenFraction==0);
 Prepare(FVector(-180,0,100));Run(FVector::ZeroVector,1,false);Put(FVector(0,0,100));Velocity(FVector(0,180,0));D->bSecurityLocked=true;D->bExternalAccessAllowed=false;D->RequestClose();Run(FVector(0,180,0),2,false);
 Check(TEXT("occupied_threshold_overrides_no_intent_and_revoked_access"),D->OpenFraction>.999f&&D->IsDoorwayOccupied()&&!D->EvaluatePassageIntent(P).HasIntent&&!D->EvaluatePassageIntent(P).Authorized);
 Put(FVector(350,0,100));Run(FVector(180,0,0),3,false);Check(TEXT("closes_after_occupant_leaves_even_when_locked"),D->OpenFraction==0);
 Prepare(FVector(-180,0,100));Run(FVector::ZeroVector,1,false);Put(FVector(350,0,100));D->RequestClose();Run(FVector(0,0,0),.15f,false);int Before=D->ClosingReversalCount;float BeforeFraction=D->OpenFraction;Put(FVector(0,0,100));Run(FVector(0,180,0),.1f,false);Check(TEXT("no_intent_occupant_reverses_a_closing_door"),D->ClosingReversalCount>Before&&D->OpenFraction>BeforeFraction);
 Prepare(FVector(180,0,100),90);Velocity(FVector(0,150,0));bool NoRawIntent=!D->EvaluatePassageIntent(P).HasIntent;bool Accepted=D->RequestOpen(P);Run(FVector(0,150,0),.9f,false);Check(TEXT("explicit_simulated_NPC_request_has_priority_over_parallel_estimate"),NoRawIntent&&Accepted&&D->OpenFraction>.999f);
 for(int I=0;I<3;I++){
  Prepare(FVector(180,0,100),180);if(I==0)D->bDestinationConstructed=false;else if(I==1)D->bSecurityLocked=true;else D->bExternalAccessAllowed=false;
  Velocity(FVector(-300,0,0));bool Intent=D->EvaluatePassageIntent(P).HasIntent;bool Denied=!D->RequestOpen(P);Run(FVector(-300,0,0),1,false);
  Check(I==0?TEXT("unbuilt_denies_valid_intent_and_explicit_use"):I==1?TEXT("lock_denies_valid_intent_and_explicit_use"):TEXT("permission_denies_valid_intent_and_explicit_use"),Intent&&Denied&&MaxFraction==0);
 }
 P->Destroy();D->bDestinationConstructed=Built;D->bSecurityLocked=Locked;D->bExternalAccessAllowed=Allowed;D->bUsePassageIntent=Enabled;D->bProximityEnabled=Proximity;D->ResetClosed();
 O->SetArrayField(TEXT("cases"),Cases);int Passed=0;for(const auto& C:Cases)if(C->AsObject()->GetBoolField(TEXT("pass")))Passed++;
 O->SetNumberField(TEXT("passed"),Passed);O->SetNumberField(TEXT("total"),Cases.Num());O->SetBoolField(TEXT("all_pass"),Passed==Cases.Num());O->SetBoolField(TEXT("saved_assets"),false);
 FString Text;FJsonSerializer::Serialize(O,TJsonWriterFactory<>::Create(&Text));return Text;
}
