#!/usr/bin/env python3
"""F11-P05-A02-02: immutable-source and frozen-history certification guard.

This is an offline evidence-integrity gate, NOT a substitute for the C++/Core
runtime suites in the companion GitHub Actions workflow.
"""
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
BASELINE = "d54457f20712849902b3815cc20a68ac813bcc4d"
BASELINE_TREE = "7538df58a95c2634cc8027c4a51adc51dd0994b6"
EXPECTED_PINS = {
    "desarrollo/integration/f04/core-revision.txt": "c147d81ed069da2e09149613ab02cbc3ebe95a4a",
    "desarrollo/integration/f04/core-history-revision.txt": "89a0e4fe4c10fb86a03086f09f034fdd0b3d3d98",
    "desarrollo/integration/f05/core-revision.txt": "76a7b7b485616d8c4994f384a90f123bf333591d",
}
ALLOWED_CHANGES = {
    ".github/workflows/f11-a02-02-certification.yml",
    "desarrollo/tools/validation/f11_p05_a02_02_certify.py",
    "proyecto/docs/roadmap/master/fases/F11/F11-P05-A02-02_CERTIFICACION_PERSISTENCIA_COMPATIBILIDAD_2026-11-11.md",
    "proyecto/docs/roadmap/master/fases/F11/README.md",
}
CAMPAIGNS = ((1, 365), (2, 365), (3, 365), (4, 365), (5, 365), (5, 730))
EXPECTED_CASES = {
    "f11.promotion", "f11.negatives", "f11.authority", "f11.identity",
    "f11.idempotency", "f11.atomic", "f11.corrupt", "f11.legacy",
    "f11.history", "f11.abi", "f11.process_save", "f11.process_load",
    "f11.product_bridge",
}

def check(test, message):
    if not test:
        raise AssertionError(message)

def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()

def main():
    # A02-01 is the actual audited source tree: certify no source, pin,
    # reference fixture, acceptance or audit provenance was modified in A02-02.
    check(git("rev-parse", BASELINE + "^{tree}") == BASELINE_TREE,
          "Audited A02-01 baseline tree mismatch")
    subprocess.run(["git", "merge-base", "--is-ancestor", BASELINE, "HEAD"],
                   cwd=ROOT, check=True)
    changed = set(git("diff", "--name-only", BASELINE, "HEAD", "--").splitlines())
    check(changed <= ALLOWED_CHANGES,
          "A02-02 changed outside certification-only allowlist: " +
          repr(sorted(changed - ALLOWED_CHANGES)))

    for name, pin in EXPECTED_PINS.items():
        check((ROOT / name).read_text(encoding="utf-8").strip() == pin,
              "Unexpected Core pin: " + name)

    # The actual CTest enumerator must retain all 13 distinct F11 cases.
    cmake = (ROOT / "desarrollo/integration/f11/CMakeLists.txt").read_text(encoding="utf-8")
    match = re.search(r"foreach\(case IN ITEMS\s+([^)]*)\)", cmake)
    check(match is not None, "Missing F11 native case enumeration")
    cases = {"f11." + item for item in match.group(1).split()}
    cases.update({"f11.process_save", "f11.process_load", "f11.product_bridge"})
    check(cases == EXPECTED_CASES, "Native F11 case list changed or incomplete")
    for name in ("process_save", "process_load", "product_bridge"):
        check("add_test(NAME f11." + name in cmake, "Missing CTest case: " + name)

    # The existing v2 auditor checks v1 provenance, immutable acceptance and
    # original oracles, as well as transition evidence bound to source hashes.
    sys.path.insert(0, str(ROOT / "desarrollo/integration/f04/tests"))
    import history_reference  # pylint: disable=import-outside-toplevel
    for profile, days in CAMPAIGNS:
        manifest, entry = history_reference.contract(
            profile, days, EXPECTED_PINS["desarrollo/integration/f04/core-history-revision.txt"], ROOT)
        history_reference.verify(ROOT / entry["oracle"], profile, days,
                                  EXPECTED_PINS["desarrollo/integration/f04/core-history-revision.txt"], ROOT)
        check(manifest.get("manifest_version") == 2, "V2 manifest protection not active")

    # This metadata names *prior* successful CI, not the new PR's outcome.
    evidence = json.loads((ROOT / "desarrollo/integration/f11/CI_EVIDENCE.json").read_text())
    check(evidence["implementation_commit"] == "1d26889fe5ea5b3390f7ba129c1fb7441c8881e8",
          "Prior native evidence origin changed")
    check(evidence["run_id"] == 43003893957, "Prior CI evidence run changed")
    check(evidence["core_revision"] == EXPECTED_PINS["desarrollo/integration/f05/core-revision.txt"],
          "Prior evidence Core pin changed")
    check({(job["platform"], job["compiler"], job["tests"], job["result"]) for job in evidence["jobs"]}
          == {("ubuntu-latest", "GNU", 13, "PASS"), ("windows-latest", "MSVC", 13, "PASS")},
          "Prior platform evidence incomplete")
    print(json.dumps({
        "phase": "F11-P05-A02-02",
        "gate": "SOURCE_AND_FROZEN_EVIDENCE_INTEGRITY",
        "result": "PASS",
        "audited_baseline": BASELINE,
        "audited_tree": BASELINE_TREE,
        "allowed_changed_files": sorted(changed),
        "frozen_history_campaigns_verified": 6,
        "f11_native_cases_declared": 13,
        "runtime_executed_by_this_script": False,
        "unreal_certified": False,
    }, indent=2))

if __name__ == "__main__":
    main()
