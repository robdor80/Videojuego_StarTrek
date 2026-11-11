#include "f11_promotions.h"
#include "../../f05/tests/f05_test_support.h"
#include <cstddef>
#include <chrono>
#include <type_traits>
extern "C" {
uint32_t f11_test_create(F04Session**);
uint32_t f11_test_fault(F04Session*,U);
uint32_t f11_test_revoke(F04Session*,U);
}
constexpr U VERSION=256,HIGH=257,MID=258,LOW=259,SERVICE=260,KEY=261,INPUT=262,COMMIT=263,FROM=264,TO=265,VISIBILITY=266;
constexpr U ROOT=256,AUTHORITY=257,GRANT=258,GRADUATION=259,COMMISSION_ORDER=260,COMMISSION=261,RANK_EVENT=262,EVALUATION=263,ORDER=264,CAUSE_REF=265;
U reference(const CampaignArchiveSnapshot& d,U id,U kind) {
 for(auto r:d.campaign.relations)if(r.source.value()==id && r.kind.value()==kind)return r.target.value();return 0;
}
std::vector<U> facts(const CampaignArchiveSnapshot& d,const std::string& kind) {
 std::vector<U> result;for(auto def:d.campaign.definitions)if(def.definition_id=="trek.f04:"+kind)result.push_back(def.entity.value());return result;
}
void change_ref(CampaignArchiveSnapshot& d,U id,U kind,U target) {
 for(auto& r:d.campaign.relations)if(r.source.value()==id && r.kind.value()==kind){r.target=EntityId{target};return;}
 throw std::runtime_error("missing reference");
}
bool same_identity(F11CharacterId a,F11CharacterId b) {return a.high48==b.high48 && a.mid48==b.mid48 && a.low32==b.low32 && a.reserved==b.reserved;}
struct Career:Lab {
 Career(){eq(f04_destroy(s),F04_OK,"destroy initial");s=nullptr;eq(f11_test_create(&s),F04_OK,"private native trial bootstrap");handles();}
 F11PersonnelView officer(U p=5){F11PersonnelView v{};eq(f11_personnel(s,person(p),&v),F04_OK,"personnel");return v;}
 F11PromotionRequest promotion_request(U p=5,U key=11){
  const auto v=officer(p);const auto d=decode(save());U order=0;
  for(U id:facts(d,"f11_personnel_order"))if(reference(d,id,2)==p)order=id;
  return {person(p),v.character,stats().revision,key,reference(d,order,GRANT),order,reference(d,order,EVALUATION),
   v.commission,v.rank_event,stats().now,reference(d,order,CAUSE_REF),1101,1102};
 }
 F11PromotionReceipt promote(const F11PromotionRequest& q,uint32_t expected=F04_OK) {
  const auto before=save();F11PromotionReceipt r{};eq(f11_commit_promotion(s,&q,&r),expected,"commit promotion");
  if(expected!=F04_OK){check(before==save(),"denial must preserve every Core byte, RNG/revision included");check(r.status==expected && !r.promotion_event_id,"denial receipt");}
  return r;
 }
 F11PromotionView event(U id,U person_id=5){F11PromotionView v{};eq(f11_promotion(s,person(person_id),id,&v),F04_OK,"promotion query");return v;}
};
void unchanged_except_promotion(const CampaignArchiveSnapshot& a,const CampaignArchiveSnapshot& b,U person,U event) {
 check(b.campaign.last_entity_id==a.campaign.last_entity_id+1,"one authoritative record only");
 check(b.campaign.definitions.size()==a.campaign.definitions.size()+1,"one definition added");
 check(b.campaign.containment==a.campaign.containment,"same physical place");
 auto left=a.campaign.relations,right=b.campaign.relations;
 auto permitted=[&](const auto& r){return r.source.value()==event || (r.source.value()==person &&
  ((r.kind.value()>>48)==0xF000+7 || r.kind.value()==RANK_EVENT));};
 std::erase_if(left,permitted);std::erase_if(right,permitted);
 check(left==right,"all unrelated relations, duties, ship, billet, qualifications and orders preserved");
 // Compare complete Core snapshots after normalizing only the allowed changes.
 auto normalized=b;normalized.campaign=a.campaign;
 check(encode(normalized)==encode(a),"RNG and timeline unchanged");
}
void promotion() {
 Career c;c.ready();auto scan=c.accepted(333);auto q=c.promotion_request();const auto before=decode(c.save());
 const auto original=c.officer();const auto command=c.stats().commander;const auto r=c.promote(q);
 check(r.promotion_event_id && r.rank_event_id==r.promotion_event_id && r.from_rank==1101 && r.to_rank==1102,"receipt");
 auto after=c.officer();check(after.rank==1102 && after.rank_event==r.promotion_event_id,"Core grade and rank provenance");
 check(r.original_commit_revision==after.revision && r.current_revision==after.revision,"receipt exact commit revision");
 check(same_identity(original.character,after.character) && after.commission==original.commission && original.ship==after.ship &&
  original.billet==after.billet && original.department==after.department,"identity/destination unchanged");
 F04Person projected{};eq(f04_person(c.s,c.h.captain,5,&projected),F04_OK,"F04 projection");check(projected.rank==1102,"real F04 rank");
 const auto after_bytes=c.save();auto d=decode(after_bytes);check(facts(d,"promotion").size()==1,"one expediente promotion");
 unchanged_except_promotion(before,d,5,r.promotion_event_id);check(c.stats().commander==command,"no command from grade");
 auto view=c.event(r.promotion_event_id);check(view.grant==q.grant && view.person==5 && view.authority && view.origin && view.cause==q.cause &&
  view.previous_rank_event==q.rank_event && view.evaluation==q.evaluation && view.visibility==F11_SUBJECT_AND_PERSONNEL && view.receipt.effective_at==q.effective_tick,"narrative fact fields");
 auto op=F04Request{c.h.ensign,c.stats().revision,F04_BRIDGE,2,0,0,0,0,11};F04Result result{};
 eq(f04_execute(c.s,&op,&result),F04_DENIED,"no ship authority");
 c.execute(scan.order); // Existing unrelated F05 order remains executable.
}
void negatives() {
 Career c;const auto q=c.promotion_request();
 auto bad=q;bad.from_rank=0;c.promote(bad,F11_RANK);bad=q;bad.to_rank=1106;c.promote(bad,F11_RANK);
 bad=q;bad.from_rank=1102;bad.to_rank=1103;c.promote(bad,F11_RANK);
 bad=q;bad.expected_revision--;c.promote(bad,F04_STALE);
 bad=q;bad.effective_tick=1;c.promote(bad,F04_EXPIRED);
 c.advance(1);bad=q;bad.expected_revision=c.stats().revision;c.promote(bad,F04_EXPIRED);
 auto other=c.promotion_request(8,12);bad=c.promotion_request();bad.evaluation=other.evaluation;c.promote(bad,F11_EVALUATION);
 bad=c.promotion_request();bad.rank_event=other.rank_event;c.promote(bad,F11_RANK);
 bad=c.promotion_request();bad.commission=other.commission;c.promote(bad,F11_UNCOMMISSIONED);
 bad=c.promotion_request();bad.order=other.order;c.promote(bad,F11_ORDER);
 bad=c.promotion_request();bad.cause=other.cause;c.promote(bad,F11_ORDER);
 for(U p:{3,4,9,10,11}){bad=c.promotion_request();bad.subject=c.person(p);c.promote(bad,F11_UNCOMMISSIONED);}
 bad=c.promotion_request();bad.subject.scope++;c.promote(bad,F04_SCOPE);
 bad=c.promotion_request();bad.subject.id=9000;c.promote(bad,F04_SCOPE);
 bad=c.promotion_request();bad.key=0;c.promote(bad,F04_ARGUMENT);
 bad=c.promotion_request();bad.character.high48=U(1)<<48;c.promote(bad,F04_ARGUMENT);
 bad=c.promotion_request();bad.character.reserved=1;c.promote(bad,F04_ARGUMENT);
 c.advance(100);bad=c.promotion_request();c.promote(bad,F11_AUTHORITY);
}
void authority() {
 Career c;c.ready();const auto scan=c.accepted(222);auto q=c.promotion_request();
 for(U fake:{c.h.captain.id,c.h.admiral.id,scan.order,scan.request}){auto bad=q;bad.grant=fake;c.promote(bad,F11_AUTHORITY);}
 auto bad=q;bad.order=scan.order;c.promote(bad,F11_ORDER);
 eq(f11_test_revoke(c.s,q.order),F04_OK,"Host order revocation");q.expected_revision=c.stats().revision;c.promote(q,F11_ORDER);
 Career d;auto p=d.promotion_request();eq(f11_test_revoke(d.s,p.grant),F04_OK,"Host grant revocation");p.expected_revision=d.stats().revision;d.promote(p,F11_AUTHORITY);
}
void identity() {
 Career c;auto q=c.promotion_request(),other=c.promotion_request(8,12);
 check(!same_identity(q.character,other.character),"distinct permanent identity");
 auto bad=q;bad.character=other.character;c.promote(bad,F11_IDENTITY);
 c.promote(q);other.expected_revision=c.stats().revision;c.promote(other);check(facts(decode(c.save()),"promotion").size()==2,"two candidates distinct event ids");
 auto before=c.officer();const auto bytes=c.save();c.load(bytes);check(c.save()==bytes,"opt-in bit exact roundtrip");
 auto after=c.officer();check(same_identity(before.character,after.character) && before.rank_event==after.rank_event,"128 bits retained");
 Career d;auto other_world=d.officer();check(!same_identity(after.character,other_world.character),"identity not derived from ship/seed/entity/name");
}
void idempotency() {
 Career c;auto q=c.promotion_request();const auto original=c.promote(q);const auto bytes=c.save();
 auto replay=c.promote(q);check(bytes==c.save() && replay.original_commit_revision==original.original_commit_revision,"old revision replay");
 q.expected_revision=c.stats().revision;replay=c.promote(q);check(bytes==c.save(),"refreshed precondition same semantic payload");
 for(U i=0;i<11;++i){auto bad=q;switch(i){case 0:bad.character.low32^=1;break;case 1:bad.grant++;break;case 2:bad.order++;break;
  case 3:bad.evaluation++;break;case 4:bad.commission++;break;case 5:bad.rank_event++;break;case 6:bad.effective_tick++;break;
  case 7:bad.cause++;break;case 8:bad.to_rank=1106;break;case 9:bad.from_rank=0;break;case 10:bad.subject=c.person(8);break;}
  c.promote(bad,F11_IDEMPOTENCY_CONFLICT);}
 auto fresh=q;fresh.key++;c.promote(fresh,F11_RANK);
 eq(f11_test_revoke(c.s,q.grant),F04_OK,"revocation after committed promotion");
 const auto revoked=c.save();replay=c.promote(q);check(revoked==c.save() && replay.promotion_event_id==original.promotion_event_id,"replay returns historical fact, no new authority");
 c.load(revoked);c.promote(q,F04_SCOPE);q.subject=c.person(5);replay=c.promote(q);
 check(revoked==c.save() && replay.original_commit_revision==original.original_commit_revision,"load replay");
 F11PromotionView denied{};eq(f11_promotion(c.s,c.h.captain,original.promotion_event_id,&denied),F04_DENIED,"visibility no automatic captain access");
}
void atomic() {
 for(U stage=1;stage<=5;++stage){Career c;auto q=c.promotion_request();const auto before=c.save();
  eq(f11_test_fault(c.s,stage),F04_OK,"arm native fault");c.promote(q,F04_INTERNAL);check(c.save()==before,"no partial bytes");
  c.load(before);q.subject=c.person(5);auto r=c.promote(q);check(r.promotion_event_id && facts(decode(c.save()),"promotion").size()==1,"retry after injected failure");}
}
void corrupt() {
 Career c;auto q=c.promotion_request();const auto receipt=c.promote(q);const auto clean=c.save();
 auto reject=[&](CampaignArchiveSnapshot bad){auto bytes=encode(bad);eq(f04_load(c.s,bytes.data(),bytes.size()),F04_SAVE,"strict Trek rejects invalid Core archive");check(c.save()==clean,"failed load atomic");};
 for(auto [id,f,value]:std::initializer_list<std::tuple<U,U,U>>{
  {5,HIGH,q.character.high48^1},{5,LOW,U(1)<<32},{5,7,1101},{5,SERVICE,0},
  {receipt.promotion_event_id,TO,1106},{receipt.promotion_event_id,VISIBILITY,0},{receipt.promotion_event_id,COMMIT,0},
  {receipt.promotion_event_id,INPUT,c.stats().revision},{receipt.promotion_event_id,KEY,0}}){auto bad=decode(clean);change(bad,id,f,value);reject(bad);}
 auto bad=decode(clean);change_ref(bad,5,COMMISSION,receipt.promotion_event_id);reject(bad);
 bad=decode(clean);change_ref(bad,receipt.promotion_event_id,EVALUATION,q.commission);reject(bad);
 bad=decode(clean);change_ref(bad,receipt.promotion_event_id,RANK_EVENT,receipt.promotion_event_id);reject(bad);
 bad=decode(clean);change_ref(bad,q.evaluation,RANK_EVENT,receipt.promotion_event_id);reject(bad);
 bad=decode(clean);change_ref(bad,q.grant,AUTHORITY,3);reject(bad);
 bad=decode(clean);change_ref(bad,q.order,ROOT,3);reject(bad);
 bad=decode(clean);change(bad,reference(bad,q.grant,ROOT),VERSION,2);reject(bad);
 // Truncated/incomplete extension must fail, including orphaned grade changes.
 bad=decode(clean);std::erase_if(bad.campaign.relations,[&](auto r){return r.source.value()==5 && (r.kind.value()>>48)==0xF000+HIGH;});reject(bad);
 // Equal identity on two people is forbidden even if all their facts agree.
 bad=decode(clean);for(U id:facts(bad,"person"))if(id==8){change(bad,id,HIGH,q.character.high48);change(bad,id,MID,q.character.mid48);change(bad,id,LOW,q.character.low32);}
 reject(bad);
}
void legacy() {
 Lab legacy;const auto before=legacy.save();legacy.load(before);check(legacy.save()==before,"legacy exact no migration");
 F11PersonnelView v{};eq(f11_personnel(legacy.s,legacy.h.ensign,&v),F11_UNCOMMISSIONED,"legacy remains uncommissioned");
 Career source;auto q=source.promotion_request();q.subject=legacy.h.ensign;q.expected_revision=legacy.stats().revision;
 F11PromotionReceipt r{};eq(f11_commit_promotion(legacy.s,&q,&r),F11_UNCOMMISSIONED,"numeric legacy no implicit commission");check(before==legacy.save(),"legacy rejection unchanged");
 F04PopulationConfig config{123,404,4,0,0,4};F04Session* population=nullptr;
 eq(f04_create_population(1,"miranda",&config,&population),F04_OK,"rank zero world");F04Handles h{};eq(f04_handles(population,&h),F04_OK,"population handles");
 F04Person p{};eq(f04_person(population,{h.ship.scope,3},3,&p),F04_OK,"rank zero person");check(p.rank==0,"legacy zero");
 F04Stats stats{};eq(f04_stats(population,&stats),F04_OK,"stats");q.subject={h.ship.scope,3};q.expected_revision=stats.revision;
 eq(f11_commit_promotion(population,&q,&r),F11_UNCOMMISSIONED,"zero is not ensign");eq(f04_destroy(population),F04_OK,"destroy");
 // A native old schema fixture must remain byte exact under the new reader.
 for(auto name:{"schema1.hex","schema2.hex"}) {
  std::ifstream in(std::string(F11_LEGACY_FIXTURES)+"/"+name);check(bool(in),"legacy fixture");std::string hex;in>>hex;
  std::vector<uint8_t> bytes;for(size_t i=0;i<hex.size();i+=2)bytes.push_back(uint8_t(std::stoul(hex.substr(i,2),nullptr,16)));
  legacy.load(bytes);check(legacy.save()==bytes,"old archive exact");
 }
}
void history(const std::string& path) {
 const auto directory=path+"/run-"+std::to_string(std::chrono::steady_clock::now().time_since_epoch().count());
 Career c;c.ready();auto q=c.promotion_request();auto receipt=c.promote(q);const auto identity=c.officer().character;
 const std::array<uint8_t,16> uuid{11,5,2,1,1};std::filesystem::create_directories(path);
 eq(f04_history_migrate(c.s,directory.c_str(),uuid.data(),16),F04_OK,"history migrate");
 c.advance(8*86400);eq(f04_history_consolidate(c.s,86400,0),F04_OK,"consolidate expired records");
 F04HistoryStats stats{};eq(f04_history_stats(c.s,&stats),F04_OK,"history stats");check(stats.archived>0,"actually archived unrelated facts");
 eq(f04_history_publish(c.s,0),F04_OK,"publish generation");
 Career reopened;eq(f04_history_open(reopened.s,directory.c_str()),F04_OK,"recover generation");reopened.handles();
 q.subject=reopened.person(5);auto before=reopened.active();F11PromotionReceipt replay{};
 eq(f11_commit_promotion(reopened.s,&q,&replay),F04_OK,"expired order replay after segmented recovery");
 check(before==reopened.active() && replay.promotion_event_id==receipt.promotion_event_id && same_identity(identity,reopened.officer().character),"history identity and tombstone retained");
 auto fresh=q;fresh.key++;fresh.expected_revision=reopened.stats().revision;fresh.effective_tick=reopened.stats().now;
 eq(f11_commit_promotion(reopened.s,&fresh,&replay),F11_RANK,"no second promotion");
 check(before==reopened.active(),"history denial no partial effects");
 auto view=reopened.event(receipt.promotion_event_id);check(view.receipt.effective_at==0,"effective time unaffected by delayed presentation");
}
void abi() {
 static_assert(sizeof(F04Ref)==16 && sizeof(F04Person)==48 && sizeof(F04Request)==72);
 static_assert(F04_ASSIGN==1 && F04_SCAN==12 && F04_CIVIL_PRESENCE==34);
 static_assert(F04_CAPTAIN==1 && F04_DUTY_HEAD==9 && F04_INTERNAL==16);
 static_assert(sizeof(F11CharacterId)==24 && sizeof(F11PromotionRequest)==120);
 static_assert(std::is_standard_layout_v<F11PromotionRequest> && offsetof(F11PromotionRequest,expected_revision)==40);
 check(std::string(f04_core_sha())=="76a7b7b485616d8c4994f384a90f123bf333591d","exact Core pin");
}
void process_save(const std::string& path) {
 Career c;c.ready();auto q=c.promotion_request();write(path+"-before.f04",c.save());
 auto r=c.promote(q);write(path+"-after.f04",c.save());
 std::ofstream out(path+".txt");out<<q.order<<' '<<q.expected_revision<<' '<<q.key<<' '<<r.promotion_event_id<<' '<<r.original_commit_revision;
 check(bool(out),"persist expected immutable receipt");
}
void process_load(const std::string& path) {
 Career c;c.load(read(path+"-before.f04"));auto q=c.promotion_request();U expected_event=0,expected_revision=0;
 std::ifstream in(path+".txt");in>>q.order>>q.expected_revision>>q.key>>expected_event>>expected_revision;check(bool(in),"read receipt");
 auto identity=q.character;auto first=c.promote(q);check(first.promotion_event_id==expected_event && first.original_commit_revision==expected_revision,"same native fact after process reload");
 check(c.save()==read(path+"-after.f04"),"future bytes deterministic from saved identity");
 c.load(read(path+"-after.f04"));q.subject=c.person(5);auto bytes=c.save();auto replay=c.promote(q);
 check(c.save()==bytes && replay.promotion_event_id==expected_event && replay.original_commit_revision==expected_revision &&
  same_identity(identity,replay.character) && replay.effective_at==0 && facts(decode(bytes),"promotion").size()==1,"new process replay identity, rank, history unique");
}
int main(int argc,char** argv) {
 try{check(argc>=3,"case and output required");const std::string test=argv[1],path=argv[2];
  if(test=="promotion")promotion();else if(test=="negatives")negatives();else if(test=="authority")authority();
  else if(test=="identity")identity();else if(test=="idempotency")idempotency();else if(test=="atomic")atomic();
  else if(test=="corrupt")corrupt();else if(test=="legacy")legacy();else if(test=="history")history(path);
  else if(test=="abi")abi();else if(test=="process_save")process_save(path);else if(test=="process_load")process_load(path);
  else throw std::runtime_error("unknown test");std::cout<<"PASS "<<test<<'\n';return 0;
 }catch(const std::exception& e){std::cerr<<"FAIL: "<<e.what()<<'\n';return 1;}
}
