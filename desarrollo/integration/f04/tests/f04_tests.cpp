#include "f04_bridge.h"
#include <corerpg/campaign_persistence.hpp>
#include <array>
#include <algorithm>
#include <cstring>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>
using U=uint64_t;
void check(bool b,const char* message) {if(!b)throw std::runtime_error(message);}
struct Lab {
 F04Session* s=nullptr;F04Handles h{};
 Lab(){check(f04_create(1,"miranda",&s)==F04_OK,"create");handles();}
 ~Lab(){if(s)f04_destroy(s);}
 void handles(){check(f04_handles(s,&h)==F04_OK,"handles");}
 F04Stats stats(){F04Stats x{};check(f04_stats(s,&x)==F04_OK,"stats");return x;}
 F04Result request(F04Ref p,U op,U target=0,U aux=0,U start=0,U end=0,U value=0,U cause=42,uint32_t expected=F04_OK,U revision=UINT64_MAX) {
  F04Request r{p,revision==UINT64_MAX?stats().revision:revision,static_cast<uint32_t>(op),static_cast<uint32_t>(value),target,aux,start,end,cause};
  F04Result out{};const auto got=f04_execute(s,&r,&out);
  if(got!=expected){std::cerr<<"op="<<op<<" actor="<<p.id<<" expected="<<expected<<" got="<<got<<"\n";throw std::runtime_error("request result");}
  return out;
 }
 void advance(U t,U expected=F04_OK,U budget=4096){U n=0;check(f04_advance(s,t,budget,&n)==expected,"advance");}
 std::vector<uint8_t> save(){U n=0;check(f04_save(s,nullptr,0,&n)==F04_CAPACITY,"save size");std::vector<uint8_t>b(n);check(f04_save(s,b.data(),n,&n)==F04_OK,"save bytes");return b;}
 void load(const std::vector<uint8_t>& b){check(f04_load(s,b.data(),b.size())==F04_OK,"load");handles();}
 U duty(U end=28800){request(h.head,F04_ASSIGN,h.sensors,h.ensign.id);return request(h.head,F04_DUTY,h.ensign.id,h.sensors,stats().now,end).record;}
 U review(U flags=7){return request(h.captain,F04_CONTACT_REVIEW,0,0,stats().now,stats().now+100,flags).record;}
 void console(){request(h.ensign,F04_MOVE,h.sensors);}
 void full(){duty(172800);request(h.captain,F04_ASSIGN,h.engineering,11);request(h.captain,F04_DUTY,11,h.engineering,0,172800);request(h.captain,F04_ASSIGN,h.bridge,h.watch.id);request(h.captain,F04_DUTY,h.watch.id,h.bridge,0,172800);}
 std::array<F04Person,9> manifest(F04Ref who={}){if(!who.id)who=h.captain;std::array<F04Person,9> x{};U n=0;check(f04_manifest(s,who,x.data(),x.size(),&n)==F04_OK && n==9,"manifest");return x;}
 std::array<F04Slot,3> slots(){std::array<F04Slot,3>x{};U n=0;check(f04_slots(s,h.captain,x.data(),x.size(),&n)==F04_OK && n==3,"slots");return x;}
};
void write(const std::string& p,const std::vector<uint8_t>& b){std::ofstream f(p,std::ios::binary|std::ios::trunc);f.write(reinterpret_cast<const char*>(b.data()),b.size());check(bool(f),"write");}
std::vector<uint8_t> read(const std::string& p){std::ifstream f(p,std::ios::binary);check(bool(f),"read");return {std::istreambuf_iterator<char>(f),{}};}
U scalar(const std::vector<uint8_t>& b,U id,U field){const auto d=corerpg::CampaignPersistence::deserialize(b);check(d.snapshot.has_value(),"decode");for(const auto& r:d.snapshot->campaign.relations)if(r.source.value()==id && (r.kind.value()>>48)==0xF000+field)return r.kind.value()&((1ULL<<48)-1);throw std::runtime_error("missing scalar");}
U succession_events(const std::vector<uint8_t>& b){const auto d=corerpg::CampaignPersistence::deserialize(b);check(d.snapshot.has_value(),"decode");U count=0;for(const auto& r:d.snapshot->campaign.relations)if((r.kind.value()>>48)==0xF000+15 && (r.kind.value()&((1ULL<<48)-1))==100)++count;return count;}
void run(const std::string& name,const std::string& file){
 if(name=="class") {F04Session*s=nullptr;check(f04_create(1,"invented_class",&s)==F04_ARGUMENT && !s,"invalid class");check(f04_create(1,"oberth",&s)==F04_OK,"real catalog class");f04_destroy(s);return;}
 Lab l;const U day=86400;
 if(name=="identity") {const auto m=l.manifest();for(size_t i=0;i<m.size();++i)for(size_t j=i+1;j<m.size();++j)check(m[i].id!=m[j].id,"unique identity");check(l.stats().crew==7 && l.stats().civilians==1 && l.stats().passengers==1,"categories");}
 else if(name=="vacancy") {auto a=l.stats();check(a.vacancies==3,"empty slots");l.duty();check(l.stats().vacancies==2,"one covered");check(l.stats().crew==a.crew,"no hidden generation");}
 else if(name=="manifest") {auto before=l.save();auto m=l.manifest();auto slots=l.slots();check(m[2].id==l.h.ensign.id && !m[2].on_duty && !m[2].at_console,"initial");check(!slots[0].person,"required vacancy");check(l.save()==before,"queries readonly");U n=0;check(f04_manifest(l.s,l.h.passenger,nullptr,0,&n)==F04_DENIED,"no passenger privileged view");}
 else if(name=="qualification") {l.request(l.h.captain,F04_ASSIGN,l.h.sensors,l.h.captain.id,0,0,0,42,F04_SCOPE);l.request(l.h.captain,F04_SCAN,0,0,0,0,0,42,F04_QUALIFICATION);l.request(l.h.captain,F04_APPOINT,l.h.ensign.id,F04_COMMAND,0,100,F04_FIRST,42,F04_QUALIFICATION);}
 else if(name=="assignment") {l.request(l.h.head,F04_ASSIGN,l.h.sensors,l.h.passenger.id,0,0,0,42,F04_DENIED);l.request(l.h.head,F04_ASSIGN,l.h.sensors,999,0,0,0,42,F04_DENIED);l.duty();auto m=l.manifest();check(m[2].on_duty && !m[2].at_console,"duty != console");l.console();check(l.manifest()[2].at_console,"physical console");}
 else if(name=="overlap") {l.duty();l.request(l.h.head,F04_REST,l.h.ensign.id,0,100,200,0,42,F04_OVERLAP);l.request(l.h.head,F04_DUTY,l.h.ensign.id,l.h.sensors,100,200,0,42,F04_OVERLAP);}
 else if(name=="adjacent") {l.duty(100);l.request(l.h.head,F04_REST,l.h.ensign.id,0,100,200);l.advance(100);check(!l.manifest()[2].on_duty,"exclusive end");}
 else if(name=="rest") {l.request(l.h.head,F04_REST,l.h.ensign.id,0,0,200);l.request(l.h.head,F04_ASSIGN,l.h.sensors,l.h.ensign.id,0,0,0,42,F04_UNAVAILABLE);check(!l.manifest()[2].available,"protected rest");}
 else if(name=="oncall") {l.duty();l.request(l.h.head,F04_ONCALL,l.h.ensign.id,0,0,200);auto m=l.manifest()[2];check(m.on_duty && m.localized && !m.at_console,"independent states");}
 else if(name=="absence") {l.duty();l.request(l.h.head,F04_ABSENCE,l.h.ensign.id,0,0,200,F04_SICK);check(l.stats().vacancies==3 && !l.manifest()[2].on_duty,"absence invalidates coverage");l.advance(200);check(l.stats().vacancies==2,"absence expiry restores eligibility");}
 else if(name=="relief") {const U a=l.duty();l.request(l.h.head,F04_ABSENCE,l.h.ensign.id,0,0,200,F04_LEAVE);l.request(l.h.head,F04_RELIEF,a,l.h.relief.id);check(l.slots()[0].person==l.h.relief.id && l.slots()[0].covered,"real relief");check(l.stats().crew==7,"no extra crew");}
 else if(name=="coverage") {l.request(l.h.captain,F04_POLICY,0,0,0,0,4,42,F04_VACANT);l.full();l.request(l.h.head,F04_ABSENCE,l.h.ensign.id,0,day-100,day+100,F04_SICK);l.request(l.h.captain,F04_POLICY,0,0,0,0,4,42,F04_VACANT);}
 else if(name=="policy") {l.full();l.request(l.h.captain,F04_POLICY,0,0,0,0,4);check(l.stats().pattern==4,"Delta selected");l.request(l.h.captain,F04_POLICY,0,0,0,0,3);check(l.stats().pattern==3,"three watches");}
 else if(name=="roles") {l.duty();l.console();l.request(l.h.ensign,F04_SCAN);l.request(l.h.ensign,F04_BRIDGE,0,0,0,0,0,42,F04_DENIED);l.request(l.h.head,F04_ASSIGN,l.h.engineering,11,0,0,0,42,F04_SCOPE);l.request(l.h.watch,F04_BRIDGE,0,0,0,0,2);check(l.stats().alert==2,"watch changes authoritative alert");l.request(l.h.watch,F04_POLICY,0,0,0,0,4,42,F04_DENIED);l.request(l.h.captain,F04_BRIDGE);l.request(l.h.admiral,F04_BRIDGE,0,0,0,0,0,42,F04_UNAVAILABLE);}
 else if(name=="watch") {l.request(l.h.watch,F04_BRIDGE);l.advance(28800);l.request(l.h.watch,F04_BRIDGE,0,0,0,0,0,42,F04_DENIED);check(l.stats().commander==l.h.captain.id,"watch not permanent captain");}
 else if(name=="appointment") {const U a=l.request(l.h.captain,F04_APPOINT,l.h.watch.id,F04_COMMAND,28800,30000,F04_WATCH).record;l.advance(28800);l.request(l.h.watch,F04_BRIDGE);l.request(l.h.captain,F04_REVOKE,a);l.request(l.h.watch,F04_BRIDGE,0,0,0,0,0,42,F04_DENIED);}
 else if(name=="succession" || name=="medical") {l.request(l.h.doctor,F04_MEDICAL,l.h.captain.id,0,0,100,F04_SICK);check(l.stats().commander==l.h.watch.id,"normal succession");l.request(l.h.doctor,F04_BRIDGE,0,0,0,0,0,42,F04_DENIED);l.request(l.h.watch,F04_BRIDGE);l.advance(100);check(l.stats().commander==l.h.captain.id,"restored titular");l.request(l.h.ensign,F04_MEDICAL,l.h.captain.id,0,100,200,F04_SICK,42,F04_QUALIFICATION);}
 else if(name=="delegation" || name=="revoke" || name=="expiry" || name=="origin") {l.full();U d=l.request(l.h.captain,F04_DELEGATE,l.h.watch.id,0,0,100,F04_POLICY).record;l.request(l.h.watch,F04_POLICY,0,0,0,0,4);
  if(name=="revoke")l.request(l.h.captain,F04_REVOKE,d);
  else if(name=="origin")l.request(l.h.doctor,F04_MEDICAL,l.h.captain.id,0,0,200,F04_SICK);
  else l.advance(100);
  if(name=="origin") { // New captain has direct authority, but old delegation cannot empower another officer.
   check(l.stats().commander==l.h.watch.id,"new authority");l.request(l.h.watch,F04_DELEGATE,l.h.ensign.id,0,0,100,F04_POLICY,42,F04_QUALIFICATION);
  }else l.request(l.h.watch,F04_POLICY,0,0,0,0,3,42,F04_DENIED);
 }
 else if(name=="technical") {l.request(l.h.captain,F04_SCAN,0,0,0,0,0,42,F04_QUALIFICATION);l.request(l.h.captain,F04_MEDICAL,l.h.ensign.id,0,0,100,F04_SICK,42,F04_QUALIFICATION);}
 else if(name=="safety") {l.request(l.h.captain,F04_IMPOSSIBLE,0,0,0,0,0,42,F04_SAFETY);check(l.stats().events==1,"denial audited");}
 else if(name=="contact") {l.request(l.h.captain,F04_CONTACT,0,0,0,0,0,0,F04_REVIEW);l.request(l.h.captain,F04_CONTACT,l.review());}
 else if(name=="superior") {U review=l.review();U order=l.request(l.h.admiral,F04_SUPERIOR,0,0,0,100,F04_CONTACT).record;l.request(l.h.captain,F04_CONTACT,review,0,0,0,0,42,F04_REVIEW);l.request(l.h.captain,F04_REVOKE,order,0,0,0,0,42,F04_DENIED);l.request(l.h.admiral,F04_REVOKE,order);l.request(l.h.captain,F04_CONTACT,review);l.request(l.h.admiral,F04_SUPERIOR,0,0,0,100,F04_POLICY,42,F04_DENIED);}

 else if(name=="ai") {const auto before=l.stats();l.request(l.h.ensign,F04_PROPOSE,0,0,0,0,4);check(l.stats().pattern==before.pattern && l.stats().commander==before.commander,"suggestion not permission");l.request(l.h.ensign,F04_POLICY,0,0,0,0,4,42,F04_DENIED);}
 else if(name=="stale") {const U r=l.stats().revision;l.request(l.h.captain,F04_BRIDGE);l.request(l.h.captain,F04_BRIDGE,0,0,0,0,0,42,F04_STALE,r);}
 else if(name=="queued") {l.duty();l.console();const U task=l.request(l.h.ensign,F04_QUEUE,0,0,10,20,F04_SCAN).record;l.request(l.h.head,F04_ABSENCE,l.h.ensign.id,0,5,100,F04_SUSPENDED);l.advance(10);check(scalar(l.save(),task,16)==F04_UNAVAILABLE,"revalidated at execution");}
 else if(name=="offscreen") {l.duty();l.console();const U task=l.request(l.h.ensign,F04_QUEUE,0,0,10,20,F04_SCAN).record;l.advance(10);check(l.stats().pending==0 && scalar(l.save(),task,16)==F04_OK,"without Actors");auto b=l.save();l.advance(10);check(l.save()==b,"no duplicate execution");}
 else if(name=="roundtrip" || name=="determinism") {l.duty();l.console();l.request(l.h.ensign,F04_QUEUE,0,0,10,20,F04_SCAN);auto b=l.save();l.advance(100);auto future=l.save();Lab other;other.load(b);check(other.save()==b,"archive identity");other.advance(100);check(other.save()==future,"deterministic resume");}
 else if(name=="corrupt") {auto b=l.save(),bad=b;bad.back()^=128;check(f04_load(l.s,bad.data(),bad.size())==F04_SAVE,"corruption");check(l.save()==b,"atomic load failure");bad=b;bad[8]=99;check(f04_load(l.s,bad.data(),bad.size())==F04_SAVE,"version");}
 else if(name=="schema") {auto b=l.save();auto d=corerpg::CampaignPersistence::deserialize(b);check(d.snapshot.has_value(),"decode");d.snapshot->campaign.relations.push_back({corerpg::EntityId{1},corerpg::RelationKind{999},corerpg::EntityId{1}});++d.snapshot->campaign.revision;std::sort(d.snapshot->campaign.relations.begin(),d.snapshot->campaign.relations.end());auto encoded=corerpg::CampaignPersistence::serialize(*d.snapshot);check(encoded.status==corerpg::CampaignArchiveStatus::success,"valid Core unknown Trek label");check(f04_load(l.s,encoded.bytes.data(),encoded.bytes.size())==F04_SAVE,"domain schema rejects");check(l.save()==b,"schema rejection atomic");}
 else if(name=="thread") {auto b=l.save();uint32_t got=0;std::thread worker([&]{F04Stats x{};got=f04_stats(l.s,&x);});worker.join();check(got==F04_THREAD && l.save()==b,"owner thread");}
 else if(name=="scope") {auto old=l.h.captain;auto b=l.save();l.load(b);l.request(old,F04_BRIDGE,0,0,0,0,0,42,F04_SCOPE);}
 else if(name=="buffers") {U n=0;check(f04_slots(l.s,l.h.captain,nullptr,0,&n)==F04_CAPACITY && n==3,"count slots");check(f04_manifest(l.s,l.h.captain,nullptr,1,&n)==F04_ARGUMENT,"bad buffer");check(f04_stats(l.s,nullptr)==F04_ARGUMENT,"null stats");}
 else if(name=="bounded") {l.duty();l.console();l.request(l.h.ensign,F04_QUEUE,0,0,10,20,F04_SCAN);l.request(l.h.ensign,F04_QUEUE,0,0,11,20,F04_SCAN);l.advance(100,F04_CAPACITY,1);check(l.stats().now==10 && l.stats().pending==1,"bounded progress");auto b=l.save();Lab other;other.load(b);other.advance(100);l.advance(100);check(other.save()==l.save(),"bounded recovery");}
 else if(name=="backwards") {l.advance(100);auto b=l.save();l.advance(99,F04_ARGUMENT);check(l.save()==b,"backwards unchanged");}
 else if(name=="recall") {const U a=l.request(l.h.head,F04_REST,l.h.relief.id,0,0,100).record;l.request(l.h.captain,F04_RECALL,a,0,0,0,0,0,F04_REVIEW);l.request(l.h.captain,F04_RECALL,a,0,0,0,60,42);check(l.manifest()[5].available && scalar(l.save(),a,14)==60,"explicit fatigue debt");}
 else if(name=="rotation") {F04WatchWindow w{};check(f04_watch_window(l.s,0,&w)==F04_OK && w.label==2 && w.end==28800,"Gamma");check(f04_watch_window(l.s,28800,&w)==F04_OK && w.label==0 && w.start==28800 && w.end==57600,"Alpha adjacent");l.full();l.request(l.h.captain,F04_POLICY,0,0,0,0,4);check(f04_watch_window(l.s,0,&w)==F04_OK && w.label==3 && w.end==21600,"Delta");check(f04_watch_window(l.s,86400+21600,&w)==F04_OK && w.label==0 && w.end-w.start==21600,"next day Alpha");}
 else if(name=="credential_expiry") {l.advance(86400);l.request(l.h.head,F04_ASSIGN,l.h.sensors,l.h.relief.id,0,0,0,42,F04_QUALIFICATION);}
 else if(name=="succession_boundaries") {l.request(l.h.doctor,F04_MEDICAL,l.h.captain.id,0,10,20,F04_SICK);auto saved=l.save();l.advance(30);check(l.stats().commander==3 && succession_events(l.save())==2,"both offscreen transitions audited");Lab other;other.load(saved);other.advance(10);check(other.stats().commander==6,"acting commander at beginning");other.advance(20);other.advance(30);check(other.save()==l.save(),"partition invariant succession history");}
 else if(name=="context_review") {U incomplete=l.review(1);l.request(l.h.captain,F04_CONTACT,incomplete,0,0,0,0,42,F04_REVIEW);U risk=l.review(15);l.request(l.h.captain,F04_CONTACT,risk);l.advance(100);l.request(l.h.captain,F04_CONTACT,risk,0,0,0,0,42,F04_REVIEW);}
 else if(name=="order_expiry") {U review=l.review();l.request(l.h.admiral,F04_SUPERIOR,0,0,0,10,F04_CONTACT);l.request(l.h.captain,F04_CONTACT,review,0,0,0,0,42,F04_REVIEW);l.advance(10);l.request(l.h.captain,F04_CONTACT,review);}
 else if(name=="origin_reappointment") {l.full();l.request(l.h.captain,F04_DELEGATE,l.h.watch.id,0,0,100,F04_POLICY);l.request(l.h.captain,F04_REVOKE,15);check(l.stats().commander==6,"successor");l.request(l.h.watch,F04_APPOINT,3,F04_COMMAND,0,1000,F04_CAPTAIN);check(l.stats().commander==3,"same issuer new appointment");l.request(l.h.watch,F04_POLICY,0,0,0,0,4,42,F04_DENIED);}
 else if(name=="pending_credential") {l.request(l.h.head,F04_ASSIGN,l.h.sensors,l.h.relief.id);l.request(l.h.head,F04_DUTY,l.h.relief.id,l.h.sensors,0,86400);l.request(l.h.relief,F04_MOVE,l.h.sensors);U task=l.request(l.h.relief,F04_QUEUE,0,0,86400,86401,F04_SCAN).record;l.advance(86400);check(scalar(l.save(),task,16)==F04_QUALIFICATION,"expired technical permit at execution");}
 else if(name=="authorized_posts") {l.duty();F04Slot slots[3]{};U n=0;check(f04_slots(l.s,l.h.ensign,slots,3,&n)==F04_OK && slots[0].authorized && !slots[1].authorized,"observer authorized posts");check(l.slots()[0].authorized==0,"captain rank no technical qualification");}
 else if(name=="integrated") {
  const U a=l.duty();l.console();l.request(l.h.ensign,F04_SCAN);l.request(l.h.watch,F04_BRIDGE);l.request(l.h.captain,F04_CONTACT,l.review());
  l.request(l.h.head,F04_ABSENCE,l.h.ensign.id,0,0,100,F04_SICK);check(l.slots()[0].covered==0,"real gap");
  l.request(l.h.head,F04_RELIEF,a,l.h.relief.id);l.request(l.h.relief,F04_MOVE,l.h.sensors);
  const U d=l.request(l.h.captain,F04_DELEGATE,l.h.watch.id,0,0,20,F04_POLICY).record;l.request(l.h.captain,F04_REVOKE,d);
  l.request(l.h.watch,F04_POLICY,0,0,0,0,4,42,F04_DENIED);l.request(l.h.captain,F04_IMPOSSIBLE,0,0,0,0,0,42,F04_SAFETY);
  l.request(l.h.relief,F04_QUEUE,0,0,10,20,F04_SCAN);auto before=l.save();l.advance(15);auto future=l.save();
  f04_destroy(l.s);l.s=nullptr;check(f04_create(1,"miranda",&l.s)==F04_OK,"new session");l.load(before);check(l.save()==before && l.stats().pending==1,"identities and pending restored");l.advance(15);check(l.save()==future,"integrated continuity");
 }
 else if(name=="process_save") {l.duty();l.console();l.request(l.h.ensign,F04_QUEUE,0,0,10,20,F04_SCAN);write(file,l.save());l.advance(100);write(file+".future",l.save());}
 else if(name=="process_load") {l.load(read(file));check(l.stats().pending==1 && l.stats().commander==3,"cross process state");l.advance(100);check(l.save()==read(file+".future"),"cross process deterministic archive");}
 else throw std::runtime_error("unknown test");
}
int main(int argc,char**argv){try{check(argc>=2,"case required");run(argv[1],argc>2?argv[2]:"");std::cout<<argv[1]<<": PASS\n";return 0;}catch(const std::exception&e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
