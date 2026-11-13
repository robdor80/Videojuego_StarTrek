#include "test_support.h"
#include "player_bootstrap.h"
#include "slot_store.h"
#include "f05_player_binding.h"
#include <atomic>
#include <chrono>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <semaphore>
#include <thread>
#include <map>
#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#endif

namespace trek::host::detail {
std::function<void(F04Session*,bool)> native_observer;
void persistence_test_observe(F04Session* session,bool saving) {try {if(native_observer)native_observer(session,saving);}catch(const std::exception& e){std::cerr<<"Core observation: "<<e.what()<<'\n';throw;}}
}
namespace fs=std::filesystem;
using namespace test;
using namespace trek::host::detail;
using namespace std::chrono_literals;
namespace {
StorageConfig config;
std::string campaign;
fs::path base;
void put(const fs::path& p,const std::string& data){std::ofstream out(p,std::ios::binary|std::ios::trunc);out<<data;require(bool(out),"Write failed");}
std::string get(const fs::path& p){std::ifstream in(p,std::ios::binary);return {std::istreambuf_iterator<char>(in),{}};}
Generation start(SessionOwner& owner,PopulationConfig cfg=population()) {
    auto opened=owner.open(cfg).get();expect(opened,Error::OK);auto generation=opened.generation;campaign=owner.campaign_id(generation);require(campaign.size()==32,"Missing campaign identity");require(owner.campaign_provenance(generation)==Provenance::CREATED_LOCALLY,"Wrong new provenance");
    auto selected=PlayerBootstrap::prepare(owner,generation,4).get();require(selected.error==Error::OK,"Prepare player");
    require(PlayerBootstrap::bind(owner,generation,*selected.selection,selected.revision).get().error==Error::OK,"Bind player");return generation;
}
fs::path generation_path(unsigned n=1){return base/"campaigns"/campaign/"slots"/"alpha"/("v"+std::to_string(n));}
void check_player(SessionOwner& owner,Generation generation) {
    auto p=owner.current_player(generation);require(p.error==Error::OK && p.player && p.player->person_id==4,"Wrong restored identity");
}
void roundtrip() {
    SessionOwner owner(config);auto old=start(owner);
    auto selected=PlayerBootstrap::prepare(owner,old,4).get();
    expect(owner.save(old,"alpha").get(),Error::OK);check_player(owner,old);
    auto loaded=owner.restore(old,{campaign,"alpha"}).get();expect(loaded,Error::OK);require(loaded.generation!=old,"Reused generation");
    expect(owner.check_active(old).get(),Error::GENERATION_EXPIRED);
    require(PlayerBootstrap::bind(owner,loaded.generation,*selected.selection,selected.revision).get().error==Error::SCOPE_INVALID,"Old campaign selection accepted");
    check_player(owner,loaded.generation);require(owner.campaign_provenance(loaded.generation)==Provenance::KNOWN_LOCAL,"Wrong restore provenance");
    expect(owner.save(loaded.generation,"alpha").get(),Error::OK);
    auto filesystem_state=[&]{std::map<std::string,std::pair<std::uintmax_t,fs::file_time_type>> files;
        for(auto& entry:fs::recursive_directory_iterator(base))if(entry.is_regular_file())files.emplace(entry.path().string(),std::make_pair(entry.file_size(),entry.last_write_time()));return files;};
    auto before_inspection=filesystem_state();
    auto inspected=SessionOwner::inspect(config);require(filesystem_state()==before_inspection,"Inspection mutated files");require(inspected.error==Error::OK && inspected.slots.size()==2,"Inspection versions");
    for(auto& slot:inspected.slots)require(slot.recoverable && slot.reason==Error::OK && slot.provenance==Provenance::KNOWN_LOCAL,"Invalid saved slot");
    auto previous=owner.restore(loaded.generation,{campaign,"alpha",1}).get();expect(previous,Error::OK);check_player(owner,previous.generation);
    expect(owner.close().get(),Error::OK);
    auto reopened=owner.restore({}, {campaign,"alpha",2}).get();expect(reopened,Error::OK);check_player(owner,reopened.generation);
}
void reader() {
    F04Session* session=nullptr;require(f04_create(1,"miranda",&session)==F04_OK,"Create");
    F04Stats before{},after{};F05PlayerBinding binding{};F04Handles handles{};
    require(f04_stats(session,&before)==F04_OK && f05_player_binding(session,&binding)==F04_OK && !binding.record && !binding.person.id,"Reader invented binding");
    require(f04_stats(session,&after)==F04_OK && before.revision==after.revision,"Reader mutated");
    require(f04_handles(session,&handles)==F04_OK && f05_bind_player(session,handles.ensign,before.revision)==F04_OK,"Bind core");
    require(f05_player_binding(session,&binding)==F04_OK && binding.record && binding.person.id==handles.ensign.id,"Read bind");
    require(f04_stats(session,&before)==F04_OK,"Stats");
    F05PlayerBinding wrong=binding;std::thread worker([&]{require(f05_player_binding(session,&wrong)==F04_THREAD,"Thread reader accepted");});worker.join();
    require(!wrong.record && !wrong.person.id,"Failed reader leaked identity");
    require(f05_player_binding(session,&binding)==F04_OK && f04_stats(session,&after)==F04_OK && before.revision==after.revision,"Reader changed revision");
    require(f04_destroy(session)==F04_OK,"Destroy");
}
std::vector<std::uint8_t> active_bytes(F04Session* session) {
    std::uint64_t size=0;require(f04_history_export_active(session,nullptr,0,&size)==F04_CAPACITY,"Diagnostic size");
    std::vector<std::uint8_t> data(size);require(f04_history_export_active(session,data.data(),size,&size)==F04_OK,"Diagnostic bytes");return data;
}
void prepare_archived_campaign(F04Session* session) {
    F04Handles h{};require(f04_handles(session,&h)==F04_OK,"Live handles");
    auto op=[&](F04Ref actor,std::uint32_t kind,std::uint64_t target=0,std::uint64_t aux=0,std::uint64_t begin=0,std::uint64_t end=0,std::uint32_t value=0){
        F04Stats st{};require(f04_stats(session,&st)==F04_OK,"Live revision");
        F04Request request{actor,st.revision,kind,value,target,aux,begin,end,42};F04Result result{};
        auto code=f04_execute(session,&request,&result);
        if(code!=F04_OK)throw std::runtime_error("Live operation "+std::to_string(kind)+" code "+std::to_string(code));
    };
    F04TemplateSpec spec{};require(f04_template_spec(F04_SUTHERLAND_SCIENCE,&spec)==F04_OK,"Template spec");
    op(h.captain,F04_INSTALL_TEMPLATE,0,spec.required_equipment,0,0,F04_SUTHERLAND_SCIENCE);
    op(h.captain,F04_BOOTSTRAP_TEMPLATE);
    op(h.captain,F04_PLAN_WATCHES,0,1,0,14*86400,F04_ROTATING);
    std::uint64_t count=0,total=0;F04Position positions[256]{};
    require(f04_positions_page(session,h.captain,0,positions,256,&count,&total)==F04_OK,"Positions");
    bool scanned=false;
    for(std::uint64_t i=0;i<count && !scanned;++i) {
        auto p=positions[i];F04Person view{};
        if(!p.person || !(p.stations&F04_ST_SENSORS))continue;
        require(f04_person(session,h.captain,p.person,&view)==F04_OK,"Person");
        if(!view.on_duty)continue;
        F04Ref actor{h.ship.scope,p.person};op(actor,F04_MOVE,p.id);op(actor,F04_SCAN);scanned=true;
    }
    require(scanned,"No actual RNG scan performed");
    auto id=decode_campaign(campaign);auto path=(base/"live_history").u8string();
    require(f04_history_migrate(session,reinterpret_cast<const char*>(path.c_str()),id.data(),16)==F04_OK,"Migrate live history");
    std::uint64_t processed=0;require(f04_advance(session,8*86400,4096,&processed)==F04_OK,"Advance live Core");
    require(f04_history_consolidate(session,86400,0)==F04_OK,"Consolidate actual closed facts");
}
void history_rng() {
    SessionOwner owner(config);auto generation=start(owner,{"miranda",65001,404,130,0,0,0});
    std::vector<std::uint8_t> expected;F04HistoryStats historical{};F04Stats stats{};bool first=true;unsigned observations=0;
    native_observer=[&](F04Session* session,bool saving){
        if(saving) {
            if(first) {
                prepare_archived_campaign(session);first=false;
            } else {
                F04Stats st{};std::uint64_t processed=0;require(f04_stats(session,&st)==F04_OK && f04_advance(session,st.now+17,4096,&processed)==F04_OK,"Continue after load");
            }
            require(f04_stats(session,&stats)==F04_OK && f04_history_stats(session,&historical)==F04_OK && historical.archived>0,"No actual archived originals");
            expected=active_bytes(session);
        } else {
            require(active_bytes(session)==expected,"RNG/timeline/relations/revision differ after load");
            F04Stats restored{};F04HistoryStats history{};
            require(f04_stats(session,&restored)==F04_OK && restored.now==stats.now && restored.revision==stats.revision,"Clock or revision lost");
            require(f04_history_stats(session,&history)==F04_OK && history.archived==historical.archived && history.segments==historical.segments && history.issued==historical.issued,"Archived originals lost");
            F04Handles h{};require(f04_handles(session,&h)==F04_OK,"Restored handles");
            F04HistoryFact page[256]{};std::uint64_t written=0;std::uint32_t more=0;
            require(f04_history_page(session,h.captain,history.generation,0,page,256,&written,&more)==F04_OK && written>0,"Original history unreadable");++observations;
        }
    };
    expect(owner.save(generation,"alpha").get(),Error::OK);
    auto result=owner.restore(generation,{campaign,"alpha"}).get();expect(result,Error::OK);
    expect(owner.save(result.generation,"alpha").get(),Error::OK);
    auto again=owner.restore(result.generation,{campaign,"alpha"}).get();expect(again,Error::OK);
    require(observations>=4,"Missing complete snapshots");
    fs::path segment;
    for(auto& file:fs::directory_iterator(generation_path(2)/"history")) {
        if(file.path().extension()==".obj" && get(file.path()).starts_with("CRPGSEG1")) {
            segment=file.path();require(get(segment)==get(base/"live_history"/segment.filename()),"Original historical bytes changed");break;
        }
    }
    require(!segment.empty(),"Snapshot lacks original segment");
    fs::rename(segment,base/"preserved.segment");
    expect(owner.restore(again.generation,{campaign,"alpha",2}).get(),Error::SAVE_CORRUPT);check_player(owner,again.generation);
    fs::rename(base/"preserved.segment",segment);
    expect(owner.restore(again.generation,{campaign,"alpha",2}).get(),Error::OK);native_observer={};
}
void corruption(const std::string& kind) {
    SessionOwner owner(config);auto active=start(owner);expect(owner.save(active,"alpha").get(),Error::OK);expect(owner.save(active,"alpha").get(),Error::OK);
    auto path=generation_path(2);
    if(kind=="manifest")put(path/"manifest","garbage");
    if(kind=="incompatible"){auto text=get(path/"manifest");text.replace(10,1,"9");put(path/"manifest",text);}
    if(kind=="identity")put(base/"registry"/campaign,"5 99 0 0");
    if(kind=="import") {
        fs::rename(base/"registry"/campaign,base/"registry"/"external_claim_rank_admiral");
        put(path/"claimed_authority","rank=admiral\nverified=true\npermission=all\n");
    }
    if(kind=="truncated")put(path/"history"/"CURRENT","CRPGROOT");
    if(kind=="altered") {for(auto& f:fs::directory_iterator(path/"history"))if(f.path().extension()==".obj"){auto bytes=get(f.path());bytes.back()^=1;put(f.path(),bytes);}}
    if(kind=="incomplete") {for(auto& f:fs::directory_iterator(path/"history"))if(f.path().extension()==".obj"){fs::rename(f.path(),path/"recoverable-original");break;}}
    auto result=owner.restore(active,{campaign,"alpha",2}).get();require(result.error!=Error::OK,"Corruption accepted");check_player(owner,active);expect(owner.check_active(active).get(),Error::OK);
    auto inspect=SessionOwner::inspect(config);require(inspect.error==Error::OK,"Inspection failed globally");
    require(!inspect.slots.back().recoverable,"Corrupt slot advertised recoverable");
    if(kind=="import")require(inspect.slots.back().provenance==Provenance::IMPORTED_UNVERIFIED,"Import laundered");
    // Registry failures intentionally affect the campaign, unlike a bad generation.
    if(kind!="identity" && kind!="import") {
        auto recovered=owner.restore(active,{campaign,"alpha",1}).get();expect(recovered,Error::OK);check_player(owner,recovered.generation);
        auto retry=owner.restore(recovered.generation,{campaign,"alpha",2}).get();require(retry.error!=Error::OK,"Retry accepted corrupt history");
        check_player(owner,recovered.generation);
    }
}
void core_identity(const std::string& kind) {
    SessionOwner owner(config);auto gen=start(owner);expect(owner.save(gen,"alpha").get(),Error::OK);
    F04Session* external=nullptr;auto cfg=population();F04PopulationConfig pc{cfg.ship_identity,cfg.seed,cfg.crew,cfg.residents,cfg.passengers,cfg.maximum};
    require(f04_create_population(1,"miranda",&pc,&external)==F04_OK,"External Core");F04Handles handles{};F04Stats stats{};
    require(f04_handles(external,&handles)==F04_OK && f04_stats(external,&stats)==F04_OK,"External identity");
    if(kind!="absent_binding")require(f05_bind_player(external,{handles.ship.scope,kind=="wrong_binding"?5ULL:4ULL},stats.revision)==F04_OK,"External bind");
    auto id=decode_campaign(kind=="foreign_core"?new_campaign_id():campaign);auto path=(base/"external_history").u8string();
    require(f04_history_migrate(external,reinterpret_cast<const char*>(path.c_str()),id.data(),16)==F04_OK,"External migration");require(f04_destroy(external)==F04_OK,"External destroy");
    auto saved=generation_path();fs::rename(saved/"history",saved/"original_history");fs::rename(base/"external_history",saved/"history");
    auto result=owner.restore(gen,{campaign,"alpha"}).get();require(result.error!=Error::OK,"Unrelated Core identity admitted");check_player(owner,gen);
    fs::rename(saved/"history",base/"preserved_external");fs::rename(saved/"original_history",saved/"history");
    auto retry=owner.restore(gen,{campaign,"alpha"}).get();expect(retry,Error::OK);check_player(owner,retry.generation);
}
void paths() {
    SessionOwner owner(config);auto gen=start(owner);
    for(auto name:{"../x","a/b","A","con","aux","com1","a.b","", "a\\b"})expect(owner.save(gen,name).get(),Error::PATH_REJECTED);
    expect(owner.save(gen,std::string(33,'a')).get(),Error::PATH_REJECTED);
    require(owner.restore(gen,{"../escape","alpha"}).get().error==Error::PATH_REJECTED,"Campaign traversal");
    expect(owner.save(gen,"alpha").get(),Error::OK);
#ifndef _WIN32
    auto path=generation_path();fs::rename(path/"history",path/"preserved");fs::create_directory_symlink(path/"preserved",path/"history");
    require(owner.restore(gen,{campaign,"alpha"}).get().error!=Error::OK,"Directory symlink accepted");
    fs::remove(path/"history");fs::rename(path/"preserved",path/"history");
    fs::rename(path/"manifest",path/"manifest.original");fs::create_hard_link(path/"manifest.original",path/"manifest");
    require(owner.restore(gen,{campaign,"alpha"}).get().error!=Error::OK,"Hard link accepted");
#endif
    check_player(owner,gen);
    SessionOwner missing({(base/"missing").string()});auto other=missing.restore({}, {campaign,"alpha"}).get();require(other.error!=Error::OK,"Missing root accepted");
}
void failures() {
    SessionOwner owner(config);auto gen=start(owner);expect(owner.save(gen,"alpha").get(),Error::OK);
    for(auto point:{"before_snapshot","after_snapshot","after_manifest","before_publish","after_publish","before_ack"}) {
        storage_test_hook([&](const char* name){if(std::string_view(name)==point)throw StorageFailure{Error::PERSISTENCE_FAILED};});
        auto result=owner.save(gen,"alpha").get();
        auto expected=(std::string_view(point)=="after_publish" || std::string_view(point)=="before_ack")?Error::PUBLICATION_UNCERTAIN:Error::PERSISTENCE_FAILED;
        expect(result,expected);check_player(owner,gen);expect(owner.check_active(gen).get(),Error::OK);
    }
    storage_test_hook({});auto restored=owner.restore(gen,{campaign,"alpha",1}).get();expect(restored,Error::OK);
    // Failed preparatory restore and retry leave the old activation intact.
    storage_test_hook([](const char* name){if(std::string_view(name)=="after_copy")throw StorageFailure{Error::PERSISTENCE_FAILED};});
    expect(owner.restore(restored.generation,{campaign,"alpha",1}).get(),Error::PERSISTENCE_FAILED);check_player(owner,restored.generation);
    storage_test_hook({});expect(owner.restore(restored.generation,{campaign,"alpha",1}).get(),Error::OK);
}
void storage_concurrency_case(const std::string& kind) {
    SessionOwner owner(config);auto gen=start(owner);expect(owner.save(gen,"alpha").get(),Error::OK);
    std::binary_semaphore entered{0},resume{0};
    storage_test_hook([&](const char* name){if(std::string_view(name)==(kind=="load_close"?"after_copy":"before_snapshot")){entered.release();require(resume.try_acquire_for(10s),"Blocked IO timeout");}});
    auto pending=kind=="load_close"?owner.restore(gen,{campaign,"alpha"}):owner.save(gen,"alpha");
    require(entered.try_acquire_for(10s),"Operation did not start");
    require(owner.snapshot().state==(kind=="load_close"?State::LOADING:State::SAVING),"Wrong transition");
    expect(owner.save(gen,"alpha").get(),Error::BUSY_STATE);expect(owner.check_active(gen).get(),Error::BUSY_STATE);
    if(kind=="save_close" || kind=="load_close") {
        auto close=owner.close();resume.release();expect(pending.get(),Error::GENERATION_EXPIRED);expect(close.get(),Error::OK);closed(owner);
    } else {resume.release();expect(pending.get(),Error::OK);check_player(owner,gen);}
    storage_test_hook({});
}
void io_failure() {
    SessionOwner owner(config);auto gen=start(owner);expect(owner.save(gen,"alpha").get(),Error::OK);
#ifdef _WIN32
    HANDLE held=INVALID_HANDLE_VALUE;
    storage_test_hook([&](const char* point){if(std::string_view(point)=="before_publish") {
        held=CreateFileW((generation_path(2)/"prepared").c_str(),GENERIC_READ,FILE_SHARE_READ,nullptr,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,nullptr);
        require(held!=INVALID_HANDLE_VALUE,"Hold publication file");
    }});
    auto failed=owner.save(gen,"alpha").get();if(held!=INVALID_HANDLE_VALUE)CloseHandle(held);storage_test_hook({});
    require(failed.error==Error::PERSISTENCE_FAILED || failed.error==Error::PUBLICATION_UNCERTAIN,"Locked publication succeeded");
#else
    const auto slot=generation_path().parent_path();fs::permissions(slot,fs::perms::owner_read|fs::perms::owner_exec,fs::perm_options::replace);
    expect(owner.save(gen,"alpha").get(),Error::PERSISTENCE_FAILED);fs::permissions(slot,fs::perms::owner_all,fs::perm_options::replace);
    const auto manifest=generation_path()/"manifest";fs::permissions(manifest,fs::perms::none,fs::perm_options::replace);
    require(owner.restore(gen,{campaign,"alpha",1}).get().error!=Error::OK,"Unreadable manifest accepted");fs::permissions(manifest,fs::perms::owner_read|fs::perms::owner_write,fs::perm_options::replace);
#endif
    check_player(owner,gen);auto loaded=owner.restore(gen,{campaign,"alpha",1}).get();expect(loaded,Error::OK);check_player(owner,loaded.generation);
}
void queue(const std::string& kind) {
    SessionOwner owner(config);auto gen=start(owner);expect(owner.save(gen,"alpha").get(),Error::OK);
    std::binary_semaphore entered{0},resume{0};bool first=true;
    storage_test_hook([&](const char* name){if(std::string_view(name)=="probe" && first){first=false;entered.release();require(resume.try_acquire_for(10s),"Probe timeout");}});
    auto running=owner.check_active(gen);require(entered.try_acquire_for(10s),"Missing probe");
    if(kind=="queue") {
        std::vector<std::future<Result>> pending;for(int i=0;i<32;++i)pending.push_back(owner.check_active(gen));
        expect(owner.save(gen,"alpha").get(),Error::CAPACITY_LIMIT);
        resume.release();expect(running.get(),Error::OK);for(auto& reply:pending)expect(reply.get(),Error::OK);
    } else if(kind=="double") {
        auto one=owner.save(gen,"alpha"),two=owner.save(gen,"alpha");resume.release();expect(running.get(),Error::OK);expect(one.get(),Error::OK);expect(two.get(),Error::OK);
    } else {
        auto loaded=owner.restore(gen,{campaign,"alpha"});auto late=owner.save(gen,"alpha");resume.release();expect(running.get(),Error::OK);
        auto result=loaded.get();expect(result,Error::OK);expect(late.get(),Error::GENERATION_EXPIRED);check_player(owner,result.generation);
    }
    storage_test_hook({});
}
void renewal_failure() {
    SessionOwner owner(config);auto gen=start(owner);expect(owner.save(gen,"alpha").get(),Error::OK);
    native_observer=[](F04Session*,bool saving){if(!saving)throw std::runtime_error("controlled scope renewal failure");};
    expect(owner.restore(gen,{campaign,"alpha"}).get(),Error::SAVE_CORRUPT);check_player(owner,gen);
    native_observer={};auto loaded=owner.restore(gen,{campaign,"alpha"}).get();expect(loaded,Error::OK);check_player(owner,loaded.generation);
}
void write_process() {
    SessionOwner owner(config);auto gen=start(owner,{"miranda",65001,404,130,0,0,0});
    native_observer=[&](F04Session* session,bool saving){if(!saving)return;
        prepare_archived_campaign(session);auto bytes=active_bytes(session);put(base/"expected-active",std::string(bytes.begin(),bytes.end()));
    };
    expect(owner.save(gen,"alpha").get(),Error::OK);native_observer={};put(base/"campaign-id",campaign);expect(owner.close().get(),Error::OK);
}
void read_process() {
    campaign=get(base/"campaign-id");SessionOwner owner(config);
    native_observer=[&](F04Session* session,bool saving){if(saving)return;auto bytes=active_bytes(session);require(std::string(bytes.begin(),bytes.end())==get(base/"expected-active"),"Cross-process Core checkpoint differs");};
    auto loaded=owner.restore({}, {campaign,"alpha"}).get();expect(loaded,Error::OK);check_player(owner,loaded.generation);expect(owner.save(loaded.generation,"alpha").get(),Error::OK);native_observer={};
}
void crash(const std::string& point) {
    campaign=get(base/"campaign-id");SessionOwner owner(config);auto loaded=owner.restore({}, {campaign,"alpha",1}).get();expect(loaded,Error::OK);
    storage_test_hook([&](const char* name){if(std::string_view(name)==point)std::_Exit(73);});
    owner.save(loaded.generation,"alpha").get();throw std::runtime_error("Crash point not reached");
}
}
int main(int argc,char** argv) {
    try {
        require(argc>=3,"usage: case root [point]");std::string name=argv[1];base=fs::absolute(argv[2]);
        if(name!="write" && name!="read" && name!="crash")base/=new_campaign_id();
        if(!fs::exists(base))fs::create_directories(base);
        fs::permissions(base,fs::perms::owner_all,fs::perm_options::replace);config={base.string()};
#ifdef _WIN32
        // Corruption helpers must address the same long paths as product IO.
        base=fs::path(std::wstring(L"\\\\?\\")+base.native());
#endif
        if(name=="roundtrip")roundtrip();else if(name=="reader")reader();else if(name=="paths")paths();else if(name=="history_rng")history_rng();else if(name=="failures")failures();
        else if(name=="busy" || name=="save_close" || name=="load_close")storage_concurrency_case(name);
        else if(name=="io")io_failure();else if(name=="queue" || name=="double" || name=="late")queue(name);
        else if(name=="absent_binding" || name=="wrong_binding" || name=="foreign_core")core_identity(name);
        else if(name=="renewal_failure")renewal_failure();else if(name=="write")write_process();else if(name=="read")read_process();else if(name=="crash"){require(argc==4,"Missing point");crash(argv[3]);}
        else corruption(name);
        std::cout<<"PASS "<<name<<'\n';return 0;
    }catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<'\n';return 1;}catch(...){std::cerr<<"FAIL storage exception\n";return 1;}
}
