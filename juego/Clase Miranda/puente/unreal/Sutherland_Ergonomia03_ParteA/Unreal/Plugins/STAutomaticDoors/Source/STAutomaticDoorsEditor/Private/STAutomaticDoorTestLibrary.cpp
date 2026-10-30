#include "STAutomaticDoorTestLibrary.h"
#include "STAutomaticDoor.h"
#include "STDoorPermissionFixture.h"
#include "Components/StaticMeshComponent.h"
#include "Components/CapsuleComponent.h"
#include "Engine/World.h"
#include "Engine/StaticMesh.h"
#include "GameFramework/Character.h"
#include "GameFramework/SpectatorPawn.h"
#include "Serialization/JsonSerializer.h"
#include "Dom/JsonObject.h"

static FString ToJson(const TSharedRef<FJsonObject>& Object) {
 FString Text;auto Writer=TJsonWriterFactory<>::Create(&Text);FJsonSerializer::Serialize(Object,Writer);return Text;
}
ACharacter* USTAutomaticDoorTestLibrary::SpawnRuntimeValidationPawn(UObject* Context,UClass* PawnClass,FVector Location) {
 UWorld* World=Cast<UWorld>(Context);if(!World&&Context)World=Context->GetWorld();
 if(!World||!PawnClass||!PawnClass->IsChildOf(ACharacter::StaticClass()))return nullptr;
 FActorSpawnParameters P;P.ObjectFlags|=RF_Transient;P.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 return World->SpawnActor<ACharacter>(PawnClass,FTransform(Location),P);
}
FString USTAutomaticDoorTestLibrary::RunAutomationChecks(UObject* Context,UClass* BPClass,UStaticMesh* LMesh,UStaticMesh* RMesh) {
 const auto Report=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Cases;
 UWorld* World=Context?Context->GetWorld():nullptr;
 if(!World)World=Cast<UWorld>(Context);
 if(!World||!BPClass||!BPClass->IsChildOf(ASTAutomaticDoor::StaticClass())||!LMesh||!RMesh){Report->SetStringField("error",TEXT("Invalid inputs"));return ToJson(Report);}
 TArray<AActor*> Temporary;FActorSpawnParameters Params;Params.ObjectFlags|=RF_Transient;
 Params.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 auto SpawnDoor=[&](FVector Pos){
  auto* D=World->SpawnActor<ASTAutomaticDoor>(BPClass,FTransform(Pos),Params);Temporary.Add(D);
  D->LeftLeaf->SetStaticMesh(LMesh);D->RightLeaf->SetStaticMesh(RMesh);
  D->LeftClosedLocation=FVector(0,-41,196);D->RightClosedLocation=FVector(0,41,196);
  D->bUsePassageIntent=true;D->OpeningWidth=164;D->OpeningHeight=392;D->TravelDistance=88;D->ConfigureSensors();D->ResetClosed();return D;
 };
 auto SpawnPawn=[&](FVector Pos){
  auto* P=World->SpawnActor<ACharacter>(ACharacter::StaticClass(),FTransform(Pos),Params);Temporary.Add(P);
  P->GetCapsuleComponent()->SetCapsuleSize(35,90);P->GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));
  P->GetCapsuleComponent()->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);return P;
 };
 auto Advance=[&](ASTAutomaticDoor* D,float Seconds){for(int32 I=0;I<FMath::CeilToInt(Seconds*60);I++)D->AdvanceDoor(1.f/60);};
 auto Check=[&](const TCHAR* Name,bool Pass,ASTAutomaticDoor* D){auto O=MakeShared<FJsonObject>();
  O->SetStringField("name",Name);O->SetBoolField("pass",Pass);O->SetNumberField("open_fraction",D->OpenFraction);
  O->SetStringField("state",StaticEnum<ESTDoorState>()->GetNameStringByValue((int64)D->DoorState));
  O->SetNumberField("closing_reversals",D->ClosingReversalCount);Cases.Add(MakeShared<FJsonValueObject>(O));};
 auto PassageBlocked=[&](ASTAutomaticDoor* D){FHitResult H;FVector C=D->GetActorLocation()+FVector(0,0,100);
  FCollisionQueryParams Query(SCENE_QUERY_STAT(P02Passage),false);
  for(AActor* A:Temporary)if(A&&A->IsA<APawn>())Query.AddIgnoredActor(A);
  return World->SweepSingleByChannel(H,C+FVector(-140,0,0),C+FVector(140,0,0),FQuat::Identity,ECC_Pawn,
    FCollisionShape::MakeCapsule(35,90),Query);};
 const FVector Origin(5000,0,1000);auto* D=SpawnDoor(Origin);auto* Other=SpawnDoor(Origin+FVector(700,0,0));
 auto* Player=SpawnPawn(Origin+FVector(-170,0,90));auto* NPC=SpawnPawn(Origin+FVector(700,600,90));
 Check(TEXT("closed_leaf_collision_blocks_capsule"),PassageBlocked(D),D);
 Advance(D,1);Check(TEXT("unbuilt_destination_stays_closed_by_proximity"),D->OpenFraction==0,D);
 Check(TEXT("unbuilt_destination_denies_explicit_request"),!D->RequestOpen(Player),D);
 D->SetDestinationConstructed(true);Advance(D,1);
 Check(TEXT("security_lock_dominates_proximity"),D->OpenFraction==0,D);
 D->SetSecurityLocked(false);Advance(D,1);
 Check(TEXT("external_permission_denial_stays_closed"),D->OpenFraction==0,D);
 D->SetExternalAccessAllowed(true);Advance(D,1);
 Check(TEXT("authorized_player_proximity_opens"),D->OpenFraction>.999f&&D->DoorState==ESTDoorState::Open,D);
 Check(TEXT("open_door_releases_capsule_passage"),!PassageBlocked(D),D);
 Check(TEXT("nearby_door_instances_are_independent"),Other->OpenFraction==0&&PassageBlocked(Other),Other);
 Player->SetActorLocation(Origin+FVector(-600,0,90));NPC->SetActorLocation(Origin+FVector(0,0,90));
 Advance(D,3);Check(TEXT("occupied_doorway_holds_open_for_NPC"),D->OpenFraction>.999f&&D->IsDoorwayOccupied(),D);
 NPC->SetActorLocation(Origin+FVector(0,600,90));Advance(D,1.3f);
 Check(TEXT("delayed_close_waits_after_occupant_leaves"),D->OpenFraction>.999f,D);
 Advance(D,.35f);Check(TEXT("door_starts_closing_after_delay"),D->OpenFraction>0&&D->OpenFraction<1,D);
 NPC->SetActorLocation(Origin+FVector(0,0,90));Advance(D,.05f);
 Check(TEXT("entering_during_close_reverses_motion"),D->ClosingReversalCount>0&&D->DoorState!=ESTDoorState::Closing,D);
 Advance(D,1);Check(TEXT("reversal_returns_fully_open"),D->OpenFraction>.999f,D);
 D->SetSecurityLocked(true);Advance(D,2);
 Check(TEXT("security_lock_does_not_crush_existing_occupant"),D->OpenFraction>.999f,D);
 NPC->SetActorLocation(Origin+FVector(0,600,90));Advance(D,3);
 Check(TEXT("locked_door_closes_after_occupant_leaves"),D->OpenFraction<.001f&&PassageBlocked(D),D);
 D->SetSecurityLocked(false);NPC->SetActorLocation(Origin+FVector(-170,0,90));Advance(D,1);
 Check(TEXT("NPC_proximity_also_opens"),D->OpenFraction>.999f,D);
 NPC->SetActorLocation(Origin+FVector(0,600,90));Advance(D,3);
 Check(TEXT("automatic_close_restores_collision"),D->OpenFraction<.001f&&PassageBlocked(D),D);
 const bool ExplicitAccepted=D->RequestOpen(Player);Advance(D,.85f);
 Check(TEXT("explicit_request_completes_opening_without_nearby_pawn"),ExplicitAccepted&&D->OpenFraction>.999f,D);
 Advance(D,3);Check(TEXT("explicit_request_eventually_closes"),D->OpenFraction<.001f,D);
 auto* Spectator=World->SpawnActor<ASpectatorPawn>(ASpectatorPawn::StaticClass(),FTransform(Origin+FVector(-170,0,90)),Params);
 Temporary.Add(Spectator);
 if(auto* Body=Cast<UPrimitiveComponent>(Spectator->GetRootComponent())){Body->SetCollisionProfileName(TEXT("Pawn"));Body->SetCollisionEnabled(ECollisionEnabled::QueryAndPhysics);}
 Check(TEXT("spectator_explicit_request_is_rejected"),!D->RequestOpen(Spectator),D);
 Advance(D,1);Check(TEXT("spectator_camera_does_not_trigger_door"),D->OpenFraction<.001f,D);Spectator->Destroy();
 auto* Adapter=World->SpawnActor<ASTDoorPermissionFixture>(ASTDoorPermissionFixture::StaticClass(),FTransform(Origin+FVector(1400,0,0)),Params);
 Temporary.Add(Adapter);Adapter->LeftLeaf->SetStaticMesh(LMesh);Adapter->RightLeaf->SetStaticMesh(RMesh);
 Adapter->SetDestinationConstructed(true);Adapter->SetSecurityLocked(false);Adapter->SetExternalAccessAllowed(false);Adapter->ResetClosed();
 const bool AdapterAccepted=Adapter->RequestOpen(Player);Advance(Adapter,.85f);
 Check(TEXT("policy_override_controls_explicit_request_consistently"),AdapterAccepted&&Adapter->OpenFraction>.999f,Adapter);
 Advance(Adapter,3);Adapter->SetDestinationConstructed(false);
 Check(TEXT("destination_safety_dominates_external_policy_override"),!Adapter->RequestOpen(Player)&&Adapter->OpenFraction<.001f,Adapter);
 Adapter->SetDestinationConstructed(true);Adapter->SetSecurityLocked(true);
 Check(TEXT("security_lock_dominates_external_policy_override"),!Adapter->RequestOpen(Player),Adapter);
 // Three unsafe instances cannot be opened even by explicit requests.
 for(int32 I=0;I<3;I++) {
  ASTAutomaticDoor* Unsafe=SpawnDoor(Origin+FVector(0,(I+2)*700,0));
  Unsafe->SetExternalAccessAllowed(true);Unsafe->SetSecurityLocked(false);
  const bool Denied=!Unsafe->RequestOpen(Player);Advance(Unsafe,2);
  FString Name=FString::Printf(TEXT("unsafe_exit_%d_remains_closed"),I+1);
  Check(*Name,Denied&&Unsafe->OpenFraction==0&&PassageBlocked(Unsafe),Unsafe);
 }
 int32 Passed=0;for(const auto& V:Cases)if(V->AsObject()->GetBoolField(TEXT("pass")))Passed++;
 Report->SetArrayField("cases",Cases);Report->SetNumberField("passed",Passed);Report->SetNumberField("total",Cases.Num());
 Report->SetBoolField("all_pass",Passed==Cases.Num());Report->SetStringField("method",TEXT("Editor-world real Chaos queries and swept movable leaves; same AdvanceDoor called by runtime Tick. Not a PIE or human traversal test."));
 for(AActor* A:Temporary)if(IsValid(A))A->Destroy();return ToJson(Report);
}
FString USTAutomaticDoorTestLibrary::AuditLeafPocketClearance(ASTAutomaticDoor* Door) {
 auto O=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Rows;
 if(!Door||!Door->GetWorld()){O->SetStringField("error",TEXT("No door/world"));return ToJson(O);}
 for(int32 I=0;I<2;I++) {
  auto* C=I==0?Door->LeftLeaf.Get():Door->RightLeaf.Get();auto R=MakeShared<FJsonObject>();
  FVector Center,Ext;C->GetLocalBounds(Center,Ext); // API returns min/max, compute center/half extent below.
  const FVector Min=Center,Max=Ext;Center=(Min+Max)/2;Ext=(Max-Min)/2;
  const FVector Start=C->GetComponentTransform().TransformPosition(Center);
  const FVector Delta=Door->GetActorTransform().TransformVectorNoScale(FVector(0,(I==0?-1:1)*Door->TravelDistance,0));
  TArray<FHitResult> Hits;FCollisionQueryParams Q(SCENE_QUERY_STAT(P02Pocket),false,Door);
  Door->GetWorld()->SweepMultiByChannel(Hits,Start,Start+Delta,C->GetComponentQuat(),ECC_Pawn,FCollisionShape::MakeBox(Ext),Q);
  TArray<TSharedPtr<FJsonValue>> Obstacles;
  for(const auto& H:Hits)if(H.bBlockingHit) {
   auto V=MakeShared<FJsonObject>();V->SetStringField("actor",H.GetActor()?H.GetActor()->GetActorLabel():TEXT("None"));
   V->SetNumberField("distance_cm",H.Distance);V->SetBoolField("initial_overlap",H.bStartPenetrating);
   Obstacles.Add(MakeShared<FJsonValueObject>(V));
  }
  R->SetStringField("leaf",I==0?TEXT("Left"):TEXT("Right"));R->SetBoolField("clear",Obstacles.IsEmpty());
  R->SetArrayField("blocking_hits",Obstacles);Rows.Add(MakeShared<FJsonValueObject>(R));
 }
 O->SetArrayField("leaves",Rows);O->SetStringField("method",TEXT("Conservative leaf-bounds sweep against copied F07 fixed collision; no leaf moved and no door unlocked."));return ToJson(O);
}
FString USTAutomaticDoorTestLibrary::RunRigChecks(ASTAutomaticDoor* Door) {
 auto Report=MakeShared<FJsonObject>();TArray<TSharedPtr<FJsonValue>> Cases;
 if(!Door||!Door->GetWorld()){Report->SetStringField("error",TEXT("No rig/world"));return ToJson(Report);}
 const bool IntentWasEnabled=Door->bUsePassageIntent;Door->bUsePassageIntent=true;UWorld* World=Door->GetWorld();FActorSpawnParameters Params;Params.ObjectFlags|=RF_Transient;
 Params.SpawnCollisionHandlingOverride=ESpawnActorCollisionHandlingMethod::AlwaysSpawn;
 auto* Pawn=World->SpawnActor<ACharacter>(ACharacter::StaticClass(),FTransform(Door->GetActorLocation()+FVector(-170,0,90)),Params);
 Pawn->GetCapsuleComponent()->SetCapsuleSize(35,90);Pawn->GetCapsuleComponent()->SetCollisionProfileName(TEXT("Pawn"));
 auto Advance=[&](float S){for(int32 I=0;I<FMath::CeilToInt(S*60);I++)Door->AdvanceDoor(1.f/60);};
 auto Blocked=[&](){FHitResult H;FVector C=Door->GetActorLocation()+FVector(0,0,100);
  FCollisionQueryParams Q(SCENE_QUERY_STAT(P02RealRigPassage),false,Pawn);
  return World->SweepSingleByChannel(H,C+FVector(-140,0,0),C+FVector(140,0,0),FQuat::Identity,ECC_Pawn,FCollisionShape::MakeCapsule(35,90),Q);};
 auto Check=[&](const TCHAR* Name,bool Pass){auto O=MakeShared<FJsonObject>();O->SetStringField("name",Name);O->SetBoolField("pass",Pass);
  O->SetNumberField("open_fraction",Door->OpenFraction);O->SetStringField("state",StaticEnum<ESTDoorState>()->GetNameStringByValue((int64)Door->DoorState));
  Cases.Add(MakeShared<FJsonValueObject>(O));};
 Door->ResetClosed();Check(TEXT("real_rig_closed_passage_blocks"),Blocked());
 Advance(1);Check(TEXT("real_rig_opens_with_floor_and_frame"),Door->OpenFraction>.999f);
 Check(TEXT("real_rig_open_passage_clear"),!Blocked());
 Pawn->SetActorLocation(Door->GetActorLocation()+FVector(0,0,90));Advance(2);
 Check(TEXT("real_rig_occupant_holds_open"),Door->OpenFraction>.999f);
 Pawn->SetActorLocation(Door->GetActorLocation()+FVector(-350,0,90));Advance(3);
 Check(TEXT("real_rig_closes_after_exit"),Door->OpenFraction<.001f&&Blocked());
 Door->ResetClosed();Door->bUsePassageIntent=IntentWasEnabled;Pawn->Destroy();int32 Passed=0;
 for(const auto& V:Cases)if(V->AsObject()->GetBoolField(TEXT("pass")))Passed++;
 Report->SetArrayField("cases",Cases);Report->SetNumberField("passed",Passed);Report->SetNumberField("total",Cases.Num());
 Report->SetBoolField("all_pass",Passed==Cases.Num());return ToJson(Report);
}

