#pragma once

#include "CoreMinimal.h"
#include "Curves/CurveFloat.h"
#include "Engine/DataAsset.h"
#include "ActOneTimeline.generated.h"

class UFont;
class USoundWave;
class USoundClass;
class UTexture2D;

UENUM()
enum class EActOneLayout : uint8
{
    Right, Left, Panorama
};

USTRUCT()
struct FActOneSpan
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, Category = "Act I")
    double Start = 0.0;

    UPROPERTY(EditAnywhere, Category = "Act I")
    double End = 0.0;

    bool Contains(double Time) const { return Time >= Start && Time < End; }
};

USTRUCT()
struct FActOneShot : public FActOneSpan
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, Category = "Act I")
    FString Id;

    UPROPERTY(EditAnywhere, Category = "Act I")
    FString File;

    UPROPERTY(EditAnywhere, Category = "Act I")
    int32 Width = 0;

    UPROPERTY(EditAnywhere, Category = "Act I")
    int32 Height = 0;

    UPROPERTY(EditAnywhere, Category = "Act I")
    TObjectPtr<UTexture2D> Image;
};

USTRUCT()
struct FActOneCue : public FActOneSpan
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, Category = "Act I", meta = (MultiLine = true))
    FString Text;
};

USTRUCT()
struct FActOneMarker
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, Category = "Act I")
    double Time = 0.0;

    UPROPERTY(EditAnywhere, Category = "Act I")
    FString Label;
};

USTRUCT()
struct FActOneIntervention : public FActOneSpan
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, Category = "Act I")
    FString Id;

    UPROPERTY(EditAnywhere, Category = "Act I")
    FString Speaker;

    UPROPERTY(EditAnywhere, Category = "Act I")
    EActOneLayout Layout = EActOneLayout::Right;

    UPROPERTY(EditAnywhere, Category = "Act I", meta = (MultiLine = true))
    FString Dialogue;

    UPROPERTY(EditAnywhere, Category = "Act I")
    TArray<FActOneShot> Shots;

    UPROPERTY(EditAnywhere, Category = "Act I")
    TArray<FActOneCue> Cues;

    UPROPERTY(EditAnywhere, Category = "Act I")
    TArray<FActOneSpan> Pauses;

    UPROPERTY(EditAnywhere, Category = "Act I")
    TArray<FActOneMarker> Markers;

    UPROPERTY(EditAnywhere, Category = "Act I")
    TSoftObjectPtr<USoundWave> Voice;
};

UCLASS()
class UActOneTimeline final : public UDataAsset
{
    GENERATED_BODY()

public:
    UActOneTimeline();

    static constexpr const TCHAR* PackagePath = TEXT("/Game/Cinematics/Act_One/DA_ActOneTimeline");
    static constexpr const TCHAR* AssetPath = TEXT("/Game/Cinematics/Act_One/DA_ActOneTimeline.DA_ActOneTimeline");
    static constexpr double Fade = 0.35;
    static constexpr double LocationStart = 5.0;
    static constexpr double ExteriorStart = 8.0;
    static constexpr double CouncilStart = 12.0;
    static constexpr double LondonStart = 15.0;
    static constexpr double CouncilAmbienceStart = 15.0;
    static constexpr double CouncilAmbienceFade = 2.0;
    static constexpr double FirstInterventionStart = 16.0;
    static constexpr double OdeStart = 130.0;
    static constexpr double LondonEnd = 145.0;
    static constexpr float OdePcmHeadroom = 0.8f;
    static constexpr double FinalFadeStart = 485.0;
    static constexpr double End = 490.0;

    UPROPERTY(EditAnywhere, Category = "Act I")
    TArray<FActOneShot> Opening;

    UPROPERTY(EditAnywhere, Category = "Act I")
    TArray<FActOneIntervention> Interventions;

    UPROPERTY(EditAnywhere, Category = "Audio")
    TObjectPtr<USoundWave> London;

    UPROPERTY(EditAnywhere, Category = "Audio")
    TObjectPtr<USoundWave> Ode;

    UPROPERTY(EditAnywhere, Category = "Audio")
    TObjectPtr<USoundWave> CouncilAmbience;

    UPROPERTY(EditAnywhere, Category = "Audio")
    TObjectPtr<USoundWave> NextActPreroll;

    UPROPERTY(EditAnywhere, Category = "Audio")
    TObjectPtr<USoundClass> VoiceClass;

    UPROPERTY(EditAnywhere, Category = "Audio")
    TObjectPtr<USoundClass> SfxClass;

    UPROPERTY(EditAnywhere, Category = "Typography")
    TObjectPtr<UFont> TitleFont;

    UPROPERTY(EditAnywhere, Category = "Typography")
    TObjectPtr<UFont> DialogueFont;

    UPROPERTY(EditAnywhere, Category = "Audio", meta = (ClampMin = "0", ClampMax = "1"))
    float LondonGain = 0.76f;

    // Curve time is measured in seconds from OdeStart.
    UPROPERTY(EditAnywhere, Category = "Audio")
    FRuntimeFloatCurve LondonFade;

    UPROPERTY(EditAnywhere, Category = "Audio", meta = (ClampMin = "0", ClampMax = "1"))
    float OdeGain = 0.27f;

    UPROPERTY(EditAnywhere, Category = "Audio", meta = (ClampMin = "0", ClampMax = "1"))
    float AmbienceGain = 0.85f;

    UPROPERTY(EditAnywhere, Category = "Audio")
    bool bEnableCouncilAmbience = false;

    UPROPERTY(EditAnywhere, Category = "Audio", meta = (ClampMin = "0", ClampMax = "1"))
    float VoiceDuck = 0.50f;

    UPROPERTY(EditAnywhere, Category = "Audio")
    bool bEnableVoices = false;

    bool Validate(FString& Error, bool bRequireAssets = true) const;
    const FActOneIntervention* FindIntervention(double Time) const;
    static float Ramp(double Time, double Begin, double Duration);
    static float EndOpacity(double Time);
    static float CouncilEnvelope(double Time);
    float LondonEnvelope(double Time) const;
};
