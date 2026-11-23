// Live QA runner for Aster. ALL contacts/observations come from the native
// F04/F06 Core campaign. stdout is a compact one-line JSON protocol for Tk.
// No 3D Unreal assets, LLM, fabricated sensor contacts or external world state.
#include "f04_bridge.h"
#include "f06_sensors.h"
#include "f06_equipment.h"
#include "aster_x1.h"
#include <chrono>
#include <charconv>
#include <fstream>
#include <filesystem>
#include <sstream>
#include "f06_bis.h"
#include "f06_autonomy.h"
#include "f06_demo_system_generated.h"
#include "f06_aster_science_generated.h"
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <cmath>
#include <map>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <vector>

using U=uint64_t;
static U number(const std::string& arg){
 U value=0;const auto parsed=std::from_chars(arg.data(),arg.data()+arg.size(),value);
 if(arg.empty() || parsed.ec!=std::errc{} || parsed.ptr!=arg.data()+arg.size())
  throw std::runtime_error("invalid unsigned argument");
 return value;
}
static void check(uint32_t result,const char* op) {
 if(result!=F04_OK)throw std::runtime_error(std::string(op)+" returned "+std::to_string(result));
}
// QA motion is derived solely from successive PUBLIC Core sensor observations.
// A future F07 tactical console can consume exactly the same read-only feed.
struct NavTrack {
 U tick=0;
 int64_t x=0,y=0,z=0;
 int heading=-1; // projected course from displacement; NOT the vessel's bow.
 int trend=0; // 1 closing, 2 opening, 0 insufficient evidence.
 int intercept=0; // projected closest approach within the safety threshold.
 int cpa=0; // closest projected approach, milli-AU.
 int64_t speed_micro_au_s=0; // 1e-6 AU/s, derived from observed displacement.
 int64_t closing_micro_au_s=0; // positive means approach.
};
struct Watch {
 F04Session* s=nullptr;
 std::map<U,NavTrack> tracks,saved_tracks;
 std::vector<std::array<int64_t,6>> nav_events,saved_nav_events;
 // QA communications ledger: a contact brief sent to the duty officer.
 // It is an actual runner action, not an inert GUI toast or an NPC dialogue.
 std::vector<std::array<U,3>> contact_briefs,saved_contact_briefs;
 F04Handles h{};
 U seed=42,world_revision=0;
 std::map<U,U> physical_revisions;
 std::map<U,std::array<U,4>> latency;
 static U monotonic(){return static_cast<U>(std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::steady_clock::now().time_since_epoch()).count());}
 U event_cursor=0;
 U checkpoint_event_cursor=0;
 size_t next_frame=0;
 int mode=0;
 std::vector<uint8_t> checkpoint;
 std::vector<std::array<U,3>> science_issues;
 ~Watch(){if(s)f04_destroy(s);}
 F04Stats stats() {
  F04Stats v{};check(f04_stats(s,&v),"stats");return v;
 }
 void op(F04Ref actor,uint32_t code,U target=0,U aux=0,U start=0,U end=0) {
  F04Request q{actor,stats().revision,code,0,target,aux,start,end,42};
  F04Result result{};check(f04_execute(s,&q,&result),"roster");
 }
 void install_legacy_physical(const F06DemoFrame& frame){
  for(U i=0;i<frame.count;++i){const auto& e=frame.entities[i];
   if(e.signature_category!=F06_CATEGORY_STARSHIP && e.signature_category!=F06_CATEGORY_SHUTTLE)continue;
   F06PhysicalInput p{};p.expected_revision=stats().revision;p.world_entity_key=e.world_entity_key;
   p.version=1;p.source_revision=1;p.length_m=e.class_id==8?1040:220;
   const std::array<unsigned,6> counts=e.class_id==18?std::array<unsigned,6>{0,0,1,1,1,2}:
      e.class_id==8?std::array<unsigned,6>{8,3,2,1,1,2}:std::array<unsigned,6>{4,2,1,1,1,2};
   for(U k=0;k<6;++k){p.count[k]=counts[k];p.state[k]=counts[k]?1:0;p.visibility_permille[k]=1000;}
   check(f06_host_physical(s,&p),"legacy physical fixture");
  }
 }
 void publish(size_t i){
  const auto& frame=F06_DEMO_FRAMES[i];
  F06WorldSnapshot snapshot{stats().revision,frame.source_revision,
    frame.tick,F06_DEMO_OBSERVER_X,F06_DEMO_OBSERVER_Y,F06_DEMO_OBSERVER_Z,
    frame.count,frame.entities};
  F06WorldReceipt receipt{};
  if(i==0){
   std::vector<F06WorldEntity> inactive(frame.entities,frame.entities+frame.count);
   for(auto& e:inactive)if(e.signature_category==F06_CATEGORY_STARSHIP || e.signature_category==F06_CATEGORY_SHUTTLE)e.active=0;
   auto staging=snapshot;staging.source_revision=frame.source_revision-1;staging.entities=inactive.data();
   check(f06_host_world_snapshot(s,&staging,&receipt),"legacy materialization");
   install_legacy_physical(frame);snapshot.expected_revision=stats().revision;
  }
  check(f06_host_world_snapshot(s,&snapshot,&receipt),"host world");
  update_navigation(frame.tick);
 }
 void update_navigation(U tick) {
  std::array<F06ContactView,64> contacts{};
  U written=0,total=0;
  check(f06_contacts_page(s,h.captain,0,0,contacts.data(),contacts.size(),
    &written,&total),"public navigation contacts");
  if(total>contacts.size())throw std::runtime_error("navigation contact limit");
  constexpr double pi=3.14159265358979323846;
  for(U i=0;i<written;++i){
   const auto& c=contacts[i];
   if(c.status!=F06_ACTIVE ||
      (c.observed_category!=F06_CATEGORY_STARSHIP &&
       c.observed_category!=F06_CATEGORY_SHUTTLE))continue;
   NavTrack now{tick,c.observed_x_milli_au,c.observed_y_milli_au,
                c.observed_z_milli_au,-1,0,0,0};
   auto it=tracks.find(c.contact_id);
   if(it==tracks.end()){tracks.emplace(c.contact_id,now);continue;}
   auto& prior=it->second;
   if(tick<=prior.tick)continue;
   const double dx=double(now.x-prior.x),dy=double(now.y-prior.y),
                dz=double(now.z-prior.z);
   const double moved=std::sqrt(dx*dx+dy*dy+dz*dz);
   if(moved<0.001)continue; // no observed movement means no new trajectory.
   const double old_r=std::sqrt(double(prior.x)*prior.x+
      double(prior.y)*prior.y+double(prior.z)*prior.z);
   const double new_r=std::sqrt(double(now.x)*now.x+
      double(now.y)*now.y+double(now.z)*now.z);
   now.trend=new_r+0.1<old_r?1:new_r>old_r+0.1?2:0;
   const double interval=static_cast<double>(now.tick-prior.tick);
   now.speed_micro_au_s=static_cast<int64_t>(std::llround(
     moved*1000.0/interval));
   now.closing_micro_au_s=static_cast<int64_t>(std::llround(
     (old_r-new_r)*1000.0/interval));
   now.heading=static_cast<int>(std::lround(
     std::fmod(std::atan2(dx,dy)*180.0/pi+360.0,360.0)))%360;
   const double dot=double(now.x)*dx+double(now.y)*dy+double(now.z)*dz;
   const double time_to_closest=-dot/(moved*moved);
   const double cx=now.x+time_to_closest*dx;
   const double cy=now.y+time_to_closest*dy;
   const double cz=now.z+time_to_closest*dz;
   const double closest=std::sqrt(cx*cx+cy*cy+cz*cz);
   now.cpa=static_cast<int>(std::lround(closest));
   // An inbound course can cross a 0.25 AU sphere around our own ship.
   // A heading toward the observer is NOT proof of hostile intention.
   now.intercept=(now.trend==1 && time_to_closest>0.0 &&
                  closest<=250.0)?1:0;
   const int delta=prior.heading<0?0:std::abs(now.heading-prior.heading);
   const bool changed=prior.heading>=0 && std::min(delta,360-delta)>=5;
   int notice=0;
   if(now.intercept && !prior.intercept)notice=2;
   else if(changed)notice=1;
   else if(prior.trend!=now.trend && now.trend==1)notice=3;
   else if(prior.trend!=now.trend && now.trend==2)notice=4;
   if(notice && nav_events.size()<128)
    nav_events.push_back({notice,static_cast<int64_t>(c.contact_id),
      static_cast<int64_t>(tick),now.heading,now.trend,now.intercept});
   prior=now;
  }
 }
 void reset(int new_mode){
  if(new_mode<0 || new_mode>4)throw std::runtime_error("invalid variant");
  if(s){check(f04_destroy(s),"destroy");s=nullptr;}
  mode=new_mode;event_cursor=0;checkpoint_event_cursor=0;next_frame=0;checkpoint.clear();science_issues.clear();
  tracks.clear();saved_tracks.clear();nav_events.clear();saved_nav_events.clear();
  contact_briefs.clear();saved_contact_briefs.clear();
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
  physical_revisions.clear();latency.clear();world_revision=0;
  if(mode==4){publish_x1(0,true);publish_x1(0);initial_scientific_survey();}else{
   publish(next_frame++);
   initial_scientific_survey();
  }
 }
 void publish_x1(U tick,bool materialize=false){
  auto units=aster_x1_units(seed,tick);
  std::vector<F06WorldEntity> entities;
  for(auto e:F06_DEMO_ENTITIES_0){
   if(e.signature_category==F06_CATEGORY_STARSHIP || e.signature_category==F06_CATEGORY_SHUTTLE)continue;
   e.absolute_x_milli_au-=F06_DEMO_OBSERVER_X;e.absolute_y_milli_au-=F06_DEMO_OBSERVER_Y;
   e.absolute_z_milli_au-=F06_DEMO_OBSERVER_Z;if(materialize)e.active=0;entities.push_back(e);
  }
  for(const auto& u:units){auto e=u.world;if(materialize)e.active=0;entities.push_back(e);}
  const U source=monotonic();
  // Install/update all physical configurations BEFORE making entities visible.
  if(!materialize)for(auto& u:units){
   if(physical_revisions[u.world.world_entity_key]==u.physical.source_revision)continue;
   u.physical.expected_revision=stats().revision;
   check(f06_host_physical(s,&u.physical),"physical source");
   physical_revisions[u.world.world_entity_key]=u.physical.source_revision;
  }
  F06WorldSnapshot snapshot{stats().revision,++world_revision,tick,0,0,0,entities.size(),entities.data()};
  F06WorldReceipt receipt{};
  const U received=monotonic();
  check(f06_host_world_snapshot(s,&snapshot,&receipt),"X1 world");
  const U published=monotonic();
  for(const auto& c:visible_contacts())if(c.status==F06_ACTIVE && c.first_seen==tick && !latency.contains(c.contact_id))
   latency[c.contact_id]={tick,source,received,published};
  update_navigation(tick);
  share_tracking();
 }
 void deliver_source(U contact,U source,uint32_t kind,uint32_t recipient){
  // Stable request key is derived from the immutable PUBLIC observation.
  F06EvidenceDeliveryRequest req{stats().revision,(source%900000000000ULL)*16+kind*4+recipient,
    contact,source,recipient,kind};
  F06DeliveryView receipt{};check(f06_deliver_evidence(s,h.ensign,&req,&receipt),"evidence QA queue");
 }
 void share_tracking(){
  // Explicit Core tracking survives process restoration. No Tk dependency.
  // Position evidence every five seconds, equipment changes immediately.
  for(const auto& c:visible_contacts()){
   F06TrackView track{};check(f06_contact_tracking(s,h.captain,c.contact_id,&track),"tracking projection");
   if(!track.mode || c.status!=F06_ACTIVE)continue;
   U n=0,total=0;F06EquipmentView e{};
   check(f06_equipment_page(s,h.captain,c.contact_id,0,nullptr,0,&n,&total),"tracking equipment count");
   if(total){check(f06_equipment_page(s,h.captain,c.contact_id,total-1,&e,1,&n,&total),"tracking equipment");delivery(c.contact_id,2);}
   std::array<F06ResultView,1> prior{};U results=0;
   check(f06_results_page(s,h.captain,c.contact_id,0,nullptr,0,&n,&results),"tracking position count");
   if(results)check(f06_results_page(s,h.captain,c.contact_id,results-1,prior.data(),1,&n,&results),"tracking previous");
   if(results)deliver_source(c.contact_id,prior[0].result_id,2,2);
   const bool moved=!results || prior[0].observed_x_milli_au!=c.observed_x_milli_au ||
      prior[0].observed_y_milli_au!=c.observed_y_milli_au || prior[0].observed_z_milli_au!=c.observed_z_milli_au;
   if(moved && (!results || stats().now>=prior[0].tick+5)){
    focus(c.contact_id);
    check(f06_results_page(s,h.captain,c.contact_id,results,prior.data(),1,&n,&results),"tracking new position");
    if(n)deliver_source(c.contact_id,prior[0].result_id,2,2);
   }
  }
 }
 void delivery(U contact,uint32_t recipient){
  U n=0,total=0;
  check(f06_equipment_page(s,h.captain,contact,0,nullptr,0,&n,&total),"equipment count for delivery");
  if(!total){
   std::array<F06ScienceReportView,32> reports{};U rn=0,rt=0;
   check(f06_science_reports_page(s,h.captain,0,reports.data(),reports.size(),&rn,&rt),"science evidence");
   for(U i=rn;i>0;--i)if(reports[i-1].contact_id==contact){deliver_source(contact,reports[i-1].report_id,3,recipient);return;}
   focus(contact);F06ResultView result{};U count=0;
   check(f06_results_page(s,h.captain,contact,0,nullptr,0,&n,&count),"position evidence count");
   check(f06_results_page(s,h.captain,contact,count-1,&result,1,&n,&count),"position evidence");
   deliver_source(contact,result.result_id,2,recipient);return;
  }
  F06EquipmentView observation{};
  check(f06_equipment_page(s,h.captain,contact,total-1,&observation,1,&n,&total),"latest equipment for delivery");
  F06DeliveryRequest req{stats().revision,(observation.observation_id%900000000000ULL)*4+recipient,contact,recipient,0};
  F06DeliveryView receipt{};check(f06_deliver(s,h.ensign,&req,&receipt),"deliver QA queue");
  if(recipient==1){
   bool known=false;for(const auto& row:contact_briefs)if(row[0]==contact)known=true;
   if(!known)contact_briefs.push_back({contact,receipt.tick,0});
  }
 }
 void file_save(const std::string& path){
  save();std::ofstream f(std::filesystem::u8path(path),std::ios::binary);if(!f)throw std::runtime_error("save open");
  const U header[4]={0x41535445525831ULL,static_cast<U>(mode),seed,checkpoint.size()};
  f.write(reinterpret_cast<const char*>(header),sizeof(header));
  f.write(reinterpret_cast<const char*>(checkpoint.data()),static_cast<std::streamsize>(checkpoint.size()));
  if(!f)throw std::runtime_error("save write");
 }
 void file_load(const std::string& path){
  std::ifstream f(std::filesystem::u8path(path),std::ios::binary);U header[4]{};
  f.read(reinterpret_cast<char*>(header),sizeof(header));
  if(!f || header[0]!=0x41535445525831ULL || header[1]!=4 || !header[3] || header[3]>64000000)
   throw std::runtime_error("invalid QA checkpoint");
  std::vector<uint8_t> bytes(static_cast<size_t>(header[3]));
  f.read(reinterpret_cast<char*>(bytes.data()),static_cast<std::streamsize>(bytes.size()));
  if(!f || f.peek()!=std::char_traits<char>::eof())throw std::runtime_error("truncated/trailing QA checkpoint");
  check(f04_load(s,bytes.data(),bytes.size()),"file load Core");
  checkpoint=std::move(bytes);mode=4;seed=header[2];check(f04_handles(s,&h),"handles");
  synchronize_x1();
 }
 void synchronize_x1(){
  physical_revisions.clear();
  for(const auto& u:aster_x1_units(seed,stats().now))physical_revisions[u.world.world_entity_key]=u.physical.source_revision;
  // The producer's source revision is deterministic: initial inactive + tick 0
  // plus one publication per elapsed second. No re-publication on restoration.
  world_revision=stats().now+2;latency.clear();tracks.clear();nav_events.clear();contact_briefs.clear();
  std::array<F06ComputerEvent,128> events{};U en=0;uint32_t more=0;
  check(f06_computer_events_page(s,h.captain,0,events.data(),events.size(),&en,&more),"restored cursor");
  if(more)throw std::runtime_error("QA restored event capacity");
  event_cursor=en?events[en-1].event_token:0;
  std::array<F06DeliveryView,512> rows{};U n=0,total=0;
  check(f06_deliveries_page(s,h.captain,0,rows.data(),rows.size(),&n,&total),"restored deliveries");
  for(U i=0;i<n;++i)if(rows[i].recipient==1)contact_briefs.push_back({rows[i].contact_id,rows[i].tick,0});
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
  const U initial=stats().now,target=std::min<U>(mode==4?540:28800,initial+amount);
  if(mode==4){
   while(stats().now<target){
    const U tick=stats().now+1;U processed=0;
    check(f04_advance(s,tick,4096,&processed),"advance X1 Core");
    if(tick==450 || tick==465){
     F06ArrayInput in{stats().revision,1000,tick==450?0u:1000u,1000,1,1,1,0};
     F06ArrayView out{};check(f06_host_array_state(s,&in,&out),"X1 equipment outage");
    }
    publish_x1(tick);
   }
   return;
  }
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
   share_tracking();
  }
 }
 void save(){
  U n=0;
  const auto status=f04_save(s,nullptr,0,&n);
  if(status!=F04_CAPACITY || !n)throw std::runtime_error("save length");
  checkpoint.resize(static_cast<size_t>(n));
  check(f04_save(s,checkpoint.data(),n,&n),"save");
  checkpoint_event_cursor=event_cursor;
  saved_tracks=tracks;
  saved_nav_events=nav_events;
  saved_contact_briefs=contact_briefs;
 }
 void load(){
  if(checkpoint.empty())throw std::runtime_error("no checkpoint");
  check(f04_load(s,checkpoint.data(),checkpoint.size()),"load");
  check(f04_handles(s,&h),"reload handles");
  next_frame=1;
  const U now=stats().now;
  while(next_frame<std::size(F06_DEMO_FRAMES) &&
     F06_DEMO_FRAMES[next_frame].tick<=now)++next_frame;
  event_cursor=checkpoint_event_cursor;
  tracks=saved_tracks;
  nav_events=saved_nav_events;
  contact_briefs=saved_contact_briefs;
  if(mode==4)synchronize_x1();
 }
 std::vector<F06ContactView> visible_contacts() {
  std::array<F06ContactView,64> rows{};
  U n=0,total=0;
  check(f06_contacts_page(s,h.captain,0,0,rows.data(),rows.size(),&n,&total),"sensor contact page");
  if(total>rows.size())throw std::runtime_error("QA contact limit");
  return {rows.begin(),rows.begin()+static_cast<std::ptrdiff_t>(n)};
 }
 // QA trusted instrument host. The measurement source is generated from
 // the physical Aster fixture, never read directly by the UI. Every published
 // result must pass native Sensors observation -> Science handoff -> Core report.
 void initial_scientific_survey() {
  for(const auto& contact:visible_contacts()){
   if(contact.status!=F06_ACTIVE || contact.observed_category!=F06_CATEGORY_PLANET)continue;
   const F06WorldEntity* source=nullptr;
   for(const auto& entity:F06_DEMO_ENTITIES_0){
    if(entity.signature_category!=F06_CATEGORY_PLANET)continue;
    const auto expected_x=entity.absolute_x_milli_au-F06_DEMO_OBSERVER_X;
    if(std::llabs(contact.observed_x_milli_au-expected_x)<=100){
     source=&entity;break;
    }
   }
   if(!source){science_issues.push_back({contact.contact_id,1,0});continue;}
   const F06AsterInstrument* instrument=nullptr;
   for(const auto& reading:F06_ASTER_INSTRUMENTS)
    if(reading.key==source->world_entity_key){instrument=&reading;break;}
   if(!instrument){science_issues.push_back({contact.contact_id,2,0});continue;}
   F06ContactView focused{};
   const auto focus_code=f06_focus(s,h.ensign,stats().revision,contact.contact_id,&focused);
   if(focus_code!=F04_OK){science_issues.push_back({contact.contact_id,3,focus_code});continue;}
   std::array<F06ResultView,16> observations{};
   U n=0,total=0;
   if(f06_results_page(s,h.captain,contact.contact_id,0,observations.data(),
       observations.size(),&n,&total)!=F04_OK || !n){
    science_issues.push_back({contact.contact_id,4,0});continue;
   }
   F06ScienceRequest req{stats().revision,770000+source->world_entity_key,
                         contact.contact_id,2,1};
   F06ScienceView handoff{};
   const auto handoff_code=f06_science_handoff(s,h.ensign,&req,&handoff);
   if(handoff_code!=F04_OK){science_issues.push_back({contact.contact_id,5,handoff_code});continue;}
   F06ScienceSample sample{stats().revision,880000+source->world_entity_key,
     handoff.handoff_id,observations[n-1].result_id,
     1000+source->world_entity_key,
     instrument->temp_k,instrument->pressure_mbar,instrument->water_permille,
     instrument->n2_permille,instrument->o2_permille,instrument->co2_permille,
     instrument->solid,instrument->bio,920,0};
   F06ScienceReportView published{};
   // Never display host-only science when the native authorization/evidence
   // check rejects it. In that case the dossier remains unclassified.
   const auto report_code=f06_host_complete_science(s,&sample,&published);
   if(report_code!=F04_OK){
    science_issues.push_back({contact.contact_id,6,report_code});
    std::cerr<<"QA science observation rejected for world key "
      <<source->world_entity_key<<": temp="<<sample.temperature_k
      <<"K, pressure="<<sample.pressure_mbar<<"mbar, water="
      <<sample.water_permille<<", bio="<<sample.biological_evidence
      <<", confidence="<<focused.confidence_permille
      <<", status="<<report_code<<"\n";
   }
  }
 }
 void study(U contact) {
  // Immediate authenticated instrument observation, no artificial clock work.
  // Derived physics is computed by f06_deep_analysis from public Core evidence.
  focus(contact);
 }
 void configure(int preset){
  F06ConfigRequest request{stats().revision,1000,1000,0,0,60,0};
  if(preset==1){request.sensitivity_permille=700;request.resolution_permille=1000;
                request.compensation_permille=150;}
  else if(preset==2){request.sensitivity_permille=700;request.resolution_permille=550;
                     request.compensation_permille=400;}
  else if(preset==3){request.sensitivity_permille=1000;request.resolution_permille=600;
                     request.compensation_permille=150;}
  else if(preset!=0)throw std::runtime_error("invalid sensor configuration");
  request.preset_id=static_cast<uint32_t>(preset);
  F06ConfigView applied{};
  check(f06_configure(s,h.ensign,&request,&applied),"sensor configuration");
 }
 void diagnostics(){
  F06DiagnosticView result{};
  check(f06_run_self_test(s,h.ensign,stats().revision,&result),"sensor diagnostics");
 }
 void focus(U contact){
  F06ContactView updated{};
  check(f06_focus(s,h.ensign,stats().revision,contact,&updated),"operator focus");
 }
 void prioritize(U contact){
  F06TrackView updated{};
  check(f06_set_tracking(s,h.ensign,stats().revision,contact,
    F06_TRACK_PRIORITY,&updated),"operator priority");
  share_tracking();
 }
 void report_contact(U contact){
  // A new measured maneuver is a new reportable situation even when no
  // equipment changed. Identical reports still reuse immutable receipts.
  std::array<F06DeliveryView,512> receipts{};U n=0,total=0,last_tick=0;
  check(f06_deliveries_page(s,h.captain,0,receipts.data(),receipts.size(),&n,&total),"report history");
  bool prior=false;
  for(U i=0;i<n;++i)if(receipts[i].contact_id==contact && receipts[i].recipient==1){prior=true;last_tick=receipts[i].tick;}
  bool changed_course=false;
  for(const auto& event:nav_events)if(static_cast<U>(event[1])==contact && static_cast<U>(event[2])>last_tick)changed_course=true;
  if(prior && changed_course){
   F06EquipmentView e{};U en=0,et=0;
   check(f06_equipment_page(s,h.captain,contact,0,nullptr,0,&en,&et),"report systems count");
   if(et)check(f06_equipment_page(s,h.captain,contact,et-1,&e,1,&en,&et),"report systems");
   if(!et || e.tick<=last_tick){
    focus(contact);F06ResultView position{};U pn=0,pt=0;
    check(f06_results_page(s,h.captain,contact,0,nullptr,0,&pn,&pt),"report position count");
    check(f06_results_page(s,h.captain,contact,pt-1,&position,1,&pn,&pt),"report position");
    deliver_source(contact,position.result_id,2,1);return;
   }
  }
  delivery(contact,1);
 }
 void emit(){
  F06ComputerStatus state{};
  check(f06_computer_status(s,h.captain,&state),"computer");
  F06EnvironmentView environment{};
  check(f06_environment_status(s,h.captain,&environment),"sensor environment");
  F06ConfigView config{};
  check(f06_configuration_status(s,h.captain,&config),"sensor configuration");
  F06DiagnosticView diagnostic{};
  check(f06_diagnostics(s,h.captain,&diagnostic),"sensor diagnostics");
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
    <<",\"duration\":"<<(mode==4?540:28800)
    <<",\"active\":"<<state.active_contacts
    <<",\"running\":"<<state.analyses_running
    <<",\"completed\":"<<state.analyses_completed
    <<",\"attention\":"<<state.needs_attention
    <<",\"offline\":"<<state.equipment_offline
    <<",\"automatic\":"<<state.autonomous
    <<",\"interference_em\":"<<environment.em_permille
    <<",\"environment\":["<<environment.em_permille<<','<<environment.thermal_permille<<','
      <<environment.gravimetric_permille<<','<<environment.subspace_permille<<','<<environment.biological_permille<<']'
    <<",\"config\":["<<config.sensitivity_permille<<','<<config.resolution_permille
      <<','<<config.compensation_permille<<','<<config.preset_id<<','
      <<config.preferred_update_seconds<<']'
    <<",\"diagnostic\":["<<diagnostic.state<<','<<diagnostic.capability_permille
      <<','<<diagnostic.power_permille<<','<<diagnostic.integrity_permille<<']'
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
  std::cout<<"],\"attention_contacts\":[";
  std::array<U,64> attention_ids{};
  U attention_n=0,attention_total=0;
  check(f06_computer_attention_contacts_page(s,h.captain,0,attention_ids.data(),
    attention_ids.size(),&attention_n,&attention_total),"operator attention contacts");
  if(attention_total!=state.needs_attention || attention_total>attention_ids.size())
    throw std::runtime_error("inconsistent public operator attention projection");
  for(U i=0;i<attention_n;++i){
    if(i)std::cout<<',';
    std::cout<<attention_ids[i];
  }
  std::cout<<"],\"scans\":[";
  std::array<F06TimedScanView,256> jobs{};
  U jobs_n=0,jobs_total=0;
  check(f06_timed_scans_page(s,h.captain,0,jobs.data(),jobs.size(),
    &jobs_n,&jobs_total),"timed scan jobs");
  for(U i=0;i<jobs_n;++i){
   if(i)std::cout<<',';
   const auto& j=jobs[i];
   std::cout<<'['<<j.scan_id<<','<<j.contact_id<<','<<j.started_at
    <<','<<j.finishes_at<<','<<j.result_id<<','<<j.status<<']';
  }
  std::cout<<"],\"science\":[";
  std::array<F06ScienceReportView,32> reports{};
  U reports_n=0,reports_total=0;
  check(f06_science_reports_page(s,h.captain,0,reports.data(),reports.size(),
    &reports_n,&reports_total),"science reports");
  if(reports_total>reports.size())throw std::runtime_error("QA report limit");
  for(U i=0;i<reports_n;++i){
   if(i)std::cout<<',';
   const auto& r=reports[i];
   std::cout<<'['<<r.contact_id<<','<<r.planet_class<<','<<r.confidence_permille
    <<','<<r.provisional<<','<<r.temperature_k<<','<<r.pressure_mbar
    <<','<<r.water_permille<<','<<r.nitrogen_permille<<','<<r.oxygen_permille
    <<','<<r.co2_permille<<','<<r.biological_evidence<<']';
  }
  std::cout<<"],\"science_issues\":[";
  for(size_t i=0;i<science_issues.size();++i){
   if(i)std::cout<<',';
   const auto& e=science_issues[i];
   std::cout<<'['<<e[0]<<','<<e[1]<<','<<e[2]<<']';
  }
  // Two most recent immutable Core observations per contact, compared by Core.
  // This is the saved sensor archive, not a GUI-side cache or host-only truth.
  std::cout<<"],\"comparisons\":[";
  bool first_comparison=true;
  for(U i=0;i<written;++i){
   U count=0,total_results=0;
   check(f06_results_page(s,h.captain,contacts[i].contact_id,0,nullptr,0,
     &count,&total_results),"observation count");
   if(total_results<2)continue;
   std::array<F06ResultView,2> last{};
   check(f06_results_page(s,h.captain,contacts[i].contact_id,total_results-2,
     last.data(),last.size(),&count,&total_results),"recent observations");
   if(count!=2)throw std::runtime_error("recent observation page incomplete");
   F06ComparisonView compared{};
   check(f06_compare_results(s,h.captain,last[0].result_id,
     last[1].result_id,&compared),"compare saved Core observations");
   if(!first_comparison)std::cout<<',';
   first_comparison=false;
   std::cout<<'['<<compared.contact_id<<','<<total_results<<','
      <<last[0].tick<<','<<last[1].tick<<','
      <<compared.confidence_delta<<','<<compared.distance_delta_milli_au
      <<','<<compared.class_changed<<']';
  }
  std::cout<<"],\"navigation\":[";
  bool first_nav=true;
  for(U i=0;i<written;++i){
   if(contacts[i].status!=F06_ACTIVE)continue;
   auto it=tracks.find(contacts[i].contact_id);
   if(it==tracks.end() || it->second.heading<0)continue;
   if(!first_nav)std::cout<<',';
   first_nav=false;
   const auto& n=it->second;
   std::cout<<'['<<contacts[i].contact_id<<','<<n.tick<<','<<n.heading
    <<','<<n.trend<<','<<n.intercept<<','<<n.cpa
    <<','<<n.speed_micro_au_s<<','<<n.closing_micro_au_s<<']';
  }
  std::cout<<"],\"navigation_alerts\":[";
  for(size_t i=0;i<nav_events.size();++i){
   if(i)std::cout<<',';
   const auto& a=nav_events[i];
   std::cout<<'['<<a[0]<<','<<a[1]<<','<<a[2]<<','<<a[3]<<','<<a[4]<<','<<a[5]<<']';
  }
  std::cout<<"],\"contact_briefs\":[";
  for(size_t i=0;i<contact_briefs.size();++i){
   if(i)std::cout<<',';
   const auto& brief=contact_briefs[i];
   std::cout<<'['<<brief[0]<<','<<brief[1]<<','<<brief[2]<<']';
  }
  std::cout<<"],\"equipment\":[";
  std::array<F06EquipmentView,512> equipment{};U en=0,et=0;
  check(f06_equipment_page(s,h.captain,0,0,equipment.data(),equipment.size(),&en,&et),"public equipment");
  if(et>equipment.size())throw std::runtime_error("QA equipment capacity");
  for(U i=0;i<en;++i){
   if(i)std::cout<<',';const auto& e=equipment[i];
   std::cout<<"{\"id\":"<<e.observation_id<<",\"contact\":"<<e.contact_id<<",\"tick\":"<<e.tick
    <<",\"class\":"<<e.class_id<<",\"catalog\":"<<e.catalog_version<<",\"length_m\":"<<e.length_m
    <<",\"confidence\":"<<e.confidence_permille<<",\"mask\":"<<e.visible_mask<<",\"slots\":[";
   for(U k=0;k<6;++k){if(k)std::cout<<',';
    std::cout<<'['<<e.count[k]<<','<<e.state[k]<<','<<e.expected[k]<<','<<e.comparison[k]<<']';}
   std::cout<<"]}";
  }
  std::cout<<"],\"deliveries\":[";
  std::array<F06DeliveryView,512> deliveries{};U dn=0,dt=0;
  check(f06_deliveries_page(s,h.captain,0,deliveries.data(),deliveries.size(),&dn,&dt),"public deliveries");
  for(U i=0;i<dn;++i){if(i)std::cout<<',';const auto& d=deliveries[i];
   std::cout<<'['<<d.receipt_id<<','<<d.contact_id<<','<<d.observation_id<<','<<d.tick<<','<<d.recipient<<','<<d.status<<']';}
  std::cout<<"],\"latency\":[";
  bool first_latency=true;
  for(const auto& [contact,l]:latency){if(!first_latency)std::cout<<',';first_latency=false;
   std::cout<<'['<<contact<<','<<l[0]<<','<<l[1]<<','<<l[2]<<','<<l[3]<<']';}
  std::cout<<"],\"contacts\":[";
  for(U i=0;i<written;++i){
   if(i)std::cout<<',';
   const auto& c=contacts[i];
   std::cout<<'['<<c.contact_id<<','<<c.observed_category<<','
     <<c.status<<','<<c.class_id<<','<<c.confidence_permille
     <<','<<c.distance_milli_au<<','<<c.transponder_id<<','<<c.loss_cause
     <<','<<c.observed_x_milli_au<<','<<c.observed_y_milli_au
     <<','<<c.observed_z_milli_au<<','<<c.last_seen<<']';
  }
  std::cout<<"],\"chart_labels\":[";
  bool first_label=true;
  for(U i=0;i<written;++i){const auto& c=contacts[i];if(c.status!=F06_ACTIVE || c.observed_category==1 || c.observed_category==2)continue;
   for(const auto& e:F06_DEMO_ENTITIES_0){
    if(c.observed_category!=e.signature_category ||
      std::llabs(c.observed_x_milli_au-(e.absolute_x_milli_au-F06_DEMO_OBSERVER_X))>10 ||
      std::llabs(c.observed_y_milli_au-(e.absolute_y_milli_au-F06_DEMO_OBSERVER_Y))>10)continue;
    for(const auto& label:F06_CHART_LABELS)if(label.key==e.world_entity_key){
     if(!first_label)std::cout<<',';first_label=false;
     std::cout<<'['<<c.contact_id<<",\""<<label.name<<"\"]";
    }
   }
  }
  std::cout<<"],\"tracking\":[";
  for(U i=0;i<written;++i){if(i)std::cout<<',';F06TrackView track{};
   check(f06_contact_tracking(s,h.captain,contacts[i].contact_id,&track),"public tracking");
   std::cout<<'['<<track.contact_id<<','<<track.mode<<','<<track.updated_at<<']';}
  std::cout<<"],\"deep_analysis\":[";
  for(U i=0;i<written;++i){if(i)std::cout<<',';F06DeepAnalysisView v{};
   check(f06_deep_analysis(s,h.captain,contacts[i].contact_id,&v),"public derived analysis");
   std::cout<<"{\"contact\":"<<v.contact_id<<",\"mask\":"<<v.valid_mask
    <<",\"position_source\":"<<v.position_source<<",\"science_source\":"<<v.science_source
    <<",\"equipment_source\":"<<v.equipment_source<<",\"oxygen_microbar\":"<<v.oxygen_microbar
    <<",\"co2_microbar\":"<<v.co2_microbar<<",\"angular_nanoradian\":"<<v.angular_nanoradian
    <<",\"interval_s\":"<<v.interval_seconds<<",\"displacement_micro_au\":"<<v.displacement_micro_au
    <<",\"equipment_changes\":"<<v.equipment_changes<<'}';}
  std::cout<<"],\"position_evidence\":[";
  std::array<F06ResultView,1024> evidence{};U pn=0,pt=0;
  check(f06_results_page(s,h.captain,0,0,evidence.data(),evidence.size(),&pn,&pt),"public position archive");
  for(U i=0;i<pn;++i){if(i)std::cout<<',';const auto& p=evidence[i];
   std::cout<<'['<<p.result_id<<','<<p.contact_id<<','<<p.tick<<','<<p.observed_x_milli_au
    <<','<<p.observed_y_milli_au<<','<<p.observed_z_milli_au<<']';}
  std::cout<<"]}"<<std::endl;
 }
};
int main(int argc,char** argv){
 Watch watch;
 try{
  watch.reset(argc>1 && std::string(argv[1])=="--x1"?4:0);watch.emit();
  std::string cmd;
  while(std::getline(std::cin,cmd)){
   const auto n=cmd.find(' ');
   const std::string action=cmd.substr(0,n);
   try{
    const std::string arg=n==std::string::npos?"":cmd.substr(n+1);
    if(action=="STEP")watch.advance(number(arg));
    else if(action=="RESTART")watch.reset(number(arg)<=4?static_cast<int>(number(arg)):-1);
    else if(action=="SAVE")watch.save();
    else if(action=="LOAD")watch.load();
    else if(action=="PRIORITY")watch.prioritize(number(arg));
    else if(action=="UNFOLLOW"){
     F06TrackView v{};check(f06_set_tracking(watch.s,watch.h.ensign,watch.stats().revision,
       number(arg),F06_TRACK_PASSIVE,&v),"release tracking");}
    else if(action=="SAVEFILE")watch.file_save(arg);
    else if(action=="LOADFILE")watch.file_load(arg);
    else if(action=="SEED"){watch.seed=number(arg);watch.reset(4);}
    else if(action=="TACTICAL_SEND")watch.delivery(number(arg),2);
    else if(action=="SCIENCE_SEND")watch.delivery(number(arg),3);
    else if(action=="REPORT")watch.report_contact(number(arg));
    else if(action=="FOCUS")watch.focus(number(arg));
    else if(action=="SCAN")watch.study(number(arg));
    else if(action=="CONFIG")watch.configure(number(arg)<=3?static_cast<int>(number(arg)):-1);
    else if(action=="DIAG")watch.diagnostics();
    else if(action=="STATUS" || action=="TACTICAL"){} // same read-only Core feed
    else throw std::runtime_error("unsupported command");
    watch.emit();
   }catch(const std::exception& e){
    std::cerr<<"QA command: "<<e.what()<<"\n";
    // The user receives actionable, safe messages for supported failure
    // conditions, not native exception details or a meaningless generic box.
    const std::string reason=e.what();
    if(action=="SCAN" && (reason.find("Los sensores ya") == 0 ||
                            reason.find("No hay señal") == 0 ||
                            reason.find("La orden no") == 0))
      std::cout<<"{\"ok\":false,\"error\":\""<<reason<<"\"}"<<std::endl;
    else
      std::cout<<"{\"ok\":false,\"error\":\"No se pudo ejecutar la orden; revisa el estado de los sensores.\"}"<<std::endl;
   }
  }
  return 0;
 }catch(const std::exception& e){
  std::cerr<<"QA startup: "<<e.what()<<"\n";
  std::cout<<"{\"ok\":false,\"error\":\"Error inicializando CoreRPG\"}"<<std::endl;
  return 1;
 }
}
