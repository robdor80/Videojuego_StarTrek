#include "organization_lab.h"
#include <corerpg/history.hpp>
#include <chrono>
#include <filesystem>
#include <sstream>
#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#include <psapi.h>
#endif
extern "C" F04_API uint32_t f04_history_test_delta(F04Session*,U,uint8_t*,U,U*);
extern "C" F04_API uint32_t f04_history_test_validate_full(F04Session*);
constexpr U day=86400;
const char* classes[]={"miranda","intrepid","sovereign","odyssey","valhalla"};
const U crews[]={130,160,700,1600,1800};
using Clock=std::chrono::steady_clock;
std::string digest(const std::vector<uint8_t>& bytes){const char* d="0123456789abcdef";std::string out;for(auto b:corerpg::HistoryPersistence::hash(bytes)){out+=d[b>>4];out+=d[b&15];}return out;}
double elapsed(Clock::time_point start){return std::chrono::duration<double,std::milli>(Clock::now()-start).count();}
U field(const corerpg::CampaignSnapshot& s,U entity,U number){for(auto r:s.relations)if(r.source.value()==entity && (r.kind.value()>>48)==0xF000+number)return r.kind.value()&forever;return 0;}
U reference(const corerpg::CampaignSnapshot& s,U entity,U kind){for(auto r:s.relations)if(r.source.value()==entity && r.kind.value()==kind)return r.target.value();return 0;}
struct CampaignLab:Lab {
 U profile;std::string static_hash;
 explicit CampaignLab(U p):Lab(true,crews[p-1],classes[p-1],true,uint32_t(p),p==5?400:0),profile(p){static_hash=digest(delta(UINT64_MAX));}
 std::vector<uint8_t> delta(U after){U n=0;check(f04_history_test_delta(s,after,nullptr,0,&n)==F04_CAPACITY,"delta size");std::vector<uint8_t> b(n);check(f04_history_test_delta(s,after,b.data(),n,&n)==F04_OK,"delta records");return b;}
 auto history(){F04HistoryStats out{};check(f04_history_stats(s,&out)==F04_OK,"history stats");return out;}
 void open(const std::string& path){check(f04_history_open(s,path.c_str())==F04_OK,"recover whole history generation");refresh();}
 F04Result execute(uint32_t op,U target,U aux,U start,U end,uint32_t value=0) {
  auto st=stats();check(st.commander!=0,"real commander before request");F04Request r{{observer.scope,st.commander},st.revision,op,value,target,aux,start,end,40401};F04Result result{};
  auto code=f04_execute(s,&r,&result);if(code!=F04_OK)std::cerr<<"operation "<<op<<" rejected "<<code<<'\n';check(code==F04_OK,"real campaign operation");return result;
 }
 void block(U completed,U days,U block_index) {
  const U start=completed*day,end=(completed+days)*day;
  U person=0;for(auto p:positions())if(p.person && !p.responsibility && p.department!=F04_COMMAND && p.person!=3){person=p.person;break;}
  check(person!=0,"real incident target");
  if(block_index%4==1){execute(F04_ABSENCE,person,0,start,start+std::min(U(2),days)*day,1);}
  if(block_index%4==2){execute(F04_REST,person,0,start,start+day);}
  const auto before=stats().entities;
  execute(F04_PLAN_WATCHES,0,completed==0?1:0,start,end,F04_ROTATING);
  // Exercise STOP and optional real relief in both the complete-history oracle
  // and consolidated campaign, choosing records only from this actual plan.
  if(block_index%4==3){auto bytes=delta(before);auto decoded=corerpg::CampaignPersistence::deserialize(bytes);check(decoded.snapshot.has_value(),"new plan decode");
   U duty=0,a=0,b=0;for(const auto& d:decoded.snapshot->campaign.definitions)if(d.definition_id=="trek.f04:activity" && field(decoded.snapshot->campaign,d.entity.value(),3)==F04_DUTY && reference(decoded.snapshot->campaign,d.entity.value(),2)==person){duty=d.entity.value();a=field(decoded.snapshot->campaign,duty,1);b=field(decoded.snapshot->campaign,duty,2);break;}
   if(duty){execute(F04_CANCEL_DUTY,duty,0,0,0);F04ReliefCandidate candidates[8]{};U n=0,total=0;
    check(f04_relief_candidates_page(s,observer,duty,a,b,0,candidates,8,&n,&total)==F04_OK,"real relief candidates");
    if(n)execute(F04_COVER_DUTY,duty,candidates[0].person,a,b);}
  }
  advance(end-1);check(digest(delta(UINT64_MAX))==static_hash,"no duplicate people, altered skills, static relations or census");
 }
};
void memory(){
#ifdef _WIN32
 PROCESS_MEMORY_COUNTERS p{};p.cb=sizeof(p);check(GetProcessMemoryInfo(GetCurrentProcess(),&p,sizeof(p))!=0,"working set");std::cout<<",\"working_set\":"<<p.WorkingSetSize<<",\"peak_working_set\":"<<p.PeakWorkingSetSize;
#endif
}
void original_query(CampaignLab& l,const corerpg::CampaignSnapshot& expected){
 auto st=l.history();F04HistoryFact facts[16]{};U n=0,verified=0;uint32_t more=0;check(f04_history_page(l.s,l.observer,st.generation,0,facts,16,&n,&more)==F04_OK,"historical page");check(n>0,"original historical facts exist");
 for(U i=0;i<n && verified<3;++i){std::vector<corerpg::EntityRelation> original;for(auto r:expected.relations)if(r.source.value()==facts[i].id)original.push_back(r);if(original.empty())continue;
  std::vector<F04HistoryRelation> actual(256);U written=0,total=0;check(f04_history_relations(l.s,l.observer,st.generation,facts[i].id,0,actual.data(),256,&written,&total)==F04_OK && written==total,"historical original relations");check(total==original.size(),"historical full relation count");
  for(size_t j=0;j<original.size();++j)check(actual[j].source==original[j].source.value() && actual[j].kind==original[j].kind.value() && actual[j].target==original[j].target.value(),"historical payload exactly equals original");++verified;}check(verified>0,"queried original plan facts");
}
void run(U profile,U target,const std::string& path) {
 CampaignLab l(profile);const auto started=Clock::now();U completed=0,block_index=0,maximum_resident=0,maximum_active_bytes=0;
 const bool oracle=
#ifdef F04_REFERENCE_ORACLE
 true;
#else
 false;
#endif
 std::fstream comparison(path+".oracle",oracle?std::ios::out:std::ios::in);check(bool(comparison),"differential oracle file");
 if(!oracle){const std::array<uint8_t,16> uuid{static_cast<uint8_t>(profile),1};check(f04_history_migrate(l.s,path.c_str(),uuid.data(),16)==F04_OK,"explicit migration");}
 std::optional<corerpg::CampaignSnapshot> first;
 while(completed<target){const U days=std::min(U(7),target-completed),before=l.stats().entities;auto block_started=Clock::now();l.block(completed,days,block_index);
  auto delta=l.delta(before);const auto hash=digest(delta);completed+=days;
  if(oracle)comparison<<completed<<' '<<l.stats().entities<<' '<<hash<<'\n';
  else{U expected_day=0,issued=0;std::string expected;check(bool(comparison>>expected_day>>issued>>expected),"expected full-history block");check(expected_day==completed && issued==l.stats().entities && expected==hash,"future assignments, events, original facts, RNG and time equal complete-history oracle");
   if(!first){auto d=corerpg::CampaignPersistence::deserialize(delta);check(d.snapshot.has_value(),"first block original facts");first=d.snapshot->campaign;}
   maximum_resident=std::max(maximum_resident,l.history().resident);U active_before=0;check(f04_history_export_active(l.s,nullptr,0,&active_before)==F04_CAPACITY,"pre-consolidation active size");maximum_active_bytes=std::max(maximum_active_bytes,active_before);
   const U now=l.stats().now;auto archive_started=Clock::now();if(now>=7*day)check(f04_history_consolidate(l.s,now-7*day,0)==F04_OK,"real consolidation");else check(f04_history_publish(l.s,0)==F04_OK,"initial publication");
   const auto archive_ms=elapsed(archive_started);auto hs=l.history();maximum_resident=std::max(maximum_resident,hs.resident);check(hs.resident<65536 && hs.issued==hs.resident+hs.archived,"fixed resident budget and exact issued identity accounting");
   U size=0;check(f04_history_export_active(l.s,nullptr,0,&size)==F04_CAPACITY,"active bytes bound");maximum_active_bytes=std::max(maximum_active_bytes,size);
   if(block_index%4==0){auto before_recovery=l.delta(0);auto recover_started=Clock::now();l.open(path);check(l.delta(0)==before_recovery,"recovery preserves full active checkpoint RNG clock and facts");std::cout<<"{\"recovery_ms\":"<<elapsed(recover_started)<<",\"completed\":"<<completed<<"}\n";}
   if(hs.archived){auto query_started=Clock::now();original_query(l,*first);std::cout<<"{\"query_ms\":"<<elapsed(query_started)<<",\"completed\":"<<completed<<"}\n";}
   std::cout<<"{\"kind\":\"block\",\"profile\":"<<profile<<",\"completed\":"<<completed<<",\"issued\":"<<hs.issued<<",\"resident\":"<<hs.resident<<",\"archived\":"<<hs.archived<<",\"segments\":"<<hs.segments<<",\"active_bytes\":"<<size<<",\"archive_ms\":"<<archive_ms<<",\"block_ms\":"<<elapsed(block_started)<<",\"oracle_equal\":true";memory();std::cout<<"}\n"<<std::flush;
  }++block_index;
 }
 check(f04_history_test_validate_full(l.s)==F04_OK,"complete unfiltered global schema at final requested horizon");
 const auto before=l.stats().entities;l.block(completed,7,block_index);const auto future=digest(l.delta(before));
 check(f04_history_test_validate_full(l.s)==F04_OK,"complete unfiltered global schema at final deterministic future");
 if(oracle)comparison<<completed+7<<' '<<l.stats().entities<<' '<<future<<'\n';
 else{U expected_day=0,issued=0;std::string expected;check(bool(comparison>>expected_day>>issued>>expected) && expected_day==completed+7 && issued==l.stats().entities && expected==future,"unpublished deterministic future");
  std::ofstream meta(path+".resume");meta<<profile<<' '<<completed<<' '<<block_index<<' '<<before<<' '<<future<<'\n';check(bool(meta),"process continuation metadata");
  std::cout<<"{\"kind\":\"acceptance\",\"profile\":"<<profile<<",\"days\":"<<target<<",\"completed\":"<<completed<<",\"maximum_resident\":"<<maximum_resident<<",\"maximum_active_bytes\":"<<maximum_active_bytes<<",\"elapsed_ms\":"<<elapsed(started)<<",\"real_watches\":true,\"all_blocks_equal_complete_history\":true";memory();std::cout<<"}\n";
 }
}
void resume(const std::string& path){U profile=0,completed=0,index=0,before=0;std::string expected;std::ifstream meta(path+".resume");check(bool(meta>>profile>>completed>>index>>before>>expected),"resume metadata");CampaignLab l(profile);l.open(path);check(l.stats().entities==before,"published final watermark");l.block(completed,7,index);check(digest(l.delta(before))==expected,"fresh process produces same future with verified historical workload");std::cout<<"{\"kind\":\"fresh_process\",\"profile\":"<<profile<<",\"completed\":"<<completed<<",\"future_equal\":true}\n";}
int main(int argc,char** argv){try{check(argc>=3,"arguments");const std::string mode=argv[1];if(mode=="resume")resume(argv[2]);else{check(argc==5,"campaign arguments");U profile=std::stoull(argv[2]),days=std::stoull(argv[3]);check(profile>=1 && profile<=5 && days>0,"profile days");run(profile,days,argv[4]);}return 0;}catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<'\n';return 1;}}
