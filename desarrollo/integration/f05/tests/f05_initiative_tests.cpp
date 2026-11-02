#include "f05_initiative_test_support.h"
void run_initiative(const std::string& name,const std::string& file) {
 InitiativeLab l;
 if(name=="scenario") {
  const U n=l.ready_need();const auto before=decode(l.save());auto q=l.input(l.h.captain,n);auto d=l.evaluate(q);
  check(d.decision==F05_ISSUE_ORDER && d.detection && d.need==n && d.actor==l.h.captain.id,"NPC captain identifies known real need");
  auto r=l.view(d.order).receipt;check(r.state==F05_ISSUED && !r.task && !r.attempt,"decision is not receipt");
  check(decode(l.save()).campaign.streams==before.campaign.streams,"need and order no effect");
  d=l.step(l.h.ensign,n);r=l.view(d.order).receipt;check(r.state==F05_ACCEPTED && r.task && !r.result,"explicit NPC reception -> P01 task");
  const auto pending=l.save();d=l.step(l.h.ensign,n);r=l.view(d.order).receipt;const auto result=l.result(r.order);
  check(r.state==F05_COMPLETED && r.request && r.order && r.task && r.attempt && r.result && r.event,"full P01 causal lifecycle");
  check(result.performed && result.consumed_random && result.stream==0xF0401 && result.value>=1 && result.value<=100,"real Core consequence");
  Lab direct;direct.load(pending);direct.execute(r.order);check(decode(l.save()).campaign.streams==decode(direct.save()).campaign.streams,"initiative reuses the same P01 Core effect");
  check(l.events(r.order).size()==4 && l.decisions(l.h.captain).size()==1 && l.decisions(l.h.ensign).size()==2,"distinct decisions versus order events");
  check(kind_ids(decode(l.save()),"f05_detection").size()==3,"three causal detections");
  std::cout<<"need="<<n<<" captain="<<q.actor.id<<" operator="<<result.executor<<" request="<<r.request<<" order="<<r.order<<" task="<<r.task<<" attempt="<<r.attempt<<" result="<<r.result<<" event="<<r.event<<" stream="<<result.stream<<" value="<<result.value<<"\n";
 } else if(name=="authority") {
  const U n=l.ready_need();auto d=l.step(l.h.ensign,n);check(d.decision==F05_ESCALATE && !d.order && d.target==l.h.captain.id,"skill/rank no general command");
  l.brief(n,l.h.watch);d=l.step(l.h.watch,n);check(d.decision==F05_PROPOSE && !d.order,"XO proposes without captain authority");
  check(orders(decode(l.save())).empty() && decode(l.save()).campaign.streams.empty(),"no unauthorized effects or orders");
  l.brief(n,l.h.head);l.issue(n,l.h.head);l.finish(n);check(l.result(orders(decode(l.save()))[0]).performed,"head acts only inside Sensors scope");
 } else if(name=="delegation" || name=="revoked") {
  const U n=l.ready_need(),grant=l.grant();l.brief(n,l.h.watch);const U o=l.issue(n,l.h.watch);l.step(l.h.ensign,n);
  if(name=="revoked")l.change(grant,F05_REVOKED);
  auto d=l.step(l.h.ensign,n);auto r=l.result(o);
  check(r.performed==(name=="delegation") && r.code==(name=="delegation"?F04_OK:F04_REVOKED),"P02 revalidated by P01 at effect");
  if(name=="revoked"){check(d.decision==F05_ESCALATE,"record rejected continuation");l.step(l.h.watch,n);check(orders(decode(l.save())).size()==1 && decode(l.save()).campaign.streams.empty(),"cannot sidestep pinned revocation");}
 } else if(name=="relief") {
  const U n=l.ready_need(),o=l.issue(n);l.step(l.h.ensign,n);const U origin=l.view(o).origin;
  l.op(l.h.captain,F04_REVOKE,origin);l.step(l.h.ensign,n);check(l.result(o).code==F04_REVOKED && !l.result(o).performed,"lost appointment stops accepted task");
  auto d=l.step(l.h.captain,n);check(d.decision==F05_NO_ACTION && l.view(o).receipt.state==F05_FAILED,"completed failed attempt never retries");
 } else if(name=="medical") {
  const U n=l.ready_need(),o=l.issue(n);l.step(l.h.ensign,n);
  l.op(l.h.doctor,F04_MEDICAL,l.h.captain.id,0,0,60,F04_SICK);
  auto d=l.step(l.h.captain,n);check(d.decision==F05_NO_ACTION && d.code==F04_UNAVAILABLE,"incapacitated captain cannot plan");
  l.step(l.h.ensign,n);check(!l.result(o).performed && l.result(o).code==F04_UNAVAILABLE,"execution rechecks issuer health");
 } else if(name=="watch_end") {
  const U n=l.ready_need(),grant=l.grant(F05_DELEGATED_AUTONOMOUS,30);l.brief(n,l.h.watch);const U o=l.issue(n,l.h.watch);l.step(l.h.ensign,n);l.advance(30);
  auto d=l.step(l.h.ensign,n);check(d.decision==F05_ESCALATE && !l.result(o).performed && l.result(o).code==F04_EXPIRED,"delegated service end before need end stops effect");(void)grant;
 } else if(name=="player") {
  const U n=l.ready_need(l.h.ensign),o=l.issue(n);const auto streams=decode(l.save()).campaign.streams;
  check(l.step(l.h.captain,n).decision==F05_WAIT_PLAYER,"issuer waits for actual player");
  check(l.step(l.h.ensign,n).decision==F05_WAIT_PLAYER,"even evaluating player cannot auto accept");
  check(l.view(o).receipt.state==F05_ISSUED && !l.view(o).receipt.task && decode(l.save()).campaign.streams==streams,"absence is not consent");
  l.receive(o);l.execute(o);check(l.result(o).performed,"explicit authenticated player P01 input still works");
 } else if(name=="player_captain") {
  const U n=l.ready_need(l.h.captain);const U grant=l.grant(F05_PROPOSAL_REQUIRES_APPROVAL);l.brief(n,l.h.watch);
  auto d=l.step(l.h.watch,n);check(d.decision==F05_PROPOSE && d.order,"P02 proposal issued but no task");const U o=d.order;
  d=l.step(l.h.ensign,n);check(d.decision==F05_PROPOSE && d.code==F04_REVIEW && !l.view(o).receipt.task,"no approval inferred");
  d=l.step(l.h.captain,n);check(d.decision==F05_WAIT_PLAYER && !l.view(o).receipt.task,"player captain must decide");
  F05Receipt r{};eq(f05_approve_order(l.s,l.h.captain,l.stats().revision,o,50305,&r),F04_OK,"real P02 positive approval");
  l.finish(n);check(l.result(o).performed,"explicit approval then real effect");(void)grant;
 } else if(name=="knowledge") {
  l.prepare();const auto n=l.requirement();auto baseline=l.save();
  auto d=l.step(l.h.captain,n.id);check(d.decision==F05_CLARIFY && !d.need && !d.order && !d.detection,"real but unbriefed need is unknown even to captain");
  l.load(baseline);auto missing=l.step(l.h.captain,99999);check(missing.decision==d.decision && missing.code==d.code && missing.examined==d.examined && !missing.need,"unknown and nonexistent indistinguishable");
  l.brief(n.id,l.h.ensign);d=l.step(l.h.captain,n.id);check(d.decision==F05_CLARIFY,"another NPC's knowledge never inherited");
  l.brief(n.id,l.h.captain);l.issue(n.id);l.finish(n.id);
  const auto archive=decode(l.save());check(archive.campaign.knowledge.size()==20,"only explicit obligation reports, no fabricated discoveries from scan");
 } else if(name=="bounded") {
  const U n=l.ready_need();auto d=l.step(l.h.captain,n,1);check(d.decision==F05_CLARIFY && d.examined<=1 && !d.detection && !d.order,"context limit conservative");
  d=l.step(l.h.captain,n);check(d.examined==7 && d.decision==F05_ISSUE_ORDER && !l.view(d.order).receipt.task,"one transition max");
  InitiativeLab future;future.prepare();auto req=future.requirement(10,80);future.brief(req.id,future.h.captain);d=future.step(future.h.captain,req.id);check(d.decision==F05_NO_ACTION && !d.detection,"no use of future time");
  future.advance(10);future.issue(req.id);
 } else if(name=="determinism") {
  const U n=l.ready_need();auto start=l.save();U key=l.next;const U o=l.issue(n);l.finish(n);auto future=l.save();
  InitiativeLab offscreen;offscreen.load(start);offscreen.next=key;
  {auto presentation=std::make_unique<U>(offscreen.h.ensign.id);check(*presentation==l.h.ensign.id,"presentation references same logical identity");}
  check(offscreen.issue(n)==o,"same stable causal order ID");offscreen.finish(n);check(offscreen.save()==future,"same seed/input/revision/clock exact bytes without representation");
  offscreen.load(future);auto d=offscreen.step(offscreen.h.ensign,n);check(d.decision==F05_NO_ACTION && offscreen.result(o).value==l.result(o).value,"recreating representation never re-executes");
 } else if(name=="idempotency") {
  const U n=l.ready_need();auto q=l.input(l.h.captain,n);const auto d=l.evaluate(q);auto before=l.save();l.evaluate(q);check(l.save()==before,"same evaluation no duplicate detection/order");
  auto bad=q;++bad.max_facts;l.evaluate(bad,F04_ARGUMENT);bad=q;--bad.max_facts;l.evaluate(bad,F05_IDEMPOTENCY_CONFLICT);check(l.save()==before,"conflict atomic");
  l.finish(n);before=l.save();l.load(before);q.actor=l.h.captain;l.evaluate(q);check(l.save()==before,"persisted decision replay despite revision advance");
  l.step(l.h.captain,n);l.step(l.h.ensign,n);check(orders(decode(l.save())).size()==1 && l.events(d.order).size()==4,"fresh keys cannot duplicate completed need");
 } else if(name=="corrupt") {
  const U n=l.ready_need();l.issue(n);l.finish(n);auto good=l.save();auto archive=decode(good);auto decisions=kind_ids(archive,"f05_decision");
  auto broken=archive;change(broken,decisions[0],field_id(broken,decisions[0],F05_ISSUE_ORDER),F05_CONTINUE_TASK+100);auto bytes=encode(broken);
  eq(f04_load(l.s,bytes.data(),bytes.size()),F04_SAVE,"Core-valid invalid decision rejected");check(l.save()==good,"load rejection atomic");
  broken=archive;broken.campaign.knowledge.push_back({EntityId{l.h.doctor.id},KnownFact{{EntityId{1}}}});
  std::sort(broken.campaign.knowledge.begin(),broken.campaign.knowledge.end(),[](const auto& a,const auto& b){return a.observer==b.observer?a.fact.key<b.fact.key:a.observer<b.observer;});
  bytes=encode(broken);eq(f04_load(l.s,bytes.data(),bytes.size()),F04_SAVE,"unauthorized memory rejected");
  broken=archive;for(auto& edge:broken.campaign.relations)if(edge.source.value()==decisions[1] && edge.target.value()==n)edge.target=EntityId{l.h.sensors};bytes=encode(broken);eq(f04_load(l.s,bytes.data(),bytes.size()),F04_SAVE,"broken need causality rejected");check(l.save()==good,"bad causality never replaces live session");
  broken=archive;for(auto& edge:broken.campaign.relations)if(edge.source.value()==decisions[0] && edge.kind.value()==2)edge.target=EntityId{l.h.head.id};bytes=encode(broken);
  eq(f04_load(l.s,bytes.data(),bytes.size()),F04_SAVE,"decision cannot claim another actor's order or briefing");check(l.save()==good,"forged actor rejected atomically");
 } else if(name=="history" || name=="history_fault") {
  const U n=l.ready_need(),o=l.issue(n);l.step(l.h.ensign,n);
  std::filesystem::path dir=file;for(unsigned i=0;std::filesystem::exists(dir);++i)dir=file+"-"+std::to_string(i);
  std::array<uint8_t,16> uuid{5,3,1};eq(f04_history_migrate(l.s,dir.string().c_str(),uuid.data(),16),F04_OK,"migrate P03 same Core history");
  l.step(l.h.ensign,n);l.advance(8*86400);eq(f04_history_consolidate(l.s,86400,0),F04_OK,"retain need, brief, duty and authority closure");
  auto before=l.active();auto pending_input=l.input(l.h.ensign,n);
  eq(f04_history_publish(l.s,name=="history_fault"?6:0),name=="history_fault"?F04_SAVE:F04_OK,"publish durable P03 generation");
  if(name=="history_fault")l.evaluate(pending_input,F04_SAVE);
  eq(f04_history_open(l.s,dir.string().c_str()),F04_OK,"recover authoritative generation");l.handles();check(l.active()==before && l.result(o).performed,"exact P03 recovery");
  auto decision=l.decisions(l.h.ensign).back();F05Evaluation replay{l.h.ensign,n,decision.key,decision.input_revision,decision.max_facts,0};l.evaluate(replay);check(l.active()==before,"history decision replay idempotent");
 } else if(name=="population" || name=="population_relief") {
  f04_destroy(l.s);l.s=nullptr;F04PopulationConfig cfg{50301,404,130,0,0,0};eq(f04_create_population(1,"miranda",&cfg,&l.s),F04_OK,"real F04 populated campaign");l.handles();
  l.op(l.h.captain,F04_INSTALL_TEMPLATE,0,F04_SUTHERLAND_EQUIPMENT,0,0,F04_SUTHERLAND_SCIENCE);l.op(l.h.captain,F04_BOOTSTRAP_TEMPLATE);
  l.op(l.h.captain,F04_PLAN_WATCHES,0,0,0,86400,F04_REFERENCE);l.advance(28801);l.handles();
  F04Position positions[130]{};U count=0,total=0;eq(f04_positions_page(l.s,l.h.captain,0,positions,130,&count,&total),F04_OK,"real slots, duty and appointments");
  for(auto slot:positions)if(slot.person && slot.on_duty && slot.qualification==F04_SENSORS){l.h.ensign=l.person(slot.person);l.h.sensors=slot.id;l.service=slot.duty_record;break;}
  check(l.service && l.h.ensign.id,"actual F04 service source");l.op(l.h.ensign,F04_MOVE,l.h.sensors);l.bind(l.person(132));
  auto req=l.requirement(28801,28881);l.brief(req.id,l.h.captain);l.brief(req.id,l.h.ensign);const U o=l.issue(req.id);
  if(name=="population_relief") {
   l.step(l.h.ensign,req.id);l.op(l.h.captain,F04_CANCEL_DUTY,l.service);auto d=l.step(l.h.ensign,req.id);
   check(d.decision==F05_ESCALATE && !l.result(o).performed,"actual SCHEMA4 cancelled watch blocks pending effect");
   auto bytes=l.save();l.load(bytes);check(l.save()==bytes,"historical need interval remains valid after shortened service");
  } else {l.finish(req.id);check(l.result(o).performed,"populated F04 initiative all the way through Core");}
  std::cout<<"population=130 service="<<l.service<<" captain="<<l.h.captain.id<<" operator="<<l.h.ensign.id<<" slot="<<l.h.sensors<<" order="<<o<<"\n";
 } else if(name=="preissue_relief") {
  const U n=l.ready_need();const auto archive=decode(l.save());U origin=0;
  for(U a:kind_ids(archive,"appointment"))if(field(archive,a,11)==F04_CAPTAIN){origin=a;break;}
  check(origin!=0,"actual captain appointment");l.op(l.h.captain,F04_REVOKE,origin);
  auto d=l.step(l.h.captain,n);check(d.decision==F05_ESCALATE && !d.order && orders(decode(l.save())).empty(),"former captain re-evaluated before issuance");
 } else if(name=="selection") {
  const U n=l.ready_need();l.op(l.h.ensign,F04_MOVE,l.h.engineering);auto d=l.step(l.h.captain,n);
  check(d.decision==F05_REPORT && d.code==F04_UNAVAILABLE && !d.order,"logical location required even without Actor");
  l.op(l.h.ensign,F04_MOVE,l.h.sensors);l.op(l.h.head,F04_ABSENCE,l.h.ensign.id,0,0,60,F04_SICK);d=l.step(l.h.captain,n);
  check(d.decision==F05_ESCALATE && !d.order && decode(l.save()).campaign.streams.empty(),"unavailable qualified recipient never selected");
 } else if(name=="requirement") {
  l.prepare();F05ScanNeedRequest q{l.h.captain,l.service,900,l.stats().revision,0,80,50301};F05NeedView v{};
  eq(f05_scan_need(l.s,&q,&v),F04_OK,"register immutable obligation");const auto before=l.save();
  eq(f05_scan_need(l.s,&q,&v),F04_OK,"requirement replay");check(l.save()==before,"no duplicate requirement");
  ++q.end;eq(f05_scan_need(l.s,&q,&v),F05_IDEMPOTENCY_CONFLICT,"conflicting requirement");
  q={l.h.captain,l.service,901,l.stats().revision,0,30000,50301};eq(f05_scan_need(l.s,&q,&v),F04_ARGUMENT,"need cannot exceed source service");
  q.end=80;eq(f05_scan_need(l.s,&q,&v),F05_TRANSITION,"one obligation per service");check(l.save()==before,"invalid requirements no changes");
 } else if(name=="communication") {
  l.prepare();auto n=l.requirement();U b=0;const U revision=l.stats().revision;
  eq(f05_brief_need(l.s,l.h.captain,l.h.captain,revision,n.id,700,50302,&b),F04_OK,"actual report");auto before=l.save();const U original=b;
  eq(f05_brief_need(l.s,l.h.captain,l.h.captain,revision,n.id,700,50302,&b),F04_OK,"communication replay");check(b==original && l.save()==before,"no duplicated communication/knowledge");
  eq(f05_brief_need(l.s,l.h.captain,l.h.ensign,revision,n.id,700,50302,&b),F05_IDEMPOTENCY_CONFLICT,"cannot silently share report");
  eq(f05_brief_need(l.s,l.h.ensign,l.h.watch,l.stats().revision,n.id,701,50302,&b),F04_DENIED,"operator cannot publish unapproved knowledge");check(l.save()==before,"unauthorized report no learning");
  l.load(before);eq(f05_brief_need(l.s,l.h.captain,l.h.captain,revision,n.id,700,50302,&b),F04_OK,"persisted report replay");check(l.save()==before,"explicit knowledge persists");
 } else if(name=="scope") {
  const U n=l.ready_need();auto q=l.input(l.h.captain,n);auto before=l.save();q.actor.scope++;l.evaluate(q,F04_DENIED);check(l.save()==before,"foreign scope no effect");
  q.actor=l.h.captain;--q.expected_revision;l.evaluate(q,F04_STALE);check(l.save()==before,"stale initiative cannot act");
  eq(f05_bind_player(l.s,l.h.ensign,l.stats().revision),F05_IDEMPOTENCY_CONFLICT,"cannot relabel player as NPC");
  uint32_t code=0;std::thread worker([&]{F05DecisionView d{};code=f05_evaluate(l.s,&q,&d);});worker.join();eq(code,F04_THREAD,"single owner");
  F05ScanNeedRequest request{l.h.watch,l.service,777,l.stats().revision,0,80,50301};F05NeedView v{};eq(f05_scan_need(l.s,&request,&v),F04_DENIED,"no unauthorized need creation");check(l.save()==before,"denied inputs atomic");
 } else if(name=="atomic") {
  const U n=l.ready_need();auto occupied=l.request(500);l.submit(occupied);auto before=l.save();auto q=l.input(l.h.captain,n);q.key=500;
  l.evaluate(q,F05_IDEMPOTENCY_CONFLICT);check(l.save()==before,"P01 key collision rolls back all P03 audit and RNG");
 } else if(name=="process_save") {
  const U n=l.ready_need(),o=l.issue(n);l.step(l.h.ensign,n);write(file+".pending",l.save());
  auto q=l.input(l.h.ensign,n);auto d=l.evaluate(q);check(l.result(o).performed,"producer actual effect");write(file+".future",l.save());
  std::ofstream meta(file+".meta");meta<<n<<' '<<q.key<<' '<<q.expected_revision<<' '<<d.id<<'\n';check(bool(meta),"metadata");
  auto dir=std::filesystem::path(file+".history");for(unsigned i=0;std::filesystem::exists(dir);++i)dir=file+".history-"+std::to_string(i);
  std::array<uint8_t,16> uuid{5,3,2};eq(f04_history_migrate(l.s,dir.string().c_str(),uuid.data(),16),F04_OK,"publish cross-process generation");std::ofstream p(file+".history-path");p<<dir.string();
 } else if(name=="process_load") {
  U n=0,key=0,revision=0,id=0;std::ifstream meta(file+".meta");meta>>n>>key>>revision>>id;check(bool(meta),"separate-process causal inputs");
  l.load(read(file+".pending"));F05Evaluation q{l.h.ensign,n,key,revision,32,0};auto d=l.evaluate(q);check(d.id==id && l.save()==read(file+".future"),"different process identical future/decisions/RNG");
  const auto before=l.save();l.evaluate(q);check(l.save()==before,"different process replay no duplicate");
  std::ifstream path(file+".history-path");std::string directory;std::getline(path,directory);check(!directory.empty(),"history path");
  eq(f04_history_open(l.s,directory.c_str()),F04_OK,"separate-process Core history recovery");l.handles();q.actor=l.h.ensign;l.evaluate(q);check(l.active()==before,"historical cross-process replay byte identical");
 } else throw std::runtime_error("unknown P03 test");
}
int main(int argc,char** argv){try{check(argc>=2,"case required");run_initiative(argv[1],argc>2?argv[2]:"");std::cout<<argv[1]<<": PASS\n";return 0;}catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
