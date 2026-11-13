#pragma once

#include "CoreMinimal.h"
#include "Containers/Ticker.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "Subsystems/WorldSubsystem.h"
#include "trek/host/host_abi.h"
#include "HostSessionSubsystem.generated.h"

UCLASS()
class UHostWorldProjection final : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    const TOptional<TrekHostCampaignView>& GetCampaignView() const { return View; }
    const TOptional<TrekHostCompletion>& GetCompletion() const { return Completion; }
    FString GetMessage() const { return Message; }

    virtual void OnWorldBeginPlay(UWorld& World) override;
    virtual void OnWorldEndPlay(UWorld& World) override;
    virtual void PreDeinitialize() override;

protected:
    virtual bool DoesSupportWorldType(EWorldType::Type Type) const override;

private:
    friend class UHostSessionSubsystem;

    void Detach();
    void Invalidate();
    void Accept(const TrekHostCompletion& Result);

    TWeakObjectPtr<class UHostSessionSubsystem> Session;
    TOptional<TrekHostCampaignView> View;
    TOptional<TrekHostCompletion> Completion;
    FString Message;
};

UCLASS()
class UHostSessionSubsystem final : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;

    bool IsAvailable() const { return Client != nullptr; }
    bool IsTransitioning() const { return Transition != 0; }
    const TrekHostStatus& GetStatus() const { return Status; }
    const FString& GetCampaignAddress() const { return CampaignAddress; }

    TrekHostCode Open(UHostWorldProjection& World);
    TrekHostCode Close(UHostWorldProjection& World);
    TrekHostCode Query(UHostWorldProjection& World);
    TrekHostCode Save(UHostWorldProjection& World, const FString& Slot);
    TrekHostCode Restore(UHostWorldProjection& World, const FString& Campaign, const FString& Slot);

private:
    friend class UHostWorldProjection;
    void Attach(UHostWorldProjection& World);
    void Detach(UHostWorldProjection& World);

    struct FObservation
    {
        uint64 Ticket;
        TWeakObjectPtr<UHostWorldProjection> World;
        TOptional<TrekHostCompletion> Ready;
    };

    bool Tick(float DeltaTime);
    bool RefreshStatus();
    void InvalidateProjections();
    void DiscardObservations();
    TrekHostCode Submit(UHostWorldProjection& World, const TrekHostRequest& Request);

    const struct FHostApi* Api = nullptr;
    TrekHostClient* Client = nullptr;
    FTSTicker::FDelegateHandle TickHandle;
    TrekHostStatus Status{sizeof(TrekHostStatus), TREK_HOST_CLOSED, 0,
                          TREK_HOST_SESSION_CLOSED, TREK_HOST_SERVICE_UNAVAILABLE};
    FString CampaignAddress;
    TArray<TWeakObjectPtr<UHostWorldProjection>> Worlds;
    TArray<FObservation, TInlineAllocator<TREK_HOST_ABI_MAX_PENDING + 1>> Pending;
    uint64 Transition = 0;
};
