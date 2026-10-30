#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STGameplayProof.generated.h"
class ASTPlayableQuinn;
class ACameraActor;
/** Optional -SutherlandGameplayProof standalone evidence, never spawned in normal Play. */
UCLASS() class F07P02_API ASTGameplayProof:public AActor {
 GENERATED_BODY()
public: ASTGameplayProof();virtual void BeginPlay() override;virtual void Tick(float Dt) override;
private:
 void Key(FName Name,bool Press);void Capture(const FString& Name);void Write(bool Complete=false,const FString& Error=TEXT(""));
 UPROPERTY() TObjectPtr<ASTPlayableQuinn> Quinn;
 int32 Phase=0,Waypoint=0,Frames=0;float Stage=0,Elapsed=0,LastSample=0;double WallStart=0,LastWall=0;
 TArray<FVector> Points;TArray<double> FrameMs;TArray<FString> Events;bool bWDown=false;
 bool bCaptureImages=true;FString ProofTag;
 bool bWaitingInCabin=false;float CabinWaitStart=0;
 int32 CameraSamples=0,CameraBlockedSamples=0;
 // Optional VISUAL_02 reference photos; never enabled in ordinary Play.
 bool bVisualReference=false,bVisualShot=false;FString VisualLabel;int32 VisualIndex=-1;float VisualStage=0;
 UPROPERTY() TObjectPtr<ACameraActor> VisualCamera;
 TArray<FVector> VisualEyes,VisualTargets;TArray<FString> VisualNames;
 void TickVisualReference(APlayerController* Controller);
};
