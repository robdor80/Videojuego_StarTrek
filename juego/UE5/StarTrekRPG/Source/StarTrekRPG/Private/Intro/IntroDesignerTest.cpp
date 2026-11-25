#if WITH_EDITOR && WITH_DEV_AUTOMATION_TESTS
#include "Editor.h"
#include "Misc/AutomationTest.h"
#include "Subsystems/AssetEditorSubsystem.h"
#include "WidgetBlueprint.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FIntroDesignerTest, "StarTrekRPG.Intro.Designers",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FIntroDesignerTest::RunTest(const FString& Parameters)
{
    UAssetEditorSubsystem* Editors = GEditor->GetEditorSubsystem<UAssetEditorSubsystem>();
    const TCHAR* Names[] = {TEXT("Pike"), TEXT("Kirk"), TEXT("Janeway"), TEXT("Sisko"), TEXT("Picard")};
    for (const TCHAR* Name : Names)
    {
        const FString Path = FString::Printf(TEXT("/Game/Cinematics/UI_Intro/WBP_Intro_%s.WBP_Intro_%s"), Name, Name);
        UWidgetBlueprint* Blueprint = LoadObject<UWidgetBlueprint>(nullptr, *Path);
        if (!TestNotNull(Path, Blueprint))
        {
            continue;
        }
        const bool bWasOpen = Editors->FindEditorForAsset(Blueprint, false) != nullptr;
        TestTrue(FString::Printf(TEXT("Open Widget Blueprint for %s"), Name), Editors->OpenEditorForAsset(Blueprint));
        TestNotNull(FString::Printf(TEXT("Asset editor instance for %s"), Name), Editors->FindEditorForAsset(Blueprint, false));
        if (!bWasOpen)
        {
            Editors->CloseAllEditorsForAsset(Blueprint);
        }
    }
    return true;
}
#endif
