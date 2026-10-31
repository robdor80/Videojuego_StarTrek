#include "organization_lab.h"
#include <tuple>
constexpr U day=86400;
struct Small:Lab {
 U profile,crew;
 Small(U id,U count=0):Lab(true,count?count:(id==1?130:160),id==1?"miranda":"intrepid",true,uint32_t(id)),profile(id),crew(count?count:(id==1?130:160)){}
 U actor(){return stats().commander;}
 void plan(U days=1,bool seed=true,U start=0,bool reference=false){op(F04_PLAN_WATCHES,0,seed&&!reference?1:0,start,start+days*day,reference?F04_REFERENCE:F04_ROTATING,F04_OK,actor());}
 std::vector<F04DutyView> duties(){U n=0,t=0;f04_duties_page(s,observer,0,nullptr,0,&n,&t);std::vector<F04DutyView> a(t);check(f04_duties_page(s,observer,0,a.data(),t,&n,&t)==F04_OK && n==t,"duties");return a;}
 std::vector<F04RosterGap> gaps(){U n=0,t=0;f04_roster_gaps_page(s,observer,0,nullptr,0,&n,&t);std::vector<F04RosterGap> a(t);check(f04_roster_gaps_page(s,observer,0,a.data(),t,&n,&t)==F04_OK && n==t,"gaps");return a;}
 std::vector<F04ServiceCoverage> coverage(U a,U b){U n=0;std::vector<F04ServiceCoverage> c(8);check(f04_service_coverage(s,observer,a,b,c.data(),8,&n)==F04_OK && n==8,"eight services");return c;}
 U sensor(){return profile==1?12:13;}
 U security(){return profile==1?21:23;}
 U medicine(){return profile==1?29:31;}
};
U schema(Lab& l){auto d=corerpg::CampaignPersistence::deserialize(l.save());check(d.snapshot.has_value(),"decode");for(auto r:d.snapshot->campaign.relations)if(r.source.value()==1 && (r.kind.value()>>48)==0xF000+19)return r.kind.value()&((1ULL<<48)-1);throw std::runtime_error("schema field");}
void audit(Small& l,U days,bool complete=true){
 std::map<U,std::vector<F04DutyView>> work;std::map<U,F04Position> slots;
 for(auto p:l.positions())slots[p.id]=p;
 for(auto d:l.duties())if(d.start<d.stopped_at){check(d.ordinary && d.end-d.start<=28800,"8h ordinary");work[d.person].push_back(d);check((l.credentials(d.person)&slots[d.slot].qualification_mask)==slots[d.slot].qualification_mask,"no fabricated skills");}
 for(auto& [p,v]:work){std::sort(v.begin(),v.end(),[](auto a,auto b){return a.start<b.start;});for(size_t i=0,left=0;i<v.size();++i){while(v[i].start-v[left].start>=7*day)++left;check(i-left+1<=5,"rolling7");if(i)check(v[i].start/day!=v[i-1].start/day && v[i].start>=v[i-1].stopped_at+43200,"one daily duty and 12h rest");}}
 if(complete)for(U w=0;w<days*3;++w)for(auto c:l.coverage(w*28800,(w+1)*28800))check(c.covered && c.person && c.first_gap==c.end,"whole critical window");
 check(l.stats().crew==l.crew,"no generated crew");
}
void same_positions(Small& l,const std::vector<F04Position>& old){auto now=l.positions();check(now.size()==old.size(),"post count");for(size_t i=0;i<old.size();++i)check(now[i].person==old[i].person && now[i].id==old[i].id && now[i].stable_id==old[i].stable_id && now[i].department==old[i].department && now[i].responsibility==old[i].responsibility,"original identities destinations appointments");}
void reference(Small& l){
 l.plan(1,false,0,true);std::map<U,std::array<U,3>> counts;std::map<U,F04Position> slots;for(auto p:l.positions())slots[p.id]=p;
 for(auto d:l.duties())++counts[slots[d.slot].section][(d.start/28800+2)%3];
 std::ifstream f(std::string(F04_FIXTURE_DIR)+(l.profile==1?"/sutherland_watches.tsv":"/intrepid_watches.tsv"));check(bool(f),"oracle");U s,t,a,b,g,o;
 while(f>>s>>t>>a>>b>>g>>o)check(counts[s]==std::array<U,3>{a,b,g} && t==a+b+g+o,"every section exact");
 check(l.duties().size()==(l.profile==1?84:103) && l.gaps().empty(),"exact day");audit(l,1);
 l.advance(28800);auto org=l.org();check(org.on_duty==(l.profile==1?53:64) && org.alpha_deficit==0 && org.continuous_required==8 && org.continuous_covered==8,"approved Alpha preserved");
 l.advance(57600);check(l.org().on_duty==(l.profile==1?18:23) && l.actor()!=3,"Beta");l.advance(day);check(l.org().on_duty==0 && l.actor()==0,"finite horizon");
}
void run(U profile,const std::string& name,const std::string& file){
 Small l(profile);
 if(name=="reference")reference(l);
 else if(name=="7" || name=="14" || name=="28" || name=="unseeded"){
  U days=name=="unseeded"?28:std::stoull(name);auto ids=l.positions();l.plan(days,name!="unseeded");audit(l,days);same_positions(l,ids);
  for(U p:{U(3),l.post(2).person}){U shifts=0;for(auto d:l.duties())shifts+=d.person==p;check(shifts<=5*(days/7) && shifts<days,"captain and first rest");}
  l.advance(days*day-1);check(l.actor() && l.person(l.actor()).on_duty,"valid final command");
 }
 else if(name=="authority"){
  l.plan();l.advance(28800);auto first=l.post(2).person,watch=l.post(3).person;
  l.op(F04_BRIDGE,0,0,0,0,2,F04_DENIED,l.post(l.security()).person);
  l.op(F04_BRIDGE,0,0,0,0,2,F04_DENIED,l.post(l.medicine()).person);
  l.op(F04_ABSENCE,3,0,28800,57600,F04_LEAVE);check(l.actor()==first,"first succeeds");
  l.op(F04_ABSENCE,first,0,28800,57600,F04_SICK,F04_OK,l.actor());check(l.actor()==watch,"appointed watch succeeds");
 }
 else if(name=="absence" || name=="cancel" || name=="mid_cancel" || name=="revoked_cancel" || name=="cover"){
  auto ids=l.positions();l.plan(1,false,0,true);auto c=l.coverage(0,28800)[2];U duty=0,sensor_slot=0;for(auto d:l.duties())if(d.person==c.person && d.start==0){duty=d.id;sensor_slot=d.slot;}check(duty,"sensor duty");
  U start=0;
  if(name=="revoked_cancel"){
   auto decoded=corerpg::CampaignPersistence::deserialize(l.save());U function=0;
   for(auto r:decoded.snapshot->campaign.relations)if(r.kind.value()==2 && r.target.value()==c.person){
    U entity=r.source.value();bool sensor=false;for(auto e:decoded.snapshot->campaign.relations)if(e.source.value()==entity && (e.kind.value()>>48)==0xF000+35 && (e.kind.value()&((1ULL<<48)-1))==F04_ST_SENSORS)sensor=true;
    bool attached=false;for(auto e:decoded.snapshot->campaign.relations)attached|=e.source.value()==entity && e.kind.value()==3 && e.target.value()==sensor_slot;
    if(sensor && attached){function=entity;break;}
   }
   check(function,"sensor function");l.op(F04_REVOKE,function,0,0,0,0,F04_OK,l.actor());
  }
  if(name=="mid_cancel"){start=100;l.advance(start);}
  if(name=="cancel" || name=="mid_cancel" || name=="revoked_cancel")l.op(F04_CANCEL_DUTY,duty,0,0,0,0,F04_OK,l.actor());else l.op(F04_ABSENCE,c.person,0,0,28800,F04_SICK,F04_OK,l.actor());
  check(!l.coverage(0,28800)[2].covered,"actual incident gap");bool recorded=false;for(auto g:l.gaps())recorded|=g.station==F04_ST_SENSORS;check(recorded,"persistent incident");
  auto bytes=l.save();l.load(bytes);check(l.save()==bytes && !l.coverage(0,28800)[2].covered,"incident survives load");
  F04ReliefCandidate cs[160]{};U n=0,total=0;check(f04_relief_candidates_page(l.s,l.observer,duty,start,28800,0,cs,160,&n,&total)==F04_OK && n,"real relief");
  l.op(F04_COVER_DUTY,duty,cs[0].person,start,28800,0,F04_OK,l.actor());check(bool(l.coverage(start,28800)[2].covered)==(name!="revoked_cancel"),"restore cancelled service without resurrecting explicit revocation");same_positions(l,ids);if(name!="revoked_cancel")audit(l,1);
  bytes=l.save();l.load(bytes);check(l.save()==bytes && bool(l.coverage(start,28800)[2].covered)==(name!="revoked_cancel") && !l.gaps().empty(),"resolved history remains");
 }
 else if(name=="deficit"){
  for(auto p:l.positions())if((p.stations&F04_ST_SENSORS) && (l.credentials(p.person)&(1ULL<<F04_SENSORS)))l.op(F04_ABSENCE,p.person,0,0,7*day,F04_SICK);
  l.plan(7,false);U missing=0;for(auto g:l.gaps())missing+=g.station==F04_ST_SENSORS;check(missing==21,"all impossible sensor windows exposed");audit(l,7,false);
 }
 else if(name=="command_rest" || name=="command_shortage"){
  if(name=="command_shortage")for(U i=1;i<=(profile==1?1:2);++i)l.op(F04_ABSENCE,l.post(3,i).person,0,0,7*day,F04_SICK);
  else for(U i=1;i<=(profile==1?3:4);++i)l.op(F04_REST,l.post(3,i).person,0,0,7*day);
  l.plan(7,false);U gaps=0;for(auto g:l.gaps())gaps+=g.station==F04_ST_COMMAND;
  if(name=="command_rest"){
   check(gaps>=11,"two command crew cannot cover 21 with capacity10");
   for(auto d:l.duties())check(d.person!=l.post(3).person && (d.person<l.post(3).person || d.person>=l.post(4).person),"critical fallback respects protected command rest");
  }else check(gaps>=1,"four qualified command crew capacity20 below21");
  audit(l,7,false);
 }
 else if(name=="medical"){
  l.plan(7);for(U i=0;i<21;++i)for(auto c:l.coverage(i*28800,(i+1)*28800))if(c.station==F04_ST_MEDICAL){auto mask=l.credentials(c.person);check(c.covered && (mask&((1ULL<<F04_Q_CLINICAL)|(1ULL<<F04_Q_NURSING))),"clinical or nursing present; no oncall fiction");}
 }
 else if(name=="rest" || name=="leave" || name=="debt"){
  U p=l.post(l.sensor(),5).person;
  if(name=="debt"){U a=l.op(F04_REST,p,0,0,day).record;l.op(F04_RECALL,a,0,0,0,43200);}else l.op(name=="leave"?F04_ABSENCE:F04_REST,p,0,0,2*day,name=="leave"?F04_LEAVE:0);
  l.plan(7,false);for(auto d:l.duties())check(d.person!=p || (name!="debt" && d.start>=2*day),"protected interval/debt");audit(l,7);
 }
 else if(name=="partial"){
  Small shortfall(profile,25);shortfall.plan();check(shortfall.org().positions==(profile==1?130:160) && shortfall.org().assigned==25 && shortfall.stats().crew==25 && !shortfall.gaps().empty(),"vacancies remain real");audit(shortfall,1,false);
 }
 else if(name=="expiry"){
  l.plan();U p=l.coverage(0,28800)[2].person;l.op(F04_CREDENTIAL,p,l.credentials(p),0,100,0,F04_OK,l.actor());auto c=l.coverage(0,28800)[2];check(!c.covered && c.first_gap==100,"interior expiry");auto b=l.save();l.load(b);check(l.save()==b,"expiry persists");
 }
 else if(name=="migration" || name=="roundtrip"){
  check(schema(l)==3,"starts schema3");auto old=l.save();auto ids=l.positions();l.plan(28);check(schema(l)==4,"explicit schema4");same_positions(l,ids);auto before=l.save();l.advance(28*day-1);auto future=l.save();
  l.load(before);check(l.save()==before,"exact archive");for(U tick=28800;tick<28*day;tick+=28800)l.advance(tick);l.advance(28*day-1);check(l.save()==future,"same future with stepped clock");
  l.load(old);check(l.save()==old && schema(l)==3 && l.duties().empty(),"schema3 no automatic rewrite");l.plan();same_positions(l,ids);
 }
 else if(name=="legacy_alpha"){
  l.alpha();auto old=l.save();auto ids=l.positions();l.plan(7,false,day);for(auto c:l.coverage(day,8*day))check(c.covered,"critical coverage after old Alpha migration");check(schema(l)==4,"schema3 Alpha then new watches");same_positions(l,ids);auto b=l.save();l.load(b);check(l.save()==b,"mixed historical Alpha persists");l.advance(8*day-1);check(l.actor(),"continued campaign");l.load(old);check(l.save()==old,"old Alpha still exact");
 }
 else if(name=="continuation"){
  l.plan(7);auto b=l.save();Small other(profile);other.load(b);l.plan(7,false,7*day);other.plan(7,false,7*day);check(l.save()==other.save(),"new plans after restore deterministic");audit(l,14);
 }
 else if(name=="corrupt"){
  l.plan();auto before=l.save();auto data=corerpg::CampaignPersistence::deserialize(before);check(data.snapshot.has_value(),"decode");U d=l.duties().front().id;bool changed=false;
  for(auto& r:data.snapshot->campaign.relations)if(r.source.value()==d && (r.kind.value()>>48)==0xF000+41){r.kind=corerpg::RelationKind{(U(0xF000+41)<<48)|2};changed=true;break;}check(changed,"tamper");std::sort(data.snapshot->campaign.relations.begin(),data.snapshot->campaign.relations.end());auto bad=corerpg::CampaignPersistence::serialize(*data.snapshot);check(f04_load(l.s,bad.bytes.data(),bad.bytes.size())==F04_SAVE && l.save()==before,"atomic semantic rejection");
 }
 else if(name=="invalid"){
  l.op(F04_PLAN_WATCHES,0,0,0,29*day,F04_ROTATING,F04_ARGUMENT);check(l.duties().empty(),"invalid atomic");l.plan();l.op(F04_PLAN_WATCHES,0,0,0,day,F04_REFERENCE,F04_OVERLAP,l.actor());l.op(F04_PLAN_WATCHES,0,0,day,2*day,F04_REFERENCE,F04_DENIED,l.post(l.security()).person);l.op(F04_PLAN_ALPHA,0,1,28800,57600,0,F04_REVIEW,l.actor());
 }
 else if(name=="process_save"){l.plan(14);write(file,l.save());l.advance(14*day-1);write(file+".future",l.save());}
 else if(name=="process_load"){l.load(read(file));l.advance(14*day-1);check(l.save()==read(file+".future"),"cross-process deterministic");}
 else throw std::runtime_error("case");
}
int main(int argc,char** argv){try{check(argc>=3,"args");run(std::stoull(argv[1]),argv[2],argc>3?argv[3]:"");std::cout<<argv[1]<<" "<<argv[2]<<": PASS\n";return 0;}catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}}
