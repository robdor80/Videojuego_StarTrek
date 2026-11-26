#include "ActOnePresentation.h"
#include "ActOneTimeline.h"

#include "Engine/Font.h"
#include "Engine/Texture2D.h"
#include "Rendering/DrawElements.h"
#include "Widgets/Images/SImage.h"
#include "Widgets/Layout/SBox.h"
#include "Widgets/Layout/SConstraintCanvas.h"
#include "Widgets/Layout/SScaleBox.h"
#include "Widgets/SLeafWidget.h"
#include "Widgets/Text/STextBlock.h"

namespace
{
    const FVector2D Design(2560, 1600);
    const FLinearColor Pearl(FColor(242, 245, 250));
    const FLinearColor Blue(FColor(158, 200, 245));

    // Fade toward the image at both edges of the upper-left caption area.
    class SCaptionShade : public SLeafWidget
    {
    public:
        SLATE_BEGIN_ARGS(SCaptionShade) : _Lower(false) {}
            SLATE_ARGUMENT(bool, Lower)
        SLATE_END_ARGS()

        void Construct(const FArguments& Args) { bLower = Args._Lower; }
        virtual FVector2D ComputeDesiredSize(float) const override { return FVector2D::ZeroVector; }

        virtual int32 OnPaint(const FPaintArgs&, const FGeometry& Geometry, const FSlateRect&,
            FSlateWindowElementList& Elements, int32 Layer, const FWidgetStyle& Style, bool) const override
        {
            const FVector2f Size(Geometry.GetLocalSize());
            const float Alpha = Style.GetColorAndOpacityTint().A;
            if (bLower)
            {
                const TArray<FSlateGradientStop> Stops = {
                    {FVector2f(0, 0), FLinearColor(0, 0, 0, 0)},
                    {FVector2f(0, Size.Y * 0.55f), FLinearColor(0, 0, 0, Alpha * 0.72f)},
                    {FVector2f(0, Size.Y), FLinearColor(0, 0, 0, Alpha)}};
                FSlateDrawElement::MakeGradient(Elements, Layer, Geometry.ToPaintGeometry(), Stops, Orient_Horizontal);
                return Layer;
            }
            constexpr int32 Bands = 28;
            const float BandHeight = Size.Y / Bands;
            for (int32 Band = 0; Band < Bands; ++Band)
            {
                const float Strength = Alpha * 0.86f * (1.0f - UActOneTimeline::Ramp(Band, 11, 17));
                const TArray<FSlateGradientStop> Stops = {
                    {FVector2f(0, 0), FLinearColor(0, 0, 0, Strength)},
                    {FVector2f(Size.X * 0.65f, 0), FLinearColor(0, 0, 0, Strength)},
                    {FVector2f(Size.X, 0), FLinearColor(0, 0, 0, 0)}};
                FSlateDrawElement::MakeGradient(Elements, Layer,
                    Geometry.ToPaintGeometry(FVector2f(Size.X, BandHeight + 0.5f),
                        FSlateLayoutTransform(FVector2f(0, Band * BandHeight))), Stops, Orient_Vertical);
            }
            return Layer;
        }

    private:
        bool bLower = false;
    };

    void Put(SConstraintCanvas& Canvas, const FVector2D& Position, const FVector2D& Size,
        const TSharedRef<SWidget>& Child)
    {
        Canvas.AddSlot()
            .Anchors(FAnchors(0.0f, 0.0f))
            .Alignment(FVector2D::ZeroVector)
            .Offset(FMargin(Position.X, Position.Y, Size.X, Size.Y))
            [Child];
    }

    TSharedRef<STextBlock> MakeText(UFont& Font, int32 Size, FLinearColor Color,
        const FString& Content = FString(), float Wrap = 0, ETextJustify::Type Justify = ETextJustify::Left)
    {
        return SNew(STextBlock)
            .Font(FSlateFontInfo(&Font, Size))
            .Text(FText::FromString(Content))
            .ColorAndOpacity(FSlateColor(Color))
            .ShadowOffset(FVector2D(2, 3))
            .ShadowColorAndOpacity(FLinearColor(0, 0, 0, 0.88f))
            .WrapTextAt(Wrap)
            .LineHeightPercentage(1.12f)
            .Justification(Justify);
    }
}

FActOnePresentation::FActOnePresentation(const UActOneTimeline& InTimeline) : Timeline(InTimeline)
{
    const TSharedRef<SConstraintCanvas> Canvas = SNew(SConstraintCanvas);
    Widget = SNew(SScaleBox)
        .Stretch(EStretch::ScaleToFit)
        .HAlign(HAlign_Center)
        .VAlign(VAlign_Center)
        [
            SNew(SBox).WidthOverride(Design.X).HeightOverride(Design.Y)
            [Canvas]
        ];
    for (const FActOneShot& Shot : Timeline.Opening)
    {
        AddImage(*Canvas, *Shot.Image, FVector2D::ZeroVector, Design, Shot.Start, Shot.End);
    }
    for (const FActOneIntervention& Line : Timeline.Interventions)
    {
        const bool bPanorama = Line.Layout == EActOneLayout::Panorama;
        const bool bRight = Line.Layout == EActOneLayout::Right;
        const FVector2D Area = bPanorama ? Design : FVector2D(1230, 1470);
        const FVector2D Origin = bPanorama ? FVector2D::ZeroVector : FVector2D(bRight ? 1290 : 40, 65);
        for (const FActOneShot& Shot : Line.Shots)
        {
            AddImage(*Canvas, *Shot.Image, Origin, Area, Shot.Start, bPanorama ? Timeline.End : Shot.End);
        }
    }

    const TSharedRef<SConstraintCanvas> Locations = SNew(SConstraintCanvas);
    UFont& TitleFont = *Timeline.TitleFont;
    UFont& DialogueFont = *Timeline.DialogueFont;
    OpeningShade = SNew(SCaptionShade);
    Put(*Canvas, FVector2D::ZeroVector, FVector2D(1820, 400), OpeningShade.ToSharedRef());
    Put(*Locations, FVector2D(100, 85), FVector2D(1450, 65),
        MakeText(TitleFont, 48, Pearl, TEXT("San Francisco, 2383")));
    Put(*Locations, FVector2D(100, 153), FVector2D(1820, 54),
        MakeText(TitleFont, 34, Blue, TEXT("Cuartel General de la Flota Estelar")));
    CouncilText = MakeText(TitleFont, 38, Pearl, TEXT("Alto Consejo de la Flota"));
    Put(*Locations, FVector2D(100, 210), FVector2D(1450, 58), CouncilText.ToSharedRef());
    OpeningText = Locations;
    Put(*Canvas, FVector2D::ZeroVector, Design, Locations);

    for (int32 Side = 0; Side < 2; ++Side)
    {
        const double X = Side == 0 ? 112 : 1390;
        Name[Side] = MakeText(TitleFont, 47, Blue);
        Dialogue[Side] = MakeText(DialogueFont, 42, Pearl, FString(), 1040);
        Put(*Canvas, FVector2D(X, 565), FVector2D(1050, 66), Name[Side].ToSharedRef());
        Put(*Canvas, FVector2D(X, 650), FVector2D(1050, 390), Dialogue[Side].ToSharedRef());
    }

    FinalShade = SNew(SCaptionShade).Lower(true);
    Put(*Canvas, FVector2D(0, 1230), FVector2D(2560, 370), FinalShade.ToSharedRef());
    Dialogue[2] = MakeText(DialogueFont, 42, Pearl, FString(), 1660, ETextJustify::Center);
    Put(*Canvas, FVector2D(450, 1310), FVector2D(1660, 230),
        SNew(SBox).VAlign(VAlign_Center)[Dialogue[2].ToSharedRef()]);
    Render(0.0);
}

void FActOnePresentation::AddImage(SConstraintCanvas& Canvas, UTexture2D& Texture,
    const FVector2D& Position, const FVector2D& Size, double Start, double End)
{
    FImage& Image = *Images.Add_GetRef(MakeUnique<FImage>());
    Image.Start = Start;
    Image.End = End;
    const FVector2D Native(Texture.GetImportedSize());
    const FVector2D Fit = Native * FMath::Min(Size.X / Native.X, Size.Y / Native.Y);
    Image.Brush.SetResourceObject(&Texture);
    Image.Brush.SetImageSize(Fit);
    Image.Brush.DrawAs = ESlateBrushDrawType::Image;
    Image.Widget = SNew(SImage).Image(&Image.Brush);
    Put(Canvas, Position + (Size - Fit) * 0.5, Fit, Image.Widget.ToSharedRef());
}

void FActOnePresentation::SetOpacity(const TSharedPtr<SWidget>& Element, float Opacity)
{
    Element->SetRenderOpacity(Opacity);
    Element->SetVisibility(Opacity > 0.0f ? EVisibility::HitTestInvisible : EVisibility::Hidden);
}

void FActOnePresentation::Render(double Time)
{
    using T = UActOneTimeline;
    for (const TUniquePtr<FImage>& Image : Images)
    {
        const float Entrance = T::Ramp(Time, Image->Start, T::Fade);
        const float Exit = Image->End == T::End ? T::EndOpacity(Time) : 1.0f - T::Ramp(Time, Image->End, T::Fade);
        SetOpacity(Image->Widget, Entrance * Exit);
    }

    const float LocationOpacity = T::Ramp(Time, 0.1, 0.9) * (1.0f - T::Ramp(Time, 10, T::Fade));
    SetOpacity(OpeningText, LocationOpacity);
    SetOpacity(OpeningShade, LocationOpacity * T::Ramp(Time, 3, T::Fade));
    SetOpacity(CouncilText, T::Ramp(Time, 7.1, 0.45));
    SetOpacity(FinalShade, T::Ramp(Time, 451, T::Fade) * T::EndOpacity(Time));

    const FActOneIntervention* Line = Timeline.FindIntervention(Time);
    for (int32 Side = 0; Side < 3; ++Side)
    {
        const int32 ActiveSide = Line ? static_cast<int32>(Line->Layout) : INDEX_NONE;
        const FActOneCue* Cue = nullptr;
        float Opacity = 0.0f;
        if (ActiveSide == Side)
        {
            Cue = Line->Cues.FindByPredicate([Time](const FActOneCue& Candidate) { return Candidate.Contains(Time); });
            Opacity = T::Ramp(Time, Line->Start, T::Fade);
            if (Side < 2)
            {
                if (DisplayedName[Side] != Line->Speaker)
                {
                    DisplayedName[Side] = Line->Speaker;
                    Name[Side]->SetText(FText::FromString(Line->Speaker));
                }
                Opacity *= 1.0f - T::Ramp(Time, Line->End - 0.2, 0.2);
            }
        }
        if (Side < 2)
        {
            SetOpacity(Name[Side], Opacity);
        }
        if (Cue && DisplayedText[Side] != Cue->Text)
        {
            DisplayedText[Side] = Cue->Text;
            Dialogue[Side]->SetText(FText::FromString(Cue->Text));
        }
        SetOpacity(Dialogue[Side], Cue ? Opacity * T::Ramp(Time, Cue->Start, 0.18) *
            (1.0f - T::Ramp(Time, Cue->End - 0.10, 0.10)) : 0.0f);
    }
}
