#!/usr/bin/env python3
"""F11-P03: invariantes de progresión GARANTIZADA en modo referencia puro.

Estos test NO prueban que Core/Unreal pueda nombrar ni trasladar al jugador.
"""
import copy
import unittest

try:
    from desarrollo.tools.validation.f11_p03_progression_reference import (
        load_policy, policy_is_valid, evaluate_progression, scenario_proposals_for_all_ranks,
        plan_key, next_rank, DENIED, NOT_DUE, REVIEW, TRAINING, DISCIPLINE,
        FITNESS, PAUSED, ANCHOR, PREPARED, URGENT, ACTIVE, RANK_LIMIT, TAG,
    )
except ModuleNotFoundError:
    from f11_p03_progression_reference import (
        load_policy, policy_is_valid, evaluate_progression, scenario_proposals_for_all_ranks,
        plan_key, next_rank, DENIED, NOT_DUE, REVIEW, TRAINING, DISCIPLINE,
        FITNESS, PAUSED, ANCHOR, PREPARED, URGENT, ACTIVE, RANK_LIMIT, TAG,
    )


def base(rank="ensign", now=12, since=0):
    return {
        "actor_id":"player-1", "rank":rank, "rank_event_id":"event-ensign-1",
        "service_start_month":0,"rank_since_month":since,"now_month":now,
        "world_revision":8,"service_status":"active","context_verified":True,
        "goal":"advance_to_enterprise_d_captain","player_opt_in":True,"pause_until_month":None,
        "qualifications":["command_qualified"] if rank=="commander" else [],
        "qualification_assessment_verified":True,"missing_qualifications":[],
        "conduct_status":"clear","medical_status":"fit","evidence_event_ids":["watch-1","mission-2"],
        "review":{"review_id":"review-1","actor_id":"player-1","rank_event_id":"event-ensign-1",
                  "signed_by_authority":True,"source_event_ids":["watch-1"],
                  "review_month":now,"source_revision":8,"outcome":"satisfactory"},
        "ready_since_month":now,"plan":None,
    }


class F11P03ProgressionTests(unittest.TestCase):
    def test(self, expected, reason=None, changes=None, policy=None):
        s=base()
        if changes:
            s.update(copy.deepcopy(changes))
        old=copy.deepcopy(s)
        p=copy.deepcopy(load_policy()) if policy is None else copy.deepcopy(policy)
        oldp=copy.deepcopy(p)
        result=evaluate_progression(s,p)
        self.assertEqual(result["status"],expected)
        if reason:
            self.assertEqual(result["reason"],reason)
        self.assertEqual(result["authority"],TAG)
        self.assertEqual(result["effects_applied"],0)
        self.assertEqual(s,old,"Never mutate professional snapshot")
        self.assertEqual(p,oldp,"Never mutate policy")
        return result

    def test_01_policy_valid(self):
        self.assertTrue(policy_is_valid(load_policy()))

    def test_02_five_adjacent_ranks(self):
        self.assertEqual([x["to_rank"] for x in load_policy()["commissioned_rank_steps"]],
                         ["lieutenant_junior_grade","lieutenant","lieutenant_commander","commander","captain"])

    def test_03_next_rank_ensign(self):
        self.assertEqual(next_rank("ensign"),"lieutenant_junior_grade")

    def test_04_next_rank_captain_none(self):
        self.assertIsNone(next_rank("captain"))

    def test_05_deterministic_plan_key(self):
        self.assertEqual(plan_key("pc","rank","lieutenant","goal"),
                         plan_key("pc","rank","lieutenant","goal"))

    def test_06_plan_key_differs_for_rank_event(self):
        self.assertNotEqual(plan_key("pc","rank-a","lieutenant","goal"),
                            plan_key("pc","rank-b","lieutenant","goal"))

    def test_07_eligible_returns_plan_not_rank(self):
        r=self.test(PREPARED, "ELIGIBLE_WINDOW_HAS_PLANNED_CAUSAL_OPPORTUNITY")
        self.assertEqual(r["next_rank"],"lieutenant_junior_grade")
        self.assertNotIn("new_rank",r)
        self.assertIn("award_rank",r["must_not"])

    def test_08_no_xp_ever_consulted(self):
        r1=evaluate_progression(base())
        x=base()
        x["XP"]=999999
        x["levels"]=1000
        self.assertEqual(r1,evaluate_progression(x))

    def test_09_service_time_not_due(self):
        self.test(NOT_DUE,"MINIMUM_ILLUSTRATIVE_SERVICE_NOT_REACHED",
                  {"now_month":11,"ready_since_month":11,"review":dict(base(now=11)["review"])})

    def test_10_rank_clock_must_be_consistent(self):
        self.test(DENIED,"INCONSISTENT_SERVICE_CLOCK",{"rank_since_month":13})

    def test_11_missing_character_id(self):
        self.test(DENIED,"MISSING_ACTOR_OR_RANK_SOURCE",{"actor_id":""})

    def test_12_missing_rank_event_id(self):
        self.test(DENIED,"MISSING_ACTOR_OR_RANK_SOURCE",{"rank_event_id":None})

    def test_13_invalid_rank(self):
        self.test(DENIED,"MISSING_ACTOR_OR_RANK_SOURCE",{"rank":"omnipotent_admiral"})

    def test_14_inactive_character_denied(self):
        self.test(DENIED,"SERVICE_OR_CONTEXT_NOT_VERIFIED",{"service_status":"retired"})

    def test_15_snapshot_unverified_denied(self):
        self.test(DENIED,"SERVICE_OR_CONTEXT_NOT_VERIFIED",{"context_verified":False})

    def test_16_invalid_world_revision(self):
        self.test(DENIED,"INVALID_SERVICE_CLOCK_OR_REVISION",{"world_revision":"8"})

    def test_17_negative_service_clock(self):
        self.test(DENIED,"INCONSISTENT_SERVICE_CLOCK",{"service_start_month":-1})

    def test_18_wrong_goal_denied(self):
        self.test(DENIED,"INVALID_PREFERENCES_OR_QUALIFICATIONS",{"goal":"immediately_become_admiral"})

    def test_19_player_opt_out_pauses(self):
        self.test(PAUSED,"VOLUNTARY_PLAYER_PAUSE",{"player_opt_in":False})

    def test_20_decline_promotion_pauses(self):
        self.test(PAUSED,"VOLUNTARY_PLAYER_PAUSE",{"goal":"pause_progression"})

    def test_21_pause_until_tick_pauses(self):
        self.test(PAUSED,"VOLUNTARY_PLAYER_PAUSE",{"pause_until_month":13})

    def test_22_pause_elapsed_rechecks(self):
        self.test(PREPARED,changes={"pause_until_month":12})

    def test_23_invalid_pause_denied(self):
        self.test(DENIED,"INVALID_PAUSE",{"pause_until_month":"forever"})

    def test_24_active_sanction_requires_review_not_automatic_rank(self):
        r=self.test(DISCIPLINE,"FORMAL_SANCTION_REQUIRES_REVIEW",{"conduct_status":"active_sanction"})
        self.assertGreater(r["next_review_no_later_than_month"],12)

    def test_25_counseling_not_permanent_block(self):
        self.test(PREPARED,changes={"conduct_status":"counseling"})

    def test_26_medical_unfit_requires_support_not_punishment(self):
        r=self.test(FITNESS,"MEDICAL_SUPPORT_AND_FITNESS_REVIEW_REQUIRED",
                    {"medical_status":"unfit"})
        self.assertIs(r["punitive"],False)

    def test_27_medical_limited_does_not_automatically_sanction(self):
        self.test(PREPARED,changes={"medical_status":"limited"})

    def test_28_missing_training_generates_remediation(self):
        r=self.test(TRAINING,"TRAINING_OR_MENTORSHIP_OPPORTUNITY_REQUIRED",
                    {"missing_qualifications":["scientific-leadership"]})
        self.assertIn("scientific-leadership",r["missing_qualifications"])

    def test_29_empty_review_generates_formal_review(self):
        self.test(REVIEW,"REVIEW_ABSENT",{"review":None})

    def test_30_unsigned_review_does_not_promote(self):
        rev=copy.deepcopy(base()["review"])
        rev["signed_by_authority"]=False
        self.test(REVIEW,"REVIEW_UNVERIFIED_OR_WRONG_ACTOR",{"review":rev})

    def test_31_review_from_another_person_denied(self):
        rev=copy.deepcopy(base()["review"])
        rev["actor_id"]="npc-another"
        self.test(REVIEW,"REVIEW_UNVERIFIED_OR_WRONG_ACTOR",{"review":rev})

    def test_32_review_from_previous_rank_denied(self):
        rev=copy.deepcopy(base()["review"])
        rev["rank_event_id"]="prior-rank"
        self.test(REVIEW,"REVIEW_UNVERIFIED_OR_WRONG_ACTOR",{"review":rev})

    def test_33_review_must_reference_real_evidence(self):
        rev=copy.deepcopy(base()["review"])
        rev["source_event_ids"]=["invented-ai-report"]
        self.test(REVIEW,"REVIEW_UNVERIFIED_OR_WRONG_ACTOR",{"review":rev})

    def test_34_ai_cannot_decide_review(self):
        rev=copy.deepcopy(base()["review"])
        rev["signed_by_authority"]=False
        rev["LLM_says"]="excellent"
        self.test(REVIEW,"REVIEW_UNVERIFIED_OR_WRONG_ACTOR",{"review":rev})

    def test_35_review_from_future_denied(self):
        rev=copy.deepcopy(base()["review"])
        rev["review_month"]=13
        self.test(REVIEW,"REVIEW_TIME_OR_SOURCE_INVALID",{"review":rev})

    def test_36_review_revision_from_future_denied(self):
        rev=copy.deepcopy(base()["review"])
        rev["source_revision"]=9
        self.test(REVIEW,"REVIEW_TIME_OR_SOURCE_INVALID",{"review":rev})

    def test_37_review_can_survive_later_world_revision(self):
        self.test(PREPARED,changes={"world_revision":9})

    def test_38_satisfactory_and_exceptional_are_both_eligible(self):
        rev=copy.deepcopy(base()["review"])
        rev["outcome"]="exceptional"
        self.test(PREPARED,changes={"review":rev})

    def test_39_needs_improvement_generates_development(self):
        rev=copy.deepcopy(base()["review"])
        rev["outcome"]="development_needed"
        self.test(TRAINING,"EVALUATION_REQUIRES_DEVELOPMENT_NOT_ARBITRARY_PROMOTION",
                  {"review":rev})

    def test_40_adverse_review_generates_development(self):
        rev=copy.deepcopy(base()["review"])
        rev["outcome"]="adverse"
        self.test(TRAINING,changes={"review":rev})

    def test_41_ready_timestamp_must_be_persistent(self):
        self.test(ANCHOR,"PERSISTENT_READY_ANCHOR_REQUIRED",{"ready_since_month":None})

    def test_42_ready_anchor_cannot_precede_review(self):
        self.test(ANCHOR,"PERSISTENT_READY_ANCHOR_REQUIRED",{"ready_since_month":11})

    def test_43_ready_anchor_cannot_come_from_future(self):
        self.test(ANCHOR,changes={"ready_since_month":13})

    def test_44_ready_anchor_reuses_finite_deadline(self):
        r=self.test(PREPARED)
        self.assertEqual(r["deadline_month"],21)
        self.assertEqual(r["ready_since_month"],12)

    def test_45_ready_after_horizon_must_escalate(self):
        s=base(now=22)
        s["review"]["review_month"]=12
        s["ready_since_month"]=12
        self.test(URGENT,changes=s)

    def test_46_at_horizon_must_escalate(self):
        s=base(now=21)
        s["review"]["review_month"]=12
        s["ready_since_month"]=12
        self.test(URGENT,changes=s)

    def test_47_plan_not_affected_by_world_revision_change(self):
        s=base()
        a=evaluate_progression(s)
        s["world_revision"]=105
        b=evaluate_progression(s)
        self.assertEqual(a["plan_id"],b["plan_id"])

    def test_48_plan_not_affected_by_now_after_ready(self):
        s=base()
        a=evaluate_progression(s)
        s["now_month"]=20
        b=evaluate_progression(s)
        self.assertEqual(a["plan_id"],b["plan_id"])

    def test_49_valid_existing_plan_prevents_duplicate(self):
        p=evaluate_progression(base())
        self.test(ACTIVE,"IDEMPOTENT_PLAN_EXISTS",
                  {"plan":{"plan_id":p["plan_id"],"rank_event_id":"event-ensign-1",
                           "target_rank":"lieutenant_junior_grade","status":"planned",
                           "created_month":12,"deadline_month":21}})

    def test_50_wrong_plan_id_denied(self):
        self.test(DENIED,"EXISTING_PLAN_STALE_OR_INCONSISTENT",
                  {"plan":{"plan_id":"invented","rank_event_id":"event-ensign-1",
                           "target_rank":"lieutenant_junior_grade","status":"planned",
                           "created_month":12,"deadline_month":21}})

    def test_51_invalid_existing_plan_denied(self):
        self.test(DENIED,"INVALID_EXISTING_PLAN",{"plan":"hacked"})

    def test_52_future_plan_creation_denied(self):
        k=evaluate_progression(base())["plan_id"]
        self.test(DENIED,"EXISTING_PLAN_STALE_OR_INCONSISTENT",
                  {"plan":{"plan_id":k,"rank_event_id":"event-ensign-1",
                           "target_rank":"lieutenant_junior_grade","status":"planned",
                           "created_month":30,"deadline_month":21}})

    def test_53_captain_promotion_requires_command_qualification(self):
        s=base(rank="commander",now=24)
        s["qualifications"]=[]
        self.test(TRAINING,"TRAINING_OR_MENTORSHIP_OPPORTUNITY_REQUIRED",changes=s)

    def test_54_commander_promotes_to_captain_with_prepared_external_ship(self):
        s=base(rank="commander",now=24)
        r=self.test(PREPARED,changes=s)
        self.assertEqual(r["next_rank"],"captain")
        self.assertEqual(r["opportunity_kind"],"fleet_captain_selection_and_external_command")

    def test_55_captain_still_needs_enterprise_d_command(self):
        s=base(rank="captain",now=80)
        self.test(RANK_LIMIT,"CAPTAIN_RANK_NOT_ENTERPRISE_D_COMMAND",s)

    def test_56_evaluation_without_xp_makes_senior_route_possible(self):
        s=base(rank="lieutenant",now=18)
        r=self.test(PREPARED,changes=s)
        self.assertEqual(r["next_rank"],"lieutenant_commander")
        self.assertEqual(r["opportunity_kind"],"future_departmental_post_preparation")

    def test_57_mission_record_must_have_verified_evidence(self):
        self.test(DENIED,"INVALID_EVIDENCE_SET",{"evidence_event_ids":None})

    def test_58_unverified_qualification_assessment_denied(self):
        self.test(DENIED,"UNVERIFIED_QUALIFICATION_ASSESSMENT",
                  {"qualification_assessment_verified":False})

    def test_59_illustrative_policy_disallows_zero_horizon(self):
        p=load_policy()
        p["illustrative_opportunity_horizon_months"]=0
        self.assertFalse(policy_is_valid(p))

    def test_60_policy_cannot_skip_rank_steps(self):
        p=load_policy()
        p["commissioned_rank_steps"][0]["to_rank"]="captain"
        self.assertFalse(policy_is_valid(p))

    def test_61_all_rank_stages_propose_without_automatic_promotion(self):
        out=scenario_proposals_for_all_ranks()
        self.assertEqual(len(out),5)
        self.assertTrue(all(x["status"]==PREPARED for x in out))
        self.assertEqual([x["proposed_next_rank"] for x in out],
                         ["lieutenant_junior_grade","lieutenant","lieutenant_commander",
                          "commander","captain"])
        self.assertEqual(len({x["plan_id"] for x in out}),5)

    def test_62_no_perpetual_wait_without_urgent_escalation(self):
        p=load_policy()
        for gap in range(0,40):
            s=base(now=12+gap)
            s["ready_since_month"]=12
            s["review"]["review_month"]=12
            r=evaluate_progression(s,p)
            expected=PREPARED if gap < p["illustrative_opportunity_horizon_months"] else URGENT
            self.assertEqual(r["status"],expected)

    def test_63_urgent_repeatedly_does_not_vanish_at_later_times(self):
        for now in (21,22,48,120,1000):
            s=base(now=now)
            s["ready_since_month"]=12
            s["review"]["review_month"]=12
            self.assertEqual(evaluate_progression(s)["status"],URGENT)

    def test_64_plan_id_unique_for_each_player(self):
        p1=evaluate_progression(base())["plan_id"]
        s=base()
        s["actor_id"]="player-2"
        s["review"]["actor_id"]="player-2"
        self.assertNotEqual(p1,evaluate_progression(s)["plan_id"])

    def test_65_commendation_does_not_override_sanction(self):
        s=base()
        s["conduct_status"]="active_sanction"
        s["commendations"]=["medal-of-honor"]
        self.assertEqual(evaluate_progression(s)["status"],DISCIPLINE)

    def test_66_rank_promotion_plan_does_not_require_a_ship_vacancy(self):
        s=base()
        s["available_ship_billets"]=0
        self.assertEqual(evaluate_progression(s)["status"],PREPARED)

    def test_67_retired_rank_should_not_start_new_progression(self):
        self.test(DENIED,"SERVICE_OR_CONTEXT_NOT_VERIFIED",{"service_status":"retired"})

    def test_68_no_unverifiable_result_can_apply_effects(self):
        for status in (DENIED,NOT_DUE,REVIEW,TRAINING,DISCIPLINE,FITNESS,PAUSED,ANCHOR,
                       PREPARED,URGENT,ACTIVE,RANK_LIMIT):
            self.assertIsInstance(status,str)
        for candidate in [base(),base(rank="commander",now=24),base(rank="captain",now=80)]:
            self.assertEqual(evaluate_progression(candidate)["effects_applied"],0)


if __name__ == "__main__":
    unittest.main()
