// Baseline diagnostics, NOT an implementation/acceptance test of archival storage.
#include "organization_lab.h"
#include <chrono>
#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#include <psapi.h>
#endif

constexpr U day=86400;
const char* classes[]={"miranda","intrepid","sovereign","odyssey","valhalla"};
const U crews[]={130,160,700,1600,1800};
using Clock=std::chrono::steady_clock;
double ms(Clock::time_point a,Clock::time_point b){return std::chrono::duration<double,std::milli>(b-a).count();}
struct Audit:Lab {
 U profile;
 explicit Audit(U id):Lab(true,crews[id-1],classes[id-1],true,uint32_t(id),id==5?400:0),profile(id){}
 auto decoded(){auto d=corerpg::CampaignPersistence::deserialize(save());check(d.snapshot.has_value(),"decode");return *d.snapshot;}
 std::vector<F04DutyView> duties(){U n=0,t=0;check(f04_duties_page(s,observer,0,nullptr,0,&n,&t)==F04_OK,"duty count");std::vector<F04DutyView> out(t);check(f04_duties_page(s,observer,0,out.data(),t,&n,&t)==F04_OK && n==t,"duties");return out;}
 uint32_t plan(U start,U days,bool seed){
  F04Request r{{observer.scope,stats().commander},stats().revision,F04_PLAN_WATCHES,F04_ROTATING,0,seed?1U:0U,start*day,(start+days)*day,40401};
  F04Result result{};auto code=f04_execute(s,&r,&result);check(code==result.code,"returned operation code");return code;
 }
};
void counts(const corerpg::CampaignArchiveSnapshot& snap){
 std::map<std::string,U> types;for(const auto& d:snap.campaign.definitions)++types[d.definition_id];
 std::cout<<"\"types\":{";bool comma=false;for(auto [name,n]:types){if(comma)std::cout<<',';comma=true;std::cout<<'"'<<name<<"\":"<<n;}std::cout<<"},\"relations\":"<<snap.campaign.relations.size();
}
void memory(){
#ifdef _WIN32
 PROCESS_MEMORY_COUNTERS pm{};pm.cb=sizeof(pm);check(GetProcessMemoryInfo(GetCurrentProcess(),&pm,sizeof(pm))!=0,"memory");
 std::cout<<",\"working_set_bytes\":"<<pm.WorkingSetSize<<",\"process_peak_working_set_bytes\":"<<pm.PeakWorkingSetSize;
#endif
}
void identities(const corerpg::CampaignArchiveSnapshot& before,const corerpg::CampaignArchiveSnapshot& after){
 // All static identity and census records remain byte-for-byte structurally equal.
 std::set<U> ids;
 for(const auto& d:before.campaign.definitions)if(d.definition_id=="trek.f04:person" || d.definition_id=="trek.f04:slot" || d.definition_id=="trek.f04:auxiliary_defiant" || d.definition_id=="trek.f04:section" || d.definition_id=="trek.f04:department")ids.insert(d.entity.value());
 std::vector<corerpg::EntityRelation> a,b;for(auto r:before.campaign.relations)if(ids.contains(r.source.value()))a.push_back(r);for(auto r:after.campaign.relations)if(ids.contains(r.source.value()))b.push_back(r);
 check(a==b,"identities, qualifications, assignments, service groups and census unchanged");
 check(before.campaign.population_memberships==after.campaign.population_memberships,"population continuity");
 for(const auto& d:before.campaign.definitions)if(ids.contains(d.entity.value()))check(std::find(after.campaign.definitions.begin(),after.campaign.definitions.end(),d)!=after.campaign.definitions.end(),"stable definitions");
}
void atomic_capacity(const std::vector<uint8_t>& before,const std::vector<uint8_t>& after){
 auto a=corerpg::CampaignPersistence::deserialize(before),b=corerpg::CampaignPersistence::deserialize(after);check(a.snapshot && b.snapshot,"capacity decode");
 const U last=a.snapshot->campaign.last_entity_id;auto& c=b.snapshot->campaign;
 check(c.last_entity_id==last+1 && c.definitions.back().definition_id=="trek.f04:event","one rejection event only");
 bool code=false;for(auto r:c.relations)if(r.source.value()==last+1 && (r.kind.value()>>48)==0xF000+16)code=(r.kind.value()&forever)==F04_CAPACITY;
 check(code,"capacity reason persisted");
 std::erase_if(c.definitions,[&](const auto& d){return d.entity.value()>last;});std::erase_if(c.relations,[&](auto r){return r.source.value()>last;});
 c.last_entity_id=last;c.revision=a.snapshot->campaign.revision;
 check(corerpg::CampaignPersistence::serialize(*b.snapshot).bytes==before,"whole state, RNG, clock and history unchanged except rejection audit");
}
void audit_work(Audit& l){
 std::map<U,std::vector<F04DutyView>> people;for(auto d:l.duties())if(d.start<d.stopped_at)people[d.person].push_back(d);
 for(auto& [p,v]:people){(void)p;std::sort(v.begin(),v.end(),[](auto a,auto b){return a.start<b.start;});for(size_t i=0,left=0;i<v.size();++i){while(v[i].start-v[left].start>=7*day)++left;check(i-left+1<=5,"rolling seven across blocks");if(i)check(v[i].start/day!=v[i-1].start/day && v[i].start>=v[i-1].stopped_at+43200,"daily duty and twelve-hour rest across blocks");}}
}
void negative_loads(Audit& l){
 const auto good=l.save();auto reject=[&](const auto& bytes){check(f04_load(l.s,bytes.data(),bytes.size())==F04_SAVE,"invalid save rejected");check(l.save()==good,"failed load leaves entire valid campaign intact");check(l.person(3).id==3,"old observer survives failed load");};
 auto bad=good;bad.pop_back();reject(bad);bad=good;bad[0]^=1;reject(bad);bad=good;bad[bad.size()/2]^=1;reject(bad);bad=good;bad[8]=99;reject(bad);
 // Structurally valid Core envelope with semantically invalid F04 interval.
 auto snap=l.decoded();bool changed=false;for(auto& r:snap.campaign.relations)if((r.kind.value()>>48)==0xF000+2 && r.target==r.source){r.kind=corerpg::RelationKind{U(0xF000+2)<<48};changed=true;break;}
 check(changed,"interval mutation");std::sort(snap.campaign.relations.begin(),snap.campaign.relations.end());auto encoded=corerpg::CampaignPersistence::serialize(snap);check(encoded.status==corerpg::CampaignArchiveStatus::success,"Core-valid domain corruption");reject(encoded.bytes);
}
void measure(U profile,U days){
 Audit l(profile);const auto initial=l.stats();auto t0=Clock::now();check(l.plan(0,days,days!=1)==F04_OK,"measure plan");auto t1=Clock::now();const auto state=l.stats();auto t2=Clock::now();auto bytes=l.save();auto t3=Clock::now();l.load(bytes);auto t4=Clock::now();check(l.save()==bytes,"lossless roundtrip");auto snap=l.decoded();
 std::cout<<"{\"kind\":\"measurement\",\"profile\":"<<profile<<",\"days\":"<<days<<",\"initial_entities\":"<<initial.entities<<",\"entities\":"<<state.entities<<",\"added\":"<<state.entities-initial.entities<<",\"bytes\":"<<bytes.size()<<",\"plan_ms\":"<<ms(t0,t1)<<",\"save_two_calls_ms\":"<<ms(t2,t3)<<",\"load_ms\":"<<ms(t3,t4)<<',';counts(snap);memory();std::cout<<"}\n";
}
void campaign(U profile,U target,const std::string& path){
 Audit l(profile);auto original=l.decoded();U completed=0,code=F04_OK;auto started=Clock::now();
 while(completed<target){
  const U days=std::min(U(28),target-completed);auto before=l.save();write(path,before);
  {std::ofstream f(path+".args");f<<profile<<' '<<completed<<' '<<days<<' '<<(completed==0)<<'\n';check(bool(f),"checkpoint metadata");}
  auto t0=Clock::now();code=l.plan(completed,days,completed==0);auto t1=Clock::now();
  if(code==F04_CAPACITY){atomic_capacity(before,l.save());write(path+".future",l.save());break;}
  check(code==F04_OK,"campaign plan");auto planned=l.save();l.advance((completed+days)*day-1);auto uninterrupted=l.save();
  l.load(planned);l.advance((completed+days)*day-1);check(l.save()==uninterrupted,"uninterrupted and save/load future equal");
  completed+=days;identities(original,l.decoded());audit_work(l);write(path+".future",uninterrupted);
  std::cout<<"{\"kind\":\"block\",\"profile\":"<<profile<<",\"completed_days\":"<<completed<<",\"entities\":"<<l.stats().entities<<",\"bytes\":"<<uninterrupted.size()<<",\"plan_ms\":"<<ms(t0,t1)<<"}\n"<<std::flush;
 }
 negative_loads(l);const auto state=l.stats();auto snap=l.decoded();
 check(completed==target || code==F04_CAPACITY,"explicit baseline outcome");
 std::cout<<"{\"kind\":\"baseline_outcome\",\"profile\":"<<profile<<",\"requested_days\":"<<target<<",\"completed_days\":"<<completed<<",\"code\":"<<code<<",\"acceptance_achieved\":false,\"entities\":"<<state.entities<<",\"bytes\":"<<l.save().size()<<",\"elapsed_ms\":"<<ms(started,Clock::now())<<',';counts(snap);memory();std::cout<<"}\n";
}
void resume(const std::string& path){
 U profile=0,start=0,days=0,seed=0;std::ifstream f(path+".args");check(bool(f>>profile>>start>>days>>seed),"checkpoint args");check(profile>=1 && profile<=5,"profile");Audit l(profile);l.load(read(path));
 const auto before=l.save();const auto code=l.plan(start,days,seed!=0);check(code==F04_OK || code==F04_CAPACITY,"resume result");
 if(code==F04_OK)l.advance((start+days)*day-1);else atomic_capacity(before,l.save());
 check(l.save()==read(path+".future"),"different process produces identical authoritative future");audit_work(l);std::cout<<"{\"kind\":\"process_resume\",\"profile\":"<<profile<<",\"code\":"<<code<<",\"equal_future\":true}\n";
}
void core_boundary(){
 corerpg::WorldState w;corerpg::RandomStreams rng(404);corerpg::Timeline time;
 for(U i=1;i<=3;++i)check(w.create_entity().value()==i,"dense identity");
 corerpg::EntityRelation r{corerpg::EntityId{2},corerpg::RelationKind{1},corerpg::EntityId{1}};check(w.add_relation(r)==corerpg::RelationChange::applied,"relation");check(w.remove_relation(r)==corerpg::RelationChange::applied,"remove relation");
 check(w.contains(corerpg::EntityId{2}) && w.entity_count()==3,"removing payload does not reclaim identity");
 auto snapshot=corerpg::CampaignPersistence::capture(w,rng,time);snapshot.campaign.last_entity_id=2;
 check(corerpg::CampaignPersistence::restore(snapshot,w,rng,time)==corerpg::CampaignArchiveStatus::success,"whole checkpoint rollback allowed");
 check(w.create_entity().value()==3,"truncating high-water mark reissues an old identity");
 std::cout<<"{\"kind\":\"core_boundary\",\"payload_removal_reclaims_identity\":false,\"checkpoint_truncation_reuses_identity\":true}\n";
}
int main(int argc,char** argv){try{
 check(argc>=2,"mode required");std::string mode=argv[1];
 if(mode=="core_boundary")core_boundary();else if(mode=="resume"){check(argc==3,"resume path");resume(argv[2]);}
 else{check(argc>=4,"profile and days");U profile=std::stoull(argv[2]),days=std::stoull(argv[3]);check(profile>=1 && profile<=5 && days>0,"arguments");
 if(mode=="measure")measure(profile,days);else if(mode=="campaign"){check(argc==5,"checkpoint path");campaign(profile,days,argv[4]);}else check(false,"mode");}
 return 0;
 }catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<'\n';return 1;}}
