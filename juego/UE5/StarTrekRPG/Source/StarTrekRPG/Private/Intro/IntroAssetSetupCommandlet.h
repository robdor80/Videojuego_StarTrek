#pragma once

#include "Commandlets/Commandlet.h"
#include "IntroAssetSetupCommandlet.generated.h"

UCLASS()
class UIntroAssetSetupCommandlet final : public UCommandlet
{
    GENERATED_BODY()

public:
    virtual int32 Main(const FString& Params) override;
};
