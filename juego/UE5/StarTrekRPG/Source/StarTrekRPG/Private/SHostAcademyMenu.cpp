#include "SHostAcademyMenu.h"

#include "Framework/Application/SlateApplication.h"
#include "HostRuntime.h"
#include "Input/Events.h"
#include "InputCoreTypes.h"
#include "Styling/CoreStyle.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SEditableTextBox.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Layout/SExpandableArea.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/SOverlay.h"
#include "Widgets/Text/STextBlock.h"
#include "Widgets/Views/STableRow.h"

#define LOCTEXT_NAMESPACE "HostAcademyMenu"

namespace
{
const FLinearColor Backdrop(0.008f, 0.015f, 0.027f);
const FLinearColor Surface(0.018f, 0.034f, 0.055f);
const FLinearColor Accent(0.34f, 0.81f, 0.96f);

TSharedRef<STextBlock> Heading(const FText& Text, int32 Size)
{
    return SNew(STextBlock).Text(Text).Font(FCoreStyle::GetDefaultFontStyle("Bold", Size))
        .ColorAndOpacity(FSlateColor(Accent)).AutoWrapText(true);
}

TSharedRef<STextBlock> Paragraph(const FText& Text)
{
    return SNew(STextBlock).Text(Text).AutoWrapText(true);
}

FText CodeText(TrekHostCode Code)
{
    return FText::FromString(HostCodeName(Code));
}

FText OperationText(EAcademyOperation Operation)
{
    switch (Operation)
    {
    case EAcademyOperation::Create: return LOCTEXT("Creating", "Creando la candidatura…");
    case EAcademyOperation::VerifyNew:
    case EAcademyOperation::VerifyRestore:
    case EAcademyOperation::VerifyWorld: return LOCTEXT("Verifying", "Verificando la candidatura en el HOST…");
    case EAcademyOperation::FirstSave: return LOCTEXT("InitialSave", "Candidatura creada. Esperando el primer guardado en «principal»…");
    case EAcademyOperation::List: return LOCTEXT("Listing", "Consultando las partidas guardadas…");
    case EAcademyOperation::Restore: return LOCTEXT("Restoring", "Recuperando la versión seleccionada…");
    case EAcademyOperation::Save:
    case EAcademyOperation::SaveAndClose: return LOCTEXT("Saving", "Esperando la confirmación del guardado…");
    case EAcademyOperation::Close:
    case EAcademyOperation::ExitClose:
    case EAcademyOperation::ResetCreate: return LOCTEXT("Closing", "Esperando a que el HOST confirme el cierre…");
    default: return FText::GetEmpty();
    }
}

FText FailureText(TrekHostCode Code, EAcademyOperation Operation)
{
    switch (Code)
    {
    case TREK_HOST_INVALID_ARGUMENT:
        return Operation == EAcademyOperation::Create
            ? LOCTEXT("InvalidName", "El nombre no es válido. Revísalo y comprueba el límite de 96 bytes en UTF-8.")
            : LOCTEXT("InvalidRequest", "El HOST ha rechazado los datos de la solicitud.");
    case TREK_HOST_SERVICE_UNAVAILABLE:
        return LOCTEXT("Unavailable", "No se puede acceder al HOST de Academia. Comprueba las bibliotecas del juego.");
    case TREK_HOST_ABI_MISMATCH:
        return LOCTEXT("AbiMismatch", "La versión de las bibliotecas del HOST no es compatible con el juego.");
    case TREK_HOST_BUSY_STATE:
        return LOCTEXT("Busy", "El estado de la sesión impide completar la operación. Comprueba el estado y vuelve a intentarlo.");
    case TREK_HOST_RETRY:
        return LOCTEXT("Retry", "El HOST está ocupado. Vuelve a intentarlo.");
    case TREK_HOST_CAPACITY_LIMIT:
        return LOCTEXT("Capacity", "El HOST ha alcanzado su límite para esta operación. Vuelve a intentarlo.");
    case TREK_HOST_GENERATION_EXPIRED:
        return Operation == EAcademyOperation::List || Operation == EAcademyOperation::Restore
            ? LOCTEXT("ListExpired", "El listado ha caducado. Vuelve a cargar las partidas.")
            : LOCTEXT("SessionExpired", "La sesión ha cambiado. Comprueba la candidatura o vuelve al menú.");
    case TREK_HOST_IDEMPOTENCY_CONFLICT:
        return LOCTEXT("ConflictingName", "Hay un intento de creación abierto. Usa el mismo nombre o cierra el intento antes de cambiarlo.");
    case TREK_HOST_SAVE_CORRUPT:
        return LOCTEXT("Corrupt", "La versión guardada está dañada.");
    case TREK_HOST_SAVE_INCOMPATIBLE:
        return LOCTEXT("Incompatible", "La versión guardada no es compatible.");
    case TREK_HOST_SAVE_UNTRUSTED:
        return LOCTEXT("Untrusted", "H04 no ha podido verificar la procedencia de esta versión.");
    case TREK_HOST_PUBLICATION_UNCERTAIN:
        return LOCTEXT("PublicationUncertain", "H04 no ha confirmado la publicación. Comprueba las versiones de la partida en Continuar antes de guardar de nuevo.");
    case TREK_HOST_PERSISTENCE_FAILED:
        return LOCTEXT("PersistenceFailed", "H04 no ha podido completar el guardado.");
    case TREK_HOST_PRINCIPAL_UNBOUND:
    case TREK_HOST_IDENTITY_MISMATCH:
    case TREK_HOST_SCOPE_INVALID:
        return LOCTEXT("Unverified", "No se ha podido verificar la identidad o el vínculo de la candidatura con el HOST.");
    case TREK_HOST_SESSION_CLOSED:
        return LOCTEXT("SessionClosed", "La sesión está cerrada.");
    default:
        return LOCTEXT("OperationFailed", "El HOST no ha podido completar la operación.");
    }
}

FText SlotState(const FHostAcademySlot& Row)
{
    if (Row.bRecoverable && Row.bCompatible && Row.Reason == TREK_HOST_OK) return LOCTEXT("Recoverable", "Recuperable");
    if (Row.Reason == TREK_HOST_SAVE_CORRUPT) return LOCTEXT("CorruptRow", "Dañada · no recuperable");
    if (Row.Reason == TREK_HOST_SAVE_INCOMPATIBLE || !Row.bCompatible)
        return LOCTEXT("IncompatibleRow", "Incompatible · no recuperable");
    return LOCTEXT("BlockedRow", "No recuperable");
}

FText SlotDescription(const FHostAcademySlot& Row)
{
    return FText::Format(LOCTEXT("SlotDescription", "Partida {0}…  |  Ranura {1}  |  Versión {2}"),
        FText::FromString(Row.Campaign.Left(8)), FText::FromString(Row.Slot), FText::AsNumber(Row.Version));
}

FText SlotProvenance(uint32 Value)
{
    switch (Value)
    {
    case TREK_HOST_CREATED_LOCALLY: return LOCTEXT("CreatedLocally", "Creada en este equipo");
    case TREK_HOST_KNOWN_LOCAL: return LOCTEXT("KnownLocal", "Local conocida");
    case TREK_HOST_IMPORTED_UNVERIFIED: return LOCTEXT("Imported", "Importada sin verificar");
    case TREK_HOST_REJECTED: return LOCTEXT("Rejected", "Rechazada");
    default: return LOCTEXT("Unknown", "Desconocida");
    }
}
}

void SHostAcademyMenu::Construct(const FArguments& Args)
{
    Menu = Args._Menu;
    ChildSlot
    [
        SNew(SBorder).BorderImage(FCoreStyle::Get().GetBrush("WhiteBrush")).BorderBackgroundColor(Backdrop)
        [
            SNew(SOverlay)
            + SOverlay::Slot().HAlign(HAlign_Center).VAlign(VAlign_Fill).Padding(20)
            [
                SNew(SBox).WidthOverride(856)
                [
                    SNew(SBorder).Padding(24).BorderImage(FCoreStyle::Get().GetBrush("WhiteBrush")).BorderBackgroundColor(Surface)
                    [
                        SNew(SVerticalBox)
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 6)
                        [ Heading(LOCTEXT("Title", "STAR TREK LEGENDS — ACADEMIA"), 30) ]
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 0, 0, 22)
                        [ SNew(STextBlock).Tag(TEXT("AcademyHost")).Text(this, &SHostAcademyMenu::HostText).AutoWrapText(true) ]
                        + SVerticalBox::Slot().FillHeight(1.0f)
                        [ SAssignNew(Content, SBox) ]
                        + SVerticalBox::Slot().AutoHeight().Padding(0, 14, 0, 0)
                        [ SNew(STextBlock).Tag(TEXT("AcademyMessage")).Text(this, &SHostAcademyMenu::MessageText).AutoWrapText(true) ]
                    ]
                ]
            ]
        ]
    ];
    Refresh();
}

void SHostAcademyMenu::Refresh()
{
    if (!bNeedsLayout && Screen == Menu->GetFlow().Screen() && LayoutRevision == Menu->GetLayoutRevision())
    {
        if (FocusTarget && FocusTarget->IsEnabled() && FSlateApplication::IsInitialized() &&
            FSlateApplication::Get().SetKeyboardFocus(FocusTarget, EFocusCause::SetDirectly))
        {
            FocusTarget.Reset();
        }
        return;
    }

    bNeedsLayout = false;
    Screen = Menu->GetFlow().Screen();
    LayoutRevision = Menu->GetLayoutRevision();
    NameField.Reset();
    FocusTarget.Reset();
    TSharedRef<SVerticalBox> Body = SNew(SVerticalBox);
    if (Menu->GetConfirmation() != EAcademyConfirmation::None)
    {
        BuildConfirmation(*Body);
    }
    else
    {
        switch (Screen)
        {
        case EAcademyScreen::Main: BuildMain(*Body); break;
        case EAcademyScreen::Name: BuildName(*Body); break;
        case EAcademyScreen::Catalog: BuildCatalog(*Body); break;
        case EAcademyScreen::Candidate: BuildCandidate(*Body); break;
        case EAcademyScreen::Recovery: BuildRecovery(*Body); break;
        }
    }
    Content->SetContent(Body);
}

void SHostAcademyMenu::BuildMain(SVerticalBox& Body)
{
    FocusTarget = Button(EAction::New, TEXT("AcademyNew"), LOCTEXT("NewGame", "Nueva partida"));
    Body.AddSlot().AutoHeight().HAlign(HAlign_Left).Padding(0, 0, 0, 10)[ FocusTarget.ToSharedRef() ];
    Body.AddSlot().AutoHeight().HAlign(HAlign_Left).Padding(0, 0, 0, 10)
    [ Button(EAction::Browse, TEXT("AcademyBrowse"), LOCTEXT("Continue", "Continuar")) ];
    const auto Exit = Button(EAction::Exit, TEXT("AcademyExit"), LOCTEXT("Exit", "Salir"));
    Body.AddSlot().AutoHeight().HAlign(HAlign_Left)[ Exit ];
    if (!Menu->IsReadyClosed()) FocusTarget = Exit;
}

void SHostAcademyMenu::BuildName(SVerticalBox& Body)
{
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 12)[ Heading(LOCTEXT("NewTitle", "Nueva partida"), 23) ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 14)
    [ Paragraph(LOCTEXT("FixedProtagonist", "Tu protagonista está definido por la historia. Puedes elegir su nombre.")) ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 5)
    [ Paragraph(LOCTEXT("NameLabel", "Nombre del personaje")) ];
    Body.AddSlot().AutoHeight().HAlign(HAlign_Left).Padding(0, 0, 0, 6)
    [
        SNew(SBox).WidthOverride(450)
        [
            SAssignNew(NameField, SEditableTextBox).Tag(TEXT("AcademyName"))
            .Text(FText::FromString(Menu->GetName()))
            .ToolTipText(LOCTEXT("NameTooltip", "Nombre del personaje. Máximo 96 bytes en UTF-8."))
            .IsEnabled_Lambda([this]() { return Menu->IsReadyClosed(); })
            .OnTextChanged_Lambda([this](const FText& Text) { Menu->EditName(Text.ToString()); })
            .OnTextCommitted_Lambda([this](const FText& Text, ETextCommit::Type Commit)
            {
                if (Commit == ETextCommit::OnEnter) Menu->Create(Text.ToString());
            })
        ]
    ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 15)[ Paragraph(LOCTEXT("NameLimit", "Máximo 96 bytes en UTF-8.")) ];
    Body.AddSlot().AutoHeight()
    [
        SNew(SHorizontalBox)
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)
        [ Button(EAction::Create, TEXT("AcademyCreate"), LOCTEXT("Create", "Crear candidatura")) ]
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)
        [ Button(EAction::Back, TEXT("AcademyBack"), LOCTEXT("Back", "Volver")) ]
        + SHorizontalBox::Slot().AutoWidth()
        [
            SNew(SBox).Visibility_Lambda([this]()
            {
                return Menu->CanResetCreate() ? EVisibility::Visible : EVisibility::Collapsed;
            })
            [ Button(EAction::ResetCreate, TEXT("AcademyResetCreate"), LOCTEXT("ResetCreate", "Cerrar intento")) ]
        ]
    ];
    FocusTarget = NameField;
}

void SHostAcademyMenu::BuildCatalog(SVerticalBox& Body)
{
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 12)
    [ Heading(LOCTEXT("ContinueTitle", "Continuar — Partidas de Academia"), 23) ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 8)
    [ SNew(STextBlock).Tag(TEXT("AcademyCatalogState")).Text(this, &SHostAcademyMenu::CatalogText).AutoWrapText(true) ];

    TSharedPtr<SListView<TSharedPtr<FHostAcademySlot>>> List;
    Body.AddSlot().FillHeight(1.0f).Padding(0, 0, 0, 12)
    [
        SAssignNew(List, SListView<TSharedPtr<FHostAcademySlot>>).Tag(TEXT("AcademyVersions"))
        .ListItemsSource(&Menu->GetRows())
        .SelectionMode(ESelectionMode::Single)
        .OnGenerateRow(this, &SHostAcademyMenu::GenerateRow)
        .OnSelectionChanged(this, &SHostAcademyMenu::SelectRow)
        .IsEnabled_Lambda([this]() { return Menu->IsReadyClosed(); })
    ];
    if (Menu->GetSelected())
    {
        List->SetSelection(Menu->GetSelected());
        List->RequestScrollIntoView(Menu->GetSelected());
    }

    const auto More = Button(EAction::More, TEXT("AcademyMore"), LOCTEXT("More", "Cargar más"));
    const auto Reload = Button(EAction::Reload, TEXT("AcademyReload"), LOCTEXT("Reload", "Empezar listado"));
    Body.AddSlot().AutoHeight()
    [
        SNew(SHorizontalBox)
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)
        [ Button(EAction::Restore, TEXT("AcademyRestore"), LOCTEXT("Restore", "Recuperar versión seleccionada")) ]
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)
        [ More ]
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)
        [ Reload ]
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)
        [ Button(EAction::Back, TEXT("AcademyBack"), LOCTEXT("Back", "Volver")) ]
        + SHorizontalBox::Slot().AutoWidth()
        [
            SNew(SBox).Visibility_Lambda([this]()
            {
                return Menu->IsCatalogEmpty() && !Menu->IsBusy() ? EVisibility::Visible : EVisibility::Collapsed;
            })
            [ Button(EAction::New, TEXT("AcademyNew"), LOCTEXT("NewGame", "Nueva partida")) ]
        ]
    ];
    if (!Menu->GetRows().IsEmpty()) FocusTarget = List;
    else FocusTarget = Menu->CanLoadMore() ? More : Reload;
}

TSharedRef<ITableRow> SHostAcademyMenu::GenerateRow(TSharedPtr<FHostAcademySlot> Row, const TSharedRef<STableViewBase>& List)
{
    const FText Detail = FText::Format(LOCTEXT("SlotTooltip", "Campaña {0}\nFormato H04 {1} · {2}\n{3} ({4})"),
        FText::FromString(Row->Campaign), FText::AsNumber(Row->Format), SlotProvenance(Row->Provenance),
        Row->Reason == TREK_HOST_OK ? SlotState(*Row) : FailureText(Row->Reason, EAcademyOperation::Restore), CodeText(Row->Reason));
    return SNew(STableRow<TSharedPtr<FHostAcademySlot>>, List).ToolTipText(Detail).Padding(7)
    [
        Paragraph(FText::Format(LOCTEXT("SlotRow", "{0}  |  {1}"), SlotDescription(*Row), SlotState(*Row)))
    ];
}

void SHostAcademyMenu::SelectRow(TSharedPtr<FHostAcademySlot> Row, ESelectInfo::Type)
{
    Menu->Select(Row);
}

void SHostAcademyMenu::BuildCandidate(SVerticalBox& Body)
{
    const auto& Candidate = Menu->GetCandidate();
    if (!Candidate.IsSet())
    {
        BuildRecovery(Body);
        return;
    }

    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 12)
    [ Heading(LOCTEXT("CandidateTitle", "Expediente de candidatura"), 23) ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 8)
    [ Heading(FText::FromString(Candidate->DisplayName), 21) ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 6)
    [ SNew(STextBlock).Tag(TEXT("AcademyCandidateState")).Text(LOCTEXT("CandidateState", "Estado · Candidato")) ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 12)
    [ Paragraph(FText::Format(LOCTEXT("Campaign", "Campaña · {0}"), FText::FromString(Candidate->Campaign))) ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 16)
    [ SNew(STextBlock).Tag(TEXT("AcademySaveState")).Text(this, &SHostAcademyMenu::SaveText).AutoWrapText(true) ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 16)
    [
        SNew(SExpandableArea).InitiallyCollapsed(true)
        .HeaderContent()[ Paragraph(LOCTEXT("Details", "Detalles técnicos de CoreRPG")) ]
        .BodyContent()
        [
            Paragraph(FText::Format(LOCTEXT("Identity", "PERSON {0} · Hecho de creación {1}\nRevisión {2} · Tick {3}\nHuella de origen {4}"),
                FText::AsNumber(Candidate->Person), FText::AsNumber(Candidate->CreationFact),
                FText::AsNumber(Candidate->Revision), FText::AsNumber(Candidate->Tick), FText::FromString(Candidate->SourceDigest)))
        ]
    ];
    const FText SaveLabel = Menu->GetFlow().SaveState() == EAcademySave::Failed
        ? LOCTEXT("RetrySave", "Reintentar guardar") : LOCTEXT("Save", "Guardar");
    const auto Save = Button(EAction::Save, TEXT("AcademySave"), SaveLabel);
    const auto Close = Button(EAction::Close, TEXT("AcademyClose"), LOCTEXT("Close", "Cerrar partida"));
    FocusTarget = Menu->CanSave() ? Save : Close;
    Body.AddSlot().AutoHeight()
    [
        SNew(SHorizontalBox)
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)[ Save ]
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)
        [ Button(EAction::SaveClose, TEXT("AcademySaveClose"), LOCTEXT("SaveClose", "Guardar y cerrar")) ]
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)
        [ Close ]
        + SHorizontalBox::Slot().AutoWidth()
        [ Button(EAction::Exit, TEXT("AcademyExit"), LOCTEXT("ExitGame", "Salir del juego")) ]
    ];
}

void SHostAcademyMenu::BuildRecovery(SVerticalBox& Body)
{
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 12)[ Heading(LOCTEXT("Verification", "Verificación de la candidatura"), 23) ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 12)
    [
        SNew(STextBlock).AutoWrapText(true).Visibility_Lambda([this]()
        {
            return Menu->GetFlow().Busy() ? EVisibility::Collapsed : EVisibility::Visible;
        }).Text(LOCTEXT("NoVerifiedCandidate", "La ficha estará disponible cuando el HOST confirme la candidatura."))
    ];
    FocusTarget = Button(EAction::Verify, TEXT("AcademyVerify"), LOCTEXT("VerifyAgain", "Volver a verificar"));
    Body.AddSlot().AutoHeight()
    [
        SNew(SHorizontalBox)
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)[ FocusTarget.ToSharedRef() ]
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)
        [ Button(EAction::Close, TEXT("AcademyClose"), LOCTEXT("Close", "Cerrar partida")) ]
        + SHorizontalBox::Slot().AutoWidth()
        [ Button(EAction::Exit, TEXT("AcademyExit"), LOCTEXT("ExitGame", "Salir del juego")) ]
    ];
}

void SHostAcademyMenu::BuildConfirmation(SVerticalBox& Body)
{
    const auto Choice = Menu->GetConfirmation();
    const bool bRestore = Choice == EAcademyConfirmation::Restore;
    FText Question = LOCTEXT("CloseWarning", "Se perderá el progreso desde el último guardado confirmado. ¿Quieres cerrar la partida?");
    FText Label = LOCTEXT("CloseWithoutSave", "Cerrar sin guardar");
    if (bRestore && Menu->GetSelected())
    {
        const auto& Row = *Menu->GetSelected();
        Question = FText::Format(LOCTEXT("RestoreQuestion", "¿Recuperar la versión {0} de la ranura «{1}» de la partida {2}…?"),
            FText::AsNumber(Row.Version), FText::FromString(Row.Slot), FText::FromString(Row.Campaign.Left(8)));
        Label = LOCTEXT("ConfirmRestore", "Recuperar versión");
    }
    else if (Choice == EAcademyConfirmation::Exit)
    {
        Question = LOCTEXT("ExitWarning", "Se perderá el progreso desde el último guardado confirmado. ¿Quieres salir del juego?");
        Label = LOCTEXT("ExitWithoutSave", "Salir sin guardar");
    }
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 12)
    [ Heading(bRestore ? LOCTEXT("RestoreHeading", "Recuperar partida") : LOCTEXT("CloseHeading", "Confirmar cierre"), 23) ];
    Body.AddSlot().AutoHeight().Padding(0, 0, 0, 16)[ Paragraph(Question) ];
    FocusTarget = Button(EAction::Cancel, TEXT("AcademyCancel"), LOCTEXT("Cancel", "Cancelar"));
    Body.AddSlot().AutoHeight()
    [
        SNew(SHorizontalBox)
        + SHorizontalBox::Slot().AutoWidth().Padding(0, 0, 8, 0)[ FocusTarget.ToSharedRef() ]
        + SHorizontalBox::Slot().AutoWidth()[ Button(EAction::Confirm, TEXT("AcademyConfirm"), Label) ]
    ];
}

TSharedRef<SWidget> SHostAcademyMenu::Button(EAction Action, FName Tag, const FText& Label)
{
    return SNew(SButton).Tag(Tag).Text(Label).ContentPadding(FMargin(12, 8))
        .IsEnabled_Lambda([this, Action]() { return IsActionEnabled(Action); })
        .OnClicked(this, &SHostAcademyMenu::Act, Action);
}

bool SHostAcademyMenu::IsActionEnabled(EAction Action) const
{
    switch (Action)
    {
    case EAction::New:
    case EAction::Browse:
    case EAction::Create:
    case EAction::Reload: return Menu->IsReadyClosed();
    case EAction::Back: return !Menu->IsBusy() && Menu->GetConfirmation() == EAcademyConfirmation::None;
    case EAction::ResetCreate: return Menu->CanResetCreate();
    case EAction::More: return Menu->CanLoadMore();
    case EAction::Restore: return Menu->CanRestore();
    case EAction::Verify: return Menu->CanRetryVerification();
    case EAction::Save:
    case EAction::SaveClose: return Menu->CanSave();
    case EAction::Close: return Menu->CanClose();
    case EAction::Exit: return Menu->CanExit();
    case EAction::Confirm:
    case EAction::Cancel: return Menu->GetConfirmation() != EAcademyConfirmation::None && !Menu->IsBusy();
    }
    return false;
}

FReply SHostAcademyMenu::Act(EAction Action)
{
    if (!IsActionEnabled(Action)) return FReply::Handled();
    switch (Action)
    {
    case EAction::New: Menu->OpenName(); break;
    case EAction::Browse: Menu->OpenCatalog(); break;
    case EAction::Back: Menu->Back(); break;
    case EAction::Create: if (NameField) Menu->Create(NameField->GetText().ToString()); break;
    case EAction::ResetCreate: Menu->ResetCreate(); break;
    case EAction::Reload: Menu->ReloadCatalog(); break;
    case EAction::More: Menu->LoadMore(); break;
    case EAction::Restore: Menu->RequestRestore(); break;
    case EAction::Verify: Menu->RetryVerification(); break;
    case EAction::Save: Menu->Save(false); break;
    case EAction::SaveClose: Menu->Save(true); break;
    case EAction::Close: Menu->RequestClose(false); break;
    case EAction::Exit: Menu->RequestClose(true); break;
    case EAction::Confirm: Menu->Confirm(); break;
    case EAction::Cancel: Menu->CancelConfirmation(); break;
    }
    return FReply::Handled();
}

FReply SHostAcademyMenu::OnPreviewKeyDown(const FGeometry&, const FKeyEvent& Event)
{
    if (Event.GetKey() == EKeys::Escape)
    {
        if (Menu->GetConfirmation() != EAcademyConfirmation::None) return Act(EAction::Cancel);
        if (Screen == EAcademyScreen::Name || Screen == EAcademyScreen::Catalog) return Act(EAction::Back);
    }
    return FReply::Unhandled();
}

FText SHostAcademyMenu::HostText() const
{
    if (Menu->IsInitializing()) return LOCTEXT("Connecting", "Conectando con el HOST…");
    const TrekHostCode Availability = Menu->GetAvailability();
    if (Availability == TREK_HOST_OK) return LOCTEXT("HostReady", "HOST de Academia disponible");
    return FText::Format(LOCTEXT("HostError", "Academia no disponible · {0} ({1})"),
        FailureText(Availability, EAcademyOperation::None), CodeText(Availability));
}

FText SHostAcademyMenu::MessageText() const
{
    const auto& Flow = Menu->GetFlow();
    if (Flow.Busy()) return OperationText(Flow.Operation());
    if (Menu->IsBusy()) return LOCTEXT("HostTransition", "El HOST está cambiando de sesión…");
    if (Flow.Error() == TREK_HOST_OK) return FText::GetEmpty();
    return FText::Format(LOCTEXT("ErrorWithCode", "{0} ({1})"),
        FailureText(Flow.Error(), Flow.LastOperation()), CodeText(Flow.Error()));
}

FText SHostAcademyMenu::SaveText() const
{
    if (IsAcademySave(Menu->GetFlow().Operation())) return LOCTEXT("SavePending", "Guardado pendiente de confirmación");
    switch (Menu->GetFlow().SaveState())
    {
    case EAcademySave::Confirmed: return LOCTEXT("Saved", "Guardado confirmado en «principal»");
    case EAcademySave::Restored: return LOCTEXT("Restored", "Versión guardada recuperada");
    case EAcademySave::Uncertain:
        return LOCTEXT("UnknownSave", "Guardado sin confirmar. Antes de guardar de nuevo, cierra y comprueba las versiones en Continuar.");
    case EAcademySave::Failed:
    case EAcademySave::Unconfirmed: return LOCTEXT("Unsaved", "Candidatura verificada. El progreso actual aún no tiene un guardado confirmado.");
    }
    return FText::GetEmpty();
}

FText SHostAcademyMenu::CatalogText() const
{
    if (Menu->IsBusy()) return FText::GetEmpty();
    if (Menu->IsCatalogExpired()) return LOCTEXT("ReloadCatalog", "Actualiza el listado con «Empezar listado».");
    if (Menu->IsCatalogEmpty()) return LOCTEXT("EmptyCatalog", "No hay candidaturas guardadas.");
    if (const auto& Row = Menu->GetSelected(); Row && Row->Reason != TREK_HOST_OK)
    {
        return FText::Format(LOCTEXT("SelectedSlotError", "{0} ({1})"),
            FailureText(Row->Reason, EAcademyOperation::Restore), CodeText(Row->Reason));
    }
    if (!Menu->GetRows().IsEmpty()) return LOCTEXT("SelectVersion", "Selecciona una versión guardada.");
    if (Menu->CanLoadMore()) return LOCTEXT("EmptyPage", "Esta página no contiene versiones de Academia. Puedes cargar más.");
    if (Menu->GetFlow().Error() == TREK_HOST_OK) return LOCTEXT("EndOfCatalog", "No hay más versiones de Academia en el listado.");
    return FText::GetEmpty();
}

#undef LOCTEXT_NAMESPACE
