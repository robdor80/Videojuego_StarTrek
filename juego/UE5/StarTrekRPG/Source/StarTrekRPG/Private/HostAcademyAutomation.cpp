#if WITH_DEV_AUTOMATION_TESTS
#include "HostSessionSubsystem.h"

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

namespace
{
constexpr auto Flags = EAutomationTestFlags::ClientContext | EAutomationTestFlags::ProductFilter;
const TCHAR* DiagnosticMap = TEXT("/Game/Diagnostics/HostDiagnostic");
const TCHAR* SlotName = TEXT("academy-c03");
const TCHAR* CandidateName = TEXT("María Vega");
constexpr uint64 Versions = TREK_HOST_ACADEMY_MAX_SLOTS + 2;

FString CandidateRecord(const FHostAcademyCandidate& Candidate)
{
    return FString::Printf(TEXT("%s|%s|%s|%llu|%llu|%llu|%llu"),
        *Candidate.Campaign, *Candidate.DisplayName, *Candidate.SourceDigest,
        Candidate.Person, Candidate.CreationFact, Candidate.Revision, Candidate.Tick);
}

struct FAcademyRun
{
    FAutomationTestBase& Test;
    TWeakObjectPtr<UGameInstance> Game;
    TWeakObjectPtr<UHostWorldProjection> Previous;
    FString Fixture;
    FString ExpectedCandidate;
    FHostAcademySlot FirstVersion;
    uint64 Generation = 0;
    uint64 Saved = 0;
    uint64 Found = 0;
    uint32 Cursor = 0;
    int32 Pages = 0;
    double Deadline = FPlatformTime::Seconds() + 120.0;
    bool bResume;
    bool bDone = false;

    enum class EStep
    {
        Start, Create, AfterTravel, Query, Candidate, Save, Saved, List, Page,
        Restore, Restored, BeforeClose, Close, Closed
    };
    EStep Step = EStep::Start;

    FAcademyRun(FAutomationTestBase& InTest, bool bInResume) : Test(InTest), bResume(bInResume) {}

    void Fail(const FString& Message)
    {
        Test.AddError(FString::Printf(TEXT("Academy step %d: %s"), static_cast<int32>(Step), *Message));
        bDone = true;
    }

    bool Admit(TrekHostCode Code, EStep Next)
    {
        if (Code == TREK_HOST_RETRY) return false;
        if (Code != TREK_HOST_OK)
        {
            Fail(FString::Printf(TEXT("submit returned %u"), Code));
            return false;
        }
        Step = Next;
        return true;
    }

    bool Completed(const TOptional<TrekHostCompletion>& Result, uint32 Operation)
    {
        if (!Result.IsSet() || Result->operation != Operation) return false;
        if (Result->code == TREK_HOST_OK && Result->ticket) return true;
        Fail(FString::Printf(TEXT("v1 operation %u returned %u"), Operation, Result->code));
        return false;
    }

    bool Completed(const TOptional<FHostAcademyResult>& Result, TrekHostCode Expected = TREK_HOST_OK)
    {
        if (!Result.IsSet()) return false;
        if (Result->Code == Expected && Result->Ticket) return true;
        Fail(FString::Printf(TEXT("Academy operation %u returned %u"), Result->Operation, Result->Code));
        return false;
    }

    bool Tick()
    {
        if (FPlatformTime::Seconds() > Deadline)
        {
            Fail(TEXT("timed out"));
            return true;
        }
        if (Step == EStep::Start)
        {
            FString UserDir;
            if (!FParse::Value(FCommandLine::Get(), TEXT("-UserDir="), UserDir) || UserDir.IsEmpty())
            {
                Fail(TEXT("requires an isolated -UserDir"));
                return true;
            }
            for (const FWorldContext& Context : GEngine->GetWorldContexts())
            {
                UWorld* World = Context.World();
                if (World && World->IsGameWorld() && World->HasBegunPlay() &&
                    World->GetPackage()->GetName() == DiagnosticMap)
                {
                    Game = World->GetGameInstance();
                    break;
                }
            }
            if (!Game.IsValid()) return false;
        }
        UWorld* World = Game.IsValid() ? Game->GetWorld() : nullptr;
        auto* Projection = World ? World->GetSubsystem<UHostWorldProjection>() : nullptr;
        auto* Host = Game.IsValid() ? Game->GetSubsystem<UHostSessionSubsystem>() : nullptr;
        if (!Host || !Projection)
        {
            Fail(TEXT("missing GameInstance or world projection"));
            return true;
        }
        if (Host->IsInitializing()) return false;
        if (Host->GetAcademyAvailability() != TREK_HOST_OK)
        {
            Fail(TEXT("Academy ABI v2 unavailable"));
            return true;
        }

        switch (Step)
        {
        case EStep::Start:
            if (RHIGetInterfaceType() != (FParse::Param(FCommandLine::Get(), TEXT("nullrhi"))
                                        ? ERHIInterfaceType::Null : ERHIInterfaceType::D3D12))
            {
                Fail(TEXT("unexpected RHI"));
                break;
            }
            Fixture = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("HostSlots/academy-c03-identity.txt"));
            if (bResume ? !FFileHelper::LoadFileToString(ExpectedCandidate, *Fixture) : FPaths::FileExists(Fixture))
            {
                Fail(TEXT("Seed needs fresh storage and Resume needs the Seed identity record"));
                break;
            }
            Step = bResume ? EStep::List : EStep::Create;
            break;
        case EStep::Create:
            if (Admit(Host->CreateAcademy(*Projection, CandidateName), EStep::AfterTravel))
            {
                Previous = Projection;
                const FURL Url(nullptr, DiagnosticMap, TRAVEL_Absolute);
                FWorldContext* Context = Game->GetWorldContext();
                FString Error;
                if (!Context || !GEngine->LoadMap(*Context, Url, nullptr, Error))
                {
                    Fail(FString::Printf(TEXT("LoadMap failed: %s"), *Error));
                }
            }
            break;
        case EStep::AfterTravel:
            if (Host->IsTransitioning()) break;
            if (Projection == Previous.Get() ||
                (Previous.IsValid() && Previous->GetAcademyResult(TREK_HOST_ACADEMY_CREATE).IsSet()) ||
                Projection->GetAcademyCandidate().IsSet() || Host->GetStatus().generation == 0)
            {
                Fail(TEXT("CREATE did not complete exclusively in GameInstance across LoadMap"));
                break;
            }
            Generation = Host->GetStatus().generation;
            Step = EStep::Query;
            break;
        case EStep::Query:
            Admit(Host->QueryAcademy(*Projection), EStep::Candidate);
            break;
        case EStep::Candidate:
            if (Completed(Projection->GetAcademyResult(TREK_HOST_ACADEMY_QUERY)))
            {
                const auto& Candidate = Projection->GetAcademyCandidate();
                if (!Candidate.IsSet() || Candidate->DisplayName != CandidateName ||
                    Candidate->Kind != TREK_HOST_KIND_ACADEMY || Candidate->CandidateState != TREK_HOST_CANDIDATE ||
                    Candidate->Generation != Generation || !Candidate->Person || !Candidate->CreationFact ||
                    Host->GetStatus().principal != TREK_HOST_OK ||
                    Host->GetStatus().institutional != TREK_HOST_SERVICE_UNAVAILABLE)
                {
                    Fail(TEXT("invalid bound candidate or authority projection"));
                    break;
                }
                if (bResume)
                {
                    if (CandidateRecord(*Candidate) != ExpectedCandidate)
                    {
                        Fail(TEXT("RESTORE changed campaign, PERSON, creation fact or Core checkpoint"));
                        break;
                    }
                    Step = EStep::BeforeClose;
                }
                else
                {
                    ExpectedCandidate = CandidateRecord(*Candidate);
                    Step = EStep::Save;
                }
            }
            break;
        case EStep::Save:
            Admit(Host->Save(*Projection, SlotName), EStep::Saved);
            break;
        case EStep::Saved:
            if (Completed(Projection->GetCompletion(), TREK_HOST_SAVE))
            {
                Step = ++Saved < Versions ? EStep::Save : EStep::BeforeClose;
            }
            break;
        case EStep::List:
            Admit(Host->ListAcademySlots(*Projection, Cursor), EStep::Page);
            break;
        case EStep::Page:
            if (Completed(Projection->GetAcademyResult(TREK_HOST_ACADEMY_SLOTS)))
            {
                const auto& Catalog = Projection->GetAcademyPage();
                if (!Catalog.IsSet() || Catalog->Generation != 0 || Catalog->Rows.Num() > TREK_HOST_ACADEMY_MAX_SLOTS ||
                    ++Pages > Versions)
                {
                    Fail(TEXT("invalid catalog page or nonterminating cursor"));
                    break;
                }
                for (const auto& Row : Catalog->Rows)
                {
                    if (Row.Slot != SlotName || Row.Kind != TREK_HOST_KIND_ACADEMY ||
                        !Row.bCompatible || !Row.bRecoverable || Row.Reason != TREK_HOST_OK ||
                        Found >= Versions || Row.Version != Versions - Found++)
                    {
                        Fail(TEXT("invalid catalog row or version order"));
                        break;
                    }
                    if (Row.Version == 1) FirstVersion = Row;
                }
                if (bDone) break;
                Cursor = Catalog->NextCursor;
                if (Catalog->HasMore())
                {
                    Step = EStep::List;
                }
                else if (Pages < 2 || Found != Versions || FirstVersion.Version != 1)
                {
                    Fail(TEXT("catalog did not include every historical version"));
                }
                else
                {
                    Step = EStep::Restore;
                }
            }
            break;
        case EStep::Restore:
            Admit(Host->RestoreAcademy(*Projection, FirstVersion), EStep::Restored);
            break;
        case EStep::Restored:
            if (Completed(Projection->GetCompletion(), TREK_HOST_RESTORE))
            {
                Generation = Host->GetStatus().generation;
                if (!Generation || Projection->GetAcademyPage().IsSet() ||
                    Host->ListAcademySlots(*Projection, 1) != TREK_HOST_GENERATION_EXPIRED)
                {
                    Fail(TEXT("RESTORE did not establish a new generation or revoke old cursors"));
                    break;
                }
                Step = EStep::Query;
            }
            break;
        case EStep::BeforeClose:
            if (!Admit(Host->QueryAcademy(*Projection), EStep::Close)) break;
            [[fallthrough]];
        case EStep::Close:
            Admit(Host->Close(*Projection), EStep::Closed);
            break;
        case EStep::Closed:
            if (Completed(Projection->GetCompletion(), TREK_HOST_CLOSE))
            {
                if (Host->GetStatus().generation || Projection->GetAcademyCandidate().IsSet() ||
                    Projection->GetAcademyResult(TREK_HOST_ACADEMY_QUERY).IsSet())
                {
                    Fail(TEXT("CLOSE did not invalidate the pending query and candidate"));
                }
                if (!bResume && !bDone && !FFileHelper::SaveStringToFile(ExpectedCandidate, *Fixture))
                {
                    Fail(TEXT("could not write the Seed identity record"));
                }
                return true;
            }
            break;
        }
        return bDone;
    }
};
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHostAcademySeed, "StarTrek.H06.Academy.Seed", Flags)
IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHostAcademyResume, "StarTrek.H06.Academy.Resume", Flags)

bool FHostAcademySeed::RunTest(const FString&)
{
    const auto Run = MakeShared<FAcademyRun>(*this, false);
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([Run]() { return Run->Tick(); }));
    return true;
}

bool FHostAcademyResume::RunTest(const FString&)
{
    const auto Run = MakeShared<FAcademyRun>(*this, true);
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([Run]() { return Run->Tick(); }));
    return true;
}
#endif
