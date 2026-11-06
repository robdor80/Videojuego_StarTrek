// F06-BIS: persistent operations and scientific knowledge on SAME Core campaign.
// This file is appended after f06_runtime.inc. No second world/clock/save stack.
#include "f06_bis.h"
namespace {
U f06_bis_public(const WorldState& w,U raw) {
 return f06_public(raw^UINT64_C(0x0b157e5715),val(w,1,SHIP_ID));
}
F06EnvironmentView f06_env_view(const WorldState& w) {
 const auto ids=all(w,"f06_environment");
 if(ids.empty())return {};
 const U id=ids[0];
 return {val(w,id,F06_ENV_REV),static_cast<uint32_t>(val(w,id,F06_ENV_EM)),
  static_cast<uint32_t>(val(w,id,F06_ENV_THERM)),
  static_cast<uint32_t>(val(w,id,F06_ENV_GRAV)),
  static_cast<uint32_t>(val(w,id,F06_ENV_SUB)),
  static_cast<uint32_t>(val(w,id,F06_ENV_BIO))};
}
U f06_section_id(const WorldState& w,U section) {
 for(U id:all(w,"f06_section_array"))if(val(w,id,F06_SEC_ID)==section)return id;
 return 0;
}
F06SectionView f06_section_view(const WorldState& w,U section) {
 const U id=f06_section_id(w,section);
 if(!id)return {static_cast<uint32_t>(section),0,0,0,0,0,0,0,0};
 return {static_cast<uint32_t>(section),1,
  static_cast<uint32_t>(val(w,id,F06_SEC_LINK)),
  static_cast<uint32_t>(val(w,id,F06_SEC_CAP)),
  static_cast<uint32_t>(val(w,id,F06_SEC_PWR)),
  static_cast<uint32_t>(val(w,id,F06_SEC_INT)),
  static_cast<uint32_t>(val(w,id,F06_SEC_SHORT)),
  static_cast<uint32_t>(val(w,id,F06_SEC_LONG)),
  static_cast<uint32_t>(val(w,id,F06_SEC_FOCUS))};
}
U f06_timed_by_public(const WorldState& w,U public_id) {
 for(U id:all(w,"f06_timed_scan"))
  if(val(w,id,F06_TIMED_PUBLIC)==public_id)return id;
 return 0;
}
F06TimedScanView f06_timed_view(const WorldState& w,U id) {
 const U c=ref(w,id,F06_CONTACT_REF);
 return {val(w,id,F06_TIMED_PUBLIC),val(w,c,F06_PUBLIC_ID),
   val(w,id,F06_TIMED_START),val(w,id,F06_TIMED_DUE),
   val(w,id,F06_TIMED_RESULT),
   static_cast<uint32_t>(val(w,id,F06_TIMED_STATUS)),
   static_cast<uint32_t>(val(w,id,F06_TIMED_COST))};
}
U f06_report_by_public(const WorldState& w,U id) {
 for(U r:all(w,"f06_science_report"))if(val(w,r,F06_SCI_PUBLIC)==id)return r;
 return 0;
}
F06ScienceReportView f06_report_view(const WorldState& w,U id) {
 const U h=ref(w,id,F06_HANDOFF_REF),o=ref(w,id,F06_OBSERVATION_REF),
  contact=ref(w,h,F06_CONTACT_REF);
 return {val(w,id,F06_SCI_PUBLIC),val(w,h,F06_H_PUBLIC),
  val(w,contact,F06_PUBLIC_ID),val(w,o,F06_O_PUBLIC),val(w,id,F06_SCI_TICK),
  static_cast<uint32_t>(val(w,id,F06_SCI_TEMP)),
  static_cast<uint32_t>(val(w,id,F06_SCI_PRESS)),
  static_cast<uint32_t>(val(w,id,F06_SCI_WATER)),
  static_cast<uint32_t>(val(w,id,F06_SCI_N2)),
  static_cast<uint32_t>(val(w,id,F06_SCI_O2)),
  static_cast<uint32_t>(val(w,id,F06_SCI_CO2)),
  static_cast<uint32_t>(val(w,id,F06_SCI_SOLID)),
  static_cast<uint32_t>(val(w,id,F06_SCI_BIO)),
  static_cast<uint32_t>(val(w,id,F06_SCI_QUALITY)),
  static_cast<uint32_t>(val(w,id,F06_SCI_CONF)),
  static_cast<uint32_t>(val(w,id,F06_SCI_PLANET)),1};
}
U f06_handoff_by_public(const WorldState& w,U id) {
 for(U h:all(w,"f06_handoff"))if(val(w,h,F06_H_PUBLIC)==id)return h;
 return 0;
}
U f06_candidate_class(const F06ScienceSample& input,U confidence) {
 if(confidence<550)return F06_PLANET_UNKNOWN;
 if(!input.solid_surface)return F06_PLANET_J;
 if(input.temperature_k>450 || input.pressure_mbar>30000)return F06_PLANET_Y;
 if(input.temperature_k>=270 && input.temperature_k<=325 &&
    input.water_permille>=80 && input.pressure_mbar>=450 &&
    input.pressure_mbar<=6000)return F06_PLANET_M;
 if(input.temperature_k<245)return F06_PLANET_P;
 if(input.water_permille==0 && input.temperature_k>=275)return F06_PLANET_H;
 return F06_PLANET_L;
}
bool f06_science_bio_corrob(const WorldState& w,U contact,U source_obs) {
 for(U id:all(w,"f06_science_report")){
  const U h=ref(w,id,F06_HANDOFF_REF);
  if(ref(w,h,F06_CONTACT_REF)==contact &&
     ref(w,id,F06_OBSERVATION_REF)!=source_obs &&
     val(w,id,F06_SCI_BIO)>=2 && val(w,id,F06_SCI_CONF)>=650)return true;
 }
 return false;
}
// Called by the existing passive-watch tick, after the world's own signals
// have been evaluated. This cannot create contacts without real signatures.
void f06_bis_tick(Campaign& c,const ContentCatalog& cat) {
 for(U job:all(c.world,"f06_timed_scan")){
  if(val(c.world,job,F06_TIMED_STATUS)!=F06_TIMED_QUEUED ||
     val(c.world,job,F06_TIMED_DUE)>c.time.now())continue;
  const U contact=ref(c.world,job,F06_CONTACT_REF);
  const U actor=ref(c.world,job,PERSON);
  const auto hw=f06_array_state(c.world);
  bool permitted=val(c.world,contact,F06_STATUS)==F06_ACTIVE &&
    hw.focused_enabled && hw.capability_permille && hw.power_permille &&
    hw.integrity_permille;
  if(permitted) {
   try {(void)scan_station(c,actor);}catch(const Denial&){permitted=false;}
  }
  if(permitted){
   const U signal=ref(c.world,contact,F06_SIGNAL_REF);
   f06_apply(c,cat,signal,true,true);
   permitted=val(c.world,contact,F06_STATUS)==F06_ACTIVE;
  }
  if(permitted){
   f06_record_focus(c,cat,contact,actor);
   const auto obs=all(c.world,"f06_observation");
   need(!obs.empty(),F04_INTERNAL);
   f06_set(c,job,F06_TIMED_RESULT,val(c.world,obs.back(),F06_O_PUBLIC));
   f06_set(c,job,F06_TIMED_STATUS,F06_TIMED_FINISHED);
   (void)event(c,cat,actor,6061,F04_OK,0,job);
  }else{
   f06_set(c,job,F06_TIMED_STATUS,F06_TIMED_FAILED);
   (void)event(c,cat,actor,6062,F04_UNAVAILABLE,0,job);
  }
 }
}
} // namespace

uint32_t f06_host_environment(F04Session* s,const F06EnvironmentInput* in,
 F06EnvironmentView* out) {
 if(!in || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(in->expected_revision==s->c->world.revision(),F04_STALE);
  need(in->source_revision && in->source_revision<=FOREVER &&
   !in->reserved && in->em_permille<=550 && in->thermal_permille<=550 &&
   in->gravimetric_permille<=550 && in->subspace_permille<=550 &&
   in->biological_permille<=550,F04_ARGUMENT);
  const auto rows=all(s->c->world,"f06_environment");
  if(!rows.empty())
   need(in->source_revision>val(s->c->world,rows[0],F06_ENV_REV),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  U id=rows.empty()?0:rows[0];
  if(!id){id=make(*next,*s->content.catalog(),"f06_environment");link(*next,id,SHIP,1);}
  f06_set(*next,id,F06_ENV_REV,in->source_revision);
  f06_set(*next,id,F06_ENV_EM,in->em_permille);
  f06_set(*next,id,F06_ENV_THERM,in->thermal_permille);
  f06_set(*next,id,F06_ENV_GRAV,in->gravimetric_permille);
  f06_set(*next,id,F06_ENV_SUB,in->subspace_permille);
  f06_set(*next,id,F06_ENV_BIO,in->biological_permille);
  f06_poll(*next,*s->content.catalog(),0,false);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_env_view(s->c->world);return F04_OK;
 });
}
uint32_t f06_environment_status(F04Session* s,F04Ref who,F06EnvironmentView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  *out=f06_env_view(s->c->world);return F04_OK;
 });
}
uint32_t f06_host_section_array(F04Session* s,const F06SectionInput* in,
 F06SectionView* out) {
 if(!in || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(in->section_id>=1 && in->section_id<=2 && in->linked<=1 &&
   in->capability_permille<=1000 && in->power_permille<=1000 &&
   in->integrity_permille<=1000 && in->short_enabled<=1 &&
   in->long_enabled<=1 && in->focused_enabled<=1,F04_ARGUMENT);
  need(in->expected_revision==s->c->world.revision(),F04_STALE);
  need(f06_profile_view(s->c->world).profile_id==5,F04_SCOPE);
  auto next=std::make_unique<Campaign>(*s->c);
  U id=f06_section_id(next->world,in->section_id);
  if(!id){id=make(*next,*s->content.catalog(),"f06_section_array");link(*next,id,SHIP,1);}
  f06_set(*next,id,F06_SEC_ID,in->section_id);
  f06_set(*next,id,F06_SEC_LINK,in->linked);
  f06_set(*next,id,F06_SEC_CAP,in->capability_permille);
  f06_set(*next,id,F06_SEC_PWR,in->power_permille);
  f06_set(*next,id,F06_SEC_INT,in->integrity_permille);
  f06_set(*next,id,F06_SEC_SHORT,in->short_enabled);
  f06_set(*next,id,F06_SEC_LONG,in->long_enabled);
  f06_set(*next,id,F06_SEC_FOCUS,in->focused_enabled);
  f06_poll(*next,*s->content.catalog(),0,false);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_section_view(s->c->world,in->section_id);return F04_OK;
 });
}
uint32_t f06_section_status(F04Session* s,F04Ref who,uint32_t section,F06SectionView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  need(section>=1 && section<=2,F04_ARGUMENT);
  *out=f06_section_view(s->c->world,section);return F04_OK;
 });
}
uint32_t f06_begin_timed_scan(F04Session* s,F04Ref who,
 const F06TimedScanRequest* req,F06TimedScanView* out) {
 if(!req || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  need(req->request_key && req->request_key<=FOREVER && !req->reserved &&
   req->nominal_seconds>=30 && req->nominal_seconds<=900,F04_ARGUMENT);
  for(U job:all(s->c->world,"f06_timed_scan"))
   if(val(s->c->world,job,F06_TIMED_KEY)==req->request_key) {
    need(ref(s->c->world,job,PERSON)==who.id &&
     val(s->c->world,ref(s->c->world,job,F06_CONTACT_REF),F06_PUBLIC_ID)==req->contact_id,
     F04_OVERLAP);
    *out=f06_timed_view(s->c->world,job);return F04_OK;
   }
  need(req->expected_revision==s->c->world.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  (void)scan_station(*next,who.id);
  const U contact=f06_contact_for_public(next->world,req->contact_id);
  need(contact && val(next->world,contact,F06_STATUS)==F06_ACTIVE,F04_UNAVAILABLE);
  const auto hw=f06_array_state(next->world);
  need(hw.focused_enabled && hw.power_permille>=400 && hw.integrity_permille &&
   hw.capability_permille,F04_UNAVAILABLE);
  U ongoing=0;
  for(U job:all(next->world,"f06_timed_scan"))
   if(val(next->world,job,F06_TIMED_STATUS)==F06_TIMED_QUEUED)++ongoing;
  need(ongoing<std::max<U>(1,hw.power_permille/350),F04_CAPACITY);
  need(all(next->world,"f06_timed_scan").size()<256,F04_CAPACITY);
  const U sig=ref(next->world,contact,F06_SIGNAL_REF);
  const U pen=val(next->world,sig,F06_INTERFERENCE);
  const U duration=(U(req->nominal_seconds)*(1000+pen)+999)/1000;
  const U cost=std::min<U>(500,100+duration/6);
  const U now=next->time.now();
  need(now<=FOREVER-duration,F04_ARGUMENT);
  const U id=make(*next,*s->content.catalog(),"f06_timed_scan");
  link(*next,id,SHIP,1);link(*next,id,PERSON,who.id);
  link(*next,id,F06_CONTACT_REF,contact);
  const U pub=f06_bis_public(next->world,id);
  need(!f06_timed_by_public(next->world,pub),F04_CAPACITY);
  f06_set(*next,id,F06_TIMED_KEY,req->request_key);
  f06_set(*next,id,F06_TIMED_PUBLIC,pub);
  f06_set(*next,id,F06_TIMED_START,now);
  f06_set(*next,id,F06_TIMED_DUE,now+duration);
  f06_set(*next,id,F06_TIMED_COST,cost);
  f06_set(*next,id,F06_TIMED_STATUS,F06_TIMED_QUEUED);
  (void)event(*next,*s->content.catalog(),who.id,6060,F04_OK,req->request_key,id);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_timed_view(s->c->world,id);return F04_OK;
 });
}
uint32_t f06_cancel_timed_scan(F04Session* s,F04Ref who,U revision,U scan,
 F06TimedScanView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  const U id=f06_timed_by_public(s->c->world,scan);
  need(id,F04_UNAVAILABLE);
  need(ref(s->c->world,id,PERSON)==who.id ||
   commander(s->c->world,s->c->time.now())==who.id,F04_DENIED);
  if(val(s->c->world,id,F06_TIMED_STATUS)==F06_TIMED_CANCELLED) {
   *out=f06_timed_view(s->c->world,id);return F04_OK;
  }
  need(val(s->c->world,id,F06_TIMED_STATUS)==F06_TIMED_QUEUED,F04_EXPIRED);
  need(revision==s->c->world.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  f06_set(*next,id,F06_TIMED_STATUS,F06_TIMED_CANCELLED);
  (void)event(*next,*s->content.catalog(),who.id,6063,F04_OK,0,id);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_timed_view(s->c->world,id);return F04_OK;
 });
}
uint32_t f06_timed_scans_page(F04Session* s,F04Ref who,U offset,
 F06TimedScanView* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  const auto ids=all(s->c->world,"f06_timed_scan");
  *total=ids.size();need(offset<=*total,F04_ARGUMENT);
  *written=std::min<U>(capacity,*total-offset);
  for(U i=0;i<*written;++i)
   out[i]=f06_timed_view(s->c->world,ids[static_cast<size_t>(offset+i)]);
  return F04_OK;
 });
}
uint32_t f06_host_complete_science(F04Session* s,const F06ScienceSample* in,
 F06ScienceReportView* out) {
 if(!in || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(in->request_key && in->request_key<=FOREVER &&
   in->instrument_revision && in->instrument_revision<=FOREVER &&
   !in->reserved && in->quality_permille>=1 && in->quality_permille<=1000 &&
   in->temperature_k>=50 && in->temperature_k<=2000 &&
   in->pressure_mbar<=100000 && in->water_permille<=1000 &&
   in->nitrogen_permille+U(in->oxygen_permille)+in->co2_permille<=1000 &&
   in->solid_surface<=1 && in->biological_evidence<=3,F04_ARGUMENT);
  const auto& w=s->c->world;
  const U handoff=f06_handoff_by_public(w,in->handoff_id);
  const U obs=f06_result_by_public(w,in->focused_result_id);
  need(handoff && obs,F04_UNAVAILABLE);
  need(ref(w,handoff,F06_CONTACT_REF)==ref(w,obs,F06_CONTACT_REF),F04_ARGUMENT);
  const U contact=ref(w,handoff,F06_CONTACT_REF);
  need(val(w,contact,F06_SEEN_CATEGORY)==F06_CATEGORY_PLANET,F04_UNAVAILABLE);
  for(U prev:all(w,"f06_science_report"))
   if(val(w,prev,F06_SCI_KEY)==in->request_key) {
    need(ref(w,prev,F06_HANDOFF_REF)==handoff &&
     ref(w,prev,F06_OBSERVATION_REF)==obs &&
     val(w,prev,F06_SCI_INSTRUMENT)==in->instrument_revision &&
     val(w,prev,F06_SCI_TEMP)==in->temperature_k &&
     val(w,prev,F06_SCI_PRESS)==in->pressure_mbar &&
     val(w,prev,F06_SCI_WATER)==in->water_permille &&
     val(w,prev,F06_SCI_N2)==in->nitrogen_permille &&
     val(w,prev,F06_SCI_O2)==in->oxygen_permille &&
     val(w,prev,F06_SCI_CO2)==in->co2_permille &&
     val(w,prev,F06_SCI_SOLID)==in->solid_surface &&
     val(w,prev,F06_SCI_BIO)==in->biological_evidence &&
     val(w,prev,F06_SCI_QUALITY)==in->quality_permille,F04_OVERLAP);
    *out=f06_report_view(w,prev);return F04_OK;
   }
  need(val(w,handoff,F06_H_STATUS)==F06_SCIENCE_QUEUED,F04_EXPIRED);
  need(in->expected_revision==w.revision(),F04_STALE);
  need(all(w,"f06_science_report").size()<512,F04_CAPACITY);
  if(in->solid_surface && !in->pressure_mbar)
   need(!in->nitrogen_permille && !in->oxygen_permille && !in->co2_permille,
    F04_ARGUMENT);
  if(in->solid_surface && in->temperature_k<273)
   need(!in->water_permille,F04_ARGUMENT);
  if(!in->solid_surface)
   need(!in->water_permille && !in->biological_evidence,F04_ARGUMENT);
  if(in->biological_evidence>=2)
   need(in->solid_surface && in->water_permille>=80 &&
    in->temperature_k>=270 && in->temperature_k<=325 &&
    in->pressure_mbar>=450 && in->quality_permille>=650,F04_ARGUMENT);
  const U confidence=std::min<U>(in->quality_permille,val(w,obs,F06_O_CONF));
  if(in->biological_evidence==3)
   need(confidence>=850 && f06_science_bio_corrob(w,contact,obs),F04_ARGUMENT);
  auto next=std::make_unique<Campaign>(*s->c);
  const U id=make(*next,*s->content.catalog(),"f06_science_report");
  link(*next,id,SHIP,1);link(*next,id,F06_HANDOFF_REF,handoff);
  link(*next,id,F06_OBSERVATION_REF,obs);
  const U pub=f06_bis_public(next->world,id^in->request_key);
  need(!f06_report_by_public(next->world,pub),F04_CAPACITY);
  f06_set(*next,id,F06_SCI_KEY,in->request_key);
  f06_set(*next,id,F06_SCI_PUBLIC,pub);
  f06_set(*next,id,F06_SCI_INSTRUMENT,in->instrument_revision);
  f06_set(*next,id,F06_SCI_TICK,next->time.now());
  f06_set(*next,id,F06_SCI_TEMP,in->temperature_k);
  f06_set(*next,id,F06_SCI_PRESS,in->pressure_mbar);
  f06_set(*next,id,F06_SCI_WATER,in->water_permille);
  f06_set(*next,id,F06_SCI_N2,in->nitrogen_permille);
  f06_set(*next,id,F06_SCI_O2,in->oxygen_permille);
  f06_set(*next,id,F06_SCI_CO2,in->co2_permille);
  f06_set(*next,id,F06_SCI_SOLID,in->solid_surface);
  f06_set(*next,id,F06_SCI_BIO,in->biological_evidence);
  f06_set(*next,id,F06_SCI_QUALITY,in->quality_permille);
  f06_set(*next,id,F06_SCI_CONF,confidence);
  f06_set(*next,id,F06_SCI_PLANET,f06_candidate_class(*in,confidence));
  f06_set(*next,handoff,F06_H_STATUS,F06_SCIENCE_COMPLETED);
  (void)event(*next,*s->content.catalog(),0,6070,F04_OK,in->request_key,id);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_report_view(s->c->world,id);return F04_OK;
 });
}
uint32_t f06_science_reports_page(F04Session* s,F04Ref who,U offset,
 F06ScienceReportView* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  const auto rows=all(s->c->world,"f06_science_report");
  *total=rows.size();need(offset<=*total,F04_ARGUMENT);
  *written=std::min<U>(capacity,*total-offset);
  for(U i=0;i<*written;++i)
   out[i]=f06_report_view(s->c->world,rows[static_cast<size_t>(offset+i)]);
  return F04_OK;
 });
}
namespace {
F06PowerApplicationView f06_apply_power_view(const WorldState& w,U id) {
 return {val(w,id,F06_PWR_PUBLIC),val(w,id,F06_PWR_ALLOC_REV),
  val(w,id,F06_PWR_APPLIED_AT),
  static_cast<uint32_t>(val(w,id,F06_PWR_APPLIED)),
  has(w,id,F06_PWR_APPLIED)?1u:0u};
}
}
uint32_t f06_host_apply_power(F04Session* s,const F06PowerApplication* in,
 F06PowerApplicationView* out) {
 if(!in || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(!in->reserved && in->allocator_revision &&
   in->allocator_revision<=FOREVER &&
   in->new_total_power_permille<=1000,F04_ARGUMENT);
  const auto& w=s->c->world;
  const U request=f06_power_by_public(w,in->request_id);
  need(request,F04_UNAVAILABLE);
  if(has(w,request,F06_PWR_APPLIED)) {
   need(val(w,request,F06_PWR_ALLOC_REV)==in->allocator_revision &&
    val(w,request,F06_PWR_APPLIED)==in->new_total_power_permille,F04_OVERLAP);
   *out=f06_apply_power_view(w,request);return F04_OK;
  }
  need(val(w,request,F06_PWR_STATE)==F06_POWER_APPROVED &&
   s->c->time.now()<val(w,request,F06_PWR_EXPIRY),F04_EXPIRED);
  need(in->expected_revision==w.revision(),F04_STALE);
  // Source and donor validation/budget belong to trusted Engineering/Operations
  // power allocator. F06 never manufactures extra watts from an approval.
  need(all(w,"f06_section_array").empty(),F04_SCOPE);
  const U current=f06_array_state(w).power_permille;
  need(in->new_total_power_permille>=current &&
   U(in->new_total_power_permille)-current<=val(w,request,F06_PWR_AMOUNT),F04_ARGUMENT);
  auto next=std::make_unique<Campaign>(*s->c);
  auto arrays=all(next->world,"f06_array");
  U id=arrays.empty()?0:arrays[0];
  if(!id){
   id=make(*next,*s->content.catalog(),"f06_array");link(*next,id,SHIP,1);
   f06_set(*next,id,F06_ARRAY_CAPABILITY,1000);
   f06_set(*next,id,F06_ARRAY_POWER,1000);
   f06_set(*next,id,F06_ARRAY_INTEGRITY,1000);
   f06_set(*next,id,F06_ARRAY_SHORT,1);
   f06_set(*next,id,F06_ARRAY_LONG,1);
   f06_set(*next,id,F06_ARRAY_FOCUS,1);
  }
  f06_set(*next,id,F06_ARRAY_POWER,in->new_total_power_permille);
  f06_set(*next,request,F06_PWR_APPLIED,in->new_total_power_permille);
  f06_set(*next,request,F06_PWR_ALLOC_REV,in->allocator_revision);
  f06_set(*next,request,F06_PWR_APPLIED_AT,next->time.now());
  f06_poll(*next,*s->content.catalog(),0,false);
  (void)event(*next,*s->content.catalog(),0,6080,F04_OK,in->request_id,request);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_apply_power_view(s->c->world,request);return F04_OK;
 });
}
uint32_t f06_power_application_status(F04Session* s,F04Ref who,U request,
 F06PowerApplicationView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  const U id=f06_power_by_public(s->c->world,request);
  need(id,F04_UNAVAILABLE);
  *out=f06_apply_power_view(s->c->world,id);return F04_OK;
 });
}
