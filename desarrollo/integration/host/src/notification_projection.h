#pragma once

#include "trek/host/session_owner.h"
#include "f05_orders.h"

#include <cstddef>
#include <cstdint>
#include <optional>
#include <string_view>
#include <utility>

namespace trek::host::detail {

// H08-P04 presentation-only formatter. Never an authority or an event emitter.
// It accepts an already-admitted F05 page from SessionOwner; callers MUST NOT
// use this formatter as an observer authorization or read from Core themselves.
class NotificationProjection final {
    struct Label {
        NotificationKind kind;
        NotificationLevel level;
        const char* title;
        const char* body;
    };

    static const Label* label(std::uint32_t state) noexcept
    {
        // F05 owns the semantic transitions. Do not invent severity from raw
        // error numbers, unseen results, guessed mission facts or local clocks.
        static constexpr Label issued{NotificationKind::ORDER_ISSUED,
            NotificationLevel::INFO, "Orden emitida", "La orden ha sido emitida."};
        static constexpr Label accepted{NotificationKind::ORDER_ACCEPTED,
            NotificationLevel::INFO, "Orden recibida", "El destinatario ha aceptado la orden."};
        static constexpr Label executing{NotificationKind::ORDER_EXECUTING,
            NotificationLevel::INFO, "Orden en curso", "La orden se encuentra en curso."};
        static constexpr Label completed{NotificationKind::ORDER_COMPLETED,
            NotificationLevel::SUCCESS, "Orden completada", "La orden ha finalizado correctamente."};
        static constexpr Label failed{NotificationKind::ORDER_FAILED,
            NotificationLevel::ERROR, "Orden no completada",
            "La orden no ha finalizado correctamente. Consulte el resultado autorizado."};
        static constexpr Label refused{NotificationKind::ORDER_REFUSED,
            NotificationLevel::WARNING, "Orden rechazada", "La orden ha sido rechazada."};
        static constexpr Label cancelled{NotificationKind::ORDER_CANCELLED,
            NotificationLevel::WARNING, "Orden cancelada", "La orden ha sido cancelada."};
        switch (state) {
        case F05_ISSUED: return &issued;
        case F05_ACCEPTED: return &accepted;
        case F05_EXECUTING: return &executing;
        case F05_COMPLETED: return &completed;
        case F05_FAILED: return &failed;
        case F05_REFUSED: return &refused;
        case F05_CANCELLED: return &cancelled;
        default: return nullptr;
        }
    }

    static bool valid_campaign(std::string_view id) noexcept
    {
        if (id.size() != 32) return false;
        for (const char c : id)
            if (!((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f'))) return false;
        return true;
    }

public:
    // Pure per-item formatter for independent tests. This is NOT an
    // authorization method; SessionOwner is the sole product poll entry.
    static std::optional<NotificationNotice> format_event(const EventNotice& event)
    {
        if (event.source != EventSource::F05_ORDER || !event.id || !event.order)
            return std::nullopt;
        const auto* text = label(event.state);
        if (!text) return std::nullopt;
        return NotificationNotice{event.source, text->kind, text->level, event.id,
                                  event.previous, event.order, event.tick,
                                  text->title, text->body};
    }

    static NotificationBatchResult from_authorized_f05(
        const EventBatchResult& source, std::string_view host_campaign)
    {
        NotificationBatchResult result;
        result.error = source.error;
        result.correlation_id = source.correlation_id;
        if (source.error != Error::OK) return result; // Never project denied rows.

        // Control-only responses must NEVER become fictional gameplay events.
        if (source.resync_required) {
            result.generation = source.generation;
            result.subscription = source.subscription;
            result.resync_required = true;
            return result;
        }
        if (source.generation == Generation{} || !source.subscription ||
            !valid_campaign(host_campaign) ||
            source.events.size() > 16) {
            result.error = Error::INTERNAL_ERROR;
            return result;
        }

        // Stage all views first. A malformed or unsupported source/state must
        // publish ZERO items, never a partial notification page.
        std::vector<NotificationNotice> staged;
        staged.reserve(source.events.size());
        std::uint64_t last_id = 0, last_tick = 0, last_order = 0;
        for (const auto& event : source.events) {
            if (event.source != EventSource::F05_ORDER || !event.id || !event.order ||
                (last_id && (event.previous != last_id || event.tick < last_tick ||
                             event.order != last_order))) {
                result.error = Error::DOMAIN_REJECTED;
                return result;
            }
            const auto projected = format_event(event);
            if (!projected) {
                result.error = event.source == EventSource::F05_ORDER
                    ? Error::SERVICE_UNAVAILABLE : Error::DOMAIN_REJECTED;
                return result;
            }
            staged.push_back(*projected);
            last_id = event.id;
            last_tick = event.tick;
            last_order = event.order;
        }
        result.generation = source.generation;
        result.subscription = source.subscription;
        result.campaign_id = host_campaign;
        result.more = source.more; // Pagination is not a fact.
        result.items = std::move(staged);
        return result;
    }
};

} // namespace trek::host::detail
