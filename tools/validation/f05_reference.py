#!/usr/bin/env python3
"""F05 reference decision gate. NOT CoreRPG, NOT a WorldState implementation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

VERDICTS = {
    "ALLOW_REFERENCE", "CLARIFY", "REFUSE", "REVIEW", "WAIT_APPROVAL",
    "WAIT", "FALLBACK", "REPLAY", "PROPOSAL_ONLY", "REJECT_STALE"
}
PHASES = {"issue", "execute", "ai_response"}
CHANNELS = {"actor", "ai"}
AUTH = {"allow", "deny", "review"}
MODES = {"none", "manual", "proposal_requires_approval", "delegated_autonomous"}


def assess(case: dict) -> dict:
    """Classify a hypothetical command. No input mutation, IO or authoritative effects."""
    if not isinstance(case, dict):
        return _out("REFUSE", "invalid_payload")
    # Ninguna decisión incompleta puede producir ALLOW_REFERENCE.
    if case.get("phase") not in PHASES or case.get("channel") not in CHANNELS:
        return _out("REFUSE", "invalid_payload")
    if type(case.get("knowledge_visible")) is not bool:
        return _out("REFUSE", "incomplete_knowledge_evidence")
    if case["channel"] == "actor":
        if case.get("authority_verdict") not in AUTH:
            return _out("REFUSE", "missing_authority_verdict")
        required = ("appointment_active", "medical_fit")
        if case["phase"] == "execute":
            required += ("duty_active", "executor_qualified", "executor_authorized",
                         "capability_available", "resources_available", "temporal_conflict")
        if any(type(case.get(key)) is not bool for key in required):
            return _out("REFUSE", "incomplete_actor_evidence")
        if any(not isinstance(case.get(key), str) or not case[key].strip()
               for key in ("actor_id", "action_id", "station_id")):
            return _out("REFUSE", "missing_actor_action_station")
        if type(case.get("state_revision")) is not int or case["state_revision"] < 0:
            return _out("REFUSE", "invalid_state_revision")
        # Prueba de *consistencia de referencia*, nunca autenticación criptográfica.
        # Solo Core podrá emitir/verificar autorización realmente vinculante.
        if case["authority_verdict"] == "allow":
            b = case.get("authorization_binding")
            if not isinstance(b, dict) or any(b.get(k) != case.get(v) for k, v in (
                ("actor_id", "actor_id"), ("action_id", "action_id"),
                ("station_id", "station_id"), ("state_revision", "state_revision")
            )):
                return _out("REFUSE", "authority_binding_invalid")
            if b.get("source") != "F04_REFERENCE" or b.get("decision") != "ALLOW":
                return _out("REFUSE", "authority_binding_invalid")
            if (type(case.get("current_tick")) is not int or
                type(b.get("issued_tick")) is not int or
                type(b.get("expires_tick")) is not int or
                not b["issued_tick"] <= case["current_tick"] < b["expires_tick"]):
                return _out("REJECT_STALE", "authorization_expired_or_stale")
    if case.get("phase", "issue") not in PHASES or case.get("channel", "actor") not in CHANNELS:
        return _out("REFUSE", "invalid_payload")
    if case.get("authority_verdict", "allow") not in AUTH:
        return _out("REFUSE", "invalid_payload")
    if case.get("control_mode", "none") not in MODES:
        return _out("REFUSE", "invalid_payload")
    if case.get("direct_world_mutation", False):
        return _out("REFUSE", "direct_mutation_forbidden")

    # The LLM only proposes. Its answer alone is never an executable order.
    if case.get("channel", "actor") == "ai":
        if case.get("provider_status", "ok") in ("down", "timeout", "unavailable"):
            if case.get("fallback_authorized", False):
                return _out("FALLBACK", "deterministic_only")
            return _out("CLARIFY", "provider_unavailable")
        if case.get("provider_status", "ok") != "ok":
            return _out("REFUSE", "invalid_ai_response")
        if case.get("context_stale", False):
            return _out("REJECT_STALE", "stale_context")
        if not case.get("knowledge_visible", True):
            return _out("CLARIFY", "insufficient_knowledge")
        return _out("PROPOSAL_ONLY", "core_validation_required")

    # An actor re-submitting a completed attempt cannot repeat its effects.
    if case.get("phase", "issue") == "execute":
        if case.get("idempotency", "fresh") == "conflict":
            return _out("REFUSE", "idempotency_conflict")
        if case.get("idempotency", "fresh") == "same":
            return _out("REPLAY", "same_stored_result")
        if case.get("context_stale", False):
            return _out("REJECT_STALE", "stale_context")

    if case.get("clarification_needed", False):
        return _out("CLARIFY", "missing_information")
    if not case.get("knowledge_visible", True):
        return _out("CLARIFY", "insufficient_knowledge")
    if case.get("authority_verdict", "allow") == "review" or case.get("regulatory_review", False):
        return _out("REVIEW", "contextual_review")
    if case.get("authority_verdict", "allow") == "deny":
        return _out("REFUSE", "authority_denied")
    if not case.get("appointment_active", True):
        return _out("REFUSE", "appointment_inactive")
    if not case.get("medical_fit", True):
        return _out("REFUSE", "medical_unfit")
    if case.get("legal_prohibition", False):
        return _out("REFUSE", "legal_constraint")

    if case.get("delegation_required", False) and case.get("delegation_status", "none") != "active":
        return _out("REFUSE", "delegation_inactive")
    if case.get("delegation_required", False) and not case.get("within_delegation_scope", True):
        return _out("REFUSE", "delegation_scope")
    mode = case.get("control_mode", "none")
    if case.get("policy_change", False) and mode in ("manual", "proposal_requires_approval"):
        if not case.get("captain_approved", False) and case.get("issuer_role", "officer") != "captain":
            return _out("WAIT_APPROVAL", "captain_approval_required")

    if case.get("phase", "issue") == "execute":
        if case.get("deadline_expired", False):
            return _out("REFUSE", "deadline_expired")
        if not case.get("duty_active", True):
            return _out("REFUSE", "off_duty")
        if not case.get("executor_qualified", True):
            return _out("REFUSE", "executor_unqualified")
        if not case.get("executor_authorized", True):
            return _out("REFUSE", "executor_unauthorized")
        if not case.get("capability_available", True):
            return _out("REFUSE", "unavailable_capability")
        if not case.get("resources_available", True):
            return _out("REFUSE", "insufficient_resources")
        if case.get("temporal_conflict", False):
            return _out("WAIT", "occupation_conflict")
        if case.get("player_unresponsive", False):
            return _out("WAIT", "player_response_pending")
        if case.get("deliberate_noncompliance", False):
            return _out("REFUSE", "deliberate_noncompliance")
    return _out("ALLOW_REFERENCE", "rules_pass_for_reference_only")


def _out(verdict: str, reason: str) -> dict:
    return {"verdict": verdict, "reason": reason, "effects_applied": 0,
            "authoritative": False, "core_integrated": False}


def verify_fixture(path: Path) -> tuple[int, list[str]]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    cases = doc["cases"]
    errors = []
    ids = set()
    for item in cases:
        cid = item["id"]
        if cid in ids:
            errors.append(f"{cid}: duplicate case id")
        ids.add(cid)
        actual = assess(item["input"])
        for field in ("verdict", "reason"):
            if actual[field] != item["expected"][field]:
                errors.append(f"{cid}: expected {field}={item['expected'][field]}, got {actual[field]}")
        if actual["effects_applied"] != 0 or actual["authoritative"]:
            errors.append(f"{cid}: illegal side effect declaration")
    return len(cases), errors


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fixture", type=Path, required=True)
    args = p.parse_args()
    count, errors = verify_fixture(args.fixture)
    for error in errors:
        print("FAIL", error)
    print(f"F05 reference: {count} cases; {len(errors)} failures; Core and UE5 NOT tested")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
