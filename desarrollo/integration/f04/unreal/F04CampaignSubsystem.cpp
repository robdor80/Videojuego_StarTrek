#include "F04CampaignSubsystem.h"
#include "Engine/World.h"
void UF04CampaignSubsystem::Deinitialize(){CloseLab();Super::Deinitialize();}
void UF04CampaignSubsystem::BeginDestroy(){CloseLab();Super::BeginDestroy();}
bool UF04CampaignSubsystem::OpenLab(){
 if(!IsInGameThread() || !F04BridgeReady())return false;
 CloseLab();return f04_create(1,"miranda",&Session)==F04_OK && f04_handles(Session,&Handles)==F04_OK;
}
void UF04CampaignSubsystem::ClearVisuals(){for(auto V:Visuals)if(V.IsValid())V->Destroy();Visuals.Empty();}
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
void UF04CampaignSubsystem::Refresh(){
 if(!Session)return;F04Person People[9]{};uint64 Count=0;
 if(f04_manifest(Session,Handles.captain,People,9,&Count)!=F04_OK)return;
 for(auto V:Visuals)if(V.IsValid())for(uint64 I=0;I<Count;++I)if(V->LogicalId==FString::Printf(TEXT("F04:%llu"),People[I].id)){
  V->OnDuty=People[I].on_duty!=0;V->Available=People[I].available!=0;
 }
}
AF04CrewMarker* UF04CampaignSubsystem::Represent(UWorld* World,uint32 Person){
 if(!IsInGameThread() || !World || !Session)return nullptr;
 F04Person People[9]{};uint64 Count=0;if(f04_manifest(Session,Handles.captain,People,9,&Count)!=F04_OK)return nullptr;
 bool Found=false;for(uint64 I=0;I<Count;++I)Found|=People[I].id==Person;if(!Found)return nullptr;
 const FString Id=FString::Printf(TEXT("F04:%u"),Person);
 for(auto V:Visuals)if(V.IsValid() && V->GetWorld()==World && V->LogicalId==Id)return V.Get();
 auto* Actor=World->SpawnActor<AF04CrewMarker>();if(!Actor)return nullptr;Actor->LogicalId=Id;Visuals.Add(Actor);Refresh();return Actor;
}
void UF04CampaignSubsystem::Dematerialize(UWorld* World){if(!IsInGameThread())return;for(auto V:Visuals)if(V.IsValid() && V->GetWorld()==World)V->Destroy();Visuals.RemoveAll([](auto V){return !V.IsValid();});}
