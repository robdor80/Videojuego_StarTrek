#include "STPlayable.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/SpringArmComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/InputComponent.h"
#include "Animation/AnimSequence.h"
#include "Animation/AnimInstance.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "EngineUtils.h"
#include "UObject/ConstructorHelpers.h"
#include "InputCoreTypes.h"
#include "Kismet/GameplayStatics.h"
#include "Misc/Paths.h"
#include "Misc/FileHelper.h"
#include "STGameplayProof.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"

ASTSeatAnchor::ASTSeatAnchor(){
 SeatRoot=CreateDefaultSubobject<USceneComponent>(TEXT("SeatRoot"));SetRootComponent(SeatRoot);
 auto Point=[this](const TCHAR* Name,FVector P){auto* C=CreateDefaultSubobject<USceneComponent>(Name);C->SetupAttachment(SeatRoot);C->SetRelativeLocation(P);return C;};
 Approach=Point(TEXT("Approach"),FVector(95,0,90));SeatedCapsule=Point(TEXT("SeatedCapsule"),FVector(0,0,110));
 Pelvis=Point(TEXT("Pelvis"),FVector(0,0,75));Back=Point(TEXT("Back"),FVector(-25,0,110));
 LeftFoot=Point(TEXT("LeftFoot"),FVector(42,-15,32));RightFoot=Point(TEXT("RightFoot"),FVector(42,15,32));Exit=Point(TEXT("SafeExit"),FVector(110,0,90));
}
bool ASTSeatAnchor::Reserve(ACharacter* C){if(!bInteractionEnabled||!C||(Occupant.IsValid()&&Occupant.Get()!=C))return false;Occupant=C;return true;}
void ASTSeatAnchor::Release(ACharacter* C){if(Occupant.Get()==C)Occupant.Reset();}
bool ASTSeatAnchor::ApproachIsClear(ACharacter* C) const {
 if(!C)return false;FCollisionQueryParams Q(SCENE_QUERY_STAT(SeatApproach),false,C);Q.AddIgnoredActor(this);
 auto* Capsule=C->GetCapsuleComponent();const FVector Target=Approach->GetComponentLocation();
 return !GetWorld()->OverlapBlockingTestByChannel(Target,FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(Capsule->GetUnscaledCapsuleRadius(),90),Q);
}
bool ASTSeatAnchor::ExitIsClear(ACharacter* C) const {
 if(!C)return false;FCollisionQueryParams Q(SCENE_QUERY_STAT(SeatExit),false,C);Q.AddIgnoredActor(this);
 const FVector Target=Exit->GetComponentLocation();
 if(GetWorld()->OverlapBlockingTestByChannel(Target,FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(35,90),Q))return false;
 FHitResult Floor; if(!GetWorld()->LineTraceSingleByChannel(Floor,Target,Target-FVector(0,0,105),ECC_Visibility,Q)||Floor.ImpactNormal.Z<.7)return false;
 for(AActor* A:ChairCollisionActors)Q.AddIgnoredActor(A);
 FHitResult Hit;return !GetWorld()->SweepSingleByChannel(Hit,C->GetActorLocation(),Target,FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(25,35),Q);
}
ASTPlayableQuinn::ASTPlayableQuinn(){
 PrimaryActorTick.bCanEverTick=true;GetCapsuleComponent()->InitCapsuleSize(35,90);bUseControllerRotationYaw=false;
 GetCharacterMovement()->bOrientRotationToMovement=true;GetCharacterMovement()->RotationRate=FRotator(0,500,0);GetCharacterMovement()->MaxWalkSpeed=180;GetCharacterMovement()->MaxStepHeight=45;GetCharacterMovement()->BrakingDecelerationWalking=1400;
 GetMesh()->SetRelativeLocation(FVector(0,0,-89));GetMesh()->SetRelativeRotation(FRotator(0,-90,0));GetMesh()->SetCollisionProfileName(TEXT("CharacterMesh"));
 GetMesh()->VisibilityBasedAnimTickOption=EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
 static ConstructorHelpers::FObjectFinder<USkeletalMesh> QuinnMeshAsset(TEXT("/Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple"));if(QuinnMeshAsset.Succeeded())GetMesh()->SetSkeletalMesh(QuinnMeshAsset.Object);
 static ConstructorHelpers::FClassFinder<UAnimInstance> Anim(TEXT("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed"));if(Anim.Succeeded())GetMesh()->SetAnimInstanceClass(Anim.Class);
 CameraBoom=CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));CameraBoom->SetupAttachment(GetCapsuleComponent());CameraBoom->TargetArmLength=230;CameraBoom->SocketOffset=FVector(0,30,55);CameraBoom->bUsePawnControlRotation=true;CameraBoom->bDoCollisionTest=true;CameraBoom->ProbeSize=14;CameraBoom->ProbeChannel=ECC_Camera;
 FollowCamera=CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));FollowCamera->SetupAttachment(CameraBoom,USpringArmComponent::SocketName);FollowCamera->FieldOfView=80;
}
void ASTPlayableQuinn::BeginPlay(){Super::BeginPlay();OriginalMeshOffset=GetMesh()->GetRelativeLocation();OriginalMeshRotation=GetMesh()->GetRelativeRotation();OriginalAnimClass=GetMesh()->GetAnimClass();if(auto* PC=Cast<APlayerController>(GetController())){PC->bShowMouseCursor=false;PC->SetInputMode(FInputModeGameOnly());}if(FParse::Param(FCommandLine::Get(),TEXT("SutherlandGameplayProof")))GetWorld()->SpawnActor<ASTGameplayProof>();}
void ASTPlayableQuinn::SetupPlayerInputComponent(UInputComponent* I){Super::SetupPlayerInputComponent(I);I->BindAxis(TEXT("Move Forward / Backward"),this,&ASTPlayableQuinn::MoveForward);I->BindAxis(TEXT("Move Right / Left"),this,&ASTPlayableQuinn::MoveRight);I->BindAxis(TEXT("Turn Right / Left Mouse"),this,&ASTPlayableQuinn::Turn);I->BindAxis(TEXT("Look Up / Down Mouse"),this,&ASTPlayableQuinn::Look);I->BindKey(EKeys::E,IE_Pressed,this,&ASTPlayableQuinn::InteractKey);I->BindKey(EKeys::LeftShift,IE_Pressed,this,&ASTPlayableQuinn::RunOn);I->BindKey(EKeys::LeftShift,IE_Released,this,&ASTPlayableQuinn::RunOff);I->BindKey(EKeys::SpaceBar,IE_Pressed,this,&ASTPlayableQuinn::JumpKey);}
void ASTPlayableQuinn::MoveForward(float V){if(SeatPhase==ESTSeatPhase::Walking&&Controller)AddMovementInput(FRotationMatrix(FRotator(0,Controller->GetControlRotation().Yaw,0)).GetUnitAxis(EAxis::X),V);}
void ASTPlayableQuinn::MoveRight(float V){if(SeatPhase==ESTSeatPhase::Walking&&Controller)AddMovementInput(FRotationMatrix(FRotator(0,Controller->GetControlRotation().Yaw,0)).GetUnitAxis(EAxis::Y),V);}
void ASTPlayableQuinn::Turn(float V){AddControllerYawInput(V);}
void ASTPlayableQuinn::Look(float V){AddControllerPitchInput(V);}
void ASTPlayableQuinn::RunOn(){bRunning=true;}void ASTPlayableQuinn::RunOff(){bRunning=false;}
void ASTPlayableQuinn::JumpKey(){if(SeatPhase==ESTSeatPhase::Walking)Jump();}
void ASTPlayableQuinn::InteractKey(){Interact();}
ASTSeatAnchor* ASTPlayableQuinn::FindUsableSeat() const {
 ASTSeatAnchor* Best=nullptr;float Dist=MAX_flt;
 for(TActorIterator<ASTSeatAnchor> It(GetWorld());It;++It){auto* S=*It;if(!S->bInteractionEnabled||S->Occupant.IsValid())continue;float D=FVector::Dist2D(GetActorLocation(),S->Approach->GetComponentLocation());if(D<S->InteractionDistance&&D<Dist&&S->ApproachIsClear(const_cast<ASTPlayableQuinn*>(this))){Best=S;Dist=D;}}
 return Best;
}
bool ASTPlayableQuinn::UseSeat(ASTSeatAnchor* S){
 if(SeatPhase!=ESTSeatPhase::Walking||!S||!S->SitAnimation||!S->SeatedAnimation||!S->StandAnimation||!S->ApproachIsClear(this)||FVector::Dist2D(GetActorLocation(),S->Approach->GetComponentLocation())>S->InteractionDistance||!S->Reserve(this))return false;
 ActiveSeat=S;SeatPhase=ESTSeatPhase::Approaching;PhaseTime=0;ApproachTimeout=0;return true;
}
bool ASTPlayableQuinn::Interact(){
 if(SeatPhase==ESTSeatPhase::Walking)return UseSeat(FindUsableSeat());
 if(SeatPhase==ESTSeatPhase::Approaching||SeatPhase==ESTSeatPhase::Aligning){AbortApproach();return true;}
 if(SeatPhase!=ESTSeatPhase::Seated||!ActiveSeat)return false;
 if(!ActiveSeat->ExitIsClear(this)){InteractionMessage=TEXT("Salida bloqueada");return false;}
 SeatPhase=ESTSeatPhase::Standing;PhaseTime=0;TransitionStart=GetActorTransform();GetMesh()->PlayAnimation(ActiveSeat->StandAnimation,false);GetMesh()->SetPlayRate(1);return true;
}
void ASTPlayableQuinn::SetSeatIgnores(bool Ignore){if(ActiveSeat)for(AActor* A:ActiveSeat->ChairCollisionActors)if(A)GetCapsuleComponent()->IgnoreActorWhenMoving(A,Ignore);}
void ASTPlayableQuinn::StartSitting(){
 SeatPhase=ESTSeatPhase::Sitting;PhaseTime=0;TransitionStart=GetActorTransform();GetCharacterMovement()->StopMovementImmediately();GetCharacterMovement()->DisableMovement();SetSeatIgnores(true);GetCapsuleComponent()->SetCapsuleSize(25,35,true);GetMesh()->PlayAnimation(ActiveSeat->SitAnimation,false);GetMesh()->SetPlayRate(1);
}
void ASTPlayableQuinn::AbortApproach(){GetCharacterMovement()->StopMovementImmediately();if(ActiveSeat)ActiveSeat->Release(this);ActiveSeat=nullptr;SeatPhase=ESTSeatPhase::Walking;GetCharacterMovement()->bOrientRotationToMovement=true;}
void ASTPlayableQuinn::FinishStanding(){
 SetSeatIgnores(false);GetCapsuleComponent()->SetCapsuleSize(35,90,true);GetMesh()->SetRelativeLocation(OriginalMeshOffset);GetMesh()->SetRelativeRotation(OriginalMeshRotation);GetMesh()->SetAnimationMode(EAnimationMode::AnimationBlueprint);GetMesh()->SetAnimInstanceClass(OriginalAnimClass);GetCharacterMovement()->SetMovementMode(MOVE_Walking);GetCharacterMovement()->bOrientRotationToMovement=true;ActiveSeat->Release(this);ActiveSeat=nullptr;SeatPhase=ESTSeatPhase::Walking;CompletedSitCycles++;
}
void ASTPlayableQuinn::Tick(float Dt){
 Super::Tick(Dt);PhaseTime+=Dt;GetCharacterMovement()->MaxWalkSpeed=bRunning?RunSpeed:WalkSpeed;
 if(SeatPhase==ESTSeatPhase::Walking){InteractionMessage=FindUsableSeat()?TEXT("E \u2014 Sentarse"):TEXT("");return;}
 if(!IsValid(ActiveSeat)){SeatPhase=ESTSeatPhase::Walking;GetCharacterMovement()->SetMovementMode(MOVE_Walking);return;}
 if(SeatPhase==ESTSeatPhase::Approaching){
  InteractionMessage=TEXT("Acerc\u00e1ndose \u2014 E cancelar");ApproachTimeout+=Dt;FVector D=ActiveSeat->Approach->GetComponentLocation()-GetActorLocation();D.Z=0;
  if(ApproachTimeout>8){AbortApproach();return;}
  if(D.Size()<4){GetCharacterMovement()->StopMovementImmediately();SeatPhase=ESTSeatPhase::Aligning;PhaseTime=0;TransitionStart=GetActorTransform();GetCharacterMovement()->bOrientRotationToMovement=false;return;}
  GetCharacterMovement()->MaxWalkSpeed=100;AddMovementInput(D.GetSafeNormal(),FMath::Clamp(D.Size()/25,0.15f,1.f));return;
 }
 if(SeatPhase==ESTSeatPhase::Aligning){
  float A=FMath::Clamp(PhaseTime/.65f,0.f,1.f);SetActorRotation(FQuat::Slerp(TransitionStart.GetRotation(),ActiveSeat->GetActorQuat(),A));if(A>=1)StartSitting();return;
 }
 if(SeatPhase==ESTSeatPhase::Seated){InteractionMessage=ActiveSeat->ExitIsClear(this)?TEXT("E \u2014 Levantarse"):TEXT("Salida bloqueada");return;}
 if(SeatPhase==ESTSeatPhase::Sitting||SeatPhase==ESTSeatPhase::Standing){
  const bool Sit=SeatPhase==ESTSeatPhase::Sitting;float A=FMath::Clamp(PhaseTime/(Sit?ActiveSeat->SitSeconds:ActiveSeat->StandSeconds),0.f,1.f);float Smooth=A*A*(3-2*A);
  // A new obstruction during a transition pauses that transition in place.
  // It never switches to a seated pose away from the physical seat.
  if(!Sit&&!ActiveSeat->ExitIsClear(this)){PhaseTime=FMath::Max(0.f,PhaseTime-Dt);GetMesh()->SetPlayRate(0);InteractionMessage=TEXT("Salida bloqueada");return;}
  FVector Goal=Sit?ActiveSeat->SeatedCapsule->GetComponentLocation():ActiveSeat->Exit->GetComponentLocation();FHitResult Hit;
  const FVector Next=FMath::Lerp(TransitionStart.GetLocation(),Goal,Smooth);
  FCollisionQueryParams Q(SCENE_QUERY_STAT(SeatTransition),false,this);
  for(AActor* ChairActor:ActiveSeat->ChairCollisionActors)Q.AddIgnoredActor(ChairActor);
  if(GetWorld()->SweepSingleByChannel(Hit,GetActorLocation(),Next,FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(25,35),Q)){
   PhaseTime=FMath::Max(0.f,PhaseTime-Dt);GetMesh()->SetPlayRate(0);InteractionMessage=TEXT("Movimiento bloqueado");return;
  }
  GetMesh()->SetPlayRate(1);SetActorLocation(Next,true,&Hit);
  if(Hit.bBlockingHit){PhaseTime=FMath::Max(0.f,PhaseTime-Dt);GetMesh()->SetPlayRate(0);InteractionMessage=TEXT("Movimiento bloqueado");return;}
  GetMesh()->SetRelativeLocation(FMath::Lerp(Sit?OriginalMeshOffset:ActiveSeat->SeatedMeshOffset,Sit?ActiveSeat->SeatedMeshOffset:OriginalMeshOffset,Smooth));InteractionMessage=Sit?TEXT("Sent\u00e1ndose"):TEXT("Levant\u00e1ndose");
  if(A>=1){if(Sit){SeatPhase=ESTSeatPhase::Seated;GetMesh()->PlayAnimation(ActiveSeat->SeatedAnimation,true);}else FinishStanding();}
 }
}
void ASTPlayableQuinn::EndPlay(const EEndPlayReason::Type R){if(ActiveSeat)ActiveSeat->Release(this);Super::EndPlay(R);}
FString ASTPlayableQuinn::RuntimeState() const {return FString::Printf(TEXT("phase=%d possessed=%d movement=%d capsule=%.1f,%.1f collision=%d cycles=%d xyz=%s"),int(SeatPhase),IsPlayerControlled(),int(GetCharacterMovement()->MovementMode),GetCapsuleComponent()->GetUnscaledCapsuleRadius(),GetCapsuleComponent()->GetUnscaledCapsuleHalfHeight(),int(GetCapsuleComponent()->GetCollisionEnabled()),CompletedSitCycles,*GetActorLocation().ToString());}
void ASTPlayableHUD::DrawHUD(){Super::DrawHUD();auto* C=Cast<ASTPlayableQuinn>(GetOwningPawn());if(!C||!Canvas)return;if(!C->InteractionMessage.IsEmpty())DrawText(C->InteractionMessage,FLinearColor(.85,.92,1),Canvas->ClipX*.42f,Canvas->ClipY*.83f,nullptr,1.1f);}
ASTPlayableGameMode::ASTPlayableGameMode(){DefaultPawnClass=ASTPlayableQuinn::StaticClass();HUDClass=ASTPlayableHUD::StaticClass();}

