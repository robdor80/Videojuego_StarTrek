#!/usr/bin/env python3
"""F11-P01. Evaluador puro de REFERENCIA, jamás autorizado para ejecutar órdenes.

NO conecta con CoreRPG/Host/UE5, no autentica contextos, no persiste ni muta
World State. Los marcadores *_verified son datos simulados NO confiables.
Las decisiones *_REFERENCE NO son permisos válidos en una partida.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "sistemas/gameplay/chain_of_command/f11_p01_personnel_authority_contract_v0.1.json"
ALLOW = "ALLOW_REFERENCE"
DENY = "DENY_REFERENCE"
TAG = "OFFLINE_REFERENCE_ONLY_NO_WORLD_STATE_MUTATION"


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def result(allowed, reason):
    return {"status": ALLOW if allowed else DENY, "reason": reason,
            "authority": TAG, "effects_applied": 0}


def valid_string(value):
    return isinstance(value, str) and bool(value.strip())


def valid_strings(value):
    return isinstance(value, list) and all(valid_string(x) for x in value) and len(value) == len(set(value))


def _delegation_for(ctx, domain):
    time = ctx["time_tick"]
    for d in ctx.get("active_delegations", []):
        if not isinstance(d, dict):
            continue
        if (d.get("domain") == domain and d.get("delegate_actor_id") == ctx["actor_id"]
                and d.get("issuer_authorized") is True and d.get("active") is True
                and d.get("revoked") is False and type(d.get("starts_at")) is int
                and type(d.get("ends_at")) is int and d["starts_at"] <= time < d["ends_at"]):
            return True
    return False


def _acting_command(ctx):
    s = ctx.get("succession")
    if not isinstance(s, dict):
        return False
    return (s.get("active") is True and s.get("order_verified") is True
            and s.get("actor_id") == ctx["actor_id"]
            and s.get("origin_position") in ("first_officer", "second_officer", "designated_qualified_successor")
            and s.get("origin_position") in ctx["position_ids"]
            and type(s.get("starts_at")) is int and type(s.get("ends_at")) is int
            and s["starts_at"] <= ctx["time_tick"] < s["ends_at"]
            and "command_qualified" in ctx["qualifications"])


def evaluate(action_id, ctx, request=None, contract=None):
    """Clasifica un ejemplo offline; niega ante datos incompletos, nunca autoriza."""
    request = request if isinstance(request, dict) else {}
    policy = load_contract() if contract is None else contract
    if not isinstance(ctx, dict) or not isinstance(policy, dict):
        return result(False, "INVALID_CONTEXT")
    action = policy.get("decisions", {}).get(action_id)
    if not isinstance(action, dict):
        return result(False, "UNKNOWN_ACTION")

    required_text = ("actor_id", "unit_id", "assignment_id", "rank", "medical_status")
    required_lists = ("position_ids", "duty_role_ids", "qualifications")
    if any(not valid_string(ctx.get(key)) for key in required_text):
        return result(False, "MISSING_IDENTITY_OR_ASSIGNMENT")
    if any(not valid_strings(ctx.get(key)) for key in required_lists):
        return result(False, "MISSING_ROLE_OR_QUALIFICATION_DATA")
    if ctx["rank"] not in policy["rank_progression"]:
        return result(False, "INVALID_RANK")
    if type(ctx.get("time_tick")) is not int or type(ctx.get("world_revision")) is not int:
        return result(False, "MISSING_TIME_OR_REVISION")
    if type(request.get("observed_revision")) is not int or request["observed_revision"] != ctx["world_revision"]:
        return result(False, "STALE_WORLD_REVISION")
    if ctx.get("reference_snapshot_complete") is not True:
        return result(False, "UNVERIFIED_REFERENCE_SNAPSHOT")
    if ctx["assignment_id"] != ctx["unit_id"]:
        return result(False, "WRONG_ASSIGNMENT")
    if ctx["medical_status"] != "fit":
        return result(False, "NOT_FIT_FOR_DUTY")

    # En un juego real estos indicadores DEBEN comprobarse en Core/Host,
    # no recibirse como booleanos proporcionados por la interfaz o la IA.
    if any(ctx.get(key) is not True for key in ("orders_within_scope", "resources_exist", "safety_limits_respected")):
        return result(False, "HARD_OPERATIONAL_LIMIT")

    if action.get("requires_on_duty") and ctx.get("on_duty") is not True:
        return result(False, "NOT_ON_DUTY")
    if not set(action.get("qualifications_all", [])) <= set(ctx["qualifications"]):
        return result(False, "MISSING_QUALIFICATION")
    if action.get("department_match_required") and (
            not valid_string(ctx.get("department_id")) or
            ctx.get("department_id") != request.get("department_id")):
        return result(False, "DEPARTMENT_SCOPE_MISMATCH")

    if action.get("requires_knowledge_and_clearance"):
        target = request.get("information_id")
        if not valid_string(target) or not valid_strings(ctx.get("known_information_ids")) or not valid_strings(ctx.get("permitted_information_ids")):
            return result(False, "MISSING_KNOWLEDGE_CONTEXT")
        if target not in ctx["known_information_ids"] or target not in ctx["permitted_information_ids"]:
            return result(False, "KNOWLEDGE_OR_CLEARANCE_DENIED")
        return result(True, "KNOWLEDGE_AND_PERMISSION_VERIFIED_REFERENCE")

    if action.get("requires_external_personnel_authority"):
        if (ctx.get("external_personnel_authority_verified") is True
                and ctx.get("vacancy_verified") is True
                and ctx.get("formal_appointment_order_verified") is True):
            return result(True, "FLEET_APPOINTMENT_REVIEWABLE_REFERENCE")
        return result(False, "FLEET_APPOINTMENT_AUTHORITY_OR_VACANCY_MISSING")

    roles = set(ctx["position_ids"]) | set(ctx["duty_role_ids"])
    authorized = bool(roles.intersection(action.get("positions_any", []) + action.get("duty_roles_any", [])))
    if (not authorized and action.get("allows_acting_succession") and
            _acting_command(ctx)):
        authorized = True
    if (not authorized and action.get("allows_delegation") and
            _delegation_for(ctx, action["domain"])):
        authorized = True
    if not authorized:
        return result(False, "POSITION_OR_VALID_DELEGATION_REQUIRED")
    if action.get("non_mutating_recommendation"):
        return result(True, "RECOMMENDATION_ONLY_NO_APPOINTMENT")
    return result(True, "ROLE_WITHIN_SCOPE_REFERENCE")


if __name__ == "__main__":
    print("F11-P01: módulo offline. Ejecutar test_f11_p01_authority_reference.py.")
