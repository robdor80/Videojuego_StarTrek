#include "ActOneAssetSetupCommandlet.h"

#if WITH_EDITOR
#include "ActOneTimeline.h"

#include "AssetRegistry/AssetRegistryModule.h"
#include "Blueprint/WidgetTree.h"
#include "Components/TextBlock.h"
#include "EditorFramework/AssetImportData.h"
#include "Engine/Font.h"
#include "Engine/Texture2D.h"
#include "Factories/SoundFactory.h"
#include "Factories/TextureFactory.h"
#include "HAL/FileManager.h"
#include "JsonObjectConverter.h"
#include "Misc/FileHelper.h"
#include "Misc/PackageName.h"
#include "Misc/Parse.h"
#include "Sound/SoundClass.h"
#include "Sound/SoundWave.h"
#include "UObject/SavePackage.h"
#include "WidgetBlueprint.h"

DEFINE_LOG_CATEGORY_STATIC(LogActOneSetup, Log, All);

namespace
{
    const FString Root = TEXT("/Game/Cinematics/Act_One/");

    template<typename T>
    T* Existing(const FString& Package)
    {
        return FPackageName::DoesPackageExist(Package) ?
            LoadObject<T>(nullptr, *(Package + TEXT(".") + FPackageName::GetShortName(Package))) : nullptr;
    }

    bool Save(UObject& Asset)
    {
        UPackage* Package = Asset.GetOutermost();
        FSavePackageArgs Args;
        Args.TopLevelFlags = RF_Public | RF_Standalone;
        const FString Filename = FPackageName::LongPackageNameToFilename(
            Package->GetName(), FPackageName::GetAssetPackageExtension());
        return UPackage::SavePackage(Package, &Asset, *Filename, Args);
    }

    template<typename T>
    T* Import(UFactory& Factory, const FString& PackagePath, const FString& File)
    {
        UPackage* Package = CreatePackage(*PackagePath);
        bool bCancelled = false;
        return Cast<T>(Factory.ImportObject(T::StaticClass(), Package, FName(*FPackageName::GetShortName(PackagePath)),
            RF_Public | RF_Standalone, File, nullptr, bCancelled));
    }

    bool InstallShot(FActOneShot& Shot, const FString& AssetsRoot)
    {
        FString Name = Shot.Id;
        Name.ReplaceInline(TEXT("."), TEXT("_"));
        const FString Package = Root + TEXT("Images/T_") + Name;
        Shot.Image = Existing<UTexture2D>(Package);
        if (!Shot.Image)
        {
            UTextureFactory* Factory = NewObject<UTextureFactory>();
            Shot.Image = Import<UTexture2D>(*Factory, Package, AssetsRoot / Shot.File);
            if (!Shot.Image || Shot.Image->Source.GetSizeX() != Shot.Width || Shot.Image->Source.GetSizeY() != Shot.Height)
            {
                UE_LOG(LogActOneSetup, Error, TEXT("Invalid image: %s (%dx%d expected)"), *Shot.File, Shot.Width, Shot.Height);
                return false;
            }
            Shot.Image->AssetImportData->SourceData.SourceFiles.Reset();
            Shot.Image->CompressionSettings = TC_EditorIcon;
            Shot.Image->MipGenSettings = TMGS_NoMipmaps;
            Shot.Image->LODGroup = TEXTUREGROUP_UI;
            Shot.Image->NeverStream = true;
            Shot.Image->PostEditChange();
            FAssetRegistryModule::AssetCreated(Shot.Image);
            if (!Save(*Shot.Image))
            {
                return false;
            }
        }
        UE_LOG(LogActOneSetup, Display, TEXT("Image %s: %s (%dx%d)"), *Shot.Id, *Shot.File, Shot.Width, Shot.Height);
        return true;
    }

    USoundClass* Bus(const TCHAR* Name)
    {
        const FString Package = Root + TEXT("Audio/SC_") + Name;
        if (USoundClass* ExistingBus = Existing<USoundClass>(Package))
        {
            return ExistingBus;
        }
        USoundClass* Class = NewObject<USoundClass>(CreatePackage(*Package),
            FName(*FPackageName::GetShortName(Package)), RF_Public | RF_Standalone);
        FAssetRegistryModule::AssetCreated(Class);
        return Save(*Class) ? Class : nullptr;
    }

    USoundWave* InstallWave(const TCHAR* Name, const FString& File, USoundClass* Class, bool bLoop, bool bRefresh)
    {
        const FString Package = Root + TEXT("Audio/") + Name;
        if (USoundWave* ExistingWave = Existing<USoundWave>(Package); ExistingWave && !bRefresh)
        {
            return ExistingWave;
        }
        USoundFactory* Factory = NewObject<USoundFactory>();
        Factory->bAutoCreateCue = false;
        Factory->SuppressImportDialogs();
        USoundWave* Wave = Import<USoundWave>(*Factory, Package, File);
        if (!Wave)
        {
            UE_LOG(LogActOneSetup, Error, TEXT("Could not import WAV: %s"), *File);
            return nullptr;
        }
        Wave->AssetImportData->SourceData.SourceFiles.Reset();
        Wave->SoundClassObject = Class;
        Wave->bLooping = bLoop;
        Wave->LoadingBehavior = ESoundWaveLoadingBehavior::ForceInline;
        Wave->SetSoundAssetCompressionType(ESoundAssetCompressionType::PCM);
        FAssetRegistryModule::AssetCreated(Wave);
        return Save(*Wave) ? Wave : nullptr;
    }

    bool Report(UActOneTimeline* Timeline)
    {
        FString Error;
        if (!Timeline || !Timeline->Validate(Error))
        {
            UE_LOG(LogActOneSetup, Error, TEXT("Act I package validation failed: %s"), *Error);
            return false;
        }
        UE_LOG(LogActOneSetup, Display, TEXT("Validated 27 images, 22 interventions, audio %.6f / %.6f / %.6f, fonts %s / %s."),
            Timeline->London->GetDuration(), Timeline->Ode->GetDuration(), Timeline->CouncilAmbience->Duration,
            *Timeline->TitleFont->GetPathName(), *Timeline->DialogueFont->GetPathName());
        return true;
    }
}

int32 UActOneAssetSetupCommandlet::Main(const FString& Params)
{
    if (!FParse::Param(*Params, TEXT("Apply")))
    {
        return Report(Existing<UActOneTimeline>(UActOneTimeline::PackagePath)) ? 0 : 1;
    }
    FString Source, AssetsRoot, WavRoot;
    if (!FParse::Value(*Params, TEXT("Timeline="), Source) ||
        !FParse::Value(*Params, TEXT("AssetsRoot="), AssetsRoot) ||
        !FParse::Value(*Params, TEXT("WavRoot="), WavRoot))
    {
        UE_LOG(LogActOneSetup, Error, TEXT("Provide -Timeline, -AssetsRoot and -WavRoot with -Apply"));
        return 1;
    }

    FString Json;
    UActOneTimeline* Parsed = NewObject<UActOneTimeline>();
    FString Error;
    if (!FFileHelper::LoadFileToString(Json, *Source) ||
        !FJsonObjectConverter::JsonObjectStringToUStruct(Json, Parsed) ||
        !Parsed->Validate(Error, false))
    {
        UE_LOG(LogActOneSetup, Error, TEXT("Invalid timeline %s: %s"), *Source, *Error);
        return 1;
    }

    TArray<FActOneShot*> Shots;
    for (FActOneShot& Shot : Parsed->Opening)
    {
        Shots.Add(&Shot);
    }
    for (FActOneIntervention& Line : Parsed->Interventions)
    {
        for (FActOneShot& Shot : Line.Shots)
        {
            Shots.Add(&Shot);
        }
    }
    for (const FActOneShot* Shot : Shots)
    {
        if (!FPaths::IsRelative(Shot->File) || Shot->File.Contains(TEXT("..")) ||
            !IFileManager::Get().FileExists(*(AssetsRoot / Shot->File)))
        {
            UE_LOG(LogActOneSetup, Error, TEXT("Missing or invalid relative source image path %s"), *Shot->File);
            return 1;
        }
    }

    UWidgetBlueprint* Pike = Existing<UWidgetBlueprint>(TEXT("/Game/Cinematics/UI_Intro/WBP_Intro_Pike"));
    const UTextBlock* IntroTitle = Pike && Pike->WidgetTree ?
        Cast<UTextBlock>(Pike->WidgetTree->FindWidget(TEXT("TXT_NombreCapitan"))) : nullptr;
    Parsed->TitleFont = IntroTitle ? Cast<UFont>(const_cast<UObject*>(IntroTitle->GetFont().FontObject.Get())) : nullptr;
    Parsed->DialogueFont = LoadObject<UFont>(nullptr, TEXT("/Engine/EngineFonts/Roboto.Roboto"));
    if (!Parsed->TitleFont || !Parsed->DialogueFont)
    {
        UE_LOG(LogActOneSetup, Error, TEXT("Verified intro title font or engine Roboto unavailable"));
        return 1;
    }

    for (FActOneShot* Shot : Shots)
    {
        if (!InstallShot(*Shot, AssetsRoot))
        {
            return 1;
        }
    }
    USoundClass* Music = Bus(TEXT("MUSIC"));
    USoundClass* Ambience = Bus(TEXT("AMBIENCE"));
    Parsed->VoiceClass = Bus(TEXT("VOICE"));
    Parsed->SfxClass = Bus(TEXT("SFX"));
    if (!Music || !Ambience || !Parsed->VoiceClass || !Parsed->SfxClass)
    {
        return 1;
    }
    const bool bRefreshAudio = FParse::Param(*Params, TEXT("RefreshAudio"));
    Parsed->London = InstallWave(TEXT("SW_LondonCalling"), WavRoot / TEXT("London.wav"), Music, false, bRefreshAudio);
    Parsed->Ode = InstallWave(TEXT("SW_OdeToHarrison"), WavRoot / TEXT("Ode.wav"), Music, false, bRefreshAudio);
    Parsed->CouncilAmbience = InstallWave(TEXT("SW_CouncilAmbience"), WavRoot / TEXT("CouncilLoop.wav"), Ambience, true, bRefreshAudio);
    if (!Report(Parsed))
    {
        return 1;
    }

    UActOneTimeline* Timeline = Existing<UActOneTimeline>(UActOneTimeline::PackagePath);
    if (!Timeline)
    {
        Timeline = DuplicateObject<UActOneTimeline>(Parsed, CreatePackage(UActOneTimeline::PackagePath), TEXT("DA_ActOneTimeline"));
        Timeline->SetFlags(RF_Public | RF_Standalone);
        FAssetRegistryModule::AssetCreated(Timeline);
    }
    else
    {
        // Versioned layout and text are authoritative on reimport. Preserve UE-only authoring.
        for (FActOneIntervention& Line : Parsed->Interventions)
        {
            if (const FActOneIntervention* Old = Timeline->Interventions.FindByPredicate(
                [&Line](const FActOneIntervention& Candidate) { return Candidate.Id == Line.Id; }))
            {
                Line.Voice = Old->Voice;
            }
        }
        Timeline->Opening = MoveTemp(Parsed->Opening);
        Timeline->Interventions = MoveTemp(Parsed->Interventions);
        Timeline->TitleFont = Parsed->TitleFont;
        Timeline->DialogueFont = Parsed->DialogueFont;
        Timeline->London = Parsed->London;
        Timeline->Ode = Parsed->Ode;
        Timeline->CouncilAmbience = Parsed->CouncilAmbience;
        Timeline->VoiceClass = Parsed->VoiceClass;
        Timeline->SfxClass = Parsed->SfxClass;
    }
    return Save(*Timeline) ? 0 : 1;
}

#else
int32 UActOneAssetSetupCommandlet::Main(const FString&)
{
    return 1;
}
#endif
