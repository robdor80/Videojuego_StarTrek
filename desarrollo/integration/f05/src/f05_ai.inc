namespace {
void f05_ai_access(F04Session* s,F04Ref actor,U r) {
 need(observer(s,actor),F04_DENIED);
 // Do not expose even the existence of another actor's private proposal.
 need(type(s->c->world,r,"f05_ai_request") && ref(s->c->world,r,PERSON)==actor.id,F04_DENIED);
}
F05AiView f05_ai_state(const WorldState& w,U r) {
 const U d=ref(w,r,F05_AI_DECISION_REF);
 return {r,ref(w,r,PERSON),val(w,r,F05_BEFORE),val(w,r,F05_AFTER),val(w,r,TICK),val(w,r,END),d,d?ref(w,d,F05_ORDER_REF):0,w.revision(),
  uint32_t(val(w,r,F05_STATUS)),uint32_t(val(w,r,F05_AI_ERROR)),uint32_t(val(w,r,F05_AI_INTENT)),uint32_t(val(w,r,F05_AI_ROUTE))};
}
F05AiContext f05_ai_context(F04Session* s,U r) {
 const auto& w=s->c->world;const U a=ref(w,r,PERSON);
 F05AiContext c{r,a,r,val(w,r,F05_BEFORE),val(w,r,TICK),val(w,r,END),0,0,0,0,0,0,1,uint32_t(val(w,r,F05_AI_ROUTE)),0,0};
 if(c.revision!=w.revision() || s->ai_requests[r]!=s->scope)return c;
 const auto n=f05_known_need(w,a,val(w,r,F05_INPUT),32);
 if(n.complete){c.complete=1;c.need=n.id;c.duty=n.duty;c.station=n.slot;c.operator_id=n.person;c.due=n.due;c.end=n.end;c.allowed_operation=F04_SCAN;}
 return c;
}
void f05_ai_settle(Campaign& c,U r,U status,U error,U intent) {
 set(c,r,F05_STATUS,status);set(c,r,F05_AI_ERROR,error);set(c,r,F05_AI_INTENT,intent);
 // Updating the existing scalar removes one edge and adds one edge.
 const U final_revision=c.world.revision()+2;set(c,r,F05_AFTER,final_revision);
 need(c.world.revision()==final_revision,F04_INTERNAL);
}
}
uint32_t f05_ai_begin(F04Session* s,const F05AiRequest* q,F05AiContext* out) {
 if(!q || !out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  need(observer(s,q->actor),F04_DENIED);const auto& w=s->c->world;
  need(q->key && q->key<=FOREVER && q->need && q->need<=FOREVER && q->expected_revision<=FOREVER && !q->reserved &&
   q->route>=F05_AI_DETERMINISTIC && q->route<=F05_AI_REASONING,F04_ARGUMENT);
  for(U r:all(w,"f05_ai_request"))if(val(w,r,F05_KEY)==q->key) {
   need(ref(w,r,PERSON)==q->actor.id && val(w,r,F05_INPUT)==q->need && val(w,r,F05_REVISION)==q->expected_revision &&
    val(w,r,END)==q->expires && val(w,r,F05_AI_ROUTE)==q->route,F05_IDEMPOTENCY_CONFLICT);
   *out=f05_ai_context(s,r);return F04_OK;
  }
  need(f05_player(w),F04_REVIEW);need(q->expected_revision==w.revision(),F04_STALE);
  const U now=s->c->time.now();need(q->expires>now && q->expires<=FOREVER && q->expires-now<=300,F04_ARGUMENT);
  need(all(w,"f05_ai_request").size()<512,F04_CAPACITY);
  const auto n=f05_known_need(w,q->actor.id,q->need,32);U r=0;
  f05_atomic(s,[&] {
   auto& c=*s->c;r=f05_record(c,*s->content.catalog(),"f05_ai_request",q->actor.id);
   set(c,r,F05_KEY,q->key);set(c,r,F05_REVISION,q->expected_revision);set(c,r,F05_INPUT,q->need);set(c,r,END,q->expires);
   set(c,r,F05_STATUS,F05_AI_PENDING);set(c,r,F05_AI_ROUTE,q->route);set(c,r,F05_AI_ERROR,0);set(c,r,F05_AI_INTENT,0);link(c,r,F05_NEED_REF,n.id);
   const U final_revision=c.world.revision()+2;set(c,r,F05_BEFORE,final_revision);set(c,r,F05_AFTER,final_revision);need(c.world.revision()==final_revision,F04_INTERNAL);
  });
  s->ai_requests[r]=s->scope;*out=f05_ai_context(s,r);return F04_OK;
 });
}
uint32_t f05_ai_view(F04Session* s,F04Ref actor,U request,F05AiView* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {f05_ai_access(s,actor,request);*out=f05_ai_state(s->c->world,request);return F04_OK;});
}
uint32_t f05_ai_finish(F04Session* s,F04Ref actor,U r,const char* json,U size,uint32_t error,F05AiView* out) {
 if(!out || error>F05_AI_QUOTA || (size && !json))return F04_ARGUMENT;*out={};
 return call(s,[&]()->uint32_t {
  f05_ai_access(s,actor,r);const auto& w=s->c->world;
  if(val(w,r,F05_STATUS)!=F05_AI_PENDING){*out=f05_ai_state(w,r);return F04_OK;} // first terminal result wins
  U status=F05_AI_REJECTED,intent=0;trek::ai::Proposal p;
  if(s->ai_requests[r]!=s->scope){status=F05_AI_STALE;error=F05_AI_RECOVERED;}
  else if(w.revision()!=val(w,r,F05_BEFORE) || s->c->time.now()>=val(w,r,END)){status=F05_AI_STALE;error=F05_AI_BINDING;}
  else if(val(w,r,F05_AI_ROUTE)==F05_AI_DETERMINISTIC){status=F05_AI_FALLBACK;error=F05_AI_NOT_CONFIGURED;}
  else if(error){status=F05_AI_FALLBACK;}
  else if(!size){status=F05_AI_FALLBACK;error=F05_AI_EMPTY;}
  else if(size>8192 || !trek::ai::parse(json,size,p)){error=F05_AI_MALFORMED;}
  else if(p.actor!=actor.id || p.request!=r || p.projection!=r || p.revision!=val(w,r,F05_BEFORE) || p.issued!=val(w,r,TICK) || p.expires!=val(w,r,END)){error=F05_AI_BINDING;}
  else {
   const auto n=f05_known_need(w,actor.id,val(w,r,F05_INPUT),32);
   if(!n.complete || p.insufficient){status=F05_AI_INSUFFICIENT;intent=F05_AI_UNKNOWN;}
   else if(p.clarification){status=F05_AI_CLARIFICATION;intent=F05_AI_ASK;}
   else {
    const auto plan=f05_plan(*s->c,actor.id,n);intent=p.intent;status=F05_AI_VALID;
    if(p.scan) {
     if(plan.decision==F05_WAIT_PLAYER || plan.decision==F05_PROPOSE)status=F05_AI_APPROVAL;
     else if(!plan.issue && !plan.receive && !plan.execute){status=F05_AI_REJECTED;error=F05_AI_RESTRICTION;intent=0;}
    }
   }
  }
  // Model prose is never presented as truth or stored as knowledge. The Host
  // may expose it only as untrusted advice; presentation uses controlled state.
  f05_atomic(s,[&]{f05_ai_settle(*s->c,r,status,error,intent);});
  *out=f05_ai_state(s->c->world,r);return F04_OK;
 });
}
uint32_t f05_ai_apply(F04Session* s,F04Ref actor,U r,F05AiView* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  f05_ai_access(s,actor,r);const auto& w=s->c->world;
  if(val(w,r,F05_STATUS)==F05_AI_APPLIED){*out=f05_ai_state(w,r);return F04_OK;}
  need((val(w,r,F05_STATUS)==F05_AI_VALID || val(w,r,F05_STATUS)==F05_AI_APPROVAL) && val(w,r,F05_AI_INTENT)==F05_AI_SCAN,F04_REVIEW);
  if(w.revision()!=val(w,r,F05_AFTER) || s->c->time.now()>=val(w,r,END)) {
   f05_atomic(s,[&]{f05_ai_settle(*s->c,r,F05_AI_STALE,F05_AI_BINDING,0);});*out=f05_ai_state(s->c->world,r);return F04_OK;
  }
  // The model selected only a supported intent. P03 computes the entire actual
  // plan again, including grants, health, duty, player identity and operation.
  F05Evaluation q{actor,val(w,r,F05_INPUT),val(w,r,F05_KEY),w.revision(),32,0};F05DecisionView d{};
  f05_atomic(s,[&]{const auto code=f05_evaluate(s,&q,&d);need(code==F04_OK,code);link(*s->c,r,F05_AI_DECISION_REF,d.id);set(*s->c,r,F05_STATUS,F05_AI_APPLIED);});
  *out=f05_ai_state(s->c->world,r);return F04_OK;
 });
}
