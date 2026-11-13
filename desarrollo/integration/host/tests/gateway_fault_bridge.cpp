// H02/H03 fault executable substitutes the bridge. Its historical oracles stay intact.
#include "native_session.h"
namespace trek::host::detail::bridge {
std::uint32_t dispatch(F04Session*, F04Ref, const GatewayRequest&, OperationResult&) noexcept
{
    return F04_INTERNAL;
}
}
