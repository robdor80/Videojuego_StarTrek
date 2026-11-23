#pragma once

#include "CoreMinimal.h"
#include "Async/Future.h"
#include "Containers/Ticker.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "Subsystems/WorldSubsystem.h"
#include "trek/host/academy_abi.h"
#include "HostSessionSubsystem.generated.h"

struct FHostAcademyCandidate
{
    FString Campaign;
    FString DisplayName;
    FString SourceDigest;
    uint64 Person = 0;
    uint64 CreationFact = 0;
    uint64 Revision = 0;
    uint64 Tick = 0;
    uint64 Generation = 0;
    uint32 Kind = TREK_HOST_KIND_UNKNOWN;
    uint32 CandidateState = 0;
};

struct FHostAcademySlot
{
    FString Campaign;
    FString Slot;
    uint64 Version = 0;
    uint32 Kind = TREK_HOST_KIND_UNKNOWN;
    uint32 Format = 0;
    uint32 Provenance = TREK_HOST_REJECTED;
    TrekHostCode Reason = TREK_HOST_SERVICE_UNAVAILABLE;
    bool bCompatible = false;
    bool bRecoverable = false;
};

struct FHostAcademyPage
{
    TArray<FHostAcademySlot> Rows;
    uint64 Generation = 0;
    uint32 NextCursor = 0;

    bool HasMore() const { return NextCursor != 0; }
};

struct FHostAcademyResult
{
    uint32 Operation = 0;
    TrekHostCode Code = TREK_HOST_SERVICE_UNAVAILABLE;
    uint64 Ticket = 0;
    uint64 Generation = 0;
};

// Optional observation of one admitted ticket. Mutations may finish after
// the submitting UWorld is gone. Read payloads remain in the world projection.
struct FHostRequestReceipt
{
    uint64 Ticket = 0;
    uint64 Generation = 0;
    TOptional<TrekHostCode> Code;
};

class FHostAcademyMenu;

UCLASS()
class UHostWorldProjection final : public UWorldSubsystem
{
    GENERATED_BODY()

public:
    const TOptional<TrekHostCampaignView>& GetCampaignView() const { return View; }
    const TOptional<TrekHostCompletion>& GetCompletion() const { return Completion; }
    const TOptional<FHostAcademyCandidate>& GetAcademyCandidate() const { return AcademyCandidate; }
    const TOptional<FHostAcademyPage>& GetAcademyPage() const { return AcademyPage; }
    const TOptional<FHostAcademyResult>& GetAcademyResult(uint32 Operation) const;
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
    void InvalidateCatalog();
    void Accept(const TrekHostCompletion& Result);
    void Accept(const TrekHostAcademyCompletion& Result);
    TrekHostCode RejectAcademy(uint32 Operation, TrekHostCode Code);

    TWeakObjectPtr<class UHostSessionSubsystem> Session;
    TOptional<TrekHostCampaignView> View;
    TOptional<TrekHostCompletion> Completion;
    TOptional<FHostAcademyCandidate> AcademyCandidate;
    TOptional<FHostAcademyPage> AcademyPage;
    TOptional<FHostAcademyResult> AcademyResults[TREK_HOST_ACADEMY_SLOTS + 1];
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
    bool IsInitializing() const { return Creating.IsValid(); }
    TrekHostCode GetAcademyAvailability() const;
    bool IsTransitioning() const { return Transition != 0; }
    const TrekHostStatus& GetStatus() const { return Status; }
    // Last published address for the naval diagnostic, including after CLOSE.
    const FString& GetCampaignAddress() const { return CampaignAddress; }

    TSharedRef<FHostAcademyMenu> GetAcademyMenu();

    TrekHostCode Open(UHostWorldProjection& World);
    TrekHostCode Close(UHostWorldProjection& World, TSharedPtr<FHostRequestReceipt>* Receipt = nullptr);
    TrekHostCode Query(UHostWorldProjection& World);
    TrekHostCode Save(UHostWorldProjection& World, const FString& Slot,
                      TSharedPtr<FHostRequestReceipt>* Receipt = nullptr);
    TrekHostCode Restore(UHostWorldProjection& World, const FString& Campaign, const FString& Slot);

    // Submit returns admission status. Read the operation result from the
    // attached world on a later tick. RETRY did not admit a native ticket.
    TrekHostCode CreateAcademy(UHostWorldProjection& World, const FString& Name,
                               TSharedPtr<FHostRequestReceipt>* Receipt = nullptr);
    TrekHostCode QueryAcademy(UHostWorldProjection& World, TSharedPtr<FHostRequestReceipt>* Receipt = nullptr);
    TrekHostCode ListAcademySlots(UHostWorldProjection& World, uint32 Cursor = 0,
                                  TSharedPtr<FHostRequestReceipt>* Receipt = nullptr);
    TrekHostCode RestoreAcademy(UHostWorldProjection& World, const FHostAcademySlot& Version,
                                TSharedPtr<FHostRequestReceipt>* Receipt = nullptr);

private:
    friend class UHostWorldProjection;
    void Attach(UHostWorldProjection& World);
    void Detach(UHostWorldProjection& World);

    struct FObservation
    {
        uint64 Ticket;
        TWeakObjectPtr<UHostWorldProjection> World;
        uint32 Operation;
        uint64 Generation;
        bool bAcademy;
        TWeakPtr<FHostRequestReceipt> Receipt;
        TOptional<TrekHostCompletion> NativeResult;
        TUniquePtr<TrekHostAcademyCompletion> AcademyNativeResult;

        bool IsReady() const { return NativeResult.IsSet() || AcademyNativeResult.IsValid(); }
        bool IsCatalog() const { return bAcademy && Operation == TREK_HOST_ACADEMY_SLOTS; }
    };

    bool Tick(float DeltaTime);
    bool RefreshStatus();
    void InvalidateProjections();
    void InvalidateCatalog();
    void DiscardObservations();
    void Discard(const FObservation& Entry);
    bool Poll(FObservation& Entry);
    void Publish(FObservation& Entry);
    TrekHostCode CheckAdmission(const UHostWorldProjection& World, bool bClosing) const;
    void Observe(UHostWorldProjection& World, uint64 Ticket, uint32 Operation,
                 uint64 Generation, bool bAcademy, bool bTransition, TSharedPtr<FHostRequestReceipt>* Receipt);
    TrekHostCode Submit(UHostWorldProjection& World, const TrekHostRequest& Request,
                        TSharedPtr<FHostRequestReceipt>* Receipt = nullptr);
    TrekHostCode Submit(UHostWorldProjection& World, const TrekHostAcademyRequest& Request,
                        TSharedPtr<FHostRequestReceipt>* Receipt);
    TrekHostCode Reject(UHostWorldProjection& World, uint32 Operation, TrekHostCode Code);
    TrekHostCode Restore(UHostWorldProjection& World, const FString& Campaign, const FString& Slot, uint64 Version,
                         TSharedPtr<FHostRequestReceipt>* Receipt = nullptr);

    TSharedPtr<const struct FHostApi, ESPMode::ThreadSafe> Api;
    TFuture<TrekHostClient*> Creating;
    TrekHostClient* Client = nullptr;
    FTSTicker::FDelegateHandle TickHandle;
    TrekHostStatus Status{sizeof(TrekHostStatus), TREK_HOST_CLOSED, 0,
                          TREK_HOST_SESSION_CLOSED, TREK_HOST_SERVICE_UNAVAILABLE};
    FString CampaignAddress;
    TArray<TWeakObjectPtr<UHostWorldProjection>> Worlds;
    TArray<FObservation, TInlineAllocator<TREK_HOST_ABI_MAX_PENDING + 1>> Pending;
    uint64 Transition = 0;
    uint64 LastCreationKey = 0;
    FString RetryCreationName;
    TSharedPtr<FHostAcademyMenu> AcademyMenu;
};
