namespace {
U f05_player(const WorldState& w) {const auto ids=all(w,"f05_player");return ids.empty()?0:ref(w,ids[0],PERSON);}
F05NeedView f05_need_view(const WorldState& w,U n) {
 return {n,ref(w,n,ISSUER),ref(w,n,ORIGIN),ref(w,n,ACTIVITY),ref(w,n,SLOT),ref(w,n,PERSON),
  val(w,n,F05_KEY),val(w,n,F05_REVISION),val(w,n,START),val(w,n,END),val(w,n,CAUSE),val(w,n,TICK)};
}
F05DecisionView f05_decision_view(const WorldState& w,U d) {
 return {d,ref(w,d,F05_NEED_REF),ref(w,d,PERSON),val(w,d,F05_KEY),val(w,d,F05_REVISION),val(w,d,TICK),
  ref(w,d,F05_DETECTION_REF),ref(w,d,F05_ORDER_REF),ref(w,d,TARGET),w.revision(),
  uint32_t(val(w,d,F05_STATUS)),uint32_t(val(w,d,CODE)),uint32_t(val(w,d,F05_EXAMINED)),uint32_t(val(w,d,F05_BUDGET))};
}
void f05_learn(Campaign& c,U p,FactKey f) {
 const auto r=c.world.learn_fact(EntityId{p},f);
 need(r==KnowledgeChange::applied || r==KnowledgeChange::no_change,F04_INTERNAL);invalidate_index();
}
bool f05_service(const Campaign& c,U a,U p,U slot) {
 const auto& w=c.world;const U t=c.time.now();
 return type(w,a,"activity") && val(w,a,VALUE)==F04_DUTY && ref(w,a,PERSON)==p && ref(w,a,SLOT)==slot &&
  val(w,a,START)<=t && t<effective_end(w,a) && (val(w,a,STATE)==ACTIVE || has(w,a,STOP)) && duty(w,p,slot,t);
}
// Transaction extends across the existing public P01 APIs and P03 audit writes.
// Nothing is observable between these calls on the sole owner thread. On any
// unexpected failure restore the original Core campaign including RNG/Timeline.
template<class F> void f05_atomic(F04Session* s,F&& f) {
 auto previous=std::make_unique<Campaign>(*s->c);s->c.swap(previous);
 try {f();need(schema(*s->c),F04_INTERNAL);}
 catch(...) {s->c.swap(previous);invalidate_index();s->index_revision=UINT64_MAX;throw;}
 invalidate_index();s->index_revision=UINT64_MAX;
}
struct F05KnownNeed {U id=0,due=0,end=0,slot=0,person=0,duty=0;uint32_t examined=0;bool complete=false;};
F05KnownNeed f05_known_need(const WorldState& w,U actor,U input,U budget) {
 // No temporary grants: never consult truth to manufacture an unknown need.
 const auto view=Visibility::project(w,EntityId{actor});
 std::array<VisibleFact,32> facts{};ContextRequest request;request.subject=EntityId{input};
 const auto r=ContextBuilder::build(view,request,facts,{static_cast<size_t>(budget),32,8192});
 F05KnownNeed n;n.examined=uint32_t(r.examined);
 if(r.status!=ContextStatus::complete)return n;
 bool exists=false,definition=false,due=false,end=false;
 for(size_t i=0;i<r.emitted;++i) {
  const auto& f=facts[i];if(!f.present)continue;
  if(f.key.kind==FactKind::existence)exists=true;
  if(f.key.kind==FactKind::definition && f.definition_id()=="trek.f04:f05_scan_need")definition=true;
  if(f.key.kind!=FactKind::relation)continue;
  const U k=f.key.relation_kind.value();
  if(k==SLOT)n.slot=f.key.target.value();if(k==PERSON)n.person=f.key.target.value();if(k==ACTIVITY)n.duty=f.key.target.value();
  if((k>>48)==0xF000+START){n.due=k&FOREVER;due=true;}
  if((k>>48)==0xF000+END){n.end=k&FOREVER;end=true;}
 }
 n.complete=exists && definition && due && end && n.slot && n.person && n.duty;
 if(n.complete)n.id=input;return n;
}
struct F05Plan {
 U order=0,delegation=0,target=0;uint32_t decision=F05_CLARIFY,code=F04_REVIEW;
 bool detected=false,issue=false,receive=false,execute=false;
};
F05Plan f05_plan(const Campaign& c,U actor_id,const F05KnownNeed& known) {
 const auto& w=c.world;
  const U t=c.time.now(),actor=actor_id;U order=0,delegation=0,target=0;
  uint32_t decision=F05_CLARIFY,code=F04_REVIEW;bool detected=false,issue=false,receive=false,execute=false;
  if(actor==f05_player(w)){decision=F05_WAIT_PLAYER;code=F04_REVIEW;}
  else if(known.complete) {
   if(t<known.due){decision=F05_NO_ACTION;code=F04_OK;}
   else {
    detected=true;
    // Actual world reads below are authorization/physical checks, never new
    // operational facts supplied to the decision context.
    if(t>=known.end){decision=F05_REPORT;code=F04_EXPIRED;}
    else if(!available(w,actor,t)){decision=F05_NO_ACTION;code=F04_UNAVAILABLE;}
    else {
     for(U o:all(w,"f05_order"))if(ref(w,ref(w,o,F05_REQUEST_REF),F05_NEED_REF)==known.id){order=o;break;}
     if(order) {
      if(actor!=ref(w,order,PERSON) && actor!=ref(w,order,ISSUER) && actor!=commander(w,t)) {
       order=0;decision=F05_REPORT;code=F04_REVIEW;
      } else if(f05_terminal(val(w,order,F05_STATUS))){decision=F05_NO_ACTION;code=uint32_t(val(w,order,CODE));}
      else if(ref(w,order,PERSON)==f05_player(w)){decision=F05_WAIT_PLAYER;code=F04_REVIEW;}
      else if(actor!=ref(w,order,PERSON)){decision=F05_NO_ACTION;code=F04_OK;}
      else {decision=F05_CONTINUE_TASK;code=F04_OK;receive=val(w,order,F05_STATUS)==F05_ISSUED;execute=!receive;}
     } else {
      bool authorized=false;
      try{(void)f05_origin(c,actor);authorized=true;}catch(const Denial& d){code=d.code;}
      // Explicit mandates take precedence, including modes requiring approval.
      // A matching revoked/suspended grant is never used as authority.
      for(U d:all(w,"delegation"))if(has(w,d,F05_MODE) && ref(w,d,PERSON)==actor &&
       ref(w,d,SLOT)==known.slot && ref(w,d,F05_EXECUTOR_REF)==known.person) {
       try{f05_grant_live(c,d);delegation=d;authorized=true;break;}catch(const Denial& d0){if(!authorized)code=d0.code;}
      }
      if(!authorized){decision=active_role(w,actor,F04_FIRST,t)?F05_PROPOSE:F05_ESCALATE;target=commander(w,t);}
      else if(!f05_service(c,known.duty,known.person,known.slot)){decision=F05_ESCALATE;code=F04_UNAVAILABLE;target=commander(w,t);}
      else {
       try {need(scan_station(c,known.person)==known.slot,F04_SCOPE);issue=true;code=F04_OK;
        decision=delegation && val(w,delegation,F05_MODE)!=F05_DELEGATED_AUTONOMOUS?F05_PROPOSE:F05_ISSUE_ORDER;
       } catch(const Denial& d){decision=F05_REPORT;code=d.code;target=commander(w,t);}
      }
     }
    }
   }
  }
 return {order,delegation,target,decision,code,detected,issue,receive,execute};
}

}
uint32_t f05_player_binding(F04Session* s,F05PlayerBinding* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  const auto& w=s->c->world;const auto ids=all(w,"f05_player");need(ids.size()<=1,F04_SAVE);
  if(ids.empty())return F04_OK;
  const U id=ids[0],person=ref(w,id,PERSON);need(observer(s,{s->scope,person}),F04_SAVE);
  *out={{s->scope,person},id,val(w,id,F05_REVISION),val(w,id,TICK)};return F04_OK;
 });
}
uint32_t f05_bind_player(F04Session* s,F04Ref p,U revision) {
 return call(s,[&]()->uint32_t {
  need(observer(s,p),F04_DENIED);
  if(U current=f05_player(s->c->world)){need(current==p.id,F05_IDEMPOTENCY_CONFLICT);return F04_OK;}
  need(revision==s->c->world.revision(),F04_STALE);
  auto next=std::make_unique<Campaign>(*s->c);const U id=f05_record(*next,*s->content.catalog(),"f05_player",p.id);
  set(*next,id,F05_REVISION,revision);need(schema(*next),F04_INTERNAL);s->c.swap(next);return F04_OK;
 });
}
uint32_t f05_scan_need(F04Session* s,const F05ScanNeedRequest* q,F05NeedView* out) {
 if(!q || !out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  need(observer(s,q->issuer),F04_DENIED);const auto& w=s->c->world;
  need(q->key && q->key<=FOREVER && q->cause && q->cause<=FOREVER && q->expected_revision<=FOREVER,F04_ARGUMENT);
  for(U n:all(w,"f05_scan_need"))if(val(w,n,F05_KEY)==q->key) {
   const auto v=f05_need_view(w,n);
   need(v.issuer==q->issuer.id && v.duty==q->duty && v.input_revision==q->expected_revision &&
    v.due==q->due && v.end==q->end && v.cause==q->cause,F05_IDEMPOTENCY_CONFLICT);*out=v;return F04_OK;
  }
  need(f05_player(w),F04_REVIEW);need(q->expected_revision==w.revision(),F04_STALE);
  const U origin=f05_origin(*s->c,q->issuer.id),a=q->duty,slot=ref(w,a,SLOT),p=ref(w,a,PERSON);
  need(type(w,a,"activity") && val(w,a,VALUE)==F04_DUTY && type(w,slot,"slot") && val(w,slot,QUAL)==F04_SENSORS,F04_SCOPE);
  need(q->due>=s->c->time.now() && q->due>=val(w,a,START) && q->due<q->end && q->end<=effective_end(w,a) &&
   val(w,a,STATE)==ACTIVE && q->end<=FOREVER,F04_ARGUMENT);
  for(U n:all(w,"f05_scan_need"))need(ref(w,n,ACTIVITY)!=a,F05_TRANSITION);
  need(all(w,"f05_scan_need").size()<128,F04_CAPACITY);
  auto next=std::make_unique<Campaign>(*s->c);const U n=f05_record(*next,*s->content.catalog(),"f05_scan_need",p);
  link(*next,n,ISSUER,q->issuer.id);link(*next,n,ORIGIN,origin);link(*next,n,ACTIVITY,a);link(*next,n,SLOT,slot);
  set(*next,n,F05_KEY,q->key);set(*next,n,F05_REVISION,q->expected_revision);set(*next,n,START,q->due);set(*next,n,END,q->end);set(*next,n,CAUSE,q->cause);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);*out=f05_need_view(s->c->world,n);return F04_OK;
 });
}
uint32_t f05_brief_need(F04Session* s,F04Ref sender,F04Ref recipient,U revision,U n,U key,U cause,U* out) {
 if(!out)return F04_ARGUMENT;*out=0;return call(s,[&]()->uint32_t {
  need(observer(s,sender) && observer(s,recipient),F04_DENIED);const auto& w=s->c->world;
  need(key && key<=FOREVER && cause && cause<=FOREVER && revision<=FOREVER,F04_ARGUMENT);
  for(U b:all(w,"f05_brief"))if(val(w,b,F05_KEY)==key) {
   need(ref(w,b,ISSUER)==sender.id && ref(w,b,PERSON)==recipient.id && ref(w,b,F05_NEED_REF)==n &&
    val(w,b,F05_REVISION)==revision && val(w,b,CAUSE)==cause,F05_IDEMPOTENCY_CONFLICT);*out=b;return F04_OK;
  }
  need(type(w,n,"f05_scan_need"),F04_ARGUMENT);need(revision==w.revision(),F04_STALE);
  (void)f05_origin(*s->c,sender.id);
  need(sender.id==ref(w,n,ISSUER) || sender.id==commander(w,s->c->time.now()),F04_DENIED);
  need(all(w,"f05_brief").size()<512,F04_CAPACITY);
  auto next=std::make_unique<Campaign>(*s->c);const U b=f05_record(*next,*s->content.catalog(),"f05_brief",recipient.id);
  link(*next,b,ISSUER,sender.id);link(*next,b,F05_NEED_REF,n);set(*next,b,F05_KEY,key);set(*next,b,F05_REVISION,revision);set(*next,b,CAUSE,cause);
  for(U id:{n,ref(w,n,SLOT),ref(w,n,PERSON),ref(w,n,ACTIVITY)})f05_learn(*next,recipient.id,{EntityId{id}});
  for(auto k:f05_need_facts(w,n))f05_learn(*next,recipient.id,k);
  need(schema(*next),F04_INTERNAL);s->c.swap(next);*out=b;return F04_OK;
 });
}
uint32_t f05_evaluate(F04Session* s,const F05Evaluation* q,F05DecisionView* out) {
 if(!q || !out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  need(observer(s,q->actor),F04_DENIED);const auto& w=s->c->world;
  need(q->key && q->key<=FOREVER && q->need && q->need<=FOREVER && q->expected_revision<=FOREVER &&
   !q->reserved && q->max_facts && q->max_facts<=32,F04_ARGUMENT);
  for(U d:all(w,"f05_decision"))if(val(w,d,F05_KEY)==q->key) {
   need(ref(w,d,PERSON)==q->actor.id && val(w,d,F05_INPUT)==q->need && val(w,d,F05_REVISION)==q->expected_revision &&
    val(w,d,F05_BUDGET)==q->max_facts,F05_IDEMPOTENCY_CONFLICT);*out=f05_decision_view(w,d);return F04_OK;
  }
  need(f05_player(w),F04_REVIEW);need(q->expected_revision==w.revision(),F04_STALE);
  need(all(w,"f05_decision").size()<2048,F04_CAPACITY);
  const auto known=f05_known_need(w,q->actor.id,q->need,q->max_facts);
  const U t=s->c->time.now(),actor=q->actor.id;
  auto [order,delegation,target,decision,code,detected,issue,receive,execute]=f05_plan(*s->c,actor,known);
  U id=0;
  f05_atomic(s,[&] {
   const auto& cat=*s->content.catalog();const U revision=s->c->world.revision();
   if(issue) {
    const U deadline=delegation?std::min(known.end,val(s->c->world,delegation,END)):known.end;
    F05OrderRequest request{q->actor,{s->scope,known.person},{s->scope,1},{s->scope,known.slot},q->key,revision,deadline,known.id,F04_SCAN,0};
    F05Receipt r{};code=delegation?f05_submit_delegated(s,&request,delegation,&r):f05_submit(s,&request,&r);
    need(r.order,code==F04_OK?F04_INTERNAL:code);need(code!=F04_INTERNAL,F04_INTERNAL);order=r.order;
    link(*s->c,r.request,F05_NEED_REF,known.id);
    if(code!=F04_OK)decision=F05_ESCALATE;
   } else if(receive || execute) {
    F05Receipt r{};code=receive?f05_receive(s,q->actor,revision,order,&r):f05_execute_order(s,q->actor,revision,order,&r);
    need(code!=F04_INTERNAL && code!=F04_SAVE && code!=F04_CAPACITY,code);
    if(code==F04_REVIEW){decision=F05_PROPOSE;target=commander(s->c->world,t);}
    else if(code!=F04_OK)decision=F05_ESCALATE;
   }
   auto& final=*s->c;U detection=0;
   if(detected){detection=f05_record(final,cat,"f05_detection",actor);link(final,detection,F05_NEED_REF,known.id);set(final,detection,F05_REVISION,q->expected_revision);}
   id=f05_record(final,cat,"f05_decision",actor);link(final,id,F05_NEED_REF,known.id);link(final,id,F05_DETECTION_REF,detection);link(final,id,F05_ORDER_REF,order);link(final,id,TARGET,target);
   set(final,id,F05_KEY,q->key);set(final,id,F05_REVISION,q->expected_revision);set(final,id,F05_INPUT,q->need);
   set(final,id,F05_BUDGET,q->max_facts);set(final,id,F05_EXAMINED,known.examined);set(final,id,F05_STATUS,decision);set(final,id,CODE,code);
  });
  *out=f05_decision_view(s->c->world,id);return F04_OK;
 });
}
uint32_t f05_decisions_page(F04Session* s,F04Ref actor,U after,F05DecisionView* out,U capacity,U* written,uint32_t* more) {
 if(!out || !written || !more || !capacity || capacity>64)return F04_ARGUMENT;*written=0;*more=0;
 return call(s,[&]()->uint32_t {
  need(observer(s,actor),F04_DENIED);const auto& w=s->c->world;
  for(U id:all(w,"f05_decision"))if(id>after && ref(w,id,PERSON)==actor.id) {
   if(*written==capacity){*more=1;break;}out[(*written)++]=f05_decision_view(w,id);
  }return F04_OK;
 });
}
