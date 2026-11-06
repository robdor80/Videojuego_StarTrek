#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "VH06Tools.generated.h"
class UStaticMesh;
UCLASS()
class VALHALLADOORSEDITOR_API UVH06Tools : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()
  public:
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06") static FString MapCheckSnapshot();
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06") static FString CorrectInstancedMaterialUsage();
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06")
    static FString SurveyGround(float CapsuleRadius, float CapsuleHalfHeight, float GridCm = 25);
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06") static void FinishCompilation();
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06") static FString ProbeSegments(const FString &Json);
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06") static FString AuditWinding();
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06") static FString CorrectWinding();
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06") static FString SetStairCollision(UStaticMesh *Mesh);
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06") static FString InspectFloor(float X, float Y);
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06") static FString CorrectFloorFaces();
    UFUNCTION(BlueprintCallable, Category = "Valhalla|V06") static FString MaterialResourceSnapshot();
};
