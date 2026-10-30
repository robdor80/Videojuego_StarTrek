#include "STChairValidation.h"
#include "STSlidingChair.h"
#include "Engine/StaticMesh.h"
#include "StaticMeshResources.h"
#include "PhysicsEngine/BodySetup.h"
#include "AssetCompilingManager.h"
#include "Components/StaticMeshComponent.h"
#include "Components/BoxComponent.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "Engine/Engine.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"
FString USTChairValidation::MeshUVSnapshot(UStaticMesh* M){
 FAssetCompilingManager::Get().FinishAllCompilation();auto O=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Vertices,Channels;const auto& L=M->GetRenderData()->LODResources[0];
 for(uint32 I=0;I<L.VertexBuffers.PositionVertexBuffer.GetNumVertices();I++){auto V=L.VertexBuffers.PositionVertexBuffer.VertexPosition(I);TArray<TSharedPtr<FJsonValue>> A;for(float X:{V.X,V.Y,V.Z})A.Add(MakeShared<FJsonValueNumber>(X));Vertices.Add(MakeShared<FJsonValueArray>(A));}
 for(uint32 C=0;C<L.VertexBuffers.StaticMeshVertexBuffer.GetNumTexCoords();C++){TArray<TSharedPtr<FJsonValue>> Values;for(uint32 I=0;I<L.VertexBuffers.StaticMeshVertexBuffer.GetNumVertices();I++){auto UV=L.VertexBuffers.StaticMeshVertexBuffer.GetVertexUV(I,C);TArray<TSharedPtr<FJsonValue>> A;A.Add(MakeShared<FJsonValueNumber>(UV.X));A.Add(MakeShared<FJsonValueNumber>(UV.Y));Values.Add(MakeShared<FJsonValueArray>(A));}Channels.Add(MakeShared<FJsonValueArray>(Values));}
 O->SetArrayField(TEXT("vertices_local_cm"),Vertices);O->SetArrayField(TEXT("UV_channels"),Channels);FString Out;FJsonSerializer::Serialize(O,TJsonWriterFactory<>::Create(&Out));return Out;
}
FString USTChairValidation::PrepareCollision(UStaticMesh* M,bool Moving){
 if(!M||!M->GetPathName().StartsWith(TEXT("/Game/ChairAutoLab/")))return TEXT("Refused outside lab namespace");
 FAssetCompilingManager::Get().FinishAllCompilation();M->CreateBodySetup();auto* B=M->GetBodySetup();B->AggGeom.EmptyElements();B->bDoubleSidedGeometry=true;
 if(Moving){
  // Thin triangular prisms follow the real imported triangles. This avoids the
  // false positives of one convex hull over the open arm frame or crossbars.
  B->CollisionTraceFlag=CTF_UseSimpleAsComplex;
  const auto& L=M->GetRenderData()->LODResources[0];const auto& V=L.VertexBuffers.PositionVertexBuffer;
  for(int32 I=0;I+2<L.IndexBuffer.GetNumIndices();I+=3){FVector A(V.VertexPosition(L.IndexBuffer.GetIndex(I))),C(V.VertexPosition(L.IndexBuffer.GetIndex(I+1))),D(V.VertexPosition(L.IndexBuffer.GetIndex(I+2)));FVector N=FVector::CrossProduct(C-A,D-A).GetSafeNormal()*.005;
   if(N.IsNearlyZero())continue;FKConvexElem E;for(auto P:{A,C,D}){E.VertexData.Add(P+N);E.VertexData.Add(P-N);}E.UpdateElemBox();B->AggGeom.ConvexElems.Add(E);
  }
 }else B->CollisionTraceFlag=CTF_UseComplexAsSimple;
 B->InvalidatePhysicsData();B->CreatePhysicsMeshes();M->MarkPackageDirty();return FString::Printf(TEXT("%s: %d triangular prisms; static complex=%d"),*M->GetName(),B->AggGeom.ConvexElems.Num(),!Moving);
}
FString USTChairValidation::RunChecks(UObject* Context){
 auto O=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Cases,Rows;auto* W=GEngine->GetWorldFromContextObjectChecked(Context);FAssetCompilingManager::Get().FinishAllCompilation();TArray<ASTSlidingChair*> Chairs;
 auto Check=[&](FString Name,bool Pass){auto C=MakeShared<FJsonObject>();C->SetStringField(TEXT("name"),Name);C->SetBoolField(TEXT("pass"),Pass);Cases.Add(MakeShared<FJsonValueObject>(C));};
 for(TActorIterator<ASTSlidingChair> It(W);It;++It){Chairs.Add(*It);It->ResetRetracted();It->FixedBase->RecreatePhysicsState();for(auto C:It->MovingParts)C->RecreatePhysicsState();}
 Chairs.Sort([](const ASTSlidingChair& A,const ASTSlidingChair& B){return A.ChairId<B.ChairId;});
 for(auto* D:Chairs){auto Row=MakeShared<FJsonObject>();Row->SetStringField(TEXT("chair"),D->ChairId);auto Prefix=D->ChairId+TEXT("_");const FTransform Base=D->FixedBase->GetComponentTransform();const FVector Start=D->MovingRig->GetComponentLocation();TArray<FTransform> Initial;bool Meshes=D->MovingParts.Num()==15;
  for(auto C:D->MovingParts){Meshes&=C->GetStaticMesh()!=nullptr;Initial.Add(C->GetComponentTransform());}
  Check(Prefix+TEXT("15_moving_parts_plus_fixed_base"),Meshes&&D->FixedBase->GetStaticMesh()!=nullptr);Check(Prefix+TEXT("57cm_unit_scale_and_local_console_axis"),FMath::IsNearlyEqual(D->StrokeCm,57.f)&&D->GetActorScale3D().Equals(FVector::OneVector,.0001)&&D->LocalTravelDirection.Equals(FVector::ForwardVector));
  bool Req=D->Extend();Check(Prefix+TEXT("contradictory_retract_rejected"),Req&&!D->Retract());float MaxCoherence=0;int Steps=0;
  for(int I=0;I<122;I++){D->AdvanceChair(D->MovementDuration/120.f);Steps++;const FVector Delta=D->MovingRig->GetComponentLocation()-Start;for(int J=0;J<Initial.Num();J++)MaxCoherence=FMath::Max(MaxCoherence,float((D->MovingParts[J]->GetComponentLocation()-Initial[J].GetLocation()-Delta).Size()));}
  Row->SetStringField(TEXT("obstruction_forward"),D->LastObstruction);Row->SetNumberField(TEXT("forward_distance_cm"),(D->MovingRig->GetComponentLocation()-Start).Size());Row->SetNumberField(TEXT("coherence_error_cm"),MaxCoherence);
  Check(Prefix+TEXT("real_122_swept_steps_reach_configured_stroke"),D->ChairState==ESTChairState::Extended&&FMath::Abs((D->MovingRig->GetComponentLocation()-Start).Size()-D->StrokeCm)<.001f);Check(Prefix+TEXT("coherent_15_part_group"),MaxCoherence<.001f);Check(Prefix+TEXT("base_fixed_during_extension"),Base.Equals(D->FixedBase->GetComponentTransform(),.00001));
  D->Retract();for(int I=0;I<122;I++){D->AdvanceChair(D->MovementDuration/120.f);Steps++;}Row->SetStringField(TEXT("obstruction_return"),D->LastObstruction);Row->SetNumberField(TEXT("return_error_cm"),(D->MovingRig->GetComponentLocation()-Start).Size());Row->SetNumberField(TEXT("actual_movement_steps"),Steps);
  Check(Prefix+TEXT("return_exact_after_122_swept_steps"),D->ChairState==ESTChairState::Retracted&&D->MovingRig->GetComponentLocation().Equals(Start,.00001));Check(Prefix+TEXT("base_fixed_entire_round_trip"),Base.Equals(D->FixedBase->GetComponentTransform(),.00001));Check(Prefix+TEXT("occupancy_interface_empty"),!D->IsOccupied());Rows.Add(MakeShared<FJsonValueObject>(Row));
 }
 for(auto* D:Chairs){D->ResetRetracted();D->Extend();}for(int I=0;I<122;I++)for(auto* D:Chairs)D->AdvanceChair(D->MovementDuration/120.f);bool AllOpen=true;for(auto* D:Chairs)AllOpen&=D->ChairState==ESTChairState::Extended;Check(TEXT("simultaneous_all_extended"),AllOpen);
 for(auto* D:Chairs)D->Retract();for(int I=0;I<122;I++)for(auto* D:Chairs)D->AdvanceChair(D->MovementDuration/120.f);bool AllClosed=true;for(auto* D:Chairs)AllClosed&=D->ChairState==ESTChairState::Retracted;Check(TEXT("simultaneous_all_returned"),AllClosed);
 // Positive controls distinguish real physics protection from disabled collision.
 if(Chairs.Num()){
  auto* D=Chairs[0];const FVector Start=D->MovingRig->GetComponentLocation();FActorSpawnParameters SP;SP.ObjectFlags=RF_Transient;auto* Block=W->SpawnActor<AActor>(AActor::StaticClass(),FTransform(Start),SP);auto* Box=NewObject<UBoxComponent>(Block);Block->SetRootComponent(Box);Box->SetBoxExtent(FVector(70,70,120));Box->SetCollisionProfileName(TEXT("BlockAll"));Box->RegisterComponent();Box->SetWorldLocation(Start+FVector(0,0,40));
  D->Extend();D->AdvanceChair(.1f);Check(TEXT("positive_control_external_obstacle_blocks_entire_group"),D->ChairState==ESTChairState::Obstructed&&D->MovingRig->GetComponentLocation().Equals(Start,.00001)&&!D->LastObstruction.IsEmpty());Block->Destroy();D->ResetRetracted();
  FHitResult H;FCollisionQueryParams Q(SCENE_QUERY_STAT(ChairBase),false);for(auto* C:Chairs)Q.AddIgnoredActor(C);bool Floor=W->LineTraceSingleByChannel(H,FVector(0,0,150),FVector(0,0,-100),ECC_WorldDynamic,Q);Check(TEXT("positive_control_context_floor_has_real_collision"),Floor);
  FCollisionQueryParams RailQuery(SCENE_QUERY_STAT(ChairRail),false);for(auto C:D->MovingParts)RailQuery.AddIgnoredComponent(C.Get());auto Center=D->FixedBase->Bounds.Origin;bool Rail=W->LineTraceSingleByChannel(H,Center+FVector(0,0,20),Center-FVector(0,0,20),ECC_WorldDynamic,RailQuery);Check(TEXT("positive_control_fixed_rail_blocks_external_probe"),Rail&&H.GetComponent()==D->FixedBase);
 }
 O->SetArrayField(TEXT("chairs"),Rows);O->SetArrayField(TEXT("cases"),Cases);int Passed=0;for(auto C:Cases)if(C->AsObject()->GetBoolField(TEXT("pass")))Passed++;O->SetNumberField(TEXT("passed"),Passed);O->SetNumberField(TEXT("total"),Cases.Num());O->SetBoolField(TEXT("all_pass"),Passed==Cases.Num());O->SetStringField(TEXT("method"),TEXT("Actual UE component motion with real triangular-prism Chaos sweeps per part, whole group advances only if all clear. Own approved mast/base contact ignored within owning actor."));FString Out;FJsonSerializer::Serialize(O,TJsonWriterFactory<>::Create(&Out));return Out;
}

