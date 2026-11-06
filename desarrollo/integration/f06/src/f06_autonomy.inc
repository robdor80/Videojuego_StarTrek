// F06 computer: work autonomously but only from observed contacts.
// This translation unit is included at the tail of f06_bis.inc.
#include "f06_autonomy.h"
namespace {
bool f06_computer_enabled(const WorldState& w) {
 const auto profile=f06_profile_numbers(w);
 return profile.id>=2 && profile.id<=5; // 24th-century modern sensor suites
}
int f06_computer_priority(const WorldState& w,U c) {
 if(val(w,c,F06_STATUS)!=F06_ACTIVE)return -1;
 const U category=val(w,c,F06_SEEN_CATEGORY);
 const U confidence=val(w,c,F06_CONFIDENCE);
 int importance=10;
 switch(category){
  case F06_CATEGORY_UNKNOWN:importance=105;break;
  case F06_CATEGORY_ANOMALY:case F06_CATEGORY_SUBSPACE:importance=120;break;
  case F06_CATEGORY_STARSHIP:importance=115;break;
  case F06_CATEGORY_SHUTTLE:case F06_CATEGORY_PROBE:importance=102;break;
  case F06_CATEGORY_ENERGY:case F06_CATEGORY_WARP:importance=108;break;
  case F06_CATEGORY_PLANET:importance=70;break;
  case F06_CATEGORY_STATION:importance=75;break;
  case F06_CATEGORY_NEBULA:importance=60;break;
  case F06_CATEGORY_MOON:importance=45;break;
  case F06_CATEGORY_STAR:importance=35;break;
  default:importance=40;break;
 }
 // The priority sees ONLY the sensor dossier, never a true hidden class.
 if(!val(w,c,F06_SEEN_CLASS) &&
    (category==F06_CATEGORY_STARSHIP || category==F06_CATEGORY_UNKNOWN))
  importance+=10;
 if(confidence<550)importance+=8;
 return importance;
}
void f06_autonomy_plan(Campaign& c,const ContentCatalog& cat) {
 if(!f06_computer_enabled(c.world))return;
 const auto hw=f06_array_state(c.world);
 if(!hw.focused_enabled || !hw.power_permille || !hw.integrity_permille ||
    !hw.capability_permille || hw.power_permille<400)return;
 const auto ids=all(c.world,"f06_timed_scan");
 if(ids.size()>=240 || all(c.world,"f06_observation").size()>=1010)return;
 U running=0;
 std::set<std::pair<U,U>> attempted;
 for(U id:ids){
  if(val(c.world,id,F06_TIMED_STATUS)==F06_TIMED_QUEUED)++running;
  if(val(c.world,id,F06_TIMED_AUTO))
   attempted.emplace(ref(c.world,id,F06_CONTACT_REF),val(c.world,id,F06_TIMED_GEN));
 }
 if(running>=2)return; // all manual + automatic scans share equipment slots
 std::vector<U> candidates;
 for(U contact:all(c.world,"f06_contact")){
  if(val(c.world,contact,F06_STATUS)!=F06_ACTIVE)continue;
  const U generation=val(c.world,contact,F06_AUTO_GEN);
  if(attempted.contains({contact,generation}))continue;
  const U source=ref(c.world,contact,F06_SIGNAL_REF);
  if(!type(c.world,source,"f06_signal"))continue;
  // Do not queue a known-impossible scan just to display fake activity.
  const U distance=f06_distance(c.world,source);
  const U quality=f06_score(c.world,source,distance,true,true)*
    f06_current_config(c.world).resolution_permille/1000;
  if(!f06_rank(quality))continue;
  candidates.push_back(contact);
 }
 std::sort(candidates.begin(),candidates.end(),[&](U a,U b){
  const int pa=f06_computer_priority(c.world,a),pb=f06_computer_priority(c.world,b);
  return pa!=pb?pa>pb:val(c.world,a,F06_PUBLIC_ID)<val(c.world,b,F06_PUBLIC_ID);
 });
 for(U contact:candidates){
  if(running>=2 || all(c.world,"f06_timed_scan").size()>=240)break;
  const U generation=val(c.world,contact,F06_AUTO_GEN);
  const U confidence=val(c.world,contact,F06_CONFIDENCE);
  const U nominal=90+(1000-confidence)/10;
  const U source=ref(c.world,contact,F06_SIGNAL_REF);
  const U interference=val(c.world,source,F06_INTERFERENCE);
  const U duration=(nominal*(1000+interference)+999)/1000;
  const U now=c.time.now();
  if(now>FOREVER-duration)break;
  const U id=make(c,cat,"f06_timed_scan");
  link(c,id,SHIP,1);link(c,id,F06_CONTACT_REF,contact);
  U key=f06_public(contact^(generation<<16)^UINT64_C(0x420d6f06),
    val(c.world,1,SHIP_ID));
  // A user-supplied key must not collide with a computer-owned operation.
  for(U row:all(c.world,"f06_timed_scan"))if(row!=id &&
    val(c.world,row,F06_TIMED_KEY)==key)
    key=f06_public(key+row,val(c.world,1,SHIP_ID));
  f06_set(c,id,F06_TIMED_KEY,key);
  const U public_id=f06_bis_public(c.world,id);
  need(!f06_timed_by_public(c.world,public_id),F04_CAPACITY);
  f06_set(c,id,F06_TIMED_PUBLIC,public_id);
  f06_set(c,id,F06_TIMED_START,now);
  f06_set(c,id,F06_TIMED_DUE,now+duration);
  f06_set(c,id,F06_TIMED_NOMINAL,nominal);
  f06_set(c,id,F06_TIMED_COST,std::min<U>(500,100+duration/6));
  f06_set(c,id,F06_TIMED_STATUS,F06_TIMED_QUEUED);
  f06_set(c,id,F06_TIMED_AUTO,1);
  f06_set(c,id,F06_TIMED_GEN,generation);
  (void)event(c,cat,0,6090,F04_OK,0,id);
  ++running;
 }
}
uint32_t f06_computer_kind(U op){
 switch(op){
  case 6001:return F06_COMPUTER_CONTACT;
  case 6002:case 6003:return F06_COMPUTER_LOSS;
  case 6004:return F06_COMPUTER_REACQUIRED;
  case 6005:return F06_COMPUTER_IDENTIFIED;
  case 6090:return F06_COMPUTER_ANALYSIS_STARTED;
  case 6091:return F06_COMPUTER_ANALYSIS_DONE;
  case 6092:return F06_COMPUTER_ANALYSIS_UNAVAILABLE;
  default:return 0;
 }
}
} // namespace
uint32_t f06_computer_status(F04Session* s,F04Ref who,F06ComputerStatus* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  const auto& w=s->c->world;
  const auto hw=f06_array_state(w);
  out->tick=s->c->time.now();
  out->autonomous=f06_computer_enabled(w)?1:0;
  out->equipment_offline=(!hw.power_permille || !hw.integrity_permille ||
     !hw.capability_permille || (!hw.short_enabled && !hw.long_enabled))?1:0;
  out->passive_operational=out->autonomous && !out->equipment_offline;
  for(U c:all(w,"f06_contact"))if(val(w,c,F06_STATUS)==F06_ACTIVE){
   ++out->active_contacts;
   const U category=val(w,c,F06_SEEN_CATEGORY);
   if((category==F06_CATEGORY_ANOMALY ||
      category==F06_CATEGORY_STARSHIP ||
      category==F06_CATEGORY_SUBSPACE ||
      category==F06_CATEGORY_UNKNOWN) &&
     !val(w,c,F06_SEEN_CLASS))++out->needs_attention;
  }
  for(U job:all(w,"f06_timed_scan"))if(val(w,job,F06_TIMED_AUTO)){
   if(val(w,job,F06_TIMED_STATUS)==F06_TIMED_QUEUED)++out->analyses_running;
   if(val(w,job,F06_TIMED_STATUS)==F06_TIMED_FINISHED)++out->analyses_completed;
  }
  return F04_OK;
 });
}
uint32_t f06_computer_events_page(F04Session* s,F04Ref who,U after,
 F06ComputerEvent* out,U capacity,U* written,uint32_t* more) {
 if(!written || !more || (!out && capacity))return F04_ARGUMENT;
 *written=0;*more=0;
 return call(s,[&]()->uint32_t{
  need(observer(s,who),F04_DENIED);
  const auto& w=s->c->world;
  bool past=after==0;
  for(U id:all(w,"event")){
   const U op=val(w,id,OP),kind=f06_computer_kind(op);
   if(!kind)continue;
   const U token=f06_public(id,val(w,1,SHIP_ID));
   if(!past){if(token==after)past=true;continue;}
   if(*written>=capacity){*more=1;break;}
   const U target=ref(w,id,TARGET);
   U contact=0;
   if(op>=6001 && op<=6005){
    if(!type(w,target,"f06_contact"))continue;
    contact=target;
   }else{
    if(!type(w,target,"f06_timed_scan") || !val(w,target,F06_TIMED_AUTO))
     continue;
    contact=ref(w,target,F06_CONTACT_REF);
   }
   if(!type(w,contact,"f06_contact"))continue;
   out[(*written)++]={token,val(w,contact,F06_PUBLIC_ID),
      val(w,id,TICK),kind};
  }
  need(past,F04_ARGUMENT);
  return F04_OK;
 });
}
