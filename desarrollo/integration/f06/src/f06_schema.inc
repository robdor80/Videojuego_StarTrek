// Shapes for the same Core WorldState used by F04/F05.
namespace {
bool f06_shape(const WorldState& w,U id,std::set<U>& allowed,
 std::set<U>& required,std::set<U>& ar,std::set<U>& rr) {
 if(type(w,id,"f06_power_request")) {
  allowed={F06_PWR_KEY,F06_PWR_PUBLIC,F06_PWR_CREATED,F06_PWR_EXPIRY,
   F06_PWR_AMOUNT,F06_PWR_STATE,F06_PWR_DECIDED};
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
   F06_CLASS,F06_TRANSPONDER,F06_ACTIVE_FLAG,F06_EXIT,F06_WORLD_ID,F06_WORLD_TICK};
  required=allowed;required.erase(F06_WORLD_ID);required.erase(F06_WORLD_TICK);
  ar={SHIP};rr=ar;return true;
 }
 if(type(w,id,"f06_contact")) {
  allowed={F06_FIRST,F06_LAST,F06_STATUS,F06_CONFIDENCE,F06_DISTANCE,
   F06_SEEN_CLASS,F06_SEEN_TRANSPONDER,F06_VISIBLE_X,F06_VISIBLE_Y,F06_VISIBLE_Z,F06_LOSS_REASON,F06_PUBLIC_ID,
   F06_TRACK_MODE,F06_TRACK_UPDATED};
  required=allowed;
  required.erase(F06_TRACK_MODE);required.erase(F06_TRACK_UPDATED);
  ar={SHIP,F06_SIGNAL_REF};rr=ar;return true;
 }
 return false;
}
bool f06_schema(const Campaign& c) {
 const auto& w=c.world;
 std::set<U> signals,public_ids;
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
   val(w,id,F06_H_STATUS)!=1 ||
   val(w,id,F06_H_CONFIDENCE)>1000)return false;
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
   (has(w,id,F06_TRACK_UPDATED) && val(w,id,F06_TRACK_UPDATED)>c.time.now()))return false; // classification remains historical even if the source changes
 }
 return true;
}
} // namespace
