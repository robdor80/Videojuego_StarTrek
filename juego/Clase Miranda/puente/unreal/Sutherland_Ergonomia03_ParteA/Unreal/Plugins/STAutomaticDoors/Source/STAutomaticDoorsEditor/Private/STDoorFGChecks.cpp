#include "STAutomaticDoorTestLibrary.h"
#include "STAutomaticDoor.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Components/CapsuleComponent.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"
#include "PhysicsEngine/BodySetup.h"
#include "GameFramework/Character.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "AssetCompilingManager.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"
bool USTAutomaticDoorTestLibrary::ConfigureFGLeafCollision(UStaticMesh* M,int32 Slices){
 if(!M||!M->GetPathName().StartsWith(TEXT("/Game/F07P03FG/Leaves/"))||Slices<1||Slices>8)return false;
 FAssetCompilingManager::Get().FinishAllCompilation();const auto& L=M->GetRenderData()->LODResources[0];const auto& P=L.VertexBuffers.PositionVertexBuffer;TArray<FVector> V;float Low=MAX_flt,High=-MAX_flt;
 for(uint32 I=0;I<P.GetNumVertices();I++){FVector X(P.VertexPosition(I));V.Add(X);Low=FMath::Min(Low,float(X.Z));High=FMath::Max(High,float(X.Z));}
 M->CreateBodySetup();auto* B=M->GetBodySetup();if(B->GetOuter()!=M)return false;B->AggGeom.EmptyElements();
 for(int32 Slice=0;Slice<Slices;Slice++){
  float A=FMath::Lerp(Low,High,float(Slice)/Slices),Z=FMath::Lerp(Low,High,float(Slice+1)/Slices);FKConvexElem C;
  auto Add=[&](FVector X){for(const auto& Y:C.VertexData)if(X.Equals(Y,.00001))return;C.VertexData.Add(X);};
  for(auto X:V)if(X.Z>=A-.00001&&X.Z<=Z+.00001)Add(X);
  for(int I=0;I<L.IndexBuffer.GetNumIndices();I+=3)for(int E=0;E<3;E++){auto X=V[L.IndexBuffer.GetIndex(I+E)],Y=V[L.IndexBuffer.GetIndex(I+(E+1)%3)];for(float Plane:{A,Z})if((X.Z-Plane)*(Y.Z-Plane)<0)Add(X+(Y-X)*((Plane-X.Z)/(Y.Z-X.Z)));}
  if(C.VertexData.Num()<4)return false;C.UpdateElemBox();B->AggGeom.ConvexElems.Add(C);
 }
 B->CollisionTraceFlag=CTF_UseSimpleAndComplex;B->InvalidatePhysicsData();B->CreatePhysicsMeshes();M->MarkPackageDirty();return true;
}

AActor* USTAutomaticDoorTestLibrary::CreateFGDestinationGuard(ASTAutomaticDoor* D){
 if(!D||D->bDestinationConstructed)return nullptr;auto* W=D->GetWorld();FName Tag(*(FString(TEXT("FG_Guard_"))+D->DoorId.ToString()));
 for(TActorIterator<AActor> It(W);It;++It)if(It->ActorHasTag(Tag))return *It;
 FActorSpawnParameters SP;SP.ObjectFlags=RF_Transactional;auto* Guard=W->SpawnActor<AActor>(AActor::StaticClass(),D->GetActorTransform(),SP);Guard->Tags.Add(Tag);Guard->SetActorLabel(TEXT("NO_DESTINATION_GUARD_")+D->DoorId.ToString());auto* Box=NewObject<UBoxComponent>(Guard,TEXT("PawnSafetyBarrier"));Guard->SetRootComponent(Box);Guard->AddInstanceComponent(Box);
 const float Low=-D->GetActorLocation().Z-10,High=D->OpeningHeight+10;Box->SetBoxExtent(FVector(2,D->OpeningWidth*.5f+2,(High-Low)*.5f));Box->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);Box->SetCollisionObjectType(ECC_WorldStatic);Box->SetCollisionResponseToAllChannels(ECR_Ignore);Box->SetCollisionResponseToChannel(ECC_Pawn,ECR_Block);Box->RegisterComponent();Box->SetWorldTransform(D->GetActorTransform());
 // Barrier remains inside the already constructed bridge. It blocks Pawns,
 // while the leaf's WorldDynamic query remains independent of this safety gate.
 Box->SetWorldLocation(D->GetActorTransform().TransformPosition(FVector(-100,0,(High+Low)*.5f)));Guard->SetActorHiddenInGame(true);return Guard;
}

FString USTAutomaticDoorTestLibrary::RunFGDoorChecks(ASTAutomaticDoor* D,bool ExpectGuard){
 if(!D)return TEXT("{\"error\":\"Missing door\"}");FAssetCompilingManager::Get().FinishAllCompilation();auto* W=D->GetWorld();D->LeftLeaf->RecreatePhysicsState();D->RightLeaf->RecreatePhysicsState();D->ResetClosed();const FTransform T=D->GetActorTransform();
 auto O=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Cases,Rows,HitsOut;auto Check=[&](FString N,bool B){auto C=MakeShared<FJsonObject>();C->SetStringField(TEXT("name"),N);C->SetBoolField(TEXT("pass"),B);Cases.Add(MakeShared<FJsonValueObject>(C));};
 AActor* Guard=nullptr;for(TActorIterator<AActor> It(W);It;++It)if(It->ActorHasTag(FName(*(FString(TEXT("FG_Guard_"))+D->DoorId.ToString()))))Guard=*It;
 const bool Built=D->bDestinationConstructed,Locked=D->bSecurityLocked,Allowed=D->bExternalAccessAllowed,Proximity=D->bProximityEnabled,Intent=D->bUsePassageIntent;D->bProximityEnabled=false;
 FComponentQueryParams Q;Q.AddIgnoredActor(D);Q.bTraceComplex=false;
 for(int Side=0;Side<2;Side++){
  auto* C=Side?D->RightLeaf.Get():D->LeftLeaf.Get();auto Name=Side?FString(TEXT("Right")):FString(TEXT("Left"));const FVector Original=C->GetRelativeLocation(),Start=C->GetComponentLocation(),Delta=T.TransformVectorNoScale(FVector(0,(Side?1:-1)*D->TravelDistance,0));bool Clear=true;TArray<TSharedPtr<FJsonValue>> Poses;
  auto Sweep=[&](FVector A,FVector B){TArray<FHitResult> H;W->ComponentSweepMultiByChannel(H,C,A,B,C->GetComponentQuat(),ECC_WorldDynamic,Q);bool Block=false;for(auto& Hit:H)if(Hit.bBlockingHit){Block=true;auto J=MakeShared<FJsonObject>();J->SetStringField(TEXT("leaf"),Name);J->SetStringField(TEXT("actor"),GetNameSafe(Hit.GetActor()));J->SetStringField(TEXT("label"),Hit.GetActor()?Hit.GetActor()->GetActorLabel():TEXT("None"));J->SetStringField(TEXT("mesh_component"),GetNameSafe(Hit.GetComponent()));J->SetStringField(TEXT("impact"),T.InverseTransformPosition(Hit.ImpactPoint).ToString());J->SetStringField(TEXT("normal"),Hit.ImpactNormal.ToString());J->SetStringField(TEXT("start"),T.InverseTransformPosition(A).ToString());J->SetStringField(TEXT("end"),T.InverseTransformPosition(B).ToString());J->SetNumberField(TEXT("penetration_depth"),Hit.PenetrationDepth);J->SetNumberField(TEXT("time"),Hit.Time);HitsOut.Add(MakeShared<FJsonValueObject>(J));}return Block;};
  for(float F:{0.f,.25f,.5f,.75f,1.f}){bool Block=Sweep(Start+Delta*F,Start+Delta*F)||Sweep(Start,Start+Delta*F)||Sweep(Start+Delta*F,Start);auto P=MakeShared<FJsonObject>();P->SetNumberField(TEXT("fraction"),F);P->SetBoolField(TEXT("blocked"),Block);Poses.Add(MakeShared<FJsonValueObject>(P));Clear&=!Block;}
  float Error=0;bool Moves=true;for(int Pass=0;Pass<2;Pass++)for(int I=0;I<=120;I++){float F=Pass?1.f-I/120.f:I/120.f;FVector Target=Original+FVector(0,(Side?1:-1)*D->TravelDistance*F,0);FHitResult H;C->SetRelativeLocation(Target,true,&H);Error=FMath::Max(Error,float((C->GetRelativeLocation()-Target).Size()));Moves&=!H.bBlockingHit;}
  Check(Name+TEXT("_five_poses_continuous_forward_reverse"),Clear);Check(Name+TEXT("_242_swept_component_steps_and_exact_return"),Moves&&Error<.01f&&C->GetRelativeLocation().Equals(Original,.0001));auto Row=MakeShared<FJsonObject>();Row->SetStringField(TEXT("leaf"),Name);Row->SetArrayField(TEXT("poses"),Poses);Row->SetNumberField(TEXT("movement_error_cm"),Error);Row->SetNumberField(TEXT("travel_cm"),D->TravelDistance);Rows.Add(MakeShared<FJsonValueObject>(Row));
 }
 FActorSpawnParameters SP;SP.ObjectFlags=RF_Transient;SP.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;auto* P=W->SpawnActor<ACharacter>(ACharacter::StaticClass(),FTransform(T.TransformPosition(FVector(0,0,1000))),SP);P->GetCapsuleComponent()->SetCapsuleSize(35,90);P->GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));
 TArray<TSharedPtr<FJsonValue>> CapsuleProfiles;
 auto Capsule=[&](float Y,bool IgnoreGuard){FHitResult H;FCollisionQueryParams C(SCENE_QUERY_STAT(FGPassage),false);C.AddIgnoredActor(P);if(IgnoreGuard&&Guard)C.AddIgnoredActor(Guard);bool Hit=W->SweepSingleByChannel(H,T.TransformPosition(FVector(-120,Y,110)),T.TransformPosition(FVector(36,Y,110)),FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(35,90),C);auto J=MakeShared<FJsonObject>();J->SetNumberField(TEXT("Y"),Y);J->SetNumberField(TEXT("door_fraction"),D->OpenFraction);J->SetBoolField(TEXT("hit"),Hit);J->SetStringField(TEXT("actor"),H.GetActor()?H.GetActor()->GetActorLabel():TEXT("None"));J->SetStringField(TEXT("point_local"),T.InverseTransformPosition(H.ImpactPoint).ToString());CapsuleProfiles.Add(MakeShared<FJsonValueObject>(J));return TPair<bool,UPrimitiveComponent*>(Hit,H.GetComponent());};
 auto Closed=Capsule(0,true);Check(TEXT("closed_real_leaves_block_pawn"),Closed.Key&&(Closed.Value==D->LeftLeaf||Closed.Value==D->RightLeaf));
 for(int Side:{-1,1}){P->SetActorLocation(T.TransformPosition(FVector(Side<0?-60:60,0,110)),false);P->SetActorRotation(FRotator(0,D->GetActorRotation().Yaw+(Side>0?180:0),0));auto E=D->EvaluatePassageIntent(P);bool Accepted=D->RequestOpen(P);Check(Side<0?TEXT("inside_intent_and_access_policy"):TEXT("outside_intent_and_access_policy"),E.HasIntent&&(Accepted==(Built&&!Locked&&Allowed)));D->ResetClosed();}
 // Only static opaque manufactured housings count as hiding a leaf. Ignore
 // cabin walls and every unrelated obstacle, so they cannot mask a missing shell.
 FCollisionQueryParams Occlusion(SCENE_QUERY_STAT(FGPocketOnly),true);int Shells=0;
 for(TActorIterator<AActor> It(W);It;++It){bool IsAssembly=false,IsShell=false;TArray<UStaticMeshComponent*> Components;It->GetComponents<UStaticMeshComponent>(Components);for(auto* C:Components)if(C->GetStaticMesh()){auto N=C->GetStaticMesh()->GetName();IsShell|=N.Contains(TEXT("PocketShell"));IsAssembly|=N.Contains(TEXT("PocketShell"))||N.Contains(TEXT("TrackFront"))||N.Contains(TEXT("TrackRear"))||N.Contains(TEXT("UpperReturn"))||N.Contains(TEXT("LowerReturn"));}if(IsAssembly&&!It->IsHidden()){Shells+=IsShell;}else Occlusion.AddIgnoredActor(*It);}
 int Hidden=0,Tested=0;
 for(int Side=0;Side<2;Side++){
  auto* C=Side?D->RightLeaf.Get():D->LeftLeaf.Get();const FVector Original=C->GetRelativeLocation();C->SetRelativeLocation(Original+FVector(0,(Side?1:-1)*D->TravelDistance,0));const auto& L=C->GetStaticMesh()->GetRenderData()->LODResources[0];const auto& V=L.VertexBuffers.PositionVertexBuffer;
  for(FVector Eye:{FVector(350,0,230),FVector(-350,0,230),FVector(350,180,230),FVector(-350,180,230),FVector(350,-180,230),FVector(-350,-180,230)})for(int I=0;I<L.IndexBuffer.GetNumIndices();I+=3)for(FVector Bary:{FVector(.2,.3,.5),FVector(.6,.2,.2),FVector(.2,.6,.2),FVector(.33,.33,.34)}){
   FVector A(V.VertexPosition(L.IndexBuffer.GetIndex(I))),B(V.VertexPosition(L.IndexBuffer.GetIndex(I+1))),Z(V.VertexPosition(L.IndexBuffer.GetIndex(I+2)));FVector Point=C->GetComponentTransform().TransformPosition(A*Bary.X+B*Bary.Y+Z*Bary.Z),From=T.TransformPosition(Eye);FHitResult H;bool Hit=W->LineTraceSingleByChannel(H,From,Point,ECC_Visibility,Occlusion);Hidden+=Hit&&(H.ImpactPoint-From).Size()+.01<(Point-From).Size();Tested++;
  }
  C->SetRelativeLocation(Original);
 }
 O->SetNumberField(TEXT("pocket_only_occluded_samples"),Hidden);O->SetNumberField(TEXT("pocket_only_samples"),Tested);Check(TEXT("both_open_leaves_hidden_by_real_housings_in_six_views"),Shells>=2&&Tested>0&&Hidden==Tested);
 if(ExpectGuard){
  Check(TEXT("unbuilt_default_three_access_gates"),!Built&&Locked&&!Allowed&&Guard!=nullptr);
  D->LeftLeaf->SetRelativeLocation(D->LeftClosedLocation+FVector(0,-D->TravelDistance,0));D->RightLeaf->SetRelativeLocation(D->RightClosedLocation+FVector(0,D->TravelDistance,0));auto H=Capsule(0,false);Check(TEXT("physical_guard_blocks_pawn_even_with_leaves_manually_parked"),Guard&&H.Key&&H.Value&&H.Value->GetOwner()==Guard);D->ResetClosed();
 }else{
  D->bDestinationConstructed=true;D->bSecurityLocked=false;D->bExternalAccessAllowed=true;P->SetActorLocation(T.TransformPosition(FVector(-60,0,110)),false);bool Accepted=D->RequestOpen(P);for(int I=0;I<122;I++)D->AdvanceDoor(D->MovementDuration/120);Check(TEXT("runtime_pair_reaches_full_open"),Accepted&&D->OpenFraction>.999);
  const float SafeY=FMath::Max(0.f,D->OpeningWidth*.5f-35-D->PathClearance);const bool LC=!Capsule(-SafeY,true).Key,CC=!Capsule(0,true).Key,RC=!Capsule(SafeY,true).Key;Check(TEXT("open_capsule_calibrated_left_center_right_lanes_cross_actual_door"),LC&&CC&&RC);Capsule(-35,true);Capsule(35,true);O->SetNumberField(TEXT("validated_lane_center_half_width_cm"),SafeY);
  P->SetActorLocation(T.TransformPosition(FVector(0,0,110)),false);D->RequestClose();D->AdvanceDoor(D->CloseDelay+1);Check(TEXT("threshold_occupant_prevents_closing"),D->IsDoorwayOccupied()&&D->OpenFraction>.999);
  P->SetActorLocation(T.TransformPosition(FVector(-300,0,110)),false);D->RequestClose();D->AdvanceDoor(.15);int Reversals=D->ClosingReversalCount;P->SetActorLocation(T.TransformPosition(FVector(0,0,110)),false);D->AdvanceDoor(.1);Check(TEXT("threshold_occupant_reverses_started_closure"),D->ClosingReversalCount>Reversals);
  P->SetActorLocation(T.TransformPosition(FVector(0,0,1000)),false);D->RequestClose();for(int I=0;I<130;I++)D->AdvanceDoor(D->MovementDuration/120);Check(TEXT("runtime_returns_fully_closed"),D->OpenFraction<.001);
  P->SetActorLocation(T.TransformPosition(FVector(60,0,110)),false);bool Outside=D->RequestOpen(P);for(int I=0;I<122;I++)D->AdvanceDoor(D->MovementDuration/120);Check(TEXT("outside_request_opens_both_leaves"),Outside&&D->OpenFraction>.999);P->SetActorLocation(T.TransformPosition(FVector(0,0,1000)),false);D->RequestClose();for(int I=0;I<130;I++)D->AdvanceDoor(D->MovementDuration/120);Check(TEXT("outside_cycle_returns_closed"),D->OpenFraction<.001);
  int Floors=0;FCollisionQueryParams Floor(SCENE_QUERY_STAT(FGFloor),false,D);Floor.AddIgnoredActor(P);if(Guard)Floor.AddIgnoredActor(Guard);
  for(float X:{-70.f,-35.f,0.f,35.f}){FHitResult H;bool Hit=W->LineTraceSingleByChannel(H,T.TransformPosition(FVector(X,0,100)),T.TransformPosition(FVector(X,0,-150)),ECC_Visibility,Floor);Floors+=Hit&&H.ImpactNormal.Z>.7f;}
  O->SetNumberField(TEXT("actual_floor_support_samples"),Floors);Check(TEXT("real_floor_under_inside_threshold_and_cabin"),Floors==4);
  FHitResult Back;bool BackHit=W->LineTraceSingleByChannel(Back,T.TransformPosition(FVector(4,0,110)),T.TransformPosition(FVector(500,0,110)),ECC_Visibility,Floor);O->SetNumberField(TEXT("cabin_backwall_local_X_cm"),BackHit?T.InverseTransformPosition(Back.ImpactPoint).X:-1);O->SetStringField(TEXT("cabin_backwall_actor"),BackHit?Back.GetActor()->GetActorLabel():TEXT("None"));
  TArray<TSharedPtr<FJsonValue>> FloorProfile;for(float X:{0.f,40.f,80.f,120.f,160.f,200.f}){FHitResult H;bool Hit=W->LineTraceSingleByChannel(H,T.TransformPosition(FVector(X,0,200)),T.TransformPosition(FVector(X,0,-200)),ECC_Visibility,Floor);auto J=MakeShared<FJsonObject>();J->SetNumberField(TEXT("X"),X);J->SetBoolField(TEXT("support"),Hit&&H.ImpactNormal.Z>.7f);J->SetNumberField(TEXT("floor_local_Z"),Hit?T.InverseTransformPosition(H.ImpactPoint).Z:-999);J->SetStringField(TEXT("actor"),Hit?H.GetActor()->GetActorLabel():TEXT("None"));FloorProfile.Add(MakeShared<FJsonValueObject>(J));}O->SetArrayField(TEXT("floor_profile"),FloorProfile);
 }
 P->Destroy();D->bDestinationConstructed=Built;D->bSecurityLocked=Locked;D->bExternalAccessAllowed=Allowed;D->bProximityEnabled=Proximity;D->bUsePassageIntent=Intent;D->ResetClosed();Check(TEXT("security_and_intent_settings_restored"),D->bDestinationConstructed==Built&&D->bSecurityLocked==Locked&&D->bExternalAccessAllowed==Allowed&&D->bUsePassageIntent==Intent);
 O->SetStringField(TEXT("door"),D->DoorId.ToString());O->SetArrayField(TEXT("cases"),Cases);O->SetArrayField(TEXT("leaf_poses"),Rows);O->SetArrayField(TEXT("hits"),HitsOut);O->SetArrayField(TEXT("capsule_profiles"),CapsuleProfiles);int Passed=0;for(auto C:Cases)Passed+=C->AsObject()->GetBoolField(TEXT("pass"));O->SetNumberField(TEXT("passed"),Passed);O->SetNumberField(TEXT("total"),Cases.Num());O->SetBoolField(TEXT("all_pass"),Passed==Cases.Num());FString Out;FJsonSerializer::Serialize(O,TJsonWriterFactory<>::Create(&Out));return Out;
}
