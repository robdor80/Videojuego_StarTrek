#pragma once

#include "CoreMinimal.h"
#include "HostAcademyMenuFlow.h"
#include "HostSessionSubsystem.h"

enum class EAcademyConfirmation { None, Restore, Close, Exit };

class FHostAcademyMenu
{
public:
    explicit FHostAcademyMenu(UHostSessionSubsystem* Host = nullptr) : Session(Host) {}

    void Tick(UHostSessionSubsystem& Host, UHostWorldProjection& World);

    void OpenName();
    void OpenCatalog();
    void Back();
    void EditName(const FString& InName);
    void Create(const FString& InName);
    void ResetCreate();
    void ReloadCatalog();
    void LoadMore();
    void Select(const TSharedPtr<FHostAcademySlot>& Row);
    void RequestRestore();
    void RetryVerification();
    void Save(bool bCloseAfterSave);
    void RequestClose(bool bExit);
    void Confirm();
    void CancelConfirmation();

    const FAcademyMenuFlow& GetFlow() const { return Flow; }
    const TOptional<FHostAcademyCandidate>& GetCandidate() const { return Candidate; }
    const TArray<TSharedPtr<FHostAcademySlot>>& GetRows() const { return Rows; }
    const TSharedPtr<FHostAcademySlot>& GetSelected() const { return Selected; }
    const FString& GetName() const { return Name; }
    EAcademyConfirmation GetConfirmation() const { return Confirmation; }
    uint32 GetLayoutRevision() const { return LayoutRevision; }
    TrekHostCode GetAvailability() const;
    bool IsInitializing() const;
    bool IsBusy() const;
    bool IsReadyClosed() const;
    bool CanRestore() const;
    bool CanLoadMore() const;
    bool CanSave() const;
    bool CanRetryVerification() const;
    bool CanClose() const;
    bool CanExit() const;
    bool IsCatalogEmpty() const { return Catalog.IsEmpty(); }
    bool IsCatalogExpired() const { return bCatalogExpired; }
    bool CanResetCreate() const { return bCreateAttempt && IsReadyClosed(); }
    bool ShouldExit() const { return bExitWithoutSession || Flow.ExitRequested(); }
#if WITH_DEV_AUTOMATION_TESTS
    uint64 GetPendingTicket() const { return Receipt ? Receipt->Ticket : 0; }
#endif

private:
    void ChangeWorld(UHostWorldProjection& World);
    void Synchronize(UHostSessionSubsystem& Host, UHostWorldProjection& World);
    TrekHostCode Submit(UHostSessionSubsystem& Host, UHostWorldProjection& World);
    void Complete(UHostSessionSubsystem& Host, UHostWorldProjection& World, TrekHostCode Code);
    bool ReadCandidate(const UHostSessionSubsystem& Host, const UHostWorldProjection& World);
    bool ReadPage(const UHostWorldProjection& World);
    bool HasCurrentPage() const;
    void ClearCatalog(bool bExpired);
    void ClearBinding();
    void Start(EAcademyOperation Operation);
    void StartList(uint32 Cursor);

    TWeakObjectPtr<UHostSessionSubsystem> Session;
    TWeakObjectPtr<UHostWorldProjection> WorldProjection;
    TSharedPtr<FHostRequestReceipt> Receipt;
    FAcademyMenuFlow Flow;
    FAcademyMenuCatalog Catalog;
    TArray<TSharedPtr<FHostAcademySlot>> Rows;
    TSharedPtr<FHostAcademySlot> Selected;
    TOptional<FHostAcademySlot> RestoreVersion;
    TOptional<FHostAcademyCandidate> Candidate;
    FString Name;
    FString ExpectedCampaign;
    uint64 ExpectedGeneration = 0;
    uint64 PreviousGeneration = 0;
    uint64 VerifiedRevision = 0;
    uint64 VerifiedTick = 0;
    uint64 SavedRevision = 0;
    uint64 SavedTick = 0;
    uint32 RequestedCursor = 0;
    uint32 LayoutRevision = 0;
    int32 SubmitRetries = 0;
    double RetryAt = 0.0;
    EAcademyConfirmation Confirmation = EAcademyConfirmation::None;
    bool bCatalogExpired = false;
    bool bCreateAttempt = false;
    bool bExitWithoutSession = false;
};
