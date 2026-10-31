# F04 history storage v1 (explicit proposed Core integration)

The stable `core-revision.txt` remains `c147d81ed069da2e09149613ab02cbc3ebe95a4a`.
`F04_ENABLE_HISTORY=OFF` is still the default. The opt-in mode uses exactly the
separate SHA in `core-history-revision.txt`, proposed by CoreRPG Draft PR #13.
It is not an audited stable dependency. Both PRs remain Draft; merge Core first
only after independent audit, then review F04. No merges are performed here.

## Responsibility and retirement policy

Core owns the issued identity watermark, original fact segments, count rules and
reductions, hash chain, manifest, generation pointer, persistence validation,
atomic publication and recovery. F04 selects closed domain facts and validates
the resulting active projection **before Core publication**. There is no second
authoritative store, seed replay, ID reset, fact deletion or increased product cap.

The product cap is still 65,536 **resident** entities. Issued IDs remain monotonic
and may exceed that cap. F04 retains present/future, at least seven operational
days, outstanding debt, crossing absences, pending tasks and the transitive
dependencies of all retained records. Old plan/origin/appointment references
keep their targets resident until they close together. Original revocations,
STOP values, replacements, causes, issuers and relationships are copied intact.
Persons, posts, competencies, population, residences and service groups remain
resident; no historical people are materialized as Actors.

The old planner counts a DUTY if `(STATE==ACTIVE || STOP exists)` and
`START < min(END, STOP if present)`. The new Core manifest count rule expresses
exactly this predicate, grouped by the persistent person reference. Core derives
the count from the original retired records and recomputes it on recovery.
F04 scores `archived_count + resident_work.size()`; recent windows, rest and
availability still use the original resident intervals. No SCHEMA 5 is needed:
these counts are versioned Core manifest data, not new Trek scalar fields.

## APIs and compatibility

All new functions are additive ABI 1 exports. Existing monolithic behavior and
SCHEMA 1/2/3/4 remain unchanged. Stable builds return F04_SAVE for unavailable
history operations. The new directory container has its own version 1.

1. Load an old save with `f04_load`; retain the original bytes/file.
2. Call `f04_history_migrate` with a **new** directory and a nonzero 16-byte
   campaign ID. It does not rewrite the original save and rejects existing output.
3. Continue using the same intention/clock APIs. Commit with
   `f04_history_publish`, or retire with `f04_history_consolidate` where
   `cutoff <= now - 604800`. Ordinary execution does not implicitly save to disk.
4. Open the entire generation with `f04_history_open`. It renews handles only
   after full Core and F04 validation. Failed recovery keeps the prior session.
5. Query original closed facts through `f04_history_page` and
   `f04_history_relations`, using one generation and exclusive ID cursor.
   Wrong generations return F04_STALE; storage failures return F04_SAVE, not
   an empty-history result. Pages are at most 256 records/relations.

After opt-in, old full-save/load and full-history duties/gaps/functions queries explicitly
return F04_SAVE. They cannot silently export an active projection as a complete
campaign. Use the versioned directory and historical APIs. Live person, position,
To branch from a legacy backup, explicitly create a fresh session and migrate to
a new campaign directory/identity; legacy load cannot reset an opted-in session.
specialist and resident projections remain available. Service coverage before
the consolidation frontier is rejected rather than inferred from missing data.
`f04_history_export_active` is a privileged diagnostic checkpoint, not a full save.
`F04Stats.entities` retains its issued-ID meaning; new `F04HistoryStats` separates
issued/resident/archived counts. No previous ABI field changes its meaning.

Core I/O/conflict or post-publication loss may leave commit outcome uncertain.
F04 blocks subsequent session use until a complete `history_open` succeeds.
The host must not retry mutations on that old projection. No fallback mixes an
older checkpoint with newer segments/RNG/time, and no valid campaign is deleted.

## Reproduction

Use an isolated build directory and clean Core checkout at the explicit proposal:

```powershell
cmake -S desarrollo/integration/f04 -B C:/F04/HistoryBuild/history -A x64 -DCORERPG_SOURCE_DIR=C:/F04/CoreHistory -DF04_ENABLE_HISTORY=ON
cmake --build C:/F04/HistoryBuild/history --config Release --parallel 4
ctest --test-dir C:/F04/HistoryBuild/history -C Release -E history_campaign_ --output-on-failure -j 4
ctest --test-dir C:/F04/HistoryBuild/history -C Release -L history_acceptance --output-on-failure -j 2
```

The campaign runner requires completed 365/730-day actual-watch campaigns; a
capacity rejection fails acceptance. Each independent process pipeline runs a
complete-history oracle, the real consolidated campaign, fresh-process future
continuation, and an independent persisted-payload audit. It preserves original
source facts and checks every block's exact original bytes, IDs, RNG/time, static
people/skills/relationships and future decisions. All post-bootstrap facts are
then reconstructed from segments plus the active checkpoint and checked against
the original oracle hashes. Large save objects remain outside the repository.

The **separate test-only oracle DLL** retains the complete original WorldState.
Only it omits the product resident budget, so it can serve as a reference; it is
not staged into Unreal or used for acceptance residency measurements. The five
local 365-day comparisons used the original unfiltered history calculation.
For 730 days, `-DF04_FAST_HISTORY_ORACLE=ON` keeps every original fact and computes
the exact lifetime count afresh, while removing work spans ending at least seven
days before now from *temporary future-window calculation*. Such spans cannot
overlap any future interval, 12h-rest or future 168h window; full historical schema
validation still checks the entire history. This is only an oracle optimization.
The optimized oracle additionally defers repeated global type/reference schema
checks to complete explicit validations at both final horizons. The complete
historical roster validator still runs at every plan. The product bridge continues
to run its full active-domain validator at every transaction without this deferral.
The original/optimized oracle's Miranda 365-day hashes are independently identical.
The product bridge always uses Core-derived authoritative counts and the fixed cap.

For old-save migration and prior phases, see `tests/check_legacy_history.py`,
`check_guardias_compatibility.py` and `tests/verify_history_regressions.py`. The
latter uses disposable F02/F03 source copies with only exact-SHA build/test
assertions changed; repository source and stable pins remain untouched.

Unreal staging accepts `run_f04.ps1 -History -F04NativeBuild <proposed-build>`.
It writes the proposed SHA and history-enabled flag into generated lab headers,
and requires 26 NullRHI tests. The normal path still requires its existing 25.
The new subsystem queries return plain history data and explicit errors; they
create no historical Actors or graphics resources.
