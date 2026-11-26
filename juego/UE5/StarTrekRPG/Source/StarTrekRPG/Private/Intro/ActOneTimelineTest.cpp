#include "ActOneTimeline.h"

#if WITH_DEV_AUTOMATION_TESTS && WITH_EDITOR
#include "Misc/AutomationTest.h"
#include "Misc/PackageName.h"
#include "Sound/SoundClass.h"
#include "Sound/SoundWave.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FActOneTimelineTest, "StarTrekRPG.Intro.ActOne.Timeline",
    EAutomationTestFlags::EditorContext | EAutomationTestFlags::EngineFilter)

bool FActOneTimelineTest::RunTest(const FString& Parameters)
{
    if (!FPackageName::DoesPackageExist(UActOneTimeline::PackagePath))
    {
        AddError(TEXT("Import the local Act I assets using Build/Import-ActOne.ps1."));
        return false;
    }
    const UActOneTimeline* Timeline = LoadObject<UActOneTimeline>(nullptr, UActOneTimeline::AssetPath);
    FString Error;
    if (!Timeline || !Timeline->Validate(Error))
    {
        AddError(TEXT("Invalid Act I package: ") + Error);
        return false;
    }

    using T = UActOneTimeline;
    const auto Intervention = [Timeline](double Time)
    {
        const FActOneIntervention* Line = Timeline->FindIntervention(Time);
        return Line ? Line->Id : FString();
    };
    TestTrue(TEXT("Opening holds before V1"), Intervention(9.999).IsEmpty());
    TestEqual(TEXT("V1 starts at ten seconds"), Intervention(10), FString(TEXT("V1")));
    TestEqual(TEXT("V7 stays one intervention through all shots"), Intervention(146), FString(TEXT("V7")));
    TestEqual(TEXT("Vote at 7:30"), Intervention(450), FString(TEXT("V21")));
    TestEqual(TEXT("Climax at 7:55"), Intervention(475), FString(TEXT("V22")));
    TestTrue(TEXT("No caption is selected during the final fade"), Intervention(T::FinalFadeStart).IsEmpty());
    TestEqual(TEXT("Final black exactly at 8:10"), T::EndOpacity(490), 0.0f);

    TestEqual(TEXT("Ambience begins silent at 7 s"), T::CouncilEnvelope(7), 0.0f);
    TestEqual(TEXT("Ambience fully in before V1"), T::CouncilEnvelope(9), 1.0f);
    TestTrue(TEXT("Borg memory ambience attenuated"), FMath::IsNearlyEqual(T::CouncilEnvelope(140), 0.22f, 1.e-5f));
    TestEqual(TEXT("Council ambience returns"), T::CouncilEnvelope(149), 1.0f);
    TestEqual(TEXT("Council ambience fades to silence"), T::CouncilEnvelope(490), 0.0f);
    TestTrue(TEXT("Ambience uses a single looping wave"), Timeline->CouncilAmbience->bLooping);
    TestTrue(TEXT("Music tracks are independent non-looping waves"),
        Timeline->London != Timeline->Ode && !Timeline->London->bLooping && !Timeline->Ode->bLooping);
    TestTrue(TEXT("Four separate audio classes"),
        Timeline->London->SoundClassObject && Timeline->Ode->SoundClassObject == Timeline->London->SoundClassObject &&
        Timeline->CouncilAmbience->SoundClassObject && Timeline->VoiceClass && Timeline->SfxClass &&
        TSet<USoundClass*>({Timeline->London->SoundClassObject, Timeline->CouncilAmbience->SoundClassObject,
            Timeline->VoiceClass, Timeline->SfxClass}).Num() == 4);
    return true;
}
#endif
