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
specialist and resident projections remain available. Service coverage before
the consolidation frontier is rejected rather than inferred from missing data.
`f04_history_export_active` is a privileged diagnostic checkpoint, not a full save.
`F04Stats.entities` retains its issued-ID meaning; new `F04HistoryStats` separates
issued/resident/archived counts. No previous ABI field changes its meaning.

To branch from a legacy backup, explicitly create a fresh session and migrate to
a new campaign directory/identity; legacy load cannot reset an opted-in session.

Core I/O/conflict or post-publication loss may leave commit outcome uncertain.
F04 blocks subsequent session use until a complete `history_open` succeeds.
The host must not retry mutations on that old projection. No fallback mixes an
older checkpoint with newer segments/RNG/time, and no valid campaign is deleted.

## Reproduction

Supply an isolated runtime output root and a clean Core checkout at the explicit
proposal. Choose local output locations according to the current repository work
policy before invoking these commands; no machine-specific directory is assumed:

```powershell
if (-not $env:F04_WORK_ROOT -or -not $env:F04_CORE_SOURCE) { throw 'Configure F04_WORK_ROOT and F04_CORE_SOURCE first' }
$env:F04_TEST_TEMP_ROOT = Join-Path $env:F04_WORK_ROOT 'reference-tests'
$env:TEMP = $env:TMP = $env:TMPDIR = Join-Path $env:F04_WORK_ROOT 'system-temp'
New-Item -ItemType Directory -Force -Path $env:TEMP | Out-Null
$env:PYTHONDONTWRITEBYTECODE = '1'
cmake -S desarrollo/integration/f04 -B "$env:F04_WORK_ROOT/build" -A x64 "-DCORERPG_SOURCE_DIR=$env:F04_CORE_SOURCE" -DF04_ENABLE_HISTORY=ON
cmake --build "$env:F04_WORK_ROOT/build" --config Release --parallel 4
ctest --test-dir "$env:F04_WORK_ROOT/build" -C Release -E history_campaign_ --output-on-failure -j 4
ctest --test-dir "$env:F04_WORK_ROOT/build" -C Release -L history_acceptance --output-on-failure -j 2
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
The oracle also appends clock events to its disposable complete-history read
index when that is the only indexed change. No original record is excluded or
rewritten by that cache optimization; the authoritative WorldState remains intact.
It also derives a first-by-ID activity-cause lookup once per clock span, preserving
the original cause selection instead of rescanning all old activities at each
boundary. This lookup is disposable and never persisted as campaign authority.
The original/optimized oracle's Miranda 365-day hashes are independently identical.
Valhalla's original and event-index-optimized 365-day hashes are also identical.
The product bridge always uses Core-derived authoritative counts and the fixed cap.

The final proposal replay additionally uses the frozen original oracle hash files
through `F04_HISTORY_REFERENCE_FIXTURES`. It still generates every watch and every
fact, performs actual Core consolidation, verifies each original block hash,
continues in another process and audits all persisted payload. No campaign state
is loaded from those hash fixtures. Their original producer used Core `63d2401`;
the final campaigns run Core `89a0e4f`, whose additional change rejects uninitialized
history operations before I/O. Both exact revisions and fixture checksums are
recorded in each acceptance file. With the fixtures option omitted, the runner
regenerates the full complete-history oracle before the consolidated campaign.

### Verified CI reference and deep audit (2026-10-31)

Run `41199067055` exhausted the 3,300-second **oracle-generation** limit for
Valhalla 730. Its real consolidated campaign had not started. This failure is
not a successful CI acceptance or evidence of a deterministic divergence.

The first corrected CI reused only the audited 730-day oracle from evidence commit
`19aaf9746927cac1e0596f7f828497a8b39eac3f`. Its raw-byte SHA-256 is
`4f5b5b096e07e4e9fc2b504cb8b4e86d898655d60e99a678b567ded58140f204`.
The five 365-day jobs initially retained independent oracle generation. Run
`41207950499` passed all six campaigns and all four workflows on commit `f2dcb907`.
Every newly generated 365-day oracle was byte-identical to its audited original.
Only after that full comparison, the normal path also reuses those five references
through the same verifier and runner. Their regeneration consumed 2,436.2 seconds
of aggregate runner time, with no different expected bytes. All productive phases
and gates remain identical. All six jobs remain isolated, with `fail-fast: false`.

`tests/fixtures/history_reference_v1.json` binds all six historical references to
their profiles, durations, producer Core revision, acceptance records and original
evidence checksums. It also fingerprints the unchanged product, native campaign,
auditor, population catalog, schema inputs and test build contract. Source
fingerprints normalize CRLF to LF; oracle/evidence hashes always cover raw bytes.
The new CMake test/timeout wiring is fingerprinted at the current revision; the
simulation sources and inputs match the audited evidence commit. A deliberate
source/contract or Core change fails verification and requires regeneration and
independent review before registering a compatible reference. The manifest is
reviewed repository provenance, not a cryptographic signature from a third party.

`history_reference.py` verifies those bindings and every oracle row (block days,
strictly growing identity watermarks, 64-digit digests and final seven-day future).
It stages an exclusive-created copy in the caller-supplied disposable output root.
The existing `F04_HISTORY_REFERENCE_FIXTURES` / `--reference-fixtures` path verifies
again before use and after the run. Missing, corrupt or incompatible fixtures fail
explicitly; no fallback hides a bad fixture by generating another reference.
Original evidence files are never written. A default run with no fixture option
continues to regenerate its independent reference.

The fast path removes only reference generation. The native product still creates
all 730 days for 1,800 crew plus 400 civilians, every watch/incident/rest/relief,
consolidates originals, checks each block, enforces residency and immutable people/
skills, recovers in another process, continues deterministically and reconstructs
all persisted original payloads. A reference contains expected hashes, no state.
Acceptance additionally records the verified manifest digest and phase timings.
Fast jobs other than the first do not build the unused reference DLL/executable
or regressions already run in the first matrix job. Productive phase timeouts
remain 3,300s. The first job still compiles all targets and runs all regressions.

Reproduce from the repository root after choosing a **new**, policy-compliant
runtime output directory and setting `F04_WORK_ROOT` and `F04_CORE_SOURCE`:

```powershell
if (-not $env:F04_WORK_ROOT -or -not $env:F04_CORE_SOURCE) { throw 'Configure F04_WORK_ROOT and F04_CORE_SOURCE first' }
$env:F04_TEST_TEMP_ROOT = Join-Path $env:F04_WORK_ROOT 'reference-tests'
$env:TEMP = $env:TMP = $env:TMPDIR = Join-Path $env:F04_WORK_ROOT 'system-temp'
New-Item -ItemType Directory -Force -Path $env:TEMP | Out-Null
$env:PYTHONDONTWRITEBYTECODE = '1'
python desarrollo/integration/f04/tests/history_reference.py --profile 5 --days 730 --directory "$env:F04_WORK_ROOT/references"
cmake -S desarrollo/integration/f04 -B "$env:F04_WORK_ROOT/build" -A x64 "-DCORERPG_SOURCE_DIR=$env:F04_CORE_SOURCE" -DF04_ENABLE_HISTORY=ON -DF04_FAST_HISTORY_ORACLE=ON "-DF04_HISTORY_REFERENCE_FIXTURES=$env:F04_WORK_ROOT/references"
cmake --build "$env:F04_WORK_ROOT/build" --config Release --parallel 4
ctest --test-dir "$env:F04_WORK_ROOT/build" -C Release -R '^f04.history_reference_contract$' --no-tests=error --output-on-failure
ctest --test-dir "$env:F04_WORK_ROOT/build" -C Release -R '^f04.history_campaign_valhalla_730$' --no-tests=error --output-on-failure
```

For a deep independent audit, configure a **separate fresh build** without
`F04_HISTORY_REFERENCE_FIXTURES` and with
`-DF04_HISTORY_ORACLE_TIMEOUT_SECONDS=18000`. Build all targets and run the same
six `history_acceptance` tests. This explicitly grants the slow independent oracle
up to five hours; it does not relax productive phase or equivalence requirements.
Alternatively dispatch this workflow on the PR branch with `regenerate_oracles`
set to true (six-hour job ceiling). New reference outputs stay in the laboratory;
never overwrite audited originals or edit expected hashes to accept a divergence.

`history_reference_tests.py --bin <Release-directory>` covers valid references,
all six registrations, bad/missing/truncated bytes, wrong profile/duration,
incompatible revisions/contracts/schema, provenance tampering, original and backup
preservation, and a genuine seven-day native campaign that fails on an intentionally
wrong expected digest. CTest runs this mandatory native case in the proposed-Core
regression job. A Python-only invocation explicitly skips that one native case.

### Disposable output paths (FASE 04 BIS 2)

The history workflow derives `F04_WORK_ROOT` from GitHub's job-local `runner.temp`
and the matrix case. Verified reference copies, build products, XML, campaign
saves, logs and audits all live below that ephemeral root. Artifact upload reads
that same root. `F04_TEST_TEMP_ROOT` supplies the reference tests' scratch directory;
an unset value fails explicitly instead of inventing a fixed project directory.
`TEMP`, `TMP` and `TMPDIR` also point below the root, including native storage-fault
tests that request the system temporary directory without naming a project path.
Python bytecode writes are disabled for this job. Local runs supply their own
authorized output root through these variables, following the current work policy.

Source, permanent audited oracle originals and pinned Core checkouts are inputs.
No product, CMake configuration or integration contract gains a dependency on a
named local experiment. Removing disposable outputs after the run leaves those
inputs intact; another fresh root reproduces the same tests. This changes only
output routing: test cases, native commands, expected hashes, revisions, acceptance
gates and timeouts are unchanged. Existing evidence packages are historical records
and are not relocated or rewritten by this correction.

New CI measurements and raw evidence are added separately from the original
acceptance package. The first correction's actual 730-day pipeline took 966.6s
(729.5s simulation, 9.2s continuation/recovery, 227.7s audit), against an earlier
3,300.6s failed oracle-only attempt. Six test pipelines totalled 4,189.1s instead
of the failed baseline's 6,609.8s: 2,420.7s less aggregate runner time, 36.6%.
This compares a completed acceptance against a failed attempt; it does not measure
the unknown time of a completed baseline 730-day oracle. Runner variability is
separate from the 2,436.2s of newly measured redundant 365-day generation.
See the committed `F04-PERSISTENCIA-03-CI-OPTIMIZACION-20261031` evidence package
and the PR's latest Actions results for the final all-reference fast-path timings.

For old-save migration and prior phases, see `tests/check_legacy_history.py`,
`check_guardias_compatibility.py` and `tests/verify_history_regressions.py`. The
latter uses disposable F02/F03 source copies with only exact-SHA build/test
assertions changed; repository source and stable pins remain untouched.

Unreal staging accepts `run_f04.ps1 -History -F04NativeBuild <proposed-build>`.
It writes the proposed SHA and history-enabled flag into generated lab headers,
and requires 26 NullRHI tests. The normal path still requires its existing 25.
The new subsystem queries return plain history data and explicit errors; they
create no historical Actors or graphics resources.
