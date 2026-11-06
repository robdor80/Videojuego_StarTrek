// F06 runtime over the EXISTING F04Session's Core WorldState.
// Include at the tail of f04_bridge.cpp; declarations precede f04_advance.
namespace {
U f06_zigzag(int64_t x) {return x<0?U(-(x+1))*2+1:U(x)*2;}
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
U f06_score(const WorldState& w,U s,U distance,bool active,bool focused) {
 if(!val(w,s,F06_ACTIVE_FLAG))return 0;
 const U limit=focused?50000:30000;
 if(distance>limit)return 0;
 const U strength=val(w,s,F06_STRENGTH),mask=val(w,s,F06_INTERFERENCE);
 auto measure=[&](U range,bool near_bonus)->U {
  if(distance>range)return 0;
  // Fixed-point gameplay abstraction. Distances are milli-AU.
  U score=strength*(1000-550*distance/range)/1000;
  score=score*(active?1080:920)/1000;
  if(near_bonus)score=std::min<U>(1000,score+100);
  if(focused)score=std::min<U>(1000,score+160);
  return score>mask?score-mask:0;
 };
 U score=measure(limit,false);
 if(!focused)score=std::max(score,measure(2000,true));
 return std::min<U>(1000,score);
}
U f06_rank(U score) {
 if(score>=720)return 4;if(score>=540)return 3;
 if(score>=380)return 2;if(score>=240)return 1;return 0;
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
 return {id,val(w,id,F06_FIRST),val(w,id,F06_LAST),
   f06_unzigzag(val(w,id,F06_VISIBLE_X)),f06_unzigzag(val(w,id,F06_VISIBLE_Y)),
   f06_unzigzag(val(w,id,F06_VISIBLE_Z)),val(w,id,F06_SEEN_TRANSPONDER),
   static_cast<uint32_t>(val(w,id,F06_STATUS)),
   static_cast<uint32_t>(val(w,id,F06_CONFIDENCE)),
   static_cast<uint32_t>(val(w,id,F06_DISTANCE)),
   static_cast<uint32_t>(val(w,id,F06_SEEN_CLASS)),
   static_cast<uint32_t>(val(w,id,F06_LOSS_REASON))};
}
void f06_apply(Campaign& c,const ContentCatalog& cat,U sig,bool active,bool focused) {
 U contact=f06_contact_for(c.world,sig);
 U d=f06_distance(c.world,sig);
 U score=f06_score(c.world,sig,d,active,focused),rank=f06_rank(score);
 // An active focused request must never create a contact out of hidden truth.
 if(!rank && !contact)return;
 if(!rank) {
  if(val(c.world,contact,F06_STATUS)==F06_ACTIVE) {
   const U previous=val(c.world,contact,F06_CONFIDENCE);
   const U cause=val(c.world,sig,F06_EXIT);
   f06_set(c,contact,F06_STATUS,F06_LOST);
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
 for(U signal:signals)f06_apply(c,cat,signal,active,false);
}
} // namespace
uint32_t f06_host_signal(F04Session* s,const F06SignalInput* in,F06SignalReceipt* out) {
 if(!in || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(in->expected_revision==s->c->world.revision(),F04_STALE);
  need(!in->reserved && in->strength_permille<=1000 && in->interference_permille<=550 &&
   in->active<=1 && in->observed_exit_evidence<=F06_EXIT_OBSERVED_OUT_OF_RANGE,
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
  for(U id:all(s->c->world,"event")) {
   const U op=val(s->c->world,id,OP);
   if(id<=after || op<6001 || op>6005)continue;
   if(*written>=capacity){*more=1;break;}
   out[(*written)++]={id,ref(s->c->world,id,TARGET),val(s->c->world,id,TICK),
     static_cast<uint32_t>(op-6000)};
  }
  return F04_OK;
 });
}
uint32_t f06_focus(F04Session* s,F04Ref who,U revision,U contact,F06ContactView* out) {
 if(!out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);need(revision==s->c->world.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);
  (void)scan_station(*next,who.id); // F04 present, qualified and on duty
  f06_poll(*next,*s->content.catalog(),contact,true);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;
  *out=f06_view(s->c->world,contact);return F04_OK;
 });
}
