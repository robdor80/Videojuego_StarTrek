#include "HostAcademyExports.h"

#include <cstddef>
#include <cstdio>
#include <cstring>
#include <initializer_list>

#ifdef _WIN32
#include <filesystem>
#include <Windows.h>
#else
#include <dlfcn.h>
#endif

static_assert(TREK_HOST_ABI_VERSION == 1 && TREK_HOST_ACADEMY_VERSION == 2);
static_assert(sizeof(TrekHostRequest) == 80 && sizeof(TrekHostCompletion) == 120);
static_assert(sizeof(TrekHostStatus) == 24 && offsetof(TrekHostCompletion, output) == 72);
static_assert(sizeof(TrekHostAcademyRequest) == 48 && sizeof(TrekHostAcademyView) == 240);
static_assert(sizeof(TrekHostSlotMetadata) == 104 && sizeof(TrekHostAcademyCompletion) == 6696);
static_assert(offsetof(TrekHostAcademyCompletion, output) == 32);

namespace
{
uint32_t TREK_HOST_ABI_CALL DraftVersion()
{
    return 1;
}

uint32_t TREK_HOST_ABI_CALL DisabledVersion()
{
    return 0;
}

bool Check(bool Passed, const char* Message)
{
    std::fprintf(Passed ? stdout : stderr, "%s %s\n", Passed ? "PASS" : "FAIL", Message);
    return Passed;
}
}

int main(int Argc, char** Argv)
{
    if (Argc != 2)
    {
        return 1;
    }
#ifdef _WIN32
    const auto HostPath = std::filesystem::absolute(Argv[1]).make_preferred();
    const auto BridgePath = HostPath.parent_path() / L"TrekF04Bridge.dll";
    constexpr auto SearchFlags = LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR | LOAD_LIBRARY_SEARCH_DEFAULT_DIRS;
    const auto Bridge = LoadLibraryExW(BridgePath.c_str(), nullptr, SearchFlags);
    if (!Bridge)
    {
        std::fprintf(stderr, "LoadLibraryExW(TrekF04Bridge.dll) failed: %lu\n", GetLastError());
        return 1;
    }
    const auto Library = LoadLibraryExW(HostPath.c_str(), nullptr, SearchFlags);
    if (!Library)
    {
        std::fprintf(stderr, "LoadLibraryExW(TrekHost.dll) failed: %lu\n", GetLastError());
        FreeLibrary(Bridge);
        return 1;
    }
    const auto Resolve = [Library](const char* Name) { return GetProcAddress(Library, Name); };
#else
    const auto Library = dlopen(Argv[1], RTLD_NOW | RTLD_LOCAL);
    const auto Resolve = [Library](const char* Name) { return dlsym(Library, Name); };
#endif
    if (!Check(Library != nullptr, "load Release product and dependencies"))
    {
        return 1;
    }

    const auto Academy = FHostAcademyApi::Negotiate(Resolve);
    bool Passed = Check(Academy.Availability == TREK_HOST_OK && Academy.Submit && Academy.Poll,
                        "negotiate all three real Academy v2 exports");
    for (const char* Missing : {"trek_host_academy_version", "trek_host_academy_submit", "trek_host_academy_poll"})
    {
        const auto Partial = FHostAcademyApi::Negotiate([&](const char* Name)
        {
            return std::strcmp(Name, Missing) == 0 ? nullptr : Resolve(Name);
        });
        Passed &= Check(Partial.Availability == TREK_HOST_SERVICE_UNAVAILABLE && !Partial.Submit && !Partial.Poll, Missing);
    }
    const auto NegotiateVersion = [&](decltype(&trek_host_academy_version) Version)
    {
        return FHostAcademyApi::Negotiate([&](const char* Name)
        {
            return std::strcmp(Name, "trek_host_academy_version") == 0
                ? reinterpret_cast<decltype(Resolve(Name))>(Version) : Resolve(Name);
        });
    };
    const auto Draft = NegotiateVersion(&DraftVersion);
    Passed &= Check(Draft.Availability == TREK_HOST_ABI_MISMATCH && !Draft.Submit && !Draft.Poll,
                    "reject Academy draft v1");
    const auto Disabled = NegotiateVersion(&DisabledVersion);
    Passed &= Check(Disabled.Availability == TREK_HOST_SERVICE_UNAVAILABLE && !Disabled.Submit && !Disabled.Poll,
                    "honor native unavailable version");

    const auto NavalVersion = reinterpret_cast<decltype(&trek_host_abi_version)>(Resolve("trek_host_abi_version"));
    const auto Create = reinterpret_cast<decltype(&trek_host_create)>(Resolve("trek_host_create"));
    const auto Destroy = reinterpret_cast<decltype(&trek_host_destroy)>(Resolve("trek_host_destroy"));
    TrekHostClient* Client = nullptr;
    Passed &= Check(NavalVersion && NavalVersion() == 1 && Create && Destroy &&
                    Create(1, "", 0, &Client) == TREK_HOST_OK && Client,
                    "naval v1 remains usable after rejected Academy negotiation");
    if (Client)
    {
        Destroy(Client);
    }
#ifdef _WIN32
    FreeLibrary(Library);
    FreeLibrary(Bridge);
#else
    dlclose(Library);
#endif
    return Passed ? 0 : 1;
}
