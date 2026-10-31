// F04 retention policy; all segment ownership, reductions, storage and validation
// belong to Core. This file defines no alternative persistence authority.
#ifdef F04_HISTORY_CORE
namespace {
HistoryCountRule workload_rule() {
 // Exactly planner_person::work: DUTY, nonempty effective interval,
 // STATE==ACTIVE or STOP present. STOP is optional and effective_end=min(END,STOP).
 HistoryCountRule rule{1,"trek.f04:activity",RelationKind{PERSON},{}};
 for(bool stopped:{false,true})for(bool active:{false,true}) {
  if(!active && !stopped)continue;
  std::vector<HistoryPredicate> term{
   {uint16_t(0xF000+VALUE),HistoryPredicateOp::equal,F04_DUTY},
   {uint16_t(0xF000+START),HistoryPredicateOp::less_field,0xF000+END}};
  if(active)term.push_back({uint16_t(0xF000+STATE),HistoryPredicateOp::equal,ACTIVE});
  term.push_back({uint16_t(0xF000+STOP),stopped?HistoryPredicateOp::present:HistoryPredicateOp::absent,0});
  if(stopped)term.push_back({uint16_t(0xF000+START),HistoryPredicateOp::less_field,0xF000+STOP});
  rule.alternatives.push_back(std::move(term));
 }return rule;
}
std::vector<HistorySelection> closed_records(const Campaign& c,U cutoff) {
 const auto& w=c.world;std::map<U,HistorySelection> candidates;
 for(auto entity:projected_ids(w)) {const U id=entity.value();
  if(type(w,id,"event")){const U tick=val(w,id,TICK);if(tick<cutoff)candidates.emplace(id,HistorySelection{entity,tick,tick+1});continue;}
  if(has(w,id,START) && has(w,id,END) && val(w,id,END)<=cutoff && !val(w,id,DEBT) &&
    !(type(w,id,"task") && val(w,id,STATE)==ACTIVE))
   candidates.emplace(id,HistorySelection{entity,val(w,id,START),val(w,id,END)});
 }
 // Keep the transitive dependency closure of every live record. This retains old
 // plans/origins/revocations used by current/future records without rewriting them.
 bool changed=true;while(changed){changed=false;
  for(auto edge:w.relations())if(!candidates.contains(edge.source.value()) && candidates.erase(edge.target.value()))changed=true;
  for(auto entity:projected_ids(w)){const auto container=w.container_of(entity);if(container.status==ContainmentStatus::contained && !candidates.contains(entity.value()) && candidates.erase(container.container.value()))changed=true;}
 }
 std::vector<HistorySelection> out;for(const auto& entry:candidates)out.push_back(entry.second);return out;
}
void history_result(F04Session* s,HistoryStatus status,uint32_t fault) {
 if(status!=HistoryStatus::success && (status==HistoryStatus::io_error || status==HistoryStatus::conflict ||
   (status==HistoryStatus::injected_failure && fault==uint32_t(HistoryFault::after_publish))))s->storage_uncertain=true;
 need(status==HistoryStatus::success,F04_SAVE);
}
}
#endif
// Differential-test export: original records created since an issued-ID cursor,
// plus actual RNG/time. It is a detached diagnostic, never a campaign save.
#ifdef F04_HISTORY_TESTING
extern "C" F04_API uint32_t f04_history_test_delta(F04Session* s,U after,uint8_t* out,U capacity,U* size) {
 if(!size || (!out && capacity))return F04_ARGUMENT;*size=0;return call(s,[&]()->uint32_t {
  auto snapshot=CampaignPersistence::capture(s->c->world,s->c->random,s->c->time);auto& c=snapshot.campaign;
  if(after==UINT64_MAX){std::set<U> ids;
   for(const auto& d:c.definitions)if(d.definition_id=="trek.f04:person" || d.definition_id=="trek.f04:slot" || d.definition_id=="trek.f04:section" || d.definition_id=="trek.f04:department" || d.definition_id=="trek.f04:auxiliary_defiant")ids.insert(d.entity.value());
   std::erase_if(c.definitions,[&](const auto& x){return !ids.contains(x.entity.value());});std::erase_if(c.relations,[&](const auto& x){return !ids.contains(x.source.value());});
   c.last_entity_id=ids.empty()?0:*ids.rbegin();c.containment.clear();snapshot.timeline.now=0;snapshot.timeline.records.clear();
  }else{
   std::erase_if(c.definitions,[&](const auto& x){return x.entity.value()<=after;});std::erase_if(c.relations,[&](const auto& x){return x.source.value()<=after;});
   std::erase_if(c.containment,[&](const auto& x){return x.entity.value()<=after;});
  }
  c.populations.clear();c.population_memberships.clear();c.knowledge.clear();
  // Consolidation adds one technical revision; compare original domain facts,
  // their IDs, exact stream state and clock independently of that revision.
  c.revision=c.last_entity_id+c.containment.size()+c.definitions.size()+c.relations.size();auto bytes=CampaignPersistence::serialize(snapshot);need(bytes.status==CampaignArchiveStatus::success,F04_SAVE);*size=bytes.bytes.size();need(capacity>=*size,F04_CAPACITY);
  if(*size)std::memcpy(out,bytes.bytes.data(),bytes.bytes.size());return F04_OK;
 });
}
extern "C" F04_API uint32_t f04_history_test_validate_full(F04Session* s) {
 return call(s,[&]()->uint32_t {need(schema(*s->c,0,true),F04_INTERNAL);return F04_OK;});
}
#endif
uint32_t f04_history_migrate(F04Session* s,const char* directory,const uint8_t* uuid,U size) {
 if(!directory || !uuid || size!=16)return F04_ARGUMENT;
 return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  need(!s->c->history && schema(*s->c),F04_SAVE);auto next=std::make_unique<Campaign>(*s->c);next->history.emplace();HistoryCampaignId id;std::copy_n(uuid,16,id.begin());
  history_result(s,HistoryPersistence::migrate(std::filesystem::path{reinterpret_cast<const char8_t*>(directory)},id,next->world,next->random,next->time,*next->history,{workload_rule()}),0);
  s->c.swap(next);return F04_OK;
#else
  return F04_SAVE;
#endif
 });
}
uint32_t f04_history_open(F04Session* s,const char* directory) {
 if(!directory)return F04_ARGUMENT;
 return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  auto next=std::make_unique<Campaign>();next->history.emplace();need(HistoryPersistence::recover(std::filesystem::path{reinterpret_cast<const char8_t*>(directory)},*next->history,next->world,next->random,next->time,s->content.catalog())==HistoryStatus::success,F04_SAVE);
  need(next->history->count_rules()==std::vector<HistoryCountRule>{workload_rule()},F04_SAVE);
  need(schema(*next),F04_SAVE);s->c.swap(next);s->storage_uncertain=false;s->scope=scopes.fetch_add(1);s->index_revision=UINT64_MAX;return F04_OK;
#else
  return F04_SAVE;
#endif
 },true);
}
uint32_t f04_history_consolidate(F04Session* s,U cutoff,uint32_t fault) {
 return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  need(s->c->history && s->c->time.now()>=604800 && cutoff<=s->c->time.now()-604800 && fault<=7);
  auto next=std::make_unique<Campaign>(*s->c);auto ids=closed_records(*next,cutoff);
  if(ids.empty()){history_result(s,HistoryPersistence::publish(*next->history,next->world,next->random,next->time,{},static_cast<HistoryFault>(fault)),fault);}
  else {
   const auto validate=[&](const CampaignArchiveSnapshot& projection){auto staged=std::make_unique<Campaign>();staged->history=next->history;
    if(CampaignPersistence::restore(projection,staged->world,staged->random,staged->time,{},s->content.catalog())!=CampaignArchiveStatus::success)return false;
    invalidate_index();return schema(*staged,ids.size());};
   history_result(s,HistoryPersistence::consolidate(*next->history,next->world,next->random,next->time,ids,cutoff,s->content.catalog(),{},static_cast<HistoryFault>(fault),validate),fault);
  }
  s->c.swap(next);s->index_revision=UINT64_MAX;return F04_OK;
#else
  return F04_SAVE;
#endif
 });
}
uint32_t f04_history_publish(F04Session* s,uint32_t fault) {
 return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  need(s->c->history && fault<=7);need(schema(*s->c),F04_SAVE);history_result(s,HistoryPersistence::publish(*s->c->history,s->c->world,s->c->random,s->c->time,{},static_cast<HistoryFault>(fault)),fault);return F04_OK;
#else
  return F04_SAVE;
#endif
 });
}
uint32_t f04_history_stats(F04Session* s,F04HistoryStats* out) {
 if(!out)return F04_ARGUMENT;*out={};return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  need(s->c->history.has_value(),F04_SAVE);const auto& a=*s->c->history;*out={1,a.generation(),s->c->world.entity_count(),a.resident_count(s->c->world),a.archived_count(),a.segments().size(),a.frontier(),s->c->world.relations().size()};return F04_OK;
#else
  return F04_SAVE;
#endif
 });
}
uint32_t f04_history_count(F04Session* s,F04Ref who,U person,U* shifts) {
 if(!shifts)return F04_ARGUMENT;*shifts=0;return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  need(observer(s,who),F04_DENIED);need(s->c->history && type(s->c->world,person,"person"));*shifts=s->c->history->count(1,EntityId{person});return F04_OK;
#else
  return F04_SAVE;
#endif
 });
}
uint32_t f04_history_export_active(F04Session* s,uint8_t* out,U capacity,U* size) {
 if(!size || (!out && capacity))return F04_ARGUMENT;*size=0;return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  need(s->c->history.has_value(),F04_SAVE);auto bytes=CampaignPersistence::serialize(CampaignPersistence::capture(s->c->world,s->c->random,s->c->time));need(bytes.status==CampaignArchiveStatus::success,F04_SAVE);*size=bytes.bytes.size();need(capacity>=*size,F04_CAPACITY);if(*size)std::memcpy(out,bytes.bytes.data(),bytes.bytes.size());return F04_OK;
#else
  return F04_SAVE;
#endif
 });
}
uint32_t f04_history_page(F04Session* s,F04Ref who,U generation,U after,F04HistoryFact* out,U capacity,U* written,uint32_t* more) {
 if(!written || !more || !out || !capacity || capacity>256)return F04_ARGUMENT;*written=0;*more=0;
 return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  need(observer(s,who),F04_DENIED);need(s->c->history && generation==s->c->history->generation(),F04_STALE);auto page=HistoryPersistence::query(*s->c->history,EntityId{after},capacity);need(page.status==HistoryStatus::success,F04_SAVE);
  for(const auto& fact:page.facts)need(fact.definition.size()<64,F04_INTERNAL);
  for(size_t i=0;i<page.facts.size();++i){const auto& fact=page.facts[i];out[i]={fact.identity.entity.value(),fact.identity.begin,fact.identity.end,fact.container?fact.container->value():0,fact.relations.size(),{}};std::memcpy(out[i].definition,fact.definition.data(),fact.definition.size());}
  *written=page.facts.size();*more=page.more?1U:0U;return F04_OK;
#else
  return F04_SAVE;
#endif
 });
}
uint32_t f04_history_relations(F04Session* s,F04Ref who,U generation,U entity,U offset,F04HistoryRelation* out,U capacity,U* written,U* total) {
 if(!written || !total || (!out && capacity) || !entity || capacity>256)return F04_ARGUMENT;*written=*total=0;
 return call(s,[&]()->uint32_t {
#ifdef F04_HISTORY_CORE
  need(observer(s,who),F04_DENIED);need(s->c->history && generation==s->c->history->generation(),F04_STALE);auto page=HistoryPersistence::query(*s->c->history,EntityId{entity-1},1);need(page.status==HistoryStatus::success,F04_SAVE);
  need(page.facts.size()==1 && page.facts[0].identity.entity.value()==entity,F04_ARGUMENT);const auto& relations=page.facts[0].relations;*total=relations.size();need(offset<=*total);*written=std::min(capacity,*total-offset);
  for(U i=0;i<*written;++i){auto edge=relations[static_cast<size_t>(offset+i)];out[i]={edge.source.value(),edge.kind.value(),edge.target.value()};}return F04_OK;
#else
  return F04_SAVE;
#endif
 });
}
