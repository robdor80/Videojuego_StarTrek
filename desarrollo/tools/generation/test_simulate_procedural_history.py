#!/usr/bin/env python3
"""Reference-only P2-B05 tests: causality, campaign isolation and replay."""
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("history_ref", HERE / "simulate_procedural_history.py")
h = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = h
spec.loader.exec_module(h)
FIXTURE = ROOT / "desarrollo/validation/fixtures/procedural_history/procedural_history_reconstruction_v0.1.json"


def case():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def state():
    return case()["initial_state"]


def event():
    return case()["events"][0]


class ProceduralHistoryReferenceTests(unittest.TestCase):
    def assert_rejected_clean(self, s, e, reason):
        before = copy.deepcopy(s)
        with self.assertRaisesRegex(ValueError, reason):
            h.apply_event(s, e)
        self.assertEqual(s, before)

    def test_01_happy_path_and_correction_append_only(self):
        f = case()
        r = h.replay(f["initial_state"], f["events"])
        self.assertEqual(2, len(r["history"]))
        self.assertEqual(105, r["last_tick"])
        self.assertEqual("hist:recovery_001", r["history"][1]["corrects_ref"])
        self.assertEqual("hist:recovery_001", r["history"][0]["event_id"])

    def test_02_deterministic_replay(self):
        f = case()
        self.assertEqual(h.digest(h.replay(f["initial_state"], f["events"])),
                         h.digest(h.replay(copy.deepcopy(f["initial_state"]), copy.deepcopy(f["events"]))))

    def test_03_no_input_mutation(self):
        s, e = state(), event()
        before = copy.deepcopy((s, e))
        h.apply_event(s, e)
        self.assertEqual((s, e), before)

    def test_04_replay_idempotent(self):
        s = h.apply_event(state(), event())
        self.assertEqual(s, h.apply_event(s, event()))

    def test_05_reused_id_conflicting_payload(self):
        s = h.apply_event(state(), event())
        e = event()
        e["major"] = False
        self.assert_rejected_clean(s, e, "different payload")

    def test_06_cannot_backdate_sealed_prefix(self):
        e = event()
        e["tick"] = 99
        self.assert_rejected_clean(state(), e, "sealed historical prefix")

    def test_07_nonmonotonic_time(self):
        e = event()
        e["tick"] = 102
        self.assert_rejected_clean(state(), e, "non-monotonic")

    def test_08_unknown_cause(self):
        e = event()
        e["source_refs"] = ["missing"]
        self.assert_rejected_clean(state(), e, "unknown source")

    def test_09_future_cause(self):
        e = event()
        e["source_refs"] = ["fact_debrief_correction"]
        self.assert_rejected_clean(state(), e, "future source")

    def test_10_kind_specific_evidence(self):
        e = event()
        e["source_refs"] = ["fact_political_vote"]
        self.assert_rejected_clean(state(), e, "kind-specific")

    def test_11_unknown_impacted_entity(self):
        e = event()
        e["impact_refs"] = ["missing"]
        self.assert_rejected_clean(state(), e, "unknown impacted")

    def test_12_impact_not_yet_existing(self):
        s = state()
        s["entities"]["station_antares"]["exists_tick"] = 110
        self.assert_rejected_clean(s, event(), "does not exist")

    def test_13_major_scale_needs_accepted_evidence(self):
        s = state()
        s["facts"]["fact_factory_restored"]["major_evidence"] = False
        self.assert_rejected_clean(s, event(), "major event requires")

    def test_14_major_scale_needs_multi_entity(self):
        e = event()
        e["impact_refs"] = ["colony_naral"]
        self.assert_rejected_clean(state(), e, "major event requires")

    def test_15_false_authority(self):
        e = event()
        e["actor_ref"] = "military_archive"
        self.assert_rejected_clean(state(), e, "authority")

    def test_16_future_television_is_not_a_trigger(self):
        e = event()
        e["provenance"] = "tv_future"
        self.assert_rejected_clean(state(), e, "television future")

    def test_17_canonical_reservation(self):
        e = event()
        e["event_id"] = "canon:romulus_2387"
        self.assert_rejected_clean(state(), e, "reservation")

    def test_18_player_arrival_is_not_causation(self):
        e = event()
        e["trigger"] = "player_presence"
        self.assert_rejected_clean(state(), e, "player presence")

    def test_19_unauthorized_discovery_and_war(self):
        for kind in ("scientific_breakthrough", "declare_war", "systemic_crisis", "emergent_mission"):
            e = event()
            e["kind"] = kind
            self.assert_rejected_clean(state(), e, "other block")

    def test_20_cross_campaign_fact_rejected(self):
        s = state()
        s["facts"]["fact_factory_restored"]["campaign_id"] = "other_campaign"
        self.assert_rejected_clean(s, event(), "foreign campaign")

    def test_21_cross_campaign_entity_rejected(self):
        s = state()
        s["entities"]["colony_naral"]["campaign_id"] = "other_campaign"
        self.assert_rejected_clean(s, event(), "foreign campaign")

    def test_22_rumor_rejected_as_source(self):
        s = state()
        s["facts"]["fact_factory_restored"]["status"] = "rumor"
        self.assert_rejected_clean(s, event(), "rumor or forecast")

    def test_23_knowledge_requires_observed_id(self):
        s = h.replay(state(), case()["events"])
        self.assertEqual([], h.visible_history(s, [], 110, "classified"))
        self.assertEqual(1, len(h.visible_history(s, ["hist:recovery_001"], 110, "public")))
        self.assertEqual([], h.visible_history(s, ["hist:record_update_002"], 110, "public"))
        self.assertEqual([], h.visible_history(s, ["hist:record_update_002"], 104, "classified"))
        self.assertEqual(1, len(h.visible_history(s, ["hist:record_update_002"], 105, "restricted")))

    def test_24_corrective_record_does_not_rewrite_past(self):
        s = h.replay(state(), case()["events"])
        first = s["history"][0]
        self.assertEqual("economic_milestone", first["kind"])
        self.assertEqual("historical_record_update", s["history"][1]["kind"])

    def test_25_correction_must_reference_real_history(self):
        e = case()["events"][1]
        self.assert_rejected_clean(state(), e, "unknown source")
        e["source_refs"] = ["fact_debrief_correction"]
        self.assert_rejected_clean(state(), e, "correction must reference")

    def test_26_no_other_kind_uses_correction_pointer(self):
        e = event()
        e["corrects_ref"] = "hist:recovery_001"
        self.assert_rejected_clean(state(), e, "correction only")

    def test_27_deterministic_proposal_independent_of_lod(self):
        s = state()
        kw = dict(kind="economic_milestone", source_refs=["fact_factory_restored"],
                  impact_refs=["colony_naral"], actor_ref="regional_archive", tick_value=104)
        a = h.proposal(s, **kw)
        self.assertEqual(a, h.proposal(copy.deepcopy(s), **kw))
        self.assertTrue(a["event_id"].startswith("hist:"))
        self.assertNotIn("player", a)

    def test_28_ordinal_changes_only_proposal_identity(self):
        s = state()
        kw = dict(kind="economic_milestone", source_refs=["fact_factory_restored"],
                  impact_refs=["colony_naral"], actor_ref="regional_archive", tick_value=104)
        self.assertNotEqual(h.proposal(s, **kw)["event_id"], h.proposal(s, **kw, ordinal="1")["event_id"])

    def test_29_event_tamper_detection(self):
        s = h.apply_event(state(), event())
        s["history"][0]["major"] = False
        with self.assertRaisesRegex(ValueError, "corrupt historical record"):
            h.validate_state(s)

    def test_30_duplicate_source_and_impact_rejected(self):
        e = event()
        e["source_refs"] = ["fact_factory_restored"] * 2
        self.assert_rejected_clean(state(), e, "duplicate source")
        e = event()
        e["impact_refs"] = ["colony_naral"] * 2
        self.assert_rejected_clean(state(), e, "duplicate impact")

    def test_31_no_past_to_future_leakage(self):
        s = state()
        s["facts"]["future_faction_state"] = dict(tick=200, status="accepted", domain="civilization",
                                                   campaign_id="campaign_alpha")
        e = event()
        e["kind"] = "civilizational_transition"
        e["actor_ref"] = "civilian_chancellery"
        e["source_refs"] = ["future_faction_state"]
        self.assert_rejected_clean(s, e, "future source")

    def test_32_wrong_clock_types(self):
        e = event()
        e["tick"] = 104.5
        self.assert_rejected_clean(state(), e, "event tick invalid")

    def test_33_missing_impact_fails_closed(self):
        e = event()
        e["impact_refs"] = []
        self.assert_rejected_clean(state(), e, "impacted entities required")


    def test_34_accepted_canonical_prefix_preserved(self):
        s = state()
        prefix = dict(event_id="canon:historical_anchor", tick=50, kind="canonical_anchor",
                      source_digest="canonical_source", visibility="public", provenance="canon")
        prefix["digest"] = h.record_digest(prefix)
        s["history"].append(prefix)
        result = h.apply_event(s, event())
        self.assertEqual(prefix, result["history"][0])
        self.assertEqual(prefix, s["history"][0])

    def test_35_distinct_campaigns_derive_distinct_history_ids(self):
        s1, s2 = state(), state()
        s2["campaign_id"] = "campaign_beta"
        kwargs = dict(kind="economic_milestone", source_refs=["fact_factory_restored"],
                      impact_refs=["colony_naral"], actor_ref="regional_archive", tick_value=104)
        self.assertNotEqual(h.proposal(s1, **kwargs)["event_id"],
                            h.proposal(s2, **kwargs)["event_id"])

    def test_36_lod_cannot_change_accepted_history(self):
        s1, s2 = state(), state()
        s1["lod"] = "near"
        s2["lod"] = "dormant"
        self.assertEqual(h.apply_event(s1, event())["history"],
                         h.apply_event(s2, event())["history"])



if __name__ == "__main__":
    unittest.main()
