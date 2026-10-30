#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "STCollisionReview.generated.h"
class UStaticMesh;
UCLASS() class CHAIRAUTOLABEDITOR_API USTCollisionReview: public UBlueprintFunctionLibrary {
 GENERATED_BODY()
public:
 UFUNCTION(BlueprintCallable) static FString DescribeActor(AActor* Actor);
 UFUNCTION(BlueprintCallable) static FString GenerateStandard(UStaticMesh* Mesh,bool Convex,int32 HullCount=8);
 UFUNCTION(BlueprintCallable) static bool CopyGeneratedCollision(UStaticMesh* Target,UStaticMesh* Proxy,bool Floor=false);
 UFUNCTION(BlueprintCallable) static FString Probe(UObject* Context,FVector Start,FVector End,float Radius=35,float HalfHeight=90,AActor* Isolate=nullptr,bool Complex=false);
};
