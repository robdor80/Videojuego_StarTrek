#include "native_session.h"
#include "f05_player_binding.h"

namespace trek::host::detail::bridge {
namespace {
OrderReceipt receipt(const F05Receipt& r)
{
    return {r.request,r.order,r.task,r.attempt,r.result,r.event,r.revision,r.state,r.code};
}
}

std::uint32_t dispatch(F04Session* session, F04Ref player, const GatewayRequest& q, OperationResult& out) noexcept
{
    out = {};
    F05PlayerBinding binding{};
    auto code = f05_player_binding(session, &binding);
    if (code != F04_OK) return code;
    if (!binding.record || binding.person.id != player.id || binding.person.scope != player.scope) return F04_DENIED;
    F04Person person{};
    code = f04_person(session, binding.person, binding.person.id, &person);
    if (code != F04_OK) return code;
    F04Stats stats{};
    code = f04_stats(session, &stats);
    if (code != F04_OK) return code;
    F04Handles handles{};
    code = f04_handles(session, &handles);
    if (code != F04_OK) return code;

    switch (q.operation) {
    case GatewayOp::VIEW:
        out.campaign = CampaignView{{},stats.revision,stats.now,person.id,handles.ship.id};
        return F04_OK;
    case GatewayOp::SUBMIT: {
        // Resolve issuer and scopes here; the caller supplies only campaign IDs.
        const auto& i = q.intent;
        const F05OrderRequest request{binding.person,{handles.ship.scope,i.recipient},handles.ship,
            {handles.ship.scope,i.station},i.key,i.expected_revision,i.deadline,i.cause,i.operation,0};
        F05Receipt r{};
        code = f05_submit(session, &request, &r);
        if (code == F04_OK) out.receipt = receipt(r);
        return code;
    }
    case GatewayOp::CANCEL: {
        F05Receipt r{};
        code = f05_cancel(session, binding.person, q.revision, q.order, &r);
        if (code == F04_OK) out.receipt = receipt(r);
        return code;
    }
    case GatewayOp::ORDER: {
        F05OrderView v{};
        code = f05_order(session, binding.person, q.order, &v);
        if (code != F04_OK) return code;
        OrderView view{{},receipt(v.receipt),v.issuer,v.recipient,v.ship,v.station,
            v.key,v.deadline,v.cause,v.input_revision,v.operation,{}};
        // A pending/cancelled/refused order has no execution result. Query only
        // when Core's receipt says there is one; never hide an unexpected error.
        if (v.receipt.result) {
            F05ResultView r{};
            code = f05_result(session, binding.person, q.order, &r);
            if (code != F04_OK) return code;
            view.execution = ExecutionResult{r.id,r.executor,r.input_revision,r.tick,r.performed,r.code,
                r.core_outcome,r.core_rejection,r.core_revision_before,r.core_revision_after,r.stream,r.value,r.consumed_random};
        }
        out.order = view;
        return F04_OK;
    }
    default: return F04_INTERNAL;
    }
}

// H08-P02: one real F05 source, read by the owning thread only. Never accept
// actor/scope from the consumer. F05 checks per-order observer access.
std::uint32_t events(F04Session* session, F04Ref player, std::uint64_t order,
                     std::uint64_t after, NativeEventPage& page) noexcept
{
    page = {};
    if (!session || !order) return F04_ARGUMENT;
    F05PlayerBinding binding{};
    auto code = f05_player_binding(session, &binding);
    if (code != F04_OK) return code;
    if (!binding.record || binding.person.id != player.id ||
        binding.person.scope != player.scope) return F04_DENIED;
    F04Person person{};
    code = f04_person(session, binding.person, binding.person.id, &person);
    if (code != F04_OK) return code;
    F05OrderView order_view{};
    code = f05_order(session, binding.person, order, &order_view);
    if (code != F04_OK) return code;
    F05EventView source[16]{};
    std::uint64_t written = 0;
    std::uint32_t more = 0;
    code = f05_events_page(session, binding.person, order, after, source, 16, &written, &more);
    if (code != F04_OK) return code;
    if (written > 16) return F04_INTERNAL;
    for (std::uint64_t i = 0; i < written; ++i) {
        page.events[i] = {EventSource::F05_ORDER, source[i].id, source[i].previous,
                          source[i].order, source[i].tick, source[i].state, source[i].code};
    }
    page.written = written;
    page.more = more != 0;
    return F04_OK;
}
/* H08-P03: privileged HOST-controlled clock service. This single owner-thread
 * call, not a gameplay order, delegates ALL timeline/task decisions to F04/Core.
 * F04_CAPACITY means an already committed partial advance. */
std::uint32_t advance(F04Session* session, F04Ref player, const ClockIntent& request,
                      NativeClockReport& report) noexcept
{
    report = {};
    if (!session || !request.intent_id || !request.task_budget ||
        request.task_budget > ClockLimits::max_tasks) return F04_ARGUMENT;
    F05PlayerBinding binding{};
    auto code = f05_player_binding(session, &binding);
    if (code != F04_OK) return code;
    if (!binding.record || binding.person.id != player.id ||
        binding.person.scope != player.scope) return F04_DENIED;
    F04Person authorized{};
    code = f04_person(session, binding.person, binding.person.id, &authorized);
    if (code != F04_OK) return code;
    F04Stats before{};
    code = f04_stats(session, &before);
    if (code != F04_OK) return code;
    if (request.expected_revision != before.revision ||
        request.expected_now != before.now) return F04_STALE;
    if (request.horizon < before.now ||
        request.horizon - before.now > ClockLimits::max_span_seconds)
        return F04_ARGUMENT;

    std::uint64_t processed = 0;
    const auto advanced = f04_advance(session, request.horizon,
                                      request.task_budget, &processed);
    // Even F04_CAPACITY can have committed work and advanced to an earlier
    // clock boundary. A subsequent call MUST be a new, explicit intent.
    if (advanced != F04_OK && advanced != F04_CAPACITY) return advanced;
    F04Stats after{};
    code = f04_stats(session, &after);
    if (code != F04_OK) return code;
    if (processed > request.task_budget || after.now < before.now ||
        after.now > request.horizon || (advanced == F04_OK && after.now != request.horizon))
        return F04_INTERNAL;
    report = {before.now,after.now,before.revision,after.revision,processed,
              advanced == F04_CAPACITY};
    return F04_OK;
}

}
