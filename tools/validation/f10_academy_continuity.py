#!/usr/bin/env python3
"""F10 P03-P05: simulador OFFLINE de continuidad, NO autoridad CoreRPG/UE5.

Los contextos CORE_HOST_VERIFIED son STUBS suministrados por fixtures de QA.
Ningun campo de este modulo autentica identidad, prueba presencia fisica ni
concede una nota, grado o destino a una partida real.
Reutiliza los resolvedores aprobados de Academy Life 18 y 19.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACADEMY = ROOT / "gameplay/careers/academy_path"
VERSION = "f10_academy_continuity_reference_v0.1"
STAGES = frozenset({"theory", "instructor_class", "real_system_practice", "continuous_evaluation"})
PRACTICES = frozenset({"sensors_training", "kobayashi_maru"})
CANDIDATE = "candidate"


def _module(relative_path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Academy Life resolver unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _text(value: object) -> bool:
    return isinstance(value, str) and 0 < len(value) <= 128 and value == value.strip()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def new_candidate(cadet_ref: str, player_profile_ref: str) -> dict:
    _require(_text(cadet_ref) and _text(player_profile_ref), "candidate identity required")
    return {
        "schema_version": VERSION, "cadet_ref": cadet_ref,
        "player_profile_ref": player_profile_ref,
        "academy_status": CANDIDATE, "academic_year": 0,
        "year_results": [], "specialization": None,
        "commissioned": False, "rank": None, "first_assignment": None,
        "event_log": [], "record_events": [], "lesson_trace": [],
        "practice_trace": [], "social_trace": [], "relationship_refs": [],
        "mentor_refs": [], "disciplinary_refs": [],
        "scope": "offline_qa_only_not_a_core_save"
    }


def _check_host(snapshot: dict, command: dict, host: dict) -> str:
    _require(isinstance(command, dict) and isinstance(host, dict), "invalid command or host")
    event_ref = command.get("event_ref")
    _require(_text(event_ref), "event_ref required")
    _require(host.get("trusted_origin") == "CORE_HOST_VERIFIED", "offline host stub not present")
    _require(host.get("character_ref") == snapshot["cadet_ref"], "character identity mismatch")
    _require(_text(host.get("effective_date")), "event provenance date required")
    _require(event_ref not in {e["event_ref"] for e in snapshot["event_log"]}, "duplicate event_ref")
    return event_ref


def _is_verified(host: dict, ref: object) -> bool:
    refs = host.get("verified_evidence_refs")
    return _text(ref) and isinstance(refs, list) and all(_text(x) for x in refs) and len(refs) == len(set(refs)) and ref in refs


def _append(snapshot: dict, action: str, event_ref: str, host: dict, payload: dict, family: str | None = None) -> None:
    snapshot["event_log"].append({
        "event_ref": event_ref, "action": action,
        "effective_date": host["effective_date"],
        "year": snapshot["academic_year"], "payload": copy.deepcopy(payload)
    })
    if family:
        module = _module("tools/generation/integrate_academy_record_step19.py", "f10_step19")
        req = {
            "cadet_ref": snapshot["cadet_ref"], "is_player": True,
            "player_profile_ref": snapshot["player_profile_ref"],
            "existing_record_events": snapshot["record_events"],
            "evidence_events": [{
                "family": family, "source_event_id": event_ref, "confirmed": True,
                "effective_date": host["effective_date"], "authority_id": "OFFLINE_QA_STUB",
                "payload": copy.deepcopy(payload)
            }]
        }
        outcome = module.resolve(req)
        _require(not outcome["rejected_or_unresolved"] and len(outcome["appended_record_events"]) == 1,
                 "record integration declined event")
        snapshot["record_events"].extend(outcome["appended_record_events"])


def _course_ids(year: int) -> set[str]:
    manifest = json.loads((ACADEMY / "curriculum/curriculum_manifest_v1_0.json").read_text(encoding="utf-8"))
    annual = manifest["years"][year - 1]["manifest_ref"]
    data = json.loads((ACADEMY / "curriculum" / annual).read_text(encoding="utf-8"))
    return set(data["course_ids"])


def _branches() -> set[str]:
    content = json.loads((ACADEMY / "specializations.json").read_text(encoding="utf-8"))
    return {item["id"] for item in content["specializations"]}


def apply(snapshot: dict, command: dict, host: dict) -> dict:
    """Pure replay of already verified fixture decisions; NEVER write Core or UE5."""
    _require(isinstance(snapshot, dict) and snapshot.get("schema_version") == VERSION,
             "invalid snapshot")
    current = copy.deepcopy(snapshot)
    event_ref = _check_host(current, command, host)
    action = command.get("action")
    year = current["academic_year"]
    status = current["academy_status"]

    if action == "admit":
        _require(status == CANDIDATE and host.get("admission_authorized") is True,
                 "admission not authorized")
        current["academy_status"] = "cadet_year_1"
        current["academic_year"] = 1
        _append(current, action, event_ref, host, {"admitted": True}, "academy_admission")
    elif action == "lesson":
        _require(status == f"cadet_year_{year}" and year in (1, 2, 3, 4),
                 "not an active cadet")
        subject = command.get("subject_id")
        stage = command.get("stage")
        _require(_text(subject) and subject in _course_ids(year) and stage in STAGES,
                 "lesson course or stage unknown")
        _require(host.get("attendance_confirmed") is True, "attendance unconfirmed")
        detail = {"subject_id": subject, "stage": stage, "result": "attendance_only"}
        current["lesson_trace"].append({"event_ref": event_ref, **detail})
        _append(current, action, event_ref, host, detail)
    elif action == "practice":
        scenario = command.get("scenario_id")
        evidence = command.get("evidence_ref")
        _require(status == f"cadet_year_{year}" and year in (1, 2, 3, 4),
                 "not an active cadet")
        _require(scenario in PRACTICES and (scenario != "kobayashi_maru" or year == 4),
                 "practice outside catalog or capstone window")
        _require(host.get("simulation_resolved_in_core") is True and
                 host.get("practical_evaluation_confirmed") is True and
                 _is_verified(host, evidence), "unverified practical result")
        detail = {"scenario_id": scenario, "evidence_ref": evidence,
                  "outcome": "reviewed_external_evidence_only"}
        current["practice_trace"].append({"event_ref": event_ref, **detail})
        _append(current, action, event_ref, host, detail, "practical_evaluation")
    elif action == "social":
        _require(status == f"cadet_year_{year}" and year in (1, 2, 3, 4),
                 "social event outside Academy")
        _require(_text(command.get("npc_ref")) and host.get("social_event_confirmed") is True,
                 "unverified social event")
        detail = {"npc_ref": command["npc_ref"], "relation_effect": "none_by_default"}
        current["social_trace"].append({"event_ref": event_ref, **detail})
        _append(current, action, event_ref, host, detail)
    elif action == "choose_specialization":
        _require(year == 2 and status == "cadet_year_2" and current["specialization"] is None,
                 "specialization window closed")
        selection = command.get("specialization_id")
        _require(selection in _branches(), "unknown specialization")
        _require(host.get("selection_window_open") is True and
                 host.get("explicit_player_choice") is True, "not a player choice")
        current["specialization"] = selection
        _append(current, action, event_ref, host, {"specialization": selection},
                "specialization_selected")
    elif action == "complete_year":
        _require(status == f"cadet_year_{year}" and year in (1, 2, 3, 4),
                 "year is not active")
        _require(host.get("authorized_academic_review") is True and
                 _is_verified(host, command.get("evidence_ref")), "academic review not verified")
        if year == 2:
            _require(current["specialization"] in _branches() and
                     host.get("explicit_player_choice") is True,
                     "year 2 cannot activate year 3 without player choice")
        evidence = host.get("consolidated_evidence")
        _require(isinstance(evidence, dict) and evidence.get("period_complete") is True,
                 "academic period incomplete")
        resolver = _module("tools/generation/resolve_academy_year_progression_step18.py", "f10_step18")
        result = resolver.resolve({
            "academic_year": year, "is_player": True,
            "evidence": copy.deepcopy(evidence),
            "policy": {"allow_advance_with_remediation": False, "max_failed_modules_for_selected_repeat": 2},
            "specialization_selection": (
                {"specialization_id": current["specialization"], "explicit_player_choice": True}
                if year == 2 else None
            )
        })
        _require(result["outcome"] in {"advance", "graduation_pending"} and
                 result["activation_state"] == "resolved", "academic requirements not passed")
        current["year_results"].append(year)
        if year == 4:
            current["academy_status"] = "graduation_pending"
        else:
            current["academic_year"] = year + 1
            current["academy_status"] = f"cadet_year_{year + 1}"
        _append(current, action, event_ref, host,
                {"completed_year": year, "resolution": result["outcome"],
                 "evidence_ref": command["evidence_ref"]}, "academy_year_progression")
    elif action == "graduate":
        _require(status == "graduation_pending" and year == 4 and
                 current["year_results"] == [1, 2, 3, 4], "incomplete Academy path")
        _require(host.get("graduation_eligible") is True and
                 host.get("authorized_academic_review") is True and
                 _is_verified(host, command.get("evidence_ref")), "graduation not authorized")
        current["academy_status"] = "graduated"
        _append(current, action, event_ref, host,
                {"specialization": current["specialization"],
                 "evidence_ref": command["evidence_ref"]}, "academy_graduation")
    elif action == "commission":
        _require(status == "graduated" and not current["commissioned"],
                 "commission requires prior graduation")
        _require(host.get("commission_authorized") is True and
                 host.get("confirmed_graduation_event_ref") in
                 {e["event_ref"] for e in current["event_log"] if e["action"] == "graduate"},
                 "commission not confirmed")
        current["commissioned"] = True
        current["rank"] = "ensign"
        _append(current, action, event_ref, host,
                {"rank": "ensign", "graduation_ref": host["confirmed_graduation_event_ref"]},
                "commission")
    elif action == "assign_first_post":
        _require(status == "graduated" and current["commissioned"] and
                 current["first_assignment"] is None, "first posting prerequisites missing")
        order_ref = host.get("confirmed_orders_ref")
        position_ref = host.get("confirmed_position_ref")
        _require(host.get("posting_authorized") is True and
                 host.get("vacancy_confirmed") is True and
                 _text(order_ref) and _text(position_ref), "vacancy and orders required")
        current["first_assignment"] = {"orders_ref": order_ref,
                                       "position_ref": position_ref,
                                       "rank": "ensign"}
        _append(current, action, event_ref, host, current["first_assignment"])
    else:
        raise ValueError("unrecognized Academy action")
    return current


def seal(snapshot: dict) -> dict:
    _require(isinstance(snapshot, dict) and snapshot.get("schema_version") == VERSION,
             "snapshot invalid")
    return {"format": VERSION, "snapshot": copy.deepcopy(snapshot),
            "sha256": hashlib.sha256(_canonical(snapshot)).hexdigest()}


def restore(envelope: dict) -> dict:
    _require(isinstance(envelope, dict) and envelope.get("format") == VERSION,
             "invalid save format")
    snap = envelope.get("snapshot")
    _require(isinstance(snap, dict) and snap.get("schema_version") == VERSION,
             "invalid save snapshot")
    _require(hashlib.sha256(_canonical(snap)).hexdigest() == envelope.get("sha256"),
             "save checksum mismatch")
    refs = [e["event_ref"] for e in snap["event_log"]]
    _require(len(refs) == len(set(refs)), "duplicate event log IDs")
    _require(snap["year_results"] == list(range(1, len(snap["year_results"]) + 1)) and
             len(snap["year_results"]) <= 4, "invalid year order")
    _require(not snap["commissioned"] or
             (snap["academy_status"] == "graduated" and snap["rank"] == "ensign"),
             "invalid commission state")
    _require(snap["first_assignment"] is None or snap["commissioned"],
             "assignment without commission")
    return copy.deepcopy(snap)


def replay(payload: dict) -> dict:
    state = new_candidate(payload["cadet_ref"], payload["player_profile_ref"])
    for step in payload["steps"]:
        state = apply(state, step["command"], step["trusted_host_fixture"])
    return seal(state)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", type=Path, required=True)
    args = parser.parse_args()
    fixture = json.loads(args.scenario.read_text(encoding="utf-8"))
    print(json.dumps(replay(fixture), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
