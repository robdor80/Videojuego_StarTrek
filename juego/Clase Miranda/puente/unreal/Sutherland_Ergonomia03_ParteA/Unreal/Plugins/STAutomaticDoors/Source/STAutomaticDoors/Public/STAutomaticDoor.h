#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "STAutomaticDoor.generated.h"
class UStaticMeshComponent;
class UBoxComponent;
class USTAutomaticDoorTestLibrary;

UENUM(BlueprintType)
enum class ESTDoorState:uint8 { Closed, Opening, Open, Closing, Obstructed };
DECLARE_DYNAMIC_MULTICAST_DELEGATE_ThreeParams(FSTDoorAccessEvent,AActor*,Requester,bool,bGranted,FName,Reason);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FSTDoorStateEvent,ESTDoorState,Previous,ESTDoorState,Current);

/** Independent observations: intention is never an access grant or a safety override. */
USTRUCT(BlueprintType)
struct STAUTOMATICDOORS_API FSTDoorIntentEvaluation {
 GENERATED_BODY()
 UPROPERTY(BlueprintReadOnly,Category="Door|Intent") bool Nearby=false;
 UPROPERTY(BlueprintReadOnly,Category="Door|Intent") bool HasIntent=false;
 UPROPERTY(BlueprintReadOnly,Category="Door|Intent") bool Authorized=false;
 UPROPERTY(BlueprintReadOnly,Category="Door|Intent") bool DoorwayOccupied=false;
 UPROPERTY(BlueprintReadOnly,Category="Door|Intent") FName Reason=TEXT("OutsideApproach");
 UPROPERTY(BlueprintReadOnly,Category="Door|Intent") float CrossingSeconds=-1;
 UPROPERTY(BlueprintReadOnly,Category="Door|Intent") float CrossingLateralCm=0;
};

/** Local sliding-door mechanism. Safety gates dominate external access decisions.
 * Local X: doorway normal. Local Y: sliding axis. Root: threshold center. Units: cm.
 */
UCLASS(Blueprintable,BlueprintType)
class STAUTOMATICDOORS_API ASTAutomaticDoor:public AActor {
 GENERATED_BODY()
public:
 ASTAutomaticDoor();
 virtual void Tick(float DeltaSeconds) override;
 virtual void OnConstruction(const FTransform& Transform) override;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Door|Components") TObjectPtr<USceneComponent> DoorRoot;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Door|Components") TObjectPtr<UStaticMeshComponent> LeftLeaf;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Door|Components") TObjectPtr<UStaticMeshComponent> RightLeaf;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Door|Components") TObjectPtr<UBoxComponent> ApproachSensor;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Door|Components") TObjectPtr<UBoxComponent> OccupancySensor;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Identity") FName DoorId;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Geometry") FVector LeftClosedLocation=FVector(0,-41,196);
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Geometry") FVector RightClosedLocation=FVector(0,41,196);
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Geometry",meta=(ClampMin="0")) float TravelDistance=87;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Geometry",meta=(ClampMin="1")) float OpeningWidth=164;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Geometry",meta=(ClampMin="1")) float OpeningHeight=392;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Timing",meta=(ClampMin="0.05")) float MovementDuration=0.7f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Timing",meta=(ClampMin="0.0")) float CloseDelay=1.5f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Sensors",meta=(ClampMin="80")) float ProximityDepth=220;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Safety") bool bDestinationConstructed=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Safety") bool bSecurityLocked=true;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Access") bool bExternalAccessAllowed=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Access") bool bProximityEnabled=true;
 /** Off only for legacy assets. New P03E D01 Blueprint enables it explicitly. */
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent") bool bUsePassageIntent=false;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0.1")) float PredictionHorizon=1.2f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0")) float MovingSpeedThreshold=15;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0")) float MinNormalSpeed=5;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0")) float SlowApproachDistance=120;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0",ClampMax="1")) float MinNormalFraction=.15f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0")) float PathClearance=5;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0")) float StationaryMaxDistance=200;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0",ClampMax="1")) float StationaryFacingDot=.55f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0")) float ClearEntryDistance=110;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0",ClampMax="1")) float ClearEntryWidthFraction=.65f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Intent",meta=(ClampMin="0",ClampMax="1")) float IntentGraceSeconds=.22f;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,Category="Door|Debug") bool bDrawIntentDebug=false;
 /** Explicit NPC/player use continues through RequestOpen and the existing access policy. */
 UFUNCTION(BlueprintPure,Category="Door|Intent") FSTDoorIntentEvaluation EvaluatePassageIntent(AActor* Requester) const;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Door|Runtime") ESTDoorState DoorState=ESTDoorState::Closed;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Door|Runtime") float OpenFraction=0;
 UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="Door|Runtime") int32 ClosingReversalCount=0;
 UPROPERTY(BlueprintAssignable,Category="Door|Integration") FSTDoorAccessEvent OnAccessEvaluated;
 UPROPERTY(BlueprintAssignable,Category="Door|Integration") FSTDoorStateEvent OnDoorStateChanged;
 /** Override this in a child BP or an external adapter. No CoreRPG reference here. */
 UFUNCTION(BlueprintNativeEvent,BlueprintPure,Category="Door|Integration") bool CanActorUseDoor(AActor* Requester) const;
 virtual bool CanActorUseDoor_Implementation(AActor* Requester) const;
 UFUNCTION(BlueprintCallable,Category="Door|Commands") bool RequestOpen(AActor* Requester);
 UFUNCTION(BlueprintCallable,Category="Door|Commands") void RequestClose();
 UFUNCTION(BlueprintCallable,Category="Door|Safety") void SetSecurityLocked(bool bLocked);
 UFUNCTION(BlueprintCallable,Category="Door|Safety") void SetDestinationConstructed(bool bConstructed);
 UFUNCTION(BlueprintCallable,Category="Door|Integration") void SetExternalAccessAllowed(bool bAllowed);
 UFUNCTION(BlueprintPure,Category="Door|Safety") bool IsDoorwayOccupied() const;
 UFUNCTION(BlueprintCallable,CallInEditor,Category="Door|Setup") void ResetClosed();
protected:
 virtual void BeginPlay() override;
 void AdvanceDoor(float DeltaSeconds);
 void ConfigureSensors();
 TArray<AActor*> QueryPawns(const UBoxComponent* Sensor) const;
 bool EvaluateAccess(AActor* Requester,FName& Reason) const;
 void ChangeState(ESTDoorState NewState);
 float TimeWithoutDemand=0;
 bool bManualCloseRequested=false;
 bool bRequestedOpen=false;
 bool bSafetyReopen=false;
 TWeakObjectPtr<AActor> RequestedActor;
 TWeakObjectPtr<AActor> OpeningRequester;
 TSet<TWeakObjectPtr<AActor>> PreviousNearby;
 TMap<TWeakObjectPtr<AActor>,float> IntentGrace;
 bool UpdatePassageIntent(AActor* Pawn,float DeltaSeconds);
 void DrawIntentDebug() const;
 friend class USTAutomaticDoorTestLibrary;
};
