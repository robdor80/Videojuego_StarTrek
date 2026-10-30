// Included inside the bridge's private namespace. All mutable state is in Core.
bool organization(const WorldState& w) {return (val(w,1,SCHEMA)==3 || val(w,1,SCHEMA)==4);}
bool station_active(const WorldState& w,U f,U tick) {
 if(!window(w,f,tick))return false;
 const U p=ref(w,f,PERSON),slot=ref(w,f,SLOT),station=val(w,f,STATIONS);
 if(!primary_operator(w,p))return false;
 const U q=station==F04_ST_TACTICAL?F04_Q_TACTICAL:val(w,slot,QUAL);
 if(val(w,1,SCHEMA)==4) {
  if(station==F04_ST_COMMAND && !active_role(w,p,F04_WATCH,tick))return false;
  if(station==F04_ST_MEDICAL && !qualified(w,p,F04_Q_CLINICAL,tick) && !qualified(w,p,F04_Q_NURSING,tick))return false;
  if(station==F04_ST_ENGINEERING && !active_role(w,p,F04_DUTY_HEAD,tick,F04_ENGINEERING))return false;
 }
 return duty(w,p,slot,tick) && qualified(w,p,q,tick);
}
void cancel_post(Campaign& c,U p) {
 for(U slot:all(c.world,"slot"))if(ref(c.world,slot,PERSON)==p)link(c,slot,PERSON,0);
 for(const char* kind:{"activity","function"})for(U id:all(c.world,kind))
  if(ref(c.world,id,PERSON)==p && (type(c.world,id,"function") || val(c.world,id,VALUE)==F04_DUTY)){if(type(c.world,id,"activity") && val(c.world,1,SCHEMA)==4)set(c,id,STOP,std::clamp(c.time.now(),val(c.world,id,START),val(c.world,id,END)));set(c,id,STATE,CANCELLED);}
 action(c,p,PlaceEntityAction{EntityId{p},EntityId{1}});
}
U install_template(Campaign& c,const ContentCatalog& cat,const F04Request& r) {
 const auto* definition=trek_templates::profile(r.value);need(val(c.world,1,SCHEMA)==2 && definition);
 const auto& spec=definition->spec;
 need(type(c.world,1,(std::string("class_")+spec.class_id).c_str()) && val(c.world,1,NOMINAL_CREW)==spec.nominal_crew,F04_SCOPE);
 need(r.aux<=FOREVER && (r.aux&spec.required_equipment)==spec.required_equipment,F04_ARGUMENT);
 need(all(c.world,"slot").empty(),F04_OVERLAP);
 // Old ABI callers sometimes omitted the department for command appointments.
 // Normalize that optional context only during the explicit version upgrade.
 for(U a:all(c.world,"appointment"))if(!val(c.world,a,DEPT)) {
  const U role=val(c.world,a,ROLE);need(role!=F04_HEAD,F04_REVIEW);
  set(c,a,DEPT,role==F04_DOCTOR?F04_MEDICINE:F04_COMMAND);
 }
 set(c,1,SCHEMA,3);set(c,1,TEMPLATE,spec.id);set(c,1,EQUIPMENT,r.aux);set(c,1,SEEDED,0);
 set(c,1,ALPHA_START,0);set(c,1,ALPHA_END,0);
 if(spec.id==F04_VALHALLA_FLAGSHIP) {
  const U auxiliary=make(c,cat,"auxiliary_defiant");link(c,auxiliary,SHIP,1);set(c,auxiliary,SHIP_ID,auxiliary);set(c,auxiliary,STATE,ACTIVE);
 }
 std::map<U,U> departments;
 for(const auto& section:definition->sections)if(!departments.contains(section.department)) {
  const U id=make(c,cat,"department");link(c,id,SHIP,1);set(c,id,DEPT,section.department);departments[section.department]=id;
 }
 for(const auto& section:definition->sections) {
  const U id=make(c,cat,"section");link(c,id,SHIP,1);link(c,id,DEPARTMENT,departments.at(section.department));
  set(c,id,DEPT,section.department);set(c,id,SECTION_KEY,section.id);
  for(U ordinal=1;ordinal<=section.total;++ordinal) {
   const U slot=make(c,cat,"slot");link(c,slot,SHIP,1);link(c,slot,SECTION,id);
   set(c,slot,DEPT,section.department);set(c,slot,QUAL,section.qualification);set(c,slot,REQUIRED,0);
   set(c,slot,STABLE_ID,section.id*100+ordinal);set(c,slot,ORDINAL,ordinal);
   set(c,slot,QUAL_MASK,definition->qualification_mask(section));
   set(c,slot,RESPONSIBILITY,definition->post_responsibility(section.id,ordinal));
   set(c,slot,STATIONS,section.stations);set(c,slot,COVERAGE,section.coverage);set(c,slot,ALPHA,ordinal<=section.alpha);
  }
 }
 return 1;
}
U bootstrap_template(Campaign& c,const ContentCatalog& cat,const F04Request& r) {
 need(organization(c.world) && !val(c.world,1,SEEDED),F04_OVERLAP);
 std::vector<U> people;
 const U captain=commander(c.world,c.time.now());
 // Refuse to overwrite any authored qualifications, rank, department or roster.
 for(U p:all(c.world,"person"))if(member(c.world,p) && val(c.world,p,CATEGORY)==1) {
  need(val(c.world,p,RANK)==0 && val(c.world,p,DEPT)==(p==captain?U(F04_COMMAND):0) &&
   val(c.world,p,QUAL)==(p==captain?1ULL<<F04_COMMAND:0),F04_REVIEW);
  people.push_back(p);
 }
 need(!people.empty() && people.size()<=trek_templates::find(val(c.world,1,TEMPLATE))->nominal_crew && people.front()==captain,F04_REVIEW);
 need(all(c.world,"activity").empty() && all(c.world,"appointment").size()==1,F04_REVIEW);
 for(U slot:all(c.world,"slot"))need(!ref(c.world,slot,PERSON),F04_OVERLAP);
 size_t i=0;
 for(U slot:all(c.world,"slot")) {
  if(i==people.size())break;
  const U p=people[i++],dept=val(c.world,slot,DEPT),role=val(c.world,slot,RESPONSIBILITY);
  set(c,p,DEPT,dept);set(c,p,QUAL,val(c.world,slot,QUAL_MASK));set(c,p,UNTIL,FOREVER);link(c,slot,PERSON,p);
  if(role && role!=F04_CAPTAIN)appointment(c,cat,p,role,dept,c.time.now(),FOREVER,r.actor.id,r.cause);
 }
 seed_valhalla(c,cat);set(c,1,SEEDED,1);return 1;
}
bool organization_schema(const WorldState& w) {
 if(!organization(w))return all(w,"department").empty() && all(w,"section").empty() && all(w,"function").empty();
 const auto* definition=trek_templates::profile(val(w,1,TEMPLATE));if(!definition)return false;
 const auto& spec=definition->spec;
 if(!type(w,1,(std::string("class_")+spec.class_id).c_str()) || val(w,1,SEEDED)>1 ||
  (val(w,1,EQUIPMENT)&spec.required_equipment)!=spec.required_equipment)return false;
 const U start=val(w,1,ALPHA_START),end=val(w,1,ALPHA_END);
 if((start || end) && (start%86400!=28800 || end!=start+28800))return false;
 auto departments=all(w,"department"),sections=all(w,"section"),slots=all(w,"slot");
 std::set<U> expected_departments;for(const auto& s:definition->sections)expected_departments.insert(s.department);
 if(departments.size()!=expected_departments.size() || sections.size()!=definition->sections.size() || slots.size()!=spec.nominal_crew)return false;
 std::set<U> depts,keys,stable_ids;
 for(U d:departments)if(!depts.insert(val(w,d,DEPT)).second || val(w,d,DEPT)<1 || val(w,d,DEPT)>7)return false;
 for(U s:sections) {
  const auto* section=trek_templates::section(*definition,val(w,s,SECTION_KEY));
  if(!section || !keys.insert(section->id).second || !type(w,ref(w,s,DEPARTMENT),"department") ||
   val(w,s,DEPT)!=section->department || val(w,ref(w,s,DEPARTMENT),DEPT)!=section->department)return false;
 }
 std::map<U,U> counts;
 for(U slot:slots) {
  if(!type(w,ref(w,slot,SECTION),"section"))return false;
  const auto* s=trek_templates::section(*definition,val(w,ref(w,slot,SECTION),SECTION_KEY));
  const U ordinal=val(w,slot,ORDINAL),stable=val(w,slot,STABLE_ID);
  if(!s || ordinal<1 || ordinal>s->total || stable!=s->id*100+ordinal || !stable_ids.insert(stable).second ||
   val(w,slot,DEPT)!=s->department || val(w,slot,QUAL)!=s->qualification ||
   val(w,slot,QUAL_MASK)!=definition->qualification_mask(*s) || val(w,slot,REQUIRED)!=0 ||
   val(w,slot,RESPONSIBILITY)!=definition->post_responsibility(s->id,ordinal) ||
   val(w,slot,ALPHA)!=(ordinal<=s->alpha) || val(w,slot,COVERAGE)!=s->coverage || val(w,slot,STATIONS)!=s->stations)return false;
  ++counts[s->id];
 }
 for(const auto& s:definition->sections)if(counts[s.id]!=s.total)return false;
 for(U f:all(w,"function")) {
  U station=val(w,f,STATIONS),slot=ref(w,f,SLOT);
  if(!station || (station&(station-1)) || !(station&val(w,slot,STATIONS)))return false;
 }
 return true;
}
// A preliminary study of six service groups, not certification of a work regime.
bool service_covered(const WorldState& w,U station,U tick) {
 if(val(w,1,SCHEMA)==4) {
  for(U f:all(w,"function"))if(val(w,f,STATIONS)==station && station_active(w,f,tick))return true;
  return false;
 }
 for(U slot:all(w,"slot"))if((val(w,slot,STATIONS)&station) && duty(w,ref(w,slot,PERSON),slot,tick)) {
  const U p=ref(w,slot,PERSON);
  if(station==F04_ST_COMMAND && !active_role(w,p,F04_WATCH,tick) && !active_role(w,p,F04_CAPTAIN,tick) && !active_role(w,p,F04_FIRST,tick))continue;
  if(station==F04_ST_TACTICAL && !qualified(w,p,F04_Q_TACTICAL,tick))continue;
  return true;
 }
 return false;
}
