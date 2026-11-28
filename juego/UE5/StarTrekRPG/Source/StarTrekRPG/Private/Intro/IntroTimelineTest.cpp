#include "IntroTimeline.h"

#if WITH_DEV_AUTOMATION_TESTS
#include "Misc/AutomationTest.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FIntroTimelineTest, "StarTrekRPG.Intro.Timeline",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FIntroTimelineTest::RunTest(const FString& Parameters)
{
    using namespace IntroTimeline;
    const double ExpectedStarts[] = {1.0, 5.5, 10.0, 14.5, 19.0, 23.5, 28.0, 32.5, 37.0, 43.0};
    static_assert(UE_ARRAY_COUNT(ExpectedStarts) == SceneCount);

    for (int32 Scene = 0; Scene < SceneCount; ++Scene)
    {
        const double Start = ExpectedStarts[Scene];
        const FString Label = FString::Printf(TEXT("Scene %d"), Scene + 1);
        TestEqual(Label + TEXT(" starts at the approved time"), ImageStart[Scene], Start);
        TestEqual(Label + TEXT(" starts black"), SceneOpacity(Scene, Start).Image, 0.0f);
        TestEqual(Label + TEXT(" image halfway after one second"), SceneOpacity(Scene, Start + 1.0).Image, 0.5f);
        TestEqual(Label + TEXT(" data remains hidden until 0.200 s"), SceneOpacity(Scene, Start + 0.200).Data, 0.0f);
        TestTrue(Label + TEXT(" data starts just after 0.200 s"), SceneOpacity(Scene, Start + 0.201).Data > 0.0f);
        TestEqual(Label + TEXT(" data halfway after 0.700 s"), SceneOpacity(Scene, Start + 0.700).Data, 0.5f);
        TestEqual(Label + TEXT(" full data after 1.200 s"), SceneOpacity(Scene, Start + 1.200).Data, 1.0f);
        TestEqual(Label + TEXT(" full image after two seconds"), SceneOpacity(Scene, Start + 2.0).Image, 1.0f);

        const double Out = Scene + 1 < SceneCount ? ExpectedStarts[Scene + 1] : 53.0;
        const double OutDuration = Scene + 1 < SceneCount ? 2.0 : 3.0;
        TestEqual(Label + TEXT(" remains visible until transition"), SceneOpacity(Scene, Out).Image, 1.0f);
        TestEqual(Label + TEXT(" outgoing image halfway"), SceneOpacity(Scene, Out + OutDuration / 2.0).Image, 0.5f);
        TestEqual(Label + TEXT(" outgoing data halfway"), SceneOpacity(Scene, Out + OutDuration / 2.0).Data, 0.5f);
        TestEqual(Label + TEXT(" outgoing image disappears"), SceneOpacity(Scene, Out + OutDuration).Image, 0.0f);
        TestEqual(Label + TEXT(" outgoing data disappears"), SceneOpacity(Scene, Out + OutDuration).Data, 0.0f);
        TestEqual(Label + TEXT(" stays hidden at the end"), SceneOpacity(Scene, 56.0).Image, 0.0f);
    }

    TestEqual(TEXT("Tribute starts at 47 s"), TributeOpacity(47.0), 0.0f);
    TestEqual(TEXT("Tribute halfway at 47.5 s"), TributeOpacity(47.5), 0.5f);
    TestEqual(TEXT("Tribute visible at 48 s"), TributeOpacity(48.0), 1.0f);
    TestEqual(TEXT("Picard remains visible with the tribute"), SceneOpacity(SceneCount - 1, 48.0).Data, 1.0f);
    TestEqual(TEXT("Tribute remains visible at 53 s"), TributeOpacity(53.0), 1.0f);
    TestEqual(TEXT("Tribute fades out at 54.5 s"), TributeOpacity(54.5), 0.5f);
    TestEqual(TEXT("Tribute invisible at 56 s"), TributeOpacity(56.0), 0.0f);
    TestEqual(TEXT("End at 56 s"), End, 56.0);
    return true;
}
#endif
