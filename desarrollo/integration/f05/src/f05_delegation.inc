// Included in the existing F04/F05 domain namespace; no second permission store.
U f05_holder(const Campaign& c,U p) {
 const auto& w=c.world;const U t=c.time.now();
 need(available(w,p,t) && primary_operator(w,p),F04_UNAVAILABLE);
 need(qualified(w,p,F04_COMMAND,t),F04_QUALIFICATION);
 for(U a:person_records(w,"appointment",p))if(window(w,a,t)) {
  const U role=val(w,a,ROLE);
  if(role==F04_CAPTAIN || role==F04_FIRST || role==F04_SECOND || role==F04_SUCCESSOR || role==F04_WATCH ||
   (role==F04_HEAD && val(w,a,DEPT)==F04_SENSORS))return a;
 }
 need(false,F04_DENIED);return 0;
}
void f05_grant_source(const Campaign& c,U issuer,U origin) {
 const auto& w=c.world;const U t=c.time.now();
 need(available(w,issuer,t),F04_UNAVAILABLE);
 need(type(w,origin,"appointment") && window(w,origin,t) && ref(w,origin,PERSON)==issuer,F04_REVOKED);
 need(commander(w,t)==issuer,F04_DENIED);
 // The precise original appointment must still confer command, not a new title.
 const U role=val(w,origin,ROLE);
 need(role==F04_CAPTAIN || role==F04_FIRST || role==F04_SECOND || role==F04_SUCCESSOR || role==F04_WATCH,F04_DENIED);
 need(qualified(w,issuer,F04_COMMAND,t),F04_QUALIFICATION);
}
void f05_grant_live(const Campaign& c,U d,bool check_state=true) {
 const auto& w=c.world;const U t=c.time.now(),p=ref(w,d,PERSON),h=ref(w,d,F05_HOLDER_REF);
 need(type(w,d,"delegation") && has(w,d,F05_MODE),F04_ARGUMENT);
 if(check_state && val(w,d,F05_STATUS)==F05_EXPIRED)need(false,F04_EXPIRED);
 if(check_state)need(val(w,d,F05_STATUS)==F05_ACTIVE && val(w,d,STATE)==ACTIVE,F04_REVOKED);
 need(t>=val(w,d,START),F04_UNAVAILABLE);need(t<val(w,d,END),F04_EXPIRED);
 f05_grant_source(c,ref(w,d,ISSUER),ref(w,d,ORIGIN));
 need(available(w,p,t) && primary_operator(w,p),F04_UNAVAILABLE);
 need(qualified(w,p,F04_COMMAND,t),F04_QUALIFICATION);
 need(type(w,h,"appointment") && ref(w,h,PERSON)==p && window(w,h,t),F04_REVOKED);
 // A WATCH appointment ends its authority with actual service, including relief.
 if(val(w,h,ROLE)==F04_WATCH || val(w,1,SCHEMA)==4)need(scheduled(w,p,t),F04_UNAVAILABLE);
}
void f05_delegated_authority(const Campaign& c,U d,U request) {
 const auto& w=c.world;f05_grant_live(c,d);
 need(ref(w,request,ISSUER)==ref(w,d,PERSON),F04_DENIED);
 need(val(w,request,OP)==val(w,d,OP) && val(w,d,D_DOMAIN)==F04_SENSORS,F04_SCOPE);
 need(ref(w,request,SHIP)==ref(w,d,SHIP) && ref(w,request,SLOT)==ref(w,d,SLOT) &&
  ref(w,request,PERSON)==ref(w,d,F05_EXECUTOR_REF),F04_SCOPE);
 need(val(w,request,END)<=val(w,d,END),F04_EXPIRED);
}
void f05_approval_required(const Campaign& c,U order) {
 const auto& w=c.world;const U d=ref(w,ref(w,order,F05_REQUEST_REF),F05_DELEGATION_REF);
 if(d && val(w,d,F05_MODE)!=F05_DELEGATED_AUTONOMOUS)need(ref(w,order,F05_APPROVAL_REF),F04_REVIEW);
}
void f05_delegation_access(F04Session* s,F04Ref who,U d) {
 need(observer(s,who),F04_DENIED);const auto& w=s->c->world;
 need(type(w,d,"delegation") && has(w,d,F05_MODE),F04_ARGUMENT);
 need(who.id==ref(w,d,ISSUER) || who.id==ref(w,d,PERSON) || who.id==commander(w,s->c->time.now()),F04_DENIED);
}
F05DelegationView f05_delegation_view(const Campaign& c,U d) {
 const auto& w=c.world;uint32_t code=F04_OK;
 try{f05_grant_live(c,d);}catch(const Denial& e){code=e.code;}
 return {d,ref(w,d,ISSUER),ref(w,d,PERSON),1,ref(w,d,SLOT),ref(w,d,F05_EXECUTOR_REF),ref(w,d,ORIGIN),ref(w,d,F05_HOLDER_REF),
  val(w,d,F05_KEY),val(w,d,F05_REVISION),val(w,d,START),val(w,d,END),val(w,d,CAUSE),ref(w,d,F05_PREVIOUS_REF),w.revision(),
  uint32_t(val(w,d,D_DOMAIN)),uint32_t(val(w,d,OP)),uint32_t(val(w,d,F05_STATUS)),uint32_t(val(w,d,F05_MODE)),code,0};
}
void f05_grant_event(Campaign& c,const ContentCatalog& cat,U d,U actor,U key,U revision,U cause,U state,U mode,U op) {
 need(all(c.world,"f05_delegation_event").size()<4096,F04_CAPACITY);
 const U e=make(c,cat,"f05_delegation_event");link(c,e,SHIP,1);link(c,e,PERSON,actor);link(c,e,F05_DELEGATION_REF,d);
 link(c,e,F05_PREVIOUS_REF,ref(c.world,d,F05_PREVIOUS_REF));
 set(c,e,F05_KEY,key);set(c,e,F05_REVISION,revision);set(c,e,CAUSE,cause);set(c,e,TICK,c.time.now());
 set(c,e,F05_STATUS,state);set(c,e,F05_MODE,mode);set(c,e,OP,op);
 link(c,d,F05_PREVIOUS_REF,e);set(c,d,F05_STATUS,state);set(c,d,F05_MODE,mode);set(c,d,STATE,state==F05_ACTIVE?ACTIVE:CANCELLED);
}
