#!/usr/bin/env python3
"""F14 reference validator for audiovisual assets/NAP. No UE5 or NAP runtime authority."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

REVIEW = "REVIEW_REQUIRED"
BLOCKED = "BLOCKED"
NO_ASSET = "NO_ASSET"
AUTHORITY = "OFFLINE_REFERENCE_ONLY_NO_NAP_OR_UE5_RUNTIME_AUTHORITY"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_SHA40 = re.compile(r"^[0-9a-f]{40}$")
PRESENTATION_FAMILIES = {"voice", "ambience", "music", "sfx", "camera", "ui"}
ERAS = {"pike", "kirk", "tng_ds9_voyager", "era_neutral"}
SOURCE_STATES = {
    "REFERENCE_ONLY",
    "LOCAL_ORIGINAL_PENDING_INVENTORY",
    "PRODUCTION_CANDIDATE",
    "PRODUCTION_VERIFIED",
}
RIGHTS_STATES = {"UNKNOWN", "DECLARED_UNVERIFIED", "VERIFIED", "PROJECT_ORIGINAL"}


def outcome(status, *reasons, **details):
    return {
        "status": status,
        "reasons": sorted(set(reasons)),
        "authority": AUTHORITY,
        **details,
    }


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def bool_exact(value):
    return type(value) is bool


def positive_number(value):
    return type(value) in (int, float) and value > 0


def valid_sha256(value):
    return isinstance(value, str) and bool(_SHA256.fullmatch(value))


def valid_sha40(value):
    return isinstance(value, str) and bool(_SHA40.fullmatch(value))


def unique_nonblank_list(value, allow_empty=False):
    return (
        isinstance(value, list)
        and (allow_empty or bool(value))
        and all(nonblank(x) for x in value)
        and len(value) == len(set(value))
    )


def audit_nap_alignment(item):
    if not isinstance(item, dict):
        return outcome(BLOCKED, "invalid_nap_alignment")
    required = (
        item.get("nap_repo") == "robdor80/NAP"
        and valid_sha40(item.get("nap_commit"))
        and item.get("manifest_schema_version") == 2
        and item.get("profile_schema_version") == 4
        and item.get("universe_id_candidate") == "star_trek"
        and unique_nonblank_list(item.get("star_trek_contract_refs"))
        and unique_nonblank_list(item.get("nap_contract_refs"))
    )
    if not required:
        return outcome(BLOCKED, "nap_contract_snapshot_incomplete")
    if not bool_exact(item.get("installed_profile")):
        return outcome(BLOCKED, "invalid_installed_profile_flag")
    if item["installed_profile"]:
        if not nonblank(item.get("runtime_validation_evidence_ref")):
            return outcome(BLOCKED, "installed_profile_claim_without_evidence")
        return outcome(
            REVIEW,
            "nap_runtime_profile_evidence_requires_human_review",
            profile_state="EVIDENCE_RECORDED_NOT_CERTIFIED_HERE",
        )
    if item.get("runtime_validation_evidence_ref") is not None:
        return outcome(BLOCKED, "uninstalled_profile_cannot_claim_runtime_evidence")
    return outcome(
        REVIEW,
        "star_trek_profile_not_installed_reference_mapping_only",
        profile_state="REFERENCE_MAPPING_ONLY",
    )


def rights_gate(item):
    if not isinstance(item, dict) or not nonblank(item.get("asset_id")):
        return outcome(BLOCKED, "invalid_rights_record")
    if not all(nonblank(item.get(k)) for k in ("source_ref", "author_declared", "license_declared")):
        return outcome(BLOCKED, "rights_provenance_incomplete")
    if not bool_exact(item.get("rights_verified")):
        return outcome(BLOCKED, "invalid_rights_verified_flag")
    if not item["rights_verified"]:
        return outcome(
            BLOCKED,
            "rights_not_verified_for_distribution",
            distribution_allowed=False,
        )
    return outcome(
        REVIEW,
        "rights_metadata_present_requires_distribution_policy_review",
        distribution_allowed=False,
    )


def priority_gate(item):
    if not isinstance(item, dict):
        return outcome(BLOCKED, "invalid_priority_record")
    if not (
        nonblank(item.get("asset_id"))
        and type(item.get("priority")) is int
        and 0 <= item["priority"] <= 4
        and nonblank(item.get("need_ref"))
        and item.get("source_state") in SOURCE_STATES
        and item.get("rights_state") in RIGHTS_STATES
        and bool_exact(item.get("ue5_claim"))
    ):
        return outcome(BLOCKED, "invalid_priority_record")
    if item["source_state"] == "PRODUCTION_VERIFIED" and item["rights_state"] not in {"VERIFIED", "PROJECT_ORIGINAL"}:
        return outcome(BLOCKED, "production_verified_with_unresolved_rights")
    if item["ue5_claim"] and not nonblank(item.get("ue5_evidence_ref")):
        return outcome(BLOCKED, "ue5_claim_without_evidence")
    if item["source_state"] != "PRODUCTION_VERIFIED":
        return outcome(
            REVIEW,
            "priority_only_not_asset_production",
            production_ready=False,
        )
    return outcome(
        REVIEW,
        "production_record_requires_build_acceptance",
        production_ready=True,
    )


def presentation_gate(item):
    if not isinstance(item, dict):
        return outcome(BLOCKED, "invalid_presentation_record")
    if not (
        nonblank(item.get("asset_id"))
        and item.get("family") in PRESENTATION_FAMILIES
        and item.get("era") in ERAS
        and bool_exact(item.get("binary_present"))
        and bool_exact(item.get("rights_verified"))
        and bool_exact(item.get("runtime_claim"))
    ):
        return outcome(BLOCKED, "invalid_presentation_record")
    if not item["binary_present"]:
        if item["runtime_claim"]:
            return outcome(BLOCKED, "runtime_claim_without_binary")
        return outcome(NO_ASSET, "production_binary_absent")
    if not item["rights_verified"]:
        return outcome(BLOCKED, "presentation_rights_unverified")
    if item["runtime_claim"] and not nonblank(item.get("ue5_evidence_ref")):
        return outcome(BLOCKED, "presentation_runtime_claim_without_ue5_evidence")
    return outcome(
        REVIEW,
        "presentation_asset_metadata_ready_for_runtime_review",
        runtime_proven=False,
    )


def optimization_gate(item):
    if not isinstance(item, dict):
        return outcome(BLOCKED, "invalid_optimization_record")
    if not (
        nonblank(item.get("asset_id"))
        and valid_sha256(item.get("original_sha256"))
        and valid_sha256(item.get("derivative_sha256"))
        and bool_exact(item.get("overwrite_original"))
        and bool_exact(item.get("claim_optimized"))
    ):
        return outcome(BLOCKED, "invalid_optimization_record")
    if item["overwrite_original"]:
        return outcome(BLOCKED, "original_overwrite_forbidden")
    if item["original_sha256"] == item["derivative_sha256"]:
        return outcome(BLOCKED, "derivative_must_be_distinct_record")
    if not item["claim_optimized"]:
        return outcome(REVIEW, "optimization_plan_only")
    metrics = item.get("metrics")
    if not isinstance(metrics, dict) or not all(
        positive_number(metrics.get(k)) for k in ("fps", "vram_mb", "draw_calls")
    ):
        return outcome(BLOCKED, "optimization_claim_without_runtime_metrics")
    if item.get("lod_verified") is not True or item.get("streaming_verified") is not True:
        return outcome(BLOCKED, "optimization_claim_without_lod_streaming_evidence")
    return outcome(
        REVIEW,
        "optimization_metrics_present_requires_ue5_acceptance",
        optimized_claim_certified=False,
    )


def traceability_gate(item):
    if not isinstance(item, dict):
        return outcome(BLOCKED, "invalid_traceability_record")
    required = (
        nonblank(item.get("asset_id"))
        and nonblank(item.get("source_ref"))
        and valid_sha256(item.get("original_sha256"))
        and nonblank(item.get("manifest_ref"))
        and nonblank(item.get("external_repo_ref"))
        and bool_exact(item.get("claim_build_functional"))
        and bool_exact(item.get("recovery_tested"))
    )
    if not required:
        return outcome(BLOCKED, "traceability_chain_incomplete")
    derivative = item.get("derivative_sha256")
    if derivative is not None and not valid_sha256(derivative):
        return outcome(BLOCKED, "invalid_derivative_hash")
    if item["claim_build_functional"]:
        if item.get("ue5_execution") != "EXECUTED" or not nonblank(item.get("build_evidence_ref")):
            return outcome(BLOCKED, "build_claim_without_execution_evidence")
    if item["recovery_tested"] and not nonblank(item.get("recovery_evidence_ref")):
        return outcome(BLOCKED, "recovery_claim_without_evidence")
    return outcome(
        REVIEW,
        "traceability_chain_present_not_runtime_certification",
        build_certified=False,
    )


def run_case(case):
    op = case.get("operation")
    data = case.get("input")
    if op == "nap_alignment":
        return audit_nap_alignment(data)
    if op == "rights":
        return rights_gate(data)
    if op == "priority":
        return priority_gate(data)
    if op == "presentation":
        return presentation_gate(data)
    if op == "optimization":
        return optimization_gate(data)
    if op == "traceability":
        return traceability_gate(data)
    return outcome(BLOCKED, "unknown_operation")


def audit_repository(repo_root):
    root = Path(repo_root)
    required = [
        "audiovisual/art_direction/nap/STAR_TREK_VISUAL_SYSTEM_NAP_CONTRACT_v0.1.md",
        "audiovisual/art_direction/schemas/nap_asset_handoff.schema.json",
        "desarrollo/validation/fixtures/nap/sensors_console_tng_v0.1/manifest.json",
        "assets/otros/escenas/bridges/f07_registry.json",
        "audiovisual/presentation/pov_profiles/starship_bridge_povs.json",
        "desarrollo/nap/profile/F14_NAP2_COMPATIBILITY_SNAPSHOT_v0.1.json",
        "desarrollo/manifests/assets/f14_asset_priority_manifest_v0.1.json",
        "desarrollo/manifests/presentation/f14_presentation_priority_manifest_v0.1.json",
    ]
    missing = [p for p in required if not (root / p).is_file()]
    if missing:
        return outcome(BLOCKED, "repository_reference_files_missing", missing=missing)

    with (root / "assets/otros/escenas/bridges/f07_registry.json").open("r", encoding="utf-8") as fh:
        registry = json.load(fh)
    entries = {e.get("asset_id"): e for e in registry.get("entries", []) if isinstance(e, dict)}
    sutherland = entries.get("bridge-sutherland-original")
    if not sutherland:
        return outcome(BLOCKED, "sutherland_registry_entry_missing")
    if sutherland.get("rights_verified") is not False:
        return outcome(BLOCKED, "sutherland_rights_state_changed_review_required")
    if sutherland.get("ue5_status") not in {"NO_EJECUTADO", "NO_VERIFICADO_EN_F07"}:
        return outcome(BLOCKED, "sutherland_ue5_state_changed_review_required")

    with (root / "desarrollo/nap/profile/F14_NAP2_COMPATIBILITY_SNAPSHOT_v0.1.json").open("r", encoding="utf-8") as fh:
        snapshot = json.load(fh)
    if snapshot.get("status") != "REFERENCE_MAPPING_NOT_INSTALLED_PROFILE":
        return outcome(BLOCKED, "nap_snapshot_overclaims_runtime")
    if snapshot.get("external_nap", {}).get("verified_main_commit") != "30a0b199fcb3200ce9e4de97944d2ff9fd0c642c":
        return outcome(BLOCKED, "nap_snapshot_commit_mismatch")

    with (root / "desarrollo/manifests/assets/f14_asset_priority_manifest_v0.1.json").open("r", encoding="utf-8") as fh:
        assets = json.load(fh)
    asset_entries = assets.get("entries")
    if assets.get("status") != "REFERENCE_PRIORITY_ONLY_NO_ASSET_PRODUCTION" or not isinstance(asset_entries, list) or not asset_entries:
        return outcome(BLOCKED, "asset_priority_manifest_invalid")
    asset_ids = [item.get("asset_id") for item in asset_entries if isinstance(item, dict)]
    if len(asset_ids) != len(asset_entries) or not all(nonblank(x) for x in asset_ids) or len(asset_ids) != len(set(asset_ids)):
        return outcome(BLOCKED, "asset_priority_manifest_ids_invalid")
    for item in asset_entries:
        source_ref = item.get("source_ref")
        if (
            type(item.get("priority")) is not int
            or not 0 <= item["priority"] <= 4
            or item.get("source_state") not in SOURCE_STATES
            or item.get("rights_state") not in RIGHTS_STATES
            or item.get("ue5_state") != "NO_EJECUTADO"
            or not nonblank(item.get("need_ref"))
            or not nonblank(source_ref)
            or not unique_nonblank_list(item.get("required_next_evidence"))
        ):
            return outcome(BLOCKED, "asset_priority_manifest_entry_invalid", asset_id=item.get("asset_id"))
        if not (root / source_ref).exists():
            return outcome(BLOCKED, "asset_priority_source_missing", asset_id=item["asset_id"], source_ref=source_ref)

    with (root / "desarrollo/manifests/presentation/f14_presentation_priority_manifest_v0.1.json").open("r", encoding="utf-8") as fh:
        presentation = json.load(fh)
    families = presentation.get("families")
    if presentation.get("status") != "REFERENCE_PRIORITY_ONLY_NO_MEDIA_RUNTIME" or not isinstance(families, list) or not families:
        return outcome(BLOCKED, "presentation_priority_manifest_invalid")
    family_ids = [item.get("id") for item in families if isinstance(item, dict)]
    if len(family_ids) != len(families) or not all(nonblank(x) for x in family_ids) or len(family_ids) != len(set(family_ids)):
        return outcome(BLOCKED, "presentation_priority_manifest_ids_invalid")
    for item in families:
        refs = item.get("source_refs")
        if (
            item.get("family") not in PRESENTATION_FAMILIES
            or item.get("era") not in ERAS
            or type(item.get("priority")) is not int
            or not 0 <= item["priority"] <= 4
            or item.get("runtime_status") != "NO_EJECUTADO"
            or not unique_nonblank_list(refs)
            or not nonblank(item.get("binary_status"))
            or not nonblank(item.get("next_gate"))
        ):
            return outcome(BLOCKED, "presentation_priority_manifest_entry_invalid", family_id=item.get("id"))
        missing_refs = [ref for ref in refs if not (root / ref).exists()]
        if missing_refs:
            return outcome(BLOCKED, "presentation_priority_source_missing", family_id=item["id"], missing=missing_refs)

    return outcome(
        REVIEW,
        "repository_reference_inventory_consistent",
        checked_files=len(required),
        asset_priority_entries=len(asset_entries),
        presentation_priority_families=len(families),
        sutherland_rights_verified=False,
        sutherland_ue5_certified=False,
    )


def execute_fixture(path, repo_root=None):
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
        expected_status = case.get("expected_status")
        expected_reason = case.get("expected_reason")
        ok = result["status"] == expected_status and expected_reason in result["reasons"]
        passed += int(ok)
        results.append({"id": case["id"], "ok": ok, "result": result})
    report = {
        "schema_version": "0.1.0",
        "phase": "F14",
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output")
    args = ap.parse_args()
    report = execute_fixture(args.scenario, args.repo_root)
    if report["cases_failed"]:
        raise SystemExit("scenario failures")
    if report["repository_audit"]["status"] == BLOCKED:
        raise SystemExit("repository audit blocked")
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
