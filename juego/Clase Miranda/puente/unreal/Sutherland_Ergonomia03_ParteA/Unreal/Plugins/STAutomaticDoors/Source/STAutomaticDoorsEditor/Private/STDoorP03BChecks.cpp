#include "STAutomaticDoorTestLibrary.h"
#include "STAutomaticDoor.h"
#include "ProceduralMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/Character.h"
#include "Engine/World.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/StaticMesh.h"
#include "PhysicsEngine/BodySetup.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"
#include "Misc/FileHelper.h"
#include "AssetCompilingManager.h"
#include "StaticMeshResources.h"

bool USTAutomaticDoorTestLibrary::SetExactLeafConvexCollision(UStaticMesh* LeafMesh) {
 if(!LeafMesh||!LeafMesh->GetPathName().StartsWith(TEXT("/Game/F07P02/P03B/Leaves/")))return false;
 FAssetCompilingManager::Get().FinishAllCompilation();FStaticMeshRenderData* Render=LeafMesh->GetRenderData();
 if(!Render||Render->LODResources.IsEmpty())return false;
 FKConvexElem Convex;const auto& Positions=Render->LODResources[0].VertexBuffers.PositionVertexBuffer;
 for(uint32 I=0;I<Positions.GetNumVertices();I++) {
  const FVector V(Positions.VertexPosition(I));bool Found=false;for(const FVector& P:Convex.VertexData)if(V.Equals(P,.0001f)){Found=true;break;}if(!Found)Convex.VertexData.Add(V);
 }
 if(Convex.VertexData.Num()!=8)return false;
 Convex.UpdateElemBox();UBodySetup* Body=LeafMesh->GetBodySetup();if(!Body)return false;
 Body->Modify();Body->AggGeom.BoxElems.Empty();Body->AggGeom.ConvexElems.Empty();Body->AggGeom.ConvexElems.Add(Convex);
 Body->CollisionTraceFlag=CTF_UseSimpleAndComplex;Body->InvalidatePhysicsData();Body->CreatePhysicsMeshes();LeafMesh->MarkPackageDirty();return true;
}

FString USTAutomaticDoorTestLibrary::RunP03BChecks(UObject* Context,UClass* BPClass,const FString& SceneFile) {
 auto Report=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Results,Cases;
 UWorld* World=Cast<UWorld>(Context);if(!World&&Context)World=Context->GetWorld();
 FString Input;TSharedPtr<FJsonObject> Root;
 if(!World||!BPClass||!FFileHelper::LoadFileToString(Input,*SceneFile)||!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Input),Root))return TEXT("{\"error\":\"invalid input\"}");
 auto Vec=[](const TArray<TSharedPtr<FJsonValue>>& A){return FVector(A[0]->AsNumber(),A[1]->AsNumber(),A[2]->AsNumber());};
 auto Check=[&](const FString& Name,bool Passed){auto C=MakeShared<FJsonObject>();C->SetStringField(TEXT("name"),Name);C->SetBoolField(TEXT("pass"),Passed);Cases.Add(MakeShared<FJsonValueObject>(C));};
 FActorSpawnParameters Params;Params.ObjectFlags=RF_Transient;Params.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 const FVector Origin(40000,0,10000);
 for(const auto& SceneValue:Root->GetArrayField(TEXT("scenes"))) {
  auto S=SceneValue->AsObject();auto O=MakeShared<FJsonObject>();FString Id=S->GetStringField(TEXT("door_id")),Scenario=S->GetStringField(TEXT("scenario"));
  O->SetStringField(TEXT("door_id"),Id);O->SetStringField(TEXT("scenario"),Scenario);
  auto* Geometry=World->SpawnActor<AActor>(AActor::StaticClass(),FTransform(Origin),Params);
  auto* Mesh=NewObject<UProceduralMeshComponent>(Geometry);Geometry->SetRootComponent(Mesh);Mesh->bUseAsyncCooking=false;Mesh->bUseComplexAsSimpleCollision=true;
  Mesh->SetCollisionProfileName(TEXT("BlockAll"));Mesh->SetGenerateOverlapEvents(false);Mesh->RegisterComponent();Geometry->SetActorLocation(Origin);
  TArray<FVector> V;TArray<int32> I;
  for(const auto& T:S->GetArrayField(TEXT("obstacle_triangles_local_cm")))for(const auto& Point:T->AsArray()){I.Add(V.Num());V.Add(Vec(Point->AsArray()));}
  Mesh->CreateMeshSection(0,V,I,TArray<FVector>(),TArray<FVector2D>(),TArray<FColor>(),TArray<FProcMeshTangent>(),true);
  Mesh->GetBodySetup()->bDoubleSidedGeometry=true;Mesh->RecreatePhysicsState();
  auto* D=World->SpawnActor<ASTAutomaticDoor>(BPClass,FTransform(Origin),Params);
  const auto& Leaves=S->GetArrayField(TEXT("leaves"));
  D->LeftLeaf->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,*Leaves[0]->AsObject()->GetStringField(TEXT("mesh"))));
  D->RightLeaf->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,*Leaves[1]->AsObject()->GetStringField(TEXT("mesh"))));
  FAssetCompilingManager::Get().FinishAllCompilation();D->LeftLeaf->RecreatePhysicsState();D->RightLeaf->RecreatePhysicsState();
  D->LeftClosedLocation=Vec(Leaves[0]->AsObject()->GetArrayField(TEXT("closed_location")));D->RightClosedLocation=Vec(Leaves[1]->AsObject()->GetArrayField(TEXT("closed_location")));
  D->TravelDistance=S->GetNumberField(TEXT("travel_cm"));D->OpeningWidth=S->GetNumberField(TEXT("opening_width"));D->OpeningHeight=S->GetNumberField(TEXT("opening_height"));
  D->SetDestinationConstructed(true);D->SetSecurityLocked(false);D->SetExternalAccessAllowed(true);D->bProximityEnabled=false;D->ResetClosed();
  auto* Pawn=World->SpawnActor<ACharacter>(ACharacter::StaticClass(),FTransform(Origin+FVector(-1000,0,110)),Params);
  Pawn->GetCapsuleComponent()->SetCapsuleSize(35,90);Pawn->GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));
  auto Advance=[&](float Seconds){for(int32 N=0;N<FMath::CeilToInt(Seconds*60);N++)D->AdvanceDoor(1.f/60);};
  auto CapsuleBlocked=[&](){FCollisionQueryParams Q(SCENE_QUERY_STAT(P03BCapsule),false,Pawn);FHitResult Hit;const FVector C=Origin+FVector(0,0,110);
   return World->SweepSingleByChannel(Hit,C-FVector(140,0,0),C+FVector(140,0,0),FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(35,90),Q);};
  TArray<TSharedPtr<FJsonValue>> Samples;
  for(int32 Side=0;Side<2;Side++)for(float F:{0.f,.25f,.5f,.75f,1.f}) {
   auto* C=Side?D->RightLeaf.Get():D->LeftLeaf.Get();FVector Min,Max;C->GetLocalBounds(Min,Max);
   FVector Start=C->GetComponentTransform().TransformPosition((Min+Max)/2)+FVector(0,(Side?1:-1)*D->TravelDistance*F,0);
   FCollisionQueryParams Q(SCENE_QUERY_STAT(P03BLeafSamples),true,D);Q.AddIgnoredActor(Pawn);FHitResult Hit;
   bool Blocked=World->SweepSingleByChannel(Hit,Start,Start,C->GetComponentQuat(),ECC_Pawn,FCollisionShape::MakeBox((Max-Min)/2),Q);
   auto T=MakeShared<FJsonObject>();T->SetStringField(TEXT("side"),Side?TEXT("Right"):TEXT("Left"));T->SetNumberField(TEXT("fraction"),F);T->SetBoolField(TEXT("box_blocked"),Blocked);Samples.Add(MakeShared<FJsonValueObject>(T));
   FComponentQueryParams CQ;CQ.AddIgnoredActor(D);CQ.AddIgnoredActor(Pawn);TArray<FHitResult> CH;
   FVector ComponentStart=C->GetComponentLocation()+FVector(0,(Side?1:-1)*D->TravelDistance*F,0);
   bool ComponentBlocked=World->ComponentSweepMultiByChannel(CH,C,ComponentStart,ComponentStart,C->GetComponentQuat(),ECC_Pawn,CQ);
   T->SetBoolField(TEXT("actual_component_blocked"),ComponentBlocked);
  }
  O->SetArrayField(TEXT("physical_pose_samples"),Samples);O->SetBoolField(TEXT("closed_capsule_blocked"),CapsuleBlocked());
  O->SetStringField(TEXT("door_location"),D->GetActorLocation().ToString());O->SetStringField(TEXT("geometry_location"),Mesh->GetComponentLocation().ToString());O->SetStringField(TEXT("leaf_location"),D->LeftLeaf->GetComponentLocation().ToString());
  O->SetNumberField(TEXT("leaf_response_worldstatic"),(int32)D->LeftLeaf->GetCollisionResponseToChannel(ECC_WorldStatic));O->SetNumberField(TEXT("leaf_collision_enabled"),(int32)D->LeftLeaf->GetCollisionEnabled());
  O->SetBoolField(TEXT("leaf_physics_state"),D->LeftLeaf->IsPhysicsStateCreated());O->SetNumberField(TEXT("leaf_response_pawn"),(int32)D->LeftLeaf->GetCollisionResponseToChannel(ECC_Pawn));
  O->SetNumberField(TEXT("leaf_box_count"),D->LeftLeaf->GetStaticMesh()->GetBodySetup()->AggGeom.BoxElems.Num());
  D->RequestOpen(Pawn);Advance(1);O->SetNumberField(TEXT("opening_fraction"),D->OpenFraction);O->SetStringField(TEXT("opening_state"),StaticEnum<ESTDoorState>()->GetNameStringByValue((int64)D->DoorState));
  O->SetBoolField(TEXT("open_capsule_clear"),!CapsuleBlocked());
  // Frame witness rays: unchanged surfaces beyond the original jamb must remain occluding after a future design.
  int32 Rays=0,BlockedRays=0;TArray<TSharedPtr<FJsonValue>> Witnesses;
  for(float Sign:{-1.f,1.f})for(float YOffset:{2.f,20.f,60.f})for(float Z:{80.f,200.f,360.f}) {
   FHitResult Hit;FCollisionQueryParams Q(SCENE_QUERY_STAT(P03BFrameWitness),true,D);Q.AddIgnoredActor(Pawn);
   FVector C=Origin+FVector(0,Sign*(D->OpeningWidth/2+YOffset),Z);bool Blocked=World->LineTraceSingleByChannel(Hit,C-FVector(50,0,0),C+FVector(50,0,0),ECC_Pawn,Q);
   Rays++;if(Blocked)BlockedRays++;auto W=MakeShared<FJsonObject>();W->SetNumberField(TEXT("y"),Sign*(D->OpeningWidth/2+YOffset));W->SetNumberField(TEXT("z"),Z);W->SetBoolField(TEXT("blocked"),Blocked);Witnesses.Add(MakeShared<FJsonValueObject>(W));
  }
  O->SetNumberField(TEXT("fixed_frame_witnesses"),Rays);O->SetNumberField(TEXT("fixed_frame_occluded"),BlockedRays);O->SetArrayField(TEXT("fixed_frame_rays"),Witnesses);
  if(Scenario==TEXT("corridor_and_floor_candidate")) {
   const FString Prefix=Id+TEXT("/");
   Check(Prefix+TEXT("closed_capsule_blocks"),O->GetBoolField(TEXT("closed_capsule_blocked")));
   Check(Prefix+TEXT("clipped_corridor_opens_fully"),D->OpenFraction>.999f);
   const float LMove=D->LeftClosedLocation.Y-D->LeftLeaf->GetRelativeLocation().Y,RMove=D->RightLeaf->GetRelativeLocation().Y-D->RightClosedLocation.Y;
   Check(Prefix+TEXT("equal_outward_travel"),FMath::Abs(LMove-D->TravelDistance)<.02f&&FMath::Abs(RMove-D->TravelDistance)<.02f);
   Check(Prefix+TEXT("height_and_normal_preserved"),FMath::Abs(D->LeftLeaf->GetRelativeLocation().Z-D->LeftClosedLocation.Z)<.001f&&FMath::Abs(D->RightLeaf->GetRelativeLocation().X-D->RightClosedLocation.X)<.001f);
   Check(Prefix+TEXT("open_capsule_clear"),!CapsuleBlocked());
   Pawn->SetActorLocation(Origin+FVector(0,0,110));Advance(3);Check(Prefix+TEXT("occupant_holds_open"),D->IsDoorwayOccupied()&&D->OpenFraction>.999f);
   Pawn->SetActorLocation(Origin+FVector(-1000,0,110));Advance(3);Check(Prefix+TEXT("closes_to_original_pose"),D->OpenFraction<.001f&&D->LeftLeaf->GetRelativeLocation().Equals(D->LeftClosedLocation,.01f)&&D->RightLeaf->GetRelativeLocation().Equals(D->RightClosedLocation,.01f));
   D->SetSecurityLocked(true);Check(Prefix+TEXT("security_lock_denies"),!D->RequestOpen(Pawn));D->SetSecurityLocked(false);D->SetDestinationConstructed(false);Check(Prefix+TEXT("unbuilt_denies"),!D->RequestOpen(Pawn));D->SetDestinationConstructed(true);
   auto* Blocker=World->SpawnActor<AStaticMeshActor>(AStaticMeshActor::StaticClass(),FTransform(Origin+FVector(0,-120,200)),Params);
   Blocker->GetStaticMeshComponent()->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube")));Blocker->SetActorScale3D(FVector(.2f,.05f,1));Blocker->GetStaticMeshComponent()->SetCollisionProfileName(TEXT("BlockAll"));
   D->RequestOpen(Pawn);Advance(1);Check(Prefix+TEXT("opening_obstacle_stops_leaf"),D->OpenFraction<.9f&&D->DoorState==ESTDoorState::Obstructed);
   O->SetNumberField(TEXT("obstacle_open_fraction"),D->OpenFraction);O->SetStringField(TEXT("obstacle_location"),Blocker->GetActorLocation().ToString());O->SetStringField(TEXT("obstacle_leaf_location"),D->LeftLeaf->GetComponentLocation().ToString());
   FHitResult BH;FCollisionQueryParams BQ(SCENE_QUERY_STAT(P03BBlocker),false,D);BQ.AddIgnoredActor(Pawn);
   O->SetBoolField(TEXT("blocker_trace_hits"),World->SweepSingleByChannel(BH,Origin+FVector(0,-80,200),Origin+FVector(0,-150,200),FQuat::Identity,ECC_WorldDynamic,FCollisionShape::MakeBox(FVector(2,2,20)),BQ));
   Blocker->Destroy();D->RequestOpen(Pawn);Advance(1);Check(Prefix+TEXT("opens_after_obstacle_removed"),D->OpenFraction>.999f);
   Blocker=World->SpawnActor<AStaticMeshActor>(AStaticMeshActor::StaticClass(),FTransform(Origin+FVector(0,-60,200)),Params);
   Blocker->GetStaticMeshComponent()->SetStaticMesh(LoadObject<UStaticMesh>(nullptr,TEXT("/Engine/BasicShapes/Cube.Cube")));Blocker->SetActorScale3D(FVector(.2f,.05f,1));Blocker->GetStaticMeshComponent()->SetCollisionProfileName(TEXT("BlockAll"));
   const int32 Previous=D->ClosingReversalCount;Advance(3);Check(Prefix+TEXT("closing_obstacle_reverses"),D->ClosingReversalCount>Previous&&D->OpenFraction>0);Blocker->Destroy();
  }
  Pawn->Destroy();D->Destroy();Geometry->Destroy();Results.Add(MakeShared<FJsonValueObject>(O));
 }
 int32 Passed=0;for(const auto& C:Cases)if(C->AsObject()->GetBoolField(TEXT("pass")))Passed++;
 Report->SetArrayField(TEXT("scenes"),Results);Report->SetArrayField(TEXT("cases"),Cases);Report->SetNumberField(TEXT("passed"),Passed);Report->SetNumberField(TEXT("total"),Cases.Num());Report->SetBoolField(TEXT("all_pass"),Passed==Cases.Num());
 Report->SetStringField(TEXT("method"),TEXT("Transient reconstructed retained triangle fragments with Chaos complex collision; same native AdvanceDoor, real simple leaf collisions; capsule radius35 halfheight90, center localZ110. No saved geometry modified."));
 FString Text;FJsonSerializer::Serialize(Report,TJsonWriterFactory<>::Create(&Text));return Text;
}
