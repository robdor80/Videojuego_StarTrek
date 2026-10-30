#include "STGameplayProof.h"
#include "STPlayable.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "InputKeyEventArgs.h"
#include "Components/SkeletalMeshComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "UnrealClient.h"
#include "Engine/GameViewportClient.h"
#include "Engine/Engine.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "HAL/IConsoleManager.h"
#include "GameFramework/GameUserSettings.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Camera/CameraComponent.h"
#include "Camera/CameraActor.h"
#include "GameFramework/HUD.h"
ASTGameplayProof::ASTGameplayProof(){PrimaryActorTick.bCanEverTick=true;PrimaryActorTick.TickGroup=TG_PostUpdateWork;}
void ASTGameplayProof::BeginPlay(){Super::BeginPlay();bVisualReference=FParse::Value(FCommandLine::Get(),TEXT("V02ReferenceCapture="),VisualLabel);WallStart=LastWall=FPlatformTime::Seconds();Points={FVector(350,700,92),FVector(-350,700,92),FVector(-425,805,92),FVector(-710,855,92),FVector(-425,805,92),FVector(-350,700,92),FVector(-350,275,92),FVector(0,275,122)};if(auto* Settings=GEngine->GetGameUserSettings()){Settings->SetOverallScalabilityLevel(3);Settings->SetScreenResolution(FIntPoint(2560,1600));Settings->SetFullscreenMode(EWindowMode::Windowed);Settings->SetVSyncEnabled(false);Settings->ApplySettings(false);}float Percent=100;FParse::Value(FCommandLine::Get(),TEXT("SutherlandScreenPercentage="),Percent);IConsoleManager::Get().FindConsoleVariable(TEXT("r.ScreenPercentage"))->Set(FMath::Clamp(Percent,50.f,100.f));bCaptureImages=!FParse::Param(FCommandLine::Get(),TEXT("SutherlandNoScreenshots"));FParse::Value(FCommandLine::Get(),TEXT("SutherlandProofTag="),ProofTag);ProofTag=FPaths::MakeValidFileName(ProofTag);}
void ASTGameplayProof::Key(FName Name,bool Press){if(!Quinn)return;auto* PC=Cast<APlayerController>(Quinn->GetController());if(PC)PC->InputKey(FInputKeyEventArgs::CreateSimulated(FKey(Name),Press?IE_Pressed:IE_Released,Press?1:0));if(Name==TEXT("W"))bWDown=Press;}
void ASTGameplayProof::Capture(const FString& Name){if(bCaptureImages)FScreenshotRequest::RequestScreenshot(FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()/TEXT("../Evidence")/Name),true,false);Events.Add(Name+TEXT(" ")+Quinn->RuntimeState());Write();}
void ASTGameplayProof::Write(bool Complete,const FString& Error){
 auto J=MakeShared<FJsonObject>();J->SetBoolField(TEXT("complete"),Complete);J->SetStringField(TEXT("error"),Error);J->SetStringField(TEXT("method"),TEXT("Standalone -game, real possessed Quinn, simulated player input through PlayerController, live collision/animation/render. No teleport on route."));if(bVisualReference){J->SetStringField(TEXT("method"),TEXT("VISUAL_02 fixed camera reference photos in native Standalone viewport; no route or seating claim. Quinn hidden in memory only for comparison."));J->SetBoolField(TEXT("visual_reference_mode"),true);}J->SetNumberField(TEXT("phase"),Phase);J->SetNumberField(TEXT("elapsed_game_s"),Elapsed);J->SetNumberField(TEXT("elapsed_wall_s"),FPlatformTime::Seconds()-WallStart);
 if(Quinn)J->SetStringField(TEXT("character"),Quinn->RuntimeState());
 UGameViewportClient* C=GEngine?GEngine->GameViewport.Get():nullptr;FIntPoint S=C&&C->Viewport?C->Viewport->GetSizeXY():FIntPoint::ZeroValue;J->SetNumberField(TEXT("viewport_x"),S.X);J->SetNumberField(TEXT("viewport_y"),S.Y);
 TArray<TSharedPtr<FJsonValue>> E;for(auto& X:Events)E.Add(MakeShared<FJsonValueString>(X));J->SetArrayField(TEXT("events"),E);
 TArray<TSharedPtr<FJsonValue>> Times;double Sum=0;for(double Ms:FrameMs){Sum+=Ms;Times.Add(MakeShared<FJsonValueNumber>(Ms));}J->SetArrayField(TEXT("frame_intervals_wall_ms"),Times);J->SetNumberField(TEXT("sample_frames"),FrameMs.Num());if(Sum>0)J->SetNumberField(TEXT("mean_fps"),1000.0*FrameMs.Num()/Sum);
 J->SetBoolField(TEXT("captures_enabled"),bCaptureImages);J->SetStringField(TEXT("run_tag"),ProofTag);J->SetNumberField(TEXT("screen_percentage"),IConsoleManager::Get().FindConsoleVariable(TEXT("r.ScreenPercentage"))->GetFloat());
 J->SetNumberField(TEXT("camera_sphere_samples"),CameraSamples);J->SetNumberField(TEXT("camera_blocked_samples"),CameraBlockedSamples);
 const FString File=ProofTag.IsEmpty()?TEXT("standalone_gameplay.json"):TEXT("standalone_gameplay_")+ProofTag+TEXT(".json");FString Out;FJsonSerializer::Serialize(J,TJsonWriterFactory<>::Create(&Out));FFileHelper::SaveStringToFile(Out,*FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()/TEXT("../Data")/File));
}
void ASTGameplayProof::Tick(float Dt){
 Super::Tick(Dt);Elapsed+=Dt;const double Now=FPlatformTime::Seconds(),WallDt=Now-LastWall;LastWall=Now;
 if(!Quinn)Quinn=Cast<ASTPlayableQuinn>(UGameplayStatics::GetPlayerCharacter(GetWorld(),0));if(!Quinn)return;
 auto* PC=Cast<APlayerController>(Quinn->GetController());if(!PC)return;
 if(bVisualReference){TickVisualReference(PC);return;}
 if(Elapsed>12&&Phase<7){FCollisionQueryParams Query(SCENE_QUERY_STAT(ProofCamera),false,Quinn);const FVector P=Quinn->FollowCamera->GetComponentLocation();CameraSamples++;CameraBlockedSamples+=GetWorld()->OverlapBlockingTestByChannel(P,FQuat::Identity,ECC_Camera,FCollisionShape::MakeSphere(12),Query)?1:0;}
 if(Elapsed>12&&Phase<7&&WallDt>0)FrameMs.Add(WallDt*1000);
 if(Elapsed>150){Key(TEXT("W"),false);Write(false,TEXT("Bounded standalone timeout"));UGameplayStatics::GetPlayerController(this,0)->ConsoleCommand(TEXT("quit"));Phase=99;return;}
 if(Phase==0){if(Elapsed<12)return;Capture(TEXT("Gameplay_01_Quinn_Bridge.png"));Phase=1;Stage=Elapsed;return;}
 if(Phase==1){
  if(bWaitingInCabin){if(Elapsed-CabinWaitStart<3)return;Capture(TEXT("Gameplay_D04_Closed_From_Cabin.png"));bWaitingInCabin=false;Waypoint++;return;}
  FVector D=Points[Waypoint]-Quinn->GetActorLocation();D.Z=0;
  if(D.Size()<25){Key(TEXT("W"),false);Events.Add(FString::Printf(TEXT("Waypoint %d reached %s"),Waypoint,*Quinn->GetActorLocation().ToString()));if(Waypoint==3){bWaitingInCabin=true;CabinWaitStart=Elapsed;PC->SetControlRotation(FRotator(-8,-10,0));Capture(TEXT("Gameplay_D04_Cabin_Entry.png"));return;}Waypoint++;if(Waypoint==Points.Num()){Phase=2;Stage=Elapsed;Capture(TEXT("Gameplay_02_Approach.png"));return;}return;}
  if(Elapsed-Stage>40){Key(TEXT("W"),false);Write(false,TEXT("Walking route physically blocked"));PC->ConsoleCommand(TEXT("quit"));Phase=99;return;}
  PC->SetControlRotation(FRotator(-8,D.Rotation().Yaw,0));Key(TEXT("W"),true);return;
 }
 if(Phase==2){if(Elapsed-Stage<.6)return;Key(TEXT("E"),true);Phase=3;Stage=Elapsed;return;}
 if(Phase==3){
  if(Elapsed-Stage>.15)Key(TEXT("E"),false);
  if(Quinn->SeatPhase==ESTSeatPhase::Sitting&&Elapsed-LastSample>1){LastSample=Elapsed;Capture(TEXT("Gameplay_03_Sitting.png"));}
  if(Quinn->SeatPhase==ESTSeatPhase::Seated){Phase=4;Stage=Elapsed;PC->SetControlRotation(FRotator(-12,45,0));Capture(TEXT("Gameplay_04_Seated.png"));return;}
  if(Elapsed-Stage>15){Write(false,TEXT("Seating did not complete"));PC->ConsoleCommand(TEXT("quit"));Phase=99;}return;
 }
 if(Phase==4){PC->SetControlRotation(FRotator(-12,45+FMath::Sin((Elapsed-Stage)*.8f)*60,0));if(Elapsed-Stage>7){Key(TEXT("E"),true);Phase=5;Stage=Elapsed;}return;}
 if(Phase==5){
  if(Elapsed-Stage>.15)Key(TEXT("E"),false);
  if(Quinn->SeatPhase==ESTSeatPhase::Standing&&Elapsed-LastSample>1){LastSample=Elapsed;Capture(TEXT("Gameplay_05_Standing.png"));}
  if(Quinn->CompletedSitCycles>0){Phase=6;Stage=Elapsed;Capture(TEXT("Gameplay_06_Control_Restored.png"));PC->SetControlRotation(FRotator(-8,90,0));Key(TEXT("W"),true);return;}
  if(Elapsed-Stage>12){Write(false,TEXT("Stand did not complete"));PC->ConsoleCommand(TEXT("quit"));Phase=99;}return;
 }
 if(Phase==6){if(Elapsed-Stage>1){Key(TEXT("W"),false);Capture(TEXT("Gameplay_07_Walking_Again.png"));Phase=7;Stage=Elapsed;}return;}
 if(Phase==7&&Elapsed-Stage>1){Write(true);PC->ConsoleCommand(TEXT("quit"));Phase=99;}
}


void ASTGameplayProof::TickVisualReference(APlayerController* PC){
 if(VisualNames.IsEmpty()){
  FString Source;FFileHelper::LoadFileToString(Source,*FPaths::ConvertRelativePathToFull(FPaths::ProjectDir()/TEXT("../Data/V02_views.json")));TArray<TSharedPtr<FJsonValue>> Rows;
  if(!FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Source),Rows)){Write(false,TEXT("Missing reference view definitions"));PC->ConsoleCommand(TEXT("quit"));return;}
  FString OnlyView;FParse::Value(FCommandLine::Get(),TEXT("V02OnlyView="),OnlyView);for(auto Row:Rows){auto O=Row->AsObject();if(!OnlyView.IsEmpty()&&O->GetStringField(TEXT("name"))!=OnlyView)continue;auto E=O->GetArrayField(TEXT("ue_position_cm"));auto T=O->GetArrayField(TEXT("ue_target_cm"));VisualNames.Add(O->GetStringField(TEXT("name")));VisualEyes.Add(FVector(E[0]->AsNumber(),E[1]->AsNumber(),E[2]->AsNumber()));VisualTargets.Add(FVector(T[0]->AsNumber(),T[1]->AsNumber(),T[2]->AsNumber()));}
  VisualLabel=FPaths::MakeValidFileName(VisualLabel);Quinn->SetActorHiddenInGame(true);if(PC->GetHUD())PC->GetHUD()->bShowHUD=false;
  VisualCamera=GetWorld()->SpawnActor<ACameraActor>();VisualCamera->GetCameraComponent()->SetFieldOfView(81.2f);VisualCamera->GetCameraComponent()->bConstrainAspectRatio=false;VisualCamera->GetCameraComponent()->SetAspectRatio(1.6f);VisualCamera->GetCameraComponent()->bOverrideAspectRatioAxisConstraint=true;VisualCamera->GetCameraComponent()->SetAspectRatioAxisConstraint(EAspectRatioAxisConstraint::AspectRatio_MaintainXFOV);PC->SetViewTarget(VisualCamera);
 }
 if(Elapsed<12)return;
 if(VisualIndex<0){VisualIndex=0;VisualStage=Elapsed;VisualCamera->SetActorLocation(VisualEyes[0]);VisualCamera->SetActorRotation((VisualTargets[0]-VisualEyes[0]).Rotation());return;}
 if(!bVisualShot&&Elapsed-VisualStage>4){Capture(TEXT("V02_")+VisualLabel+TEXT("/")+VisualNames[VisualIndex]+TEXT(".png"));bVisualShot=true;return;}
 if(bVisualShot&&Elapsed-VisualStage>5){VisualIndex++;if(VisualIndex>=VisualNames.Num()){Write(true);PC->ConsoleCommand(TEXT("quit"));return;}VisualStage=Elapsed;bVisualShot=false;VisualCamera->SetActorLocation(VisualEyes[VisualIndex]);VisualCamera->SetActorRotation((VisualTargets[VisualIndex]-VisualEyes[VisualIndex]).Rotation());}
}
