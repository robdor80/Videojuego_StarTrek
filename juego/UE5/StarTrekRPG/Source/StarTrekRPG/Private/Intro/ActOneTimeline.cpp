#include "ActOneTimeline.h"

#include "Engine/Texture2D.h"
#include "Sound/SoundWave.h"

UActOneTimeline::UActOneTimeline()
{
    FRichCurve& Curve = LondonFade.EditorCurveData;
    const FVector2f Points[] = {{0, 1}, {3, 0.90f}, {5, 0.75f}, {8, 0.50f},
        {10, 0.30f}, {13, 0.10f}, {static_cast<float>(LondonEnd - OdeStart), 0}};
    for (const FVector2f& Point : Points)
    {
        const FKeyHandle Key = Curve.AddKey(Point.X, Point.Y);
        Curve.SetKeyInterpMode(Key, RCIM_Cubic, false);
    }
    Curve.AutoSetTangents();
}

float UActOneTimeline::LondonEnvelope(double Time) const
{
    if (Time < LondonStart || Time >= LondonEnd)
    {
        return 0.0f;
    }
    if (Time <= OdeStart)
    {
        return 1.0f;
    }
    return FMath::Clamp(LondonFade.GetRichCurveConst()->Eval(static_cast<float>(Time - OdeStart)), 0.0f, 1.0f);
}

bool UActOneTimeline::Validate(FString& Error, bool bRequireAssets) const
{
    const auto Fail = [&Error](const FString& Message) { Error = Message; return false; };
    const auto ValidShot = [bRequireAssets](const FActOneShot& Shot)
    {
        return !Shot.Id.IsEmpty() && !Shot.File.IsEmpty() && Shot.Width > 0 && Shot.Height > 0 &&
            Shot.End > Shot.Start && (!bRequireAssets || (Shot.Image &&
            Shot.Image->GetImportedSize() == FIntPoint(Shot.Width, Shot.Height)));
    };

    if (Opening.Num() != 2 || Interventions.Num() != 22 ||
        Opening[0].Start != 3 || Opening[0].End != 7 || Opening[1].Start != 7 || Opening[1].End != 10 ||
        !ValidShot(Opening[0]) || !ValidShot(Opening[1]))
    {
        return Fail(TEXT("Invalid opening or intervention count"));
    }

    double Start = Opening.Last().End;
    TSet<FString> Files = { Opening[0].File, Opening[1].File };
    const double Starts[] = {10, 37, 60, 65, 69, 93, 116, 176, 182, 200, 226, 234,
        239, 267, 290, 301, 328, 347, 366, 391, 429, 451};
    for (int32 Index = 0; Index < Interventions.Num(); ++Index)
    {
        const FActOneIntervention& Line = Interventions[Index];
        const FString Id = FString::Printf(TEXT("V%d"), Index + 1);
        const bool bMemory = Index == 6;
        const EActOneLayout Expected = Index == 21 ? EActOneLayout::Panorama :
            (Index % 2 ? EActOneLayout::Left : EActOneLayout::Right);
        if (Line.Id != Id || Line.Start != Start || Line.Start != Starts[Index] ||
            Line.End <= Start || Line.Speaker.IsEmpty() || Line.Layout != Expected ||
            Line.Shots.Num() != (bMemory ? 4 : 1) || Line.Cues.IsEmpty())
        {
            return Fail(TEXT("Invalid intervention ") + Id);
        }

        double ShotStart = Start;
        const double MemoryStarts[] = {116, 130, 138, 147};
        for (int32 ShotIndex = 0; ShotIndex < Line.Shots.Num(); ++ShotIndex)
        {
            const FActOneShot& Shot = Line.Shots[ShotIndex];
            const FString ShotId = ShotIndex == 0 ? Id : Id + FString::Printf(TEXT(".%d"), ShotIndex);
            if (!ValidShot(Shot) || Shot.Id != ShotId || Shot.Start != ShotStart || Files.Contains(Shot.File) ||
                (bMemory && Shot.Start != MemoryStarts[ShotIndex]))
            {
                return Fail(TEXT("Invalid shot ") + ShotId);
            }
            Files.Add(Shot.File);
            ShotStart = Shot.End;
        }
        if (ShotStart != Line.End)
        {
            return Fail(TEXT("Shots do not cover ") + Id);
        }

        TArray<FString> Text;
        double PreviousEnd = Start;
        int32 Pause = 0;
        const auto CoversGap = [&Line, &Pause](double A, double B)
        {
            if (A == B)
            {
                return true;
            }
            if (!Line.Pauses.IsValidIndex(Pause))
            {
                return false;
            }
            const FActOneSpan& Span = Line.Pauses[Pause++];
            return Span.Start == A && Span.End == B;
        };
        for (const FActOneCue& Cue : Line.Cues)
        {
            if (Cue.Text.IsEmpty() || Cue.Start < PreviousEnd || Cue.End <= Cue.Start || Cue.End > Line.End ||
                !CoversGap(PreviousEnd, Cue.Start))
            {
                return Fail(TEXT("Invalid dialogue block in ") + Id);
            }
            Text.Add(Cue.Text);
            PreviousEnd = Cue.End;
        }
        if (!CoversGap(PreviousEnd, Line.End) || Pause != Line.Pauses.Num() ||
            FString::Join(Text, TEXT(" ")) != Line.Dialogue)
        {
            return Fail(TEXT("Invalid pauses or full dialogue in ") + Id);
        }
        for (const FActOneMarker& Marker : Line.Markers)
        {
            if (!Line.Contains(Marker.Time) || Marker.Label.IsEmpty())
            {
                return Fail(TEXT("Invalid marker in ") + Id);
            }
        }
        Start = Line.End;
    }
    const auto HasMarker = [this](int32 Index, double Time)
    {
        return Interventions[Index].Markers.ContainsByPredicate(
            [Time](const FActOneMarker& Marker) { return Marker.Time == Time; });
    };
    const auto CueAt = [this](int32 Index, double Time) -> const FActOneCue*
    {
        return Interventions[Index].Cues.FindByPredicate(
            [Time](const FActOneCue& Cue) { return Cue.Contains(Time); });
    };
    const FActOneCue* Vote = CueAt(20, 450.0);
    const FActOneCue* Climax = CueAt(21, 475.0);
    if (Start != FinalFadeStart || Files.Num() != 27 ||
        !HasMarker(6, OdeStart) || !HasMarker(19, 400) || !HasMarker(20, 430) ||
        !HasMarker(20, 450) || !HasMarker(21, 475) ||
        !Vote || Vote->Text != TEXT("Mi voto es favorable.") ||
        !Climax || !Climax->Text.StartsWith(TEXT("Y que sean sus acciones")))
    {
        return Fail(TEXT("Invalid master timeline or priority markers"));
    }
    if (bRequireAssets && (!London || London->GetDuration() < LondonEnd - LondonStart || !Ode ||
        Ode->GetDuration() < End - OdeStart || !CouncilAmbience || CouncilAmbience->Duration <= 0 ||
        !TitleFont || !DialogueFont || !VoiceClass || !SfxClass))
    {
        return Fail(TEXT("Missing fonts or incomplete audio"));
    }
    return true;
}

const FActOneIntervention* UActOneTimeline::FindIntervention(double Time) const
{
    return Interventions.FindByPredicate([Time](const FActOneIntervention& Line) { return Line.Contains(Time); });
}

float UActOneTimeline::Ramp(double Time, double Begin, double Duration)
{
    const float Alpha = static_cast<float>(FMath::Clamp((Time - Begin) / Duration, 0.0, 1.0));
    return FMath::SmoothStep(0.0f, 1.0f, Alpha);
}

float UActOneTimeline::EndOpacity(double Time)
{
    return 1.0f - Ramp(Time, FinalFadeStart, End - FinalFadeStart);
}

float UActOneTimeline::CouncilEnvelope(double Time)
{
    return Ramp(Time, 7.0, 1.35) * FMath::Lerp(1.0f, 0.22f,
        Ramp(Time, OdeStart, 1.1) * (1.0f - Ramp(Time, 147.0, 1.4))) * EndOpacity(Time);
}
