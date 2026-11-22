#pragma once

#include "Widgets/Children.h"
#include "Widgets/SWidget.h"

inline TSharedPtr<SWidget> FindHostWidget(const TSharedRef<SWidget>& Root, FName Tag)
{
    if (Root->GetTag() == Tag) return Root;
    if (FChildren* Children = Root->GetChildren())
    {
        for (int32 Index = 0; Index < Children->Num(); ++Index)
        {
            if (TSharedPtr<SWidget> Found = FindHostWidget(Children->GetChildAt(Index), Tag))
            {
                return Found;
            }
        }
    }
    return nullptr;
}
