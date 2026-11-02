#include "f05_test_support.h"
#include "f05_delegation.h"
struct DelegationLab:Lab {
 U next_key=1000,command_duty=0;
 void ready_delegate(){ready();op(h.captain,F04_ASSIGN,h.bridge,h.watch.id);command_duty=op(h.captain,F04_DUTY,h.watch.id,h.bridge,0,28800).record;}
 F05DelegationRequest grant(U mode=F05_DELEGATED_AUTONOMOUS,U end=90){return {h.captain,h.watch,h.ship,person(h.sensors),h.ensign,next_key++,stats().revision,stats().now,end,50201,0,F04_SENSORS,F04_SCAN,uint32_t(mode),0};}
 F05DelegationView create(const F05DelegationRequest& q,U code=F04_OK){F05DelegationView v{};eq(f05_delegate(s,&q,&v),code,"create delegation");return v;}
 F05DelegationView change(U d,U state,U mode=F05_DELEGATED_AUTONOMOUS,U code=F04_OK,F04Ref actor={}){
  if(!actor.id)actor=h.captain;F05DelegationChange q{actor,d,next_key++,stats().revision,50202,uint32_t(state),uint32_t(mode)};
  F05DelegationView v{};eq(f05_change_delegation(s,&q,&v),code,"change delegation");return v;
 }
 U activate(U mode=F05_DELEGATED_AUTONOMOUS,U end=90){auto d=create(grant(mode,end));change(d.id,F05_ACTIVE,mode);return d.id;}
 F05Receipt issue(U d,U key=1,U code=F04_OK){auto q=request(key);q.issuer=h.watch;q.deadline=stats().now+80;F05Receipt r{};eq(f05_submit_delegated(s,&q,d,&r),code,"delegated submit");return r;}
 F05Receipt accept(U d,U key=1){return receive(issue(d,key).order);}
 F05DelegationView dv(U d){F05DelegationView v{};eq(f05_delegation(s,h.captain,d,&v),F04_OK,"delegation query");return v;}
 std::vector<F05DelegationEvent> de(U d){std::vector<F05DelegationEvent> out;U after=0,n=0;uint32_t more=0;do{F05DelegationEvent e[2]{};eq(f05_delegation_events(s,h.captain,d,after,e,2,&n,&more),F04_OK,"delegation event page");for(U i=0;i<n;++i){out.push_back(e[i]);after=e[i].id;}}while(more);return out;}
 F05Receipt replay_delegated(U d,U o,U code=F04_OK){auto q=replay(o);F05Receipt r{};eq(f05_submit_delegated(s,&q,d,&r),code,"replay delegated");return r;}
};
std::vector<U> grants(const CampaignArchiveSnapshot& d){std::vector<U> ids;for(auto x:d.campaign.definitions)if(x.definition_id=="trek.f04:delegation")ids.push_back(x.entity.value());return ids;}
void delegation_run(const std::string& name,const std::string& file){
 DelegationLab l;
 if(name=="valid") {
  l.ready_delegate();auto q=l.grant();auto d=l.create(q);check(d.state==F05_DRAFT && d.effective_code==F04_REVOKED,"draft has no authority");l.issue(d.id,1,F04_REVOKED);
  l.change(d.id,F05_ACTIVE);auto a=l.accept(d.id,2);auto pending=l.save();l.execute(a.order);auto result=l.result(a.order);
  check(result.performed && result.consumed_random && result.stream==0xF0401,"real Core effect");
  Lab direct;direct.load(pending);direct.op(direct.h.ensign,F04_SCAN);check(decode(direct.save()).campaign.streams==decode(l.save()).campaign.streams,"same F04 Core stream");
  const auto snap=decode(l.save());bool real=false;for(auto x:snap.campaign.definitions)if(x.entity.value()==d.id)real=x.definition_id=="trek.f04:delegation";check(real,"existing F04 entity in real Core archive");
  std::cout<<"delegation="<<d.id<<" origin="<<d.origin<<" holder="<<d.holder<<" order="<<a.order<<" stream="<<result.stream<<" value="<<result.value<<"\n";
 } else if(name=="scope") {
  l.ready_delegate();auto d=l.activate();auto q=l.request();q.issuer=l.h.watch;q.deadline=l.stats().now+80;q.station.id=l.h.engineering;F05Receipt r{};
  eq(f05_submit_delegated(l.s,&q,d,&r),F04_SCOPE,"station restriction");q=l.request(2);q.issuer=l.h.watch;q.deadline=l.stats().now+80;q.recipient=l.h.relief;eq(f05_submit_delegated(l.s,&q,d,&r),F04_SCOPE,"executor restriction");
  q=l.request(3);q.issuer=l.h.watch;q.deadline=l.stats().now+80;q.operation=F04_BRIDGE;eq(f05_submit_delegated(l.s,&q,d,&r),F04_SCOPE,"permission restriction");
  q=l.request(4);q.issuer=l.h.head;q.deadline=l.stats().now+80;eq(f05_submit_delegated(l.s,&q,d,&r),F04_DENIED,"cannot use someone else's grant even with own authority");
  q=l.request(5);q.issuer=l.h.watch;q.deadline=91;eq(f05_submit_delegated(l.s,&q,d,&r),F04_EXPIRED,"duration restriction");
  check(decode(l.save()).campaign.streams.empty(),"no unauthorized Core action");
 } else if(name=="authority") {
  l.ready_delegate();auto q=l.grant();q.delegant=l.h.head;l.create(q,F04_DENIED);
  q=l.grant();q.delegant=l.h.admiral;l.create(q,F04_UNAVAILABLE);
  q=l.grant();q.delegate=l.h.civilian;l.create(q,F04_UNAVAILABLE);
  q=l.grant();q.delegate=l.h.ensign;l.create(q,F04_QUALIFICATION);
  q=l.grant();q.executor=l.h.doctor;l.create(q,F04_QUALIFICATION);
  q=l.grant();q.end=28801;l.create(q,F04_EXPIRED);
  q=l.grant();q.domain=F04_POLICY;l.create(q,F05_UNSUPPORTED);
  q=l.grant();q.ship.scope++;l.create(q,F04_SCOPE);
 } else if(name=="revoke") {
  l.ready_delegate();auto d=l.activate();auto done=l.accept(d,1);l.execute(done.order);auto past=l.events(done.order);auto streams=decode(l.save()).campaign.streams;
  auto pending=l.accept(d,2);l.change(d,F05_REVOKED);l.execute(pending.order,F04_REVOKED);check(!l.result(pending.order).performed,"revoked pending never executes");
  check(l.events(done.order).size()==past.size() && l.result(done.order).performed,"confirmed past preserved");check(decode(l.save()).campaign.streams==streams,"no second roll");
  l.change(d,F05_ACTIVE,F05_DELEGATED_AUTONOMOUS,F05_TRANSITION);l.issue(d,3,F04_REVOKED);
  l.load(l.save());l.replay_delegated(d,done.order);l.execute(done.order);l.replay_delegated(d,pending.order,F04_REVOKED);
 } else if(name=="suspend") {
  l.ready_delegate();auto d=l.activate();auto p=l.accept(d);l.change(d,F05_SUSPENDED);l.execute(p.order,F04_REVOKED);
  l.change(d,F05_ACTIVE);auto ok=l.accept(d,2);l.execute(ok.order);check(l.result(ok.order).performed,"explicit reactivation after rechecks");
 } else if(name=="expiry") {
  l.ready_delegate();auto d=l.activate(F05_DELEGATED_AUTONOMOUS,80);auto p=l.accept(d);l.advance(80);l.execute(p.order,F04_EXPIRED);
  check(l.dv(d).effective_code==F04_EXPIRED,"effective expiry requires no scheduler");l.change(d,F05_EXPIRED);check(l.de(d).back().state==F05_EXPIRED,"expiry audit persisted");
 } else if(name=="relief") {
  l.ready_delegate();auto d=l.activate();auto p=l.accept(d);l.op(l.h.captain,F04_RELIEF,l.command_duty,l.h.captain.id);l.execute(p.order,F04_UNAVAILABLE);check(!l.result(p.order).performed,"relieved watch cannot issue through delegation");
 } else if(name=="origin") {
  l.ready_delegate();auto d=l.activate();auto p=l.accept(d);l.op(l.h.captain,F04_REVOKE,l.dv(d).origin);l.execute(p.order,F04_REVOKED);
  check(l.stats().commander==l.h.watch.id,"F04 successor is still scoped by original source");F05ResultView result{};eq(f05_result(l.s,l.h.ensign,p.order,&result),F04_OK,"recipient still sees result");check(!result.performed,"new command does not rescue pinned revoked grant");
 } else if(name=="medical") {
  l.ready_delegate();auto d=l.activate();auto p=l.accept(d);l.op(l.h.doctor,F04_MEDICAL,l.h.captain.id,0,0,90,F04_SICK);l.execute(p.order,F04_UNAVAILABLE);
 } else if(name=="subdelegate") {
  l.ready_delegate();auto d=l.activate();auto q=l.grant();q.parent=d;q.delegant=l.h.watch;q.delegate=l.h.head;l.create(q,F05_UNSUPPORTED);
  q=l.grant();q.delegant=l.h.watch;q.delegate=l.h.head;l.create(q,F04_DENIED); // grant never makes a commander
  F04Request req{l.h.watch,l.stats().revision,F04_POLICY,4,0,0,0,0,50201};F04Result result{};eq(f04_execute(l.s,&req,&result),F04_DENIED,"scan delegation grants no F04 policy");
 } else if(name=="modes") {
  l.ready_delegate();for(U mode:{U(F05_MANUAL),U(F05_PROPOSAL_REQUIRES_APPROVAL)}) {
   auto d=l.activate(mode);auto r=l.issue(d,mode);auto before=l.save();l.receive(r.order,F04_REVIEW);check(l.save()==before,"proposal cannot accept or roll without approval");
   F05Receipt out{};eq(f05_approve_order(l.s,l.h.watch,l.stats().revision,r.order,1,&out),F04_DENIED,"delegate cannot self approve");
   auto rev=l.stats().revision;eq(f05_approve_order(l.s,l.h.captain,rev,r.order,1,&out),F04_OK,"real current captain approval");
   before=l.save();eq(f05_approve_order(l.s,l.h.captain,rev,r.order,1,&out),F04_OK,"approval replay");check(l.save()==before,"approval idempotent");
   l.receive(r.order);if(mode==F05_MANUAL){l.execute(r.order);check(l.result(r.order).performed,"approved manual action");}else{l.change(d,F05_REVOKED,mode);l.execute(r.order,F04_REVOKED);}
  }
 } else if(name=="mode_change") {
  l.ready_delegate();auto d=l.activate();auto p=l.accept(d);l.change(d,F05_ACTIVE,F05_MANUAL);l.execute(p.order,F04_REVIEW);check(!l.result(p.order).performed,"mode revision rechecked at effect");
 } else if(name=="idempotency") {
  l.ready_delegate();auto q=l.grant();auto d=l.create(q);auto before=l.save();l.create(q);check(l.save()==before,"create replay");auto bad=q;bad.end--;l.create(bad,F05_IDEMPOTENCY_CONFLICT);
  F05DelegationChange c{l.h.captain,d.id,2000,l.stats().revision,2,F05_ACTIVE,F05_DELEGATED_AUTONOMOUS};F05DelegationView v{};
  eq(f05_change_delegation(l.s,&c,&v),F04_OK,"activate");before=l.save();eq(f05_change_delegation(l.s,&c,&v),F04_OK,"change replay");check(l.save()==before,"change replay unchanged");
  c.state=F05_REVOKED;eq(f05_change_delegation(l.s,&c,&v),F05_IDEMPOTENCY_CONFLICT,"change conflict");
  l.load(before);q.delegant=l.h.captain;q.delegate=l.h.watch;q.ship=l.h.ship;q.station=l.person(q.station.id);q.executor=l.h.ensign;l.create(q);check(l.save()==before,"create idempotency after restore");
  auto o=l.issue(d.id);auto r=l.replay(o.order);l.submit(r,F05_IDEMPOTENCY_CONFLICT);check(l.view(o.order).receipt.state==F05_ISSUED,"cannot remove pinned delegation on replay");
 } else if(name=="causal") {
  l.ready_delegate();auto d=l.activate();l.change(d,F05_SUSPENDED);l.change(d,F05_ACTIVE);l.change(d,F05_REVOKED);auto events=l.de(d);check(events.size()==5,"complete causal lifecycle");
  U prev=0;for(auto e:events){check(e.previous==prev && e.delegation==d && e.actor==l.h.captain.id,"event chain identity");prev=e.id;}auto before=l.save();l.load(before);check(l.de(d).size()==5 && l.save()==before,"lifecycle persisted");
  auto broken=decode(before);for(auto& edge:broken.campaign.relations)if(edge.source.value()==events[4].id && edge.target.value()==events[3].id)edge.target=EntityId{events[0].id};auto b=encode(broken);eq(f04_load(l.s,b.data(),b.size()),F04_SAVE,"Core-valid broken delegation causal chain rejected");check(l.save()==before,"bad load atomic");
 } else if(name=="history") {
  l.ready_delegate();auto d=l.activate();auto done=l.accept(d);l.execute(done.order);auto p=l.accept(d,2);l.change(d,F05_REVOKED);l.execute(p.order,F04_REVOKED);l.advance(8*86400);
  std::filesystem::path dir=file;for(unsigned i=0;std::filesystem::exists(dir);++i)dir=file+"-"+std::to_string(i);std::array<uint8_t,16> uuid{5,2,1};
  eq(f04_history_migrate(l.s,dir.string().c_str(),uuid.data(),16),F04_OK,"same Core history migration");eq(f04_history_consolidate(l.s,86400,0),F04_OK,"retain delegation/order causal closure");eq(f04_history_publish(l.s,0),F04_OK,"publish");
  auto before=l.Lab::active();
  DelegationLab recovered;eq(f04_history_open(recovered.s,dir.string().c_str()),F04_OK,"Core recover delegation history");recovered.handles();check(recovered.Lab::active()==before,"exact historical projection");
  recovered.replay_delegated(d,done.order);recovered.execute(done.order);recovered.replay_delegated(d,p.order,F04_REVOKED);check(recovered.Lab::active()==before,"history replay cannot duplicate effect");check(recovered.de(d).size()==3,"retained causal delegation events");
 } else if(name=="restore_and_access") {
  l.ready_delegate();auto d=l.activate();auto saved=l.save();l.load(saved);F05DelegationView found[2]{};U n=0;uint32_t more=0;
  eq(f05_delegations_page(l.s,l.h.captain,0,found,2,&n,&more),F04_OK,"recover delegation inventory from Core");check(n==1 && !more && found[0].id==d && found[0].effective_code==F04_OK,"recovered live authority");
  eq(f05_delegations_page(l.s,l.h.ensign,0,found,2,&n,&more),F04_OK,"unrelated crew filtered");check(!n,"no universal read by crew");
  auto r=l.accept(d);F05Receipt out{};eq(f05_cancel(l.s,l.h.watch,l.stats().revision,r.order,&out),F04_OK,"delegated issuer can cancel own pending order");
  F04Request revoke{l.h.captain,l.stats().revision,F04_REVOKE,0,d,0,0,0,50203};F04Result result{};eq(f04_execute(l.s,&revoke,&result),F04_REVIEW,"legacy revoke cannot bypass P02 lifecycle log");
  auto pending=l.accept(d,2);l.op(l.h.captain,F04_REVOKE,l.dv(d).holder);l.execute(pending.order,F04_REVOKED);check(!l.result(pending.order).performed,"lost recipient appointment rechecked");
 } else if(name=="population") {
  f04_destroy(l.s);l.s=nullptr;F04PopulationConfig cfg{50201,404,130,0,0,0};eq(f04_create_population(1,"miranda",&cfg,&l.s),F04_OK,"population");l.handles();
  l.op(l.h.captain,F04_INSTALL_TEMPLATE,0,F04_SUTHERLAND_EQUIPMENT,0,0,F04_SUTHERLAND_SCIENCE);l.op(l.h.captain,F04_BOOTSTRAP_TEMPLATE);
  l.op(l.h.captain,F04_PLAN_ALPHA,0,0,28800,57600);l.advance(28800);
  std::vector<F04Position> positions(130);U n=0,total=0;eq(f04_positions_page(l.s,l.h.captain,0,positions.data(),130,&n,&total),F04_OK,"F04 positions");
  bool sensor=false,first=false;for(auto slot:positions)if(slot.person && slot.on_duty){if(slot.qualification==F04_SENSORS && !sensor){l.h.ensign=l.person(slot.person);l.h.sensors=slot.id;sensor=true;}if(slot.responsibility==F04_FIRST){l.h.watch=l.person(slot.person);first=true;}}
  check(sensor && first,"real current officer appointments and station operators");l.op(l.h.ensign,F04_MOVE,l.h.sensors);
  auto q=l.grant(F05_DELEGATED_AUTONOMOUS,28900);auto d=l.create(q);l.change(d.id,F05_ACTIVE);auto r=l.accept(d.id);l.execute(r.order);check(l.result(r.order).performed,"populated F04 organization uses same real delegation and scan");
 } else if(name=="process_save") {
  l.ready_delegate();auto d=l.activate();auto a=l.accept(d);auto done=l.accept(d,2);l.execute(done.order);write(file+".pending",l.save());l.change(d,F05_REVOKED);l.execute(a.order,F04_REVOKED);write(file+".future",l.save());
  std::filesystem::path dir=file+".history";for(unsigned i=0;std::filesystem::exists(dir);++i)dir=file+".history-"+std::to_string(i);std::array<uint8_t,16> uuid{5,2,2};
  eq(f04_history_migrate(l.s,dir.string().c_str(),uuid.data(),16),F04_OK,"publish delegation cross-process history");std::ofstream path(file+".history-path");path<<dir.string();check(bool(path),"history path");
 } else if(name=="process_load") {
  l.load(read(file+".pending"));auto ids=orders(decode(l.save()));auto ds=grants(decode(l.save()));check(ids.size()==2 && ds.size()==1,"cross-process delegation/order identities");U d=ds[0];auto before=l.save();l.replay_delegated(d,ids[1]);l.execute(ids[1]);check(l.save()==before,"completed idempotency across process");
  l.next_key=1002;l.change(d,F05_REVOKED);l.execute(ids[0],F04_REVOKED);check(l.save()==read(file+".future"),"exact revoked future across process");
  std::ifstream path(file+".history-path");std::string dir;std::getline(path,dir);check(bool(path),"history directory");DelegationLab other;eq(f04_history_open(other.s,dir.c_str()),F04_OK,"cross-process Core history recover");other.handles();auto checkpoint=other.Lab::active();check(checkpoint==l.save(),"exact historical future");
  other.replay_delegated(d,ids[1]);other.execute(ids[1]);other.replay_delegated(d,ids[0],F04_REVOKED);check(other.Lab::active()==checkpoint,"cross-process historical idempotency");
 } else throw std::runtime_error("unknown delegation case");
}
int main(int argc,char** argv){try{check(argc>=2,"case required");delegation_run(argv[1],argc>2?argv[2]:"");std::cout<<argv[1]<<": PASS\n";return 0;}catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
