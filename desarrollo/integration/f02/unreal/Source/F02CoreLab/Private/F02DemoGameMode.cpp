#include "F02CampaignSubsystem.h"
#include "Camera/CameraActor.h"
#include "Engine/GameInstance.h"
#include "Engine/PointLight.h"
#include "Components/PointLightComponent.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "GameFramework/PlayerController.h"
#include "HAL/FileManager.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"
#include "UnrealClient.h"
#include "TimerManager.h"

void AF02DemoGameMode::BeginPlay() {
    Super::BeginPlay();
    Host=GetGameInstance()->GetSubsystem<UF02CampaignSubsystem>();
    if (!Host || !Host->OpenLab()) {
        UE_LOG(LogTemp,Error,TEXT("F02 demo: Core unavailable; actions disabled")); return;
    }
    InitialId=Host->DiagnosticId(); Marker=Host->Represent(GetWorld());
    auto* Camera=GetWorld()->SpawnActor<ACameraActor>(FVector(650,0,260),FRotator(-15,180,0));
    if (auto* PC=GetWorld()->GetFirstPlayerController()) PC->SetViewTarget(Camera);
    auto* Light=GetWorld()->SpawnActor<APointLight>(FVector(250,-200,400),FRotator::ZeroRotator);
    Light->PointLightComponent->SetIntensity(100000);
    Light->PointLightComponent->SetAttenuationRadius(2000);
    if (GEngine) GEngine->AddOnScreenDebugMessage(42,-1,FColor::Cyan,
        TEXT("F02 | REAL CoreRPG + UE 5.8.2 | isolated laboratory"));
    GetWorldTimerManager().SetTimer(DemoTimer,this,&AF02DemoGameMode::Advance,2.0f,true);
}
void AF02DemoGameMode::Advance() {
    ++Step; bool Pass=true; FString Message;
    if (Step==1) {
        Pass=Marker && Host->Exists(); if (Marker) Marker->Destroy(); Marker=nullptr;
        Pass &= Host->Exists(); Message=TEXT("Actor destroyed; logical entity still exists");
    } else if (Step==2) {
        Marker=Host->Represent(GetWorld());
        Pass=Marker && Marker->LogicalId==InitialId && Host->Place();
        Message=TEXT("New Actor, same EntityId; real Core action accepted");
    } else if (Step==3) {
        const FString Dir=FPaths::Combine(FPaths::ProjectSavedDir(),TEXT("F02Evidence"));
        IFileManager::Get().MakeDirectory(*Dir,true);
        const FString Path=FPaths::Combine(Dir,FGuid::NewGuid().ToString()+TEXT(".save"));
        Pass=Host->WriteSave(Path) && Host->ReadSave(Path);
        Marker=Host->Represent(GetWorld());
        Pass &= Marker && Marker->LogicalId==InitialId && Host->VerifyProjection();
        Message=TEXT("Disk save/load; identity and authorized projection verified");
    } else if (Step==4) {
        Message=TEXT("F02 demonstration finished | EntityId = ")+InitialId;
        const FString Dir=FPaths::Combine(FPaths::ProjectSavedDir(),TEXT("F02Evidence"));
        IFileManager::Get().MakeDirectory(*Dir,true);
        FScreenshotRequest::RequestScreenshot(FPaths::Combine(Dir,TEXT("F02-Core-UE5.png")),false,false);
    } else if (Step==6) {
        GetWorldTimerManager().ClearTimer(DemoTimer);
        if (FParse::Param(FCommandLine::Get(),TEXT("F02AutoQuit")))
            GetWorld()->GetFirstPlayerController()->ConsoleCommand(TEXT("quit"));
        return;
    } else return;
    UE_LOG(LogTemp,Display,TEXT("F02 DEMO step=%d pass=%d EntityId=%s %s"),Step,Pass,*InitialId,*Message);
    if (!Pass) UE_LOG(LogTemp,Error,TEXT("F02 demonstration assertion failed"));
    if (GEngine) GEngine->AddOnScreenDebugMessage(43,-1,Pass?FColor::Green:FColor::Red,
        (Pass?TEXT("PASS | "):TEXT("FAIL | "))+Message);
}
