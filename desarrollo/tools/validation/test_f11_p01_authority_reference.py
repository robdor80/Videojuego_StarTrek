#!/usr/bin/env python3
"""Regresiones F11-P01. Solo mock offline; NO verifica permisos efectivos CoreRPG."""
import copy
import unittest

try:
    from desarrollo.tools.validation.f11_p01_authority_reference import evaluate, ALLOW, DENY, TAG, load_contract
except ModuleNotFoundError:
    from f11_p01_authority_reference import evaluate, ALLOW, DENY, TAG, load_contract


BASE = {
    "actor_id": "officer-01",
    "unit_id": "enterprise-d",
    "assignment_id": "enterprise-d",
    "rank": "lieutenant",
    "position_ids": [],
    "duty_role_ids": ["sensor_operator"],
    "qualifications": ["sensors_qualified"],
    "medical_status": "fit",
    "department_id": "science",
    "time_tick": 100,
    "world_revision": 7,
    "reference_snapshot_complete": True,
    "orders_within_scope": True,
    "resources_exist": True,
    "safety_limits_respected": True,
    "on_duty": True,
    "active_delegations": [],
    "known_information_ids": [],
    "permitted_information_ids": [],
}


class AuthorityReferenceTests(unittest.TestCase):
    def check(self, action, expected, reason=None, changes=None, request=None):
        ctx = copy.deepcopy(BASE)
        if changes:
            ctx.update(copy.deepcopy(changes))
        payload = {"observed_revision": ctx["world_revision"]}
        if request:
            payload.update(request)
        original = copy.deepcopy(ctx)
        output = evaluate(action, ctx, payload)
        self.assertEqual(output["status"], expected)
        if reason:
            self.assertEqual(output["reason"], reason)
        self.assertEqual(output["authority"], TAG)
        self.assertEqual(output["effects_applied"], 0)
        self.assertEqual(original, ctx, "Una evaluación de referencia jamás debe mutar el contexto.")

    def test_01_sensor_qualified_on_watch(self):
        self.check("sensor_read", ALLOW)

    def test_02_sensor_off_duty_blocked(self):
        self.check("sensor_read", DENY, "NOT_ON_DUTY", {"on_duty": False})

    def test_03_rank_alone_cannot_command(self):
        self.check("assume_ship_command", DENY, "MISSING_QUALIFICATION", {"rank": "commander"})

    def test_04_rank_plus_qualification_cannot_command_without_position(self):
        self.check("assume_ship_command", DENY, "POSITION_OR_VALID_DELEGATION_REQUIRED",
                   {"rank": "captain", "qualifications": ["command_qualified"]})

    def test_05_department_head_organizes_own_department(self):
        self.check("department_roster", ALLOW,
                   changes={"rank": "lieutenant_commander", "position_ids": ["chief_engineering_officer"],
                            "department_id": "engineering"}, request={"department_id": "engineering"})

    def test_06_department_head_cannot_command_other_department(self):
        self.check("department_roster", DENY, "DEPARTMENT_SCOPE_MISMATCH",
                   {"position_ids": ["chief_engineering_officer"], "department_id": "engineering"},
                   {"department_id": "science"})

    def test_07_department_head_cannot_change_mission(self):
        self.check("mission_directive_change", DENY, "POSITION_OR_VALID_DELEGATION_REQUIRED",
                   {"rank": "commander", "position_ids": ["chief_engineering_officer"]})

    def test_08_xo_must_have_valid_succession(self):
        self.check("assume_ship_command", DENY, "POSITION_OR_VALID_DELEGATION_REQUIRED",
                   {"rank": "commander", "position_ids": ["first_officer"],
                    "qualifications": ["command_qualified"]})

    def test_09_xo_can_act_during_verified_succession(self):
        self.check("assume_ship_command", ALLOW,
                   changes={"rank": "commander", "position_ids": ["first_officer"],
                            "qualifications": ["command_qualified"],
                            "succession": {"actor_id": "officer-01", "origin_position": "first_officer",
                                           "active": True, "order_verified": True,
                                           "starts_at": 90, "ends_at": 110}})

    def test_10_expired_succession_does_not_command(self):
        self.check("assume_ship_command", DENY, "POSITION_OR_VALID_DELEGATION_REQUIRED",
                   {"rank": "commander", "position_ids": ["first_officer"],
                    "qualifications": ["command_qualified"],
                    "succession": {"actor_id": "officer-01", "origin_position": "first_officer",
                                   "active": True, "order_verified": True,
                                   "starts_at": 50, "ends_at": 100}})

    def test_11_delegated_navigation_within_window(self):
        self.check("ship_course_change", ALLOW,
                   changes={"active_delegations": [{"domain": "ship_navigation",
                    "delegate_actor_id": "officer-01", "issuer_authorized": True,
                    "active": True, "revoked": False, "starts_at": 90, "ends_at": 110}]})

    def test_12_revoked_delegation_does_not_command(self):
        self.check("ship_course_change", DENY, "POSITION_OR_VALID_DELEGATION_REQUIRED",
                   {"active_delegations": [{"domain": "ship_navigation",
                    "delegate_actor_id": "officer-01", "issuer_authorized": True,
                    "active": True, "revoked": True, "starts_at": 90, "ends_at": 110}]})

    def test_13_delegation_in_other_domain_is_insufficient(self):
        self.check("mission_directive_change", DENY, "POSITION_OR_VALID_DELEGATION_REQUIRED",
                   {"active_delegations": [{"domain": "ship_navigation",
                    "delegate_actor_id": "officer-01", "issuer_authorized": True,
                    "active": True, "revoked": False, "starts_at": 90, "ends_at": 110}]})

    def test_14_cmo_medical_scope(self):
        self.check("declare_unfit_for_duty", ALLOW,
                   changes={"position_ids": ["chief_medical_officer"],
                            "qualifications": ["medical_fitness_authority"]})

    def test_15_cmo_not_mission_commander(self):
        self.check("mission_directive_change", DENY, "POSITION_OR_VALID_DELEGATION_REQUIRED",
                   {"position_ids": ["chief_medical_officer"],
                    "qualifications": ["medical_fitness_authority"]})

    def test_16_captain_recommendation_not_appointment(self):
        self.check("recommend_first_officer", ALLOW, "RECOMMENDATION_ONLY_NO_APPOINTMENT",
                   {"rank": "captain", "position_ids": ["commanding_officer"]})

    def test_17_captain_cannot_self_appoint_fleet_position(self):
        self.check("appoint_first_officer", DENY, "FLEET_APPOINTMENT_AUTHORITY_OR_VACANCY_MISSING",
                   {"rank": "captain", "position_ids": ["commanding_officer"]})

    def test_18_formal_appointment_requires_all_checks(self):
        self.check("appoint_first_officer", ALLOW, "FLEET_APPOINTMENT_REVIEWABLE_REFERENCE",
                   {"external_personnel_authority_verified": True,
                    "vacancy_verified": True, "formal_appointment_order_verified": True})

    def test_19_vacancy_alone_does_not_appoint(self):
        self.check("appoint_first_officer", DENY, "FLEET_APPOINTMENT_AUTHORITY_OR_VACANCY_MISSING",
                   {"vacancy_verified": True})

    def test_20_padd_knowledge_without_clearance_denied(self):
        self.check("view_restricted_padd", DENY, "KNOWLEDGE_OR_CLEARANCE_DENIED",
                   {"rank": "captain", "known_information_ids": ["secret-7"]},
                   {"information_id": "secret-7"})

    def test_21_padd_both_requirements_reference(self):
        self.check("view_restricted_padd", ALLOW, "KNOWLEDGE_AND_PERMISSION_VERIFIED_REFERENCE",
                   {"known_information_ids": ["secret-7"],
                    "permitted_information_ids": ["secret-7"]},
                   {"information_id": "secret-7"})

    def test_22_unfit_captain_blocked(self):
        self.check("mission_directive_change", DENY, "NOT_FIT_FOR_DUTY",
                   {"rank": "captain", "position_ids": ["commanding_officer"],
                    "medical_status": "unfit"})

    def test_23_missing_resource_blocked(self):
        self.check("mission_directive_change", DENY, "HARD_OPERATIONAL_LIMIT",
                   {"rank": "captain", "position_ids": ["commanding_officer"],
                    "resources_exist": False})

    def test_24_untrusted_reference_snapshot_blocked(self):
        self.check("sensor_read", DENY, "UNVERIFIED_REFERENCE_SNAPSHOT",
                   {"reference_snapshot_complete": False})

    def test_25_mismatched_assignment_blocked(self):
        self.check("sensor_read", DENY, "WRONG_ASSIGNMENT",
                   {"assignment_id": "station-42"})

    def test_26_missing_role_data_blocked(self):
        self.check("sensor_read", DENY, "MISSING_ROLE_OR_QUALIFICATION_DATA",
                   {"duty_role_ids": None})

    def test_27_stale_revision_blocked(self):
        self.check("sensor_read", DENY, "STALE_WORLD_REVISION",
                   request={"observed_revision": 6})

    def test_28_unknown_action_blocked(self):
        self.check("create_rank_out_of_thin_air", DENY, "UNKNOWN_ACTION")

    def test_29_contract_has_six_commissioned_ranks(self):
        self.assertEqual(load_contract()["rank_progression"],
                         ["ensign", "lieutenant_junior_grade", "lieutenant",
                          "lieutenant_commander", "commander", "captain"])

    def test_30_mutual_separation_of_rank_and_effective_command(self):
        c = load_contract()
        self.assertTrue(c["rank_policy"]["rank_never_implies_ship_command"])
        self.assertTrue(c["rank_policy"]["rank_never_auto_grants_position"])
        self.assertFalse(c["succession"]["changes_rank"])


if __name__ == "__main__":
    unittest.main()
