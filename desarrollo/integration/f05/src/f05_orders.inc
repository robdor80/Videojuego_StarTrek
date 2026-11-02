namespace {
// These functions borrow F04's existing WorldState, authorities and Core clock.
U f05_origin(const Campaign& c,U issuer) {
 const auto& w=c.world;const U t=c.time.now();
 need(available(w,issuer,t),F04_UNAVAILABLE);
 const bool command=commander(w,t)==issuer,department=head(w,issuer,F04_SENSORS,t);
 need(command || department,F04_DENIED);
 for(U a:person_records(w,"appointment",issuer))if(window(w,a,t)) {
  const U role=val(w,a,ROLE);
  if((command && (role==F04_CAPTAIN || role==F04_FIRST || role==F04_SECOND || role==F04_SUCCESSOR || role==F04_WATCH)) ||
   (department && val(w,a,DEPT)==F04_SENSORS && (role==F04_HEAD || role==F04_DEPUTY || role==F04_DUTY_HEAD)))return a;
 }
 need(false,F04_DENIED);return 0;
}
void f05_validate(const Campaign& c,U request,U origin) {
 const auto& w=c.world;const U issuer=ref(w,request,ISSUER),recipient=ref(w,request,PERSON),t=c.time.now();
 need(t<val(w,request,END),F04_EXPIRED);
 need(!origin || (window(w,origin,t) && ref(w,origin,PERSON)==issuer),F04_REVOKED);
 (void)f05_origin(c,issuer);
 need(val(w,request,OP)==F04_SCAN,F05_UNSUPPORTED);
 need(type(w,recipient,"person") && member(w,recipient) && val(w,recipient,CATEGORY)==1,F04_DENIED);
 need(available(w,recipient,t),F04_UNAVAILABLE);
 need(scan_station(c,recipient)==ref(w,request,SLOT),F04_SCOPE);
}
void f05_access(F04Session* s,F04Ref who,U order) {
 need(observer(s,who),F04_DENIED);const auto& c=*s->c;const auto& w=c.world;
 need(type(w,order,"f05_order"),F04_ARGUMENT);
 need(who.id==ref(w,order,ISSUER) || who.id==ref(w,order,PERSON) || who.id==commander(w,c.time.now()),F04_DENIED);
}
F05Receipt f05_receipt(const Campaign& c,U order) {
 const auto& w=c.world;const U result=ref(w,order,F05_RESULT_REF);
 return {ref(w,order,F05_REQUEST_REF),order,ref(w,order,F05_TASK_REF),result?ref(w,result,F05_ATTEMPT_REF):0,
  result,ref(w,order,F05_PREVIOUS_REF),w.revision(),uint32_t(val(w,order,F05_STATUS)),uint32_t(val(w,order,CODE))};
}
U f05_record(Campaign& c,const ContentCatalog& cat,const char* kind,U person) {
 const U id=make(c,cat,kind);link(c,id,SHIP,1);link(c,id,PERSON,person);set(c,id,TICK,c.time.now());return id;
}
void f05_event(Campaign& c,const ContentCatalog& cat,U order,U actor,U state,U code,U attempt=0,U result=0) {
 const auto& w=c.world;need(f05_step(val(w,order,F05_STATUS),state),F05_TRANSITION);
 const U e=f05_record(c,cat,"f05_event",actor),previous=ref(w,order,F05_PREVIOUS_REF);
 link(c,e,F05_REQUEST_REF,ref(w,order,F05_REQUEST_REF));link(c,e,F05_ORDER_REF,order);
 link(c,e,F05_PREVIOUS_REF,previous);link(c,e,F05_TASK_REF,ref(w,order,F05_TASK_REF));
 link(c,e,F05_ATTEMPT_REF,attempt);link(c,e,F05_RESULT_REF,result);
 set(c,e,F05_STATUS,state);set(c,e,CODE,code);
 set(c,order,F05_STATUS,state);set(c,order,CODE,code);link(c,order,F05_PREVIOUS_REF,e);
}
bool f05_same(const WorldState& w,U r,const F05OrderRequest& q) {
 return ref(w,r,ISSUER)==q.issuer.id && ref(w,r,PERSON)==q.recipient.id && ref(w,r,SHIP)==q.ship.id &&
  ref(w,r,SLOT)==q.station.id && val(w,r,F05_KEY)==q.key && val(w,r,F05_REVISION)==q.expected_revision &&
  val(w,r,END)==q.deadline && val(w,r,CAUSE)==q.cause && val(w,r,OP)==q.operation;
}
void f05_commit(F04Session* s,std::unique_ptr<Campaign>& next,U order,F05Receipt* out) {
 need(schema(*next),F04_INTERNAL);s->c.swap(next);s->index_revision=UINT64_MAX;*out=f05_receipt(*s->c,order);
}
}
uint32_t f05_submit(F04Session* s,const F05OrderRequest* q,F05Receipt* out) {
 if(!q || !out)return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  need(!q->reserved && q->key && q->key<=FOREVER && q->cause && q->cause<=FOREVER &&
   q->expected_revision<=FOREVER && q->deadline<=FOREVER,F04_ARGUMENT);
  for(F04Ref r:{q->issuer,q->recipient,q->ship,q->station})need(r.scope==s->scope,F04_SCOPE);
  const auto& w=s->c->world;
  need(type(w,q->issuer.id,"person") && type(w,q->recipient.id,"person") && q->ship.id==1 && type(w,q->station.id,"slot"),F04_SCOPE);
  // Campaign-wide tombstone: lookup precedes revision, authority and deadline.
  for(U o:all(w,"f05_order")) {
   const U r=ref(w,o,F05_REQUEST_REF);if(val(w,r,F05_KEY)!=q->key)continue;
   *out=f05_receipt(*s->c,o);return f05_same(w,r,*q)?out->code:uint32_t(F05_IDEMPOTENCY_CONFLICT);
  }
  need(q->deadline>s->c->time.now(),F04_ARGUMENT);
  need(all(w,"f05_order").size()<512,F04_CAPACITY);
  auto next=std::make_unique<Campaign>(*s->c);const auto& cat=*s->content.catalog();
  const U r=f05_record(*next,cat,"f05_request",q->recipient.id);
  link(*next,r,ISSUER,q->issuer.id);link(*next,r,SLOT,q->station.id);
  set(*next,r,F05_KEY,q->key);set(*next,r,F05_REVISION,q->expected_revision);set(*next,r,END,q->deadline);
  set(*next,r,CAUSE,q->cause);set(*next,r,OP,q->operation);
  const U o=f05_record(*next,cat,"f05_order",q->recipient.id);
  link(*next,o,ISSUER,q->issuer.id);link(*next,o,SLOT,q->station.id);link(*next,o,F05_REQUEST_REF,r);
  f05_event(*next,cat,o,q->issuer.id,F05_ISSUED,F04_OK);
  uint32_t code=F04_OK;
  try {
   need(q->expected_revision==w.revision(),F04_STALE);
   const U origin=f05_origin(*next,q->issuer.id);link(*next,o,ORIGIN,origin);f05_validate(*next,r,origin);
  } catch(const Denial& d) {code=d.code;f05_event(*next,cat,o,q->issuer.id,F05_REFUSED,code);}
  f05_commit(s,next,o,out);return code;
 });
}
uint32_t f05_receive(F04Session* s,F04Ref who,U revision,U order,F05Receipt* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  f05_access(s,who,order);const auto& w=s->c->world;need(who.id==ref(w,order,PERSON),F04_DENIED);
  *out=f05_receipt(*s->c,order);
  if(out->state==F05_ACCEPTED || f05_terminal(out->state))return out->code;
  need(out->state==F05_ISSUED,F05_TRANSITION);need(revision==w.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);const auto& cat=*s->content.catalog();uint32_t code=F04_OK;
  try {f05_validate(*next,out->request,ref(w,order,ORIGIN));}
  catch(const Denial& d){code=d.code;}
  if(code==F04_OK) {
   const U task=f05_record(*next,cat,"f05_task",who.id);link(*next,task,F05_ORDER_REF,order);
   set(*next,task,F05_STATUS,F05_TASK_ACKNOWLEDGED);link(*next,order,F05_TASK_REF,task);
  }
  f05_event(*next,cat,order,who.id,code==F04_OK?F05_ACCEPTED:F05_REFUSED,code);
  f05_commit(s,next,order,out);return code;
 });
}
uint32_t f05_execute_order(F04Session* s,F04Ref who,U revision,U order,F05Receipt* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  f05_access(s,who,order);const auto& w=s->c->world;need(who.id==ref(w,order,PERSON),F04_DENIED);
  *out=f05_receipt(*s->c,order);if(f05_terminal(out->state))return out->code;
  need(out->state==F05_ACCEPTED,F05_TRANSITION);need(revision==w.revision() && revision<=FOREVER,F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);const auto& cat=*s->content.catalog();
  const U task=out->task,request=out->request,attempt=f05_record(*next,cat,"f05_attempt",who.id);
  link(*next,attempt,F05_ORDER_REF,order);link(*next,attempt,F05_TASK_REF,task);set(*next,attempt,F05_REVISION,revision);
  set(*next,task,F05_STATUS,F05_TASK_IN_PROGRESS);f05_event(*next,cat,order,who.id,F05_EXECUTING,F04_OK,attempt);
  uint32_t code=F04_OK;bool performed=false;ActionResult actual{};
  try {
   f05_validate(*next,request,ref(w,order,ORIGIN));
   const F04Request op{who,next->world.revision(),F04_SCAN,0,0,0,0,0,val(w,request,CAUSE)};
   performed=true;(void)perform(*next,cat,op,false,&actual);
  } catch(const Denial& d){code=d.code;}
  const U result=f05_record(*next,cat,"f05_result",who.id);
  link(*next,result,F05_ORDER_REF,order);link(*next,result,F05_TASK_REF,task);link(*next,result,F05_ATTEMPT_REF,attempt);
  set(*next,result,VALUE,performed?1:0);set(*next,result,CODE,code);
  set(*next,result,F05_OUTCOME,performed?uint32_t(actual.outcome):0);set(*next,result,F05_REJECTION,performed?uint32_t(actual.rejection):0);
  set(*next,result,F05_BEFORE,performed?actual.revision_before:0);set(*next,result,F05_AFTER,performed?actual.revision_after:0);
  const auto* roll=std::get_if<RollConsequence>(&actual.consequence);
  set(*next,result,F05_STREAM,roll?roll->stream_id:0);
  set(*next,result,F05_ROLL,roll?roll->value:0);set(*next,result,F05_CONSUMED,roll && roll->consumed_random?1:0);
  link(*next,order,F05_RESULT_REF,result);set(*next,task,F05_STATUS,code==F04_OK?F05_TASK_COMPLETED:F05_TASK_FAILED);
  f05_event(*next,cat,order,who.id,code==F04_OK?F05_COMPLETED:F05_FAILED,code,attempt,result);
  f05_commit(s,next,order,out);return code;
 });
}
uint32_t f05_cancel(F04Session* s,F04Ref who,U revision,U order,F05Receipt* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  f05_access(s,who,order);const auto& w=s->c->world;
  need(who.id==ref(w,order,ISSUER) || who.id==commander(w,s->c->time.now()),F04_DENIED);
  *out=f05_receipt(*s->c,order);if(out->state==F05_CANCELLED)return F04_OK;
  need(!f05_terminal(out->state),F05_TRANSITION);need(revision==w.revision(),F04_STALE);
  (void)f05_origin(*s->c,who.id);
  auto next=std::make_unique<Campaign>(*s->c);
  if(out->task)set(*next,out->task,F05_STATUS,F05_TASK_CANCELLED);
  f05_event(*next,*s->content.catalog(),order,who.id,F05_CANCELLED,F04_OK);f05_commit(s,next,order,out);return F04_OK;
 });
}
uint32_t f05_order(F04Session* s,F04Ref who,U order,F05OrderView* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  f05_access(s,who,order);const auto& w=s->c->world;const U r=ref(w,order,F05_REQUEST_REF);
  out->receipt=f05_receipt(*s->c,order);out->issuer=ref(w,r,ISSUER);out->recipient=ref(w,r,PERSON);out->ship=1;
  out->station=ref(w,r,SLOT);out->origin=ref(w,order,ORIGIN);out->key=val(w,r,F05_KEY);out->deadline=val(w,r,END);
  out->cause=val(w,r,CAUSE);out->issued_at=val(w,r,TICK);out->input_revision=val(w,r,F05_REVISION);
  out->operation=uint32_t(val(w,r,OP));return F04_OK;
 });
}
uint32_t f05_result(F04Session* s,F04Ref who,U order,F05ResultView* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  f05_access(s,who,order);const auto& w=s->c->world;const U r=ref(w,order,F05_RESULT_REF);need(r,F05_TRANSITION);
  const U at=ref(w,r,F05_ATTEMPT_REF);
  *out={r,order,ref(w,r,F05_TASK_REF),ref(w,r,PERSON),val(w,at,F05_REVISION),val(w,r,TICK),
   uint32_t(val(w,r,VALUE)),uint32_t(val(w,r,CODE)),uint32_t(val(w,r,F05_OUTCOME)),uint32_t(val(w,r,F05_REJECTION)),
   val(w,r,F05_BEFORE),val(w,r,F05_AFTER),val(w,r,F05_STREAM),val(w,r,F05_ROLL),uint32_t(val(w,r,F05_CONSUMED)),0};return F04_OK;
 });
}
uint32_t f05_events_page(F04Session* s,F04Ref who,U order,U after,F05EventView* out,U capacity,U* written,uint32_t* more) {
 if(!written || !more || (!out && capacity) || !capacity || capacity>256)return F04_ARGUMENT;*written=0;*more=0;
 return call(s,[&]()->uint32_t {
  f05_access(s,who,order);const auto& w=s->c->world;
  for(U e:all(w,"f05_event"))if(e>after && ref(w,e,F05_ORDER_REF)==order) {
   if(*written==capacity){*more=1;break;}
   out[(*written)++]={e,ref(w,e,F05_PREVIOUS_REF),ref(w,e,F05_REQUEST_REF),order,ref(w,e,F05_TASK_REF),
    ref(w,e,F05_ATTEMPT_REF),ref(w,e,F05_RESULT_REF),ref(w,e,PERSON),val(w,e,TICK),uint32_t(val(w,e,F05_STATUS)),uint32_t(val(w,e,CODE))};
  }return F04_OK;
 });
}
