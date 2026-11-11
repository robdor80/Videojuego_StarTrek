#pragma once
#include "f11_promotions.h"
#include <cstdint>

// Trusted native Host-side consumer of already committed F11 facts.
// NOT a public authority endpoint. Calling code must authenticate the person
// and authorize disclosure BEFORE passing the F04Ref to these functions.
// No Blueprint/AI/client entrypoint. No commissions, grants or ranks are minted.
namespace trek::f11_host {

struct Career {
  F11CharacterId character{};
  std::uint64_t local_person=0, commission=0, rank_event=0, ship=0;
  std::uint64_t billet=0, department=0, world_revision=0;
  std::uint32_t rank=0, service_status=0;
};

struct Promotion {
  F11CharacterId character{};
  std::uint64_t promotion_event=0, personnel_order=0, original_revision=0;
  std::uint64_t effective_tick=0, person=0, ship=0, billet=0, department=0;
  std::uint32_t from_rank=0, to_rank=0, visibility=0;
};

// Read-only projections, NOT security capabilities. F04 owns the WorldState.
// No presentation timestamps, synthetic grades or secondary data stores.
std::uint32_t career(F04Session* session, F04Ref subject, Career* out) noexcept;
std::uint32_t promotion(F04Session* session, F04Ref subject,
                        std::uint64_t event, Promotion* out) noexcept;

} // namespace trek::f11_host
