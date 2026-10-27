#!/usr/bin/env python3
"""Audit F02-P05 handoff against existing Trek fixture and P03/P04 registries.

Documentary checks only: NOT Core RPG, UE5 or runtime acceptance tests.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load(root: Path, path: str):
    return json.loads((root / path).read_text(encoding="utf-8"))


def check(root: Path):
    errors = []
    base = "proyecto/docs/roadmap/master/fases/F02/"
    try:
        plan = load(root, base + "HOJA_RUTA_EJECUCION_P05.json")
        fixture = load(root, "desarrollo/validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json")
        adapters = load(root, base + "MAPA_ADAPTADORES_P03.json")
        policy = load(root, base + "REGISTRO_FALLOS_COMPATIBILIDAD_P04.json")
    except (OSError, ValueError) as exc:
        return [f"required JSON unavailable or invalid: {exc}"]
    work = plan.get("work_items", [])
    coverage = plan.get("fixture_coverage", [])
    if len(work) != 11:
        errors.append("expected 11 handoff work items")
    work_ids = [w.get("id") for w in work]
    if len(set(work_ids)) != len(work_ids):
        errors.append("duplicate work item IDs")
    if work_ids != [f"INT-{i:02d}" for i in range(11)]:
        errors.append("unexpected order or identity of INT-00..INT-10")
    allowed_adapters = {a["id"] for a in adapters["adapters"]}
    allowed_tests = {t["id"] for t in policy["tests"]}
    for w in work:
        wid = w.get("id", "<unknown>")
        if any(ref not in work_ids or ref == wid for ref in w.get("depends_on", [])):
            errors.append(f"{wid}: missing/self dependency")
        if any(ref not in allowed_adapters for ref in w.get("adapters", [])):
            errors.append(f"{wid}: unknown adapter")
        if any(ref not in allowed_tests for ref in w.get("tests", [])):
            errors.append(f"{wid}: unknown test")
        if not w.get("owner") or not w.get("exit_gate"):
            errors.append(f"{wid}: unassigned owner or missing acceptance gate")
    ids = {entry.get("id") for entry in coverage}
    expected = {entry["id"] for entry in fixture["must_pass"]}
    if len(coverage) != len(ids) or ids != expected or len(expected) != 13:
        errors.append(f"fixture coverage mismatch: expected 13 exact IDs; difference={sorted(ids ^ expected)}")
    for entry in coverage:
        if entry.get("primary_work_item") not in work_ids:
            errors.append(f"{entry.get('id')}: invalid owner work item")
        if entry.get("status") != "DESIGNED_NOT_E2E_TESTED":
            errors.append(f"{entry.get('id')}: cannot imply fixture E2E completion")
    scope = plan.get("scope", {})
    fixture_context = fixture.get("campaign_context", {})
    for plan_key, fixture_key in (
        ("era", "era_id"),
        ("campaign_date", "campaign_date"),
        ("seed", "campaign_seed"),
    ):
        if scope.get(plan_key) != fixture_context.get(fixture_key):
            errors.append(f"campaign fixture mismatch: {plan_key}")
    if scope.get("not_product_release") is not True:
        errors.append("v0.0.1 must remain an internal test")
    if plan.get("evidence", {}).get("core_ue5_integration_executed") is not False:
        errors.append("no real Core UE5 integration evidence")
    if plan.get("evidence", {}).get("tests_currently_passing_for_fixture") != 0:
        errors.append("fixture E2E pass count cannot be claimed")
    if plan.get("status") != "P05_PLAN_DOCUMENTED_EXTERNAL_ACCEPTANCE_BLOCKED":
        errors.append("external contract review still blocked")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[3]
    errors = check(root)
    if errors:
        for message in errors:
            print("F02-P05 ERROR:", message, file=sys.stderr)
        return 1
    print("PASS: P05 work packages=11, fixture invariants=13/13 mapped,")
    print("dependencies/test refs/adapter refs consistent; external Core/UE5 acceptance PENDING.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
