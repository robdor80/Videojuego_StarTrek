#pragma once
#ifndef TREK_HOST_GATEWAY_TESTING
#error "This infrastructure is available only in the separate M0 test executable"
#endif
#include "trek/host/session_owner.h"
#include "f04_bridge.h"
#include <functional>

namespace trek::host {
// Trusted fixture and recipient simulation. Always scheduled on SessionOwner's
// worker; no test symbol or arbitrary actor capability exists in TrekHost.
class GatewayTestAccess {
public:
    static std::future<Result> visit(SessionOwner&, Generation, std::function<void(F04Session*)>);
};
}
