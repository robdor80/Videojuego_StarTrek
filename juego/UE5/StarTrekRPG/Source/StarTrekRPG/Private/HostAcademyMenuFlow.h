#pragma once

#include "trek/host/academy_abi.h"

enum class EAcademyScreen { Main, Name, Catalog, Recovery, Candidate };
enum class EAcademySave { Unconfirmed, Confirmed, Restored, Failed, Uncertain };
enum class EAcademyOperation
{
    None, Create, VerifyNew, FirstSave, List, Restore, VerifyRestore, VerifyWorld,
    Save, SaveAndClose, Close, ExitClose, ResetCreate
};

inline bool IsAcademyVerification(EAcademyOperation Operation)
{
    return Operation == EAcademyOperation::VerifyNew || Operation == EAcademyOperation::VerifyRestore ||
           Operation == EAcademyOperation::VerifyWorld;
}

inline bool IsAcademySave(EAcademyOperation Operation)
{
    return Operation == EAcademyOperation::FirstSave || Operation == EAcademyOperation::Save ||
           Operation == EAcademyOperation::SaveAndClose;
}

// Presentation sequencing. The adapter resolves an operation only with a
// rejected submission or with the outcome of its admitted HOST ticket.
class FAcademyMenuFlow
{
public:
    EAcademyScreen Screen() const { return CurrentScreen; }
    EAcademyOperation Operation() const { return Pending; }
    EAcademyOperation LastOperation() const { return Last; }
    TrekHostCode Error() const { return LastError; }
    EAcademySave SaveState() const { return Saved; }
    bool Busy() const { return Pending != EAcademyOperation::None; }
    bool CanSave() const { return !Busy() && CurrentScreen == EAcademyScreen::Candidate && Saved != EAcademySave::Uncertain; }
    bool HasConfirmedProgress() const { return Saved == EAcademySave::Confirmed || Saved == EAcademySave::Restored; }
    bool ExitRequested() const { return bExitRequested; }

    bool Navigate(EAcademyScreen Screen)
    {
        if (Busy()) return false;
        CurrentScreen = Screen;
        LastError = TREK_HOST_OK;
        return true;
    }

    bool Begin(EAcademyOperation Operation)
    {
        if (Busy() || bExitRequested) return false;
        if (IsAcademySave(Operation) && !CanSave()) return false;
        Pending = Operation;
        LastError = TREK_HOST_OK;
        return true;
    }

    void Resolve(TrekHostCode Code, bool bSaveOutcomeUnknown = false)
    {
        const auto Completed = Pending;
        Last = Completed;
        LastError = Code;
        Pending = EAcademyOperation::None;

        if (IsAcademyVerification(Completed))
        {
            Verification = Completed;
            if (Code != TREK_HOST_OK)
            {
                CurrentScreen = EAcademyScreen::Recovery;
                return;
            }

            if (Completed == EAcademyOperation::VerifyNew)
            {
                Saved = EAcademySave::Unconfirmed;
                Pending = EAcademyOperation::FirstSave;
                return;
            }
            if (Completed == EAcademyOperation::VerifyRestore) Saved = EAcademySave::Restored;
            CurrentScreen = EAcademyScreen::Candidate;
            return;
        }

        if (IsAcademySave(Completed))
        {
            if (Code == TREK_HOST_OK)
            {
                Saved = EAcademySave::Confirmed;
                if (Completed == EAcademyOperation::SaveAndClose) Pending = EAcademyOperation::Close;
            }
            else
            {
                Saved = Code == TREK_HOST_PUBLICATION_UNCERTAIN || bSaveOutcomeUnknown
                    ? EAcademySave::Uncertain : EAcademySave::Failed;
            }
            CurrentScreen = EAcademyScreen::Candidate;
            return;
        }

        if (Code != TREK_HOST_OK) return;

        switch (Completed)
        {
        case EAcademyOperation::Create:
            Pending = EAcademyOperation::VerifyNew;
            break;
        case EAcademyOperation::Restore:
            Pending = EAcademyOperation::VerifyRestore;
            break;
        case EAcademyOperation::Close:
        case EAcademyOperation::ExitClose:
        case EAcademyOperation::ResetCreate:
            ResetSession(Completed == EAcademyOperation::ResetCreate ? EAcademyScreen::Name : EAcademyScreen::Main);
            bExitRequested = Completed == EAcademyOperation::ExitClose;
            break;
        default:
            break;
        }
    }

    void VerifyWorld()
    {
        if (Begin(EAcademyOperation::VerifyWorld)) CurrentScreen = EAcademyScreen::Recovery;
    }

    bool CanRetryVerification() const { return CurrentScreen == EAcademyScreen::Recovery && !Busy() && Verification != EAcademyOperation::None; }
    void RetryVerification() { if (CanRetryVerification()) Begin(Verification); }

    void ShowUnverifiedSession()
    {
        CurrentScreen = EAcademyScreen::Recovery;
        Verification = EAcademyOperation::None;
    }

    void ResetSession(EAcademyScreen Screen = EAcademyScreen::Main)
    {
        CurrentScreen = Screen;
        Saved = EAcademySave::Unconfirmed;
        Verification = EAcademyOperation::VerifyWorld;
    }

    void ProgressChanged()
    {
        if (HasConfirmedProgress()) Saved = EAcademySave::Unconfirmed;
    }

private:
    EAcademyScreen CurrentScreen = EAcademyScreen::Main;
    EAcademyOperation Pending = EAcademyOperation::None;
    EAcademyOperation Last = EAcademyOperation::None;
    EAcademyOperation Verification = EAcademyOperation::VerifyWorld;
    EAcademySave Saved = EAcademySave::Unconfirmed;
    TrekHostCode LastError = TREK_HOST_OK;
    bool bExitRequested = false;
};

class FAcademyMenuCatalog
{
public:
    void Accept(uint32_t NextCursor, bool bHasAcademyRows)
    {
        Next = NextCursor;
        bSeenAcademy |= bHasAcademyRows;
        bLoaded = true;
    }

    uint32_t Cursor() const { return Next; }
    bool HasPage() const { return bLoaded; }
    bool IsEmpty() const { return bLoaded && !Next && !bSeenAcademy; }

    static bool CanRestore(uint32_t Kind, uint64_t Version, bool bCompatible, bool bRecoverable, TrekHostCode Reason)
    {
        return Kind == TREK_HOST_KIND_ACADEMY && Version && bCompatible && bRecoverable && Reason == TREK_HOST_OK;
    }

private:
    uint32_t Next = 0;
    bool bSeenAcademy = false;
    bool bLoaded = false;
};
