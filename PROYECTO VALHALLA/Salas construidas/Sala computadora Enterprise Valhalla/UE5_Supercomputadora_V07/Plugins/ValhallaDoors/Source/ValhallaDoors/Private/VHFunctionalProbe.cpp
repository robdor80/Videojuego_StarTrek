#include "VHFunctionalProbe.h"
#include "VHAutomaticDoor.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/InputComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/App.h"
#include "Misc/FileHelper.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"

AVHPreviewCharacter::AVHPreviewCharacter(){
 GetCapsuleComponent()->InitCapsuleSize(35,90);bUseControllerRotationYaw=true;GetCharacterMovement()->MaxWalkSpeed=200;
 Camera=CreateDefaultSubobject<UCameraComponent>(TEXT("FirstPersonPreview"));Camera->SetupAttachment(GetCapsuleComponent());Camera->SetRelativeLocation(FVector(0,0,64));Camera->bUsePawnControlRotation=true;
}
void AVHPreviewCharacter::SetupPlayerInputComponent(UInputComponent* I){Super::SetupPlayerInputComponent(I);I->BindAxis(TEXT("Forward"),this,&AVHPreviewCharacter::Forward);I->BindAxis(TEXT("Strafe"),this,&AVHPreviewCharacter::Strafe);I->BindAxis(TEXT("Turn"),this,&AVHPreviewCharacter::Turn);I->BindAxis(TEXT("Look"),this,&AVHPreviewCharacter::Look);}
void AVHPreviewCharacter::Forward(float V){AddMovementInput(GetActorForwardVector(),V);}void AVHPreviewCharacter::Strafe(float V){AddMovementInput(GetActorRightVector(),V);}void AVHPreviewCharacter::Turn(float V){AddControllerYawInput(V);}void AVHPreviewCharacter::Look(float V){AddControllerPitchInput(V);}
AVHPreviewGameMode::AVHPreviewGameMode(){DefaultPawnClass=FParse::Param(FCommandLine::Get(),TEXT("VHRunValidation"))?nullptr:AVHPreviewCharacter::StaticClass();}

AVHFunctionalProbe::AVHFunctionalProbe(){PrimaryActorTick.bCanEverTick=true;}
void AVHFunctionalProbe::BeginPlay(){
 Super::BeginPlay();if(!FParse::Param(FCommandLine::Get(),TEXT("VHRunValidation"))||!FParse::Value(FCommandLine::Get(),TEXT("VHValidationReport="),ReportPath)){SetActorTickEnabled(false);return;}
 for(TActorIterator<AVHAutomaticDoor> It(GetWorld());It;++It)if(It->DoorId==TEXT("VALHALLA_SC_EXTERIOR_D01")){Door=*It;break;}
 if(!Door){Check(TEXT("door_exists"),false);Finish();return;}
 AddTickPrerequisiteActor(Door);FApp::SetUseFixedTimeStep(true);FApp::SetFixedDeltaTime(1./60.);
 FActorSpawnParameters P;P.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;Pawn=GetWorld()->SpawnActor<ACharacter>(ACharacter::StaticClass(),Door->GetActorLocation()+FVector(-170,0,95),FRotator::ZeroRotator,P);
 Pawn->GetCharacterMovement()->DisableMovement();Pawn->GetCapsuleComponent()->SetCapsuleSize(35,90);Pawn->GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));Pawn->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);
 Door->SetDestinationConstructed(true);Door->SetSecurityLocked(false);Door->SetExternalAccessAllowed(true);Door->ResetClosed();Check(TEXT("runtime_closed_blocks_capsule"),PassageBlocked());
}
void AVHFunctionalProbe::Check(const FString& Name,bool Pass){auto O=MakeShared<FJsonObject>();O->SetStringField(TEXT("name"),Name);O->SetBoolField(TEXT("pass"),Pass);if(Door){O->SetNumberField(TEXT("fraction"),Door->OpenFraction);O->SetStringField(TEXT("state"),StaticEnum<EVHDoorState>()->GetNameStringByValue((int64)Door->DoorState));O->SetStringField(TEXT("blocking_mesh"),Door->LastBlockingMesh);O->SetStringField(TEXT("blocking_normal"),Door->LastBlockingNormal.ToString());O->SetNumberField(TEXT("penetration_depth_cm"),Door->LastPenetrationDepth);O->SetBoolField(TEXT("starts_penetrating"),Door->bLastStartPenetrating);}Results.Add(MakeShared<FJsonValueObject>(O));UE_LOG(LogTemp,Display,TEXT("VH_RUNTIME_CHECK %s %s"),*Name,Pass?TEXT("PASS"):TEXT("FAIL"));}
void AVHFunctionalProbe::MovePawn(float X,float Y){Pawn->SetActorLocation(Door->GetActorLocation()+FVector(X,Y,95));}
bool AVHFunctionalProbe::PassageBlocked() const {FHitResult H;FCollisionQueryParams Q(SCENE_QUERY_STAT(VHRuntimePassage),false);Q.AddIgnoredActor(Pawn);FVector C=Door->GetActorLocation()+FVector(0,0,95);return GetWorld()->SweepSingleByChannel(H,C+FVector(-100,0,0),C+FVector(100,0,0),FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(35,90),Q);}
void AVHFunctionalProbe::Finish(){
 auto O=MakeShared<FJsonObject>();int32 Passed=0;for(auto V:Results)if(V->AsObject()->GetBoolField(TEXT("pass")))Passed++;O->SetBoolField(TEXT("all_pass"),Passed==Results.Num());O->SetNumberField(TEXT("passed"),Passed);O->SetNumberField(TEXT("total"),Results.Num());O->SetArrayField(TEXT("cases"),Results);O->SetStringField(TEXT("world_type"),TEXT("Game world; native door Tick, real Chaos capsule queries, complete imported V04E"));O->SetBoolField(TEXT("human_quinn_v06_completed"),false);FString S;auto W=TJsonWriterFactory<>::Create(&S);FJsonSerializer::Serialize(O,W);FFileHelper::SaveStringToFile(S,*ReportPath);SetActorTickEnabled(false);FPlatformMisc::RequestExit(false);
}
void AVHFunctionalProbe::Tick(float Dt){
 Super::Tick(Dt);if(!Door||!Pawn||ReportPath.IsEmpty())return;Elapsed+=Dt;
 auto Next=[&](int32 P){Phase=P;Elapsed=0;};
 switch(Phase){
 case 0:if(Elapsed>1.2f){Check(TEXT("runtime_side_A_opens"),Door->OpenFraction>.999f);Check(TEXT("runtime_open_passage_clear"),!PassageBlocked());MovePawn(500);Next(1);}break;
 case 1:if(Elapsed>3){Check(TEXT("runtime_auto_close_blocks_again"),Door->OpenFraction<.001f&&PassageBlocked());MovePawn(170);Next(2);}break;
 case 2:if(Elapsed>1.2f){Check(TEXT("runtime_side_B_opens"),Door->OpenFraction>.999f);MovePawn(0);Next(3);}break;
 case 3:if(Elapsed>3){Check(TEXT("runtime_occupied_holds_open"),Door->OpenFraction>.999f&&Door->IsDoorwayOccupied());Door->SetSecurityLocked(true);Next(4);}break;
 case 4:if(Elapsed>2){Check(TEXT("runtime_lock_preserves_occupant"),Door->OpenFraction>.999f);MovePawn(500);Next(5);}break;
 case 5:if(Elapsed>3){Check(TEXT("runtime_lock_closes_when_clear"),Door->OpenFraction<.001f&&Door->DoorState==EVHDoorState::Blocked);MovePawn(-170);Next(6);}break;
 case 6:if(Elapsed>1){Check(TEXT("runtime_locked_approach_denied"),Door->OpenFraction<.001f);Door->SetSecurityLocked(false);Next(7);}break;
 case 7:if(Elapsed>1.2f){Check(TEXT("runtime_unlock_reopens"),Door->OpenFraction>.999f);MovePawn(500);Next(8);}break;
 case 8:if(Door->DoorState==EVHDoorState::Closing&&Door->OpenFraction>.2f){Reversals=Door->ClosingReversalCount;MovePawn(0);Next(9);}else if(Elapsed>4){Check(TEXT("runtime_closing_observed"),false);Next(9);}break;
 case 9:if(Elapsed>.2f){Check(TEXT("runtime_close_interrupted_safely"),Door->ClosingReversalCount>Reversals&&Door->DoorState!=EVHDoorState::Closing);Next(10);}break;
 case 10:if(Elapsed>1){Check(TEXT("runtime_interruption_reopens"),Door->OpenFraction>.999f);MovePawn(500);Next(11);}break;
 case 11:if(Elapsed>3){Check(FString::Printf(TEXT("runtime_cycle_%02d_closed"),Cycle+1),Door->OpenFraction<.001f);MovePawn(Cycle%2?170:-170);Next(12);}break;
 case 12:if(Elapsed>1.2f){Check(FString::Printf(TEXT("runtime_cycle_%02d_open"),Cycle+1),Door->OpenFraction>.999f);Cycle++;MovePawn(500);Next(Cycle>=8?13:11);}break;
 case 13:if(Elapsed>3){Door->SetSecurityLocked(true);Door->SetEmergencyHoldOpen(true);Next(14);}break;
 case 14:if(Elapsed>1.2f){Check(TEXT("runtime_emergency_opens_locked_door"),Door->OpenFraction>.999f);Next(15);}break;
 case 15:if(Elapsed>3){Check(TEXT("runtime_emergency_holds_open"),Door->OpenFraction>.999f);Door->SetEmergencyHoldOpen(false);Next(16);}break;
 case 16:if(Elapsed>3){Check(TEXT("runtime_emergency_release_closes_safely"),Door->OpenFraction<.001f&&Door->DoorState==EVHDoorState::Blocked);Finish();}break;
 }
}
