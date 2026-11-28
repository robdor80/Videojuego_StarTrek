#pragma once

#include "CoreMinimal.h"

namespace IntroTimeline
{
    inline constexpr int32 PairCount = 5;
    inline constexpr double ImageStart[] = {1.0, 5.5, 10.0, 14.5, 19.0, 23.5, 28.0, 32.5, 37.0, 43.0};
    inline constexpr int32 SceneCount = UE_ARRAY_COUNT(ImageStart);
    inline constexpr double EntranceFade = 2.0;
    inline constexpr double ExitFade = 1.0;
    inline constexpr double TributeStart = 47.0;
    inline constexpr double TributeFade = 1.0;
    inline constexpr double FinalFadeStart = 53.0;
    inline constexpr double End = 56.0;

    static_assert(SceneCount == PairCount * 2);

    inline constexpr double SceneEnd(int32 Scene)
    {
        return Scene + 1 < SceneCount ? ImageStart[Scene + 1] : End;
    }

    inline constexpr double SceneExitStart(int32 Scene)
    {
        return Scene + 1 < SceneCount ? SceneEnd(Scene) - ExitFade : FinalFadeStart;
    }

    inline float FadeIn(double Time, double Start, double Duration)
    {
        const float Progress = static_cast<float>(FMath::Clamp((Time - Start) / Duration, 0.0, 1.0));
        return FMath::SmoothStep(0.0f, 1.0f, Progress);
    }

    inline float FinalOpacity(double Time)
    {
        return 1.0f - FadeIn(Time, FinalFadeStart, End - FinalFadeStart);
    }

    inline float SceneOpacity(int32 Scene, double Time)
    {
        const double ExitStart = SceneExitStart(Scene);
        return FadeIn(Time, ImageStart[Scene], EntranceFade) *
            (1.0f - FadeIn(Time, ExitStart, SceneEnd(Scene) - ExitStart));
    }

    inline float TributeOpacity(double Time)
    {
        return FadeIn(Time, TributeStart, TributeFade) * FinalOpacity(Time);
    }
}
