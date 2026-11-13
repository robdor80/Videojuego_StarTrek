#if WITH_DEV_AUTOMATION_TESTS
#include "HostDiagnosticGameMode.h"
#include "HostRuntime.h"
#include "HostSessionSubsystem.h"
#include "DynamicRHI.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "HAL/FileManager.h"
#include "HAL/PlatformMemory.h"
#include "Misc/AutomationTest.h"
#include "Misc/CommandLine.h"
#include "Misc/Paths.h"
#include "Misc/Parse.h"
#include "UObject/Package.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SEditableTextBox.h"

namespace
{
constexpr auto Flags = EAutomationTestFlags::ClientContext | EAutomationTestFlags::ProductFilter;
const TCHAR* DiagnosticMap = TEXT("/Game/Diagnostics/HostDiagnostic");

TSharedPtr<SWidget> FindWidget(const TSharedRef<SWidget>& Root, FName Tag)
{
    if (Root->GetTag() == Tag) return Root;
    if (FChildren* Children = Root->GetChildren())
    {
        for (int32 Index = 0; Index < Children->Num(); ++Index)
        {
            if (TSharedPtr<SWidget> Found = FindWidget(Children->GetChildAt(Index), Tag))
            {
                return Found;
            }
        }
    }
    return nullptr;
}

struct FDiagnosticRun
{
    FAutomationTestBase& Test;
    TWeakObjectPtr<UGameInstance> Game;
    TWeakObjectPtr<UHostSessionSubsystem> Host;
    TWeakObjectPtr<UHostWorldProjection> OriginalProjection;
    TWeakObjectPtr<UWorld> OriginalWorld;
    TWeakObjectPtr<UWorld> SecondWorld;
    FString Campaign;
    TrekHostCampaignView SavedView{};
    uint64 Generation = 0;
    double Deadline = FPlatformTime::Seconds() + 40;
    double Started = FPlatformTime::Seconds();
    int32 Stage = 0;
    bool bFixture = false;
    bool bDone = false;

    explicit FDiagnosticRun(FAutomationTestBase& InTest) : Test(InTest) {}

    ~FDiagnosticRun()
    {
        DestroySecondWorld();
    }

    void DestroySecondWorld()
    {
        if (UWorld* Other = SecondWorld.Get())
        {
            Other->EndPlay(EEndPlayReason::LevelTransition);
            Other->DestroyWorld(false);
            GEngine->DestroyWorldContext(Other);
            SecondWorld.Reset();
        }
    }

    bool Click(UWorld& World, uint32 Op, const TCHAR* Slot = nullptr, const FString* Address = nullptr)
    {
        auto* Controller = Cast<AHostDiagnosticPlayerController>(Game->GetFirstLocalPlayerController(&World));
        if (!Controller) return Fail(TEXT("Missing diagnostic player controller"));
        const TSharedPtr<SWidget> Panel = Controller->GetDiagnosticPanel();
        if (!Panel) return Fail(TEXT("Missing actual viewport panel"));
        if (Slot)
        {
            auto Field = StaticCastSharedPtr<SEditableTextBox>(FindWidget(Panel.ToSharedRef(), TEXT("H06_Slot")));
            if (!Field) return Fail(TEXT("Missing slot widget"));
            Field->SetText(FText::FromString(Slot));
        }
        if (Address)
        {
            auto Field = StaticCastSharedPtr<SEditableTextBox>(FindWidget(Panel.ToSharedRef(), TEXT("H06_Campaign")));
            if (!Field) return Fail(TEXT("Missing campaign widget"));
            Field->SetText(FText::FromString(*Address));
        }
        auto Button = StaticCastSharedPtr<SButton>(FindWidget(Panel.ToSharedRef(), FName(*FString::Printf(TEXT("H06_%u"), Op))));
        if (!Button || !Button->IsEnabled()) return Fail(TEXT("Missing or disabled diagnostic button"));
        Button->SimulateClick();
        return true;
    }

    bool Fail(const TCHAR* Message)
    {
        Test.AddError(FString::Printf(TEXT("H06 stage %d: %s"), Stage, Message));
        bDone = true;
        return false;
    }

    bool Completion(UHostWorldProjection& Projection, uint32 Op, TrekHostCode Expected)
    {
        const auto& Result = Projection.GetCompletion();
        if (!Result.IsSet() || Result->operation != Op) return false;
        if (Result->code != Expected)
        {
            Test.AddError(FString::Printf(TEXT("Operation %u: expected %s, got %s"),
                                         Op, HostCodeName(Expected), HostCodeName(Result->code)));
            bDone = true;
            return false;
        }
        return true;
    }

    bool Tick()
    {
        if (bDone) return true;
        if (FPlatformTime::Seconds() > Deadline)
        {
            Fail(TEXT("Timed out waiting for world or HOST reply"));
            return true;
        }

        if (Stage == 0)
        {
            for (const FWorldContext& Context : GEngine->GetWorldContexts())
            {
                UWorld* World = Context.World();
                if (World && World->IsGameWorld() && World->HasBegunPlay() &&
                    World->GetPackage()->GetName() == DiagnosticMap)
                {
                    Game = World->GetGameInstance();
                    OriginalWorld = World;
                    OriginalProjection = World->GetSubsystem<UHostWorldProjection>();
                    break;
                }
            }
            if (!Game.IsValid()) return false;
            Host = Game->GetSubsystem<UHostSessionSubsystem>();
            if (!Host.IsValid() || !Host->IsAvailable() || !OriginalProjection.IsValid())
            {
                Fail(TEXT("HOST or world subsystem unavailable"));
                return true;
            }

            const auto ActualRhi = RHIGetInterfaceType();
            const bool bNull = FParse::Param(FCommandLine::Get(), TEXT("nullrhi"));
            if (ActualRhi != (bNull ? ERHIInterfaceType::Null : ERHIInterfaceType::D3D12))
            {
                Fail(TEXT("Unexpected active RHI"));
                return true;
            }

            FParse::Value(FCommandLine::Get(), TEXT("-H06FixtureCampaign="), Campaign);
            bFixture = !Campaign.IsEmpty();
            Test.AddInfo(FString::Printf(TEXT("RHI=%s, fixture=%d, map=%s"), GDynamicRHI->GetName(), bFixture, DiagnosticMap));
            if (Click(*OriginalWorld, TREK_HOST_OPEN)) ++Stage;
            return bDone;
        }

        UWorld* Current = Game.IsValid() ? Game->GetWorld() : nullptr;
        auto* Projection = Current ? Current->GetSubsystem<UHostWorldProjection>() : nullptr;
        if (!Current || !Projection || !Host.IsValid())
        {
            Fail(TEXT("Lost GameInstance or projection"));
            return true;
        }

        switch (Stage)
        {
        case 1:
            if (!Completion(*Projection, TREK_HOST_OPEN, TREK_HOST_OK)) break;
            Generation = Host->GetStatus().generation;
            Test.TestTrue(TEXT("Single active campaign and generation"), Generation != 0 && Host->GetStatus().state == TREK_HOST_ACTIVE);
            Test.TestEqual(TEXT("OPEN leaves principal unbound"), Host->GetStatus().principal, uint32(TREK_HOST_PRINCIPAL_UNBOUND));
            Test.TestEqual(TEXT("F11 unavailable"), Host->GetStatus().institutional, uint32(TREK_HOST_SERVICE_UNAVAILABLE));
            if (Click(*Current, TREK_HOST_QUERY_VIEW)) ++Stage;
            break;
        case 2:
            if (!Completion(*Projection, TREK_HOST_QUERY_VIEW, TREK_HOST_PRINCIPAL_UNBOUND)) break;
            Test.TestFalse(TEXT("Unbound UI exposes no campaign view"), Projection->GetCampaignView().IsSet());
            if (Click(*Current, TREK_HOST_SAVE, TEXT("principal"))) ++Stage;
            break;
        case 3:
            if (!Completion(*Projection, TREK_HOST_SAVE, TREK_HOST_PRINCIPAL_UNBOUND)) break;
            if (Click(*Current, TREK_HOST_RESTORE, TEXT("../principal"), &Host->GetCampaignAddress())) ++Stage;
            break;
        case 4:
            if (!Completion(*Projection, TREK_HOST_RESTORE, TREK_HOST_PATH_REJECTED)) break;
            Test.TestEqual(TEXT("Invalid restore preserves generation"), Host->GetStatus().generation, Generation);
            if (Click(*Current, TREK_HOST_CLOSE)) ++Stage;
            break;
        case 5:
            if (!Completion(*Projection, TREK_HOST_CLOSE, TREK_HOST_OK)) break;
            Test.TestEqual(TEXT("Close revokes generation"), Host->GetStatus().generation, uint64(0));
            if (bFixture)
            {
                if (Click(*Current, TREK_HOST_RESTORE, TEXT("alpha"), &Campaign)) ++Stage;
            }
            else
            {
                return true;
            }
            break;
        case 6:
            if (!Completion(*Projection, TREK_HOST_RESTORE, TREK_HOST_OK)) break;
            Test.TestTrue(TEXT("H04 restore renews the generation"), Host->GetStatus().generation > Generation);
            Test.TestEqual(TEXT("Only H04 restored fixture identity"), Host->GetStatus().principal, uint32(TREK_HOST_OK));
            Generation = Host->GetStatus().generation;
            if (Click(*Current, TREK_HOST_QUERY_VIEW)) ++Stage;
            break;
        case 7:
            if (!Completion(*Projection, TREK_HOST_QUERY_VIEW, TREK_HOST_OK)) break;
            if (!Projection->GetCampaignView().IsSet()) { Fail(TEXT("Missing authorized view")); break; }
            SavedView = Projection->GetCampaignView().GetValue();
            Test.TestTrue(TEXT("Fixture view matches H04"), SavedView.person == 3 && SavedView.ship == 1 && SavedView.tick == 28800);
            if (Click(*Current, TREK_HOST_SAVE, TEXT("unreal"))) ++Stage;
            break;
        case 8:
            if (!Completion(*Projection, TREK_HOST_SAVE, TREK_HOST_OK)) break;
            {
                const FString Marker = FPaths::Combine(FPaths::ProjectSavedDir(), TEXT("HostSlots/campaigns"),
                    Campaign, TEXT("slots/unreal/v1/COMMITTED"));
                Test.TestTrue(TEXT("SAVE success follows H04 COMMITTED"), IFileManager::Get().FileExists(*Marker));
                const auto Values = UWorld::InitializationValues().AllowAudioPlayback(false)
                    .CreatePhysicsScene(false).CreateNavigation(false).CreateAISystem(false).SetTransactional(false);
                UWorld* Other = UWorld::CreateWorld(EWorldType::Game, false, NAME_None, nullptr, true, ERHIFeatureLevel::Num, &Values);
                SecondWorld = Other;
                GEngine->CreateNewWorldContext(EWorldType::Game).SetCurrentWorld(Other);
                Other->SetGameInstance(Game.Get());
                auto* OtherProjection = Other->GetSubsystem<UHostWorldProjection>();
                if (!OtherProjection) { Fail(TEXT("Missing second UWorld projection")); break; }
                const FURL Url(nullptr, DiagnosticMap, TRAVEL_Absolute);
                Other->SetGameMode(Url);
                Other->InitializeActorsForPlay(Url);
                Other->BeginPlay();
                Test.TestTrue(TEXT("Two simultaneous UWorlds have distinct projections"), OtherProjection != Projection);
                Test.TestFalse(TEXT("Second world starts empty"), OtherProjection->GetCampaignView().IsSet());
                if (Host->Query(*OtherProjection) != TREK_HOST_OK) { Fail(TEXT("Second world query admission")); break; }
                ++Stage;
            }
            break;
        case 9:
            {
                auto* Other = SecondWorld->GetSubsystem<UHostWorldProjection>();
                if (!Completion(*Other, TREK_HOST_QUERY_VIEW, TREK_HOST_OK)) break;
                Test.TestTrue(TEXT("Two views share one native generation and identity"),
                              Other->GetCompletion()->generation == Generation &&
                              Other->GetCampaignView()->person == SavedView.person &&
                              Other->GetCampaignView()->revision == SavedView.revision);
                if (Host->Query(*Other) != TREK_HOST_OK) { Fail(TEXT("Late query admission")); break; }
                if (!Click(*Current, TREK_HOST_RESTORE, TEXT("unreal"), &Campaign)) break;
                Test.TestFalse(TEXT("Restore clears other world immediately"), Other->GetCampaignView().IsSet());
                ++Stage;
            }
            break;
        case 10:
            if (!Completion(*Projection, TREK_HOST_RESTORE, TREK_HOST_OK)) break;
            Test.TestTrue(TEXT("LOAD renews generation"), Host->GetStatus().generation > Generation);
            Test.TestFalse(TEXT("Old query cannot update other world after LOAD"),
                           SecondWorld->GetSubsystem<UHostWorldProjection>()->GetCompletion().IsSet());
            Generation = Host->GetStatus().generation;
            if (Click(*Current, TREK_HOST_QUERY_VIEW)) ++Stage;
            break;
        case 11:
            if (!Completion(*Projection, TREK_HOST_QUERY_VIEW, TREK_HOST_OK)) break;
            {
                const auto& View = Projection->GetCampaignView().GetValue();
                Test.TestTrue(TEXT("Recovery preserves view"), View.person == SavedView.person && View.ship == SavedView.ship &&
                              View.tick == SavedView.tick && View.revision == SavedView.revision);
                DestroySecondWorld();
                if (Host->Query(*Projection) != TREK_HOST_OK) { Fail(TEXT("Pre-travel query admission")); break; }
                FString Error;
                FWorldContext* Context = Game->GetWorldContext();
                const FURL Url(nullptr, DiagnosticMap, TRAVEL_Absolute);
                if (!Context || !GEngine->LoadMap(*Context, Url, nullptr, Error))
                {
                    Test.AddError(Error);
                    Fail(TEXT("Real LoadMap failed"));
                    break;
                }
                ++Stage;
            }
            break;
        case 12:
            Test.TestTrue(TEXT("Travel creates a fresh world and preserves the owner"),
                          Current != OriginalWorld.Get() && Host.Get() == Game->GetSubsystem<UHostSessionSubsystem>() &&
                          Host->GetStatus().generation == Generation);
            Test.TestTrue(TEXT("Travel invalidates old world UI and creates a clean projection"),
                          (!OriginalProjection.IsValid() || !OriginalProjection->GetCompletion().IsSet()) &&
                          !Projection->GetCompletion().IsSet());
            if (Click(*Current, TREK_HOST_QUERY_VIEW)) ++Stage;
            break;
        case 13:
            if (!Completion(*Projection, TREK_HOST_QUERY_VIEW, TREK_HOST_OK)) break;
            Test.TestTrue(TEXT("New world can query same identity"), Projection->GetCampaignView()->person == SavedView.person);
            if (Host->Query(*Projection) != TREK_HOST_OK) { Fail(TEXT("Pre-close query admission")); break; }
            if (Click(*Current, TREK_HOST_CLOSE)) ++Stage;
            break;
        case 14:
            if (!Completion(*Projection, TREK_HOST_CLOSE, TREK_HOST_OK)) break;
            Test.TestTrue(TEXT("Close invalidates the view and generation"), !Projection->GetCampaignView().IsSet() &&
                          Host->GetStatus().generation == 0);
            Test.AddInfo(FString::Printf(TEXT("H06 completed in %.2f s; process peak working set %.1f MiB"),
                FPlatformTime::Seconds() - Started,
                double(FPlatformMemory::GetStats().PeakUsedPhysical) / (1024 * 1024)));
            return true;
        }
        return bDone;
    }
};
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHostDiagnosticFlow, "StarTrek.H06.DiagnosticFlow", Flags)

bool FHostDiagnosticFlow::RunTest(const FString&)
{
    const auto Run = MakeShared<FDiagnosticRun>(*this);
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([Run]() { return Run->Tick(); }));
    return true;
}

#endif
