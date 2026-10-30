#include "organization_lab.h"
#include <chrono>
#include <sstream>
constexpr U day=86400;
struct Sovereign:Lab {
 Sovereign(U n=700):Lab(true,n,"sovereign",true,F04_SOVEREIGN_MULTIMISSION){}
 U actor(){return stats().commander;}
 void plan(U days=1,bool reference=true,U start=0,bool seed=false) {op(F04_PLAN_WATCHES,0,seed?1:0,start,start+days*day,reference?F04_REFERENCE:F04_ROTATING,F04_OK,actor());}
 std::vector<F04DutyView> duties(){U n=0,total=0;std::vector<F04DutyView> d(22000);check(f04_duties_page(s,observer,0,d.data(),d.size(),&n,&total)==F04_OK && n==total,"duties");d.resize(n);return d;}
 std::vector<F04RosterGap> gaps(){U n=0,total=0;std::vector<F04RosterGap> d(2000);check(f04_roster_gaps_page(s,observer,0,d.data(),d.size(),&n,&total)==F04_OK && n==total,"gaps");d.resize(n);return d;}
 std::vector<F04ServiceCoverage> coverage(U start,U end){U n=0;std::vector<F04ServiceCoverage> c(8);check(f04_service_coverage(s,observer,start,end,c.data(),8,&n)==F04_OK && n==8,"coverage");return c;}
};
struct Metrics {U shifts=0,critical_gaps=0,quota_gaps=0,max7=0,min_gap=UINT64_MAX,off_days=0,rotating=0;};
Metrics audit(Sovereign& l,U days,bool critical=true) {
 Metrics m;std::map<U,std::vector<F04DutyView>> people;std::map<U,F04Position> slots;
 for(auto p:l.positions())slots[p.id]=p;
 for(auto d:l.duties())if(d.start<d.stopped_at) {
  ++m.shifts;people[d.person].push_back(d);check(d.ordinary==1 && d.end-d.start<=28800,"ordinary hours");
  U mask=l.credentials(d.person);check((mask&slots.at(d.slot).qualification_mask)==slots.at(d.slot).qualification_mask,"real complete credentials");
 }
 for(auto& [p,list]:people) {
  std::sort(list.begin(),list.end(),[](auto a,auto b){return a.start<b.start;});
  std::set<U> labels,worked_days;
  for(size_t i=0,left=0;i<list.size();++i) {
   while(list[i].start-list[left].start>=7*day)++left;
   m.max7=std::max(m.max7,U(i-left+1));check(i-left+1<=5,"independent rolling seven-day ceiling");
   check(worked_days.insert(list[i].start/day).second,"one ordinary shift per day");labels.insert(list[i].start%day/28800);
   if(i){check(list[i].start>=list[i-1].stopped_at+43200,"independent twelve-hour interval");m.min_gap=std::min(m.min_gap,list[i].start-list[i-1].stopped_at);}
  }
  m.off_days+=days-worked_days.size();if(labels.size()>1)++m.rotating;
 }
 for(const auto& g:l.gaps())if(g.station)++m.critical_gaps;else m.quota_gaps+=g.missing;
 if(critical)for(U d=0;d<days;++d)for(U w=0;w<3;++w)for(auto c:l.coverage(d*day+w*28800,d*day+(w+1)*28800)){if(!c.covered)std::cerr<<"COVERAGE GAP station="<<c.station<<" start="<<c.start<<" first="<<c.first_gap<<"\n";check(c.covered && c.first_gap==c.end,"entire critical window covered");}
 std::cout<<"METRICS days="<<days<<" shifts="<<m.shifts<<" critical_gaps="<<m.critical_gaps<<" quota_missing="<<m.quota_gaps<<" max_rolling7="<<m.max7<<" min_gap_seconds="<<m.min_gap<<" off_days="<<m.off_days<<" changed_shift_people="<<m.rotating<<"\n";
 return m;
}
void run(const std::string& name,const std::string& file) {
 Sovereign l;
 if(name=="structure") {
  const auto o=l.org();check(o.positions==700 && o.departments==7 && o.sections==59 && o.assigned==700 && o.vacant==0,"organization");
  check(l.stats().crew==700 && l.stats().civilians==0 && l.stats().passengers==0,"nominal categories");
  std::set<U> ids,persons;std::map<U,std::array<U,4>> expected;
  std::ifstream f(std::string(F04_FIXTURE_DIR)+"/sovereign_approved.tsv");check(bool(f),"approved fixture");
  U section,total,a,b,g,off;while(f>>section>>total>>a>>b>>g>>off){check(total==a+b+g+off,"approved sum");expected[section]={total,a,b,g};}
  check(expected.size()==59,"independent 59 sections");
  std::map<U,U> counts;for(auto p:l.positions()){check(ids.insert(p.stable_id).second && persons.insert(p.person).second,"unique positions and people");++counts[p.section];check(p.stable_id==p.section*100+p.ordinal,"stable keys");}
  for(auto [s,x]:expected)check(counts[s]==x[0],"independent section total");
  U n=0;std::array<F04WatchDemand,59>d{};check(f04_template_watch_demands(3,d.data(),59,&n)==F04_OK && n==59,"watch data");for(auto x:d)check(expected[x.section]==std::array<U,4>{counts[x.section],x.alpha,x.beta,x.gamma},"approved demands");
  U seconds=0;for(auto p:l.positions())seconds+=p.responsibility==F04_SECOND;check(seconds==1,"one explicitly appointed second");
 }
 else if(name=="reference") {
  l.plan();auto ds=l.duties();check(ds.size()==480,"480 distinct daily duties");
  std::map<U,F04Position> slots;for(auto p:l.positions())slots[p.id]=p;
  std::map<U,std::array<U,3>> counts;std::set<U> people;std::array<U,3> totals{};
  for(auto d:ds){check(people.insert(d.person).second,"one daily shift");U w=(d.start%day/28800+2)%3;++counts[slots[d.slot].section][w];++totals[w];}
  check(totals==std::array<U,3>{230,150,100} && 700-people.size()==220,"700/230/150/100/220");
  std::ifstream f(std::string(F04_FIXTURE_DIR)+"/sovereign_approved.tsv");U s,t,a,b,g,o;while(f>>s>>t>>a>>b>>g>>o)check(counts[s]==std::array<U,3>{a,b,g},"per-section reference watches");
  for(auto g:l.gaps())std::cerr<<"GAP dept="<<g.department<<" station="<<g.station<<" start="<<g.start<<" missing="<<g.missing<<"\n";check(l.gaps().empty(),"reference no gaps");audit(l,1);
  check(l.person(3).on_duty==0 && l.person(l.actor()).on_duty==1,"Gamma command while captain off duty");
  l.advance(28800);check(l.org().on_duty==230 && l.actor()==3 && l.person(3).on_duty,"Alpha captain");
  l.advance(57600);check(l.org().on_duty==150 && l.actor()!=3,"Beta relief");
  l.advance(86400);check(l.org().on_duty==0 && l.actor()==0,"horizon ends honestly, no invented recurrence");
 }
 else if(name=="7" || name=="14" || name=="28") {
  U days=std::stoull(name);l.plan(days,false,0,true);auto m=audit(l,days);
  check(m.critical_gaps==0 && m.max7<=5 && m.off_days>0,"sustainable minimum services");
  if(days>=14)check(m.rotating>0,"actual watch rotation");
  auto ds=l.duties();U captain=0,first=l.post(2).person;std::set<U> captain_days,first_days;
  for(auto d:ds){if(d.person==3){++captain;captain_days.insert(d.start/day);}if(d.person==first)first_days.insert(d.start/day);}
  check(captain<=days/7*5 && captain_days.size()<days && first_days.size()<days,"captain and first rest");
  l.advance(days*day-1);check(l.actor()!=0 && l.person(l.actor()).on_duty,"offscreen final watch");
 }
 else if(name=="temporal") {
  l.plan(2,false,0,true);for(U tick:{0ULL,28799ULL,28800ULL,57599ULL,57600ULL,86399ULL,86400ULL,115200ULL}) {
   F04WatchWindow w{};check(f04_watch_window(l.s,tick,&w)==F04_OK && w.start<=tick && tick<w.end && w.end-w.start==28800,"half-open boundaries");
   l.advance(tick);auto who=l.actor();check(who && l.person(who).on_duty,"effective commander each boundary");
  }
 }
 else if(name=="authority") {
  l.plan();l.advance(28800);const auto second=l.post(3).person;check(second!=3 && second!=l.post(2).person,"distinct second");
  U security=l.post(37).person,adj=l.post(9,2).person;
  l.op(F04_BRIDGE,0,0,0,0,2,F04_DENIED,security);l.op(F04_BRIDGE,0,0,0,0,2,F04_DENIED,adj);
  l.op(F04_ABSENCE,3,0,28800,57600,F04_LEAVE);check(l.actor()==l.post(2).person,"first succeeds captain");
  l.op(F04_ABSENCE,l.post(2).person,0,28800,57600,F04_LEAVE,F04_OK,l.actor());check(l.actor()==second,"explicit second succeeds first");
  l.op(F04_ABSENCE,second,0,28800,57600,F04_LEAVE,F04_OK,l.actor());check(l.actor()!=0 && l.actor()!=adj && l.actor()!=security,"watch successor, no deputy promotion");
 }
 else if(name=="absence" || name=="leave" || name=="cover") {
  l.plan();auto c=l.coverage(0,28800);U target=0,substitute=0;auto positions=l.positions();
  for(auto d:l.duties())if(d.person==c[2].person && d.start==0)target=d.id;
  check(target!=0,"sensor duty");const U outgoing=c[2].person;
  for(auto p:positions)if(p.section==20 && !l.person(p.person).on_duty && p.person!=outgoing) {
   bool busy=false;for(auto d:l.duties())if(d.person==p.person)busy=true;if(!busy){substitute=p.person;break;}
  }
  check(substitute!=0,"real off-day qualified substitute");
  F04ReliefCandidate candidates[700]{};U written=0,total=0;
  check(f04_relief_candidates_page(l.s,l.observer,target,0,28800,0,candidates,700,&written,&total)==F04_OK && written==total && total>0,"real candidate search");
  bool found=false;for(U i=0;i<written;++i)found|=candidates[i].person==substitute;check(found,"known qualified off-day candidate found");
  l.op(F04_ABSENCE,outgoing,0,0,28800,name=="leave"?F04_LEAVE:F04_SICK,F04_OK,l.actor());
  check(!l.coverage(0,28800)[2].covered,"absence exposes actual gap");
  bool recorded=false;for(auto g:l.gaps())recorded|=g.station==F04_ST_SENSORS;check(recorded,"incident deficit persisted");
  l.op(F04_COVER_DUTY,target,substitute,0,28800,0,F04_OK,l.actor());
  check(l.coverage(0,28800)[2].covered && l.person(substitute).on_duty,"qualified temporary cover");
  check(l.positions().size()==700 && l.stats().crew==700,"no new identities");
  auto after=l.positions();for(size_t i=0;i<positions.size();++i)check(after[i].person==positions[i].person,"all permanent destinations preserved");
  check(l.duties().back().temporary==1,"temporary explicitly recorded");
  l.advance(28800);check(l.person(outgoing).available,"return after absence expires");
 }
 else if(name=="deficit") {
  for(U ordinal=1;ordinal<=4;++ordinal)l.op(F04_ABSENCE,l.post(19,ordinal).person,0,0,7*day,F04_SICK);
  for(U ordinal=1;ordinal<=28;++ordinal)l.op(F04_ABSENCE,l.post(20,ordinal).person,0,0,7*day,F04_SICK);
  l.plan(7,false);U gaps=0;for(auto g:l.gaps())if(g.station==F04_ST_SENSORS)++gaps;
  std::cerr<<"SENSOR GAPS="<<gaps<<"\n";check(gaps==21,"all 21 impossible sensor services persisted");check(!l.coverage(0,7*day)[2].covered,"no nominal availability fiction");audit(l,7,false);
 }
 else if(name=="partial") {
  Sovereign small(25);small.plan();check(small.org().positions==700 && small.org().assigned==25 && !small.gaps().empty(),"real persistent vacancies");
  check(small.stats().crew==25,"planner never generates people");
 }
 else if(name=="rest" || name=="fatigue") {
  U p=l.post(20).person;l.op(F04_REST,p,0,0,2*day);
  l.plan(7,false);for(auto d:l.duties())check(d.person!=p || d.start>=2*day,"protected rest respected");audit(l,7);
  auto first=l.duties().front();l.op(F04_DUTY,first.person,first.slot,first.end,first.end+28800,0,F04_OVERLAP,l.actor());
 }
 else if(name=="medical") {
  l.plan();for(auto c:l.coverage(0,day))if(c.station==F04_ST_MEDICAL)check(c.covered && c.person!=0,"present qualified medical response");
  l.advance(57600);check(l.org().urgent_response==1,"night medical response");
 }
 else if(name=="lifecycle") {
  l.plan();auto d=l.duties().front();U actor=l.actor();
  l.op(F04_DEPART,d.person,0,0,0,0,F04_OK,actor);check(l.org().vacant==1 && l.stats().crew==699,"departure real vacancy");
  l.op(F04_EMBARK,d.person,0,0,0,1,F04_OK,l.actor());check(l.stats().crew==700 && l.org().vacant==1,"same identity returns without automatic post");
  l.op(F04_ASSIGN,d.slot,d.person,0,0,0,F04_OK,l.actor());check(l.org().vacant==0,"explicit return to post");
 }
 else if(name=="mid_absence") {
  l.plan();auto c=l.coverage(0,28800);l.op(F04_ABSENCE,c[2].person,0,100,200,F04_SICK,F04_OK,l.actor());
  auto after=l.coverage(0,28800)[2];check(!after.covered && after.first_gap==100,"interior absence found, not just endpoints");
 }
 else if(name=="migration" || name=="roundtrip") {
  auto old=l.save();auto decoded=corerpg::CampaignPersistence::deserialize(old);check(decoded.snapshot.has_value(),"old schema3");
  l.plan(7,false,0,true);auto before=l.save();check(before!=old,"explicit migration");l.advance(7*day-1);auto future=l.save();
  Sovereign other;other.load(before);check(other.save()==before,"schema4 exact roundtrip");for(U tick=28800;tick<7*day;tick+=28800)other.advance(tick);other.advance(7*day-1);check(other.save()==future,"deterministic clock continuation");
  other.load(old);check(other.save()==old && other.duties().empty(),"schema3 still byte-identical");other.plan();
 }
 else if(name=="corrupt") {
  l.plan();const auto before=l.save();auto bad=before;bad.back()^=128;check(f04_load(l.s,bad.data(),bad.size())==F04_SAVE,"checksum corruption");
  auto data=corerpg::CampaignPersistence::deserialize(before);check(data.snapshot.has_value(),"decode");
  const U first_duty=l.duties().front().id;bool changed=false;for(auto& r:data.snapshot->campaign.relations)if(r.source.value()==first_duty && (r.kind.value()>>48)==0xF000+41) {r.kind=corerpg::RelationKind{(U(0xF000+41)<<48)|2};changed=true;break;}
  check(changed,"ordinary field tamper");std::sort(data.snapshot->campaign.relations.begin(),data.snapshot->campaign.relations.end());
  auto bytes=corerpg::CampaignPersistence::serialize(*data.snapshot);check(bytes.status==corerpg::CampaignArchiveStatus::success,"valid Core corrupt domain");
  check(f04_load(l.s,bytes.bytes.data(),bytes.bytes.size())==F04_SAVE && l.save()==before,"atomic domain rejection");
 }
 else if(name=="transfer") {
  l.plan();const auto old=l.post(23,1),destination=l.post(23,2);const auto old_person=l.person(old.person);
  l.op(F04_ASSIGN,destination.id,0,0,0,0,F04_OK,l.actor());
  l.op(F04_TRANSFER,destination.id,old.person,0,0,0,F04_OK,l.actor());
  check(l.post(23,1).person==0 && l.post(23,2).person==old.person && l.person(old.person).department==old_person.department,"explicit permanent move");
  for(auto d:l.duties())if(d.person==old.person)check(d.stopped_at==d.start,"future duties explicitly stopped");
  auto saved=l.save();l.load(saved);check(l.save()==saved,"transfer history persists");
 }
 else if(name=="cancel") {
  l.plan();auto c=l.coverage(0,28800);U duty=0;for(auto d:l.duties())if(d.person==c[2].person && d.start==0)duty=d.id;
  l.op(F04_CANCEL_DUTY,duty,0,0,0,0,F04_OK,l.actor());check(!l.coverage(0,28800)[2].covered,"cancel exposes service gap");
  U p=c[2].person;for(auto d:l.duties())if(d.id==duty)check(d.stopped_at==0 && d.cause!=0,"cancelled history retained");
  check(l.person(p).on_duty==0 && l.post(20,1).person!=0,"no permanent removal");
 }
 else if(name=="debt") {
  U p=l.post(20,1).person;U rest=l.op(F04_REST,p,0,0,day).record;
  l.op(F04_RECALL,rest,0,0,0,43200,F04_OK,l.actor());l.plan(7,false);
  for(auto d:l.duties())check(d.person!=p,"outstanding emergency debt prevents ordinary scheduling");
  auto saved=l.save();l.load(saved);check(l.save()==saved,"debt persists without magical recovery");
 }
 else if(name=="expiry") {
  l.plan();auto c=l.coverage(0,28800);U p=c[2].person;
  l.op(F04_CREDENTIAL,p,l.credentials(p),0,100,0,F04_OK,l.actor());
  auto gap=l.coverage(0,28800)[2];check(!gap.covered && gap.first_gap==100,"qualification expiry detected inside window");
  l.advance(100);check(!l.person(p).on_duty,"expired operator off duty");
 }
 else if(name=="invalid") {
  auto before=l.save();l.op(F04_PLAN_WATCHES,0,0,0,29*day,F04_ROTATING,F04_ARGUMENT);check(l.duties().empty(),"invalid plan atomic");
  l.plan();l.op(F04_POLICY,0,0,0,0,4,F04_REVIEW,l.actor());
  l.op(F04_PLAN_ALPHA,0,0,28800,57600,0,F04_REVIEW,l.actor()); // Legacy Alpha must not mix with SCHEMA 4
  l.op(F04_PLAN_WATCHES,0,0,0,day,F04_REFERENCE,F04_OVERLAP,l.actor());
  l.op(F04_PLAN_WATCHES,0,0,day,2*day,F04_REFERENCE,F04_DENIED,l.post(37).person);
  check(l.stats().crew==700,"no unauthorized state change");
 }
 else if(name=="buffers") {
  l.plan();U n=0,total=0;F04DutyView out{};check(f04_duties_page(l.s,l.observer,480,&out,1,&n,&total)==F04_OK && n==0 && total==480,"last page");
  check(f04_duties_page(l.s,l.observer,481,&out,1,&n,&total)==F04_ARGUMENT,"bad offset");
  check(f04_service_coverage(l.s,l.observer,0,day,nullptr,0,&n)==F04_CAPACITY && n==8,"coverage count");
  auto old=l.observer;auto b=l.save();l.load(b);check(f04_duties_page(l.s,old,0,&out,1,&n,&total)==F04_DENIED,"stale handles");
 }
 else if(name=="process_save") {l.plan(14,false,0,true);write(file,l.save());l.advance(14*day-1);write(file+".future",l.save());}
 else if(name=="process_load") {l.load(read(file));l.advance(14*day-1);check(l.save()==read(file+".future"),"cross-process deterministic roster");}
 else if(name=="benchmark") {
  using clock=std::chrono::steady_clock;auto t=clock::now();Sovereign other;auto t1=clock::now();
  F04Person manifest[700]{};U n=0;check(f04_manifest(other.s,other.observer,manifest,700,&n)==F04_OK,"manifest benchmark");auto t2=clock::now();
  other.plan(28,false,0,true);auto t3=clock::now();other.coverage(0,28*day);auto t4=clock::now();auto saved=other.save();auto t5=clock::now();other.load(saved);auto t6=clock::now();other.advance(28*day-1);auto t7=clock::now();
  auto ms=[](auto a,auto b){return std::chrono::duration<double,std::milli>(b-a).count();};
  std::cout<<"PERF create700_ms="<<ms(t,t1)<<" manifest_ms="<<ms(t1,t2)<<" plan28_ms="<<ms(t2,t3)<<" coverage28_ms="<<ms(t3,t4)<<" save_ms="<<ms(t4,t5)<<" load_ms="<<ms(t5,t6)<<" advance28_ms="<<ms(t6,t7)<<" bytes="<<saved.size()<<"\n";
 }
 else throw std::runtime_error("unknown sovereign case");
}
int main(int argc,char** argv){try{check(argc>=2,"case");run(argv[1],argc>2?argv[2]:"");std::cout<<argv[1]<<": PASS\n";return 0;}catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
