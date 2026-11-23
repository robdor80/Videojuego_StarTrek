#pragma once

#include "academy_candidate_factory.h"
#include "academy_identity.h"

#include <corerpg/campaign_persistence.hpp>
#include <corerpg/content_catalog.hpp>
#include <corerpg/history.hpp>

namespace trek::host::detail {

struct PreparedSlot;
class PinnedDirectory;

inline constexpr std::size_t academy_payload_limit = 1024;

struct UnapprovedAcademySource {};

std::optional<std::string> academy_display_name(std::string_view payload);
corerpg::HistoryHash academy_digest(std::string_view bytes);
AcademySnapshotIdentity academy_identity(const AcademyCandidateView&, std::string profile);

#ifdef TREK_HOST_ACADEMY_TESTING
enum class AcademyFault { NONE, SOURCE_VERSION, SOURCE_DIGEST, SOURCE_BYTES,
                          CATALOG, PERSON, FACT, HISTORY, BEFORE_PUBLICATION };
void set_academy_fault(AcademyFault fault) noexcept;
void academy_fail_at(AcademyFault fault);
#endif

// Live only on the SessionOwner thread. Until committed this object is staging.
class AcademyCampaign final {
public:
    static std::unique_ptr<AcademyCampaign> stage(std::string_view campaign, std::string_view name);
    static std::unique_ptr<AcademyCampaign> restore(const PreparedSlot&);
    Error snapshot(const std::filesystem::path&, const corerpg::HistoryCampaignId&) const;
    AcademyCandidateView inspect() const;
    AcademyCandidateView inspect_checkpoint() const;

private:
#ifdef TREK_HOST_ACADEMY_TESTING
    friend struct AcademyPersistenceTest;
#endif
    AcademyCampaign(corerpg::ContentCatalog catalog, std::uint64_t seed);
    corerpg::EntityId create_entity(std::string_view definition);

    corerpg::ContentCatalog catalog_;
    std::string catalog_digest_;
    corerpg::WorldState world_;
    corerpg::RandomStreams random_;
    corerpg::Timeline timeline_;
    corerpg::EntityId campus_, person_, creation_fact_;
    corerpg::HistoryArchive history_;
    std::shared_ptr<PinnedDirectory> history_pin_;
};

} // namespace trek::host::detail
