#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "STAutomaticDoorTestLibrary.generated.h"
class ASTAutomaticDoor;
class UStaticMesh;
class ACharacter;
class AActor;
UCLASS()
class STAUTOMATICDOORSEDITOR_API USTAutomaticDoorTestLibrary:public UBlueprintFunctionLibrary {
 GENERATED_BODY()
public:
 UFUNCTION(BlueprintCallable,Category="P02|Validation")
 static FString RunAutomationChecks(UObject* WorldContextObject,UClass* DoorBlueprintClass,UStaticMesh* LeftMesh,UStaticMesh* RightMesh);
 UFUNCTION(BlueprintCallable,Category="P02|Validation")
 static FString AuditLeafPocketClearance(ASTAutomaticDoor* Door);
 UFUNCTION(BlueprintCallable,Category="P02|Validation")
 static FString RunRigChecks(ASTAutomaticDoor* Door);
 UFUNCTION(BlueprintCallable,Category="P02|Validation")
 static ACharacter* SpawnRuntimeValidationPawn(UObject* WorldContextObject,UClass* PawnClass,FVector Location);
 /** P03B validation only: reconstructed clipped surfaces and real leaves in transient actors. */
 UFUNCTION(BlueprintCallable,Category="P03B|Validation")
 static FString RunP03BChecks(UObject* WorldContextObject,UClass* DoorBlueprintClass,const FString& SceneFile);
 UFUNCTION(BlueprintCallable,Category="P03B|Authoring")
 static bool SetExactLeafConvexCollision(UStaticMesh* LeafMesh);
 UFUNCTION(BlueprintCallable,Category="P03C|Authoring")
 static bool ConfigureP03CWallCollision(UStaticMesh* WallMesh);
 UFUNCTION(BlueprintCallable,Category="P03C|Validation")
 static FString RunP03CPilotChecks(ASTAutomaticDoor* Door);
 UFUNCTION(BlueprintCallable,Category="P03D|Validation")
 static FString RunP03DChecks(ASTAutomaticDoor* Door);
 UFUNCTION(BlueprintCallable,Category="P03E|Validation")
 static FString RunP03EIntentChecks(ASTAutomaticDoor* Door);
 UFUNCTION(BlueprintCallable,Category="P03E|Validation")
 static bool SetValidationVelocity(ACharacter* Pawn,FVector Velocity);
 UFUNCTION(BlueprintCallable,Category="P03FG|Authoring") static AActor* CreateFGDestinationGuard(ASTAutomaticDoor* Door);
 UFUNCTION(BlueprintCallable,Category="P03FG|Validation") static FString RunFGDoorChecks(ASTAutomaticDoor* Door,bool ExpectGuard);
 UFUNCTION(BlueprintCallable,Category="P03FG|Authoring") static bool ConfigureFGLeafCollision(UStaticMesh* Mesh,int32 Slices);
 UFUNCTION(BlueprintCallable,Category="P03FG|Validation") static FString RunFGNavigation(ASTAutomaticDoor* Door);
 UFUNCTION(BlueprintCallable,Category="P03FG|Validation") static AActor* SpawnFGVisual(UObject* Context,UClass* Class,FTransform Transform);
};

