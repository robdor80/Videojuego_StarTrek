#include "test_support.h"
#include "player_bootstrap.h"
#include "gateway_test_access.h"
#include "f05_player_binding.h"
#include "slot_store.h"
#include <corerpg/campaign_persistence.hpp>
#include <atomic>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <semaphore>
#include <sstream>
#include <thread>
#include <type_traits>

using namespace test;
using namespace std::chrono_literals;
namespace fs = std::filesystem;
namespace {
using U = std::uint64_t;
std::atomic_bool pause_dispatch{false};
std::atomic_uint forced_code{F04_OK};
std::binary_semaphore entered{0}, resume{0};
void wait_pause() noexcept {
    entered.release();
    if (!resume.try_acquire_for(15s)) std::terminate();
}
void await_pause() { require(entered.try_acquire_for(15s),"Owner did not reach controlled pause"); }
void check_code(unsigned got, unsigned expected, const char* message) {
    if (got != expected) throw std::runtime_error(std::string(message)+" code="+std::to_string(got)+" expected="+std::to_string(expected));
}
void operation_error(const OperationResult& r, Error error, U correlation = 0) {
    require(r.error == error,"Unexpected gateway status");
    require(r.correlation_id == correlation,"Lost correlation");
    if (error != Error::OK) require(r.generation == Generation{} && !r.campaign && !r.order && !r.receipt,"Failure leaked projection");
}
void put(const fs::path& path, const std::string& value) {
    std::ofstream out(path,std::ios::binary); out << value; require(bool(out),"Write evidence");
}
std::string get(const fs::path& path) {
    std::ifstream in(path,std::ios::binary); require(bool(in),"Read evidence"); return {std::istreambuf_iterator<char>(in),{}};
}
std::vector<std::uint8_t> active(F04Session* s) {
    U size = 0;
    auto export_bytes = f04_save;
    auto code = export_bytes(s,nullptr,0,&size);
    if (code == F04_SAVE) { export_bytes = f04_history_export_active; code = export_bytes(s,nullptr,0,&size); }
    check_code(code,F04_CAPACITY,"Diagnostic size");
    std::vector<std::uint8_t> bytes(size);
    check_code(export_bytes(s,bytes.data(),size,&size),F04_OK,"Diagnostic export"); return bytes;
}
std::string bytes_text(const std::vector<std::uint8_t>& bytes) { return {bytes.begin(),bytes.end()}; }

// Compile-time client boundary: no issuer, actor, scope, raw session or receiver API.
template<class T> concept HasActor = requires(T t) { t.actor; };
template<class T> concept HasIssuer = requires(T t) { t.issuer; };
template<class T> concept CanReceive = requires(T& t, Generation g) { t.receive_order(g, U{}, U{}); };
template<class T> concept CanAccessCore = requires(T& t) { t.session(); };
static_assert(!HasActor<OrderIntent> && !HasIssuer<OrderIntent>);
static_assert(!CanReceive<SessionOwner> && !CanAccessCore<SessionOwner>);

struct Fixture {
    StorageConfig storage;
    SessionOwner owner;
    Generation generation;
    U captain = 0, recipient = 0, station = 0;
    std::string campaign;

    explicit Fixture(const fs::path& root, bool bind = true, U person = 3)
        : storage{root.string()},owner(storage) {
        const auto opened = owner.open({"miranda",65001,404,130,0,0,0}).get();
        expect(opened,Error::OK); generation = opened.generation; campaign = owner.campaign_id(generation);
        visit([&](F04Session* s) {
            F04Handles h{}; check_code(f04_handles(s,&h),F04_OK,"Fixture handles"); captain = h.captain.id;
            auto op = [&](F04Ref actor,unsigned kind,U target=0,U aux=0,U begin=0,U end=0,unsigned value=0) {
                F04Stats stats{}; check_code(f04_stats(s,&stats),F04_OK,"Fixture revision");
                F04Request q{actor,stats.revision,kind,value,target,aux,begin,end,50501}; F04Result r{};
                check_code(f04_execute(s,&q,&r),F04_OK,"Fixture operation");
            };
            op(h.captain,F04_INSTALL_TEMPLATE,0,F04_SUTHERLAND_EQUIPMENT,0,0,F04_SUTHERLAND_SCIENCE);
            op(h.captain,F04_BOOTSTRAP_TEMPLATE);
            op(h.captain,F04_PLAN_ALPHA,0,0,28800,57600);
            U processed=0; check_code(f04_advance(s,28800,4096,&processed),F04_OK,"Fixture clock");
            F04Position positions[130]{}; U count=0,total=0;
            check_code(f04_positions_page(s,h.captain,0,positions,130,&count,&total),F04_OK,"Fixture positions");
            for (U i=0;i<count;++i) if (positions[i].person && positions[i].qualification==F04_SENSORS && positions[i].on_duty) {
                recipient=positions[i].person; station=positions[i].id; break;
            }
            require(recipient && station && recipient!=captain,"No distinct real recipient");
            op({h.ship.scope,recipient},F04_MOVE,station);
        });
        if (bind) bind_person(person);
    }
    void visit(std::function<void(F04Session*)> f) {
        expect(GatewayTestAccess::visit(owner,generation,std::move(f)).get(),Error::OK);
    }
    void bind_person(U person) {
        auto selected=PlayerBootstrap::prepare(owner,generation,person).get();
        require(selected.error==Error::OK && selected.selection,"Prepare legitimate person");
        require(PlayerBootstrap::bind(owner,generation,*selected.selection,selected.revision).get().error==Error::OK,"Bind legitimate person");
    }
    CampaignView view() {
        auto r=owner.query_view(generation).get(); operation_error(r,Error::OK);
        require(r.campaign && r.campaign->generation==generation,"Missing campaign view"); return *r.campaign;
    }
    OrderIntent intent(U key=7001) { return {recipient,station,key,view().revision,28900,50501,F04_SCAN}; }
    OrderReceipt submit(OrderIntent q) {
        auto r=owner.submit_order(generation,q,17).get(); operation_error(r,Error::OK,17);
        require(r.receipt && r.receipt->order,"Missing F05 receipt"); return *r.receipt;
    }
    OrderView order(U id) {
        auto r=owner.query_order(generation,id).get(); operation_error(r,Error::OK);
        require(r.order && r.order->generation==generation,"Missing order view"); return *r.order;
    }
    std::vector<std::uint8_t> bytes() {
        std::vector<std::uint8_t> out; visit([&](F04Session* s) {out=active(s);}); return out;
    }
    F05Receipt transition(U order,bool execute,U actor=0,unsigned expected=F04_OK) {
        F05Receipt out{};
        visit([&](F04Session* s) {
            F04Handles h{}; F04Stats stats{};
            check_code(f04_handles(s,&h),F04_OK,"Recipient scope"); check_code(f04_stats(s,&stats),F04_OK,"Recipient revision");
            F04Ref who{h.ship.scope,actor?actor:recipient};
            const auto before=active(s);
            auto code=execute?f05_execute_order(s,who,stats.revision,order,&out):f05_receive(s,who,stats.revision,order,&out);
            check_code(code,expected,"Recipient transition");
            if (expected==F04_DENIED) require(active(s)==before,"Wrong recipient mutated Core");
        }); return out;
    }
    void complete(U order) {
        const auto initial=corerpg::CampaignPersistence::deserialize(bytes());
        auto accepted=transition(order,false); require(accepted.state==F05_ACCEPTED && accepted.task && !accepted.result,"Reception performed action");
        auto done=transition(order,true); require(done.state==F05_COMPLETED && done.result && done.attempt,"Core execution missing");
        auto v=this->order(order); require(v.execution && v.execution->performed && v.execution->consumed_random &&
            v.execution->executor==recipient && v.execution->core_revision_after==v.execution->core_revision_before &&
            v.execution->core_outcome==unsigned(corerpg::ActionOutcome::accepted) && !v.execution->core_rejection &&
            v.execution->value>=1 && v.execution->value<=100,"Not a genuine Core RNG result");
        const auto final=corerpg::CampaignPersistence::deserialize(bytes());
        require(initial.snapshot && final.snapshot && initial.snapshot->campaign.streams!=final.snapshot->campaign.streams,
            "Core execution did not consume its persisted RNG stream");
        visit([&](F04Session* s) {
            F04Handles h{}; check_code(f04_handles(s,&h),F04_OK,"Events observer");
            F05EventView events[8]{}; U n=0; unsigned more=0;
            check_code(f05_events_page(s,h.captain,order,0,events,8,&n,&more),F04_OK,"Core event chain");
            require(n==4 && !more,"Expected issued/accepted/executing/completed");
            require(events[0].actor==captain && events[1].actor==recipient && events[2].actor==recipient &&
                events[3].actor==recipient && events[3].result==done.result,"Wrong causal actors/result");
            for(U i=1;i<n;++i) require(events[i].previous==events[i-1].id,"Broken Core event chain");
            std::cout<<"Core order="<<order<<" attempt="<<done.attempt<<" result="<<done.result<<" terminal_event="<<done.event<<" revision="<<done.revision
                <<" stream="<<v.execution->stream<<" value="<<v.execution->value<<" consumed_random="<<v.execution->consumed_random<<'\n';
        });
    }
};

void replay(Fixture& f) {
    auto q=f.intent(8001); auto issued=f.submit(q); f.complete(issued.order); const auto before=f.bytes();
    auto repeat=f.owner.submit_order(f.generation,q,990).get(); operation_error(repeat,Error::OK,990);
    require(repeat.receipt && repeat.receipt->order==issued.order,"Correlation replaced domain key");
    f.transition(issued.order,true); require(f.bytes()==before,"Replay created effect/event/RNG");
}
void refusal(Fixture& f,const std::string& name) {
    auto q=f.intent(); auto before=f.bytes();
    if(name=="scope") q.station=1;
    if(name=="stale") --q.expected_revision;
    if(name=="unsupported") q.operation=F04_BRIDGE;
    const auto error=name=="scope"?Error::SCOPE_INVALID:name=="stale"?Error::REVISION_STALE:
        name=="authority"?Error::ACCESS_DENIED:Error::DOMAIN_REJECTED;
    auto r=f.owner.submit_order(f.generation,q).get(); operation_error(r,error);
    if(name=="scope") require(f.bytes()==before,"Atomic scope rejection mutated Core");
    else {
        // F05 intentionally persists an audited refusal, not a partial scan.
        const unsigned expected=name=="stale"?unsigned(F04_STALE):name=="authority"?unsigned(F04_DENIED):unsigned(F05_UNSUPPORTED);
        f.visit([&](F04Session* s) {
            F04Handles h{};check_code(f04_handles(s,&h),F04_OK,"Refusal scope");
            F05OrderRequest request{{h.ship.scope,f.owner.current_player(f.generation).player->person_id},
                {h.ship.scope,q.recipient},h.ship,{h.ship.scope,q.station},q.key,q.expected_revision,q.deadline,q.cause,q.operation,0};
            const auto refused=active(s); F05Receipt receipt{};
            check_code(f05_submit(s,&request,&receipt),expected,"Refusal replay");
            require(receipt.state==F05_REFUSED && !receipt.task && !receipt.attempt && !receipt.result && active(s)==refused,"Refused order performed work");
            std::cout<<"Audited refusal code="<<expected<<" order="<<receipt.order<<" no task/attempt/result\n";
        });
        auto initial=corerpg::CampaignPersistence::deserialize(before);
        auto refused=corerpg::CampaignPersistence::deserialize(f.bytes());
        require(initial.snapshot && refused.snapshot && initial.snapshot->campaign.streams==refused.snapshot->campaign.streams &&
            initial.snapshot->campaign.master_seed==refused.snapshot->campaign.master_seed &&
            initial.snapshot->timeline.now==refused.snapshot->timeline.now,"Refusal consumed RNG or advanced clock");
    }
}

void run_case(const std::string& name,const fs::path& root) {
    Fixture f(root,name!="unbound",(name=="authority" || name=="observer")?4:3);
    if(name=="bound") {
        auto v=f.view(); require(v.person==f.captain && v.ship==1,"Projection uses wrong person");
    } else if(name=="readonly") {
        const auto before=f.bytes(); auto a=f.view(), b=f.view();
        require(a.revision==b.revision && a.now==b.now && f.bytes()==before,"Read changed Core/RNG/clock");
    } else if(name=="submit") {
        auto receipt=f.submit(f.intent()); require(receipt.state==F05_ISSUED && !receipt.task && !receipt.result,"Submit falsely executed");
        auto before=f.bytes(); auto v=f.order(receipt.order); require(v.issuer==f.captain && v.recipient==f.recipient && !v.execution && f.bytes()==before,"Pending projection mutated");
    } else if(name=="execute") { f.complete(f.submit(f.intent()).order); }
    else if(name=="replay") replay(f);
    else if(name=="conflict") {
        auto q=f.intent();f.submit(q);auto before=f.bytes();++q.cause;
        operation_error(f.owner.submit_order(f.generation,q).get(),Error::IDEMPOTENCY_CONFLICT);
        require(f.bytes()==before,"Conflict mutated Core");
    } else if(name=="scope" || name=="stale" || name=="authority" || name=="unsupported") refusal(f,name);
    else if(name=="unbound") {
        auto before=f.bytes(); operation_error(f.owner.query_view(f.generation).get(),Error::PRINCIPAL_UNBOUND);
        operation_error(f.owner.submit_order(f.generation,{}).get(),Error::PRINCIPAL_UNBOUND);
        require(f.bytes()==before,"Unbound auto-bound or mutated");
    } else if(name=="recipient") {
        auto receipt=f.submit(f.intent());f.transition(receipt.order,false,f.captain,F04_DENIED);
        f.transition(receipt.order,true,f.captain,F04_DENIED); f.complete(receipt.order);
    } else if(name=="expired") {
        auto q=f.intent();auto old=f.generation;expect(f.owner.close().get(),Error::OK);
        operation_error(f.owner.submit_order(old,q,9).get(),Error::GENERATION_EXPIRED,9);
        f.generation=f.owner.open(population()).get().generation;
        operation_error(f.owner.query_view(old).get(),Error::GENERATION_EXPIRED);
    } else if(name=="institutional") {
        auto before=f.bytes();operation_error(f.owner.institutional_command(f.generation).get(),Error::SERVICE_UNAVAILABLE);
        require(f.bytes()==before,"Institutional operation mutated");
    } else if(name=="observer") {
        // Bind cannot switch observer. A Core-only fixture order by captain to
        // another recipient must not be visible to unrelated bound crew member.
        U order=0;
        f.visit([&](F04Session* s) {
            F04Handles h{}; F04Stats stats{};F05Receipt r{};
            check_code(f04_handles(s,&h),F04_OK,"Private fixture scope");check_code(f04_stats(s,&stats),F04_OK,"Private fixture revision");
            F05OrderRequest q{h.captain,{h.ship.scope,f.recipient},h.ship,{h.ship.scope,f.station},7001,stats.revision,28900,50501,F04_SCAN,0};
            check_code(f05_submit(s,&q,&r),F04_OK,"Private fixture issuer");order=r.order;
        });
        auto before=f.bytes();
        operation_error(f.owner.query_order(f.generation,order).get(),Error::ACCESS_DENIED);
        auto selected=PlayerBootstrap::prepare(f.owner,f.generation,3).get();
        require(PlayerBootstrap::bind(f.owner,f.generation,*selected.selection,selected.revision).get().error==Error::IDEMPOTENCY_CONFLICT,"Observer switched");
        require(f.view().person==4 && f.bytes()==before,"Observer conflict leaked/mutated");
        f.visit([&](F04Session* s) {
            F04Handles h{}; check_code(f04_handles(s,&h),F04_OK,"Observer scope"); F05OrderView out{};
            check_code(f05_order(s,{h.ship.scope,4},order,&out),F04_DENIED,"Foreign observer");
            require(!out.receipt.order,"Denied F05 projection exposed order");
        });
    } else if(name=="unknown") {
        auto before=f.bytes();forced_code=49151;
        operation_error(f.owner.query_view(f.generation).get(),Error::DOMAIN_REJECTED);
        forced_code=F04_OK;require(f.bytes()==before,"Unknown error changed Core");
    } else if(name=="cancel") {
        auto r=f.submit(f.intent());auto reply=f.owner.cancel_order(f.generation,r.order,f.view().revision).get();
        operation_error(reply,Error::OK);require(reply.receipt && reply.receipt->state==F05_CANCELLED,"Cancel not delegated");
        auto before=f.bytes();require(!f.order(r.order).execution,"Cancel invented execution");require(f.bytes()==before,"Read changed cancellation");
    } else if(name=="concurrent") {
        auto q=f.intent();auto a=f.owner.submit_order(f.generation,q,1);auto b=f.owner.submit_order(f.generation,q,2);
        auto first=a.get(), second=b.get(); operation_error(first,Error::OK,1);operation_error(second,Error::OK,2);
        require(first.receipt->order==second.receipt->order,"Concurrent same key duplicated order");
        f.complete(first.receipt->order);
    } else if(name=="saving" || name=="loading") {
        expect(f.owner.save(f.generation,"alpha").get(),Error::OK);
        auto q=f.intent();
        trek::host::detail::storage_test_hook([&](const char* point) {
            if(std::string_view(point)==(name=="saving"?"before_snapshot":"after_copy"))wait_pause();
        });
        auto running=name=="saving"?f.owner.save(f.generation,"alpha"):f.owner.restore(f.generation,{f.campaign,"alpha"});
        await_pause();require(f.owner.snapshot().state==(name=="saving"?State::SAVING:State::LOADING),"Missing transitional state");
        operation_error(f.owner.query_view(f.generation,16).get(),Error::BUSY_STATE,16);
        operation_error(f.owner.submit_order(f.generation,q).get(),Error::BUSY_STATE);
        resume.release();auto done=running.get();expect(done,Error::OK);f.generation=done.generation;
        trek::host::detail::storage_test_hook({});
    } else if(name=="save_order" || name=="close_order") {
        auto q=f.intent();pause_dispatch=true;auto running=f.owner.submit_order(f.generation,q,81);await_pause();
        auto queued=f.owner.query_view(f.generation,82);
        if(name=="close_order") {
            auto close=f.owner.close();operation_error(queued.get(),Error::GENERATION_EXPIRED,82);
            pause_dispatch=false;resume.release();operation_error(running.get(),Error::GENERATION_EXPIRED,81);expect(close.get(),Error::OK);
        } else {
            auto save=f.owner.save(f.generation,"alpha");require(save.wait_for(0ms)==std::future_status::timeout,"SAVE overlapped Core dispatch");
            pause_dispatch=false;resume.release();auto issued=running.get();operation_error(issued,Error::OK,81);operation_error(queued.get(),Error::OK,82);
            expect(save.get(),Error::OK);auto loaded=f.owner.restore(f.generation,{f.campaign,"alpha"}).get();expect(loaded,Error::OK);
            f.generation=loaded.generation;require(f.order(issued.receipt->order).receipt.state==F05_ISSUED,"SAVE stored partial order");
        }
    } else if(name=="recover" || name=="pending") {
        auto q=f.intent();auto issued=f.submit(q);if(name=="recover")f.complete(issued.order);
        const auto before=f.bytes();expect(f.owner.save(f.generation,"alpha").get(),Error::OK);
        expect(f.owner.restore(f.generation,{f.campaign,"absent"}).get(),Error::PATH_REJECTED);
        require(f.bytes()==before,"Failed LOAD damaged healthy Core");
        auto old=f.generation;auto loaded=f.owner.restore(old,{f.campaign,"alpha"}).get();expect(loaded,Error::OK);f.generation=loaded.generation;
        operation_error(f.owner.query_order(old,issued.order).get(),Error::GENERATION_EXPIRED);
        require(f.bytes()==before,"LOAD changed facts/RNG/revision");
        if(name=="pending") f.complete(issued.order);
        else { require(f.order(issued.order).execution.has_value(),"Lost result");replay(f); }
        expect(f.owner.save(f.generation,"alpha").get(),Error::OK);
    } else throw std::runtime_error("Unknown M0 case");
}

void writer(const fs::path& root,bool pending) {
    Fixture f(root);auto fresh=f.bytes();
    auto start=std::chrono::steady_clock::now();expect(f.owner.save(f.generation,"alpha").get(),Error::OK);
    auto first=std::chrono::steady_clock::now();require(f.bytes()==fresh,"SAVE mutated initial campaign");
    auto q=f.intent();auto issued=f.submit(q);if(!pending)f.complete(issued.order);
    auto expected=f.bytes();auto second_start=std::chrono::steady_clock::now();expect(f.owner.save(f.generation,"alpha").get(),Error::OK);
    auto second=std::chrono::steady_clock::now();expect(f.owner.save(f.generation,"alpha").get(),Error::OK);
    auto third=std::chrono::steady_clock::now();require(f.bytes()==expected,"SAVE mutated played campaign");
    put(root/"expected-active",bytes_text(expected));
    put(root/"campaign-id",f.campaign);
    std::ostringstream fields;fields<<issued.order<<' '<<q.recipient<<' '<<q.station<<' '<<q.key<<' '<<q.expected_revision<<' '<<q.deadline<<' '<<q.cause<<' '<<q.operation;
    put(root/"request",fields.str());
    std::cout<<"SAVE durations_us="<<std::chrono::duration_cast<std::chrono::microseconds>(first-start).count()<<','
        <<std::chrono::duration_cast<std::chrono::microseconds>(second-second_start).count()<<','<<std::chrono::duration_cast<std::chrono::microseconds>(third-second).count()<<'\n';
    expect(f.owner.close().get(),Error::OK);
    operation_error(f.owner.query_view(f.generation).get(),Error::GENERATION_EXPIRED);
}
void reader(const fs::path& root,bool pending) {
    StorageConfig storage{root.string()};SessionOwner owner(storage);const auto campaign=get(root/"campaign-id");
    U id=0;OrderIntent q{};std::istringstream fields(get(root/"request"));
    fields>>id>>q.recipient>>q.station>>q.key>>q.expected_revision>>q.deadline>>q.cause>>q.operation;require(bool(fields),"Read original intent");
    auto start=std::chrono::steady_clock::now();auto restored=owner.restore({}, {campaign,"alpha"}).get();expect(restored,Error::OK);
    auto generation=restored.generation;
    std::cout<<"RESTORE duration_us="<<std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::steady_clock::now()-start).count()<<'\n';
    require(owner.campaign_id(generation)==campaign && owner.current_player(generation).player->person_id==3,"Restored wrong identity/campaign");
    auto inspect=[&](const std::function<void(F04Session*)>& check) {expect(GatewayTestAccess::visit(owner,generation,check).get(),Error::OK);};
    inspect([&](F04Session* s) {require(bytes_text(active(s))==get(root/"expected-active"),"Cross-process facts/clock/RNG/identity/revision mismatch");});
    auto view=owner.query_order(generation,id).get();operation_error(view,Error::OK);
    require(view.order && view.order->receipt.state==(pending?F05_ISSUED:F05_COMPLETED),"Cross-process order state");
    if(!pending)require(view.order->execution && view.order->execution->performed && view.order->execution->consumed_random,"Cross-process Core result missing");
    auto replay=owner.submit_order(generation,q,123).get();operation_error(replay,Error::OK,123);require(replay.receipt->order==id,"Cross-process key replay duplicated order");
    inspect([&](F04Session* s) {require(bytes_text(active(s))==get(root/"expected-active"),"Cross-process replay mutated Core");});
    if(!pending) inspect([&](F04Session* s) {
        F04Handles h{};F04Stats stats{};F05Receipt r{};
        check_code(f04_handles(s,&h),F04_OK,"Terminal recipient scope");check_code(f04_stats(s,&stats),F04_OK,"Terminal revision");
        check_code(f05_execute_order(s,{h.ship.scope,q.recipient},stats.revision,id,&r),F04_OK,"Terminal replay after RESTORE");
        require(bytes_text(active(s))==get(root/"expected-active"),"Terminal execution replay consumed RNG after RESTORE");
    });
    auto old=generation;auto again=owner.restore(generation,{campaign,"alpha"}).get();expect(again,Error::OK);generation=again.generation;
    require(old!=generation,"LOAD reused old generation");operation_error(owner.submit_order(old,q).get(),Error::GENERATION_EXPIRED);
    if(pending) inspect([&](F04Session* s) {
        F04Handles h{};F04Stats stats{};F05Receipt r{};check_code(f04_handles(s,&h),F04_OK,"Restored recipient scope");
        check_code(f04_stats(s,&stats),F04_OK,"Restored revision");check_code(f05_receive(s,{h.ship.scope,q.recipient},stats.revision,id,&r),F04_OK,"Receive restored pending");
        check_code(f04_stats(s,&stats),F04_OK,"Execution revision");check_code(f05_execute_order(s,{h.ship.scope,q.recipient},stats.revision,id,&r),F04_OK,"Execute restored pending");
        require(r.state==F05_COMPLETED && r.result,"Restored pending failed to complete");
    });
    expect(owner.save(generation,"alpha").get(),Error::OK);
}
}
namespace trek::host::detail {
void persistence_test_observe(F04Session*,bool) {}
void gateway_test_after_dispatch(F04Session*,std::uint32_t& code) {
    if(forced_code!=F04_OK)code=forced_code;
    if(pause_dispatch)wait_pause();
}
}
int main(int argc,char** argv) {
    try {
        require(argc==3,"Usage: case root");std::string name=argv[1];auto root=fs::absolute(argv[2]);
        if(name!="write" && name!="read" && name!="write_pending" && name!="read_pending")root/=trek::host::detail::new_campaign_id();
        fs::create_directories(root);fs::permissions(root,fs::perms::owner_all,fs::perm_options::replace);
        if(name=="write" || name=="write_pending")writer(root,name=="write_pending");
        else if(name=="read" || name=="read_pending")reader(root,name=="read_pending");
        else run_case(name,root);
        std::cout<<"PASS "<<name<<'\n';return 0;
    }catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<'\n';return 1;}
}
