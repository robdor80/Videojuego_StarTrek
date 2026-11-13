#pragma once

#include <cstdint>
#include <mutex>
#include <string_view>

namespace trek::host {
class SessionOwner;
class Generation;
namespace detail {

// The outer guard lets the C boundary fail fast under contention. The
// existing SessionOwner methods still acquire this mutex recursively, so
// their admission rules and all historical callers share the same path.
class AbiAdmission {
public:
    explicit AbiAdmission(SessionOwner&);
    static std::uint64_t token(Generation) noexcept;
    std::string_view campaign() const noexcept;
    explicit operator bool() const noexcept { return lock_.owns_lock(); }

private:
    SessionOwner& owner_;
    std::unique_lock<std::recursive_mutex> lock_;
};

} // namespace detail
} // namespace trek::host
