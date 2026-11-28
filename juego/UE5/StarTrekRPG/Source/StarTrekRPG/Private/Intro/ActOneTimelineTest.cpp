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
    TestEqual(TEXT("Location appears at 0:05"), T::LocationStart, 5.0);
    TestEqual(TEXT("Exterior starts at 0:08"), Timeline->Opening[0].Start, 8.0);
    TestEqual(TEXT("Council starts at 0:12"), Timeline->Opening[1].Start, 12.0);
    TestTrue(TEXT("Opening holds before V1"), Intervention(15.999).IsEmpty());
    TestEqual(TEXT("V1 starts at 0:16"), Intervention(16), FString(TEXT("V1")));
    TestEqual(TEXT("V2 starts at 0:37"), Intervention(37), FString(TEXT("V2")));

    const FActOneIntervention& First = Timeline->Interventions[0];
    TArray<FString> Words;
    First.Dialogue.ParseIntoArrayWS(Words);
    TestEqual(TEXT("V1 retains the full dialogue"), Words.Num(), 54);
    if (TestEqual(TEXT("V1 has four reading blocks"), First.Cues.Num(), 4))
    {
        const double Boundaries[] = {16.35, 18.15, 23.3, 31.35, 36.55};
        for (int32 Index = 0; Index < First.Cues.Num(); ++Index)
        {
            TestEqual(TEXT("V1 block start"), First.Cues[Index].Start, Boundaries[Index]);
            TestEqual(TEXT("V1 block end"), First.Cues[Index].End, Boundaries[Index + 1]);
        }
    }
    TestFalse(TEXT("Act I ships with voices disabled"), Timeline->bEnableVoices);
    TestEqual(TEXT("V7 stays one intervention through all shots"), Intervention(146), FString(TEXT("V7")));
    TestEqual(TEXT("Vote at 7:30"), Intervention(450), FString(TEXT("V21")));
    TestEqual(TEXT("Climax at 7:55"), Intervention(475), FString(TEXT("V22")));
    TestTrue(TEXT("No caption is selected during the final fade"), Intervention(T::FinalFadeStart).IsEmpty());
    TestEqual(TEXT("Final black exactly at 8:10"), T::EndOpacity(490), 0.0f);

    TestEqual(TEXT("London starts at 0:15"), T::LondonStart, 15.0);
    TestEqual(TEXT("Ode starts at 2:10"), T::OdeStart, 130.0);
    TestEqual(TEXT("London ends at 2:25"), T::LondonEnd, 145.0);
    TestEqual(TEXT("London silent before its entry"), Timeline->LondonEnvelope(14.999), 0.0f);
    TestEqual(TEXT("London reaches its current gain at entry"), Timeline->LondonEnvelope(15), 1.0f);
    const FVector2f LondonAnchors[] = {{130, 1}, {133, 0.90f}, {135, 0.75f}, {138, 0.50f},
        {140, 0.30f}, {143, 0.10f}, {145, 0}};
    for (const FVector2f& Point : LondonAnchors)
    {
        TestEqual(TEXT("London fade anchor"), Timeline->LondonEnvelope(Point.X), Point.Y);
    }
    float PreviousGain = 1.0f;
    for (int32 Step = 1; Step <= 1500; ++Step)
    {
        const float Gain = Timeline->LondonEnvelope(T::OdeStart + Step * 0.01);
        if (Gain < 0.0f || Gain > PreviousGain + 1.e-6f || PreviousGain - Gain > 0.002f)
        {
            AddError(TEXT("London fade must decrease smoothly throughout the overlap."));
            break;
        }
        PreviousGain = Gain;
    }

    TestFalse(TEXT("Act I ships with Council ambience disabled"), Timeline->bEnableCouncilAmbience);
    TestEqual(TEXT("Optional ambience enters with London"), T::CouncilAmbienceStart, T::LondonStart);
    TestEqual(TEXT("Ambience silent before entry"), T::CouncilEnvelope(14.999), 0.0f);
    TestEqual(TEXT("Ambience starts from silence at 0:15"), T::CouncilEnvelope(15), 0.0f);
    TestEqual(TEXT("Ambience halfway up at 0:16"), T::CouncilEnvelope(16), 0.5f);
    TestEqual(TEXT("Ambience reaches its approved level at 0:17"), T::CouncilEnvelope(17), 1.0f);
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
    TArray<uint8> PCM;
    uint32 Rate = 0;
    uint16 Channels = 0;
    if (TestTrue(TEXT("Ode source PCM available"),
        Timeline->Ode->GetImportedSoundWaveData(PCM, Rate, Channels)))
    {
        TestEqual(TEXT("PCM sample rate"), Rate, 48000u);
        TestEqual(TEXT("PCM channel count"), Channels, static_cast<uint16>(2));
        const int16* Samples = reinterpret_cast<const int16*>(PCM.GetData());
        int32 Peak = 0;
        for (int32 Sample = 0; Sample < PCM.Num() / sizeof(int16); ++Sample)
        {
            Peak = FMath::Max(Peak, FMath::Abs(static_cast<int32>(Samples[Sample])));
        }
        TestTrue(TEXT("Converted Ode retains peaks with headroom"), Peak > 30000 && Peak < 32500);
    }
    return true;
}
#endif
