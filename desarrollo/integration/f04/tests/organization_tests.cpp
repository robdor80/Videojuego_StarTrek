#include "f04_bridge.h"
#include <corerpg/campaign_persistence.hpp>
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using U=uint64_t;
constexpr U forever=(1ULL<<48)-1;
void check(bool b,const char* m){if(!b)throw std::runtime_error(m);}
struct Lab {
 F04Session* s=nullptr;F04Ref observer{};
 Lab(bool seed=true,U crew=130,const char* cls="miranda",bool install=true) {
  F04PopulationConfig cfg{65001,404,crew,0,0,0};check(f04_create_population(1,cls,&cfg,&s)==F04_OK,"population");refresh();
  if(install){op(F04_INSTALL_TEMPLATE,0,F04_SUTHERLAND_EQUIPMENT,0,0,F04_SUTHERLAND_SCIENCE);if(seed)op(F04_BOOTSTRAP_TEMPLATE);}
 }
 ~Lab(){f04_destroy(s);}
 void refresh(){F04Handles h{};check(f04_handles(s,&h)==F04_OK,"handles");observer={h.ship.scope,3};}
 F04Stats stats(){F04Stats x{};check(f04_stats(s,&x)==F04_OK,"stats");return x;}
 F04OrganizationStats org(){F04OrganizationStats x{};check(f04_organization_stats(s,observer,&x)==F04_OK,"organization stats");return x;}
 F04Result op(uint32_t kind,U target=0,U aux=0,U start=0,U end=0,uint32_t value=0,uint32_t expected=F04_OK,U actor=3) {
  F04Request q{{observer.scope,actor},stats().revision,kind,value,target,aux,start,end,40401};F04Result result{};
  auto code=f04_execute(s,&q,&result);if(code!=expected)std::cerr<<"op="<<kind<<" actor="<<actor<<" got="<<code<<" expected="<<expected<<"\n";
  check(code==expected,"operation");return result;
 }
 std::vector<F04Position> positions(){std::vector<F04Position> result;U offset=0,total=0,n=0;
  do{F04Position page[23]{};check(f04_positions_page(s,observer,offset,page,23,&n,&total)==F04_OK,"positions page");result.insert(result.end(),page,page+n);offset+=n;}while(offset<total);return result;}
 F04Position post(U section,U ordinal=1){for(const auto& p:positions())if(p.section==section && p.ordinal==ordinal)return p;throw std::runtime_error("post");}
 F04Person person(U p){F04Person x{};check(f04_person(s,observer,p,&x)==F04_OK,"person");return x;}
 void advance(U tick){U n=0;check(f04_advance(s,tick,4096,&n)==F04_OK,"advance");}
 void alpha(){check(op(F04_PLAN_ALPHA,0,1,28800,57600).record==1,"Alpha recorded on ship");advance(28800);}
 std::vector<uint8_t> save(){U n=0;check(f04_save(s,nullptr,0,&n)==F04_CAPACITY,"size");std::vector<uint8_t>b(n);check(f04_save(s,b.data(),n,&n)==F04_OK,"save");return b;}
 void load(const std::vector<uint8_t>& b){check(f04_load(s,b.data(),b.size())==F04_OK,"load");refresh();}
 U credentials(U p){U mask=0,expiry=0;check(f04_person_credentials(s,observer,p,&mask,&expiry)==F04_OK,"credentials");return mask;}
 std::vector<F04FunctionView> functions(){U n=0;auto code=f04_functions(s,observer,nullptr,0,&n);check(code==(n?F04_CAPACITY:F04_OK),"function size");std::vector<F04FunctionView> f(n);check(f04_functions(s,observer,f.data(),n,&n)==F04_OK,"functions");return f;}
};
void write(const std::string& p,const std::vector<uint8_t>& b){std::ofstream f(p,std::ios::binary);f.write(reinterpret_cast<const char*>(b.data()),b.size());check(bool(f),"write");}
std::vector<uint8_t> read(const std::string& p){std::ifstream f(p,std::ios::binary);check(bool(f),"read");return {std::istreambuf_iterator<char>(f),{}};}
std::vector<uint8_t> hex_fixture(const char* name){std::ifstream f(std::string(F04_FIXTURE_DIR)+"/"+name);check(bool(f),"fixture");std::string hex;f>>hex;check(hex.size()%2==0,"hex");std::vector<uint8_t>b;for(size_t i=0;i<hex.size();i+=2)b.push_back(static_cast<uint8_t>(std::stoul(hex.substr(i,2),nullptr,16)));return b;}
void run(const std::string& name,const std::string& path) {
 if(name=="profile") {
  check(F04_SENSORS==1 && F04_ENGINEERING==2 && F04_COMMAND==3 && F04_MEDICINE==4,"legacy department IDs");
  for(const char* cls:{"miranda","intrepid","sovereign","odyssey","valhalla"}) {
   Lab l(false,1,cls,false);check(l.stats().slots==0,"no automatic template");
   if(std::string(cls)!="miranda")l.op(F04_INSTALL_TEMPLATE,0,F04_SUTHERLAND_EQUIPMENT,0,0,1,F04_SCOPE);
   else {l.op(F04_INSTALL_TEMPLATE,0,1,0,0,1,F04_ARGUMENT);l.op(F04_INSTALL_TEMPLATE,0,F04_SUTHERLAND_EQUIPMENT,0,0,1);l.op(F04_INSTALL_TEMPLATE,0,F04_SUTHERLAND_EQUIPMENT,0,0,1,F04_ARGUMENT);}
   check(l.stats().crew==1,"no synthetic people");
  }
  Lab generic(false,130,"miranda",false);generic.op(F04_CREATE_SLOT,0,0,0,0,F04_SENSORS);generic.op(F04_INSTALL_TEMPLATE,0,F04_SUTHERLAND_EQUIPMENT,0,0,1,F04_OVERLAP);return;
 }
 if(name=="legacy") {
  Lab l;for(const char* fixture:{"schema1.hex","schema2.hex"}) {auto b=hex_fixture(fixture);l.load(b);check(l.save()==b,"pre-extension archive byte exact");if(std::string(fixture)=="schema1.hex")check(l.stats().crew==7 && l.stats().slots==3,"schema1 retained");else{check(l.stats().crew==3 && !l.stats().slots,"schema2 retained");l.op(F04_INSTALL_TEMPLATE,0,F04_SUTHERLAND_EQUIPMENT,0,0,1);check(l.org().vacant==130 && l.stats().crew==3,"schema2 explicit upgrade");}}return;
 }
 Lab l(name!="vacant" && name!="assignment");
 if(name=="structure") {
  const std::array<U,32> totals{1,1,3,5,2,2,8,6,7,9,2,8,6,5,4,5,2,5,5,6,2,5,6,3,1,3,4,4,1,2,5,2};
  const std::array<U,32> alpha{1,1,1,2,1,1,3,2,2,3,1,3,3,2,2,3,1,2,1,2,1,1,2,1,1,1,2,2,1,1,2,1};
  const std::map<U,std::pair<U,U>> depts{{F04_COMMAND,{12,6}},{F04_ENGINEERING,{32,11}},{F04_SENSORS,{30,14}},{F04_OPERATIONS,{18,6}},{F04_SECURITY,{16,5}},{F04_LOGISTICS,{12,6}},{F04_MEDICINE,{10,5}}};
  std::array<U,32> observed{},observed_alpha{};std::map<U,std::pair<U,U>> counts;std::set<U> stable,people;
  for(const auto& p:l.positions()){check(stable.insert(p.stable_id).second && people.insert(p.person).second,"unique slot and occupant");++observed[p.section-1];observed_alpha[p.section-1]+=p.alpha;++counts[p.department].first;counts[p.department].second+=p.alpha;}
  check(observed==totals && observed_alpha==alpha && counts==depts,"approved section and department totals");
  auto s=l.org();check(s.positions==130 && s.departments==7 && s.sections==32 && s.alpha_expected==53,"exact template");
  F04TemplateSpec spec{};check(f04_template_spec(1,&spec)==F04_OK && spec.nominal_crew==130 && spec.nominal_residents==0,"profile descriptor");
  F04SectionSpec sections[32]{};U n=0;check(f04_template_sections(1,sections,32,&n)==F04_OK && n==32,"section descriptors");
  for(const auto& section:sections)check(section.name && section.responsibilities && section.equipment,"documented section");
 }
 else if(name=="vacant") {auto s=l.org();check(s.assigned==0 && s.vacant==130 && l.stats().crew==130,"installation only vacancies");check(l.op(F04_PLAN_ALPHA,0,1,28800,57600).record==1,"empty Alpha recorded");l.advance(28800);check(l.org().alpha_deficit==53 && l.org().continuous_covered==0,"real complete deficit");check(l.stats().crew==130,"no people generated");auto b=l.save();l.load(b);check(l.org().vacant==130,"vacancy persists");}
 else if(name=="bootstrap") {for(const auto& p:l.positions()){check(l.person(p.person).rank==0,"rank author pending");check(l.credentials(p.person)==p.qualification_mask,"only explicit starting skills");}check(l.org().assigned==130,"existing identities assigned");l.op(F04_BOOTSTRAP_TEMPLATE,0,0,0,0,0,F04_OVERLAP);check(l.stats().crew==130,"one-time fixture");Lab partial(false,127);partial.op(F04_BOOTSTRAP_TEMPLATE);check(partial.org().assigned==127 && partial.org().vacant==3 && partial.stats().crew==127,"partial crew no invention");}
 else if(name=="assignment") {
  auto sensor=l.post(12);l.op(F04_ASSIGN,sensor.id,4,0,0,0,F04_SCOPE);
  l.op(F04_CREDENTIAL,4,(1ULL<<F04_SENSORS)|(1ULL<<F04_Q_ASTROMETRY),0,forever);
  l.op(F04_TRANSFER,sensor.id,4);check(l.post(12).person==4,"compatible assignment");
  l.op(F04_ASSIGN,l.post(12,2).id,4,0,0,0,F04_OVERLAP);l.op(F04_ASSIGN,l.post(19).id,4,0,0,0,F04_SCOPE);
  l.op(F04_ASSIGN,sensor.id,0);check(l.org().vacant==130 && l.stats().crew==130,"unassignment retains identity");
 }
 else if(name=="qualifications") {auto p=l.post(12);l.op(F04_CREDENTIAL,p.person,1ULL<<F04_SENSORS,0,forever);l.op(F04_ASSIGN,p.id,p.person,0,0,0,F04_QUALIFICATION);l.op(F04_DUTY,p.person,p.id,28800,57600,0,F04_QUALIFICATION);check(l.org().alpha_deficit==53,"no false coverage");auto pilot=l.post(26);check(!(l.credentials(pilot.person)&(1ULL<<F04_Q_HELM)),"shuttle pilot not helm");auto transport=l.post(19);check(!(l.credentials(transport.person)&(1ULL<<F04_Q_REPAIR)),"transporter operation not repair");}
 else if(name=="authority") {
  l.alpha();auto first=l.post(2),chief=l.post(21),deputy=l.post(21,2),doctor=l.post(29),sensor=l.post(12);
  check(chief.person!=deputy.person && chief.responsibility==F04_HEAD && deputy.responsibility==F04_DEPUTY,"chief and deputy distinct");
  l.op(F04_BRIDGE,0,0,0,0,2,F04_OK,first.person);check(l.stats().commander==3,"watch does not replace captain");
  l.op(F04_BRIDGE,0,0,0,0,2,F04_DENIED,chief.person);l.op(F04_BRIDGE,0,0,0,0,2,F04_DENIED,doctor.person);
  l.op(F04_APPOINT,sensor.person,F04_COMMAND,28800,57600,F04_WATCH,F04_QUALIFICATION);
  l.op(F04_ABSENCE,l.post(23).person,0,28800,30000,F04_LEAVE,F04_OK,chief.person);
  l.op(F04_ABSENCE,l.post(7).person,0,28800,30000,F04_LEAVE,F04_SCOPE,chief.person);
  l.op(F04_MEDICAL,3,0,28800,28900,F04_SICK,F04_OK,doctor.person);check(l.stats().commander==first.person,"normal succession");l.advance(28900);check(l.stats().commander==3,"captain restored");
 }
 else if(name=="authority_boundary") {
  // A departmental deputy is not a command succession role or an origin for POLICY delegation.
  l.alpha();auto deputy=l.post(21,2),first=l.post(2),doctor=l.post(29);
  l.op(F04_CREDENTIAL,deputy.person,l.credentials(deputy.person)|(1ULL<<F04_COMMAND),0,forever);
  l.op(F04_APPOINT,deputy.person,F04_COMMAND,28800,forever,F04_SECOND);
  l.op(F04_MEDICAL,3,0,28800,28900,F04_SICK,F04_OK,doctor.person);
  l.op(F04_MEDICAL,first.person,0,28800,28900,F04_SICK,F04_OK,doctor.person);
  check(l.stats().commander==deputy.person,"only explicit SECOND appoints successor");
  const U delegation=l.op(F04_DELEGATE,l.post(3).person,0,28800,28890,F04_POLICY,F04_OK,deputy.person).record;
  const auto archive=corerpg::CampaignPersistence::deserialize(l.save());check(archive.snapshot.has_value(),"decode delegation");
  U origin=0,role=0;
  for(const auto& r:archive.snapshot->campaign.relations)
   if(r.source.value()==delegation && r.kind.value()==6)origin=r.target.value();
  check(origin!=0,"delegation origin is an appointment");
  for(const auto& r:archive.snapshot->campaign.relations)
   if(r.source.value()==origin && (r.kind.value()>>48)==0xF000+11)role=r.kind.value()&forever;
  check(role==F04_SECOND,"delegation must originate in command succession, not departmental deputy");
 }
 else if(name=="alpha") {l.alpha();auto s=l.org();check(s.on_duty==53 && s.alpha_present==53 && s.alpha_deficit==0 && s.continuous_covered==6 && !s.coverage_validated,"53 active distinct people; coverage not certified");std::set<U> active;for(const auto& p:l.positions())if(p.on_duty)check(active.insert(p.person).second,"no duplicated duty");check(active.size()==53,"53 unique");auto functions=l.functions();check(functions.size()==1 && functions[0].person==l.post(21).person && functions[0].active,"chief is tactical operator");l.advance(57600);check(l.org().on_duty==0 && l.org().continuous_covered==0,"Alpha is not 24h coverage");}
 else if(name=="alpha_deficit") {auto sensor=l.post(12);l.op(F04_ASSIGN,sensor.id);check(l.op(F04_PLAN_ALPHA,0,1,28800,57600).record==1,"Alpha with vacancy recorded");l.advance(28800);check(l.org().alpha_present==52 && l.org().alpha_deficit==1 && l.org().vacant==1,"real missing worker");l.op(F04_ABSENCE,l.post(12,2).person,0,28800,30000,F04_SICK);check(l.org().alpha_deficit==2,"absence adds deficit");l.op(F04_POLICY,0,0,0,0,4,F04_VACANT);check(l.stats().pattern==3,"cannot claim complete next cycle");}
 else if(name=="functions") {l.alpha();auto chief=l.post(21),tactical=l.post(22);check(l.functions()[0].person==chief.person,"single chief identity");l.op(F04_FUNCTION,tactical.person,tactical.id,28800,57600,F04_ST_TACTICAL,F04_OVERLAP);l.op(F04_ABSENCE,chief.person,0,28800,30000,F04_SICK);check(!l.functions()[0].active,"absence disables console function");l.advance(30000);check(l.functions()[0].active,"function resumes on return");l.op(F04_CREDENTIAL,chief.person,1ULL<<F04_SECURITY,0,forever);check(!l.functions()[0].active && !l.post(21).on_duty,"missing tactical qualification disables coverage");}
 else if(name=="beta_gamma") {
  l.alpha();const std::array<std::pair<U,U>,6> beta{{{3,2},{4,3},{12,4},{18,3},{6,2},{22,2}}},gamma{{{3,3},{4,4},{12,5},{18,4},{7,4},{22,3}}};
  auto schedule=[&](const auto& selection,U start,U end){for(auto [section,ordinal]:selection){auto p=l.post(section,ordinal);l.op(F04_DUTY,p.person,p.id,start,end);if(section==3)l.op(F04_APPOINT,p.person,F04_COMMAND,start,end,F04_WATCH);if(section==22)l.op(F04_FUNCTION,p.person,p.id,start,end,F04_ST_TACTICAL);}auto medical=l.post(30,2);l.op(F04_ONCALL,medical.person,0,start,end);};
  schedule(beta,57600,86400);schedule(gamma,86400,115200);
  l.advance(57600);auto b=l.org();check(b.on_duty==6 && b.continuous_covered==6 && b.urgent_response==2 && !b.coverage_validated,"Beta six active; medical oncall illustrative");
  l.advance(86400);auto g=l.org();check(g.on_duty==6 && g.continuous_covered==6 && g.urgent_response==2 && !g.coverage_validated,"Gamma six active; no rest policy claim");
  l.advance(115200);check(l.org().on_duty==0 && l.org().continuous_covered==0 && l.org().urgent_response==0,"finite example; actual deficits exposed");
 }
 else if(name=="transfer") {l.alpha();auto sensor=l.post(12),dest=l.post(19);l.op(F04_ASSIGN,dest.id);l.op(F04_TRANSFER,dest.id,sensor.person,0,0,0,F04_QUALIFICATION);l.op(F04_CREDENTIAL,sensor.person,1ULL<<F04_Q_TRANSPORTER,0,forever);l.op(F04_TRANSFER,dest.id,sensor.person);check(!l.post(12).person && l.post(19).person==sensor.person && l.person(sensor.person).department==F04_OPERATIONS && !l.person(sensor.person).on_duty,"transfer cancels old duties; same identity");auto b=l.save();l.load(b);check(l.save()==b,"transfer persisted");}
 else if(name=="relief") {l.alpha();auto outgoing=l.post(12),incoming=l.post(12,4);check(outgoing.duty_record!=0,"bulk Alpha exposes real duty record");l.op(F04_ASSIGN,incoming.id);l.op(F04_ABSENCE,outgoing.person,0,28800,30000,F04_SICK);check(l.org().alpha_deficit==1,"sick worker exposes gap");l.op(F04_RELIEF,outgoing.duty_record,incoming.person);check(l.post(12).person==incoming.person && l.post(12).on_duty && !l.post(12,4).person && l.org().alpha_deficit==0 && l.stats().crew==130,"existing person relieves without duplication");auto b=l.save();l.load(b);check(l.save()==b && l.post(12).person==incoming.person,"relief relationships persist");}
 else if(name=="lifecycle") {l.alpha();auto chief=l.post(21);l.op(F04_DEPART,chief.person);check(!l.post(21).person && !l.functions()[0].active && l.stats().crew==129,"departure clears duty function and post");auto b=l.save();l.load(b);l.op(F04_EMBARK,chief.person,0,0,0,1);l.op(F04_ASSIGN,chief.id,chief.person);check(l.post(21).person==chief.person && l.stats().crew==130 && !l.post(21).on_duty,"same identity returns without stale authority");l.op(F04_DUTY,chief.person,chief.id,28800,57600,0,F04_DENIED);l.op(F04_APPOINT,chief.person,F04_SECURITY,28800,forever,F04_HEAD);l.op(F04_DUTY,chief.person,chief.id,28800,57600);check(l.post(21).on_duty,"explicit fresh appointment");}
 else if(name=="rest") {auto person=l.post(13,6).person;l.op(F04_REST,person,0,28800,57600);l.advance(28800);check(!l.person(person).available && !l.person(person).on_duty,"recorded rest distinguished from off duty");auto b=l.save();l.load(b);check(!l.person(person).available,"rest persists");}
 else if(name=="roundtrip" || name=="determinism" || name=="process_save" || name=="process_load") {
  l.alpha();auto initial=l.save();Lab other;other.alpha();check(other.save()==initial,"deterministic bootstrap and Alpha");
  if(name=="process_load"){initial=read(path);l.load(initial);check(l.save()==initial && l.org().on_duty==53,"cross process relationships");l.advance(57600);check(l.save()==read(path+".future"),"cross process future");}
  else {auto ids=l.positions();l.load(initial);check(l.save()==initial && l.org().on_duty==53 && l.functions()[0].active,"exact complete organization roundtrip");auto after=l.positions();for(size_t i=0;i<ids.size();++i)check(ids[i].stable_id==after[i].stable_id && ids[i].person==after[i].person,"stable identities");l.advance(57600);auto future=l.save();other.advance(57600);check(other.save()==future,"deterministic future");if(name=="process_save"){write(path,initial);write(path+".future",future);}}
 }
 else if(name=="corrupt") {
  l.alpha();auto original=l.save();auto post=l.post(12);
  // Core-valid archives with invalid Trek relations must be rejected atomically.
  for(U field:{U(4),U(31),U(32),U(33),U(34),U(35),U(36),U(37)}) {
   auto d=corerpg::CampaignPersistence::deserialize(original);check(d.snapshot.has_value(),"decode");bool changed=false;
   for(auto& r:d.snapshot->campaign.relations)if(r.source.value()==post.id && (r.kind.value()>>48)==0xF000+field){r.kind=corerpg::RelationKind{((0xF000+field)<<48)|9999};changed=true;break;}
   check(changed,"target scalar exists");++d.snapshot->campaign.revision;std::sort(d.snapshot->campaign.relations.begin(),d.snapshot->campaign.relations.end());auto archive=corerpg::CampaignPersistence::serialize(*d.snapshot);check(archive.status==corerpg::CampaignArchiveStatus::success,"encode");check(f04_load(l.s,archive.bytes.data(),archive.bytes.size())==F04_SAVE,"invalid organization rejected");check(l.save()==original,"atomic rejected load");
  }
 }
 else if(name=="buffers") {U total=0,n=0;check(f04_positions_page(l.s,l.observer,0,nullptr,0,&n,&total)==F04_OK && total==130 && n==0,"count query");check(f04_positions_page(l.s,l.observer,131,nullptr,0,&n,&total)==F04_ARGUMENT,"offset bounds");F04Ref old=l.observer;auto b=l.save();l.load(b);check(f04_positions_page(l.s,old,0,nullptr,0,&n,&total)==F04_DENIED,"old scope rejected");check(f04_positions_page(l.s,l.observer,0,nullptr,1,&n,&total)==F04_ARGUMENT,"buffer contract");}
 else throw std::runtime_error("unknown test");
}
int main(int argc,char** argv){try{check(argc>=2,"args");run(argv[1],argc>2?argv[2]:"");std::cout<<argv[1]<<" passed\n";return 0;}catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}}
