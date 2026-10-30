#include "STPlayableTest.h"
#include "Editor.h"
#include "PlayInEditorDataTypes.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/Pawn.h"
#include "InputKeyEventArgs.h"
#include "UnrealClient.h"
#include "Engine/GameViewportClient.h"
#include "Engine/Engine.h"
#include "HAL/IConsoleManager.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/Character.h"
#include "Components/SkeletalMeshComponent.h"
#include "Rendering/SkeletalMeshRenderData.h"
#include "SkeletalRenderPublic.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"
#include "Misc/FileHelper.h"
void USTPlayableTest::BeginPlayablePIE(){FRequestPlaySessionParams P;P.WorldType=EPlaySessionWorldType::PlayInEditor;P.SessionDestination=EPlaySessionDestinationType::InProcess;GEditor->RequestPlaySession(P);}
bool USTPlayableTest::SendPlayerKey(APawn* Pawn,FString Key,bool Pressed){auto* PC=Pawn?Cast<APlayerController>(Pawn->GetController()):nullptr;if(!PC)return false;return PC->InputKey(FInputKeyEventArgs::CreateSimulated(FKey(*Key),Pressed?IE_Pressed:IE_Released,Pressed?1:0));}
bool USTPlayableTest::SendPlayerAxis(APawn* Pawn,FString Key,float Value){auto* PC=Pawn?Cast<APlayerController>(Pawn->GetController()):nullptr;if(!PC)return false;return PC->InputKey(FInputKeyEventArgs::CreateSimulated(FKey(*Key),IE_Axis,Value));}
void USTPlayableTest::Screenshot(FString Filename){FScreenshotRequest::RequestScreenshot(Filename,true,false);}
FString USTPlayableTest::ViewportInfo(){UGameViewportClient* C=GEngine?GEngine->GameViewport.Get():nullptr;auto* V=C?C->Viewport:nullptr;const FIntPoint S=V?V->GetSizeXY():FIntPoint::ZeroValue;auto* Screen=IConsoleManager::Get().FindConsoleVariable(TEXT("r.ScreenPercentage"));return FString::Printf(TEXT("viewport=%dx%d screenPercentage=%.1f"),S.X,S.Y,Screen?Screen->GetFloat():0);}
AActor* USTPlayableTest::SpawnTransient(UObject* Context,UClass* Class,FTransform Transform){auto* W=GEngine->GetWorldFromContextObject(Context,EGetWorldErrorMode::ReturnNull);if(!W||!Class||!W->GetPathName().Contains(TEXT("Sutherland_Playable01")))return nullptr;FActorSpawnParameters P;P.ObjectFlags=RF_Transient;P.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;return W->SpawnActor<AActor>(Class,Transform,P);}
bool USTPlayableTest::WriteSkinSnapshot(ACharacter* Character,FString Filename){
 if(!Character||!Character->GetMesh())return false;auto* MeshComponent=Character->GetMesh();auto* Asset=MeshComponent->GetSkeletalMeshAsset();if(!Asset||!Asset->GetResourceForRendering())return false;
 TArray<FFinalSkinVertex> V;MeshComponent->GetCPUSkinnedVertices(V,0);if(V.IsEmpty())return false;
 const auto& LOD=Asset->GetResourceForRendering()->LODRenderData[0];const auto* Indices=LOD.MultiSizeIndexContainer.GetIndexBuffer();auto J=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Positions,Triangles;
 for(const auto& Vertex:V){const FVector P=MeshComponent->GetComponentTransform().TransformPosition(FVector(Vertex.Position));TArray<TSharedPtr<FJsonValue>> C;C.Add(MakeShared<FJsonValueNumber>(P.X));C.Add(MakeShared<FJsonValueNumber>(P.Y));C.Add(MakeShared<FJsonValueNumber>(P.Z));Positions.Add(MakeShared<FJsonValueArray>(C));}
 for(int32 I=0;I+2<Indices->Num();I+=3){TArray<TSharedPtr<FJsonValue>> C;for(int32 K=0;K<3;K++)C.Add(MakeShared<FJsonValueNumber>(Indices->Get(I+K)));Triangles.Add(MakeShared<FJsonValueArray>(C));}
 J->SetArrayField(TEXT("vertices_world_cm"),Positions);J->SetArrayField(TEXT("triangles"),Triangles);J->SetStringField(TEXT("character"),Character->GetPathName());J->SetBoolField(TEXT("player_controlled"),Character->IsPlayerControlled());J->SetStringField(TEXT("source"),TEXT("Actual live Character component CPU-skinned vertices, LOD0, current animation pose"));FString Out;FJsonSerializer::Serialize(J,TJsonWriterFactory<>::Create(&Out));return FFileHelper::SaveStringToFile(Out,*Filename);
}

