#include "f06_sensors.h"
#include "f05_orders.h"
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using U=uint64_t;
void ok(bool pass,const char* why){if(!pass)throw std::runtime_error(why);}
struct Lab {
 F04Session* s=nullptr;F04Handles h{};
 Lab(){ok(f04_create(1,"miranda",&s)==F04_OK,"Core session");handles();}
 ~Lab(){if(s)f04_destroy(s);}
 void handles(){ok(f04_handles(s,&h)==F04_OK,"handles");}
 F04Stats stats(){F04Stats x{};ok(f04_stats(s,&x)==F04_OK,"Core stats");return x;}
 F06SignalInput signal(U strength=960,int64_t x=100,U cls=1,U transponder=127) {
  return {stats().revision,0,x,0,0,transponder,static_cast<uint32_t>(strength),0,
   static_cast<uint32_t>(cls),1,F06_EXIT_UNKNOWN,0};
 }
 F06SignalReceipt upsert(F06SignalInput in,uint32_t expected=F04_OK){
  F06SignalReceipt out{};auto got=f06_host_signal(s,&in,&out);
  if(got!=expected){std::cerr<<"upsert expected="<<expected<<" actual="<<got<<"\n";throw std::runtime_error("upsert");}
  return out;
 }
 std::vector<F06ContactView> contacts(uint32_t status=0){
  std::array<F06ContactView,50> a{};U written=0,total=0;
  ok(f06_contacts_page(s,h.captain,status,0,a.data(),a.size(),&written,&total)==F04_OK,"contacts page");
  ok(written==total,"all contacts fit");
  return {a.begin(),a.begin()+static_cast<long>(written)};
 }
 std::vector<F06NoticeView> notices(){
  std::array<F06NoticeView,50> a{};U written=0;uint32_t more=0;
  ok(f06_notices_page(s,h.captain,0,a.data(),a.size(),&written,&more)==F04_OK,"notices page");
  ok(!more,"all notices fit");
  return {a.begin(),a.begin()+static_cast<long>(written)};
 }
 std::vector<uint8_t> save(){
  U n=0;ok(f04_save(s,nullptr,0,&n)==F04_CAPACITY && n,"save length");
  std::vector<uint8_t> data(n);ok(f04_save(s,data.data(),n,&n)==F04_OK,"save");
  return data;
 }
 void load(const std::vector<uint8_t>& bytes){
  ok(f04_load(s,bytes.data(),bytes.size())==F04_OK,"load");
  handles();
 }
 void op(F04Ref who,uint32_t op,U target=0,U aux=0,U start=0,U end=0,U value=0){
  F04Request q{who,stats().revision,op,static_cast<uint32_t>(value),target,aux,start,end,42};
  F04Result result{};auto code=f04_execute(s,&q,&result);
  if(code!=F04_OK){std::cerr<<"f04 op="<<op<<" result="<<code<<"\n";throw std::runtime_error("F04 setup");}
 }
 void ready(){
  op(h.head,F04_ASSIGN,h.sensors,h.ensign.id);
  op(h.head,F04_DUTY,h.ensign.id,h.sensors,0,28800);
  op(h.ensign,F04_MOVE,h.sensors);
 }
 void advance(U tick){U n=0;ok(f04_advance(s,tick,4096,&n)==F04_OK,"Core advance");}
};
void run(const std::string& scenario){
 Lab l;
 if(scenario=="quiet") {
  l.advance(28800);ok(l.contacts().empty() && l.notices().empty(),"quiet eight-hour watch cannot spawn encounters");
 } else if(scenario=="detection") {
  l.upsert(l.signal());auto contacts=l.contacts();auto notices=l.notices();
  ok(contacts.size()==1 && contacts[0].status==F06_ACTIVE,"real materialized signature detected");
  ok(contacts[0].class_id==1 && contacts[0].transponder_id==127,"resolved class and transponder");
  ok(notices.size()==2 && notices[0].kind==F06_NEW_CONTACT && notices[1].kind==F06_IDENTIFIED,"significant events");
  const auto checkpoint=l.save();l.advance(0);ok(l.notices().size()==2,"no repeated alert");
  ok(checkpoint==l.save(),"same instant and world cannot mutate");
 } else if(scenario=="partial") {
  l.upsert(l.signal(580,5000,4,999));
  const auto contact=l.contacts();
  ok(contact.size()==1 && contact[0].status==F06_ACTIVE,"partial detection");
  ok(contact[0].class_id==0 && contact[0].transponder_id==0,"no hidden identity leakage");
  ok(contact[0].confidence_permille<750,"partial is uncertain");
 } else if(scenario=="loss") {
  auto world=l.signal();auto receipt=l.upsert(world);auto previous=l.contacts()[0];
  world.signal_id=receipt.signal_id;world.expected_revision=l.stats().revision;world.active=0;
  l.upsert(world);ok(l.contacts(F06_ACTIVE).empty(),"lost not in active view");
  const auto lost=l.contacts(F06_LOST);
  ok(lost.size()==1 && lost[0].contact_id==previous.contact_id,"same identity in lost archive");
  ok(lost[0].loss_cause==F06_EXIT_UNKNOWN,"no imagined warp/destruction");
  auto notices=l.notices();ok(notices.back().kind==F06_ANOMALOUS_LOSS,"unexplained strong loss alerts");
 } else if(scenario=="reacquire") {
  auto world=l.signal();auto receipt=l.upsert(world);auto first=l.contacts()[0].contact_id;
  world.signal_id=receipt.signal_id;world.expected_revision=l.stats().revision;world.active=0;l.upsert(world);
  world.expected_revision=l.stats().revision;world.active=1;l.upsert(world);
  ok(l.contacts(F06_ACTIVE).size()==1 && l.contacts(F06_ACTIVE)[0].contact_id==first,"reacquisition preserves contact");
  ok(l.notices().back().kind==F06_REACQUIRED,"reacquired only after real world return");
 } else if(scenario=="focused") {
  l.ready();l.upsert(l.signal(580,5000,4,999));
  auto before=l.contacts()[0];ok(before.class_id==0,"weak is unidentified");
  F06ContactView out{};
  ok(f06_focus(l.s,l.h.ensign,l.stats().revision,before.contact_id,&out)==F04_OK,"focused authorized");
  ok(out.class_id==4 && out.transponder_id==999,"focused observation improves knowledge");
 } else if(scenario=="stale") {
  auto input=l.signal();auto before=l.save();
  input.expected_revision=0;ok(l.upsert(input,F04_STALE).signal_id==0,"stale denied");
  ok(before==l.save(),"denied materialization atomic");
 } else if(scenario=="unauthorized") {
  l.upsert(l.signal());auto before=l.save();
  F06ContactView result{};const U id=l.contacts()[0].contact_id;
  ok(f06_focus(l.s,l.h.captain,l.stats().revision,id,&result)==F04_QUALIFICATION,"captain not sensor operator");
  ok(before==l.save(),"denied focus changes nothing");
  auto invalid=l.h.captain;invalid.scope++;
  U total=0,written=0;ok(f06_contacts_page(l.s,invalid,0,0,nullptr,0,&written,&total)==F04_DENIED,"scope enforced");
 } else if(scenario=="save_load") {
  l.upsert(l.signal());auto before=l.contacts();auto bytes=l.save();
  l.load(bytes);
  ok(l.contacts().size()==before.size() && l.contacts()[0].contact_id==before[0].contact_id,"Core persistent dossier");
  ok(l.save()==bytes,"byte-identical Core roundtrip");
 } else if(scenario=="degraded") {
  l.ready();l.upsert(l.signal());
  F06ArrayView initial{};
  ok(f06_array_status(l.s,l.h.ensign,&initial)==F04_OK &&
     initial.power_permille==1000 && initial.long_enabled,"initial matrix nominal");
  auto id=l.contacts()[0].contact_id;
  F06ArrayInput disabled{l.stats().revision,1000,0,1000,1,1,1,0};
  F06ArrayView affected{};
  ok(f06_host_array_state(l.s,&disabled,&affected)==F04_OK && !affected.power_permille,
     "power outage committed in Core");
  auto lost=l.contacts(F06_LOST);
  ok(lost.size()==1 && lost[0].loss_cause==F06_EXIT_SENSOR_OFFLINE,
     "known matrix outage does not invent cloaking");
  ok(l.notices().back().kind==F06_CONTACT_LOST,"no anomalous loss due to known outage");
  F06ContactView focal{};
  ok(f06_focus(l.s,l.h.ensign,l.stats().revision,id,&focal)==F04_UNAVAILABLE,
     "focused scan forbidden without matrix power");
  auto snapshot=l.save();
  l.load(snapshot);ok(l.contacts(F06_LOST).size()==1,"hardware and loss persist");
  disabled.expected_revision=l.stats().revision;disabled.power_permille=1000;
  ok(f06_host_array_state(l.s,&disabled,&affected)==F04_OK,"restore power");
  ok(l.contacts(F06_ACTIVE).size()==1 && l.contacts()[0].contact_id==id,
     "reacquisition after actual repair preserves contact identity");
 } else if(scenario=="power_queue") {
  l.ready();
  F06PowerRequest request{l.stats().revision,8010,180,900};
  F06PowerView view{};auto before=l.save();
  ok(f06_request_power(l.s,l.h.captain,&request,&view)==F04_QUALIFICATION,
     "captain cannot impersonate sensor officer");
  ok(before==l.save(),"denied request changes nothing");
  ok(f06_request_power(l.s,l.h.ensign,&request,&view)==F04_OK &&
    view.request_id && view.state==F06_POWER_QUEUED,"queued Core request");
  F06ArrayView array{};
  ok(f06_array_status(l.s,l.h.captain,&array)==F04_OK &&
     array.power_permille==1000,"request cannot change actual power");
  auto saved=l.save();const U id=view.request_id;
  ok(f06_request_power(l.s,l.h.ensign,&request,&view)==F04_OK &&
     view.request_id==id && l.save()==saved,"idempotent request");
  ok(f06_decide_power(l.s,l.h.ensign,l.stats().revision,id,
     F06_POWER_APPROVED,&view)==F04_DENIED,"sensor officer cannot approve power");
  ok(f06_decide_power(l.s,l.h.captain,l.stats().revision,id,
     F06_POWER_APPROVED,&view)==F04_OK && view.state==F06_POWER_APPROVED,
     "commander approves request");
  ok(f06_array_status(l.s,l.h.captain,&array)==F04_OK &&
     array.power_permille==1000,"approval not fabricated power grant");
  saved=l.save();l.load(saved);
  F06PowerView rows[4]{};U count=0,total=0;
  ok(f06_power_requests_page(l.s,l.h.captain,0,rows,4,&count,&total)==F04_OK &&
     count==1 && total==1 && rows[0].state==F06_POWER_APPROVED,
     "power request persists across Core save/load");
  F06PowerRequest due{l.stats().revision,8011,100,10};
  ok(f06_request_power(l.s,l.h.ensign,&due,&view)==F04_OK,"second request");
  l.advance(30);
  count=total=0;
  ok(f06_power_requests_page(l.s,l.h.captain,0,rows,4,&count,&total)==F04_OK &&
     total==2 && rows[1].state==F06_POWER_EXPIRED,
     "pending power request expires on Core clock");
 } else if(scenario=="tracking") {
  l.ready();auto first=l.upsert(l.signal());
  const auto id=l.contacts()[0].contact_id;
  F06TrackView before{};
  ok(f06_tracking_status(l.s,l.h.ensign,&before)==F04_OK &&
     before.mode==0 && before.used_slots==0 && before.available_slots>=15,"nominal finite capacity");
  F06TrackView view{};
  ok(f06_set_tracking(l.s,l.h.captain,l.stats().revision,id,F06_TRACK_PRIORITY,&view)==F04_QUALIFICATION,
     "captain cannot control sensor tracking without post");
  ok(f06_set_tracking(l.s,l.h.ensign,l.stats().revision,id,F06_TRACK_NORMAL,&view)==F04_OK &&
     view.mode==F06_TRACK_NORMAL && view.used_slots==1,"normal tracking allocated");
  auto checkpoint=l.save();
  ok(f06_set_tracking(l.s,l.h.ensign,0,id,F06_TRACK_NORMAL,&view)==F04_OK &&
     checkpoint==l.save(),"idempotent already-allocated tracking does not mutate");
  ok(f06_set_tracking(l.s,l.h.ensign,l.stats().revision,id,F06_TRACK_PRIORITY,&view)==F04_OK &&
     view.used_slots==3,"priority tracking costs 3 slots");
  for(int i=0;i<5;++i) {
   auto world=l.signal(960,100+static_cast<int64_t>(i+1)*20,1,128+i);
   l.upsert(world);
   const auto candidates=l.contacts();
   const U latest=candidates.back().contact_id;
   F06TrackView quota{};
   const auto code=f06_set_tracking(l.s,l.h.ensign,l.stats().revision,latest,F06_TRACK_PRIORITY,&quota);
   if(i<4)ok(code==F04_OK,"priority within budget");
   else ok(code==F04_CAPACITY,"priority overload denied atomically");
  }
  auto snapshot=l.save();l.load(snapshot);
  F06TrackView stats{};
  ok(f06_tracking_status(l.s,l.h.captain,&stats)==F04_OK &&
     stats.used_slots==15 && !stats.overloaded,"persistent tracking survives Core save/load");
  auto world=l.signal();world.signal_id=first.signal_id;world.expected_revision=l.stats().revision;world.active=0;
  l.upsert(world);ok(l.contacts(F06_LOST).size()==1,"old target lost");
  ok(f06_tracking_status(l.s,l.h.captain,&stats)==F04_OK && stats.used_slots==12,
     "lost contact releases dedicated tracking budget automatically");
 } else if(scenario=="tracking_capacity_recovery") {
  l.ready();l.upsert(l.signal());
  for(int i=0;i<4;++i)l.upsert(l.signal(960,120+20*i,1,128+i));
  const auto all_contacts=l.contacts();
  ok(all_contacts.size()==5,"five independently observed contacts");
  for(const auto& c:all_contacts) {
   F06TrackView selected{};
   ok(f06_set_tracking(l.s,l.h.ensign,l.stats().revision,c.contact_id,
     F06_TRACK_PRIORITY,&selected)==F04_OK,"allocate dedicated tracking while nominal");
  }
  F06TrackView current{};
  ok(f06_tracking_status(l.s,l.h.captain,&current)==F04_OK &&
    current.used_slots==15 && current.available_slots==1 && !current.overloaded,
    "available slots must be the unallocated remainder, not nominal capacity");
  F06ArrayInput degraded{l.stats().revision,500,1000,1000,1,1,1,0};
  F06ArrayView hardware{};
  ok(f06_host_array_state(l.s,&degraded,&hardware)==F04_OK,
    "trusted host materializes damaged sensor capacity");
  ok(l.contacts(F06_ACTIVE).size()==5,
    "partial damage must not invent lost contacts while they remain detectable");
  ok(f06_tracking_status(l.s,l.h.captain,&current)==F04_OK &&
    current.used_slots==15 && current.available_slots==0 && current.overloaded,
    "overcommitted hardware reports no free slots and explicit overload");
  F06TrackView changed{};
  const U first=all_contacts.front().contact_id;
  ok(f06_set_tracking(l.s,l.h.ensign,l.stats().revision,first,
    F06_TRACK_NORMAL,&changed)==F04_OK &&
    changed.used_slots==13 && !changed.available_slots && changed.overloaded,
    "reducing priority always frees slots even while still overloaded");
  auto checkpoint=l.save();
  ok(f06_set_tracking(l.s,l.h.ensign,l.stats().revision,first,
    F06_TRACK_PRIORITY,&changed)==F04_CAPACITY && l.save()==checkpoint,
    "increasing resource use above hardware capacity is denied atomically");
  for(size_t i=1;i<=2;++i)
   ok(f06_set_tracking(l.s,l.h.ensign,l.stats().revision,
     all_contacts[i].contact_id,F06_TRACK_PASSIVE,&changed)==F04_OK,
     "progressive release must be allowed even if intermediate result remains overloaded");
  ok(f06_tracking_status(l.s,l.h.captain,&current)==F04_OK &&
    current.used_slots==7 && current.available_slots==1 && !current.overloaded,
    "releasing resource slots clears overload with accurate free capacity");
  checkpoint=l.save();l.load(checkpoint);
  ok(f06_tracking_status(l.s,l.h.captain,&current)==F04_OK &&
    current.used_slots==7 && current.available_slots==1 && !current.overloaded,
    "hardware degradation and recovered tracking budget persist across Core save/load");
 } else if(scenario=="notices_cursor") {
  l.upsert(l.signal());
  F06NoticeView rows[1]{};U written=0;uint32_t more=0;
  ok(f06_notices_page(l.s,l.h.captain,0,rows,1,&written,&more)==F04_OK &&
     written==1 && more && rows[0].kind==F06_NEW_CONTACT,"first opaque notice");
  const U cursor=rows[0].event_id;
  written=0;more=0;
  ok(f06_notices_page(l.s,l.h.captain,cursor,rows,1,&written,&more)==F04_OK &&
     written==1 && !more && rows[0].kind==F06_IDENTIFIED,
     "opaque cursor fetches next notice without Core entity IDs");
  const U next=rows[0].event_id;
  written=0;more=0;
  ok(f06_notices_page(l.s,l.h.captain,next,rows,1,&written,&more)==F04_OK &&
     !written && !more,"cursor at end of stream");
  ok(f06_notices_page(l.s,l.h.captain,UINT64_MAX,rows,1,&written,&more)==F04_ARGUMENT,
     "forged notice cursor is invalid");
 } else if(scenario=="area_scan") {
  l.ready();l.upsert(l.signal(280,5000,4,999));
  ok(l.contacts().empty(),"weak signal genuinely below passive threshold");
  F06AreaRequest req{l.stats().revision,5000,0,0,1000,0};
  F06AreaReceipt result{};
  auto snap=l.save();
  ok(f06_scan_area(l.s,l.h.captain,&req,&result)==F04_QUALIFICATION,
     "only qualified Sensors operator may focus volume");
  ok(snap==l.save(),"rejection without mutation or leaked contact");
  req.center_x_milli_au=10000;
  ok(f06_scan_area(l.s,l.h.ensign,&req,&result)==F04_OK &&
     !result.observed_contacts && !result.new_contacts && l.contacts().empty(),
     "wrong area cannot reveal unobserved source");
  req.center_x_milli_au=5000;req.expected_revision=l.stats().revision;
  ok(f06_scan_area(l.s,l.h.ensign,&req,&result)==F04_OK &&
     result.observed_contacts==1 && result.new_contacts==1,"focused area discovers signal");
  auto contact=l.contacts();
  ok(contact.size()==1 && !contact[0].class_id && !contact[0].transponder_id,
     "area scan preserves limited identification");
  req.expected_revision=l.stats().revision;
  ok(f06_scan_area(l.s,l.h.ensign,&req,&result)==F04_OK &&
     result.observed_contacts==1 && !result.new_contacts,"no duplicate dossier");
 } else if(scenario=="f05_order") {
  l.ready();l.upsert(l.signal(280,5000,4,999));
  ok(l.contacts().empty(),"passive signal invisible before authorized order");
  F05OrderRequest q{l.h.captain,l.h.ensign,l.h.ship,
    {l.h.ship.scope,l.h.sensors},3001,l.stats().revision,100,50501,F04_SCAN,0};
  F05Receipt r{};
  ok(f05_submit(l.s,&q,&r)==F04_OK && r.state==F05_ISSUED,
     "captain submits Core F05 order");
  ok(l.contacts().empty(),"request cannot cause scan");
  ok(f05_receive(l.s,l.h.ensign,l.stats().revision,r.order,&r)==F04_OK &&
     r.state==F05_ACCEPTED,"sensor operator acknowledges order");
  ok(l.contacts().empty(),"acknowledge cannot cause scan");
  ok(f05_execute_order(l.s,l.h.ensign,l.stats().revision,r.order,&r)==F04_OK &&
     r.state==F05_COMPLETED,"F05 authorized order actually executed");
  auto observed=l.contacts();
  ok(observed.size()==1 && observed[0].status==F06_ACTIVE &&
     !observed[0].class_id && !observed[0].transponder_id,
     "F05 scan observes weaker signal but does not leak identity");
  const auto saved=l.save();
  ok(f05_execute_order(l.s,l.h.ensign,0,r.order,&r)==F04_OK &&
     saved==l.save(),"replayed F05 order does not scan twice");
 } else if(scenario=="results_compare") {
  l.ready();const auto source=l.upsert(l.signal(500,5000,4,999));
  const U id=l.contacts()[0].contact_id;
  F06ContactView inspected{};
  ok(f06_focus(l.s,l.h.ensign,l.stats().revision,id,&inspected)==F04_OK,
    "first focused readout");
  F06ResultView results[4]{};U n=0,total=0;
  ok(f06_results_page(l.s,l.h.captain,id,0,results,4,&n,&total)==F04_OK &&
     n==1 && total==1 && !results[0].class_id,
     "first observed snapshot has no invented Defiant identity");
  const U first=results[0].result_id;
  auto world=l.signal(960,5000,4,999);
  world.signal_id=source.signal_id;
  world.expected_revision=l.stats().revision;
  l.upsert(world); // update the exact same source; never add a second ship
  ok(f06_focus(l.s,l.h.ensign,l.stats().revision,id,&inspected)==F04_OK,
    "second focused readout");
  n=total=0;
  ok(f06_results_page(l.s,l.h.captain,id,0,results,4,&n,&total)==F04_OK &&
    n==2 && total==2,"two immutable results recorded");
  F06ComparisonView comparison{};
  ok(f06_compare_results(l.s,l.h.captain,first,results[1].result_id,&comparison)==F04_OK &&
     comparison.contact_id==id,"comparative readout uses public IDs");
  auto saved=l.save();l.load(saved);
  ok(f06_compare_results(l.s,l.h.captain,first,results[1].result_id,&comparison)==F04_OK,
    "comparison persists through Core save/load");
  ok(f06_compare_results(l.s,l.h.captain,first,UINT64_MAX,&comparison)==F04_UNAVAILABLE,
    "unknown result id cannot address Core internals");
 } else if(scenario=="configuration") {
  l.ready();
  F06ConfigView current{};
  ok(f06_configuration_status(l.s,l.h.captain,&current)==F04_OK &&
    current.sensitivity_permille==1000 && current.resolution_permille==1000,
    "legacy configurations nominal until explicitly installed");
  const auto original=l.save();
  F06ConfigRequest invalid{l.stats().revision,1000,1000,500,1,20,0};
  ok(f06_configure(l.s,l.h.ensign,&invalid,&current)==F04_ARGUMENT &&
    l.save()==original,"unbounded simultaneous maximization rejected atomically");
  F06ConfigRequest request{l.stats().revision,800,800,200,2,30,0};
  ok(f06_configure(l.s,l.h.captain,&request,&current)==F04_QUALIFICATION &&
    l.save()==original,"captain cannot configure unoccupied station");
  ok(f06_configure(l.s,l.h.ensign,&request,&current)==F04_OK &&
    current.compensation_permille==200 && current.preferred_update_seconds==30,
    "configuration persists and respects trade-offs");
  ok(l.contacts().empty(),"changing configuration cannot create contacts");
  const auto snapshot=l.save();l.load(snapshot);
  ok(f06_configuration_status(l.s,l.h.captain,&current)==F04_OK &&
     current.sensitivity_permille==800 && current.preset_id==2,
     "configuration survives Core save/load");
 } else if(scenario=="search") {
  l.upsert(l.signal(960,100,1,101));
  l.upsert(l.signal(580,5000,4,900));
  F06ContactView matches[4]{};U n=0,total=0;
  F06ContactQuery q{F06_ACTIVE,4,0,0};
  ok(f06_search_contacts_page(l.s,l.h.captain,&q,0,matches,4,&n,&total)==F04_OK &&
    total==0 && !n,"search must not see undiscovered Defiant class from world truth");
  q.confirmed_class_id=1;
  ok(f06_search_contacts_page(l.s,l.h.captain,&q,0,matches,4,&n,&total)==F04_OK &&
    total==1 && n==1 && matches[0].class_id==1,"known Galaxy class searchable");
  q.confirmed_class_id=0;q.max_distance_milli_au=200;
  ok(f06_search_contacts_page(l.s,l.h.captain,&q,0,matches,4,&n,&total)==F04_OK &&
    total==1 && matches[0].distance_milli_au<=200,"range search uses observed distance");
 } else if(scenario=="categories") {
  auto galaxy=l.signal(960,100,1,101);
  galaxy.signature_category=F06_CATEGORY_STARSHIP;
  l.upsert(galaxy);
  auto shuttle=l.signal(580,3000,0,0);
  shuttle.signature_category=F06_CATEGORY_SHUTTLE;
  l.upsert(shuttle);
  const auto contacts=l.contacts();
  ok(contacts.size()==2 && contacts[0].observed_category==F06_CATEGORY_STARSHIP &&
     contacts[1].observed_category==F06_CATEGORY_SHUTTLE,
    "observed signatures give category without inventing class");
  F06ContactQuery query{F06_ACTIVE,0,0,0,F06_CATEGORY_SHUTTLE};
  F06ContactView out[3]{};U count=0,total=0;
  ok(f06_search_contacts_page(l.s,l.h.captain,&query,0,out,3,&count,&total)==F04_OK &&
     count==1 && total==1 && out[0].observed_category==F06_CATEGORY_SHUTTLE &&
     !out[0].class_id,"category filtering does not leak unknown class");
 } else if(scenario=="diagnostics") {
  l.ready();
  F06DiagnosticView diag{};
  ok(f06_diagnostics(l.s,l.h.captain,&diag)==F04_OK &&
    diag.state==1 && diag.configuration_budget_remaining==100,
    "nominal equipment and default config");
  const auto before=l.save();
  ok(f06_run_self_test(l.s,l.h.captain,l.stats().revision,&diag)==F04_QUALIFICATION &&
    before==l.save(),"self test requires sensor post");
  ok(f06_run_self_test(l.s,l.h.ensign,l.stats().revision,&diag)==F04_OK &&
    diag.state==1,"self-test recorded against real sensor hardware");
  F06ArrayInput failure{l.stats().revision,1000,0,1000,1,1,1,0};
  F06ArrayView after{};
  ok(f06_host_array_state(l.s,&failure,&after)==F04_OK,"trusted physical power loss");
  ok(f06_diagnostics(l.s,l.h.captain,&diag)==F04_OK &&
    diag.state==3,"offline status is not mistaken for an anomaly");
 } else if(scenario=="profiles") {
  F06ProfileView previous{};U last_short=0,last_long=0,last_focus=0,last_slots=0;
  for(uint32_t id=1;id<=5;++id) {
   F06ProfileInstall in{l.stats().revision,id,0};
   F06ProfileView profile{};
   ok(f06_host_install_profile(l.s,&in,&profile)==F04_OK &&
      profile.profile_id==id && profile.tier==id,"trusted installed ship profile");
   ok(profile.short_permille>last_short && profile.long_permille>last_long &&
      profile.focus_permille>last_focus && profile.tracking_slots>last_slots,
      "ordered sensor capability tiers");
   last_short=profile.short_permille;last_long=profile.long_permille;
   last_focus=profile.focus_permille;last_slots=profile.tracking_slots;
   previous=profile;
  }
  ok(previous.profile_id==5 && previous.long_permille==1000 &&
    previous.interference_resistance_permille>0,
    "Enterprise-D individual Geordi refit top tier, no canon figures");
  const auto saved=l.save();l.load(saved);
  F06ProfileView read{};
  ok(f06_installed_profile(l.s,l.h.captain,&read)==F04_OK &&
     read.profile_id==5,"installed hardware profile persists through Core save/load");
  const auto invalid=F06ProfileInstall{l.stats().revision,6,0};
  ok(f06_host_install_profile(l.s,&invalid,&read)==F04_ARGUMENT &&
     saved==l.save(),"invalid refit denied without modifying campaign");
  // Same real signal, same Core configuration and MSI-ready numeric test scale:
  // the individual Galaxy refit must outperform Odyssey in detection evidence.
  Lab odyssey,refit;
  F06ProfileView pOld{},pNew{};
  F06ProfileInstall installOld{odyssey.stats().revision,4,0};
  F06ProfileInstall installNew{refit.stats().revision,5,0};
  ok(f06_host_install_profile(odyssey.s,&installOld,&pOld)==F04_OK &&
     f06_host_install_profile(refit.s,&installNew,&pNew)==F04_OK,
     "separate test hulls with authorized experimental sensor loads");
  odyssey.upsert(odyssey.signal(800,5000,4,999));
  refit.upsert(refit.signal(800,5000,4,999));
  const auto older=odyssey.contacts(),newer=refit.contacts();
  ok(older.size()==1 && newer.size()==1 &&
     newer[0].confidence_permille>older[0].confidence_permille,
     "Enterprise-D individual sensor score exceeds Odyssey for identical observation");
 } else if(scenario=="world_feed") {
  const auto ship=l.stats();
  F06WorldEntity fleet[2]{
   {200,6500,0,0,700,4,1000,0,1,F06_EXIT_UNKNOWN},
   {100,5200,0,0,600,2,950,0,1,F06_EXIT_UNKNOWN}
  };
  F06WorldSnapshot snap{ship.revision,1001,0,5000,0,0,2,fleet};
  F06WorldReceipt receipt{};
  ok(f06_host_world_snapshot(l.s,&snap,&receipt)==F04_OK &&
    receipt.created==2 && receipt.retired==0,"trusted full world materialization");
  const auto observed=l.contacts();
  ok(observed.size()==2,"both existing spatial entities observable");
  const U first=observed[0].contact_id,second=observed[1].contact_id;
  auto stable=l.save();
  ok(f06_host_world_snapshot(l.s,&snap,&receipt)==F04_STALE &&
    l.save()==stable,"stale spatial source revision cannot reappear");
  snap.expected_revision=l.stats().revision;snap.source_revision=1002;
  F06WorldEntity duplicate[2]{fleet[0],fleet[0]};snap.entities=duplicate;
  ok(f06_host_world_snapshot(l.s,&snap,&receipt)==F04_ARGUMENT &&
    l.save()==stable,"duplicate persistent world IDs rejected atomically");
  snap.entities=fleet;snap.entity_count=2;
  snap.observer_x_milli_au=6000;
  ok(f06_host_world_snapshot(l.s,&snap,&receipt)==F04_OK &&
    receipt.updated==2 && !receipt.created,"observer motion recomputes positions");
  const auto moved=l.contacts();
  ok(moved.size()==2 && moved[0].contact_id==first &&
    moved[1].contact_id==second,"movement preserves persistent contact identities");
  snap.expected_revision=l.stats().revision;snap.source_revision=1003;
  snap.entities=&fleet[0];snap.entity_count=1;
  ok(f06_host_world_snapshot(l.s,&snap,&receipt)==F04_OK &&
    receipt.retired==1 && l.contacts(F06_LOST).size()==1,
    "omitted spatial entity becomes lost, not destroyed");
  auto persist=l.save();l.load(persist);
  ok(l.contacts(F06_LOST).size()==1,"world source retirement survives save/load");
  snap.expected_revision=l.stats().revision;snap.source_revision=1004;
  snap.entities=fleet;snap.entity_count=2;
  ok(f06_host_world_snapshot(l.s,&snap,&receipt)==F04_OK &&
    !receipt.created && l.contacts(F06_ACTIVE).size()==2,
    "reappearing real entity reuses previous materialized Core identity");
  const auto reunited=l.contacts();
  ok(reunited[0].contact_id==first && reunited[1].contact_id==second,
    "reacquisition IDs stable through world snapshots");
  snap.expected_revision=l.stats().revision;snap.source_revision=1005;
  snap.entities=nullptr;snap.entity_count=0;
  ok(f06_host_world_snapshot(l.s,&snap,&receipt)==F04_OK &&
    receipt.retired==2 && l.contacts(F06_ACTIVE).empty(),
    "full empty universe snapshot retires all spatial signals");
 } else if(scenario=="science_queue") {
  l.ready();l.upsert(l.signal(580,5000,4,999));
  const U id=l.contacts()[0].contact_id;
  ok(l.contacts()[0].class_id==0,"contact class remains unknown");
  F06ScienceRequest req{l.stats().revision,123456,id,2,1};
  F06ScienceView sent{};
  auto before=l.save();
  ok(f06_science_handoff(l.s,l.h.captain,&req,&sent)==F04_QUALIFICATION,
    "unqualified captain cannot send a sensor report");
  ok(before==l.save(),"denial cannot mutate campaign");
  ok(f06_science_handoff(l.s,l.h.ensign,&req,&sent)==F04_OK,
    "qualified sensor operator queues actual Core Science task");
  ok(sent.handoff_id && sent.contact_id==id && sent.status==1 &&
    sent.class_id==0 && !sent.transponder_id,"only observed knowledge leaves sensors");
  F06ScienceView read{};U n=0,total=0;
  ok(f06_science_queue_page(l.s,l.h.captain,0,&read,1,&n,&total)==F04_OK &&
     n==1 && total==1 && read.handoff_id==sent.handoff_id,"Science queue query");
  auto stable=l.save();F06ScienceView replay{};
  ok(f06_science_handoff(l.s,l.h.ensign,&req,&replay)==F04_OK &&
    replay.handoff_id==sent.handoff_id && stable==l.save(),"idempotent duplicate without mutation");
  l.load(stable);l.op(l.h.ensign,F04_SCAN); // only real authorized scan, no truth without signature permission override
  n=total=0;
  ok(f06_science_queue_page(l.s,l.h.captain,0,&read,1,&n,&total)==F04_OK &&
     n==1 && read.class_id==0,"snapshot survives Core save/load without invented class");
 } else if(scenario=="eight_hours") {
  l.upsert(l.signal());auto checkpoint=l.save();
  l.advance(28800);auto after=l.save();auto current=l.contacts()[0];
  ok(current.last_seen==28800 && l.notices().size()==2,"eight hours no invented events");
  Lab another;another.load(checkpoint);another.advance(28800);
  ok(after==another.save(),"deterministic Core timeline and save/load resume");
 } else throw std::runtime_error("unknown scenario");
}
int main(int argc,char** argv){
 if(argc!=2)return 2;
 try{run(argv[1]);std::cout<<"PASS "<<argv[1]<<"\n";return 0;}
 catch(const std::exception& e){std::cerr<<"FAIL "<<argv[1]<<": "<<e.what()<<"\n";return 1;}
}
