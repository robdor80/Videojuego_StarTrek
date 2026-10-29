#include "f02_bridge.h"
#include <array>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

#define CHECK(x) do { if (!(x)) throw std::runtime_error(#x); } while(false)
struct Session {
    F02Session* p{};
    Session() { CHECK(f02_create(1, 2372, &p) == F02_OK); }
    ~Session() { if (p) f02_destroy(p); }
    F02Handles handles() { F02Handles h{}; CHECK(f02_handles(p, &h) == F02_OK); return h; }
    uint64_t revision() { uint64_t r{}; CHECK(f02_revision(p, &r) == F02_OK); return r; }
    std::vector<uint8_t> save() {
        uint64_t n{}; CHECK(f02_save(p, nullptr, 0, &n) == F02_CAPACITY);
        std::vector<uint8_t> bytes(static_cast<size_t>(n));
        CHECK(f02_save(p, bytes.data(), bytes.size(), &n) == F02_OK); return bytes;
    }
    void place() {
        auto h = handles(); F02ActionResult result{};
        CHECK(f02_place(p, h.subject, h.room, revision(), &result) == F02_OK);
        CHECK(result.revision_after == result.revision_before + 1);
    }
    uint64_t roll() {
        F02ActionResult result{};
        CHECK(f02_roll(p, handles().subject, 1, 1000000, revision(), &result) == F02_OK);
        return result.rolled;
    }
};
void run(const std::string& name) {
    Session s; auto h = s.handles();
    if (name == "identity") {
        uint32_t exists{};
        CHECK(f02_contains(s.p, h.subject, &exists) == F02_OK && exists == 1);
        // Native code has no fake Actor lifecycle; the real lifecycle is tested in UE.
        CHECK(s.handles().subject.id == h.subject.id);
    } else if (name == "placement") {
        s.place(); std::array<F02Fact,8> facts{}; uint64_t n{};
        CHECK(f02_view(s.p, 0, facts.data(), facts.size(), &n) == F02_OK);
        bool found=false;
        for (size_t i=0;i<n;++i) if (facts[i].subject==h.subject.id && facts[i].kind==3)
            found = facts[i].present && facts[i].reference==h.room.id;
        CHECK(found);
    } else if (name == "invalid") {
        const auto before=s.save(); F02ActionResult r{};
        CHECK(f02_roll(s.p,h.subject,10,1,s.revision(),&r)==F02_CORE_REJECTED);
        CHECK(r.core_rejection != 0 && before==s.save());
    } else if (name == "stale") {
        auto old=s.revision(); s.place(); auto before=s.save(); F02ActionResult r{};
        CHECK(f02_roll(s.p,h.subject,1,6,old,&r)==F02_CORE_REJECTED);
        CHECK(r.core_rejection!=0 && before==s.save());
    } else if (name == "denied") {
        auto before=s.save(); auto old=s.revision(); CHECK(f02_set_permission(s.p,0)==F02_OK);
        F02ActionResult r{};
        CHECK(f02_place(s.p,h.subject,h.room,old,&r)==F02_DENIED);
        CHECK(f02_roll(s.p,h.subject,1,6,old,&r)==F02_DENIED);
        CHECK(before==s.save());
        CHECK(f02_set_permission(s.p,1)==F02_OK);
        F02Ref hidden{h.subject.scope,3};
        CHECK(f02_place(s.p,h.subject,hidden,old,&r)==F02_DENIED);
        CHECK(before==s.save());
    } else if (name == "visibility" || name == "context") {
        s.place(); auto before=s.save(); std::array<F02Fact,8> facts{}; uint64_t n{};
        CHECK(f02_view(s.p,name=="context",facts.data(),facts.size(),&n)==F02_OK);
        CHECK(n==(name=="context" ? 2U : 3U));
        for(size_t i=0;i<n;++i) {
            CHECK(facts[i].subject!=3 && facts[i].reference!=3);
            if(name=="context") CHECK(facts[i].subject==h.subject.id);
        }
        CHECK(before==s.save());
        uint32_t exists=1;
        CHECK(f02_contains(s.p,{h.subject.scope,3},&exists)==F02_DENIED && exists==0);
    } else if (name == "roundtrip") {
        s.place(); s.roll(); auto bytes=s.save();
        const auto path=std::filesystem::path("f02-roundtrip.save");
        { std::ofstream file(path,std::ios::binary); CHECK(file.good());
          file.write(reinterpret_cast<const char*>(bytes.data()),bytes.size()); CHECK(file.good()); }
        std::ifstream file(path,std::ios::binary);
        std::vector<uint8_t> disk{std::istreambuf_iterator<char>(file),{}};
        CHECK(bytes==disk);
        Session recovered;
        CHECK(f02_load(recovered.p,disk.data(),disk.size())==F02_OK);
        CHECK(recovered.handles().subject.id==h.subject.id && recovered.save()==bytes);
        const auto current=recovered.handles(); F02ActionResult result{};
        CHECK(f02_place(recovered.p,current.subject,current.room,recovered.revision(),&result)==F02_OK);
        CHECK(result.revision_before==result.revision_after && recovered.save()==bytes);
    } else if (name == "rng") {
        s.roll(); auto saved=s.save(); auto expected=s.roll();
        CHECK(f02_load(s.p,saved.data(),saved.size())==F02_OK);
        CHECK(s.roll()==expected);
    } else if (name == "corrupt") {
        s.place(); s.roll(); const auto before=s.save();
        for (auto index : {size_t{0},before.size()/2,before.size()-1}) {
            auto bytes=before; bytes[index]^=0x5a;
            CHECK(f02_load(s.p,bytes.data(),bytes.size())==F02_SAVE_REJECTED);
            CHECK(s.save()==before && s.handles().subject.scope==h.subject.scope);
        }
        CHECK(f02_load(s.p,before.data(),before.size()-1)==F02_SAVE_REJECTED);
        CHECK(s.save()==before);
    } else if (name == "incompatible") {
        CHECK(f02_abi_version()==1);
        CHECK(std::string(f02_core_sha())=="4f282863737bcd8f5add401202a9e1064c133672");
        F02Session* bad=nullptr; CHECK(f02_create(99,1,&bad)==F02_VERSION && !bad);
        const auto before=s.save(); auto unsupported=before;
        // Audited Core save header: eight-byte magic then little-endian uint32 version.
        CHECK(unsupported.size()>12); unsupported[8]=99;
        CHECK(f02_load(s.p,unsupported.data(),unsupported.size())==F02_SAVE_REJECTED);
        CHECK(s.save()==before);
    } else if (name == "scope") {
        Session other; F02ActionResult r{}; auto before=other.save();
        CHECK(f02_place(other.p,h.subject,other.handles().room,other.revision(),&r)==F02_DENIED);
        CHECK(other.save()==before);
        auto bytes=s.save(); CHECK(f02_load(s.p,bytes.data(),bytes.size())==F02_OK);
        CHECK(s.handles().subject.id==h.subject.id && s.handles().subject.scope!=h.subject.scope);
        CHECK(f02_roll(s.p,h.subject,1,6,s.revision(),&r)==F02_DENIED);
        CHECK(s.save()==bytes);
    } else if (name == "thread") {
        auto before=s.save(); uint32_t read=0,write=0,destroy=0;
        uint32_t result_status=0;
        std::thread worker([&] {
            uint64_t rev{}; read=f02_revision(s.p,&rev);
            F02ActionResult r{}; write=f02_roll(s.p,h.subject,1,6,0,&r);
            result_status=r.status;
            destroy=f02_destroy(s.p);
        }); worker.join();
        CHECK(read==F02_THREAD && write==F02_THREAD && destroy==F02_THREAD);
        CHECK(result_status==F02_THREAD);
        CHECK(before==s.save());
    } else if (name == "buffers") {
        auto before=s.save(); uint64_t n{}; std::array<uint8_t,2> buffer{0xaa,0xbb};
        CHECK(f02_save(s.p,buffer.data(),buffer.size(),&n)==F02_CAPACITY);
        CHECK(buffer[0]==0xaa && buffer[1]==0xbb && n>2);
        std::array<F02Fact,1> facts{{{99,99,99,99}}};
        CHECK(f02_view(s.p,0,facts.data(),1,&n)==F02_CAPACITY && facts[0].subject==99);
        CHECK(f02_save(s.p,nullptr,1,&n)==F02_ARGUMENT);
        CHECK(f02_load(s.p,nullptr,10)==F02_ARGUMENT);
        CHECK(before==s.save());
    } else if (name == "host_failure") {
        s.place(); auto saved=s.save(); auto expected=s.roll();
        CHECK(f02_destroy(s.p)==F02_OK); s.p=nullptr;
        Session restarted;
        CHECK(f02_load(restarted.p,saved.data(),saved.size())==F02_OK);
        CHECK(restarted.handles().subject.id==h.subject.id && restarted.roll()==expected);
        // Process crash/power-loss durability is not claimed by this test.
    } else throw std::runtime_error("unknown case");
}
int main(int argc,char** argv) {
    try { CHECK(argc==2); run(argv[1]); std::cout<<"PASS "<<argv[1]<<'\n'; return 0; }
    catch(const std::exception& e) { std::cerr<<"FAIL "<<(argc>1?argv[1]:"arguments")<<": "<<e.what()<<'\n'; return 1; }
}
