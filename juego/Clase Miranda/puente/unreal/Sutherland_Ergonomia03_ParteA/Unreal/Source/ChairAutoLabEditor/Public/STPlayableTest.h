#pragma once
#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "STPlayableTest.generated.h"
UCLASS() class CHAIRAUTOLABEDITOR_API USTPlayableTest:public UBlueprintFunctionLibrary {
 GENERATED_BODY()
public:
 UFUNCTION(BlueprintCallable) static void BeginPlayablePIE();
 UFUNCTION(BlueprintCallable) static bool SendPlayerKey(APawn* Pawn,FString Key,bool Pressed);
 UFUNCTION(BlueprintCallable) static bool SendPlayerAxis(APawn* Pawn,FString Key,float Value);
 UFUNCTION(BlueprintCallable) static void Screenshot(FString Filename);
 UFUNCTION(BlueprintPure) static FString ViewportInfo();
 UFUNCTION(BlueprintCallable) static AActor* SpawnTransient(UObject* Context,UClass* Class,FTransform Transform);
 UFUNCTION(BlueprintCallable) static bool WriteSkinSnapshot(ACharacter* Character,FString Filename);
};
