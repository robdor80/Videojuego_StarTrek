#include "HostWindowBounds.h"
#include "Engine/GameViewportClient.h"
#include "GenericPlatform/GenericWindow.h"
#include "Widgets/SWindow.h"
#include "Windows/WindowsHWrapper.h"

void FitHostAcademyWindow(UGameViewportClient& Viewport)
{
    const auto Window = Viewport.GetWindow();
    if (!Window || !Window->GetNativeWindow() || Window->GetWindowMode() != EWindowMode::Windowed) return;
    HWND Handle = static_cast<HWND>(Window->GetNativeWindow()->GetOSWindowHandle());
    if (!Handle || ::IsIconic(Handle) || ::IsZoomed(Handle)) return;
    RECT Client{}, Outer{};
    MONITORINFO Monitor{}; Monitor.cbSize = sizeof(Monitor);
    if (!::GetClientRect(Handle, &Client) || !::GetWindowRect(Handle, &Outer) ||
        !::GetMonitorInfoW(::MonitorFromWindow(Handle, MONITOR_DEFAULTTONEAREST), &Monitor)) return;
    const auto& Work = Monitor.rcWork;
    const int BorderX = (Outer.right - Outer.left) - Client.right;
    const int BorderY = (Outer.bottom - Outer.top) - Client.bottom;
    const int Width = FMath::Min<int>(Client.right, FMath::Max<int>(1, Work.right - Work.left - BorderX));
    const int Height = FMath::Min<int>(Client.bottom, FMath::Max<int>(1, Work.bottom - Work.top - BorderY));
    if (Width != Client.right || Height != Client.bottom)
    {
        Window->Resize(FVector2D(Width, Height));
        UE_LOG(LogTemp, Display, TEXT("H06 window fit: requested client=%ldx%ld effective=%dx%d work=%ldx%ld decorations=%dx%d DPI=%u"),
            Client.right, Client.bottom, Width, Height, Work.right-Work.left, Work.bottom-Work.top, BorderX, BorderY, ::GetDpiForWindow(Handle));
    }
    const int X = FMath::Clamp<int>(Outer.left, Work.left, Work.right - Width - BorderX);
    const int Y = FMath::Clamp<int>(Outer.top, Work.top, Work.bottom - Height - BorderY);
    if (X != Outer.left || Y != Outer.top)
    {
        // SWindow position denotes its client origin for a native title bar.
        const FVector2D Position = Window->GetPositionInScreen();
        Window->MoveWindowTo(Position + FVector2D(X - Outer.left, Y - Outer.top));
    }
}
