#include "HostAcademyMenu.h"

#include "HAL/PlatformTime.h"

namespace
{
const TCHAR* MainSlot = TEXT("principal");
constexpr int32 MaxSubmitRetries = 5;
constexpr double SubmitRetryDelay = 0.08;
}

TrekHostCode FHostAcademyMenu::GetAvailability() const
{
    const auto* Host = Session.Get();
    return Host ? Host->GetAcademyAvailability() : TREK_HOST_SERVICE_UNAVAILABLE;
}

bool FHostAcademyMenu::IsInitializing() const
{
    const auto* Host = Session.Get();
    return Host && Host->IsInitializing();
}

bool FHostAcademyMenu::IsBusy() const
{
    const auto* Host = Session.Get();
    return Flow.Busy() || (Host && Host->IsTransitioning());
}

bool FHostAcademyMenu::IsReadyClosed() const
{
    const auto* Host = Session.Get();
    return Host && WorldProjection.IsValid() && GetAvailability() == TREK_HOST_OK && !IsBusy() &&
           Confirmation == EAcademyConfirmation::None && Host->GetStatus().state == TREK_HOST_CLOSED;
}

bool FHostAcademyMenu::HasCurrentPage() const
{
    const auto* World = WorldProjection.Get();
    return World && Catalog.HasPage() && World->GetAcademyPage().IsSet();
}

bool FHostAcademyMenu::CanRestore() const
{
    return Flow.Screen() == EAcademyScreen::Catalog && IsReadyClosed() && HasCurrentPage() && Selected &&
           FAcademyMenuCatalog::CanRestore(Selected->Kind, Selected->Version, Selected->bCompatible,
                                          Selected->bRecoverable, Selected->Reason);
}

bool FHostAcademyMenu::CanLoadMore() const
{
    return Flow.Screen() == EAcademyScreen::Catalog && IsReadyClosed() && HasCurrentPage() && Catalog.Cursor() != 0;
}

bool FHostAcademyMenu::CanSave() const
{
    const auto* Host = Session.Get();
    return Host && Candidate.IsSet() && GetAvailability() == TREK_HOST_OK && !IsBusy() && Flow.CanSave() &&
           Confirmation == EAcademyConfirmation::None && Host->GetStatus().state == TREK_HOST_ACTIVE &&
           Candidate->Generation == Host->GetStatus().generation;
}

bool FHostAcademyMenu::CanClose() const
{
    const auto* Host = Session.Get();
    return Host && WorldProjection.IsValid() && !IsBusy() && Confirmation == EAcademyConfirmation::None &&
           Host->GetStatus().state != TREK_HOST_CLOSED && Host->GetStatus().state != TREK_HOST_SAVING;
}

bool FHostAcademyMenu::CanExit() const
{
    const auto* Host = Session.Get();
    return !ShouldExit() && !IsBusy() && Confirmation == EAcademyConfirmation::None &&
           (!Host || Host->GetStatus().state == TREK_HOST_CLOSED || CanClose());
}

void FHostAcademyMenu::OpenName()
{
    if (!IsReadyClosed()) return;
    ClearCatalog(false);
    if (!bCreateAttempt) Name.Reset();
    Flow.Navigate(EAcademyScreen::Name);
}

void FHostAcademyMenu::OpenCatalog()
{
    if (!IsReadyClosed() || !Flow.Navigate(EAcademyScreen::Catalog)) return;
    ReloadCatalog();
}

void FHostAcademyMenu::Back()
{
    if (IsBusy() || Confirmation != EAcademyConfirmation::None) return;
    if (Flow.Screen() == EAcademyScreen::Name || Flow.Screen() == EAcademyScreen::Catalog)
    {
        ClearCatalog(false);
        Flow.Navigate(EAcademyScreen::Main);
    }
}

void FHostAcademyMenu::EditName(const FString& InName)
{
    if (Flow.Screen() == EAcademyScreen::Name && IsReadyClosed()) Name = InName;
}

void FHostAcademyMenu::Create(const FString& InName)
{
    if (Flow.Screen() != EAcademyScreen::Name || !IsReadyClosed()) return;
    Name = InName;
    Start(EAcademyOperation::Create);
}

void FHostAcademyMenu::ResetCreate()
{
    if (CanResetCreate()) Start(EAcademyOperation::ResetCreate);
}

void FHostAcademyMenu::ReloadCatalog()
{
    if (Flow.Screen() != EAcademyScreen::Catalog || !IsReadyClosed()) return;
    ClearCatalog(false);
    StartList(0);
}

void FHostAcademyMenu::LoadMore()
{
    if (CanLoadMore()) StartList(Catalog.Cursor());
}

void FHostAcademyMenu::Select(const TSharedPtr<FHostAcademySlot>& Row)
{
    if (Flow.Screen() == EAcademyScreen::Catalog && IsReadyClosed() && (!Row || Rows.Contains(Row)))
    {
        Selected = Row;
    }
}

void FHostAcademyMenu::RequestRestore()
{
    if (CanRestore())
    {
        Confirmation = EAcademyConfirmation::Restore;
        ++LayoutRevision;
    }
}

bool FHostAcademyMenu::CanRetryVerification() const
{
    const auto* Host = Session.Get();
    return Host && Flow.CanRetryVerification() && !IsBusy() &&
           Confirmation == EAcademyConfirmation::None && GetAvailability() == TREK_HOST_OK &&
           Host->GetStatus().state == TREK_HOST_ACTIVE;
}

void FHostAcademyMenu::RetryVerification()
{
    if (CanRetryVerification())
    {
        Flow.RetryVerification();
        SubmitRetries = 0;
        RetryAt = 0;
    }
}

void FHostAcademyMenu::Save(bool bCloseAfterSave)
{
    if (CanSave()) Start(bCloseAfterSave ? EAcademyOperation::SaveAndClose : EAcademyOperation::Save);
}

void FHostAcademyMenu::RequestClose(bool bExit)
{
    if (bExit ? !CanExit() : !CanClose()) return;
    if (!CanClose())
    {
        if (bExit && bCreateAttempt && Session.IsValid() && WorldProjection.IsValid())
        {
            Start(EAcademyOperation::ExitClose);
        }
        else if (bExit)
        {
            bExitWithoutSession = true;
        }
        return;
    }

    if (!Flow.HasConfirmedProgress() || !Candidate.IsSet())
    {
        Confirmation = bExit ? EAcademyConfirmation::Exit : EAcademyConfirmation::Close;
        ++LayoutRevision;
        return;
    }
    Start(bExit ? EAcademyOperation::ExitClose : EAcademyOperation::Close);
}

void FHostAcademyMenu::Confirm()
{
    const auto Choice = Confirmation;
    CancelConfirmation();
    if (Choice == EAcademyConfirmation::Restore && CanRestore())
    {
        RestoreVersion = *Selected;
        PreviousGeneration = Session->GetStatus().generation;
        Start(EAcademyOperation::Restore);
    }
    else if ((Choice == EAcademyConfirmation::Close || Choice == EAcademyConfirmation::Exit) && CanClose())
    {
        Start(Choice == EAcademyConfirmation::Exit ? EAcademyOperation::ExitClose : EAcademyOperation::Close);
    }
}

void FHostAcademyMenu::CancelConfirmation()
{
    if (Confirmation != EAcademyConfirmation::None)
    {
        Confirmation = EAcademyConfirmation::None;
        ++LayoutRevision;
    }
}

void FHostAcademyMenu::Start(EAcademyOperation Operation)
{
    if (Flow.Begin(Operation))
    {
        SubmitRetries = 0;
        RetryAt = 0;
    }
}

void FHostAcademyMenu::StartList(uint32 Cursor)
{
    RequestedCursor = Cursor;
    Selected.Reset();
    ++LayoutRevision;
    Start(EAcademyOperation::List);
}

void FHostAcademyMenu::ClearCatalog(bool bExpired)
{
    Catalog = {};
    Rows.Reset();
    Selected.Reset();
    bCatalogExpired = bExpired;
    if (Confirmation == EAcademyConfirmation::Restore) CancelConfirmation();
    ++LayoutRevision;
}

void FHostAcademyMenu::ClearBinding()
{
    Candidate.Reset();
    ExpectedCampaign.Reset();
    ExpectedGeneration = 0;
    VerifiedRevision = VerifiedTick = SavedRevision = SavedTick = 0;
}

void FHostAcademyMenu::ChangeWorld(UHostWorldProjection& World)
{
    const bool bReplaced = WorldProjection.IsStale() || WorldProjection.IsValid();
    WorldProjection = &World;
    if (!bReplaced) return;

    Candidate.Reset();
    CancelConfirmation();
    if (IsAcademyVerification(Flow.Operation()))
    {
        // The old read projection was detached. Requery the live generation.
        Receipt.Reset();
        SubmitRetries = 0;
        RetryAt = 0;
    }
    else if (Flow.Operation() == EAcademyOperation::List)
    {
        Receipt.Reset();
        Flow.Resolve(TREK_HOST_GENERATION_EXPIRED);
    }
    if (Flow.Operation() == EAcademyOperation::Restore && !Receipt)
    {
        RestoreVersion.Reset();
        Flow.Resolve(TREK_HOST_GENERATION_EXPIRED);
    }
    if (Flow.Screen() == EAcademyScreen::Catalog) ClearCatalog(true);
    if (Flow.Screen() == EAcademyScreen::Candidate && !Flow.Busy()) Flow.VerifyWorld();
}

void FHostAcademyMenu::Synchronize(UHostSessionSubsystem& Host, UHostWorldProjection& World)
{
    const auto& Status = Host.GetStatus();
    if (Flow.Screen() == EAcademyScreen::Catalog && Catalog.HasPage() && !World.GetAcademyPage().IsSet())
    {
        ClearCatalog(true);
    }
    if (ExpectedGeneration && ExpectedGeneration != Status.generation)
    {
        ClearBinding();
        CancelConfirmation();
        Flow.ResetSession();
    }
    if (Status.state == TREK_HOST_ACTIVE &&
        (Flow.Screen() == EAcademyScreen::Main || Flow.Screen() == EAcademyScreen::Name ||
         Flow.Screen() == EAcademyScreen::Catalog ||
         (Flow.Screen() == EAcademyScreen::Candidate && !Candidate.IsSet())))
    {
        if (Flow.Screen() == EAcademyScreen::Catalog) ClearCatalog(true);
        Flow.VerifyWorld();
    }
    else if (Status.state == TREK_HOST_CLOSED &&
             (Flow.Screen() == EAcademyScreen::Recovery || Flow.Screen() == EAcademyScreen::Candidate))
    {
        ClearBinding();
        CancelConfirmation();
        Flow.ResetSession();
    }
}

void FHostAcademyMenu::AttachView(UHostWorldProjection& World)
{
    if (WorldProjection.Get() != &World) ChangeWorld(World);
}

void FHostAcademyMenu::Tick(UHostSessionSubsystem& Host, UHostWorldProjection& World)
{
    AttachView(World);
    if (ShouldExit()) return;

    if (Receipt)
    {
        if (Receipt->Code.IsSet())
        {
            Complete(Host, World, Receipt->Code.GetValue());
            Receipt.Reset();
        }
        return;
    }
    if (Host.IsInitializing() || Host.IsTransitioning()) return;

    if (!Flow.Busy() && GetAvailability() == TREK_HOST_OK) Synchronize(Host, World);
    if (!Flow.Busy() || FPlatformTime::Seconds() < RetryAt) return;

    const TrekHostCode Code = Submit(Host, World);
    if (Code == TREK_HOST_OK) return;
    if (Code == TREK_HOST_RETRY && SubmitRetries < MaxSubmitRetries)
    {
        ++SubmitRetries;
        RetryAt = FPlatformTime::Seconds() + SubmitRetryDelay;
        return;
    }
    Complete(Host, World, Code);
}

TrekHostCode FHostAcademyMenu::Submit(UHostSessionSubsystem& Host, UHostWorldProjection& World)
{
    const auto Operation = Flow.Operation();
    const auto& Status = Host.GetStatus();
    if (IsAcademyVerification(Operation) || IsAcademySave(Operation))
    {
        if (ExpectedGeneration && ExpectedGeneration != Status.generation) return TREK_HOST_GENERATION_EXPIRED;
        if (IsAcademyVerification(Operation)) return Host.QueryAcademy(World, &Receipt);
        return Host.Save(World, MainSlot, &Receipt);
    }

    switch (Operation)
    {
    case EAcademyOperation::Create:
        if (Status.state != TREK_HOST_CLOSED) return TREK_HOST_BUSY_STATE;
        if (const auto Code = Host.CreateAcademy(World, Name, &Receipt); Code != TREK_HOST_OK) return Code;
        bCreateAttempt = true;
        return TREK_HOST_OK;
    case EAcademyOperation::List:
        if (Status.state != TREK_HOST_CLOSED) return TREK_HOST_BUSY_STATE;
        return Host.ListAcademySlots(World, RequestedCursor, &Receipt);
    case EAcademyOperation::Restore:
        if (!RestoreVersion.IsSet() || !HasCurrentPage()) return TREK_HOST_GENERATION_EXPIRED;
        return Host.RestoreAcademy(World, *RestoreVersion, &Receipt);
    case EAcademyOperation::Close:
    case EAcademyOperation::ExitClose:
        if (ExpectedGeneration && Status.generation != ExpectedGeneration && Status.state != TREK_HOST_CLOSED)
            return TREK_HOST_GENERATION_EXPIRED;
        return Host.Close(World, &Receipt);
    case EAcademyOperation::ResetCreate:
        return Status.state == TREK_HOST_CLOSED ? Host.Close(World, &Receipt) : TREK_HOST_BUSY_STATE;
    default:
        return TREK_HOST_INVALID_ARGUMENT;
    }
}

void FHostAcademyMenu::Complete(UHostSessionSubsystem& Host, UHostWorldProjection& World, TrekHostCode Code)
{
    const auto Operation = Flow.Operation();
    const auto& Status = Host.GetStatus();
    if (Code == TREK_HOST_OK && (!Receipt || !Receipt->Ticket || Receipt->Generation != Status.generation))
    {
        Code = TREK_HOST_GENERATION_EXPIRED;
    }
    if (Code == TREK_HOST_OK)
    {
        if (Operation == EAcademyOperation::Create || Operation == EAcademyOperation::Restore)
        {
            ExpectedCampaign = Host.GetCampaignAddress();
            ExpectedGeneration = Status.generation;
            if (!ExpectedGeneration || ExpectedCampaign.IsEmpty() ||
                (Operation == EAcademyOperation::Restore &&
                 (!RestoreVersion.IsSet() || ExpectedGeneration == PreviousGeneration || ExpectedCampaign != RestoreVersion->Campaign)))
            {
                Code = TREK_HOST_IDENTITY_MISMATCH;
            }
        }
        else if (IsAcademyVerification(Operation) && !ReadCandidate(Host, World))
        {
            Code = TREK_HOST_IDENTITY_MISMATCH;
        }
        else if (Operation == EAcademyOperation::List && !ReadPage(World))
        {
            Code = TREK_HOST_GENERATION_EXPIRED;
        }
        else if (IsAcademySave(Operation))
        {
            SavedRevision = VerifiedRevision;
            SavedTick = VerifiedTick;
        }
        else if (Operation == EAcademyOperation::Close || Operation == EAcademyOperation::ExitClose ||
                 Operation == EAcademyOperation::ResetCreate)
        {
            if (Status.state == TREK_HOST_CLOSED)
            {
                ClearBinding();
                ClearCatalog(false);
                bCreateAttempt = false;
            }
            else
            {
                Code = TREK_HOST_BUSY_STATE;
            }
        }
    }

    if (Operation == EAcademyOperation::List && Code != TREK_HOST_OK &&
        (Receipt || Code == TREK_HOST_GENERATION_EXPIRED))
    {
        ClearCatalog(Code == TREK_HOST_GENERATION_EXPIRED);
    }
    if (Operation == EAcademyOperation::Restore)
    {
        RestoreVersion.Reset();
        if (Receipt || Code == TREK_HOST_GENERATION_EXPIRED) ClearCatalog(Code != TREK_HOST_OK);
    }
    if (Operation == EAcademyOperation::Create && Code == TREK_HOST_IDEMPOTENCY_CONFLICT) bCreateAttempt = true;

    const bool bSaveOutcomeUnknown = Receipt && IsAcademySave(Operation) &&
        (Code == TREK_HOST_UNKNOWN_TICKET || Code == TREK_HOST_ABI_MISMATCH);
    Flow.Resolve(Code, bSaveOutcomeUnknown);
    if ((Operation == EAcademyOperation::Create || Operation == EAcademyOperation::Restore) &&
        Code != TREK_HOST_OK && Status.state == TREK_HOST_ACTIVE)
    {
        Flow.ShowUnverifiedSession();
    }
    SubmitRetries = 0;
    RetryAt = 0;
    ++LayoutRevision;
}

bool FHostAcademyMenu::ReadCandidate(const UHostSessionSubsystem& Host, const UHostWorldProjection& World)
{
    const auto& Result = World.GetAcademyResult(TREK_HOST_ACADEMY_QUERY);
    const auto& Value = World.GetAcademyCandidate();
    const auto& Status = Host.GetStatus();
    if (!Result.IsSet() || Result->Ticket != Receipt->Ticket || !Value.IsSet() ||
        Status.state != TREK_HOST_ACTIVE || Status.principal != TREK_HOST_OK ||
        Value->Generation != Status.generation || !Value->Generation ||
        Value->Kind != TREK_HOST_KIND_ACADEMY || Value->CandidateState != TREK_HOST_CANDIDATE ||
        Value->Campaign.IsEmpty() || Value->DisplayName.IsEmpty() || !Value->Person || !Value->CreationFact ||
        (!ExpectedCampaign.IsEmpty() && ExpectedCampaign != Value->Campaign))
    {
        return false;
    }

    if (Flow.Operation() == EAcademyOperation::VerifyNew && !Value->DisplayName.Equals(Name, ESearchCase::CaseSensitive))
    {
        return false;
    }
    if (Flow.Operation() == EAcademyOperation::VerifyRestore)
    {
        SavedRevision = Value->Revision;
        SavedTick = Value->Tick;
    }
    else if (SavedRevision != Value->Revision || SavedTick != Value->Tick)
    {
        Flow.ProgressChanged();
    }
    Candidate = *Value;
    ExpectedCampaign = Value->Campaign;
    ExpectedGeneration = Value->Generation;
    VerifiedRevision = Value->Revision;
    VerifiedTick = Value->Tick;
    return true;
}

bool FHostAcademyMenu::ReadPage(const UHostWorldProjection& World)
{
    const auto& Result = World.GetAcademyResult(TREK_HOST_ACADEMY_SLOTS);
    const auto& Page = World.GetAcademyPage();
    if (!Result.IsSet() || Result->Ticket != Receipt->Ticket || !Page.IsSet() ||
        Page->Generation != Receipt->Generation || (RequestedCursor && Page->NextCursor == RequestedCursor))
    {
        return false;
    }

    Rows.Reset();
    for (const auto& Row : Page->Rows)
    {
        if (Row.Kind == TREK_HOST_KIND_ACADEMY) Rows.Add(MakeShared<FHostAcademySlot>(Row));
    }
    Catalog.Accept(Page->NextCursor, !Rows.IsEmpty());
    bCatalogExpired = false;
    return true;
}
