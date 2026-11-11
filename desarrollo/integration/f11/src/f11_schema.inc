// Trek vocabulary only. Core owns identity, relations, clock and persistence.
F11CharacterId f11_identity(const WorldState& w,U person) {
 return {val(w,person,F11_ID_HIGH),val(w,person,F11_ID_MID),uint32_t(val(w,person,F11_ID_LOW)),0};
}
bool f11_equal(F11CharacterId a,F11CharacterId b) {
 return a.high48==b.high48 && a.mid48==b.mid48 && a.low32==b.low32 && !a.reserved && !b.reserved;
}
bool f11_valid_identity(F11CharacterId id) {
 return id.high48<=FOREVER && id.mid48<=FOREVER && !id.reserved && (id.high48 || id.mid48 || id.low32);
}
bool f11_shape(const WorldState& w,U id,std::set<U>& allowed,std::set<U>& required,std::set<U>& ar,std::set<U>& rr) {
 allowed={F11_VERSION};ar={SHIP,F11_ROOT_REF};bool person=false;
 if(type(w,id,"f11_root")) {allowed.insert({TICK,CAUSE});ar={SHIP};}
 else if(type(w,id,"f11_office")) {}
 else if(type(w,id,"f11_grant")) {allowed.insert({START,END,STATE,D_DOMAIN,F11_FROM,F11_TO,F11_REVOKED_AT});ar.insert(F11_AUTHORITY_REF);}
 else if(type(w,id,"f11_graduation")) {allowed.insert(TICK);person=true;}
 else if(type(w,id,"f11_commission_order")) {allowed.insert(TICK);ar.insert({F11_GRADUATION_REF,F11_AUTHORITY_REF});person=true;}
 else if(type(w,id,"f11_commission")) {allowed.insert({TICK,F11_TO});ar.insert({F11_GRADUATION_REF,F11_COMMISSION_ORDER_REF});person=true;}
 else if(type(w,id,"f11_evaluation")) {allowed.insert({START,END,STATE});ar.insert({F11_COMMISSION_REF,F11_RANK_EVENT_REF,F11_AUTHORITY_REF});person=true;}
 else if(type(w,id,"f11_cause")) {allowed.insert({TICK,CAUSE});person=true;}
 else if(type(w,id,"f11_personnel_order")) {
  allowed.insert({START,END,STATE,F11_FROM,F11_TO,F11_REVOKED_AT});
  ar.insert({F11_COMMISSION_REF,F11_RANK_EVENT_REF,F11_EVALUATION_REF,F11_GRANT_REF,F11_CAUSE_REF,F11_AUTHORITY_REF});person=true;
 }
 else if(type(w,id,"promotion")) {
  allowed.insert({TICK,F11_FROM,F11_TO,F11_KEY,F11_INPUT_REVISION,F11_COMMIT_REVISION,F11_VISIBILITY,DEPT});
  ar.insert({F11_COMMISSION_REF,F11_RANK_EVENT_REF,F11_EVALUATION_REF,F11_GRANT_REF,F11_ORDER_REF,F11_CAUSE_REF,F11_AUTHORITY_REF});person=true;
 }
 else return false;
 if(person){allowed.insert({F11_ID_HIGH,F11_ID_MID,F11_ID_LOW});ar.insert(PERSON);}
 required=allowed;rr=ar;
 if(type(w,id,"promotion"))ar.insert(SLOT); // Unassigned officer is legal.
 return true;
}
bool f11_history_live_at(const WorldState& w,U record,U tick) {
 // Historical validation only: a commit can precede revocation within one
 // campaign tick. New executions use window(), which requires ACTIVE now;
 // CANCELLED never grants new authority, even when tick == REVOKED_AT.
 return val(w,record,START)<=tick && tick<val(w,record,END) &&
  (val(w,record,STATE)==ACTIVE || (val(w,record,STATE)==CANCELLED && tick<=val(w,record,F11_REVOKED_AT)));
}
bool f11_schema(const Campaign& c) {
 const auto& w=c.world;const auto roots=all(w,"f11_root");
 if(roots.size()>1)return false;
 const U root=roots.empty()?0:roots.front();
 // This identifies the compiled native trial issuer, not a client-verification
 // flag. As in F04, archives must come from trusted Host storage, not players.
 if(root && (val(w,root,F11_VERSION)!=1 || val(w,root,CAUSE)!=110501 || val(w,root,TICK)>c.time.now()))return false;
 std::set<std::array<U,3>> identities;std::set<U> keys,used_orders;
 std::map<U,U> commissions,promotions,graduations,commission_orders;
 const auto offices=all(w,"f11_office");
 if((root && offices.size()!=1) || (!root && !offices.empty()))return false;
 for(auto entity:projected_ids(w)) {
  const U id=entity.value();const auto* definition=w.definition_of(entity);
  const std::string name=definition?std::string(definition->value()):"";
  const bool fact=name.starts_with("trek.f04:f11_") || type(w,id,"promotion");
  if(type(w,id,"person")) {
   if(!has(w,id,F11_VERSION))continue;
   const auto identity=f11_identity(w,id);
   if(!root || val(w,id,F11_VERSION)!=1 || !f11_valid_identity(identity) || val(w,id,F11_ID_LOW)>UINT32_MAX ||
    !identities.insert({identity.high48,identity.mid48,identity.low32}).second || val(w,id,F11_SERVICE)!=1 || val(w,id,CATEGORY)!=1 ||
    !type(w,ref(w,id,F11_COMMISSION_REF),"f11_commission"))return false;
   const U rank_event=ref(w,id,F11_RANK_EVENT_REF);
   if((!type(w,rank_event,"f11_commission") && !type(w,rank_event,"promotion")) ||
     ref(w,rank_event,PERSON)!=id || val(w,id,RANK)!=val(w,rank_event,F11_TO))return false;
   continue;
  }
  if(!fact)continue;
  if(!root || val(w,id,F11_VERSION)!=1 || (id!=root && ref(w,id,F11_ROOT_REF)!=root))return false;
  if(has(w,id,TICK) && val(w,id,TICK)>c.time.now())return false;
  if(has(w,id,F11_REVOKED_AT) && (val(w,id,STATE)>CANCELLED ||
    (val(w,id,STATE)==ACTIVE && val(w,id,F11_REVOKED_AT)) ||
    (val(w,id,STATE)==CANCELLED && val(w,id,F11_REVOKED_AT)>c.time.now())))return false;
  const U p=ref(w,id,PERSON);
  if(p && (!has(w,p,F11_VERSION) || !f11_equal(f11_identity(w,id),f11_identity(w,p)) || val(w,id,F11_ID_LOW)>UINT32_MAX))return false;
  const U authority=ref(w,id,F11_AUTHORITY_REF);
  if(authority && (offices.empty() || authority!=offices.front()))return false;
  if(type(w,id,"f11_grant")) {
   if(val(w,id,D_DOMAIN)!=1 || val(w,id,F11_FROM)!=1101 || val(w,id,F11_TO)!=1102)return false;
  }
  if(type(w,id,"f11_graduation")) {if(!graduations.emplace(p,id).second)return false;}
  if(type(w,id,"f11_commission_order")) {
   if(!commission_orders.emplace(p,id).second)return false;
   const U grad=ref(w,id,F11_GRADUATION_REF);
   if(!type(w,grad,"f11_graduation") || ref(w,grad,PERSON)!=p || val(w,grad,TICK)>val(w,id,TICK))return false;
  }
  if(type(w,id,"f11_commission")) {
   if(!commissions.emplace(p,id).second || ref(w,p,F11_COMMISSION_REF)!=id || val(w,id,F11_TO)!=1101)return false;
   const U grad=ref(w,id,F11_GRADUATION_REF),order=ref(w,id,F11_COMMISSION_ORDER_REF);
   if(!type(w,grad,"f11_graduation") || !type(w,order,"f11_commission_order") || ref(w,grad,PERSON)!=p ||
    ref(w,order,PERSON)!=p || ref(w,order,F11_GRADUATION_REF)!=grad || val(w,order,TICK)>val(w,id,TICK))return false;
  }
  if(type(w,id,"f11_evaluation") || type(w,id,"f11_personnel_order") || type(w,id,"promotion")) {
   const U commission=ref(w,id,F11_COMMISSION_REF),previous=ref(w,id,F11_RANK_EVENT_REF);
   if(commission!=ref(w,p,F11_COMMISSION_REF) || previous!=commission || !type(w,commission,"f11_commission") || ref(w,commission,PERSON)!=p)return false;
   const U tick=type(w,id,"promotion")?val(w,id,TICK):val(w,id,START);
   if(val(w,commission,TICK)>tick)return false;
  }
  if(type(w,id,"f11_personnel_order") || type(w,id,"promotion")) {
   const U evaluation=ref(w,id,F11_EVALUATION_REF),grant=ref(w,id,F11_GRANT_REF),cause=ref(w,id,F11_CAUSE_REF);
   if(!type(w,evaluation,"f11_evaluation") || ref(w,evaluation,PERSON)!=p ||
    ref(w,evaluation,F11_RANK_EVENT_REF)!=ref(w,id,F11_RANK_EVENT_REF) ||
    !type(w,grant,"f11_grant") || ref(w,grant,F11_AUTHORITY_REF)!=authority ||
    !type(w,cause,"f11_cause") || ref(w,cause,PERSON)!=p || !val(w,cause,CAUSE) ||
    val(w,id,F11_FROM)!=1101 || val(w,id,F11_TO)!=1102)return false;
  }
  if(type(w,id,"promotion")) {
   const U order=ref(w,id,F11_ORDER_REF),tick=val(w,id,TICK),grant=ref(w,id,F11_GRANT_REF),evaluation=ref(w,id,F11_EVALUATION_REF);
   if(!promotions.emplace(p,id).second || !used_orders.insert(order).second || !val(w,id,F11_KEY) || !keys.insert(val(w,id,F11_KEY)).second ||
    !type(w,order,"f11_personnel_order") || ref(w,order,PERSON)!=p || ref(w,p,F11_RANK_EVENT_REF)!=id ||
    val(w,id,F11_VISIBILITY)!=F11_SUBJECT_AND_PERSONNEL || val(w,id,F11_INPUT_REVISION)>=val(w,id,F11_COMMIT_REVISION) ||
    val(w,id,F11_COMMIT_REVISION)>w.revision() ||
    !f11_history_live_at(w,order,tick) || !f11_history_live_at(w,grant,tick) || !f11_history_live_at(w,evaluation,tick) ||
    val(w,ref(w,id,F11_CAUSE_REF),TICK)>tick)return false;
   for(Ref r:{F11_COMMISSION_REF,F11_RANK_EVENT_REF,F11_EVALUATION_REF,F11_GRANT_REF,F11_CAUSE_REF,F11_AUTHORITY_REF})
    if(ref(w,order,r)!=ref(w,id,r))return false;
   if(val(w,id,DEPT)<1 || val(w,id,DEPT)>7)return false;
  }
 }
 if(graduations.size()!=identities.size() || commissions.size()!=identities.size() || commission_orders.size()!=identities.size())return false;
 for(U p:all(w,"person"))if(has(w,p,F11_VERSION)) {
  if(!commissions.contains(p))return false;
  const U rank=ref(w,p,F11_RANK_EVENT_REF);
  if(rank!=commissions[p] && (!promotions.contains(p) || promotions[p]!=rank))return false;
 }
 return true;
}
