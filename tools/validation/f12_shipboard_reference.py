#!/usr/bin/env python3
"""F12: referencia offline de vida a bordo. NO es CoreRPG ni escribe World State.

Los datos de entrada son fixtures NO AUTENTICADOS. REVIEW_REQUIRED sólo solicita
revisión por Core/Host; nunca constituye consentimiento, orden o mutación real.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOCKED = "BLOCKED"
REVIEW = "REVIEW_REQUIRED"
NO_CHANGE = "NO_CHANGE"
AUTHORITY = "OFFLINE_REFERENCE_ONLY_NO_MUTATION"
SOCIAL = frozenset(("social_meal", "friendship_social_visit", "lounge_or_common_room"))
SOCIAL_EVENTS = frozenset(("first_meeting", "repeated_encounter", "shared_duty",
                          "successful_collaboration", "social_activity",
                          "romantic_expression", "romantic_rejection",
                          "consensual_intimacy", "relationship_commitment"))
ROMANTIC = frozenset(("romantic_expression", "romantic_rejection",
                       "consensual_intimacy", "relationship_commitment"))
CONTEXTUAL_CONSENT = frozenset(("consensual_intimacy", "relationship_commitment"))


def outcome(status, *reasons, **details):
    return {"status": status, "reasons": sorted(set(reasons)),
            "authority": AUTHORITY, **details}


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def ids(value, nonempty=True):
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(nonblank(v) for v in value) and len(value) == len(set(value)))


def valid_minute(value):
    return type(value) is int and 0 <= value <= 100_000_000


def validate_world(world):
    if not isinstance(world, dict) or not isinstance(world.get("ships"), dict):
        raise ValueError("invalid_ships")
    people = world.get("characters")
    if not isinstance(people, dict) or not people:
        raise ValueError("invalid_characters")
    for key, p in people.items():
        if not nonblank(key) or not isinstance(p, dict) or p.get("character_id") != key:
            raise ValueError("identity_mismatch")
        if p.get("ship_id") not in world["ships"] or not nonblank(p.get("location_id")):
            raise ValueError("invalid_assignment")
        if type(p.get("adult_equivalent")) is not bool or p.get("sex_category") not in ("male", "female", "other"):
            raise ValueError("invalid_age_or_sex")
        if type(p.get("player")) is not bool or p.get("lod") not in ("A", "B", "C"):
            raise ValueError("invalid_player_or_lod")
        if not isinstance(p.get("blocks"), list):
            raise ValueError("invalid_schedule")
        ordered = sorted(p["blocks"], key=lambda x: x.get("start", -1) if isinstance(x, dict) else -1)
        prior = -1
        for b in ordered:
            if (not isinstance(b, dict) or not valid_minute(b.get("start"))
                    or not valid_minute(b.get("end")) or b["start"] >= b["end"]
                    or not nonblank(b.get("family")) or b["start"] < prior):
                raise ValueError("invalid_or_overlapping_existing_schedule")
            prior = b["end"]
    for ship in world["ships"].values():
        if not isinstance(ship, dict) or not isinstance(ship.get("locations"), dict):
            raise ValueError("invalid_ship_locations")
        for loc in ship["locations"].values():
            if (not isinstance(loc, dict) or type(loc.get("capacity")) is not int
                    or loc["capacity"] < 1 or not ids(loc.get("activities", []), False)):
                raise ValueError("invalid_facility")
    return True


def screen_activity(world, req):
    """P02: cribado conservador sin reservas ni desplazamientos automáticos."""
    try:
        validate_world(world)
    except (ValueError, TypeError):
        return outcome(BLOCKED, "invalid_world")
    if not isinstance(req, dict):
        return outcome(BLOCKED, "invalid_request")
    if (not nonblank(req.get("activity_id")) or not nonblank(req.get("ship_id"))
            or not nonblank(req.get("location_id")) or not nonblank(req.get("activity_type"))
            or not ids(req.get("participants")) or not valid_minute(req.get("start"))
            or not valid_minute(req.get("end")) or req["start"] >= req["end"]):
        return outcome(BLOCKED, "invalid_activity")
    participants = req["participants"]
    ship = world["ships"].get(req["ship_id"])
    if not ship:
        return outcome(BLOCKED, "unknown_ship")
    loc = ship["locations"].get(req["location_id"])
    if not loc or req["activity_type"] not in loc["activities"]:
        return outcome(BLOCKED, "missing_ship_facility")
    if len(participants) > loc["capacity"]:
        return outcome(BLOCKED, "facility_capacity")
    consented = req.get("accepted_participants", [])
    if not ids(consented, False) or not set(consented).issubset(participants):
        return outcome(BLOCKED, "invalid_acceptance_record")
    if req["activity_type"] in SOCIAL and set(consented) != set(participants):
        return outcome(BLOCKED, "missing_explicit_participant_acceptance")
    for pid in participants:
        p = world["characters"].get(pid)
        if p is None:
            return outcome(BLOCKED, "unknown_participant")
        if p["ship_id"] != req["ship_id"]:
            return outcome(BLOCKED, "participant_not_on_ship")
        if p["location_id"] != req["location_id"]:
            return outcome(BLOCKED, "travel_not_verified")
        for block in p["blocks"]:
            if req["start"] < block["end"] and block["start"] < req["end"]:
                return outcome(BLOCKED, "schedule_conflict", blocking_family=block["family"])
    return outcome(REVIEW, "requires_core_host_authorization",
                   activity_id=req["activity_id"], participants=participants)


def screen_social_event(world, evt):
    """P03: contacto y cambios son candidatos; la ubicación no causa amistad."""
    try:
        validate_world(world)
    except (ValueError, TypeError):
        return outcome(BLOCKED, "invalid_world")
    if not isinstance(evt, dict) or evt.get("event_type") not in SOCIAL_EVENTS:
        return outcome(BLOCKED, "invalid_event_type")
    people = evt.get("participants")
    if (not ids(people) or len(people) != 2 or not nonblank(evt.get("event_id"))
            or not nonblank(evt.get("cause_event_ref")) or not valid_minute(evt.get("minute"))
            or not nonblank(evt.get("shared_location_ref"))):
        return outcome(BLOCKED, "missing_event_provenance")
    a, b = (world["characters"].get(pid) for pid in people)
    if not a or not b:
        return outcome(BLOCKED, "unknown_participant")
    # Un encuentro fuera de escena exige una causa verificable, no proximidad o LOD.
    if a["ship_id"] != b["ship_id"] and not nonblank(evt.get("travel_or_contact_ref")):
        return outcome(BLOCKED, "contact_not_plausible")
    kind = evt["event_type"]
    if kind in ROMANTIC:
        if not (a["adult_equivalent"] and b["adult_equivalent"]):
            return outcome(BLOCKED, "adults_only")
        if {a["sex_category"], b["sex_category"]} != {"male", "female"}:
            return outcome(BLOCKED, "project_romantic_pair_eligibility")
        # El interés del jugador es una acción expresa, no se infiere de la IA.
        player_ids = {x["character_id"] for x in (a, b) if x["player"]}
        actions = evt.get("explicit_player_action_ids", [])
        if not ids(actions, False) or not player_ids.issubset(actions):
            return outcome(BLOCKED, "missing_player_action")
        if kind in CONTEXTUAL_CONSENT:
            consent = evt.get("explicit_consent_ids", [])
            if not ids(consent, False) or set(consent) != set(people):
                return outcome(BLOCKED, "missing_contextual_consent")
    # No hay recompensas sociales por co-localización ni por una mera petición.
    allowed_changes = {
        "first_meeting": ["familiarity"],
        "repeated_encounter": ["familiarity"],
        "shared_duty": ["familiarity"],
        "successful_collaboration": ["professional_respect"],
    }.get(kind, [])
    return outcome(REVIEW, "causal_event_requires_core_validation",
                   candidate_dimensions=allowed_changes, event_id=evt["event_id"])


def project_event_for_npc(evt, observer_id):
    """P03: un testigo ve ocurrencia, no conversaciones íntimas ni graph global."""
    if not isinstance(evt, dict) or not nonblank(observer_id):
        return None
    if not nonblank(evt.get("event_id")) or not ids(evt.get("participants")):
        return None
    if observer_id in evt["participants"]:
        return {"event_id": evt["event_id"], "level": "participant",
                "known_event_type": evt.get("event_type")}
    witnesses = evt.get("witnesses", [])
    if not ids(witnesses, False):
        return None
    if observer_id in witnesses:
        return {"event_id": evt["event_id"], "level": "witness",
                "known_event_type": "interaction_occurred"}
    return None


def replay_reference(world, stream, months):
    """P05: referencia de meses con causalidad explícita y traslados, sin World State."""
    try:
        validate_world(world)
    except (ValueError, TypeError):
        return outcome(BLOCKED, "invalid_world")
    if type(months) is not int or not 1 <= months <= 24 or not isinstance(stream, list):
        return outcome(BLOCKED, "invalid_horizon")
    state = copy.deepcopy(world)
    relationships = {}
    memories = {key: [] for key in state["characters"]}
    seen = set()
    previous = -1
    audit = []
    for evt in stream:
        if not isinstance(evt, dict) or not nonblank(evt.get("event_id")):
            return outcome(BLOCKED, "invalid_stream_event")
        eid = evt["event_id"]
        minute = evt.get("minute")
        if (eid in seen or not valid_minute(minute) or minute < previous
                or minute >= months * 30 * 24 * 60 or not nonblank(evt.get("cause_event_ref"))):
            return outcome(BLOCKED, "duplicate_or_disordered_or_unproven_event")
        seen.add(eid)
        previous = minute
        if evt.get("event_type") == "transfer":
            who = evt.get("character_id")
            new_ship = evt.get("new_ship_id")
            new_loc = evt.get("new_location_id")
            if (who not in state["characters"] or new_ship not in state["ships"]
                    or new_loc not in state["ships"][new_ship]["locations"]):
                return outcome(BLOCKED, "invalid_transfer")
            state["characters"][who]["ship_id"] = new_ship
            state["characters"][who]["location_id"] = new_loc
            audit.append({"event_id": eid, "kind": "transfer"})
            continue
        checked = screen_social_event(state, evt)
        if checked["status"] != REVIEW:
            return outcome(BLOCKED, "invalid_social_event", detail=checked["reasons"])
        a, b = evt["participants"]
        dimension = checked["candidate_dimensions"]
        for observer, subject in ((a, b), (b, a)):
            edge_key = observer + "->" + subject
            edge = relationships.setdefault(edge_key, {"event_refs": [], "dimensions": {}})
            edge["event_refs"].append(eid)
            for d in dimension:
                # Una dimensión tiene procedencia, no un baremo numérico universal.
                edge["dimensions"].setdefault(d, []).append(eid)
            memories[observer].append(eid)
        audit.append({"event_id": eid, "kind": "social_reference"})
    digest = hashlib.sha256(json.dumps(
        {"state": state, "relations": relationships, "memories": memories, "audit": audit},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()
    return outcome(REVIEW, "not_a_core_save_or_authorized_evolution",
                   elapsed_months=months, identities=sorted(state["characters"]),
                   assignments={k: v["ship_id"] for k, v in sorted(state["characters"].items())},
                   relationship_evidence=relationships, memories_by_owner=memories,
                   processed_events=len(audit), sha256=digest)


def render_lod_plan(world, scene_ship, scene_location, budget):
    """P04: solo selección visual, sin tocar identidad, horarios ni memoria."""
    try:
        validate_world(world)
    except (ValueError, TypeError):
        return outcome(BLOCKED, "invalid_world")
    if (not nonblank(scene_ship) or not nonblank(scene_location)
            or type(budget) is not int or budget < 0):
        return outcome(BLOCKED, "invalid_render_request")
    priority = {"A": 0, "B": 1, "C": 2}
    visible = sorted((
        p for p in world["characters"].values()
        if p["ship_id"] == scene_ship and p["location_id"] == scene_location
    ), key=lambda p: (priority[p["lod"]], p["character_id"]))
    return outcome(REVIEW, "representation_only_no_materialization",
                   actors=[p["character_id"] for p in visible[:budget]],
                   not_rendered=[p["character_id"] for p in visible[budget:]],
                   persistent_population=len(world["characters"]))


def run_scenarios(path):
    fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    world = fixture["world"]
    failures, results = [], []
    for case in fixture["cases"]:
        kind = case["operation"]
        if kind == "activity":
            got = screen_activity(world, case["input"])
        elif kind == "social":
            got = screen_social_event(world, case["input"])
        elif kind == "projection":
            view = project_event_for_npc(case["input"]["event"], case["input"]["observer"])
            got = {"status": "VISIBLE" if view else "HIDDEN"}
        elif kind == "replay":
            got = replay_reference(world, case["input"]["events"], case["input"]["months"])
        elif kind == "lod":
            args = case["input"]
            got = render_lod_plan(world, args["ship"], args["location"], args["budget"])
        else:
            raise ValueError("unknown_operation")
        ok = got["status"] == case["expected_status"]
        if "expected_reason" in case:
            ok = ok and case["expected_reason"] in got.get("reasons", [])
        results.append({"id": case["id"], "ok": ok, "actual": got["status"]})
        if not ok:
            failures.append(case["id"])
    result = {"scope": AUTHORITY, "scenario_count": len(results),
              "passed": sum(x["ok"] for x in results), "failed_ids": failures,
              "results": results}
    result["sha256"] = hashlib.sha256(json.dumps(
        result, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = run_scenarios(args.scenario)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": report["scenario_count"], "passed": report["passed"],
                      "sha256": report["sha256"]}))
    if report["failed_ids"]:
        raise SystemExit("F12 FAILED: " + ", ".join(report["failed_ids"]))
