#include "f05_orders.h"
#include <corerpg/campaign_persistence.hpp>
#include <corerpg/action.hpp>
#include <corerpg/content_catalog.hpp>
#include <algorithm>
#include <array>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <thread>
#include <vector>
using U=uint64_t;
using namespace corerpg;
void check(bool b,const char* msg){if(!b)throw std::runtime_error(msg);}
void eq(uint32_t got,uint32_t expected,const char* msg){if(got!=expected){std::cerr<<msg<<" got="<<got<<" expected="<<expected<<"\n";throw std::runtime_error(msg);}}
struct Lab {
 F04Session* s=nullptr;F04Handles h{};
 Lab(){eq(f04_create(1,"miranda",&s),F04_OK,"create");handles();}
 ~Lab(){if(s)f04_destroy(s);}
 void handles(){eq(f04_handles(s,&h),F04_OK,"handles");}
 F04Ref person(U id){return {h.ship.scope,id};}
 F04Stats stats(){F04Stats x{};eq(f04_stats(s,&x),F04_OK,"stats");return x;}
 F04Result op(F04Ref who,U kind,U target=0,U aux=0,U start=0,U end=0,U value=0){
  F04Request q{who,stats().revision,uint32_t(kind),uint32_t(value),target,aux,start,end,50501};
  F04Result r{};eq(f04_execute(s,&q,&r),F04_OK,"F04 fixture operation");return r;
 }
 void ready(){op(h.head,F04_ASSIGN,h.sensors,h.ensign.id);op(h.head,F04_DUTY,h.ensign.id,h.sensors,0,28800);op(h.ensign,F04_MOVE,h.sensors);}
 void advance(U t){U n=0;eq(f04_advance(s,t,4096,&n),F04_OK,"Core advance");}
 std::vector<uint8_t> save(){U n=0;eq(f04_save(s,nullptr,0,&n),F04_CAPACITY,"save size");std::vector<uint8_t>b(n);eq(f04_save(s,b.data(),n,&n),F04_OK,"save");return b;}
 void load(const std::vector<uint8_t>& b){eq(f04_load(s,b.data(),b.size()),F04_OK,"load");handles();}
 F05OrderRequest request(U key=1){return {h.captain,h.ensign,h.ship,{h.ship.scope,h.sensors},key,stats().revision,100,50501,F04_SCAN,0};}
 F05Receipt submit(const F05OrderRequest& q,uint32_t code=F04_OK){F05Receipt r{};eq(f05_submit(s,&q,&r),code,"submit");return r;}
 F05Receipt receive(U o,uint32_t code=F04_OK){F05Receipt r{};eq(f05_receive(s,h.ensign,stats().revision,o,&r),code,"receive");return r;}
 F05Receipt execute(U o,uint32_t code=F04_OK){F05Receipt r{};eq(f05_execute_order(s,h.ensign,stats().revision,o,&r),code,"execute");return r;}
 F05Receipt accepted(U key=1){return receive(submit(request(key)).order);}
 F05OrderView view(U o){F05OrderView v{};eq(f05_order(s,h.captain,o,&v),F04_OK,"order view");return v;}
 F05ResultView result(U o){F05ResultView v{};eq(f05_result(s,h.captain,o,&v),F04_OK,"result view");return v;}
 F05OrderRequest replay(U o){auto v=view(o);return {person(v.issuer),person(v.recipient),h.ship,person(v.station),v.key,v.input_revision,v.deadline,v.cause,v.operation,0};}
 std::vector<F05EventView> events(U o){std::vector<F05EventView> all;U after=0,n=0;uint32_t more=0;do{F05EventView e[2]{};eq(f05_events_page(s,h.captain,o,after,e,2,&n,&more),F04_OK,"event page");for(U i=0;i<n;++i){all.push_back(e[i]);after=e[i].id;}}while(more);return all;}
};
CampaignArchiveSnapshot decode(const std::vector<uint8_t>& b){auto d=CampaignPersistence::deserialize(b);check(d.snapshot.has_value(),"Core decode");return *d.snapshot;}
std::vector<uint8_t> encode(CampaignArchiveSnapshot d){++d.campaign.revision;std::sort(d.campaign.relations.begin(),d.campaign.relations.end());auto b=CampaignPersistence::serialize(d);check(b.status==CampaignArchiveStatus::success,"Core accepts candidate");return b.bytes;}
U field(const CampaignArchiveSnapshot& d,U id,U f){for(auto r:d.campaign.relations)if(r.source.value()==id && (r.kind.value()>>48)==0xF000+f)return r.kind.value()&((1ULL<<48)-1);throw std::runtime_error("field missing");}
U field_id(const CampaignArchiveSnapshot& d,U id,U value){for(auto r:d.campaign.relations)if(r.source.value()==id && r.target.value()==id && (r.kind.value()>>48)>=0xF000 && (r.kind.value()&((1ULL<<48)-1))==value)return (r.kind.value()>>48)-0xF000;throw std::runtime_error("field id missing");}
void change(CampaignArchiveSnapshot& d,U id,U f,U value){for(auto& r:d.campaign.relations)if(r.source.value()==id && (r.kind.value()>>48)==0xF000+f){r.kind=RelationKind{((0xF000+f)<<48)|value};return;}throw std::runtime_error("change missing");}
void write(const std::string& p,const std::vector<uint8_t>& b){std::ofstream f(p,std::ios::binary);f.write(reinterpret_cast<const char*>(b.data()),std::streamsize(b.size()));check(bool(f),"write fixture");}
std::vector<uint8_t> read(const std::string& p){std::ifstream f(p,std::ios::binary);check(bool(f),"read fixture");return {std::istreambuf_iterator<char>(f),{}};}
std::vector<U> orders(const CampaignArchiveSnapshot& d){std::vector<U> ids;for(const auto& x:d.campaign.definitions)if(x.definition_id=="trek.f04:f05_order")ids.push_back(x.entity.value());return ids;}
void run(const std::string& name,const std::string& file) {
 Lab l;
 if(name=="scenario") {
  l.ready();auto before=decode(l.save());auto q=l.request();auto r=l.submit(q);
  check(r.state==F05_ISSUED && !r.task && !r.result,"issued isn't acceptance or effect");
  check(decode(l.save()).campaign.streams==before.campaign.streams,"creation never rolls");
  r=l.receive(r.order);check(r.state==F05_ACCEPTED && r.task && !r.attempt,"accepted task only");
  check(decode(l.save()).campaign.streams==before.campaign.streams,"ack never rolls");
  auto pending=l.save();r=l.execute(r.order);auto v=l.result(r.order);auto d=decode(l.save());
  check(r.state==F05_COMPLETED && v.performed && v.code==F04_OK && v.executor==q.recipient.id,"real result");
  check(v.core_outcome==uint32_t(ActionOutcome::accepted) && !v.core_rejection && v.consumed_random && v.value>=1 && v.value<=100,"true roll contract");
  std::set<U> distinct{r.request,r.order,r.task,r.attempt,r.result,r.event};check(distinct.size()==6,"six identities differ");
  auto e=l.events(r.order);check(e.size()==4 && e[0].state==F05_ISSUED && e[1].state==F05_ACCEPTED && e[2].state==F05_EXECUTING && e[3].state==F05_COMPLETED,"transition chain");
  check(!e[0].previous && e[1].previous==e[0].id && e[2].previous==e[1].id && e[3].previous==e[2].id && e[3].result==r.result,"causal events");
  check(e[0].actor==q.issuer.id && e[1].actor==q.recipient.id,"issuer versus recipient");
  Lab direct;direct.load(pending);direct.op(direct.h.ensign,F04_SCAN);
  check(decode(direct.save()).campaign.streams==d.campaign.streams,"F05 and existing F04 consume exactly the same Core stream");
  // Independently invoke the real Core on the pre-action archive, no mock resolver.
  WorldState world;RandomStreams rng{1};Timeline time;
  std::set<std::string> definitions;for(const auto& binding:decode(pending).campaign.definitions)definitions.insert(binding.definition_id);
  std::vector<ContentDefinitionInput> inputs;for(const auto& id:definitions)inputs.emplace_back(ResourceDefinition{*DefinitionId::parse(id),*ResourceKind::parse("structural")});
  const auto version=*SemanticVersion::parse("0.1.0");
  const auto catalog=ContentCatalog::create({ContentPackInput{ContentManifest{*PackId::parse("trek.f04"),version,version,version},std::move(inputs)}});
  check(catalog.succeeded(),"independent declarative catalog");
  check(CampaignPersistence::load(pending,world,rng,time,{},catalog.catalog())==CampaignArchiveStatus::success,"independent Core load");
  const auto actual=ActionEngine::process(world,rng,{EntityId{q.recipient.id},StreamRollAction{0xF0401,1,100},world.revision()});
  const auto roll=std::get<RollConsequence>(actual.consequence);
  check(roll.value==v.value && roll.consumed_random==bool(v.consumed_random),"stored consequence equals independent real Core");
  check(v.core_revision_before==v.core_revision_after && v.core_revision_after<d.campaign.revision,"true action revisions exclude later audit writes");
  std::cout<<"issuer="<<q.issuer.id<<" recipient="<<q.recipient.id<<" request="<<r.request<<" order="<<r.order<<" task="<<r.task<<" attempt="<<r.attempt<<" result="<<r.result<<" event="<<r.event<<" Core stream="<<v.stream<<" value="<<v.value<<"\n";
 } else if(name=="authority") {
  l.ready();auto q=l.request();q.issuer=l.h.ensign;auto r=l.submit(q,F04_DENIED);check(r.state==F05_REFUSED && !r.task,"no command by skill/rank");
  q=l.request(2);q.issuer=l.h.admiral;l.submit(q,F04_UNAVAILABLE);check(decode(l.save()).campaign.streams.empty(),"refusals no RNG");
  q=l.request(3);q.issuer=l.h.head;l.receive(l.submit(q).order); // existing departmental scope
 } else if(name=="recipient") {
  l.ready();auto q=l.request();q.recipient=l.h.doctor;auto r=l.submit(q,F04_QUALIFICATION);check(r.state==F05_REFUSED,"incompatible medical recipient");
  q=l.request(2);q.recipient=l.h.civilian;l.submit(q,F04_DENIED);
  q=l.request(3);q.station.id=l.h.engineering;l.submit(q,F04_SCOPE);check(decode(l.save()).campaign.streams.empty(),"no effects on mismatch");
 } else if(name=="unsupported") {
  l.ready();auto q=l.request();q.operation=F04_BRIDGE;auto r=l.submit(q,F05_UNSUPPORTED);check(r.state==F05_REFUSED,"unsupported explicit refusal");check(l.stats().alert==1,"unsupported operation never called");
 } else if(name=="scope") {
  l.ready();auto q=l.request();auto before=l.save();q.recipient.scope++;l.submit(q,F04_SCOPE);check(l.save()==before,"foreign recipient scope");
  q=l.request();q.issuer.id=9999;l.submit(q,F04_SCOPE);check(l.save()==before,"unknown issuer no fake record");
  q=l.request();auto o=l.submit(q).order;F05OrderView v{};eq(f05_order(l.s,l.h.doctor,o,&v),F04_DENIED,"no omniscient NPC read");
  auto old=l.h.ensign;l.load(l.save());F05Receipt r{};eq(f05_receive(l.s,old,l.stats().revision,o,&r),F04_DENIED,"old session ref rejected");
 } else if(name=="stale") {
  l.ready();auto q=l.request();q.expected_revision--;auto r=l.submit(q,F04_STALE);check(r.state==F05_REFUSED,"stale creation audited");
  auto a=l.accepted(2);auto b=l.save();F05Receipt out{};eq(f05_execute_order(l.s,l.h.ensign,l.stats().revision-1,a.order,&out),F04_STALE,"stale attempt");check(l.save()==b,"stale execution preserves task and RNG");
 } else if(name=="reception") {
  l.ready();auto r=l.submit(l.request());F05Receipt out{};auto b=l.save();eq(f05_receive(l.s,l.h.captain,l.stats().revision,r.order,&out),F04_DENIED,"issuer cannot acknowledge recipient");check(l.save()==b,"denied receive atomic");
  eq(f05_receive(l.s,l.h.ensign,l.stats().revision-1,r.order,&out),F04_STALE,"stale receive");
  l.op(l.h.head,F04_ABSENCE,l.h.ensign.id,0,0,50,F04_SICK);r=l.receive(r.order,F04_UNAVAILABLE);check(r.state==F05_REFUSED && !r.task,"receive revalidates");
 } else if(name=="duplicate") {
  l.ready();auto q=l.request();auto r=l.submit(q);auto b=l.save();check(l.submit(q).order==r.order && l.save()==b,"duplicate issued");
  r=l.receive(r.order);b=l.save();l.receive(r.order);l.submit(q);check(l.save()==b,"duplicate accepted");
  r=l.execute(r.order);b=l.save();l.execute(r.order);l.submit(q);check(l.save()==b,"duplicate complete has no second effect/event");
  for(int i=0;i<5;++i){auto bad=q;if(i==0)bad.operation=F04_BRIDGE;if(i==1)bad.recipient=l.h.doctor;if(i==2)bad.cause++;if(i==3)bad.deadline++;if(i==4)bad.expected_revision++;l.submit(bad,F05_IDEMPOTENCY_CONFLICT);check(l.save()==b,"conflicting payload rejected unchanged");}
  l.load(b);q=l.replay(r.order);l.submit(q);l.execute(r.order);check(l.save()==b,"idempotency survives reload/scopes");
 } else if(name=="revalidate") {
  l.ready();auto a=l.accepted();l.op(l.h.head,F04_ABSENCE,l.h.ensign.id,0,0,50,F04_SICK);auto r=l.execute(a.order,F04_UNAVAILABLE);check(r.state==F05_FAILED && !l.result(r.order).performed,"medical change stops Core action");
  check(decode(l.save()).campaign.streams.empty(),"failed recheck doesn't roll");
  l.advance(50);a=l.accepted(2);l.op(l.h.doctor,F04_MEDICAL,l.h.captain.id,0,50,70,F04_SICK);l.execute(a.order,F04_UNAVAILABLE);
  l.advance(70);a=l.accepted(3);l.op(l.h.captain,F04_REVOKE,l.view(a.order).origin);l.execute(a.order,F04_REVOKED);
 } else if(name=="expired") {
  l.ready();auto a=l.accepted();l.advance(100);auto r=l.execute(a.order,F04_EXPIRED);check(r.state==F05_FAILED && !l.result(r.order).performed,"deadline boundary");auto b=l.save();l.submit(l.replay(r.order),F04_EXPIRED);l.execute(r.order,F04_EXPIRED);check(l.save()==b,"expired replay no retry");
 } else if(name=="cancel") {
  l.ready();auto a=l.accepted();F05Receipt r{};eq(f05_cancel(l.s,l.h.ensign,l.stats().revision,a.order,&r),F04_DENIED,"recipient cannot cancel issuer order");
  eq(f05_cancel(l.s,l.h.captain,l.stats().revision,a.order,&r),F04_OK,"cancel");check(r.state==F05_CANCELLED && !r.result,"cancel is not an executed result");auto b=l.save();l.execute(r.order);l.submit(l.replay(r.order));eq(f05_cancel(l.s,l.h.captain,0,a.order,&r),F04_OK,"cancel replay");check(l.save()==b,"cancel tombstone");
 } else if(name=="transition") {
  l.ready();auto a=l.submit(l.request());auto b=l.save();F05Receipt r{};eq(f05_execute_order(l.s,l.h.ensign,l.stats().revision,a.order,&r),F05_TRANSITION,"no execute before ack");check(l.save()==b,"transition no effect");l.receive(a.order);l.execute(a.order);eq(f05_cancel(l.s,l.h.captain,l.stats().revision,a.order,&r),F05_TRANSITION,"cannot cancel past effect");
 } else if(name=="determinism") {
  l.ready();auto a=l.accepted();auto pending=l.save();l.advance(1);l.execute(a.order);auto future=l.save();Lab other;other.load(pending);other.advance(1);other.execute(a.order);check(other.save()==future,"byte identical deterministic future");
 } else if(name=="corrupt") {
  l.ready();auto a=l.accepted();a=l.execute(a.order);auto good=l.save();auto bad=good;bad.back()^=128;eq(f04_load(l.s,bad.data(),bad.size()),F04_SAVE,"checksum reject");check(l.save()==good,"corrupt atomic");
  auto d=decode(good);const U state_field=field_id(d,a.order,F05_COMPLETED);change(d,a.order,state_field,F05_ISSUED);bad=encode(d);eq(f04_load(l.s,bad.data(),bad.size()),F04_SAVE,"Core-valid impossible order rejected");check(l.save()==good,"bad state atomic");
  d=decode(good);const U e=l.events(a.order).back().id;for(auto& rel:d.campaign.relations)if(rel.source.value()==e && rel.target.value()==a.result)rel.target=EntityId{a.order};bad=encode(d);eq(f04_load(l.s,bad.data(),bad.size()),F04_SAVE,"broken causal result rejected");check(l.save()==good,"bad link atomic");
 } else if(name=="buffers") {
  l.ready();auto a=l.submit(l.request());auto b=l.save();F05Receipt r{};eq(f05_submit(l.s,nullptr,&r),F04_ARGUMENT,"null request");eq(f05_receive(l.s,l.h.ensign,0,a.order,nullptr),F04_ARGUMENT,"null out");U n=0;uint32_t more=0;eq(f05_events_page(l.s,l.h.captain,a.order,0,nullptr,1,&n,&more),F04_ARGUMENT,"invalid buffer");
  uint32_t code=0;std::thread worker([&]{code=f05_receive(l.s,l.h.ensign,0,a.order,&r);});worker.join();eq(code,F04_THREAD,"one owner thread");check(l.save()==b,"invalid entry no changes");
 } else if(name=="population") {
  f04_destroy(l.s);l.s=nullptr;F04PopulationConfig cfg{50501,404,130,0,0,0};eq(f04_create_population(1,"miranda",&cfg,&l.s),F04_OK,"population");l.handles();
  l.op(l.h.captain,F04_INSTALL_TEMPLATE,0,F04_SUTHERLAND_EQUIPMENT,0,0,F04_SUTHERLAND_SCIENCE);l.op(l.h.captain,F04_BOOTSTRAP_TEMPLATE);
  l.op(l.h.captain,F04_PLAN_ALPHA,0,0,28800,57600);l.advance(28800);
  std::vector<F04Position> p(130);U n=0,total=0;eq(f04_positions_page(l.s,l.h.captain,0,p.data(),130,&n,&total),F04_OK,"real positions");
  bool found=false;for(auto slot:p)if(slot.person && slot.qualification==F04_SENSORS && slot.on_duty){l.h.ensign=l.person(slot.person);l.h.sensors=slot.id;found=true;break;}check(found,"existing qualified roster operator");
  l.op(l.h.ensign,F04_MOVE,l.h.sensors);auto q=l.request();q.deadline=28900;auto a=l.receive(l.submit(q).order);l.execute(a.order);check(l.result(a.order).performed,"same API on F04 populated organization");
 } else if(name=="history") {
  l.ready();auto a=l.accepted();l.execute(a.order);l.advance(8*86400);
  auto dir=std::filesystem::path(file);for(unsigned i=0;std::filesystem::exists(dir);++i)dir=file+"-"+std::to_string(i);
  std::array<uint8_t,16> uuid{5,5,1};eq(f04_history_migrate(l.s,dir.string().c_str(),uuid.data(),uuid.size()),F04_OK,"Core history migrate");
  eq(f04_history_consolidate(l.s,86400,0),F04_OK,"Core consolidation preserves order dependencies");eq(f04_history_publish(l.s,0),F04_OK,"Core publish");
  Lab recovered;eq(f04_history_open(recovered.s,dir.string().c_str()),F04_OK,"Core recover");recovered.handles();auto q=recovered.replay(a.order);auto r=recovered.submit(q);check(r.state==F05_COMPLETED && recovered.result(a.order).value==l.result(a.order).value,"recovered tombstone/result");
  F04HistoryStats before{},after{};eq(f04_history_stats(recovered.s,&before),F04_OK,"history before");recovered.execute(a.order);eq(f04_history_stats(recovered.s,&after),F04_OK,"history after");check(before.issued==after.issued && before.relations==after.relations,"history replay no duplicate");
 } else if(name=="process_save") {
  l.ready();auto issued=l.submit(l.request());auto accepted=l.accepted(2);auto done=l.accepted(3);l.execute(done.order);
  auto q=l.request(4);q.operation=F04_BRIDGE;l.submit(q,F05_UNSUPPORTED);
  write(file+".pending",l.save());l.receive(issued.order);l.execute(issued.order);l.execute(accepted.order);write(file+".future",l.save());
 } else if(name=="process_load") {
  l.load(read(file+".pending"));auto ids=orders(decode(l.save()));check(ids.size()==4,"cross-process four orders");auto b=l.save();l.submit(l.replay(ids[2]));l.execute(ids[2]);l.submit(l.replay(ids[3]),F05_UNSUPPORTED);check(l.save()==b,"cross-process completed/rejected idempotency");
  l.receive(ids[0]);l.execute(ids[0]);l.execute(ids[1]);check(l.save()==read(file+".future"),"different OS process exact future and RNG");
 } else throw std::runtime_error("unknown test");
}
int main(int argc,char** argv){try{check(argc>=2,"case required");run(argv[1],argc>2?argv[2]:"");std::cout<<argv[1]<<": PASS\n";return 0;}catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
