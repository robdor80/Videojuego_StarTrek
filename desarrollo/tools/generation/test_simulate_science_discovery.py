#!/usr/bin/env python3
"""P2-B06 adversarial reference tests. No remote, UE, HOST or CoreRPG needed."""
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("science_ref", HERE / "simulate_science_discovery.py")
sci = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sci
spec.loader.exec_module(sci)
FIXTURE = ROOT / "desarrollo/validation/fixtures/science_discovery/science_discovery_refit_v0.1.json"


def case():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def state():
    return case()["initial_state"]


def events():
    return case()["events"]


def at(n):
    f = case()
    return sci.replay(f["initial_state"], f["events"][:n])


class ScienceReferenceTests(unittest.TestCase):
    def reject(self, snapshot, proposal, pattern):
        before = copy.deepcopy((snapshot, proposal))
        with self.assertRaisesRegex(ValueError, pattern):
            sci.apply_event(snapshot, proposal)
        self.assertEqual(before, (snapshot, proposal))

    def test_01_happy_path_installed_only_on_one_ship(self):
        result = at(11)
        self.assertEqual(len(result["events"]), 11)
        self.assertTrue(result["installations"]["ship_observer:design_filter"]["active"])
        self.assertEqual(len(result["installations"]), 1)
        self.assertEqual(result["projects"]["project_filter"]["spent"], 2)
        self.assertEqual(result["recognitions"]["project_filter"]["contributors"],
                         ["science_lead", "science_peer"])

    def test_02_replay_determinism(self):
        self.assertEqual(sci.digest(at(11)), sci.digest(at(11)))

    def test_03_immutable_original_input(self):
        s, e = state(), events()[0]
        before = copy.deepcopy((s, e))
        sci.apply_event(s, e)
        self.assertEqual((s, e), before)

    def test_04_idempotent_exact_replay_event(self):
        s = at(1)
        self.assertEqual(s, sci.apply_event(s, events()[0]))

    def test_05_reused_id_different_payload(self):
        s = at(1)
        e = events()[0]
        e["hypothesis"] = "other"
        self.reject(s, e, "different payload")

    def test_06_protected_prefix(self):
        e = events()[0]
        e["tick"] = 89
        self.reject(state(), e, "sealed")

    def test_07_monotonic_clock(self):
        e = events()[1]
        e["tick"] = 99
        self.reject(at(1), e, "non-monotonic")

    def test_08_no_player_spawn(self):
        e = events()[0]
        e["trigger"] = "player_presence"
        self.reject(state(), e, "player cannot")

    def test_09_no_cross_block_fields(self):
        for field in ("lod", "spawn", "world_delta", "mission_id", "route_creation",
                      "time_travel", "tech_band_delta"):
            e = events()[0]
            e[field] = 1
            self.reject(state(), e, "forbidden")

    def test_10_no_other_block_operations(self):
        for kind in ("make_anomaly", "declare_war", "issue_mission", "simulate_galaxy"):
            e = events()[0]
            e["kind"] = kind
            self.reject(state(), e, "other-block")

    def test_11_actor_permission_required(self):
        e = events()[0]
        e["actor_ref"] = "yard_master"
        self.reject(state(), e, "not authorized")

    def test_12_canonical_reserved_id(self):
        e = events()[0]
        e["event_id"] = "canon:reserved_technology"
        self.reject(state(), e, "reservation")

    def test_13_cross_campaign_entity(self):
        s = state()
        s["entities"]["subject_signal"]["campaign_id"] = "another"
        self.reject(s, events()[0], "foreign campaign")

    def test_14_future_source_fact(self):
        e = events()[1]
        e["tick"] = 100
        self.reject(at(1), e, "future observation")

    def test_15_observation_source_required(self):
        e = events()[1]
        e["fact_ref"] = "fabricated"
        self.reject(at(1), e, "accepted observation")

    def test_16_provenance_instrument_mismatch(self):
        e = events()[1]
        e["instrument_ref"] = "scanner_beta"
        self.reject(at(1), e, "provenance mismatch")

    def test_17_uncalibrated_instrument(self):
        s = at(1)
        s["entities"]["scanner_alpha"]["calibrated"] = False
        self.reject(s, events()[1], "not available or calibrated")

    def test_18_research_resources_are_finite(self):
        s = at(1)
        s["allocations"]["budget_lab"]["units"] = 0
        self.reject(s, events()[1], "resources exhausted")

    def test_19_two_independent_instruments(self):
        s = at(3)
        s["projects"]["project_filter"]["observations"][1]["instrument_ref"] = "scanner_alpha"
        self.reject(s, events()[3], "independent corroboration")

    def test_20_two_independent_observers(self):
        s = at(3)
        s["projects"]["project_filter"]["observations"][1]["actor_ref"] = "science_lead"
        self.reject(s, events()[3], "independent corroboration")

    def test_21_contradictory_evidence_blocks_validation(self):
        s = at(3)
        s["projects"]["project_filter"]["observations"][1]["result"] = "contradicts"
        self.reject(s, events()[3], "independent corroboration")

    def test_22_review_without_validation_forbidden(self):
        self.reject(at(3), events()[4], "unvalidated")

    def test_23_no_unapproved_era_technology(self):
        e = events()[5]
        e["era_approved"] = False
        self.reject(at(5), e, "era")

    def test_24_no_unsafe_technology(self):
        e = events()[5]
        e["safety_approved"] = False
        self.reject(at(5), e, "safety")

    def test_25_omega_is_not_ordinary_technology(self):
        s = at(5)
        s["projects"]["project_filter"]["category"] = "omega"
        self.reject(s, events()[5], "exceptional")

    def test_26_temporal_phenomenon_cannot_unlock_time_travel(self):
        s = at(5)
        s["projects"]["project_filter"]["category"] = "temporal"
        self.reject(s, events()[5], "exceptional")

    def test_27_wormhole_observation_cannot_create_route(self):
        s = at(5)
        s["projects"]["project_filter"]["category"] = "wormhole"
        self.reject(s, events()[5], "exceptional")

    def test_28_ship_class_compatibility_required(self):
        s = at(6)
        s["entities"]["ship_observer"]["class_ref"] = "Intrepid"
        self.reject(s, events()[6], "incompatible")

    def test_29_cannot_instantly_complete_refit(self):
        e = events()[7]
        e["tick"] = 111
        self.reject(at(7), e, "cannot finish early")

    def test_30_duplicate_refit_rejected(self):
        s = at(7)
        e = events()[6]
        e["event_id"] = "science:another_order"
        e["work_order_id"] = "another_work"
        self.reject(s, e, "already claimed")

    def test_31_failed_trial_does_not_activate(self):
        s = at(8)
        s["facts"]["trial_1"]["result"] = "fail"
        output = sci.apply_event(s, events()[8])
        self.assertFalse(output["installations"]["ship_observer:design_filter"]["active"])

    def test_32_trial_must_have_accepted_evidence(self):
        e = events()[8]
        e["fact_ref"] = "invented_trial"
        self.reject(at(8), e, "trial evidence")

    def test_33_honorary_name_not_automatic(self):
        self.assertEqual(at(9)["recognitions"], {})
        e = events()[9]
        e["institutional_approval"] = False
        self.reject(at(9), e, "formal approval")

    def test_34_no_npc_credit_theft(self):
        e = events()[9]
        e["contributors"] = ["science_lead"]
        self.reject(at(9), e, "full team")

    def test_35_knowledge_grant_requires_communication(self):
        self.assertEqual(sci.visible_knowledge(at(10), "recipient", 150, "classified"), [])
        self.assertEqual(len(sci.visible_knowledge(at(11), "recipient", 122, "restricted")), 1)
        self.assertEqual(sci.visible_knowledge(at(11), "recipient", 121, "classified"), [])
        self.assertEqual(sci.visible_knowledge(at(11), "recipient", 122, "public"), [])

    def test_36_restricted_knowledge_cannot_be_downgraded(self):
        e = events()[10]
        e["classification"] = "public"
        self.reject(at(10), e, "downgrade")

    def test_37_stable_ids_cannot_cross_campaign(self):
        s1, s2 = state(), state()
        s2["campaign_id"] = "another_campaign"
        self.assertNotEqual(sci.stable_event_id(s1, "observe", "project", "source"),
                            sci.stable_event_id(s2, "observe", "project", "source"))

    def test_38_lod_does_not_change_history(self):
        s1, s2 = state(), state()
        s1["lod"] = "near"
        s2["lod"] = "dormant"
        self.assertEqual(sci.replay(s1, events())["events"],
                         sci.replay(s2, events())["events"])

    def test_39_event_digest_tamper_detected(self):
        s = at(1)
        s["events"][0]["actor_ref"] = "fake"
        with self.assertRaisesRegex(ValueError, "tampered"):
            sci.validate_state(s)

    def test_40_installation_is_not_active_before_trials(self):
        s = at(8)
        self.assertFalse(s["installations"]["ship_observer:design_filter"]["active"])

    def test_41_no_universal_fleet_deployment(self):
        s = at(11)
        self.assertNotIn("all_ships", s["installations"])
        self.assertEqual(set(s["installations"]), {"ship_observer:design_filter"})

    def test_42_no_double_pledge_of_budget(self):
        s = at(1)
        e = events()[0]
        e["event_id"] = "science:start_002"
        e["project_id"] = "project_2"
        self.reject(s, e, "already claimed")

    def test_43_minimum_yard_duration(self):
        e = events()[6]
        e["duration"] = 0
        self.reject(at(6), e, "real refit duration")

    def test_44_wrong_trial_at_older_tick(self):
        s = at(8)
        s["facts"]["trial_1"]["tick"] = 115
        e = events()[8]
        e["tick"] = 115
        self.reject(s, e, "instant trials")

    def test_45_future_actor_cannot_act(self):
        s = state()
        s["entities"]["science_lead"]["exists_tick"] = 110
        self.reject(s, events()[0], "actor not yet existing")

    def test_46_no_observation_before_project(self):
        self.reject(state(), events()[1], "project not open")

    def test_47_wrong_facility_allocation(self):
        s = state()
        s["allocations"]["budget_lab"]["facility_ref"] = "shipyard_alpha"
        self.reject(s, events()[0], "facility mismatch")

    def test_48_unapproved_review_never_enables_engineering(self):
        e = events()[4]
        e["decision"] = "reject"
        s = sci.apply_event(at(4), e)
        self.reject(s, events()[5], "review not approved")

    def test_49_prior_science_not_rewritten_on_replay(self):
        s = at(3)
        original = copy.deepcopy(s["events"])
        later = sci.replay(s, events()[3:])
        self.assertEqual(later["events"][:3], original)

    def test_50_no_foreign_allocation(self):
        s = state()
        s["allocations"]["budget_lab"]["campaign_id"] = "foreign"
        self.reject(s, events()[0], "allocation provenance")


    def test_51_trial_requires_authorized_source_author(self):
        s = at(8)
        s["facts"]["trial_1"]["actor_ref"] = "science_peer"
        self.reject(s, events()[8], "trial provenance")

    def test_52_trial_source_must_be_after_installation(self):
        s = at(8)
        s["facts"]["trial_1"]["tick"] = 114
        self.reject(s, events()[8], "trial provenance")

    def test_53_failed_trial_evidence_cannot_be_reused(self):
        s = at(8)
        s["facts"]["trial_1"]["result"] = "fail"
        s = sci.apply_event(s, events()[8])
        e = events()[8]
        e["event_id"] = "science:trial_reused"
        e["tick"] = 121
        self.reject(s, e, "already consumed")

    def test_54_duplicate_official_name_denied(self):
        s = at(9)
        s["recognitions"]["other_project"] = {"official_name": "filtro vesper"}
        self.reject(s, events()[9], "duplicate honorary name")


if __name__ == "__main__":
    unittest.main()
