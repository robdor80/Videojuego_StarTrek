#pragma once
#include "HostSessionSubsystem.h"
#include "HostRuntime.h"
#include "Widgets/SCompoundWidget.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "Widgets/Text/STextBlock.h"

// Presentation only. The HOST resolves the subject; event is only a lookup key.
class SHostInstitutionalView final : public SCompoundWidget
{
public:
    SLATE_BEGIN_ARGS(SHostInstitutionalView) {}
        SLATE_ARGUMENT(UHostSessionSubsystem*, Host)
        SLATE_ARGUMENT(UHostWorldProjection*, Projection)
    SLATE_END_ARGS()
    void Construct(const FArguments& Args)
    {
        Host = Args._Host;
        Projection = Args._Projection;
        ChildSlot[
            SNew(SVerticalBox)
            + SVerticalBox::Slot().AutoHeight()[SNew(SButton).Tag(TEXT("H07Career"))
                .Text(FText::FromString(TEXT("Consultar mi expediente profesional")))
                .OnClicked_Lambda([this]() { return Query(TREK_HOST_CAREER); })]
            + SVerticalBox::Slot().AutoHeight()[SAssignNew(Event, SEditableTextBox).Tag(TEXT("H07Event"))
                .HintText(FText::FromString(TEXT("Identificador del evento de ascenso")))]
            + SVerticalBox::Slot().AutoHeight()[SNew(SButton).Tag(TEXT("H07Promotion"))
                .Text(FText::FromString(TEXT("Consultar ascenso confirmado")))
                .OnClicked_Lambda([this]() { return Query(TREK_HOST_PROMOTION); })]
            + SVerticalBox::Slot().AutoHeight()[SNew(STextBlock).Tag(TEXT("H07Facts"))
                .Text_Lambda([this]() { return Facts(); }).AutoWrapText(true)]
        ];
    }
private:
    FReply Query(uint32 Operation)
    {
        if (auto* Session = Host.Get(); Session && Projection.IsValid())
        {
            uint64 Id = 0;
            if (Operation == TREK_HOST_PROMOTION) LexTryParseString(Id, *Event->GetText().ToString());
            Session->QueryInstitutional(*Projection, Operation, Id);
        }
        return FReply::Handled();
    }
    FText Facts() const
    {
        FString Text;
        if (const auto* World = Projection.Get())
            for (uint32 Operation : {uint32(TREK_HOST_CAREER), uint32(TREK_HOST_PROMOTION)})
            {
                const auto Result = World->GetInstitutional(Operation);
                if (!Result.IsSet()) continue;
                if (Result->code != TREK_HOST_OK)
                    Text += FString::Printf(TEXT("%s: %s; sin datos autorizados.\n"),
                        Operation == TREK_HOST_CAREER ? TEXT("Expediente") : TEXT("Ascenso"), HostCodeName(Result->code));
                else if (Operation == TREK_HOST_CAREER)
                    Text += FString::Printf(TEXT("Rango F11 %u | Estado de servicio %u | Hecho de rango %llu | Revision Core %llu\n"),
                        Result->rank, Result->service_status, Result->event_id, Result->world_revision);
                else
                    Text += FString::Printf(TEXT("Ascenso %llu: %u a %u | Fecha efectiva (tick Core) %llu | Revision original %llu\n"),
                        Result->event_id, Result->from_rank, Result->to_rank, Result->effective_tick, Result->original_revision);
            }
        return FText::FromString(Text);
    }
    TWeakObjectPtr<UHostSessionSubsystem> Host;
    TWeakObjectPtr<UHostWorldProjection> Projection;
    TSharedPtr<SEditableTextBox> Event;
};
