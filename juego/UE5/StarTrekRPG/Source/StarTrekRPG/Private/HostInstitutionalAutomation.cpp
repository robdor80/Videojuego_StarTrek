#if WITH_DEV_AUTOMATION_TESTS
#include "HostSessionSubsystem.h"
#include "HostDiagnosticGameMode.h"
#include "HostSlateAutomation.h"
#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "Misc/AutomationTest.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/FileHelper.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "Widgets/Text/STextBlock.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FHostInstitutional, "StarTrek.H07.Institutional.Roundtrip",
    EAutomationTestFlags::ClientContext | EAutomationTestFlags::ProductFilter)

bool FHostInstitutional::RunTest(const FString&)
{
    struct FRun
    {
        FAutomationTestBase* Test;
        FString Campaign;
        uint64 Event=0, OriginalRevision=0, Generation=0, Revision=0;
        int32 Step=0;
        double Deadline=FPlatformTime::Seconds()+120;
        bool Fail(const TCHAR* Why) { Test->AddError(FString::Printf(TEXT("H07 step %d: %s"),Step,Why));return true; }
        bool Tick()
        {
            if (FPlatformTime::Seconds()>Deadline) return Fail(TEXT("timeout"));
            UWorld* World=nullptr;
            for(const auto& Context:GEngine->GetWorldContexts())
                if(Context.World()&&Context.World()->IsGameWorld()&&Context.World()->HasBegunPlay()) World=Context.World();
            if(!World)return false;
            auto* Game=World->GetGameInstance();
            auto* Host=Game?Game->GetSubsystem<UHostSessionSubsystem>():nullptr;
            auto* Projection=World->GetSubsystem<UHostWorldProjection>();
            auto* Player=Game?Cast<AHostDiagnosticPlayerController>(Game->GetFirstLocalPlayerController(World)):nullptr;
            const auto Panel=Player?Player->GetDiagnosticPanel():TSharedPtr<SWidget>();
            if(!Host||Host->IsInitializing()||!Projection||!Panel)return false;
            if(!Host->IsAvailable())return Fail(TEXT("real native DLL unavailable"));
            const auto Career=Projection->GetInstitutional(TREK_HOST_CAREER);
            const auto Promotion=Projection->GetInstitutional(TREK_HOST_PROMOTION);
            auto Query=[&](uint32 Op,uint64 Id=0){const auto C=Host->QueryInstitutional(*Projection,Op,Id);if(C==TREK_HOST_RETRY)return false;if(C!=TREK_HOST_OK)Test->AddError(TEXT("query not admitted"));return C==TREK_HOST_OK;};
            auto Complete=[&](uint32 Op){const auto& C=Projection->GetCompletion();return C.IsSet()&&C->operation==Op&&C->code==TREK_HOST_OK;};
            switch(Step)
            {
            case 0:
            {
                FString Path,Record;
                if(!FParse::Value(FCommandLine::Get(),TEXT("H07Expected="),Path)||!FFileHelper::LoadFileToString(Record,*Path))return Fail(TEXT("isolated F11/H04 fixture metadata required"));
                TArray<FString> Fields;Record.ParseIntoArrayWS(Fields);
                if(Fields.Num()!=3||!LexTryParseString(Event,*Fields[1])||!LexTryParseString(OriginalRevision,*Fields[2]))return Fail(TEXT("bad fixture metadata"));
                Campaign=Fields[0];
                if(Query(TREK_HOST_CAREER))Step=1;
                break;
            }
            case 1:
                if(!Career.IsSet())break;
                if(Career->code!=TREK_HOST_SESSION_CLOSED||Career->event_id||Career->rank||Career->generation)return Fail(TEXT("closed query leaked facts"));
                if(Host->Restore(*Projection,Campaign,TEXT("career"))==TREK_HOST_OK)Step=2;
                break;
            case 2:
                if(!Complete(TREK_HOST_RESTORE))break;
                Generation=Host->GetStatus().generation;
                if(!Generation||Host->GetStatus().principal!=TREK_HOST_OK)return Fail(TEXT("restored binding missing"));
                {
                    auto Field=StaticCastSharedPtr<SEditableTextBox>(FindHostWidget(Panel.ToSharedRef(),TEXT("H07Event")));
                    auto CareerButton=StaticCastSharedPtr<SButton>(FindHostWidget(Panel.ToSharedRef(),TEXT("H07Career")));
                    auto PromotionButton=StaticCastSharedPtr<SButton>(FindHostWidget(Panel.ToSharedRef(),TEXT("H07Promotion")));
                    if(!Field||!CareerButton||!PromotionButton)return Fail(TEXT("actual institutional Slate controls missing"));
                    Field->SetText(FText::AsNumber(Event,&FNumberFormattingOptions::DefaultNoGrouping()));
                    CareerButton->SimulateClick();PromotionButton->SimulateClick();Step=3;
                }
                break;
            case 3:
                if(!Career.IsSet()||!Promotion.IsSet())break;
                if(Career->code||Promotion->code||Career->rank!=1102||Career->event_id!=Event||
                    Promotion->event_id!=Event||Promotion->original_revision!=OriginalRevision||Promotion->from_rank!=1101||Promotion->to_rank!=1102)
                    return Fail(TEXT("facts differ from isolated confirmed F11 Core archive"));
                Revision=Career->world_revision;
                {
                    Panel->SlatePrepass(1.0f);
                    auto Label=StaticCastSharedPtr<STextBlock>(FindHostWidget(Panel.ToSharedRef(),TEXT("H07Facts")));
                    if(!Label||!Label->GetText().ToString().Contains(TEXT("1102")))return Fail(TEXT("authorized facts not presented"));
                }
                Test->AddInfo(FString::Printf(TEXT("REAL H07: campaign=%s rank=%u status=%u event=%llu effective_tick=%llu original_revision=%llu world_revision=%llu correlation=%llu/%llu"),
                    *Campaign,Career->rank,Career->service_status,Event,Promotion->effective_tick,OriginalRevision,Revision,Career->correlation,Promotion->correlation));
                if(Query(TREK_HOST_PROMOTION,Event+1000))Step=4;
                break;
            case 4:
                if(!Promotion.IsSet())break;
                if(Promotion->code!=TREK_HOST_ACCESS_DENIED||Promotion->event_id||Promotion->generation)return Fail(TEXT("foreign/unknown lookup leaked"));
                if(Query(TREK_HOST_CAREER))Step=5;
                break;
            case 5:
                if(!Career.IsSet())break;
                if(Career->code||Career->world_revision!=Revision)return Fail(TEXT("repeat changed revision"));
                if(Host->Save(*Projection,TEXT("ue_h07"))==TREK_HOST_OK)
                {
                    if(Projection->GetInstitutional(TREK_HOST_CAREER).IsSet())return Fail(TEXT("SAVE retained facts"));Step=6;
                }
                break;
            case 6:
                if(Complete(TREK_HOST_SAVE)&&Query(TREK_HOST_CAREER))Step=7;
                break;
            case 7:
                if(!Career.IsSet())break;
                if(Career->code||Career->rank!=1102||Career->world_revision!=Revision)return Fail(TEXT("post-save query wrong"));
                if(Host->Restore(*Projection,Campaign,TEXT("career"))==TREK_HOST_OK)
                {
                    if(Projection->GetInstitutional(TREK_HOST_CAREER).IsSet())return Fail(TEXT("RESTORE retained facts"));Step=8;
                }
                break;
            case 8:
                if(!Complete(TREK_HOST_RESTORE))break;
                if(Host->GetStatus().generation==Generation)return Fail(TEXT("RESTORE did not retire generation"));
                if(Query(TREK_HOST_PROMOTION,Event))Step=9;
                break;
            case 9:
                if(!Promotion.IsSet())break;
                if(Promotion->code||Promotion->original_revision!=OriginalRevision||Promotion->world_revision!=Revision)return Fail(TEXT("restore lost original event"));
                if(Query(TREK_HOST_CAREER)&&Host->Close(*Projection)==TREK_HOST_OK)Step=10;
                break;
            case 10:
                if(!Complete(TREK_HOST_CLOSE))break;
                if(Projection->GetInstitutional(TREK_HOST_CAREER).IsSet()||Projection->GetInstitutional(TREK_HOST_PROMOTION).IsSet())return Fail(TEXT("late reply survived CLOSE"));
                if(Host->CreateAcademy(*Projection,TEXT("Candidatura H07 laboratorio"))==TREK_HOST_OK)Step=11;
                break;
            case 11:
                if(!Projection->GetAcademyCandidate().IsSet())break;
                if(Query(TREK_HOST_CAREER))Step=12;
                break;
            case 12:
                if(!Career.IsSet())break;
                if(Career->code!=TREK_HOST_SERVICE_UNAVAILABLE||Career->event_id||Career->rank||Career->generation)return Fail(TEXT("cadet obtained institutional facts"));
                if(Host->GetStatus().institutional!=TREK_HOST_SERVICE_UNAVAILABLE)return Fail(TEXT("issuer enabled"));
                Test->AddInfo(TEXT("PASS UE real: canonical read, denial, correlation, repeat, SAVE, RESTORE, late CLOSE, uncommissioned Academy; F11 issuer unavailable"));return true;
            }
            return false;
        }
    };
    const auto Run=MakeShared<FRun>();Run->Test=this;
    ADD_LATENT_AUTOMATION_COMMAND(FFunctionLatentCommand([Run](){return Run->Tick();}));return true;
}
#endif
