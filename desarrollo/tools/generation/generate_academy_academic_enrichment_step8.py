#!/usr/bin/env python3
"""Deterministic reference academic-enrichment registration planner for Academy Life Step 8."""
from __future__ import annotations
import argparse, copy, hashlib, heapq, json
from pathlib import Path
from typing import Any

RULES_VERSION = "academy_academic_enrichment_v0.1"
VALID_TYPES = {"conference", "seminar", "additional_course"}

def stable_hex(*parts: Any, size: int = 16) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:size]

def make_graph(request: dict[str, Any]) -> dict[str, list[tuple[str, int]]]:
    g: dict[str, list[tuple[str, int]]] = {}
    for edge in request.get("travel_edges", []):
        a, b, minutes = edge["from"], edge["to"], int(edge["minutes"])
        if minutes < 0:
            raise ValueError("negative travel time")
        g.setdefault(a, []).append((b, minutes))
        if edge.get("bidirectional", True):
            g.setdefault(b, []).append((a, minutes))
    return g

def travel_minutes(g: dict[str, list[tuple[str, int]]], a: str, b: str) -> int | None:
    if a == b:
        return 0
    queue = [(0, a)]
    seen: dict[str, int] = {}
    while queue:
        distance, node = heapq.heappop(queue)
        if node in seen and seen[node] <= distance:
            continue
        seen[node] = distance
        if node == b:
            return distance
        for nxt, cost in g.get(node, []):
            heapq.heappush(queue, (distance + cost, nxt))
    return None

def eligible(cadet: dict[str, Any], offering: dict[str, Any]) -> bool:
    allowed_classes = offering.get("allowed_cadet_class_ids")
    if allowed_classes and cadet.get("cadet_class_id") not in allowed_classes:
        return False
    required_qualifications = set(offering.get("required_qualification_refs", []))
    if not required_qualifications.issubset(set(cadet.get("qualification_refs", []))):
        return False
    specializations = offering.get("required_specialization_ids")
    if specializations and cadet.get("specialization") not in specializations:
        return False
    prerequisite_courses = set(offering.get("required_completed_course_refs", []))
    if not prerequisite_courses.issubset(set(cadet.get("completed_course_refs", []))):
        return False
    return True

def sessions_feasible(
    slot: str,
    offering: dict[str, Any],
    windows: list[dict[str, Any]],
    g: dict[str, list[tuple[str, int]]],
) -> bool:
    for session in offering.get("sessions", []):
        start = int(session["start_minute"])
        end = int(session["end_minute"])
        if start >= end:
            raise ValueError("invalid offering session")
        location_ref = session.get("location_ref", offering["location_ref"])
        matched = False
        for window in windows:
            if window["population_slot_ref"] != slot or int(window["day_index"]) != int(session["day_index"]):
                continue
            inbound = travel_minutes(g, window["start_location_ref"], location_ref)
            outbound = travel_minutes(g, location_ref, window["end_location_ref"])
            if inbound is None or outbound is None:
                continue
            if (
                int(window["start_minute"]) + inbound <= start
                and end + outbound <= int(window["end_minute"])
            ):
                matched = True
                break
        if not matched:
            return False
    return True

def presenter_available(offering: dict[str, Any]) -> bool:
    if not offering.get("presenter_ref"):
        return False
    available = set(offering.get("presenter_available_session_ids", []))
    required = {session["session_id"] for session in offering.get("sessions", [])}
    return required.issubset(available)

def build_registrations(request: dict[str, Any]) -> dict[str, Any]:
    seed = request["campaign_seed"]
    cadets = copy.deepcopy(request["cadets"])
    offerings = copy.deepcopy(request["offerings"])
    windows = copy.deepcopy(request["available_windows"])
    locations = copy.deepcopy(request.get("locations", []))
    graph = make_graph(request)

    slots = [c["population_slot_ref"] for c in cadets]
    if len(slots) != len(set(slots)):
        raise ValueError("duplicate cadet population_slot_ref")
    by_slot = {c["population_slot_ref"]: c for c in cadets}

    for offering_id, offering in offerings.items():
        if offering.get("offering_type") not in VALID_TYPES:
            raise ValueError("invalid academic enrichment type")
        if int(offering.get("capacity", 0)) < 0:
            raise ValueError("negative offering capacity")

    location_caps = {x["location_ref"]: set(x.get("capability_tags", [])) for x in locations}
    existing = copy.deepcopy(request.get("existing_registrations", []))
    player_requests = {(x["population_slot_ref"], x["offering_id"]) for x in request.get("player_registration_requests", [])}
    max_regs = int(request.get("max_active_enrichment_registrations_per_cadet", 2))
    if max_regs < 0:
        raise ValueError("invalid registration limit")

    rosters = {oid: [] for oid in offerings}
    registrations: list[dict[str, Any]] = []
    schedule_entries: list[dict[str, Any]] = []
    waitlist: list[dict[str, Any]] = []
    player_options: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    active_count = {slot: 0 for slot in slots}

    def offering_feasible(slot: str, offering_id: str) -> tuple[bool, str | None]:
        offering = offerings[offering_id]
        if not eligible(by_slot[slot], offering):
            return False, "ineligible"
        caps = set(offering.get("required_location_capabilities", []))
        if not caps.issubset(location_caps.get(offering["location_ref"], set())):
            return False, "facility_unavailable"
        if not presenter_available(offering):
            return False, "presenter_unavailable"
        if not sessions_feasible(slot, offering, windows, graph):
            return False, "schedule_or_travel_conflict"
        return True, None

    def add_registration(slot: str, offering_id: str, source: str, registration_id: str | None = None) -> None:
        rosters[offering_id].append(slot)
        active_count[slot] += 1
        registrations.append({
            "registration_id": registration_id or f"enrich:{offering_id}:{slot}",
            "offering_id": offering_id,
            "population_slot_ref": slot,
            "registration_state": "registered",
            "source": source,
            "attendance_state": "unresolved",
            "completion_state": "not_evaluated",
            "academic_record_effect": "deferred_step_19",
            "automatic_relationship_effect": "none",
            "automatic_skill_or_grade_effect": "none",
        })

    for registration in sorted(existing, key=lambda x: (x["offering_id"], x["population_slot_ref"])):
        slot = registration["population_slot_ref"]
        offering_id = registration["offering_id"]
        if slot not in by_slot or offering_id not in offerings:
            raise ValueError("existing registration references unknown entity")
        if registration.get("registration_state", "registered") != "registered":
            continue
        ok, reason = offering_feasible(slot, offering_id)
        if not ok:
            rejected.append({
                "population_slot_ref": slot,
                "offering_id": offering_id,
                "reason": "existing_registration_invalid_" + str(reason),
            })
            continue
        if len(rosters[offering_id]) >= int(offerings[offering_id]["capacity"]):
            raise ValueError("existing registrations exceed offering capacity")
        if active_count[slot] >= max_regs:
            raise ValueError("existing registrations exceed cadet registration limit")
        add_registration(slot, offering_id, "existing_preserved", registration.get("registration_id"))

    def candidate_options(slot: str) -> list[tuple[str, int, str]]:
        cadet = by_slot[slot]
        affinities = (
            set(cadet.get("interest_refs", []))
            | set(cadet.get("branch_interest_ids", []))
            | set(cadet.get("academic_enrichment_preference_refs", []))
        )
        options = []
        for offering_id in sorted(offerings):
            if slot in rosters[offering_id]:
                continue
            ok, _ = offering_feasible(slot, offering_id)
            if not ok:
                continue
            score = len(affinities & set(offerings[offering_id].get("affinity_refs", [])))
            options.append((
                offering_id,
                score,
                stable_hex(seed, "enrichment", slot, offering_id, RULES_VERSION),
            ))
        return sorted(options, key=lambda x: (-x[1], x[2], x[0]))

    for slot in sorted(slots):
        if not by_slot[slot].get("is_player", False):
            continue
        for offering_id, score, _ in candidate_options(slot):
            state = "eligible_option" if len(rosters[offering_id]) < int(offerings[offering_id]["capacity"]) else "waitlist_only"
            player_options.append({
                "population_slot_ref": slot,
                "offering_id": offering_id,
                "affinity_score": score,
                "state": state,
            })
        for offering_id in sorted(oid for s, oid in player_requests if s == slot):
            if offering_id not in offerings:
                rejected.append({"population_slot_ref": slot, "offering_id": offering_id, "reason": "unknown_offering"})
                continue
            if active_count[slot] >= max_regs:
                rejected.append({"population_slot_ref": slot, "offering_id": offering_id, "reason": "registration_limit"})
                continue
            ok, reason = offering_feasible(slot, offering_id)
            if not ok:
                rejected.append({"population_slot_ref": slot, "offering_id": offering_id, "reason": reason})
                continue
            if slot in rosters[offering_id]:
                continue
            if len(rosters[offering_id]) >= int(offerings[offering_id]["capacity"]):
                waitlist.append({
                    "population_slot_ref": slot,
                    "offering_id": offering_id,
                    "source": "explicit_player_request",
                    "state": "waitlisted",
                })
                continue
            add_registration(slot, offering_id, "explicit_player_choice")

    candidates = []
    for slot in sorted(slots):
        if by_slot[slot].get("is_player", False) or active_count[slot] >= max_regs:
            continue
        for offering_id, score, tie in candidate_options(slot):
            candidates.append((-score, tie, slot, offering_id))
    newly_registered_npcs: set[str] = set()
    for _, __, slot, offering_id in sorted(candidates):
        if slot in newly_registered_npcs or active_count[slot] >= max_regs or slot in rosters[offering_id]:
            continue
        if len(rosters[offering_id]) >= int(offerings[offering_id]["capacity"]):
            waitlist.append({
                "population_slot_ref": slot,
                "offering_id": offering_id,
                "source": "npc_autonomous",
                "state": "waitlisted",
            })
            newly_registered_npcs.add(slot)
            continue
        add_registration(slot, offering_id, "npc_autonomous")
        newly_registered_npcs.add(slot)

    for registration in registrations:
        offering = offerings[registration["offering_id"]]
        for session in offering.get("sessions", []):
            schedule_entries.append({
                "entry_id": f'enrichment:{registration["offering_id"]}:{registration["population_slot_ref"]}:{session["session_id"]}',
                "population_slot_ref": registration["population_slot_ref"],
                "offering_id": registration["offering_id"],
                "entry_type": "academic_enrichment",
                "day_index": int(session["day_index"]),
                "start_minute": int(session["start_minute"]),
                "end_minute": int(session["end_minute"]),
                "location_ref": session.get("location_ref", offering["location_ref"]),
                "obligation_level": "voluntary_registered_commitment",
                "attendance_state": "unresolved",
            })

    return {
        "rules_version": RULES_VERSION,
        "registrations": sorted(registrations, key=lambda x: (x["population_slot_ref"], x["offering_id"])),
        "rosters": {oid: sorted(rosters[oid]) for oid in sorted(rosters)},
        "waitlist": sorted(waitlist, key=lambda x: (x["offering_id"], x["population_slot_ref"])),
        "schedule_entries": sorted(schedule_entries, key=lambda x: (x["population_slot_ref"], x["day_index"], x["start_minute"], x["offering_id"])),
        "player_eligible_options": sorted(player_options, key=lambda x: (x["population_slot_ref"], x["offering_id"])),
        "rejected_or_unresolved": sorted(rejected, key=lambda x: (x["population_slot_ref"], x["offering_id"], str(x["reason"]))),
        "registration_truth_semantics": "registration_not_attendance_or_completion",
        "completion_record_effect": "deferred_step_19",
        "automatic_relationship_effect": "none",
        "automatic_skill_grade_reputation_wellbeing_effect": "none",
        "future_step_state": {
            "social_events": [],
            "romance_state": [],
            "relationship_changes": [],
            "mentor_changes": [],
            "wellbeing_effects": [],
            "disciplinary_consequences": [],
            "campus_event_mutations": [],
            "offscreen_execution": [],
            "academy_record_writes": [],
        },
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(build_registrations(payload.get("request", payload)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
