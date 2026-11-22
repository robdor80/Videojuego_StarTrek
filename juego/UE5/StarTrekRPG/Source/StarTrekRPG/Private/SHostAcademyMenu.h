#pragma once

#include "HostAcademyMenu.h"
#include "Widgets/SCompoundWidget.h"
#include "Widgets/Views/SListView.h"

class SBox;
class SEditableTextBox;
class SVerticalBox;

class SHostAcademyMenu final : public SCompoundWidget
{
public:
    SLATE_BEGIN_ARGS(SHostAcademyMenu) {}
        SLATE_ARGUMENT(TSharedPtr<FHostAcademyMenu>, Menu)
    SLATE_END_ARGS()

    void Construct(const FArguments& Args);
    void Refresh();
    virtual bool SupportsKeyboardFocus() const override { return true; }
    virtual FReply OnPreviewKeyDown(const FGeometry& Geometry, const FKeyEvent& Event) override;

private:
    enum class EAction
    {
        New, Browse, Back, Create, ResetCreate, Reload, More, Restore, Verify, Save, SaveClose, Close, Exit,
        Confirm, Cancel
    };

    void BuildMain(SVerticalBox& Body);
    void BuildName(SVerticalBox& Body);
    void BuildCatalog(SVerticalBox& Body);
    void BuildCandidate(SVerticalBox& Body);
    void BuildRecovery(SVerticalBox& Body);
    void BuildConfirmation(SVerticalBox& Body);
    TSharedRef<SWidget> Button(EAction Action, FName Tag, const FText& Label);
    bool IsActionEnabled(EAction Action) const;
    FReply Act(EAction Action);
    FText HostText() const;
    FText MessageText() const;
    FText SaveText() const;
    FText CatalogText() const;
    TSharedRef<ITableRow> GenerateRow(TSharedPtr<FHostAcademySlot> Row, const TSharedRef<STableViewBase>& List);
    void SelectRow(TSharedPtr<FHostAcademySlot> Row, ESelectInfo::Type SelectInfo);

    TSharedPtr<FHostAcademyMenu> Menu;
    TSharedPtr<SBox> Content;
    TSharedPtr<SEditableTextBox> NameField;
    TSharedPtr<SWidget> FocusTarget;
    EAcademyScreen Screen = EAcademyScreen::Main;
    uint32 LayoutRevision = 0;
    bool bNeedsLayout = true;
};
