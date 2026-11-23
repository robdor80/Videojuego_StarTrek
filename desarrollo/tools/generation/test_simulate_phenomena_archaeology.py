#!/usr/bin/env python3
"""P2-B07: pruebas adversariales del adaptador offline de fenómenos/arqueología."""
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("b07_reference", HERE / "simulate_phenomena_archaeology.py")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
FIXTURE = ROOT / "desarrollo/validation/fixtures/phenomena_archaeology/phenomena_archaeology_exploration_v0.1.json"


def fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def state():
    return fixture()["initial_state"]


def events():
    return fixture()["events"]


def at(count):
    f = fixture()
    return mod.replay(f["initial_state"], f["events"][:count])


class PhenomenaArchaeologyReferenceTests(unittest.TestCase):
    def reject(self, s, e, reason):
        initial = copy.deepcopy((s, e))
        with self.assertRaisesRegex(ValueError, reason):
            mod.apply_event(s, e)
        self.assertEqual(initial, (s, e), "a rejected proposal mutated its inputs")

    def test_01_full_pipeline_two_persistent_entities(self):
        final = at(12)
        self.assertEqual(len(final["events"]), 12)
        self.assertEqual(len(final["phenomena"]), 2)
        self.assertEqual(final["phenomena"]["p2b07:camp_fixture:rift_lira"]["phase"], "active")
        ruin = final["phenomena"]["p2b07:camp_fixture:ruin_lyra"]
        self.assertEqual(ruin["phase"], "stable_ruin")
        self.assertEqual(len(ruin["recoveries"]), 1)
        self.assertEqual(ruin["interpretations"][0]["status"], "supported_not_certain")

    def test_02_replay_is_deterministic(self):
        self.assertEqual(mod.digest(at(12)), mod.digest(at(12)))

    def test_03_state_and_event_are_never_mutated(self):
        s, e = state(), events()[0]
        original = copy.deepcopy((s, e))
        mod.apply_event(s, e)
        self.assertEqual((s, e), original)

    def test_04_exact_duplicate_idempotent(self):
        self.assertEqual(at(1), mod.apply_event(at(1), events()[0]))

    def test_05_conflicting_duplicate_rejected(self):
        e = events()[0]
        e["slot_ref"] = "ruin_lyra"
        self.reject(at(1), e, "payload conflict")

    def test_06_identity_is_campaign_scoped(self):
        s = state()
        old = mod.stable_entity_id(s, "rift_lira")
        s["campaign_id"] = "parallel"
        self.assertNotEqual(old, mod.stable_entity_id(s, "rift_lira"))

    def test_07_slot_seed_not_affected_by_other_slot(self):
        s = state()
        v = mod.roll_bps(s, "rift_lira")
        s["slots"]["new_slot"] = copy.deepcopy(s["slots"]["rift_lira"])
        self.assertEqual(v, mod.roll_bps(s, "rift_lira"))

    def test_08_lod_independent_identity(self):
        s = state()
        self.assertEqual(mod.stable_entity_id(s, "rift_lira"),
                         mod.stable_entity_id(dict(s, lod="unloaded"), "rift_lira"))

    def test_09_zero_rarity_does_not_materialize(self):
        s = state()
        s["slots"]["rift_lira"]["rarity_bps"] = 0
        out = mod.apply_event(s, events()[0])
        self.assertEqual(out["phenomena"], {})
        self.assertEqual(out["events"][0]["outcome"], "empty_slot")

    def test_10_player_proximity_cannot_trigger_generation(self):
        e = events()[0]
        e["trigger"] = "player_presence"
        self.reject(state(), e, "player-triggered")

    def test_11_cross_block_mutations_forbidden(self):
        for name in sorted(mod.FORBIDDEN):
            e = events()[0]
            e[name] = True
            self.reject(state(), e, "cross-block")

    def test_12_other_blocks_cannot_be_invoked(self):
        for kind in ("declare_crisis", "generate_mission", "unlock_tech", "simulate_galaxy"):
            e = events()[0]
            e["kind"] = kind
            self.reject(state(), e, "other-block")

    def test_13_scope_required(self):
        e = events()[0]
        e["actor_ref"] = "recipient"
        self.reject(state(), e, "lacks authority")

    def test_14_canon_prefix_sealed(self):
        e = events()[0]
        e["tick"] = 99
        self.reject(state(), e, "sealed historical")

    def test_15_clock_monotonic(self):
        e = events()[2]
        e["tick"] = 99
        self.reject(at(2), e, "sealed historical|non-monotonic")

    def test_16_foreign_campaign_provenance_rejected(self):
        s = state()
        s["facts"]["rift_formed"]["campaign_id"] = "foreign"
        self.reject(s, events()[0], "foreign-campaign")

    def test_17_missing_formation_source_rejected(self):
        s = state()
        del s["facts"]["rift_formed"]
        self.reject(s, events()[0], "formation fact")

    def test_18_formative_event_must_be_preexisting(self):
        s = state()
        s["facts"]["rift_formed"]["tick"] = 100
        self.reject(s, events()[0], "not pre-existing")

    def test_19_reserved_canonical_id_rejected(self):
        s = state()
        s["reserved_ids"].append("p2b07:camp_fixture:rift_lira")
        self.reject(s, events()[0], "reserved entity id")

    def test_20_reserved_canonical_location_rejected(self):
        s = state()
        s["locations"]["sector_lira"]["reserved"] = True
        self.reject(s, events()[0], "canonical protected")

    def test_21_extraordinary_temporal_not_generated(self):
        s = state()
        s["slots"]["rift_lira"]["family"] = "temporal"
        self.reject(s, events()[0], "exceptional phenomenon")

    def test_22_traversable_wormhole_not_created(self):
        s = state()
        s["slots"]["rift_lira"]["family"] = "wormhole"
        self.reject(s, events()[0], "exceptional phenomenon")

    def test_23_broken_sensor_cannot_supply_evidence(self):
        s = at(2)
        s["instruments"]["scanner_alpha"]["operational"] = False
        self.reject(s, events()[2], "sensor not operational")

    def test_24_uncalibrated_sensor_cannot_supply_evidence(self):
        s = at(2)
        s["instruments"]["scanner_alpha"]["calibrated"] = False
        self.reject(s, events()[2], "sensor not operational")

    def test_25_unattested_sensor_fact_rejected(self):
        e = events()[2]
        e["fact_ref"] = "invented"
        self.reject(at(2), e, "sensor_observation fact")

    def test_26_sensor_author_must_match_provenance(self):
        e = events()[2]
        e["actor_ref"] = "officer_b"
        self.reject(at(2), e, "sensor provenance mismatch")

    def test_27_future_evidence_unusable(self):
        s = at(2)
        s["facts"]["a_obs_1"]["tick"] = 102
        self.reject(s, events()[2], "future source fact")

    def test_28_same_observation_cannot_be_reused(self):
        s = at(3)
        e = events()[2]
        e["event_id"] = "b07:repeat_reading"
        e["tick"] = 103
        self.reject(s, e, "observation fact reused")

    def test_29_no_observation_of_not_yet_materialized_entity(self):
        s = state()
        self.reject(s, events()[2], "phenomenon must pre-exist")

    def test_30_interpretation_needs_two_independent_sources(self):
        e = events()[4]
        self.reject(at(3), e, "independent evidence")

    def test_31_contradiction_blocks_interpretation(self):
        s = at(4)
        s["phenomena"]["p2b07:camp_fixture:rift_lira"]["observations"].append({
            "fact_ref": "contradiction", "actor_ref": "officer_a", "instrument_ref": "scanner_alpha",
            "result": "contradicts", "tick": 102
        })
        self.reject(s, events()[4], "unresolved contradiction")

    def test_32_no_excavation_of_natural_phenomenon(self):
        e = events()[8]
        e["entity_ref"] = "p2b07:camp_fixture:rift_lira"
        self.reject(at(8), e, "cannot excavate")

    def test_33_excavation_requires_valid_permit(self):
        e = events()[8]
        e["permit"] = False
        self.reject(at(8), e, "permit and preservation")

    def test_34_excavation_requires_right_custodian(self):
        e = events()[8]
        e["custodian_ref"] = "recipient"
        self.reject(at(8), e, "custodian mismatch")

    def test_35_excavation_requires_real_artifact_fact(self):
        e = events()[8]
        e["fact_ref"] = "missing_artifact"
        self.reject(at(8), e, "excavation fact")

    def test_36_excavation_cannot_seize_artifact(self):
        e = events()[8]
        e["trade_delta"] = {"artifact_lyra_001": 1}
        self.reject(at(8), e, "cross-block")

    def test_37_archaeological_culture_required(self):
        s = state()
        del s["facts"]["settlement_vacated"]["culture_ref"]
        self.reject(s, events()[1], "archaeological culture")

    def test_38_archaeological_custodian_required(self):
        s = state()
        s["slots"]["ruin_lyra"]["custodian_ref"] = "unknown"
        self.reject(s, events()[1], "unknown custodian")

    def test_39_invalid_physical_transition(self):
        e = events()[5]
        e["target_phase"] = "lost_ruin"
        self.reject(at(5), e, "illegal physical transition")

    def test_40_physical_transition_needs_matching_cause(self):
        e = events()[5]
        e["target_phase"] = "spent"
        self.reject(at(5), e, "physical cause mismatch")

    def test_41_knowledge_delivered_not_instantly(self):
        s = at(11)
        self.assertEqual(mod.observed(s, "recipient", 110, "restricted"), [])
        rows = mod.observed(s, "recipient", 111, "restricted")
        self.assertEqual([x["entity_ref"] for x in rows],
                         ["p2b07:camp_fixture:ruin_lyra"])

    def test_42_knowledge_respects_clearance(self):
        self.assertEqual(mod.observed(at(12), "recipient", 111, "public")[0]["entity_ref"],
                         "p2b07:camp_fixture:rift_lira")
        self.assertEqual(len(mod.observed(at(12), "recipient", 111, "public")), 1)

    def test_43_presentation_does_not_leak_truth(self):
        rows = mod.observed(at(12), "recipient", 120, "restricted")
        self.assertTrue(rows)
        self.assertNotIn("world_seed", mod.canonical(rows))
        self.assertNotIn("origin_tick", mod.canonical(rows))
        self.assertNotIn("artifact_ref", mod.canonical(rows))

    def test_44_no_classification_downgrade(self):
        e = events()[10]
        e["classification"] = "public"
        self.reject(at(10), e, "downgrade")

    def test_45_uncredentialled_recipient_rejected(self):
        s = at(10)
        s["actors"]["recipient"]["clearance"] = "public"
        self.reject(s, events()[10], "recipient lacks clearance")

    def test_46_communication_must_have_real_fact(self):
        e = events()[10]
        e["fact_ref"] = "invented"
        self.reject(at(10), e, "communication fact")

    def test_47_no_cross_campaign_observation(self):
        s = at(2)
        s["facts"]["a_obs_1"]["campaign_id"] = "other"
        self.reject(s, events()[2], "foreign-campaign")

    def test_48_recoveries_preserve_artifact_identity_and_owner(self):
        s = at(9)
        rec = s["phenomena"]["p2b07:camp_fixture:ruin_lyra"]["recoveries"][0]
        self.assertEqual(rec["artifact_ref"], "artifact_lyra_001")
        self.assertEqual(rec["custodian_ref"], "custodian")
        self.assertNotIn("inventory", s)

    def test_49_fixture_is_synthetic_only(self):
        f = fixture()
        self.assertTrue(f["synthetic_noncanonical"])
        self.assertIn("not attested", f["notice"])

    def test_50_data_version_and_initial_validation(self):
        self.assertEqual(mod.VERSION, "0.1.0")
        self.assertTrue(mod.validate(state()))

    def test_51_source_event_digest_detects_tampering(self):
        s = at(1)
        s["events"][0]["kind"] = "survey"
        self.reject(s, events()[1], "tampered event digest")

    def test_52_stable_final_snapshot_unchanged_by_view(self):
        s = at(12)
        before = mod.digest(s)
        mod.observed(s, "recipient", 200, "restricted")
        self.assertEqual(before, mod.digest(s))

    def test_53_case_cannot_materialize_twice(self):
        e = events()[0]
        e["event_id"] = "b07:second_materialization"
        self.reject(at(1), e, "slot already materialized")

    def test_54_past_cannot_be_rewritten_by_camera_or_ship(self):
        base = state()
        self.assertEqual(mod.roll_bps(base, "ruin_lyra"),
                         mod.roll_bps(dict(base, player_ship="Intrepid", camera_distance=99),
                                      "ruin_lyra"))


    def test_55_empty_slot_materialization_decision_cannot_reroll(self):
        s = state()
        s["slots"]["rift_lira"]["rarity_bps"] = 0
        s = mod.apply_event(s, events()[0])
        e = events()[0]
        e["event_id"] = "b07:retry_empty_slot"
        e["tick"] = 101
        self.reject(s, e, "slot materialization decision already recorded")

    def test_56_new_physical_causes_after_campaign_cutoff_are_eligible(self):
        s = state()
        s["facts"]["rift_formed"]["tick"] = 103
        e = events()[0]
        e["tick"] = 104
        out = mod.apply_event(s, e)
        self.assertIn("p2b07:camp_fixture:rift_lira", out["phenomena"])
        self.assertEqual(out["phenomena"]["p2b07:camp_fixture:rift_lira"]["origin_tick"], 103)


if __name__ == "__main__":
    unittest.main()
