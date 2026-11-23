#!/usr/bin/env python3
"""F11-P02: pruebas puras del cribado. Nunca declaran una plaza ocupada en Core."""
import copy
import json
import unittest

try:
    from desarrollo.tools.validation.f11_p02_assignments_reference import (
        load_references, validate_catalog, screen_billet,
        review_offer_transition, CANDIDATE, WAITING, BLOCKED, REVIEW, TAG
    )
except ModuleNotFoundError:
    from f11_p02_assignments_reference import (
        load_references, validate_catalog, screen_billet,
        review_offer_transition, CANDIDATE, WAITING, BLOCKED, REVIEW, TAG
    )


PERSON = {
    "character_id": "cadet-11", "rank": "ensign", "service_status": "commissioned",
    "qualifications": ["science_qualified"], "medical_status": "fit",
    "current_unit_id": None, "current_billet_id": None, "current_department_id": None,
}
UNIT = {
    "unit_id": "ship-synthetic-galaxy-01", "type": "starship",
    "class_id": "galaxy", "live_unit_verified": True, "operational": True,
    "era_profile": "tng_ds9_voyager", "campaign_year": 2387,
    "world_revision": 12, "time_tick": 100,
}
BILLET = {
    "billet_id": "slot-12001", "unit_id": "ship-synthetic-galaxy-01",
    "profile_id": "science_officer", "slot_reference_verified": True,
    "vacancy_state": "vacant", "occupant_id": None,
}
OFFER = {
    "offer_id": "offer-synthetic-1", "candidate_id": "cadet-11",
    "unit_id": "ship-synthetic-galaxy-01", "billet_id": "slot-12001",
    "status": "offered", "intent": "first_assignment",
    "world_revision": 12, "issued_at_tick": 90, "expires_at_tick": 150,
    "personnel_authority_verified": True, "selection_authorized": True,
    "order_id": "orders-1", "formal_order_verified": True,
    "order_effective_at_tick": 90, "atomic_core_transaction_authorized": True,
}


class F11P02ReferenceTests(unittest.TestCase):
    def check(self, expected, reason=None, *, person=None, unit=None, billet=None,
              intent="first_assignment", person_changes=None, unit_changes=None, billet_changes=None):
        p = copy.deepcopy(PERSON if person is None else person)
        u = copy.deepcopy(UNIT if unit is None else unit)
        b = copy.deepcopy(BILLET if billet is None else billet)
        p.update(person_changes or {})
        u.update(unit_changes or {})
        b.update(billet_changes or {})
        before = copy.deepcopy((p,u,b))
        result = screen_billet(p,u,b,intent)
        self.assertEqual(result["status"], expected)
        if reason:
            self.assertIn(reason, result["reasons"])
        self.assertEqual(result["authority"], TAG)
        self.assertEqual(result["effects_applied"], 0)
        self.assertEqual(before, (p,u,b), "Screening must not mutate its inputs")
        return result

    def offer(self, status, target, expected, reason=None, *,
              changes=None, unit_changes=None, billet_changes=None):
        p,u,b,o = copy.deepcopy((PERSON,UNIT,BILLET,OFFER))
        o["status"] = status
        o.update(changes or {})
        u.update(unit_changes or {})
        b.update(billet_changes or {})
        before = copy.deepcopy((p,u,b,o))
        result = review_offer_transition(p,u,b,o,target)
        self.assertEqual(result["status"],expected)
        if reason:
            self.assertIn(reason,result["reasons"])
        self.assertEqual(result["authority"], TAG)
        self.assertEqual(result["effects_applied"],0)
        self.assertEqual(before,(p,u,b,o), "Offer validation must not mutate")
        return result

    def test_01_catalog_matches_existing_star_fleet_positions(self):
        self.assertTrue(validate_catalog())

    def test_02_seven_f04_groups_preserved(self):
        catalog,_ = load_references()
        self.assertEqual({x["f04_department_id"] for x in catalog["groups"]},set(range(1,8)))

    def test_03_formal_and_functional_profiles_not_confused(self):
        catalog,_ = load_references()
        self.assertEqual(sum(p["classification"]=="existing_formal_position" for p in catalog["profiles"]),14)
        self.assertEqual(sum(p["classification"]=="functional_assignment_reference_only" for p in catalog["profiles"]),9)
        self.assertTrue(all(p["formal_position_id"] is None for p in catalog["profiles"]
                            if p["classification"]=="functional_assignment_reference_only"))

    def test_04_ensign_qualified_first_assignment_candidate(self):
        self.check(CANDIDATE,"ELIGIBLE_FOR_AUTHORIZED_REVIEW_ONLY")

    def test_05_uncommissioned_student_is_not_assigned(self):
        self.check(BLOCKED,"NOT_COMMISSIONED_FOR_FIRST_ASSIGNMENT",person_changes={"service_status":"graduated"})

    def test_06_non_ensign_initial_assignment_requires_special_route(self):
        self.check(BLOCKED,"NOT_COMMISSIONED_FOR_FIRST_ASSIGNMENT",person_changes={"rank":"lieutenant"})

    def test_07_existing_unit_disallows_first_assignment(self):
        self.check(BLOCKED,"NOT_COMMISSIONED_FOR_FIRST_ASSIGNMENT",
                   person_changes={"current_unit_id":"another-unit"})

    def test_08_rank_incompatible(self):
        self.check(BLOCKED,"RANK_NOT_COMPATIBLE_WITH_BILLET",
                   person_changes={"rank":"captain"})

    def test_09_missing_professional_qualification(self):
        self.check(BLOCKED,"MISSING_PROFESSIONAL_QUALIFICATION",
                   person_changes={"qualifications":[]})

    def test_10_medically_unfit_not_assignable(self):
        self.check(BLOCKED,"PERSON_NOT_VERIFIABLE_OR_FIT",
                   person_changes={"medical_status":"unfit"})

    def test_11_missing_actor_identity_denied(self):
        self.check(BLOCKED,"PERSON_NOT_VERIFIABLE_OR_FIT",
                   person_changes={"character_id":""})

    def test_12_ship_not_operational(self):
        self.check(BLOCKED,"UNIT_NOT_VERIFIED_OPERATIONAL",
                   unit_changes={"operational":False})

    def test_13_unverified_ship_denied(self):
        self.check(BLOCKED,"UNIT_NOT_VERIFIED_OPERATIONAL",
                   unit_changes={"live_unit_verified":False})

    def test_14_galaxy_not_operational_in_pike_era(self):
        self.check(BLOCKED,"STARSHIP_CLASS_NOT_TEMPORALLY_VERIFIED",
                   unit_changes={"era_profile":"pike","campaign_year":2255})

    def test_15_unverified_odyssey_not_silently_enabled(self):
        self.check(BLOCKED,"STARSHIP_CLASS_NOT_TEMPORALLY_VERIFIED",
                   unit_changes={"class_id":"odyssey","campaign_year":2387})

    def test_16_nonship_station_requires_era_activation(self):
        self.check(BLOCKED,"NONSHIP_ACTIVATION_NOT_VERIFIED",
                   unit_changes={"type":"station","class_id":None})

    def test_17_valid_station_can_be_screened(self):
        self.check(CANDIDATE,unit_changes={"type":"station","class_id":None,"nonship_activation_verified":True})

    def test_18_slot_of_other_unit_denied(self):
        self.check(BLOCKED,"SLOT_NOT_VERIFIED_OR_WRONG_UNIT",
                   billet_changes={"unit_id":"other-ship"})

    def test_19_unverified_slot_denied(self):
        self.check(BLOCKED,"SLOT_NOT_VERIFIED_OR_WRONG_UNIT",
                   billet_changes={"slot_reference_verified":False})

    def test_20_unknown_professional_profile_denied(self):
        self.check(BLOCKED,"UNKNOWN_BILLET_PROFILE",
                   billet_changes={"profile_id":"self_proclaimed_admiral"})

    def test_21_vacant_state_cannot_have_occupant(self):
        self.check(BLOCKED,"INCONSISTENT_BILLET_STATE",
                   billet_changes={"occupant_id":"npc-1"})

    def test_22_occupied_is_not_vacant_even_if_desired_by_player(self):
        self.check(WAITING,"BILLET_NOT_EFFECTIVELY_VACANT",
                   billet_changes={"vacancy_state":"occupied","occupant_id":"npc-1"})

    def test_23_planned_npc_transfer_does_not_free_slot(self):
        r=self.check(WAITING,"BILLET_NOT_EFFECTIVELY_VACANT",
                     billet_changes={"vacancy_state":"planned","occupant_id":"npc-xo"})
        self.assertEqual(r["vacancy_state"],"planned")

    def test_24_reserved_slot_is_not_general_vacancy(self):
        self.check(WAITING,"BILLET_NOT_EFFECTIVELY_VACANT",
                   billet_changes={"vacancy_state":"reserved","occupant_id":None})

    def test_25_planned_slot_must_keep_real_occupant(self):
        self.check(BLOCKED,"INCONSISTENT_BILLET_STATE",
                   billet_changes={"vacancy_state":"planned","occupant_id":None})

    def test_26_retired_slot_not_applicable(self):
        self.check(BLOCKED,"BILLET_NOT_USABLE",
                   billet_changes={"vacancy_state":"decommissioned"})

    def test_27_suspended_slot_not_applicable(self):
        self.check(BLOCKED,"BILLET_NOT_USABLE",
                   billet_changes={"vacancy_state":"suspended"})

    def test_28_valid_transfer_between_ships(self):
        self.check(CANDIDATE,intent="transfer",
                   person_changes={"service_status":"active","current_unit_id":"ship-old",
                                   "current_billet_id":"slot-old","current_department_id":"science"})

    def test_29_same_unit_not_transfer(self):
        self.check(BLOCKED,"SAME_UNIT_USE_POSITION_CHANGE",intent="transfer",
                   person_changes={"service_status":"active","current_unit_id":UNIT["unit_id"],
                                   "current_billet_id":"slot-old","current_department_id":"science"})

    def test_30_valid_intraunit_position_change(self):
        self.check(CANDIDATE,intent="position_change",
                   person_changes={"service_status":"active","current_unit_id":UNIT["unit_id"],
                                   "current_billet_id":"slot-old","current_department_id":"science"})

    def test_31_cross_unit_position_change_invalid(self):
        self.check(BLOCKED,"DIFFERENT_UNIT_USE_TRANSFER",intent="position_change",
                   person_changes={"service_status":"active","current_unit_id":"ship-other",
                                   "current_billet_id":"slot-old","current_department_id":"science"})

    def test_32_transfer_without_active_personnel_denied(self):
        self.check(BLOCKED,"NOT_ACTIVE_WITH_CURRENT_ASSIGNMENT",intent="transfer")

    def test_33_cannot_change_into_another_specialty_without_authorization(self):
        self.check(BLOCKED,"CROSS_SPECIALTY_NEEDS_AUTHORIZATION",intent="position_change",
                   person_changes={"service_status":"active","current_unit_id":UNIT["unit_id"],
                                   "current_billet_id":"slot-old","current_department_id":"engineering"})

    def test_34_cross_specialty_with_training_and_authorization_candidate(self):
        self.check(CANDIDATE,intent="position_change",
                   person_changes={"service_status":"active","current_unit_id":UNIT["unit_id"],
                                   "current_billet_id":"slot-old","current_department_id":"engineering",
                                   "cross_specialty_authorized":True})

    def test_35_cannot_take_current_billet_as_new_position(self):
        self.check(BLOCKED,"ALREADY_OCCUPIES_TARGET_BILLET",intent="position_change",
                   person_changes={"service_status":"active","current_unit_id":UNIT["unit_id"],
                                   "current_billet_id":BILLET["billet_id"],"current_department_id":"science"})

    def test_36_unqualified_commander_cannot_be_xo(self):
        self.check(BLOCKED,"MISSING_PROFESSIONAL_QUALIFICATION",
                   person_changes={"rank":"commander","service_status":"active","current_unit_id":"old",
                                   "current_billet_id":"slot-old","qualifications":[]},
                   billet_changes={"profile_id":"first_officer"},intent="transfer")

    def test_37_commander_qualified_for_xo_is_candidate_if_vacant(self):
        self.check(CANDIDATE,intent="transfer",
                   person_changes={"rank":"commander","service_status":"active",
                                   "current_unit_id":"old","current_billet_id":"slot-old",
                                   "current_department_id":"command",
                                   "qualifications":["command_qualified"]},
                   billet_changes={"profile_id":"first_officer"})

    def test_38_xo_currently_occupied_must_wait_even_if_player_qualified(self):
        self.check(WAITING,intent="transfer",
                   person_changes={"rank":"commander","service_status":"active",
                                   "current_unit_id":"old","current_billet_id":"slot-old",
                                   "current_department_id":"command",
                                   "qualifications":["command_qualified"]},
                   billet_changes={"profile_id":"first_officer","vacancy_state":"occupied",
                                   "occupant_id":"existing-xo"})

    def test_39_first_assignment_owns_no_ranks_or_position(self):
        output=self.check(CANDIDATE)
        self.assertNotIn("new_rank",output)
        self.assertNotIn("occupant_id",output)

    def test_40_offer_draft_screened_reference_only(self):
        self.offer("draft","screened",REVIEW,"SCREENING_SUCCESS_REFERENCE")

    def test_41_offer_authorized_issuance_reference_only(self):
        self.offer("screened","offered",REVIEW,"OFFER_REQUIRES_AUTHORIZED_ISSUANCE")

    def test_42_unverified_issuer_cannot_offer(self):
        self.offer("screened","offered",BLOCKED,"PERSONNEL_AUTHORITY_REQUIRED",
                   changes={"personnel_authority_verified":False})

    def test_43_accepting_offer_does_not_occupy_slot(self):
        self.offer("offered","accepted",REVIEW,"ACCEPTANCE_DOES_NOT_OCCUPY_BILLET")

    def test_44_offer_expired_before_accept(self):
        self.offer("offered","accepted",BLOCKED,"OFFER_EXPIRED",
                   unit_changes={"time_tick":150})

    def test_45_cannot_expire_before_deadline(self):
        self.offer("offered","expired",BLOCKED,"OFFER_NOT_YET_EXPIRED")

    def test_46_expiration_can_be_recorded_after_deadline(self):
        self.offer("offered","expired",REVIEW,"TERMINAL_EVENT_REQUIRES_CORE_RECORD",
                   unit_changes={"time_tick":151})

    def test_47_unauthorized_selection_cannot_issue_orders(self):
        self.offer("accepted","orders_issued",BLOCKED,"AUTHORIZED_SELECTION_AND_ORDERS_REQUIRED",
                   changes={"selection_authorized":False})

    def test_48_verified_selection_and_order_is_only_reviewable(self):
        self.offer("accepted","orders_issued",REVIEW,"ORDERS_NEED_CORE_COMMIT")

    def test_49_effective_requires_authoritative_transaction(self):
        self.offer("orders_issued","effective",BLOCKED,"CORE_ATOMIC_APPOINTMENT_NOT_READY",
                   changes={"atomic_core_transaction_authorized":False})

    def test_50_effective_before_order_time_denied(self):
        self.offer("orders_issued","effective",BLOCKED,"CORE_ATOMIC_APPOINTMENT_NOT_READY",
                   changes={"order_effective_at_tick":101})

    def test_51_effective_ready_never_mutates(self):
        self.offer("orders_issued","effective",REVIEW,"READY_FOR_CORE_ATOMIC_TRANSACTION_NOT_EXECUTED")

    def test_52_stale_revision_prevents_double_claim(self):
        self.offer("orders_issued","effective",BLOCKED,"OFFER_STALE_OR_INVALID_TIME",
                   unit_changes={"world_revision":13})

    def test_53_offer_issued_for_other_candidate_denied(self):
        self.offer("offered","accepted",BLOCKED,"OFFER_IDENTITY_MISMATCH",
                   changes={"candidate_id":"other-person"})

    def test_54_offer_for_other_billet_denied(self):
        self.offer("offered","accepted",BLOCKED,"OFFER_IDENTITY_MISMATCH",
                   changes={"billet_id":"different-billet"})

    def test_55_invalid_state_jump_to_effective(self):
        self.offer("offered","effective",BLOCKED,"INVALID_OFFER_TRANSITION")

    def test_56_billet_occupied_before_accepted_denied(self):
        self.offer("offered","accepted",BLOCKED,"CANDIDATE_OR_VACANCY_NO_LONGER_VALID",
                   billet_changes={"vacancy_state":"occupied","occupant_id":"npc-first"})

    def test_57_ordered_appointment_cannot_displace_occupied_npc(self):
        self.offer("orders_issued","effective",BLOCKED,"CANDIDATE_OR_VACANCY_NO_LONGER_VALID",
                   billet_changes={"vacancy_state":"occupied","occupant_id":"npc-old"})

    def test_58_transfers_need_actual_position_source(self):
        self.check(BLOCKED,"NOT_ACTIVE_WITH_CURRENT_ASSIGNMENT",intent="transfer",
                   person_changes={"service_status":"active","current_unit_id":"another-unit",
                                   "current_billet_id":None})

    def test_59_empty_catalog_cannot_pass_matching(self):
        catalog,_=load_references()
        catalog["profiles"]=[]
        self.assertFalse(validate_catalog(catalog))

    def test_60_rename_existing_position_not_allowed(self):
        catalog,_=load_references()
        catalog["profiles"][0]["formal_position_id"]="invented-command-post"
        self.assertFalse(validate_catalog(catalog))


if __name__ == "__main__":
    unittest.main()
