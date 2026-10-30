#include "f04_bridge.h"
#include <chrono>
#include <fstream>
#include <iostream>
#include <memory>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#endif
using U=uint64_t;
void check(bool b,const char* m){if(!b)throw std::runtime_error(m);}
struct Session {
 F04Session* s=nullptr;F04Handles h{};
 Session(const char* cls,U crew,U residents,U passengers=0,U max=0){F04PopulationConfig cfg{65001,404,crew,residents,passengers,max};check(f04_create_population(1,cls,&cfg,&s)==F04_OK,"create population");handles();}
 ~Session(){f04_destroy(s);}
 void handles(){check(f04_handles(s,&h)==F04_OK,"handles");}
 F04Stats stats(){F04Stats x{};check(f04_stats(s,&x)==F04_OK,"stats");return x;}
 F04PopulationStats population(){F04PopulationStats x{};check(f04_population_stats(s,&x)==F04_OK,"population stats");return x;}
 F04Result op(U kind,U target=0,U value=0,U aux=0,uint32_t expected=F04_OK,U actor=3,U revision=UINT64_MAX){F04Request q{{h.captain.scope,actor},revision==UINT64_MAX?stats().revision:revision,static_cast<uint32_t>(kind),static_cast<uint32_t>(value),target,aux,0,1000,42};F04Result r{};auto code=f04_execute(s,&q,&r);if(code!=expected)std::cerr<<"op="<<kind<<" code="<<code<<" expected="<<expected<<"\n";check(code==expected,"operation");return r;}
 std::vector<F04Person> manifest(){std::vector<F04Person> all;U total=0,n=0,offset=0;do{F04Person page[73]{};check(f04_manifest_page(s,h.captain,offset,page,73,&n,&total)==F04_OK,"page");all.insert(all.end(),page,page+n);offset+=n;}while(offset<total);return all;}
 std::vector<uint8_t> save(){U n=0;check(f04_save(s,nullptr,0,&n)==F04_CAPACITY,"size");std::vector<uint8_t>b(n);check(f04_save(s,b.data(),n,&n)==F04_OK,"save");return b;}
 void load(const std::vector<uint8_t>& b){check(f04_load(s,b.data(),b.size())==F04_OK,"load");handles();}
};
template<class F> double measure(F f){auto t=std::chrono::steady_clock::now();f();return std::chrono::duration<double,std::milli>(std::chrono::steady_clock::now()-t).count();}
void write(const std::string& path,const std::vector<uint8_t>& b){std::ofstream f(path,std::ios::binary);f.write(reinterpret_cast<const char*>(b.data()),b.size());check(bool(f),"write");}
std::vector<uint8_t> read(const std::string& path){std::ifstream f(path,std::ios::binary);check(bool(f),"read");return {std::istreambuf_iterator<char>(f),{}};}
int main(int argc,char** argv){try{
 check(argc>=4,"args");std::string cls=argv[1],mode=argv[2],path=argv[3];
 U crew=cls=="miranda"?130:cls=="intrepid"?160:cls=="sovereign"?700:cls=="odyssey"?1600:1800,residents=cls=="valhalla"?400:0;
 if(mode=="budget") {Session large("valhalla",5000,0);check(large.stats().entities>4096,"old entity ceiling exceeded");auto b=large.save();large.load(b);check(large.population().assigned==5000,"technical headroom roundtrip");return 0;}
 if(mode=="dynamic"){
  Session s("miranda",127,0,2);auto p=s.population();check(p.assigned==127 && p.present==127 && p.nominal_vacancies==3 && p.passengers==2 && p.maximum==0,"127 crew plus passengers");
  U entities=s.stats().entities;U slot=s.op(F04_CREATE_SLOT,0,F04_COMMAND).record;check(s.stats().entities==entities+2 && s.population().assigned==127,"vacancy does not spawn person");
  s.op(F04_ASSIGN,slot,0,3);s.op(F04_DUTY,3,0,slot);s.op(F04_ABSENCE,3,F04_LEAVE);check(s.population().present==126,"temporary absence");U processed=0;check(f04_advance(s.s,1000,4096,&processed)==F04_OK,"absence expiry");
  auto newcomer=s.op(F04_EMBARK,0,1).record;check(newcomer>129,"new identity");s.op(F04_EMBARK,newcomer,1,0,F04_OVERLAP);
  s.op(F04_DEPART,newcomer);check(s.population().departed==1,"departure retained identity");
  // A departed crewmember retains a historical ship link but must not receive
  // fresh assignments, duties, absences or appointments from the current captain.
  s.op(F04_REST,newcomer,0,0,F04_DENIED);
  s.op(F04_APPOINT,newcomer,F04_FIRST,0,F04_DENIED);
  s.op(F04_ASSIGN,slot,0,newcomer,F04_DENIED);
  F04Person view{};check(f04_person(s.s,s.h.captain,newcomer,&view)==F04_SCOPE,"departed not representable");
  s.op(F04_EMBARK,newcomer,1);check(s.population().departed==0,"return same identity");
  auto civilian=s.op(F04_EMBARK,0,2).record;auto passenger=s.op(F04_EMBARK,0,3).record;check(s.population().residents==1 && s.population().passengers==3,"categories");s.op(F04_DEPART,civilian);s.op(F04_DEPART,passenger);
  s.op(F04_EMBARK,0,1,0,F04_STALE,3,0);s.op(F04_EMBARK,0,1,0,F04_DENIED,4);
  auto bytes=s.save();s.load(bytes);check(s.save()==bytes,"dynamic archive continuity");
  // Captain departure clears appointment, slots, duty and delegated authority.
  s.op(F04_DEPART,3);check(s.stats().commander==0,"no old captain authority");s.op(F04_BRIDGE,0,0,0,F04_UNAVAILABLE);check(s.stats().vacancies==1,"slot remains vacant");auto final=s.save();s.load(final);check(s.save()==final,"departed commander load");
  Session limited("miranda",127,0,2,129);limited.op(F04_EMBARK,0,1,0,F04_CAPACITY);
  Session over("miranda",131,0);check(over.population().assigned==131 && over.population().nominal_vacancies==0,"nominal is not capacity");
  F04Session* invalid=nullptr;F04PopulationConfig bad{1,1,8193,0,0,0};check(f04_create_population(1,"miranda",&bad,&invalid)!=F04_OK && !invalid,"technical budget");return 0;
 }
 std::unique_ptr<Session> s;double create=measure([&]{s=std::make_unique<Session>(cls.c_str(),crew,residents);});
 if(mode=="load"){auto bytes=read(path);s->load(bytes);check(s->save()==bytes,"cross process archive");F04Person captain{};check(f04_person(s->s,s->h.captain,3,&captain)==F04_OK && captain.on_duty,"persisted assignment and watch");auto expected=read(path+".future");s->op(F04_EMBARK,0,3);check(s->save()==expected,"cross process deterministic future");return 0;}
 U slot=s->op(F04_CREATE_SLOT,0,F04_COMMAND).record;s->op(F04_ASSIGN,slot,0,3);s->op(F04_DUTY,3,0,slot);
 std::vector<F04Person> people;double query=measure([&]{people=s->manifest();});std::set<U> ids;U fleet=0,civ=0;
 for(const auto& p:people){check(ids.insert(p.id).second,"unique identity");fleet+=p.category==1;civ+=p.category==2;}
 check(fleet==crew && civ==residents && ids.size()==crew+residents,"exact real population");
 auto pop=s->population();check(pop.nominal_crew==crew && pop.nominal_residents==residents && pop.maximum==0,"approved nominal complement");
 U written=99,total=0;check(f04_manifest_page(s->s,s->h.captain,0,nullptr,0,&written,&total)==F04_OK && !written && total==crew+residents,"count query");
 F04Person page{};check(f04_manifest_page(s->s,s->h.captain,total+1,&page,1,&written,&total)==F04_ARGUMENT,"offset bounds");
 F04Ref old=s->h.captain;{Session other("miranda",1,0);check(f04_person(s->s,other.h.captain,3,&page)==F04_DENIED,"cross ship/session handle rejected");}
 F04Person one{};double lookup=measure([&]{for(int i=0;i<1000;++i)check(f04_person(s->s,s->h.captain,people.back().id,&one)==F04_OK,"individual lookup");});
 std::vector<uint8_t> bytes;double save=measure([&]{bytes=s->save();});double load=measure([&]{s->load(bytes);});check(s->save()==bytes,"roundtrip");
 {Session same(cls.c_str(),crew,residents);U same_slot=same.op(F04_CREATE_SLOT,0,F04_COMMAND).record;same.op(F04_ASSIGN,same_slot,0,3);same.op(F04_DUTY,3,0,same_slot);check(same.save()==bytes,"same config and seed reproduce bootstrap");}
 check(f04_person(s->s,old,3,&page)==F04_DENIED,"expired handle after load");
 double update=measure([&]{s->op(F04_EMBARK,0,3);});auto future=s->save();s->load(bytes);s->op(F04_EMBARK,0,3);check(s->save()==future,"deterministic future");
 write(path,bytes);write(path+".future",future);
 U memory=0;
#ifdef _WIN32
 PROCESS_MEMORY_COUNTERS info{};if(GetProcessMemoryInfo(GetCurrentProcess(),&info,sizeof(info)))memory=info.PeakWorkingSetSize;
#endif
 std::cout<<cls<<" people="<<people.size()<<" create_ms="<<create<<" manifest_ms="<<query<<" lookup_1000_ms="<<lookup<<" update_ms="<<update<<" save_ms="<<save<<" load_ms="<<load<<" archive_bytes="<<bytes.size()<<" peak_working_set_bytes="<<memory<<"\n";
 return 0;
 }catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}}
