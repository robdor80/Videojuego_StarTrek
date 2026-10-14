#!/usr/bin/env python3
"""F11: comprobador DE REFERENCIA de carrera, sin escritura en CoreRPG/UE5.

Todos los datos de perfil/oferta/evidencia son testimonios offline no autenticados.
El resultado REVIEW_REQUIRED nunca es una autorización de la Flota Estelar.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ERA_PROFILES = frozenset(("pike", "kirk", "tng_ds9_voyager"))
RANKS = (
    "ensign", "lieutenant_junior_grade", "lieutenant",
    "lieutenant_commander", "commander", "captain",
)
ACTIONS = frozenset((
    "remain", "decline_promotion", "promotion", "transfer",
    "change_position", "change_specialty", "temporary_command",
    "permanent_command", "evaluation",
))
CANDIDATE = "CANDIDATE_FOR_AUTHORIZED_REVIEW"
REVIEW = "REVIEW_REQUIRED"
BLOCKED = "BLOCKED"
NO_CHANGE = "NO_CHANGE"


def load_reference_data():
    catalog = json.loads(
        (ROOT / "lore/starships/classes/core_starship_classes.json").read_text(encoding="utf-8")
    )
    routes = json.loads(
        (ROOT / "gameplay/careers/starfleet_service/f11_route_plan_v0.1.json").read_text(encoding="utf-8")
    )
    return catalog, routes


def _strings(value):
    return isinstance(value, list) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    ) and len(value) == len(set(value))


def _result(status, reasons=(), **extra):
    return {
        "status": status,
        "reasons": list(dict.fromkeys(reasons)),
        "authority": "OFFLINE_REFERENCE_ONLY_NO_WORLD_STATE_MUTATION",
        **extra,
    }


def class_temporally_available(class_id, era, year, catalog):
    """Falla cerrado: pertenencia al catálogo y evidencia temporal conservadora.

    confirmed_active_from_decade no autoriza el primer año de la década: solo
    consideramos segura una fecha a partir de la década siguiente.
    """
    if era not in ERA_PROFILES or type(year) is not int or year < 2200 or year > 2999:
        return False
    if not isinstance(catalog, dict) or not isinstance(catalog.get("classes"), list):
        return False
    matches = [c for c in catalog["classes"] if isinstance(c, dict) and c.get("class_id") == class_id]
    if len(matches) != 1 or matches[0].get("operator") != "starfleet":
        return False
    availability = matches[0].get("availability")
    if not isinstance(availability, dict):
        return False
    if era not in availability.get("retained_playable_profiles", []):
        return False
    for key in ("operational_class_from_year", "confirmed_active_by_year"):
        value = availability.get(key)
        if type(value) is int and year >= value:
            return True
    decade = availability.get("confirmed_active_from_decade")
    return type(decade) is int and decade % 10 == 0 and year >= decade + 10


def _validate_profile(profile, routes):
    reasons = []
    if not isinstance(profile, dict):
        return ["invalid_profile"]
    if profile.get("rank") not in RANKS:
        reasons.append("invalid_rank")
    if profile.get("era_profile") not in ERA_PROFILES:
        reasons.append("invalid_era")
    if type(profile.get("campaign_year")) is not int or not 2200 <= profile["campaign_year"] <= 2999:
        reasons.append("invalid_year")
    if profile.get("route") not in routes.get("routes", {}):
        reasons.append("invalid_route")
    if not _strings(profile.get("qualifications")):
        reasons.append("invalid_qualifications")
    if type(profile.get("command_qualified")) is not bool:
        reasons.append("invalid_command_qualification")
    if not isinstance(profile.get("assignment_id"), (str, type(None))):
        reasons.append("invalid_assignment")
    if not isinstance(profile.get("ship_id"), (str, type(None))):
        reasons.append("invalid_ship_identity")
    return reasons


def screen_assignment(profile, offer, catalog=None, routes=None):
    """Filtra una posible plaza; ni concede destino ni genera órdenes."""
    if catalog is None or routes is None:
        default_catalog, default_routes = load_reference_data()
        catalog = default_catalog if catalog is None else catalog
        routes = default_routes if routes is None else routes
    reasons = _validate_profile(profile, routes)
    if not isinstance(offer, dict):
        return _result(BLOCKED, reasons + ["invalid_offer"])
    if not isinstance(offer.get("assignment_id"), str) or not offer["assignment_id"].strip():
        reasons.append("invalid_assignment_id")
    if not isinstance(offer.get("ship_id"), str) or not offer["ship_id"].strip():
        reasons.append("invalid_ship_id")
    if not isinstance(offer.get("position_id"), str) or not offer["position_id"].strip():
        reasons.append("invalid_position_id")
    if not _strings(offer.get("accepted_ranks")) or not offer["accepted_ranks"]:
        reasons.append("invalid_accepted_ranks")
    if not _strings(offer.get("required_qualifications")):
        reasons.append("invalid_required_qualifications")
    if type(offer.get("vacancy")) is not bool or not offer["vacancy"]:
        reasons.append("no_verified_vacancy")
    if type(offer.get("ship_operational")) is not bool or not offer["ship_operational"]:
        reasons.append("ship_not_operational")
    if reasons:
        return _result(BLOCKED, reasons)
    if not class_temporally_available(
        offer.get("class_id"), profile["era_profile"], profile["campaign_year"], catalog
    ):
        reasons.append("class_not_temporally_verified")
    if profile["rank"] not in offer["accepted_ranks"]:
        reasons.append("rank_incompatible")
    missing = sorted(set(offer["required_qualifications"]) - set(profile["qualifications"]))
    if missing:
        reasons.append("missing_qualification")
    if offer["position_id"] == "ship_captain" and (
        profile["rank"] != "captain" or not profile["command_qualified"]
    ):
        reasons.append("captaincy_not_automatic")
    if reasons:
        return _result(BLOCKED, reasons)
    priorities = routes["routes"][profile["route"]]["class_priorities"]
    return _result(
        CANDIDATE,
        route_fit="preferred" if offer["class_id"] in priorities else "cross_route_possible",
        requires=["host_vacancy_verification", "authorized_orders", "core_persistence"],
        assignment_id=offer["assignment_id"],
    )


def _evidence_present(request):
    return _strings(request.get("evidence_event_ids")) and bool(request["evidence_event_ids"])


def review_career_request(profile, request, offer=None, catalog=None, routes=None):
    """Examina la coherencia de una petición; NUNCA aprueba su ejecución."""
    if catalog is None or routes is None:
        default_catalog, default_routes = load_reference_data()
        catalog = default_catalog if catalog is None else catalog
        routes = default_routes if routes is None else routes
    reasons = _validate_profile(profile, routes)
    if not isinstance(request, dict):
        return _result(BLOCKED, reasons + ["invalid_request"])
    action = request.get("action")
    if action not in ACTIONS:
        reasons.append("unsupported_action")
    if reasons:
        return _result(BLOCKED, reasons)
    if action in ("remain", "decline_promotion"):
        # Expresar preferencia no altera la partida ni cancela una orden autoritativa.
        return _result(NO_CHANGE, ["player_choice_preserved"], choice=action)
    if not _evidence_present(request):
        reasons.append("missing_operational_evidence")
    if action == "promotion":
        target = request.get("target_rank")
        i = RANKS.index(profile["rank"])
        if i == len(RANKS) - 1 or target != RANKS[i + 1]:
            reasons.append("invalid_promotion_step")
        if target == "captain" and not profile["command_qualified"]:
            reasons.append("command_qualification_required")
    elif action in ("transfer", "change_position", "permanent_command"):
        screened = screen_assignment(profile, offer, catalog, routes)
        if screened["status"] != CANDIDATE:
            reasons.extend(screened["reasons"])
        if action == "permanent_command" and (
            profile["rank"] != "captain"
            or not profile["command_qualified"]
            or not isinstance(offer, dict)
            or offer.get("position_id") != "ship_captain"
        ):
            reasons.append("permanent_command_requires_captain_and_billet")
        if action == "transfer" and isinstance(offer, dict) and (
            offer.get("assignment_id") == profile["assignment_id"]
        ):
            reasons.append("already_assigned")
    elif action == "temporary_command":
        if not profile["command_qualified"]:
            reasons.append("command_qualification_required")
        if not isinstance(request.get("operational_order_ref"), str) or not request["operational_order_ref"].strip():
            reasons.append("missing_operational_order")
        if not profile["ship_id"]:
            reasons.append("no_ship_assignment")
    elif action == "change_specialty":
        if request.get("target_route") not in routes.get("routes", {}):
            reasons.append("invalid_target_route")
        if request.get("target_route") == profile["route"]:
            reasons.append("same_specialty")
        bridge = request.get("bridging_qualification")
        if not isinstance(bridge, str) or bridge not in profile["qualifications"]:
            reasons.append("missing_bridge_training")
    elif action == "evaluation":
        if not isinstance(request.get("supervisor_id"), str) or not request["supervisor_id"].strip():
            reasons.append("missing_supervisor")
    if reasons:
        return _result(BLOCKED, reasons)
    return _result(
        REVIEW,
        ["authoritative_decision_required"],
        action=action,
        requires=[
            "verify_source_events", "verify_actor_authority", "revalidate_live_world",
            "commit_append_only_in_CoreRPG", "preserve_social_history",
        ],
    )


def scenario_fingerprint(scenario):
    """Huella estable de entrada OFFLINE; no es firma ni savegame autenticado."""
    payload = json.dumps(scenario, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def run_scenarios(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("scenarios"), list):
        raise ValueError("Invalid F11 fixture")
    catalog, routes = load_reference_data()
    results = []
    for scenario in data["scenarios"]:
        kind = scenario["kind"]
        if kind == "assignment":
            decision = screen_assignment(scenario["profile"], scenario["offer"], catalog, routes)
        elif kind == "career":
            decision = review_career_request(
                scenario["profile"], scenario["request"], scenario.get("offer"), catalog, routes
            )
        else:
            raise ValueError("Unknown fixture action")
        results.append({
            "id": scenario["id"], "result": decision,
            "matches_expected": decision["status"] == scenario["expected_status"],
        })
    return {
        "test_only": True,
        "schema": "f11_offline_reference_0.1",
        "input_sha256": scenario_fingerprint(data),
        "results": results,
        "all_match": all(r["matches_expected"] for r in results),
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_scenarios(args.scenario)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    print(json.dumps({
        "scenarios": len(report["results"]), "matches": report["all_match"],
        "input_sha256": report["input_sha256"],
        "test_only": True,
    }))
    raise SystemExit(0 if report["all_match"] else 1)
