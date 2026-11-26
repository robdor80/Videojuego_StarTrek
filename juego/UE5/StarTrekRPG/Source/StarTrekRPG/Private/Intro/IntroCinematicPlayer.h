#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "IntroTimeline.h"
#include "IntroCinematicPlayer.generated.h"

class SWidget;
class SOverlay;
class UActOneTimeline;
class FActOnePresentation;
struct FActOneIntervention;
class UAudioComponent;
class USoundWave;
class UUserWidget;
class UWidget;

DECLARE_DYNAMIC_MULTICAST_DELEGATE(FIntroFinished);

UCLASS(NotBlueprintable)
class AIntroCinematicPlayer final : public AActor
{
    GENERATED_BODY()

public:
    AIntroCinematicPlayer();

    UPROPERTY(BlueprintAssignable, Category = "Intro")
    FIntroFinished OnIntroFinished;

    UPROPERTY(BlueprintAssignable, Category = "Act I")
    FIntroFinished OnActOneFinished;

    virtual void Tick(float DeltaSeconds) override;

private:
    friend class UIntroAssetSetupCommandlet;

    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type Reason) override;

    bool PreparePresentation();
    void StartPlayback();
    void PrepareActOne(SOverlay& Overlay);
    void TickActOne(double Time);
    void RenderAt(double Time);
    void TraceTimeline(double Time);

    UPROPERTY(EditInstanceOnly, Category = "Intro", meta = (AllowPrivateAccess = "true"))
    TArray<TSubclassOf<UUserWidget>> PairWidgets;

    UPROPERTY(EditInstanceOnly, Category = "Intro", meta = (AllowPrivateAccess = "true"))
    TObjectPtr<USoundWave> Music;

    UPROPERTY(Transient)
    TObjectPtr<UAudioComponent> MusicPlayer;

    UPROPERTY(Transient)
    TArray<TObjectPtr<UUserWidget>> Compositions;

    UPROPERTY(Transient)
    TObjectPtr<UActOneTimeline> ActOne;

    UPROPERTY(Transient)
    TObjectPtr<UAudioComponent> ActOneMusic;

    UPROPERTY(Transient)
    TObjectPtr<UAudioComponent> ActOneLondon;

    UPROPERTY(Transient)
    TObjectPtr<UAudioComponent> ActOneAmbience;

    UPROPERTY(Transient)
    TObjectPtr<UAudioComponent> ActOneVoice;

    TSharedPtr<FActOnePresentation> ActOneView;
    const FActOneIntervention* ActOneVoiceLine = nullptr;
    bool bActOneRunning = false;
    bool bCouncilStarted = false;
    bool bLondonStarted = false;
    bool bOdeStarted = false;
    float VoiceMusicGain = 1.0f;
    double PreviousActOneTime = 0.0;
    TArray<double> ActOneTraceTimes;
    TSet<FName> ActOneTracedWaves;
    int32 ActOneNextTrace = 0;
    int32 ActOneNextCapture = 0;
    FString ActOneCaptureDirectory;

    TSharedPtr<SWidget> Presentation;

    struct FSceneWidgets
    {
        UWidget* Image = nullptr;
        UWidget* Data[3] = {};
    };

    FSceneWidgets Scenes[IntroTimeline::SceneCount];
    UWidget* Tribute[2] = {};

    // Present the black overlay before the playback clock; the first RHI frames may stall.
    int32 WarmupFramesRemaining = 3;
    double StartTime = 0.0;
    TArray<double> TraceTimes;
    int32 NextTrace = 0;
    bool bAudioProgressTraced = false;
    FString CaptureDirectory;
    int32 NextCapture = 0;
};
