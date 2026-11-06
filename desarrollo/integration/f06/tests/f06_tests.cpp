#include "f06_sensors.h"
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
