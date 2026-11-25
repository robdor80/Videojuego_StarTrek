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
        TestEqual(Label + TEXT(" data starts one second later"), SceneOpacity(Scene, Start + 1.0).Data, 0.0f);
        TestEqual(Label + TEXT(" data halfway after 1.5 seconds"), SceneOpacity(Scene, Start + 1.5).Data, 0.5f);
        TestEqual(Label + TEXT(" full image after two seconds"), SceneOpacity(Scene, Start + 2.0).Image, 1.0f);
        TestEqual(Label + TEXT(" full data after two seconds"), SceneOpacity(Scene, Start + 2.0).Data, 1.0f);

        const double Out = Scene + 1 < SceneCount ? ExpectedStarts[Scene + 1] : 53.0;
        const double OutDuration = Scene + 1 < SceneCount ? 2.0 : 1.0;
        TestEqual(Label + TEXT(" remains visible until transition"), SceneOpacity(Scene, Out).Image, 1.0f);
        TestEqual(Label + TEXT(" outgoing image halfway"), SceneOpacity(Scene, Out + OutDuration / 2.0).Image, 0.5f);
        TestEqual(Label + TEXT(" outgoing data halfway"), SceneOpacity(Scene, Out + OutDuration / 2.0).Data, 0.5f);
        TestEqual(Label + TEXT(" outgoing image disappears"), SceneOpacity(Scene, Out + OutDuration).Image, 0.0f);
        TestEqual(Label + TEXT(" outgoing data disappears"), SceneOpacity(Scene, Out + OutDuration).Data, 0.0f);
        TestEqual(Label + TEXT(" stays hidden at the end"), SceneOpacity(Scene, 54.0).Image, 0.0f);
    }

    TestEqual(TEXT("Tribute starts at 47 s"), TributeOpacity(47.0), 0.0f);
    TestEqual(TEXT("Tribute halfway at 47.5 s"), TributeOpacity(47.5), 0.5f);
    TestEqual(TEXT("Tribute visible at 48 s"), TributeOpacity(48.0), 1.0f);
    TestEqual(TEXT("Picard remains visible with the tribute"), SceneOpacity(SceneCount - 1, 48.0).Data, 1.0f);
    TestEqual(TEXT("Tribute remains visible at 53 s"), TributeOpacity(53.0), 1.0f);
    TestEqual(TEXT("Tribute fades out at 53.5 s"), TributeOpacity(53.5), 0.5f);
    TestEqual(TEXT("Tribute invisible at 54 s"), TributeOpacity(54.0), 0.0f);
    TestEqual(TEXT("End at 54 s"), End, 54.0);
    return true;
}
#endif
