// Compiled ONLY into TrekF11TrialHost, never the product bridge.
// The task authorizes this native trial issuer and two explicit commissions.
// There is no JSON, actor ID, verified flag, AI text or client-supplied evidence
// input. This is a trusted scenario bootstrap, not an academic gameplay result.
#include <random>
namespace {
void f11_trial_identity(Campaign& c,U p) {
 std::random_device source;
 auto bits32=[&](){return U(std::uniform_int_distribution<uint32_t>{}(source));};
 F11CharacterId identity{};
 for(U attempt=0;attempt<8;++attempt) {
  identity={(bits32()<<16)|(bits32()&65535),(bits32()<<16)|(bits32()&65535),uint32_t(bits32()),0};
  if(!f11_valid_identity(identity))continue;
  bool collision=false;for(U person:all(c.world,"person"))collision|=f11_equal(f11_identity(c.world,person),identity);
  if(!collision)break;
  identity={};
 }
 need(f11_valid_identity(identity),F04_INTERNAL);
 set(c,p,F11_VERSION,1);set(c,p,F11_ID_HIGH,identity.high48);set(c,p,F11_ID_MID,identity.mid48);
 set(c,p,F11_ID_LOW,identity.low32);set(c,p,F11_SERVICE,1);
}
U f11_trial_fact(Campaign& c,const ContentCatalog& cat,const char* kind,U root,U person=0) {
 const U id=make(c,cat,kind);set(c,id,F11_VERSION,1);link(c,id,SHIP,1);link(c,id,F11_ROOT_REF,root);
 if(person){link(c,id,PERSON,person);const auto identity=f11_identity(c.world,person);
  set(c,id,F11_ID_HIGH,identity.high48);set(c,id,F11_ID_MID,identity.mid48);set(c,id,F11_ID_LOW,identity.low32);}
 return id;
}
void f11_bootstrap_authorized_trial(Campaign& c,const ContentCatalog& cat) {
 need(all(c.world,"f11_root").empty());
 const U root=f11_trial_fact(c,cat,"f11_root",0);set(c,root,TICK,c.time.now());set(c,root,CAUSE,110501);
 const U office=f11_trial_fact(c,cat,"f11_office",root);
 const U grant=f11_trial_fact(c,cat,"f11_grant",root);link(c,grant,F11_AUTHORITY_REF,office);
 temporal(c,grant,c.time.now(),100);set(c,grant,D_DOMAIN,1);set(c,grant,F11_FROM,1101);set(c,grant,F11_TO,1102);set(c,grant,F11_REVOKED_AT,0);
 for(U p:{5,8}) {
  // Deliberate separate authorized trial commissions for these people only.
  // Other legacy ranks (including captain/admiral) stay exactly as initialized.
  f11_trial_identity(c,p);
  const U graduation=f11_trial_fact(c,cat,"f11_graduation",root,p);set(c,graduation,TICK,c.time.now());
  const U authorization=f11_trial_fact(c,cat,"f11_commission_order",root,p);
  link(c,authorization,F11_AUTHORITY_REF,office);link(c,authorization,F11_GRADUATION_REF,graduation);set(c,authorization,TICK,c.time.now());
  const U commission=f11_trial_fact(c,cat,"f11_commission",root,p);
  link(c,commission,F11_GRADUATION_REF,graduation);link(c,commission,F11_COMMISSION_ORDER_REF,authorization);
  set(c,commission,TICK,c.time.now());set(c,commission,F11_TO,1101);
  link(c,p,F11_COMMISSION_REF,commission);link(c,p,F11_RANK_EVENT_REF,commission);set(c,p,RANK,1101);
  const U evaluation=f11_trial_fact(c,cat,"f11_evaluation",root,p);
  temporal(c,evaluation,c.time.now(),100);link(c,evaluation,F11_AUTHORITY_REF,office);
  link(c,evaluation,F11_COMMISSION_REF,commission);link(c,evaluation,F11_RANK_EVENT_REF,commission);
  const U cause=f11_trial_fact(c,cat,"f11_cause",root,p);set(c,cause,TICK,c.time.now());set(c,cause,CAUSE,110502);
  const U order=f11_trial_fact(c,cat,"f11_personnel_order",root,p);temporal(c,order,c.time.now(),100);
  set(c,order,F11_REVOKED_AT,0);set(c,order,F11_FROM,1101);set(c,order,F11_TO,1102);
  for(auto [r,value]:std::initializer_list<std::pair<Ref,U>>{{F11_AUTHORITY_REF,office},{F11_GRANT_REF,grant},
    {F11_COMMISSION_REF,commission},{F11_RANK_EVENT_REF,commission},{F11_EVALUATION_REF,evaluation},{F11_CAUSE_REF,cause}})link(c,order,r,value);
 }
}
}
extern "C" F04_API uint32_t f11_test_create(F04Session** out) {
 if(!out)return F04_ARGUMENT;*out=nullptr;
 try {
  auto s=std::make_unique<F04Session>("miranda");
  auto next=std::make_unique<Campaign>(*s->c);
  f11_bootstrap_authorized_trial(*next,*s->content.catalog());need(schema(*next),F04_INTERNAL);
  s->c.swap(next);*out=s.release();return F04_OK;
 }catch(const Denial& e){return e.code;}catch(...){return F04_INTERNAL;}
}
extern "C" F04_API uint32_t f11_test_fault(F04Session* s,U stage) {
 return call(s,[&]()->uint32_t{need(stage<=5);f11_fault=stage;return F04_OK;});
}
extern "C" F04_API uint32_t f11_test_revoke(F04Session* s,U id) {
 return call(s,[&]()->uint32_t {
  need(type(s->c->world,id,"f11_grant") || type(s->c->world,id,"f11_personnel_order"));
  auto next=std::make_unique<Campaign>(*s->c);set(*next,id,STATE,CANCELLED);set(*next,id,F11_REVOKED_AT,next->time.now());
  need(schema(*next),F04_INTERNAL);s->c.swap(next);return F04_OK;
 });
}
