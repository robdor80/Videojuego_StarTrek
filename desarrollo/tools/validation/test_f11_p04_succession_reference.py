#!/usr/bin/env python3
"""F11-P04: pruebas de propuestas de carrera NPC. NUNCA ejecutan ascensos ni relevos."""
from __future__ import annotations

import copy
import unittest

try:
    from desarrollo.tools.validation.f11_p04_succession_reference import (
        load_policy, policy_valid, episode_plan_id, propose_succession,
        simulate_reference_ladder, INVALID, PAUSED, ALREADY, DIRECT,
        NPC_WAIT, ORDERS_WAIT, DEPARTURE_WAIT, CONFIRM_WAIT,
        ALTERNATIVE, URGENT, TAG
    )
except ModuleNotFoundError:
    from f11_p04_succession_reference import (
        load_policy, policy_valid, episode_plan_id, propose_succession,
        simulate_reference_ladder, INVALID, PAUSED, ALREADY, DIRECT,
        NPC_WAIT, ORDERS_WAIT, DEPARTURE_WAIT, CONFIRM_WAIT,
        ALTERNATIVE, URGENT, TAG
    )


def base():
    return {
        "episode_id":"episode-1", "upstream_plan_id":"p03-plan-1",
        "rank_event_id":"commander-rank-event-1",
        "stage":"enterprise_d_first_officer", "now_month":48,
        "ready_since_month":42, "deadline_month":51, "world_revision":12,
        "live_context_verified":True, "upstream_plan_verified":True,
        "ready_anchor_event_id":"ready-event-1",
        "player":{
            "character_id":"player-1", "rank":"commander",
            "current_unit_id":"ship-D-1", "current_billet_id":"eng-01",
            "current_position_id":"chief_engineering_officer",
            "service_status":"active", "professional_review_verified":True,
            "qualifications":["command_qualified","engineering_leadership_qualified"],
            "department_qualification_verified":True, "preference":"continue",
        },
        "target":{
            "unit_id":"ship-D-1", "unit_key":"enterprise_d_ncc_1701_d_refit",
            "unit_type":"starship", "unit_operational_verified":True,
            "billet_verified":True, "billet_id":"xo-D-1","position_id":"first_officer",
            "vacancy_state":"occupied", "occupant_id":"npc-xo-1",
        },
        "incumbent":{
            "character_id":"npc-xo-1", "current_unit_id":"ship-D-1",
            "current_billet_id":"xo-D-1", "rank":"commander",
            "service_status":"active", "professional_review_verified":True,
            "qualifications":["command_qualified"],
            "career_motivation_event_ids":["npc-eval-1","npc-command-ambition-2"],
        },
        "opportunities":[{
            "opportunity_id":"fleet-captain-offer-1", "candidate_id":"npc-xo-1",
            "professional_reason_event_id":"npc-command-ambition-2",
            "professional_source_events":["npc-eval-1","npc-command-ambition-2"],
            "kind":"ship_command","npc_decision":"considering",
            "prepared_at_month":44,"effective_not_before_month":49,
            "professional_merit_verified":True,
            "fleet_organizational_need_verified":True,
            "destination_unit_id":"another-ship-1",
            "destination_billet_id":"captain-other-ship-1",
            "destination_billet_state":"vacant",
            "destination_operational_verified":True,
            "destination_billet_verified":True,
            "npc_qualified_for_destination":True,
            "captain_promotion_board_verified":True,
            "orders_verified":False,"departure_effective_verified":False,
            "offer_issued_verified":False,"npc_decision_verified":False,
        }]
    }


class F11P04SuccessionTests(unittest.TestCase):
    def check(self, status, reason=None, *, top=None, player=None, target=None,
              npc=None, option=None, options=None):
        s=base()
        s.update(copy.deepcopy(top or {}))
        s["player"].update(copy.deepcopy(player or {}))
        s["target"].update(copy.deepcopy(target or {}))
        s["incumbent"].update(copy.deepcopy(npc or {}))
        s["opportunities"][0].update(copy.deepcopy(option or {}))
        if options is not None:
            s["opportunities"]=copy.deepcopy(options)
        original=copy.deepcopy(s)
        p=load_policy()
        original_policy=copy.deepcopy(p)
        result=propose_succession(s,p)
        self.assertEqual(result["status"],status)
        if reason:
            self.assertEqual(result["reason"],reason)
        self.assertEqual(result["authority"],TAG)
        self.assertEqual(result["effects_applied"],0)
        self.assertEqual(s,original,"El director NO muta ninguna entidad ni plaza")
        self.assertEqual(p,original_policy,"El contrato es inmutable")
        return result

    def test_01_policy_valid_and_offline(self):
        self.assertTrue(policy_valid(load_policy()))
        self.assertEqual(load_policy()["maturity"],TAG)

    def test_02_four_career_stages(self):
        self.assertEqual(set(load_policy()["target_stages"]),{
            "department_head","enterprise_d_first_officer",
            "captain_other_ship","enterprise_d_captain"
        })

    def test_03_plan_id_deterministic(self):
        self.assertEqual(episode_plan_id("a","b","c"),episode_plan_id("a","b","c"))

    def test_04_plan_id_differs_by_target(self):
        self.assertNotEqual(episode_plan_id("a","b","c"),episode_plan_id("a","b","d"))

    def test_05_xo_plausible_npc_career(self):
        r=self.check(NPC_WAIT,"NPC_MUST_MAKE_INDEPENDENT_CAREER_DECISION")
        self.assertEqual(r["incumbent_id"],"npc-xo-1")
        self.assertTrue(r["incumbent_stays_until_authorized_departure"])

    def test_06_journey_proposes_four_career_opportunities(self):
        rows=simulate_reference_ladder()
        self.assertEqual(len(rows),4)
        self.assertTrue(all(x["status"]==NPC_WAIT and x["effects_applied"]==0 for x in rows))

    def test_07_no_free_xo_vacancy_for_commander(self):
        r=self.check(NPC_WAIT)
        self.assertNotIn("new_rank",r)
        self.assertNotIn("vacancy_created",r)

    def test_08_bad_upstream_plan_identity_denied(self):
        self.check(INVALID,"MISSING_EPISODE_IDENTITY",top={"upstream_plan_id":""})

    def test_09_missing_episode_identity_denied(self):
        self.check(INVALID,"MISSING_EPISODE_IDENTITY",top={"episode_id":None})

    def test_10_invalid_stage_denied(self):
        self.check(INVALID,"UNSUPPORTED_CAREER_STAGE",top={"stage":"instant_galactic_admiral"})

    def test_11_missing_world_revision(self):
        self.check(INVALID,"INVALID_EPISODE_CLOCK",top={"world_revision":None})

    def test_12_boolean_not_world_revision(self):
        self.check(INVALID,"INVALID_EPISODE_CLOCK",top={"world_revision":True})

    def test_13_time_cannot_run_backward(self):
        self.check(INVALID,"STALE_OR_UNVERIFIED_EPISODE",top={"now_month":41})

    def test_14_ready_anchor_must_exist(self):
        self.check(INVALID,"STALE_OR_UNVERIFIED_EPISODE",top={"ready_anchor_event_id":None})

    def test_15_upstream_p03_plan_must_be_verified(self):
        self.check(INVALID,"STALE_OR_UNVERIFIED_EPISODE",top={"upstream_plan_verified":False})

    def test_16_live_world_required(self):
        self.check(INVALID,"STALE_OR_UNVERIFIED_EPISODE",top={"live_context_verified":False})

    def test_17_deadline_cannot_precede_ready_anchor(self):
        self.check(INVALID,"STALE_OR_UNVERIFIED_EPISODE",top={"deadline_month":41})

    def test_18_player_identity_must_exist(self):
        self.check(INVALID,"MISSING_PLAYER_IDENTITY",player={"character_id":""})

    def test_19_player_professional_review_required(self):
        self.check(INVALID,"PLAYER_CAREER_EVIDENCE_INCOMPLETE",
                   player={"professional_review_verified":False})

    def test_20_player_cannot_be_retired(self):
        self.check(INVALID,"PLAYER_CAREER_EVIDENCE_INCOMPLETE",
                   player={"service_status":"retired"})

    def test_21_player_preference_must_be_valid(self):
        self.check(INVALID,"PLAYER_PREFERENCE_INVALID",player={"preference":"auto_force"})

    def test_22_player_may_pause_without_rewriting_target(self):
        self.check(PAUSED,"PLAYER_REFUSES_OR_PAUSES_CURRENT_PATH",player={"preference":"pause"})

    def test_23_player_may_decline_without_forcing_leave(self):
        self.check(PAUSED,"PLAYER_REFUSES_OR_PAUSES_CURRENT_PATH",player={"preference":"decline"})

    def test_24_player_wrong_rank_for_xo(self):
        self.check(INVALID,"PLAYER_RANK_NOT_ELIGIBLE",player={"rank":"ensign"})

    def test_25_player_missing_command_qualification(self):
        self.check(INVALID,"PLAYER_COMMAND_QUALIFICATION_MISSING",
                   player={"qualifications":["engineering_leadership_qualified"]})

    def test_26_wrong_unit_not_enterprise_d(self):
        self.check(INVALID,"ENTERPRISE_D_UNIT_MISMATCH",
                   target={"unit_key":"other-ship"})

    def test_27_wrong_role_for_target(self):
        self.check(INVALID,"WRONG_TARGET_POSITION_FOR_STAGE",
                   target={"position_id":"commanding_officer"})

    def test_28_invalid_vacancy_enum(self):
        self.check(INVALID,"INVALID_TARGET_VACANCY_STATE",
                   target={"vacancy_state":"free_for_player_by_magic"})

    def test_29_falsely_vacant_while_npc_present(self):
        self.check(INVALID,"VACANCY_HAS_OCCUPANT",
                   target={"vacancy_state":"vacant"})

    def test_30_planned_replacement_does_not_release_incumbent(self):
        self.check(NPC_WAIT,target={"vacancy_state":"planned"})

    def test_31_occupied_position_must_have_incumbent(self):
        self.check(INVALID,"OCCUPIED_VACANCY_WITHOUT_NPC",
                   target={"occupant_id":None})

    def test_32_wrong_incumbent_identity_denied(self):
        self.check(INVALID,"NPC_DOES_NOT_OCCUPY_TARGET_BILLET",
                   npc={"character_id":"npc-wrong"})

    def test_33_incumbent_cannot_reside_in_other_unit(self):
        self.check(INVALID,"NPC_DOES_NOT_OCCUPY_TARGET_BILLET",
                   npc={"current_unit_id":"another-ship"})

    def test_34_incumbent_cannot_have_other_billet(self):
        self.check(INVALID,"NPC_DOES_NOT_OCCUPY_TARGET_BILLET",
                   npc={"current_billet_id":"engineering-slot"})

    def test_35_incumbent_review_verified(self):
        self.check(INVALID,"NPC_CAREER_EVIDENCE_INCOMPLETE",
                   npc={"professional_review_verified":False})

    def test_36_incumbent_not_retired(self):
        self.check(INVALID,"NPC_CAREER_EVIDENCE_INCOMPLETE",
                   npc={"service_status":"retired"})

    def test_37_incumbent_motivation_exists(self):
        self.check(INVALID,"NPC_CAREER_EVIDENCE_INCOMPLETE",
                   npc={"career_motivation_event_ids":[]})

    def test_38_opportunity_for_another_npc_cannot_displace_xo(self):
        r=self.check(ALTERNATIVE,option={"candidate_id":"another-npc"})
        self.assertEqual(r["rejected_options"][0]["reason"],"OPPORTUNITY_NPC_MISMATCH")

    def test_39_unsupported_opportunity_kind_skipped(self):
        r=self.check(ALTERNATIVE,option={"kind":"invented_death"})
        self.assertEqual(r["rejected_options"][0]["reason"],"OPPORTUNITY_NPC_MISMATCH")

    def test_40_no_opportunity_requires_alternative(self):
        self.check(ALTERNATIVE,"REPLAN_NPC_CAREER_WITH_REAL_OPTIONS",options=[])

    def test_41_overdue_without_opportunity_escalates(self):
        r=self.check(URGENT,"REPLAN_NPC_CAREER_WITH_REAL_OPTIONS",
                     top={"now_month":52},options=[])
        self.assertTrue(r["escalation_required"])
        self.assertEqual(r["ready_since_month"],42)

    def test_42_no_deadline_reset_even_after_years(self):
        r=self.check(URGENT,top={"now_month":180},options=[])
        self.assertEqual(r["deadline_month"],51)

    def test_43_refused_npc_offer_keeps_occupant(self):
        r=self.check(ALTERNATIVE,option={"npc_decision":"declined"})
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_DECLINED_OR_WITHDREW")

    def test_44_withdrawn_npc_offer_keeps_occupant(self):
        self.check(ALTERNATIVE,option={"npc_decision":"withdrawn"})

    def test_45_unverified_merit_cannot_prepare_credible_succession(self):
        r=self.check(ALTERNATIVE,option={"professional_merit_verified":False})
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_PROFESSIONAL_MERIT_UNVERIFIED")

    def test_46_fleet_need_must_be_grounded(self):
        r=self.check(ALTERNATIVE,option={"fleet_organizational_need_verified":False})
        self.assertEqual(r["rejected_options"][0]["reason"],"FLEET_NEED_UNVERIFIED")

    def test_47_npc_destination_must_actually_be_vacant(self):
        r=self.check(ALTERNATIVE,option={"destination_billet_state":"occupied"})
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_DESTINATION_NOT_GENUINELY_AVAILABLE")

    def test_48_destination_ship_operational_and_verified(self):
        r=self.check(ALTERNATIVE,option={"destination_operational_verified":False})
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_DESTINATION_NOT_GENUINELY_AVAILABLE")

    def test_49_destination_billet_exists(self):
        r=self.check(ALTERNATIVE,option={"destination_billet_verified":False})
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_DESTINATION_NOT_GENUINELY_AVAILABLE")

    def test_50_npc_qualified_for_new_post(self):
        r=self.check(ALTERNATIVE,option={"npc_qualified_for_destination":False})
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_DESTINATION_NOT_GENUINELY_AVAILABLE")

    def test_51_npc_cannot_transfer_to_same_ship_as_new_ship(self):
        r=self.check(ALTERNATIVE,option={"destination_unit_id":"ship-D-1"})
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_DESTINATION_NOT_GENUINELY_AVAILABLE")

    def test_52_npc_cannot_time_travel_to_propose(self):
        r=self.check(ALTERNATIVE,option={"prepared_at_month":49})
        self.assertEqual(r["rejected_options"][0]["reason"],"FUTURE_OR_NEGATIVE_PREPARATION_DATE")

    def test_53_no_same_day_transfer_without_notice(self):
        r=self.check(ALTERNATIVE,option={"effective_not_before_month":44})
        self.assertEqual(r["rejected_options"][0]["reason"],"MISSING_REASONABLE_NPC_NOTICE")

    def test_54_npc_cannot_be_accepted_without_signed_evidence(self):
        r=self.check(ALTERNATIVE,option={"npc_decision":"accepted"})
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_ACCEPTANCE_NOT_AUTHORITATIVELY_RECORDED")

    def test_55_npc_acceptance_records_never_auto_evict(self):
        option={"npc_decision":"accepted","offer_issued_verified":True,
                "npc_decision_verified":True,"npc_decision_event_id":"npc-choice-1"}
        self.check(ORDERS_WAIT,"NPC_ACCEPTED_BUT_FLEET_ORDER_IS_MISSING",option=option)

    def test_56_accepted_but_no_valid_order_cannot_leave(self):
        option={"npc_decision":"accepted","offer_issued_verified":True,
                "npc_decision_verified":True,"npc_decision_event_id":"npc-choice-1",
                "orders_verified":True}
        r=self.check(ALTERNATIVE,option=option)
        self.assertEqual(r["rejected_options"][0]["reason"],"UNVERIFIED_PERSONNEL_ORDER")

    def test_57_ordered_npc_remains_at_post_until_effective_departure(self):
        opt={"npc_decision":"accepted","offer_issued_verified":True,
             "npc_decision_verified":True,"npc_decision_event_id":"npc-choice-1",
             "orders_verified":True,"personnel_order_id":"fleet-order-1",
             "order_approved_by_fleet":True}
        self.check(DEPARTURE_WAIT,"NPC_ORDERS_VERIFIED_NOT_YET_RELINQUISHED",option=opt)

    def test_58_departure_effective_before_date_rejected(self):
        opt={"npc_decision":"accepted","offer_issued_verified":True,
             "npc_decision_verified":True,"npc_decision_event_id":"npc-choice-1",
             "orders_verified":True,"personnel_order_id":"fleet-order-1",
             "order_approved_by_fleet":True,"departure_effective_verified":True,
             "departure_event_id":"depart-1"}
        r=self.check(ALTERNATIVE,option=opt)
        self.assertEqual(r["rejected_options"][0]["reason"],"DEPARTURE_BEFORE_EFFECTIVE_DATE")

    def test_59_npc_departure_recorded_but_core_slot_still_occupied(self):
        opt={"npc_decision":"accepted","offer_issued_verified":True,
             "npc_decision_verified":True,"npc_decision_event_id":"npc-choice-1",
             "orders_verified":True,"personnel_order_id":"fleet-order-1",
             "order_approved_by_fleet":True,"departure_effective_verified":True,
             "departure_event_id":"depart-1"}
        self.check(CONFIRM_WAIT,"NPC_DEPARTURE_RECORDED_ORIGIN_STILL_OCCUPIED",
                   top={"now_month":50},option=opt)

    def test_60_real_vacancy_requires_verifiable_origin(self):
        self.check(INVALID,"VACANCY_PROVENANCE_UNVERIFIED",
                   target={"vacancy_state":"vacant","occupant_id":None})

    def test_61_real_authorized_vacancy_enters_player_selection(self):
        self.check(DIRECT,"VACANCY_ALREADY_REAL_PLAYER_STILL_NEEDS_SELECTION",
                   target={"vacancy_state":"vacant","occupant_id":None,
                           "vacancy_provenance_type":"verified_effective_departure",
                           "vacancy_event_id":"npc-departure-verified"})

    def test_62_newly_authorized_billet_can_be_vacant(self):
        self.check(DIRECT,target={"vacancy_state":"vacant","occupant_id":None,
                                 "vacancy_provenance_type":"authorized_new_billet",
                                 "vacancy_event_id":"fleet-new-billet-1"})

    def test_63_reserved_billet_not_automatically_available(self):
        self.check(ALTERNATIVE,target={"vacancy_state":"reserved","occupant_id":None})

    def test_64_suspended_billet_cannot_be_taken(self):
        self.check(ALTERNATIVE,target={"vacancy_state":"suspended","occupant_id":None})

    def test_65_decommissioned_billet_cannot_be_taken(self):
        self.check(ALTERNATIVE,target={"vacancy_state":"decommissioned","occupant_id":None})

    def test_66_player_already_in_correct_position_requires_no_new_plan(self):
        self.check(ALREADY,"PLAYER_ALREADY_OCCUPIES_TARGET_BILLET",
                   player={"current_billet_id":"xo-D-1","current_position_id":"first_officer"},
                   target={"occupant_id":"player-1"})

    def test_91_player_cannot_claim_an_npc_occupied_billet(self):
        self.check(INVALID,"PLAYER_AND_CORE_BILLET_OCCUPANT_DISAGREE",
                   player={"current_billet_id":"xo-D-1","current_position_id":"first_officer"})

    def test_92_slot_cannot_claim_player_if_player_still_elsewhere(self):
        self.check(INVALID,"PLAYER_AND_CORE_BILLET_OCCUPANT_DISAGREE",
                   target={"occupant_id":"player-1"})

    def test_67_npc_source_event_evidence_cannot_be_forged(self):
        r=self.check(ALTERNATIVE,option={"professional_source_events":["AI_invented_merit"]})
        self.assertEqual(r["rejected_options"][0]["reason"],"OPPORTUNITY_CAREER_EVIDENCE_INVALID")

    def test_68_npc_commander_needs_captain_board_for_ship_command(self):
        r=self.check(ALTERNATIVE,option={"captain_promotion_board_verified":False})
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_CAPTAIN_PROMOTION_BOARD_MISSING")

    def test_69_no_npc_command_qualification(self):
        r=self.check(ALTERNATIVE,npc={"qualifications":[]})
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_COMMAND_QUALIFICATION_MISSING")

    def test_70_duplicate_fleet_opportunity_id_rejected(self):
        op=base()["opportunities"][0]
        self.check(INVALID,"DUPLICATE_OPTION_ID",options=[op,copy.deepcopy(op)])

    def test_71_alternative_after_npc_refusal(self):
        first=base()["opportunities"][0]
        first["npc_decision"]="declined"
        other=copy.deepcopy(first)
        other.update({"opportunity_id":"fleet-captain-offer-2",
                      "npc_decision":"considering",
                      "destination_unit_id":"another-ship-2",
                      "destination_billet_id":"captain-ship-2"})
        r=self.check(NPC_WAIT,options=[first,other])
        self.assertEqual(r["selected_npc_opportunity_id"],"fleet-captain-offer-2")
        self.assertEqual(r["rejected_options"][0]["reason"],"NPC_DECLINED_OR_WITHDREW")

    def test_72_prefer_valid_accepted_offer_over_unaccepted(self):
        one=base()["opportunities"][0]
        two=copy.deepcopy(one)
        two.update({"opportunity_id":"offer-already-accepted",
                    "npc_decision":"accepted",
                    "destination_unit_id":"another-ship-2",
                    "destination_billet_id":"captain-ship-2",
                    "offer_issued_verified":True,
                    "npc_decision_verified":True,
                    "npc_decision_event_id":"npc-choice-2"})
        r=self.check(ORDERS_WAIT,options=[one,two])
        self.assertEqual(r["selected_npc_opportunity_id"],"offer-already-accepted")

    def test_73_urgent_flag_survives_when_npc_is_deliberating(self):
        r=self.check(NPC_WAIT,top={"now_month":60})
        self.assertTrue(r["escalation_required"])

    def test_74_no_new_episode_identity_per_tick(self):
        a=propose_succession(base())
        s=base()
        s["now_month"]=50
        b=propose_succession(s)
        self.assertEqual(a["episode_plan_id"],b["episode_plan_id"])

    def test_75_not_accidentally_ranked_as_a_new_captain(self):
        r=self.check(NPC_WAIT)
        self.assertEqual(r["effects_applied"],0)
        self.assertTrue(all(key not in r for key in (
            "new_rank","personnel_orders_created","npc_departed","player_appointed")))

    def test_76_captain_is_rank_not_automatic_enterprise_d_command(self):
        self.check(INVALID,"PLAYER_RANK_NOT_ELIGIBLE",player={"rank":"captain"})

    def test_77_not_applicable_to_unauthenticated_ship(self):
        self.check(INVALID,"TARGET_NOT_AUTHORITATIVELY_VERIFIED",
                   target={"unit_operational_verified":False})

    def test_78_target_billet_cannot_be_fake(self):
        self.check(INVALID,"TARGET_NOT_AUTHORITATIVELY_VERIFIED",
                   target={"billet_verified":False})

    def test_79_flag_fleet_career_requires_catalogued_staff_post(self):
        s=base()
        s["stage"]="enterprise_d_captain"
        s["player"]["rank"]="captain"
        s["target"]["position_id"]="commanding_officer"
        s["incumbent"]["rank"]="captain"
        s["opportunities"][0]["kind"]="fleet_staff"
        s["opportunities"][0]["fleet_staff_role_verified"]=False
        r=propose_succession(s)
        self.assertEqual(r["status"],ALTERNATIVE)
        self.assertEqual(r["rejected_options"][0]["reason"],"FLEET_STAFF_APPOINTMENT_NOT_CATALOGUED")

    def test_80_flag_fleet_career_with_real_post_prepares_option(self):
        s=base()
        s["stage"]="enterprise_d_captain"
        s["player"]["rank"]="captain"
        s["target"]["position_id"]="commanding_officer"
        s["incumbent"]["rank"]="captain"
        s["opportunities"][0]["kind"]="fleet_staff"
        s["opportunities"][0]["fleet_staff_role_verified"]=True
        self.assertEqual(propose_succession(s)["status"],NPC_WAIT)

    def test_81_captain_other_ship_does_not_depend_on_enterprise_d_vacancy(self):
        s=base()
        s["stage"]="captain_other_ship"
        s["player"]["rank"]="captain"
        s["target"].update({"unit_id":"ship-X","unit_key":"other_ship_verified",
                            "billet_id":"captain-X","position_id":"commanding_officer",
                            "occupant_id":None,"vacancy_state":"vacant",
                            "vacancy_provenance_type":"authorized_new_billet",
                            "vacancy_event_id":"activation-X"})
        self.assertEqual(propose_succession(s)["status"],DIRECT)

    def test_82_cannot_call_enterprise_d_an_other_ship(self):
        s=base()
        s["stage"]="captain_other_ship"
        s["player"]["rank"]="captain"
        s["target"]["position_id"]="commanding_officer"
        self.assertEqual(propose_succession(s)["reason"],"OTHER_COMMAND_MUST_BE_OTHER_SHIP")

    def test_83_department_head_opportunity_requires_qualification(self):
        s=base()
        s["stage"]="department_head"
        s["player"]["rank"]="lieutenant_commander"
        s["target"]["position_id"]="chief_engineering_officer"
        s["player"]["department_qualification_verified"]=False
        self.assertEqual(propose_succession(s)["reason"],"DEPARTMENT_QUALIFICATION_MISSING")

    def test_84_department_head_can_succeed_through_normal_transfer(self):
        s=base()
        s["stage"]="department_head"
        s["player"]["rank"]="lieutenant_commander"
        s["target"]["position_id"]="chief_engineering_officer"
        s["opportunities"][0]["kind"]="equivalent_transfer"
        self.assertEqual(propose_succession(s)["status"],NPC_WAIT)

    def test_85_existing_retirement_cannot_be_fabricated_today(self):
        r=self.check(ALTERNATIVE,
                     option={"kind":"existing_retirement",
                             "preexisting_retirement_event_id":"retire-1",
                             "preexisting_retirement_event_month":46})
        self.assertEqual(r["rejected_options"][0]["reason"],"RETIREMENT_NOT_INDEPENDENTLY_PREEXISTING")

    def test_86_existing_retirement_must_be_independently_recorded(self):
        r=self.check(NPC_WAIT,option={"kind":"existing_retirement",
                                     "preexisting_retirement_event_id":"retire-1",
                                     "preexisting_retirement_event_month":30})
        self.assertEqual(r["selected_reason"],"NPC_CONSIDERING")

    def test_87_malicious_order_before_acceptance_rejected(self):
        r=self.check(ALTERNATIVE,option={"orders_verified":True})
        self.assertEqual(r["rejected_options"][0]["reason"],"UNACCEPTED_NPC_OFFER_CANNOT_BE_EXECUTED")

    def test_88_decommissioned_starship_cannot_receive_succession(self):
        self.check(INVALID,"TARGET_NOT_AUTHORITATIVELY_VERIFIED",
                   target={"unit_operational_verified":False})

    def test_89_ready_anchor_does_not_auto_grant_any_billet(self):
        r=self.check(NPC_WAIT,top={"now_month":100})
        self.assertEqual(r["ready_since_month"],42)
        self.assertEqual(r["target_billet_id"],"xo-D-1")

    def test_90_invalid_policy_missing_core_stage(self):
        policy=load_policy()
        del policy["target_stages"]["enterprise_d_captain"]
        self.assertFalse(policy_valid(policy))


if __name__ == "__main__":
    unittest.main()
