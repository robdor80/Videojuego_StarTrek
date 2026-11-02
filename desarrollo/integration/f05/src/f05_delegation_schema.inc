bool f05_delegations_schema(const Campaign& c) {
 const auto& w=c.world;std::set<U> keys,events,approvals;U count=0;
 if(all(w,"f05_delegation_event").size()>4096)return false;
 for(U d:all(w,"delegation"))if(has(w,d,F05_MODE)) {
  if(++count>256)return false;
  const U issuer=ref(w,d,ISSUER),person=ref(w,d,PERSON),origin=ref(w,d,ORIGIN),holder=ref(w,d,F05_HOLDER_REF),executor=ref(w,d,F05_EXECUTOR_REF);
  if(issuer==person || !type(w,origin,"appointment") || ref(w,origin,PERSON)!=issuer ||
   !type(w,holder,"appointment") || ref(w,holder,PERSON)!=person || !type(w,executor,"person") ||
   !type(w,ref(w,d,SLOT),"slot") || val(w,ref(w,d,SLOT),DEPT)!=F04_SENSORS ||
   val(w,d,D_DOMAIN)!=F04_SENSORS || val(w,d,OP)!=F04_SCAN || !val(w,d,F05_KEY) || !val(w,d,CAUSE) ||
   val(w,d,TICK)>val(w,d,START) || val(w,d,END)>val(w,origin,END) || val(w,d,END)>val(w,holder,END))return false;
  const auto role=[](U r){return r==F04_CAPTAIN || r==F04_FIRST || r==F04_SECOND || r==F04_SUCCESSOR || r==F04_WATCH;};
  if(!role(val(w,origin,ROLE)) || !(role(val(w,holder,ROLE)) || (val(w,holder,ROLE)==F04_HEAD && val(w,holder,DEPT)==F04_SENSORS)))return false;
  U previous=0,state=0,mode=0,tick=val(w,d,TICK);
  for(U e:all(w,"f05_delegation_event"))if(ref(w,e,F05_DELEGATION_REF)==d) {
   const U next=val(w,e,F05_STATUS),m=val(w,e,F05_MODE),at=val(w,e,TICK),op=val(w,e,OP);
   if(!events.insert(e).second || !keys.insert(val(w,e,F05_KEY)).second || !val(w,e,F05_KEY) || !val(w,e,CAUSE) ||
    ref(w,e,F05_PREVIOUS_REF)!=previous || !f05_delegation_step(state,next) ||
    m<F05_MANUAL || m>F05_DELEGATED_AUTONOMOUS || at<tick || at>c.time.now())return false;
   if(!previous) {
    if(op || ref(w,e,PERSON)!=issuer || val(w,e,F05_KEY)!=val(w,d,F05_KEY) ||
     val(w,e,F05_REVISION)!=val(w,d,F05_REVISION) || val(w,e,CAUSE)!=val(w,d,CAUSE) || at!=val(w,d,TICK))return false;
   } else if(op!=1)return false;
   if(next==F05_EXPIRED && at<val(w,d,END))return false;
   previous=e;state=next;mode=m;tick=at;
  }
  if(!previous || previous!=ref(w,d,F05_PREVIOUS_REF) || state!=val(w,d,F05_STATUS) || mode!=val(w,d,F05_MODE) ||
   (state!=F05_ACTIVE && val(w,d,STATE)!=CANCELLED))return false;
 }
 if(events.size()!=all(w,"f05_delegation_event").size())return false;
 for(U o:all(w,"f05_order"))if(U a=ref(w,o,F05_APPROVAL_REF)) {
  const U r=ref(w,o,F05_REQUEST_REF),d=ref(w,r,F05_DELEGATION_REF);
  if(!type(w,a,"f05_approval") || !approvals.insert(a).second || !type(w,d,"delegation") || !has(w,d,F05_MODE) ||
   ref(w,a,F05_ORDER_REF)!=o || ref(w,a,F05_DELEGATION_REF)!=d || ref(w,a,PERSON)!=ref(w,d,ISSUER) ||
   !val(w,a,CAUSE) || val(w,a,TICK)<val(w,r,TICK) || val(w,a,TICK)>c.time.now())return false;
 }
 return approvals.size()==all(w,"f05_approval").size();
}
