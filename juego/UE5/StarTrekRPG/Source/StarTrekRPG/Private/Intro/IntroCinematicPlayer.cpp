#include "IntroCinematicPlayer.h"

#include "Blueprint/UserWidget.h"
#include "Components/AudioComponent.h"
#include "Components/Widget.h"
#include "Engine/GameViewportClient.h"
#include "HAL/PlatformTime.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Sound/SoundWave.h"
#include "Styling/CoreStyle.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/SOverlay.h"
#include "UnrealClient.h"

DEFINE_LOG_CATEGORY_STATIC(LogIntroCinematic, Log, All);

AIntroCinematicPlayer::AIntroCinematicPlayer()
{
    PrimaryActorTick.bCanEverTick = true;
    PrimaryActorTick.bStartWithTickEnabled = false;
    PrimaryActorTick.bTickEvenWhenPaused = true;

    MusicPlayer = CreateDefaultSubobject<UAudioComponent>(TEXT("IntroMusicPlayer"));
    SetRootComponent(MusicPlayer);
    MusicPlayer->bAutoActivate = false;
    MusicPlayer->bAllowSpatialization = false;
    MusicPlayer->bIsUISound = true;
}

void AIntroCinematicPlayer::BeginPlay()
{
    Super::BeginPlay();
    if (!GetWorld()->GetGameViewport() || !PreparePresentation())
    {
        return;
    }

    if (FParse::Param(FCommandLine::Get(), TEXT("IntroTrace")))
    {
        TraceTimes.Add(0.0);
        FParse::Value(FCommandLine::Get(), TEXT("IntroCaptureDir="), CaptureDirectory);
        MusicPlayer->OnAudioPlaybackPercentNative.AddWeakLambda(this,
            [this](const UAudioComponent*, const USoundWave*, float Percent)
            {
                if (!bAudioProgressTraced)
                {
                    bAudioProgressTraced = true;
                    UE_LOG(LogIntroCinematic, Display, TEXT("First mixer playback callback at %.6f s (%.6f through the wave)"),
                        FPlatformTime::Seconds() - StartTime, Percent);
                }
            });
        for (const double Start : IntroTimeline::ImageStart)
        {
            TraceTimes.Append({Start, Start + IntroTimeline::DataDelay, Start + IntroTimeline::SceneFade});
        }
        TraceTimes.Append({IntroTimeline::TributeStart,
            IntroTimeline::TributeStart + IntroTimeline::TributeFade,
            IntroTimeline::FinalFadeStart, IntroTimeline::End});
    }

    RenderAt(0.0);

    if (Music)
    {
        MusicPlayer->SetSound(Music);
    }
    SetActorTickEnabled(true);
}

void AIntroCinematicPlayer::StartPlayback()
{
    StartTime = FPlatformTime::Seconds();
    if (Music)
    {
        MusicPlayer->Play();
    }
    UE_LOG(LogIntroCinematic, Display, TEXT("Started. Music requested: %d"), Music != nullptr);
    TraceTimeline(0.0);
}

bool AIntroCinematicPlayer::PreparePresentation()
{
    static const FName Names[2][4] = {
        {TEXT("IMG_Nave"), TEXT("TXT_Matricula"), TEXT("IMG_LineaNave"), TEXT("TXT_NombreNave")},
        {TEXT("IMG_Capitan"), TEXT("TXT_RangoCapitan"), TEXT("IMG_LineaCapitan"), TEXT("TXT_NombreCapitan")}
    };
    if (PairWidgets.Num() != IntroTimeline::PairCount)
    {
        UE_LOG(LogIntroCinematic, Error, TEXT("Expected five intro widget classes, found %d"), PairWidgets.Num());
        return false;
    }

    const TSharedRef<SOverlay> Overlay = SNew(SOverlay)
        .Visibility(EVisibility::HitTestInvisible);
    Overlay->AddSlot()
    [
        SNew(SBorder)
        .BorderImage(FCoreStyle::Get().GetBrush("WhiteBrush"))
        .BorderBackgroundColor(FLinearColor::Black)
        .Padding(0)
    ];

    for (int32 Pair = 0; Pair < PairWidgets.Num(); ++Pair)
    {
        UUserWidget* Composition = PairWidgets[Pair] ? CreateWidget(GetWorld(), PairWidgets[Pair]) : nullptr;
        if (!Composition)
        {
            UE_LOG(LogIntroCinematic, Error, TEXT("Invalid widget in intro pair %d"), Pair + 1);
            return false;
        }
        Compositions.Add(Composition);

        for (int32 Member = 0; Member < 2; ++Member)
        {
            FSceneWidgets& Scene = Scenes[Pair * 2 + Member];
            Scene.Image = Composition->GetWidgetFromName(Names[Member][0]);
            for (int32 DataIndex = 0; DataIndex < 3; ++DataIndex)
            {
                Scene.Data[DataIndex] = Composition->GetWidgetFromName(Names[Member][DataIndex + 1]);
            }
            if (!Scene.Image || !Scene.Data[0] || !Scene.Data[1] || !Scene.Data[2])
            {
                UE_LOG(LogIntroCinematic, Error, TEXT("Missing a named intro element in %s"), *Composition->GetName());
                return false;
            }
        }

        if (UWidget* Background = Composition->GetWidgetFromName(TEXT("IMG_FondoNegro")))
        {
            Background->SetRenderOpacity(0.0f);
        }
        Overlay->AddSlot()
        [
            Composition->TakeWidget()
        ];
    }

    UUserWidget* Last = Compositions.Last();
    Tribute[0] = Last->GetWidgetFromName(TEXT("TXT_HomenajePatrickStewart"));
    Tribute[1] = Last->GetWidgetFromName(TEXT("TXT_FechasPatrickStewart"));
    if (!Tribute[0] || !Tribute[1])
    {
        UE_LOG(LogIntroCinematic, Error, TEXT("Missing a named tribute text in %s"), *Last->GetName());
        return false;
    }

    Presentation = Overlay;
    GetWorld()->GetGameViewport()->AddViewportWidgetContent(Overlay, 100);
    return true;
}

void AIntroCinematicPlayer::RenderAt(double Time)
{
    for (int32 SceneIndex = 0; SceneIndex < IntroTimeline::SceneCount; ++SceneIndex)
    {
        const IntroTimeline::FSceneOpacity Opacity = IntroTimeline::SceneOpacity(SceneIndex, Time);
        const FSceneWidgets& Scene = Scenes[SceneIndex];
        Scene.Image->SetRenderOpacity(Opacity.Image);
        for (UWidget* Data : Scene.Data)
        {
            Data->SetRenderOpacity(Opacity.Data);
        }
    }
    for (UWidget* Text : Tribute)
    {
        Text->SetRenderOpacity(IntroTimeline::TributeOpacity(Time));
    }
}

void AIntroCinematicPlayer::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);

    if (WarmupFramesRemaining > 0)
    {
        if (--WarmupFramesRemaining == 0)
        {
            StartPlayback();
        }
        return;
    }

    const double Elapsed = FPlatformTime::Seconds() - StartTime;
    RenderAt(FMath::Min(Elapsed, IntroTimeline::End));
    TraceTimeline(Elapsed);
    if (!CaptureDirectory.IsEmpty())
    {
        static constexpr double CaptureTimes[] = {
            0.2, 3.3, 5.95, 7.8, 12.3, 16.8, 21.3, 25.8, 30.3, 34.8, 39.3, 45.3, 48.3, 53.5, 54.0
        };
        if (NextCapture < UE_ARRAY_COUNT(CaptureTimes) && Elapsed >= CaptureTimes[NextCapture])
        {
            const FString Filename = CaptureDirectory / FString::Printf(TEXT("Intro_%05.2fs.png"), CaptureTimes[NextCapture++]);
            FScreenshotRequest::RequestScreenshot(Filename, true, false, false, FIntRect(), true);
        }
    }
    if (Elapsed >= IntroTimeline::End)
    {
        MusicPlayer->Stop();
        SetActorTickEnabled(false);
        UE_LOG(LogIntroCinematic, Display, TEXT("Finished at %.6f s. Music playing: %d"),
            Elapsed, MusicPlayer->IsPlaying());
        OnIntroFinished.Broadcast();
    }
}

void AIntroCinematicPlayer::TraceTimeline(double Time)
{
    while (TraceTimes.IsValidIndex(NextTrace) && Time >= TraceTimes[NextTrace])
    {
        FString Opacities;
        for (const FSceneWidgets& Scene : Scenes)
        {
            Opacities += FString::Printf(TEXT(" %.3f/%.3f"),
                Scene.Image->GetRenderOpacity(), Scene.Data[0]->GetRenderOpacity());
        }
        UE_LOG(LogIntroCinematic, Display,
            TEXT("Target %.3f s, frame %.6f s, image/data:%s, tribute %.3f, music playing %d"),
            TraceTimes[NextTrace++], Time, *Opacities, Tribute[0]->GetRenderOpacity(),
            MusicPlayer->IsPlaying());
    }
}

void AIntroCinematicPlayer::EndPlay(const EEndPlayReason::Type Reason)
{
    MusicPlayer->Stop();
    if (Presentation.IsValid())
    {
        if (UGameViewportClient* Viewport = GetWorld()->GetGameViewport())
        {
            Viewport->RemoveViewportWidgetContent(Presentation.ToSharedRef());
        }
        Presentation.Reset();
    }
    Super::EndPlay(Reason);
}
