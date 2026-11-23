// Physical truth and immutable, knowledge-filtered equipment observations.
#include "f06_equipment_catalog_generated.h"
namespace {
U f06_physical_for(const WorldState& w,U sig) {
 for(U id:all(w,"f06_physical"))if(ref(w,id,F06_SIGNAL_REF)==sig)return id;
 return 0;
}
U f06_latest_equipment(const WorldState& w,U contact) {
 U latest=0;
 for(U id:all(w,"f06_equipment"))if(ref(w,id,F06_CONTACT_REF)==contact)latest=id;
 return latest;
}
void f06_measure_equipment(Campaign& c,const ContentCatalog& cat,U contact,U sig,U score) {
 const auto& w=c.world;
 const U p=f06_physical_for(w,sig);
 if(!p || val(w,p,F06_P_CLOAK) || score<240)return;
 const U old=f06_latest_equipment(w,contact);
 U mask=0;
 std::array<U,6> values{};
 for(U k=0;k<6;++k){
  const U raw=val(w,p,Field(F06_P_0+k)),visibility=raw>>10;
  // Visibility=0 explicitly models unobservable internal hardware. No leak,
  // including counts, unavailable state, or a negative claim of absence.
  if(visibility && score*visibility/1000>=240){mask|=U(1)<<k;values[k]=raw&1023;}
 }
 const U length=score>=540?val(w,p,F06_P_LENGTH):0;
 const U klass=val(w,contact,F06_SEEN_CLASS);
 bool changed=!old || val(w,old,F06_E_MASK)!=mask ||
   val(w,old,F06_E_LENGTH)!=length || val(w,old,F06_E_CLASS)!=klass;
 for(U k=0;k<6 && !changed;++k)changed=val(w,old,Field(F06_E_0+k))!=values[k];
 if(!changed)return; // immutable change history, no repeated warnings
 need(all(w,"f06_equipment").size()<4096,F04_CAPACITY);
 const U id=make(c,cat,"f06_equipment");
 link(c,id,SHIP,1);link(c,id,F06_CONTACT_REF,contact);
 f06_set(c,id,F06_E_PUBLIC,f06_public(id,val(c.world,1,SHIP_ID)));
 f06_set(c,id,F06_E_TICK,c.time.now());f06_set(c,id,F06_E_CLASS,klass);
 U catalog_version=0;
 for(const auto& row:F06_EQUIPMENT_CATALOG)if(row.class_id==klass)catalog_version=1;
 f06_set(c,id,F06_E_CATALOG,catalog_version);
 f06_set(c,id,F06_E_LENGTH,length);f06_set(c,id,F06_E_CONF,val(c.world,contact,F06_CONFIDENCE));
 f06_set(c,id,F06_E_MASK,mask);
 for(U k=0;k<6;++k)f06_set(c,id,Field(F06_E_0+k),values[k]);
 if(old)f06_notice(c,cat,contact,6); // one actual equipment change
}
F06EquipmentView f06_equipment_view(const WorldState& w,U id) {
 F06EquipmentView v{};
 v.observation_id=val(w,id,F06_E_PUBLIC);
 v.contact_id=val(w,ref(w,id,F06_CONTACT_REF),F06_PUBLIC_ID);
 v.tick=val(w,id,F06_E_TICK);v.class_id=static_cast<uint32_t>(val(w,id,F06_E_CLASS));
 v.length_m=static_cast<uint32_t>(val(w,id,F06_E_LENGTH));
 v.confidence_permille=static_cast<uint32_t>(val(w,id,F06_E_CONF));
 v.visible_mask=static_cast<uint32_t>(val(w,id,F06_E_MASK));
 const F06EquipmentCatalog* catalog=nullptr;
 for(const auto& row:F06_EQUIPMENT_CATALOG)if(val(w,id,F06_E_CATALOG)==1 && row.class_id==v.class_id)catalog=&row;
 v.catalog_version=catalog?1:0;
 for(U k=0;k<6;++k){
  const U raw=val(w,id,Field(F06_E_0+k));v.count[k]=raw&255;v.state[k]=raw>>8;
  if(catalog)v.expected[k]=catalog->count[k];
  if(v.visible_mask&(U(1)<<k)){
   v.comparison[k]=catalog?(v.count[k]==v.expected[k]?1:2):0;
   if(k<2 && v.count[k] && v.state[k]==3)v.comparison[k]=3;
  }
 }
 return v;
}
F06DeliveryView f06_delivery_view(const WorldState& w,U id) {
 const U target=ref(w,id,TARGET);
 return {val(w,id,F06_D_PUBLIC),val(w,ref(w,id,F06_CONTACT_REF),F06_PUBLIC_ID),
  val(w,target,type(w,target,"f06_equipment")?F06_E_PUBLIC:
   type(w,target,"f06_observation")?F06_O_PUBLIC:F06_SCI_PUBLIC),val(w,id,F06_D_TICK),
  static_cast<uint32_t>(val(w,id,F06_D_RECIPIENT)),1};
}
}
uint32_t f06_host_physical(F04Session* s,const F06PhysicalInput* in) {
 if(!in)return F04_ARGUMENT;
 return call(s,[&]()->uint32_t {
  need(in->expected_revision==s->c->world.revision(),F04_STALE);
  need(in->version==1 && !in->reserved && in->world_entity_key &&
   in->source_revision && in->source_revision<=FOREVER && in->length_m<=10000 && in->cloaked<=1,F04_ARGUMENT);
  for(U k=0;k<6;++k)need(in->count[k]<=64 && in->state[k]<=(k<2?3u:2u) &&
   in->visibility_permille[k]<=1000 && (in->count[k] || !in->state[k]),F04_ARGUMENT);
  U sig=0;
  for(U id:all(s->c->world,"f06_signal"))
   if(val(s->c->world,id,F06_WORLD_ID)==in->world_entity_key)sig=id;
  need(sig,F04_SCOPE);
  const U old=f06_physical_for(s->c->world,sig);
  if(old)need(in->source_revision>val(s->c->world,old,F06_P_REV),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  U id=old;
  if(!id){id=make(*next,*s->content.catalog(),"f06_physical");link(*next,id,SHIP,1);link(*next,id,F06_SIGNAL_REF,sig);}
  f06_set(*next,id,F06_P_REV,in->source_revision);f06_set(*next,id,F06_P_LENGTH,in->length_m);
  f06_set(*next,id,F06_P_CLOAK,in->cloaked);
  for(U k=0;k<6;++k)f06_set(*next,id,Field(F06_P_0+k),
    U(in->count[k])+(U(in->state[k])<<8)+(U(in->visibility_permille[k])<<10));
  f06_poll(*next,*s->content.catalog(),0,false);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;return F04_OK;
 });
}
uint32_t f06_equipment_page(F04Session* s,F04Ref who,U contact,U offset,
 F06EquipmentView* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  for(U id:all(s->c->world,"f06_equipment")) {
   const auto v=f06_equipment_view(s->c->world,id);
   if(contact && v.contact_id!=contact)continue;
   if((*total)++>=offset && *written<capacity)out[(*written)++]=v;
  }
  return F04_OK;
 });
}
uint32_t f06_deliver(F04Session* s,F04Ref who,const F06DeliveryRequest* req,F06DeliveryView* out) {
 if(!req || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  need(req->request_key && req->request_key<=FOREVER && req->recipient>=1 &&
   req->recipient<=3 && !req->reserved,F04_ARGUMENT);
  // Authenticate current console authority even for retries.
  (void)scan_station(*s->c,who.id);
  for(U id:all(s->c->world,"f06_delivery"))if(val(s->c->world,id,F06_D_KEY)==req->request_key){
   const auto v=f06_delivery_view(s->c->world,id);
   need(ref(s->c->world,id,PERSON)==who.id && v.contact_id==req->contact_id &&
    v.recipient==req->recipient,F04_OVERLAP);*out=v;return F04_OK;
  }
  need(req->expected_revision==s->c->world.revision(),F04_STALE);
  const U contact=f06_contact_for_public(s->c->world,req->contact_id);
  need(contact && val(s->c->world,contact,F06_STATUS)==F06_ACTIVE,F04_UNAVAILABLE);
  const U observation=f06_latest_equipment(s->c->world,contact);
  need(observation,F04_UNAVAILABLE);
  need(all(s->c->world,"f06_delivery").size()<512,F04_CAPACITY);
  auto next=std::make_unique<Campaign>(*s->c);
  const U id=make(*next,*s->content.catalog(),"f06_delivery");
  link(*next,id,SHIP,1);link(*next,id,PERSON,who.id);link(*next,id,F06_CONTACT_REF,contact);link(*next,id,TARGET,observation);
  f06_set(*next,id,F06_D_KEY,req->request_key);f06_set(*next,id,F06_D_PUBLIC,f06_public(id,val(next->world,1,SHIP_ID)));
  f06_set(*next,id,F06_D_TICK,next->time.now());f06_set(*next,id,F06_D_RECIPIENT,req->recipient);
  (void)event(*next,*s->content.catalog(),who.id,6060+req->recipient,F04_OK,0,contact);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_delivery_view(s->c->world,id);return F04_OK;
 });
}
uint32_t f06_deliveries_page(F04Session* s,F04Ref who,U offset,F06DeliveryView* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity))return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);
  for(U id:all(s->c->world,"f06_delivery"))
   if((*total)++>=offset && *written<capacity)out[(*written)++]=f06_delivery_view(s->c->world,id);
  return F04_OK;
 });
}

uint32_t f06_deliver_evidence(F04Session* s,F04Ref who,const F06EvidenceDeliveryRequest* req,F06DeliveryView* out) {
 if(!req || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);(void)scan_station(*s->c,who.id);
  need(req->request_key && req->request_key<=FOREVER && req->source_id &&
   req->recipient>=1 && req->recipient<=3 && req->kind>=1 && req->kind<=3,F04_ARGUMENT);
  const auto& w=s->c->world;U source=0;
  if(req->kind==1){for(U id:all(w,"f06_equipment"))if(val(w,id,F06_E_PUBLIC)==req->source_id)source=id;}
  else if(req->kind==2)source=f06_result_by_public(w,req->source_id);
  else source=f06_report_by_public(w,req->source_id);
  need(source,F04_UNAVAILABLE);
  const U contact=req->kind==3?ref(w,ref(w,source,F06_HANDOFF_REF),F06_CONTACT_REF):ref(w,source,F06_CONTACT_REF);
  need(val(w,contact,F06_PUBLIC_ID)==req->contact_id,F04_SCOPE);
  for(U id:all(w,"f06_delivery"))if(val(w,id,F06_D_KEY)==req->request_key){
   const auto v=f06_delivery_view(w,id);
   need(ref(w,id,PERSON)==who.id && ref(w,id,TARGET)==source && v.contact_id==req->contact_id &&
     v.recipient==req->recipient,F04_OVERLAP);*out=v;return F04_OK;
  }
  need(req->expected_revision==w.revision(),F04_STALE);
  need(val(w,contact,F06_STATUS)==F06_ACTIVE,F04_UNAVAILABLE);
  need(all(w,"f06_delivery").size()<512,F04_CAPACITY);
  auto next=std::make_unique<Campaign>(*s->c);
  const U id=make(*next,*s->content.catalog(),"f06_delivery");
  link(*next,id,SHIP,1);link(*next,id,PERSON,who.id);link(*next,id,F06_CONTACT_REF,contact);link(*next,id,TARGET,source);
  f06_set(*next,id,F06_D_KEY,req->request_key);f06_set(*next,id,F06_D_PUBLIC,f06_public(id,val(next->world,1,SHIP_ID)));
  f06_set(*next,id,F06_D_TICK,next->time.now());f06_set(*next,id,F06_D_RECIPIENT,req->recipient);
  (void)event(*next,*s->content.catalog(),who.id,6060+req->recipient,F04_OK,0,contact);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_delivery_view(s->c->world,id);return F04_OK;
 });
}
uint32_t f06_contact_tracking(F04Session* s,F04Ref who,U public_id,F06TrackView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;
  const U contact=f06_contact_for_public(w,public_id);need(contact,F04_UNAVAILABLE);
  const U cap=f06_tracking_capacity(w),used=f06_tracking_used(w);
  *out={public_id,val(w,contact,F06_TRACK_UPDATED),static_cast<uint32_t>(val(w,contact,F06_TRACK_MODE)),
   static_cast<uint32_t>(used),static_cast<uint32_t>(cap>used?cap-used:0),static_cast<uint32_t>(used>cap)};
  return F04_OK;
 });
}
uint32_t f06_deep_analysis(F04Session* s,F04Ref who,U public_id,F06DeepAnalysisView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;
  const U contact=f06_contact_for_public(w,public_id);need(contact,F04_UNAVAILABLE);
  out->contact_id=public_id;
  U first=0,last=0;
  for(U id:all(w,"f06_observation"))if(ref(w,id,F06_CONTACT_REF)==contact){if(!first)first=id;last=id;}
  if(last){out->position_source=val(w,last,F06_O_PUBLIC);
   if(val(w,last,F06_O_TICK)>val(w,first,F06_O_TICK)){
    const auto a=f06_result_view(w,first),b=f06_result_view(w,last);
    const long double dx=b.observed_x_milli_au-a.observed_x_milli_au,
     dy=b.observed_y_milli_au-a.observed_y_milli_au,dz=b.observed_z_milli_au-a.observed_z_milli_au;
    out->interval_seconds=b.tick-a.tick;
    out->displacement_micro_au=static_cast<U>(std::llround(std::sqrt(dx*dx+dy*dy+dz*dz)*1000));out->valid_mask|=4;
   }
  }
  for(U id:all(w,"f06_science_report"))if(ref(w,ref(w,id,F06_HANDOFF_REF),F06_CONTACT_REF)==contact){
   out->science_source=val(w,id,F06_SCI_PUBLIC);
   // 1 mbar=1000 microbar; concentration is permille, so units cancel.
   out->oxygen_microbar=val(w,id,F06_SCI_PRESS)*val(w,id,F06_SCI_O2);
   out->co2_microbar=val(w,id,F06_SCI_PRESS)*val(w,id,F06_SCI_CO2);out->valid_mask|=1;
  }
  const U equipment=f06_latest_equipment(w,contact);
  if(equipment){
   out->equipment_source=val(w,equipment,F06_E_PUBLIC);U count=0;
   for(U id:all(w,"f06_equipment"))if(ref(w,id,F06_CONTACT_REF)==contact)++count;
   out->equipment_changes=count?count-1:0;if(count>1)out->valid_mask|=8;
   const U length=val(w,equipment,F06_E_LENGTH),distance=val(w,contact,F06_DISTANCE);
   if(length && distance && val(w,contact,F06_STATUS)==F06_ACTIVE){
    // Small-angle physical extent; AU is exactly 149597870700 metres.
    out->angular_nanoradian=static_cast<U>(std::llround(
     2*std::atan(static_cast<long double>(length)/(2*distance*149597870.7L))*1000000000));
    out->valid_mask|=2;
   }
  }
  return F04_OK;
 });
}
