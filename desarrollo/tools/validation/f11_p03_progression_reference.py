#!/usr/bin/env python3
"""F11-P03: referencia pura de evaluación y PREPARACIÓN de oportunidades.

No ejecuta rangos, nombramientos, movimientos de NPC, órdenes ni vacantes.
Una propuesta no es un ascenso. Los *_verified son datos ficticios de prueba;
en producción deben venir del Host/CoreRPG, nunca de la UI, PADD o LLM.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POLICY_PATH = ROOT / "sistemas/gameplay/careers/promotions/f11_p03_progression_policy_v0.1.json"
TAG = "OFFLINE_REFERENCE_ONLY_NO_WORLD_STATE_MUTATION"
DENIED = "REFERENCE_DENIED"
NOT_DUE = "NOT_DUE"
REVIEW = "REVIEW_PREPARATION_REQUIRED"
TRAINING = "TRAINING_PREPARATION_REQUIRED"
DISCIPLINE = "DISCIPLINE_RESOLUTION_REQUIRED"
FITNESS = "FITNESS_SUPPORT_REQUIRED"
PAUSED = "PAUSED_BY_PLAYER"
ANCHOR = "READY_ANCHOR_RECORD_REQUIRED"
PREPARED = "PLAN_PREPARED"
URGENT = "PLAN_URGENT"
ACTIVE = "PLAN_ALREADY_ACTIVE"
RANK_LIMIT = "CAPTAIN_POSITION_HANDOFF"

STEPS = (
    ("ensign", "lieutenant_junior_grade"),
    ("lieutenant_junior_grade", "lieutenant"),
    ("lieutenant", "lieutenant_commander"),
    ("lieutenant_commander", "commander"),
    ("commander", "captain"),
)
KNOWN_GOALS = frozenset(("advance_to_enterprise_d_captain",
                         "advance_in_current_specialty", "pause_progression"))


def load_policy():
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _str(v):
    return isinstance(v, str) and bool(v.strip())


def _ids(v):
    return isinstance(v, list) and all(_str(x) for x in v) and len(v) == len(set(v))


def _int(v):
    return type(v) is int


def _result(status, reason, **kwargs):
    return dict(status=status, reason=reason, authority=TAG, effects_applied=0, **kwargs)


def policy_is_valid(policy):
    if not isinstance(policy, dict) or policy.get("maturity") != "OFFLINE_REFERENCE_ONLY_NO_WORLD_STATE_MUTATION":
        return False
    steps = policy.get("commissioned_rank_steps")
    if not isinstance(steps, list) or len(steps) != len(STEPS):
        return False
    for entry, (source, target) in zip(steps, STEPS):
        if (not isinstance(entry, dict) or entry.get("from_rank") != source
                or entry.get("to_rank") != target or
                not _int(entry.get("illustrative_min_months")) or
                entry["illustrative_min_months"] < 1 or
                not _str(entry.get("opportunity_kind"))):
            return False
    if any(not _int(policy.get(k)) or policy[k] < 1 for k in (
            "illustrative_review_window_months",
            "illustrative_remediation_review_window_months",
            "illustrative_opportunity_horizon_months")):
        return False
    if policy.get("requirements", {}).get("no_generic_xp") is not True:
        return False
    if policy.get("requirements", {}).get("no_npc_displacement") is not True:
        return False
    return True


def next_rank(rank, policy=None):
    policy = load_policy() if policy is None else policy
    if not policy_is_valid(policy):
        return None
    return next((x["to_rank"] for x in policy["commissioned_rank_steps"]
                 if x["from_rank"] == rank), None)


def plan_key(actor_id, rank_event_id, target_rank, goal):
    """ID de episodio determinista, independiente de llamadas/revisión/tiempo."""
    source = f"F11-P03/v0.1|{actor_id}|{rank_event_id}|{target_rank}|{goal}"
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:24]


def _validate_snapshot(s, policy):
    if not policy_is_valid(policy) or not isinstance(s, dict):
        return "INVALID_POLICY_OR_SNAPSHOT"
    if (not _str(s.get("actor_id")) or not _str(s.get("rank_event_id")) or
            s.get("rank") not in ([x[0] for x in STEPS] + ["captain"])):
        return "MISSING_ACTOR_OR_RANK_SOURCE"
    for k in ("service_start_month", "rank_since_month", "now_month", "world_revision"):
        if not _int(s.get(k)):
            return "INVALID_SERVICE_CLOCK_OR_REVISION"
    if not (0 <= s["service_start_month"] <= s["rank_since_month"] <= s["now_month"]
            and s["world_revision"] >= 0):
        return "INCONSISTENT_SERVICE_CLOCK"
    if s.get("service_status") != "active" or s.get("context_verified") is not True:
        return "SERVICE_OR_CONTEXT_NOT_VERIFIED"
    if (s.get("goal") not in KNOWN_GOALS or type(s.get("player_opt_in")) is not bool
            or not _ids(s.get("qualifications"))):
        return "INVALID_PREFERENCES_OR_QUALIFICATIONS"
    if s.get("conduct_status") not in ("clear", "counseling", "active_sanction"):
        return "UNVERIFIED_DISCIPLINE_STATE"
    if s.get("medical_status") not in ("fit", "limited", "unfit"):
        return "UNVERIFIED_MEDICAL_STATUS"
    if not _ids(s.get("evidence_event_ids")):
        return "INVALID_EVIDENCE_SET"
    if s.get("qualification_assessment_verified") is not True:
        return "UNVERIFIED_QUALIFICATION_ASSESSMENT"
    if not _ids(s.get("missing_qualifications")):
        return "INVALID_QUALIFICATION_GAPS"
    if s.get("plan") is not None and not isinstance(s["plan"], dict):
        return "INVALID_EXISTING_PLAN"
    if s.get("pause_until_month") is not None and (
            not _int(s["pause_until_month"]) or s["pause_until_month"] < 0):
        return "INVALID_PAUSE"
    return None


def _review_state(s):
    rev = s.get("review")
    if rev is None:
        return "REVIEW_ABSENT"
    if not isinstance(rev, dict) or not _str(rev.get("review_id")):
        return "REVIEW_INVALID"
    if (rev.get("actor_id") != s["actor_id"] or
            rev.get("rank_event_id") != s["rank_event_id"] or
            rev.get("signed_by_authority") is not True or
            not _ids(rev.get("source_event_ids")) or
            not rev["source_event_ids"] or
            not set(rev["source_event_ids"]) <= set(s["evidence_event_ids"])):
        return "REVIEW_UNVERIFIED_OR_WRONG_ACTOR"
    if (not _int(rev.get("review_month")) or
            not s["rank_since_month"] <= rev["review_month"] <= s["now_month"] or
            not _int(rev.get("source_revision")) or
            not 0 <= rev["source_revision"] <= s["world_revision"]):
        return "REVIEW_TIME_OR_SOURCE_INVALID"
    if rev.get("outcome") not in ("satisfactory", "development_needed", "exceptional", "adverse"):
        return "REVIEW_OUTCOME_UNKNOWN"
    return None


def _opportunity_type(rank, goal):
    if rank == "commander":
        return "fleet_captain_selection_and_external_command"
    if rank == "lieutenant_commander":
        return "senior_officer_leadership_board"
    if rank == "lieutenant":
        return "future_departmental_post_preparation"
    return "routine_rank_promotion_review"


def evaluate_progression(snapshot, policy=None):
    """Una consulta pura. No modifica datos ni concede el próximo grado."""
    policy = load_policy() if policy is None else policy
    error = _validate_snapshot(snapshot, policy)
    if error:
        return _result(DENIED, error)
    s = snapshot
    if s["goal"] == "pause_progression" or not s["player_opt_in"] or (
            s.get("pause_until_month") is not None and s["now_month"] < s["pause_until_month"]):
        return _result(PAUSED, "VOLUNTARY_PLAYER_PAUSE")
    if s["rank"] == "captain":
        return _result(RANK_LIMIT, "CAPTAIN_RANK_NOT_ENTERPRISE_D_COMMAND",
                       next_phase="F11-P04", requires="authorized_enterprise_d_command_succession")
    step = next(x for x in policy["commissioned_rank_steps"] if x["from_rank"] == s["rank"])
    target = step["to_rank"]
    since_rank = s["now_month"] - s["rank_since_month"]
    if since_rank < step["illustrative_min_months"]:
        return _result(NOT_DUE, "MINIMUM_ILLUSTRATIVE_SERVICE_NOT_REACHED",
                       next_rank=target, missing_months=step["illustrative_min_months"] - since_rank)
    if s["conduct_status"] == "active_sanction":
        return _result(DISCIPLINE, "FORMAL_SANCTION_REQUIRES_REVIEW",
                       next_rank=target, next_review_no_later_than_month=(
                           s["now_month"] + policy["illustrative_remediation_review_window_months"]))
    if s["medical_status"] == "unfit":
        return _result(FITNESS, "MEDICAL_SUPPORT_AND_FITNESS_REVIEW_REQUIRED",
                       next_rank=target, punitive=False)
    if s["missing_qualifications"] or (
            target == "captain" and "command_qualified" not in s["qualifications"]):
        missing = sorted(set(s["missing_qualifications"]) |
                         ({"command_qualified"} if target == "captain" and
                          "command_qualified" not in s["qualifications"] else set()))
        return _result(TRAINING, "TRAINING_OR_MENTORSHIP_OPPORTUNITY_REQUIRED",
                       next_rank=target, missing_qualifications=missing,
                       review_by_month=s["now_month"]+policy["illustrative_remediation_review_window_months"])
    review_error = _review_state(s)
    if review_error:
        return _result(REVIEW, review_error, next_rank=target,
                       review_by_month=s["now_month"]+policy["illustrative_review_window_months"])
    if s["review"]["outcome"] in ("development_needed", "adverse"):
        return _result(TRAINING, "EVALUATION_REQUIRES_DEVELOPMENT_NOT_ARBITRARY_PROMOTION",
                       next_rank=target,
                       review_by_month=s["now_month"]+policy["illustrative_remediation_review_window_months"])
    # Anchor must be in the authoritative professional record. Resetting it on
    # every call would make the 'guaranteed within a horizon' promise impossible.
    start = s.get("ready_since_month")
    if not _int(start) or not s["rank_since_month"] <= start <= s["now_month"] or start < s["review"]["review_month"]:
        return _result(ANCHOR, "PERSISTENT_READY_ANCHOR_REQUIRED",
                       next_rank=target, suggested_anchor_month=s["now_month"],
                       needs_authoritative_event=True)
    key = plan_key(s["actor_id"], s["rank_event_id"], target, s["goal"])
    deadline = start + policy["illustrative_opportunity_horizon_months"]
    existing = s.get("plan")
    if existing is not None:
        if (existing.get("plan_id") != key or existing.get("rank_event_id") != s["rank_event_id"]
                or existing.get("target_rank") != target or
                existing.get("status") not in ("planned", "preparing", "offered") or
                not _int(existing.get("created_month")) or existing["created_month"] < start
                or existing["created_month"] > s["now_month"] or
                not _int(existing.get("deadline_month")) or
                existing["deadline_month"] != deadline):
            return _result(DENIED, "EXISTING_PLAN_STALE_OR_INCONSISTENT")
        if s["now_month"] < deadline:
            return _result(ACTIVE, "IDEMPOTENT_PLAN_EXISTS", plan_id=key,
                           next_rank=target, deadline_month=deadline, no_new_plan=True)
    status = URGENT if s["now_month"] >= deadline else PREPARED
    return _result(status,
                   "ELIGIBLE_WINDOW_REQUIRES_URGENT_CAUSAL_OPPORTUNITY" if status == URGENT
                   else "ELIGIBLE_WINDOW_HAS_PLANNED_CAUSAL_OPPORTUNITY",
                   plan_id=key, next_rank=target, opportunity_kind=_opportunity_type(s["rank"],s["goal"]),
                   ready_since_month=start, deadline_month=deadline,
                   proposed_events=["schedule_star_fleet_review", "prepare_professional_opportunity"],
                   handoff_to="F11-P04" if s["goal"]=="advance_to_enterprise_d_captain" else "F11-P03",
                   must_not=["award_rank","evict_npc","invent_vacancy","modify_world_state"],
                   escalation_required=status==URGENT)


def scenario_proposals_for_all_ranks(policy=None):
    """Campaña sintética: se ACTUALIZA rango mediante eventos ficticios externos,
    nunca por este módulo. Produce las propuestas para todas las etapas.
    """
    p = load_policy() if policy is None else policy
    if not policy_is_valid(p):
        raise ValueError("Invalid policy")
    out = []
    now = 0
    for index, stage in enumerate(p["commissioned_rank_steps"]):
        now += stage["illustrative_min_months"]
        rank = stage["from_rank"]
        rank_since = now - stage["illustrative_min_months"]
        snapshot = {
            "actor_id":"player-1","rank":rank,"rank_event_id":f"external-rank-event-{index}",
            "service_start_month":0,"rank_since_month":rank_since,"now_month":now,
            "world_revision":100+index,"service_status":"active","context_verified":True,
            "goal":"advance_to_enterprise_d_captain","player_opt_in":True,"pause_until_month":None,
            "qualifications":["command_qualified"] if rank=="commander" else [],
            "qualification_assessment_verified":True, "missing_qualifications":[],
            "medical_status":"fit","conduct_status":"clear",
            "evidence_event_ids":[f"service-evidence-{index}"],
            "review":{"review_id":f"review-{index}","actor_id":"player-1",
                      "rank_event_id":f"external-rank-event-{index}","signed_by_authority":True,
                      "source_event_ids":[f"service-evidence-{index}"],
                      "review_month":now,"source_revision":100+index,"outcome":"satisfactory"},
            "ready_since_month":now,"plan":None,
        }
        res = evaluate_progression(snapshot,p)
        out.append({"rank":rank, "proposed_next_rank":res.get("next_rank"), "status":res["status"],
                    "plan_id":res.get("plan_id")})
    return out


if __name__ == "__main__":
    print(json.dumps(scenario_proposals_for_all_ranks(),indent=2,ensure_ascii=False))
