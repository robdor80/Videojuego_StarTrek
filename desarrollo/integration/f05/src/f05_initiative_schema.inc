// Append-only P03 vocabulary. Obligations, communications and decisions live in
// Core, not an NPC mirror. P01 owns order/task/attempt/result event chains.
bool f05_initiative_shape(const WorldState& w,U id,std::set<U>& a,std::set<U>& q,std::set<U>& ar,std::set<U>& rr) {
 if(type(w,id,"f05_player")) {a={F05_REVISION,TICK};ar={SHIP,PERSON};q=a;rr=ar;}
 else if(type(w,id,"f05_scan_need")) {
  a={F05_KEY,F05_REVISION,START,END,CAUSE,TICK};q=a;
  ar={SHIP,ISSUER,ORIGIN,ACTIVITY,SLOT,PERSON};rr=ar;
 } else if(type(w,id,"f05_brief")) {
  a={F05_KEY,F05_REVISION,CAUSE,TICK};q=a;ar={SHIP,ISSUER,PERSON,F05_NEED_REF};rr=ar;
 } else if(type(w,id,"f05_detection")) {
  a={F05_REVISION,TICK};q=a;ar={SHIP,PERSON,F05_NEED_REF};rr=ar;
 } else if(type(w,id,"f05_decision")) {
  a={F05_KEY,F05_REVISION,F05_INPUT,F05_BUDGET,F05_EXAMINED,F05_STATUS,CODE,TICK};q=a;
  ar={SHIP,PERSON,F05_NEED_REF,F05_DETECTION_REF,F05_ORDER_REF,TARGET};rr={SHIP,PERSON};
 } else return false;
 return true;
}
std::vector<FactKey> f05_need_facts(const WorldState& w,U n) {
 std::vector<FactKey> facts{{EntityId{n}},{EntityId{n},FactKind::definition}};
 for(auto r:w.relations_from(EntityId{n}))if(r.kind.value()==SLOT || r.kind.value()==PERSON || r.kind.value()==ACTIVITY ||
  (r.kind.value()>>48)==0xF000+START || (r.kind.value()>>48)==0xF000+END)
  facts.push_back({EntityId{n},FactKind::relation,r.kind,r.target});
 return facts;
}
bool f05_initiative_schema(const Campaign& c) {
 const auto& w=c.world;const auto players=all(w,"f05_player"),needs=all(w,"f05_scan_need"),briefs=all(w,"f05_brief"),decisions=all(w,"f05_decision");
 if(players.size()>1 || needs.size()>128 || briefs.size()>512 || decisions.size()>2048)return false;
 if(players.empty() && (!needs.empty() || !briefs.empty() || !decisions.empty()))return false;
 for(U p:players)if(val(w,p,TICK)>c.time.now() || val(w,p,F05_REVISION)>=w.revision() || val(w,ref(w,p,PERSON),CATEGORY)!=1)return false;
 std::set<U> keys,duties,detections,linked_orders;
 for(U n:needs) {
  const U a=ref(w,n,ACTIVITY),origin=ref(w,n,ORIGIN);
  if(!keys.insert(val(w,n,F05_KEY)).second || !val(w,n,F05_KEY) || !val(w,n,CAUSE) ||
   !duties.insert(a).second || !type(w,a,"activity") || val(w,a,VALUE)!=F04_DUTY ||
   ref(w,n,PERSON)!=ref(w,a,PERSON) || ref(w,n,SLOT)!=ref(w,a,SLOT) || val(w,ref(w,n,SLOT),QUAL)!=F04_SENSORS ||
   !type(w,origin,"appointment") || ref(w,origin,PERSON)!=ref(w,n,ISSUER) ||
   val(w,n,START)<val(w,a,START) || val(w,n,START)>=val(w,n,END) || val(w,n,TICK)>val(w,n,START) ||
   val(w,n,TICK)>c.time.now() || val(w,n,F05_REVISION)>=w.revision())return false;
  // One attempt per obligation, including orders emitted by different NPCs.
  U count=0;for(U o:all(w,"f05_order"))if(ref(w,ref(w,o,F05_REQUEST_REF),F05_NEED_REF)==n) {
   ++count;linked_orders.insert(o);const U r=ref(w,o,F05_REQUEST_REF);
   if(ref(w,r,PERSON)!=ref(w,n,PERSON) || ref(w,r,SLOT)!=ref(w,n,SLOT) || val(w,r,OP)!=F04_SCAN || val(w,r,CAUSE)!=n || val(w,r,END)>val(w,n,END))return false;
  }
  if(count>1)return false;
 }
 for(U o:all(w,"f05_order"))if(ref(w,ref(w,o,F05_REQUEST_REF),F05_NEED_REF) && !linked_orders.contains(o))return false;
 keys.clear();std::map<U,std::set<FactKey>> allowed;
 for(U b:briefs) {
  const U n=ref(w,b,F05_NEED_REF),p=ref(w,b,PERSON);
  if(!type(w,n,"f05_scan_need") || !keys.insert(val(w,b,F05_KEY)).second || !val(w,b,F05_KEY) || !val(w,b,CAUSE) ||
   val(w,b,TICK)<val(w,n,TICK) || val(w,b,TICK)>c.time.now() || val(w,b,F05_REVISION)>=w.revision())return false;
  for(auto f:f05_need_facts(w,n))allowed[p].insert(f);
  for(Ref r:{PERSON,SLOT,ACTIVITY})allowed[p].insert({EntityId{ref(w,n,r)}});
 }
 // A valid Core archive can still be invalid Trek knowledge. No arbitrary secret
 // memories can be injected on load, even if their subject exists in WorldState.
 for(U p:all(w,"person")) {
  const auto known=w.knowledge_of(EntityId{p});if(known.size()>4096)return false;
  for(const auto& k:known) {
   if(!allowed[p].contains(k.fact.key) || !k.fact.present)return false;
   if(k.fact.key.kind==FactKind::definition && k.fact.definition_id()!="trek.f04:f05_scan_need")return false;
  }
 }
 for(auto id:projected_ids(w))if(!type(w,id.value(),"person") && !w.knowledge_of(id).empty())return false;
 keys.clear();
 for(U d:decisions) {
  const U n=ref(w,d,F05_NEED_REF),detection=ref(w,d,F05_DETECTION_REF),o=ref(w,d,F05_ORDER_REF),kind=val(w,d,F05_STATUS),tick=val(w,d,TICK);
  if(!val(w,d,F05_KEY) || !keys.insert(val(w,d,F05_KEY)).second || kind<F05_NO_ACTION || kind>F05_WAIT_PLAYER ||
   !val(w,d,F05_BUDGET) || val(w,d,F05_BUDGET)>32 || val(w,d,F05_EXAMINED)>val(w,d,F05_BUDGET) ||
   val(w,d,CODE)>F05_TRANSITION || tick>c.time.now() || val(w,d,F05_REVISION)>=w.revision() ||
   (n && (!type(w,n,"f05_scan_need") || n!=val(w,d,F05_INPUT))))return false;
  if(detection) {
   if(!n || !type(w,detection,"f05_detection") || !detections.insert(detection).second ||
    ref(w,detection,F05_NEED_REF)!=n || ref(w,detection,PERSON)!=ref(w,d,PERSON) ||
    val(w,detection,TICK)!=tick || val(w,detection,F05_REVISION)!=val(w,d,F05_REVISION) || tick<val(w,n,START))return false;
  }
  if(n) {
   bool briefed=false;for(U b:briefs)if(ref(w,b,F05_NEED_REF)==n && ref(w,b,PERSON)==ref(w,d,PERSON) &&
    val(w,b,TICK)<=tick && val(w,b,F05_REVISION)<val(w,d,F05_REVISION))briefed=true;
   if(!briefed)return false;
  }
  if(o && (!linked_orders.contains(o) || ref(w,ref(w,o,F05_REQUEST_REF),F05_NEED_REF)!=n))return false;
  if((kind==F05_ISSUE_ORDER || kind==F05_CONTINUE_TASK) && (!o || !detection))return false;
  if((kind==F05_ISSUE_ORDER || kind==F05_CONTINUE_TASK) && ref(w,d,PERSON)==ref(w,players[0],PERSON))return false;
  if(kind==F05_ISSUE_ORDER && (ref(w,d,PERSON)!=ref(w,o,ISSUER) || val(w,d,CODE)!=F04_OK))return false;
  if(kind==F05_CONTINUE_TASK && (ref(w,d,PERSON)!=ref(w,o,PERSON) || val(w,d,CODE)!=F04_OK))return false;
  if(ref(w,d,TARGET) && !type(w,ref(w,d,TARGET),"person"))return false;
 }
 for(U o:linked_orders) {
  const U r=ref(w,o,F05_REQUEST_REF);bool creation=false;
  for(U d:decisions)if(ref(w,d,F05_ORDER_REF)==o && ref(w,d,PERSON)==ref(w,o,ISSUER) &&
   val(w,d,F05_KEY)==val(w,r,F05_KEY) && val(w,d,F05_REVISION)==val(w,r,F05_REVISION) &&
   (val(w,d,F05_STATUS)==F05_ISSUE_ORDER || val(w,d,F05_STATUS)==F05_PROPOSE || val(w,d,F05_STATUS)==F05_ESCALATE))creation=true;
  if(!creation)return false;
 }
 return detections.size()==all(w,"f05_detection").size();
}
