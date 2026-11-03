#include "VH06Probe.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "Components/SkeletalMeshComponent.h"
#include "Dom/JsonObject.h"
#include "Engine/Engine.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "EnhancedPlayerInput.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/SpringArmComponent.h"
#include "InputAction.h"
#include "InputActionValue.h"
#include "Kismet/GameplayStatics.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Misc/CommandLine.h"
#include "Misc/FileHelper.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"
#include "RHI.h"
#include "RHIStats.h"
#include "RenderTimer.h"
#include "Serialization/JsonSerializer.h"
#include "UnrealClient.h"
#include "VHAutomaticDoor.h"
static TArray<TSharedPtr<FJsonValue>> VJ(FVector V)
{
    return {MakeShared<FJsonValueNumber>(V.X), MakeShared<FJsonValueNumber>(V.Y), MakeShared<FJsonValueNumber>(V.Z)};
}
static FVector JV(const TArray<TSharedPtr<FJsonValue>> &A)
{
    return FVector(A[0]->AsNumber(), A[1]->AsNumber(), A[2]->AsNumber());
}
AVH06Probe::AVH06Probe()
{
    PrimaryActorTick.bCanEverTick = true;
    PrimaryActorTick.TickGroup = TG_PostUpdateWork;
}
void AVH06Probe::BeginPlay()
{
    Super::BeginPlay();
    FString File;
    if (!FParse::Value(FCommandLine::Get(), TEXT("VH06Plan="), File) ||
        !FParse::Value(FCommandLine::Get(), TEXT("VH06Report="), ReportPath))
    {
        SetActorTickEnabled(false);
        return;
    }
    FString S;
    if (!FFileHelper::LoadFileToString(S, *File) ||
        !FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(S), Plan))
    {
        SetActorTickEnabled(false);
        return;
    }
    Cases = Plan->GetArrayField(TEXT("cases"));
    Report = MakeShared<FJsonObject>();
    Report->SetStringField(TEXT("method"),
                           TEXT("Official possessed Quinn, EnhancedInput injection, real CharacterMovement, actual "
                                "collision and gravity; teleport only to each case start"));
    Active = true;
    LastWall = FPlatformTime::Seconds();
}
TSharedPtr<FJsonObject> AVH06Probe::Snapshot()
{
    auto O = MakeShared<FJsonObject>();
    FVector P = Pawn->GetActorLocation();
    float H = Pawn->GetCapsuleComponent()->GetScaledCapsuleHalfHeight();
    O->SetArrayField(TEXT("feet_cm"), VJ(P - FVector(0, 0, H)));
    O->SetArrayField(TEXT("velocity"), VJ(Pawn->GetVelocity()));
    O->SetBoolField(TEXT("walkable_floor"), Pawn->GetCharacterMovement()->CurrentFloor.IsWalkableFloor());
    O->SetArrayField(TEXT("movement_floor_normal"),
                     VJ(Pawn->GetCharacterMovement()->CurrentFloor.HitResult.ImpactNormal));
    O->SetNumberField(TEXT("floor_distance"), Pawn->GetCharacterMovement()->CurrentFloor.FloorDist);
    O->SetNumberField(TEXT("body_yaw"), Pawn->GetActorRotation().Yaw);
    O->SetNumberField(TEXT("control_yaw"), PC->GetControlRotation().Yaw);
    O->SetNumberField(TEXT("control_pitch"), PC->GetControlRotation().Pitch);
    O->SetBoolField(TEXT("falling"), Pawn->GetCharacterMovement()->IsFalling());
    FCollisionQueryParams Q;
    Q.AddIgnoredActor(Pawn);
    FHitResult Hit;
    if (GetWorld()->LineTraceSingleByChannel(Hit, P, P - FVector(0, 0, 1000), ECC_Visibility, Q))
    {
        O->SetArrayField(TEXT("floor_cm"), VJ(Hit.ImpactPoint));
        O->SetStringField(TEXT("floor_actor"), (Hit.GetActor() ? Hit.GetActor()->GetActorNameOrLabel() : TEXT("None")));
        O->SetStringField(TEXT("floor_component"), GetNameSafe(Hit.GetComponent()));
        O->SetNumberField(TEXT("floor_instance"), Hit.Item);
    }
    if (GetWorld()->LineTraceSingleByChannel(Hit, P, P + FVector(0, 0, 1000), ECC_Visibility, Q))
    {
        O->SetArrayField(TEXT("ceiling_cm"), VJ(Hit.ImpactPoint));
        O->SetStringField(TEXT("ceiling_actor"),
                          (Hit.GetActor() ? Hit.GetActor()->GetActorNameOrLabel() : TEXT("None")));
        O->SetStringField(TEXT("ceiling_component"), GetNameSafe(Hit.GetComponent()));
        O->SetNumberField(TEXT("ceiling_instance"), Hit.Item);
    }
    FVector D = Pawn->GetVelocity().GetSafeNormal2D();
    if (D.IsNearlyZero())
        D = PC->GetControlRotation().Vector().GetSafeNormal2D();
    if (GetWorld()->SweepSingleByChannel(Hit, P, P + D * 55, FQuat::Identity, ECC_Pawn,
                                         FCollisionShape::MakeCapsule(34.5, H - .5), Q))
    {
        O->SetStringField(TEXT("ahead_actor"), (Hit.GetActor() ? Hit.GetActor()->GetActorNameOrLabel() : TEXT("None")));
        O->SetStringField(TEXT("ahead_component"), GetNameSafe(Hit.GetComponent()));
        O->SetNumberField(TEXT("ahead_instance"), Hit.Item);
        O->SetArrayField(TEXT("ahead_normal"), VJ(Hit.ImpactNormal));
        O->SetArrayField(TEXT("ahead_point"), VJ(Hit.ImpactPoint));
    }
    for (TActorIterator<AVHAutomaticDoor> I(GetWorld()); I; ++I)
    {
        O->SetNumberField(TEXT("door_fraction"), I->OpenFraction);
        O->SetNumberField(TEXT("door_state"), (int32)I->DoorState);
        O->SetBoolField(TEXT("door_occupied"), I->IsDoorwayOccupied());
        O->SetNumberField(TEXT("door_reversals"), I->ClosingReversalCount);
        break;
    }
    auto Cam = Pawn->FindComponentByClass<UCameraComponent>();
    auto Arm = Pawn->FindComponentByClass<USpringArmComponent>();
    if (Cam)
    {
        O->SetArrayField(TEXT("camera_cm"), VJ(Cam->GetComponentLocation()));
        O->SetBoolField(TEXT("camera_blocking_overlap"),
                        GetWorld()->OverlapBlockingTestByChannel(Cam->GetComponentLocation(), FQuat::Identity,
                                                                 ECC_Camera, FCollisionShape::MakeSphere(10), Q));
    }
    if (Arm)
        O->SetNumberField(TEXT("camera_distance"),
                          FVector::Distance(Cam->GetComponentLocation(), Arm->GetComponentLocation()));
    return O;
}
void AVH06Probe::Next()
{
    CaseIndex++;
    if (CaseIndex >= Cases.Num())
    {
        Finish();
        return;
    }
    Current = Cases[CaseIndex]->AsObject();
    PointIndex = 0;
    Elapsed = SampleTime = 0;
    Captured = false;
    MovePause = 0;
    DoneTime = 0;
    Settle = Current->HasField(TEXT("warmup_s")) ? Current->GetNumberField(TEXT("warmup_s")) : 1;
    Travel = PoseChange = 0;
    Trace.Empty();
    Frames.Empty();
    if (Current->HasField(TEXT("step_cm")))
        Pawn->GetCharacterMovement()->MaxStepHeight = Current->GetNumberField(TEXT("step_cm"));
    Start = JV(Current->GetArrayField(TEXT("start")));
    MinFloor = Start.Z;
    for (auto V : Current->GetArrayField(TEXT("points")))
        MinFloor = FMath::Min(MinFloor, (float)JV(V->AsArray()).Z);
    Pawn->SetActorLocation(Start + FVector(0, 0, Pawn->GetCapsuleComponent()->GetScaledCapsuleHalfHeight() + 2.15),
                           false, nullptr, ETeleportType::TeleportPhysics);
    Pawn->GetCharacterMovement()->StopMovementImmediately();
    Pawn->GetCharacterMovement()->SetMovementMode(MOVE_Walking);
    PC->SetControlRotation(FRotator(-15, Current->HasField(TEXT("yaw")) ? Current->GetNumberField(TEXT("yaw")) : 0, 0));
    if (Current->HasField(TEXT("console")))
        PC->ConsoleCommand(Current->GetStringField(TEXT("console")), true);
    Pawn->SetActorRotation(FRotator(0, PC->GetControlRotation().Yaw, 0));
    Previous = Pawn->GetActorLocation();
    LastWall = FPlatformTime::Seconds();
    UE_LOG(LogTemp, Display, TEXT("VH06 CASE %s"), *Current->GetStringField(TEXT("name")));
    for (TActorIterator<AVHAutomaticDoor> I(GetWorld()); I; ++I)
    {
        I->SetEmergencyHoldOpen(false);
        I->SetDestinationConstructed(true);
        I->SetSecurityLocked(false);
        I->SetExternalAccessAllowed(true);
        I->ResetClosed();
        if (Current->HasField(TEXT("locked")))
            I->SetSecurityLocked(Current->GetBoolField(TEXT("locked")));
        if (Current->HasField(TEXT("constructed")))
            I->SetDestinationConstructed(Current->GetBoolField(TEXT("constructed")));
        if (Current->HasField(TEXT("emergency")))
            I->SetEmergencyHoldOpen(Current->GetBoolField(TEXT("emergency")));
    }
}
void AVH06Probe::EndCase(bool Passed, const FString &Reason)
{
    if (Current->HasField(TEXT("key")))
        PC->InputKey(FInputKeyParams(FKey(*Current->GetStringField(TEXT("key"))), IE_Released, 0.0));
    if (Current->HasField(TEXT("door_min")))
        for (TActorIterator<AVHAutomaticDoor> I(GetWorld()); I; ++I)
            Passed &= I->OpenFraction >= Current->GetNumberField(TEXT("door_min"));
    if (Current->HasField(TEXT("door_max")))
        for (TActorIterator<AVHAutomaticDoor> I(GetWorld()); I; ++I)
            Passed &= I->OpenFraction <= Current->GetNumberField(TEXT("door_max"));
    if (Current->HasField(TEXT("min_waypoints")))
        Passed &= PointIndex >= Current->GetNumberField(TEXT("min_waypoints"));
    Passed &= !Pawn->GetCharacterMovement()->IsFalling();
    auto O = Snapshot();
    if (Current->HasField(TEXT("require_close_reopen")))
    {
        bool Closing = false, Reopened = false;
        double Low = 1;
        for (auto V : Trace)
        {
            auto T = V->AsObject();
            double F = T->GetNumberField(TEXT("door_fraction"));
            if (T->GetIntegerField(TEXT("door_state")) == 3 && F > 0 && F < 1)
            {
                Closing = true;
                Low = FMath::Min(Low, F);
            }
            if (Closing && F > Low + .05)
                Reopened = true;
        }
        O->SetBoolField(TEXT("partial_close_then_reopen"), Reopened);
        Passed &= Reopened;
    }
    if (Current->HasField(TEXT("mouse_test")))
        Passed &= FMath::Abs(PC->GetControlRotation().Yaw) > 1 &&
                  FMath::Abs(FMath::FindDeltaAngleDegrees(-15, PC->GetControlRotation().Pitch)) > 1;
    if (Current->HasField(TEXT("expect_actor_prefix")))
    {
        FString Hit;
        O->TryGetStringField(TEXT("ahead_actor"), Hit);
        Passed &= Hit.StartsWith(Current->GetStringField(TEXT("expect_actor_prefix")));
    }
    O->SetStringField(TEXT("name"), Current->GetStringField(TEXT("name")));
    O->SetBoolField(TEXT("passed"), Passed);
    O->SetStringField(TEXT("reason"), Reason);
    O->SetNumberField(TEXT("elapsed_s"), Elapsed);
    O->SetNumberField(TEXT("travel_cm"), Travel);
    O->SetNumberField(TEXT("pose_change_cm"), PoseChange);
    O->SetNumberField(TEXT("waypoints_reached"), PointIndex);
    O->SetArrayField(TEXT("trace"), Trace);
    int32 VX = 0, VY = 0;
    PC->GetViewportSize(VX, VY);
    O->SetNumberField(TEXT("viewport_width"), VX);
    O->SetNumberField(TEXT("viewport_height"), VY);
    O->SetArrayField(TEXT("frames"), Frames);
    Results.Add(MakeShared<FJsonValueObject>(O));
    Next();
}
void AVH06Probe::Finish()
{
    Report->SetArrayField(TEXT("results"), Results);
    FString S;
    FJsonSerializer::Serialize(Report.ToSharedRef(), TJsonWriterFactory<>::Create(&S));
    FFileHelper::SaveStringToFile(S, *ReportPath);
    Active = false;
    FPlatformMisc::RequestExit(false);
}
void AVH06Probe::Tick(float Dt)
{
    Super::Tick(Dt);
    if (!Active)
        return;
    if (!Pawn)
    {
        PC = UGameplayStatics::GetPlayerController(GetWorld(), 0);
        Pawn = PC ? Cast<ACharacter>(PC->GetPawn()) : nullptr;
        if (!Pawn)
            return;
        MoveAction = LoadObject<UInputAction>(nullptr, TEXT("/Game/Input/Actions/IA_Move.IA_Move"));
        auto C = Pawn->GetCapsuleComponent();
        Report->SetNumberField(TEXT("capsule_radius_cm"), C->GetUnscaledCapsuleRadius());
        Report->SetNumberField(TEXT("capsule_half_height_cm"), C->GetUnscaledCapsuleHalfHeight());
        Report->SetStringField(TEXT("mesh"), Pawn->GetMesh()->GetSkinnedAsset()->GetPathName());
        Report->SetStringField(TEXT("animation_class"), Pawn->GetMesh()->GetAnimClass()->GetPathName());
        Report->SetNumberField(TEXT("max_step_cm"), Pawn->GetCharacterMovement()->MaxStepHeight);
        int32 VX = 0, VY = 0;
        PC->GetViewportSize(VX, VY);
        Report->SetNumberField(TEXT("viewport_width"), VX);
        Report->SetNumberField(TEXT("viewport_height"), VY);
        Report->SetStringField(TEXT("player_input_class"), PC->PlayerInput->GetClass()->GetPathName());
        Report->SetNumberField(TEXT("walkable_angle"), Pawn->GetCharacterMovement()->GetWalkableFloorAngle());
        Pawn->GetMesh()->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::AlwaysTickPoseAndRefreshBones;
        Next();
        return;
    }
    if (Settle > 0)
    {
        Settle -= Dt;
        LastBone = Pawn->GetMesh()->GetSocketTransform(TEXT("foot_l"), RTS_Component).GetLocation();
        LastWall = FPlatformTime::Seconds();
        return;
    }
    Elapsed += Dt;
    SampleTime += Dt;
    if (Current->HasField(TEXT("mouse_test")) && Elapsed - Dt < .3f && Elapsed >= .3f)
    {
        PC->InputKey(FInputKeyParams(EKeys::MouseX, 30.0, Dt, 1));
        PC->InputKey(FInputKeyParams(EKeys::MouseY, 20.0, Dt, 1));
    }
    if (Current->HasField(TEXT("jump_at")) && Elapsed - Dt < Current->GetNumberField(TEXT("jump_at")) &&
        Elapsed >= Current->GetNumberField(TEXT("jump_at")))
        Pawn->Jump();
    double Now = FPlatformTime::Seconds();
    double Wall = Now - LastWall;
    LastWall = Now;
    Travel += FVector::Dist2D(Previous, Pawn->GetActorLocation());
    Previous = Pawn->GetActorLocation();
    FVector Bone = Pawn->GetMesh()->GetSocketTransform(TEXT("foot_l"), RTS_Component).GetLocation();
    PoseChange += FVector::Distance(Bone, LastBone);
    LastBone = Bone;
    if (Current->HasField(TEXT("perf")) && Current->GetBoolField(TEXT("perf")))
    {
        auto F = MakeShared<FJsonObject>();
        F->SetNumberField(TEXT("wall_ms"), Wall * 1000);
        F->SetNumberField(TEXT("game_thread_ms"), FPlatformTime::ToMilliseconds(GGameThreadTime));
        F->SetNumberField(TEXT("render_thread_ms"), FPlatformTime::ToMilliseconds(GRenderThreadTime));
        F->SetNumberField(TEXT("gpu_ms"), FPlatformTime::ToMilliseconds(RHIGetGPUFrameCycles()));
        F->SetNumberField(TEXT("draw_calls"), GNumDrawCallsRHI[0]);
        F->SetNumberField(TEXT("primitives"), GNumPrimitivesDrawnRHI[0]);
        FRHIMemoryStats M;
        RHIGetMemoryStats(M);
        F->SetNumberField(TEXT("vram_used_bytes"), M.UsedLocal);
        F->SetNumberField(TEXT("vram_budget_bytes"), M.BudgetLocal);
        Frames.Add(MakeShared<FJsonValueObject>(F));
    }
    if (SampleTime >= .15)
    {
        auto O = Snapshot();
        O->SetNumberField(TEXT("t"), Elapsed);
        Trace.Add(MakeShared<FJsonValueObject>(O));
        SampleTime = 0;
    }
    if (Pawn->GetCharacterMovement()->IsFalling() &&
        Pawn->GetActorLocation().Z - Pawn->GetCapsuleComponent()->GetScaledCapsuleHalfHeight() < MinFloor - 100)
    {
        EndCase(false, TEXT("unsupported_drop"));
        return;
    }
    bool CaptureNow = Elapsed > 1;
    if (Current->HasField(TEXT("capture_at")))
        CaptureNow = FVector::Dist2D(Pawn->GetActorLocation(), JV(Current->GetArrayField(TEXT("capture_at")))) < 45;
    if (Current->HasField(TEXT("screenshot")) && CaptureNow && !Captured)
    {
        FScreenshotRequest::RequestScreenshot(Current->GetStringField(TEXT("screenshot")), false, false);
        Captured = true;
    }
    if (Current->HasField(TEXT("commands")))
    {
        for (auto V : Current->GetArrayField(TEXT("commands")))
        {
            auto C = V->AsObject();
            float T = C->GetNumberField(TEXT("t"));
            if (Elapsed - Dt < T && Elapsed >= T)
                for (TActorIterator<AVHAutomaticDoor> I(GetWorld()); I; ++I)
                {
                    if (C->HasField(TEXT("lock")))
                        I->SetSecurityLocked(C->GetBoolField(TEXT("lock")));
                    if (C->HasField(TEXT("emergency")))
                        I->SetEmergencyHoldOpen(C->GetBoolField(TEXT("emergency")));
                    if (C->HasField(TEXT("constructed")))
                        I->SetDestinationConstructed(C->GetBoolField(TEXT("constructed")));
                    if (C->HasField(TEXT("close")))
                        I->RequestClose();
                }
        }
    }
    MovePause = FMath::Max(0.f, MovePause - Dt);
    auto Points = Current->GetArrayField(TEXT("points"));
    if (PointIndex < Points.Num() && MovePause <= 0)
    {
        FVector Target = JV(Points[PointIndex]->AsArray());
        FVector P = Pawn->GetActorLocation();
        FVector D = Target - P;
        D.Z = 0;
        float Dist = D.Size();
        if (Dist < 20 && FMath::Abs(P.Z - Pawn->GetCapsuleComponent()->GetScaledCapsuleHalfHeight() - Target.Z) < 48)
        {
            if (Current->HasField(TEXT("waypoint_waits")))
                MovePause = Current->GetArrayField(TEXT("waypoint_waits"))[PointIndex]->AsNumber();
            PointIndex++;
            if (Current->HasField(TEXT("key")))
                PC->InputKey(FInputKeyParams(FKey(*Current->GetStringField(TEXT("key"))), IE_Released, 0.0));
        }
        else
        {
            float Yaw = D.Rotation().Yaw;
            if (Current->HasField(TEXT("key")))
            {
                FString K = Current->GetStringField(TEXT("key"));
                if (K == TEXT("S"))
                    Yaw += 180;
                if (K == TEXT("A"))
                    Yaw += 90;
                if (K == TEXT("D"))
                    Yaw -= 90;
                PC->SetControlRotation(FRotator(-15, Yaw, 0));
                PC->InputKey(FInputKeyParams(FKey(*K), IE_Pressed, 1.0));
            }
            else
            {
                PC->SetControlRotation(FRotator(-15, Yaw, 0));
                if (auto Input = Cast<UEnhancedPlayerInput>(PC->PlayerInput))
                    Input->InjectInputForAction(MoveAction,
                                                FInputActionValue(FVector2D(0, FMath::Clamp(Dist / 100.f, .15f, 1.f))));
            }
        }
    }
    float Limit = Current->HasField(TEXT("seconds")) ? Current->GetNumberField(TEXT("seconds")) : 15;
    bool BlockedExpected = Current->HasField(TEXT("expect_blocked")) && Current->GetBoolField(TEXT("expect_blocked"));
    if (PointIndex == Points.Num() && !BlockedExpected && !Current->HasField(TEXT("hold")))
    {
        DoneTime += Dt;
        if (DoneTime > .4f && !Pawn->GetCharacterMovement()->IsFalling())
        {
            EndCase(true, TEXT("walked_all_waypoints_grounded"));
            return;
        }
    }
    if (Elapsed >= Limit)
    {
        EndCase(BlockedExpected ? PointIndex < Points.Num() && !Pawn->GetCharacterMovement()->IsFalling()
                                : PointIndex == Points.Num(),
                BlockedExpected ? TEXT("physical_boundary_test") : TEXT("duration_finished"));
    }
}
