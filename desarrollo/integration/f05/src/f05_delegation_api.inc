uint32_t f05_delegate(F04Session* s,const F05DelegationRequest* q,F05DelegationView* out) {
 if(!q || !out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  need(!q->reserved && q->key && q->key<=FOREVER && q->cause && q->cause<=FOREVER && q->expected_revision<=FOREVER,F04_ARGUMENT);
  for(F04Ref r:{q->delegant,q->delegate,q->ship,q->station,q->executor})need(r.scope==s->scope,F04_SCOPE);
  const auto& w=s->c->world;
  for(U e:all(w,"f05_delegation_event"))if(val(w,e,F05_KEY)==q->key) {
   const U d=ref(w,e,F05_DELEGATION_REF);
   need(val(w,e,OP)==0 && ref(w,d,ISSUER)==q->delegant.id && ref(w,d,PERSON)==q->delegate.id && q->ship.id==1 &&
    ref(w,d,SLOT)==q->station.id && ref(w,d,F05_EXECUTOR_REF)==q->executor.id && val(w,d,F05_REVISION)==q->expected_revision &&
    val(w,d,START)==q->start && val(w,d,END)==q->end && val(w,d,CAUSE)==q->cause && !q->parent &&
    val(w,d,D_DOMAIN)==q->domain && val(w,d,OP)==q->operation && val(w,e,F05_MODE)==q->mode,F05_IDEMPOTENCY_CONFLICT);
   f05_delegation_access(s,q->delegant,d);*out=f05_delegation_view(*s->c,d);return F04_OK;
  }
  need(!q->parent,F05_UNSUPPORTED); // No contractual subdelegation executor exists.
  need(q->expected_revision==w.revision(),F04_STALE);
  need(q->ship.id==1 && type(w,q->station.id,"slot") && val(w,q->station.id,DEPT)==F04_SENSORS,F04_SCOPE);
  need(q->domain==F04_SENSORS && q->operation==F04_SCAN,F05_UNSUPPORTED);
  need(q->mode>=F05_MANUAL && q->mode<=F05_DELEGATED_AUTONOMOUS,F04_ARGUMENT);
  need(q->start>=s->c->time.now() && q->start<q->end && q->end<=FOREVER,F04_ARGUMENT);
  need(q->delegant.id!=q->delegate.id,F04_DENIED);
  const U origin=f05_origin(*s->c,q->delegant.id);f05_grant_source(*s->c,q->delegant.id,origin);
  const U holder=f05_holder(*s->c,q->delegate.id);
  need(q->end<=val(w,origin,END) && q->end<=val(w,holder,END) && q->end<=val(w,q->delegate.id,UNTIL) &&
   q->end<=val(w,q->delegant.id,UNTIL),F04_EXPIRED);
  need(type(w,q->executor.id,"person") && member(w,q->executor.id) && primary_operator(w,q->executor.id) &&
   val(w,q->executor.id,CATEGORY)==1,F04_DENIED);
  need(qualified(w,q->executor.id,F04_SENSORS,s->c->time.now()),F04_QUALIFICATION);
  U count=0;for(U d:all(w,"delegation"))if(has(w,d,F05_MODE))++count;need(count<256,F04_CAPACITY);
  auto next=std::make_unique<Campaign>(*s->c);const auto& cat=*s->content.catalog();const U d=make(*next,cat,"delegation");
  link(*next,d,SHIP,1);link(*next,d,ISSUER,q->delegant.id);link(*next,d,PERSON,q->delegate.id);link(*next,d,ORIGIN,origin);
  link(*next,d,F05_HOLDER_REF,holder);link(*next,d,SLOT,q->station.id);link(*next,d,F05_EXECUTOR_REF,q->executor.id);
  temporal(*next,d,q->start,q->end);set(*next,d,D_DOMAIN,q->domain);set(*next,d,OP,q->operation);set(*next,d,CAUSE,q->cause);
  set(*next,d,F05_KEY,q->key);set(*next,d,F05_REVISION,q->expected_revision);set(*next,d,TICK,next->time.now());
  f05_grant_event(*next,cat,d,q->delegant.id,q->key,q->expected_revision,q->cause,F05_DRAFT,q->mode,0);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);*out=f05_delegation_view(*s->c,d);return F04_OK;
 });
}
uint32_t f05_change_delegation(F04Session* s,const F05DelegationChange* q,F05DelegationView* out) {
 if(!q || !out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  f05_delegation_access(s,q->actor,q->delegation);const auto& w=s->c->world;const U d=q->delegation;
  need(q->key && q->key<=FOREVER && q->cause && q->cause<=FOREVER && q->expected_revision<=FOREVER,F04_ARGUMENT);
  for(U e:all(w,"f05_delegation_event"))if(val(w,e,F05_KEY)==q->key) {
   need(val(w,e,OP)==1 && ref(w,e,F05_DELEGATION_REF)==d && ref(w,e,PERSON)==q->actor.id &&
    val(w,e,F05_REVISION)==q->expected_revision && val(w,e,CAUSE)==q->cause && val(w,e,F05_STATUS)==q->state &&
    val(w,e,F05_MODE)==q->mode,F05_IDEMPOTENCY_CONFLICT);
   *out=f05_delegation_view(*s->c,d);return F04_OK;
  }
  need(q->expected_revision==w.revision(),F04_STALE);
  need(q->mode>=F05_MANUAL && q->mode<=F05_DELEGATED_AUTONOMOUS,F04_ARGUMENT);
  need(f05_delegation_step(val(w,d,F05_STATUS),q->state),F05_TRANSITION);
  const U t=s->c->time.now();
  if(q->state==F05_EXPIRED)need(t>=val(w,d,END) && q->mode==val(w,d,F05_MODE),F04_ARGUMENT);
  else {
   need(q->actor.id==commander(w,t) && available(w,q->actor.id,t),F04_DENIED);
   if(q->state==F05_ACTIVE)f05_grant_live(*s->c,d,false);
  }
  auto next=std::make_unique<Campaign>(*s->c);
  f05_grant_event(*next,*s->content.catalog(),d,q->actor.id,q->key,q->expected_revision,q->cause,q->state,q->mode,1);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);*out=f05_delegation_view(*s->c,d);return F04_OK;
 });
}
uint32_t f05_delegation(F04Session* s,F04Ref who,U d,F05DelegationView* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  f05_delegation_access(s,who,d);*out=f05_delegation_view(*s->c,d);return F04_OK;
 });
}
uint32_t f05_delegation_events(F04Session* s,F04Ref who,U d,U after,F05DelegationEvent* out,U capacity,U* written,uint32_t* more) {
 if(!written || !more || !out || !capacity || capacity>256)return F04_ARGUMENT;*written=0;*more=0;
 return call(s,[&]()->uint32_t {
  f05_delegation_access(s,who,d);const auto& w=s->c->world;
  for(U e:all(w,"f05_delegation_event"))if(e>after && ref(w,e,F05_DELEGATION_REF)==d) {
   if(*written==capacity){*more=1;break;}
   out[(*written)++]={e,ref(w,e,F05_PREVIOUS_REF),d,ref(w,e,PERSON),val(w,e,F05_KEY),val(w,e,F05_REVISION),
    val(w,e,CAUSE),val(w,e,TICK),uint32_t(val(w,e,F05_STATUS)),uint32_t(val(w,e,F05_MODE)),uint32_t(val(w,e,OP)),0};
  }return F04_OK;
 });
}
uint32_t f05_approve_order(F04Session* s,F04Ref who,U revision,U order,U cause,F05Receipt* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;
  need(type(w,order,"f05_order"),F04_ARGUMENT);const U r=ref(w,order,F05_REQUEST_REF),d=ref(w,r,F05_DELEGATION_REF);
  need(d && who.id==ref(w,d,ISSUER),F04_DENIED);need(cause && cause<=FOREVER,F04_ARGUMENT);
  if(U a=ref(w,order,F05_APPROVAL_REF)) {
   need(ref(w,a,PERSON)==who.id && val(w,a,CAUSE)==cause && val(w,a,F05_REVISION)==revision,F05_IDEMPOTENCY_CONFLICT);
   *out=f05_receipt(*s->c,order);return F04_OK;
  }
  need(revision==w.revision(),F04_STALE);need(val(w,order,F05_STATUS)==F05_ISSUED,F05_TRANSITION);
  f05_validate(*s->c,r,ref(w,order,ORIGIN));
  f05_grant_source(*s->c,who.id,ref(w,d,ORIGIN));
  auto next=std::make_unique<Campaign>(*s->c);const U a=f05_record(*next,*s->content.catalog(),"f05_approval",who.id);
  link(*next,a,F05_ORDER_REF,order);link(*next,a,F05_DELEGATION_REF,d);set(*next,a,F05_REVISION,revision);set(*next,a,CAUSE,cause);
  link(*next,order,F05_APPROVAL_REF,a);f05_commit(s,next,order,out);return F04_OK;
 });
}
uint32_t f05_delegations_page(F04Session* s,F04Ref who,U after,F05DelegationView* out,U capacity,U* written,uint32_t* more) {
 if(!written || !more || !out || !capacity || capacity>256)return F04_ARGUMENT;*written=0;*more=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,who),F04_DENIED);const auto& w=s->c->world;const U command=commander(w,s->c->time.now());
  for(U d:all(w,"delegation"))if(d>after && has(w,d,F05_MODE) &&
   (who.id==command || who.id==ref(w,d,ISSUER) || who.id==ref(w,d,PERSON))) {
   if(*written==capacity){*more=1;break;}out[(*written)++]=f05_delegation_view(*s->c,d);
  }return F04_OK;
 });
}
