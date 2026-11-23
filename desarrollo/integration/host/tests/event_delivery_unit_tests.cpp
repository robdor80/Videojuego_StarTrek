#include "event_delivery.h"

#include <iostream>
#include <stdexcept>
#include <string>
#include <cstdint>

using trek::host::EventNotice;
using trek::host::EventSource;
using trek::host::detail::EventDelivery;

namespace {
void require(bool ok, const char* why)
{
    if (!ok) throw std::runtime_error(why);
}
EventNotice notice(std::uint64_t id, std::uint64_t previous, std::uint64_t order=45)
{
    return {EventSource::F05_ORDER,id,previous,order,5000,3,0};
}
void run(const std::string& name)
{
    EventDelivery delivery;
    const auto token=delivery.subscribe(45);
    auto* sub=delivery.find(token);
    require(sub && sub->order==45 && sub->pending.empty(),"Subscription missing");
    const EventNotice valid[]={notice(7,0),notice(8,7),notice(9,8)};
    if(name=="causal") {
        require(EventDelivery::append(*sub,valid,3,false),"Valid Core order rejected");
        require(sub->cursor==9 && sub->pending.size()==3,"Queue did not commit source page");
        require(EventDelivery::ack(*sub,8),"In-order cumulative ack failed");
        require(sub->pending.size()==1 && sub->pending.front().id==9,"Ack retained stale item");
        require(EventDelivery::ack(*sub,8),"Repeated UI ack not idempotent");
        require(EventDelivery::ack(*sub,9) && sub->pending.empty(),"Final ack failed");
    } else if(name=="invalid_gap") {
        EventNotice broken[]={notice(7,0),notice(9,7),notice(10,6)};
        require(!EventDelivery::append(*sub,broken,3,false),"Source gap accepted");
        require(sub->pending.empty() && sub->cursor==0,"Partial page leaked");
        require(EventDelivery::append(*sub,valid,3,false),"Valid page after gap failed");
    } else if(name=="wrong_order") {
        EventNotice foreign[]={notice(7,0,700)};
        require(!EventDelivery::append(*sub,foreign,1,false),"Wrong source order accepted");
        require(sub->cursor==0 && sub->pending.empty(),"Foreign event mutated queue");
    } else if(name=="empty_more") {
        require(!EventDelivery::append(*sub,nullptr,0,true),"Empty source MORE accepted");
        require(sub->pending.empty(),"Empty page populated queue");
    } else if(name=="invalid_ack") {
        require(EventDelivery::append(*sub,valid,3,false),"Valid Core page rejected");
        require(!EventDelivery::ack(*sub,11) && !EventDelivery::ack(*sub,0),
                "UI acked an unseen/invalid event");
        require(sub->pending.size()==3,"Invalid ack dropped Core event");
    } else if(name=="bounded") {
        for(std::size_t i=1;i<EventDelivery::max_subscriptions;++i)
            require(delivery.subscribe(45)!=0,"Max subscription less than limit");
        require(!delivery.has_capacity() && delivery.subscribe(45)==0,
                "Unbounded subscriber list");
    } else if(name=="invalidate") {
        require(EventDelivery::append(*sub,valid,3,false),"Valid page rejected");
        delivery.invalidate();
        require(delivery.find(token)==nullptr,"Invalidation left old observer mailbox");
        const auto next=delivery.subscribe(45);
        require(next && next!=token,"Reused old session token");
    } else if(name=="read_only") {
        require(!EventDelivery::append(*sub,valid,EventDelivery::page_capacity+1,false),
                "Oversize source page admitted");
        require(sub->pending.empty() && !sub->cursor,"Oversize page mutated queue");
    } else throw std::runtime_error("Unknown H08 unit case");
}
} // namespace

int main(int argc,char** argv)
{
    try {
        require(argc==2,"Usage: event_delivery_unit_tests case");
        run(argv[1]);
        std::cout<<"PASS H08-P02 "<<argv[1]<<'\n';
        return 0;
    } catch(const std::exception& e) {
        std::cerr<<"FAIL H08-P02 "<<e.what()<<'\n';
        return 1;
    }
}
