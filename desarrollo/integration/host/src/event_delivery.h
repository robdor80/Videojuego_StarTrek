#pragma once

#include "trek/host/session_owner.h"

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <deque>
#include <limits>
#include <vector>

namespace trek::host::detail {

// H08-P02: owner-thread-only, bounded, ephemeral delivery of already
// authorized Core projections. This is NOT an authoritative event store.
// Do not export across the C ABI; no Core calls occur in this container.
class EventDelivery final {
public:
    static constexpr std::size_t max_subscriptions = 16;
    static constexpr std::size_t page_capacity = 16;

    struct Subscription {
        std::uint64_t token = 0;
        std::uint64_t order = 0;
        std::uint64_t cursor = 0; // Last source event admitted, NOT a page offset.
        std::uint64_t last_ack = 0;
        bool source_more = false;
        std::deque<EventNotice> pending;
    };

    void invalidate() noexcept { subscriptions_.clear(); } // Tokens never reused.
    [[nodiscard]] bool has_capacity() const noexcept {
        return subscriptions_.size() < max_subscriptions && last_token_ < std::numeric_limits<std::uint64_t>::max();
    }
    [[nodiscard]] std::uint64_t subscribe(std::uint64_t order) {
        if (!order || !has_capacity()) return 0;
        const auto token = ++last_token_;
        subscriptions_.push_back({token, order, 0, 0, false, {}});
        return token;
    }
    [[nodiscard]] Subscription* find(std::uint64_t token) noexcept {
        for (auto& entry : subscriptions_)
            if (entry.token == token) return &entry;
        return nullptr;
    }

    // Reject malformed/out-of-order source pages *before* modifying the queue.
    // A gap means the consumer must resync from an authorized view; never forge
    // missing facts. F05 itself owns state transitions and causal relations.
    [[nodiscard]] static bool append(Subscription& entry,
                                     const EventNotice* items, std::size_t count, bool source_more) {
        if (!entry.pending.empty() || count > page_capacity || (count && !items)) return false;
        if (!count && source_more) return false;
        auto previous = entry.cursor;
        for (std::size_t i = 0; i < count; ++i) {
            const auto& e = items[i];
            if (!e.id || e.source != EventSource::F05_ORDER || e.order != entry.order ||
                e.previous != previous || e.id == previous) return false;
            previous = e.id;
        }
        for (std::size_t i = 0; i < count; ++i) entry.pending.push_back(items[i]);
        entry.cursor = previous;
        entry.source_more = source_more;
        return true;
    }

    // Ack is presentation-only; it can only consume events already supplied to
    // this subscription, in causal order. No f05_receive or Core mutation.
    [[nodiscard]] static bool ack(Subscription& entry, std::uint64_t event_id) noexcept {
        if (!event_id) return false;
        if (event_id == entry.last_ack) return true; // Repeated UI delivery ack.
        auto found = std::find_if(entry.pending.begin(), entry.pending.end(),
                                  [&](const EventNotice& e) { return e.id == event_id; });
        if (found == entry.pending.end()) return false;
        while (!entry.pending.empty()) {
            const auto front = entry.pending.front().id;
            entry.pending.pop_front();
            if (front == event_id) break;
        }
        entry.last_ack = event_id;
        return true;
    }

private:
    std::vector<Subscription> subscriptions_;
    std::uint64_t last_token_ = 0;
};

} // namespace trek::host::detail
