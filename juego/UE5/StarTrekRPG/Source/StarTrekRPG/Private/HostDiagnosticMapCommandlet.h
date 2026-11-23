#pragma once

#include "Commandlets/Commandlet.h"
#include "HostDiagnosticMapCommandlet.generated.h"

UCLASS()
class UHostDiagnosticMapCommandlet final : public UCommandlet
{
    GENERATED_BODY()

public:
    virtual int32 Main(const FString& Params) override;
};
