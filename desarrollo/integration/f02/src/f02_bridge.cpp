#include "f02_bridge.h"
#include <corerpg/action.hpp>
#include <corerpg/context_builder.hpp>
#include <corerpg/persistence.hpp>
#include <algorithm>
#include <array>
#include <atomic>
#include <cstring>
#include <limits>
#include <memory>
#include <stdexcept>
#include <thread>

namespace {
// Scopes are ephemeral Host bindings, never persisted world identities.
std::atomic<uint64_t> next_scope{1};
uint64_t allocate_scope() {
    auto value = next_scope.load();
    for (;;) {
        if (value == std::numeric_limits<uint64_t>::max())
            throw std::overflow_error("Host binding scopes exhausted");
        if (next_scope.compare_exchange_weak(value, value + 1)) return value;
    }
}
}
struct F02Session {
    const std::thread::id owner{std::this_thread::get_id()};
    corerpg::WorldState world;
    corerpg::RandomStreams random;
    uint64_t scope{allocate_scope()};
    bool allowed{true};
    const corerpg::EntityId subject{1}, room{2};
    explicit F02Session(uint64_t seed) : random(seed) {
        for (int i=0; i<3; ++i) {
            if (!world.create_entity().is_valid()) throw std::runtime_error("create");
        }
        if (world.learn_fact(subject, {subject}) != corerpg::KnowledgeChange::applied ||
            world.learn_fact(subject, {room}) != corerpg::KnowledgeChange::applied)
            throw std::runtime_error("knowledge");
    }
    bool valid(F02Ref r) const { return r.scope == scope && r.id != 0; }
    F02Ref ref(corerpg::EntityId id) const { return {scope, id.value()}; }
};
namespace {
uint32_t guard(F02Session* s) {
    if (!s) return F02_ARGUMENT;
    return s->owner == std::this_thread::get_id() ? F02_OK : F02_THREAD;
}
template<class F> uint32_t call(F02Session* s, F&& f) noexcept {
    if (auto status = guard(s); status != F02_OK) return status;
    try { return f(); } catch (...) { return F02_INTERNAL; }
}
uint32_t action(F02Session* s, F02Ref actor, corerpg::ActionOperation operation,
                uint64_t revision, F02ActionResult* out) {
    if (!out) return F02_ARGUMENT;
    *out = {};
    return call(s, [&]() -> uint32_t {
        if (!s->allowed || !s->valid(actor) || actor.id != s->subject.value())
            return out->status = F02_DENIED;
        const auto result = corerpg::ActionEngine::process(s->world, s->random,
            {s->subject, operation, revision});
        out->revision_before = result.revision_before;
        out->revision_after = result.revision_after;
        out->core_rejection = static_cast<uint32_t>(result.rejection);
        if (const auto* roll = std::get_if<corerpg::RollConsequence>(&result.consequence))
            out->rolled = roll->value;
        return out->status = result.outcome == corerpg::ActionOutcome::rejected
                                ? F02_CORE_REJECTED : F02_OK;
    });
}
}
uint32_t f02_abi_version() { return 1; }
const char* f02_core_sha() { return F02_CORE_SHA; }
uint32_t f02_create(uint32_t abi, uint64_t seed, F02Session** out) {
    if (!out) return F02_ARGUMENT;
    *out = nullptr;
    if (abi != f02_abi_version()) return F02_VERSION;
    try { *out = new F02Session(seed); return F02_OK; }
    catch (...) { return F02_INTERNAL; }
}
uint32_t f02_destroy(F02Session* s) {
    if (auto status = guard(s); status != F02_OK) return status;
    delete s; return F02_OK;
}
uint32_t f02_handles(F02Session* s, F02Handles* out) {
    if (!out) return F02_ARGUMENT;
    return call(s, [&]() -> uint32_t { *out = {s->ref(s->subject), s->ref(s->room)}; return F02_OK; });
}
uint32_t f02_contains(F02Session* s, F02Ref r, uint32_t* out) {
    if (!out) return F02_ARGUMENT;
    *out = 0;
    return call(s, [&]() -> uint32_t {
        if (!s->valid(r) || (r.id != 1 && r.id != 2)) return F02_DENIED;
        *out = s->world.contains(corerpg::EntityId{r.id}); return F02_OK;
    });
}
uint32_t f02_revision(F02Session* s, uint64_t* out) {
    if (!out) return F02_ARGUMENT;
    return call(s, [&]() -> uint32_t { *out = s->world.revision(); return F02_OK; });
}
uint32_t f02_place(F02Session* s, F02Ref actor, F02Ref room,
                   uint64_t revision, F02ActionResult* out) {
    if (!out) return F02_ARGUMENT;
    *out = {};
    if (auto status = guard(s); status != F02_OK) return status;
    if (!s->valid(room) || room.id != s->room.value()) return out->status = F02_DENIED;
    return action(s, actor, corerpg::PlaceEntityAction{s->subject, s->room}, revision, out);
}
uint32_t f02_roll(F02Session* s, F02Ref actor, uint64_t minimum, uint64_t maximum,
                  uint64_t revision, F02ActionResult* out) {
    return action(s, actor, corerpg::StreamRollAction{7, minimum, maximum}, revision, out);
}
uint32_t f02_set_permission(F02Session* s, uint32_t allowed) {
    if (allowed > 1) return F02_ARGUMENT;
    return call(s, [&]() -> uint32_t { s->allowed = allowed != 0; return F02_OK; });
}
uint32_t f02_view(F02Session* s, uint32_t context, F02Fact* out,
                  uint64_t capacity, uint64_t* count) {
    if (!count || (!out && capacity) || context > 1) return F02_ARGUMENT;
    *count = 0;
    return call(s, [&]() -> uint32_t {
        const std::array grants{corerpg::FactKey{s->subject, corerpg::FactKind::containment}};
        const auto view = corerpg::Visibility::project(s->world, s->subject, grants);
        std::array<corerpg::VisibleFact, 8> selected;
        auto facts = view.facts();
        if (context) {
            corerpg::ContextRequest request;
            request.subject = s->subject;
            const auto result = corerpg::ContextBuilder::build(view, request, selected);
            if (result.status != corerpg::ContextStatus::complete) return F02_INTERNAL;
            facts = std::span<const corerpg::VisibleFact>{selected}.first(result.emitted);
        }
        *count = facts.size();
        if (capacity < facts.size()) return F02_CAPACITY;
        for (size_t i=0; i<facts.size(); ++i) {
            const auto& f = facts[i];
            out[i] = {f.key.subject.value(), f.reference.value(),
                      static_cast<uint32_t>(f.key.kind), f.present ? 1U : 0U};
        }
        return F02_OK;
    });
}
uint32_t f02_save(F02Session* s, uint8_t* out, uint64_t capacity, uint64_t* size) {
    if (!size || (!out && capacity)) return F02_ARGUMENT;
    *size = 0;
    return call(s, [&]() -> uint32_t {
        const auto encoded = corerpg::Persistence::serialize(corerpg::Persistence::capture(s->world, s->random));
        if (encoded.status != corerpg::PersistenceStatus::success) return F02_SAVE_REJECTED;
        *size = encoded.bytes.size();
        if (capacity < encoded.bytes.size()) return F02_CAPACITY;
        std::memcpy(out, encoded.bytes.data(), encoded.bytes.size()); return F02_OK;
    });
}
uint32_t f02_load(F02Session* s, const uint8_t* bytes, uint64_t size) {
    constexpr uint64_t max_bytes = 64ULL * 1024ULL * 1024ULL;
    if (!bytes || size == 0 || size > max_bytes) return F02_ARGUMENT;
    return call(s, [&]() -> uint32_t {
        const auto decoded = corerpg::Persistence::deserialize({bytes, static_cast<size_t>(size)});
        if (decoded.status != corerpg::PersistenceStatus::success || !decoded.snapshot)
            return F02_SAVE_REJECTED;
        const auto& snapshot = *decoded.snapshot;
        // This laboratory only supports its own three-entity fixture. It does not
        // claim to be the game's general campaign loader or a migration system.
        if (snapshot.last_entity_id != 3 || !snapshot.definitions.empty()) return F02_SAVE_REJECTED;
        for (const auto& record : snapshot.knowledge) {
            if (record.observer != s->subject || record.fact.key.kind != corerpg::FactKind::existence ||
                (record.fact.key.subject != s->subject && record.fact.key.subject != s->room))
                return F02_SAVE_REJECTED;
        }
        const auto new_scope = allocate_scope(); // Can fail BEFORE publication.
        const auto status = corerpg::Persistence::restore(snapshot, s->world, s->random);
        if (status != corerpg::PersistenceStatus::success) return F02_SAVE_REJECTED;
        s->scope = new_scope; // Invalidate all old Actor bindings and queued proposals.
        return F02_OK;
    });
}
