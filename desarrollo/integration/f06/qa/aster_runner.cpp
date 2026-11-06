// Live QA runner for Aster. ALL contacts/observations come from the native
// F04/F06 Core campaign. stdout is a compact one-line JSON protocol for Tk.
// No 3D Unreal assets, LLM, fabricated sensor contacts or external world state.
#include "f04_bridge.h"
#include "f06_sensors.h"
#include "f06_bis.h"
#include "f06_autonomy.h"
#include "f06_demo_system_generated.h"
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using U=uint64_t;
static void check(uint32_t result,const char* op) {
 if(result!=F04_OK)throw std::runtime_error(std::string(op)+" returned "+std::to_string(result));
}
struct Watch {
 F04Session* s=nullptr;
 F04Handles h{};
 U event_cursor=0;
 size_t next_frame=0;
 int mode=0;
 std::vector<uint8_t> checkpoint;
 ~Watch(){if(s)f04_destroy(s);}
 F04Stats stats() {
  F04Stats v{};check(f04_stats(s,&v),"stats");return v;
 }
 void op(F04Ref actor,uint32_t code,U target=0,U aux=0,U start=0,U end=0) {
  F04Request q{actor,stats().revision,code,0,target,aux,start,end,42};
  F04Result result{};check(f04_execute(s,&q,&result),"roster");
 }
 void publish(size_t i){
  const auto& frame=F06_DEMO_FRAMES[i];
  F06WorldSnapshot snapshot{stats().revision,frame.source_revision,
    frame.tick,F06_DEMO_OBSERVER_X,F06_DEMO_OBSERVER_Y,F06_DEMO_OBSERVER_Z,
    frame.count,frame.entities};
  F06WorldReceipt receipt{};
  check(f06_host_world_snapshot(s,&snapshot,&receipt),"host world");
 }
 void reset(int new_mode){
  if(s){check(f04_destroy(s),"destroy");s=nullptr;}
  if(new_mode<0 || new_mode>3)throw std::runtime_error("invalid variant");
  mode=new_mode;event_cursor=0;next_frame=0;checkpoint.clear();
  check(f04_create(1,"miranda",&s),"create");
  check(f04_handles(s,&h),"handles");
  // A real F04 console operator is available for optional supervised actions;
  // the automatic computer does NOT depend on that person being present.
  op(h.head,F04_ASSIGN,h.sensors,h.ensign.id);
  op(h.head,F04_DUTY,h.ensign.id,h.sensors,0,28800);
  op(h.ensign,F04_MOVE,h.sensors);
  F06ProfileInstall install{stats().revision,5,0};
  F06ProfileView profile{};
  check(f06_host_install_profile(s,&install,&profile),"modernized Enterprise-D equipment");
  publish(next_frame++);
 }
 void scenario_event(U tick){
  if(mode==2 && (tick==3600 || tick==7200)){
   F06EnvironmentInput in{stats().revision,tick==3600?1u:2u,
      static_cast<uint32_t>(tick==3600?550:0),0,0,0,0,0};
   F06EnvironmentView v{};check(f06_host_environment(s,&in,&v),"interference");
  }
  if(mode==3 && (tick==7200 || tick==9000)){
   F06ArrayInput in{stats().revision,1000,
    static_cast<uint32_t>(tick==7200?0:1000),1000,1,1,1,0};
   F06ArrayView v{};check(f06_host_array_state(s,&in,&v),"array state");
  }
 }
 void advance(U amount) {
  if(amount>28800)throw std::runtime_error("requested step outside watch");
  const U initial=stats().now,target=std::min<U>(28800,initial+amount);
  while(stats().now<target){
   U bound=target;
   if(next_frame<std::size(F06_DEMO_FRAMES))
     bound=std::min(bound,F06_DEMO_FRAMES[next_frame].tick);
   if(mode==2){
    for(U candidate:{U(3600),U(7200)})
     if(candidate>stats().now)bound=std::min(bound,candidate);
   }
   if(mode==3){
    for(U candidate:{U(7200),U(9000)})
     if(candidate>stats().now)bound=std::min(bound,candidate);
   }
   if(bound<=stats().now)throw std::runtime_error("nonprogressive tick");
   U processed=0;
   check(f04_advance(s,bound,4096,&processed),"advance Core");
   scenario_event(bound);
   if(next_frame<std::size(F06_DEMO_FRAMES) &&
      F06_DEMO_FRAMES[next_frame].tick==bound)
     publish(next_frame++);
  }
 }
 void save(){
  U n=0;
  const auto status=f04_save(s,nullptr,0,&n);
  if(status!=F04_CAPACITY || !n)throw std::runtime_error("save length");
  checkpoint.resize(static_cast<size_t>(n));
  check(f04_save(s,checkpoint.data(),n,&n),"save");
 }
 void load(){
  if(checkpoint.empty())throw std::runtime_error("no checkpoint");
  check(f04_load(s,checkpoint.data(),checkpoint.size()),"load");
  check(f04_handles(s,&h),"reload handles");
  next_frame=1;
  const U now=stats().now;
  while(next_frame<std::size(F06_DEMO_FRAMES) &&
     F06_DEMO_FRAMES[next_frame].tick<=now)++next_frame;
  event_cursor=0;
 }
 void prioritize(U contact){
  F06TrackView updated{};
  check(f06_set_tracking(s,h.ensign,stats().revision,contact,
    F06_TRACK_PRIORITY,&updated),"operator priority");
 }
 void emit(){
  F06ComputerStatus state{};
  check(f06_computer_status(s,h.captain,&state),"computer");
  std::array<F06ContactView,64> contacts{};
  U written=0,total=0;
  check(f06_contacts_page(s,h.captain,0,0,contacts.data(),contacts.size(),
    &written,&total),"contacts");
  if(total>contacts.size())throw std::runtime_error("QA contact limit");
  std::array<F06ComputerEvent,128> ev{};
  U event_n=0;uint32_t more=0;
  check(f06_computer_events_page(s,h.captain,event_cursor,ev.data(),ev.size(),
    &event_n,&more),"events");
  if(more)throw std::runtime_error("QA event batch limit");
  if(event_n)event_cursor=ev[event_n-1].event_token;
  std::cout<<"{\"ok\":true,\"tick\":"<<state.tick<<",\"mode\":"<<mode
    <<",\"active\":"<<state.active_contacts
    <<",\"running\":"<<state.analyses_running
    <<",\"completed\":"<<state.analyses_completed
    <<",\"attention\":"<<state.needs_attention
    <<",\"offline\":"<<state.equipment_offline
    <<",\"automatic\":"<<state.autonomous
    <<",\"events\":[";
  for(U i=0;i<event_n;++i){
   if(i)std::cout<<',';
   uint32_t category=0,klass=0;
   for(U j=0;j<written;++j)
    if(contacts[j].contact_id==ev[i].contact_id){
     category=contacts[j].observed_category;
     klass=contacts[j].class_id;break;
    }
   std::cout<<'['<<ev[i].kind<<','<<ev[i].contact_id<<','<<ev[i].tick<<','
    <<category<<','<<klass<<']';
  }
  std::cout<<"],\"contacts\":[";
  for(U i=0;i<written;++i){
   if(i)std::cout<<',';
   const auto& c=contacts[i];
   std::cout<<'['<<c.contact_id<<','<<c.observed_category<<','
     <<c.status<<','<<c.class_id<<']';
  }
  std::cout<<"]}"<<std::endl;
 }
};
int main(){
 Watch watch;
 try{
  watch.reset(0);watch.emit();
  std::string cmd;
  while(std::getline(std::cin,cmd)){
   try{
    const auto n=cmd.find(' ');
    const std::string action=cmd.substr(0,n);
    const std::string arg=n==std::string::npos?"":cmd.substr(n+1);
    if(action=="STEP")watch.advance(std::stoull(arg));
    else if(action=="RESTART")watch.reset(std::stoi(arg));
    else if(action=="SAVE")watch.save();
    else if(action=="LOAD")watch.load();
    else if(action=="PRIORITY")watch.prioritize(std::stoull(arg));
    else if(action=="STATUS"){}
    else throw std::runtime_error("unsupported command");
    watch.emit();
   }catch(const std::exception& e){
    std::cerr<<"QA command: "<<e.what()<<"\n";
    std::cout<<"{\"ok\":false,\"error\":\"No se pudo ejecutar la orden\"}"<<std::endl;
   }
  }
  return 0;
 }catch(const std::exception& e){
  std::cerr<<"QA startup: "<<e.what()<<"\n";
  std::cout<<"{\"ok\":false,\"error\":\"Error inicializando CoreRPG\"}"<<std::endl;
  return 1;
 }
}
