// Reusable deterministic 3x8 planning. Only Core entities/relations persist.
struct Span {U start,end;};
struct PlannerPerson {
 U id,slot,department,section,ordinal,role,mask,expiry,stations;
 std::vector<Span> work,blocked;bool debt=false;
};
bool ordinary_fits(const PlannerPerson& p,U start,U end) {
 if(p.debt || start>=end || end-start>28800 || end>p.expiry)return false;
 for(const auto& b:p.blocked)if(overlaps(start,end,b.start,b.end))return false;
 U count=0;
 for(const auto& a:p.work) {
  if(overlaps(start,end,a.start,a.end) || start/86400==a.start/86400)return false;
  if(a.end<=start && start-a.end<43200)return false;
  if(end<=a.start && a.start-end<43200)return false;
 }
 // Check all rolling 168-hour windows, including already-planned future work.
 std::vector<U> starts{start};for(const auto& a:p.work)starts.push_back(a.start);
 std::sort(starts.begin(),starts.end());size_t left=0;
 for(size_t right=0;right<starts.size();++right) {
  while(starts[right]-starts[left]>=604800)++left;
  count=std::max(count,U(right-left+1));
 }
 return count<=5;
}
PlannerPerson planner_person(const WorldState& w,U p,U slot) {
 PlannerPerson x{p,slot,val(w,p,DEPT),val(w,ref(w,slot,SECTION),SECTION_KEY),
  val(w,slot,ORDINAL),val(w,slot,RESPONSIBILITY),val(w,p,QUAL),val(w,p,UNTIL),val(w,slot,STATIONS)};
 for(U a:person_records(w,"activity",p)) {
  if(val(w,a,DEBT))x.debt=true;
  const U start=val(w,a,START),end=effective_end(w,a);
  if(val(w,a,VALUE)==F04_DUTY && (val(w,a,STATE)==ACTIVE || has(w,a,STOP)) && start<end)x.work.push_back({start,end});
  if(val(w,a,STATE)==ACTIVE && (val(w,a,VALUE)==F04_REST || val(w,a,VALUE)==F04_ABSENCE))x.blocked.push_back({start,end});
 }
 return x;
}
void ordinary_allowed(const WorldState& w,U p,U start,U end) {
 need(end-start==28800 && start%28800==0,F04_ARGUMENT);
 U slot=0;for(U s:all(w,"slot"))if(ref(w,s,PERSON)==p){slot=s;break;}
 need(slot,F04_VACANT);need(ordinary_fits(planner_person(w,p,slot),start,end),F04_OVERLAP);
}
bool role_through(const WorldState& w,U p,U role,U dept,U start,U end) {
 if(!role)return true;
 for(U a:person_records(w,"appointment",p))if(val(w,a,ROLE)==role && val(w,a,DEPT)==dept &&
  val(w,a,STATE)==ACTIVE && val(w,a,START)<=start && end<=val(w,a,END))return true;
 return false;
}
bool service_skill(const WorldState& w,const PlannerPerson& p,U station,U end) {
 if(!(p.stations&station) || end>p.expiry || !slot_qualified(w,p.id,p.slot,end-1))return false;
 if(station==F04_ST_COMMAND)return (p.mask&(1ULL<<F04_COMMAND))!=0;
 if(station==F04_ST_TACTICAL)return (p.mask&(1ULL<<F04_Q_TACTICAL))!=0;
 if(station==F04_ST_MEDICAL)return (p.mask&((1ULL<<F04_Q_CLINICAL)|(1ULL<<F04_Q_NURSING)))!=0;
 return true;
}
U add_duty(Campaign& c,const ContentCatalog& cat,const F04Request& r,U person,U slot,U start,U end,U plan,bool temporary=false,U origin=0) {
 const U a=make(c,cat,"activity");link(c,a,SHIP,1);link(c,a,PERSON,person);link(c,a,SLOT,slot);link(c,a,ISSUER,r.actor.id);
 if(plan)link(c,a,PLAN,plan);if(origin)link(c,a,ACTIVITY,origin);
 temporal(c,a,start,end);set(c,a,VALUE,F04_DUTY);set(c,a,CAUSE,r.cause);set(c,a,ORDINARY,1);set(c,a,TEMPORARY,temporary?1:0);return a;
}
U add_service(Campaign& c,const ContentCatalog& cat,const F04Request& r,U p,U slot,U station,U start,U end) {
 const U f=make(c,cat,"function");link(c,f,SHIP,1);link(c,f,PERSON,p);link(c,f,SLOT,slot);link(c,f,ISSUER,r.actor.id);
 temporal(c,f,start,end);set(c,f,STATIONS,station);set(c,f,CAUSE,r.cause);return f;
}
void roster_gap(Campaign& c,const ContentCatalog& cat,const F04Request& r,U plan,U start,U end,U dept,U station,U missing) {
 const U g=make(c,cat,"roster_gap");link(c,g,SHIP,1);link(c,g,ISSUER,r.actor.id);link(c,g,PLAN,plan);
 temporal(c,g,start,end);set(c,g,DEPT,dept);set(c,g,STATIONS,station);set(c,g,VALUE,missing);set(c,g,CAUSE,r.cause);
}
U plan_watches(Campaign& c,const ContentCatalog& cat,const F04Request& r) {
 need(organization(c.world) && r.cause && val(c.world,1,PATTERN)==3);
 need(r.start>=c.time.now() && r.start%86400==0 && r.end%86400==0 && r.start<r.end && r.end-r.start<=28*86400);
 need((r.value==F04_REFERENCE && r.end-r.start==86400 && r.aux==0) || (r.value==F04_ROTATING && r.aux<=1));
 const auto* profile=trek_templates::profile(val(c.world,1,TEMPLATE));need(!profile->watch_demands.empty(),F04_REVIEW);
 for(U a:all(c.world,"roster_plan"))need(!overlaps(r.start,r.end,val(c.world,a,START),val(c.world,a,END)),F04_OVERLAP);
 // Reject old overlapping duties/functions rather than silently rewrite a roster.
 for(const char* kind:{"activity","function","appointment"})for(U a:all(c.world,kind))if(val(c.world,a,STATE)==ACTIVE &&
  (type(c.world,a,"function") || (type(c.world,a,"activity") && val(c.world,a,VALUE)==F04_DUTY) ||
   (type(c.world,a,"appointment") && (val(c.world,a,ROLE)==F04_WATCH || val(c.world,a,ROLE)==F04_DUTY_HEAD))))
  need(!overlaps(r.start,r.end,val(c.world,a,START),effective_end(c.world,a)),F04_OVERLAP);
 std::vector<PlannerPerson> people;
 std::map<U,F04WatchDemand> demands;std::map<U,std::array<U,3>> department_targets;
 for(const auto& d:profile->watch_demands) {
  demands[d.section]=d;const auto* section=trek_templates::section(*profile,d.section);need(section,F04_INTERNAL);
  department_targets[section->department][0]+=d.alpha;department_targets[section->department][1]+=d.beta;department_targets[section->department][2]+=d.gamma;
 }
 for(U slot:all(c.world,"slot")) {
  const U p=ref(c.world,slot,PERSON);
  if(p && member(c.world,p) && val(c.world,p,CATEGORY)==1)people.push_back(planner_person(c.world,p,slot));
 }
 // Protect a small real qualified relief pool from discretionary workloads.
 // A greedy departmental fill otherwise spends every sensor/operator's weekly
 // capacity early and leaves the sixth day uncovered despite ample total crew.
 std::map<size_t,U> reserved;
 for(U station:profile->continuous_stations) {
  std::vector<size_t> candidates;
  for(size_t i=0;i<people.size();++i)if(!reserved.contains(i) && service_skill(c.world,people[i],station,r.end))candidates.push_back(i);
  std::stable_sort(candidates.begin(),candidates.end(),[&](size_t a,size_t b){
   auto priority=[](U role){return role==F04_CAPTAIN || role==F04_FIRST?2:role?1:0;};
   return priority(people[a].role)<priority(people[b].role);
  });
  for(size_t j=0;j<std::min(size_t(8),candidates.size());++j)reserved[candidates[j]]=station;
 }
 // Versioned additive vocabulary; no SCHEMA 1/2/3 field changes its meaning.
 set(c,1,SCHEMA,4);
 const U plan=make(c,cat,"roster_plan");link(c,plan,SHIP,1);link(c,plan,ISSUER,r.actor.id);
 temporal(c,plan,r.start,r.end);set(c,plan,VALUE,r.value);set(c,plan,CAUSE,r.cause);
 for(U day=r.start;day<r.end;day+=86400)for(U window_index=0;window_index<3;++window_index) {
  const U start=day+window_index*28800,end=start+28800,label=(window_index+2)%3;
  const bool reference=r.value==F04_REFERENCE || (r.aux==1 && day==r.start);
  std::set<size_t> selected;std::map<U,size_t> services;std::map<U,U> actual;
  auto eligible=[&](size_t i) {
   const auto& p=people[i];const U date=day/86400;
   const bool free_day=(date+p.id*5+date/7)%7>=5;
   return (reference || !free_day) && !selected.contains(i) && ordinary_fits(p,start,end) &&
    slot_qualified(c.world,p.id,p.slot,end-1) && role_through(c.world,p.id,p.role,p.department,start,end);
  };
  auto add=[&](size_t i) {selected.insert(i);++actual[people[i].department];};
  if(reference) {
   for(size_t i=0;i<people.size();++i) {
    const auto& p=people[i];const auto d=demands.at(p.section);
    U wanted=p.ordinal<=d.alpha?0:p.ordinal<=d.alpha+d.beta?1:p.ordinal<=d.alpha+d.beta+d.gamma?2:3;
    if(wanted==label && eligible(i))add(i);
   }
  }
  auto order=[&](size_t a,size_t b) {
   const auto score=[&](const PlannerPerson& p) {
    U recent=0;for(const auto& x:p.work)if(x.start<=start && start-x.start<604800)++recent;
    // Prefer fewer lifetime shifts, then rotate shift preference weekly.
    return std::array<U,4>{recent,U(p.work.size()),(label+3-(p.id+day/604800)%3)%3,p.id};
   };return score(people[a])<score(people[b]);
  };
  for(U station:profile->continuous_stations) {
   std::vector<size_t> candidates;
   for(size_t i=0;i<people.size();++i)if((reference?selected.contains(i):eligible(i)) && service_skill(c.world,people[i],station,end)) {
    bool used=false;for(auto [s,j]:services){(void)s;used|=j==i;}if(!used)candidates.push_back(i);
   }
   std::sort(candidates.begin(),candidates.end(),[&](size_t a,size_t b){
    const bool ra=reserved.contains(a) && reserved.at(a)==station,rb=reserved.contains(b) && reserved.at(b)==station;
    if(ra!=rb)return ra;
    if(bool(people[a].role)!=bool(people[b].role))return people[a].role==0;return order(a,b);
   });
   if(candidates.empty())roster_gap(c,cat,r,plan,start,end,station==F04_ST_COMMAND||station==F04_ST_HELM?U(F04_COMMAND):
    station==F04_ST_SENSORS?U(F04_SENSORS):station==F04_ST_ENGINEERING?U(F04_ENGINEERING):station==F04_ST_TACTICAL?U(F04_SECURITY):station==F04_ST_MEDICAL?U(F04_MEDICINE):U(F04_OPERATIONS),station,1);
   else {const auto i=candidates.front();services[station]=i;if(!reference)add(i);}
  }
  if(!reference)for(const auto& [dept,target]:department_targets) {
   std::vector<size_t> candidates;for(size_t i=0;i<people.size();++i)if(people[i].department==dept && !reserved.contains(i) && eligible(i))candidates.push_back(i);
   std::sort(candidates.begin(),candidates.end(),order);
   for(size_t i:candidates){if(actual[dept]>=target[label])break;add(i);}
  }
  for(const auto& [dept,target]:department_targets)if(actual[dept]<target[label])roster_gap(c,cat,r,plan,start,end,dept,0,target[label]-actual[dept]);
  for(size_t i:selected) {
   auto& p=people[i];add_duty(c,cat,r,p.id,p.slot,start,end,plan);p.work.push_back({start,end});
  }
  for(const auto& [station,i]:services) {
   const auto& p=people[i];add_service(c,cat,r,p.id,p.slot,station,start,end);
   if(station==F04_ST_COMMAND)appointment(c,cat,p.id,F04_WATCH,F04_COMMAND,start,end,r.actor.id,r.cause);
   if(station==F04_ST_ENGINEERING)appointment(c,cat,p.id,F04_DUTY_HEAD,F04_ENGINEERING,start,end,r.actor.id,r.cause);
  }
 }
 need(roster_schema(c.world),F04_REVIEW);
 return plan;
}
void stop_related(Campaign& c,U person,U slot,U start,U end) {
 for(const char* kind:{"function","appointment"})for(U id:all(c.world,kind))if(ref(c.world,id,PERSON)==person && val(c.world,id,STATE)==ACTIVE &&
  (type(c.world,id,"function")?ref(c.world,id,SLOT)==slot:(val(c.world,id,ROLE)==F04_WATCH || val(c.world,id,ROLE)==F04_DUTY_HEAD)) &&
  overlaps(start,end,val(c.world,id,START),val(c.world,id,END))) {
  if(val(c.world,id,START)<start)set(c,id,END,start);else set(c,id,STATE,CANCELLED);
 }
}
U stop_duty(Campaign& c,const F04Request& r) {
 need(val(c.world,1,SCHEMA)==4 && r.cause && type(c.world,r.target,"activity") && val(c.world,r.target,VALUE)==F04_DUTY &&
  val(c.world,r.target,STATE)==ACTIVE && c.time.now()<effective_end(c.world,r.target));
 const U at=std::max(c.time.now(),val(c.world,r.target,START));
 stop_related(c,ref(c.world,r.target,PERSON),ref(c.world,r.target,SLOT),at,effective_end(c.world,r.target));
 set(c,r.target,STOP,at);return r.target;
}
U cover_duty(Campaign& c,const ContentCatalog& cat,const F04Request& r) {
 need(val(c.world,1,SCHEMA)==4 && r.cause && type(c.world,r.target,"activity") && val(c.world,r.target,VALUE)==F04_DUTY);
 const U old=r.target,slot=ref(c.world,old,SLOT),outgoing=ref(c.world,old,PERSON),person=r.aux;
 need(r.start>=c.time.now() && r.start>=val(c.world,old,START) && r.end==val(c.world,old,END) && r.start<r.end);
 need(type(c.world,person,"person") && member(c.world,person) && val(c.world,person,CATEGORY)==1 && person!=outgoing,F04_DENIED);
 need(slot_qualified(c.world,person,slot,r.end-1),F04_QUALIFICATION);
 need(role_through(c.world,person,val(c.world,slot,RESPONSIBILITY),val(c.world,slot,DEPT),r.start,r.end),F04_DENIED);
 U own=0;for(U s:all(c.world,"slot"))if(ref(c.world,s,PERSON)==person){own=s;break;}
 need(own,F04_VACANT);need(ordinary_fits(planner_person(c.world,person,own),r.start,r.end),F04_OVERLAP);
 for(U a:all(c.world,"activity"))if(a!=old && ref(c.world,a,SLOT)==slot && val(c.world,a,VALUE)==F04_DUTY &&
  val(c.world,a,STATE)==ACTIVE && val(c.world,a,START)<effective_end(c.world,a))
  need(!overlaps(r.start,r.end,val(c.world,a,START),effective_end(c.world,a)),F04_OVERLAP);
 std::vector<U> stations;
 for(U f:person_records(c.world,"function",outgoing))if(ref(c.world,f,SLOT)==slot && val(c.world,f,STATE)==ACTIVE &&
  val(c.world,f,START)<=r.start && r.end<=val(c.world,f,END))stations.push_back(val(c.world,f,STATIONS));
 for(U station:stations)need(service_skill(c.world,planner_person(c.world,person,slot),station,r.end),F04_QUALIFICATION);
 stop_related(c,outgoing,slot,r.start,r.end);set(c,old,STOP,std::min(effective_end(c.world,old),r.start));
 const U result=add_duty(c,cat,r,person,slot,r.start,r.end,ref(c.world,old,PLAN),true,old);
 for(U station:stations) {
  add_service(c,cat,r,person,slot,station,r.start,r.end);
  if(station==F04_ST_COMMAND)appointment(c,cat,person,F04_WATCH,F04_COMMAND,r.start,r.end,r.actor.id,r.cause);
  if(station==F04_ST_ENGINEERING)appointment(c,cat,person,F04_DUTY_HEAD,F04_ENGINEERING,r.start,r.end,r.actor.id,r.cause);
 }
 return result;
}
bool roster_schema(const WorldState& w) {
 if(val(w,1,SCHEMA)!=4)return all(w,"roster_plan").empty() && all(w,"roster_gap").empty();
 const auto* profile=trek_templates::profile(val(w,1,TEMPLATE));if(!profile)return false;
 std::vector<Span> plans;std::map<U,std::vector<Span>> work,slots;
 for(U id:all(w,"roster_plan")) {
  const U a=val(w,id,START),b=val(w,id,END);
  if(a%86400 || b%86400 || b-a>28*86400 || val(w,id,STATE)!=ACTIVE || !val(w,id,CAUSE) ||
   (val(w,id,VALUE)!=F04_REFERENCE && val(w,id,VALUE)!=F04_ROTATING))return false;
  for(auto x:plans)if(overlaps(a,b,x.start,x.end))return false;plans.push_back({a,b});
 }
 for(U a:all(w,"activity")) {
  if((has(w,a,ORDINARY) || has(w,a,TEMPORARY) || has(w,a,STOP) || ref(w,a,PLAN)) && val(w,a,VALUE)!=F04_DUTY)return false;
  const U start=val(w,a,START),end=val(w,a,END),stop=effective_end(w,a),p=ref(w,a,PERSON),slot=ref(w,a,SLOT),plan=ref(w,a,PLAN);
  if(has(w,a,STOP) && (val(w,a,STOP)<start || val(w,a,STOP)>end))return false;
  if(val(w,a,TEMPORARY)>1 || val(w,a,ORDINARY)>1)return false;
  if(val(w,a,ORDINARY)) {
   if(!has(w,a,TEMPORARY) || end-start>28800 || (!val(w,a,TEMPORARY) && !ref(w,a,ACTIVITY) && (end-start!=28800 || start%28800)))return false;
   if(plan && (start<val(w,plan,START) || val(w,plan,END)<end))return false;
   if(val(w,a,TEMPORARY) || ref(w,a,ACTIVITY)) {
    const U origin=ref(w,a,ACTIVITY);
    if(!origin || origin>=a || ref(w,origin,SLOT)!=slot || val(w,origin,VALUE)!=F04_DUTY ||
     val(w,origin,START)>start || val(w,origin,END)<end || effective_end(w,origin)>start)return false;
   }
  }
  if(val(w,a,VALUE)==F04_DUTY && (val(w,a,STATE)==ACTIVE || has(w,a,STOP)) && start<stop) {
   work[p].push_back({start,stop});slots[slot].push_back({start,stop});
  }
 }
 for(auto& [p,list]:work) {
  std::sort(list.begin(),list.end(),[](Span a,Span b){return a.start<b.start;});
  for(size_t i=0,left=0;i<list.size();++i) {
   while(list[i].start-list[left].start>=604800)++left;
   if(i-left+1>5 || (i && (list[i].start/86400==list[i-1].start/86400 || list[i].start<list[i-1].end || list[i].start-list[i-1].end<43200)))return false;
  }
 }
 for(auto& [slot,list]:slots) {
  std::sort(list.begin(),list.end(),[](Span a,Span b){return a.start<b.start;});
  for(size_t i=1;i<list.size();++i)if(list[i].start<list[i-1].end)return false;
 }
 for(U id:all(w,"roster_gap")) {
  const U plan=ref(w,id,PLAN),station=val(w,id,STATIONS);
  if(!plan || !val(w,id,VALUE) || val(w,id,VALUE)>700 || val(w,id,DEPT)<1 || val(w,id,DEPT)>7 ||
   val(w,id,START)<val(w,plan,START) || val(w,id,END)>val(w,plan,END) ||
   (station && std::find(profile->continuous_stations.begin(),profile->continuous_stations.end(),station)==profile->continuous_stations.end()))return false;
 }
 return true;
}
// Append incident snapshots; initial planning gaps and resolved historical gaps
// remain evidence. The live coverage query always recomputes current validity.
void record_incident_gaps(Campaign& c,const ContentCatalog& cat,const F04Request& r) {
 if(val(c.world,1,SCHEMA)!=4)return;
 U person=0;
 switch(r.op) {
 case F04_ABSENCE:case F04_MEDICAL:case F04_CREDENTIAL:case F04_DEPART:person=r.target;break;
 case F04_TRANSFER:person=r.aux;break;
 case F04_ASSIGN:break;
 case F04_CANCEL_DUTY:case F04_COVER_DUTY:case F04_REVOKE:person=ref(c.world,r.target,PERSON);break;
 default:return;
 }
 std::set<U> plans;
 const auto activities=r.op==F04_ASSIGN?all(c.world,"activity"):person_records(c.world,"activity",person);
 for(U a:activities)if((r.op!=F04_ASSIGN || ref(c.world,a,SLOT)==r.target) && ref(c.world,a,PLAN) && val(c.world,a,END)>c.time.now())plans.insert(ref(c.world,a,PLAN));
 struct Missing {U plan,start,end,department,station;};std::vector<Missing> missing;
 const auto* profile=trek_templates::profile(val(c.world,1,TEMPLATE));
 for(U plan:plans) {
  const U start=std::max(c.time.now(),val(c.world,plan,START)),end=val(c.world,plan,END);
  std::set<U> boundaries{start,end};
  for(const char* kind:{"activity","appointment","function"})for(U a:all(c.world,kind))
   for(U b:{val(c.world,a,START),val(c.world,a,END),effective_end(c.world,a)})if(start<b && b<end)boundaries.insert(b);
  for(U p:all(c.world,"person")){U b=val(c.world,p,UNTIL);if(start<b && b<end)boundaries.insert(b);}
  for(U station:profile->continuous_stations) {
   const U dept=station==F04_ST_COMMAND||station==F04_ST_HELM?U(F04_COMMAND):station==F04_ST_SENSORS?U(F04_SENSORS):
    station==F04_ST_ENGINEERING?U(F04_ENGINEERING):station==F04_ST_TACTICAL?U(F04_SECURITY):station==F04_ST_MEDICAL?U(F04_MEDICINE):U(F04_OPERATIONS);
   U gap_start=end;
   for(U b:boundaries) {
    const bool covered=b==end || service_covered(c.world,station,b);
    if(!covered && gap_start==end)gap_start=b;
    if(covered && gap_start!=end){missing.push_back({plan,gap_start,b,dept,station});gap_start=end;}
   }
  }
 }
 for(const auto& g:missing)roster_gap(c,cat,r,g.plan,g.start,g.end,g.department,g.station,1);
}
