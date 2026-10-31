#include "F04CampaignSubsystem.h"
#include "Engine/World.h"
void UF04CampaignSubsystem::Deinitialize(){CloseLab();Super::Deinitialize();}
void UF04CampaignSubsystem::BeginDestroy(){CloseLab();Super::BeginDestroy();}
bool UF04CampaignSubsystem::OpenLab(){
 if(!IsInGameThread() || !F04BridgeReady())return false;
 CloseLab();return f04_create(1,"miranda",&Session)==F04_OK && f04_handles(Session,&Handles)==F04_OK;
}
bool UF04CampaignSubsystem::OpenPopulation(const char* ClassId,const F04PopulationConfig& Config){
 if(!IsInGameThread() || !F04BridgeReady())return false;
 CloseLab();return f04_create_population(1,ClassId,&Config,&Session)==F04_OK && f04_handles(Session,&Handles)==F04_OK;
}
bool UF04CampaignSubsystem::InstallOrganization(uint32 TemplateId,uint64 InstalledEquipment){
 return Intent(static_cast<uint32>(Handles.captain.id),F04_INSTALL_TEMPLATE,0,InstalledEquipment,0,0,TemplateId)==F04_OK;
}
bool UF04CampaignSubsystem::BootstrapOrganizationFixture(){return Intent(static_cast<uint32>(Handles.captain.id),F04_BOOTSTRAP_TEMPLATE)==F04_OK;}
bool UF04CampaignSubsystem::PlanAlpha(uint64 Start,bool FirstOfficerWatch){return Intent(static_cast<uint32>(Handles.captain.id),F04_PLAN_ALPHA,0,FirstOfficerWatch?1:0,Start,Start+28800)==F04_OK;}
bool UF04CampaignSubsystem::PlanWatches(uint64 Start,uint64 End,bool ReferenceDay,bool SeedReference){
 return Intent(static_cast<uint32>(Handles.captain.id),F04_PLAN_WATCHES,0,SeedReference?1:0,Start,End,ReferenceDay?F04_REFERENCE:F04_ROTATING)==F04_OK;
}
bool UF04CampaignSubsystem::ServiceCoverage(uint64 Start,uint64 End,TArray<F04ServiceCoverage>& Out)const{
 Out.Empty();if(!IsInGameThread() || !Session)return false;uint64 Count=0;
 if(f04_service_coverage(Session,Handles.captain,Start,End,nullptr,0,&Count)!=F04_CAPACITY || Count>MAX_int32)return false;
 Out.SetNumUninitialized(static_cast<int32>(Count));return f04_service_coverage(Session,Handles.captain,Start,End,Out.GetData(),Count,&Count)==F04_OK;
}
bool UF04CampaignSubsystem::Organization(F04OrganizationStats& Out)const{return IsInGameThread() && Session && f04_organization_stats(Session,Handles.captain,&Out)==F04_OK;}
bool UF04CampaignSubsystem::Positions(TArray<F04Position>& Out)const{
 Out.Empty();if(!IsInGameThread() || !Session)return false;uint64 Written=0,Total=0;
 if(f04_positions_page(Session,Handles.captain,0,nullptr,0,&Written,&Total)!=F04_OK || Total>MAX_int32)return false;
 Out.SetNumUninitialized(static_cast<int32>(Total));return f04_positions_page(Session,Handles.captain,0,Out.GetData(),Total,&Written,&Total)==F04_OK;
}
void UF04CampaignSubsystem::ClearVisuals(){for(auto V:Visuals)if(V.IsValid())V->Destroy();Visuals.Empty();}
bool UF04CampaignSubsystem::Residents(TArray<F04Resident>& Out)const{
 Out.Empty();if(!IsInGameThread() || !Session)return false;uint64 Written=0,Total=0;
 if(f04_residents_page(Session,Handles.captain,0,nullptr,0,&Written,&Total)!=F04_OK || Total>MAX_int32)return false;
 Out.SetNumUninitialized(static_cast<int32>(Total));return f04_residents_page(Session,Handles.captain,0,Out.GetData(),Total,&Written,&Total)==F04_OK;
}
bool UF04CampaignSubsystem::Specialists(TArray<F04Specialist>& Out)const{
 Out.Empty();if(!IsInGameThread() || !Session)return false;uint64 Written=0,Total=0;
 if(f04_specialists_page(Session,Handles.captain,0,nullptr,0,&Written,&Total)!=F04_OK || Total>MAX_int32)return false;
 Out.SetNumUninitialized(static_cast<int32>(Total));return f04_specialists_page(Session,Handles.captain,0,Out.GetData(),Total,&Written,&Total)==F04_OK;
}
bool UF04CampaignSubsystem::Auxiliary(F04Auxiliary& Out)const{return IsInGameThread() && Session && f04_auxiliary(Session,Handles.captain,&Out)==F04_OK;}
void UF04CampaignSubsystem::CloseLab(){if(!IsInGameThread())return;ClearVisuals();if(Session){f04_destroy(Session);Session=nullptr;}}
bool UF04CampaignSubsystem::Stats(F04Stats& Out)const{return IsInGameThread() && Session && f04_stats(Session,&Out)==F04_OK;}
uint32 UF04CampaignSubsystem::Intent(uint32 Person,uint32 Op,uint64 Target,uint64 Aux,uint64 Start,uint64 End,uint32 Value,uint64 Cause,uint64* Record){
 if(!IsInGameThread() || !Session)return F04_THREAD;
 F04Stats State{};if(!Stats(State))return F04_INTERNAL;
 const F04Request Request{{Handles.captain.scope,Person},State.revision,Op,Value,Target,Aux,Start,End,Cause};
 F04Result Result{};const uint32 Code=f04_execute(Session,&Request,&Result);if(Record)*Record=Result.record;Refresh();return Code;
}
bool UF04CampaignSubsystem::Advance(uint64 Tick){if(!IsInGameThread() || !Session)return false;uint64 Count=0;const bool OK=f04_advance(Session,Tick,4096,&Count)==F04_OK;Refresh();return OK;}
bool UF04CampaignSubsystem::Save(TArray<uint8>& Out)const{
 Out.Empty();if(!IsInGameThread() || !Session)return false;uint64 Size=0;
 if(f04_save(Session,nullptr,0,&Size)!=F04_CAPACITY || Size>MAX_int32)return false;
 Out.SetNumUninitialized(static_cast<int32>(Size));return f04_save(Session,Out.GetData(),Size,&Size)==F04_OK;
}
bool UF04CampaignSubsystem::Load(const TArray<uint8>& Bytes){
 if(!IsInGameThread() || !Session || f04_load(Session,Bytes.GetData(),Bytes.Num())!=F04_OK)return false;
 ClearVisuals();return f04_handles(Session,&Handles)==F04_OK;
}
bool UF04CampaignSubsystem::MigrateHistory(const FString& Directory){
 if(!IsInGameThread() || !Session)return false;const FGuid Id=FGuid::NewGuid();uint8 Bytes[16];static_assert(sizeof(Id)==sizeof(Bytes));FMemory::Memcpy(Bytes,&Id,sizeof(Bytes));
 return f04_history_migrate(Session,TCHAR_TO_UTF8(*Directory),Bytes,16)==F04_OK;
}
bool UF04CampaignSubsystem::OpenHistory(const FString& Directory){
 if(!IsInGameThread() || !Session || f04_history_open(Session,TCHAR_TO_UTF8(*Directory))!=F04_OK)return false;
 ClearVisuals();return f04_handles(Session,&Handles)==F04_OK;
}
bool UF04CampaignSubsystem::PublishHistory(){return IsInGameThread() && Session && f04_history_publish(Session,0)==F04_OK;}
bool UF04CampaignSubsystem::ConsolidateHistory(uint64 Cutoff){return IsInGameThread() && Session && f04_history_consolidate(Session,Cutoff,0)==F04_OK;}
bool UF04CampaignSubsystem::HistoryStats(F04HistoryStats& Out)const{return IsInGameThread() && Session && f04_history_stats(Session,&Out)==F04_OK;}
bool UF04CampaignSubsystem::HistoryPage(uint64 Generation,uint64 After,TArray<F04HistoryFact>& Out,bool& More)const{
 Out.Empty();More=false;if(!IsInGameThread() || !Session)return false;F04HistoryFact Page[256]{};uint64 Written=0;uint32 HasMore=0;
 if(f04_history_page(Session,Handles.captain,Generation,After,Page,256,&Written,&HasMore)!=F04_OK)return false;
 Out.Append(Page,static_cast<int32>(Written));More=HasMore!=0;return true;
}
bool UF04CampaignSubsystem::HistoryRelations(uint64 Generation,uint64 Entity,TArray<F04HistoryRelation>& Out)const{
 Out.Empty();if(!IsInGameThread() || !Session)return false;F04HistoryRelation Page[256]{};uint64 Written=0,Total=0;
 if(f04_history_relations(Session,Handles.captain,Generation,Entity,0,Page,256,&Written,&Total)!=F04_OK || Written!=Total)return false;
 Out.Append(Page,static_cast<int32>(Written));return true;
}
bool UF04CampaignSubsystem::ActiveHistoryCheckpoint(TArray<uint8>& Out)const{
 Out.Empty();if(!IsInGameThread() || !Session)return false;uint64 Size=0;
 if(f04_history_export_active(Session,nullptr,0,&Size)!=F04_CAPACITY || Size>MAX_int32)return false;
 Out.SetNumUninitialized(static_cast<int32>(Size));return f04_history_export_active(Session,Out.GetData(),Size,&Size)==F04_OK;
}
void UF04CampaignSubsystem::Refresh(){
 if(!Session)return;
 f04_handles(Session,&Handles);
 for(auto V:Visuals)if(V.IsValid()) {F04Person Person{};
  if(f04_person(Session,Handles.captain,V->CorePersonId,&Person)!=F04_OK){V->Destroy();continue;}
  V->OnDuty=Person.on_duty!=0;V->Available=Person.available!=0;
 }
}
AF04CrewMarker* UF04CampaignSubsystem::Represent(UWorld* World,uint32 Person){
 if(!IsInGameThread() || !World || !Session)return nullptr;
 F04Person View{};if(f04_person(Session,Handles.captain,Person,&View)!=F04_OK)return nullptr;
 const FString Id=FString::Printf(TEXT("F04:%u"),Person);
 for(auto V:Visuals)if(V.IsValid() && V->GetWorld()==World && V->LogicalId==Id)return V.Get();
 auto* Actor=World->SpawnActor<AF04CrewMarker>();if(!Actor)return nullptr;Actor->LogicalId=Id;Actor->CorePersonId=Person;Visuals.Add(Actor);Refresh();return Actor;
}
void UF04CampaignSubsystem::Dematerialize(UWorld* World){if(!IsInGameThread())return;for(auto V:Visuals)if(V.IsValid() && V->GetWorld()==World)V->Destroy();Visuals.RemoveAll([](auto V){return !V.IsValid();});}
