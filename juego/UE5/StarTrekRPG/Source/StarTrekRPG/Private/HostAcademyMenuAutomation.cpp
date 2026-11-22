#if WITH_DEV_AUTOMATION_TESTS
#include "HostAcademyMenu.h"
#include "HostDiagnosticGameMode.h"
#include "HostSlateAutomation.h"

#include "DynamicRHI.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Misc/AutomationTest.h"
#include "Misc/CommandLine.h"
#include "Misc/FileHelper.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"
#include "UObject/Package.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "Widgets/Text/STextBlock.h"
#include "Widgets/Views/SListView.h"

namespace
{
constexpr auto MenuFlags = EAutomationTestFlags::ClientContext | EAutomationTestFlags::ProductFilter;
const TCHAR* AcademyMenuMap = TEXT("/Game/Diagnostics/HostDiagnostic");
const TCHAR* AcademyMenuName = TEXT("María Vega");
constexpr uint64 AcademyMenuVersions = TREK_HOST_ACADEMY_MAX_SLOTS + 2;

FString InvalidMenuName(int32 Index)
{
    if (Index == 0) return FString();
    if (Index == 1) return FString::ChrN(49, TEXT('é'));
    return TEXT(" María");
}

enum class EMenuScenario { Seed, Resume, SaveFailure, Unavailable };

FString MenuCandidateRecord(const FHostAcademyCandidate& Value)
{
    return FString::Printf(TEXT("%s|%s|%llu|%llu|%llu|%llu|%s"),
        *Value.Campaign, *Value.DisplayName, Value.Person, Value.CreationFact,
        Value.Revision, Value.Tick, *Value.SourceDigest);
}

struct FAcademyMenuRun
{
    using Op = EAcademyOperation;
    using Screen = EAcademyScreen;
    using Save = EAcademySave;

    EMenuScenario Scenario;
    FAutomationTestBase& Test;
    const double Deadline = FPlatformTime::Seconds() + 180.0;
    TWeakObjectPtr<UGameInstance> Game;
    TWeakObjectPtr<UHostWorldProjection> PreviousWorld;
    FString Fixture;
    FString Expected;
    TSet<uint64> VersionsSeen;
    TSet<uint64> RejectedVersions;
    uint64 Saves = 0;
    uint32 ExpiredCursor = 0;
    bool bSawEmptyPage = false;
    int32 InvalidNamesTested = 0;
    bool bDone = false;
    enum class EStep
    {
        Start, Name, InvalidName, Create, Query, FirstSave, Candidate,
        SaveVersion, CloseAfterSave, Closed, SaveFailed, CancelClose, ConfirmClose,
        Catalog, StaleCatalog, ConfirmRestore, Restored
    };
    EStep Step = EStep::Start;

    FAcademyMenuRun(EMenuScenario InScenario, FAutomationTestBase& InTest) : Scenario(InScenario), Test(InTest) {}

    bool Fail(const TCHAR* Message)
    {
        bDone = true;
        Test.AddError(FString::Printf(TEXT("Academy menu step %d: %s"), static_cast<int>(Step), Message));
        return false;
    }

    template <typename Widget>
    TSharedPtr<Widget> Find(const TSharedRef<SWidget>& Panel, FName Tag)
    {
        return StaticCastSharedPtr<Widget>(FindHostWidget(Panel, Tag));
    }

    bool Click(const TSharedRef<SWidget>& Panel, FName Tag, bool bDoubleClick = false)
    {
        const auto Button = Find<SButton>(Panel, Tag);
        if (!Button || !Button->IsEnabled()) return Fail(*FString::Printf(TEXT("Missing or disabled: %s"), *Tag.ToString()));
        Button->SimulateClick();
        if (bDoubleClick) Button->SimulateClick();
        return true;
    }

    bool EnterName(const TSharedRef<SWidget>& Panel, const FString& Value, bool bDoubleClick = false)
    {
        const auto Field = Find<SEditableTextBox>(Panel, TEXT("AcademyName"));
        if (!Field) return Fail(TEXT("Name field missing"));
        Field->SetText(FText::FromString(Value));
        return Click(Panel, TEXT("AcademyCreate"), bDoubleClick);
    }

    bool Travel(UHostWorldProjection& Projection)
    {
        PreviousWorld = &Projection;
        const FURL Url(nullptr, AcademyMenuMap, TRAVEL_Absolute);
        FWorldContext* Context = Game->GetWorldContext();
        FString Error;
        if (Context && GEngine->LoadMap(*Context, Url, nullptr, Error)) return true;
        return Fail(*FString::Printf(TEXT("Could not reload the Academy map: %s"), *Error));
    }

    bool CheckOldProjection(const UHostWorldProjection& Current)
    {
        if (auto* Old = PreviousWorld.Get(); Old &&
            (Old == &Current || Old->GetAcademyCandidate().IsSet() || Old->GetCompletion().IsSet() ||
             Old->GetAcademyResult(TREK_HOST_ACADEMY_CREATE).IsSet() || Old->GetAcademyResult(TREK_HOST_ACADEMY_QUERY).IsSet()))
        {
            return Fail(TEXT("A discarded UWorld retained an active projection or received a late result"));
        }
        return true;
    }

    bool CheckCandidate(const TSharedRef<SWidget>& Panel, const FHostAcademyMenu& Menu, const UHostSessionSubsystem& Host)
    {
        const auto& Value = Menu.GetCandidate();
        const auto Label = Find<STextBlock>(Panel, TEXT("AcademyCandidateState"));
        if (!Value.IsSet() || Value->DisplayName != AcademyMenuName ||
            Value->CandidateState != TREK_HOST_CANDIDATE || Value->Kind != TREK_HOST_KIND_ACADEMY ||
            Value->Generation != Host.GetStatus().generation || !Value->Generation || !Value->Person || !Value->CreationFact ||
            Host.GetStatus().principal != TREK_HOST_OK || Host.GetStatus().institutional != TREK_HOST_SERVICE_UNAVAILABLE ||
            !Label || !Label->GetText().ToString().Contains(TEXT("Candidato")))
        {
            return Fail(TEXT("The visible file is not the verified, bound candidate"));
        }
        return true;
    }

    void CatalogPage(const TSharedRef<SWidget>& Panel, FHostAcademyMenu& Menu,
                     UHostSessionSubsystem& Host, UHostWorldProjection& World)
    {
        const auto& Page = World.GetAcademyPage();
        if (!Page.IsSet() || Menu.IsCatalogEmpty())
        {
            Fail(TEXT("A valid Academy walk was reported empty"));
            return;
        }
        if (Page->HasMore() && !ExpiredCursor)
        {
            const uint32 Cursor = Page->NextCursor;
            const TrekHostCode Code = Host.Close(World); // Retire the live catalog as an external consumer.
            if (Code == TREK_HOST_RETRY) return;
            if (Code != TREK_HOST_OK)
            {
                Fail(TEXT("Could not retire the live catalog"));
                return;
            }
            ExpiredCursor = Cursor;
            Step = EStep::StaleCatalog;
            return;
        }

        using FSlotList = SListView<TSharedPtr<FHostAcademySlot>>;
        const auto List = Find<FSlotList>(Panel, TEXT("AcademyVersions"));
        if (!List)
        {
            Fail(TEXT("The real Slate version list is missing"));
            return;
        }
        bSawEmptyPage |= Menu.GetRows().IsEmpty() && Page->HasMore();
        TSharedPtr<FHostAcademySlot> First;
        for (const auto& Row : Menu.GetRows())
        {
            if (Row->Kind != TREK_HOST_KIND_ACADEMY || Row->Slot != TEXT("principal") ||
                !Expected.StartsWith(Row->Campaign + TEXT("|")) || VersionsSeen.Contains(Row->Version) ||
                Row->Version == 0 || Row->Version > AcademyMenuVersions)
            {
                Fail(TEXT("Unexpected Academy row, duplicate version or unfiltered naval row"));
                return;
            }
            VersionsSeen.Add(Row->Version);
            if (Row->Version == 1) First = Row;
            if (Row->Version == 2 || Row->Version == AcademyMenuVersions)
            {
                List->SetSelection(Row);
                const auto Button = Find<SButton>(Panel, TEXT("AcademyRestore"));
                if (Row->Reason != TREK_HOST_SAVE_CORRUPT || Menu.GetSelected() != Row ||
                    Menu.CanRestore() || !Button || Button->IsEnabled())
                {
                    Fail(TEXT("The damaged version must be visible and disabled for recovery"));
                    return;
                }
                RejectedVersions.Add(Row->Version);
            }
        }
        if (Page->HasMore())
        {
            Click(Panel, TEXT("AcademyMore"));
            return;
        }
        if (!bSawEmptyPage || RejectedVersions.Num() != 2 || VersionsSeen.Num() != static_cast<int32>(AcademyMenuVersions) || !First)
        {
            Fail(TEXT("Expected an empty continuation, all 66 versions and recoverable version 1"));
            return;
        }
        List->SetSelection(First);
        if (Click(Panel, TEXT("AcademyRestore"))) Step = EStep::ConfirmRestore;
    }

    bool Tick()
    {
        if (bDone) return true;
        if (FPlatformTime::Seconds() > Deadline)
        {
            Fail(TEXT("Timed out waiting for the Slate panel or HOST"));
            return true;
        }

        if (!Game.IsValid())
        {
            FString UserDir;
            if (!FParse::Value(FCommandLine::Get(), TEXT("-UserDir="), UserDir) || UserDir.IsEmpty() ||
                !FParse::Param(FCommandLine::Get(), TEXT("AcademyMenu")))
            {
                Fail(TEXT("Requires -AcademyMenu and an isolated -UserDir"));
                return true;
            }
            for (const FWorldContext& Context : GEngine->GetWorldContexts())
            {
                UWorld* World = Context.World();
                if (World && World->IsGameWorld() && World->HasBegunPlay() &&
                    World->GetOutermost()->GetName() == AcademyMenuMap)
                {
                    Game = World->GetGameInstance();
                    break;
                }
            }
            if (!Game.IsValid()) return false;
        }

        UWorld* World = Game->GetWorld();
        auto* Host = Game->GetSubsystem<UHostSessionSubsystem>();
        auto* Projection = World ? World->GetSubsystem<UHostWorldProjection>() : nullptr;
        auto* Player = World ? Cast<AHostDiagnosticPlayerController>(Game->GetFirstLocalPlayerController(World)) : nullptr;
        const auto Panel = Player ? Player->GetDiagnosticPanel() : TSharedPtr<SWidget>();
        if (!Host || !Projection || !Panel || Host->IsInitializing()) return false;
        const auto Menu = Host->GetAcademyMenu();
        const auto& Flow = Menu->GetFlow();

        switch (Step)
        {
        case EStep::Start:
            if (Scenario == EMenuScenario::Unavailable)
            {
                const auto New = Find<SButton>(Panel.ToSharedRef(), TEXT("AcademyNew"));
                const auto Continue = Find<SButton>(Panel.ToSharedRef(), TEXT("AcademyBrowse"));
                const auto Status = Find<STextBlock>(Panel.ToSharedRef(), TEXT("AcademyHost"));
                if (!New || !Continue || !Status || New->IsEnabled() || Continue->IsEnabled() ||
                    Host->GetAcademyAvailability() == TREK_HOST_OK || Host->GetStatus().state != TREK_HOST_CLOSED ||
                    !Status->GetText().ToString().Contains(TEXT("Academia no disponible")))
                {
                    Fail(TEXT("Unavailable Academy must show an error and never open a naval session"));
                }
                return true;
            }
            if (Host->GetAcademyAvailability() != TREK_HOST_OK ||
                RHIGetInterfaceType() != (FParse::Param(FCommandLine::Get(), TEXT("nullrhi")) ? ERHIInterfaceType::Null : ERHIInterfaceType::D3D12))
            {
                Fail(TEXT("Expected the real Academy v2 library and requested RHI"));
                break;
            }
            if (!Menu->IsReadyClosed()) break;
            Fixture = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("HostSlots/academy-c04-identity.txt"));
            if (Scenario == EMenuScenario::Resume)
            {
                if (!FFileHelper::LoadFileToString(Expected, *Fixture)) Fail(TEXT("Resume requires the identity captured by Seed"));
                else if (Click(Panel.ToSharedRef(), TEXT("AcademyBrowse"))) Step = EStep::Catalog;
            }
            else if (FPaths::FileExists(Fixture))
            {
                Fail(TEXT("Seed or SaveFailure requires fresh test storage"));
            }
            else if (Click(Panel.ToSharedRef(), TEXT("AcademyNew")))
            {
                Step = EStep::Name;
            }
            break;
        case EStep::Name:
            if (FindHostWidget(Panel.ToSharedRef(), TEXT("AcademyName")))
            {
                if (Scenario == EMenuScenario::Seed)
                {
                    const TCHAR InvalidUnit = static_cast<TCHAR>(0xd800);
                    if (Host->CreateAcademy(*Projection, FString(1, &InvalidUnit)) != TREK_HOST_INVALID_ARGUMENT)
                        Fail(TEXT("A lone UTF-16 surrogate must not be replaced before submitting CREATE"));
                    else if (EnterName(Panel.ToSharedRef(), InvalidMenuName(InvalidNamesTested)))
                        Step = EStep::InvalidName;
                }
                else if (Scenario == EMenuScenario::SaveFailure && EnterName(Panel.ToSharedRef(), AcademyMenuName))
                    Step = EStep::Candidate;
            }
            break;
        case EStep::InvalidName:
            if (!Flow.Busy())
            {
                if (Flow.Error() != TREK_HOST_INVALID_ARGUMENT || Host->GetStatus().generation ||
                    Projection->GetAcademyCandidate().IsSet() || Projection->GetCompletion().IsSet())
                {
                    Fail(TEXT("An invalid name passed validation or touched the session"));
                }
                else if (++InvalidNamesTested < 3)
                {
                    EnterName(Panel.ToSharedRef(), InvalidMenuName(InvalidNamesTested));
                }
                else if (EnterName(Panel.ToSharedRef(), AcademyMenuName, true)) Step = EStep::Create;
            }
            break;
        case EStep::Create:
            if (Flow.Operation() == Op::Create && Menu->GetPendingTicket() && Travel(*Projection)) Step = EStep::Query;
            break;
        case EStep::Query:
            if (Flow.Operation() == Op::VerifyNew && Menu->GetPendingTicket() && CheckOldProjection(*Projection) &&
                Travel(*Projection)) Step = EStep::FirstSave;
            break;
        case EStep::FirstSave:
            if (Flow.Operation() == Op::FirstSave && Menu->GetPendingTicket() && CheckOldProjection(*Projection))
            {
                if (Flow.HasConfirmedProgress() || FindHostWidget(Panel.ToSharedRef(), TEXT("AcademyCandidateState")))
                    Fail(TEXT("An admitted first SAVE was presented as complete"));
                else if (Travel(*Projection)) Step = EStep::Candidate;
            }
            break;
        case EStep::Candidate:
            if (Flow.Screen() == Screen::Candidate && !Flow.Busy() && Menu->GetCandidate().IsSet() &&
                FindHostWidget(Panel.ToSharedRef(), TEXT("AcademyCandidateState")) &&
                CheckOldProjection(*Projection) && CheckCandidate(Panel.ToSharedRef(), *Menu, *Host))
            {
                if (Scenario == EMenuScenario::SaveFailure)
                {
                    if (Flow.SaveState() != Save::Failed || Flow.HasConfirmedProgress())
                        Fail(TEXT("A real H04 storage error was shown as a successful first save"));
                    else if (Click(Panel.ToSharedRef(), TEXT("AcademySaveClose"))) Step = EStep::SaveFailed;
                }
                else if (Flow.SaveState() != Save::Confirmed)
                {
                    Fail(TEXT("The first SAVE lost its terminal result during world travel"));
                }
                else
                {
                    Expected = MenuCandidateRecord(*Menu->GetCandidate());
                    const FString Marker = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("HostSlots/campaigns"),
                        Menu->GetCandidate()->Campaign, TEXT("slots/principal/v1/COMMITTED"));
                    if (!FPaths::FileExists(Marker)) Fail(TEXT("There is no committed version 1 in principal"));
                    else if (Click(Panel.ToSharedRef(), TEXT("AcademySave"))) { Saves = 1; Step = EStep::SaveVersion; }
                }
            }
            break;
        case EStep::SaveVersion:
            if (!Flow.Busy())
            {
                if (Flow.SaveState() != Save::Confirmed || !Menu->GetCandidate().IsSet() ||
                    MenuCandidateRecord(*Menu->GetCandidate()) != Expected)
                {
                    Fail(TEXT("SAVE failed or changed the candidate"));
                }
                else if (++Saves < AcademyMenuVersions - 1) Click(Panel.ToSharedRef(), TEXT("AcademySave"));
                else if (Click(Panel.ToSharedRef(), TEXT("AcademySaveClose"))) Step = EStep::CloseAfterSave;
            }
            break;
        case EStep::CloseAfterSave:
            if (Flow.Operation() == Op::Close)
            {
                if (Flow.SaveState() != Save::Confirmed) Fail(TEXT("CLOSE started before the final SAVE confirmed"));
                else Step = EStep::Closed;
            }
            break;
        case EStep::SaveFailed:
            if (!Flow.Busy())
            {
                if (Flow.SaveState() != Save::Failed || Host->GetStatus().state != TREK_HOST_ACTIVE)
                    Fail(TEXT("A failed Save and Close must keep the candidate active"));
                else if (Click(Panel.ToSharedRef(), TEXT("AcademyClose"))) Step = EStep::CancelClose;
            }
            break;
        case EStep::CancelClose:
            if (FindHostWidget(Panel.ToSharedRef(), TEXT("AcademyCancel")) && Click(Panel.ToSharedRef(), TEXT("AcademyCancel")))
                Step = EStep::ConfirmClose;
            break;
        case EStep::ConfirmClose:
            if (FindHostWidget(Panel.ToSharedRef(), TEXT("AcademyConfirm")))
            {
                if (Click(Panel.ToSharedRef(), TEXT("AcademyConfirm"))) Step = EStep::Closed;
            }
            else if (Menu->GetConfirmation() == EAcademyConfirmation::None &&
                     FindHostWidget(Panel.ToSharedRef(), TEXT("AcademyClose")))
            {
                if (Host->GetStatus().state != TREK_HOST_ACTIVE) Fail(TEXT("Cancelling closed the session"));
                else Click(Panel.ToSharedRef(), TEXT("AcademyClose"));
            }
            break;
        case EStep::Closed:
            if (Flow.Screen() == Screen::Main && !Flow.Busy())
            {
                if (Host->GetStatus().state != TREK_HOST_CLOSED || Menu->GetCandidate().IsSet() || !Menu->CanExit())
                    Fail(TEXT("Closing did not leave the frontend and HOST in CLOSED"));
                if (Scenario == EMenuScenario::Seed && !bDone &&
                    !FFileHelper::SaveStringToFile(Expected, *Fixture, FFileHelper::EEncodingOptions::ForceUTF8WithoutBOM))
                    Fail(TEXT("Could not record the candidate for the second process"));
                return true;
            }
            break;
        case EStep::Catalog:
            if (!Flow.Busy()) CatalogPage(Panel.ToSharedRef(), *Menu, *Host, *Projection);
            break;
        case EStep::StaleCatalog:
            if (!Host->IsTransitioning() && Menu->IsCatalogExpired())
            {
                if (Menu->CanLoadMore() || Menu->CanRestore() || !Menu->GetRows().IsEmpty())
                    Fail(TEXT("A retired cursor left old selections usable"));
                else if (Click(Panel.ToSharedRef(), TEXT("AcademyReload"))) Step = EStep::Catalog;
            }
            break;
        case EStep::ConfirmRestore:
            if (FindHostWidget(Panel.ToSharedRef(), TEXT("AcademyConfirm")) &&
                Click(Panel.ToSharedRef(), TEXT("AcademyConfirm"))) Step = EStep::Restored;
            break;
        case EStep::Restored:
            if (Flow.Screen() == Screen::Candidate && !Flow.Busy() &&
                FindHostWidget(Panel.ToSharedRef(), TEXT("AcademyCandidateState")) &&
                CheckCandidate(Panel.ToSharedRef(), *Menu, *Host))
            {
                if (Flow.SaveState() != Save::Restored || MenuCandidateRecord(*Menu->GetCandidate()) != Expected)
                    Fail(TEXT("RESTORE and QUERY did not preserve the saved PERSON, campaign, fact and checkpoint"));
                else if (Click(Panel.ToSharedRef(), TEXT("AcademyClose"))) Step = EStep::Closed;
            }
            break;
        }
        return bDone;
    }
};
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHostAcademyMenuSeed, "StarTrek.H06.AcademyMenu.Seed", MenuFlags)
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHostAcademyMenuResume, "StarTrek.H06.AcademyMenu.Resume", MenuFlags)
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHostAcademyMenuSaveFailure, "StarTrek.H06.AcademyMenu.SaveFailure", MenuFlags)
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHostAcademyMenuUnavailable, "StarTrek.H06.AcademyMenu.Unavailable", MenuFlags)

bool FHostAcademyMenuSeed::RunTest(const FString&)
{
    const auto Run = MakeShared<FAcademyMenuRun>(EMenuScenario::Seed, *this);
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([Run]() { return Run->Tick(); }));
    return true;
}

bool FHostAcademyMenuResume::RunTest(const FString&)
{
    const auto Run = MakeShared<FAcademyMenuRun>(EMenuScenario::Resume, *this);
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([Run]() { return Run->Tick(); }));
    return true;
}

bool FHostAcademyMenuSaveFailure::RunTest(const FString&)
{
    const auto Run = MakeShared<FAcademyMenuRun>(EMenuScenario::SaveFailure, *this);
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([Run]() { return Run->Tick(); }));
    return true;
}

bool FHostAcademyMenuUnavailable::RunTest(const FString&)
{
    const auto Run = MakeShared<FAcademyMenuRun>(EMenuScenario::Unavailable, *this);
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([Run]() { return Run->Tick(); }));
    return true;
}
#endif
