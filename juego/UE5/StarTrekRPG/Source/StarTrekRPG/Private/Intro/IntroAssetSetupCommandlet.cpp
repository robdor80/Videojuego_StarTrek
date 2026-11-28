#include "IntroAssetSetupCommandlet.h"

#if WITH_EDITOR
#include "IntroCinematicPlayer.h"

#include "Animation/WidgetAnimation.h"
#include "AssetRegistry/AssetRegistryModule.h"
#include "AssetToolsModule.h"
#include "Blueprint/WidgetTree.h"
#include "Components/CanvasPanel.h"
#include "Components/CanvasPanelSlot.h"
#include "Components/Image.h"
#include "Components/TextBlock.h"
#include "EditorFramework/AssetImportData.h"
#include "Engine/Blueprint.h"
#include "Engine/Texture2D.h"
#include "Blueprint/UserWidget.h"
#include "EngineUtils.h"
#include "Factories/SoundFactory.h"
#include "FileHelpers.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/WorldSettings.h"
#include "Kismet2/BlueprintEditorUtils.h"
#include "Kismet2/KismetEditorUtilities.h"
#include "LevelSequenceActor.h"
#include "Misc/PackageName.h"
#include "Misc/Parse.h"
#include "MovieScene.h"
#include "Sound/SoundWave.h"
#include "UObject/SavePackage.h"
#include "WidgetBlueprint.h"

DEFINE_LOG_CATEGORY_STATIC(LogIntroSetup, Log, All);

namespace
{
    const FString MapPath = TEXT("/Game/Cinematics/L_Intro_StarTrekLegends");
    const FString UIPath = TEXT("/Game/Cinematics/UI_Intro/");
    const FString TexturePath = TEXT("/Game/Cinematics/Textures_Intro/");
    const FString MusicPath = TEXT("/Game/Cinematics/Audio_Intro/SW_Intro_Music");
    const FString LegacyClass = TEXT("/Game/Cinematics/BP_IntroController.BP_IntroController_C");

    struct FPair
    {
        const TCHAR* WidgetName;
        const TCHAR* ShipTexture;
        const TCHAR* CaptainTexture;
        const TCHAR* ShipId;
        const TCHAR* Ship;
        const TCHAR* Captain;
    };

    const FPair Pairs[] = {
        {TEXT("WBP_Intro_Pike"), TEXT("ncc1701"), TEXT("pike"), nullptr, nullptr, nullptr},
        {TEXT("WBP_Intro_Kirk"), TEXT("ncc1701A"), TEXT("kirk"), TEXT("NCC-1701-A"), TEXT("USS Enterprise"), TEXT("James T. Kirk")},
        {TEXT("WBP_Intro_Janeway"), TEXT("voyager"), TEXT("jeanway"), TEXT("NCC-74656"), TEXT("USS Voyager"), TEXT("Kathryn Janeway")},
        {TEXT("WBP_Intro_Sisko"), TEXT("ds9"), TEXT("sisko"), TEXT("ESTACI\u00d3N ESPACIAL"), TEXT("Deep Space Nine"), TEXT("Benjamin Sisko")},
        {TEXT("WBP_Intro_Picard"), TEXT("ncc1701D"), TEXT("picard"), TEXT("NCC-1701-D"), TEXT("USS Enterprise"), TEXT("Jean-Luc Picard")}
    };
    static_assert(UE_ARRAY_COUNT(Pairs) == IntroTimeline::PairCount);

    constexpr const TCHAR* DesignElements[] = {
        TEXT("IMG_FondoNegro"), TEXT("IMG_Nave"), TEXT("TXT_Matricula"), TEXT("IMG_LineaNave"),
        TEXT("TXT_NombreNave"), TEXT("IMG_Capitan"), TEXT("TXT_RangoCapitan"),
        TEXT("IMG_LineaCapitan"), TEXT("TXT_NombreCapitan")
    };

    template<typename T>
    T* LoadAsset(const FString& Path)
    {
        if (!FPackageName::DoesPackageExist(Path))
        {
            return nullptr;
        }
        return LoadObject<T>(nullptr, *(Path + TEXT(".") + FPackageName::GetShortName(Path)));
    }

    bool SaveAsset(UObject* Object)
    {
        UPackage* Package = Object->GetOutermost();
        const FString Filename = FPackageName::LongPackageNameToFilename(
            Package->GetName(), FPackageName::GetAssetPackageExtension());
        FSavePackageArgs Args;
        Args.TopLevelFlags = RF_Public | RF_Standalone;
        return UPackage::SavePackage(Package, Object, *Filename, Args);
    }

    bool CheckStructure(const UWidgetBlueprint* Blueprint, bool bTribute)
    {
        if (!Blueprint || !Blueprint->WidgetTree || !Blueprint->WidgetTree->RootWidget)
        {
            return false;
        }
        for (const TCHAR* Name : DesignElements)
        {
            if (!Blueprint->WidgetTree->FindWidget(FName(Name)))
            {
                UE_LOG(LogIntroSetup, Error, TEXT("%s is missing %s"), *Blueprint->GetName(), Name);
                return false;
            }
        }
        return !bTribute || (
            Cast<UTextBlock>(Blueprint->WidgetTree->FindWidget(TEXT("TXT_HomenajePatrickStewart"))) &&
            Cast<UTextBlock>(Blueprint->WidgetTree->FindWidget(TEXT("TXT_FechasPatrickStewart"))));
    }

    void AddTribute(UWidgetTree& Tree, const UTextBlock& Reference, UCanvasPanel& Canvas,
        FName Name, const TCHAR* Content, float Y, int32 ZOrder)
    {
        UTextBlock* Text = Tree.ConstructWidget<UTextBlock>(UTextBlock::StaticClass(), Name);
        Text->SetFont(Reference.GetFont());
        Text->SetColorAndOpacity(FSlateColor(FLinearColor::White));
        Text->SetText(FText::FromString(Content));
        UCanvasPanelSlot* Slot = Canvas.AddChildToCanvas(Text);
        Slot->SetPosition(FVector2D(210, Y));
        Slot->SetSize(FVector2D(1750, 65));
        Slot->SetZOrder(ZOrder);
    }

    UWidgetBlueprint* CreatePair(UWidgetBlueprint& Source, const FPair& Pair)
    {
        const FString Path = UIPath + Pair.WidgetName;
        const bool bPicard = &Pair == &Pairs[UE_ARRAY_COUNT(Pairs) - 1];
        UTexture2D* Ship = LoadAsset<UTexture2D>(TexturePath + Pair.ShipTexture);
        UTexture2D* Captain = LoadAsset<UTexture2D>(TexturePath + Pair.CaptainTexture);
        if (!Ship || !Captain)
        {
            UE_LOG(LogIntroSetup, Error, TEXT("Missing source texture for %s"), Pair.WidgetName);
            return nullptr;
        }

        IAssetTools& AssetTools = FModuleManager::LoadModuleChecked<FAssetToolsModule>(TEXT("AssetTools")).Get();
        UWidgetBlueprint* Blueprint = Cast<UWidgetBlueprint>(
            AssetTools.DuplicateAsset(Pair.WidgetName, UIPath.LeftChop(1), &Source));
        if (!CheckStructure(Blueprint, false))
        {
            return nullptr;
        }

        const TArray<UEdGraph*> EventGraphs(Blueprint->UbergraphPages);
        for (UEdGraph* Graph : EventGraphs)
        {
            FBlueprintEditorUtils::RemoveGraph(Blueprint, Graph, EGraphRemoveFlags::None);
        }
        for (const UWidgetAnimation* Animation : Blueprint->Animations)
        {
            Blueprint->OnVariableRemoved(Animation->GetMovieScene()->GetFName());
        }
        Blueprint->Animations.Reset();
        Blueprint->Bindings.Reset();

        UWidgetTree& Tree = *Blueprint->WidgetTree;
        for (const TCHAR* Name : DesignElements)
        {
            Tree.FindWidget(FName(Name))->SetRenderOpacity(1.0f);
        }

        UImage* ShipImage = Cast<UImage>(Tree.FindWidget(TEXT("IMG_Nave")));
        UImage* CaptainImage = Cast<UImage>(Tree.FindWidget(TEXT("IMG_Capitan")));
        UTextBlock* Id = Cast<UTextBlock>(Tree.FindWidget(TEXT("TXT_Matricula")));
        UTextBlock* ShipName = Cast<UTextBlock>(Tree.FindWidget(TEXT("TXT_NombreNave")));
        UTextBlock* Rank = Cast<UTextBlock>(Tree.FindWidget(TEXT("TXT_RangoCapitan")));
        UTextBlock* CaptainName = Cast<UTextBlock>(Tree.FindWidget(TEXT("TXT_NombreCapitan")));
        if (!ShipImage || !CaptainImage || !Id || !ShipName || !Rank || !CaptainName)
        {
            UE_LOG(LogIntroSetup, Error, TEXT("Unexpected designer element types in %s"), Pair.WidgetName);
            return nullptr;
        }

        if (Pair.Ship)
        {
            ShipImage->SetBrushFromTexture(Ship);
            CaptainImage->SetBrushFromTexture(Captain);
            Id->SetText(FText::FromString(Pair.ShipId));
            ShipName->SetText(FText::FromString(Pair.Ship));
            Rank->SetText(FText::FromString(TEXT("CAPIT\u00c1N")));
            CaptainName->SetText(FText::FromString(Pair.Captain));
        }
        else if (ShipImage->GetBrush().GetResourceObject() != Ship || CaptainImage->GetBrush().GetResourceObject() != Captain)
        {
            UE_LOG(LogIntroSetup, Error, TEXT("Pike template textures differ from the expected asset references"));
            return nullptr;
        }

        if (bPicard)
        {
            UCanvasPanel* Canvas = Cast<UCanvasPanel>(CaptainName->GetParent());
            if (!Canvas)
            {
                UE_LOG(LogIntroSetup, Error, TEXT("Expected a canvas in Picard's composition"));
                return nullptr;
            }
            int32 TributeZOrder = 1;
            for (const UWidget* Child : Canvas->GetAllChildren())
            {
                if (const UCanvasPanelSlot* Slot = Cast<UCanvasPanelSlot>(Child->Slot))
                {
                    TributeZOrder = FMath::Max(TributeZOrder, Slot->GetZOrder() + 1);
                }
            }
            AddTribute(Tree, *Id, *Canvas, TEXT("TXT_HomenajePatrickStewart"),
                TEXT("En memoria de Sir Patrick Stewart"), 1300.0f, TributeZOrder);
            AddTribute(Tree, *Id, *Canvas, TEXT("TXT_FechasPatrickStewart"),
                TEXT("1940 - 2026"), 1370.0f, TributeZOrder);
            Blueprint->OnVariableAdded(TEXT("TXT_HomenajePatrickStewart"));
            Blueprint->OnVariableAdded(TEXT("TXT_FechasPatrickStewart"));
        }

        return Blueprint;
    }

    bool Compile(UWidgetBlueprint& Blueprint)
    {
        FKismetEditorUtilities::CompileBlueprint(&Blueprint);
        const bool bCompiled = Blueprint.Status == BS_UpToDate || Blueprint.Status == BS_UpToDateWithWarnings;
        UE_LOG(LogIntroSetup, Display, TEXT("%s compile status: %s"), *Blueprint.GetName(),
            Blueprint.Status == BS_UpToDate ? TEXT("clean") : bCompiled ? TEXT("warnings") : TEXT("failed"));
        return bCompiled;
    }

    USoundWave* ImportMusic(const FString& File)
    {
        if (File.IsEmpty())
        {
            return nullptr;
        }
        UPackage* Package = CreatePackage(*MusicPath);
        const FName Name(*FPackageName::GetShortName(MusicPath));
        USoundFactory* Factory = NewObject<USoundFactory>();
        Factory->bAutoCreateCue = false;
        Factory->SuppressImportDialogs();

        bool bCanceled = false;
        USoundWave* Music = Cast<USoundWave>(
            Factory->ImportObject(USoundWave::StaticClass(), Package, Name,
                RF_Public | RF_Standalone, File, nullptr, bCanceled));
        if (!Music || !FMath::IsNearlyEqual(static_cast<double>(Music->GetDuration()), IntroTimeline::End, 0.001))
        {
            UE_LOG(LogIntroSetup, Error, TEXT("Music import failed or WAV duration does not match the intro timeline"));
            return nullptr;
        }

        if (Music->AssetImportData)
        {
            Music->AssetImportData->SourceData.SourceFiles.Reset();
        }
        Music->bLooping = false;
        Music->LoadingBehavior = ESoundWaveLoadingBehavior::ForceInline;
        Music->SetSoundAssetCompressionType(ESoundAssetCompressionType::PCM);
        FAssetRegistryModule::AssetCreated(Music);
        return SaveAsset(Music) ? Music : nullptr;
    }

    bool VerifyPike(const UWidgetBlueprint& Source, const UWidgetBlueprint& Pike)
    {
        const auto CheckProperty = [](const UObject& A, const UObject& B, FName Name)
        {
            const FProperty* Property = A.GetClass()->FindPropertyByName(Name);
            return Property && Property->Identical_InContainer(&A, &B);
        };

        TArray<UWidget*> Originals;
        Source.WidgetTree->GetAllWidgets(Originals);
        for (const UWidget* Original : Originals)
        {
            const UWidget* Copy = Pike.WidgetTree->FindWidget(Original->GetFName());
            if (!Copy || Copy->GetClass() != Original->GetClass())
            {
                UE_LOG(LogIntroSetup, Error, TEXT("Pike widget tree differs at %s"), *Original->GetName());
                return false;
            }
            const UPanelWidget* OriginalParent = Original->GetParent();
            const UPanelWidget* CopyParent = Copy->GetParent();
            if (OriginalParent && (!CopyParent || CopyParent->GetFName() != OriginalParent->GetFName() ||
                OriginalParent->GetChildIndex(Original) != CopyParent->GetChildIndex(Copy)))
            {
                UE_LOG(LogIntroSetup, Error, TEXT("Pike widget parent or order differs at %s"), *Original->GetName());
                return false;
            }
            TArray<FName> Properties = {TEXT("RenderTransform"), TEXT("RenderTransformPivot"), TEXT("Visibility")};
            if (Original->IsA<UImage>())
            {
                Properties.Append({TEXT("Brush"), TEXT("ColorAndOpacity")});
            }
            if (Original->IsA<UTextBlock>())
            {
                Properties.Append({TEXT("Text"), TEXT("Font"), TEXT("ColorAndOpacity"), TEXT("Justification")});
            }
            for (const FName Property : Properties)
            {
                if (!CheckProperty(*Original, *Copy, Property))
                {
                    UE_LOG(LogIntroSetup, Error, TEXT("Pike property differs at %s.%s"), *Original->GetName(), *Property.ToString());
                    return false;
                }
            }
            if (Original->Slot && Original->Slot->IsA<UCanvasPanelSlot>() &&
                (!Copy->Slot || !CheckProperty(*Original->Slot, *Copy->Slot, TEXT("LayoutData")) ||
                    !CheckProperty(*Original->Slot, *Copy->Slot, TEXT("ZOrder"))))
            {
                UE_LOG(LogIntroSetup, Error, TEXT("Pike canvas layout differs at %s"), *Original->GetName());
                return false;
            }
        }
        UE_LOG(LogIntroSetup, Display, TEXT("Pike checked: hierarchy, order, canvas layout, image brushes, colors, text and typography"));
        return true;
    }
}

int32 UIntroAssetSetupCommandlet::Main(const FString& Params)
{
    const bool bApply = FParse::Param(*Params, TEXT("Apply"));
    const bool bInspect = FParse::Param(*Params, TEXT("Inspect"));
    FString AudioFile;
    FParse::Value(*Params, TEXT("MusicWav="), AudioFile);
    const auto Fail = [](const TCHAR* Message)
    {
        UE_LOG(LogIntroSetup, Error, TEXT("%s"), Message);
        return 1;
    };

    UWidgetBlueprint* Source = LoadAsset<UWidgetBlueprint>(UIPath + TEXT("WBP_IntroScene"));
    if (!CheckStructure(Source, false))
    {
        return Fail(TEXT("The protected WBP_IntroScene template is required"));
    }

    UWorld* World = UEditorLoadingAndSavingUtils::LoadMap(MapPath);
    if (!World)
    {
        return Fail(TEXT("The existing intro level is required"));
    }

    TArray<AActor*> LegacyActors;
    TArray<ALevelSequenceActor*> AutoplaySequences;
    AIntroCinematicPlayer* Player = nullptr;
    for (TActorIterator<AActor> It(World); It; ++It)
    {
        AActor* Actor = *It;
        if (bInspect)
        {
            UE_LOG(LogIntroSetup, Display, TEXT("Map actor: %s [%s]"), *Actor->GetName(), *Actor->GetClass()->GetPathName());
        }
        if (Actor->GetClass()->GetPathName() == LegacyClass)
        {
            LegacyActors.Add(Actor);
        }
        if (ALevelSequenceActor* Sequence = Cast<ALevelSequenceActor>(Actor))
        {
            if (Sequence->PlaybackSettings.bAutoPlay)
            {
                AutoplaySequences.Add(Sequence);
            }
        }
        if (AIntroCinematicPlayer* Existing = Cast<AIntroCinematicPlayer>(Actor))
        {
            if (Player)
            {
                return Fail(TEXT("The level contains multiple intro players"));
            }
            Player = Existing;
        }
    }
    if (bInspect)
    {
        Source->WidgetTree->ForEachWidget([](UWidget* Widget)
        {
            UE_LOG(LogIntroSetup, Display, TEXT("Designer: %s [%s] opacity %.3f visibility %d"),
                *Widget->GetName(), *Widget->GetClass()->GetName(), Widget->GetRenderOpacity(),
                static_cast<int32>(Widget->GetVisibility()));
        });
        UE_LOG(LogIntroSetup, Display, TEXT("Source animations %d, bindings %d, autoplay sequences %d"),
            Source->Animations.Num(), Source->Bindings.Num(), AutoplaySequences.Num());
        return 0;
    }

    TArray<TSubclassOf<UUserWidget>> Classes;
    for (const FPair& Pair : Pairs)
    {
        const bool bPicard = &Pair == &Pairs[UE_ARRAY_COUNT(Pairs) - 1];
        const FString Path = UIPath + Pair.WidgetName;
        UWidgetBlueprint* Blueprint = LoadAsset<UWidgetBlueprint>(Path);
        const bool bNew = bApply && !Blueprint && !FPackageName::DoesPackageExist(Path);
        if (bNew)
        {
            Blueprint = CreatePair(*Source, Pair);
        }
        if (!CheckStructure(Blueprint, bPicard) || !Compile(*Blueprint))
        {
            return Fail(TEXT("Pair widget is missing or invalid"));
        }
        if (&Pair == &Pairs[0] && FParse::Param(*Params, TEXT("CheckInitialLayout")) && !VerifyPike(*Source, *Blueprint))
        {
            return 1;
        }
        if (bNew && !SaveAsset(Blueprint))
        {
            return Fail(TEXT("Could not save pair widget"));
        }
        Classes.Add(Blueprint->GeneratedClass.Get());
    }

    USoundWave* Music = LoadAsset<USoundWave>(MusicPath);
    const bool bRefreshMusic = FParse::Param(*Params, TEXT("RefreshMusic"));
    if (bRefreshMusic || (bApply && !Music && !FPackageName::DoesPackageExist(MusicPath)))
    {
        Music = ImportMusic(AudioFile);
    }
    if (!Music || Music->bLooping ||
        !FMath::IsNearlyEqual(static_cast<double>(Music->GetDuration()), IntroTimeline::End, 0.001))
    {
        return Fail(TEXT("Intro music must be non-looping and match the timeline. Use -RefreshMusic -MusicWav=<WAV>."));
    }
    UE_LOG(LogIntroSetup, Display, TEXT("Music duration %.6f s, looping %d, external source entries %d"),
        Music->GetDuration(), Music->bLooping,
        Music->AssetImportData ? Music->AssetImportData->GetSourceFileCount() : 0);

    AWorldSettings* Settings = World->GetWorldSettings();
    if (!bApply)
    {
        if (!Player || Player->PairWidgets != Classes || Player->Music != Music || !LegacyActors.IsEmpty() ||
            !AutoplaySequences.IsEmpty() || Settings->DefaultGameMode != AGameModeBase::StaticClass())
        {
            return Fail(TEXT("The level is not wired for one intro playback"));
        }
        return 0;
    }

    const bool bMapChanged = !Player || Player->PairWidgets != Classes || Player->Music != Music ||
        !LegacyActors.IsEmpty() || !AutoplaySequences.IsEmpty() || Settings->DefaultGameMode != AGameModeBase::StaticClass();
    if (!bMapChanged)
    {
        return 0;
    }

    if (!Player)
    {
        Player = World->SpawnActor<AIntroCinematicPlayer>();
    }
    if (!Player)
    {
        return Fail(TEXT("Could not place the intro player"));
    }
    Player->SetActorLabel(TEXT("Intro Cinematic Player"));
    Player->PairWidgets = MoveTemp(Classes);
    Player->Music = Music;
    Settings->DefaultGameMode = AGameModeBase::StaticClass();

    for (AActor* Legacy : LegacyActors)
    {
        if (!World->EditorDestroyActor(Legacy, true))
        {
            return Fail(TEXT("Could not remove the legacy controller from the intro level"));
        }
    }
    for (ALevelSequenceActor* Sequence : AutoplaySequences)
    {
        Sequence->PlaybackSettings.bAutoPlay = false;
    }

    return UEditorLoadingAndSavingUtils::SaveMap(World, MapPath) ? 0 : Fail(TEXT("Could not save the intro level"));
}
#else
int32 UIntroAssetSetupCommandlet::Main(const FString&)
{
    return 1;
}
#endif
