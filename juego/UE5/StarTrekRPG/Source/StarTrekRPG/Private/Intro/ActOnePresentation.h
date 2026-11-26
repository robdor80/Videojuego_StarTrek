#pragma once

#include "CoreMinimal.h"
#include "Styling/SlateBrush.h"

class SWidget;
class STextBlock;
class SConstraintCanvas;
class UActOneTimeline;
class UTexture2D;

class FActOnePresentation
{
public:
    explicit FActOnePresentation(const UActOneTimeline& Timeline);
    void Render(double Time);

    TSharedPtr<SWidget> Widget;

private:
    struct FImage
    {
        double Start = 0;
        double End = 0;
        TSharedPtr<SWidget> Widget;
        FSlateBrush Brush;
    };

    void AddImage(SConstraintCanvas& Canvas, UTexture2D& Texture,
        const FVector2D& Position, const FVector2D& Size, double Start, double End, bool bPortraitSlot);
    static void SetOpacity(const TSharedPtr<SWidget>& Element, float Opacity);

    const UActOneTimeline& Timeline;
    TArray<TUniquePtr<FImage>> Images;
    TSharedPtr<SWidget> OpeningText;
    TSharedPtr<SWidget> CouncilText;
    TSharedPtr<SWidget> OpeningShade;
    TSharedPtr<SWidget> FinalShade;
    TSharedPtr<STextBlock> Name[2];
    TSharedPtr<STextBlock> Dialogue[3];
    FString DisplayedName[2];
    FString DisplayedText[3];
};
