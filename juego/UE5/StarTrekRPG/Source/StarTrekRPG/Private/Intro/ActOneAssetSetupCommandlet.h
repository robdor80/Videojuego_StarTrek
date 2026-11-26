#pragma once

#include "Commandlets/Commandlet.h"
#include "ActOneAssetSetupCommandlet.generated.h"

UCLASS()
class UActOneAssetSetupCommandlet final : public UCommandlet
{
    GENERATED_BODY()

public:
    virtual int32 Main(const FString& Params) override;
};
