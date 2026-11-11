namespace {
U f11_billet(const WorldState& w,U p) {
 for(U slot:all(w,"slot"))if(ref(w,slot,PERSON)==p)return slot;
 return 0;
}
void f11_subject(F04Session* s,F04Ref subject) {
 need(subject.scope==s->scope,F04_SCOPE);
 need(type(s->c->world,subject.id,"person"),F04_SCOPE);
}
F11PromotionReceipt f11_receipt(const Campaign& c,U e) {
 const auto& w=c.world;
 return {f11_identity(w,e),val(w,e,F11_KEY),e,ref(w,e,F11_ORDER_REF),e,
  val(w,e,F11_COMMIT_REVISION),w.revision(),val(w,e,TICK),
  uint32_t(val(w,e,F11_FROM)),uint32_t(val(w,e,F11_TO)),F04_OK,0};
}
bool f11_same(const WorldState& w,U e,const F11PromotionRequest& q) {
 return f11_equal(f11_identity(w,e),q.character) && ref(w,e,PERSON)==q.subject.id &&
  ref(w,e,F11_GRANT_REF)==q.grant && ref(w,e,F11_ORDER_REF)==q.order &&
  ref(w,e,F11_EVALUATION_REF)==q.evaluation && ref(w,e,F11_COMMISSION_REF)==q.commission &&
  ref(w,e,F11_RANK_EVENT_REF)==q.rank_event && ref(w,e,F11_CAUSE_REF)==q.cause &&
  val(w,e,F11_FROM)==q.from_rank && val(w,e,F11_TO)==q.to_rank && val(w,e,TICK)==q.effective_tick;
}
void f11_validate(const Campaign& c,const F11PromotionRequest& q) {
 const auto& w=c.world;const U p=q.subject.id,t=c.time.now();
 need(has(w,p,F11_VERSION),F11_UNCOMMISSIONED);
 need(f11_equal(f11_identity(w,p),q.character),F11_IDENTITY);
 need(q.from_rank==1101 && q.to_rank==1102 && val(w,p,RANK)==1101,F11_RANK);
 need(member(w,p) && val(w,p,F11_SERVICE)==1 && val(w,p,CATEGORY)==1,F11_UNCOMMISSIONED);
 need(q.commission==ref(w,p,F11_COMMISSION_REF) && type(w,q.commission,"f11_commission"),F11_UNCOMMISSIONED);
 need(q.rank_event==ref(w,p,F11_RANK_EVENT_REF) && q.rank_event==q.commission,F11_RANK);
 need(q.effective_tick==t,F04_EXPIRED);
 need(type(w,q.grant,"f11_grant") && window(w,q.grant,t),F11_AUTHORITY);
 need(type(w,ref(w,q.grant,F11_ROOT_REF),"f11_root") &&
  type(w,ref(w,q.grant,F11_AUTHORITY_REF),"f11_office") && val(w,q.grant,D_DOMAIN)==1 &&
  val(w,q.grant,F11_FROM)==q.from_rank && val(w,q.grant,F11_TO)==q.to_rank,F11_AUTHORITY);
 need(type(w,q.evaluation,"f11_evaluation") && window(w,q.evaluation,t) && ref(w,q.evaluation,PERSON)==p &&
  ref(w,q.evaluation,F11_COMMISSION_REF)==q.commission && ref(w,q.evaluation,F11_RANK_EVENT_REF)==q.rank_event,F11_EVALUATION);
 need(type(w,q.order,"f11_personnel_order") && window(w,q.order,t) && ref(w,q.order,PERSON)==p,F11_ORDER);
 for(auto [r,expected]:std::initializer_list<std::pair<Ref,U>>{{F11_GRANT_REF,q.grant},{F11_COMMISSION_REF,q.commission},
   {F11_RANK_EVENT_REF,q.rank_event},{F11_EVALUATION_REF,q.evaluation},{F11_CAUSE_REF,q.cause}})
  need(ref(w,q.order,r)==expected,F11_ORDER);
 need(ref(w,q.order,F11_AUTHORITY_REF)==ref(w,q.grant,F11_AUTHORITY_REF) &&
  val(w,q.order,F11_FROM)==q.from_rank && val(w,q.order,F11_TO)==q.to_rank,F11_ORDER);
 need(type(w,q.cause,"f11_cause") && ref(w,q.cause,PERSON)==p && val(w,q.cause,TICK)<=t,F11_ORDER);
}
#ifdef F11_NATIVE_TEST_HOST
thread_local U f11_fault=0;
void f11_boundary(U stage) {if(f11_fault==stage){f11_fault=0;throw std::runtime_error("injected F11 preparation failure");}}
#else
void f11_boundary(U) {}
#endif
}
uint32_t f11_commit_promotion(F04Session* s,const F11PromotionRequest* q,F11PromotionReceipt* out) {
 if(!q || !out)return F04_ARGUMENT;*out={};
 const auto code=call(s,[&]()->uint32_t {
  need(f11_valid_identity(q->character) && q->key && q->key<=FOREVER && q->expected_revision<=FOREVER &&
   q->effective_tick<=FOREVER,F04_ARGUMENT);
  f11_subject(s,q->subject);
  const auto& live=*s->c;const auto& w=live.world;
  for(U e:all(w,"promotion"))if(val(w,e,F11_KEY)==q->key) {
   need(f11_same(w,e,*q),F11_IDEMPOTENCY_CONFLICT);*out=f11_receipt(live,e);return F04_OK;
  }
  need(q->expected_revision==w.revision(),F04_STALE);
  f11_validate(live,*q);
  auto next=std::make_unique<Campaign>(live);const auto& cat=*s->content.catalog();
  f11_boundary(1);
  const U e=make(*next,cat,"promotion");
  for(auto [field,value]:std::initializer_list<std::pair<Field,U>>{{F11_VERSION,1},{F11_ID_HIGH,q->character.high48},
   {F11_ID_MID,q->character.mid48},{F11_ID_LOW,q->character.low32},{TICK,q->effective_tick},
   {F11_KEY,q->key},{F11_INPUT_REVISION,q->expected_revision},{F11_FROM,q->from_rank},{F11_TO,q->to_rank},
   {F11_VISIBILITY,F11_SUBJECT_AND_PERSONNEL},{DEPT,val(w,q->subject.id,DEPT)}})set(*next,e,field,value);
  for(auto [r,target]:std::initializer_list<std::pair<Ref,U>>{{SHIP,1},{PERSON,q->subject.id},
   {SLOT,f11_billet(w,q->subject.id)},{F11_ROOT_REF,ref(w,q->grant,F11_ROOT_REF)},
   {F11_AUTHORITY_REF,ref(w,q->grant,F11_AUTHORITY_REF)},{F11_GRANT_REF,q->grant},{F11_ORDER_REF,q->order},
   {F11_EVALUATION_REF,q->evaluation},{F11_COMMISSION_REF,q->commission},{F11_RANK_EVENT_REF,q->rank_event},
   {F11_CAUSE_REF,q->cause}})link(*next,e,r,target);
  f11_boundary(2); // Complete event, old rank. Never visible to caller/save.
  set(*next,q->subject.id,RANK,1102);
  f11_boundary(3); // New grade, old rank pointer. Still private staging.
  link(*next,q->subject.id,F11_RANK_EVENT_REF,e);
  set(*next,e,F11_COMMIT_REVISION,next->world.revision()+1);
  need(schema(*next),F04_INTERNAL);
  f11_boundary(4);
  // Single owner thread (call guard); recheck all live preconditions at publish.
  need(s->c->world.revision()==q->expected_revision,F04_STALE);f11_validate(*s->c,*q);
  const auto receipt=f11_receipt(*next,e);
  f11_boundary(5);
  s->c.swap(next);s->index_revision=UINT64_MAX;*out=receipt;return F04_OK;
 });
 if(code!=F04_OK){*out={};out->status=code;}
 return code;
}
uint32_t f11_personnel(F04Session* s,F04Ref subject,F11PersonnelView* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  f11_subject(s,subject);const auto& w=s->c->world;const U p=subject.id;
  need(has(w,p,F11_VERSION),F11_UNCOMMISSIONED);
  *out={f11_identity(w,p),p,ref(w,p,F11_COMMISSION_REF),ref(w,p,F11_RANK_EVENT_REF),ref(w,p,SHIP),
   f11_billet(w,p),val(w,p,DEPT),w.revision(),uint32_t(val(w,p,RANK)),uint32_t(val(w,p,F11_SERVICE))};return F04_OK;
 });
}
uint32_t f11_promotion(F04Session* s,F04Ref subject,U e,F11PromotionView* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
  f11_subject(s,subject);const auto& w=s->c->world;
  need(type(w,e,"promotion"),F04_ARGUMENT);need(ref(w,e,PERSON)==subject.id,F04_DENIED);
  *out={f11_receipt(*s->c,e),subject.id,ref(w,e,SHIP),ref(w,e,SLOT),val(w,e,DEPT),
   ref(w,e,F11_GRANT_REF),ref(w,e,F11_AUTHORITY_REF),ref(w,e,F11_ROOT_REF),
   ref(w,e,F11_COMMISSION_REF),ref(w,e,F11_RANK_EVENT_REF),ref(w,e,F11_EVALUATION_REF),ref(w,e,F11_CAUSE_REF),
   val(w,e,F11_INPUT_REVISION),uint32_t(val(w,e,F11_VISIBILITY)),0};return F04_OK;
 });
}
