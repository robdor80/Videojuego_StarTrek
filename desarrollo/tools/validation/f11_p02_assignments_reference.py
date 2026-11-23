#!/usr/bin/env python3
"""F11-P02: cribado OFFLINE no mutador de plazas, destinos y ofertas.

NO conecta con CoreRPG/Host/UE5 y NO autentica los marcadores 'verified'.
Sus resultados NO son órdenes, permisos, ocupaciones ni guardados de partida.
"""
from __future__ import annotations

import json
from pathlib import Path

try:
    from desarrollo.tools.validation.f11_career_reference import class_temporally_available
except ModuleNotFoundError:
    from f11_career_reference import class_temporally_available

ROOT = Path(__file__).resolve().parents[3]
PROFILE_PATH = ROOT / "sistemas/gameplay/careers/assignments/f11_p02_billet_profiles_v0.1.json"
SHIPS_PATH = ROOT / "mundo/lore/starships/classes/core_starship_classes.json"
CANON_POSITIONS = ROOT / "mundo/lore/federation/starfleet/positions/positions.json"
CANON_SPECIALTIES = ROOT / "mundo/lore/federation/starfleet/departments/divisions_and_departments.json"

CANDIDATE = "CANDIDATE_FOR_AUTHORIZED_REVIEW"
WAITING = "WAITING_FOR_REAL_VACANCY"
BLOCKED = "BLOCKED_REFERENCE"
REVIEW = "REVIEW_REQUIRED"
TAG = "OFFLINE_REFERENCE_ONLY_NO_WORLD_STATE_MUTATION"
INTENTS = frozenset(("first_assignment", "transfer", "position_change"))
NEXT_STATES = {
    "draft": frozenset(("screened", "withdrawn")),
    "screened": frozenset(("offered", "withdrawn")),
    "offered": frozenset(("accepted", "declined", "withdrawn", "expired")),
    "accepted": frozenset(("orders_issued", "cancelled")),
    "orders_issued": frozenset(("effective", "cancelled")),
}


def load_references():
    return (
        json.loads(PROFILE_PATH.read_text(encoding="utf-8")),
        json.loads(SHIPS_PATH.read_text(encoding="utf-8")),
    )


def _id(value):
    return isinstance(value, str) and bool(value.strip())


def _string_list(value):
    return isinstance(value, list) and all(_id(x) for x in value) and len(value) == len(set(value))


def _result(status, *reasons, **details):
    return dict(status=status, reasons=list(dict.fromkeys(reasons)),
                authority=TAG, effects_applied=0, **details)


def _find_profile(data, profile_id):
    profiles = data.get("profiles", []) if isinstance(data, dict) else []
    matched = [p for p in profiles if isinstance(p, dict) and p.get("profile_id") == profile_id]
    return matched[0] if len(matched) == 1 else None


def validate_catalog(catalog=None):
    """La identidad del catálogo refleja las definiciones existentes, no nuevas plazas."""
    catalog = load_references()[0] if catalog is None else catalog
    if not isinstance(catalog, dict):
        return False
    groups = catalog.get("groups")
    profiles = catalog.get("profiles")
    if not isinstance(groups, list) or not isinstance(profiles, list):
        return False
    canonical = json.loads(CANON_POSITIONS.read_text(encoding="utf-8"))
    specialties = json.loads(CANON_SPECIALTIES.read_text(encoding="utf-8"))
    existing_positions = {x["id"] for x in canonical["positions"]}
    existing_depts = {x["id"] for x in specialties["departments"]}
    existing_divisions = {x["id"] for x in specialties["divisions"]}
    group_ids = [g.get("id") for g in groups if isinstance(g, dict)]
    profile_ids = [p.get("profile_id") for p in profiles if isinstance(p, dict)]
    if len(group_ids) != len(groups) or len(set(group_ids)) != len(group_ids):
        return False
    if len(group_ids) != 7 or {g.get("f04_department_id") for g in groups} != set(range(1, 8)):
        return False
    if len(profile_ids) != len(profiles) or len(set(profile_ids)) != len(profile_ids):
        return False
    for g in groups:
        if (not _id(g.get("id")) or g.get("typical_division_id") not in existing_divisions
                or not _string_list(g.get("specialty_department_ids"))
                or not set(g["specialty_department_ids"]) <= existing_depts):
            return False
    global_formal_ids = []
    for p in profiles:
        if (not _id(p.get("profile_id")) or p.get("group_id") not in group_ids
                or p.get("department_id") not in existing_depts
                or not _string_list(p.get("accepted_ranks")) or not p["accepted_ranks"]
                or not _string_list(p.get("required_qualifications"))
                or type(p.get("is_command_post")) is not bool or p.get("require_named_billet") is not True):
            return False
        if p.get("classification") == "existing_formal_position":
            if p.get("formal_position_id") not in existing_positions:
                return False
            if p["formal_position_id"] != p["profile_id"]:
                return False
            global_formal_ids.append(p["formal_position_id"])
        elif p.get("classification") == "functional_assignment_reference_only":
            if p.get("formal_position_id") is not None or p.get("is_command_post"):
                return False
        else:
            return False
    return set(global_formal_ids) == existing_positions and len(global_formal_ids) == len(existing_positions)


def screen_billet(person, unit, billet, intent, catalog=None, ships=None):
    """Solo determina si una candidatura ficticia puede pasar a revisión."""
    if catalog is None or ships is None:
        default_catalog, default_ships = load_references()
        catalog = default_catalog if catalog is None else catalog
        ships = default_ships if ships is None else ships
    if intent not in INTENTS or not isinstance(person, dict) or not isinstance(unit, dict) or not isinstance(billet, dict):
        return _result(BLOCKED, "INVALID_INPUT")
    if (not _id(person.get("character_id")) or not _id(person.get("rank"))
            or not _string_list(person.get("qualifications"))
            or person.get("medical_status") != "fit"):
        return _result(BLOCKED, "PERSON_NOT_VERIFIABLE_OR_FIT")
    if (not _id(unit.get("unit_id")) or unit.get("type") not in catalog.get("unit_types", [])
            or unit.get("live_unit_verified") is not True or unit.get("operational") is not True):
        return _result(BLOCKED, "UNIT_NOT_VERIFIED_OPERATIONAL")
    if (type(unit.get("world_revision")) is not int or unit["world_revision"] < 0
            or type(unit.get("time_tick")) is not int or unit["time_tick"] < 0
            or type(unit.get("campaign_year")) is not int or not 2200 <= unit["campaign_year"] <= 2999
            or unit.get("era_profile") not in ("pike", "kirk", "tng_ds9_voyager")):
        return _result(BLOCKED, "INVALID_UNIT_TIME_OR_ERA")
    if unit["type"] == "starship":
        if not _id(unit.get("class_id")) or not class_temporally_available(
                unit["class_id"], unit["era_profile"], unit["campaign_year"], ships):
            return _result(BLOCKED, "STARSHIP_CLASS_NOT_TEMPORALLY_VERIFIED")
    elif unit.get("nonship_activation_verified") is not True:
        return _result(BLOCKED, "NONSHIP_ACTIVATION_NOT_VERIFIED")
    if (not _id(billet.get("billet_id")) or billet.get("unit_id") != unit["unit_id"]
            or billet.get("slot_reference_verified") is not True):
        return _result(BLOCKED, "SLOT_NOT_VERIFIED_OR_WRONG_UNIT")
    profile = _find_profile(catalog, billet.get("profile_id"))
    if profile is None:
        return _result(BLOCKED, "UNKNOWN_BILLET_PROFILE")
    state = billet.get("vacancy_state")
    occupant = billet.get("occupant_id")
    if (state not in catalog["vacancy_states"]
            or (occupant is not None and not _id(occupant))
            or (state == "vacant" and occupant is not None)
            or (state in ("occupied", "planned") and not _id(occupant))):
        return _result(BLOCKED, "INCONSISTENT_BILLET_STATE")
    if person["rank"] not in profile["accepted_ranks"]:
        return _result(BLOCKED, "RANK_NOT_COMPATIBLE_WITH_BILLET")
    if not set(profile["required_qualifications"]).issubset(set(person["qualifications"])):
        return _result(BLOCKED, "MISSING_PROFESSIONAL_QUALIFICATION")
    if profile["is_command_post"] and "command_qualified" not in person["qualifications"]:
        return _result(BLOCKED, "MISSING_COMMAND_QUALIFICATION")
    if intent == "first_assignment":
        if (person.get("service_status") != "commissioned" or person.get("rank") != "ensign"
                or person.get("current_unit_id") is not None or person.get("current_billet_id") is not None):
            return _result(BLOCKED, "NOT_COMMISSIONED_FOR_FIRST_ASSIGNMENT")
    else:
        if (person.get("service_status") != "active" or not _id(person.get("current_unit_id"))
                or not _id(person.get("current_billet_id"))):
            return _result(BLOCKED, "NOT_ACTIVE_WITH_CURRENT_ASSIGNMENT")
        if intent == "transfer" and person["current_unit_id"] == unit["unit_id"]:
            return _result(BLOCKED, "SAME_UNIT_USE_POSITION_CHANGE")
        if intent == "position_change" and person["current_unit_id"] != unit["unit_id"]:
            return _result(BLOCKED, "DIFFERENT_UNIT_USE_TRANSFER")
        if person["current_billet_id"] == billet["billet_id"]:
            return _result(BLOCKED, "ALREADY_OCCUPIES_TARGET_BILLET")
        if (person.get("current_department_id") not in (None, profile["department_id"])
                and person.get("cross_specialty_authorized") is not True):
            return _result(BLOCKED, "CROSS_SPECIALTY_NEEDS_AUTHORIZATION")
    if state in ("occupied", "planned", "reserved"):
        return _result(WAITING, "BILLET_NOT_EFFECTIVELY_VACANT",
                       vacancy_state=state, billet_id=billet["billet_id"],
                       planning_may_propose_future_opportunity=True)
    if state in ("suspended", "decommissioned"):
        return _result(BLOCKED, "BILLET_NOT_USABLE")
    return _result(CANDIDATE, "ELIGIBLE_FOR_AUTHORIZED_REVIEW_ONLY",
                   profile_id=profile["profile_id"], billet_id=billet["billet_id"],
                   unit_id=unit["unit_id"], needs=["live_Core_check", "selection", "orders", "atomic_assignment"])


def review_offer_transition(person, unit, billet, offer, target, catalog=None, ships=None):
    """Simula transiciones de oferta. NO cambia offer/puesto/persona."""
    if not all(isinstance(x, dict) for x in (person, unit, billet, offer)):
        return _result(BLOCKED, "INVALID_OFFER_CONTEXT")
    current = offer.get("status")
    if target not in NEXT_STATES.get(current, frozenset()):
        return _result(BLOCKED, "INVALID_OFFER_TRANSITION")
    if (not _id(offer.get("offer_id")) or offer.get("candidate_id") != person.get("character_id")
            or offer.get("unit_id") != unit.get("unit_id")
            or offer.get("billet_id") != billet.get("billet_id")
            or offer.get("intent") not in INTENTS):
        return _result(BLOCKED, "OFFER_IDENTITY_MISMATCH")
    if (type(offer.get("world_revision")) is not int
            or offer["world_revision"] != unit.get("world_revision")
            or type(offer.get("issued_at_tick")) is not int
            or type(offer.get("expires_at_tick")) is not int
            or offer["issued_at_tick"] >= offer["expires_at_tick"]):
        return _result(BLOCKED, "OFFER_STALE_OR_INVALID_TIME")
    now = unit.get("time_tick")
    if type(now) is not int or now < 0:
        return _result(BLOCKED, "INVALID_CURRENT_TIME")
    if target in ("withdrawn", "declined", "cancelled", "expired"):
        if target == "expired" and now < offer["expires_at_tick"]:
            return _result(BLOCKED, "OFFER_NOT_YET_EXPIRED")
        return _result(REVIEW, "TERMINAL_EVENT_REQUIRES_CORE_RECORD",
                       proposed_status=target)
    if target in ("accepted", "screened", "offered") and now >= offer["expires_at_tick"]:
        return _result(BLOCKED, "OFFER_EXPIRED")
    screening = screen_billet(person, unit, billet, offer["intent"], catalog, ships)
    if screening["status"] != CANDIDATE:
        return _result(BLOCKED, "CANDIDATE_OR_VACANCY_NO_LONGER_VALID", screening=screening)
    if target == "screened":
        return _result(REVIEW, "SCREENING_SUCCESS_REFERENCE", proposed_status=target)
    if target == "offered":
        if offer.get("personnel_authority_verified") is not True:
            return _result(BLOCKED, "PERSONNEL_AUTHORITY_REQUIRED")
        return _result(REVIEW, "OFFER_REQUIRES_AUTHORIZED_ISSUANCE", proposed_status=target)
    if target == "accepted":
        return _result(REVIEW, "ACCEPTANCE_DOES_NOT_OCCUPY_BILLET", proposed_status=target)
    if target == "orders_issued":
        if (offer.get("selection_authorized") is not True
                or offer.get("personnel_authority_verified") is not True
                or not _id(offer.get("order_id")) or offer.get("formal_order_verified") is not True):
            return _result(BLOCKED, "AUTHORIZED_SELECTION_AND_ORDERS_REQUIRED")
        return _result(REVIEW, "ORDERS_NEED_CORE_COMMIT", proposed_status=target)
    if target == "effective":
        if (offer.get("selection_authorized") is not True
                or offer.get("formal_order_verified") is not True
                or offer.get("personnel_authority_verified") is not True
                or not _id(offer.get("order_id"))
                or offer.get("atomic_core_transaction_authorized") is not True
                or type(offer.get("order_effective_at_tick")) is not int
                or now < offer["order_effective_at_tick"]):
            return _result(BLOCKED, "CORE_ATOMIC_APPOINTMENT_NOT_READY")
        return _result(REVIEW, "READY_FOR_CORE_ATOMIC_TRANSACTION_NOT_EXECUTED",
                       proposed_status=target)
    return _result(BLOCKED, "UNSUPPORTED_TRANSITION")


if __name__ == "__main__":
    print("F11-P02 reference only; execute test_f11_p02_assignments_reference.py")
