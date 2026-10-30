#include "organization_lab.h"
struct Intrepid:Lab {
 Intrepid(bool seed=true,U crew=160):Lab(seed,crew,"intrepid",true,F04_INTREPID_EXPLORATION){}
};
void run(const std::string& name,const std::string& path) {
 if(name=="profile") {
  F04TemplateSpec spec{};check(f04_template_spec(2,&spec)==F04_OK && spec.nominal_crew==160 && !spec.nominal_residents,"160 fleet, no residents");
  check(std::string(spec.class_id)=="intrepid" && std::string(spec.era)=="post_nemesis","class and era");
  for(const char* cls:{"miranda","sovereign","odyssey","valhalla"}) {
   Lab other(false,1,cls,false);other.op(F04_INSTALL_TEMPLATE,0,F04_INTREPID_EQUIPMENT,0,0,2,F04_SCOPE);
   check(other.stats().crew==1 && !other.stats().slots,"other classes unchanged");
  }
  Lab generic(false,160,"intrepid",false);check(!generic.stats().slots,"no automatic profile");
  generic.op(F04_INSTALL_TEMPLATE,0,1,0,0,2,F04_ARGUMENT);
  generic.op(F04_INSTALL_TEMPLATE,0,F04_INTREPID_EQUIPMENT,0,0,2);
  generic.op(F04_INSTALL_TEMPLATE,0,F04_INTREPID_EQUIPMENT,0,0,2,F04_ARGUMENT);return;
 }
 Intrepid l(name!="vacant" && name!="assignment");
 if(name=="structure") {
  const std::array<U,34> totals{1,1,4,7,3,2,9,8,6,7,4,2,10,7,6,4,5,2,6,6,7,4,2,5,8,3,1,4,7,5,1,3,7,3};
  const std::array<U,34> alpha{1,1,1,3,1,1,3,3,2,3,1,1,4,3,2,2,2,1,2,2,3,2,1,2,3,1,1,2,2,2,1,1,3,1};
  const std::map<U,std::pair<U,U>> expected{{F04_COMMAND,{16,7}},{F04_ENGINEERING,{36,13}},{F04_SENSORS,{34,14}},{F04_OPERATIONS,{25,10}},{F04_SECURITY,{18,7}},{F04_LOGISTICS,{17,7}},{F04_MEDICINE,{14,6}}};
  std::array<U,34> observed{},selected{};std::map<U,std::pair<U,U>> counts;std::set<U> people,stable;
  for(const auto& p:l.positions()) {
   check(p.section>=1 && p.section<=34,"section range");++observed[p.section-1];selected[p.section-1]+=p.alpha;
   ++counts[p.department].first;counts[p.department].second+=p.alpha;
   check(stable.insert(p.stable_id).second && p.stable_id==p.section*100+p.ordinal,"stable unique keys");
   check(p.person && people.insert(p.person).second,"unique persistent people");
   check(l.person(p.person).rank==0 && l.credentials(p.person)==p.qualification_mask,"no invented ranks or competencies");
  }
  check(observed==totals && selected==alpha && counts==expected,"all 34 section and 7 department subtotals");
  auto s=l.org();check(s.positions==160 && s.assigned==160 && s.departments==7 && s.sections==34 && s.alpha_expected==64,"organization counts");
  F04PopulationStats population{};check(f04_population_stats(l.s,&population)==F04_OK && population.assigned==160 && !population.residents,"EMH not a 161st person");
  F04SectionSpec sections[34]{};U n=0;check(f04_template_sections(2,sections,34,&n)==F04_OK && n==34,"section descriptors");
  for(auto& s:sections)check(s.name && s.responsibilities && s.equipment,"documented groups");
 }
 else if(name=="vacant") {
  check(l.org().vacant==160 && !l.org().assigned && l.stats().crew==160,"installation creates vacancies only");
  l.alpha();check(l.org().alpha_deficit==64 && !l.org().continuous_covered,"no fictitious cover");
  auto b=l.save();l.load(b);check(l.save()==b && l.org().vacant==160,"vacancies persist");
 }
 else if(name=="partial") {
  Intrepid partial(false,157);partial.op(F04_BOOTSTRAP_TEMPLATE);
  check(partial.org().assigned==157 && partial.org().vacant==3 && partial.stats().crew==157,"understaffing stays real");
  l.op(F04_BOOTSTRAP_TEMPLATE,0,0,0,0,0,F04_OVERLAP);
 }
 else if(name=="assignment") {
  auto sensor=l.post(13);l.op(F04_ASSIGN,sensor.id,4,0,0,0,F04_SCOPE);
  l.op(F04_CREDENTIAL,4,(1ULL<<F04_SENSORS)|(1ULL<<F04_Q_ASTROMETRY),0,forever);
  l.op(F04_TRANSFER,sensor.id,4);check(l.post(13).person==4,"assign existing person");
  l.op(F04_ASSIGN,l.post(13,2).id,4,0,0,0,F04_OVERLAP);
  l.op(F04_ASSIGN,sensor.id);check(l.org().vacant==160 && l.stats().crew==160,"release retains identity");
 }
 else if(name=="qualifications") {
  for(U section:{U(13),U(14),U(20),U(21),U(22)})check(!(l.credentials(l.post(section).person)&(1ULL<<F04_Q_REPAIR)),"operator or scientist is not repair technician");
  check(l.credentials(l.post(11).person)&(1ULL<<F04_Q_REPAIR),"engineering repairs deflectors");
  check(!(l.credentials(l.post(28).person)&(1ULL<<F04_Q_HELM)),"shuttle is distinct from main helm");
  check(!(l.credentials(l.post(4).person)&(1ULL<<F04_Q_SHUTTLE)),"main helm is distinct from shuttle");
  auto sensor=l.post(13);l.op(F04_CREDENTIAL,sensor.person,1ULL<<F04_SENSORS,0,forever);
  l.op(F04_DUTY,sensor.person,sensor.id,28800,57600,0,F04_QUALIFICATION);
 }
 else if(name=="alpha") {
  l.alpha();auto s=l.org();check(s.on_duty==64 && s.alpha_present==64 && !s.alpha_deficit && s.continuous_required==7 && s.continuous_covered==7 && s.urgent_response==1 && !s.coverage_validated,"64 distinct workers and 8 critical services including medicine");
  std::set<U> active;for(auto& p:l.positions())if(p.on_duty)check(active.insert(p.person).second,"one person per duty");check(active.size()==64,"64 unique");
  check(l.functions().size()==1 && l.functions()[0].person==l.post(23).person && l.functions()[0].active,"security chief same identity at tactical");
  l.advance(57600);check(!l.org().on_duty && !l.org().continuous_covered,"Alpha finite");
 }
 else if(name=="authority") {
  l.alpha();auto first=l.post(2),chief=l.post(23),doctor=l.post(31);
  check(chief.responsibility==F04_HEAD && l.post(23,2).responsibility==F04_DEPUTY,"chief and deputy");
  l.op(F04_BRIDGE,0,0,0,0,2,F04_OK,first.person);check(l.stats().commander==3,"first plus WATCH respects captain");
  l.op(F04_APPOINT,l.post(3).person,F04_COMMAND,28800,57600,F04_WATCH,F04_OVERLAP);
  l.op(F04_BRIDGE,0,0,0,0,2,F04_DENIED,chief.person);l.op(F04_BRIDGE,0,0,0,0,2,F04_DENIED,doctor.person);
  l.op(F04_MEDICAL,3,0,28800,28900,F04_SICK,F04_OK,doctor.person);check(l.stats().commander==first.person,"succession");
  l.advance(28900);check(l.stats().commander==3,"captain restored");
 }
 else if(name=="watch_fallback") {
  l.op(F04_ASSIGN,l.post(2).id);l.alpha();
  auto officer=l.post(3);check(l.org().on_duty==63 && l.org().alpha_deficit==1,"first officer vacancy stays real");
  l.op(F04_BRIDGE,0,0,0,0,2,F04_OK,officer.person);
  l.op(F04_APPOINT,l.post(3,2).person,F04_COMMAND,28800,57600,F04_WATCH,F04_OVERLAP);
  check(l.stats().commander==3,"one watch officer under captain");
 }
 else if(name=="functions") {
  l.alpha();auto chief=l.post(23),tactical=l.post(24);
  l.op(F04_FUNCTION,tactical.person,tactical.id,28800,57600,F04_ST_TACTICAL,F04_OVERLAP);
  l.op(F04_ABSENCE,chief.person,0,28800,30000,F04_SICK);check(!l.functions()[0].active && l.org().alpha_deficit==1,"absence disables tactical function");
  l.advance(30000);check(l.functions()[0].active,"return resumes function");
  l.op(F04_CREDENTIAL,chief.person,1ULL<<F04_SECURITY,0,forever);check(!l.functions()[0].active,"tactical competence required");
 }
 else if(name=="deficit_relief") {
  l.alpha();auto outgoing=l.post(13),incoming=l.post(13,5);l.op(F04_ASSIGN,incoming.id);
  l.op(F04_ABSENCE,outgoing.person,0,28800,30000,F04_SICK);check(l.org().alpha_deficit==1,"actual illness deficit");
  l.op(F04_RELIEF,outgoing.duty_record,incoming.person);
  check(l.post(13).person==incoming.person && l.post(13).on_duty && !l.post(13,5).person && l.stats().crew==160,"relief existing identity leaves real vacancy");
  auto b=l.save();l.load(b);check(l.save()==b && !l.org().alpha_deficit && l.org().vacant==1,"relief persists");
 }
 else if(name=="transfer") {
  l.alpha();auto sensor=l.post(13),dest=l.post(20);l.op(F04_ASSIGN,dest.id);
  l.op(F04_TRANSFER,dest.id,sensor.person,0,0,0,F04_QUALIFICATION);
  l.op(F04_CREDENTIAL,sensor.person,1ULL<<F04_Q_TRANSPORTER,0,forever);l.op(F04_TRANSFER,dest.id,sensor.person);
  check(!l.post(13).person && l.post(20).person==sensor.person && l.person(sensor.person).department==F04_OPERATIONS && !l.person(sensor.person).on_duty,"same identity, new destination and old duties cancelled");
  auto b=l.save();l.load(b);check(l.save()==b,"transfer persists");
 }
 else if(name=="lifecycle") {
  l.alpha();auto chief=l.post(23);l.op(F04_DEPART,chief.person);
  check(!l.post(23).person && !l.functions()[0].active && l.stats().crew==159,"departure releases position and console");
  auto b=l.save();l.load(b);l.op(F04_EMBARK,chief.person,0,0,0,1);l.op(F04_ASSIGN,chief.id,chief.person);
  check(l.stats().crew==160 && !l.post(23).on_duty,"same person returns without stale duties");
  l.op(F04_DUTY,chief.person,chief.id,28800,57600,0,F04_DENIED);
  l.op(F04_APPOINT,chief.person,F04_SECURITY,28800,forever,F04_HEAD);l.op(F04_DUTY,chief.person,chief.id,28800,57600);
 }
 else if(name=="rest") {
  auto p=l.post(14,7).person;l.op(F04_REST,p,0,28800,57600);l.advance(28800);
  check(!l.person(p).available && !l.person(p).on_duty,"protected rest distinct from idle");auto b=l.save();l.load(b);check(!l.person(p).available,"rest persists");
 }
 else if(name=="beta_gamma") {
  l.alpha();const std::array<std::pair<U,U>,7> beta{{{3,2},{4,4},{13,5},{21,4},{19,3},{6,2},{24,3}}},gamma{{{3,3},{4,5},{13,6},{21,5},{19,4},{7,4},{24,4}}};
  auto schedule=[&](const auto& selection,U start,U end,U medic){for(auto [section,ordinal]:selection){auto p=l.post(section,ordinal);check(!p.alpha,"night workers outside Alpha");l.op(F04_DUTY,p.person,p.id,start,end);if(section==3)l.op(F04_APPOINT,p.person,F04_COMMAND,start,end,F04_WATCH);if(section==24)l.op(F04_FUNCTION,p.person,p.id,start,end,F04_ST_TACTICAL);}l.op(F04_ONCALL,l.post(32,medic).person,0,start,end);};
  schedule(beta,57600,86400,2);schedule(gamma,86400,115200,3);
  l.advance(57600);check(l.org().on_duty==7 && l.org().continuous_covered==7 && l.org().urgent_response==2 && !l.org().coverage_validated,"Beta finite proposal, urgent oncall");
  // Operations must not be mistaken for communications in this profile.
  l.op(F04_ABSENCE,l.post(21,4).person,0,57600,58000,F04_SICK);check(l.org().continuous_covered==6,"separate operations gap");
  l.advance(86400);check(l.org().on_duty==7 && l.org().continuous_covered==7 && l.org().urgent_response==2 && !l.org().coverage_validated,"Gamma finite proposal");
  l.advance(115200);check(!l.org().on_duty && !l.org().continuous_covered && !l.org().urgent_response,"no invented next cycle");
 }
 else if(name=="patterns") {
  F04WatchWindow w{};check(f04_watch_window(l.s,28800,&w)==F04_OK && w.count==3 && w.start==28800 && w.end==57600,"3x8 retained");
  l.op(F04_POLICY,0,0,0,0,4,F04_VACANT);check(l.stats().pattern==3,"uncovered cycle rejected");
  // Four disjoint six-hour teams, with existing people; no 24-hour worker.
  for(U shift=0;shift<4;++shift)for(auto section:{3,4,13,21,19,7,24}){
   auto p=l.post(section,shift+1);U start=shift*21600,end=start+21600;
   l.op(F04_DUTY,p.person,p.id,start,end);if(section==3)l.op(F04_APPOINT,p.person,F04_COMMAND,start,end,F04_WATCH);
  }
  l.op(F04_POLICY,0,0,0,0,4);check(f04_watch_window(l.s,28800,&w)==F04_OK && w.count==4 && w.start==21600 && w.end==43200,"4x6 retained; coverage only, not rest certification");
 }
 else if(name=="roundtrip" || name=="process_save" || name=="process_load") {
  l.alpha();auto initial=l.save();Intrepid other;other.alpha();check(other.save()==initial,"deterministic profiles");
  if(name=="process_load"){initial=read(path);l.load(initial);check(l.save()==initial && l.org().on_duty==64,"other-process exact restore");l.advance(57600);check(l.save()==read(path+".future"),"other-process future");}
  else {auto ids=l.positions();l.load(initial);check(l.save()==initial && l.functions()[0].active,"full schema3 exact restore");auto after=l.positions();for(size_t i=0;i<ids.size();++i)check(ids[i].person==after[i].person && ids[i].stable_id==after[i].stable_id && ids[i].responsibility==after[i].responsibility,"identity sections responsibilities");l.advance(57600);other.advance(57600);check(l.save()==other.save(),"offscreen authoritative future");if(name=="process_save"){write(path,initial);write(path+".future",l.save());}}
 }
 else if(name=="corrupt") {
  l.alpha();auto original=l.save();
  for(U field:{U(28),U(31),U(33),U(34),U(37)}){
   auto d=corerpg::CampaignPersistence::deserialize(original);check(d.snapshot.has_value(),"Core decode");
   U target=field==28?1:l.post(13).id;bool changed=false;
   for(auto& r:d.snapshot->campaign.relations)if(r.source.value()==target && (r.kind.value()>>48)==0xF000+field){r.kind=corerpg::RelationKind{((0xF000+field)<<48)|9999};changed=true;break;}
   check(changed,"mutated profile field");++d.snapshot->campaign.revision;std::sort(d.snapshot->campaign.relations.begin(),d.snapshot->campaign.relations.end());auto archive=corerpg::CampaignPersistence::serialize(*d.snapshot);
   check(archive.status==corerpg::CampaignArchiveStatus::success && f04_load(l.s,archive.bytes.data(),archive.bytes.size())==F04_SAVE,"semantic corruption rejected");check(l.save()==original,"atomic failure");
  }
 }
 else throw std::runtime_error("unknown test");
}
int main(int argc,char** argv){try{check(argc>=2,"args");run(argv[1],argc>2?argv[2]:"");std::cout<<"intrepid "<<argv[1]<<" passed\n";return 0;}catch(const std::exception& e){std::cerr<<e.what()<<"\n";return 1;}}
