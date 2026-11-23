#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "VHAutomaticDoorTools.generated.h"
class AVHAutomaticDoor;
UCLASS()
class VALHALLADOORSEDITOR_API UVHAutomaticDoorTools : public UBlueprintFunctionLibrary {
 GENERATED_BODY()
public:
 UFUNCTION(BlueprintCallable,Category="Valhalla|Authoring") static FString BuildScene(const FString& SourceFile,const FString& PackageRoot);
 UFUNCTION(BlueprintCallable,Category="Valhalla|Validation") static FString RunChecks(AVHAutomaticDoor* Door);
 UFUNCTION(BlueprintCallable,Category="Valhalla|Authoring") static FString SetFloorClearance(AVHAutomaticDoor* Door,float ClearanceCm=.2f);
 UFUNCTION(BlueprintCallable,Category="Valhalla|Validation") static FString AuditImportedScene(const FString& SourceFile,const FString& PackageRoot);
 /** Import explicitly partitioned source faces into a NEW V07 copy only. */
 UFUNCTION(BlueprintCallable,Category="Valhalla|Authoring") static FString BuildDoorExtensions(const FString& SourceFile);
 UFUNCTION(BlueprintCallable,Category="Valhalla|Authoring") static FString SetV07LeafCollisionInset(AVHAutomaticDoor* Door,float InsetCm=1.f);
};
