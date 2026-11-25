#if WITH_EDITOR && WITH_DEV_AUTOMATION_TESTS
#include "IntroCinematicPlayer.h"

#include "Editor.h"
#include "EngineUtils.h"
#include "Misc/AutomationTest.h"
#include "Tests/AutomationCommon.h"
#include "Tests/AutomationEditorCommon.h"

DEFINE_LATENT_AUTOMATION_COMMAND_ONE_PARAMETER(FCheckIntroPIE, FAutomationTestBase*, Test);

bool FCheckIntroPIE::Update()
{
    if (!Test->TestNotNull(TEXT("PIE world"), GEditor->PlayWorld.Get()))
    {
        return true;
    }
    int32 Players = 0;
    for (TActorIterator<AIntroCinematicPlayer> It(GEditor->PlayWorld); It; ++It)
    {
        ++Players;
        Test->TestTrue(TEXT("Player started in PIE"), It->IsActorTickEnabled());
    }
    Test->TestEqual(TEXT("Exactly one active intro player in PIE"), Players, 1);
    return true;
}

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FIntroPIERestartTest, "StarTrekRPG.Intro.PIERestart",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FIntroPIERestartTest::RunTest(const FString& Parameters)
{
    ADD_LATENT_AUTOMATION_COMMAND(FEditorLoadMap(TEXT("/Game/Cinematics/L_Intro_StarTrekLegends")));
    for (int32 Run = 0; Run < 2; ++Run)
    {
        ADD_LATENT_AUTOMATION_COMMAND(FStartPIECommand(false));
        ADD_LATENT_AUTOMATION_COMMAND(FWaitLatentCommand(1.5f));
        ADD_LATENT_AUTOMATION_COMMAND(FCheckIntroPIE(this));
        ADD_LATENT_AUTOMATION_COMMAND(FEndPlayMapCommand());
        ADD_LATENT_AUTOMATION_COMMAND(FWaitLatentCommand(0.5f));
    }
    return true;
}
#endif
