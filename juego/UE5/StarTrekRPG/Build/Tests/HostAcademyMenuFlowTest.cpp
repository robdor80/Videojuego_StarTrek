#include "HostAcademyMenuFlow.h"

#include <cstdlib>
#include <iostream>
#include <string_view>

namespace
{
using Op = EAcademyOperation;
using Screen = EAcademyScreen;
using Save = EAcademySave;

void Check(bool Condition, const char* Message)
{
    if (!Condition)
    {
        std::cerr << Message << '\n';
        std::exit(EXIT_FAILURE);
    }
}

void VerifyNew(FAcademyMenuFlow& Flow)
{
    Check(Flow.Navigate(Screen::Name) && Flow.Begin(Op::Create), "New game must allow one CREATE");
    Check(!Flow.Begin(Op::Create) && !Flow.Navigate(Screen::Main), "A pending CREATE must own the flow");
    Check(Flow.Screen() == Screen::Name && !Flow.HasConfirmedProgress(), "An admitted CREATE confirms nothing");

    Flow.Resolve(TREK_HOST_OK);
    Check(Flow.Operation() == Op::VerifyNew && !Flow.CanSave(), "CREATE must be followed by QUERY");
    Flow.Resolve(TREK_HOST_OK);
    Check(Flow.Operation() == Op::FirstSave && Flow.Screen() != Screen::Candidate,
          "The first SAVE must be triggered by verified QUERY");
    Check(!Flow.HasConfirmedProgress(), "An admitted SAVE confirms nothing");
}

void NewGame()
{
    FAcademyMenuFlow Flow;
    Check(Flow.Navigate(Screen::Name) && Flow.Begin(Op::Create), "Open the name screen");
    Flow.Resolve(TREK_HOST_INVALID_ARGUMENT);
    Check(Flow.Screen() == Screen::Name && Flow.Error() == TREK_HOST_INVALID_ARGUMENT && !Flow.Busy(),
          "A rejected name must stay editable without saving");

    VerifyNew(Flow);
    Flow.Resolve(TREK_HOST_OK);
    Check(Flow.Screen() == Screen::Candidate && Flow.SaveState() == Save::Confirmed, "Show the confirmed candidate");
    Check(Flow.Begin(Op::SaveAndClose), "Start SAVE before closing");
    Flow.Resolve(TREK_HOST_OK);
    Check(Flow.Operation() == Op::Close && Flow.Screen() == Screen::Candidate, "Wait for CLOSE after SAVE");
    Flow.Resolve(TREK_HOST_OK);
    Check(Flow.Screen() == Screen::Main && !Flow.HasConfirmedProgress(), "Forget the closed session");
}

void PersistenceFailures()
{
    FAcademyMenuFlow Flow;
    VerifyNew(Flow);
    Flow.Resolve(TREK_HOST_PERSISTENCE_FAILED);
    Check(Flow.Screen() == Screen::Candidate && Flow.SaveState() == Save::Failed && Flow.CanSave(),
          "A failed first SAVE must expose an unsaved candidate and allow a manual retry");

    Check(Flow.Begin(Op::SaveAndClose), "Retry the save");
    Flow.Resolve(TREK_HOST_PUBLICATION_UNCERTAIN);
    Check(Flow.Screen() == Screen::Candidate && Flow.SaveState() == Save::Uncertain && !Flow.Busy() &&
          !Flow.HasConfirmedProgress() && !Flow.Begin(Op::Save) && !Flow.Begin(Op::SaveAndClose),
          "Uncertain publication must never close or resubmit SAVE");

    Flow.VerifyWorld();
    Flow.Resolve(TREK_HOST_OK);
    Check(Flow.SaveState() == Save::Uncertain && !Flow.CanSave(), "A world refresh cannot confirm publication");
    Check(Flow.Begin(Op::ExitClose) && !Flow.ExitRequested(), "Wait for successful CLOSE before exit");
    Flow.Resolve(TREK_HOST_RETRY);
    Check(!Flow.ExitRequested() && Flow.Screen() == Screen::Candidate, "A rejected CLOSE cannot exit");
    Check(Flow.Begin(Op::ExitClose), "Retry the close explicitly");
    Flow.Resolve(TREK_HOST_OK);
    Check(Flow.ExitRequested(), "A confirmed CLOSE allows exit");
}

void RestoreAndVerify()
{
    FAcademyMenuFlow Flow;
    Check(Flow.Navigate(Screen::Catalog) && Flow.Begin(Op::Restore), "A selected version starts RESTORE");
    Flow.Resolve(TREK_HOST_SAVE_CORRUPT);
    Check(Flow.Screen() == Screen::Catalog && Flow.Error() == TREK_HOST_SAVE_CORRUPT, "Keep the failed restore in the catalog");

    Check(Flow.Begin(Op::Restore), "Select another version");
    Flow.Resolve(TREK_HOST_OK);
    Check(Flow.Operation() == Op::VerifyRestore && !Flow.HasConfirmedProgress(), "RESTORE must verify through QUERY");
    Flow.Resolve(TREK_HOST_GENERATION_EXPIRED);
    Check(Flow.Screen() == Screen::Recovery && Flow.CanRetryVerification() && !Flow.CanSave(),
          "A stale QUERY cannot expose or save a candidate");
    Flow.RetryVerification();
    Check(Flow.Operation() == Op::VerifyRestore, "Retry QUERY alone");
    Flow.Resolve(TREK_HOST_OK);
    Check(Flow.Screen() == Screen::Candidate && Flow.SaveState() == Save::Restored && !Flow.Busy(),
          "The verified restored candidate must not trigger CREATE or SAVE");

    Flow.VerifyWorld();
    Check(Flow.Screen() == Screen::Recovery && Flow.Operation() == Op::VerifyWorld, "Travel refreshes the view with QUERY");
    Flow.ProgressChanged();
    Flow.Resolve(TREK_HOST_OK);
    Check(!Flow.HasConfirmedProgress(), "Changed progress must require a new SAVE");
}

void Catalog()
{
    FAcademyMenuCatalog Catalog;
    Check(!Catalog.IsEmpty() && !Catalog.HasPage(), "The untouched catalog is not evidence of an empty store");
    Catalog.Accept(7, false);
    Check(Catalog.HasPage() && !Catalog.IsEmpty() && Catalog.Cursor() == 7, "Keep a continuation in an empty or filtered page");
    Catalog.Accept(12, true);
    Catalog.Accept(0, true);
    Check(!Catalog.IsEmpty() && Catalog.Cursor() == 0, "Keep Academy observations across multiple pages");
    Catalog.Accept(0, false);
    Check(!Catalog.IsEmpty(), "An empty final page cannot hide earlier results");

    Catalog = {};
    Catalog.Accept(8, false);
    Catalog.Accept(0, false);
    Check(Catalog.IsEmpty(), "Only an exhausted walk without Academy rows is empty");

    using CatalogType = FAcademyMenuCatalog;
    Check(CatalogType::CanRestore(TREK_HOST_KIND_ACADEMY, 1, true, true, TREK_HOST_OK), "An exact healthy version is selectable");
    Check(!CatalogType::CanRestore(TREK_HOST_KIND_ACADEMY, 0, true, true, TREK_HOST_OK), "Never select latest implicitly");
    Check(!CatalogType::CanRestore(TREK_HOST_KIND_NAVAL, 1, true, true, TREK_HOST_OK), "Never recover a naval row");
    Check(!CatalogType::CanRestore(TREK_HOST_KIND_ACADEMY, 2, true, false, TREK_HOST_SAVE_CORRUPT), "Block corrupt versions");
    Check(!CatalogType::CanRestore(TREK_HOST_KIND_ACADEMY, 3, false, false, TREK_HOST_SAVE_INCOMPATIBLE), "Block incompatible versions");
}
}

int main(int Argc, char** Argv)
{
    Check(Argc == 2, "Expected the name of the presentation scenario");
    const std::string_view Scenario = Argv[1];
    if (Scenario == "new") NewGame();
    else if (Scenario == "failure") PersistenceFailures();
    else if (Scenario == "restore") RestoreAndVerify();
    else if (Scenario == "catalog") Catalog();
    else Check(false, "Unknown presentation scenario");
}
