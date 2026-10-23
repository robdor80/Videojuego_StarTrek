#!/usr/bin/env python3
"""Positive and negative documentary mutation tests for LORE-03 A."""
import copy
import unittest
from validate_lore03_a import validate, validate_index, load

class ChronologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load("lore/historical_events/lore03_a_chronology_index_v0.1.json")
        cls.diplomatic = {e["event_id"] for e in load("lore/diplomacy/historical_events_v0.1.json")["events"]}
        cls.sources = {e["source_id"] for e in load("sources/source_registry/source_registry.json")["sources"]}
        cls.eras = {e: load(f"universe/chronology/era_profiles/{e}/era_profile.json")["playable"]
                    for e in ("pike", "kirk", "tng_ds9_voyager")}
    def check_bad(self, alter):
        d = copy.deepcopy(self.data)
        alter(d)
        with self.assertRaises(AssertionError):
            validate_index(d, self.diplomatic, self.sources, self.eras)

    def test_positive_full_validation(self): self.assertGreaterEqual(validate()["reused_historical_refs"], 40)
    def test_positive_epoch(self): self.assertEqual(self.eras, {"pike":False,"kirk":False,"tng_ds9_voyager":True})
    def test_negative_wrong_era(self): self.check_bad(lambda d: d.update(scope="pike"))
    def test_negative_true_runtime(self): self.check_bad(lambda d: d.update(gameplay_activated=True))
    def test_negative_forced_future(self): self.check_bad(lambda d: d.update(auto_bootstrap_future=True))
    def test_negative_playable_temporal_jump(self): self.check_bad(lambda d: d.update(playable_time_travel=True))
    def test_negative_start_year_invented(self): self.check_bad(lambda d: d["reference_window"].update(campaign_start_date="2372-03-14"))
    def test_negative_original_event_purged(self): self.check_bad(lambda d: d["reused_catalogues"][0]["retained_event_ids"].pop())
    def test_negative_duplicate_original(self): self.check_bad(lambda d: d["reused_catalogues"][0]["retained_event_ids"].append(d["reused_catalogues"][0]["retained_event_ids"][0]))
    def test_negative_false_report_reclassified(self): self.check_bad(lambda d: d["reused_catalogues"][0].update(false_claim_event_ids=[]))
    def test_negative_unknown_source(self): self.check_bad(lambda d: d["additional_historical_anchors"][0]["provenance"][0].update(source_id="NO_SUCH_EPISODE"))
    def test_negative_invent_exact_date(self): self.check_bad(lambda d: d["additional_historical_anchors"][0]["time_anchor"].update(precision="EXACT_DAY"))
    def test_negative_off_period(self): self.check_bad(lambda d: d["additional_historical_anchors"][0]["time_anchor"].update(reference_year=2265))
    def test_negative_future_mandatory(self): self.check_bad(lambda d: d["additional_historical_anchors"][0].update(must_never_force_poststart=False))
    def test_negative_universal_knowledge(self): self.check_bad(lambda d: d["additional_historical_anchors"][0].update(knowledge_not_universal=False))
    def test_negative_valhalla_backdate(self): self.check_bad(lambda d: d["ship_temporal_reservations"][0].update(service_entry_year=2372))
    def test_negative_odyssey_backdate(self): self.check_bad(lambda d: d["ship_temporal_reservations"][1].update(service_entry_year=2373))
    def test_negative_wrong_playable_profile(self):
        with self.assertRaises(AssertionError):
            validate_index(self.data, self.diplomatic, self.sources, {"pike":True,"kirk":False,"tng_ds9_voyager":True})

if __name__ == "__main__":
    unittest.main(verbosity=2)
