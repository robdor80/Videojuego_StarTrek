#include "HostDiagnosticGameMode.h"

#include "HostRuntime.h"
#include "HostSessionSubsystem.h"
#include "Engine/GameInstance.h"
#include "Engine/GameViewportClient.h"
#include "Engine/LocalPlayer.h"
#include "Engine/World.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Layout/SUniformGridPanel.h"
#include "Widgets/SCompoundWidget.h"
#include "Widgets/SOverlay.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/Text/STextBlock.h"

#define LOCTEXT_NAMESPACE "HostDiagnostic"

namespace
{
class SHostDiagnostic final : public SCompoundWidget
{
public:
    SLATE_BEGIN_ARGS(SHostDiagnostic) {}
        SLATE_ARGUMENT(UHostSessionSubsystem*, Host)
        SLATE_ARGUMENT(UHostWorldProjection*, Projection)
    SLATE_END_ARGS()

    void Construct(const FArguments& Args)
    {
        Host = Args._Host;
        Projection = Args._Projection;
        ChildSlot
        [
            SNew(SOverlay)
            + SOverlay::Slot().HAlign(HAlign_Center).VAlign(VAlign_Center).Padding(20)
            [
                SNew(SBox).WidthOverride(610)
                [
                    SNew(SBorder).Padding(18)
                    [
                        SNew(SVerticalBox)
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 12)
                        [
                            SNew(STextBlock).Text(LOCTEXT("Title", "Star Trek RPG | Diagnóstico HOST"))
                        ]
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 12)
                        [
                            SNew(STextBlock).Text(this, &SHostDiagnostic::StatusText)
                        ]
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 12)
                        [
                            SNew(SUniformGridPanel).SlotPadding(3)
                            + SUniformGridPanel::Slot(0, 0)[Button(LOCTEXT("Open", "Abrir sesión técnica"), TREK_HOST_OPEN)]
                            + SUniformGridPanel::Slot(1, 0)[Button(LOCTEXT("View", "Consultar vista"), TREK_HOST_QUERY_VIEW)]
                            + SUniformGridPanel::Slot(2, 0)[Button(LOCTEXT("Close", "Cerrar sesión"), TREK_HOST_CLOSE)]
                        ]
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 4)
                        [
                            SNew(STextBlock).Text(LOCTEXT("Campaign", "ID de campaña local para recuperar"))
                        ]
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 8)
                        [
                            SAssignNew(Campaign, SEditableTextBox).Tag(TEXT("H06_Campaign"))
                            .Text(this, &SHostDiagnostic::CampaignText)
                            .OnTextChanged_Lambda([this](const FText& Value) { CampaignOverride = Value; })
                        ]
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 4)
                        [
                            SNew(STextBlock).Text(LOCTEXT("Slot", "Ranura"))
                        ]
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 8)
                        [
                            SAssignNew(Slot, SEditableTextBox).Tag(TEXT("H06_Slot")).Text(LOCTEXT("DefaultSlot", "principal"))
                        ]
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 12)
                        [
                            SNew(SUniformGridPanel).SlotPadding(3)
                            + SUniformGridPanel::Slot(0, 0)[Button(LOCTEXT("Save", "Guardar"), TREK_HOST_SAVE)]
                            + SUniformGridPanel::Slot(1, 0)[Button(LOCTEXT("Restore", "Recuperar"), TREK_HOST_RESTORE)]
                        ]
                        + SVerticalBox::Slot().AutoHeight()
                        [
                            SNew(STextBlock).Text(this, &SHostDiagnostic::ResultText).AutoWrapText(true)
                        ]
                    ]
                ]
            ]
        ];
    }

private:
    TSharedRef<SWidget> Button(const FText& Label, uint32 Operation)
    {
        TSharedRef<SButton> Widget = SNew(SButton).Text(Label)
            .IsEnabled_Lambda([this, Operation]()
            {
                const UHostSessionSubsystem* Session = Host.Get();
                if (!Session || !Session->IsAvailable() || !Projection.IsValid()) return false;
                if (Operation == TREK_HOST_CLOSE) return Session->IsTransitioning() ||
                    Session->GetStatus().state != TREK_HOST_CLOSED;
                if (Session->IsTransitioning()) return false;
                if (Operation == TREK_HOST_OPEN) return Session->GetStatus().state == TREK_HOST_CLOSED;
                if (Operation == TREK_HOST_RESTORE) return Session->GetStatus().state == TREK_HOST_CLOSED ||
                    Session->GetStatus().state == TREK_HOST_ACTIVE;
                return Session->GetStatus().state == TREK_HOST_ACTIVE;
            })
            .OnClicked(this, &SHostDiagnostic::Act, Operation);
        Widget->SetTag(FName(*FString::Printf(TEXT("H06_%u"), Operation)));
        return Widget;
    }

    FReply Act(uint32 Operation)
    {
        UHostSessionSubsystem* Session = Host.Get();
        UHostWorldProjection* World = Projection.Get();
        if (Session && World)
        {
            switch (Operation)
            {
            case TREK_HOST_OPEN: Session->Open(*World); break;
            case TREK_HOST_CLOSE: Session->Close(*World); break;
            case TREK_HOST_QUERY_VIEW: Session->Query(*World); break;
            case TREK_HOST_SAVE: Session->Save(*World, Slot->GetText().ToString()); break;
            case TREK_HOST_RESTORE: Session->Restore(*World, Campaign->GetText().ToString(), Slot->GetText().ToString()); break;
            }
        }
        return FReply::Handled();
    }

    FText CampaignText() const
    {
        if (CampaignOverride.IsSet()) return CampaignOverride.GetValue();
        if (const UHostSessionSubsystem* Session = Host.Get()) return FText::FromString(Session->GetCampaignAddress());
        return FText::GetEmpty();
    }

    FText StatusText() const
    {
        const UHostSessionSubsystem* Session = Host.Get();
        if (!Session || !Session->IsAvailable()) return LOCTEXT("Unavailable", "HOST no disponible");
        const TrekHostStatus& Status = Session->GetStatus();
        return FText::FromString(FString::Printf(
            TEXT("Sesión %s | Generación %llu\nIdentidad %s | F11 %s\nÓrdenes de jugador pendientes de bootstrap H03"),
            HostStateName(Status.state), Status.generation, HostCodeName(Status.principal),
            HostCodeName(Status.institutional)));
    }

    FText ResultText() const
    {
        const UHostWorldProjection* World = Projection.Get();
        if (!World) return FText::GetEmpty();
        FString Result = World->GetMessage();
        if (const TOptional<TrekHostCampaignView>& View = World->GetCampaignView(); View.IsSet())
        {
            Result += FString::Printf(TEXT("\nPersona %llu | Nave %llu | Tick %llu | Revisión %llu"),
                                     View->person, View->ship, View->tick, View->revision);
        }
        return FText::FromString(Result);
    }

    TWeakObjectPtr<UHostSessionSubsystem> Host;
    TWeakObjectPtr<UHostWorldProjection> Projection;
    TSharedPtr<SEditableTextBox> Campaign;
    TSharedPtr<SEditableTextBox> Slot;
    TOptional<FText> CampaignOverride;
};
}

AHostDiagnosticGameMode::AHostDiagnosticGameMode()
{
    PlayerControllerClass = AHostDiagnosticPlayerController::StaticClass();
    DefaultPawnClass = nullptr;
    // Keep the engine HUD class so ClientSetHUD has a valid class during travel.
}

void AHostDiagnosticGameMode::HandleStartingNewPlayer_Implementation(APlayerController*)
{
    // The diagnostic is a local panel and requires no pawn.
}

void AHostDiagnosticPlayerController::BeginPlay()
{
    Super::BeginPlay();
    ULocalPlayer* LocalPlayer = GetLocalPlayer();
    UGameViewportClient* Viewport = LocalPlayer ? LocalPlayer->ViewportClient : nullptr;
    UWorld* World = GetWorld();
    if (!Viewport || !World)
    {
        return;
    }
    UGameInstance* Game = World->GetGameInstance();
    UHostSessionSubsystem* Host = Game ? Game->GetSubsystem<UHostSessionSubsystem>() : nullptr;
    UHostWorldProjection* Projection = World->GetSubsystem<UHostWorldProjection>();
    Panel = SNew(SHostDiagnostic).Host(Host).Projection(Projection);
    PanelViewport = Viewport;
    Viewport->AddViewportWidgetForPlayer(LocalPlayer, Panel.ToSharedRef(), 10);
    bShowMouseCursor = true;
    FInputModeGameAndUI Input;
    Input.SetHideCursorDuringCapture(false);
    SetInputMode(Input);
}

void AHostDiagnosticPlayerController::EndPlay(const EEndPlayReason::Type Reason)
{
    if (UGameViewportClient* Viewport = PanelViewport.Get(); Viewport && Panel)
    {
        if (ULocalPlayer* LocalPlayer = GetLocalPlayer())
        {
            Viewport->RemoveViewportWidgetForPlayer(LocalPlayer, Panel.ToSharedRef());
        }
    }
    Panel.Reset();
    Super::EndPlay(Reason);
}

#undef LOCTEXT_NAMESPACE
