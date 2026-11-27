#include "notification_projection.h"

#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <string_view>

namespace {
using namespace trek::host;
using trek::host::detail::NotificationProjection;

void require(bool condition, const char* error) {
    if (!condition) throw std::runtime_error(error);
}
EventNotice make(std::uint32_t state, std::uint64_t id=42,
                 std::uint64_t previous=0, std::uint64_t order=20) {
    return {EventSource::F05_ORDER,id,previous,order,1000,state,0};
}
void run(std::string_view name) {
    if(name=="states") {
        struct Expected { std::uint32_t state; NotificationKind kind; NotificationLevel level; };
        constexpr std::array<Expected,7> cases{{
            {F05_ISSUED,NotificationKind::ORDER_ISSUED,NotificationLevel::INFO},
            {F05_ACCEPTED,NotificationKind::ORDER_ACCEPTED,NotificationLevel::INFO},
            {F05_EXECUTING,NotificationKind::ORDER_EXECUTING,NotificationLevel::INFO},
            {F05_COMPLETED,NotificationKind::ORDER_COMPLETED,NotificationLevel::SUCCESS},
            {F05_FAILED,NotificationKind::ORDER_FAILED,NotificationLevel::ERROR},
            {F05_REFUSED,NotificationKind::ORDER_REFUSED,NotificationLevel::WARNING},
            {F05_CANCELLED,NotificationKind::ORDER_CANCELLED,NotificationLevel::WARNING},
        }};
        for(const auto& c:cases) {
            auto mapped=NotificationProjection::format_event(make(c.state));
            require(mapped.has_value(),"Known F05 state omitted");
            require(mapped->kind==c.kind && mapped->level==c.level &&
                    mapped->source_event_id==42 && mapped->order==20 &&
                    !mapped->title.empty() && !mapped->body.empty(),
                    "Known F05 state mapped incorrectly");
        }
    } else if(name=="unknown") {
        require(!NotificationProjection::format_event(make(9999)),
                "Unknown F05 state became invented notification");
    } else if(name=="foreign") {
        auto event=make(F05_COMPLETED);
        event.source=static_cast<EventSource>(999);
        require(!NotificationProjection::format_event(event),
                "Unknown source presented as F05");
    } else if(name=="malformed") {
        require(!NotificationProjection::format_event(make(F05_ISSUED,0)),
                "Missing source event ID accepted");
        require(!NotificationProjection::format_event(make(F05_ISSUED,42,0,0)),
                "Missing Core order ID accepted");
    } else if(name=="metadata") {
        auto event=make(F05_ACCEPTED,1001,999,904);
        event.tick=123456;
        auto mapped=NotificationProjection::format_event(event);
        require(mapped && mapped->previous_event_id==999 &&
                mapped->core_tick==123456 && mapped->source_event_id==1001 &&
                mapped->order==904,"Changed Core event metadata or invented wall time");
    } else if(name=="idempotent") {
        auto a=NotificationProjection::format_event(make(F05_COMPLETED));
        auto b=NotificationProjection::format_event(make(F05_COMPLETED));
        require(a && b && *a==*b,"Repeated formatter generated different result");
    } else if(name=="private") {
        const auto item=NotificationProjection::format_event(make(F05_FAILED,65112,0,91888));
        require(item && item->body.find("91888")==std::string::npos &&
                item->body.find("65112")==std::string::npos &&
                item->body.find("cause")==std::string::npos,
                "Formatter leaked identifiers or private cause into message");
    } else if(name=="access_denied") {
        EventBatchResult source;
        source.error=Error::ACCESS_DENIED;
        source.events={make(F05_COMPLETED)};
        auto out=NotificationProjection::from_authorized_f05(
            source,"0123456789abcdef0123456789abcdef");
        require(out.error==Error::ACCESS_DENIED && out.items.empty() &&
                out.campaign_id.empty() && !out.resync_required,
                "Denied source leaked presentation");
    } else if(name=="resync") {
        EventBatchResult source;
        source.error=Error::OK;
        source.resync_required=true;
        source.subscription=9;
        source.events={make(F05_COMPLETED)};
        auto out=NotificationProjection::from_authorized_f05(
            source,"0123456789abcdef0123456789abcdef");
        require(out.error==Error::OK && out.resync_required && out.items.empty() &&
                out.campaign_id.empty() && out.subscription==9,
                "RESYNC became a synthetic game event");
    } else if(name=="untrusted") {
        EventBatchResult source;
        source.subscription=9;
        source.events={make(F05_COMPLETED)};
        auto out=NotificationProjection::from_authorized_f05(source,"fake");
        require(out.error==Error::INTERNAL_ERROR && out.items.empty() &&
                out.campaign_id.empty() && out.subscription==0,
                "Untrusted source fabricated an authorized batch");
    } else throw std::runtime_error("Unknown projection unit test");
}
}

int main(int argc,char** argv) {
    try {
        require(argc==2,"Usage: notification_projection_unit_tests case");
        run(argv[1]);
        std::cout<<"PASS H08-P04 "<<argv[1]<<'\n';
        return 0;
    } catch(const std::exception& e) {
        std::cerr<<"FAIL H08-P04 "<<e.what()<<'\n';
        return 1;
    }
}
