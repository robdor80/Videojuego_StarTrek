// Durable minimal request/accepted intent and causal P03 reference. No prompts,
// raw responses, model prose, remote identifiers, models, URLs or credentials.
bool f05_ai_shape(const WorldState& w,U id,std::set<U>& a,std::set<U>& q,std::set<U>& ar,std::set<U>& rr) {
 if(!type(w,id,"f05_ai_request"))return false;
 a={F05_KEY,F05_REVISION,F05_INPUT,END,TICK,F05_BEFORE,F05_AFTER,F05_STATUS,F05_AI_ROUTE,F05_AI_ERROR,F05_AI_INTENT};q=a;
 ar={SHIP,PERSON,F05_NEED_REF,F05_AI_DECISION_REF};rr={SHIP,PERSON};return true;
}
bool f05_ai_schema(const Campaign& c) {
 const auto& w=c.world;const auto requests=all(w,"f05_ai_request");if(requests.size()>512)return false;
 std::set<U> keys,decisions;
 for(U r:requests) {
  const U status=val(w,r,F05_STATUS),n=ref(w,r,F05_NEED_REF),d=ref(w,r,F05_AI_DECISION_REF),actor=ref(w,r,PERSON);
  if(!val(w,r,F05_KEY) || !keys.insert(val(w,r,F05_KEY)).second || !val(w,r,F05_INPUT) ||
   val(w,r,F05_REVISION)>=val(w,r,F05_BEFORE) || val(w,r,F05_BEFORE)>w.revision() ||
   val(w,r,F05_AFTER)<val(w,r,F05_BEFORE) || val(w,r,F05_AFTER)>w.revision() ||
   val(w,r,TICK)>c.time.now() || val(w,r,END)<=val(w,r,TICK) || val(w,r,END)-val(w,r,TICK)>300 ||
   val(w,r,F05_AI_ROUTE)<F05_AI_DETERMINISTIC || val(w,r,F05_AI_ROUTE)>F05_AI_REASONING ||
   status>F05_AI_APPROVAL || val(w,r,F05_AI_ERROR)>F05_AI_RECOVERED || val(w,r,F05_AI_INTENT)>F05_AI_UNKNOWN ||
   val(w,actor,CATEGORY)!=1 || all(w,"f05_player").empty())return false;
  if(n) {
   if(!type(w,n,"f05_scan_need") || n!=val(w,r,F05_INPUT))return false;
   bool briefed=false;for(U b:all(w,"f05_brief"))if(ref(w,b,PERSON)==actor && ref(w,b,F05_NEED_REF)==n && val(w,b,F05_REVISION)<val(w,r,F05_REVISION))briefed=true;
   if(!briefed)return false;
  }
  const U intent=val(w,r,F05_AI_INTENT);
  if(status==F05_AI_PENDING && (intent || val(w,r,F05_AI_ERROR) || d || val(w,r,F05_BEFORE)!=val(w,r,F05_AFTER)))return false;
  if((status==F05_AI_VALID || status==F05_AI_APPLIED || status==F05_AI_APPROVAL) && (!n || (intent!=F05_AI_SCAN && intent!=F05_AI_ADVISE) || val(w,r,F05_AI_ERROR)))return false;
  if(status==F05_AI_CLARIFICATION && intent!=F05_AI_ASK)return false;
  if(status==F05_AI_INSUFFICIENT && intent!=F05_AI_UNKNOWN)return false;
  if(status!=F05_AI_PENDING && val(w,r,F05_AFTER)<=val(w,r,F05_BEFORE))return false;
  if((status==F05_AI_VALID || status==F05_AI_APPLIED || status==F05_AI_APPROVAL || status==F05_AI_CLARIFICATION || status==F05_AI_INSUFFICIENT) && val(w,r,F05_AI_ERROR))return false;
  if(status==F05_AI_FALLBACK && (val(w,r,F05_AI_ERROR)<F05_AI_NOT_CONFIGURED || val(w,r,F05_AI_ERROR)>F05_AI_EMPTY || intent))return false;
  if(status==F05_AI_REJECTED && (val(w,r,F05_AI_ERROR)<F05_AI_MALFORMED || val(w,r,F05_AI_ERROR)>F05_AI_RESTRICTION || intent))return false;
  if(status==F05_AI_STALE && ((val(w,r,F05_AI_ERROR)!=F05_AI_BINDING && val(w,r,F05_AI_ERROR)!=F05_AI_RECOVERED) || intent))return false;
  if((status==F05_AI_APPLIED)!=bool(d))return false;
  if(d && (!type(w,d,"f05_decision") || !decisions.insert(d).second || ref(w,d,PERSON)!=actor ||
   val(w,d,F05_KEY)!=val(w,r,F05_KEY) || val(w,d,F05_INPUT)!=val(w,r,F05_INPUT) ||
   val(w,d,F05_REVISION)!=val(w,r,F05_AFTER) || val(w,d,TICK)<val(w,r,TICK) || intent!=F05_AI_SCAN || val(w,d,TICK)>=val(w,r,END)))return false;
 }
 return true;
}
