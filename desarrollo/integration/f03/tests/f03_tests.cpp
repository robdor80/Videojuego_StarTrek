#include "f03_bridge.h"
#include <corerpg/campaign_persistence.hpp>
#include <algorithm>
#include <array>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>
#define CHECK(x) do { if(!(x)) throw std::runtime_error(#x); } while(false)
struct Session {
    F03Session* p{};
    explicit Session(uint64_t seed=2372) { CHECK(f03_create(1,seed,&p)==F03_OK); }
    ~Session() { if(p) f03_destroy(p); }
    F03Handles handles() { F03Handles h{}; CHECK(f03_handles(p,&h)==F03_OK); return h; }
    F03Stats stats() { F03Stats s{}; CHECK(f03_stats(p,&s)==F03_OK); return s; }
    std::vector<uint8_t> save() {
        uint64_t size{}; CHECK(f03_save(p,nullptr,0,&size)==F03_CAPACITY);
        std::vector<uint8_t> bytes(static_cast<size_t>(size));
        CHECK(f03_save(p,bytes.data(),size,&size)==F03_OK); return bytes;
    }
    std::vector<F03Fact> view(F03Ref observer,uint32_t context=0) {
        std::array<F03Fact,32> facts{}; uint64_t n{};
        CHECK(f03_view(p,observer,context,facts.data(),facts.size(),&n)==F03_OK);
        return {facts.begin(),facts.begin()+static_cast<size_t>(n)};
    }
    uint64_t advance(uint64_t to) { uint64_t n{}; CHECK(f03_advance(p,to,64,&n)==F03_OK); return n; }
    F03MarkerState marker(F03Ref ref) { F03MarkerState m{}; CHECK(f03_marker_state(p,ref,&m)==F03_OK); return m; }
    uint64_t roll() { uint64_t r{}; CHECK(f03_roll(p,handles().primary,stats().revision,&r)==F03_OK); return r; }
    void route() { CHECK(f03_schedule_route(p)==F03_OK); }
    void acquire() { CHECK(f03_acquire(p,handles().secondary,1)==F03_OK); }
    void load(const std::vector<uint8_t>& bytes) { CHECK(f03_load(p,bytes.data(),bytes.size())==F03_OK); }
};
bool romulan(const std::vector<F03Fact>& facts) {
    return std::any_of(facts.begin(),facts.end(),[](const auto& f) { return f.classification==2; });
}
void integrated(Session& s) {
    s.route(); CHECK(s.advance(20)==2); s.acquire();
    CHECK(f03_acquire(s.p,s.handles().primary,2)==F03_OK); s.roll();
}
void run(const std::string& name,const std::string& file) {
    Session s; const auto h=s.handles();
    if(name=="identity") {
        CHECK(s.stats().entities==8); CHECK(h.primary.id!=h.secondary.id);
        CHECK(s.marker(h.primary).identity==h.primary.id); CHECK(s.marker(h.secondary).location==1);
    } else if(name=="determinism") {
        Session same; CHECK(s.save()==same.save()); integrated(s); integrated(same); CHECK(s.save()==same.save());
        Session different(2373); CHECK(s.save()!=different.save());
    } else if(name=="observers") {
        CHECK(s.view(h.primary).size()!=s.view(h.secondary).size());
        CHECK(s.view(h.primary)[0].contact!=s.view(h.secondary)[0].contact);
    } else if(name=="hidden") {
        CHECK(!romulan(s.view(h.primary))); CHECK(!romulan(s.view(h.secondary)));
        CHECK(!romulan(s.view(h.primary,1))); CHECK(!romulan(s.view(h.secondary,1)));
        CHECK(f03_acquire(s.p,h.secondary,1)==F03_DENIED);
    } else if(name=="acquire") {
        s.route(); s.advance(19); CHECK(f03_acquire(s.p,h.secondary,1)==F03_DENIED);
        s.advance(20); s.acquire(); CHECK(romulan(s.view(h.secondary))); CHECK(!romulan(s.view(h.primary)));
        const auto before=s.save(); s.acquire(); CHECK(before==s.save());
    } else if(name=="report") {
        CHECK(f03_acquire(s.p,h.primary,2)==F03_DENIED); s.route(); s.advance(20); s.acquire();
        const auto n=s.view(h.primary).size(); CHECK(f03_acquire(s.p,h.primary,2)==F03_OK);
        CHECK(s.view(h.primary).size()==n+1); CHECK(!romulan(s.view(h.primary))); CHECK(romulan(s.view(h.secondary)));
    } else if(name=="denied") {
        const auto before=s.save(); CHECK(f03_set_permission(s.p,0)==F03_OK);
        CHECK(f03_schedule_route(s.p)==F03_DENIED); uint64_t n{},r{}; F03MarkerState m{}; F03Fact f{};
        CHECK(f03_advance(s.p,100,64,&n)==F03_DENIED);
        CHECK(f03_acquire(s.p,h.primary,2)==F03_DENIED);
        CHECK(f03_view(s.p,h.primary,0,&f,1,&n)==F03_DENIED);
        CHECK(f03_marker_state(s.p,h.primary,&m)==F03_DENIED);
        CHECK(f03_roll(s.p,h.primary,s.stats().revision,&r)==F03_DENIED); CHECK(before==s.save());
        CHECK(f03_set_permission(s.p,1)==F03_OK); s.route();
    } else if(name=="readonly") {
        const auto before=s.save(); for(int i=0;i<10;++i) { s.view(h.primary); s.view(h.secondary,1); s.marker(h.secondary); }
        CHECK(before==s.save());
    } else if(name=="offscreen") {
        s.route(); CHECK(s.advance(20)==2); CHECK(s.marker(h.secondary).location==2); CHECK(s.stats().entities==8);
    } else if(name=="order") {
        s.route(); CHECK(s.advance(9)==0); CHECK(s.marker(h.secondary).location==1);
        CHECK(s.advance(10)==1); CHECK(s.marker(h.secondary).location==0);
        CHECK(s.advance(20)==1); CHECK(s.marker(h.secondary).location==2);
        CHECK(s.advance(21)==1); CHECK(s.advance(40)==1); CHECK(s.marker(h.secondary).location==1);
    } else if(name=="bounded") {
        s.route(); uint64_t n{}; CHECK(f03_advance(s.p,100,1,&n)==F03_MORE && n==1); CHECK(s.stats().tick==10);
        const auto bytes=s.save(); Session recovered; recovered.load(bytes);
        CHECK(recovered.advance(100)==3); CHECK(s.advance(100)==3); CHECK(s.save()==recovered.save());
    } else if(name=="duplicate") {
        s.route(); s.advance(100); const auto before=s.save(); s.route(); CHECK(s.advance(100)==0); CHECK(before==s.save());
    } else if(name=="backwards") {
        s.advance(100); const auto before=s.save(); uint64_t n{};
        CHECK(f03_advance(s.p,99,64,&n)==F03_REJECTED && n==0); CHECK(before==s.save());
    } else if(name=="roundtrip") {
        integrated(s); const auto bytes=s.save(); CHECK(s.advance(100)==2); const auto future=s.save();
        CHECK(f03_destroy(s.p)==F03_OK); s.p=nullptr;
        Session recovered(999); recovered.load(bytes); CHECK(recovered.save()==bytes);
        CHECK(romulan(recovered.view(recovered.handles().secondary)));
        CHECK(!romulan(recovered.view(recovered.handles().primary)));
        CHECK(recovered.advance(100)==2); CHECK(recovered.save()==future); CHECK(recovered.stats().entities==8);
    } else if(name=="rng") {
        integrated(s); const auto bytes=s.save(); const auto expected=s.roll(); Session recovered; recovered.load(bytes);
        CHECK(recovered.roll()==expected); CHECK(recovered.save()==s.save());
    } else if(name=="corrupt") {
        integrated(s); const auto valid=s.save();
        for(size_t i=0;i<valid.size();++i) {
            auto bad=valid; bad[i]^=0x80; CHECK(f03_load(s.p,bad.data(),bad.size())==F03_SAVE_REJECTED);
            if(i) CHECK(f03_load(s.p,valid.data(),i)==F03_SAVE_REJECTED);
        }
        CHECK(s.save()==valid); CHECK(s.handles().primary.scope==h.primary.scope);
    } else if(name=="incompatible") {
        const auto valid=s.save(); auto bad=valid; bad[8]=99;
        CHECK(f03_load(s.p,bad.data(),bad.size())==F03_SAVE_REJECTED); CHECK(s.save()==valid);
    } else if(name=="scope") {
        Session other; F03MarkerState m{};
        CHECK(f03_marker_state(other.p,h.secondary,&m)==F03_DENIED);
        const auto valid=s.save(); s.load(valid); CHECK(s.handles().secondary.id==h.secondary.id);
        CHECK(f03_marker_state(s.p,h.secondary,&m)==F03_DENIED);
        CHECK(s.marker(s.handles().secondary).identity==h.secondary.id);
        F03Fact f{}; uint64_t n{}; CHECK(f03_view(s.p,{s.handles().primary.scope,3},0,&f,1,&n)==F03_DENIED);
    } else if(name=="thread") {
        const auto before=s.save(); uint32_t status{};
        std::thread worker([&] { F03Stats x{}; status=f03_stats(s.p,&x); }); worker.join();
        CHECK(status==F03_THREAD); CHECK(s.save()==before);
    } else if(name=="buffers") {
        const auto before=s.save(); uint64_t n{}; std::array<uint8_t,4> small{1,2,3,4};
        CHECK(f03_save(s.p,small.data(),small.size(),&n)==F03_CAPACITY); CHECK(small[0]==1 && small[3]==4);
        CHECK(f03_save(s.p,nullptr,1,&n)==F03_ARGUMENT); CHECK(f03_load(s.p,nullptr,1)==F03_ARGUMENT);
        CHECK(f03_advance(s.p,1,4097,&n)==F03_ARGUMENT); CHECK(s.save()==before);
        F03Session* invalid{}; CHECK(f03_create(2,1,&invalid)==F03_VERSION && invalid==nullptr);
    } else if(name=="stale") {
        const auto revision=s.stats().revision; s.route(); s.advance(20); const auto before=s.save(); uint64_t r{};
        CHECK(f03_roll(s.p,h.primary,revision,&r)==F03_REJECTED); CHECK(s.save()==before);
    } else if(name=="calendar") {
        F03Calendar c{}; CHECK(f03_calendar(s.p,&c)==F03_OK);
        CHECK(c.year==2372 && c.month==3 && c.day==14 && c.hour==10 && c.minute==42 && c.second==0 && c.stardate_elapsed==0);
        s.advance(47); CHECK(f03_calendar(s.p,&c)==F03_OK); CHECK(c.second==47 && c.minute==42);
        s.advance(86400); CHECK(f03_calendar(s.p,&c)==F03_OK); CHECK(c.day==15 && c.hour==10 && c.minute==42);
        const auto bytes=s.save(); Session restored; restored.load(bytes); F03Calendar other{}; CHECK(f03_calendar(restored.p,&other)==F03_OK);
        CHECK(c.day==other.day && c.stardate_elapsed==other.stardate_elapsed);
        uint64_t n{}; CHECK(f03_advance(s.p,UINT64_MAX,64,&n)==F03_REJECTED); CHECK(s.save()==bytes);
    } else if(name=="tampered") {
        using namespace corerpg;
        integrated(s); const auto before=s.save();
        const auto decoded=CampaignPersistence::deserialize(before); CHECK(decoded.snapshot.has_value());
        auto bad=*decoded.snapshot; bad.timeline.records[3].action.actor=EntityId{3};
        auto encoded=CampaignPersistence::serialize(bad); CHECK(encoded.status==CampaignArchiveStatus::success);
        CHECK(f03_load(s.p,encoded.bytes.data(),encoded.bytes.size())==F03_SAVE_REJECTED);
        bad=*decoded.snapshot;
        KnownFact secret; secret.key={EntityId{3},FactKind::definition}; secret.definition=std::make_shared<const std::string>("trek.f03:romulan_ship");
        bad.campaign.knowledge.push_back({EntityId{1},secret});
        std::sort(bad.campaign.knowledge.begin(),bad.campaign.knowledge.end(),[](const auto& a,const auto& b) {
            return a.observer<b.observer || (a.observer==b.observer && a.fact.key<b.fact.key);
        });
        encoded=CampaignPersistence::serialize(bad); CHECK(encoded.status==CampaignArchiveStatus::success);
        CHECK(f03_load(s.p,encoded.bytes.data(),encoded.bytes.size())==F03_SAVE_REJECTED);
        CHECK(s.save()==before);
    } else if(name=="process_save") {
        integrated(s); const auto bytes=s.save();
        // Test-owned deterministic path in the isolated build, never a personal save.
        std::ofstream out(file,std::ios::binary); CHECK(out.good()); out.write(reinterpret_cast<const char*>(bytes.data()),bytes.size());
        CHECK(out.good()); std::cout<<"campaign written; pending=2 tick=20 entities=8\n";
    } else if(name=="process_load") {
        std::ifstream in(file,std::ios::binary); CHECK(in.good());
        const std::vector<uint8_t> bytes{std::istreambuf_iterator<char>{in},{}}; s.load(bytes);
        Session reference; integrated(reference); CHECK(s.save()==reference.save());
        CHECK(s.advance(100)==2); CHECK(reference.advance(100)==2); CHECK(s.save()==reference.save());
        CHECK(s.advance(100)==0); std::cout<<"new process restored campaign; finished=4 tick=100 entities=8\n";
    } else throw std::runtime_error("unknown case");
}
int main(int argc,char** argv) {
    try { CHECK(argc>=2); run(argv[1],argc>=3?argv[2]:""); std::cout<<"PASS "<<argv[1]<<" Core="<<f03_core_sha()<<"\n"; return 0; }
    catch(const std::exception& e) { std::cerr<<"FAIL "<<e.what()<<"\n"; return 1; }
}
