#include "STSlidingChair.h"
#include "Components/StaticMeshComponent.h"
#include "Components/InputComponent.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/PlayerController.h"
#include "Camera/CameraActor.h"
#include "Engine/Engine.h"
ASTSlidingChair::ASTSlidingChair(){
 PrimaryActorTick.bCanEverTick=true;
 FixedRoot=CreateDefaultSubobject<USceneComponent>(TEXT("FixedRoot"));SetRootComponent(FixedRoot);FixedRoot->SetMobility(EComponentMobility::Static);
 FixedBase=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("FixedRailBase"));FixedBase->SetupAttachment(FixedRoot);FixedBase->SetMobility(EComponentMobility::Static);FixedBase->SetCollisionProfileName(TEXT("BlockAll"));
 MovingRig=CreateDefaultSubobject<USceneComponent>(TEXT("MovingRig"));MovingRig->SetupAttachment(FixedRoot);MovingRig->SetMobility(EComponentMobility::Movable);
 for(int I=0;I<15;I++){auto* C=CreateDefaultSubobject<UStaticMeshComponent>(*FString::Printf(TEXT("MovingPart_%02d"),I+1));C->SetupAttachment(MovingRig);C->SetMobility(EComponentMobility::Movable);C->SetCollisionProfileName(TEXT("BlockAllDynamic"));MovingParts.Add(C);}
}
void ASTSlidingChair::OnConstruction(const FTransform& T){Super::OnConstruction(T);MovingRig->SetRelativeLocation(RetractedLocalPosition);Fraction=0;ChairState=ESTChairState::Retracted;}
void ASTSlidingChair::BeginPlay(){Super::BeginPlay();ResetRetracted();}
bool ASTSlidingChair::IsMoving()const{return ChairState==ESTChairState::Extending||ChairState==ESTChairState::Retracting;}
bool ASTSlidingChair::Request(float Target){
 if(IsMoving())return Target==TargetFraction;
 if(FMath::IsNearlyEqual(Fraction,Target))return true;
 Elapsed=0;StartFraction=Fraction;TargetFraction=Target;ChairState=Target>Fraction?ESTChairState::Extending:ESTChairState::Retracting;LastObstruction.Empty();return true;
}
bool ASTSlidingChair::Extend(){return Request(1);}
bool ASTSlidingChair::Retract(){return Request(0);}
bool ASTSlidingChair::Toggle(){return IsMoving()?false:Request(Fraction>.5f?0:1);}
bool ASTSlidingChair::ApplyFraction(float Value,bool Sweep){
 FVector Target=RetractedLocalPosition+LocalTravelDirection.GetSafeNormal()*StrokeCm*Value;
 FVector Delta=MovingRig->GetAttachParent()->GetComponentTransform().TransformVectorNoScale(Target-MovingRig->GetRelativeLocation());
 if(Sweep&&!Delta.IsNearlyZero()){
  FComponentQueryParams Q;Q.AddIgnoredActor(this);Q.bTraceComplex=false;
  // Occupant motion is a future integration responsibility. Any external actor,
  // including an occupant, remains a blocker; the approved own rail interface is ignored.
  for(auto C:MovingParts){TArray<FHitResult> Hits;GetWorld()->ComponentSweepMultiByChannel(Hits,C,C->GetComponentLocation(),C->GetComponentLocation()+Delta,C->GetComponentQuat(),ECC_WorldDynamic,Q);
   for(const auto& H:Hits)if(H.bBlockingHit){LastObstruction=GetNameSafe(H.GetActor())+TEXT("/")+GetNameSafe(H.GetComponent())+TEXT(" moving=")+C->GetStaticMesh()->GetName()+TEXT(" impact=")+H.ImpactPoint.ToString()+FString::Printf(TEXT(" time=%.6f initial=%d depth=%.6f"),H.Time,H.bStartPenetrating,H.PenetrationDepth);ChairState=ESTChairState::Obstructed;return false;}
  }
 }
 MovingRig->SetRelativeLocation(Target);Fraction=Value;return true;
}
void ASTSlidingChair::AdvanceChair(float Dt){
 if(!IsMoving())return;Elapsed+=FMath::Max(0.f,Dt);float T=FMath::Clamp(Elapsed/FMath::Max(.05f,MovementDuration),0.f,1.f);float Smooth=T*T*(3-2*T);
 if(ApplyFraction(FMath::Lerp(StartFraction,TargetFraction,Smooth),true)&&T>=1)ChairState=TargetFraction==1?ESTChairState::Extended:ESTChairState::Retracted;
}
void ASTSlidingChair::Tick(float Dt){Super::Tick(Dt);AdvanceChair(Dt);}
void ASTSlidingChair::ResetRetracted(){Elapsed=0;ApplyFraction(0,false);ChairState=ESTChairState::Retracted;LastObstruction.Empty();}
ASTChairLabControls::ASTChairLabControls(){PrimaryActorTick.bCanEverTick=false;}
void ASTChairLabControls::BeginPlay(){
 Super::BeginPlay();auto* P=GetWorld()->GetFirstPlayerController();if(!P)return;EnableInput(P);
 InputComponent->BindKey(EKeys::E,IE_Pressed,this,&ASTChairLabControls::ExtendAll);InputComponent->BindKey(EKeys::R,IE_Pressed,this,&ASTChairLabControls::RetractAll);
 InputComponent->BindKey(EKeys::One,IE_Pressed,this,&ASTChairLabControls::Toggle01);InputComponent->BindKey(EKeys::Two,IE_Pressed,this,&ASTChairLabControls::Toggle02);InputComponent->BindKey(EKeys::Three,IE_Pressed,this,&ASTChairLabControls::Toggle03);InputComponent->BindKey(EKeys::Four,IE_Pressed,this,&ASTChairLabControls::Toggle04);InputComponent->BindKey(EKeys::Five,IE_Pressed,this,&ASTChairLabControls::Toggle05);InputComponent->BindKey(EKeys::Six,IE_Pressed,this,&ASTChairLabControls::Toggle06);
 for(TActorIterator<ACameraActor> It(GetWorld());It;++It)if(It->ActorHasTag(TEXT("LabOverview"))){P->SetViewTarget(*It);break;}
 if(GEngine)GEngine->AddOnScreenDebugMessage(-1,120,FColor::Cyan,TEXT("Sutherland Chair Lab | E: extend all 30 cm | R: retract | 1-6: individual | Esc: stop"));
}
void ASTChairLabControls::ExtendAll(){for(TActorIterator<ASTSlidingChair> It(GetWorld());It;++It)It->Extend();}
void ASTChairLabControls::RetractAll(){for(TActorIterator<ASTSlidingChair> It(GetWorld());It;++It)It->Retract();}
void ASTChairLabControls::ToggleIndex(int I){for(TActorIterator<ASTSlidingChair> It(GetWorld());It;++It)if(It->ChairId==FString::Printf(TEXT("Chair%02d"),I))It->Toggle();}
void ASTChairLabControls::Toggle01(){ToggleIndex(1);}void ASTChairLabControls::Toggle02(){ToggleIndex(2);}void ASTChairLabControls::Toggle03(){ToggleIndex(3);}void ASTChairLabControls::Toggle04(){ToggleIndex(4);}void ASTChairLabControls::Toggle05(){ToggleIndex(5);}void ASTChairLabControls::Toggle06(){ToggleIndex(6);}

