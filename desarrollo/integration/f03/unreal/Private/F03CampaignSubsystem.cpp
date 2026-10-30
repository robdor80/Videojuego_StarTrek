#include "F03CampaignSubsystem.h"
#include "Components/StaticMeshComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "Misc/FileHelper.h"
#include "HAL/FileManager.h"
#include "Misc/Paths.h"
#include "UObject/ConstructorHelpers.h"

AF03LogicalMarker::AF03LogicalMarker() {
    auto* Mesh=CreateDefaultSubobject<UStaticMeshComponent>(TEXT("DiagnosticShip")); SetRootComponent(Mesh);
    static ConstructorHelpers::FObjectFinder<UStaticMesh> Cube(TEXT("/Engine/BasicShapes/Cube.Cube"));
    if(Cube.Succeeded()) Mesh->SetStaticMesh(Cube.Object);
    auto* Label=CreateDefaultSubobject<UTextRenderComponent>(TEXT("CoreState")); Label->SetupAttachment(Mesh);
    Label->SetRelativeLocation(FVector(0,0,130)); Label->SetWorldSize(24); Label->SetTextRenderColor(FColor::Cyan);
}
void AF03LogicalMarker::Refresh(const F03MarkerState& State,uint32 Detail) {
    LogicalId=FString::Printf(TEXT("%llu"),static_cast<unsigned long long>(State.identity)); Location=State.location;
    SetActorLocation(FVector(Location==2 ? 600 : Location==1 ? 0 : 300,State.identity==1 ? -180 : 180,100));
    auto* Mesh=FindComponentByClass<UStaticMeshComponent>(); Mesh->SetRelativeScale3D(Detail ? FVector(2,0.6,0.35) : FVector(0.5));
    FindComponentByClass<UTextRenderComponent>()->SetText(FText::FromString(
        FString::Printf(TEXT("Core ship %s | zone %d | LOD %u"),*LogicalId,Location,Detail)));
}
void UF03CampaignSubsystem::Initialize(FSubsystemCollectionBase& C) { Super::Initialize(C); OpenLab(); }
void UF03CampaignSubsystem::Deinitialize() { CloseLab(); Super::Deinitialize(); }
void UF03CampaignSubsystem::BeginDestroy() { CloseLab(); Super::BeginDestroy(); }
bool UF03CampaignSubsystem::OpenLab() {
    if(!IsInGameThread() || !F03BridgeReady()) return false;
    if(Session) return true;
    if(f03_create(1,2372,&Session)!=F03_OK) return false;
    if(f03_handles(Session,&Handles)!=F03_OK) { CloseLab(); return false; }
    return true;
}
void UF03CampaignSubsystem::ClearVisuals() {
    for(auto& Visual:Visuals) if(Visual.Actor.IsValid()) Visual.Actor->Destroy(); Visuals.Empty();
}
void UF03CampaignSubsystem::CloseLab() {
    if(!Session) return; check(IsInGameThread()); ClearVisuals();
    ensure(f03_destroy(Session)==F03_OK); Session=nullptr; Handles={};
}
F03Ref UF03CampaignSubsystem::Observer(uint32 Id) const { return Id==1 ? Handles.primary : Id==2 ? Handles.secondary : F03Ref{}; }
AF03LogicalMarker* UF03CampaignSubsystem::Represent(UWorld* World,uint32 Ship,uint32 Detail) {
    if(!IsInGameThread() || !Session || !IsValid(World) || World->GetGameInstance()!=GetGameInstance() || Detail>1) return nullptr;
    F03MarkerState State{}; if(f03_marker_state(Session,Observer(Ship),&State)!=F03_OK) return nullptr;
    for(auto& Visual:Visuals) if(Visual.Actor.IsValid() && Visual.Ship==Ship && Visual.Actor->GetWorld()==World) {
        Visual.Detail=Detail; Visual.Actor->Refresh(State,Detail); return Visual.Actor.Get();
    }
    auto* Actor=World->SpawnActor<AF03LogicalMarker>();
    if(Actor) { Actor->Refresh(State,Detail); Visuals.Add({Actor,Ship,Detail}); } return Actor;
}
void UF03CampaignSubsystem::Dematerialize(UWorld* World) {
    if(!IsInGameThread()) return;
    for(int32 I=Visuals.Num()-1;I>=0;--I) {
        auto& V=Visuals[I];
        if(!V.Actor.IsValid() || V.Actor->GetWorld()==World) {
            if(V.Actor.IsValid()) V.Actor->Destroy(); Visuals.RemoveAt(I);
        }
    }
}
bool UF03CampaignSubsystem::ScheduleRoute() { return IsInGameThread() && Session && f03_schedule_route(Session)==F03_OK; }
bool UF03CampaignSubsystem::Advance(uint64 Horizon) {
    if(!IsInGameThread() || !Session) return false;
    uint64_t N{}; if(f03_advance(Session,Horizon,64,&N)!=F03_OK) return false;
    for(auto& Visual:Visuals) if(Visual.Actor.IsValid()) {
        F03MarkerState State{}; if(f03_marker_state(Session,Observer(Visual.Ship),&State)==F03_OK) Visual.Actor->Refresh(State,Visual.Detail);
    }
    return true;
}
bool UF03CampaignSubsystem::Acquire(uint32 Id,uint32 Channel) { return IsInGameThread() && Session && f03_acquire(Session,Observer(Id),Channel)==F03_OK; }
bool UF03CampaignSubsystem::SetPermission(bool Allowed) { return IsInGameThread() && Session && f03_set_permission(Session,Allowed?1:0)==F03_OK; }
bool UF03CampaignSubsystem::View(uint32 Id,TArray<F03Fact>& Out) const {
    if(!IsInGameThread() || !Session) return false;
    F03Fact Facts[32]{}; uint64_t N{};
    if(f03_view(Session,Observer(Id),0,Facts,32,&N)!=F03_OK) return false;
    Out.Reset(); Out.Append(Facts,static_cast<int32>(N)); return true;
}
bool UF03CampaignSubsystem::Save(TArray<uint8>& Out) const {
    if(!IsInGameThread() || !Session) return false;
    uint64_t N{}; if(f03_save(Session,nullptr,0,&N)!=F03_CAPACITY || N>64*1024*1024) return false;
    TArray<uint8> Candidate; Candidate.SetNumUninitialized(static_cast<int32>(N));
    if(f03_save(Session,Candidate.GetData(),N,&N)!=F03_OK) return false; Out=MoveTemp(Candidate); return true;
}
bool UF03CampaignSubsystem::Load(const TArray<uint8>& Bytes) {
    if(!IsInGameThread() || !Session || Bytes.IsEmpty() || f03_load(Session,Bytes.GetData(),Bytes.Num())!=F03_OK) return false;
    ClearVisuals(); return f03_handles(Session,&Handles)==F03_OK;
}
bool UF03CampaignSubsystem::WriteSave(const FString& Path) const {
    if(!IsInGameThread()) return false;
    TArray<uint8> Bytes; return !FPaths::FileExists(Path) && Save(Bytes) && FFileHelper::SaveArrayToFile(Bytes,*Path);
}
bool UF03CampaignSubsystem::ReadSave(const FString& Path) {
    if(!IsInGameThread() || !Session) return false;
    const int64 N=IFileManager::Get().FileSize(*Path); if(N<=0 || N>64*1024*1024) return false;
    TArray<uint8> Bytes; return FFileHelper::LoadFileToArray(Bytes,*Path) && Load(Bytes);
}
bool UF03CampaignSubsystem::Stats(F03Stats& Out) const { return IsInGameThread() && Session && f03_stats(Session,&Out)==F03_OK; }
