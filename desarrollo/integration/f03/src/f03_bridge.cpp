#include "f03_bridge.h"
#include <corerpg/campaign_persistence.hpp>
#include <corerpg/content_catalog.hpp>
#include <corerpg/context_builder.hpp>
#include <array>
#include <atomic>
#include <cstring>
#include <limits>
#include <memory>
#include <stdexcept>
#include <thread>
#include <type_traits>

namespace {
using namespace corerpg;
std::atomic<uint64_t> scopes{1};
uint64_t scope() {
    auto n=scopes.load();
    for(;;) {
        if(n==UINT64_MAX) throw std::overflow_error("binding scope exhausted");
        if(scopes.compare_exchange_weak(n,n+1)) return n;
    }
}
CatalogBuildResult catalog() {
    const auto p=*PackId::parse("trek.f03"); const auto v=*SemanticVersion::parse("0.1.0");
    std::vector<ContentDefinitionInput> defs;
    for(const auto* text:{"trek.f03:starfleet_ship","trek.f03:romulan_ship","trek.f03:sector","trek.f03:crew"})
        defs.emplace_back(ResourceDefinition{*DefinitionId::parse(text),*ResourceKind::parse("structural")});
    return ContentCatalog::create({ContentPackInput{ContentManifest{p,v,v,v},std::move(defs)}});
}
struct Campaign {
    WorldState world;
    RandomStreams random;
    Timeline time;
    explicit Campaign(uint64_t seed):random(seed) {}
};
void require(bool value) { if(!value) throw std::runtime_error("F03 fixture rejected"); }
uint64_t contact(EntityId observer,EntityId entity) {
    if(!entity.is_valid()) return 0;
    // Presentation keys are observer-relative; never expose Core IDs in a view.
    uint64_t x=entity.value()^(observer.value()*0x9E3779B97F4A7C15ULL);
    x=(x^(x>>30))*0xBF58476D1CE4E5B9ULL; x=(x^(x>>27))*0x94D049BB133111EBULL;
    return (x^(x>>31))|1ULL;
}
}
struct F03Session {
    const std::thread::id owner{std::this_thread::get_id()};
    CatalogBuildResult content{catalog()};
    std::unique_ptr<Campaign> campaign;
    uint64_t binding{scope()};
    bool allowed{true};
    explicit F03Session(uint64_t seed):campaign(std::make_unique<Campaign>(seed)) {
        require(content.succeeded());
        auto& w=campaign->world;
        for(int i=0;i<6;++i) require(w.create_entity().is_valid());
        for(uint64_t i=1;i<=6;++i) {
            const auto* name=i<=2 ? "trek.f03:starfleet_ship" : i==3 ? "trek.f03:romulan_ship" :
                i<=5 ? "trek.f03:sector" : "trek.f03:crew";
            require(w.bind_definition(EntityId{i},*content.catalog(),*DefinitionId::parse(name))==DefinitionBindingChange::applied);
        }
        require(w.place_entity(EntityId{1},EntityId{4})==ContainmentChange::applied);
        require(w.place_entity(EntityId{2},EntityId{4})==ContainmentChange::applied);
        require(w.place_entity(EntityId{3},EntityId{5})==ContainmentChange::applied);
        require(w.declare_population(EntityId{6},3)==PopulationChange::applied);
        require(w.materialize_population(EntityId{6},2).status==MaterializationStatus::applied);
        for(uint64_t id:{7ULL,8ULL}) {
            const auto ship=1+*campaign->random.stream(0xF0301).uniform_closed(0,1);
            require(w.place_entity(EntityId{id},EntityId{ship})==ContainmentChange::applied);
        }
        for(uint64_t observer:{1ULL,2ULL}) {
            for(uint64_t id:{1ULL,2ULL,4ULL}) require(w.learn_fact(EntityId{observer},{EntityId{id}})==KnowledgeChange::applied);
            require(w.learn_fact(EntityId{observer},{EntityId{observer},FactKind::definition})==KnowledgeChange::applied);
        }
        // Secondary knows a destination, but neither observer knows the Romulan ship.
        require(w.learn_fact(EntityId{2},{EntityId{5}})==KnowledgeChange::applied);
    }
    bool observer(F03Ref ref) const { return ref.scope==binding && (ref.id==1 || ref.id==2); }
};
namespace {
uint32_t guard(F03Session* s) { return !s ? F03_ARGUMENT : s->owner!=std::this_thread::get_id() ? F03_THREAD : F03_OK; }
template<class F> uint32_t call(F03Session* s,F&& f) noexcept {
    if(auto status=guard(s);status!=F03_OK) return status;
    try { return f(); } catch(...) { return F03_INTERNAL; }
}
// Saves for this vertical are deliberately bounded and versioned by exact catalog
// bindings/population and the four supported route actions. Not a general game save.
bool fixture(const CampaignArchiveSnapshot& s,const ContentCatalog& content) {
    const auto& w=s.campaign;
    if(w.last_entity_id!=8 || w.definitions.size()!=6 || w.populations.size()!=1 ||
       w.populations[0]!=PopulationRecord{EntityId{6},3,1} || w.population_memberships.size()!=2 ||
       w.population_memberships[0]!=PopulationMembership{EntityId{7},EntityId{6}} ||
       w.population_memberships[1]!=PopulationMembership{EntityId{8},EntityId{6}} || !w.relations.empty()) return false;
    for(size_t i=0;i<w.definitions.size();++i) {
        const auto& d=w.definitions[i];
        const auto* expected=i<2 ? "trek.f03:starfleet_ship" : i==2 ? "trek.f03:romulan_ship" : i<5 ? "trek.f03:sector" : "trek.f03:crew";
        if(d.entity!=EntityId{i+1} || d.definition_id!=expected || !content.find_by_value(d.definition_id)) return false;
    }
    // No imported observer, relation, population or private crew knowledge.
    for(const auto& k:w.knowledge) {
        const auto id=k.fact.key.subject.value(); const auto who=k.observer.value();
        if((who!=1 && who!=2) || id<1 || id>5 || !k.fact.present ||
            (k.fact.key.kind!=FactKind::existence && k.fact.key.kind!=FactKind::definition && k.fact.key.kind!=FactKind::containment) ||
            (who==1 && ((id==3 && k.fact.key.kind!=FactKind::existence) || id==5))) return false;
    }
    return true;
}
}
uint32_t f03_abi_version() { return 1; }
const char* f03_core_sha() { return F03_CORE_SHA; }
uint32_t f03_create(uint32_t abi,uint64_t seed,F03Session** out) {
    if(!out) return F03_ARGUMENT; *out=nullptr;
    if(abi!=1) return F03_VERSION;
    try { *out=new F03Session(seed); return F03_OK; } catch(...) { return F03_INTERNAL; }
}
uint32_t f03_destroy(F03Session* s) { if(auto r=guard(s);r!=F03_OK) return r; delete s; return F03_OK; }
uint32_t f03_handles(F03Session* s,F03Handles* out) {
    if(!out) return F03_ARGUMENT;
    return call(s,[&]() -> uint32_t { *out={{s->binding,1},{s->binding,2}}; return F03_OK; });
}
uint32_t f03_stats(F03Session* s,F03Stats* out) {
    if(!out) return F03_ARGUMENT;
    return call(s,[&]() -> uint32_t {
        const auto& c=*s->campaign; uint64_t done=0;
        for(const auto& r:c.time.records()) if(r.state!=TimedState::pending) ++done;
        *out={c.world.entity_count(),c.world.revision(),c.time.now(),c.time.records().size(),done}; return F03_OK;
    });
}
uint32_t f03_set_permission(F03Session* s,uint32_t allowed) {
    if(allowed>1) return F03_ARGUMENT;
    return call(s,[&]() -> uint32_t { s->allowed=allowed!=0; return F03_OK; });
}
uint32_t f03_schedule_route(F03Session* s) {
    return call(s,[&]() -> uint32_t {
        if(!s->allowed) return F03_DENIED;
        auto candidate=s->campaign->time;
        const std::array<TimedAction,4> route{{
            {1,10,0,EntityId{2},RemoveContainmentAction{EntityId{2}}},
            {2,20,1,EntityId{2},PlaceEntityAction{EntityId{2},EntityId{5}}},
            {3,21,2,EntityId{2},StreamRollAction{0xF0303,1,1000000}},
            {4,40,3,EntityId{2},PlaceEntityAction{EntityId{2},EntityId{4}}}}};
        for(const auto& action:route) {
            const auto status=candidate.schedule(s->campaign->world,action);
            if(status!=TimelineStatus::completed && status!=TimelineStatus::no_change) return F03_REJECTED;
        }
        static_assert(std::is_nothrow_move_assignable_v<Timeline>);
        s->campaign->time=std::move(candidate); return F03_OK;
    });
}
uint32_t f03_advance(F03Session* s,uint64_t horizon,uint64_t max,uint64_t* processed) {
    if(!processed || max>Timeline::max_records) return F03_ARGUMENT; *processed=0;
    return call(s,[&]() -> uint32_t {
        if(!s->allowed) return F03_DENIED;
        auto& c=*s->campaign; const auto result=c.time.advance(c.world,c.random,horizon,static_cast<size_t>(max));
        *processed=result.processed;
        return result.status==TimelineStatus::completed ? F03_OK : result.status==TimelineStatus::action_limit ? F03_MORE : F03_REJECTED;
    });
}
uint32_t f03_acquire(F03Session* s,F03Ref observer,uint32_t channel) {
    return call(s,[&]() -> uint32_t {
        if(!s->allowed || !s->observer(observer)) return F03_DENIED;
        auto& c=*s->campaign;
        if(channel==1) {
            if(observer.id!=2 || c.world.container_of(EntityId{2}).container!=EntityId{5}) return F03_DENIED;
        } else if(channel==2) {
            if(observer.id!=1 || !Visibility::project(c.world,EntityId{2}).knows(EntityId{3})) return F03_DENIED;
        } else return F03_DENIED;
        // Stage all acquisitions, so allocation failure never publishes a partial report.
        auto candidate=c.world;
        for(auto kind:{FactKind::existence,FactKind::definition,FactKind::containment}) {
            if(channel==2 && kind!=FactKind::existence) continue;
            const auto status=candidate.learn_fact(EntityId{observer.id},{EntityId{3},kind});
            if(status!=KnowledgeChange::applied && status!=KnowledgeChange::no_change) return F03_REJECTED;
        }
        c.world=std::move(candidate); return F03_OK;
    });
}
uint32_t f03_view(F03Session* s,F03Ref observer,uint32_t context,F03Fact* out,uint64_t capacity,uint64_t* count) {
    if(!count || (!out && capacity) || context>1) return F03_ARGUMENT; *count=0;
    return call(s,[&]() -> uint32_t {
        if(!s->allowed || !s->observer(observer)) return F03_DENIED;
        const auto who=EntityId{observer.id}; const auto view=Visibility::project(s->campaign->world,who);
        std::array<VisibleFact,32> selected; auto facts=view.facts();
        if(context) {
            ContextRequest request; request.subject=who;
            const auto result=ContextBuilder::build(view,request,selected);
            if(result.status!=ContextStatus::complete) return F03_INTERNAL;
            facts=std::span<const VisibleFact>{selected}.first(result.emitted);
        }
        *count=facts.size(); if(capacity<facts.size()) return F03_CAPACITY;
        for(size_t i=0;i<facts.size();++i) {
            const auto& f=facts[i];
            const uint32_t classification=f.definition_id()=="trek.f03:starfleet_ship" ? 1 : f.definition_id()=="trek.f03:romulan_ship" ? 2 : 0;
            out[i]={contact(who,f.key.subject),contact(who,f.reference),static_cast<uint32_t>(f.key.kind),f.present?1U:0U,
                classification,static_cast<uint32_t>(f.provenance())};
        }
        return F03_OK;
    });
}
uint32_t f03_marker_state(F03Session* s,F03Ref ref,F03MarkerState* out) {
    if(!out) return F03_ARGUMENT; *out={};
    return call(s,[&]() -> uint32_t {
        if(!s->allowed || !s->observer(ref)) return F03_DENIED;
        const std::array grants{FactKey{EntityId{ref.id},FactKind::containment}};
        const auto view=Visibility::project(s->campaign->world,EntityId{ref.id},grants);
        const auto* f=view.find(grants[0]); if(!f) return F03_REJECTED;
        *out={ref.id,!f->present ? 0U : f->reference==EntityId{4} ? 1U : f->reference==EntityId{5} ? 2U : 0U,0};
        return F03_OK;
    });
}
uint32_t f03_roll(F03Session* s,F03Ref ref,uint64_t revision,uint64_t* out) {
    if(!out) return F03_ARGUMENT; *out=0;
    return call(s,[&]() -> uint32_t {
        if(!s->allowed || !s->observer(ref)) return F03_DENIED;
        auto& c=*s->campaign;
        const auto result=ActionEngine::process(c.world,c.random,{EntityId{ref.id},StreamRollAction{0xF0304,1,1000000},revision});
        const auto* roll=std::get_if<RollConsequence>(&result.consequence);
        if(!roll || result.outcome==ActionOutcome::rejected) return F03_REJECTED;
        *out=roll->value; return F03_OK;
    });
}
uint32_t f03_save(F03Session* s,uint8_t* out,uint64_t capacity,uint64_t* size) {
    if(!size || (!out && capacity)) return F03_ARGUMENT; *size=0;
    return call(s,[&]() -> uint32_t {
        const auto& c=*s->campaign; const auto saved=CampaignPersistence::serialize(CampaignPersistence::capture(c.world,c.random,c.time));
        if(saved.status!=CampaignArchiveStatus::success) return F03_SAVE_REJECTED;
        *size=saved.bytes.size(); if(capacity<*size) return F03_CAPACITY;
        std::memcpy(out,saved.bytes.data(),saved.bytes.size()); return F03_OK;
    });
}
uint32_t f03_load(F03Session* s,const uint8_t* bytes,uint64_t size) {
    if(!bytes || !size || size>64ULL*1024*1024) return F03_ARGUMENT;
    return call(s,[&]() -> uint32_t {
        const auto decoded=CampaignPersistence::deserialize({bytes,static_cast<size_t>(size)});
        if(decoded.status!=CampaignArchiveStatus::success || !fixture(*decoded.snapshot,*s->content.catalog())) return F03_SAVE_REJECTED;
        const auto binding=scope(); auto candidate=std::make_unique<Campaign>(0);
        if(CampaignPersistence::restore(*decoded.snapshot,candidate->world,candidate->random,candidate->time,{},s->content.catalog())!=CampaignArchiveStatus::success) return F03_SAVE_REJECTED;
        s->campaign.swap(candidate); s->binding=binding; return F03_OK;
    });
}
