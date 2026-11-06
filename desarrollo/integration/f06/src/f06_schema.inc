// Shapes for the same Core WorldState used by F04/F05.
namespace {
bool f06_shape(const WorldState& w,U id,std::set<U>& allowed,
 std::set<U>& required,std::set<U>& ar,std::set<U>& rr) {
 if(type(w,id,"f06_environment")) {
  allowed={F06_ENV_REV,F06_ENV_EM,F06_ENV_THERM,F06_ENV_GRAV,F06_ENV_SUB,F06_ENV_BIO};
  required=allowed;ar={SHIP};rr=ar;return true;
 }
 if(type(w,id,"f06_section_array")) {
  allowed={F06_SEC_ID,F06_SEC_LINK,F06_SEC_CAP,F06_SEC_PWR,F06_SEC_INT,
   F06_SEC_SHORT,F06_SEC_LONG,F06_SEC_FOCUS};
  required=allowed;ar={SHIP};rr=ar;return true;
 }
 if(type(w,id,"f06_timed_scan")) {
  allowed={F06_TIMED_KEY,F06_TIMED_PUBLIC,F06_TIMED_START,F06_TIMED_DUE,F06_TIMED_NOMINAL,
   F06_TIMED_COST,F06_TIMED_STATUS,F06_TIMED_RESULT};
  required=allowed;required.erase(F06_TIMED_RESULT);
  ar={SHIP,PERSON,F06_CONTACT_REF};rr=ar;return true;
 }
 if(type(w,id,"f06_science_report")) {
  allowed={F06_SCI_KEY,F06_SCI_PUBLIC,F06_SCI_INSTRUMENT,F06_SCI_TICK,
   F06_SCI_TEMP,F06_SCI_PRESS,F06_SCI_WATER,F06_SCI_N2,F06_SCI_O2,
   F06_SCI_CO2,F06_SCI_SOLID,F06_SCI_BIO,F06_SCI_QUALITY,F06_SCI_CONF,
   F06_SCI_PLANET};
  required=allowed;
  ar={SHIP,F06_HANDOFF_REF,F06_OBSERVATION_REF};rr=ar;return true;
 }
 if(type(w,id,"f06_power_request")) {
  allowed={F06_PWR_KEY,F06_PWR_PUBLIC,F06_PWR_CREATED,F06_PWR_EXPIRY,
   F06_PWR_AMOUNT,F06_PWR_STATE,F06_PWR_DECIDED,F06_PWR_APPLIED,F06_PWR_ALLOC_REV,F06_PWR_APPLIED_AT};
  required={F06_PWR_KEY,F06_PWR_PUBLIC,F06_PWR_CREATED,F06_PWR_EXPIRY,
   F06_PWR_AMOUNT,F06_PWR_STATE};
  ar={SHIP,PERSON,ISSUER};rr={SHIP,PERSON};return true;
 }
 if(type(w,id,"f06_handoff")) {
  allowed={F06_H_KEY,F06_H_PUBLIC,F06_H_TIME,F06_H_OBSERVED,F06_H_PRIORITY,F06_H_KIND,
   F06_H_STATUS,F06_H_CLASS,F06_H_CONFIDENCE,F06_H_TRANSPONDER,F06_H_X,F06_H_Y,F06_H_Z};
  required=allowed;ar={SHIP,PERSON,F06_CONTACT_REF};rr=ar;return true;
 }
 if(type(w,id,"f06_array")) {
  allowed={F06_ARRAY_CAPABILITY,F06_ARRAY_POWER,F06_ARRAY_INTEGRITY,
   F06_ARRAY_SHORT,F06_ARRAY_LONG,F06_ARRAY_FOCUS,F06_ARRAY_PROFILE};
  required=allowed;required.erase(F06_ARRAY_PROFILE);
  ar={SHIP};rr=ar;return true;
 }
 if(type(w,id,"f06_observation")) {
  allowed={F06_O_PUBLIC,F06_O_TICK,F06_O_CONF,F06_O_DISTANCE,
    F06_O_CLASS,F06_O_X,F06_O_Y,F06_O_Z};
  required=allowed;ar={SHIP,PERSON,F06_CONTACT_REF};rr=ar;return true;
 }
 if(type(w,id,"f06_configuration")) {
  allowed={F06_CONFIG_SENS,F06_CONFIG_RES,F06_CONFIG_COMP,
   F06_CONFIG_PRESET,F06_CONFIG_INTERVAL};
  required=allowed;ar={SHIP};rr=ar;return true;
 }
 if(type(w,id,"f06_world_feed")) {
  allowed={F06_WORLD_REV,F06_WORLD_TICK,F06_WORLD_ORIGIN_X,
   F06_WORLD_ORIGIN_Y,F06_WORLD_ORIGIN_Z};
  required=allowed;ar={SHIP};rr=ar;return true;
 }
 if(type(w,id,"f06_signal")) {
  allowed={F06_X,F06_Y,F06_Z,F06_STRENGTH,F06_INTERFERENCE,
   F06_CLASS,F06_TRANSPONDER,F06_ACTIVE_FLAG,F06_EXIT,F06_WORLD_ID,F06_WORLD_TICK,F06_CATEGORY};
  required=allowed;required.erase(F06_WORLD_ID);required.erase(F06_WORLD_TICK);required.erase(F06_CATEGORY);
  ar={SHIP};rr=ar;return true;
 }
 if(type(w,id,"f06_contact")) {
  allowed={F06_FIRST,F06_LAST,F06_STATUS,F06_CONFIDENCE,F06_DISTANCE,
   F06_SEEN_CLASS,F06_SEEN_TRANSPONDER,F06_VISIBLE_X,F06_VISIBLE_Y,F06_VISIBLE_Z,F06_LOSS_REASON,F06_PUBLIC_ID,
   F06_TRACK_MODE,F06_TRACK_UPDATED,F06_SEEN_CATEGORY};
  required=allowed;
  required.erase(F06_TRACK_MODE);required.erase(F06_TRACK_UPDATED);required.erase(F06_SEEN_CATEGORY);
  ar={SHIP,F06_SIGNAL_REF};rr=ar;return true;
 }
 return false;
}
bool f06_schema(const Campaign& c) {
 const auto& w=c.world;
 std::set<U> signals,public_ids;
 std::set<U> observation_ids;
 const auto observations=all(w,"f06_observation");
 if(observations.size()>1024)return false;
 for(U id:observations){
  if(!val(w,id,F06_O_PUBLIC) ||
   !observation_ids.insert(val(w,id,F06_O_PUBLIC)).second ||
   !type(w,ref(w,id,F06_CONTACT_REF),"f06_contact") ||
   val(w,id,F06_O_TICK)>c.time.now() ||
   val(w,id,F06_O_CONF)>1000 ||
   val(w,id,F06_O_DISTANCE)>50000)return false;
 }
 std::set<U> environment_revisions;
 const auto env=all(w,"f06_environment");
 if(env.size()>1)return false;
 for(U id:env){
  if(!val(w,id,F06_ENV_REV) || !environment_revisions.insert(val(w,id,F06_ENV_REV)).second ||
   val(w,id,F06_ENV_EM)>550 || val(w,id,F06_ENV_THERM)>550 ||
   val(w,id,F06_ENV_GRAV)>550 || val(w,id,F06_ENV_SUB)>550 ||
   val(w,id,F06_ENV_BIO)>550)return false;
 }
 std::set<U> section_ids;
 const auto sections=all(w,"f06_section_array");
 if(sections.size()>2)return false;
 for(U id:sections){
  const U k=val(w,id,F06_SEC_ID);
  if(k<F06_SECTION_SAUCER || k>F06_SECTION_BATTLE ||
   !section_ids.insert(k).second ||
   val(w,id,F06_SEC_LINK)>1 || val(w,id,F06_SEC_CAP)>1000 ||
   val(w,id,F06_SEC_PWR)>1000 || val(w,id,F06_SEC_INT)>1000 ||
   val(w,id,F06_SEC_SHORT)>1 || val(w,id,F06_SEC_LONG)>1 ||
   val(w,id,F06_SEC_FOCUS)>1)return false;
 }
 std::set<U> timed_keys,timed_public;
 if(all(w,"f06_timed_scan").size()>256)return false;
 for(U id:all(w,"f06_timed_scan")){
  const U status=val(w,id,F06_TIMED_STATUS),start=val(w,id,F06_TIMED_START),
   due=val(w,id,F06_TIMED_DUE);
  if(!val(w,id,F06_TIMED_KEY) || !timed_keys.insert(val(w,id,F06_TIMED_KEY)).second ||
   !val(w,id,F06_TIMED_PUBLIC) || !timed_public.insert(val(w,id,F06_TIMED_PUBLIC)).second ||
   !type(w,ref(w,id,F06_CONTACT_REF),"f06_contact") ||
   start>c.time.now() || due<=start || due-start>3600 ||
   val(w,id,F06_TIMED_NOMINAL)<30 || val(w,id,F06_TIMED_NOMINAL)>900 ||
   val(w,id,F06_TIMED_COST)<50 || val(w,id,F06_TIMED_COST)>500 ||
   status<F06_TIMED_QUEUED || status>F06_TIMED_CANCELLED ||
   (has(w,id,F06_TIMED_RESULT) != (status==F06_TIMED_FINISHED)))return false;
 }
 std::set<U> report_keys,report_public,reported_handoffs;
 if(all(w,"f06_science_report").size()>512)return false;
 for(U id:all(w,"f06_science_report")){
  const U h=ref(w,id,F06_HANDOFF_REF),o=ref(w,id,F06_OBSERVATION_REF);
  if(!type(w,h,"f06_handoff") || !type(w,o,"f06_observation") ||
   !val(w,id,F06_SCI_KEY) || !report_keys.insert(val(w,id,F06_SCI_KEY)).second ||
   !val(w,id,F06_SCI_PUBLIC) || !report_public.insert(val(w,id,F06_SCI_PUBLIC)).second ||
   !reported_handoffs.insert(h).second ||
   ref(w,h,F06_CONTACT_REF)!=ref(w,o,F06_CONTACT_REF) ||
   val(w,h,F06_H_STATUS)!=F06_SCIENCE_COMPLETED ||
   val(w,id,F06_SCI_TICK)>c.time.now() ||
   !val(w,id,F06_SCI_INSTRUMENT) ||
   val(w,id,F06_SCI_TEMP)<50 || val(w,id,F06_SCI_TEMP)>2000 ||
   val(w,id,F06_SCI_PRESS)>100000 ||
   val(w,id,F06_SCI_WATER)>1000 ||
   val(w,id,F06_SCI_N2)+val(w,id,F06_SCI_O2)+val(w,id,F06_SCI_CO2)>1000 ||
   val(w,id,F06_SCI_SOLID)>1 || val(w,id,F06_SCI_BIO)>3 ||
   val(w,id,F06_SCI_QUALITY)>1000 || val(w,id,F06_SCI_CONF)>1000 ||
   val(w,id,F06_SCI_PLANET)>F06_PLANET_Y)return false;
 }
 std::set<U> power_keys,power_ids;
 const auto power=all(w,"f06_power_request");
 if(power.size()>256)return false;
 for(U id:power) {
  const U status=val(w,id,F06_PWR_STATE),start=val(w,id,F06_PWR_CREATED),
    expiry=val(w,id,F06_PWR_EXPIRY);
  if(!val(w,id,F06_PWR_KEY) || !power_keys.insert(val(w,id,F06_PWR_KEY)).second ||
     !val(w,id,F06_PWR_PUBLIC) || !power_ids.insert(val(w,id,F06_PWR_PUBLIC)).second ||
     start>c.time.now() || expiry<=start || expiry-start>28800 ||
     val(w,id,F06_PWR_AMOUNT)<1 || val(w,id,F06_PWR_AMOUNT)>1000 ||
     status<F06_POWER_QUEUED || status>F06_POWER_EXPIRED)return false;
  const bool applied=has(w,id,F06_PWR_APPLIED);
  if(applied && (status!=F06_POWER_APPROVED ||
    !val(w,id,F06_PWR_ALLOC_REV) || !has(w,id,F06_PWR_APPLIED_AT) ||
    val(w,id,F06_PWR_APPLIED)>1000 ||
    val(w,id,F06_PWR_APPLIED_AT)>c.time.now()))return false;
  if(!applied && (has(w,id,F06_PWR_ALLOC_REV)||has(w,id,F06_PWR_APPLIED_AT)))return false;
  const bool decided=(status==F06_POWER_APPROVED || status==F06_POWER_DENIED);
  if(decided != bool(ref(w,id,ISSUER)) || decided != has(w,id,F06_PWR_DECIDED))return false;
  if(decided && (val(w,id,F06_PWR_DECIDED)<start ||
     val(w,id,F06_PWR_DECIDED)>=expiry ||
     val(w,id,F06_PWR_DECIDED)>c.time.now()))return false;
 }
 std::set<U> handoff_keys,handoff_ids;
 if(all(w,"f06_handoff").size()>512)return false;
 for(U id:all(w,"f06_handoff")) {
  if(!type(w,ref(w,id,F06_CONTACT_REF),"f06_contact") ||
   !val(w,id,F06_H_KEY) || !handoff_keys.insert(val(w,id,F06_H_KEY)).second ||
   !val(w,id,F06_H_PUBLIC) || !handoff_ids.insert(val(w,id,F06_H_PUBLIC)).second ||
   val(w,id,F06_H_TIME)>c.time.now() ||
   val(w,id,F06_H_OBSERVED)>val(w,id,F06_H_TIME) ||
   val(w,id,F06_H_PRIORITY)<1 || val(w,id,F06_H_PRIORITY)>4 ||
   val(w,id,F06_H_KIND)<1 || val(w,id,F06_H_KIND)>4 ||
   (val(w,id,F06_H_STATUS)!=F06_SCIENCE_QUEUED && val(w,id,F06_H_STATUS)!=F06_SCIENCE_COMPLETED) ||
   val(w,id,F06_H_CONFIDENCE)>1000 ||
   ((val(w,id,F06_H_STATUS)==F06_SCIENCE_COMPLETED)!=
     reported_handoffs.contains(id)))return false;
 }
 const auto cfg=all(w,"f06_configuration");
 if(cfg.size()>1)return false;
 for(U id:cfg){
  const U sens=val(w,id,F06_CONFIG_SENS),res=val(w,id,F06_CONFIG_RES),
   comp=val(w,id,F06_CONFIG_COMP);
  if(sens<400 || sens>1000 || res<400 || res>1000 || comp>500 ||
   sens+res+2*comp>2100 || val(w,id,F06_CONFIG_PRESET)>6 ||
   val(w,id,F06_CONFIG_INTERVAL)<1 || val(w,id,F06_CONFIG_INTERVAL)>900)return false;
 }
 const auto arrays=all(w,"f06_array");
 if(arrays.size()>1)return false;
 if(!sections.empty() && (arrays.empty() || val(w,arrays[0],F06_ARRAY_PROFILE)!=5))return false;
 for(U id:arrays) {
  if(val(w,id,F06_ARRAY_PROFILE)>5 || val(w,id,F06_ARRAY_CAPABILITY)>1000 ||
   val(w,id,F06_ARRAY_POWER)>1000 ||
   val(w,id,F06_ARRAY_INTEGRITY)>1000 ||
   val(w,id,F06_ARRAY_SHORT)>1 || val(w,id,F06_ARRAY_LONG)>1 ||
   val(w,id,F06_ARRAY_FOCUS)>1)return false;
 }
 const auto feeds=all(w,"f06_world_feed");
 if(feeds.size()>1)return false;
 for(U feed:feeds)
  if(!val(w,feed,F06_WORLD_REV) || val(w,feed,F06_WORLD_TICK)>c.time.now())return false;
 std::set<U> world_keys;
 const auto source=all(w,"f06_signal");
 if(source.size()>2048 || all(w,"f06_contact").size()>2048)return false;
 for(U id:source) {
  if(val(w,id,F06_STRENGTH)>1000 || val(w,id,F06_INTERFERENCE)>550 ||
   val(w,id,F06_ACTIVE_FLAG)>1 || val(w,id,F06_EXIT)>F06_EXIT_SENSOR_OFFLINE ||
   val(w,id,F06_CATEGORY)>F06_CATEGORY_ASTEROID ||
   (has(w,id,F06_WORLD_ID) &&
    (!val(w,id,F06_WORLD_ID) || feeds.size()!=1 ||
      !has(w,id,F06_WORLD_TICK) || val(w,id,F06_WORLD_TICK)>c.time.now() ||
      !world_keys.insert(val(w,id,F06_WORLD_ID)).second)))return false;
 }
 for(U id:all(w,"f06_contact")) {
  const U s=ref(w,id,F06_SIGNAL_REF);
  if(!type(w,s,"f06_signal") || !signals.insert(s).second ||
   !val(w,id,F06_PUBLIC_ID) || !public_ids.insert(val(w,id,F06_PUBLIC_ID)).second ||
   val(w,id,F06_FIRST)>val(w,id,F06_LAST) ||
   val(w,id,F06_LAST)>c.time.now() ||
   val(w,id,F06_STATUS)<F06_ACTIVE || val(w,id,F06_STATUS)>F06_LOST ||
   val(w,id,F06_CONFIDENCE)>1000 ||
   val(w,id,F06_LOSS_REASON)>F06_EXIT_SENSOR_OFFLINE ||
   val(w,id,F06_DISTANCE)>50000 ||
   val(w,id,F06_TRACK_MODE)>F06_TRACK_PRIORITY ||
   val(w,id,F06_SEEN_CATEGORY)>F06_CATEGORY_ASTEROID ||
   (has(w,id,F06_TRACK_UPDATED) && val(w,id,F06_TRACK_UPDATED)>c.time.now()))return false; // classification remains historical even if the source changes
 }
 return true;
}
} // namespace
