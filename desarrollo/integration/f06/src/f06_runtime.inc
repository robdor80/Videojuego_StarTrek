// F06 runtime over the EXISTING F04Session's Core WorldState.
// Include at the tail of f04_bridge.cpp; declarations precede f04_advance.
#include "f06_profiles_generated.h"
namespace {
void f06_bis_tick(Campaign&,const ContentCatalog&);
U f06_zigzag(int64_t x) {return x<0?U(-(x+1))*2+1:U(x)*2;}
U f06_public(U source,U ship_identity) {
 U z=source+UINT64_C(0x9e3779b97f4a7c15)+(ship_identity<<1);
 z=(z^(z>>30))*UINT64_C(0xbf58476d1ce4e5b9);
 z=(z^(z>>27))*UINT64_C(0x94d049bb133111eb);
 const U id=(z^(z>>31))&FOREVER;return id?id:1;
}
int64_t f06_unzigzag(U x) {return (x&1)?-int64_t(x/2)-1:int64_t(x/2);}
void f06_set(Campaign& c,U id,Field field,U v) {
 if(!has(c.world,id,field) || val(c.world,id,field)!=v)set(c,id,field,v);
}
U f06_distance(const WorldState& w,U s) {
 const long double x=f06_unzigzag(val(w,s,F06_X));
 const long double y=f06_unzigzag(val(w,s,F06_Y));
 const long double z=f06_unzigzag(val(w,s,F06_Z));
 return static_cast<U>(std::sqrt(x*x+y*y+z*z));
}
F06ArrayView f06_array_state(const WorldState& w) {
 // On the modernized Enterprise the two physical arrays stay independent.
 // A detached array never helps the current observer's ship.
 const auto sections=all(w,"f06_section_array");
 if(!sections.empty()) {
  U best=0,quality=0;
  for(U id:sections)if(val(w,id,F06_SEC_LINK)){
   const U q=val(w,id,F06_SEC_CAP)*val(w,id,F06_SEC_PWR)*
     val(w,id,F06_SEC_INT)/U(1000000);
   if(!best || q>quality){best=id;quality=q;}
  }
  if(!best)return {0,0,0,0,0,0};
  F06ArrayView effective{
   static_cast<uint32_t>(val(w,best,F06_SEC_CAP)),
   static_cast<uint32_t>(val(w,best,F06_SEC_PWR)),
   static_cast<uint32_t>(val(w,best,F06_SEC_INT)),0,0,0};
  // Flags represent modes available SOMEWHERE on the linked ship. Actual
  // strength is always computed independently for each hardware array.
  for(U id:sections)if(val(w,id,F06_SEC_LINK) &&
    val(w,id,F06_SEC_CAP) && val(w,id,F06_SEC_PWR) &&
    val(w,id,F06_SEC_INT)){
    effective.short_enabled|=static_cast<uint32_t>(val(w,id,F06_SEC_SHORT));
    effective.long_enabled|=static_cast<uint32_t>(val(w,id,F06_SEC_LONG));
    effective.focused_enabled|=static_cast<uint32_t>(val(w,id,F06_SEC_FOCUS));
  }
  return effective;
 }
 const auto rows=all(w,"f06_array");
 if(rows.empty())return {1000,1000,1000,1,1,1}; // nominal installed profile
 const U id=rows[0];
 return {static_cast<uint32_t>(val(w,id,F06_ARRAY_CAPABILITY)),
  static_cast<uint32_t>(val(w,id,F06_ARRAY_POWER)),
  static_cast<uint32_t>(val(w,id,F06_ARRAY_INTEGRITY)),
  static_cast<uint32_t>(val(w,id,F06_ARRAY_SHORT)),
  static_cast<uint32_t>(val(w,id,F06_ARRAY_LONG)),
  static_cast<uint32_t>(val(w,id,F06_ARRAY_FOCUS))};
}

F06ConfigView f06_current_config(const WorldState& w) {
 const auto rows=all(w,"f06_configuration");
 if(rows.empty())return {1000,1000,0,0,60}; // unchanged default
 const U id=rows[0];
 return {static_cast<uint32_t>(val(w,id,F06_CONFIG_SENS)),
  static_cast<uint32_t>(val(w,id,F06_CONFIG_RES)),
  static_cast<uint32_t>(val(w,id,F06_CONFIG_COMP)),
  static_cast<uint32_t>(val(w,id,F06_CONFIG_PRESET)),
  static_cast<uint32_t>(val(w,id,F06_CONFIG_INTERVAL))};
}
F06DiagnosticView f06_diagnostic_state(const Campaign& c) {
 const auto hw=f06_array_state(c.world);
 const auto cfg=f06_current_config(c.world);
 U state=1;
 if(!hw.power_permille || !hw.integrity_permille || !hw.capability_permille ||
    (!hw.short_enabled && !hw.long_enabled))state=3;
 else if(hw.power_permille<750 || hw.integrity_permille<750 ||
    hw.capability_permille<750)state=2;
 else if(cfg.sensitivity_permille<500 || cfg.resolution_permille<500)state=4;
 return {c.time.now(),static_cast<uint32_t>(state),hw.capability_permille,
   hw.power_permille,hw.integrity_permille,cfg.sensitivity_permille,
   static_cast<uint32_t>(2100-cfg.sensitivity_permille-cfg.resolution_permille-
     2*cfg.compensation_permille)};
}
F06ProfileNumbers f06_profile_numbers(const WorldState& w) {
 const auto arrays=all(w,"f06_array");
 const U id=arrays.empty()?0:val(w,arrays[0],F06_ARRAY_PROFILE);
 for(const auto& row:F06_PROFILE_NUMBERS)if(row.id==id)return row;
 return {0,0,1000,1000,1000,0,16}; // unchanged F06 baseline
}
F06ProfileView f06_profile_view(const WorldState& w) {
 const auto row=f06_profile_numbers(w);
 return {row.id,row.tier,row.short_permille,row.long_permille,row.focus_permille,
   row.interference_resistance_permille,row.tracking_slots};
}
U f06_tracking_capacity(const WorldState& w) {
 const auto hw=f06_array_state(w);
 // Ship-specific equipment can replace this normalized nominal ceiling later.
 return (U(f06_profile_numbers(w).tracking_slots)*hw.capability_permille*hw.power_permille*hw.integrity_permille)/
   U(1000000000);
}
U f06_track_cost(U mode) {return mode==F06_TRACK_PRIORITY?3:mode==F06_TRACK_NORMAL?1:0;}
U f06_tracking_used(const WorldState& w) {
 U used=0;
 for(U id:all(w,"f06_contact"))if(val(w,id,F06_STATUS)==F06_ACTIVE)
  used+=f06_track_cost(val(w,id,F06_TRACK_MODE));
 return used;
}
U f06_score_from_array(const WorldState& w,U s,U distance,bool active,bool focused,
 const F06ArrayView& array) {
 if(!array.capability_permille || !array.power_permille || !array.integrity_permille)return 0;
 if(focused && !array.focused_enabled)return 0;
 if(!focused && !array.long_enabled && !array.short_enabled)return 0;
 if(!val(w,s,F06_ACTIVE_FLAG))return 0;
 const U limit=focused?50000:30000;
 if(distance>limit)return 0;
 const auto profile=f06_profile_numbers(w);
 const U strength=val(w,s,F06_STRENGTH);
 const auto config=f06_current_config(w);
 U mask=U(val(w,s,F06_INTERFERENCE))*
  (1000-profile.interference_resistance_permille)/1000;
 mask=mask*(1000-config.compensation_permille)/1000;
 // Local band interference is authoritative Host-supplied state.
 const auto environments=all(w,"f06_environment");
 if(!environments.empty()) {
  Field field=F06_ENV_EM;
  switch(val(w,s,F06_CATEGORY)){
   case F06_CATEGORY_STAR:case F06_CATEGORY_ENERGY:case F06_CATEGORY_PARTICLES:
      field=F06_ENV_THERM;break;
   case F06_CATEGORY_PLANET:case F06_CATEGORY_MOON:case F06_CATEGORY_ASTEROID:
      field=F06_ENV_GRAV;break;
   case F06_CATEGORY_SUBSPACE:case F06_CATEGORY_WARP:case F06_CATEGORY_ANOMALY:
      field=F06_ENV_SUB;break;
   case F06_CATEGORY_LIFEFORM:field=F06_ENV_BIO;break;
   default:field=F06_ENV_EM;break;
  }
  mask=std::min<U>(850,mask+
    val(w,environments[0],field)*(1000-config.compensation_permille)/1000);
 }
 auto measure=[&](U range,bool near_bonus)->U {
  if(distance>range)return 0;
  // Fixed-point gameplay abstraction. Distances are milli-AU.
  U score=strength*(1000-550*distance/range)/1000;
  score=score*(active?1080:920)/1000;
  if(near_bonus)score=std::min<U>(1000,score+100);
  if(focused)score=std::min<U>(1000,score+160);
  return score>mask?score-mask:0;
 };
 U score=focused?measure(limit,false)*profile.focus_permille/1000:
   (array.long_enabled?measure(limit,false)*profile.long_permille/1000:0);
 if(!focused && array.short_enabled)
  score=std::max(score,measure(2000,true)*profile.short_permille/1000);
 score=score*array.capability_permille/1000;
 score=score*array.power_permille/1000;
 score=score*array.integrity_permille/1000;
 score=score*config.sensitivity_permille/1000;
 return std::min<U>(1000,score);
}

U f06_score(const WorldState& w,U s,U distance,bool active,bool focused) {
 const auto sections=all(w,"f06_section_array");
 if(sections.empty())
  return f06_score_from_array(w,s,distance,active,focused,f06_array_state(w));
 U strongest=0;
 for(U id:sections){
  if(!val(w,id,F06_SEC_LINK))continue;
  const F06ArrayView hw{
   static_cast<uint32_t>(val(w,id,F06_SEC_CAP)),
   static_cast<uint32_t>(val(w,id,F06_SEC_PWR)),
   static_cast<uint32_t>(val(w,id,F06_SEC_INT)),
   static_cast<uint32_t>(val(w,id,F06_SEC_SHORT)),
   static_cast<uint32_t>(val(w,id,F06_SEC_LONG)),
   static_cast<uint32_t>(val(w,id,F06_SEC_FOCUS))
  };
  strongest=std::max<U>(strongest,
   f06_score_from_array(w,s,distance,active,focused,hw));
 }
 return strongest;
}

U f06_rank(U score) {
 if(score>=720)return 4;if(score>=540)return 3;
 if(score>=380)return 2;if(score>=240)return 1;return 0;
}
U f06_contact_for_public(const WorldState& w,U public_id) {
 for(U c:all(w,"f06_contact"))if(val(w,c,F06_PUBLIC_ID)==public_id)return c;
 return 0;
}
U f06_contact_for(const WorldState& w,U source) {
 for(U c:all(w,"f06_contact"))if(ref(w,c,F06_SIGNAL_REF)==source)return c;
 return 0;
}
void f06_notice(Campaign& c,const ContentCatalog& cat,U contact,U kind) {
 // F04 events are Core-archivable; never allocate a second unbounded event log.
 (void)event(c,cat,0,6000+kind,F04_OK,0,contact);
}
F06ContactView f06_view(const WorldState& w,U id) {
 return {val(w,id,F06_PUBLIC_ID),val(w,id,F06_FIRST),val(w,id,F06_LAST),
   f06_unzigzag(val(w,id,F06_VISIBLE_X)),f06_unzigzag(val(w,id,F06_VISIBLE_Y)),
   f06_unzigzag(val(w,id,F06_VISIBLE_Z)),val(w,id,F06_SEEN_TRANSPONDER),
   static_cast<uint32_t>(val(w,id,F06_STATUS)),
   static_cast<uint32_t>(val(w,id,F06_CONFIDENCE)),
   static_cast<uint32_t>(val(w,id,F06_DISTANCE)),
   static_cast<uint32_t>(val(w,id,F06_SEEN_CLASS)),
   static_cast<uint32_t>(val(w,id,F06_LOSS_REASON)),
   static_cast<uint32_t>(val(w,id,F06_SEEN_CATEGORY))};
}
void f06_apply(Campaign& c,const ContentCatalog& cat,U sig,bool active,bool focused,
 U known_contact=0,bool indexed=false,U* allocated_cache=nullptr) {
 U contact=indexed?known_contact:f06_contact_for(c.world,sig);
 U d=f06_distance(c.world,sig);
 
 U score=f06_score(c.world,sig,d,active,focused);
 // Dedicated tracking gives a modest evidence improvement ONLY when an actual
 // sensor signal already passed the passive minimum, and no array overload exists.
 if(contact && score>=240 &&
  (allocated_cache?*allocated_cache:f06_tracking_used(c.world))<=f06_tracking_capacity(c.world))
  score=std::min<U>(1000,score+(val(c.world,contact,F06_TRACK_MODE)==F06_TRACK_PRIORITY?60:0));
 U rank=f06_rank(score*f06_current_config(c.world).resolution_permille/1000);
 // An active focused request must never create a contact out of hidden truth.
 if(!rank && !contact)return;
 if(!rank) {
  if(val(c.world,contact,F06_STATUS)==F06_ACTIVE) {
   const U previous=val(c.world,contact,F06_CONFIDENCE);
   const auto hw=f06_array_state(c.world);
   const bool unavailable=!hw.capability_permille || !hw.power_permille || !hw.integrity_permille ||
    (!hw.long_enabled && !hw.short_enabled);
   const U cause=unavailable?F06_EXIT_SENSOR_OFFLINE:val(c.world,sig,F06_EXIT);
   
   f06_set(c,contact,F06_STATUS,F06_LOST);
   if(allocated_cache) {
    const U slots=f06_track_cost(val(c.world,contact,F06_TRACK_MODE));
    need(*allocated_cache>=slots,F04_INTERNAL);
    *allocated_cache-=slots;
   }
   // An unavailable contact may not consume finite dedicated-tracking slots.
   f06_set(c,contact,F06_TRACK_MODE,F06_TRACK_PASSIVE);
   f06_set(c,contact,F06_LOSS_REASON,cause);
   f06_notice(c,cat,contact,(!cause && previous>=500)?F06_ANOMALOUS_LOSS:F06_CONTACT_LOST);
  }
  return;
 }
 const U confidence=std::min<U>(1000,(score-180)*1000/720);
 const U current_time=c.time.now();
 const bool fresh=!contact;
 const bool reacquired=contact && val(c.world,contact,F06_STATUS)==F06_LOST;
 if(fresh) {
  need(all(c.world,"f06_contact").size()<2048,F04_CAPACITY);
  contact=make(c,cat,"f06_contact");
  link(c,contact,SHIP,1);link(c,contact,F06_SIGNAL_REF,sig);
  const U public_id=f06_public(sig,val(c.world,1,SHIP_ID));
  need(!f06_contact_for_public(c.world,public_id),F04_CAPACITY);
  f06_set(c,contact,F06_PUBLIC_ID,public_id);
  f06_set(c,contact,F06_FIRST,current_time);
 }
 const U previous_class=val(c.world,contact,F06_SEEN_CLASS);
 f06_set(c,contact,F06_LAST,current_time);
 f06_set(c,contact,F06_STATUS,F06_ACTIVE);
 f06_set(c,contact,F06_LOSS_REASON,F06_EXIT_UNKNOWN);
 f06_set(c,contact,F06_CONFIDENCE,confidence);
 f06_set(c,contact,F06_DISTANCE,d);
 // Truth at sensor range is NOT automatically observed. Exact identity is
 // projected only on a resolved reading, never by catalogue lookup.
 if(rank>=2 && val(c.world,sig,F06_CATEGORY))
  f06_set(c,contact,F06_SEEN_CATEGORY,val(c.world,sig,F06_CATEGORY));
 if(rank>=4) {
  f06_set(c,contact,F06_SEEN_CLASS,val(c.world,sig,F06_CLASS));
  f06_set(c,contact,F06_SEEN_TRANSPONDER,val(c.world,sig,F06_TRANSPONDER));
 } else if(fresh) {
  f06_set(c,contact,F06_SEEN_CLASS,0);
  f06_set(c,contact,F06_SEEN_TRANSPONDER,0);
 }
 const U step=rank>=4?1:rank>=3?10:100;
 for(const auto [raw,field]:{std::pair(Field(F06_X),Field(F06_VISIBLE_X)),
  std::pair(Field(F06_Y),Field(F06_VISIBLE_Y)),std::pair(Field(F06_Z),Field(F06_VISIBLE_Z))}) {
  const int64_t p=f06_unzigzag(val(c.world,sig,raw));
  const int64_t approx=rank<2?0:(p/ static_cast<int64_t>(step))*static_cast<int64_t>(step);
  f06_set(c,contact,field,f06_zigzag(approx));
 }
 if(fresh)f06_notice(c,cat,contact,F06_NEW_CONTACT);
 else if(reacquired)f06_notice(c,cat,contact,F06_REACQUIRED);
 if(rank>=4 && !previous_class && val(c.world,contact,F06_SEEN_CLASS))
  f06_notice(c,cat,contact,F06_IDENTIFIED);
}
// Called on Core-clock advance or a privileged world-signature material change.
// The routine does not emit randomness or spawn entities/events without sources.
void f06_poll(Campaign& c,const ContentCatalog& cat,U focus,bool active) {
 const auto signals=all(c.world,"f06_signal");
 if(focus) {
  need(type(c.world,focus,"f06_contact") && val(c.world,focus,F06_STATUS)==F06_ACTIVE,F04_UNAVAILABLE);
  const U source=ref(c.world,focus,F06_SIGNAL_REF);
  need(type(c.world,source,"f06_signal"),F04_SCOPE);
  f06_apply(c,cat,source,true,true);return;
 }
 // Build once per polling window; otherwise every signal re-enumerates every
 // dossier and its tracking allocation, giving quadratic CPU/memory churn.
 std::map<U,U> known_contacts;
 for(U id:all(c.world,"f06_contact"))
  known_contacts.emplace(ref(c.world,id,F06_SIGNAL_REF),id);
 U allocated=f06_tracking_used(c.world);
 for(U signal:signals){
  const auto it=known_contacts.find(signal);
  f06_apply(c,cat,signal,active,false,
    it==known_contacts.end()?0:it->second,true,&allocated);
 }
 for(U id:all(c.world,"f06_power_request")) {
  if(val(c.world,id,F06_PWR_STATE)==F06_POWER_QUEUED &&
     val(c.world,id,F06_PWR_EXPIRY)<=c.time.now()) {
   f06_set(c,id,F06_PWR_STATE,F06_POWER_EXPIRED);
   (void)event(c,cat,0,6032,F04_OK,0,id);
  }
 }
 f06_bis_tick(c,cat);
}
} // namespace
namespace {
F06ScienceView f06_science_view(const WorldState& w,U id) {
 const U contact=ref(w,id,F06_CONTACT_REF);
 return {val(w,id,F06_H_PUBLIC),val(w,contact,F06_PUBLIC_ID),
  val(w,id,F06_H_TIME),val(w,id,F06_H_OBSERVED),val(w,id,F06_H_TRANSPONDER),
  f06_unzigzag(val(w,id,F06_H_X)),f06_unzigzag(val(w,id,F06_H_Y)),
  f06_unzigzag(val(w,id,F06_H_Z)),
  static_cast<uint32_t>(val(w,id,F06_H_PRIORITY)),
  static_cast<uint32_t>(val(w,id,F06_H_KIND)),static_cast<uint32_t>(val(w,id,F06_H_STATUS)),
  static_cast<uint32_t>(val(w,id,F06_H_CLASS)),
  static_cast<uint32_t>(val(w,id,F06_H_CONFIDENCE))};
}
} // namespace
uint32_t f06_science_handoff(F04Session* s,F04Ref who,
 const F06ScienceRequest* req,F06ScienceView* out) {
 if(!req || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  const auto& w=s->c->world;
  need(req->request_key && req->request_key<=FOREVER &&
   req->priority>=1 && req->priority<=4 &&
   req->analysis_kind>=1 && req->analysis_kind<=4,F04_ARGUMENT);
  // Idempotency is campaign-wide: it works after save/load and even if
  // world revision changed. A conflicting duplicate must not reveal its task.
  for(U h:all(w,"f06_handoff"))if(val(w,h,F06_H_KEY)==req->request_key) {
   need(ref(w,h,PERSON)==who.id &&
    val(w,ref(w,h,F06_CONTACT_REF),F06_PUBLIC_ID)==req->contact_id &&
    val(w,h,F06_H_PRIORITY)==req->priority &&
    val(w,h,F06_H_KIND)==req->analysis_kind,F04_OVERLAP);
   *out=f06_science_view(w,h);return F04_OK;
  }
  need(req->expected_revision==w.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  (void)scan_station(*next,who.id);
  const U c=f06_contact_for_public(next->world,req->contact_id);
  need(c,F04_UNAVAILABLE); // no handoff of unknown truth
  need(all(next->world,"f06_handoff").size()<512,F04_CAPACITY);
  const U id=make(*next,*s->content.catalog(),"f06_handoff");
  link(*next,id,SHIP,1);link(*next,id,PERSON,who.id);
  link(*next,id,F06_CONTACT_REF,c);
  const U public_id=f06_public(req->contact_id^req->request_key,
   val(next->world,1,SHIP_ID));
  for(U previous:all(next->world,"f06_handoff"))if(previous!=id)
   need(val(next->world,previous,F06_H_PUBLIC)!=public_id,F04_CAPACITY);
  f06_set(*next,id,F06_H_KEY,req->request_key);
  f06_set(*next,id,F06_H_PUBLIC,public_id);
  f06_set(*next,id,F06_H_TIME,next->time.now());
  f06_set(*next,id,F06_H_OBSERVED,val(next->world,c,F06_LAST));
  f06_set(*next,id,F06_H_PRIORITY,req->priority);
  f06_set(*next,id,F06_H_KIND,req->analysis_kind);
  f06_set(*next,id,F06_H_STATUS,1); // queued: Science has NOT analyzed it
  f06_set(*next,id,F06_H_CLASS,val(next->world,c,F06_SEEN_CLASS));
  f06_set(*next,id,F06_H_CONFIDENCE,val(next->world,c,F06_CONFIDENCE));
  f06_set(*next,id,F06_H_TRANSPONDER,val(next->world,c,F06_SEEN_TRANSPONDER));
  f06_set(*next,id,F06_H_X,val(next->world,c,F06_VISIBLE_X));
  f06_set(*next,id,F06_H_Y,val(next->world,c,F06_VISIBLE_Y));
  f06_set(*next,id,F06_H_Z,val(next->world,c,F06_VISIBLE_Z));
  (void)event(*next,*s->content.catalog(),who.id,6010,F04_OK,req->request_key,id);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_science_view(s->c->world,id);
  return F04_OK;
 });
}
uint32_t f06_science_queue_page(F04Session* s,F04Ref who,U offset,
 F06ScienceView* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  const auto handoffs=all(s->c->world,"f06_handoff");
  *total=handoffs.size();need(offset<=*total,F04_ARGUMENT);
  *written=std::min(capacity,*total-offset);
  for(U i=0;i<*written;++i)out[i]=f06_science_view(s->c->world,
   handoffs[static_cast<size_t>(offset+i)]);
  return F04_OK;
 });
}


namespace {
F06PowerView f06_power_view(const WorldState& w,U id) {
 return {val(w,id,F06_PWR_PUBLIC),val(w,id,F06_PWR_CREATED),
  val(w,id,F06_PWR_EXPIRY),val(w,id,F06_PWR_DECIDED),
  static_cast<uint32_t>(val(w,id,F06_PWR_AMOUNT)),
  static_cast<uint32_t>(val(w,id,F06_PWR_STATE))};
}
U f06_power_by_public(const WorldState& w,U public_id) {
 for(U id:all(w,"f06_power_request"))if(val(w,id,F06_PWR_PUBLIC)==public_id)return id;
 return 0;
}
}
uint32_t f06_request_power(F04Session* s,F04Ref who,const F06PowerRequest* req,F06PowerView* out) {
 if(!req || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  need(req->request_key && req->request_key<=FOREVER &&
   req->extra_power_permille>=1 && req->extra_power_permille<=1000 &&
   req->duration_seconds>=1 && req->duration_seconds<=28800,F04_ARGUMENT);
  const auto& w=s->c->world;
  for(U id:all(w,"f06_power_request"))if(val(w,id,F06_PWR_KEY)==req->request_key) {
   need(ref(w,id,PERSON)==who.id && val(w,id,F06_PWR_AMOUNT)==req->extra_power_permille &&
    val(w,id,F06_PWR_EXPIRY)-val(w,id,F06_PWR_CREATED)==req->duration_seconds,F04_OVERLAP);
   *out=f06_power_view(w,id);return F04_OK;
  }
  need(req->expected_revision==w.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  (void)scan_station(*next,who.id);
  need(all(next->world,"f06_power_request").size()<256,F04_CAPACITY);
  const U now=next->time.now();need(now<=FOREVER-req->duration_seconds,F04_ARGUMENT);
  const U id=make(*next,*s->content.catalog(),"f06_power_request");
  link(*next,id,SHIP,1);link(*next,id,PERSON,who.id);
  const U public_id=f06_public(req->request_key,val(next->world,1,SHIP_ID));
  need(!f06_power_by_public(next->world,public_id),F04_CAPACITY);
  f06_set(*next,id,F06_PWR_KEY,req->request_key);
  f06_set(*next,id,F06_PWR_PUBLIC,public_id);
  f06_set(*next,id,F06_PWR_CREATED,now);
  f06_set(*next,id,F06_PWR_EXPIRY,now+req->duration_seconds);
  f06_set(*next,id,F06_PWR_AMOUNT,req->extra_power_permille);
  f06_set(*next,id,F06_PWR_STATE,F06_POWER_QUEUED);
  (void)event(*next,*s->content.catalog(),who.id,6030,F04_OK,req->request_key,id);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_power_view(s->c->world,id);return F04_OK;
 });
}
uint32_t f06_decide_power(F04Session* s,F04Ref who,U revision,U public_id,
 uint32_t decision,F06PowerView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  need(decision==F06_POWER_APPROVED || decision==F06_POWER_DENIED,F04_ARGUMENT);
  const auto& w=s->c->world;const U id=f06_power_by_public(w,public_id);
  need(id,F04_UNAVAILABLE);
  const U now=s->c->time.now();
  need(commander(w,now)==who.id || head(w,who.id,F04_OPERATIONS,now),F04_DENIED);
  const U old=val(w,id,F06_PWR_STATE);
  if(old==decision && ref(w,id,ISSUER)==who.id) {
   *out=f06_power_view(w,id);return F04_OK;
  }
  need(old==F06_POWER_QUEUED && now<val(w,id,F06_PWR_EXPIRY),F04_EXPIRED);
  need(revision==w.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  link(*next,id,ISSUER,who.id);f06_set(*next,id,F06_PWR_STATE,decision);
  f06_set(*next,id,F06_PWR_DECIDED,now);
  (void)event(*next,*s->content.catalog(),who.id,6031,F04_OK,decision,id);
  // Approval does not assign actual power. Engineering/Operations host must.
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_power_view(s->c->world,id);return F04_OK;
 });
}
uint32_t f06_power_requests_page(F04Session* s,F04Ref who,U offset,F06PowerView* out,
 U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  const auto ids=all(s->c->world,"f06_power_request");
  *total=ids.size();need(offset<=*total,F04_ARGUMENT);
  *written=std::min<U>(capacity,*total-offset);
  for(U i=0;i<*written;++i)out[i]=f06_power_view(s->c->world,ids[static_cast<size_t>(offset+i)]);
  return F04_OK;
 });
}
uint32_t f06_tracking_status(F04Session* s,F04Ref who,F06TrackView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  const auto& w=s->c->world;
  const U cap=f06_tracking_capacity(w),used=f06_tracking_used(w);
  // "available" means FREE slots, not total installed capacity.
  *out={0,0,0,static_cast<uint32_t>(used),static_cast<uint32_t>(cap>used?cap-used:0),
   static_cast<uint32_t>(used>cap)};
  return F04_OK;
 });
}
uint32_t f06_set_tracking(F04Session* s,F04Ref who,U revision,U public_id,
 uint32_t mode,F06TrackView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  need(mode<=F06_TRACK_PRIORITY,F04_ARGUMENT);
  auto next=std::make_unique<Campaign>(*s->c);
  (void)scan_station(*next,who.id);
  const U contact=f06_contact_for_public(next->world,public_id);
  need(contact,F04_UNAVAILABLE);
  const U current=val(next->world,contact,F06_TRACK_MODE);
  need(mode==F06_TRACK_PASSIVE ||
   val(next->world,contact,F06_STATUS)==F06_ACTIVE,F04_UNAVAILABLE);
  const U cap=f06_tracking_capacity(next->world),used=f06_tracking_used(next->world);
  if(current!=mode){
   need(revision==next->world.revision(),F04_STALE);
   need(used>=f06_track_cost(current),F04_INTERNAL);
   const U requested=used-f06_track_cost(current)+f06_track_cost(mode);
   // After physical damage, used may exceed capacity. Always permit a
   // reduction to release slots, even if the remaining total is overloaded.
   // Never permit increases above the actual current hardware capacity.
   need(requested<=used || requested<=cap,F04_CAPACITY);
   f06_set(*next,contact,F06_TRACK_MODE,mode);
   f06_set(*next,contact,F06_TRACK_UPDATED,next->time.now());
   (void)event(*next,*s->content.catalog(),who.id,6020,F04_OK,mode,contact);
   need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  }
  const auto& w=s->c->world;const U capacity=f06_tracking_capacity(w),allocated=f06_tracking_used(w);
  *out={public_id,val(w,contact,F06_TRACK_UPDATED),static_cast<uint32_t>(val(w,contact,F06_TRACK_MODE)),
   static_cast<uint32_t>(allocated),static_cast<uint32_t>(capacity>allocated?capacity-allocated:0),
   static_cast<uint32_t>(allocated>capacity)};
  return F04_OK;
 });
}
uint32_t f06_host_array_state(F04Session* s,const F06ArrayInput* in,F06ArrayView* out) {
 if(!in || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(in->expected_revision==s->c->world.revision(),F04_STALE);
  need(!in->reserved && in->capability_permille<=1000 &&
   in->power_permille<=1000 && in->integrity_permille<=1000 &&
   in->short_enabled<=1 && in->long_enabled<=1 && in->focused_enabled<=1,
   F04_ARGUMENT);
  // Once individual physical arrays are installed, their Host is the only
  // authority. A legacy aggregate write must not silently be ignored.
  need(all(s->c->world,"f06_section_array").empty(),F04_SCOPE);
  auto next=std::make_unique<Campaign>(*s->c);
  const auto rows=all(next->world,"f06_array");
  U id=rows.empty()?0:rows[0];
  if(!id) {id=make(*next,*s->content.catalog(),"f06_array");link(*next,id,SHIP,1);}
  f06_set(*next,id,F06_ARRAY_CAPABILITY,in->capability_permille);
  f06_set(*next,id,F06_ARRAY_POWER,in->power_permille);
  f06_set(*next,id,F06_ARRAY_INTEGRITY,in->integrity_permille);
  f06_set(*next,id,F06_ARRAY_SHORT,in->short_enabled);
  f06_set(*next,id,F06_ARRAY_LONG,in->long_enabled);
  f06_set(*next,id,F06_ARRAY_FOCUS,in->focused_enabled);
  f06_poll(*next,*s->content.catalog(),0,false);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_array_state(s->c->world);
  return F04_OK;
 });
}
uint32_t f06_array_status(F04Session* s,F04Ref who,F06ArrayView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  *out=f06_array_state(s->c->world);
  return F04_OK;
 });
}
/* The spatial feed never exposes world keys or signal EntityIds to operator
 * APIs. All writes and resulting detections commit with one Core revision. */
uint32_t f06_configuration_status(F04Session* s,F04Ref who,F06ConfigView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  *out=f06_current_config(s->c->world);return F04_OK;
 });
}
uint32_t f06_configure(F04Session* s,F04Ref who,
 const F06ConfigRequest* req,F06ConfigView* out) {
 if(!req || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  need(req->sensitivity_permille>=400 && req->sensitivity_permille<=1000 &&
   req->resolution_permille>=400 && req->resolution_permille<=1000 &&
   req->compensation_permille<=500 &&
   U(req->sensitivity_permille)+req->resolution_permille+2*U(req->compensation_permille)<=2100 &&
   req->preset_id<=6 && req->preferred_update_seconds>=1 &&
   req->preferred_update_seconds<=900 && !req->reserved,F04_ARGUMENT);
  need(req->expected_revision==s->c->world.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  (void)scan_station(*next,who.id);
  const auto arrays=f06_array_state(next->world);
  need(arrays.capability_permille && arrays.power_permille &&
    arrays.integrity_permille,F04_UNAVAILABLE);
  auto rows=all(next->world,"f06_configuration");
  U id=rows.empty()?0:rows[0];
  if(!id){id=make(*next,*s->content.catalog(),"f06_configuration");link(*next,id,SHIP,1);}
  f06_set(*next,id,F06_CONFIG_SENS,req->sensitivity_permille);
  f06_set(*next,id,F06_CONFIG_RES,req->resolution_permille);
  f06_set(*next,id,F06_CONFIG_COMP,req->compensation_permille);
  f06_set(*next,id,F06_CONFIG_PRESET,req->preset_id);
  f06_set(*next,id,F06_CONFIG_INTERVAL,req->preferred_update_seconds);
  // Hardware power is unchanged. Re-evaluate the already-running passive
  // watch now, so a weaker setting cannot leave stale "active" contacts until
  // a later clock advance. This is NOT a commanded/active scan or world spawn.
  f06_poll(*next,*s->content.catalog(),0,false);
  (void)event(*next,*s->content.catalog(),who.id,6041,F04_OK,req->preset_id,0);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_current_config(s->c->world);return F04_OK;
 });
}
uint32_t f06_search_contacts_page(F04Session* s,F04Ref who,const F06ContactQuery* q,
 U offset,F06ContactView* out,U capacity,U* written,U* total) {
 if(!q || !written || !total || (!out && capacity))return F04_ARGUMENT;
 *written=*total=0;
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  need(q->status<=F06_LOST && q->min_confidence_permille<=1000 &&
    q->max_distance_milli_au<=50000 && q->observed_category<=F06_CATEGORY_ASTEROID,F04_ARGUMENT);
  std::vector<U> ids;
  for(U id:all(s->c->world,"f06_contact")){
   const auto c=f06_view(s->c->world,id);
   if(q->status && c.status!=q->status)continue;
   if(q->confirmed_class_id && c.class_id!=q->confirmed_class_id)continue;
   if(q->observed_category && c.observed_category!=q->observed_category)continue;
   if(c.confidence_permille<q->min_confidence_permille)continue;
   if(q->max_distance_milli_au && c.distance_milli_au>q->max_distance_milli_au)continue;
   ids.push_back(id);
  }
  *total=ids.size();need(offset<=*total,F04_ARGUMENT);
  *written=std::min<U>(capacity,*total-offset);
  for(U i=0;i<*written;++i)out[i]=f06_view(s->c->world,ids[static_cast<size_t>(offset+i)]);
  return F04_OK;
 });
}
uint32_t f06_diagnostics(F04Session* s,F04Ref who,F06DiagnosticView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  *out=f06_diagnostic_state(*s->c);return F04_OK;
 });
}
uint32_t f06_run_self_test(F04Session* s,F04Ref who,U revision,F06DiagnosticView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  need(revision==s->c->world.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  (void)scan_station(*next,who.id);
  const auto state=f06_diagnostic_state(*next);
  (void)event(*next,*s->content.catalog(),who.id,6040,F04_OK,state.state,0);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=state;return F04_OK;
 });
}
uint32_t f06_host_install_profile(F04Session* s,const F06ProfileInstall* in,F06ProfileView* out) {
 if(!in || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(!in->reserved && in->profile_id<=5,F04_ARGUMENT);
  need(in->expected_revision==s->c->world.revision(),F04_STALE);
  need(all(s->c->world,"f06_section_array").empty() || in->profile_id==5,F04_SCOPE);
  auto next=std::make_unique<Campaign>(*s->c);
  auto arrays=all(next->world,"f06_array");
  U id=arrays.empty()?0:arrays[0];
  if(!id) {
   id=make(*next,*s->content.catalog(),"f06_array");link(*next,id,SHIP,1);
   f06_set(*next,id,F06_ARRAY_CAPABILITY,1000);
   f06_set(*next,id,F06_ARRAY_POWER,1000);
   f06_set(*next,id,F06_ARRAY_INTEGRITY,1000);
   f06_set(*next,id,F06_ARRAY_SHORT,1);
   f06_set(*next,id,F06_ARRAY_LONG,1);
   f06_set(*next,id,F06_ARRAY_FOCUS,1);
  }
  f06_set(*next,id,F06_ARRAY_PROFILE,in->profile_id);
  f06_poll(*next,*s->content.catalog(),0,false);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_profile_view(s->c->world);return F04_OK;
 });
}
uint32_t f06_installed_profile(F04Session* s,F04Ref who,F06ProfileView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  *out=f06_profile_view(s->c->world);return F04_OK;
 });
}
uint32_t f06_host_world_snapshot(F04Session* s,const F06WorldSnapshot* in,F06WorldReceipt* out) {
 if(!in || !out || (in->entity_count && !in->entities))return F04_ARGUMENT;
 *out={};
 return call(s,[&]()->uint32_t{
  need(in->expected_revision==s->c->world.revision(),F04_STALE);
  need(in->snapshot_tick==s->c->time.now() && in->source_revision &&
    in->source_revision<=FOREVER && in->entity_count<=2048,F04_ARGUMENT);
  const auto valid=[](int64_t n){return n>=-100000000 && n<=100000000;};
  need(valid(in->observer_x_milli_au) && valid(in->observer_y_milli_au) &&
    valid(in->observer_z_milli_au),F04_ARGUMENT);
  const auto prior=all(s->c->world,"f06_world_feed");
  if(!prior.empty())need(in->source_revision>val(s->c->world,prior[0],F06_WORLD_REV),F04_STALE);
  std::vector<const F06WorldEntity*> rows;
  rows.reserve(static_cast<size_t>(in->entity_count));
  for(U n=0;n<in->entity_count;++n) {
   const auto& e=in->entities[n];
   need(e.world_entity_key && e.world_entity_key<=FOREVER &&
     e.transponder_id<=FOREVER && e.strength_permille<=1000 &&
     e.interference_permille<=550 && e.active<=1 &&
     e.observed_exit_evidence<=F06_EXIT_OBSERVED_OUT_OF_RANGE &&
     e.signature_category<=F06_CATEGORY_ASTEROID &&
     valid(e.absolute_x_milli_au) && valid(e.absolute_y_milli_au) &&
     valid(e.absolute_z_milli_au) &&
     valid(e.absolute_x_milli_au-in->observer_x_milli_au) &&
     valid(e.absolute_y_milli_au-in->observer_y_milli_au) &&
     valid(e.absolute_z_milli_au-in->observer_z_milli_au),F04_ARGUMENT);
   rows.push_back(&e);
  }
  std::sort(rows.begin(),rows.end(),[](const auto* a,const auto* b){
    return a->world_entity_key<b->world_entity_key;
  });
  for(size_t i=1;i<rows.size();++i)
   need(rows[i-1]->world_entity_key!=rows[i]->world_entity_key,F04_ARGUMENT);
  auto next=std::make_unique<Campaign>(*s->c);
  U feed=prior.empty()?0:prior[0];
  if(!feed){feed=make(*next,*s->content.catalog(),"f06_world_feed");link(*next,feed,SHIP,1);}
  f06_set(*next,feed,F06_WORLD_REV,in->source_revision);
  f06_set(*next,feed,F06_WORLD_TICK,in->snapshot_tick);
  f06_set(*next,feed,F06_WORLD_ORIGIN_X,f06_zigzag(in->observer_x_milli_au));
  f06_set(*next,feed,F06_WORLD_ORIGIN_Y,f06_zigzag(in->observer_y_milli_au));
  f06_set(*next,feed,F06_WORLD_ORIGIN_Z,f06_zigzag(in->observer_z_milli_au));
  std::map<U,U> existing;
  for(U id:all(next->world,"f06_signal"))
   if(has(next->world,id,F06_WORLD_ID))
    existing.emplace(val(next->world,id,F06_WORLD_ID),id);
  std::set<U> incoming;
  U created=0,updated=0,retired=0;
  for(const F06WorldEntity* source:rows){
   incoming.insert(source->world_entity_key);
   const auto it=existing.find(source->world_entity_key);
   U id=it==existing.end()?0:it->second;
   if(!id){
    need(all(next->world,"f06_signal").size()<2048,F04_CAPACITY);
    id=make(*next,*s->content.catalog(),"f06_signal");link(*next,id,SHIP,1);
    f06_set(*next,id,F06_WORLD_ID,source->world_entity_key);++created;
   }else ++updated;
   f06_set(*next,id,F06_WORLD_TICK,in->snapshot_tick);
   f06_set(*next,id,F06_X,f06_zigzag(source->absolute_x_milli_au-in->observer_x_milli_au));
   f06_set(*next,id,F06_Y,f06_zigzag(source->absolute_y_milli_au-in->observer_y_milli_au));
   f06_set(*next,id,F06_Z,f06_zigzag(source->absolute_z_milli_au-in->observer_z_milli_au));
   f06_set(*next,id,F06_STRENGTH,source->strength_permille);
   f06_set(*next,id,F06_INTERFERENCE,source->interference_permille);
   f06_set(*next,id,F06_CLASS,source->class_id);
   f06_set(*next,id,F06_TRANSPONDER,source->transponder_id);
   f06_set(*next,id,F06_CATEGORY,source->signature_category);
   f06_set(*next,id,F06_ACTIVE_FLAG,source->active);
   f06_set(*next,id,F06_EXIT,source->observed_exit_evidence);
  }
  for(const auto& [world_id,id]:existing)if(!incoming.contains(world_id)){
   if(val(next->world,id,F06_ACTIVE_FLAG)){++retired;
    f06_set(*next,id,F06_ACTIVE_FLAG,0);
    f06_set(*next,id,F06_EXIT,F06_EXIT_UNKNOWN);
    f06_set(*next,id,F06_WORLD_TICK,in->snapshot_tick);
   }
  }
  f06_poll(*next,*s->content.catalog(),0,false);
  need(schema(*next),F04_INTERNAL);
  s->c.swap(next);s->index_revision=UINT64_MAX;
  *out={s->c->world.revision(),in->source_revision,
    static_cast<uint32_t>(created),static_cast<uint32_t>(updated),
    static_cast<uint32_t>(retired)};
  return F04_OK;
 });
}
uint32_t f06_host_signal(F04Session* s,const F06SignalInput* in,F06SignalReceipt* out) {
 if(!in || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(in->expected_revision==s->c->world.revision(),F04_STALE);
  need(!in->reserved && in->strength_permille<=1000 && in->interference_permille<=550 &&
   in->active<=1 && in->observed_exit_evidence<=F06_EXIT_OBSERVED_OUT_OF_RANGE &&
   in->signature_category<=F06_CATEGORY_ASTEROID,
   F04_ARGUMENT);
  for(int64_t coordinate:{in->relative_x_milli_au,in->relative_y_milli_au,in->relative_z_milli_au})
   need(coordinate>=-100000000 && coordinate<=100000000,F04_ARGUMENT);
  need(in->transponder_id<=FOREVER,F04_ARGUMENT);
  auto next=std::make_unique<Campaign>(*s->c);
  U id=in->signal_id;
  if(id)need(type(next->world,id,"f06_signal"),F04_SCOPE);
  else {
   need(all(next->world,"f06_signal").size()<2048,F04_CAPACITY);
   id=make(*next,*s->content.catalog(),"f06_signal");link(*next,id,SHIP,1);
  }
  f06_set(*next,id,F06_X,f06_zigzag(in->relative_x_milli_au));
  f06_set(*next,id,F06_Y,f06_zigzag(in->relative_y_milli_au));
  f06_set(*next,id,F06_Z,f06_zigzag(in->relative_z_milli_au));
  f06_set(*next,id,F06_STRENGTH,in->strength_permille);
  f06_set(*next,id,F06_INTERFERENCE,in->interference_permille);
  f06_set(*next,id,F06_CLASS,in->class_id);
  f06_set(*next,id,F06_TRANSPONDER,in->transponder_id);
  f06_set(*next,id,F06_CATEGORY,in->signature_category);
  f06_set(*next,id,F06_ACTIVE_FLAG,in->active);
  f06_set(*next,id,F06_EXIT,in->observed_exit_evidence);
  f06_poll(*next,*s->content.catalog(),0,false);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out={id,s->c->world.revision()};return F04_OK;
 });
}
uint32_t f06_contacts_page(F04Session* s,F04Ref who,uint32_t status,U offset,
 F06ContactView* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);need(status<=F06_LOST,F04_ARGUMENT);
  std::vector<U> ids;
  for(U id:all(s->c->world,"f06_contact"))
   if(!status || val(s->c->world,id,F06_STATUS)==status)ids.push_back(id);
  *total=ids.size();need(offset<=*total,F04_ARGUMENT);
  *written=std::min(capacity,*total-offset);
  for(U i=0;i<*written;++i)out[i]=f06_view(s->c->world,ids[static_cast<size_t>(offset+i)]);
  return F04_OK;
 });
}
uint32_t f06_notices_page(F04Session* s,F04Ref who,U after,
 F06NoticeView* out,U capacity,U* written,uint32_t* more) {
 if(!written || !more || (!out && capacity))return F04_ARGUMENT;*written=0;*more=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  const auto& w=s->c->world;
  // Cursor is opaque. No raw Core EntityId ever leaves this sensor endpoint.
  bool past=after==0;
  for(U id:all(w,"event")) {
   const U op=val(w,id,OP);
   if(op<6001 || op>6005)continue;
   const U token=f06_public(id,val(w,1,SHIP_ID));
   if(!past) {if(token==after)past=true;continue;}
   if(*written>=capacity){*more=1;break;}
   out[(*written)++]={token,val(w,ref(w,id,TARGET),F06_PUBLIC_ID),
     val(w,id,TICK),static_cast<uint32_t>(op-6000)};
  }
  need(past,F04_ARGUMENT);
  return F04_OK;
 });
}
namespace {
F06ResultView f06_result_view(const WorldState& w,U id) {
 const U contact=ref(w,id,F06_CONTACT_REF);
 return {val(w,id,F06_O_PUBLIC),val(w,contact,F06_PUBLIC_ID),
   val(w,id,F06_O_TICK),
   f06_unzigzag(val(w,id,F06_O_X)),
   f06_unzigzag(val(w,id,F06_O_Y)),
   f06_unzigzag(val(w,id,F06_O_Z)),
   static_cast<uint32_t>(val(w,id,F06_O_CONF)),
   static_cast<uint32_t>(val(w,id,F06_O_DISTANCE)),
   static_cast<uint32_t>(val(w,id,F06_O_CLASS))};
}
U f06_result_by_public(const WorldState& w,U id) {
 for(U entity:all(w,"f06_observation"))if(val(w,entity,F06_O_PUBLIC)==id)return entity;
 return 0;
}
void f06_record_focus(Campaign& c,const ContentCatalog& cat,U contact,U actor) {
 need(all(c.world,"f06_observation").size()<1024,F04_CAPACITY);
 const U id=make(c,cat,"f06_observation");
 link(c,id,SHIP,1);link(c,id,PERSON,actor);link(c,id,F06_CONTACT_REF,contact);
 const auto view=f06_view(c.world,contact);
 const U pub=f06_public(id^UINT64_C(0x205c0de),val(c.world,1,SHIP_ID));
 need(!f06_result_by_public(c.world,pub),F04_CAPACITY);
 f06_set(c,id,F06_O_PUBLIC,pub);
 f06_set(c,id,F06_O_TICK,c.time.now());
 f06_set(c,id,F06_O_CONF,view.confidence_permille);
 f06_set(c,id,F06_O_DISTANCE,view.distance_milli_au);
 f06_set(c,id,F06_O_CLASS,view.class_id);
 f06_set(c,id,F06_O_X,f06_zigzag(view.observed_x_milli_au));
 f06_set(c,id,F06_O_Y,f06_zigzag(view.observed_y_milli_au));
 f06_set(c,id,F06_O_Z,f06_zigzag(view.observed_z_milli_au));
 (void)event(c,cat,actor,6050,F04_OK,0,id);
}
}
uint32_t f06_results_page(F04Session* s,F04Ref who,U public_contact,U offset,
 F06ResultView* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  if(public_contact)need(f06_contact_for_public(s->c->world,public_contact),F04_UNAVAILABLE);
  std::vector<U> ids;
  for(U id:all(s->c->world,"f06_observation")) {
   if(public_contact && val(s->c->world,ref(s->c->world,id,F06_CONTACT_REF),
      F06_PUBLIC_ID)!=public_contact)continue;
   ids.push_back(id);
  }
  *total=ids.size();need(offset<=*total,F04_ARGUMENT);
  *written=std::min<U>(capacity,*total-offset);
  for(U i=0;i<*written;++i)out[i]=f06_result_view(s->c->world,ids[static_cast<size_t>(offset+i)]);
  return F04_OK;
 });
}
uint32_t f06_compare_results(F04Session* s,F04Ref who,U a,U b,F06ComparisonView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  const U older=f06_result_by_public(s->c->world,a),newer=f06_result_by_public(s->c->world,b);
  need(older && newer,F04_UNAVAILABLE);
  need(ref(s->c->world,older,F06_CONTACT_REF)==ref(s->c->world,newer,F06_CONTACT_REF),
    F04_ARGUMENT);
  need(val(s->c->world,older,F06_O_TICK)<=val(s->c->world,newer,F06_O_TICK),
    F04_ARGUMENT);
  const auto x=f06_result_view(s->c->world,older),y=f06_result_view(s->c->world,newer);
  *out={a,b,x.contact_id,
    int64_t(y.confidence_permille)-int64_t(x.confidence_permille),
    int64_t(y.distance_milli_au)-int64_t(x.distance_milli_au),
    static_cast<uint32_t>(x.class_id!=y.class_id)};
  return F04_OK;
 });
}
uint32_t f06_focus(F04Session* s,F04Ref who,U revision,U contact,F06ContactView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);need(revision==s->c->world.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  (void)scan_station(*next,who.id); // F04 present, qualified and on duty
  const auto hw=f06_array_state(next->world);
  need(hw.focused_enabled && hw.capability_permille && hw.power_permille && hw.integrity_permille,F04_UNAVAILABLE);
  const U internal=f06_contact_for_public(next->world,contact);
  need(internal,F04_UNAVAILABLE);
  f06_poll(*next,*s->content.catalog(),internal,true);
  f06_record_focus(*next,*s->content.catalog(),internal,who.id);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_view(s->c->world,internal);return F04_OK;
 });
}

uint32_t f06_scan_area(F04Session* s,F04Ref who,
 const F06AreaRequest* req,F06AreaReceipt* out) {
 if(!req || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  need(!req->reserved && req->radius_milli_au>=1 &&
   req->radius_milli_au<=3000,F04_ARGUMENT);
  const auto valid_coordinate=[](int64_t n){return n>=-50000 && n<=50000;};
  need(valid_coordinate(req->center_x_milli_au) &&
   valid_coordinate(req->center_y_milli_au) &&
   valid_coordinate(req->center_z_milli_au),F04_ARGUMENT);
  const long double cx=req->center_x_milli_au,cy=req->center_y_milli_au,cz=req->center_z_milli_au;
  need(cx*cx+cy*cy+cz*cz<=static_cast<long double>(50000)*50000,F04_ARGUMENT);
  need(req->expected_revision==s->c->world.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  (void)scan_station(*next,who.id);
  const auto hw=f06_array_state(next->world);
  need(hw.focused_enabled && hw.capability_permille &&
    hw.power_permille && hw.integrity_permille,F04_UNAVAILABLE);
  U observed=0,created=0;
  for(U signal:all(next->world,"f06_signal")) {
   const int64_t dx=f06_unzigzag(val(next->world,signal,F06_X))-req->center_x_milli_au;
   const int64_t dy=f06_unzigzag(val(next->world,signal,F06_Y))-req->center_y_milli_au;
   const int64_t dz=f06_unzigzag(val(next->world,signal,F06_Z))-req->center_z_milli_au;
   const uint64_t sq=uint64_t(dx*dx)+uint64_t(dy*dy)+uint64_t(dz*dz);
   if(sq>U(req->radius_milli_au)*req->radius_milli_au)continue;
   const U before=f06_contact_for(next->world,signal);
   f06_apply(*next,*s->content.catalog(),signal,true,true);
   const U after=f06_contact_for(next->world,signal);
   if(after && val(next->world,after,F06_STATUS)==F06_ACTIVE) {
    ++observed;
    if(!before)++created;
   }
  }
  // This is an explicit operator action, unlike free continuous watch.
  (void)event(*next,*s->content.catalog(),who.id,6021,F04_OK,0,0);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out={s->c->world.revision(),observed,created};return F04_OK;
 });
}

// Additive F06-BIS runtime within the exact same Core campaign.
#include "f06_bis.inc"
