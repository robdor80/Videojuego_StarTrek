#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "STChairValidation.generated.h"
class UStaticMesh;
UCLASS()
class CHAIRAUTOLABEDITOR_API USTChairValidation:public UBlueprintFunctionLibrary {
 GENERATED_BODY()
public:
 UFUNCTION(BlueprintCallable) static FString PrepareCollision(UStaticMesh* Mesh,bool Moving);
 UFUNCTION(BlueprintCallable) static FString RunChecks(UObject* WorldContext);
 UFUNCTION(BlueprintCallable) static FString MeshUVSnapshot(UStaticMesh* Mesh);
};
