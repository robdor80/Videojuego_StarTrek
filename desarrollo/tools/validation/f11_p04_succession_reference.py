#!/usr/bin/env python3
"""F11-P04. Director de sucesiones de NPC: SOLO PROPUESTAS OFFLINE, SIN EFECTOS.

Evalúa hechos simulados del expediente, plazas, consentimiento del NPC y posibles
oportunidades profesionales de Flota. Nunca crea personas, puestos, ascensos,
vacantes, órdenes ni historial. Core/Host deben revalidar TODO en vivo.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POLICY_PATH = ROOT / "sistemas/gameplay/careers/succession/f11_p04_causal_succession_policy_v0.1.json"
P02_CATALOG_PATH = ROOT / "sistemas/gameplay/careers/assignments/f11_p02_billet_profiles_v0.1.json"
TAG = "OFFLINE_REFERENCE_ONLY_NO_WORLD_STATE_MUTATION"
INVALID = "INVALID_CONTEXT"
PAUSED = "PLAYER_PAUSED"
ALREADY = "ALREADY_IN_TARGET_POST"
DIRECT = "DIRECT_SELECTION_POSSIBLE"
PREPARED = "CAUSAL_OPPORTUNITY_PREPARED"
NPC_WAIT = "AWAITING_NPC_DECISION"
ORDERS_WAIT = "AWAITING_VALID_ORDERS"
DEPARTURE_WAIT = "AWAITING_EFFECTIVE_DEPARTURE"
CONFIRM_WAIT = "AWAITING_VACANCY_CONFIRMATION"
ALTERNATIVE = "FLEET_ALTERNATIVE_REQUIRED"
URGENT = "URGENT_FLEET_ESCALATION"
READY = "FUTURE_CANDIDACY_READY"
REQUESTED_STAGES = frozenset(("department_head", "enterprise_d_first_officer",
                              "captain_other_ship", "enterprise_d_captain"))
OPTIONS = frozenset(("ship_command", "fleet_staff", "equivalent_transfer",
                     "existing_retirement"))
NPC_DECISIONS = frozenset(("considering", "accepted", "declined", "withdrawn"))
OTHER_STAGES = frozenset(("department_head", "captain_other_ship"))
ENTERPRISE_STAGES = frozenset(("enterprise_d_first_officer", "enterprise_d_captain"))
STATUS_MUST_NOT_MUTATE = ["rank", "assignments", "vacancies", "npc_life",
                          "personnel_orders", "historical_events"]


def load_policy():
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _valid_id(v):
    return isinstance(v, str) and bool(v.strip())


def _ids(v):
    return isinstance(v, list) and all(_valid_id(x) for x in v) and len(v) == len(set(v))


def _int(v):
    return type(v) is int


def _out(status, reason, **extra):
    return dict(status=status, reason=reason, authority=TAG, effects_applied=0,
                no_world_mutations=list(STATUS_MUST_NOT_MUTATE), **extra)


def policy_valid(policy):
    if not isinstance(policy, dict) or policy.get("maturity") != TAG:
        return False
    stages = policy.get("target_stages")
    if not isinstance(stages, dict) or set(stages) != set(REQUESTED_STAGES):
        return False
    if policy.get("project_ship_key") != "enterprise_d_ncc_1701_d_refit":
        return False
    settings = policy.get("scheduling_parameters_illustrative_not_final", {})
    for key in ("minimum_departure_notice_months", "alternate_career_review_months",
                "advance_preparation_window_months", "npc_decision_window_months"):
        if not _int(settings.get(key)) or settings[key] < 1:
            return False
    profiles = json.loads(P02_CATALOG_PATH.read_text(encoding="utf-8"))
    formal_ids = {x["formal_position_id"] for x in profiles["profiles"]
                  if x["formal_position_id"] is not None}
    for stage in stages.values():
        if not isinstance(stage, dict) or not _ids(stage.get("accepted_ranks")):
            return False
        if not _ids(stage.get("position_ids")) or not set(stage["position_ids"]) <= formal_ids:
            return False
        if stage.get("unit_scope") not in ("qualified_any_unit", "enterprise_d_only",
                                           "other_ship_only"):
            return False
    return True


def episode_plan_id(episode_id, upstream_plan_id, target_billet_id):
    value = f"F11-P04/v0.1|{episode_id}|{upstream_plan_id}|{target_billet_id}"
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def _snapshot_error(s, policy):
    if not policy_valid(policy) or not isinstance(s, dict):
        return "INVALID_POLICY_OR_SNAPSHOT"
    if any(not _valid_id(s.get(k)) for k in ("episode_id", "upstream_plan_id",
                                             "rank_event_id", "stage")):
        return "MISSING_EPISODE_IDENTITY"
    if s["stage"] not in policy["target_stages"]:
        return "UNSUPPORTED_CAREER_STAGE"
    if any(not _int(s.get(k)) for k in ("now_month", "ready_since_month",
                                        "deadline_month", "world_revision")):
        return "INVALID_EPISODE_CLOCK"
    if (s["ready_since_month"] < 0 or s["now_month"] < s["ready_since_month"]
            or s["deadline_month"] < s["ready_since_month"]
            or s["world_revision"] < 0 or s.get("live_context_verified") is not True):
        return "STALE_OR_UNVERIFIED_EPISODE"
    p = s.get("player")
    if not isinstance(p, dict) or any(not _valid_id(p.get(k)) for k in (
            "character_id", "rank", "current_unit_id", "current_position_id")):
        return "MISSING_PLAYER_IDENTITY"
    if (p.get("service_status") != "active" or p.get("professional_review_verified") is not True
            or not _ids(p.get("qualifications"))):
        return "PLAYER_CAREER_EVIDENCE_INCOMPLETE"
    if p.get("preference") not in ("continue", "pause", "decline"):
        return "PLAYER_PREFERENCE_INVALID"
    target = s.get("target")
    if not isinstance(target, dict) or any(not _valid_id(target.get(k)) for k in (
            "unit_id", "unit_key", "billet_id", "position_id")):
        return "TARGET_IDENTITY_MISSING"
    if (target.get("unit_type") != "starship"
            or target.get("unit_operational_verified") is not True
            or target.get("billet_verified") is not True):
        return "TARGET_NOT_AUTHORITATIVELY_VERIFIED"
    if target.get("vacancy_state") not in ("vacant", "occupied", "planned", "reserved",
                                            "suspended", "decommissioned"):
        return "INVALID_TARGET_VACANCY_STATE"
    if (target["vacancy_state"] == "vacant" and target.get("occupant_id") is not None):
        return "VACANCY_HAS_OCCUPANT"
    if target["vacancy_state"] in ("occupied", "planned") and not _valid_id(target.get("occupant_id")):
        return "OCCUPIED_VACANCY_WITHOUT_NPC"
    if target.get("vacancy_state") == "vacant" and (
            target.get("vacancy_provenance_type") not in ("authorized_new_billet",
                                                         "verified_effective_departure")
            or not _valid_id(target.get("vacancy_event_id"))):
        return "VACANCY_PROVENANCE_UNVERIFIED"
    stage = policy["target_stages"][s["stage"]]
    if p["rank"] not in stage["accepted_ranks"]:
        return "PLAYER_RANK_NOT_ELIGIBLE"
    if target["position_id"] not in stage["position_ids"]:
        return "WRONG_TARGET_POSITION_FOR_STAGE"
    if stage["requires_command_qualification"] and "command_qualified" not in p["qualifications"]:
        return "PLAYER_COMMAND_QUALIFICATION_MISSING"
    if stage["requires_department_qualification"] and p.get("department_qualification_verified") is not True:
        return "DEPARTMENT_QUALIFICATION_MISSING"
    enterprise_key = policy["project_ship_key"]
    if s["stage"] in ENTERPRISE_STAGES and target["unit_key"] != enterprise_key:
        return "ENTERPRISE_D_UNIT_MISMATCH"
    if s["stage"] in OTHER_STAGES and s["stage"] == "captain_other_ship" and target["unit_key"] == enterprise_key:
        return "OTHER_COMMAND_MUST_BE_OTHER_SHIP"
    if not isinstance(s.get("opportunities"), list):
        return "INVALID_NPC_OPPORTUNITIES_LIST"
    return None


def _npc_error(npc, target):
    if not isinstance(npc, dict):
        return "MISSING_NPC_SERVICE_RECORD"
    if (npc.get("character_id") != target["occupant_id"]
            or npc.get("current_unit_id") != target["unit_id"]
            or npc.get("current_billet_id") != target["billet_id"]):
        return "NPC_DOES_NOT_OCCUPY_TARGET_BILLET"
    if (npc.get("service_status") != "active" or npc.get("professional_review_verified") is not True
            or not _ids(npc.get("qualifications"))
            or not _ids(npc.get("career_motivation_event_ids"))):
        return "NPC_CAREER_EVIDENCE_INCOMPLETE"
    return None


def _opportunity_state(option, snapshot, npc, policy):
    target = snapshot["target"]
    now = snapshot["now_month"]
    if not isinstance(option, dict) or any(not _valid_id(option.get(k)) for k in (
            "opportunity_id", "candidate_id", "professional_reason_event_id")):
        return "INVALID_OPPORTUNITY"
    if option["candidate_id"] != npc["character_id"] or option.get("kind") not in OPTIONS:
        return "OPPORTUNITY_NPC_MISMATCH"
    if (option.get("npc_decision") not in NPC_DECISIONS or
            not _ids(option.get("professional_source_events")) or
            not option["professional_source_events"] or
            not set(option["professional_source_events"]) <= set(npc["career_motivation_event_ids"])):
        return "OPPORTUNITY_CAREER_EVIDENCE_INVALID"
    if not _int(option.get("prepared_at_month")) or not _int(option.get("effective_not_before_month")):
        return "OPPORTUNITY_TIME_INVALID"
    notice = policy["scheduling_parameters_illustrative_not_final"]["minimum_departure_notice_months"]
    if option["prepared_at_month"] > now or option["prepared_at_month"] < 0:
        return "FUTURE_OR_NEGATIVE_PREPARATION_DATE"
    if option["effective_not_before_month"] < option["prepared_at_month"] + notice:
        return "MISSING_REASONABLE_NPC_NOTICE"
    if option.get("professional_merit_verified") is not True:
        return "NPC_PROFESSIONAL_MERIT_UNVERIFIED"
    if option.get("fleet_organizational_need_verified") is not True:
        return "FLEET_NEED_UNVERIFIED"
    if option.get("kind") == "existing_retirement":
        if (not _valid_id(option.get("preexisting_retirement_event_id"))
                or option.get("preexisting_retirement_event_month") is None
                or not _int(option.get("preexisting_retirement_event_month"))
                or option["preexisting_retirement_event_month"] > snapshot["ready_since_month"]):
            return "RETIREMENT_NOT_INDEPENDENTLY_PREEXISTING"
    else:
        if (not _valid_id(option.get("destination_unit_id"))
                or option["destination_unit_id"] == target["unit_id"]
                or not _valid_id(option.get("destination_billet_id"))
                or option.get("destination_billet_state") != "vacant"
                or option.get("destination_operational_verified") is not True
                or option.get("destination_billet_verified") is not True
                or option.get("npc_qualified_for_destination") is not True):
            return "NPC_DESTINATION_NOT_GENUINELY_AVAILABLE"
        if option.get("kind") == "fleet_staff" and option.get("fleet_staff_role_verified") is not True:
            return "FLEET_STAFF_APPOINTMENT_NOT_CATALOGUED"
        if option.get("kind") == "ship_command" and "command_qualified" not in npc["qualifications"]:
            return "NPC_COMMAND_QUALIFICATION_MISSING"
    if option["npc_decision"] in ("declined", "withdrawn"):
        return "NPC_DECLINED_OR_WITHDREW"
    if option["npc_decision"] == "considering":
        if option.get("orders_verified") is True or option.get("departure_effective_verified") is True:
            return "UNACCEPTED_NPC_OFFER_CANNOT_BE_EXECUTED"
        return "NPC_CONSIDERING"
    if option.get("orders_verified") is not True:
        if option.get("departure_effective_verified") is True:
            return "DEPARTURE_WITHOUT_ORDERS"
        return "AWAITING_ORDERS"
    if (not _valid_id(option.get("personnel_order_id")) or
            option.get("order_approved_by_fleet") is not True):
        return "UNVERIFIED_PERSONNEL_ORDER"
    if now < option["effective_not_before_month"] and option.get("departure_effective_verified") is True:
        return "DEPARTURE_BEFORE_EFFECTIVE_DATE"
    if option.get("departure_effective_verified") is True:
        if not _valid_id(option.get("departure_event_id")):
            return "DEPARTURE_WITHOUT_EVENT"
        return "DEPARTURE_PROPOSED_CONFIRMED"
    return "ORDERS_EXIST_DEPARTURE_PENDING"


def propose_succession(snapshot, policy=None):
    """Produce propuestas causales sin modificar el estado ni inventar vacantes."""
    policy = load_policy() if policy is None else policy
    error = _snapshot_error(snapshot, policy)
    if error:
        return _out(INVALID, error)
    player, target = snapshot["player"], snapshot["target"]
    eid = episode_plan_id(snapshot["episode_id"], snapshot["upstream_plan_id"],
                          target["billet_id"])
    urgent = snapshot["now_month"] >= snapshot["deadline_month"]
    base = {"episode_plan_id":eid, "stage":snapshot["stage"],
            "target_billet_id":target["billet_id"], "deadline_month":snapshot["deadline_month"],
            "ready_since_month":snapshot["ready_since_month"],"escalation_required":urgent}
    if player["preference"] != "continue":
        return _out(PAUSED, "PLAYER_REFUSES_OR_PAUSES_CURRENT_PATH", **base)
    if (player["current_unit_id"] == target["unit_id"] and
            player.get("current_billet_id") == target["billet_id"] and
            player["current_position_id"] == target["position_id"]):
        return _out(ALREADY, "PLAYER_ALREADY_OCCUPIES_TARGET_BILLET", **base)
    if target["vacancy_state"] == "vacant":
        return _out(DIRECT, "VACANCY_ALREADY_REAL_PLAYER_STILL_NEEDS_SELECTION",
                    **base, required_next=["fleet_personnel_selection","player_acceptance",
                                           "formal_orders","atomic_Core_assignment"])
    if target["vacancy_state"] in ("reserved", "suspended", "decommissioned"):
        return _out(URGENT if urgent else ALTERNATIVE,
                    "TARGET_NOT_AVAILABLE_FOR_ANY_NPC_CAREER_MOVE", **base,
                    required_next=["find_valid_alternative","authorized_fleet_review"])
    error = _npc_error(snapshot.get("incumbent"), target)
    if error:
        return _out(INVALID, error, **base)
    npc = snapshot["incumbent"]
    valid = []
    rejected = []
    seen = set()
    for option in snapshot["opportunities"]:
        if not isinstance(option, dict) or not _valid_id(option.get("opportunity_id")):
            return _out(INVALID,"INVALID_OPTION_ID",**base)
        if option["opportunity_id"] in seen:
            return _out(INVALID,"DUPLICATE_OPTION_ID",**base)
        seen.add(option["opportunity_id"])
        status = _opportunity_state(option, snapshot, npc, policy)
        if status in ("NPC_CONSIDERING","AWAITING_ORDERS",
                      "ORDERS_EXIST_DEPARTURE_PENDING","DEPARTURE_PROPOSED_CONFIRMED"):
            valid.append((option,status))
        else:
            rejected.append({"opportunity_id":option["opportunity_id"],"reason":status})
    if not valid:
        return _out(URGENT if urgent else ALTERNATIVE,"REPLAN_NPC_CAREER_WITH_REAL_OPTIONS",
                    **base, rejected_options=rejected,
                    required_next=["seek_another_credible_fleet_opportunity",
                                   "retain_incumbent","do_not_reset_ready_anchor",
                                   "recheck_on_authoritative_event"])
    # A valid accepted/ordered opportunity is preferred to an unaccepted one;
    # deterministic order never chooses by pseudo-random or player favoritism.
    priority = {"DEPARTURE_PROPOSED_CONFIRMED":0,"ORDERS_EXIST_DEPARTURE_PENDING":1,
                "AWAITING_ORDERS":2,"NPC_CONSIDERING":3}
    valid.sort(key=lambda it: (priority[it[1]],it[0]["effective_not_before_month"],
                               it[0]["opportunity_id"]))
    option,status = valid[0]
    chain = [
        {"kind":"npc_merit_and_motivation", "source_events":list(option["professional_source_events"])},
        {"kind":"independent_fleet_opportunity", "ref":option["opportunity_id"],
         "requires":"authoritative_Fleet_billet_and_personnel_authority"},
        {"kind":"npc_decision", "requires":"real_consent_or_independent_valid_service_order"},
        {"kind":"npc_orders", "requires":"fleet_issued_and_current"},
        {"kind":"npc_departure_effective", "requires":"Core_event_releases_original_billet"},
        {"kind":"verify_origin_vacancy", "requires":"Core_occupant_null_and_revision"},
        {"kind":"player_selection", "requires":"P01_P02_merit_selection_player_decision"},
        {"kind":"player_appointment", "requires":"authorized_Core_assignment"}
    ]
    attrs = dict(base, incumbent_id=npc["character_id"],
                 selected_npc_opportunity_id=option["opportunity_id"],
                 selected_reason=status, causal_chain=chain, rejected_options=rejected,
                 incumbent_stays_until_authorized_departure=True,
                 next_milestone=option["effective_not_before_month"])
    if status == "NPC_CONSIDERING":
        return _out(NPC_WAIT,"NPC_MUST_MAKE_INDEPENDENT_CAREER_DECISION",**attrs)
    if status == "AWAITING_ORDERS":
        return _out(ORDERS_WAIT,"NPC_ACCEPTED_BUT_FLEET_ORDER_IS_MISSING",**attrs)
    if status == "ORDERS_EXIST_DEPARTURE_PENDING":
        return _out(DEPARTURE_WAIT,"NPC_ORDERS_VERIFIED_NOT_YET_RELINQUISHED",**attrs)
    # Even a transfer event cannot declare the slot vacant while the live Core
    # occupant record still says the old NPC is there.
    return _out(CONFIRM_WAIT,"NPC_DEPARTURE_RECORDED_ORIGIN_STILL_OCCUPIED",
                **attrs, required_next=["reconcile_authoritative_Core_slot_state",
                                        "reject_inconsistent_state_without_forced_eviction"])


def simulate_reference_ladder():
    """Cuatro escenarios sintéticos independientes. Son propuestas, NO recorrido jugable."""
    p = load_policy()
    d = p["project_ship_key"]
    proposals = []
    fixtures = [
        ("department_head","lieutenant_commander","chief_engineering_officer","other_ship","head-npc","engineering"),
        ("enterprise_d_first_officer","commander","first_officer",d,"xo-npc","command"),
        ("captain_other_ship","captain","commanding_officer","other_ship","other-captain-npc","command"),
        ("enterprise_d_captain","captain","commanding_officer",d,"captain-d-npc","command")
    ]
    for i,(stage,rank,position,unit_key,inc,department) in enumerate(fixtures):
        s = {
            "episode_id":f"case-{i}","upstream_plan_id":f"p03-plan-{i}",
            "rank_event_id":f"rank-{i}","stage":stage,"now_month":90+i*12,
            "ready_since_month":84+i*12,"deadline_month":93+i*12,
            "world_revision":42+i,"live_context_verified":True,
            "player":{"character_id":"player","rank":rank,"current_unit_id":"old-post",
                      "current_billet_id":"old-billet","current_position_id":"chief_engineering_officer",
                      "service_status":"active","professional_review_verified":True,
                      "preference":"continue",
                      "qualifications":["command_qualified","engineering_leadership_qualified"],
                      "department_qualification_verified":True},
            "target":{"unit_id":f"destination-{i}","unit_key":unit_key,"unit_type":"starship",
                      "unit_operational_verified":True,"billet_verified":True,
                      "billet_id":f"billet-{i}","position_id":position,
                      "vacancy_state":"occupied","occupant_id":inc},
            "incumbent":{"character_id":inc,"current_unit_id":f"destination-{i}",
                         "current_billet_id":f"billet-{i}","rank":"captain",
                         "service_status":"active","professional_review_verified":True,
                         "qualifications":["command_qualified"],
                         "career_motivation_event_ids":[f"npc-record-{i}"]},
            "opportunities":[{
                "opportunity_id":f"fleet-op-{i}","candidate_id":inc,
                "professional_reason_event_id":f"npc-record-{i}",
                "professional_source_events":[f"npc-record-{i}"],
                "kind":"fleet_staff" if stage=="enterprise_d_captain" else "ship_command",
                "npc_decision":"considering","prepared_at_month":88+i*12,
                "effective_not_before_month":91+i*12,
                "professional_merit_verified":True,"fleet_organizational_need_verified":True,
                "destination_unit_id":f"another-unit-{i}","destination_billet_id":f"other-billet-{i}",
                "destination_billet_state":"vacant","destination_operational_verified":True,
                "destination_billet_verified":True,"npc_qualified_for_destination":True,
                "fleet_staff_role_verified":True,
                "orders_verified":False,"departure_effective_verified":False
            }]
        }
        proposals.append(propose_succession(s,p))
    return proposals


if __name__ == "__main__":
    print(json.dumps([{"stage":x.get("stage"),"status":x["status"],"effects":x["effects_applied"]}
                      for x in simulate_reference_ladder()],ensure_ascii=False,indent=2))
