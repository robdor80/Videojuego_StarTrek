#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/HUD.h"
#include "STPlayable.generated.h"
class USpringArmComponent; class UCameraComponent; class UAnimSequence; class UBlendSpace;
UENUM(BlueprintType) enum class ESTSeatPhase:uint8 { Walking, Approaching, Aligning, Sitting, Seated, Standing };
/** Reusable seat contract. No mesh, name lookup, or captain-specific code. */
UCLASS(Blueprintable) class F07P02_API ASTSeatAnchor:public AActor {
 GENERATED_BODY()
public:
 ASTSeatAnchor();
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneComponent> SeatRoot;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneComponent> Approach;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneComponent> SeatedCapsule;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneComponent> Pelvis;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneComponent> Back;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneComponent> LeftFoot;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneComponent> RightFoot;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneComponent> Exit;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<TObjectPtr<AActor>> ChairCollisionActors;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TObjectPtr<UAnimSequence> SitAnimation;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TObjectPtr<UAnimSequence> SeatedAnimation;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TObjectPtr<UAnimSequence> StandAnimation;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float InteractionDistance=165;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float SitSeconds=2.6f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float StandSeconds=2.6f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FVector SeatedMeshOffset=FVector(0,0,-109);
 UPROPERTY(EditAnywhere,BlueprintReadWrite) bool bInteractionEnabled=true;
 UPROPERTY(Transient,BlueprintReadOnly) TWeakObjectPtr<ACharacter> Occupant;
 UFUNCTION(BlueprintCallable) bool Reserve(ACharacter* Character);
 UFUNCTION(BlueprintCallable) void Release(ACharacter* Character);
 UFUNCTION(BlueprintPure) bool ExitIsClear(ACharacter* Character) const;
 UFUNCTION(BlueprintPure) bool ApproachIsClear(ACharacter* Character) const;
};
UCLASS(Blueprintable) class F07P02_API ASTPlayableQuinn:public ACharacter {
 GENERATED_BODY()
public:
 ASTPlayableQuinn();
 virtual void BeginPlay() override;
 virtual void Tick(float DeltaSeconds) override;
 virtual void EndPlay(const EEndPlayReason::Type Reason) override;
 virtual void SetupPlayerInputComponent(UInputComponent* Input) override;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USpringArmComponent> CameraBoom;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<UCameraComponent> FollowCamera;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) ESTSeatPhase SeatPhase=ESTSeatPhase::Walking;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<ASTSeatAnchor> ActiveSeat;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) FString InteractionMessage;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) int32 CompletedSitCycles=0;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float WalkSpeed=180;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) float RunSpeed=360;
 UFUNCTION(BlueprintCallable) bool Interact();
 UFUNCTION(BlueprintCallable) bool UseSeat(ASTSeatAnchor* Seat);
 UFUNCTION(BlueprintPure) ASTSeatAnchor* FindUsableSeat() const;
 UFUNCTION(BlueprintPure) FString RuntimeState() const;
private:
 void MoveForward(float Value); void MoveRight(float Value);void Turn(float Value);void Look(float Value);
 void InteractKey(); void RunOn(); void RunOff(); void JumpKey();
 void StartSitting();void FinishStanding();void AbortApproach();void SetSeatIgnores(bool Ignore);
 float PhaseTime=0;float ApproachTimeout=0;FTransform TransitionStart;
 FVector OriginalMeshOffset;FRotator OriginalMeshRotation;
 UPROPERTY() TObjectPtr<UClass> OriginalAnimClass;
 bool bRunning=false;
};
UCLASS() class F07P02_API ASTPlayableHUD:public AHUD { GENERATED_BODY() public: virtual void DrawHUD() override; };
UCLASS() class F07P02_API ASTPlayableGameMode:public AGameModeBase { GENERATED_BODY() public: ASTPlayableGameMode(); };
