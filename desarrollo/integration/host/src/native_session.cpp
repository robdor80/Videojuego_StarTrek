#include "native_session.h"

#include <atomic>
#include <exception>
#include <string_view>

namespace trek::host::detail {
namespace {

// The reservation covers initialization and any failed destruction.
constinit std::atomic_bool campaign_reserved{false};

Outcome normalize(std::uint32_t code) noexcept
{
    switch (code) {
    case F04_OK: return {};
    case F04_ARGUMENT: return {Error::INVALID_ARGUMENT, code};
    case F04_THREAD: return {Error::WRONG_THREAD, code};
    case F04_CAPACITY: return {Error::CAPACITY_LIMIT, code};
    case F04_INTERNAL: return {Error::INTERNAL_ERROR, code};
    default: return {Error::DOMAIN_REJECTED, code};
    }
}

} // namespace

NativeSession::~NativeSession() noexcept
{
    if (session_ || reserved_) {
        std::terminate();
    }
}

Outcome NativeSession::open(const PopulationConfig& config) noexcept
{
    bool available = false;
    if (!campaign_reserved.compare_exchange_strong(available, true)) {
        return {Error::BUSY_STATE};
    }
    reserved_ = true;

    const auto* sha = bridge::core_sha();
    if (!sha || std::string_view(sha) != TREK_HOST_CORE_SHA) {
        return {Error::INTERNAL_ERROR};
    }
    const auto created = normalize(bridge::create(config, &session_));
    if (created.error != Error::OK) {
        return created;
    }
    if (!session_) {
        return {Error::INTERNAL_ERROR};
    }
    return probe();
}

Outcome NativeSession::probe() const noexcept
{
    return normalize(bridge::probe(session_));
}

Outcome NativeSession::close() noexcept
{
    if (session_) {
        const auto destroyed = normalize(bridge::destroy(session_));
        if (destroyed.error != Error::OK) {
            return destroyed;
        }
        session_ = nullptr;
    }
    if (reserved_) {
        reserved_ = false;
        campaign_reserved.store(false);
    }
    return {};
}

} // namespace trek::host::detail
