#!/usr/bin/env python3
"""F15 release-readiness reference gate.

This tool validates self-reported QA/release metadata and repository state.
It never certifies Core integration, UE5 execution, MSI performance, beta
acceptance, or a distributable build by itself.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

BLOCKED = "BLOCKED"
REVIEW = "REVIEW_REQUIRED"
AUTHORITY = "OFFLINE_REFERENCE_ONLY_NO_CORE_UE5_MSI_OR_RELEASE_AUTHORITY"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$")
JOURNEY_STAGES = (
    "academy",
    "first_assignment",
    "mission",
    "career_decision",
    "save",
    "load",
)
UX_AREAS = {
    "castellano",
    "controls",
    "accessibility",
    "ux",
    "logs",
    "migrations",
    "recoverable_errors",
}

def nonblank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())

def bool_exact(value: Any) -> bool:
    return type(value) is bool

def number(value: Any) -> bool:
    return type(value) in (int, float) and not isinstance(value, bool)

def positive(value: Any) -> bool:
    return number(value) and value > 0

def sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(_SHA256.fullmatch(value))

def outcome(status: str, reason: str, **details: Any) -> dict[str, Any]:
    return {
        "status": status,
        "reasons": [reason],
        "runtime_certified": False,
        "release_certified": False,
        **details,
    }

def qa_gate(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return outcome(BLOCKED, "invalid_qa_record")
    areas = ("domain_ci", "core_integration", "ue5_automation")
    if not all(bool_exact(item.get(k)) for k in areas):
        return outcome(BLOCKED, "invalid_qa_record")
    refs = item.get("evidence_refs")
    if not isinstance(refs, list) or any(not nonblank(x) for x in refs):
        return outcome(BLOCKED, "invalid_qa_record")
    if any(item[k] for k in areas) and not refs:
        return outcome(BLOCKED, "qa_claim_without_evidence")
    if not all(item[k] for k in areas):
        return outcome(
            BLOCKED,
            "qa_layers_incomplete",
            missing=[k for k in areas if not item[k]],
        )
    return outcome(REVIEW, "qa_metadata_complete_requires_runtime_review")

def journey_gate(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return outcome(BLOCKED, "invalid_journey_record")
    stages = item.get("stages")
    if stages != list(JOURNEY_STAGES):
        return outcome(BLOCKED, "journey_stage_contract_mismatch")
    if not bool_exact(item.get("executed")) or not bool_exact(item.get("save_load_continuity")):
        return outcome(BLOCKED, "invalid_journey_record")
    refs = item.get("evidence_refs")
    if not isinstance(refs, list) or any(not nonblank(x) for x in refs):
        return outcome(BLOCKED, "invalid_journey_record")
    if not item["executed"]:
        return outcome(BLOCKED, "e2e_not_executed")
    if not refs:
        return outcome(BLOCKED, "e2e_execution_without_evidence")
    if not item["save_load_continuity"]:
        return outcome(BLOCKED, "e2e_save_load_continuity_failed")
    return outcome(REVIEW, "e2e_capture_requires_manual_acceptance")

def performance_gate(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return outcome(BLOCKED, "invalid_performance_record")
    if not bool_exact(item.get("executed_on_msi")) or not bool_exact(item.get("provider_failure_recovered")):
        return outcome(BLOCKED, "invalid_performance_record")
    metrics = item.get("metrics")
    required = (
        "fps_avg",
        "fps_1pct_low",
        "vram_mb_peak",
        "ram_mb_peak",
        "cpu_ms_avg",
        "session_minutes",
    )
    if not isinstance(metrics, dict) or not all(positive(metrics.get(k)) for k in required):
        return outcome(BLOCKED, "performance_metrics_incomplete")
    if not nonblank(item.get("evidence_ref")):
        return outcome(BLOCKED, "performance_evidence_missing")
    if not item["executed_on_msi"]:
        return outcome(BLOCKED, "msi_execution_not_confirmed")
    if not item["provider_failure_recovered"]:
        return outcome(BLOCKED, "remote_provider_failure_not_recovered")
    return outcome(
        REVIEW,
        "performance_measurements_present_threshold_acceptance_pending",
        thresholds_applied=False,
    )

def ux_gate(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict) or item.get("locale") != "es-ES":
        return outcome(BLOCKED, "invalid_ux_record")
    checks = item.get("checks")
    if not isinstance(checks, dict) or set(checks) != UX_AREAS:
        return outcome(BLOCKED, "ux_checklist_incomplete")
    allowed = {"PASS", "FAIL", "BLOCKED", "NO_EJECUTADO"}
    if any(v not in allowed for v in checks.values()):
        return outcome(BLOCKED, "ux_check_status_invalid")
    refs = item.get("evidence_refs")
    if not isinstance(refs, list) or any(not nonblank(x) for x in refs):
        return outcome(BLOCKED, "invalid_ux_record")
    if any(v != "PASS" for v in checks.values()):
        return outcome(
            BLOCKED,
            "ux_acceptance_incomplete",
            pending=sorted(k for k, v in checks.items() if v != "PASS"),
        )
    if not refs:
        return outcome(BLOCKED, "ux_pass_without_evidence")
    return outcome(REVIEW, "ux_evidence_complete_requires_human_review")

def release_gate(item: Any) -> dict[str, Any]:
    if not isinstance(item, dict):
        return outcome(BLOCKED, "invalid_release_record")
    version = item.get("version")
    if not isinstance(version, str) or not _SEMVER.fullmatch(version):
        return outcome(BLOCKED, "invalid_release_version")
    if item.get("channel") not in {"internal_beta", "beta", "release_candidate"}:
        return outcome(BLOCKED, "invalid_release_channel")
    if not sha256(item.get("artifact_sha256")):
        return outcome(BLOCKED, "invalid_build_hash")
    bools = ("build_executed", "e2e_passed", "migration_tested", "rollback_tested")
    if not all(bool_exact(item.get(k)) for k in bools):
        return outcome(BLOCKED, "invalid_release_record")
    blockers = item.get("blocker_count")
    if type(blockers) is not int or blockers < 0:
        return outcome(BLOCKED, "invalid_blocker_count")
    refs = item.get("evidence_refs")
    if not isinstance(refs, list) or any(not nonblank(x) for x in refs):
        return outcome(BLOCKED, "invalid_release_record")
    if not item["build_executed"]:
        return outcome(BLOCKED, "build_not_executed")
    if not item["e2e_passed"]:
        return outcome(BLOCKED, "release_e2e_not_passed")
    if not item["migration_tested"] or not item["rollback_tested"]:
        return outcome(BLOCKED, "update_recovery_not_tested")
    if blockers:
        return outcome(BLOCKED, "release_blockers_present", blocker_count=blockers)
    if not refs:
        return outcome(BLOCKED, "release_claim_without_evidence")
    return outcome(REVIEW, "release_candidate_requires_manual_beta_acceptance")

def validate_capture(payload: Any) -> dict[str, Any]:
    """Validate the five F15 capture sections without ever certifying release."""
    if not isinstance(payload, dict):
        return outcome(BLOCKED, "invalid_f15_capture")
    sections = {
        "qa": qa_gate(payload.get("qa")),
        "journey": journey_gate(payload.get("journey")),
        "performance": performance_gate(payload.get("performance")),
        "ux": ux_gate(payload.get("ux")),
        "release": release_gate(payload.get("release")),
    }
    blocked = sorted(name for name, result in sections.items() if result["status"] != REVIEW)
    if blocked:
        return outcome(
            BLOCKED,
            "f15_capture_not_ready",
            blocked_sections=blocked,
            sections=sections,
        )
    return outcome(
        REVIEW,
        "f15_capture_requires_manual_acceptance",
        sections=sections,
    )

def run_case(case: dict[str, Any]) -> dict[str, Any]:
    op = case.get("operation")
    item = case.get("input")
    if op == "qa":
        return qa_gate(item)
    if op == "journey":
        return journey_gate(item)
    if op == "performance":
        return performance_gate(item)
    if op == "ux":
        return ux_gate(item)
    if op == "release":
        return release_gate(item)
    return outcome(BLOCKED, "unknown_operation")

def audit_repository(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    required = [
        "proyecto/docs/roadmap/master/PLAN_MAESTRO.md",
        "proyecto/docs/roadmap/master/ESTADO_GLOBAL.json",
        "proyecto/docs/roadmap/master/CRITERIOS_DE_CIERRE.md",
        "proyecto/docs/roadmap/master/fases/F15/README.md",
        "desarrollo/tools/validation/f08_acceptance_gate.py",
        "desarrollo/tools/validation/f14_audiovisual_reference.py",
        "proyecto/docs/decisions/prototype_validation_and_release_policy.md",
        "audiovisual/localization/README.md",
        "audiovisual/ui/README.md",
    ]
    missing = [p for p in required if not (root / p).is_file()]
    if missing:
        return outcome(BLOCKED, "repository_reference_files_missing", missing=missing)

    state = json.loads((root / "proyecto/docs/roadmap/master/ESTADO_GLOBAL.json").read_text(encoding="utf-8"))
    phases = state.get("phases")
    if state.get("phase_count") != 16 or not isinstance(phases, list):
        return outcome(BLOCKED, "roadmap_phase_inventory_invalid")
    f15 = next((p for p in phases if isinstance(p, dict) and p.get("id") == "F15"), None)
    if not f15 or f15.get("target_maturity") != "ACEPTACION_SUPERADA":
        return outcome(BLOCKED, "f15_target_maturity_mismatch")
    if f15.get("status") != "PLANIFICADA":
        return outcome(BLOCKED, "f15_state_changed_requires_governance_review")

    loc = (root / "audiovisual/localization/README.md").read_text(encoding="utf-8").strip()
    ui = (root / "audiovisual/ui/README.md").read_text(encoding="utf-8").strip()
    return outcome(
        REVIEW,
        "repository_ready_for_f15_reference_only",
        current_global_phase=state.get("current_global_phase"),
        f15_status=f15.get("status"),
        localization_reserved_only=("Reserved" in loc),
        ui_reserved_only=("Reserved" in ui),
        runtime_gaps_expected=True,
    )

def execute_fixture(path: str | Path, repo_root: str | Path | None = None) -> dict[str, Any]:
    p = Path(path)
    raw = p.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("invalid_cases")
    ids = [c.get("id") for c in cases]
    if not all(nonblank(x) for x in ids) or len(ids) != len(set(ids)):
        raise ValueError("invalid_case_ids")

    results = []
    passed = 0
    for case in cases:
        result = run_case(case)
        ok = (
            result["status"] == case.get("expected_status")
            and case.get("expected_reason") in result["reasons"]
        )
        passed += int(ok)
        results.append({"id": case["id"], "ok": ok, "result": result})

    report = {
        "schema_version": "0.1.0",
        "phase": "F15",
        "authority": AUTHORITY,
        "scenario_sha256": hashlib.sha256(raw).hexdigest(),
        "cases_total": len(cases),
        "cases_passed": passed,
        "cases_failed": len(cases) - passed,
        "results": results,
    }
    if repo_root is not None:
        report["repository_audit"] = audit_repository(repo_root)
    return report

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True, type=Path)
    ap.add_argument("--repo-root", default=Path("."))
    ap.add_argument("--output", type=Path)
    ap.add_argument("--capture-template", type=Path)
    args = ap.parse_args()

    report = execute_fixture(args.scenario, args.repo_root)
    if args.capture_template:
        template = json.loads(args.capture_template.read_text(encoding="utf-8"))
        template_audit = validate_capture(template)
        report["capture_template_audit"] = template_audit
        if template_audit["status"] != BLOCKED:
            raise SystemExit("NO_EJECUTADO capture template must remain blocked")
    if report["cases_failed"]:
        raise SystemExit("scenario failures")
    if report["repository_audit"]["status"] == BLOCKED:
        raise SystemExit("repository audit blocked")
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
