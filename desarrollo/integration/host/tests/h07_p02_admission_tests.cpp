// H07-P02: native admission and fail-closed regressions.
// New, independent test binary: no change to historical M0 fixtures or CoreRPG.
// No F11 trial issuer is compiled or linked here.
#include "test_support.h"
#include "player_bootstrap.h"
#include "gateway_test_access.h"
#include "slot_store.h"

#include <filesystem>
#include <iostream>
#include <string>
#include <vector>

using namespace test;
namespace fs = std::filesystem;
namespace {
using U = std::uint64_t;

void check(unsigned actual, unsigned expected, const char* message)
{
    require(actual == expected, message);
}

void denied(const OperationResult& result, Error expected, U correlation)
{
    require(result.error == expected, "Unexpected institutional admission outcome");
    require(result.correlation_id == correlation, "Lost transport correlation");
    require(result.generation == Generation{}, "Denied institutional request exposed generation");
    require(!result.campaign && !result.order && !result.receipt,
            "Denied institutional request exposed an output projection");
}

std::vector<std::uint8_t> exported(F04Session* session)
{
    U size = 0;
    auto exporter = f04_save;
    auto code = exporter(session, nullptr, 0, &size);
    if (code == F04_SAVE) {
        exporter = f04_history_export_active;
        code = exporter(session, nullptr, 0, &size);
    }
    check(code, F04_CAPACITY, "Cannot size authoritative Core snapshot");
    std::vector<std::uint8_t> bytes(size);
    check(exporter(session, bytes.data(), size, &size), F04_OK, "Cannot export Core snapshot");
    bytes.resize(static_cast<std::size_t>(size));
    return bytes;
}

struct Fixture {
    SessionOwner owner;
    Generation generation;
    std::string campaign;

    Fixture(const fs::path& root, bool bind)
        : owner(StorageConfig{root.string()})
    {
        auto opened = owner.open({"miranda", 65001, 404, 130, 0, 0, 0}).get();
        expect(opened, Error::OK);
        generation = opened.generation;
        campaign = owner.campaign_id(generation);
        // Use the same *legitimate* local-person fixture preparation as H05,
        // not a test-only institutional grant, promotion or F11 commissioner.
        visit([&](F04Session* session) {
            F04Handles handles{};
            check(f04_handles(session, &handles), F04_OK, "Cannot fetch fixture captain");
            auto apply = [&](unsigned operation, U aux = 0, U begin = 0, U end = 0,
                             unsigned value = 0) {
                F04Stats stats{};
                check(f04_stats(session, &stats), F04_OK, "Cannot fetch fixture revision");
                F04Request request{handles.captain, stats.revision, operation, value,
                                   0, aux, begin, end, 50501};
                F04Result result{};
                check(f04_execute(session, &request, &result), F04_OK, "Cannot prepare fixture");
            };
            apply(F04_INSTALL_TEMPLATE, F04_SUTHERLAND_EQUIPMENT, 0, 0, F04_SUTHERLAND_SCIENCE);
            apply(F04_BOOTSTRAP_TEMPLATE);
            apply(F04_PLAN_ALPHA, 0, 28800, 57600);
            U processed = 0;
            check(f04_advance(session, 28800, 4096, &processed), F04_OK, "Cannot advance fixture");
        });
        if (bind) {
            auto prepared = PlayerBootstrap::prepare(owner, generation, 3).get();
            require(prepared.error == Error::OK && prepared.selection.has_value(),
                    "Cannot prepare local player for admission test");
            auto result = PlayerBootstrap::bind(owner, generation, *prepared.selection,
                                                prepared.revision).get();
            require(result.error == Error::OK, "Cannot bind local player for admission test");
        }
    }

    void visit(std::function<void(F04Session*)> callback)
    {
        expect(GatewayTestAccess::visit(owner, generation, std::move(callback)).get(), Error::OK);
    }

    std::vector<std::uint8_t> bytes()
    {
        std::vector<std::uint8_t> result;
        visit([&](F04Session* session) { result = exported(session); });
        return result;
    }
};

void run(std::string_view name, const fs::path& root)
{
    Fixture fixture(root, name != "unbound");
    const auto before = fixture.bytes();
    if (name == "unbound") {
        denied(fixture.owner.institutional_command(fixture.generation, 701).get(),
               Error::PRINCIPAL_UNBOUND, 701);
        require(fixture.bytes() == before, "Unbound request mutated Core");
    } else if (name == "repeated") {
        for (U i = 0; i < 8; ++i) {
            denied(fixture.owner.institutional_command(fixture.generation, 800 + i).get(),
                   Error::SERVICE_UNAVAILABLE, 800 + i);
            require(fixture.bytes() == before, "Repeated institutional request mutated Core");
        }
    } else if (name == "expired") {
        const auto old = fixture.generation;
        const auto old_campaign = fixture.campaign;
        expect(fixture.owner.close().get(), Error::OK);
        const auto opened = fixture.owner.open({"miranda", 65001, 405, 130, 0, 0, 0}).get();
        expect(opened, Error::OK);
        fixture.generation = opened.generation;
        require(old != fixture.generation && old_campaign != fixture.owner.campaign_id(fixture.generation),
                "Reopen did not replace the scope");
        const auto fresh_bytes = fixture.bytes();
        denied(fixture.owner.institutional_command(old, 901).get(), Error::GENERATION_EXPIRED, 901);
        denied(fixture.owner.institutional_command(fixture.generation, 902).get(),
               Error::PRINCIPAL_UNBOUND, 902);
        require(fixture.bytes() == fresh_bytes, "Old-scope request mutated new campaign");
    } else if (name == "restore") {
        expect(fixture.owner.save(fixture.generation, "alpha").get(), Error::OK);
        const auto old = fixture.generation;
        const auto restored = fixture.owner.restore(old, {fixture.campaign, "alpha"}).get();
        expect(restored, Error::OK);
        fixture.generation = restored.generation;
        require(old != fixture.generation, "Restore reused old generation");
        denied(fixture.owner.institutional_command(old, 1001).get(), Error::GENERATION_EXPIRED, 1001);
        denied(fixture.owner.institutional_command(fixture.generation, 1002).get(),
               Error::SERVICE_UNAVAILABLE, 1002);
        require(fixture.bytes() == before, "Institutional path or restore changed authoritative Core");
    } else if (name == "closed") {
        const auto old = fixture.generation;
        expect(fixture.owner.close().get(), Error::OK);
        denied(fixture.owner.institutional_command(old, 1101).get(), Error::GENERATION_EXPIRED, 1101);
        denied(fixture.owner.institutional_command(Generation{}, 1102).get(),
               Error::SESSION_CLOSED, 1102);
    } else {
        throw std::runtime_error("Unknown H07-P02 case");
    }
}
} // namespace

namespace trek::host::detail {
void gateway_test_after_bind() {}
void gateway_test_after_dispatch(F04Session*, std::uint32_t&) {}
void gateway_test_after_clock(F04Session*) {}
} // namespace trek::host::detail

int main(int argc, char** argv)
{
    try {
        require(argc == 3, "Usage: h07-case root");
        const fs::path root = fs::absolute(argv[2]) / trek::host::detail::new_campaign_id();
        fs::create_directories(root);
        fs::permissions(root, fs::perms::owner_all, fs::perm_options::replace);
        run(argv[1], root);
        std::cout << "PASS H07-P02 " << argv[1] << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "FAIL H07-P02 " << error.what() << '\n';
        return 1;
    }
}
