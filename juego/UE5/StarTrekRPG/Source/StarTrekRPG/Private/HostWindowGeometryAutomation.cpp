#if WITH_DEV_AUTOMATION_TESTS
#include "HostDiagnosticGameMode.h"
#include "HostAcademyMenu.h"
#include "HostSlateAutomation.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/GameViewportClient.h"
#include "Engine/World.h"
#include "Framework/Application/SlateApplication.h"
#include "GenericPlatform/GenericWindow.h"
#include "Widgets/SWindow.h"
#include "Misc/AutomationTest.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"
#include "UnrealClient.h"
#include "Windows/WindowsHWrapper.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHostWindowGeometry, "StarTrek.H06.AcademyMenu.Geometry",
    EAutomationTestFlags::ClientContext | EAutomationTestFlags::ProductFilter)

bool FHostWindowGeometry::RunTest(const FString&)
{
    struct FRun
    {
        FAutomationTestBase* Test;
        double Deadline = FPlatformTime::Seconds() + 90;
        double SampleAt = FPlatformTime::Seconds() + 4;
        int32 Step = 0;
        bool Tick()
        {
            if (FPlatformTime::Seconds() > Deadline) { Test->AddError(TEXT("Geometry timed out")); return true; }
            if (FPlatformTime::Seconds() < SampleAt) return false;
            UWorld* World = nullptr;
            for (const auto& Context : GEngine->GetWorldContexts())
                if (Context.World() && Context.World()->IsGameWorld() && Context.World()->HasBegunPlay()) World = Context.World();
            if (!World) return false;
            auto* Game = World->GetGameInstance();
            auto* Host = Game ? Game->GetSubsystem<UHostSessionSubsystem>() : nullptr;
            auto* Player = Game ? Cast<AHostDiagnosticPlayerController>(Game->GetFirstLocalPlayerController(World)) : nullptr;
            const auto Panel = Player ? Player->GetDiagnosticPanel() : TSharedPtr<SWidget>();
            const auto Window = Game ? Game->GetGameViewportClient()->GetWindow() : TSharedPtr<SWindow>();
            if (!Host || Host->IsInitializing() || !Panel || !Window || !Window->GetNativeWindow()) return false;
            const auto Menu = Host->GetAcademyMenu();
            if (Menu->IsBusy()) return false;
            HWND Handle = static_cast<HWND>(Window->GetNativeWindow()->GetOSWindowHandle());
            RECT Client{}, Outer{};
            ::GetClientRect(Handle, &Client); ::GetWindowRect(Handle, &Outer);
            POINT Origin{0,0}; ::ClientToScreen(Handle, &Origin);
            MONITORINFO Info{}; Info.cbSize = sizeof(Info);
            ::GetMonitorInfoW(::MonitorFromWindow(Handle, MONITOR_DEFAULTTONEAREST), &Info);
            const uint32 Dpi = ::GetDpiForWindow(Handle);
            const int Awareness = int(::GetAwarenessFromDpiAwarenessContext(::GetWindowDpiAwarenessContext(Handle)));
            const auto& Root = Panel->GetCachedGeometry();
            Test->AddInfo(FString::Printf(TEXT("GEOMETRY step=%d monitor=(%ld,%ld,%ld,%ld) work=(%ld,%ld,%ld,%ld) outer=(%ld,%ld,%ld,%ld) client=%ldx%ld origin=%ld,%ld DPI=%u awareness=%d SlateDPI=%.3f app=%.3f rootLocal=%s rootAbs=%s rootScale=%.3f viewport=%s"),
                Step, Info.rcMonitor.left,Info.rcMonitor.top,Info.rcMonitor.right,Info.rcMonitor.bottom,
                Info.rcWork.left,Info.rcWork.top,Info.rcWork.right,Info.rcWork.bottom,
                Outer.left,Outer.top,Outer.right,Outer.bottom,Client.right,Client.bottom,Origin.x,Origin.y,Dpi,Awareness,
                Window->GetDPIScaleFactor(), FSlateApplication::Get().GetApplicationScale(),
                *Root.GetLocalSize().ToString(), *Root.LocalToAbsolute(FVector2D::ZeroVector).ToString(), Root.Scale,
                *Game->GetGameViewportClient()->Viewport->GetSizeXY().ToString()));
            DEVMODEW Display{}; Display.dmSize=sizeof(Display);
            ::EnumDisplaySettingsW(nullptr, ENUM_CURRENT_SETTINGS, &Display);
            Test->AddInfo(FString::Printf(TEXT("PHYSICAL display=%lux%lu mode=%d"),Display.dmPelsWidth,Display.dmPelsHeight,int(Window->GetWindowMode())));
            Test->TestTrue(TEXT("DPI aware game process"), Awareness != DPI_AWARENESS_UNAWARE);
            if (Window->GetWindowMode() == EWindowMode::Windowed)
                Test->TestTrue(TEXT("Complete window inside work area"), Outer.left >= Info.rcWork.left && Outer.top >= Info.rcWork.top && Outer.right <= Info.rcWork.right && Outer.bottom <= Info.rcWork.bottom);
            for (const FName Tag : {FName(TEXT("AcademySurface")), FName(TEXT("AcademyNew")), FName(TEXT("AcademyBrowse")),
                FName(TEXT("AcademyExit")), FName(TEXT("AcademyBack")), FName(TEXT("AcademyReload"))})
            {
                const auto Widget = FindHostWidget(Panel.ToSharedRef(), Tag);
                if (!Widget) continue;
                const auto& Geometry = Widget->GetCachedGeometry();
                const FVector2D Top = Geometry.LocalToAbsolute(FVector2D::ZeroVector);
                const FVector2D Bottom = Geometry.LocalToAbsolute(Geometry.GetLocalSize());
                Test->AddInfo(FString::Printf(TEXT("WIDGET %s top=%s bottom=%s local=%s scale=%.3f"),
                    *Tag.ToString(), *Top.ToString(), *Bottom.ToString(), *Geometry.GetLocalSize().ToString(), Geometry.Scale));
                Test->TestTrue(*FString::Printf(TEXT("%s inside physical client"),*Tag.ToString()),
                    Top.X >= Origin.x - 2 && Top.Y >= Origin.y - 2 &&
                    Bottom.X <= Origin.x + Client.right + 2 && Bottom.Y <= Origin.y + Client.bottom + 2);
            }
            FScreenshotRequest::RequestScreenshot(FPaths::Combine(FPaths::ProjectSavedDir(), FString::Printf(TEXT("geometry-%d.png"),Step)), true, false);
            if (Step % 2 == 0)
            {
                Menu->OpenCatalog(); ++Step; SampleAt = FPlatformTime::Seconds()+2; return false;
            }
            if (FParse::Param(FCommandLine::Get(), TEXT("H06Transitions")) && Step < 5)
            {
                Menu->Back();
                // Engine command used by Alt+Enter, without requiring an unlocked desktop.
                Game->GetGameViewportClient()->HandleToggleFullscreenCommand();
                ++Step; SampleAt = FPlatformTime::Seconds()+4; return false;
            }
            return true;
        }
    };
    const auto Run = MakeShared<FRun>(); Run->Test = this;
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([Run]() { return Run->Tick(); }));
    return true;
}
#endif
