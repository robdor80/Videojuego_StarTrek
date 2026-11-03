#include "f05_initiative_test_support.h"
#include "f05_ai_provider.h"
#include <jsoncons/json.hpp>
#include <chrono>
using namespace trek::ai;
using json=jsoncons::json;

// Integration fixtures use only the trusted, single-owner native ABI. No Actor,
// UWorld, transport, wall-clock scheduler or second authoritative store exists.
struct AuditLab:InitiativeLab {
 F05AiContext begin(F04Ref who,U n,U route=F05_AI_FAST,U ttl=70) {
  F05AiRequest q{who,n,next++,stats().revision,stats().now+ttl,uint32_t(route),0};F05AiContext c{};
  eq(f05_ai_begin(s,&q,&c),F04_OK,"optional context");return c;
 }
 F05AiView settle(const F05AiContext& c,const std::string& body,U error=0) {
  F05AiView v{};eq(f05_ai_finish(s,person(c.actor),c.request,body.data(),body.size(),uint32_t(error),&v),F04_OK,"external response");return v;
 }
 F05AiView apply(const F05AiContext& c,U expected=F04_OK) {
  F05AiView v{};eq(f05_ai_apply(s,person(c.actor),c.request,&v),uint32_t(expected),"explicit handoff");return v;
 }
 F05DecisionView by_id(U id,F04Ref who) {
  for(auto d:decisions(who))if(d.id==id)return d;throw std::runtime_error("missing causal decision");
 }
 void no_roll(){check(decode(save()).campaign.streams.empty() && kind_ids(decode(save()),"f05_result").empty(),"no hidden effect/RNG");}
 F05DelegationView delegation(U id,F04Ref who={}) {
  F05DelegationView d{};eq(f05_delegation(s,who.id?who:h.captain,id,&d),F04_OK,"mandate view");return d;
 }
 F05OrderView order(U id,F04Ref who={}) {
  F05OrderView o{};eq(f05_order(s,who.id?who:h.captain,id,&o),F04_OK,"causal order");return o;
 }
 F05ResultView result_as(U id,F04Ref who) {
  F05ResultView r{};eq(f05_result(s,who,id,&r),F04_OK,"authorized result view");return r;
 }
 CampaignArchiveSnapshot snapshot() {
  U size=0;const auto code=f04_save(s,nullptr,0,&size);
  return decode(code==F04_SAVE?active():save());
 }
 void reject_archive(const CampaignArchiveSnapshot& archive) {
  const auto before=save();const auto old=h.captain;const auto b=encode(archive);
  eq(f04_load(s,b.data(),b.size()),F04_SAVE,"incoherent archive rejected");
  check(save()==before,"load failure preserves campaign, RNG and scope");
  F05DecisionView d[1]{};U count=0;uint32_t more=0;
  eq(f05_decisions_page(s,old,0,d,1,&count,&more),F04_OK,"failed load preserves bindings");
 }
};

void causal_scan(AuditLab& l,U o) {
 const auto r=l.result(o);auto events=l.events(o);
 check(r.performed && r.code==F04_OK && r.core_outcome==uint32_t(ActionOutcome::accepted) &&
  !r.core_rejection && r.stream==0xF0401 && r.consumed_random && r.value>=1 && r.value<=100,"actual Core roll");
 check(events.size()==4,"exact issued/accepted/executing/completed chain");
 const U states[]={F05_ISSUED,F05_ACCEPTED,F05_EXECUTING,F05_COMPLETED};
 for(size_t i=0;i<events.size();++i) {
  check(events[i].state==states[i] && events[i].previous==(i?events[i-1].id:0),"ordered causal links");
  check(events[i].request==events[0].request && events[i].order==o,"same request/order");
 }
 check(events[3].result==r.id && events[2].attempt==events[3].attempt && events[3].task==r.task,"result/task/attempt causality");
 const auto archive=l.snapshot();check(archive.campaign.streams.size()==1,"exactly one real RNG stream");
 check(archive.campaign.knowledge.size()==10*kind_ids(archive,"f05_brief").size(),"only explicitly communicated knowledge");
}

void run(const std::string& name,const std::string& file) {
 AuditLab l;
 if(name=="A_captain") {
  U n=l.ready_need();auto c=l.begin(l.h.captain,n);l.settle(c,response(c,F05_AI_ADVISE));
  auto knowledge=decode(l.save()).campaign.knowledge;U o=l.issue(n);l.no_roll();l.finish(n);causal_scan(l,o);
  check(decode(l.save()).campaign.knowledge==knowledge,"external advice and scan teach nothing");
 } else if(name=="B_command") {
  U n=l.ready_need(),g=l.grant();l.brief(n,l.h.watch);U o=l.issue(n,l.h.watch);l.step(l.h.ensign,n);
  auto c=l.begin(l.h.watch,n);const U origin=l.delegation(g).origin;
  l.op(l.h.captain,F04_REVOKE,origin);check(l.stats().commander==l.h.watch.id,"effective XO succession");
  check(l.settle(c,response(c)).status==F05_AI_STALE,"old optional snapshot retired");
  auto q=l.request(l.next++);q.issuer=l.h.captain;l.submit(q,F04_DENIED);
  l.step(l.h.ensign,n);check(!l.result_as(o,l.h.watch).performed && l.result_as(o,l.h.watch).code==F04_REVOKED,"old delegated origin cannot execute");
  auto d=l.step(l.h.watch,n);check(d.order==o && d.decision==F05_NO_ACTION,"new command respects terminal history");
  check(decode(l.save()).campaign.streams.empty(),"denied authority never consumes RNG");
 } else if(name=="B_cancel_successor") {
  U n=l.ready_need(),g=l.grant();l.brief(n,l.h.watch);U o=l.issue(n,l.h.watch);l.step(l.h.ensign,n);
  auto c=l.begin(l.h.watch,n);l.op(l.h.captain,F04_REVOKE,l.delegation(g).origin);
  check(l.stats().commander==l.h.watch.id,"delegate now effective commander");
  F05Receipt r{};eq(f05_cancel(l.s,l.h.watch,l.stats().revision,o,&r),F04_OK,"current commander cancels own former delegated order");
  check(r.state==F05_CANCELLED && !r.result,"cancellation has no operational effect");
  check(l.settle(c,response(c)).status==F05_AI_STALE,"late proposal cannot resurrect cancelled order");
  l.step(l.h.ensign,n);l.no_roll();
 } else if(name=="cancel_revoked_issuer") {
  U n=l.ready_need(),g=l.grant();l.brief(n,l.h.watch);U o=l.issue(n,l.h.watch);l.change(g,F05_REVOKED);
  auto before=l.save();F05Receipt r{};
  eq(f05_cancel(l.s,l.h.watch,l.stats().revision,o,&r),F04_REVOKED,"former delegate cannot cancel as issuer");
  check(l.save()==before,"denied cancellation unchanged");
  eq(f05_cancel(l.s,l.h.captain,l.stats().revision,o,&r),F04_OK,"current captain can cancel revoked grant order");l.no_roll();
 } else if(name=="availability") {
  U n=l.ready_need(),g=l.grant();l.brief(n,l.h.watch);U o=l.issue(n,l.h.watch);l.step(l.h.ensign,n);
  auto c=l.begin(l.h.watch,n);auto knowledge=decode(l.save()).campaign.knowledge;
  l.op(l.h.doctor,F04_MEDICAL,l.h.ensign.id,0,0,60,F04_SICK);
  check(l.settle(c,response(c)).status==F05_AI_STALE,"operator medical change invalidates external context");
  auto d=l.step(l.h.ensign,n);check(d.decision==F05_NO_ACTION && d.code==F04_UNAVAILABLE,"incapacitated NPC does not continue");
  l.execute(o,F04_UNAVAILABLE);check(!l.result(o).performed && decode(l.save()).campaign.streams.empty(),"direct effect also blocked without RNG");
  check(decode(l.save()).campaign.knowledge==knowledge && l.delegation(g).state==F05_ACTIVE,"medical state neither grants knowledge nor rewrites mandate");
 } else if(name=="C_revoked" || name=="C_suspended" || name=="C_expired" || name=="C_mode") {
  U n=l.ready_need(),g=l.grant();l.brief(n,l.h.watch);U o=l.issue(n,l.h.watch);l.step(l.h.ensign,n);
  const auto old=l.events(o);auto c=l.begin(l.h.watch,n);
  U expected=F04_REVOKED;
  if(name=="C_expired"){l.advance(80);expected=F04_EXPIRED;}
  else l.change(g,name=="C_revoked"?F05_REVOKED:name=="C_suspended"?F05_SUSPENDED:F05_ACTIVE,name=="C_mode"?F05_MANUAL:F05_DELEGATED_AUTONOMOUS);
  check(l.settle(c,response(c)).status==F05_AI_STALE,"late external context blocked");
  if(name=="C_expired")l.execute(o,F04_EXPIRED);
  else {l.step(l.h.ensign,n);if(name=="C_mode")expected=F04_REVIEW;}
  check(!l.result(o).performed && l.result(o).code==expected,"permission/time/mode revalidated at effect");
  const auto events=l.events(o);for(size_t i=0;i<old.size();++i)check(events[i].id==old[i].id && events[i].state==old[i].state && events[i].previous==old[i].previous,"prior events retained");
  check(decode(l.save()).campaign.streams.empty(),"rejected effect consumes no RNG");
 } else if(name=="D_player") {
  U n=l.ready_need(l.h.ensign);auto c=l.begin(l.h.captain,n);l.settle(c,response(c));U o=l.apply(c).order;
  for(unsigned i=0;i<3;++i)check(l.step(l.h.ensign,n).decision==F05_WAIT_PLAYER,"subordinate awaits explicit player input");
  c=l.begin(l.h.ensign,n);check(l.settle(c,response(c)).status==F05_AI_APPROVAL,"AI cannot supply player consent");l.apply(c);
  check(l.order(o).receipt.state==F05_ISSUED && !l.order(o).receipt.task,"still pending");l.no_roll();
  l.receive(o);l.execute(o);causal_scan(l,o);
 } else if(name=="E_player_captain") {
  U n=l.ready_need(l.h.captain),g=l.grant(F05_PROPOSAL_REQUIRES_APPROVAL);l.brief(n,l.h.watch);
  auto c=l.begin(l.h.watch,n);check(l.settle(c,response(c)).status==F05_AI_APPROVAL,"recommendation requires approval");U o=l.apply(c).order;
  auto d=l.step(l.h.ensign,n);check(d.decision==F05_PROPOSE && l.order(o).receipt.state==F05_ISSUED && !l.order(o).receipt.task,"operator cannot approve");
  F05Receipt r{};eq(f05_approve_order(l.s,l.h.watch,l.stats().revision,o,50501,&r),F04_DENIED,"XO cannot impersonate captain");
  l.no_roll();eq(f05_approve_order(l.s,l.h.captain,l.stats().revision,o,50501,&r),F04_OK,"explicit captain input");
  l.finish(n);causal_scan(l,o);check(l.delegation(g).mode==F05_PROPOSAL_REQUIRES_APPROVAL,"no mode widening");
 } else if(name=="F_officers" || name=="F_contradictions") {
  U n=l.ready_need(),g=l.grant();l.brief(n,l.h.watch);l.brief(n,l.h.head);
  auto c=l.begin(l.h.watch,n);auto second=l.begin(l.h.head,n);
  check(l.settle(c,response(c,name=="F_contradictions"?F05_AI_ADVISE:F05_AI_SCAN)).status==F05_AI_STALE,"later snapshot invalidates first response");
  check(l.settle(second,response(second)).status==F05_AI_STALE,"settlement itself changes revision");
  U o=l.issue(n,l.h.watch);l.step(l.h.captain,n);l.step(l.h.head,n);l.step(l.h.watch,n);
  check(l.step(l.h.relief,n).decision==F05_CLARIFY,"unbriefed officer learns nothing");
  l.finish(n);auto after=l.save();l.execute(o);check(l.save()==after,"no second operation");
  l.step(l.h.head,n);l.step(l.h.watch,n);check(orders(decode(l.save())).size()==1,"one order per need across officers");
  check(l.delegation(g).executor==l.h.ensign.id && l.delegation(g).station==l.h.sensors,"scope preserved");causal_scan(l,o);
 } else if(name=="G_timeout" || name=="G_quota" || name=="G_corrupt" || name=="G_injection" || name=="G_exception") {
  U n=l.ready_need(),g=l.grant();l.brief(n,l.h.watch);SimulatedProvider p;Config cfg{"mock-fast","mock-reasoning",10};
  if(name=="G_timeout")p.delay=100;
  if(name=="G_quota")p.reply.error=F05_AI_QUOTA;
  if(name=="G_exception")p.throw_poll=true;
  Job job(l.s,l.h.watch,&p);F05AiRequest q{l.h.watch,n,l.next++,l.stats().revision,70,F05_AI_FAST,0};
  eq(job.start(q,"known service only",cfg,100),F04_OK,"simulated optional provider");
  auto c=job.context();p.reply.body=response(c);
  if(name=="G_corrupt")p.reply.body="{broken";
  if(name=="G_injection"){auto j=json::parse(p.reply.body);j["actions"][0]["parameters"]["grant_command"]=true;p.reply.body=j.to_string();}
  F05AiView v{};eq(job.poll(name=="G_timeout"?110:100,v),F04_OK,"provider fault settled");
  check(v.status==(name=="G_corrupt" || name=="G_injection"?F05_AI_REJECTED:F05_AI_FALLBACK),"safe external fault category");l.no_roll();
  U o=l.issue(n,l.h.watch);l.finish(n);causal_scan(l,o);
  check(l.delegation(g).state==F05_ACTIVE,"provider cannot alter grant");
 } else if(name=="H_offscreen") {
  U n=l.ready_need(),g=l.grant();l.brief(n,l.h.watch);auto start=l.save();U key=l.next;
  auto c=l.begin(l.h.watch,n);l.settle(c,response(c));U o=l.apply(c).order;l.finish(n);auto future=l.save();
  AuditLab other;other.load(start);other.next=key;auto c2=other.begin(other.h.watch,n);other.settle(c2,response(c2));
  check(other.apply(c2).order==o,"same logical order without presentation");other.finish(n);
  check(other.save()==future,"exact world, history, knowledge, time and RNG bytes");causal_scan(l,o);(void)g;
 } else if(name=="J_time") {
  l.prepare();U n=l.requirement(10,80).id;l.brief(n,l.h.captain);l.brief(n,l.h.ensign);U g=l.grant();
  SimulatedProvider p;p.delay=100;Job job(l.s,l.h.captain,&p);F05AiRequest q{l.h.captain,n,l.next++,l.stats().revision,70,F05_AI_FAST,0};
  eq(job.start(q,"wait",{"mock","mock",10},0),F04_OK,"transport clock independent");
  auto paused=l.save();std::this_thread::sleep_for(std::chrono::milliseconds(50));
  F05AiView v{};eq(job.poll(9,v),F04_OK,"pending wall time");check(l.save()==paused && l.stats().now==0,"elapsed real time and poll cannot advance gameplay");
  eq(job.poll(60000,v),F04_OK,"transport timeout while paused");check(l.stats().now==0 && v.status==F05_AI_FALLBACK,"timeout is no game progress");
  check(l.step(l.h.captain,n).decision==F05_NO_ACTION,"future obligation still not due");auto frozen=l.save();
  AuditLab reopened;reopened.load(frozen);check(reopened.save()==frozen && reopened.stats().now==0,"save/close/load causes no offline catch-up");
  reopened.next=l.next;reopened.advance(10);check(orders(decode(reopened.save())).empty(),"explicit time advance alone does not schedule F05 work");
  U o=reopened.issue(n);reopened.finish(n);causal_scan(reopened,o);
  auto a=reopened.save();U count=99;eq(f04_advance(reopened.s,9,4096,&count),F04_ARGUMENT,"backward game time refused");check(reopened.save()==a && !count,"backward time atomic");
  check(reopened.delegation(g).state==F05_ACTIVE,"wall time never expires game mandate");
 } else if(name=="limits") {
  U n=l.ready_need();for(U budget:{1,6}){auto d=l.step(l.h.captain,n,budget);check(d.decision==F05_CLARIFY && !d.order && d.examined<=budget,"insufficient fact budget degrades safely");}
  auto before=l.save();auto q=l.input(l.h.captain,n);q.max_facts=33;l.evaluate(q,F04_ARGUMENT);check(l.save()==before,"invalid budget atomic");
  auto c=l.begin(l.h.captain,n,F05_AI_FAST,300);l.settle(c,"",F05_AI_QUOTA);l.no_roll();
  F05AiRequest request{l.h.captain,n,l.next++,l.stats().revision,301,F05_AI_FAST,0};F05AiContext out{};
  before=l.save();eq(f05_ai_begin(l.s,&request,&out),F04_ARGUMENT,"301 tick optional request rejected");check(l.save()==before,"TTL boundary atomic");
  U o=l.issue(n);l.finish(n);causal_scan(l,o);
 } else if(name=="capacity_ai") {
  U n=l.ready_need();for(unsigned i=0;i<512;++i)l.begin(l.h.captain,n);
  auto before=l.save();F05AiRequest q{l.h.captain,n,l.next++,l.stats().revision,70,F05_AI_FAST,0};F05AiContext c{};
  eq(f05_ai_begin(l.s,&q,&c),F04_CAPACITY,"optional request capacity enforced");check(l.save()==before && !c.request,"capacity failure atomic");
  U o=l.issue(n);l.finish(n);causal_scan(l,o);
 } else if(name=="capacity_orders") {
  U n=l.ready_need();for(unsigned i=0;i<512;++i){auto q=l.request(l.next++);q.operation=F04_BRIDGE;l.submit(q,F05_UNSUPPORTED);}
  auto before=l.save();l.evaluate(l.input(l.h.captain,n),F04_CAPACITY);check(l.save()==before,"full P01 capacity rolls back P03 transaction");
  check(kind_ids(decode(before),"f05_detection").empty() && decode(before).campaign.streams.empty(),"capacity creates no partial detection or RNG");
 } else if(name=="capacity_delegations") {
  U n=l.ready_need(),g=l.grant();l.brief(n,l.h.watch);
  F05DelegationRequest q{l.h.captain,l.h.watch,l.h.ship,l.person(l.h.sensors),l.h.ensign,0,0,0,80,50501,0,F04_SENSORS,F04_SCAN,F05_DELEGATED_AUTONOMOUS,0};F05DelegationView d{};
  for(unsigned i=1;i<256;++i){q.key=l.next++;q.expected_revision=l.stats().revision;eq(f05_delegate(l.s,&q,&d),F04_OK,"fill bounded mandate inventory");}
  q.key=l.next++;q.expected_revision=l.stats().revision;auto before=l.save();eq(f05_delegate(l.s,&q,&d),F04_CAPACITY,"mandate capacity enforced");check(l.save()==before,"mandate overflow atomic");
  U o=l.issue(n,l.h.watch);l.finish(n);causal_scan(l,o);check(l.delegation(g).state==F05_ACTIVE,"existing mandate still usable at capacity");
 } else if(name=="capacity_decisions") {
  U n=l.ready_need();for(unsigned i=0;i<2048;++i)check(l.step(l.h.watch,99999).decision==F05_CLARIFY,"unknown need never inferred at high load");
  auto before=l.save();l.evaluate(l.input(l.h.captain,n),F04_CAPACITY);check(l.save()==before,"decision overflow atomic");
  auto c=l.begin(l.h.captain,n);check(l.settle(c,response(c)).status==F05_AI_VALID,"optional interpretation acquires no capacity bypass");before=l.save();l.apply(c,F04_CAPACITY);check(l.save()==before,"P04 cannot bypass exhausted P03");
  auto o=l.accepted(l.next++).order;l.execute(o);causal_scan(l,o);
 } else if(name=="key_collision") {
  U n=l.ready_need();auto q=l.input(l.h.captain,n,1);l.evaluate(q);auto c=l.begin(l.h.captain,n);
  // A separate P04 namespace can use a P03 key; it must fail atomically at handoff.
  F05AiRequest request{l.h.captain,n,q.key,l.stats().revision,70,F05_AI_FAST,0};F05AiContext colliding{};
  eq(f05_ai_begin(l.s,&request,&colliding),F04_OK,"independent request key namespace");l.settle(colliding,response(colliding));auto before=l.save();
  l.apply(colliding,F05_IDEMPOTENCY_CONFLICT);check(l.save()==before,"cross-layer collision creates no partial decision or RNG");
  U o=l.issue(n);l.finish(n);causal_scan(l,o);(void)c;
 } else if(name=="archive_ttl") {
  U n=l.ready_need();auto c=l.begin(l.h.captain,n);auto archive=decode(l.save());
  change(archive,c.request,2,301);l.reject_archive(archive);
 } else if(name=="archive_causality") {
  U n=l.ready_need();auto c=l.begin(l.h.captain,n);l.settle(c,response(c));U o=l.apply(c).order;l.finish(n);
  const auto archive=decode(l.save());auto bad=archive;
  const U request=l.order(o).receipt.request;
  for(auto& edge:bad.campaign.relations)if(edge.source.value()==request && edge.kind.value()==24)edge.target=EntityId{c.request};
  l.reject_archive(bad);
  bad=archive;for(auto& edge:bad.campaign.relations)if(edge.source.value()==c.request && edge.kind.value()==26)edge.target=EntityId{l.decisions(l.h.ensign).back().id};
  l.reject_archive(bad);
 } else if(name=="I_process_save") {
  U n=l.ready_need(),g=l.grant(F05_PROPOSAL_REQUIRES_APPROVAL);l.brief(n,l.h.watch);
  auto c=l.begin(l.h.watch,n);l.settle(c,response(c));U o=l.apply(c).order;
  auto pending=l.begin(l.h.watch,n);write(file+".issued",l.save());
  F05Receipt r{};eq(f05_approve_order(l.s,l.h.captain,l.stats().revision,o,50501,&r),F04_OK,"approve for continuation");
  l.step(l.h.ensign,n);write(file+".accepted",l.save());U key=l.next;auto q=l.input(l.h.ensign,n);l.evaluate(q);causal_scan(l,o);write(file+".future",l.save());
  auto dir=file+".history";check(!std::filesystem::exists(dir),"fresh history output required");
  std::array<uint8_t,16> uuid{5,5,1};eq(f04_history_migrate(l.s,dir.c_str(),uuid.data(),16),F04_OK,"publish cross-process history");
  std::ofstream meta(file+".meta");meta<<n<<' '<<g<<' '<<o<<' '<<c.request<<' '<<pending.request<<' '<<key<<' '<<q.expected_revision<<'\n';check(bool(meta),"cross-process metadata");
 } else if(name=="I_process_load") {
  U n=0,g=0,o=0,applied=0,pending=0,key=0,revision=0;std::ifstream meta(file+".meta");meta>>n>>g>>o>>applied>>pending>>key>>revision;check(bool(meta),"actual producer metadata");
  l.load(read(file+".issued"));auto old=l.h.watch;l.load(l.save());F05AiView v{};
  eq(f05_ai_view(l.s,old,pending,&v),F04_DENIED,"pre-restore ref retired");
  eq(f05_ai_finish(l.s,l.h.watch,pending,nullptr,0,F05_AI_TIMEOUT,&v),F04_OK,"pending transport recovered");check(v.status==F05_AI_STALE && v.error==F05_AI_RECOVERED,"no automatic network retry");
  check(l.order(o).receipt.state==F05_ISSUED && !l.order(o).receipt.task && l.delegation(g).mode==F05_PROPOSAL_REQUIRES_APPROVAL,"issued state/approval preserved");
  l.load(read(file+".accepted"));F05Evaluation q{l.h.ensign,n,key,revision,32,0};l.evaluate(q);check(l.save()==read(file+".future"),"exact future and RNG in independent process");
  auto future=l.save();l.evaluate(q);eq(f05_ai_apply(l.s,l.h.watch,applied,&v),F04_OK,"durable P04 replay");check(l.save()==future,"idempotency survives process recovery");
  eq(f04_history_open(l.s,(file+".history").c_str()),F04_OK,"independent history recovery");l.handles();auto active=l.active();q.actor=l.h.ensign;l.evaluate(q);
  eq(f05_ai_apply(l.s,l.h.watch,applied,&v),F04_OK,"historical applied intent replay");check(l.active()==active,"history replay exact");causal_scan(l,o);
 } else throw std::runtime_error("unknown integration audit case");
}
int main(int argc,char** argv){try{check(argc>=3,"case and fresh output prefix required");run(argv[1],argv[2]);std::cout<<argv[1]<<": PASS\n";return 0;}catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<'\n';return 1;}}
