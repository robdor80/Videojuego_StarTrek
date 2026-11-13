#pragma once
#include "trek/host/session_owner.h"

namespace trek::host::detail {
enum class GatewayOp { VIEW, SUBMIT, ORDER, CANCEL, INSTITUTIONAL };
struct GatewayRequest {
    GatewayOp operation = GatewayOp::VIEW;
    OrderIntent intent;
    std::uint64_t order = 0, revision = 0, correlation = 0;
};
}
