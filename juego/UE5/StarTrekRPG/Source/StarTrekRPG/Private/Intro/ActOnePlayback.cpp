#include "IntroCinematicPlayer.h"
#include "ActOnePresentation.h"
#include "ActOneTimeline.h"

#include "Components/AudioComponent.h"
#include "HAL/PlatformTime.h"
#include "Misc/CommandLine.h"
#include "Misc/PackageName.h"
#include "Misc/Parse.h"
#include "Sound/SoundWave.h"
#include "Sound/SoundClass.h"
#include "UnrealClient.h"
#include "Widgets/SOverlay.h"

DEFINE_LOG_CATEGORY_STATIC(LogActOne, Log, All);

void AIntroCinematicPlayer::PrepareActOne(SOverlay& Overlay)
{
    if (!FPackageName::DoesPackageExist(UActOneTimeline::PackagePath))
    {
        UE_LOG(LogActOne, Display, TEXT("Act I content is unavailable. Intro will finish normally."));
        return;
    }
    ActOne = LoadObject<UActOneTimeline>(nullptr, UActOneTimeline::AssetPath);
    FString Error;
    if (!ActOne || !ActOne->Validate(Error))
    {
        UE_LOG(LogActOne, Error, TEXT("Act I timeline could not be loaded: %s"), *Error);
        ActOne = nullptr;
        return;
    }

    ActOneView = MakeShared<FActOnePresentation>(*ActOne);
    Overlay.AddSlot()[ActOneView->Widget.ToSharedRef()];
    ActOneLondon->SetSound(ActOne->London);
    ActOneAmbience->SetSound(ActOne->CouncilAmbience);
    ActOneAmbience->SoundClassOverride = ActOne->CouncilAmbience->SoundClassObject;
    ActOneVoice->SoundClassOverride = ActOne->VoiceClass;

    if (FParse::Param(FCommandLine::Get(), TEXT("ActOneTrace")))
    {
        using T = UActOneTimeline;
        ActOneTraceTimes.Append({0.0, T::LocationStart, T::ExteriorStart, T::CouncilStart, T::LondonStart,
            T::CouncilAmbienceStart + T::CouncilAmbienceFade, 108.0, 131.0, 133.0, 138.0, 141.0, T::LondonEnd, 153.0});
        for (const FActOneIntervention& Line : ActOne->Interventions)
        {
            for (const FActOneShot& Shot : Line.Shots)
            {
                ActOneTraceTimes.Add(Shot.Start);
            }
            for (const FActOneMarker& Marker : Line.Markers)
            {
                ActOneTraceTimes.AddUnique(Marker.Time);
            }
        }
        ActOneTraceTimes.Append({UActOneTimeline::FinalFadeStart, UActOneTimeline::End});
        ActOneTraceTimes.Sort();
        FParse::Value(FCommandLine::Get(), TEXT("ActOneCaptureDir="), ActOneCaptureDirectory);
        const auto TraceAudioStart = [this](UAudioComponent& Player, const TCHAR* Track)
        {
            Player.OnAudioPlaybackPercentNative.AddWeakLambda(this,
                [this, Track](const UAudioComponent*, const USoundWave* Wave, float Percent)
                {
                    if (!bActOneRunning || ActOneTracedWaves.Contains(Wave->GetFName()))
                    {
                        return;
                    }
                    ActOneTracedWaves.Add(Wave->GetFName());
                    UE_LOG(LogActOne, Display, TEXT("%s mixer first callback %s at %.6f s, offset %.6f s"),
                        Track, *Wave->GetName(), FPlatformTime::Seconds() - StartTime - IntroTimeline::End,
                        Percent * Wave->Duration);
                });
        };
        TraceAudioStart(*ActOneMusic, TEXT("Music"));
        TraceAudioStart(*ActOneLondon, TEXT("Music"));
        TraceAudioStart(*ActOneAmbience, TEXT("Ambience"));
    }
}

void AIntroCinematicPlayer::TickActOne(double Time)
{
    using T = UActOneTimeline;
    Time = FMath::Max(0.0, Time);
    ActOneView->Render(FMath::Min(Time, T::End));

    if (ActOne->bEnableCouncilAmbience && !bCouncilStarted && Time >= T::CouncilAmbienceStart && Time < T::End)
    {
        bCouncilStarted = true;
        ActOneAmbience->SetVolumeMultiplier(ActOne->AmbienceGain * T::CouncilEnvelope(Time));
        // Keep the approved loop phase after the delayed entrance.
        constexpr double CouncilLoopOrigin = 5.0;
        const double Offset = FMath::Fmod(Time - CouncilLoopOrigin, ActOne->CouncilAmbience->Duration);
        ActOneAmbience->Play(Offset);
        UE_LOG(LogActOne, Display, TEXT("Council ambience requested at %.6f s (offset %.6f s)"), Time, Offset);
    }

    const FActOneIntervention* Line = ActOne->FindIntervention(Time);
    if (ActOneVoiceLine != Line)
    {
        ActOneVoiceLine = Line;
        ActOneVoice->Stop();
        if (ActOne->bEnableVoices && Line && !Line->Voice.IsNull())
        {
            if (USoundWave* Voice = Line->Voice.LoadSynchronous())
            {
                ActOneVoice->SetSound(Voice);
                ActOneVoice->Play(Time - Line->Start);
            }
        }
    }
    const float DuckTarget = ActOneVoice->IsPlaying() ? ActOne->VoiceDuck : 1.0f;
    VoiceMusicGain = FMath::FInterpTo(VoiceMusicGain, DuckTarget, Time - PreviousActOneTime, 6.0f);
    PreviousActOneTime = Time;
    const float OdeEnvelope = FMath::Lerp(0.92f, 1.0f, T::Ramp(Time, 398.0, 54.0)) * T::EndOpacity(Time);

    if (!bOdeStarted && Time >= T::OdeStart && Time < T::End)
    {
        bOdeStarted = true;
        ActOneMusic->SetSound(ActOne->Ode);
        ActOneMusic->SetVolumeMultiplier((ActOne->OdeGain / T::OdePcmHeadroom) * OdeEnvelope * VoiceMusicGain);
        ActOneMusic->Play(Time - T::OdeStart);
        UE_LOG(LogActOne, Display, TEXT("Ode to Harrison requested at %.6f s (offset %.6f s)"), Time, Time - T::OdeStart);
    }
    else if (bOdeStarted)
    {
        ActOneMusic->SetVolumeMultiplier((ActOne->OdeGain / T::OdePcmHeadroom) * OdeEnvelope * VoiceMusicGain);
    }
    if (Time >= T::LondonStart && Time < T::LondonEnd)
    {
        ActOneLondon->SetVolumeMultiplier(ActOne->LondonGain * ActOne->LondonEnvelope(Time) * VoiceMusicGain);
        if (!bLondonStarted)
        {
            bLondonStarted = true;
            ActOneLondon->Play(Time - T::LondonStart);
            UE_LOG(LogActOne, Display, TEXT("London Calling requested at %.6f s (offset %.6f s)"), Time, Time - T::LondonStart);
        }
    }
    else if (bLondonStarted)
    {
        bLondonStarted = false;
        ActOneLondon->SetVolumeMultiplier(0.0f);
        ActOneLondon->Stop();
        UE_LOG(LogActOne, Display, TEXT("London Calling stopped at %.6f s"), Time);
    }
    ActOneAmbience->SetVolumeMultiplier(bCouncilStarted ? ActOne->AmbienceGain * T::CouncilEnvelope(Time) : 0.0f);

    while (ActOneTraceTimes.IsValidIndex(ActOneNextTrace) && Time >= ActOneTraceTimes[ActOneNextTrace])
    {
        const FActOneCue* Cue = Line ? Line->Cues.FindByPredicate(
            [Time](const FActOneCue& Candidate) { return Candidate.Contains(Time); }) : nullptr;
        UE_LOG(LogActOne, Display, TEXT("Target %.3f s, frame %.6f s, %s, text %s, Ode %.3f (playing %d), London %.3f (playing %d), ambience %.3f (playing %d)"),
            ActOneTraceTimes[ActOneNextTrace++], Time, Line ? *Line->Id : TEXT("-"),
            Cue ? *Cue->Text : TEXT("-"), bOdeStarted ? ActOneMusic->VolumeMultiplier : 0.0f, ActOneMusic->IsPlaying(),
            bLondonStarted ? ActOneLondon->VolumeMultiplier : 0.0f, ActOneLondon->IsPlaying(),
            ActOneAmbience->VolumeMultiplier, ActOneAmbience->IsPlaying());
    }
    if (!ActOneCaptureDirectory.IsEmpty())
    {
        static constexpr double Captures[] = {0.5, 2.95, 4.3, 7.1, 11.1, 13.5, 15.4, 18.4, 25.3, 31.9,
            38.2, 92.0, 130.0, 139.0, 448.0, 454.0, 473.0, T::End};
        if (ActOneNextCapture < UE_ARRAY_COUNT(Captures) && Time >= Captures[ActOneNextCapture])
        {
            const double At = Captures[ActOneNextCapture++];
            const FString Filename = ActOneCaptureDirectory / FString::Printf(TEXT("ActoI_%06.2fs.png"), At);
            FScreenshotRequest::RequestScreenshot(Filename, true, false, false, FIntRect(), true);
        }
    }

    if (Time >= T::End)
    {
        ActOneMusic->Stop();
        ActOneLondon->Stop();
        ActOneAmbience->Stop();
        ActOneVoice->Stop();
        bActOneRunning = false;
        SetActorTickEnabled(false);
        UE_LOG(LogActOne, Display, TEXT("Finished at %.6f s. Music playing: %d. Ambience playing: %d."),
            Time, ActOneMusic->IsPlaying(), ActOneAmbience->IsPlaying());
        if (ActOne->NextActPreroll)
        {
            ActOneAmbience->SetSound(ActOne->NextActPreroll);
            ActOneAmbience->SetVolumeMultiplier(ActOne->AmbienceGain);
            ActOneAmbience->Play();
        }
        OnActOneFinished.Broadcast();
    }
}
