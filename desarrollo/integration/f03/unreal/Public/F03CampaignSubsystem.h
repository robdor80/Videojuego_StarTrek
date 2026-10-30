#pragma once
#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "GameFramework/Actor.h"
#include "f03_bridge.h"
#include "F03CampaignSubsystem.generated.h"

UCLASS()
class F02CORELAB_API AF03LogicalMarker : public AActor {
    GENERATED_BODY()
public:
    AF03LogicalMarker();
    UPROPERTY(VisibleAnywhere,Category="F03 diagnostic") FString LogicalId;
    UPROPERTY(VisibleAnywhere,Category="F03 diagnostic") int32 Location=0;
private:
    friend class UF03CampaignSubsystem;
    void Refresh(const F03MarkerState&,uint32 Detail);
};
// One campaign per GameInstance; transient visual bindings per (identity,UWorld).
// Diagnostic native methods only; no Blueprint/AI authority or raw world exposure.
UCLASS()
class F02CORELAB_API UF03CampaignSubsystem : public UGameInstanceSubsystem {
    GENERATED_BODY()
public:
    virtual void Initialize(FSubsystemCollectionBase&) override;
    virtual void Deinitialize() override;
    virtual void BeginDestroy() override;
    bool OpenLab();
    void CloseLab();
    AF03LogicalMarker* Represent(UWorld*,uint32 Ship=2,uint32 Detail=0);
    void Dematerialize(UWorld*);
    bool ScheduleRoute();
    bool Advance(uint64 Horizon);
    bool Acquire(uint32 Observer,uint32 Channel);
    bool SetPermission(bool Allowed);
    bool View(uint32 Observer,TArray<F03Fact>& Out) const;
    bool Save(TArray<uint8>& Out) const;
    bool Load(const TArray<uint8>&);
    bool WriteSave(const FString&) const;
    bool ReadSave(const FString&);
    bool Stats(F03Stats&) const;
private:
    F03Session* Session=nullptr;
    F03Handles Handles{};
    struct FVisual { TWeakObjectPtr<AF03LogicalMarker> Actor; uint32 Ship,Detail; };
    TArray<FVisual> Visuals;
    F03Ref Observer(uint32 Id) const;
    void ClearVisuals();
};
bool F03BridgeReady();
