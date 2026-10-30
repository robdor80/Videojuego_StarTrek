#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STSlidingChair.generated.h"
class UStaticMeshComponent;
UENUM(BlueprintType) enum class ESTChairState:uint8 { Retracted, Extending, Extended, Retracting, Obstructed };
UCLASS(Blueprintable)
class CHAIRAUTOLAB_API ASTSlidingChair:public AActor {
 GENERATED_BODY()
public:
 ASTSlidingChair();
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneComponent> FixedRoot;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<USceneComponent> MovingRig;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TObjectPtr<UStaticMeshComponent> FixedBase;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly) TArray<TObjectPtr<UStaticMeshComponent>> MovingParts;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Chair") FString ChairId;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Chair",meta=(ClampMin="0")) float StrokeCm=30;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Chair",meta=(ClampMin="0.05")) float MovementDuration=1;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Chair") FVector RetractedLocalPosition=FVector::ZeroVector;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Chair") FVector LocalTravelDirection=FVector::ForwardVector;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Chair") ESTChairState ChairState=ESTChairState::Retracted;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Chair") float Fraction=0;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Chair") FString LastObstruction;
 UPROPERTY(Transient,BlueprintReadOnly,Category="Chair") TWeakObjectPtr<AActor> Occupant;
 UFUNCTION(BlueprintCallable,Category="Chair") bool Extend();
 UFUNCTION(BlueprintCallable,Category="Chair") bool Retract();
 UFUNCTION(BlueprintCallable,Category="Chair") bool Toggle();
 UFUNCTION(BlueprintPure,Category="Chair") bool IsMoving() const;
 UFUNCTION(BlueprintPure,Category="Chair") bool IsOccupied() const {return Occupant.IsValid();}
 UFUNCTION(BlueprintCallable,Category="Chair") void SetOccupant(AActor* Actor){Occupant=Actor;}
 UFUNCTION(BlueprintCallable,Category="Chair") void AdvanceChair(float DeltaSeconds);
 UFUNCTION(BlueprintCallable,Category="Chair") void ResetRetracted();
 virtual void Tick(float DeltaSeconds) override;
 virtual void OnConstruction(const FTransform& Transform) override;
protected:
 virtual void BeginPlay() override;
private:
 float Elapsed=0,StartFraction=0,TargetFraction=0;
 bool Request(float Target);
 bool ApplyFraction(float Value,bool Sweep);
};

UCLASS(Blueprintable)
class CHAIRAUTOLAB_API ASTChairLabControls:public AActor {
 GENERATED_BODY()
public:
 ASTChairLabControls();
 virtual void BeginPlay() override;
 UFUNCTION(BlueprintCallable) void ExtendAll();
 UFUNCTION(BlueprintCallable) void RetractAll();
 UFUNCTION(BlueprintCallable) void Toggle01();
 UFUNCTION(BlueprintCallable) void Toggle02();
 UFUNCTION(BlueprintCallable) void Toggle03();
 UFUNCTION(BlueprintCallable) void Toggle04();
 UFUNCTION(BlueprintCallable) void Toggle05();
 UFUNCTION(BlueprintCallable) void Toggle06();
 void ToggleIndex(int Index);
};
