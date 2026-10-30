#include "f04_bridge.h"
#include "f04_catalog.h"
#include "f04_templates.h"
#include <corerpg/campaign_persistence.hpp>
#include <corerpg/content_catalog.hpp>
#include <algorithm>
#include <array>
#include <atomic>
#include <cstring>
#include <memory>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <thread>
#include <unordered_map>

namespace {
using namespace corerpg;
using U=uint64_t;
constexpr U FOREVER=(1ULL<<48)-1;
// Versioned Trek relation-label vocabulary. Scalar values are self-edges;
// references use fixed kinds. Core owns both, without interpreting domain data.
enum Ref:U { SHIP=1,PERSON,SLOT,ISSUER,TARGET,ORIGIN,ACTIVITY,DEPARTMENT,SECTION };
enum Field:U { START=1,END,VALUE,DEPT,QUAL,UNTIL,RANK,CATEGORY,REQUIRED,STATE,
 ROLE,D_DOMAIN,CAUSE,DEBT,OP,CODE,TICK,PATTERN,SCHEMA,SEQUENCE,ALERT,
 MEMBER,SHIP_ID,NOMINAL_CREW,NOMINAL_RESIDENTS,MAXIMUM,INITIAL,
 TEMPLATE,EQUIPMENT,SECTION_KEY,STABLE_ID,ORDINAL,QUAL_MASK,RESPONSIBILITY,
 STATIONS,COVERAGE,ALPHA,SEEDED,ALPHA_START,ALPHA_END };
enum State:U { ACTIVE=0,CANCELLED=1,DONE=2 };
struct Denial { uint32_t code; };
void need(bool yes,uint32_t code=F04_ARGUMENT) { if(!yes) throw Denial{code}; }
struct Campaign { WorldState world; RandomStreams random{404}; Timeline time; };
U ref(const WorldState& w,U id,Ref field) {
 for(const auto& r:w.relations_from(EntityId{id})) if(r.kind.value()==field) return r.target.value();
 return 0;
}
U val(const WorldState& w,U id,Field field) {
 const U prefix=(0xF000+field)<<48;
 for(const auto& r:w.relations_from(EntityId{id})) if((r.kind.value()&~FOREVER)==prefix) return r.kind.value()&FOREVER;
 return 0;
}
bool has(const WorldState& w,U id,Field f) {
 for(const auto& r:w.relations_from(EntityId{id})) if((r.kind.value()>>48)==0xF000+f) return true;
 return false;
}
bool type(const WorldState& w,U id,const char* name) {
 static thread_local std::unordered_map<std::string,DefinitionId> ids;
 auto it=ids.find(name);if(it==ids.end())it=ids.emplace(name,*DefinitionId::parse(std::string("trek.f04:")+name)).first;
 const auto* d=w.definition_of(EntityId{id}); return d && *d==it->second;
}
bool member(const WorldState& w,U p) { return ref(w,p,SHIP)==1 && (val(w,1,SCHEMA)==1 || val(w,p,MEMBER)==1); }
std::vector<U> all(const WorldState& w,const char* name) {
 std::vector<U> ids; for(U id=1;id<=w.entity_count();++id) if(type(w,id,name)) ids.push_back(id); return ids;
}
bool window(const WorldState& w,U id,U t) { return val(w,id,STATE)==ACTIVE && val(w,id,START)<=t && t<val(w,id,END); }
bool overlaps(U a,U b,U c,U d) { return a<d && c<b; }
void action(Campaign& c,U actor,ActionOperation op) {
 const auto r=ActionEngine::process(c.world,c.random,{EntityId{actor},std::move(op),c.world.revision()});
 need(r.outcome!=ActionOutcome::rejected,F04_INTERNAL);
}
void edge(Campaign& c,U id,U kind,U target) { action(c,id,AddRelationAction{{EntityId{id},RelationKind{kind},EntityId{target}}}); }
void erase(Campaign& c,const EntityRelation& e) { action(c,e.source.value(),RemoveRelationAction{e}); }
void set(Campaign& c,U id,Field field,U value) {
 need(value<=FOREVER); std::vector<EntityRelation> old;
 for(const auto& r:c.world.relations_from(EntityId{id})) if((r.kind.value()>>48)==0xF000+field) old.push_back(r);
 for(const auto& r:old) erase(c,r);
 edge(c,id,((0xF000+field)<<48)|value,id);
}
void link(Campaign& c,U id,Ref field,U target) {
 std::vector<EntityRelation> old;
 for(const auto& r:c.world.relations_from(EntityId{id})) if(r.kind.value()==field) old.push_back(r);
 for(const auto& r:old) erase(c,r);
 if(target) edge(c,id,field,target);
}
CatalogBuildResult catalog() {
 const auto p=*PackId::parse("trek.f04"); const auto v=*SemanticVersion::parse("0.1.0");
 std::vector<ContentDefinitionInput> defs;
 for(const char* t:{"population","person","slot","activity","appointment","delegation","event","task","order","mandate","review","department","section","function"})
  defs.emplace_back(ResourceDefinition{*DefinitionId::parse(std::string("trek.f04:")+t),*ResourceKind::parse("structural")});
 for(const char* t:class_ids) defs.emplace_back(ResourceDefinition{*DefinitionId::parse(std::string("trek.f04:class_")+t),*ResourceKind::parse("structural")});
 return ContentCatalog::create({ContentPackInput{ContentManifest{p,v,v,v},std::move(defs)}});
}
U make(Campaign& c,const ContentCatalog& cat,const char* name) {
 // Technical archive/work budget, not a physical ship capacity: 2200 people
 // plus up to ~29 operational records per person within the 64 MiB loader cap.
 need(c.world.entity_count()<65536,F04_CAPACITY);
 const auto id=c.world.create_entity(); need(id.is_valid(),F04_INTERNAL);
 need(c.world.bind_definition(id,cat,*DefinitionId::parse(std::string("trek.f04:")+name))==DefinitionBindingChange::applied,F04_INTERNAL);
 return id.value();
}
void temporal(Campaign& c,U id,U start,U end) { need(start<end && end<=FOREVER); set(c,id,START,start);set(c,id,END,end);set(c,id,STATE,ACTIVE); }
constexpr U QUALIFICATIONS=(1ULL<<31)-2;
bool qualified(const WorldState& w,U p,U q,U t) { return q>=1 && q<=30 && (val(w,p,QUAL)&(1ULL<<q)) && t<val(w,p,UNTIL); }
bool slot_qualified(const WorldState& w,U p,U slot,U t) {
 const U mask=has(w,slot,QUAL_MASK)?val(w,slot,QUAL_MASK):1ULL<<val(w,slot,QUAL);
 return (val(w,p,QUAL)&mask)==mask && t<val(w,p,UNTIL);
}
bool available(const WorldState& w,U p,U t) {
 if(!type(w,p,"person") || val(w,p,CATEGORY)!=1 || !member(w,p)) return false;
 for(U a:all(w,"activity")) if(ref(w,a,PERSON)==p && window(w,a,t) &&
  (val(w,a,VALUE)==F04_ABSENCE || val(w,a,VALUE)==F04_REST)) return false;
 return true;
}
bool active_role(const WorldState& w,U p,U role,U t,U dept=0) {
 if(!member(w,p))return false;
 for(U a:all(w,"appointment")) if(ref(w,a,PERSON)==p && val(w,a,ROLE)==role && window(w,a,t) && (!dept || val(w,a,DEPT)==dept)) return true;
 return false;
}
U commander(const WorldState& w,U t) {
 for(U role:{U(F04_CAPTAIN),U(F04_FIRST),U(F04_SECOND),U(F04_SUCCESSOR)})
  for(U a:all(w,"appointment")) { const U p=ref(w,a,PERSON);
   if(val(w,a,ROLE)==role && window(w,a,t) && available(w,p,t) && qualified(w,p,F04_COMMAND,t)) return p;
  }
 return 0;
}
bool duty(const WorldState& w,U p,U slot,U t) {
 if(!available(w,p,t) || ref(w,slot,PERSON)!=p || !slot_qualified(w,p,slot,t)) return false;
 const U role=val(w,slot,RESPONSIBILITY);
 if(role && !active_role(w,p,role,t,val(w,slot,DEPT)))return false;
 for(U a:all(w,"activity")) if(ref(w,a,PERSON)==p && ref(w,a,SLOT)==slot && val(w,a,VALUE)==F04_DUTY && window(w,a,t)) return true;
 return false;
}
bool command_authority(const WorldState& w,U p,U domain,U t) {
 if(!member(w,p))return false;
 if(commander(w,t)==p) return true;
 for(U d:all(w,"delegation")) {
  const U origin=ref(w,d,ORIGIN), issuer=ref(w,d,ISSUER);
  if(ref(w,d,PERSON)==p && val(w,d,D_DOMAIN)==domain && window(w,d,t) &&
   issuer==commander(w,t) && type(w,origin,"appointment") && window(w,origin,t) &&
   ref(w,origin,PERSON)==issuer && qualified(w,p,F04_COMMAND,t)) return true;
 }
 return false;
}
bool external_authority(const WorldState& w,U p,U domain,U t) {
 if(!member(w,p))return false;
 for(U a:all(w,"mandate")) if(ref(w,a,PERSON)==p && val(w,a,D_DOMAIN)==domain && window(w,a,t))return true;
 return false;
}
bool head(const WorldState& w,U p,U dept,U t) {
 return (active_role(w,p,F04_HEAD,t,dept) || (val(w,1,SCHEMA)==3 && dept==F04_MEDICINE && active_role(w,p,F04_DOCTOR,t))) && qualified(w,p,dept,t);
}
U appointment(Campaign& c,const ContentCatalog& cat,U p,U role,U dept,U start,U end,U issuer,U cause) {
 const U id=make(c,cat,"appointment");link(c,id,SHIP,1);link(c,id,PERSON,p);link(c,id,ISSUER,issuer);
 temporal(c,id,start,end);set(c,id,ROLE,role);set(c,id,DEPT,dept);set(c,id,CAUSE,cause);return id;
}
U event(Campaign& c,const ContentCatalog& cat,U actor,U op,U code,U cause,U target) {
 const U id=make(c,cat,"event");link(c,id,SHIP,1); if(actor && c.world.contains(EntityId{actor})) link(c,id,PERSON,actor);
 if(target && c.world.contains(EntityId{target})) link(c,id,TARGET,target);
 set(c,id,OP,op);set(c,id,CODE,code);set(c,id,CAUSE,cause);set(c,id,TICK,c.time.now());return id;
}
void initialize(Campaign& c,const ContentCatalog& cat,const char* cls) {
 bool found=false; for(const auto* s:class_ids) found|=std::strcmp(cls,s)==0;need(found);
 const std::string def=std::string("class_")+cls;need(make(c,cat,def.c_str())==1);set(c,1,SCHEMA,1);set(c,1,PATTERN,3);set(c,1,ALERT,1);
 need(make(c,cat,"population")==2);need(c.world.declare_population(EntityId{2},9)==PopulationChange::applied);
 need(c.world.materialize_population(EntityId{2},9).status==MaterializationStatus::applied);
 for(U p=3;p<=11;++p) {
  need(c.world.bind_definition(EntityId{p},cat,*DefinitionId::parse("trek.f04:person"))==DefinitionBindingChange::applied);
  link(c,p,SHIP,1);set(c,p,CATEGORY,p==9?2:p==10?3:1);set(c,p,RANK,p==10?10:p==3?8:1);
  const U dept=p==5 || p==4 || p==8?F04_SENSORS:p==7?F04_MEDICINE:p==11?F04_ENGINEERING:F04_COMMAND;
  set(c,p,DEPT,dept);set(c,p,QUAL,1ULL<<dept);set(c,p,UNTIL,p==8?86400:FOREVER);
  action(c,p,PlaceEntityAction{EntityId{p},EntityId{1}});
 }
 for(U dept=1;dept<=3;++dept) {
  const U slot=make(c,cat,"slot");link(c,slot,SHIP,1);set(c,slot,DEPT,dept);set(c,slot,QUAL,dept);set(c,slot,REQUIRED,1);
  action(c,slot,PlaceEntityAction{EntityId{slot},EntityId{1}});
 }
 appointment(c,cat,3,F04_CAPTAIN,F04_COMMAND,0,FOREVER,3,1);
 appointment(c,cat,4,F04_HEAD,F04_SENSORS,0,FOREVER,3,1);
 appointment(c,cat,6,F04_WATCH,F04_COMMAND,0,8*3600,3,1);
 appointment(c,cat,7,F04_DOCTOR,F04_MEDICINE,0,FOREVER,3,1);
 appointment(c,cat,6,F04_FIRST,F04_COMMAND,0,FOREVER,3,1);
 // Explicit synthetic mission authority, imported by trusted bootstrap. Visiting
 // rank alone grants no such mandate and no shipboard command or technical role.
 const U mandate=make(c,cat,"mandate");link(c,mandate,SHIP,1);link(c,mandate,PERSON,10);
 temporal(c,mandate,0,FOREVER);set(c,mandate,D_DOMAIN,F04_CONTACT);set(c,mandate,CAUSE,40401);
}
void initialize_population(Campaign& c,const ContentCatalog& cat,const char* cls,const F04PopulationConfig& config) {
 const Complement* spec=nullptr;for(const auto& s:complements)if(std::strcmp(cls,s.id)==0)spec=&s;
 need(spec && config.ship_identity && config.ship_identity<=FOREVER);
 need(config.crew>=1 && config.crew<=8192 && config.residents<=8192 && config.passengers<=8192);
 const U count=config.crew+config.residents+config.passengers;
 need(count<=8192 && (!config.maximum || count<=config.maximum),F04_CAPACITY);
 need(config.maximum<=8192,F04_CAPACITY);c.random=RandomStreams{config.seed};
 const std::string def=std::string("class_")+cls;need(make(c,cat,def.c_str())==1);
 set(c,1,SCHEMA,2);set(c,1,PATTERN,3);set(c,1,ALERT,1);set(c,1,SHIP_ID,config.ship_identity);
 set(c,1,NOMINAL_CREW,spec->crew);set(c,1,NOMINAL_RESIDENTS,spec->residents);set(c,1,MAXIMUM,config.maximum);set(c,1,INITIAL,count);
 need(make(c,cat,"population")==2);need(c.world.declare_population(EntityId{2},count)==PopulationChange::applied);
 need(c.world.materialize_population(EntityId{2},count,8192).status==MaterializationStatus::applied);
 for(U i=0;i<count;++i) {
  U p=i+3;need(c.world.bind_definition(EntityId{p},cat,*DefinitionId::parse("trek.f04:person"))==DefinitionBindingChange::applied);
  link(c,p,SHIP,1);set(c,p,MEMBER,1);set(c,p,CATEGORY,i<config.crew?1:i<config.crew+config.residents?2:3);
  // Only the explicit bootstrap captain has an operational role. No invented
  // department/rank distribution for the remaining population.
  set(c,p,RANK,0);set(c,p,DEPT,i==0?F04_COMMAND:0);set(c,p,QUAL,i==0?1ULL<<F04_COMMAND:0);set(c,p,UNTIL,FOREVER);
  action(c,p,PlaceEntityAction{EntityId{p},EntityId{1}});
 }
 appointment(c,cat,3,F04_CAPTAIN,F04_COMMAND,0,FOREVER,3,1);
}
#include "f04_organization.inc"
// Strict relational schema. It rejects undeclared labels/fields and duplicate
// scalar/reference fields before any restored graph becomes live.
bool schema(const Campaign& c) {
 const auto& w=c.world;
 const bool org=organization(w),general=val(w,1,SCHEMA)>=2;const U initial=general?val(w,1,INITIAL):9;
 if(w.entity_count()<(general?4U:19U) || w.entity_count()>65536 || val(w,1,SCHEMA)<1 || val(w,1,SCHEMA)>3 || !w.definition_of(EntityId{1}) ||
    val(w,1,PATTERN)<3 || val(w,1,PATTERN)>4 || val(w,1,ALERT)<1 || val(w,1,ALERT)>3 || c.time.now()>FOREVER || !c.time.records().empty()) return false;
 bool cls=false;for(auto* s:class_ids) cls|=type(w,1,(std::string("class_")+s).c_str());if(!cls)return false;
 for(U id=1;id<=w.entity_count();++id) {
  std::set<U> fields,refs; std::set<U> allowed,required,ar,rr;
  if(id==1) { allowed={SCHEMA,PATTERN,ALERT};if(general)allowed.insert({SHIP_ID,NOMINAL_CREW,NOMINAL_RESIDENTS,MAXIMUM,INITIAL});if(org)allowed.insert({TEMPLATE,EQUIPMENT,SEEDED,ALPHA_START,ALPHA_END});required=allowed; }
  else if(type(w,id,"population")) { if(id!=2)return false; }
  else if(type(w,id,"person")) { allowed={CATEGORY,RANK,DEPT,QUAL,UNTIL};if(general)allowed.insert(MEMBER);required=allowed;ar={SHIP};rr=ar; }
  else if(type(w,id,"slot")) { allowed={DEPT,QUAL,REQUIRED};if(org)allowed.insert({STABLE_ID,ORDINAL,QUAL_MASK,RESPONSIBILITY,STATIONS,COVERAGE,ALPHA});required=allowed;ar={SHIP,PERSON};rr={SHIP};if(org){ar.insert(SECTION);rr.insert(SECTION);} }
  else if(type(w,id,"department") && org) {allowed={DEPT};required=allowed;ar={SHIP};rr=ar;}
  else if(type(w,id,"section") && org) {allowed={DEPT,SECTION_KEY};required=allowed;ar={SHIP,DEPARTMENT};rr=ar;}
  else if(type(w,id,"function") && org) {allowed={START,END,STATE,STATIONS,CAUSE};required=allowed;ar={SHIP,PERSON,SLOT,ISSUER};rr=ar;}
  else if(type(w,id,"activity")) { allowed={START,END,STATE,VALUE,CAUSE,DEBT,CODE}; required={START,END,STATE,VALUE,CAUSE};ar={SHIP,PERSON,SLOT,ISSUER,ACTIVITY};rr={SHIP,PERSON,ISSUER}; }
  else if(type(w,id,"appointment")) { allowed={START,END,STATE,ROLE,DEPT,CAUSE};required=allowed;ar={SHIP,PERSON,ISSUER};rr=ar; }
  else if(type(w,id,"delegation")) { allowed={START,END,STATE,D_DOMAIN,CAUSE};required=allowed;ar={SHIP,PERSON,ISSUER,ORIGIN};rr=ar; }
  else if(type(w,id,"task")) { allowed={START,END,STATE,OP,CODE,CAUSE};required={START,END,STATE,OP,CAUSE};ar={SHIP,PERSON};rr=ar; }
  else if(type(w,id,"order")) { allowed={START,END,STATE,D_DOMAIN,CAUSE};required=allowed;ar={SHIP,ISSUER};rr=ar; }
  else if(type(w,id,"mandate")) { allowed={START,END,STATE,D_DOMAIN,CAUSE};required=allowed;ar={SHIP,PERSON};rr=ar; }
  else if(type(w,id,"review")) { allowed={START,END,STATE,VALUE,CAUSE,CODE};required=allowed;ar={SHIP,ISSUER};rr=ar; }
  else if(type(w,id,"event")) { allowed={OP,CODE,CAUSE,TICK};required=allowed;ar={SHIP,PERSON,TARGET};rr={SHIP}; }
  else return false;
  for(const auto& r:w.relations_from(EntityId{id})) {
   const U k=r.kind.value();
   if(k>>48) { const U f=(k>>48)-0xF000;
    if(!allowed.contains(f) || r.target.value()!=id || !fields.insert(f).second) return false;
   } else if(!ar.contains(k) || !refs.insert(k).second) return false;
  }
  for(U f:required) if(!fields.contains(f)) return false;
  for(U r:rr) if(!refs.contains(r)) return false;
  if(refs.contains(SHIP) && ref(w,id,SHIP)!=1) return false;
  if(refs.contains(PERSON) && !type(w,ref(w,id,PERSON),"person")) return false;
  if(refs.contains(ISSUER) && !type(w,ref(w,id,ISSUER),"person")) return false;
  if(refs.contains(SLOT) && !type(w,ref(w,id,SLOT),"slot")) return false;
  if(refs.contains(ORIGIN) && !type(w,ref(w,id,ORIGIN),"appointment")) return false;
  if(refs.contains(ACTIVITY) && !type(w,ref(w,id,ACTIVITY),"activity")) return false;
  if(fields.contains(START) && (val(w,id,START)>=val(w,id,END) || val(w,id,STATE)>DONE)) return false;
  if(type(w,id,"person") && (id<3 || (!general && id>11) || val(w,id,CATEGORY)<1 || val(w,id,CATEGORY)>3 || (!general && val(w,id,DEPT)<1) || val(w,id,DEPT)>(org?7U:4U) || (org?(val(w,id,QUAL)&~QUALIFICATIONS):(val(w,id,QUAL)>30)) || (general && val(w,id,MEMBER)>1))) return false;
  if(type(w,id,"slot") && (val(w,id,QUAL)<1 || val(w,id,QUAL)>(org?30U:4U) || val(w,id,DEPT)<1 || val(w,id,DEPT)>(org?7U:4U) || val(w,id,REQUIRED)>1)) return false;
  if(type(w,id,"activity") && val(w,id,VALUE)!=F04_DUTY && val(w,id,VALUE)!=F04_REST && val(w,id,VALUE)!=F04_ONCALL && val(w,id,VALUE)!=F04_ABSENCE) return false;
  if(type(w,id,"appointment") && (val(w,id,ROLE)<1 || val(w,id,ROLE)>(org?F04_DEPUTY:F04_SUCCESSOR))) return false;
  if(org && type(w,id,"appointment") && (val(w,id,DEPT)<1 || val(w,id,DEPT)>7))return false;
  if(type(w,id,"delegation") && val(w,id,D_DOMAIN)!=F04_POLICY) return false;
  if(type(w,id,"mandate") && (ref(w,id,PERSON)!=10 || val(w,id,D_DOMAIN)!=F04_CONTACT || val(w,id,CAUSE)!=40401))return false;
  if(type(w,id,"order") && !external_authority(w,ref(w,id,ISSUER),val(w,id,D_DOMAIN),val(w,id,START)))return false;
  if(type(w,id,"review") && ((val(w,id,VALUE)&~15ULL) ||
    val(w,id,CODE)!=((val(w,id,VALUE)&7U)==7?F04_OK:F04_REVIEW)))return false;
  if(type(w,id,"task") && val(w,id,OP)!=F04_SCAN && val(w,id,OP)!=F04_POLICY) return false;
  if(type(w,id,"task") && val(w,id,STATE)==ACTIVE && val(w,id,START)<c.time.now())return false;
 }
 if(w.populations().size()!=1 || w.populations()[0]!=PopulationRecord{EntityId{2},initial,0} || w.population_memberships().size()!=initial || !w.knowledge_of(EntityId{1}).empty()) return false;
 for(U p=3;p<initial+3;++p) if(!type(w,p,"person") || w.population_origin(EntityId{p})!=EntityId{2}) return false;
 if(general) {
  U aboard=0;for(U p:all(w,"person"))aboard+=member(w,p)?1:0;
  if(!val(w,1,SHIP_ID) || !initial || initial>8192 || aboard>8192 || val(w,1,MAXIMUM)>8192 || (val(w,1,MAXIMUM) && aboard>val(w,1,MAXIMUM)))return false;
  const Complement* spec=nullptr;for(const auto& s:complements)if(type(w,1,(std::string("class_")+s.id).c_str()))spec=&s;
  if(!spec || val(w,1,NOMINAL_CREW)!=spec->crew || val(w,1,NOMINAL_RESIDENTS)!=spec->residents)return false;
 }
 std::set<U> occupied;
 for(U s:all(w,"slot")) if(const U p=ref(w,s,PERSON)) {
  if(!member(w,p) || val(w,p,CATEGORY)!=1 || !occupied.insert(p).second || val(w,p,DEPT)!=val(w,s,DEPT)) return false;
 }
 for(U a:all(w,"activity")) if(val(w,a,VALUE)==F04_DUTY && !ref(w,a,SLOT)) return false;
 // Validate disjoint intervals within a person/role, not all pairs of the crew.
 std::map<std::pair<U,U>,std::vector<std::pair<U,U>>> intervals;
 for(U a:all(w,"activity"))if(val(w,a,STATE)==ACTIVE && val(w,a,VALUE)!=F04_ONCALL && val(w,a,VALUE)!=F04_ABSENCE)
  intervals[{0,ref(w,a,PERSON)}].push_back({val(w,a,START),val(w,a,END)});
 for(U a:all(w,"appointment"))if(val(w,a,STATE)==ACTIVE)
  intervals[{val(w,a,ROLE),(val(w,a,ROLE)==F04_HEAD || val(w,a,ROLE)==F04_DEPUTY)?val(w,a,DEPT):0}].push_back({val(w,a,START),val(w,a,END)});
 for(U f:all(w,"function"))if(val(w,f,STATE)==ACTIVE)
  intervals[{100+val(w,f,STATIONS),0}].push_back({val(w,f,START),val(w,f,END)});
 for(U f:all(w,"function"))if(val(w,f,STATE)==ACTIVE)
  intervals[{99,ref(w,f,PERSON)}].push_back({val(w,f,START),val(w,f,END)});
 for(auto& entry:intervals) {auto& list=entry.second;std::sort(list.begin(),list.end());
  for(size_t i=1;i<list.size();++i)if(list[i].first<list[i-1].second)return false;
 }
 return organization_schema(w);
}
U perform(Campaign& c,const ContentCatalog& cat,const F04Request& r,bool queued=false) {
 const U p=r.actor.id,t=c.time.now(),target=r.target;
 need(type(c.world,p,"person"),F04_DENIED);
 need(r.cause<=FOREVER && r.start<=FOREVER && r.end<=FOREVER,F04_ARGUMENT);
 if(r.op==F04_PROPOSE) return 0; // Logged suggestion only; grants nothing.
 const bool external=r.op==F04_SUPERIOR || (r.op==F04_REVOKE && type(c.world,target,"order"));
 if(external)need(external_authority(c.world,p,r.op==F04_SUPERIOR?r.value:val(c.world,target,D_DOMAIN),t),F04_DENIED);
 else need(available(c.world,p,t),F04_UNAVAILABLE);
 auto cmd=[&]() { need(commander(c.world,t)==p,F04_DENIED); };
 auto manage=[&](U dept) { need(commander(c.world,t)==p || head(c.world,p,dept,t),F04_SCOPE); };
 auto times=[&]() { need(r.start>=t && r.start<r.end && r.end<=FOREVER); };
 auto person=[&](U who) { need(type(c.world,who,"person") && val(c.world,who,CATEGORY)==1 && member(c.world,who),F04_DENIED); };
 switch(r.op) {
 case F04_INSTALL_TEMPLATE:cmd();need(r.cause);return install_template(c,cat,r);
 case F04_BOOTSTRAP_TEMPLATE:cmd();need(r.cause);return bootstrap_template(c,cat,r);
 case F04_CREDENTIAL: {
  cmd();person(target);need(organization(c.world) && r.cause && r.end>t && r.aux && !(r.aux&~QUALIFICATIONS));
  set(c,target,QUAL,r.aux);set(c,target,UNTIL,r.end);return target;
 }
 case F04_TRANSFER: {
  cmd();person(r.aux);need(organization(c.world) && type(c.world,target,"slot") && r.cause);
  need(!ref(c.world,target,PERSON) || ref(c.world,target,PERSON)==r.aux,F04_OVERLAP);
  need(slot_qualified(c.world,r.aux,target,t),F04_QUALIFICATION);need(available(c.world,r.aux,t),F04_UNAVAILABLE);
  if(ref(c.world,target,PERSON)==r.aux)return target;
  cancel_post(c,r.aux);
  for(U a:all(c.world,"appointment"))if(ref(c.world,a,PERSON)==r.aux &&
    (val(c.world,a,ROLE)==F04_HEAD || val(c.world,a,ROLE)==F04_DEPUTY || val(c.world,a,ROLE)==F04_DOCTOR))set(c,a,STATE,CANCELLED);
  set(c,r.aux,DEPT,val(c.world,target,DEPT));link(c,target,PERSON,r.aux);return target;
 }
 case F04_FUNCTION: {
  person(target);need(organization(c.world) && type(c.world,r.aux,"slot"));manage(val(c.world,r.aux,DEPT));times();need(r.cause);
  need(r.value && !(r.value&(r.value-1)) && (val(c.world,r.aux,STATIONS)&r.value),F04_SCOPE);
  need(duty(c.world,target,r.aux,r.start) && duty(c.world,target,r.aux,r.end-1),F04_UNAVAILABLE);
  if(r.value==F04_ST_TACTICAL)need(qualified(c.world,target,F04_Q_TACTICAL,r.end-1),F04_QUALIFICATION);
  // Every boundary is checked; endpoints alone can hide an absence inside.
  for(const char* kind:{"activity","appointment"})for(U a:all(c.world,kind))for(U b:{val(c.world,a,START),val(c.world,a,END)})
   if(r.start<b && b<r.end)need(duty(c.world,target,r.aux,b),F04_UNAVAILABLE);
  for(U f:all(c.world,"function"))if(val(c.world,f,STATE)==ACTIVE && (val(c.world,f,STATIONS)==r.value || ref(c.world,f,PERSON)==target))
   need(!overlaps(r.start,r.end,val(c.world,f,START),val(c.world,f,END)),F04_OVERLAP);
  U f=make(c,cat,"function");link(c,f,SHIP,1);link(c,f,PERSON,target);link(c,f,SLOT,r.aux);link(c,f,ISSUER,p);
  temporal(c,f,r.start,r.end);set(c,f,STATIONS,r.value);set(c,f,CAUSE,r.cause);return f;
 }
 case F04_PLAN_ALPHA: {
  cmd();times();need(organization(c.world) && r.cause && r.aux<=1 && r.start%86400==28800 && r.end==r.start+28800 && val(c.world,1,PATTERN)==3);
  need(!val(c.world,1,ALPHA_END) || r.start>=val(c.world,1,ALPHA_END),F04_OVERLAP);
  U first=0,watch=0,security=0,security_slot=0;
  for(U slot:all(c.world,"slot"))if(val(c.world,slot,ALPHA)) {
   U who=ref(c.world,slot,PERSON);if(!who)continue;
   F04Request q=r;q.op=F04_DUTY;q.target=who;q.aux=slot;
   try {perform(c,cat,q); }catch(const Denial&){continue;}
   const U responsibility=val(c.world,slot,RESPONSIBILITY);
   if(responsibility==F04_FIRST)first=who;
   if(!responsibility && val(c.world,slot,QUAL)==F04_COMMAND && !watch)watch=who;
   if(responsibility==F04_HEAD && val(c.world,slot,DEPT)==F04_SECURITY && (val(c.world,slot,STATIONS)&F04_ST_TACTICAL)){security=who;security_slot=slot;}
  }
  U bridge_watch=r.aux && first?first:watch;
  if(bridge_watch){F04Request q=r;q.op=F04_APPOINT;q.target=bridge_watch;q.value=F04_WATCH;q.aux=F04_COMMAND;perform(c,cat,q);}
  if(security){F04Request q=r;q.op=F04_FUNCTION;q.target=security;q.aux=security_slot;q.value=F04_ST_TACTICAL;perform(c,cat,q);}
  set(c,1,ALPHA_START,r.start);set(c,1,ALPHA_END,r.end);return 1;
 }
 case F04_CREATE_SLOT: {
  cmd();need(val(c.world,1,SCHEMA)==2 && r.value>=1 && r.value<=4 && r.cause);
  U id=make(c,cat,"slot");link(c,id,SHIP,1);set(c,id,DEPT,r.value);set(c,id,QUAL,r.value);set(c,id,REQUIRED,1);return id;
 }
 case F04_EMBARK: {
  cmd();need(val(c.world,1,SCHEMA)>=2);need(r.cause && r.value>=1 && r.value<=3 && r.aux<=(organization(c.world)?7U:4U));
  U count=0;for(U id:all(c.world,"person"))count+=member(c.world,id)?1:0;
  const U max=val(c.world,1,MAXIMUM);need(count<8192 && (!max || count<max),F04_CAPACITY);
  if(target){need(type(c.world,target,"person") && !member(c.world,target),F04_OVERLAP);set(c,target,MEMBER,1);set(c,target,CATEGORY,r.value);action(c,target,PlaceEntityAction{EntityId{target},EntityId{1}});return target;}
  const U id=make(c,cat,"person");link(c,id,SHIP,1);set(c,id,MEMBER,1);set(c,id,CATEGORY,r.value);set(c,id,RANK,0);set(c,id,DEPT,r.aux);set(c,id,QUAL,0);set(c,id,UNTIL,FOREVER);
  action(c,id,PlaceEntityAction{EntityId{id},EntityId{1}});return id;
 }
 case F04_DEPART: {
  cmd();need(val(c.world,1,SCHEMA)>=2 && type(c.world,target,"person") && member(c.world,target));need(r.cause);
  for(U slot:all(c.world,"slot"))if(ref(c.world,slot,PERSON)==target)link(c,slot,PERSON,0);
  for(const char* kind:{"activity","appointment","delegation","task","mandate","order","review","function"})for(U id:all(c.world,kind))
   if(ref(c.world,id,PERSON)==target || ref(c.world,id,ISSUER)==target)set(c,id,STATE,CANCELLED);
  set(c,target,MEMBER,0);action(c,target,RemoveContainmentAction{EntityId{target}});return target;
 }
 case F04_ASSIGN: {
  need(type(c.world,target,"slot"));manage(val(c.world,target,DEPT));
  if(r.aux) {
   person(r.aux);need(val(c.world,r.aux,DEPT)==val(c.world,target,DEPT),F04_SCOPE);
   need(slot_qualified(c.world,r.aux,target,t),F04_QUALIFICATION);
   need(available(c.world,r.aux,t),F04_UNAVAILABLE);
   for(U s:all(c.world,"slot")) need(s==target || ref(c.world,s,PERSON)!=r.aux,F04_OVERLAP);
  }
  if(organization(c.world) && ref(c.world,target,PERSON) && ref(c.world,target,PERSON)!=r.aux)cancel_post(c,ref(c.world,target,PERSON));
  link(c,target,PERSON,r.aux);return target;
 }
 case F04_DUTY: case F04_REST: case F04_ONCALL: case F04_ABSENCE: {
  person(target);manage(val(c.world,target,DEPT));times();need(r.cause!=0);
  if(r.op==F04_ABSENCE) need(r.value>=F04_LEAVE && r.value<=F04_SUSPENDED);
  if(r.op==F04_DUTY) {
   need(type(c.world,r.aux,"slot") && ref(c.world,r.aux,PERSON)==target,F04_VACANT);
   need(slot_qualified(c.world,target,r.aux,r.end-1),F04_QUALIFICATION);
   const U role=val(c.world,r.aux,RESPONSIBILITY);
   if(role)need(active_role(c.world,target,role,r.start,val(c.world,r.aux,DEPT)) && active_role(c.world,target,role,r.end-1,val(c.world,r.aux,DEPT)),F04_DENIED);
   need(available(c.world,target,r.start),F04_UNAVAILABLE);
  }
  for(U a:all(c.world,"activity")) if(ref(c.world,a,PERSON)==target && val(c.world,a,STATE)==ACTIVE &&
    overlaps(r.start,r.end,val(c.world,a,START),val(c.world,a,END))) {
   // Recorded absence can invalidate an existing watch; it must expose a vacancy.
   if(r.op==F04_ABSENCE || val(c.world,a,VALUE)==F04_ONCALL || r.op==F04_ONCALL) continue;
   need(false,F04_OVERLAP);
  }
  U a=make(c,cat,"activity");link(c,a,SHIP,1);link(c,a,PERSON,target);link(c,a,ISSUER,p);
  if(r.op==F04_DUTY) link(c,a,SLOT,r.aux);
  temporal(c,a,r.start,r.end);set(c,a,VALUE,r.op);set(c,a,CAUSE,r.cause);
  if(r.op==F04_ABSENCE)set(c,a,CODE,r.value);
  return a;
 }
 case F04_RELIEF: {
  need(type(c.world,target,"activity") && val(c.world,target,VALUE)==F04_DUTY && window(c.world,target,t));
  const U slot=ref(c.world,target,SLOT);manage(val(c.world,slot,DEPT));person(r.aux);
  need(r.cause!=0);need(slot_qualified(c.world,r.aux,slot,val(c.world,target,END)-1),F04_QUALIFICATION);
  const U role=val(c.world,slot,RESPONSIBILITY);if(role)need(active_role(c.world,r.aux,role,t,val(c.world,slot,DEPT)) && active_role(c.world,r.aux,role,val(c.world,target,END)-1,val(c.world,slot,DEPT)),F04_DENIED);
  need(val(c.world,r.aux,DEPT)==val(c.world,slot,DEPT),F04_SCOPE);
  need(available(c.world,r.aux,t),F04_UNAVAILABLE);
  for(U s:all(c.world,"slot"))need(s==slot || ref(c.world,s,PERSON)!=r.aux,F04_OVERLAP);
  for(U a:all(c.world,"activity")) if(ref(c.world,a,PERSON)==r.aux && val(c.world,a,STATE)==ACTIVE && val(c.world,a,VALUE)!=F04_ONCALL)
   need(!overlaps(t,val(c.world,target,END),val(c.world,a,START),val(c.world,a,END)),F04_OVERLAP);
  U a=make(c,cat,"activity");link(c,a,SHIP,1);link(c,a,PERSON,r.aux);link(c,a,SLOT,slot);link(c,a,ISSUER,p);link(c,a,ACTIVITY,target);
  temporal(c,a,t,val(c.world,target,END));set(c,a,VALUE,F04_DUTY);set(c,a,CAUSE,r.cause);
  if(organization(c.world)) {
   for(U f:all(c.world,"function"))if(ref(c.world,f,SLOT)==slot && val(c.world,f,STATE)==ACTIVE)set(c,f,STATE,CANCELLED);
   action(c,ref(c.world,slot,PERSON),PlaceEntityAction{EntityId{ref(c.world,slot,PERSON)},EntityId{1}});
  }
  set(c,target,STATE,CANCELLED);link(c,slot,PERSON,r.aux);return a;
 }
 case F04_APPOINT: {
  cmd();person(target);times();need(r.cause && r.value>=F04_CAPTAIN && r.value<=static_cast<uint32_t>(organization(c.world)?F04_DEPUTY:F04_SUCCESSOR));
  const bool departmental=r.value==F04_HEAD || r.value==F04_DEPUTY;
  if(departmental && organization(c.world))need(r.aux>=1 && r.aux<=7);
  const U q=r.value==F04_DOCTOR?F04_MEDICINE:departmental?r.aux:F04_COMMAND;
  need(qualified(c.world,target,q,r.end-1),F04_QUALIFICATION);
  for(U a:all(c.world,"appointment")) if(val(c.world,a,ROLE)==r.value && (!departmental || val(c.world,a,DEPT)==r.aux) && val(c.world,a,STATE)==ACTIVE)
   need(!overlaps(r.start,r.end,val(c.world,a,START),val(c.world,a,END)),F04_OVERLAP);
  return appointment(c,cat,target,r.value,organization(c.world) && !departmental?q:r.aux,r.start,r.end,p,r.cause);
 }
 case F04_DELEGATE: {
  cmd();person(target);times();need(r.value==F04_POLICY && r.cause);
  need(qualified(c.world,target,F04_COMMAND,r.end-1),F04_QUALIFICATION);
  U origin=0;for(U a:all(c.world,"appointment")) if(ref(c.world,a,PERSON)==p && window(c.world,a,t) &&
   (val(c.world,a,ROLE)==F04_CAPTAIN || val(c.world,a,ROLE)>=F04_FIRST) && r.end<=val(c.world,a,END)) {origin=a;break;}
  need(origin,F04_EXPIRED);const U d=make(c,cat,"delegation");link(c,d,SHIP,1);link(c,d,PERSON,target);link(c,d,ISSUER,p);link(c,d,ORIGIN,origin);
  temporal(c,d,r.start,r.end);set(c,d,D_DOMAIN,r.value);set(c,d,CAUSE,r.cause);return d;
 }
 case F04_REVOKE: {
  need(type(c.world,target,"appointment") || type(c.world,target,"delegation") || type(c.world,target,"order") || (organization(c.world) && type(c.world,target,"function")));
  if(type(c.world,target,"order"))need(ref(c.world,target,ISSUER)==p,F04_DENIED);else cmd();need(r.cause);
  set(c,target,STATE,CANCELLED);return target;
 }
 case F04_MEDICAL: {
  need(active_role(c.world,p,F04_DOCTOR,t) && qualified(c.world,p,F04_MEDICINE,t),F04_QUALIFICATION);
  person(target);times();need(r.cause && r.value==F04_SICK,F04_REVIEW);
  const U a=make(c,cat,"activity");link(c,a,SHIP,1);link(c,a,PERSON,target);link(c,a,ISSUER,p);
  temporal(c,a,r.start,r.end);set(c,a,VALUE,F04_ABSENCE);set(c,a,CAUSE,r.cause);set(c,a,CODE,F04_SICK);
  event(c,cat,p,F04_MEDICAL,F04_OK,r.cause,commander(c.world,t));return a;
 }
 case F04_POLICY: {
  need(command_authority(c.world,p,F04_POLICY,t),F04_DENIED);need(r.value==3 || r.value==4);
  if(organization(c.world)) {
   std::set<U> boundaries{t};
   for(const char* kind:{"activity","appointment"})for(U a:all(c.world,kind))
    for(U b:{val(c.world,a,START),val(c.world,a,END)})if(t<b && b<t+86400)boundaries.insert(b);
   for(U person_id:all(c.world,"person"))if(t<val(c.world,person_id,UNTIL) && val(c.world,person_id,UNTIL)<t+86400)boundaries.insert(val(c.world,person_id,UNTIL));
   for(U b:boundaries)for(U station:trek_templates::profile(val(c.world,1,TEMPLATE))->continuous_stations)need(service_covered(c.world,station,b),F04_VACANT);
  }
  // Pattern changes require coverage through an entire cycle, including future absences.
  for(U slot:all(c.world,"slot")) if(val(c.world,slot,REQUIRED)) {
   std::vector<U> boundaries{t,t+86400};
   for(U a:all(c.world,"activity")) for(U b:{val(c.world,a,START),val(c.world,a,END)}) if(t<b && b<t+86400)boundaries.push_back(b);
   for(U b:boundaries) if(b<t+86400) need(duty(c.world,ref(c.world,slot,PERSON),slot,b),F04_VACANT);
  }
  for(U o:all(c.world,"order")) if(window(c.world,o,t) && val(c.world,o,D_DOMAIN)==F04_POLICY) need(false,F04_REVIEW);
  set(c,1,PATTERN,r.value);return 1;
 }
 case F04_SCAN: {
  U slot=val(c.world,1,SCHEMA)==1?12:0;
  if(!slot)for(U id:all(c.world,"slot"))if(ref(c.world,id,PERSON)==p && val(c.world,id,QUAL)==F04_SENSORS){slot=id;break;}
  need(qualified(c.world,p,F04_SENSORS,t),F04_QUALIFICATION);
  need(duty(c.world,p,slot,t),F04_DENIED);
  need(c.world.container_of(EntityId{p}).container==EntityId{slot},F04_UNAVAILABLE);
  // A real authoritative consequence, separate from the illustrative F06 sensor model.
  action(c,p,StreamRollAction{0xF0401,1,100});return 0;
 }
 case F04_MOVE: {
  need(type(c.world,target,"slot") && duty(c.world,p,target,t),F04_DENIED);
  action(c,p,PlaceEntityAction{EntityId{p},EntityId{target}});return target;
 }
 case F04_BRIDGE: {
  need(commander(c.world,t)==p || (active_role(c.world,p,F04_WATCH,t) && qualified(c.world,p,F04_COMMAND,t)),F04_DENIED);
  need(r.value<=3);set(c,1,ALERT,r.value?r.value:1);return 1;
 }
 case F04_IMPOSSIBLE: cmd();need(false,F04_SAFETY);return 0;
 case F04_CONTACT: {
  cmd(); // A persisted scoped review, never a caller-supplied 'authorized' boolean.
  need(type(c.world,target,"review") && window(c.world,target,t) && val(c.world,target,CODE)==F04_OK,F04_REVIEW);
  need(ref(c.world,target,ISSUER)==p,F04_REVIEW);
  for(U o:all(c.world,"order")) if(window(c.world,o,t) && val(c.world,o,D_DOMAIN)==F04_CONTACT)need(false,F04_REVIEW);
  return 0;
 }
 case F04_CONTACT_REVIEW: {
  cmd();times();need(r.cause,F04_REVIEW);need((r.value&~15U)==0);
  // Known context + interference assessment + explicit mission review are required.
  // Risk bit 8 is recorded for consequences; it is not a universal automatic ban.
  const U review=make(c,cat,"review");link(c,review,SHIP,1);link(c,review,ISSUER,p);temporal(c,review,r.start,r.end);
  set(c,review,VALUE,r.value);set(c,review,CAUSE,r.cause);set(c,review,CODE,(r.value&7U)==7?F04_OK:F04_REVIEW);return review;
 }
 case F04_SUPERIOR: {
  times();need(r.cause); // external_authority above checks domain and current mandate.
  bool bounded=false;for(U a:all(c.world,"mandate"))if(ref(c.world,a,PERSON)==p && val(c.world,a,D_DOMAIN)==r.value && window(c.world,a,t) && r.end<=val(c.world,a,END))bounded=true;
  need(bounded,F04_SCOPE);
  const U o=make(c,cat,"order");link(c,o,SHIP,1);link(c,o,ISSUER,p);temporal(c,o,r.start,r.end);set(c,o,D_DOMAIN,r.value);set(c,o,CAUSE,r.cause);return o;
 }
 case F04_QUEUE: {
  need(!queued && (r.value==F04_SCAN || r.value==F04_POLICY));times();need(r.cause);
  F04Request check=r;check.op=r.value;check.value=static_cast<uint32_t>(r.aux);
  // Validate now on a disposable campaign. Execution still revalidates later.
  Campaign probe=c;perform(probe,cat,check,true);
  const U a=make(c,cat,"task");link(c,a,SHIP,1);link(c,a,PERSON,p);temporal(c,a,r.start,r.end);set(c,a,OP,r.value);set(c,a,CAUSE,r.cause);
  if(r.value==F04_POLICY) need(false,F04_ARGUMENT); // Reserved for future parameterized queue.
  return a;
 }
 case F04_RECALL: {
  cmd();need(type(c.world,target,"activity") && val(c.world,target,VALUE)==F04_REST && window(c.world,target,t));
  need(r.cause && r.value>0,F04_REVIEW);set(c,target,STATE,CANCELLED);set(c,target,DEBT,r.value);return target;
 }
 default:need(false,F04_ARGUMENT);return 0;
 }
}
std::atomic<U> scopes{1};
}
struct F04Session {
 const std::thread::id owner{std::this_thread::get_id()};
 CatalogBuildResult content{catalog()};std::unique_ptr<Campaign> c{std::make_unique<Campaign>()};U scope{scopes.fetch_add(1)};
 explicit F04Session(const char* cls) {need(content.succeeded(),F04_INTERNAL);initialize(*c,*content.catalog(),cls);need(schema(*c),F04_INTERNAL);}
 F04Session(const char* cls,const F04PopulationConfig& config) {need(content.succeeded(),F04_INTERNAL);initialize_population(*c,*content.catalog(),cls,config);need(schema(*c),F04_INTERNAL);}
 U index_revision=UINT64_MAX;std::vector<U> people,activities;std::unordered_map<U,std::vector<U>> person_activities;
 void index() { if(index_revision==c->world.revision())return;people.clear();activities.clear();
  for(U p:all(c->world,"person"))if(member(c->world,p))people.push_back(p);
  activities=all(c->world,"activity");person_activities.clear();for(U a:activities)person_activities[ref(c->world,a,PERSON)].push_back(a);index_revision=c->world.revision();
 }
};
namespace {
uint32_t guard(F04Session* s) {return !s?F04_ARGUMENT:s->owner!=std::this_thread::get_id()?F04_THREAD:F04_OK;}
template<class F> uint32_t call(F04Session* s,F&& f) noexcept {
 if(auto r=guard(s);r)return r;
 try{return f();}catch(const Denial& e){return e.code;}catch(...){return F04_INTERNAL;}
}
bool observer(F04Session* s,F04Ref p) { return p.scope==s->scope && type(s->c->world,p.id,"person") && member(s->c->world,p.id) && val(s->c->world,p.id,CATEGORY)==1; }
}
const char* f04_core_sha() {return F04_CORE_SHA;}
uint32_t f04_create(uint32_t abi,const char* cls,F04Session** out) {
 if(!out)return F04_ARGUMENT;*out=nullptr;if(abi!=1 || !cls)return F04_ARGUMENT;
 try{*out=new F04Session(cls);return F04_OK;}catch(const Denial& e){return e.code;}catch(...){return F04_INTERNAL;}
}
uint32_t f04_destroy(F04Session* s) {if(auto r=guard(s);r)return r;delete s;return F04_OK;}
uint32_t f04_create_population(uint32_t abi,const char* cls,const F04PopulationConfig* config,F04Session** out) {
 if(!out)return F04_ARGUMENT;*out=nullptr;if(abi!=1 || !cls || !config)return F04_ARGUMENT;
 try{*out=new F04Session(cls,*config);return F04_OK;}catch(const Denial& e){return e.code;}catch(...){return F04_INTERNAL;}
}
uint32_t f04_handles(F04Session* s,F04Handles* out) {
 if(!out)return F04_ARGUMENT;
 return call(s,[&]() -> uint32_t {auto h=[&](U id){return F04Ref{s->scope,id};};if(val(s->c->world,1,SCHEMA)>=2){*out={};out->ship=h(1);out->captain=h(commander(s->c->world,s->c->time.now()));return F04_OK;}*out={h(1),h(3),h(4),h(5),h(6),h(7),h(8),h(9),h(10),h(10),12,13,14};return F04_OK;});
}
uint32_t f04_stats(F04Session* s,F04Stats* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]() -> uint32_t {const auto& c=*s->c;out->entities=c.world.entity_count();out->revision=c.world.revision();out->now=c.time.now();
  for(U p:all(c.world,"person")) if(member(c.world,p)) {const U k=val(c.world,p,CATEGORY);if(k==1)++out->crew;else if(k==2)++out->civilians;else ++out->passengers;}
  for(U a:all(c.world,"slot")){++out->slots;if(!duty(c.world,ref(c.world,a,PERSON),a,c.time.now()))++out->vacancies;}
  for(U a:all(c.world,"task"))if(val(c.world,a,STATE)==ACTIVE)++out->pending;
  out->events=all(c.world,"event").size();out->commander=commander(c.world,c.time.now());out->pattern=val(c.world,1,PATTERN);out->alert=val(c.world,1,ALERT);return F04_OK;
 });
}
uint32_t f04_execute(F04Session* s,const F04Request* r,F04Result* out) {
 if(!r || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]() -> uint32_t {
  need(r->actor.scope==s->scope,F04_SCOPE);
  auto next=std::make_unique<Campaign>(*s->c);uint32_t code=F04_OK;U record=0;
  try {need(r->revision==s->c->world.revision(),F04_STALE);record=perform(*next,*s->content.catalog(),*r);}
  catch(const Denial& e) {code=e.code;next=std::make_unique<Campaign>(*s->c);}
  const U audit=event(*next,*s->content.catalog(),r->actor.id,r->op,code,r->cause<=FOREVER?r->cause:0,r->target);
  const U previous=commander(s->c->world,s->c->time.now()),current=commander(next->world,next->time.now());
  if(previous!=current)event(*next,*s->content.catalog(),previous,100,F04_OK,r->cause,current);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);*out={code,0,record?record:audit,s->c->world.revision()};return code;
 });
}
uint32_t f04_advance(F04Session* s,U horizon,U budget,U* processed) {
 if(!processed)return F04_ARGUMENT;*processed=0;
 return call(s,[&]() -> uint32_t {
  need(horizon>=s->c->time.now() && horizon<=FOREVER && budget<=4096);
  auto next=std::make_unique<Campaign>(*s->c);U done=0;
  std::vector<U> tasks;for(U a:all(next->world,"task"))if(val(next->world,a,STATE)==ACTIVE && val(next->world,a,START)<=horizon)tasks.push_back(a);
  std::sort(tasks.begin(),tasks.end(),[&](U a,U b){return std::pair(val(next->world,a,START),a)<std::pair(val(next->world,b,START),b);});
  auto clock_to=[&](U until) {
   std::set<U> boundaries{until};
   for(const char* kind:{"activity","appointment","delegation","order","mandate","review"}) for(U a:all(next->world,kind))
    for(U b:{val(next->world,a,START),val(next->world,a,END)}) if(next->time.now()<b && b<=until)boundaries.insert(b);
   for(U b:boundaries) {
    const U before=commander(next->world,next->time.now());
    need(next->time.advance(next->world,next->random,b).status==TimelineStatus::completed,F04_INTERNAL);
    const U after=commander(next->world,b);
    if(before!=after) {
     U cause=0;for(U a:all(next->world,"activity")) if(val(next->world,a,START)==b || val(next->world,a,END)==b) {cause=val(next->world,a,CAUSE);break;}
     event(*next,*s->content.catalog(),before,100,F04_OK,cause,after);
    }
   }
  };
  for(U a:tasks) {
   if(done==budget)break;
   const U due=val(next->world,a,START);clock_to(due);
   F04Request r{{s->scope,ref(next->world,a,PERSON)},next->world.revision(),static_cast<uint32_t>(val(next->world,a,OP)),0,0,0,0,0,val(next->world,a,CAUSE)};
   uint32_t code=F04_OK;auto attempt=std::make_unique<Campaign>(*next);
   try {need(due<val(next->world,a,END),F04_EXPIRED);perform(*attempt,*s->content.catalog(),r,true);}
   catch(const Denial& e){code=e.code;attempt=std::make_unique<Campaign>(*next);}
   set(*attempt,a,STATE,DONE);set(*attempt,a,CODE,code);event(*attempt,*s->content.catalog(),r.actor.id,r.op,code,r.cause,a);next.swap(attempt);++done;
  }
  const bool more=tasks.size()>done;
  if(!more)clock_to(horizon);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);*processed=done;return more?F04_CAPACITY:F04_OK;
 });
}
uint32_t f04_manifest(F04Session* s,F04Ref who,F04Person* out,U capacity,U* count) {
 if(!count || (!out && capacity))return F04_ARGUMENT;*count=0;
 return call(s,[&]() -> uint32_t {need(observer(s,who),F04_DENIED);s->index();*count=s->people.size();need(capacity>=*count,F04_CAPACITY);
  U written=0,total=0;return f04_manifest_page(s,who,0,out,capacity,&written,&total);});
}
namespace {
F04Person person_view(F04Session* s,U p) {
 const auto& c=*s->c;const auto& w=c.world;bool on=false,localized=false,free=member(w,p) && val(w,p,CATEGORY)==1;
 const auto found=s->person_activities.find(p);
 if(found!=s->person_activities.end())for(U a:found->second)if(window(w,a,c.time.now())) {
  const U kind=val(w,a,VALUE);if(kind==F04_ABSENCE || kind==F04_REST)free=false;
  if(kind==F04_DUTY && duty(w,p,ref(w,a,SLOT),c.time.now()))on=true;
  localized|=kind==F04_ONCALL;
 }
 return {p,val(w,p,CATEGORY),val(w,p,RANK),val(w,p,DEPT),free?1U:0U,on&&free?1U:0U,localized?1U:0U,type(w,w.container_of(EntityId{p}).container.value(),"slot")?1U:0U};
}
}
uint32_t f04_manifest_page(F04Session* s,F04Ref who,U offset,F04Person* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {need(observer(s,who),F04_DENIED);s->index();*total=s->people.size();
  need(offset<=*total);*written=std::min(capacity,*total-offset);
  for(U i=0;i<*written;++i)out[i]=person_view(s,s->people[static_cast<size_t>(offset+i)]);return F04_OK;});
}
uint32_t f04_person(F04Session* s,F04Ref who,U p,F04Person* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t{need(observer(s,who),F04_DENIED);
  need(type(s->c->world,p,"person") && member(s->c->world,p),F04_SCOPE);s->index();*out=person_view(s,p);return F04_OK;});
}
uint32_t f04_population_stats(F04Session* s,F04PopulationStats* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {const auto& w=s->c->world;need(val(w,1,SCHEMA)>=2);
  out->ship_identity=val(w,1,SHIP_ID);out->nominal_crew=val(w,1,NOMINAL_CREW);out->nominal_residents=val(w,1,NOMINAL_RESIDENTS);out->maximum=val(w,1,MAXIMUM);s->index();
  for(U p:all(w,"person")){if(!member(w,p)){++out->departed;continue;}U cat=val(w,p,CATEGORY);
   if(cat==1){++out->assigned;bool absent=false;const auto found=s->person_activities.find(p);if(found!=s->person_activities.end())for(U a:found->second)if(window(w,a,s->c->time.now()) && val(w,a,VALUE)==F04_ABSENCE)absent=true;if(!absent)++out->present;}
   else if(cat==2)++out->residents;else ++out->passengers;}
  out->nominal_vacancies=out->nominal_crew>out->assigned?out->nominal_crew-out->assigned:0;return F04_OK;});
}
uint32_t f04_slots(F04Session* s,F04Ref who,F04Slot* out,U capacity,U* count) {
 if(!count || (!out && capacity))return F04_ARGUMENT;*count=0;
 return call(s,[&]() -> uint32_t {need(observer(s,who),F04_DENIED);const auto& c=*s->c;const auto slots=all(c.world,"slot");*count=slots.size();need(capacity>=*count,F04_CAPACITY);
  for(size_t i=0;i<slots.size();++i){U a=slots[i],p=ref(c.world,a,PERSON);out[i]={a,p,val(c.world,a,DEPT),val(c.world,a,QUAL),static_cast<uint32_t>(val(c.world,a,REQUIRED)),duty(c.world,p,a,c.time.now())?1U:0U,duty(c.world,who.id,a,c.time.now())?1U:0U,0};}return F04_OK;});
}
uint32_t f04_save(F04Session* s,uint8_t* out,U capacity,U* size) {
 if(!size || (!out && capacity))return F04_ARGUMENT;*size=0;
 return call(s,[&]() -> uint32_t {const auto& c=*s->c;const auto saved=CampaignPersistence::serialize(CampaignPersistence::capture(c.world,c.random,c.time));need(saved.status==CampaignArchiveStatus::success,F04_SAVE);*size=saved.bytes.size();need(capacity>=*size,F04_CAPACITY);std::memcpy(out,saved.bytes.data(),saved.bytes.size());return F04_OK;});
}
uint32_t f04_watch_window(F04Session* s,U tick,F04WatchWindow* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]() -> uint32_t {
  need(tick<=FOREVER-86400);const U count=val(s->c->world,1,PATTERN),duration=86400/count;
  const U day=tick/86400*86400,index=(tick%86400)/duration;
  *out={day+index*duration,day+(index+1)*duration,static_cast<uint32_t>(count),static_cast<uint32_t>((index+count-1)%count)};
  return F04_OK;
 });
}
uint32_t f04_load(F04Session* s,const uint8_t* bytes,U size) {
 if(!bytes || !size || size>64ULL*1024*1024)return F04_ARGUMENT;
 return call(s,[&]() -> uint32_t {auto next=std::make_unique<Campaign>();need(CampaignPersistence::load({bytes,static_cast<size_t>(size)},next->world,next->random,next->time,{},s->content.catalog())==CampaignArchiveStatus::success,F04_SAVE);need(schema(*next),F04_SAVE);s->c.swap(next);s->scope=scopes.fetch_add(1);s->index_revision=UINT64_MAX;return F04_OK;});
}
uint32_t f04_template_spec(U id,F04TemplateSpec* out) {
 if(!out)return F04_ARGUMENT;*out={};const auto* definition=trek_templates::find(id);if(!definition)return F04_ARGUMENT;
 *out=*definition;return F04_OK;
}
uint32_t f04_template_sections(U id,F04SectionSpec* out,U capacity,U* count) {
 if(!count || (!out && capacity))return F04_ARGUMENT;*count=0;const auto* definition=trek_templates::profile(id);if(!definition)return F04_ARGUMENT;
 *count=definition->sections.size();if(capacity<*count)return F04_CAPACITY;
 std::copy(definition->sections.begin(),definition->sections.end(),out);return F04_OK;
}
uint32_t f04_positions_page(F04Session* s,F04Ref who,U offset,F04Position* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;need(organization(w));
  auto slots=all(w,"slot");*total=slots.size();need(offset<=*total);*written=std::min(capacity,*total-offset);
  for(U i=0;i<*written;++i) {
   const U slot=slots[static_cast<size_t>(offset+i)],p=ref(w,slot,PERSON);bool stationed=false;U duty_record=0;
   for(U a:all(w,"activity"))if(ref(w,a,PERSON)==p && ref(w,a,SLOT)==slot && val(w,a,VALUE)==F04_DUTY && window(w,a,s->c->time.now()))duty_record=a;
   for(U f:all(w,"function"))if(ref(w,f,SLOT)==slot && station_active(w,f,s->c->time.now()))stationed=true;
   out[i]={slot,val(w,slot,STABLE_ID),val(w,slot,DEPT),val(w,ref(w,slot,SECTION),SECTION_KEY),val(w,slot,ORDINAL),p,
    val(w,slot,QUAL),val(w,slot,QUAL_MASK),val(w,slot,RESPONSIBILITY),val(w,slot,STATIONS),val(w,slot,COVERAGE),val(w,slot,ALPHA),duty_record,
    duty(w,p,slot,s->c->time.now())?1U:0U,stationed?1U:0U};
  }
  return F04_OK;
 });
}
uint32_t f04_person_credentials(F04Session* s,F04Ref who,U person,U* mask,U* expiry) {
 if(!mask || !expiry)return F04_ARGUMENT;*mask=*expiry=0;
 return call(s,[&]()->uint32_t {need(observer(s,who),F04_DENIED);const auto& w=s->c->world;
  need(type(w,person,"person") && member(w,person),F04_SCOPE);*mask=val(w,person,QUAL);*expiry=val(w,person,UNTIL);return F04_OK;});
}
uint32_t f04_functions(F04Session* s,F04Ref who,F04FunctionView* out,U capacity,U* count) {
 if(!count || (!out && capacity))return F04_ARGUMENT;*count=0;
 return call(s,[&]()->uint32_t {need(observer(s,who),F04_DENIED);const auto& w=s->c->world;need(organization(w));
  auto functions=all(w,"function");*count=functions.size();need(capacity>=*count,F04_CAPACITY);
  for(size_t i=0;i<functions.size();++i){U f=functions[i];out[i]={ref(w,f,PERSON),ref(w,f,SLOT),val(w,f,STATIONS),val(w,f,START),val(w,f,END),station_active(w,f,s->c->time.now())?1U:0U,0};}return F04_OK;});
}
uint32_t f04_organization_stats(F04Session* s,F04Ref who,F04OrganizationStats* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {need(observer(s,who),F04_DENIED);const auto& w=s->c->world;const U tick=s->c->time.now();need(organization(w));
  out->template_id=val(w,1,TEMPLATE);out->departments=all(w,"department").size();out->sections=all(w,"section").size();
  for(U slot:all(w,"slot")) {
   ++out->positions;const U p=ref(w,slot,PERSON);if(p)++out->assigned;else ++out->vacant;
   const bool on=duty(w,p,slot,tick);out->on_duty+=on;
   if(val(w,slot,ALPHA)){++out->alpha_expected;out->alpha_present+=on;}
   out->continuous_candidates+=val(w,slot,COVERAGE)==F04_CONTINUOUS_CANDIDATE;
   if(val(w,slot,DEPT)==F04_MEDICINE && on)out->urgent_response=1;
  }
  if(!out->urgent_response)for(U a:all(w,"activity"))if(val(w,a,VALUE)==F04_ONCALL && window(w,a,tick)) {
   U p=ref(w,a,PERSON);if(val(w,p,DEPT)==F04_MEDICINE && available(w,p,tick) &&
    (qualified(w,p,F04_MEDICINE,tick) || qualified(w,p,F04_Q_CLINICAL,tick)))out->urgent_response=2;
  }
  out->alpha_deficit=out->alpha_expected-out->alpha_present;
  const auto stations=trek_templates::profile(val(w,1,TEMPLATE))->continuous_stations;
  out->continuous_required=stations.size();for(U station:stations)out->continuous_covered+=service_covered(w,station,tick);
  return F04_OK;
 });
}
