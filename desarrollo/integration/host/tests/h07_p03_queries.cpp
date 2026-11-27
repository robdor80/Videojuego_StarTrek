#include "academy_interface.h"
#include "gateway_test_access.h"
#include "institutional_queries.h"
#include "player_bootstrap.h"
#include "slot_store.h"
#include "test_support.h"

#ifdef F11_HOST_READ_ONLY
#include "f11_promotions.h"
#endif

#include <chrono>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <semaphore>

using namespace test;
using namespace trek::host::detail;
namespace fs = std::filesystem;

namespace {
using U = std::uint64_t;
using Bytes = std::vector<std::uint8_t>;
std::function<void(bool)> observe_persistence;

void denied(const InstitutionalResult& result, Error expected, U correlation)
{
    require(result.error == expected && result.correlation_id == correlation &&
            result.generation == Generation{} && !result.view && !result.persistence_epoch,
            "Incorrect denial, correlation or empty projection");
}

void issuance_closed(SessionOwner& owner, Generation generation)
{
    auto result = owner.institutional_command(generation, 17).get();
    require(result.error == Error::SERVICE_UNAVAILABLE && result.correlation_id == 17 &&
            result.generation == Generation{} && !result.campaign && !result.order && !result.receipt,
            "A valid player obtained output from the institutional command path");
}

void bind(SessionOwner& owner, Generation generation, U player)
{
    const auto prepared = PlayerBootstrap::prepare(owner, generation, player).get();
    require(prepared.error == Error::OK && prepared.selection, "Cannot resolve test player");
    require(PlayerBootstrap::bind(owner, generation, *prepared.selection, prepared.revision).get().error == Error::OK,
            "Cannot bind test player");
}

struct Fixture {
    SessionOwner owner;
    Generation generation;

    explicit Fixture(const fs::path& root) : owner(StorageConfig{root.string()}) {}

    void visit(std::function<void(F04Session*)> fn)
    {
        expect(GatewayTestAccess::visit(owner, generation, std::move(fn)).get(), Error::OK);
    }

    Bytes bytes()
    {
        Bytes result;
        visit([&](F04Session* session) {
            U size = 0;
            auto export_core = f04_save;
            auto code = export_core(session, nullptr, 0, &size);
            if (code == F04_SAVE) {
                export_core = f04_history_export_active;
                code = export_core(session, nullptr, 0, &size);
            }
            require(code == F04_CAPACITY && size, "Cannot size Core snapshot");
            result.resize(static_cast<std::size_t>(size));
            require(export_core(session, result.data(), size, &size) == F04_OK, "Cannot export Core snapshot");
        });
        return result;
    }

    void load_fixture(const Bytes& bytes)
    {
        visit([&](F04Session* session) {
            require(f04_load(session, bytes.data(), bytes.size()) == F04_OK, "Cannot load F11 archive in product bridge");
        });
    }

    InstitutionalResult career(U correlation = 11)
    {
        return InstitutionalQueries::career(owner, generation, correlation).get();
    }

    InstitutionalResult promotion(U event, U correlation = 12)
    {
        return InstitutionalQueries::promotion(owner, generation, event, correlation).get();
    }
};

void capability(const fs::path& root)
{
    Fixture f(root);
    denied(f.career(), Error::SESSION_CLOSED, 11);
    f.generation = open(f.owner);
    denied(f.career(), Error::PRINCIPAL_UNBOUND, 11);
    bind(f.owner, f.generation, 3);
    const auto before = f.bytes();
#ifdef F11_HOST_READ_ONLY
    denied(f.career(), Error::DOMAIN_REJECTED, 11);
#else
    denied(f.career(), Error::SERVICE_UNAVAILABLE, 11);
    denied(f.promotion(42), Error::SERVICE_UNAVAILABLE, 12);
#endif
    issuance_closed(f.owner, f.generation);
    require(f.bytes() == before, "Reading a legacy campaign changed Core");
}

void academy()
{
    SessionOwner owner;
    const auto candidate = AcademyInterface::create_bound(owner, 1, R"({"display_name":"Aren"})").get();
    require(candidate.error == Error::OK && candidate.candidate, "Cannot create bound H06 cadet");
    denied(InstitutionalQueries::career(owner, candidate.generation, 21).get(), Error::SERVICE_UNAVAILABLE, 21);
    denied(InstitutionalQueries::promotion(owner, candidate.generation, 10, 22).get(), Error::SERVICE_UNAVAILABLE, 22);
    const auto after = AcademyInterface::query(owner, candidate.generation).get();
    require(after.error == Error::OK && after.candidate && after.candidate->revision == candidate.candidate->revision &&
            after.candidate->person == candidate.candidate->person, "F11 query changed Academy identity or revision");
}

#ifdef F11_HOST_READ_ONLY
constexpr U promoted = 5, other_officer = 8, legacy_captain = 3;
struct CommittedEvent { U id, revision; };

Bytes read_bytes(const fs::path& path)
{
    std::ifstream input(path, std::ios::binary);
    require(bool(input), "Cannot open Core snapshot");
    return {std::istreambuf_iterator<char>(input), {}};
}

CommittedEvent initialize(Fixture& f, U player)
{
    // Output generated by the separate F11 process_save regression.
    const auto* source = std::getenv("TREK_HOST_H07_FIXTURE");
    require(source && *source, "Set TREK_HOST_H07_FIXTURE to the isolated F11 process_save file prefix");
    std::ifstream metadata(std::string(source) + ".txt");
    U order = 0, input = 0, key = 0;
    CommittedEvent event{};
    require(bool(metadata >> order >> input >> key >> event.id >> event.revision) && event.id && event.revision,
            "Missing commit metadata from F11 process_save");
    f.generation = open(f.owner);
    f.load_fixture(read_bytes(std::string(source) + "-after.f04"));
    bind(f.owner, f.generation, player);
    return event;
}

void check_career(Fixture& f, U person)
{
    F11PersonnelView canonical{};
    f.visit([&](F04Session* session) {
        F04Handles handles{};
        require(f04_handles(session, &handles) == F04_OK &&
                f11_personnel(session, {handles.ship.scope, person}, &canonical) == F04_OK,
                "Cannot read canonical F11 personnel");
    });
    const auto result = f.career();
    require(result.correlation_id == 11 && result.generation == f.generation &&
            InstitutionalQueries::is_current(f.owner, result), "Career reply is missing or out of date");
    const auto& view = std::get<CareerViewV1>(result.view->facts);
    require(result.view->world_revision == canonical.revision && view.rank == canonical.rank &&
            view.rank_event_id == canonical.rank_event && view.service_status == canonical.service_status,
            "Career projection diverged from F11 Core facts");
}

void check_promotion(Fixture& f, CommittedEvent event)
{
    F11PromotionView canonical{};
    f.visit([&](F04Session* session) {
        F04Handles handles{};
        require(f04_handles(session, &handles) == F04_OK &&
                f11_promotion(session, {handles.ship.scope, promoted}, event.id, &canonical) == F04_OK,
                "Cannot read canonical F11 promotion");
    });
    const auto result = f.promotion(event.id);
    require(result.correlation_id == 12 && result.generation == f.generation &&
            InstitutionalQueries::is_current(f.owner, result), "Promotion reply is missing or out of date");
    const auto& view = std::get<PromotionViewV1>(result.view->facts);
    require(view.event_id == canonical.receipt.promotion_event_id && view.original_revision == event.revision &&
            view.original_revision == canonical.receipt.original_commit_revision &&
            result.view->world_revision == canonical.receipt.current_revision &&
            view.effective_tick == canonical.receipt.effective_at && view.from_rank == canonical.receipt.from_rank &&
            view.to_rank == canonical.receipt.to_rank && view.from_rank == F11_ENSIGN &&
            view.to_rank == F11_LIEUTENANT_JUNIOR_GRADE, "Promotion projection diverged from F11 Core facts");
}

void rejected_scope(Fixture& f, const Bytes& before, CommittedEvent event)
{
    require(InstitutionalQueries::is_current(f.owner, f.career()), "Valid binding missing before scope change");
    f.load_fixture(before); // F04 renews the scope even with exactly the same archived player binding.
    denied(f.career(), Error::SCOPE_INVALID, 11);
    denied(f.promotion(event.id), Error::SCOPE_INVALID, 12);
}

void close_with_pending_read(Fixture& f, CommittedEvent event)
{
    const auto previous = f.career();
    require(InstitutionalQueries::is_current(f.owner, previous), "Missing view before close");
    std::binary_semaphore reached{0}, resume{0};
    auto gate = GatewayTestAccess::visit(f.owner, f.generation, [&](F04Session*) {
        reached.release();
        resume.acquire();
    });
    if (!reached.try_acquire_for(std::chrono::seconds(10))) {
        resume.release();
        gate.get();
        throw std::runtime_error("Owner did not enter test gate");
    }
    auto pending = InstitutionalQueries::promotion(f.owner, f.generation, event.id, 31);
    auto closing = f.owner.close();
    resume.release();
    denied(pending.get(), Error::GENERATION_EXPIRED, 31);
    expect(gate.get(), Error::GENERATION_EXPIRED);
    expect(closing.get(), Error::OK);
    require(!InstitutionalQueries::is_current(f.owner, previous), "CLOSE retained a previous view");
    denied(f.career(), Error::GENERATION_EXPIRED, 11);
    denied(InstitutionalQueries::career(f.owner, {}, 32).get(), Error::SESSION_CLOSED, 32);
}

void save_then_restore(Fixture& f, const fs::path& root, const Bytes& before, CommittedEvent event)
{
    const auto campaign = f.owner.campaign_id(f.generation);
    const auto old = f.generation;
    const auto previous = f.career();
    require(InstitutionalQueries::is_current(f.owner, previous), "Missing view before SAVE");
    std::binary_semaphore reached{0}, resume{0};
    auto pause = [&](bool expected) {
        observe_persistence = [&, expected](bool saving) {
            if (saving == expected) {
                reached.release();
                resume.acquire();
            }
        };
    };
    auto finish = [&](std::future<Result> operation, U correlation) {
        const auto entered = reached.try_acquire_for(std::chrono::seconds(10));
        InstitutionalResult busy;
        if (entered) busy = f.promotion(event.id, correlation);
        resume.release();
        const auto result = operation.get();
        observe_persistence = {};
        require(entered, "Owner did not enter persistence gate");
        denied(busy, Error::BUSY_STATE, correlation);
        expect(result, Error::OK);
        return result;
    };
    pause(true);
    finish(f.owner.save(old, "career"), 41);
    require(!InstitutionalQueries::is_current(f.owner, previous), "SAVE retained a previous view");
    check_career(f, promoted);

    const auto fresh = f.career();
    pause(false);
    const auto restored = finish(f.owner.restore(old, {campaign, "career"}), 42);
    f.generation = restored.generation;
    require(old != f.generation && !InstitutionalQueries::is_current(f.owner, fresh),
            "RESTORE retained the old generation or view");
    denied(InstitutionalQueries::career(f.owner, old, 51).get(), Error::GENERATION_EXPIRED, 51);
    check_career(f, promoted);
    check_promotion(f, event);
    issuance_closed(f.owner, f.generation);
    require(f.bytes() == before, "SAVE/RESTORE or reading mutated Core");

    std::ofstream metadata(root / "career-fixture.txt");
    metadata << campaign << ' ' << event.id << ' ' << event.revision << '\n';
    require(bool(metadata), "Cannot persist test metadata");
    std::ofstream archive(root / "canonical.f04", std::ios::binary);
    archive.write(reinterpret_cast<const char*>(before.data()), static_cast<std::streamsize>(before.size()));
    require(bool(archive), "Cannot persist Core comparison snapshot");
}

void restore_in_new_process(const fs::path& root, bool imported)
{
    std::ifstream metadata(root / "career-fixture.txt");
    std::string campaign;
    CommittedEvent event{};
    require(bool(metadata >> campaign >> event.id >> event.revision), "Missing saved-query fixture");
    const auto storage = imported ? root / new_campaign_id() : root;
    if (imported) {
        fs::create_directory(storage);
        fs::copy(root / "campaigns", storage / "campaigns", fs::copy_options::recursive);
    }
    Fixture f(storage);
    const auto restored = f.owner.restore({}, {campaign, "career"}).get();
    if (imported) {
        expect(restored, Error::SAVE_UNTRUSTED);
        denied(f.career(), Error::SESSION_CLOSED, 11);
        return;
    }
    expect(restored, Error::OK);
    f.generation = restored.generation;
    require(f.owner.campaign_provenance(f.generation) == Provenance::KNOWN_LOCAL, "H04 lost local provenance");
    check_career(f, promoted);
    check_promotion(f, event);
    issuance_closed(f.owner, f.generation);
    require(f.bytes() == read_bytes(root / "canonical.f04"), "Cross-process restore or queries mutated Core");
}

void run_confirmed(std::string_view name, const fs::path& root)
{
    if (name == "restore" || name == "import") {
        restore_in_new_process(root, name == "import");
        return;
    }
    Fixture f(root);
    const auto event = initialize(f, name == "foreign" ? other_officer :
                                     name == "uncommissioned" ? legacy_captain : promoted);
    const auto before = f.bytes();
    if (name == "career") {
        check_career(f, promoted);
    } else if (name == "promotion") {
        check_promotion(f, event);
    } else if (name == "uncommissioned") {
        denied(f.career(), Error::DOMAIN_REJECTED, 11);
        denied(f.promotion(event.id), Error::ACCESS_DENIED, 12);
    } else if (name == "foreign") {
        check_career(f, other_officer);
        denied(f.promotion(event.id), Error::ACCESS_DENIED, 12);
        denied(f.promotion(event.id + 1000), Error::ACCESS_DENIED, 12);
        denied(f.promotion(0), Error::INVALID_ARGUMENT, 12);
    } else if (name == "scope") {
        rejected_scope(f, before, event);
    } else if (name == "closed") {
        close_with_pending_read(f, event);
        return;
    } else if (name == "repeated") {
        for (unsigned i = 0; i < 4; ++i) {
            check_career(f, promoted);
            check_promotion(f, event);
            issuance_closed(f.owner, f.generation);
        }
    } else if (name == "save") {
        save_then_restore(f, root, before, event);
    } else {
        throw std::runtime_error("Unknown H07-P03 test");
    }
    require(f.bytes() == before, "Institutional reads or denials changed Core bytes");
}
#endif
} // namespace

namespace trek::host::detail {
void gateway_test_after_bind() {}
void gateway_test_after_dispatch(F04Session*, std::uint32_t&) {}
void gateway_test_after_clock(F04Session*) {}
void persistence_test_observe(F04Session*, bool saving)
{
    if (observe_persistence) observe_persistence(saving);
}
} // namespace trek::host::detail

int main(int argc, char** argv)
{
    try {
        require(argc == 3, "Usage: host_h07_query_tests case root");
        const std::string_view name = argv[1];
        const fs::path root = fs::absolute(argv[2]);
        fs::create_directories(root);
        fs::permissions(root, fs::perms::owner_all, fs::perm_options::replace);
        if (name == "capability") capability(root);
        else if (name == "academy") academy();
#ifdef F11_HOST_READ_ONLY
        else run_confirmed(name, root);
#else
        else throw std::runtime_error("F11 read composition OFF");
#endif
        std::cout << "PASS H07-P03 " << name << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL H07-P03 " << error.what() << '\n';
        return 1;
    }
}
