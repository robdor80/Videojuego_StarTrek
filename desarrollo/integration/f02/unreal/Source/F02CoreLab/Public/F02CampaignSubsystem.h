#pragma once
#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "GameFramework/Actor.h"
#include "GameFramework/GameModeBase.h"
#include "f02_bridge.h"
#include "F02CampaignSubsystem.generated.h"

UCLASS()
class F02CORELAB_API AF02LogicalMarker : public AActor {
    GENERATED_BODY()
public:
    AF02LogicalMarker();
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="F02 diagnostic")
    FString LogicalId;
private:
    friend class UF02CampaignSubsystem;
    void Bind(uint64 Id);
};

// GameInstance lifetime outlives Actors and streamed scenes. No BlueprintCallable
// mutation APIs, UPROPERTY WorldState, external session/grants, or AI entrypoints.
UCLASS()
class F02CORELAB_API UF02CampaignSubsystem : public UGameInstanceSubsystem {
    GENERATED_BODY()
public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;
    virtual void BeginDestroy() override;
    bool OpenLab();
    void CloseLab();
    AF02LogicalMarker* Represent(UWorld* World);
    bool Exists() const;
    FString DiagnosticId() const;
    bool Place();
    bool Save(TArray<uint8>& Bytes) const;
    bool Load(const TArray<uint8>& Bytes);
    bool WriteSave(const FString& Path) const;
    bool ReadSave(const FString& Path);
    bool VerifyProjection() const;
private:
    F02Session* Session = nullptr;
    F02Handles Handles{};
    TArray<TWeakObjectPtr<AF02LogicalMarker>> Visuals;
    void ClearVisuals();
};

UCLASS()
class F02CORELAB_API AF02DemoGameMode : public AGameModeBase {
    GENERATED_BODY()
public:
    virtual void BeginPlay() override;
private:
    UPROPERTY() TObjectPtr<UF02CampaignSubsystem> Host;
    UPROPERTY() TObjectPtr<AF02LogicalMarker> Marker;
    FTimerHandle DemoTimer;
    int32 Step = 0;
    FString InitialId;
    void Advance();
};

bool F02BridgeReady();
