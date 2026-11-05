#include "VHAutomaticDoorTools.h"
#include "VHAutomaticDoor.h"
#include "VHFunctionalProbe.h"
#include "Editor.h"
#include "Engine/World.h"
#include "Engine/StaticMesh.h"
#include "Engine/StaticMeshActor.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "GameFramework/Character.h"
#include "GameFramework/PlayerStart.h"
#include "GameFramework/WorldSettings.h"
#include "Engine/DirectionalLight.h"
#include "Engine/SkyLight.h"
#include "Components/DirectionalLightComponent.h"
#include "Components/SkyLightComponent.h"
#include "MeshDescription.h"
#include "StaticMeshAttributes.h"
#include "PhysicsEngine/BodySetup.h"
#include "PhysicsEngine/ConvexElem.h"
#include "Materials/Material.h"
#include "Materials/MaterialExpressionConstant3Vector.h"
#include "Materials/MaterialExpressionConstant.h"
#include "Materials/MaterialExpressionTextureSample.h"
#include "ImageUtils.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Misc/PackageName.h"
#include "UObject/SavePackage.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"
#include "EngineUtils.h"
#include "Serialization/BufferArchive.h"
#include "Misc/SecureHash.h"

namespace {
FVector Vec(const TArray<TSharedPtr<FJsonValue>>& A){return FVector(A[0]->AsNumber(),A[1]->AsNumber(),A[2]->AsNumber());}
FString Json(const TSharedRef<FJsonObject>& O){FString S;auto W=TJsonWriterFactory<>::Create(&S);FJsonSerializer::Serialize(O,W);return S;}
FString SurfaceDigest(UStaticMesh* Mesh){FBufferArchive Bytes;Mesh->GetMeshDescription(0)->Serialize(Bytes);FSHAHash Hash;FSHA1::HashBuffer(Bytes.GetData(),Bytes.Num(),Hash.Hash);return Hash.ToString();}
bool Save(UObject* O){UPackage* P=O->GetOutermost();P->MarkPackageDirty();FSavePackageArgs A;A.TopLevelFlags=RF_Public|RF_Standalone;A.SaveFlags=SAVE_NoError;return UPackage::SavePackage(P,O,*FPackageName::LongPackageNameToFilename(P->GetName(),FPackageName::GetAssetPackageExtension()),A);}
UMaterial* MakeMaterial(const TSharedPtr<FJsonObject>& R,const FString& Path,const FString& SourceDirectory){
 auto* P=CreatePackage(*Path);auto* M=NewObject<UMaterial>(P,*FPaths::GetBaseFilename(Path),RF_Public|RF_Standalone);
 auto C=R->GetArrayField(TEXT("color"));auto* RGB=NewObject<UMaterialExpressionConstant3Vector>(M);RGB->Constant=FLinearColor(C[0]->AsNumber(),C[1]->AsNumber(),C[2]->AsNumber());M->GetExpressionCollection().AddExpression(RGB);M->GetEditorOnlyData()->BaseColor.Expression=RGB;
 auto Scalar=[&](const TCHAR* Field,FScalarMaterialInput& Input){auto* E=NewObject<UMaterialExpressionConstant>(M);E->R=R->GetNumberField(Field);M->GetExpressionCollection().AddExpression(E);Input.Expression=E;};
 Scalar(TEXT("roughness"),M->GetEditorOnlyData()->Roughness);Scalar(TEXT("metallic"),M->GetEditorOnlyData()->Metallic);
 float Alpha=R->GetNumberField(TEXT("alpha"));if(Alpha<.999f){M->BlendMode=BLEND_Translucent;auto* E=NewObject<UMaterialExpressionConstant>(M);E->R=Alpha;M->GetExpressionCollection().AddExpression(E);M->GetEditorOnlyData()->Opacity.Expression=E;}
 FString Image;if(R->TryGetStringField(TEXT("image"),Image)&&!Image.IsEmpty()){
  auto* Texture=FImageUtils::ImportFileAsTexture2D(FPaths::Combine(SourceDirectory,Image));
  if(Texture){FString TP=Path+TEXT("_OriginalImage");auto* Package=CreatePackage(*TP);Texture->Rename(*FPaths::GetBaseFilename(TP),Package);Texture->SetFlags(RF_Public|RF_Standalone);FAssetRegistryModule::AssetCreated(Texture);Save(Texture);auto* Sample=NewObject<UMaterialExpressionTextureSample>(M);Sample->Texture=Texture;M->GetExpressionCollection().AddExpression(Sample);M->GetEditorOnlyData()->BaseColor.Expression=Sample;}
 }
 // Opposite source faces retain their original materials. Single-sided
 // rasterization selects each anverso/reverso; collision is configured separately.
 M->TwoSided=false;M->PostEditChange();FAssetRegistryModule::AssetCreated(M);check(Save(M));return M;
}
UStaticMesh* MakeMesh(const TSharedPtr<FJsonObject>& R,const FString& Path,const TMap<FString,UMaterial*>& Mats,bool Leaf){
 auto* Package=CreatePackage(*Path);auto* Mesh=NewObject<UStaticMesh>(Package,*FPaths::GetBaseFilename(Path),RF_Public|RF_Standalone);FMeshDescription MD;FStaticMeshAttributes A(MD);A.Register();auto Position=A.GetVertexPositions();auto Normals=A.GetVertexInstanceNormals();auto UV=A.GetVertexInstanceUVs();UV.SetNumChannels(1);auto Slot=A.GetPolygonGroupMaterialSlotNames();
 TArray<FVertexID> IDs;TArray<FVector> CollisionVertices;
 for(const auto& V:R->GetArrayField(TEXT("vertices"))){FVector P=Vec(V->AsArray());auto ID=MD.CreateVertex();Position[ID]=FVector3f(P);IDs.Add(ID);if(Leaf)CollisionVertices.Add(P);}
 TArray<FPolygonGroupID> Groups;
 for(const auto& Name:R->GetArrayField(TEXT("materials"))){auto G=MD.CreatePolygonGroup();FName MaterialName(*Name->AsString());Slot[G]=MaterialName;Groups.Add(G);Mesh->GetStaticMaterials().Add(FStaticMaterial(Mats.FindRef(Name->AsString()),MaterialName,MaterialName));}
 for(const auto& Value:R->GetArrayField(TEXT("triangles"))){auto T=Value->AsObject();auto VI=T->GetArrayField(TEXT("v"));TArray<FVertexInstanceID> Corners;auto N=T->GetArrayField(TEXT("n"));auto U=T->GetArrayField(TEXT("uv"));
  for(int32 I=0;I<3;I++){auto C=MD.CreateVertexInstance(IDs[(int32)VI[I]->AsNumber()]);Normals[C]=FVector3f(Vec(N[I]->AsArray()));auto Tex=U[I]->AsArray();UV.Set(C,0,FVector2f(Tex[0]->AsNumber(),Tex[1]->AsNumber()));Corners.Add(C);}
  // New construction uses Unreal front faces. Recheck after float conversion:
  // tiny triangulation slivers can change orientation when baked in world space.
  if(Path.Contains(TEXT("/Completion/"))&&!Path.Contains(TEXT("_Architecture"))){
   auto X=Position[MD.GetVertexInstanceVertex(Corners[0])];auto Y=Position[MD.GetVertexInstanceVertex(Corners[1])];auto Z=Position[MD.GetVertexInstanceVertex(Corners[2])];
   if(FVector3f::DotProduct(FVector3f::CrossProduct(Y-X,Z-X),Normals[Corners[0]]+Normals[Corners[1]]+Normals[Corners[2]])>0)Swap(Corners[1],Corners[2]);
  }
  MD.CreateTriangle(Groups[(int32)T->GetNumberField(TEXT("material"))],Corners);
 }
 auto& Source=Mesh->AddSourceModel();Source.BuildSettings.bRecomputeNormals=false;Source.BuildSettings.bRecomputeTangents=true;Source.BuildSettings.bUseFullPrecisionUVs=true;Source.BuildSettings.bGenerateLightmapUVs=false;
 UStaticMesh::FBuildMeshDescriptionsParams Params;Params.bAllowCpuAccess=true;Params.bBuildSimpleCollision=false;Params.bFastBuild=false;
 check(Mesh->BuildFromMeshDescriptions({&MD},Params));Mesh->CreateBodySetup();auto* Body=Mesh->GetBodySetup();
 if(Leaf){Body->CollisionTraceFlag=CTF_UseSimpleAndComplex;FKConvexElem Convex;Convex.VertexData=CollisionVertices;Convex.UpdateElemBox();Body->AggGeom.ConvexElems.Add(MoveTemp(Convex));}
 else{Body->CollisionTraceFlag=CTF_UseComplexAsSimple;Body->bDoubleSidedGeometry=true;}
 Body->InvalidatePhysicsData();Body->CreatePhysicsMeshes();FAssetRegistryModule::AssetCreated(Mesh);check(Save(Mesh));return Mesh;
}
}

FString UVHAutomaticDoorTools::BuildScene(const FString& File,const FString& Root){
 auto Result=MakeShared<FJsonObject>();FString Text;TSharedPtr<FJsonObject> Data;
 if(!FFileHelper::LoadFileToString(Text,*File)||!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text),Data)||!Root.StartsWith(TEXT("/Game/"))){Result->SetStringField(TEXT("error"),TEXT("Invalid source or package root"));return Json(Result);}
 UWorld* World=GEditor->GetEditorWorldContext().World();check(World);TMap<FString,UMaterial*> Materials;int32 N=0;
 for(const auto& V:Data->GetArrayField(TEXT("materials"))){auto R=V->AsObject();Materials.Add(R->GetStringField(TEXT("name")),MakeMaterial(R,FString::Printf(TEXT("%s/Materials/M_%03d"),*Root,N++),FPaths::GetPath(File)));}
 TMap<FString,UStaticMesh*> Meshes;N=0;auto DoorData=Data->GetObjectField(TEXT("door"));TSet<FString> LeafNames;
 for(const auto& V:DoorData->GetArrayField(TEXT("leaves")))LeafNames.Add(V->AsObject()->GetStringField(TEXT("mesh")));
 for(const auto& Entry:Data->GetObjectField(TEXT("meshes"))->Values){FString Key(Entry.Key.ToView());Meshes.Add(Key,MakeMesh(Entry.Value->AsObject(),FString::Printf(TEXT("%s/Meshes/SM_%03d"),*Root,N++),Materials,LeafNames.Contains(Key)));}
 auto* Room=World->SpawnActor<AActor>();Room->SetActorLabel(TEXT("Sala V04E - geometria original y uniones validadas"));auto* RoomRoot=NewObject<USceneComponent>(Room,TEXT("RoomRoot"));Room->SetRootComponent(RoomRoot);Room->AddInstanceComponent(RoomRoot);RoomRoot->SetMobility(EComponentMobility::Static);RoomRoot->RegisterComponent();TMap<FString,UInstancedStaticMeshComponent*> Batches;
 for(const auto& V:Data->GetArrayField(TEXT("instances"))){auto R=V->AsObject();FString Key=R->GetStringField(TEXT("mesh"));auto*& Batch=Batches.FindOrAdd(Key);
  if(!Batch){Batch=NewObject<UInstancedStaticMeshComponent>(Room);Room->AddInstanceComponent(Batch);Batch->SetupAttachment(RoomRoot);Batch->SetMobility(EComponentMobility::Static);Batch->SetStaticMesh(Meshes[Key]);Batch->SetCollisionProfileName(TEXT("BlockAll"));Batch->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);Batch->RegisterComponent();}
  auto Q=R->GetArrayField(TEXT("rotation"));FQuat Rotation(Q[0]->AsNumber(),Q[1]->AsNumber(),Q[2]->AsNumber(),Q[3]->AsNumber());Batch->AddInstance(FTransform(Rotation,Vec(R->GetArrayField(TEXT("location"))),Vec(R->GetArrayField(TEXT("scale")))),true);
 }
 auto* Door=World->SpawnActor<AVHAutomaticDoor>(Vec(DoorData->GetArrayField(TEXT("root"))),FRotator::ZeroRotator);Door->SetActorLabel(TEXT("D01 - Puerta automatica supercomputadora"));Door->DoorId=FName(*DoorData->GetStringField(TEXT("id")));auto Leaves=DoorData->GetArrayField(TEXT("leaves"));
 Door->LeftLeaf->SetStaticMesh(Meshes[Leaves[0]->AsObject()->GetStringField(TEXT("mesh"))]);Door->RightLeaf->SetStaticMesh(Meshes[Leaves[1]->AsObject()->GetStringField(TEXT("mesh"))]);Door->LeftClosedLocation=Vec(Leaves[0]->AsObject()->GetArrayField(TEXT("closed")));Door->RightClosedLocation=Vec(Leaves[1]->AsObject()->GetArrayField(TEXT("closed")));Door->OpeningWidth=DoorData->GetNumberField(TEXT("opening_width_cm"));Door->OpeningHeight=DoorData->GetNumberField(TEXT("opening_height_cm"));Door->TravelDistance=DoorData->GetNumberField(TEXT("travel_cm"));Door->MovementDuration=.8f;Door->CloseDelay=1.5f;Door->ProximityDepth=180;Door->SetDestinationConstructed(true);Door->SetSecurityLocked(false);Door->SetExternalAccessAllowed(true);Door->ResetClosed();
 auto* Sun=World->SpawnActor<ADirectionalLight>(FVector::ZeroVector,FRotator(-45,-35,0));Sun->SetActorLabel(TEXT("Luz provisional de validacion"));Sun->GetLightComponent()->SetIntensity(3);Sun->GetLightComponent()->SetMobility(EComponentMobility::Movable);
 auto* Sky=World->SpawnActor<ASkyLight>();Sky->GetLightComponent()->SetMobility(EComponentMobility::Movable);Sky->GetLightComponent()->SetIntensity(.7f);
 auto* Start=World->SpawnActor<APlayerStart>(Door->GetActorLocation()+FVector(-200,0,92),FRotator::ZeroRotator);Start->SetActorLabel(TEXT("Inicio provisional; sustituir pawn por Quinn en V06"));
 World->GetWorldSettings()->DefaultGameMode=AVHPreviewGameMode::StaticClass();World->SpawnActor<AVHFunctionalProbe>();
 Result->SetBoolField(TEXT("ok"),true);Result->SetNumberField(TEXT("mesh_assets"),Meshes.Num());Result->SetNumberField(TEXT("static_placements"),Data->GetArrayField(TEXT("instances")).Num());Result->SetNumberField(TEXT("material_assets"),Materials.Num());Result->SetStringField(TEXT("door_id"),Door->DoorId.ToString());return Json(Result);
}

FString UVHAutomaticDoorTools::RunChecks(AVHAutomaticDoor* Door){
 auto Report=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Cases;if(!Door){Report->SetStringField(TEXT("error"),TEXT("Missing door"));return Json(Report);}auto* World=Door->GetWorld();FActorSpawnParameters P;P.ObjectFlags|=RF_Transient;P.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 auto* Pawn=World->SpawnActor<ACharacter>(ACharacter::StaticClass(),Door->GetActorTransform().TransformPosition(FVector(-160,0,90)),FRotator::ZeroRotator,P);Pawn->GetCapsuleComponent()->SetCapsuleSize(35,90);Pawn->GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));Pawn->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
 auto Move=[&](FVector Local){Pawn->SetActorLocation(Door->GetActorTransform().TransformPosition(Local));};auto Advance=[&](float Seconds){for(int32 I=0;I<FMath::CeilToInt(Seconds*60);I++)Door->AdvanceDoor(1.f/60);};
 auto Check=[&](const TCHAR* Name,bool Pass){auto O=MakeShared<FJsonObject>();O->SetStringField(TEXT("name"),Name);O->SetBoolField(TEXT("pass"),Pass);O->SetNumberField(TEXT("fraction"),Door->OpenFraction);O->SetStringField(TEXT("state"),StaticEnum<EVHDoorState>()->GetNameStringByValue((int64)Door->DoorState));O->SetStringField(TEXT("blocking_mesh"),Door->LastBlockingMesh);O->SetStringField(TEXT("blocking_normal"),Door->LastBlockingNormal.ToString());O->SetNumberField(TEXT("penetration_depth_cm"),Door->LastPenetrationDepth);O->SetBoolField(TEXT("starts_penetrating"),Door->bLastStartPenetrating);Cases.Add(MakeShared<FJsonValueObject>(O));};
 auto Blocked=[&](){FHitResult H;FCollisionQueryParams Q(SCENE_QUERY_STAT(VHPassage),false);Q.AddIgnoredActor(Pawn);FVector C=Door->GetActorTransform().TransformPosition(FVector(0,0,95));return World->SweepSingleByChannel(H,C+Door->GetActorTransform().TransformVectorNoScale(FVector(-100,0,0)),C+Door->GetActorTransform().TransformVectorNoScale(FVector(100,0,0)),Door->GetActorQuat(),ECC_Pawn,FCollisionShape::MakeCapsule(35,90),Q);};
 Check(TEXT("closed_blocks_capsule"),Blocked());Advance(1.2f);Check(TEXT("approach_side_A_opens"),Door->OpenFraction>.999f);Check(TEXT("open_passage_is_clear"),!Blocked());
 Move(FVector(-500,0,90));Advance(3);Check(TEXT("automatic_close"),Door->OpenFraction<.001f&&Blocked());Move(FVector(160,0,90));Advance(1.2f);Check(TEXT("approach_side_B_opens"),Door->OpenFraction>.999f);
 Move(FVector(0,0,90));Advance(3);Check(TEXT("occupation_holds_open"),Door->IsDoorwayOccupied()&&Door->OpenFraction>.999f);Door->RequestClose();Advance(2);Check(TEXT("close_command_cannot_crush_occupant"),Door->OpenFraction>.999f);
 Move(FVector(500,0,90));Advance(1.7f);Check(TEXT("closing_starts_after_clear_delay"),Door->DoorState==EVHDoorState::Closing);int32 Before=Door->ClosingReversalCount;Move(FVector(0,0,90));Advance(.1f);Check(TEXT("occupant_interrupts_close"),Door->ClosingReversalCount>Before&&Door->DoorState!=EVHDoorState::Closing);Advance(1);Check(TEXT("reversal_reopens_fully"),Door->OpenFraction>.999f);
 Door->SetSecurityLocked(true);Advance(2);Check(TEXT("lock_respects_existing_occupant"),Door->OpenFraction>.999f);Move(FVector(500,0,90));Advance(3);Move(FVector(-160,0,90));Advance(1);Check(TEXT("locked_denies_approach"),Door->OpenFraction<.001f&&!Door->RequestOpen(Pawn));Door->SetSecurityLocked(false);Advance(1.2f);Check(TEXT("unlock_reopens_on_approach"),Door->OpenFraction>.999f);
 bool Repeated=true;for(int I=0;I<12;I++){Move(FVector(500,0,90));Advance(3);Repeated&=Door->OpenFraction<.001f;Move(FVector(I%2?160:-160,0,90));Advance(1.2f);Repeated&=Door->OpenFraction>.999f;}Check(TEXT("twelve_repeated_cycles_both_sides"),Repeated);
 Move(FVector(500,0,90));Advance(3);
 auto* Obstacle=World->SpawnActor<AActor>(AActor::StaticClass(),FTransform::Identity,P);auto* Box=NewObject<UBoxComponent>(Obstacle);Obstacle->SetRootComponent(Box);Obstacle->AddInstanceComponent(Box);Box->SetBoxExtent(FVector(.5,1,1));Box->SetCollisionProfileName(TEXT("BlockAll"));Box->RegisterComponent();
 Box->SetWorldLocation(Door->GetActorTransform().TransformPosition(Door->LeafLocationAtFraction(true,.95f)));Move(FVector(-160,0,90));Advance(1.2f);Check(TEXT("opening_obstacle_reports_blocked"),Door->DoorState==EVHDoorState::Blocked&&Door->OpenFraction<.99f);
 Box->SetCollisionEnabled(ECollisionEnabled::NoCollision);Advance(1.2f);Check(TEXT("removing_opening_obstacle_recovers"),Door->OpenFraction>.999f);
 Box->SetWorldLocation(Door->GetActorTransform().TransformPosition(Door->LeafLocationAtFraction(true,.15f)));Box->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);Move(FVector(500,0,90));Before=Door->ClosingReversalCount;Advance(2.5f);Check(TEXT("solid_obstacle_reverses_closing"),Door->ClosingReversalCount>Before);
 FCollisionQueryParams OverlapQuery(SCENE_QUERY_STAT(VHCrushCheck),false);Check(TEXT("solid_obstacle_not_penetrated"),!Door->LeftLeaf->ComponentOverlapComponent(Box,Box->GetComponentLocation(),Box->GetComponentQuat(),OverlapQuery));Box->SetCollisionEnabled(ECollisionEnabled::NoCollision);Obstacle->Destroy();Advance(3);
 Door->SetSecurityLocked(true);Door->SetDestinationConstructed(false);Door->SetEmergencyHoldOpen(true);Advance(2.f);Check(TEXT("emergency_cannot_open_unbuilt_destination"),Door->OpenFraction<.001f&&Door->DoorState==EVHDoorState::Blocked);Door->SetDestinationConstructed(true);Advance(1.2f);Check(TEXT("emergency_hold_open_command"),Door->OpenFraction>.999f);Advance(3);Check(TEXT("emergency_hold_open_persists_without_pawns"),Door->OpenFraction>.999f);Door->SetEmergencyHoldOpen(false);Advance(3);Check(TEXT("emergency_release_closes_under_lock"),Door->OpenFraction<.001f&&Door->DoorState==EVHDoorState::Blocked);Door->SetSecurityLocked(false);
 Pawn->Destroy();Door->ResetClosed();int32 Passed=0;for(auto V:Cases)if(V->AsObject()->GetBoolField(TEXT("pass")))Passed++;Report->SetArrayField(TEXT("cases"),Cases);Report->SetNumberField(TEXT("passed"),Passed);Report->SetNumberField(TEXT("total"),Cases.Num());Report->SetBoolField(TEXT("all_pass"),Passed==Cases.Num());Report->SetStringField(TEXT("method"),TEXT("Real Chaos queries, complete room, convex moving leaf collision; editor world calling the runtime AdvanceDoor. Separate game-world Tick probe required."));return Json(Report);
}

FString UVHAutomaticDoorTools::SetFloorClearance(AVHAutomaticDoor* Door,float ClearanceCm){
 auto Report=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Leaves;
 if(!Door||ClearanceCm<=0||ClearanceCm>1){Report->SetStringField(TEXT("error"),TEXT("A configured door and a clearance in (0,1] cm are required"));return Json(Report);}
 for(UStaticMeshComponent* Leaf:{Door->LeftLeaf.Get(),Door->RightLeaf.Get()}){
  UStaticMesh* Mesh=Leaf->GetStaticMesh();if(!Mesh||!Mesh->GetBodySetup())return TEXT("{\"error\":\"Missing leaf mesh or body\"}");
  FString Before=SurfaceDigest(Mesh);auto* Body=Mesh->GetBodySetup();FBox Bounds=Mesh->GetBoundingBox();float Cut=Bounds.Min.Z+ClearanceCm;
  FKConvexElem Hull;for(const FVertexID ID:Mesh->GetMeshDescription(0)->Vertices().GetElementIDs()){FVector V(FStaticMeshAttributes(*Mesh->GetMeshDescription(0)).GetVertexPositions()[ID]);V.Z=FMath::Max(V.Z,(double)Cut);Hull.VertexData.Add(V);}Hull.UpdateElemBox();Body->AggGeom.EmptyElements();Body->AggGeom.ConvexElems.Add(MoveTemp(Hull));Body->CollisionTraceFlag=CTF_UseSimpleAndComplex;Body->InvalidatePhysicsData();Body->CreatePhysicsMeshes();Leaf->RecreatePhysicsState();
  FString After=SurfaceDigest(Mesh);check(Before==After);check(Save(Mesh));auto R=MakeShared<FJsonObject>();R->SetStringField(TEXT("asset"),Mesh->GetPathName());R->SetStringField(TEXT("surface_digest_before"),Before);R->SetStringField(TEXT("surface_digest_after"),After);R->SetBoolField(TEXT("visual_geometry_normals_uv_unchanged"),true);R->SetNumberField(TEXT("collision_floor_clearance_cm"),ClearanceCm);Leaves.Add(MakeShared<FJsonValueObject>(R));
 }
 Report->SetBoolField(TEXT("ok"),true);Report->SetArrayField(TEXT("leaves"),Leaves);return Json(Report);
}

FString UVHAutomaticDoorTools::AuditImportedScene(const FString& SourceFile,const FString& Root){
 auto Report=MakeShared<FJsonObject>();FString Text;TSharedPtr<FJsonObject> Data;
 if(!FFileHelper::LoadFileToString(Text,*SourceFile)||!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text),Data))return TEXT("{\"error\":\"Cannot read source\"}");
 UWorld* World=GEditor->GetEditorWorldContext().World();TMap<FString,UStaticMesh*> Meshes;TMap<UStaticMesh*,UInstancedStaticMeshComponent*> Batches;TMap<UStaticMesh*,int32> Next;
 for(TActorIterator<AActor> It(World);It;++It){TArray<UInstancedStaticMeshComponent*> Parts;It->GetComponents(Parts);for(auto* Part:Parts)Batches.Add(Part->GetStaticMesh(),Part);}
 double PositionError=0,UVError=0,NormalError=0,WorldError=0;int32 Index=0,MeshCount=0,Placements=0;bool CountsMatch=true,MaterialsMatch=true,TransformsMatch=true;
 for(const auto& Entry:Data->GetObjectField(TEXT("meshes"))->Values){
  FString Key(Entry.Key.ToView());FString Asset=FString::Printf(TEXT("%s/Meshes/SM_%03d.SM_%03d"),*Root,Index,Index);Index++;auto* Mesh=LoadObject<UStaticMesh>(nullptr,*Asset);if(!Mesh||!Mesh->GetMeshDescription(0)){CountsMatch=false;continue;}Meshes.Add(Key,Mesh);MeshCount++;
  auto R=Entry.Value->AsObject();const FMeshDescription& MD=*Mesh->GetMeshDescription(0);FStaticMeshConstAttributes A(MD);auto V=R->GetArrayField(TEXT("vertices"));auto T=R->GetArrayField(TEXT("triangles"));CountsMatch&=MD.Vertices().Num()==V.Num()&&MD.VertexInstances().Num()==T.Num()*3;
  int32 J=0;for(const FVertexID ID:MD.Vertices().GetElementIDs()){if(J>=V.Num())break;PositionError=FMath::Max(PositionError,FVector::Distance(FVector(A.GetVertexPositions()[ID]),Vec(V[J++]->AsArray())));}
  J=0;for(const FVertexInstanceID ID:MD.VertexInstances().GetElementIDs()){if(J/3>=T.Num())break;auto Tri=T[J/3]->AsObject();auto U=Tri->GetArrayField(TEXT("uv"))[J%3]->AsArray();auto N=Vec(Tri->GetArrayField(TEXT("n"))[J%3]->AsArray());auto UV=A.GetVertexInstanceUVs().Get(ID,0);UVError=FMath::Max(UVError,FMath::Max(FMath::Abs(UV.X-U[0]->AsNumber()),FMath::Abs(UV.Y-U[1]->AsNumber())));NormalError=FMath::Max(NormalError,FVector::Distance(FVector(A.GetVertexInstanceNormals()[ID]),N));J++;}
  auto Names=R->GetArrayField(TEXT("materials"));MaterialsMatch&=Mesh->GetStaticMaterials().Num()==Names.Num();J=0;for(FPolygonGroupID G:MD.PolygonGroups().GetElementIDs()){if(J>=Names.Num()){MaterialsMatch=false;break;}MaterialsMatch&=A.GetPolygonGroupMaterialSlotNames()[G].ToString()==Names[J++]->AsString();}
 }
 for(const auto& Value:Data->GetArrayField(TEXT("instances"))){auto R=Value->AsObject();auto* Mesh=Meshes.FindRef(R->GetStringField(TEXT("mesh")));auto* Batch=Batches.FindRef(Mesh);if(!Batch){TransformsMatch=false;continue;}int32 Instance=Next.FindOrAdd(Mesh)++;FTransform Actual;if(!Batch->GetInstanceTransform(Instance,Actual,true)){TransformsMatch=false;continue;}auto Q=R->GetArrayField(TEXT("rotation"));FTransform Expected(FQuat(Q[0]->AsNumber(),Q[1]->AsNumber(),Q[2]->AsNumber(),Q[3]->AsNumber()),Vec(R->GetArrayField(TEXT("location"))),Vec(R->GetArrayField(TEXT("scale"))));FBox Box=Mesh->GetBoundingBox();for(int I=0;I<8;I++){FVector P(I&1?Box.Max.X:Box.Min.X,I&2?Box.Max.Y:Box.Min.Y,I&4?Box.Max.Z:Box.Min.Z);WorldError=FMath::Max(WorldError,FVector::Distance(Actual.TransformPosition(P),Expected.TransformPosition(P)));}Placements++;}
 for(auto& Entry:Batches)CountsMatch&=Next.FindRef(Entry.Key)==Entry.Value->GetInstanceCount();
 Report->SetBoolField(TEXT("ok"),CountsMatch&&MaterialsMatch&&TransformsMatch&&MeshCount==Data->GetObjectField(TEXT("meshes"))->Values.Num()&&PositionError<.002&&WorldError<.005&&UVError<.0001&&NormalError<.0001);Report->SetBoolField(TEXT("counts_match"),CountsMatch);Report->SetBoolField(TEXT("material_slots_match"),MaterialsMatch);Report->SetNumberField(TEXT("mesh_assets_checked"),MeshCount);Report->SetNumberField(TEXT("static_placements_checked"),Placements);Report->SetNumberField(TEXT("maximum_local_position_error_cm"),PositionError);Report->SetNumberField(TEXT("maximum_world_transform_error_cm"),WorldError);Report->SetNumberField(TEXT("maximum_uv_error"),UVError);Report->SetNumberField(TEXT("maximum_normal_error"),NormalError);return Json(Report);
}

FString UVHAutomaticDoorTools::TraceV07Surfaces(const FString& Input){
 TSharedPtr<FJsonObject> Data;if(!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Input),Data))return TEXT("{}");
 auto* W=GEditor->GetEditorWorldContext().World();TArray<TSharedPtr<FJsonValue>> Rows;
 for(auto V:Data->GetArrayField(TEXT("rays"))){auto R=V->AsObject();FHitResult H;FCollisionQueryParams Q;Q.bTraceComplex=true;bool Hit=W->LineTraceSingleByChannel(H,Vec(R->GetArrayField(TEXT("start"))),Vec(R->GetArrayField(TEXT("end"))),ECC_Visibility,Q);auto O=MakeShared<FJsonObject>();O->SetStringField(TEXT("id"),R->GetStringField(TEXT("id")));O->SetBoolField(TEXT("hit"),Hit);O->SetNumberField(TEXT("z"),H.ImpactPoint.Z);O->SetNumberField(TEXT("normal_z"),H.ImpactNormal.Z);O->SetStringField(TEXT("actor"),GetNameSafe(H.GetActor()));Rows.Add(MakeShared<FJsonValueObject>(O));}
 auto O=MakeShared<FJsonObject>();O->SetArrayField(TEXT("rays"),Rows);return Json(O);
}

bool UVHAutomaticDoorTools::ExportV07Geometry(const FString& File){
 auto* World=GEditor->GetEditorWorldContext().World();
 if(!World||!World->GetOutermost()->GetName().Contains(TEXT("V07"))||FPaths::FileExists(File))return false;
 auto Out=MakeShared<FJsonObject>();auto Meshes=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Instances;
 auto Array=[](FVector V){return TArray<TSharedPtr<FJsonValue>>{MakeShared<FJsonValueNumber>(V.X),MakeShared<FJsonValueNumber>(V.Y),MakeShared<FJsonValueNumber>(V.Z)};};
 for(TActorIterator<AActor> It(World);It;++It){TArray<UStaticMeshComponent*> Cs;It->GetComponents(Cs);for(auto* C:Cs){UStaticMesh* M=C->GetStaticMesh();if(!M||!M->GetMeshDescription(0))continue;FString Key=M->GetPathName();
  if(!Meshes->HasField(Key)){auto R=MakeShared<FJsonObject>();const auto& MD=*M->GetMeshDescription(0);FStaticMeshConstAttributes A(MD);TArray<TSharedPtr<FJsonValue>> Verts,Tris,Mats;TMap<FVertexID,int32> VertexIndex;TMap<FPolygonGroupID,int32> GroupIndex;
   for(auto V:MD.Vertices().GetElementIDs()){VertexIndex.Add(V,Verts.Num());Verts.Add(MakeShared<FJsonValueArray>(Array(FVector(A.GetVertexPositions()[V]))));}
   for(auto G:MD.PolygonGroups().GetElementIDs()){GroupIndex.Add(G,Mats.Num());auto Slot=A.GetPolygonGroupMaterialSlotNames()[G];auto Index=M->GetMaterialIndex(Slot);auto* Mat=M->GetMaterial(Index);if(!Mat)return false;Mats.Add(MakeShared<FJsonValueString>(Mat->GetPathName()));}
   for(auto T:MD.Triangles().GetElementIDs()){auto R2=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> VI,UVs,Ns;for(auto I:MD.GetTriangleVertexInstances(T)){VI.Add(MakeShared<FJsonValueNumber>(VertexIndex[MD.GetVertexInstanceVertex(I)]));auto UV=A.GetVertexInstanceUVs().Get(I,0);UVs.Add(MakeShared<FJsonValueArray>(TArray<TSharedPtr<FJsonValue>>{MakeShared<FJsonValueNumber>(UV.X),MakeShared<FJsonValueNumber>(UV.Y)}));Ns.Add(MakeShared<FJsonValueArray>(Array(FVector(A.GetVertexInstanceNormals()[I]))));}R2->SetArrayField(TEXT("v"),VI);R2->SetArrayField(TEXT("uv"),UVs);R2->SetArrayField(TEXT("n"),Ns);R2->SetNumberField(TEXT("material"),GroupIndex[MD.GetTrianglePolygonGroup(T)]);Tris.Add(MakeShared<FJsonValueObject>(R2));}
   R->SetArrayField(TEXT("vertices"),Verts);R->SetArrayField(TEXT("triangles"),Tris);R->SetArrayField(TEXT("materials"),Mats);Meshes->SetObjectField(Key,R);
  }
  auto* Batch=Cast<UInstancedStaticMeshComponent>(C);for(int32 I=0;I<(Batch?Batch->GetInstanceCount():1);++I){FTransform T=C->GetComponentTransform();if(Batch)Batch->GetInstanceTransform(I,T,true);auto R=MakeShared<FJsonObject>();R->SetStringField(TEXT("actor"),It->GetName());R->SetStringField(TEXT("component"),C->GetName());R->SetStringField(TEXT("mesh"),Key);R->SetNumberField(TEXT("index"),Batch?I:-1);TArray<TSharedPtr<FJsonValue>> Overrides;for(auto* Material:C->GetMaterials())Overrides.Add(MakeShared<FJsonValueString>(Material?Material->GetPathName():TEXT("")));R->SetArrayField(TEXT("overrides"),Overrides);R->SetArrayField(TEXT("location"),Array(T.GetLocation()));R->SetArrayField(TEXT("scale"),Array(T.GetScale3D()));auto Q=T.GetRotation();R->SetArrayField(TEXT("rotation"),{MakeShared<FJsonValueNumber>(Q.X),MakeShared<FJsonValueNumber>(Q.Y),MakeShared<FJsonValueNumber>(Q.Z),MakeShared<FJsonValueNumber>(Q.W)});Instances.Add(MakeShared<FJsonValueObject>(R));}
 }}Out->SetObjectField(TEXT("meshes"),Meshes);Out->SetArrayField(TEXT("instances"),Instances);return FFileHelper::SaveStringToFile(Json(Out),*File);
}

FString UVHAutomaticDoorTools::BuildV07Completion(const FString& File){
 auto* World=GEditor->GetEditorWorldContext().World();FString Text;TSharedPtr<FJsonObject> Data;
 if(!World||!World->GetOutermost()->GetName().Contains(TEXT("V07"))||!FFileHelper::LoadFileToString(Text,*File)||!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text),Data))return TEXT("{\"ok\":false,\"error\":\"Invalid V07 world or manifest\"}");
 for(TActorIterator<AActor> A(World);A;++A)if(A->ActorHasTag(TEXT("V07_COMPLETION")))return TEXT("{\"ok\":false,\"error\":\"Completion already exists\"}");
 struct FRemoval{UInstancedStaticMeshComponent* C;int32 I;};TArray<FRemoval> Remove;TSet<FString> Seen;
 for(auto V:Data->GetArrayField(TEXT("remove"))){auto R=V->AsObject();FString Actor=R->GetStringField(TEXT("actor")),Comp=R->GetStringField(TEXT("component"));int32 Index=R->GetIntegerField(TEXT("index"));FString Identity=Actor+TEXT("/")+Comp+FString::FromInt(Index);if(Seen.Contains(Identity))return TEXT("{\"ok\":false,\"error\":\"Duplicate removal\"}");Seen.Add(Identity);UInstancedStaticMeshComponent* Found=nullptr;
  for(TActorIterator<AActor> A(World);A;++A)if(A->GetName()==Actor){TArray<UInstancedStaticMeshComponent*> Cs;A->GetComponents(Cs);for(auto* C:Cs)if(C->GetName()==Comp)Found=C;}
  FTransform T;if(!Found||!Found->GetStaticMesh()||Found->GetStaticMesh()->GetPathName()!=R->GetStringField(TEXT("mesh"))||!Found->GetInstanceTransform(Index,T,true)||(!T.GetLocation().Equals(Vec(R->GetArrayField(TEXT("location"))),.005)||!T.GetScale3D().Equals(Vec(R->GetArrayField(TEXT("scale"))),.00001)||!T.GetRotation().Equals(FQuat(R->GetArrayField(TEXT("rotation"))[0]->AsNumber(),R->GetArrayField(TEXT("rotation"))[1]->AsNumber(),R->GetArrayField(TEXT("rotation"))[2]->AsNumber(),R->GetArrayField(TEXT("rotation"))[3]->AsNumber()),.00001)))return TEXT("{\"ok\":false,\"error\":\"Source identity changed\"}");Remove.Add({Found,Index});
 }
 TMap<FString,UMaterial*> Mats;for(auto V:Data->GetArrayField(TEXT("materials"))){FString Path=V->AsString();auto* M=LoadObject<UMaterial>(nullptr,*Path);if(!M)return TEXT("{\"ok\":false,\"error\":\"Missing material\"}");Mats.Add(Path,M);}
 for(auto V:Data->GetArrayField(TEXT("parts"))){auto R=V->AsObject();FString Path=TEXT("/Game/ValhallaV07/Completion/")+R->GetStringField(TEXT("name"));if(FPackageName::DoesPackageExist(Path))return TEXT("{\"ok\":false,\"error\":\"Target asset exists\"}");}
 for(auto V:Data->GetArrayField(TEXT("parts"))){auto R=V->AsObject();FString Name=R->GetStringField(TEXT("name"));auto* M=MakeMesh(R,TEXT("/Game/ValhallaV07/Completion/")+Name,Mats,false);auto* A=World->SpawnActor<AStaticMeshActor>();A->SetActorLabel(Name);A->Tags.Add(TEXT("V07_COMPLETION"));A->GetStaticMeshComponent()->SetStaticMesh(M);A->GetStaticMeshComponent()->SetCollisionProfileName(TEXT("BlockAll"));}
 Remove.Sort([](const FRemoval& A,const FRemoval& B){return A.C==B.C?A.I>B.I:UPTRINT(A.C)<UPTRINT(B.C);});for(auto R:Remove)check(R.C->RemoveInstance(R.I));
 auto Out=MakeShared<FJsonObject>();Out->SetBoolField(TEXT("ok"),true);Out->SetNumberField(TEXT("replaced_instances"),Remove.Num());Out->SetNumberField(TEXT("parts"),Data->GetArrayField(TEXT("parts")).Num());return Json(Out);
}

FString UVHAutomaticDoorTools::BuildDoorExtensions(const FString& File){
 FString Text;TSharedPtr<FJsonObject> Data;
 if(!FFileHelper::LoadFileToString(Text,*File)||!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Text),Data))return TEXT("{\"ok\":false,\"error\":\"Invalid manifest\"}");
 auto Result=MakeShared<FJsonObject>();auto* World=GEditor->GetEditorWorldContext().World();
 if(!World||!World->GetOutermost()->GetName().Contains(TEXT("V07")))return TEXT("{\"ok\":false,\"error\":\"Author only a NEW V07 map\"}");
 for(TActorIterator<AVHAutomaticDoor> I(World);I;++I)if(I->DoorId.ToString().StartsWith(TEXT("V07_")))return TEXT("{\"ok\":false,\"error\":\"V07 already authored\"}");
 TMap<FString,UMaterial*> Materials;
 for(const auto& E:Data->GetObjectField(TEXT("materials"))->Values){auto* M=LoadObject<UMaterial>(nullptr,*E.Value->AsString());if(!M)return TEXT("{\"ok\":false,\"error\":\"Missing source material\"}");Materials.Add(FString(E.Key.ToView()),M);}
 struct FRemove { UInstancedStaticMeshComponent* Component;int32 Index; };
 TArray<FRemove> Remove;TArray<TSharedPtr<FJsonValue>> Rows;
 // Resolve every source placement before creating assets or removing an instance.
 for(const auto& V:Data->GetArrayField(TEXT("doors"))){auto R=V->AsObject();TArray<FRemove> Found;FVector Location=Vec(R->GetArrayField(TEXT("original_location")));auto* Source=LoadObject<UStaticMesh>(nullptr,*R->GetStringField(TEXT("original_asset")));
  for(TActorIterator<AActor> A(World);A;++A){TArray<UInstancedStaticMeshComponent*> Cs;A->GetComponents(Cs);for(auto* C:Cs)if(C->GetStaticMesh()==Source)for(int32 J=0;J<C->GetInstanceCount();J++){FTransform T;C->GetInstanceTransform(J,T,true);if(T.GetLocation().Equals(Location,.005))Found.Add({C,J});}}
  if(Found.Num()!=1)return TEXT("{\"ok\":false,\"error\":\"Ambiguous source placement; no instances removed\"}");Remove.Add(Found[0]);
 }
 auto BuildPart=[&](const TSharedPtr<FJsonObject>& Part,const FString& Path,bool Leaf){
  auto Old=Part->GetArrayField(TEXT("materials"));TArray<TSharedPtr<FJsonValue>> Used;TMap<int32,int32> Slots;
  for(const auto& Value:Part->GetArrayField(TEXT("triangles"))){auto Tri=Value->AsObject();int32 Index=Tri->GetIntegerField(TEXT("material"));if(!Slots.Contains(Index)){Slots.Add(Index,Used.Num());Used.Add(Old[Index]);}Tri->SetNumberField(TEXT("material"),Slots[Index]);}
  Part->SetArrayField(TEXT("materials"),Used);return MakeMesh(Part,Path,Materials,Leaf);
 };
 int32 DoorIndex=0;
 for(const auto& V:Data->GetArrayField(TEXT("doors"))){auto R=V->AsObject();FString Id=R->GetStringField(TEXT("id"));FString Root=TEXT("/Game/ValhallaV07/Meshes/")+Id;
  FVector P=Vec(R->GetArrayField(TEXT("root")));FRotator Rot(0,R->GetNumberField(TEXT("yaw")),0);auto* Door=World->SpawnActor<AVHAutomaticDoor>(P,Rot);Door->DoorId=FName(*(TEXT("V07_")+Id));Door->SetActorLabel(Id+TEXT(" - automatica - destino no construido"));Door->Tags.Add(TEXT("V07_AUTOMATIC_DOOR"));
  auto Leaves=R->GetArrayField(TEXT("leaves"));int32 J=0;for(auto* C:{Door->LeftLeaf.Get(),Door->RightLeaf.Get()}){auto Leaf=Leaves[J]->AsObject();auto* M=BuildPart(Leaf->GetObjectField(TEXT("mesh")),Root+FString::Printf(TEXT("_Leaf%d"),J),true);C->SetStaticMesh(M);
   // A few source surfaces are open skins. Give the convex collision a small
   // thickness without changing any rendered vertex, UV, normal or material.
   auto* B=M->GetBodySetup();auto& Hull=B->AggGeom.ConvexElems[0];TArray<FVector> Points=Hull.VertexData;FBox Box=M->GetBoundingBox();Hull.VertexData.Reset();
   for(FVector Point:Points){Point.Z=FMath::Max(Point.Z,Box.Min.Z+.2);if(Box.GetSize().X<.2){auto Other=Point;Point.X-=.1;Other.X+=.1;Hull.VertexData.Add(Other);}Hull.VertexData.Add(Point);}Hull.UpdateElemBox();B->InvalidatePhysicsData();B->CreatePhysicsMeshes();C->RecreatePhysicsState();check(Save(M));
   if(J==0)Door->LeftClosedLocation=Vec(Leaf->GetArrayField(TEXT("closed")));else Door->RightClosedLocation=Vec(Leaf->GetArrayField(TEXT("closed")));J++;
  }
  Door->OpeningWidth=R->GetNumberField(TEXT("width"));Door->OpeningHeight=R->GetNumberField(TEXT("height"));Door->TravelDistance=R->GetNumberField(TEXT("travel"));Door->bUseConfiguredTravel=true;Door->LeftTravel=FVector(0,-Door->TravelDistance,0);Door->RightTravel=FVector(0,Door->TravelDistance,0);Door->LeftClearanceOffset=Door->RightClearanceOffset=FVector(Id==TEXT("D04")?20:-20,0,0);Door->ProximityDepth=240;Door->MovementDuration=.8f;Door->bUsePassageIntent=false;Door->SetSecurityLocked(true);Door->SetDestinationConstructed(false);Door->SetExternalAccessAllowed(true);Door->ResetClosed();
  if(R->HasField(TEXT("frame"))){auto* M=BuildPart(R->GetObjectField(TEXT("frame")),Root+TEXT("_OriginalFrame"),false);auto* A=World->SpawnActor<AStaticMeshActor>(P,Rot);A->SetActorLabel(Id+TEXT(" - marco original particionado"));A->GetStaticMeshComponent()->SetStaticMesh(M);A->GetStaticMeshComponent()->SetCollisionProfileName(TEXT("BlockAll"));A->Tags.Add(TEXT("V07_ORIGINAL_FRAME"));}
  auto O=MakeShared<FJsonObject>();O->SetStringField(TEXT("id"),Door->DoorId.ToString());O->SetNumberField(TEXT("width_cm"),Door->OpeningWidth);O->SetNumberField(TEXT("height_cm"),Door->OpeningHeight);O->SetBoolField(TEXT("locked_unbuilt_destination"),true);O->SetNumberField(TEXT("source_surface_area_error_cm2"),R->GetNumberField(TEXT("surface_area_error_cm2")));Rows.Add(MakeShared<FJsonValueObject>(O));DoorIndex++;
 }
 Remove.Sort([](const FRemove& A,const FRemove& B){return A.Component==B.Component?A.Index>B.Index:UPTRINT(A.Component)<UPTRINT(B.Component);});
 for(const auto& E:Remove)check(E.Component->RemoveInstance(E.Index));
 Result->SetBoolField(TEXT("ok"),true);Result->SetNumberField(TEXT("new_doors"),DoorIndex);Result->SetNumberField(TEXT("source_instances_partitioned"),Remove.Num());Result->SetArrayField(TEXT("doors"),Rows);return Json(Result);
}

FString UVHAutomaticDoorTools::SetV07LeafCollisionInset(AVHAutomaticDoor* Door,float InsetCm){
 if(!Door||InsetCm<0||InsetCm>4)return TEXT("{\"ok\":false,\"error\":\"Inset must be within 0..4 cm\"}");
 auto Result=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Rows;
 for(auto* Leaf:{Door->LeftLeaf.Get(),Door->RightLeaf.Get()}){
  UStaticMesh* Mesh=Leaf->GetStaticMesh();if(!Mesh||!Mesh->GetPathName().StartsWith(TEXT("/Game/ValhallaV07/Meshes/")))return TEXT("{\"ok\":false,\"error\":\"Only private V07 leaves may be changed\"}");
  FString Before=SurfaceDigest(Mesh);auto* Body=Mesh->GetBodySetup();auto Box=Mesh->GetBoundingBox();auto Center=Box.GetCenter();auto Size=Box.GetSize();FKConvexElem Hull;
  for(auto ID:Mesh->GetMeshDescription(0)->Vertices().GetElementIDs()){
   FVector P(FStaticMeshAttributes(*Mesh->GetMeshDescription(0)).GetVertexPositions()[ID]);
   P.Y=Center.Y+(P.Y-Center.Y)*FMath::Max(.1,1-2*InsetCm/FMath::Max(Size.Y,1.));
   P.Z=Center.Z+(P.Z-Center.Z)*FMath::Max(.1,1-2*InsetCm/FMath::Max(Size.Z,1.));
   P.Z=FMath::Max(P.Z,Box.Min.Z+.2);
   if(Size.X<.2){auto Q=P;P.X-=.1;Q.X+=.1;Hull.VertexData.Add(Q);}Hull.VertexData.Add(P);
  }
  Hull.UpdateElemBox();Body->AggGeom.EmptyElements();Body->AggGeom.ConvexElems.Add(MoveTemp(Hull));Body->CollisionTraceFlag=CTF_UseSimpleAndComplex;Body->InvalidatePhysicsData();Body->CreatePhysicsMeshes();Leaf->RecreatePhysicsState();check(Before==SurfaceDigest(Mesh));check(Save(Mesh));
  auto Row=MakeShared<FJsonObject>();Row->SetStringField(TEXT("mesh"),Mesh->GetPathName());Row->SetStringField(TEXT("surface_digest"),Before);Row->SetNumberField(TEXT("collision_inset_cm"),InsetCm);Row->SetBoolField(TEXT("visual_geometry_unchanged"),true);Rows.Add(MakeShared<FJsonValueObject>(Row));
 }
 Result->SetBoolField(TEXT("ok"),true);Result->SetArrayField(TEXT("leaves"),Rows);return Json(Result);
}
