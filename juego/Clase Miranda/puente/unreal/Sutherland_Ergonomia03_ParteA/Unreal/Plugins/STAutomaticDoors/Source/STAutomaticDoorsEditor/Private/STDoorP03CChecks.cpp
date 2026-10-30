#include "STAutomaticDoorTestLibrary.h"
#include "STAutomaticDoor.h"
#include "Components/StaticMeshComponent.h"
#include "Components/CapsuleComponent.h"
#include "Engine/World.h"
#include "Engine/StaticMesh.h"
#include "GameFramework/Character.h"
#include "PhysicsEngine/BodySetup.h"
#include "AssetCompilingManager.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"

bool USTAutomaticDoorTestLibrary::ConfigureP03CWallCollision(UStaticMesh* M) {
 if(!M||(!M->GetPathName().StartsWith(TEXT("/Game/F07P03C/"))&&!M->GetPathName().StartsWith(TEXT("/Game/F07P03D/"))&&!M->GetPathName().StartsWith(TEXT("/Game/F07P03FG/"))))return false;
 FAssetCompilingManager::Get().FinishAllCompilation();M->CreateBodySetup();auto* B=M->GetBodySetup();
 B->Modify();B->AggGeom.EmptyElements();B->CollisionTraceFlag=CTF_UseComplexAsSimple;B->bDoubleSidedGeometry=true;
 B->InvalidatePhysicsData();B->CreatePhysicsMeshes();M->MarkPackageDirty();return true;
}
FString USTAutomaticDoorTestLibrary::RunP03CPilotChecks(ASTAutomaticDoor* D) {
 auto O=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Cases,Poses;
 if(!D||D->DoorId!=TEXT("DOOR_F07_001"))return TEXT("{\"error\":\"Wrong pilot\"}");
 FAssetCompilingManager::Get().FinishAllCompilation();auto* W=D->GetWorld();D->LeftLeaf->RecreatePhysicsState();D->RightLeaf->RecreatePhysicsState();D->ResetClosed();
 auto Check=[&](const TCHAR* Name,bool Pass){auto C=MakeShared<FJsonObject>();C->SetStringField(TEXT("name"),Name);C->SetBoolField(TEXT("pass"),Pass);Cases.Add(MakeShared<FJsonValueObject>(C));};
 const FVector OriginalLeft=D->LeftLeaf->GetRelativeLocation(),OriginalRight=D->RightLeaf->GetRelativeLocation();
 FComponentQueryParams Q;Q.AddIgnoredActor(D);Q.bTraceComplex=false;
 auto HitsAt=[&](FVector Start,FVector End){TArray<FHitResult> H;W->ComponentSweepMultiByChannel(H,D->RightLeaf,Start,End,D->RightLeaf->GetComponentQuat(),ECC_Pawn,Q);return H;};
 auto AnyBlocking=[](const TArray<FHitResult>& H){for(const auto& Hit:H)if(Hit.bBlockingHit)return true;return false;};
 const FVector Start=D->RightLeaf->GetComponentLocation(),Delta=D->GetActorTransform().TransformVectorNoScale(FVector(0,D->TravelDistance,0));
 for(float F:{0.f,.25f,.5f,.75f,1.f}){
  auto P=MakeShared<FJsonObject>();P->SetNumberField(TEXT("fraction"),F);
  P->SetBoolField(TEXT("fixed_overlap"),AnyBlocking(HitsAt(Start+Delta*F,Start+Delta*F)));
  P->SetBoolField(TEXT("sweep_forward_blocked"),AnyBlocking(HitsAt(Start,Start+Delta*F)));
  P->SetBoolField(TEXT("sweep_reverse_blocked"),AnyBlocking(HitsAt(Start+Delta*F,Start)));
  Poses.Add(MakeShared<FJsonValueObject>(P));
 }
 bool AllClear=true;for(const auto& P:Poses)for(const TCHAR* Key:{TEXT("fixed_overlap"),TEXT("sweep_forward_blocked"),TEXT("sweep_reverse_blocked")})if(P->AsObject()->GetBoolField(Key))AllClear=false;
 Check(TEXT("five_poses_and_bidirectional_convex_sweeps_clear"),AllClear);
 auto Capsule=[&](float Y, bool& IsRight){FHitResult H;FCollisionQueryParams C(SCENE_QUERY_STAT(P03CCapsule),false);
  FVector A=D->GetActorTransform().TransformPosition(FVector(-120,Y,110)),B=D->GetActorTransform().TransformPosition(FVector(120,Y,110));
  bool Blocked=W->SweepSingleByChannel(H,A,B,FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(35,90),C);IsRight=H.GetComponent()==D->RightLeaf.Get();return Blocked;};
 bool IsRight=false;Check(TEXT("closed_right_leaf_blocks_actual_size_pawn_capsule"),Capsule(41,IsRight)&&IsRight);
 bool MotionClear=true;float MaxError=0;
 for(int32 Pass=0;Pass<2;Pass++)for(int32 I=0;I<=120;I++) {
  float F=Pass?1.f-I/120.f:I/120.f;FVector Target=OriginalRight+FVector(0,D->TravelDistance*F,0);FHitResult Hit;
  D->RightLeaf->SetRelativeLocation(Target,true,&Hit);MaxError=FMath::Max(MaxError,(D->RightLeaf->GetRelativeLocation()-Target).Size());if(Hit.bBlockingHit)MotionClear=false;
  if(Pass==0&&I==120)Check(TEXT("open_right_half_has_no_invisible_static_barrier"),!Capsule(41,IsRight));
 }
 O->SetNumberField(TEXT("movement_max_error_cm"),MaxError);Check(TEXT("actual_leaf_motion_242_swept_steps"),MotionClear&&MaxError<.01f);
 Check(TEXT("left_leaf_never_moved"),D->LeftLeaf->GetRelativeLocation().Equals(OriginalLeft,.0001f));
 Check(TEXT("right_returns_exactly_closed"),D->RightLeaf->GetRelativeLocation().Equals(OriginalRight,.0001f));
 Check(TEXT("unbuilt_security_policy_preserved"),!D->bDestinationConstructed&&D->bSecurityLocked&&!D->bExternalAccessAllowed);
 FActorSpawnParameters SP;SP.ObjectFlags=RF_Transient;SP.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 auto* Pawn=W->SpawnActor<ACharacter>(ACharacter::StaticClass(),FTransform(D->GetActorLocation()+FVector(0,0,1000)),SP);
 Check(TEXT("locked_unbuilt_door_rejects_open_request"),!D->RequestOpen(Pawn));Pawn->Destroy();
 bool Perimeter=true;int32 WitnessCount=0;
 for(float Y:{92.f,110.f,130.f,150.f,170.f})for(float Z:{110.f,220.f,350.f}) {
  FHitResult H;FCollisionQueryParams C(SCENE_QUERY_STAT(P03CPerimeter),false,D);auto T=D->GetActorTransform();
  if(!W->SweepSingleByChannel(H,T.TransformPosition(FVector(-80,Y,Z)),T.TransformPosition(FVector(80,Y,Z)),FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(35,90),C))Perimeter=false;WitnessCount++;
 }
 O->SetNumberField(TEXT("casing_capsule_witnesses"),WitnessCount);Check(TEXT("casing_keeps_perimeter_solid"),Perimeter);
 D->ResetClosed();O->SetArrayField(TEXT("poses"),Poses);O->SetArrayField(TEXT("cases"),Cases);int32 Passed=0;for(const auto& C:Cases)if(C->AsObject()->GetBoolField(TEXT("pass")))Passed++;
 O->SetNumberField(TEXT("passed"),Passed);O->SetNumberField(TEXT("total"),Cases.Num());O->SetBoolField(TEXT("all_pass"),Passed==Cases.Num());O->SetBoolField(TEXT("saved_assets"),false);
 FString Text;FJsonSerializer::Serialize(O,TJsonWriterFactory<>::Create(&Text));return Text;
}


