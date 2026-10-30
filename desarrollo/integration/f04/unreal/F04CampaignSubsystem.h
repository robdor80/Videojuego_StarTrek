#pragma once
#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "GameFramework/Actor.h"
#include "f04_bridge.h"
#include "F04CampaignSubsystem.generated.h"

UCLASS()
class F02CORELAB_API AF04CrewMarker : public AActor {
 GENERATED_BODY()
public:
 UPROPERTY(VisibleAnywhere,Category="F04 diagnostic") FString LogicalId;
 uint64 CorePersonId=0;
 UPROPERTY(VisibleAnywhere,Category="F04 diagnostic") bool OnDuty=false;
 UPROPERTY(VisibleAnywhere,Category="F04 diagnostic") bool Available=false;
};

UCLASS()
class F02CORELAB_API UF04CampaignSubsystem : public UGameInstanceSubsystem {
 GENERATED_BODY()
public:
 virtual void Deinitialize() override;
 virtual void BeginDestroy() override;
 bool OpenLab();
 bool OpenPopulation(const char* ClassId,const F04PopulationConfig& Config);
 bool InstallOrganization(uint32 TemplateId,uint64 InstalledEquipment);
 bool BootstrapOrganizationFixture();
 bool PlanAlpha(uint64 Start,bool FirstOfficerWatch=true);
 bool Organization(F04OrganizationStats&) const;
 bool Positions(TArray<F04Position>&) const;
 void CloseLab();
 bool Stats(F04Stats&) const;
 uint32 Intent(uint32 Person,uint32 Op,uint64 Target=0,uint64 Aux=0,uint64 Start=0,uint64 End=0,uint32 Value=0,uint64 Cause=42,uint64* Record=nullptr);
 bool Advance(uint64 Tick);
 bool Save(TArray<uint8>&) const;
 bool Load(const TArray<uint8>&);
 AF04CrewMarker* Represent(UWorld*,uint32 Person);
 void Dematerialize(UWorld*);
private:
 F04Session* Session=nullptr;
 F04Handles Handles{};
 TArray<TWeakObjectPtr<AF04CrewMarker>> Visuals;
 void Refresh();
 void ClearVisuals();
};
bool F04BridgeReady();
