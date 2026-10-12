#!/usr/bin/env python3
"""F04 reference-only Star Trek authorization and scheduling checks.

NOT a CoreRPG API, a runtime world-state engine, or a substitute for UE5 E2E.
All inputs are explicitly resolved state. Safe on incomplete input (deny).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ACTIONS = {
    "sensor_scan", "change_watch_policy", "assign_department_watch",
    "bridge_order", "relieve_command_medically", "first_contact",
}


def result(decision: str, code: str, **extra: object) -> dict:
    return {"decision": decision, "code": code, **extra}


def current_command(ctx: dict) -> bool:
    """Formal command appointment, or qualified and time-bound acting command."""
    if ctx.get("position") == "commanding_officer":
        return bool(ctx.get("appointment_active"))
    return all((
        ctx.get("acting_command"),
        ctx.get("acting_appointment_active"),
        ctx.get("command_qualified"),
    ))


def valid_delegation(ctx: dict, domain: str) -> bool:
    d = ctx.get("delegation") or {}
    t = ctx.get("now")
    if not (isinstance(t, int) and isinstance(d.get("starts_at"), int)
            and isinstance(d.get("ends_at"), int)):
        return False
    return all((
        d.get("from_authorized_commander") is True,
        d.get("to_actor") is True,
        d.get("domain") == domain,
        d.get("status") == "active",
        isinstance(t, int),
        isinstance(d.get("starts_at"), int),
        isinstance(d.get("ends_at"), int),
        d["starts_at"] <= t < d["ends_at"],
        ctx.get("control_mode") == "delegated_autonomous",
    ))


def evaluate(ctx: dict) -> dict:
    """Conservative policy sample. 'REVIEW' means no automatic execution."""
    action = ctx.get("action")
    if action not in ACTIONS:
        return result("DENY", "UNKNOWN_ACTION")
    if ctx.get("actor_active") is not True or ctx.get("actor_fit") is not True:
        return result("DENY", "UNAVAILABLE_ACTOR")
    if ctx.get("safety_interlock") == "non_overrideable":
        return result("DENY", "HARD_INTERLOCK")
    if ctx.get("technical_available") is not True:
        return result("DENY", "CAPABILITY_UNAVAILABLE")

    if action == "sensor_scan":
        if not all((ctx.get("station") == "sensors", ctx.get("on_duty") is True,
                    ctx.get("assignment_active") is True, ctx.get("qualified") is True)):
            return result("DENY", "SENSOR_STATION_OR_QUALIFICATION")
        return result("ALLOW", "SENSOR_OPERATION")

    if action == "relieve_command_medically":
        if ctx.get("position") != "chief_medical_officer" or not all((
                ctx.get("appointment_active") is True,
                ctx.get("professional_qualified") is True,
                ctx.get("medical_judgement_documented") is True,
                ctx.get("target_medically_unfit") is True)):
            return result("DENY", "MEDICAL_AUTHORITY_OR_EVIDENCE")
        return result("ALLOW", "MEDICAL_RELIEF", transfers_command=False,
                      effect="activate_normal_succession")

    if action == "assign_department_watch":
        if not all((ctx.get("position") == "department_head",
                    ctx.get("appointment_active") is True,
                    ctx.get("qualified") is True,
                    ctx.get("department") is not None,
                    ctx.get("department") == ctx.get("target_department"))):
            return result("DENY", "OUTSIDE_DEPARTMENT")
        return result("ALLOW", "DEPARTMENT_SCOPE")

    if action == "bridge_order":
        if current_command(ctx):
            return result("ALLOW", "COMMAND_APPOINTMENT")
        if all((ctx.get("position") == "officer_of_watch",
                ctx.get("watch_active") is True,
                ctx.get("appointment_active") is True,
                ctx.get("command_qualified") is True,
                ctx.get("within_standing_orders") is True)):
            return result("ALLOW", "WATCH_SCOPE")
        return result("DENY", "NOT_IN_BRIDGE_WATCH_AUTHORITY")

    # Remaining two actions require actual command appointment or bounded delegation.
    domain = "watch_policy" if action == "change_watch_policy" else "first_contact_policy"
    own = current_command(ctx)
    if not own and not valid_delegation(ctx, domain):
        return result("DENY", "COMMAND_APPOINTMENT_REQUIRED")
    if ctx.get("control_mode") == "proposal_requires_approval" and not own:
        return result("DENY", "CAPTAIN_APPROVAL_REQUIRED")
    if ctx.get("control_mode") == "proposal_requires_approval" and own:
        if ctx.get("proposal_approved") is not True:
            return result("REVIEW", "PENDING_CAPTAIN_APPROVAL")
    if action == "first_contact":
        # Canon: Prime Directive is not an unconditional hard block.
        if ctx.get("higher_order_conflict") is True:
            return result("REVIEW", "HIGHER_ORDER_CONFLICT",
                          consequence="explicit_disobedience_process")
        if ctx.get("prime_directive_risk") is True:
            return result("REVIEW", "PRIME_DIRECTIVE_RISK",
                          consequence="document_and_assess_interference")
        if ctx.get("contact_authorized") is not True:
            return result("REVIEW", "CONTACT_AUTHORIZATION_REQUIRED")
        return result("ALLOW", "CONTACT_WITHIN_MISSION")
    if ctx.get("staffing_valid") is not True:
        return result("DENY", "INVALID_WATCH_COVERAGE")
    if ctx.get("higher_order_conflict") is True:
        return result("REVIEW", "HIGHER_ORDER_CONFLICT",
                      consequence="explicit_disobedience_process")
    return result("ALLOW", "VALID_WATCH_POLICY")



def issue_reference_binding(ctx: dict, *, actor_id: str, action_id: str,
                            station_id: str, state_revision: int,
                            issued_tick: int, expires_tick: int) -> dict | None:
    """Puente de TEST F04->F05, NO acredita credenciales reales de Core.

    Las identidades/tiempos proceden del harness de referencia. Un Host o IA
    no pueden certificar por sí mismos esta estructura en producción.
    """
    if (not all(isinstance(x, str) and x for x in (actor_id, action_id, station_id))
        or type(state_revision) is not int or state_revision < 0
        or type(issued_tick) is not int or type(expires_tick) is not int
        or issued_tick >= expires_tick or ctx.get("action") != action_id):
        return None
    if evaluate(ctx)["decision"] != "ALLOW":
        return None
    return {"source": "F04_REFERENCE", "decision": "ALLOW",
            "actor_id": actor_id, "action_id": action_id,
            "station_id": station_id, "state_revision": state_revision,
            "issued_tick": issued_tick, "expires_tick": expires_tick}


def check_roster(slots: list[dict], people: dict[str, dict],
                 assignments: list[dict]) -> list[str]:
    """Find missing slots, spurious crew, duplicated assignments and deficiencies."""
    errors: list[str] = []
    slots_by_id = {s["slot_id"]: s for s in slots}
    if len(slots_by_id) != len(slots):
        errors.append("DUPLICATED_SLOT")
    seen_slots: set[str] = set()
    seen_people: set[str] = set()
    for a in assignments:
        slot, person_id = a["slot_id"], a["character_id"]
        if slot not in slots_by_id:
            errors.append("UNKNOWN_SLOT:" + slot)
            continue
        if slot in seen_slots:
            errors.append("DOUBLE_FILLED_SLOT:" + slot)
        seen_slots.add(slot)
        if person_id in seen_people:
            errors.append("DOUBLE_ASSIGNED_PERSON:" + person_id)
        seen_people.add(person_id)
        person = people.get(person_id)
        if person is None:
            errors.append("NONEXISTENT_CREW:" + person_id)
        elif not all((
            person.get("is_duty_crew") is True,
            person.get("aboard") is True,
            person.get("fit") is True,
            slots_by_id[slot].get("qualification") in person.get("qualifications", []),
        )):
            errors.append("INELIGIBLE_CREW:" + person_id)
    for s in slots:
        if s["slot_id"] not in seen_slots and s.get("continuous") is True:
            errors.append("UNCOVERED_CONTINUOUS_SLOT:" + s["slot_id"])
    return sorted(errors)


def check_schedule(items: list[dict]) -> list[str]:
    """Reference intervals: [start,end), incompatible overlap unless traced preemption."""
    errors: list[str] = []
    indexed: dict[str, dict] = {}
    for it in items:
        ident = it["id"]
        if ident in indexed:
            errors.append("DUPLICATED_ACTIVITY:" + ident)
        indexed[ident] = it
        if not isinstance(it.get("start"), int) or not isinstance(it.get("end"), int) or it["start"] >= it["end"]:
            errors.append("INVALID_WINDOW:" + ident)
    for n, a in enumerate(items):
        for b in items[n + 1:]:
            if a["character_id"] != b["character_id"]:
                continue
            if not (a.get("exclusive", True) and b.get("exclusive", True)):
                continue
            if a["start"] >= b["end"] or b["start"] >= a["end"]:
                continue
            preempted = (a, b) if a.get("preempted_by") == b["id"] else ((b, a) if b.get("preempted_by") == a["id"] else None)
            if preempted:
                interrupted, emergency = preempted
                if all((
                    emergency.get("kind") == "emergency",
                    bool(interrupted.get("preemption_event_id")),
                    isinstance(interrupted.get("fatigue_debt"), (int, float)),
                    isinstance(interrupted.get("fatigue_debt"), (int, float))
                    and interrupted["fatigue_debt"] > 0,
                )):
                    continue
            errors.append("INCOMPATIBLE_OVERLAP:" + ":".join(sorted((a["id"], b["id"]))))
    return sorted(errors)


def verify_fixture(path: Path) -> list[str]:
    fixture = json.loads(path.read_text(encoding="utf-8"))
    issues: list[str] = []
    for case in fixture["authority_cases"]:
        got = evaluate(case["context"])
        for key in ("decision", "code"):
            if got.get(key) != case["expected"][key]:
                issues.append(f"{case['id']}:{key}:{got.get(key)}!={case['expected'][key]}")
    for case in fixture["roster_cases"]:
        got = check_roster(case["slots"], case["people"], case["assignments"])
        if got != case["expected_errors"]:
            issues.append(f"{case['id']}:roster:{got}")
    for case in fixture["schedule_cases"]:
        got = check_schedule(case["items"])
        if got != case["expected_errors"]:
            issues.append(f"{case['id']}:schedule:{got}")
    return issues


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", type=Path, required=True)
    args = parser.parse_args()
    problems = verify_fixture(args.fixture)
    if problems:
        raise SystemExit("\n".join(problems))
    print("F04 reference fixture: PASS")
