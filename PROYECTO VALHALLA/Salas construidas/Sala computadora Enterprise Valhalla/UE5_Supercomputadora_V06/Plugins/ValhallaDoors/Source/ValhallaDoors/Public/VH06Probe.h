#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "VH06Probe.generated.h"
class ACharacter;
class APlayerController;
class UInputAction;
class FJsonObject;
class FJsonValue;
/** Opt-in real-player traversal recorder; never runs in ordinary Play. */
UCLASS()
class VALHALLADOORS_API AVH06Probe : public AActor
{
    GENERATED_BODY()
  public:
    AVH06Probe();
    virtual void BeginPlay() override;
    virtual void Tick(float DeltaSeconds) override;

  private:
    UPROPERTY() TObjectPtr<ACharacter> Pawn;
    UPROPERTY() TObjectPtr<APlayerController> PC;
    UPROPERTY() TObjectPtr<UInputAction> MoveAction;
    TSharedPtr<FJsonObject> Plan, Report, Current;
    TArray<TSharedPtr<FJsonValue>> Cases, Results, Trace, Frames;
    FString ReportPath;
    int32 CaseIndex = -1, PointIndex = 0;
    float Elapsed = 0, SampleTime = 0, Settle = 0;
    double LastWall = 0;
    bool Active = false, Captured = false;
    float MovePause = 0, DoneTime = 0, MinFloor = 0;
    FVector Previous, Start;
    float Travel = 0;
    FVector LastBone = FVector::ZeroVector;
    float PoseChange = 0;
    void Next();
    void EndCase(bool Passed, const FString &Reason);
    void Finish();
    TSharedPtr<FJsonObject> Snapshot();
};
