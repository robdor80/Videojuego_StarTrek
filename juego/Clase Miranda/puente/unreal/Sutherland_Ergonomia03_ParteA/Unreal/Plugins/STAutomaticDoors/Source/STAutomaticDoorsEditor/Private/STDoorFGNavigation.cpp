#include "STAutomaticDoorTestLibrary.h"
#include "STAutomaticDoor.h"
#include "Components/StaticMeshComponent.h"
#include "NavMesh/NavMeshBoundsVolume.h"
#include "NavMesh/RecastNavMesh.h"
#include "NavigationSystem.h"
#include "NavigationPath.h"
#include "AI/NavigationSystemBase.h"
#include "Builders/CubeBuilder.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"
#include "Engine/Engine.h"
#include "Model.h"
#include "Components/BrushComponent.h"
#include "EngineUtils.h"
#include "Engine/Polys.h"
AActor* USTAutomaticDoorTestLibrary::SpawnFGVisual(UObject* Context,UClass* Class,FTransform Transform){auto* W=GEngine->GetWorldFromContextObject(Context,EGetWorldErrorMode::ReturnNull);if(!W||!Class||!W->GetPathName().Contains(TEXT("F07P03FG")))return nullptr;FActorSpawnParameters P;P.ObjectFlags=RF_Transient;P.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;return W->SpawnActor<AActor>(Class,Transform,P);}
FString USTAutomaticDoorTestLibrary::RunFGNavigation(ASTAutomaticDoor* D){
 if(!D)return TEXT("{\"ok\":false,\"error\":\"Missing door\"}");auto* W=D->GetWorld();auto T=D->GetActorTransform();D->ResetClosed();D->LeftLeaf->SetRelativeLocation(D->LeftClosedLocation+FVector(0,-D->TravelDistance,0));D->RightLeaf->SetRelativeLocation(D->RightClosedLocation+FVector(0,D->TravelDistance,0));
 FActorSpawnParameters SP;SP.ObjectFlags=RF_Transient;auto* V=W->SpawnActor<ANavMeshBoundsVolume>(T.TransformPosition(FVector(0,0,200)),FRotator::ZeroRotator,SP);V->Brush=NewObject<UModel>(V,NAME_None,RF_Transient);V->Brush->Initialize(V,false);V->GetBrushComponent()->Brush=V->Brush;auto* Builder=NewObject<UCubeBuilder>(V);V->BrushBuilder=Builder;Builder->X=1200;Builder->Y=1200;Builder->Z=650;Builder->Build(W,V);V->Brush->BuildBound();V->GetBrushComponent()->UpdateBounds();V->PostEditChange();V->SetActorLocation(T.TransformPosition(FVector(0,0,200)));
 auto* Nav=FNavigationSystem::GetCurrent<UNavigationSystemV1>(W);if(!Nav){FNavigationSystem::AddNavigationSystemToWorld(*W,FNavigationSystemRunMode::EditorMode);Nav=FNavigationSystem::GetCurrent<UNavigationSystemV1>(W);}
 auto J=MakeShared<FJsonObject>();bool OK=false;TArray<TSharedPtr<FJsonValue>> Points;
 J->SetStringField(TEXT("volume_bounds"),V->GetComponentsBoundingBox(true).ToString());J->SetNumberField(TEXT("volume_polygons"),V->Brush&&V->Brush->Polys?V->Brush->Polys->Element.Num():-1);int Meshes=0,Relevant=0;for(TActorIterator<AActor> It(W);It;++It){TArray<UStaticMeshComponent*> C;It->GetComponents(C);for(auto* X:C){Meshes++;Relevant+=X->CanEverAffectNavigation();}}J->SetNumberField(TEXT("static_mesh_components"),Meshes);J->SetNumberField(TEXT("nav_eligible_components"),Relevant);
 if(Nav){Nav->OnNavigationBoundsAdded(V);Nav->RemoveNavigationBuildLock(ENavigationBuildLock::AsyncLoadLock);Nav->Tick(.1f);auto* Data=Nav->GetDefaultNavDataInstance(FNavigationSystem::Create);if(auto* R=Cast<ARecastNavMesh>(Data)){R->SetActorLabel(TEXT("P03FG_TransientNavigationProof"));R->AgentRadius=35;R->AgentHeight=180;}
 Nav->Build();if(Data)Data->EnsureBuildCompletion();J->SetNumberField(TEXT("registered_bounds"),Nav->GetNavigationBounds().Num());J->SetStringField(TEXT("navigable_world_bounds"),Nav->GetNavigableWorldBounds().ToString());if(auto* Recast=Cast<ARecastNavMesh>(Data)){J->SetStringField(TEXT("recast_bounds"),Recast->GetNavMeshBounds().ToString());J->SetNumberField(TEXT("tile_capacity"),Recast->GetNavMeshTilesCount());}FNavLocation PS,PE;J->SetBoolField(TEXT("start_projects"),Nav->ProjectPointToNavigation(T.TransformPosition(FVector(-180,0,0)),PS,FVector(80,80,250)));J->SetBoolField(TEXT("end_projects"),Nav->ProjectPointToNavigation(T.TransformPosition(FVector(160,0,0)),PE,FVector(80,80,250)));auto* Path=UNavigationSystemV1::FindPathToLocationSynchronously(W,T.TransformPosition(FVector(-180,0,0)),T.TransformPosition(FVector(160,0,0)));OK=Path&&Path->IsValid()&&!Path->IsPartial();if(Path){J->SetBoolField(TEXT("partial"),Path->IsPartial());J->SetNumberField(TEXT("length_cm"),Path->GetPathLength());for(auto X:Path->PathPoints){TArray<TSharedPtr<FJsonValue>> A;auto P=T.InverseTransformPosition(X);for(double X1:{P.X,P.Y,P.Z})A.Add(MakeShared<FJsonValueNumber>(X1));Points.Add(MakeShared<FJsonValueArray>(A));}}}
 J->SetBoolField(TEXT("ok"),OK);J->SetArrayField(TEXT("path_local_cm"),Points);J->SetStringField(TEXT("scope"),TEXT("Actual Recast bake and full path bridge to existing cabin, D04 physically open, agent radius35 height180. Transient editor proof, no AI or automatic navigation links; no assets saved."));V->Destroy();D->ResetClosed();FString Out;FJsonSerializer::Serialize(J,TJsonWriterFactory<>::Create(&Out));return Out;
}
