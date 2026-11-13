#include "test_support.h"

#include "f04_bridge.h"

#include <barrier>
#include <iostream>
#include <thread>

#ifdef _WIN32
# define NOMINMAX
# include <windows.h>
#else
# include <dlfcn.h>
#endif

namespace {
using namespace test;

void opening()
{
    SessionOwner owner;
    closed(owner);
    const auto generation = open(owner);
    expect(owner.check_active(generation).get(), Error::OK);
    expect(owner.close().get(), Error::OK);
    closed(owner);
}

void open_failure()
{
    SessionOwner owner;
    auto invalid = population();
    invalid.class_id = "class_missing_from_f04";
    expect(owner.open(invalid).get(), Error::INVALID_ARGUMENT);
    closed(owner);

    invalid = population();
    invalid.maximum = 1;
    expect(owner.open(invalid).get(), Error::CAPACITY_LIMIT);
    closed(owner);

    invalid.class_id.assign("miranda\0ignored", 15);
    expect(owner.open(invalid).get(), Error::INVALID_ARGUMENT);
    closed(owner);

    SessionOwner other;
    open(other);
    expect(other.close().get(), Error::OK);
    open(owner);
    expect(owner.close().get(), Error::OK);
}

void duplicate()
{
    SessionOwner owner;
    std::barrier start(2);
    std::future<Result> first;
    std::jthread caller([&] {
        start.arrive_and_wait();
        first = owner.open(population());
    });
    start.arrive_and_wait();
    auto second = owner.open(population());
    caller.join();
    const auto a = first.get();
    const auto b = second.get();
    require((a.error == Error::OK) != (b.error == Error::OK), "Expected exactly one successful open");
    expect(a.error == Error::OK ? b : a, Error::BUSY_STATE);
    expect(owner.check_active((a.error == Error::OK ? a : b).generation).get(), Error::OK);
    expect(owner.close().get(), Error::OK);
}

void double_close()
{
    SessionOwner owner;
    const auto old = open(owner);
    const auto first = owner.close();
    const auto second = owner.close();
    expect(owner.check_active(old).get(), Error::GENERATION_EXPIRED);
    expect(first.get(), Error::OK);
    expect(second.get(), Error::OK);
    closed(owner);
    expect(owner.check_active({}).get(), Error::SESSION_CLOSED);
}

void thread_boundary()
{
    SessionOwner owner;
    Result result;
    std::jthread opener([&] { result = owner.open(population()).get(); });
    opener.join();
    expect(result, Error::OK);
    // The initiating producer is gone. F04 rejects this call if it bypasses the owner.
    expect(owner.check_active(result.generation).get(), Error::OK);
    std::jthread closer([&] { result = owner.close().get(); });
    closer.join();
    expect(result, Error::OK);
    closed(owner);
}

void reopen()
{
    SessionOwner owner;
    auto old = open(owner);
    expect(owner.close().get(), Error::OK);
    const auto first = old;
    for (int i = 0; i < 24; ++i) {
        const auto current = open(owner);
        require(old != current && first != current, "Generation reused");
        expect(owner.check_active(old).get(), Error::GENERATION_EXPIRED);
        expect(owner.check_active(first).get(), Error::GENERATION_EXPIRED);
        expect(owner.close().get(), Error::OK);
        old = current;
    }
}

void exclusive()
{
    SessionOwner first;
    SessionOwner second;
    std::barrier start(2);
    std::future<Result> pending;
    std::jthread other([&] {
        start.arrive_and_wait();
        pending = first.open(population());
    });
    start.arrive_and_wait();
    const auto b = second.open(population()).get();
    other.join();
    const auto a = pending.get();
    require((a.error == Error::OK) != (b.error == Error::OK), "Two owners acquired the campaign or neither did");
    const bool first_won = a.error == Error::OK;
    expect(first_won ? b : a, Error::BUSY_STATE);
    auto& winner = first_won ? first : second;
    auto& next = first_won ? second : first;
    const auto old = first_won ? a.generation : b.generation;
    expect(winner.close().get(), Error::OK);
    const auto current = open(next);
    require(old != current, "Generation reused across owners");
    expect(next.check_active(old).get(), Error::GENERATION_EXPIRED);
    expect(next.close().get(), Error::OK);
}

void shutdown()
{
    std::future<Result> last;
    {
        SessionOwner owner;
        last = owner.check_active(open(owner));
    }
    const auto result = last.get();
    require(result.error == Error::OK || result.error == Error::GENERATION_EXPIRED,
            "Shutdown did not settle the last request");
    SessionOwner next;
    open(next);
    expect(next.close().get(), Error::OK);
}

void product_boundary()
{
    require(std::string_view(f04_core_sha()) == TREK_HOST_CORE_SHA, "Wrong Core in loaded bridge");
    const char* forbidden[]{"f11_test_create", "f11_test_revoke", "f11_test_fault", "f11_commit_promotion"};
#ifdef _WIN32
    const auto bridge = GetModuleHandleW(L"TrekF04Bridge.dll");
    require(bridge != nullptr, "Product bridge not loaded");
    require(GetModuleHandleW(L"TrekF11TrialHost.dll") == nullptr, "Trial host is loaded");
    for (const auto* symbol : forbidden) {
        require(GetProcAddress(bridge, symbol) == nullptr, symbol);
    }
#else
    Dl_info info{};
    require(dladdr(reinterpret_cast<void*>(&f04_core_sha), &info) != 0, "Cannot locate loaded bridge");
    auto* bridge = dlopen(info.dli_fname, RTLD_NOW | RTLD_LOCAL);
    require(bridge != nullptr, "Cannot inspect loaded bridge");
    for (const auto* symbol : forbidden) {
        require(dlsym(bridge, symbol) == nullptr && dlsym(RTLD_DEFAULT, symbol) == nullptr, symbol);
    }
    dlclose(bridge);
#endif
}

constexpr Case cases[]{
    {"hc01_open", opening},
    {"hc02_open_failure", open_failure},
    {"hc03_duplicate", duplicate},
    {"hc04_double_close", double_close},
    {"hc05_thread_boundary", thread_boundary},
    {"reopen", reopen},
    {"exclusive", exclusive},
    {"shutdown", shutdown},
    {"product_boundary", product_boundary},
};
} // namespace

int main(int argc, char** argv)
{
    try {
        if (argc == 2) {
            for (const auto& scenario : cases) {
                if (scenario.name == argv[1]) {
                    scenario.run();
                    std::cout << "PASS " << scenario.name << '\n';
                    return 0;
                }
            }
        }
        throw std::runtime_error("Unknown H02 native test");
    } catch (const std::exception& error) {
        std::cerr << "FAIL " << error.what() << '\n';
        return 1;
    }
}
