#include "organization_lab.h"
#include <chrono>
constexpr U day=86400;
struct Valhalla:Lab {
 Valhalla(U crew=1800,U residents=400):Lab(true,crew,"valhalla",true,F04_VALHALLA_FLAGSHIP,residents){}
 U actor(){return stats().commander;}
 void plan(U days=1,U start=0){op(F04_PLAN_WATCHES,0,days==1?0:1,start,start+days*day,days==1?F04_REFERENCE:F04_ROTATING,F04_OK,actor());}
 template<class T,class Fn>std::vector<T> pages(Fn fn) {
  U n=0,total=0,offset=0;std::vector<T> result;
  do{T page[97]{};check(fn(s,observer,offset,page,97,&n,&total)==F04_OK,"paged query");result.insert(result.end(),page,page+n);offset+=n;}while(offset<total);
  return result;
 }
 auto duties(){return pages<F04DutyView>(f04_duties_page);}
 auto gaps(){return pages<F04RosterGap>(f04_roster_gaps_page);}
 auto residents(){return pages<F04Resident>(f04_residents_page);}
 auto specialists(){return pages<F04Specialist>(f04_specialists_page);}
 auto coverage(U a,U b){std::array<F04ServiceCoverage,8>x{};U n=0;check(f04_service_coverage(s,observer,a,b,x.data(),8,&n)==F04_OK && n==8,"coverage");return x;}
};
void audit(Valhalla& l,U days,bool expect_critical=true) {
 std::map<U,std::vector<F04DutyView>> people;std::set<U> fleet;
 for(auto p:l.positions())fleet.insert(p.person);
 const auto duties=l.duties();for(auto d:duties){check(fleet.contains(d.person),"only existing fleet slots");if(d.start<d.stopped_at)people[d.person].push_back(d);}
 U max7=0,min_rest=UINT64_MAX,changed=0;
 for(auto& [p,work]:people){
  std::sort(work.begin(),work.end(),[](auto a,auto b){return a.start<b.start;});std::set<U> dates,labels;
  for(size_t i=0,left=0;i<work.size();++i){
   auto d=work[i];check(d.ordinary && d.end-d.start==28800,"eight hours");check(dates.insert(d.start/day).second,"one ordinary duty per day");labels.insert(d.start%day);
   while(d.start-work[left].start>=7*day)++left;max7=std::max(max7,U(i-left+1));check(i-left+1<=5,"rolling 7-day ceiling");
   if(i){check(d.start>=work[i-1].stopped_at+43200,"12-hour rest");min_rest=std::min(min_rest,d.start-work[i-1].stopped_at);}
  }changed+=labels.size()>1;
 }
 U quota=0,critical=0,covered=0;for(auto g:l.gaps())if(g.station)++critical;else quota+=g.missing;
 std::map<U,U> groups;for(auto p:l.specialists())groups[p.person]=p.group;
 for(U d=0;d<days;++d)for(U w=0;w<3;++w)for(auto c:l.coverage(d*day+w*28800,d*day+(w+1)*28800)) {
  covered+=c.covered;if(expect_critical)check(c.covered && c.first_gap==c.end,"full critical interval");
  if(c.person)check(groups[c.person]==F04_VALHALLA_NAVAL,"no Marines/Defiant counted as Valhalla service");
 }
 std::cout<<"METRICS days="<<days<<" shifts="<<duties.size()<<" critical="<<covered<<"/"<<days*24<<" quota_missing="<<quota<<" critical_gaps="<<critical<<" max7="<<max7<<" min_rest="<<min_rest<<" changed="<<changed<<"\n";
}
void run(const std::string& name,const std::string& path) {
 Valhalla l;
 if(name=="structure" || name=="reference") {
  check(l.stats().crew==1800 && l.stats().civilians==400,"1800+400");auto org=l.org();check(org.positions==1800 && org.assigned==1800 && org.sections==90 && org.departments==7,"organization");
  std::map<U,std::array<U,5>> expected;std::ifstream f(std::string(F04_FIXTURE_DIR)+"/valhalla_approved.tsv");U s,t,a,b,g,o;
  while(f>>s>>t>>a>>b>>g>>o)expected[s]={t,a,b,g,o};check(expected.size()==90,"official fixture");
  std::map<U,U> counts,depts;std::set<U> people,stable;
  for(auto p:l.positions()){++counts[p.section];++depts[p.department];check(people.insert(p.person).second && stable.insert(p.stable_id).second,"unique fleet/slots");}
  for(auto [s,row]:expected)check(counts[s]==row[0],"exact section total");
  check(depts==std::map<U,U>{{3,130},{2,405},{1,300},{5,310},{6,300},{7,215},{4,140}},"exact departments");
  for(auto r:l.residents())check(people.insert(r.person).second,"civil identity disjoint");check(people.size()==2200,"2200 unique");
  if(name=="structure")return;
  l.plan();std::map<U,F04Position> slots;for(auto p:l.positions())slots[p.id]=p;
  std::map<U,std::array<U,3>> actual;std::array<U,3> total{};std::set<U> workers;
  for(auto d:l.duties()){U w=(d.start%day/28800+2)%3;++actual[slots[d.slot].section][w];++total[w];check(workers.insert(d.person).second,"one day one duty");}
  check(total==std::array<U,3>{550,380,255} && 1800-workers.size()==615,"550/380/255/615");
  for(auto [s,row]:expected)check(actual[s]==std::array<U,3>{row[1],row[2],row[3]},"all 90 watch rows");check(l.gaps().empty(),"no reference gaps");audit(l,1);
  l.advance(28800);check(l.org().on_duty==550 && l.actor()==3,"Alpha");l.advance(57600);check(l.org().on_duty==380 && l.actor()!=3,"Beta");l.advance(day);check(l.actor()==0,"finite horizon");
 } else if(name=="7" || name=="14" || name=="28") {
  U days=std::stoull(name);l.plan(days);audit(l,days);l.advance(days*day-1);check(l.actor() && l.person(l.actor()).on_duty,"offscreen commander");
 } else if(name=="specialists") {
  U naval=0,marines=0,ordinary=0;std::map<U,U> sections;F04Auxiliary aux{};check(f04_auxiliary(l.s,l.observer,&aux)==F04_OK && aux.parent==1 && aux.entity!=1 && aux.docked,"persistent Defiant");
  std::map<U,F04Specialist> members;for(auto x:l.specialists())members[x.person]=x;
  for(auto [p,x]:members) {
   ++sections[x.section];naval+=x.group==2;marines+=x.group==3;ordinary+=x.group==1;
   check(x.administrative_ship==1 && x.operational_ship==(x.group==2?aux.entity:1),"one admin destination, one operational vessel");
   if(x.group==3){check(!(l.credentials(p)&((1ULL<<41)-2)),"no naval skill on Marines");if(x.superior)check(members.at(x.superior).group==3,"Marine chain stays in detachment");else check(x.section==63,"detachment command root");}
  }
  check(naval==40 && marines==60 && ordinary==1700,"40 naval + 60 Marines included");check(sections[79]==15,"docking technicians excluded");
  check(sections[63]==4 && sections[64]==10 && sections[65]==10 && sections[66]==10 && sections[67]==10 && sections[68]==6 && sections[69]==6 && sections[70]==4,"approved eight Marine units");
  l.plan();for(auto c:l.coverage(0,day))check(members.at(c.person).group==1,"no remote coverage");
  auto before=l.save();l.load(before);F04Auxiliary after{};check(f04_auxiliary(l.s,l.observer,&after)==F04_OK && aux.entity==after.entity && l.save()==before,"auxiliary survives load without duplicate people");
 } else if(name=="civilians") {
  auto rows=l.residents();check(rows.size()==400,"400 residents");std::array<U,7> counts{};std::set<U> homes,minor_contacts,adult_ids;
  for(auto r:rows)if(r.category==1)adult_ids.insert(r.person);
  for(auto r:rows){++counts[r.category];check(r.present && r.residence && homes.insert(r.residence).second && r.area==1,"unique logical residence");check(!l.credentials(r.person) && l.person(r.person).department==0 && !l.person(r.person).on_duty,"no military occupation");check(r.agenda_end-r.agenda_start==7200,"civil optional reservation, not 3x8");if(r.category==2){check(r.related_person && adult_ids.contains(r.related_person) && r.agenda_kind==2,"student linked to existing adult contact");check(minor_contacts.insert(r.related_person).second,"synthetic student contacts distributed among adults");}}
  check(counts==std::array<U,7>{0,130,90,65,50,35,30},"exact primary census");
  U p=rows.front().person;l.op(F04_CIVIL_PRESENCE,p,0,0,0,0);check(!l.residents()[0].present,"real absence");auto before=l.save();l.load(before);check(!l.residents()[0].present && l.save()==before,"absence persists");
  l.op(F04_CIVIL_PRESENCE,p,0,0,0,1);l.advance(rows.front().agenda_start);check(l.residents()[0].agenda_active,"agenda active without Actor");l.advance(rows.front().agenda_end);check(!l.residents()[0].agenda_active,"agenda ends");
 } else if(name=="authority" || name=="negative") {
  U marine=l.post(64).person,naval=l.post(12).person,civil=l.residents()[0].person,chief=l.post(52).person;
  l.op(F04_CREDENTIAL,marine,1ULL<<F04_Q_HELM,0,forever,0,F04_QUALIFICATION);
  l.op(F04_CREDENTIAL,marine,1ULL<<F04_Q_DEFIANT_BRIDGE,0,forever,0,F04_QUALIFICATION);
  l.op(F04_ASSIGN,l.post(4).id,marine,0,0,0,F04_SCOPE);l.op(F04_TRANSFER,l.post(12).id,marine,0,0,0,F04_OVERLAP);
  l.op(F04_ASSIGN,l.post(12).id,0);l.op(F04_TRANSFER,l.post(12).id,marine,0,0,0,F04_QUALIFICATION);
  l.op(F04_APPOINT,marine,F04_COMMAND,0,forever,F04_WATCH,F04_SCOPE);
  l.op(F04_APPOINT,naval,F04_COMMAND,0,forever,F04_WATCH,F04_SCOPE);
  l.op(F04_DUTY,civil,l.post(4).id,0,28800,0,F04_DENIED);
  l.op(F04_ASSIGN,l.post(4).id,civil,0,0,0,F04_DENIED);
  l.op(F04_BRIDGE,0,0,0,0,2,F04_UNAVAILABLE,civil);
  l.op(F04_BRIDGE,0,0,0,0,2,F04_DENIED,chief);
  l.op(F04_BRIDGE,0,0,0,0,2,F04_DENIED,marine);
  l.op(F04_IMPOSSIBLE,0,0,0,0,0,F04_SAFETY);
  check(l.stats().crew==1800 && l.stats().civilians==400 && l.org().vacant==1,"no substitute generation");
 } else if(name=="absence" || name=="relief") {
  l.plan();auto c=l.coverage(0,28800)[2];U target=0;for(auto d:l.duties())if(d.person==c.person && d.start==0)target=d.id;
  F04ReliefCandidate candidates[1800]{};U n=0,total=0;check(f04_relief_candidates_page(l.s,l.observer,target,0,28800,0,candidates,1800,&n,&total)==F04_OK && n,"qualified relief");U substitute=candidates[0].person;
  l.op(F04_ABSENCE,c.person,0,0,28800,F04_SICK,F04_OK,l.actor());check(!l.coverage(0,28800)[2].covered && !l.gaps().empty(),"actual incident gap");
  auto positions=l.positions();l.op(F04_COVER_DUTY,target,substitute,0,28800,0,F04_OK,l.actor());check(l.coverage(0,28800)[2].covered,"real relief");
  auto after=l.positions();for(size_t i=0;i<positions.size();++i)check(after[i].person==positions[i].person,"no permanent move");check(l.stats().crew==1800,"no invented people");
  auto before=l.save();l.load(before);check(l.save()==before && l.coverage(0,28800)[2].covered,"incident history survives");
 } else if(name=="deficit") {
  for(auto p:l.positions())if(p.section==27 || p.section==28)l.op(F04_ABSENCE,p.person,0,0,7*day,F04_SICK);
  l.plan(7);U missing=0;for(auto g:l.gaps())missing+=g.station==F04_ST_SENSORS;check(missing==21,"all impossible sensor windows recorded");audit(l,7,false);
 } else if(name=="rest") {
  U p=l.post(28).person;l.op(F04_REST,p,0,0,2*day);l.plan(7);for(auto d:l.duties())check(d.person!=p || d.start>=2*day,"rest protected");audit(l,7);
 } else if(name=="partial") {
  Valhalla small(25,0);small.plan();check(small.org().positions==1800 && small.org().assigned==25 && small.stats().crew==25 && !small.gaps().empty(),"real vacancies, no civilians drafted");
 } else if(name=="roundtrip" || name=="process_save" || name=="process_load") {
  if(name=="process_load"){l.load(read(path));l.advance(14*day-1);check(l.save()==read(path+".future"),"cross-process deterministic future");return;}
  auto old=l.save();l.plan(14);auto before=l.save();if(name=="process_save")write(path,before);l.advance(14*day-1);auto future=l.save();
  if(name=="process_save"){write(path+".future",future);return;}l.load(before);check(l.save()==before,"schema4 exact");l.advance(14*day-1);check(l.save()==future,"same future without Actors");l.load(old);check(l.save()==old && l.duties().empty(),"schema3 retained");
 } else if(name=="corrupt") {
  l.plan();auto before=l.save();auto data=corerpg::CampaignPersistence::deserialize(before);check(data.snapshot.has_value(),"decode");U marine=l.post(64).person;bool changed=false;
  for(auto& r:data.snapshot->campaign.relations)if(r.source.value()==marine && (r.kind.value()>>48)==0xF000+5){r.kind=corerpg::RelationKind{(U(0xF000+5)<<48)|(1ULL<<F04_Q_HELM)};changed=true;break;}
  check(changed,"Marine tamper");std::sort(data.snapshot->campaign.relations.begin(),data.snapshot->campaign.relations.end());auto bytes=corerpg::CampaignPersistence::serialize(*data.snapshot);check(bytes.status==corerpg::CampaignArchiveStatus::success,"checksum valid tamper");check(f04_load(l.s,bytes.bytes.data(),bytes.bytes.size())==F04_SAVE && l.save()==before,"atomic domain rejection");
 } else if(name=="limits") {
  l.plan(28);l.advance(28*day-1);const auto before=l.save();const auto count=l.duties().size();
  l.op(F04_PLAN_WATCHES,0,0,28*day,56*day,F04_ROTATING,F04_CAPACITY,l.actor());
  check(l.duties().size()==count && l.stats().crew==1800 && l.stats().civilians==400,"no partial capacity publication");
  const auto after=l.save(); // A rejection event is allowed, operational graph is unchanged.
  auto original=corerpg::CampaignPersistence::deserialize(before);auto rejected=corerpg::CampaignPersistence::deserialize(after);
  check(original.snapshot.has_value() && rejected.snapshot.has_value(),"decode capacity snapshots");
  const U last=original.snapshot->campaign.last_entity_id;auto& campaign=rejected.snapshot->campaign;
  check(campaign.last_entity_id==last+1 && campaign.definitions.back().definition_id=="trek.f04:event","only one rejection event added");
  std::erase_if(campaign.definitions,[&](const auto& d){return d.entity.value()>last;});
  std::erase_if(campaign.relations,[&](const auto& r){return r.source.value()>last;});
  campaign.last_entity_id=last;campaign.revision=original.snapshot->campaign.revision;
  auto normalized=corerpg::CampaignPersistence::serialize(*rejected.snapshot);
  check(normalized.bytes==before,"entire campaign, RNG and timeline unchanged except rejection audit event/revision");
  std::cout<<"CAPACITY entities28="<<l.stats().entities<<" archive_bytes28="<<before.size()<<" duties="<<count<<" after_rejection_bytes="<<after.size()<<"\n";
 } else if(name=="buffers") {
  U n=0,total=0;F04Resident r{};check(f04_residents_page(l.s,l.observer,400,&r,1,&n,&total)==F04_OK && n==0 && total==400,"last census page");check(f04_residents_page(l.s,l.observer,401,&r,1,&n,&total)==F04_ARGUMENT,"bad offset");auto before=l.save();auto stale=l.observer;l.load(before);check(f04_residents_page(l.s,stale,0,&r,1,&n,&total)==F04_DENIED,"stale handle");
 } else throw std::runtime_error("unknown case");
}
int main(int argc,char** argv){try{check(argc>1,"case");run(argv[1],argc>2?argv[2]:"");std::cout<<argv[1]<<": PASS\n";return 0;}catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<"\n";return 1;}}
