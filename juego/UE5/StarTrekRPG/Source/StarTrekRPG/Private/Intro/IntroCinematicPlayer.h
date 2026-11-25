#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "IntroTimeline.h"
#include "IntroCinematicPlayer.generated.h"

class SWidget;
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

    virtual void Tick(float DeltaSeconds) override;

private:
    friend class UIntroAssetSetupCommandlet;

    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type Reason) override;

    bool PreparePresentation();
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

    TSharedPtr<SWidget> Presentation;

    struct FSceneWidgets
    {
        UWidget* Image = nullptr;
        UWidget* Data[3] = {};
    };

    FSceneWidgets Scenes[IntroTimeline::SceneCount];
    UWidget* Tribute[2] = {};

    double StartTime = 0.0;
    TArray<double> TraceTimes;
    int32 NextTrace = 0;
};
