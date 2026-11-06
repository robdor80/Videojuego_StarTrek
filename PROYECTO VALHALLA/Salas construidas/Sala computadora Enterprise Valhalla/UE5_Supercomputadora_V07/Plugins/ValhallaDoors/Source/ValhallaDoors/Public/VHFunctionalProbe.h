#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Character.h"
#include "GameFramework/GameModeBase.h"
#include "VHFunctionalProbe.generated.h"
class AVHAutomaticDoor;
class UCameraComponent;
class FJsonValue;
UCLASS()
class VALHALLADOORS_API AVHPreviewCharacter:public ACharacter {
 GENERATED_BODY()
public:
 AVHPreviewCharacter();
 virtual void SetupPlayerInputComponent(UInputComponent* Input) override;
private:
 void Forward(float Value);void Strafe(float Value);void Turn(float Value);void Look(float Value);
 UPROPERTY() TObjectPtr<UCameraComponent> Camera;
};
UCLASS()
class VALHALLADOORS_API AVHPreviewGameMode:public AGameModeBase {
 GENERATED_BODY()
public: AVHPreviewGameMode();
};
/** Dormant unless explicitly launched with -VHRunValidation and -VHValidationReport. */
UCLASS()
class VALHALLADOORS_API AVHFunctionalProbe:public AActor {
 GENERATED_BODY()
public:
 AVHFunctionalProbe();
 virtual void BeginPlay() override;
 virtual void Tick(float DeltaSeconds) override;
private:
 UPROPERTY() TObjectPtr<AVHAutomaticDoor> Door;
 UPROPERTY() TObjectPtr<ACharacter> Pawn;
 FString ReportPath;
 TArray<TSharedPtr<FJsonValue>> Results;
 int32 Phase=0,Cycle=0,Reversals=0;float Elapsed=0;
 void Check(const FString& Name,bool Passed);void MovePawn(float X,float Y=0);bool PassageBlocked() const;void Finish();
};
