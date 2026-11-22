#if WITH_DEV_AUTOMATION_TESTS
#include "HostAcademyMenu.h"
#include "HostDiagnosticGameMode.h"
#include "HostSlateAutomation.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/GameViewportClient.h"
#include "Engine/World.h"
#include "Framework/Application/SlateApplication.h"
#include "Misc/AutomationTest.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "Widgets/SViewport.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHostAcademyNavigation, "StarTrek.H06.AcademyMenu.Navigation",
    EAutomationTestFlags::ClientContext | EAutomationTestFlags::ProductFilter)

bool FHostAcademyNavigation::RunTest(const FString&)
{
    struct FRun
    {
        FAutomationTestBase* Test;
        int32 Step = 0;
        double Deadline = FPlatformTime::Seconds() + 40;
        bool Tick()
        {
            if (FPlatformTime::Seconds() > Deadline) { Test->AddError(TEXT("Navigation timed out")); return true; }
            UWorld* World = nullptr;
            for (const auto& Context : GEngine->GetWorldContexts())
                if (Context.World() && Context.World()->IsGameWorld() && Context.World()->HasBegunPlay()) World = Context.World();
            if (!World) return false;
            auto* Game = World->GetGameInstance();
            auto* Host = Game ? Game->GetSubsystem<UHostSessionSubsystem>() : nullptr;
            auto* Player = Game ? Cast<AHostDiagnosticPlayerController>(Game->GetFirstLocalPlayerController(World)) : nullptr;
            const auto Panel = Player ? Player->GetDiagnosticPanel() : TSharedPtr<SWidget>();
            if (!Host || Host->IsInitializing() || !Panel) return false;
            const auto Menu = Host->GetAcademyMenu();
            if (Menu->IsBusy()) return false;
            auto Click = [&](FName Tag)
            {
                Panel->SlatePrepass(1.0f);
                const auto Button = StaticCastSharedPtr<SButton>(FindHostWidget(Panel.ToSharedRef(), Tag));
                if (!Button || !Button->IsEnabled()) return false;
                Button->SimulateClick(); return true;
            };
            auto Escape = [&](TSharedPtr<SWidget> Focus)
            {
                FSlateApplication::Get().SetKeyboardFocus(Focus, EFocusCause::SetDirectly);
                const FKeyEvent Key(EKeys::Escape, FModifierKeysState(), 0, false, 0, 0);
                FSlateApplication::Get().ProcessKeyDownEvent(Key);
                FSlateApplication::Get().ProcessKeyUpEvent(Key);
            };
            // Each assertion runs on a later frame, after the event's presentation update.
            if (Step % 2 == 0)
            {
                if (Menu->GetFlow().Screen() != EAcademyScreen::Main)
                { Test->AddError(FString::Printf(TEXT("Escape failed after focus case %d"), Step / 2)); return true; }
                if (Step == 12)
                {
                    Test->TestEqual(TEXT("Escape on main leaves HOST closed"), Host->GetStatus().state, uint32(TREK_HOST_CLOSED));
                    Test->TestFalse(TEXT("Escape on main does not exit"), Menu->ShouldExit());
                    return true;
                }
                if (Step == 10) Escape(Game->GetGameViewportClient()->GetGameViewportWidget());
                else
                {
                    if (!Click(Step == 8 ? TEXT("AcademyBrowse") : TEXT("AcademyNew"))) return false;
                    if (Step == 8)
                    {
                        Test->TestTrue(TEXT("Catalog request is pending"), Menu->IsBusy());
                        Escape(Game->GetGameViewportClient()->GetGameViewportWidget());
                        Test->TestTrue(TEXT("Escape respects pending HOST operation"), Menu->GetFlow().Screen() == EAcademyScreen::Catalog);
                    }
                }
                ++Step; return false;
            }
            if (Step == 11) { ++Step; return false; }
            const auto Expected = Step == 9 ? EAcademyScreen::Catalog : EAcademyScreen::Name;
            if (Menu->GetFlow().Screen() != Expected) return false;
            const auto Field = StaticCastSharedPtr<SEditableTextBox>(FindHostWidget(Panel.ToSharedRef(), TEXT("AcademyName")));
            if (Step == 1) Escape(Field);
            else if (Step == 5)
            {
                if (!Field) return false;
                Field->SetText(FText::FromString(TEXT("María Vega")));
                Escape(Game->GetGameViewportClient()->GetGameViewportWidget());
            }
            else if (Step == 7) Escape(FindHostWidget(Panel.ToSharedRef(), TEXT("AcademyBack")));
            else Escape(Game->GetGameViewportClient()->GetGameViewportWidget());
            ++Step; return false;
        }
    };
    const auto Run = MakeShared<FRun>(); Run->Test = this;
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([Run]() { return Run->Tick(); }));
    return true;
}
#endif
