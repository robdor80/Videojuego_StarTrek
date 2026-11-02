// Included inside F04's domain namespace. The Core graph is the only storage.
bool f05_shape(const WorldState& w,U id,std::set<U>& a,std::set<U>& q,std::set<U>& ar,std::set<U>& rr) {
 if(type(w,id,"f05_request")) {
  a={F05_KEY,F05_REVISION,END,OP,CAUSE,TICK};ar={SHIP,ISSUER,PERSON,SLOT};q=a;rr=ar;
 } else if(type(w,id,"f05_order")) {
  a={F05_STATUS,CODE,TICK};q=a;ar={SHIP,ISSUER,PERSON,SLOT,F05_REQUEST_REF,ORIGIN,F05_TASK_REF,F05_RESULT_REF,F05_PREVIOUS_REF};
  rr={SHIP,ISSUER,PERSON,SLOT,F05_REQUEST_REF,F05_PREVIOUS_REF};
 } else if(type(w,id,"f05_task")) {
  a={F05_STATUS,TICK};ar={SHIP,PERSON,F05_ORDER_REF};q=a;rr=ar;
 } else if(type(w,id,"f05_attempt")) {
  a={F05_REVISION,TICK};ar={SHIP,PERSON,F05_ORDER_REF,F05_TASK_REF};q=a;rr=ar;
 } else if(type(w,id,"f05_result")) {
  a={VALUE,CODE,F05_OUTCOME,F05_REJECTION,F05_BEFORE,F05_AFTER,F05_ROLL,F05_CONSUMED,F05_STREAM,TICK};
  ar={SHIP,PERSON,F05_ORDER_REF,F05_TASK_REF,F05_ATTEMPT_REF};q=a;rr=ar;
 } else if(type(w,id,"f05_event")) {
  a={F05_STATUS,CODE,TICK};q=a;ar={SHIP,PERSON,F05_REQUEST_REF,F05_ORDER_REF,F05_TASK_REF,F05_ATTEMPT_REF,F05_RESULT_REF,F05_PREVIOUS_REF};
  rr={SHIP,PERSON,F05_REQUEST_REF,F05_ORDER_REF};
 } else return false;
 return true;
}
bool f05_terminal(U state) {return state>=F05_COMPLETED && state<=F05_CANCELLED;}
bool f05_step(U from,U to) {
 return (!from && to==F05_ISSUED) ||
  (from==F05_ISSUED && (to==F05_ACCEPTED || to==F05_REFUSED || to==F05_CANCELLED)) ||
  (from==F05_ACCEPTED && (to==F05_EXECUTING || to==F05_CANCELLED)) ||
  (from==F05_EXECUTING && (to==F05_COMPLETED || to==F05_FAILED));
}
bool f05_schema(const Campaign& c) {
 const auto& w=c.world;std::set<U> keys,requests,tasks,attempts,results,events;
 const auto orders=all(w,"f05_order");if(orders.size()>512)return false;
 for(U o:orders) {
  const U r=ref(w,o,F05_REQUEST_REF),task=ref(w,o,F05_TASK_REF),result=ref(w,o,F05_RESULT_REF),state=val(w,o,F05_STATUS);
  if(!type(w,r,"f05_request") || !requests.insert(r).second || !keys.insert(val(w,r,F05_KEY)).second ||
   !val(w,r,F05_KEY) || !val(w,r,CAUSE) || val(w,r,TICK)>c.time.now() || val(w,r,END)<=val(w,r,TICK) ||
   state<F05_ISSUED || state>F05_CANCELLED || val(w,o,CODE)>F05_TRANSITION || val(w,o,TICK)>c.time.now())return false;
  for(Ref f:{SHIP,ISSUER,PERSON,SLOT})if(ref(w,o,f)!=ref(w,r,f))return false;
  if(!type(w,ref(w,o,SLOT),"slot"))return false;
  const U origin=ref(w,o,ORIGIN);
  if((!origin && state!=F05_REFUSED) || (origin && (!type(w,origin,"appointment") || ref(w,origin,PERSON)!=ref(w,o,ISSUER))))return false;
  if(val(w,o,TICK)!=val(w,r,TICK))return false;
  if((state==F05_ISSUED || state==F05_REFUSED) && task)return false;
  if((state==F05_ACCEPTED || state==F05_COMPLETED || state==F05_FAILED) && !task)return false;
  if(state==F05_EXECUTING)return false; // Never publish a half-applied action.
  if((state==F05_COMPLETED || state==F05_FAILED)!=bool(result))return false;
  if(state==F05_COMPLETED && val(w,o,CODE)!=F04_OK)return false;
  if((state==F05_FAILED || state==F05_REFUSED) && val(w,o,CODE)==F04_OK)return false;
  if(task) {
   if(!type(w,task,"f05_task") || !tasks.insert(task).second || ref(w,task,F05_ORDER_REF)!=o || ref(w,task,PERSON)!=ref(w,o,PERSON))return false;
   const U expected=state==F05_ACCEPTED?F05_TASK_ACKNOWLEDGED:state==F05_COMPLETED?F05_TASK_COMPLETED:state==F05_CANCELLED?F05_TASK_CANCELLED:F05_TASK_FAILED;
   if(val(w,task,F05_STATUS)!=expected || val(w,task,TICK)>c.time.now())return false;
  }
  if(result) {
   const U at=ref(w,result,F05_ATTEMPT_REF),performed=val(w,result,VALUE),code=val(w,result,CODE);
   if(!type(w,result,"f05_result") || !results.insert(result).second || !type(w,at,"f05_attempt") || !attempts.insert(at).second ||
    code!=val(w,o,CODE) || performed>1 || val(w,result,TICK)>c.time.now() || val(w,at,TICK)!=val(w,result,TICK))return false;
   for(U x:{result,at})if(ref(w,x,F05_ORDER_REF)!=o || ref(w,x,F05_TASK_REF)!=task || ref(w,x,PERSON)!=ref(w,o,PERSON))return false;
   if(performed) {
    if(val(w,r,OP)!=F04_SCAN || val(w,result,F05_OUTCOME)>2 || val(w,result,F05_REJECTION)>uint32_t(ActionRejection::invalid_operation) ||
     val(w,result,F05_BEFORE)>val(w,result,F05_AFTER) || val(w,result,F05_AFTER)>w.revision())return false;
    if(code==F04_OK) {
     if(val(w,result,F05_OUTCOME)!=uint32_t(ActionOutcome::accepted) || val(w,result,F05_REJECTION) ||
      val(w,result,F05_ROLL)<1 || val(w,result,F05_ROLL)>100 || val(w,result,F05_CONSUMED)!=1 || val(w,result,F05_STREAM)!=0xF0401 ||
      val(w,result,F05_BEFORE)!=val(w,result,F05_AFTER))return false;
    } else if(val(w,result,F05_OUTCOME)!=uint32_t(ActionOutcome::rejected))return false;
   } else {
    if(code==F04_OK)return false;
    for(Field f:{F05_OUTCOME,F05_REJECTION,F05_BEFORE,F05_AFTER,F05_ROLL,F05_CONSUMED,F05_STREAM})if(val(w,result,f))return false;
   }
  }
  U previous=0,previous_state=0,last_tick=val(w,r,TICK);
  for(U e:all(w,"f05_event"))if(ref(w,e,F05_ORDER_REF)==o) {
   const U es=val(w,e,F05_STATUS),tick=val(w,e,TICK);
   if(!events.insert(e).second || ref(w,e,F05_PREVIOUS_REF)!=previous || !f05_step(previous_state,es) ||
    ref(w,e,F05_REQUEST_REF)!=r || tick<last_tick || tick>c.time.now() || val(w,e,CODE)>F05_TRANSITION)return false;
   if((es==F05_ISSUED || es==F05_ACCEPTED || es==F05_EXECUTING || es==F05_COMPLETED || es==F05_CANCELLED) && val(w,e,CODE)!=F04_OK)return false;
   if((es==F05_FAILED || es==F05_REFUSED) && !val(w,e,CODE))return false;
   if(es==F05_ISSUED && ref(w,e,PERSON)!=ref(w,o,ISSUER))return false;
   if((es==F05_ACCEPTED || es==F05_EXECUTING || es==F05_COMPLETED || es==F05_FAILED) && ref(w,e,PERSON)!=ref(w,o,PERSON))return false;
   if((es==F05_ACCEPTED || es==F05_EXECUTING || es==F05_COMPLETED || es==F05_FAILED) && ref(w,e,F05_TASK_REF)!=task)return false;
   if(ref(w,e,F05_TASK_REF) && ref(w,e,F05_TASK_REF)!=task)return false;
   if(ref(w,e,F05_RESULT_REF) && ref(w,e,F05_RESULT_REF)!=result)return false;
   if(ref(w,e,F05_ATTEMPT_REF) && (!result || ref(w,e,F05_ATTEMPT_REF)!=ref(w,result,F05_ATTEMPT_REF)))return false;
   if((es==F05_COMPLETED || es==F05_FAILED) && (!ref(w,e,F05_RESULT_REF) || !ref(w,e,F05_ATTEMPT_REF)))return false;
   previous=e;previous_state=es;last_tick=tick;
  }
  if(!previous || ref(w,o,F05_PREVIOUS_REF)!=previous || previous_state!=state || val(w,previous,CODE)!=val(w,o,CODE))return false;
 }
 return requests.size()==all(w,"f05_request").size() && tasks.size()==all(w,"f05_task").size() &&
  attempts.size()==all(w,"f05_attempt").size() && results.size()==all(w,"f05_result").size() && events.size()==all(w,"f05_event").size();
}
