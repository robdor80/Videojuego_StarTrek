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
        const double Finish = Scene + 1 < SceneCount ? ExpectedStarts[Scene + 1] : 56.0;
        const double Exit = Scene + 1 < SceneCount ? Finish - 1.0 : 53.0;
        const FString Label = FString::Printf(TEXT("Scene %d"), Scene + 1);
        TestEqual(Label + TEXT(" starts at the approved time"), ImageStart[Scene], Start);
        TestEqual(Label + TEXT(" starts black"), SceneOpacity(Scene, Start), 0.0f);
        TestTrue(Label + TEXT(" starts fading in immediately"), SceneOpacity(Scene, Start + 0.01) > 0.0f);
        TestEqual(Label + TEXT(" halfway in"), SceneOpacity(Scene, Start + 1.0), 0.5f);
        TestEqual(Label + TEXT(" fully visible"), SceneOpacity(Scene, Start + 2.0), 1.0f);
        TestEqual(Label + TEXT(" stays visible until its exit"), SceneOpacity(Scene, Exit), 1.0f);
        TestEqual(Label + TEXT(" halfway out"), SceneOpacity(Scene, (Exit + Finish) / 2.0), 0.5f);
        TestTrue(Label + TEXT(" stays visible until just before its boundary"), SceneOpacity(Scene, Finish - 0.01) > 0.0f);
        TestEqual(Label + TEXT(" fully dark at its boundary"), SceneOpacity(Scene, Finish), 0.0f);
        TestEqual(Label + TEXT(" stays dark after its boundary"), SceneOpacity(Scene, Finish + 0.01), 0.0f);
        if (Scene + 1 < SceneCount)
        {
            TestEqual(Label + TEXT(" the next scene stays dark throughout the exit"),
                SceneOpacity(Scene + 1, Finish - 0.01), 0.0f);
            TestEqual(Label + TEXT(" the next scene starts from black"),
                SceneOpacity(Scene + 1, Finish), 0.0f);
        }
    }

    for (int32 Step = 0; Step <= 5600; ++Step)
    {
        int32 VisibleScenes = 0;
        for (int32 Scene = 0; Scene < SceneCount; ++Scene)
        {
            VisibleScenes += SceneOpacity(Scene, Step / 100.0) > 0.0f ? 1 : 0;
        }
        if (VisibleScenes > 1)
        {
            AddError(FString::Printf(TEXT("Scenes overlap at %.2f s"), Step / 100.0));
            break;
        }
    }

    TestEqual(TEXT("Tribute starts at 47 s"), TributeOpacity(47.0), 0.0f);
    TestEqual(TEXT("Tribute halfway at 47.5 s"), TributeOpacity(47.5), 0.5f);
    TestEqual(TEXT("Tribute visible at 48 s"), TributeOpacity(48.0), 1.0f);
    TestEqual(TEXT("Picard remains visible with the tribute"), SceneOpacity(SceneCount - 1, 48.0), 1.0f);
    TestEqual(TEXT("Tribute remains visible at 53 s"), TributeOpacity(53.0), 1.0f);
    TestEqual(TEXT("Tribute fades out at 54.5 s"), TributeOpacity(54.5), 0.5f);
    TestEqual(TEXT("Tribute invisible at 56 s"), TributeOpacity(56.0), 0.0f);
    TestEqual(TEXT("End at 56 s"), End, 56.0);
    return true;
}
#endif
