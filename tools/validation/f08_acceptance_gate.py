#!/usr/bin/env python3
"""F08: auditor de evidencia externa para v0.0.1 (SOLO LECTURA).

Nunca crea World State, ejecuta órdenes, interpreta el sensor ni certifica
ejecución real. READY_FOR_MANUAL_REVIEW significa *consistencia formal*, no
aprobación de un build ni existencia verificada de Core/UE5.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ACCEPTANCE = ROOT / "validation/fixtures/sensors_vertical_slice_acceptance_v0.0.1.json"
REQUIRED_ARTIFACTS = frozenset({
    "core_trace", "ue5_log", "save_file", "screenshot", "performance",
})
CHAIN = ("ORDER_ISSUED", "ORDER_ACKNOWLEDGED", "ACTION_STARTED",
         "RESULT_CREATED", "REPORT_MADE")
BANNED_PUBLIC_KEYS = frozenset({
    "entity_id", "ground_truth", "world_state", "truth",
    "hidden_properties", "unresolved_properties", "undetected_entities",
    "secret_entity_ids", "event_candidates", "authorization_binding",
})
GOOD_HASH = set("0123456789abcdef")
OUTCOMES = frozenset({"PASS", "FAIL", "BLOCKED", "NO_EJECUTADO"})


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def reference_fixture(path: Path = ACCEPTANCE) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _issue(errors: list[str], code: str) -> None:
    if code not in errors:
        errors.append(code)


def _validate_events(record: dict, errors: list[str]) -> None:
    events = record.get("events")
    if not isinstance(events, list) or not events:
        _issue(errors, "EVENTS_MISSING")
        return
    seen: set[str] = set()
    sequence: list[str] = []
    named: dict[str, dict] = {}
    event_types = set()
    for event in events:
        if not isinstance(event, dict):
            _issue(errors, "EVENT_MALFORMED")
            continue
        eid, etype = event.get("event_id"), event.get("event_type")
        if not nonempty(eid) or eid in seen:
            _issue(errors, "EVENT_ID_DUPLICATE_OR_INVALID")
            continue
        seen.add(eid)
        if not nonempty(etype):
            _issue(errors, "EVENT_TYPE_INVALID")
        else:
            event_types.add(etype)
        if event.get("candidate_only") is not None or event.get("requires_core_confirmation") is not None:
            _issue(errors, "CANDIDATE_EVENT_NOT_COMMITTED")
        provenance = event.get("provenance")
        if not isinstance(provenance, dict) or not provenance:
            _issue(errors, "EVENT_PROVENANCE_MISSING")
        elif any("reference" in str(x).lower() for x in provenance.values()):
            _issue(errors, "REFERENCE_EVENT_NOT_AUTHORITATIVE")
        if (not isinstance(event.get("scope"), dict)
                or not isinstance(event.get("actor_refs"), (dict, list))
                or not isinstance(event.get("subject_refs"), dict)
                or not isinstance(event.get("visibility"), dict)
                or not nonempty(event.get("occurred_at"))):
            _issue(errors, "EVENT_CONTRACT_FIELDS_MISSING")
        refs = event.get("causal_refs", [])
        if (not isinstance(refs, list) or
                any(not nonempty(ref) or ref not in seen for ref in refs)):
            _issue(errors, "CAUSAL_REFERENCE_NOT_PRIOR")
        if etype in CHAIN:
            if etype in named:
                _issue(errors, "DUPLICATE_REQUIRED_EVENT_TYPE")
            named[etype] = event
            sequence.append(etype)

    if sequence != list(CHAIN):
        _issue(errors, "ORDER_SCAN_REPORT_CHAIN_INVALID")
        return
    order = record.get("order", {})
    oid = order.get("order_id") if isinstance(order, dict) else None
    expected_order = (CHAIN[0], CHAIN[1], CHAIN[4])
    for name in expected_order:
        if named[name].get("subject_refs", {}).get("order_id") != oid or not nonempty(oid):
            _issue(errors, "ORDER_REFERENCE_MISMATCH")
    action = named["ACTION_STARTED"].get("subject_refs", {})
    result = named["RESULT_CREATED"].get("subject_refs", {})
    report = named["REPORT_MADE"].get("subject_refs", {})
    if (not nonempty(action.get("operation_id"))
            or result.get("operation_id") != action.get("operation_id")):
        _issue(errors, "OPERATION_REFERENCE_MISMATCH")
    if (not nonempty(result.get("result_id"))
            or report.get("result_id") != result.get("result_id")):
        _issue(errors, "RESULT_REFERENCE_MISMATCH")
    if (named["ORDER_ISSUED"]["event_id"]
            not in named["ORDER_ACKNOWLEDGED"].get("causal_refs", [])):
        _issue(errors, "ORDER_ACK_CAUSALITY_MISSING")
    if (named["ACTION_STARTED"]["event_id"]
            not in named["RESULT_CREATED"].get("causal_refs", [])):
        _issue(errors, "SCAN_RESULT_CAUSALITY_MISSING")
    if (named["RESULT_CREATED"]["event_id"]
            not in named["REPORT_MADE"].get("causal_refs", [])):
        _issue(errors, "REPORT_CAUSALITY_MISSING")


def _validate_projection(value: Any, errors: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in BANNED_PUBLIC_KEYS:
                _issue(errors, "PUBLIC_PROJECTION_CONTAINS_HIDDEN_FIELDS")
            _validate_projection(child, errors)
    elif isinstance(value, list):
        for child in value:
            _validate_projection(child, errors)


def _validate_checkpoint(record: dict, errors: list[str]) -> None:
    state = record.get("save_load")
    if not isinstance(state, dict):
        _issue(errors, "SAVE_LOAD_EVIDENCE_MISSING")
        return
    before, after = state.get("before"), state.get("after")
    if not isinstance(before, dict) or not isinstance(after, dict):
        _issue(errors, "SAVE_LOAD_EVIDENCE_MISSING")
        return
    for name in ("entity_ids", "known_contact_ids", "event_ids",
                 "pending_order_ids", "campaign_seed", "observer_id"):
        a, b = before.get(name), after.get(name)
        if a is None or b is None or a != b:
            _issue(errors, "SAVE_LOAD_CONTINUITY_FAILURE:" + name)
        if name.endswith("_ids"):
            if (not isinstance(a, list) or not isinstance(b, list)
                    or any(not nonempty(x) for x in a + b)
                    or len(a) != len(set(a)) or len(b) != len(set(b))):
                _issue(errors, "SAVE_LOAD_INVALID_IDENTITIES:" + name)
    old, new = before.get("revision"), after.get("revision")
    if type(old) is not int or type(new) is not int or old < 0 or new < old:
        _issue(errors, "SAVE_LOAD_REVISION_INVALID")


def _validate_artifacts(record: dict, folder: Path | None, errors: list[str]) -> None:
    evidence = record.get("artifacts")
    if not isinstance(evidence, dict) or not REQUIRED_ARTIFACTS <= evidence.keys():
        _issue(errors, "ARTIFACTS_INCOMPLETE")
        return
    if folder is None:
        _issue(errors, "ARTIFACT_BASE_DIRECTORY_MISSING")
        return
    base = folder.resolve()
    for name in REQUIRED_ARTIFACTS:
        artifact = evidence[name]
        if not isinstance(artifact, dict):
            _issue(errors, "ARTIFACT_MALFORMED:" + name)
            continue
        rel, expected = artifact.get("path"), artifact.get("sha256")
        if (not nonempty(rel) or
                not nonempty(expected) or
                len(expected) != 64 or
                not set(expected) <= GOOD_HASH):
            _issue(errors, "ARTIFACT_METADATA_INVALID:" + name)
            continue
        relative = Path(rel)
        if relative.is_absolute() or any(part in (".", "..") for part in relative.parts):
            _issue(errors, "ARTIFACT_PATH_UNSAFE:" + name)
            continue
        candidate = (base / relative).resolve()
        if not candidate.is_relative_to(base) or not candidate.is_file():
            _issue(errors, "ARTIFACT_MISSING_OR_OUTSIDE_ROOT:" + name)
            continue
        digest = hashlib.sha256()
        size = 0
        try:
            with candidate.open("rb") as file:
                for chunk in iter(lambda: file.read(1024 * 1024), b""):
                    size += len(chunk)
                    digest.update(chunk)
        except OSError:
            _issue(errors, "ARTIFACT_UNREADABLE:" + name)
            continue
        if size == 0 or digest.hexdigest() != expected:
            _issue(errors, "ARTIFACT_INTEGRITY_FAILURE:" + name)


def validate_capture(record: Any, *,
                     artifact_dir: Path | None = None,
                     fixture: dict | None = None) -> dict[str, Any]:
    """Check *self-reported* execution and file integrity; no runtime certification."""
    errors: list[str] = []
    fixture = reference_fixture() if fixture is None else fixture
    if not isinstance(record, dict):
        return {"verdict": "BLOCKED", "problems": ["INVALID_RECORD"],
                "runtime_certified": False}
    expected = {item["id"] for item in fixture["must_pass"]}
    cases = record.get("cases")
    if not isinstance(cases, dict) or set(cases) != expected:
        _issue(errors, "ACCEPTANCE_CASE_IDS_MISMATCH")
    else:
        for name in sorted(expected):
            case = cases[name]
            if (not isinstance(case, dict) or case.get("status") not in OUTCOMES
                    or not isinstance(case.get("evidence_ids"), list)):
                _issue(errors, "ACCEPTANCE_CASE_INVALID:" + name)
                continue
            if case["status"] == "PASS" and not case["evidence_ids"]:
                _issue(errors, "PASS_WITHOUT_EVIDENCE:" + name)
            if case["status"] in ("FAIL", "BLOCKED"):
                _issue(errors, "CASE_NOT_PASSED:" + name)
    if record.get("fixture_id") != fixture.get("fixture_id"):
        _issue(errors, "FIXTURE_ID_MISMATCH")
    if record.get("campaign_context") != fixture.get("campaign_context"):
        _issue(errors, "CAMPAIGN_CONTEXT_MISMATCH")
    if record.get("execution_kind") != "core_ue5_runtime":
        _issue(errors, "NO_CORE_UE5_RUNTIME_DECLARED")
    env = record.get("environment")
    if not isinstance(env, dict) or any(
        not nonempty(env.get(field)) for field in
        ("trek_commit", "core_commit", "ue_version", "map_name", "build_hash",
         "msi_model", "build_type")
    ):
        _issue(errors, "RUNTIME_ENVIRONMENT_INCOMPLETE")
    elif env.get("msi_model") != "MSI Raider GE78 HX 14V":
        _issue(errors, "MSI_PLATFORM_NOT_CONFIRMED")
    order = record.get("order")
    if not isinstance(order, dict) or not all(
        nonempty(order.get(name)) for name in
        ("order_id", "issuer_character_id", "recipient_character_id")
    ):
        _issue(errors, "ORDER_IDENTITIES_MISSING")
    elif (not isinstance(order.get("authorization"), dict)
          or order["authorization"].get("checked_by") != "CoreRPG"
          or order["authorization"].get("decision") != "allow"
          or order["authorization"].get("validated") is not True):
        _issue(errors, "CORE_ORDER_AUTHORIZATION_UNVERIFIED")
    _validate_events(record, errors)
    projection = record.get("public_projection")
    if not isinstance(projection, dict):
        _issue(errors, "PUBLIC_PROJECTION_MISSING")
    else:
        _validate_projection(projection, errors)
    _validate_checkpoint(record, errors)
    _validate_artifacts(record, artifact_dir, errors)
    valid_case_evidence = isinstance(cases, dict) and isinstance(record.get("artifacts"), dict)
    if valid_case_evidence:
        for key, case in cases.items():
            if isinstance(case, dict) and case.get("status") == "PASS":
                if any(ref not in record["artifacts"] for ref in case.get("evidence_ids", [])):
                    _issue(errors, "PASS_EVIDENCE_REFERENCE_UNKNOWN:" + key)
    all_pass = isinstance(cases, dict) and set(cases) == expected and all(
        isinstance(case, dict) and case.get("status") == "PASS"
        for case in cases.values()
    )
    # Nunca emitir ACCEPTED: lectura de fichero no demuestra ejecución ni autoría.
    verdict = ("READY_FOR_MANUAL_REVIEW" if not errors and all_pass
               else "BLOCKED" if not errors else "INCONSISTENT")
    return {"verdict": verdict, "problems": errors,
            "runtime_certified": False, "acceptance_pass_claims": all_pass}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--capture", required=True, type=Path)
    parser.add_argument("--artifacts-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        record = json.loads(args.capture.read_text(encoding="utf-8"))
        answer = validate_capture(record, artifact_dir=args.artifacts_dir)
    except (OSError, ValueError, UnicodeError) as exc:
        answer = {"verdict": "INCONSISTENT", "problems": ["CAPTURE_UNREADABLE:" + str(exc)],
                  "runtime_certified": False}
    print(json.dumps(answer, indent=2, ensure_ascii=False, sort_keys=True))
    return 0 if answer["verdict"] == "READY_FOR_MANUAL_REVIEW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
