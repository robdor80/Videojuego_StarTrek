#include "STAutomaticDoorTestLibrary.h"
#include "STAutomaticDoor.h"
#include "Components/StaticMeshComponent.h"
#include "Engine/World.h"
#include "GameFramework/Character.h"
#include "AssetCompilingManager.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"

FString USTAutomaticDoorTestLibrary::RunP03DChecks(ASTAutomaticDoor* D) {
 auto O=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Cases,Poses,Contacts;
 if(!D||D->DoorId!=TEXT("DOOR_F07_001"))return TEXT("{\"error\":\"Wrong D01\"}");
 FAssetCompilingManager::Get().FinishAllCompilation();auto* W=D->GetWorld();
 D->LeftLeaf->RecreatePhysicsState();D->RightLeaf->RecreatePhysicsState();D->ResetClosed();
 auto Check=[&](FString Name,bool Pass){auto C=MakeShared<FJsonObject>();C->SetStringField(TEXT("name"),Name);C->SetBoolField(TEXT("pass"),Pass);Cases.Add(MakeShared<FJsonValueObject>(C));};
 const bool Built=D->bDestinationConstructed,Locked=D->bSecurityLocked,Allowed=D->bExternalAccessAllowed,Proximity=D->bProximityEnabled;
 FComponentQueryParams Q;Q.AddIgnoredActor(D);Q.bTraceComplex=false;
 for(int Side=0;Side<2;Side++){
  auto* C=Side?D->RightLeaf.Get():D->LeftLeaf.Get();FString Name=Side?TEXT("Right"):TEXT("Left");
  const FVector Original=C->GetRelativeLocation(),Start=C->GetComponentLocation(),Delta=D->GetActorTransform().TransformVectorNoScale(FVector(0,(Side?1:-1)*D->TravelDistance,0));
  auto Sweep=[&](FVector A,FVector B){TArray<FHitResult> Hits;W->ComponentSweepMultiByChannel(Hits,C,A,B,C->GetComponentQuat(),ECC_Pawn,Q);bool Block=false;
   for(const auto& H:Hits)if(H.bBlockingHit){Block=true;auto V=MakeShared<FJsonObject>();V->SetStringField(TEXT("leaf"),Name);V->SetStringField(TEXT("actor"),GetNameSafe(H.GetActor()));V->SetNumberField(TEXT("time"),H.Time);Contacts.Add(MakeShared<FJsonValueObject>(V));}return Block;};
  bool Clear=true;
  for(float F:{0.f,.25f,.5f,.75f,1.f}){
   auto P=MakeShared<FJsonObject>();P->SetStringField(TEXT("leaf"),Name);P->SetNumberField(TEXT("fraction"),F);
   bool A=Sweep(Start+Delta*F,Start+Delta*F),B=Sweep(Start,Start+Delta*F),E=Sweep(Start+Delta*F,Start);
   P->SetBoolField(TEXT("pose_blocked"),A);P->SetBoolField(TEXT("forward_blocked"),B);P->SetBoolField(TEXT("reverse_blocked"),E);Poses.Add(MakeShared<FJsonValueObject>(P));Clear&=!(A||B||E);
  }
  Check(Name+TEXT("_five_poses_and_continuous_convex_sweeps"),Clear);
  bool Moved=true;float Error=0;
  for(int Pass=0;Pass<2;Pass++)for(int I=0;I<=120;I++){
   float F=Pass?1.f-I/120.f:I/120.f;FVector Target=Original+FVector(0,(Side?1:-1)*D->TravelDistance*F,0);FHitResult H;C->SetRelativeLocation(Target,true,&H);
   Error=FMath::Max(Error,float((C->GetRelativeLocation()-Target).Size()));if(H.bBlockingHit)Moved=false;
  }
  O->SetNumberField(Name+TEXT("_movement_max_error_cm"),Error);Check(Name+TEXT("_242_actual_component_swept_steps_and_return"),Moved&&Error<.01f&&C->GetRelativeLocation().Equals(Original,.0001f));
 }
 auto Capsule=[&](float Y,UPrimitiveComponent* Expected){FHitResult H;FCollisionQueryParams C(SCENE_QUERY_STAT(P03DCapsule),false);auto T=D->GetActorTransform();bool Hit=W->SweepSingleByChannel(H,T.TransformPosition(FVector(-120,Y,110)),T.TransformPosition(FVector(120,Y,110)),FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(35,90),C);return Expected?(Hit&&H.GetComponent()==Expected):!Hit;};
 Check(TEXT("Left_closed_blocks_pawn_capsule"),Capsule(-41,D->LeftLeaf));Check(TEXT("Right_closed_blocks_pawn_capsule"),Capsule(41,D->RightLeaf));
 Check(TEXT("bridge_access_policy_still_locked_unbuilt"),!Built&&Locked&&!Allowed);
 FActorSpawnParameters SP;SP.ObjectFlags=RF_Transient;SP.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 auto* Pawn=W->SpawnActor<ACharacter>(ACharacter::StaticClass(),FTransform(D->GetActorLocation()+FVector(0,0,1000)),SP);
 Check(TEXT("bridge_rejects_open_request"),!D->RequestOpen(Pawn));
 D->bDestinationConstructed=true;D->bSecurityLocked=false;D->bExternalAccessAllowed=true;D->bProximityEnabled=false;
 bool Requested=D->RequestOpen(Pawn);float JointError=0;
 auto Measure=[&](){JointError=FMath::Max(JointError,float((D->LeftLeaf->GetRelativeLocation()-(D->LeftClosedLocation+FVector(0,-D->TravelDistance*D->OpenFraction,0))).Size()));JointError=FMath::Max(JointError,float((D->RightLeaf->GetRelativeLocation()-(D->RightClosedLocation+FVector(0,D->TravelDistance*D->OpenFraction,0))).Size()));};
 for(int I=0;I<122;I++){D->AdvanceDoor(D->MovementDuration/120);Measure();}
 Check(TEXT("joint_real_mechanism_reaches_full_open"),Requested&&D->OpenFraction>.999f&&JointError<.01f);
 Check(TEXT("full_open_left_center_right_passages_clear"),Capsule(-41,nullptr)&&Capsule(0,nullptr)&&Capsule(41,nullptr));
 Pawn->SetActorLocation(D->GetActorTransform().TransformPosition(FVector(0,0,110)),false);D->RequestClose();D->AdvanceDoor(D->CloseDelay+1);
 Check(TEXT("actual_character_in_D01_holds_both_leaves_open"),D->IsDoorwayOccupied()&&D->OpenFraction>.999f);
 Pawn->SetActorLocation(D->GetActorLocation()+FVector(0,0,1000),false);D->RequestClose();D->AdvanceDoor(.1f);int Before=D->ClosingReversalCount;
 Pawn->SetActorLocation(D->GetActorTransform().TransformPosition(FVector(0,0,110)),false);D->AdvanceDoor(.05f);
 Check(TEXT("actual_character_reverses_joint_closing"),D->ClosingReversalCount>Before&&D->DoorState==ESTDoorState::Opening);
 Pawn->SetActorLocation(D->GetActorLocation()+FVector(0,0,1000),false);D->RequestClose();
 for(int I=0;I<122;I++){D->AdvanceDoor(D->MovementDuration/120);Measure();}
 Check(TEXT("joint_returns_closed_without_collision_or_offset"),D->OpenFraction<.001f&&D->LeftLeaf->GetRelativeLocation().Equals(D->LeftClosedLocation,.0001f)&&D->RightLeaf->GetRelativeLocation().Equals(D->RightClosedLocation,.0001f)&&JointError<.01f);
 O->SetNumberField(TEXT("joint_max_sync_error_cm"),JointError);
 Pawn->Destroy();D->bDestinationConstructed=Built;D->bSecurityLocked=Locked;D->bExternalAccessAllowed=Allowed;D->bProximityEnabled=Proximity;D->ResetClosed();
 bool Solid=true;int Witnesses=0;
 for(float Sign:{-1.f,1.f})for(float Y:{92.f,110.f,130.f,150.f,170.f})for(float Z:{110.f,220.f,350.f}){
  FHitResult H;FCollisionQueryParams C(SCENE_QUERY_STAT(P03DPerimeter),false,D);auto T=D->GetActorTransform();
  if(!W->SweepSingleByChannel(H,T.TransformPosition(FVector(-80,Y*Sign,Z)),T.TransformPosition(FVector(80,Y*Sign,Z)),FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(35,90),C))Solid=false;Witnesses++;
 }
 Check(TEXT("both_housings_keep_pawn_perimeter_solid"),Solid);Check(TEXT("all_security_settings_restored"),D->bDestinationConstructed==Built&&D->bSecurityLocked==Locked&&D->bExternalAccessAllowed==Allowed&&D->bProximityEnabled==Proximity);
 O->SetNumberField(TEXT("casing_capsule_witnesses"),Witnesses);O->SetArrayField(TEXT("contacts"),Contacts);O->SetArrayField(TEXT("poses"),Poses);O->SetArrayField(TEXT("cases"),Cases);
 int Passed=0;for(const auto& C:Cases)if(C->AsObject()->GetBoolField(TEXT("pass")))Passed++;
 O->SetNumberField(TEXT("passed"),Passed);O->SetNumberField(TEXT("total"),Cases.Num());O->SetBoolField(TEXT("all_pass"),Passed==Cases.Num());O->SetBoolField(TEXT("saved_assets"),false);
 FString Text;FJsonSerializer::Serialize(O,TJsonWriterFactory<>::Create(&Text));return Text;
}
