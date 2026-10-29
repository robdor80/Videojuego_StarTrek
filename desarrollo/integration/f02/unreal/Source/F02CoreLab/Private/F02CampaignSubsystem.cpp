#include "F02CampaignSubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/StaticMesh.h"
#include "Misc/FileHelper.h"
#include "UObject/ConstructorHelpers.h"

AF02LogicalMarker::AF02LogicalMarker() {
    auto* Mesh=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("DiagnosticCube"));
    SetRootComponent(Mesh);
    static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));
    if (Cube.Succeeded()) Mesh->SetStaticMesh(Cube.Object);
    auto* Label=CreateDefaultSubobject<UTextRenderComponent>(TEXT("LogicalIdentity"));
    Label->SetupAttachment(Mesh); Label->SetRelativeLocation(FVector(60,0,100));
    Label->SetHorizontalAlignment(EHTA_Center); Label->SetWorldSize(24);
    Label->SetTextRenderColor(FColor::Cyan);
}
void AF02LogicalMarker::Bind(uint64 Id) {
    LogicalId=FString::Printf(TEXT("%llu"),static_cast<unsigned long long>(Id));
    FindComponentByClass<UTextRenderComponent>()->SetText(FText::FromString(TEXT("Core EntityId = ")+LogicalId));
}
void UF02CampaignSubsystem::Initialize(FSubsystemCollectionBase& C) { Super::Initialize(C); OpenLab(); }
void UF02CampaignSubsystem::Deinitialize() { CloseLab(); Super::Deinitialize(); }
void UF02CampaignSubsystem::BeginDestroy() { CloseLab(); Super::BeginDestroy(); }
bool UF02CampaignSubsystem::OpenLab() {
    if (!IsInGameThread() || !F02BridgeReady()) return false;
    if (Session) return true;
    if (f02_create(1,2372,&Session)!=F02_OK) return false;
    if (f02_handles(Session,&Handles)!=F02_OK) { CloseLab(); return false; }
    return true;
}
void UF02CampaignSubsystem::ClearVisuals() {
    for (auto& Visual:Visuals) if (Visual.IsValid()) Visual->Destroy();
    Visuals.Empty();
}
void UF02CampaignSubsystem::CloseLab() {
    if (!Session) return;
    check(IsInGameThread());
    ClearVisuals();
    ensure(f02_destroy(Session)==F02_OK); Session=nullptr; Handles={};
}
AF02LogicalMarker* UF02CampaignSubsystem::Represent(UWorld* World) {
    if (!IsInGameThread() || !Session || !IsValid(World) || !Exists() || !VerifyProjection()) return nullptr;
    // One live representation per fixture identity and visual world.
    // Overlapping worlds share Core identity, never their temporary Actors.
    for (auto& Visual:Visuals)
        if (Visual.IsValid() && Visual->GetWorld()==World) return Visual.Get();
    auto* Actor=World->SpawnActor<AF02LogicalMarker>(FVector(0,0,80),FRotator::ZeroRotator);
    if (Actor) { Actor->Bind(Handles.subject.id); Visuals.Add(Actor); }
    return Actor;
}
bool UF02CampaignSubsystem::Exists() const {
    if (!IsInGameThread() || !Session) return false;
    uint32_t Value=0; return f02_contains(Session,Handles.subject,&Value)==F02_OK && Value==1;
}
FString UF02CampaignSubsystem::DiagnosticId() const {
    return Exists()? FString::Printf(TEXT("%llu"),static_cast<unsigned long long>(Handles.subject.id)):FString();
}
bool UF02CampaignSubsystem::Place() {
    if (!IsInGameThread() || !Session) return false;
    uint64_t Revision{}; F02ActionResult Result{};
    return f02_revision(Session,&Revision)==F02_OK &&
        f02_place(Session,Handles.subject,Handles.room,Revision,&Result)==F02_OK;
}
bool UF02CampaignSubsystem::Save(TArray<uint8>& Bytes) const {
    if (!IsInGameThread() || !Session) return false;
    uint64_t Size{};
    if (f02_save(Session,nullptr,0,&Size)!=F02_CAPACITY || Size>64*1024*1024) return false;
    TArray<uint8> Candidate; Candidate.SetNumUninitialized(static_cast<int32>(Size));
    if (f02_save(Session,Candidate.GetData(),Size,&Size)!=F02_OK) return false;
    Bytes=MoveTemp(Candidate); return true;
}
bool UF02CampaignSubsystem::Load(const TArray<uint8>& Bytes) {
    if (!IsInGameThread() || !Session || Bytes.IsEmpty()) return false;
    if (f02_load(Session,Bytes.GetData(),Bytes.Num())!=F02_OK) return false;
    // Successful restore invalidates old visual bindings. Failed load preserves them.
    ClearVisuals();
    return f02_handles(Session,&Handles)==F02_OK;
}
bool UF02CampaignSubsystem::WriteSave(const FString& Path) const {
    TArray<uint8> Bytes;
    // Evidence paths are unique per run; never overwrite an existing save.
    return !FPaths::FileExists(Path) && Save(Bytes) && FFileHelper::SaveArrayToFile(Bytes,*Path);
}
bool UF02CampaignSubsystem::ReadSave(const FString& Path) {
    if (!IsInGameThread() || !Session) return false;
    // Bound IO before allocation as well as at the native decode boundary.
    const int64 Size=IFileManager::Get().FileSize(*Path);
    if (Size<=0 || Size>64*1024*1024) return false;
    TArray<uint8> Bytes; return FFileHelper::LoadFileToArray(Bytes,*Path) && Load(Bytes);
}
bool UF02CampaignSubsystem::VerifyProjection() const {
    if (!IsInGameThread() || !Session) return false;
    F02Fact Facts[8]{}; uint64_t Count{};
    if (f02_view(Session,0,Facts,8,&Count)!=F02_OK) return false;
    bool Known=false;
    for (uint64_t I=0;I<Count;++I) {
        if (Facts[I].subject==3 || Facts[I].reference==3) return false;
        Known|=Facts[I].subject==Handles.subject.id && Facts[I].kind==1 && Facts[I].present==1;
    }
    return Known;
}
