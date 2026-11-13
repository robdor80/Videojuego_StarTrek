#pragma once

#include "GameFramework/GameModeBase.h"
#include "GameFramework/PlayerController.h"
#include "HostDiagnosticGameMode.generated.h"

class SWidget;
class UGameViewportClient;

UCLASS()
class AHostDiagnosticPlayerController final : public APlayerController
{
    GENERATED_BODY()

public:
#if WITH_DEV_AUTOMATION_TESTS
    TSharedPtr<SWidget> GetDiagnosticPanel() const { return Panel; }
#endif

protected:
    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type Reason) override;

private:
    TWeakObjectPtr<UGameViewportClient> PanelViewport;
    TSharedPtr<SWidget> Panel;
};

UCLASS()
class AHostDiagnosticGameMode final : public AGameModeBase
{
    GENERATED_BODY()

public:
    AHostDiagnosticGameMode();

protected:
    virtual void HandleStartingNewPlayer_Implementation(APlayerController* NewPlayer) override;
};
