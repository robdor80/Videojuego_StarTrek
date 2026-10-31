// ABI projections only; query buffers never own operational state.
uint32_t f04_relief_candidates_page(F04Session* s,F04Ref who,U activity,U start,U end,U offset,F04ReliefCandidate* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;
  need(val(w,1,SCHEMA)==4 && type(w,activity,"activity") && val(w,activity,VALUE)==F04_DUTY &&
   start>=s->c->time.now() && val(w,activity,START)<=start && start<end && end==val(w,activity,END));
  const U slot=ref(w,activity,SLOT),original=ref(w,activity,PERSON);std::vector<F04ReliefCandidate> candidates;
  const auto services=duty_services(w,activity,start,end);
  for(U own:all(w,"slot")) {
   U p=ref(w,own,PERSON);if(!p || p==original || !member(w,p) || val(w,p,CATEGORY)!=1 || !slot_qualified(w,p,slot,end-1) ||
    !role_through(w,p,val(w,slot,RESPONSIBILITY),val(w,slot,DEPT),start,end))continue;
   if(!ordinary_fits(planner_person(w,p,own),start,end))continue;
   bool valid=true;for(U station:services)valid&=service_skill(w,planner_person(w,p,slot),station,end);
   if(valid)candidates.push_back({p,own});
  }
  std::sort(candidates.begin(),candidates.end(),[](auto a,auto b){return a.person<b.person;});
  *total=candidates.size();need(offset<=*total);*written=std::min(capacity,*total-offset);
  for(U i=0;i<*written;++i)out[i]=candidates[static_cast<size_t>(offset+i)];return F04_OK;
 });
}
uint32_t f04_template_watch_demands(U id,F04WatchDemand* out,U capacity,U* count) {
 if(!count || (!out && capacity))return F04_ARGUMENT;*count=0;
 const auto* p=trek_templates::profile(id);if(!p)return F04_ARGUMENT;
 *count=p->watch_demands.size();if(capacity<*count)return F04_CAPACITY;
 std::copy(p->watch_demands.begin(),p->watch_demands.end(),out);return F04_OK;
}
uint32_t f04_duties_page(F04Session* s,F04Ref who,U offset,F04DutyView* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;std::vector<U> duties;
  for(U a:all(w,"activity"))if(val(w,a,VALUE)==F04_DUTY)duties.push_back(a);
  *total=duties.size();need(offset<=*total);*written=std::min(capacity,*total-offset);
  for(U i=0;i<*written;++i) {
   const U a=duties[static_cast<size_t>(offset+i)];out[i]={a,ref(w,a,PERSON),ref(w,a,SLOT),val(w,a,START),val(w,a,END),
    has(w,a,STOP)?val(w,a,STOP):val(w,a,END),ref(w,a,PLAN),val(w,a,CAUSE),
    static_cast<uint32_t>(val(w,a,ORDINARY)),static_cast<uint32_t>(val(w,a,TEMPORARY)),static_cast<uint32_t>(val(w,a,STATE)),0};
  }return F04_OK;
 });
}
uint32_t f04_roster_gaps_page(F04Session* s,F04Ref who,U offset,F04RosterGap* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;const auto gaps=all(w,"roster_gap");
  *total=gaps.size();need(offset<=*total);*written=std::min(capacity,*total-offset);
  for(U i=0;i<*written;++i){const U g=gaps[static_cast<size_t>(offset+i)];out[i]={g,val(w,g,START),val(w,g,END),val(w,g,DEPT),val(w,g,STATIONS),val(w,g,VALUE),ref(w,g,PLAN)};}
  return F04_OK;
 });
}
uint32_t f04_service_coverage(F04Session* s,F04Ref who,U start,U end,F04ServiceCoverage* out,U capacity,U* count) {
 if(!count || (!out && capacity))return F04_ARGUMENT;*count=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;need(organization(w) && start<end && end<=FOREVER && end-start<=28*86400);
  const auto stations=organization_services(w);
  *count=stations.size();need(capacity>=*count,F04_CAPACITY);
  std::set<U> boundaries{start};
  for(const char* kind:{"activity","appointment","function"})for(U a:all(w,kind))
   for(U b:{val(w,a,START),val(w,a,END),effective_end(w,a)})if(start<b && b<end)boundaries.insert(b);
  for(U p:all(w,"person")){U b=val(w,p,UNTIL);if(start<b && b<end)boundaries.insert(b);}
  for(size_t i=0;i<stations.size();++i) {
   const U station=stations[i];out[i]={station,start,end,end,0,1,0};
   for(U b:boundaries)if(!service_covered(w,station,b)){out[i].covered=0;out[i].first_gap=b;break;}
   if(val(w,1,SCHEMA)==4)for(U f:all(w,"function"))if(val(w,f,STATIONS)==station && station_active(w,f,start)){out[i].person=ref(w,f,PERSON);break;}
  }return F04_OK;
 });
}
