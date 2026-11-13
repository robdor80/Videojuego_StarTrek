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
}
