#!/usr/bin/env python3
"""Regression and mutation tests for historical chronology: editorial only."""
import copy
import unittest
from validate_lore03_a import validate,validate_index,load,classify_by_year

class AChronologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d=load("lore/historical_events/lore03_a_chronology_index_v0.1.json")
        cls.dipl={e["event_id"]:e for e in load("lore/diplomacy/historical_events_v0.1.json")["events"]}
        cls.registry={s["source_id"] for s in load("sources/source_registry/source_registry.json")["sources"]}
        cls.eras={e:load(f"universe/chronology/era_profiles/{e}/era_profile.json")["playable"]
                  for e in ("pike","kirk","tng_ds9_voyager")}
    def bad(self,mutator,eras=None,dipl=None):
        d=copy.deepcopy(self.d)
        mutator(d)
        with self.assertRaises(AssertionError):
            validate_index(d, self.dipl if dipl is None else dipl,self.registry,self.eras if eras is None else eras)

    def test_01_full(self):self.assertEqual(validate()["years"],15)
    def test_02_sources(self):self.assertGreaterEqual(validate()["sources"],507)
    def test_03_anchor_count(self):self.assertGreaterEqual(validate()["additional_anchors"],20)
    def test_04_original_count(self):self.assertEqual(validate()["historical_refs"],40)
    def test_05_temporal_past(self):self.assertEqual(classify_by_year(self.d["additional_historical_anchors"][0],2365),"ESTABLISHED_BEFORE_D")
    def test_06_temporal_future(self):self.assertEqual(classify_by_year(self.d["additional_historical_anchors"][0],2364),"UNRESOLVED_SAME_YEAR")
    def test_07_wolf_future(self):self.assertEqual(classify_by_year(self.d["additional_historical_anchors"][1],2366),"NOT_YET_AT_D")
    def test_08_voyager_future(self):
        x=next(e for e in self.d["additional_historical_anchors"] if e["event_id"]=="voyager_canonical_return")
        self.assertEqual(classify_by_year(x,2377),"NOT_YET_AT_D")
    def test_09_voyager_same_year_unresolved(self):
        x=next(e for e in self.d["additional_historical_anchors"] if e["event_id"]=="voyager_canonical_return")
        self.assertEqual(classify_by_year(x,2378),"UNRESOLVED_SAME_YEAR")
    def test_10_year_out_of_window(self):
        with self.assertRaises(AssertionError):
            classify_by_year(self.d["additional_historical_anchors"][0],2390)

    def test_11_wrong_status(self):self.bad(lambda d:d.update(status="COMPLETE"))
    def test_12_wrong_scope(self):self.bad(lambda d:d.update(scope="kirk"))
    def test_13_mutation_authority(self):self.bad(lambda d:d.update(authority="AI"))
    def test_14_live_runtime(self):self.bad(lambda d:d.update(gameplay_activated=True))
    def test_15_auto_future(self):self.bad(lambda d:d.update(auto_bootstrap_future=True))
    def test_16_temporal_play(self):self.bad(lambda d:d.update(playable_time_travel=True))
    def test_17_exact_start(self):self.bad(lambda d:d["reference_window"].update(campaign_start_date="2372-03-14"))
    def test_18_start_approved(self):self.bad(lambda d:d["reference_window"].update(date_is_author_approved=True))
    def test_19_wrong_window(self):self.bad(lambda d:d["reference_window"].update(start_year=2265))
    def test_20_same_year_forced(self):self.bad(lambda d:d.update(same_year_boundary_rule="PAST"))
    def test_21_missing_pike_history(self):self.bad(lambda d:d["prior_eras"].pop("pike"))
    def test_22_profile_era_reactivated(self):
        with self.assertRaises(AssertionError):
            validate_index(self.d,self.dipl,self.registry,{"pike":True,"kirk":False,"tng_ds9_voyager":True})
    def test_23_original_event_missing(self):self.bad(lambda d:d["reused_catalogues"][0]["retained_event_ids"].pop())
    def test_24_original_event_duplicate(self):self.bad(lambda d:d["reused_catalogues"][0]["retained_event_ids"].append("romulan_return"))
    def test_25_false_tzenkethi(self):self.bad(lambda d:d["reused_catalogues"][0].update(false_claim_event_ids=[]))
    def test_26_duplicate_canonical_event(self):self.bad(lambda d:d["additional_historical_anchors"][0].update(event_id="romulan_return"))
    def test_27_new_event_duplicate(self):self.bad(lambda d:d["additional_historical_anchors"][0].update(event_id="wolf_359_battle"))
    def test_28_no_source(self):self.bad(lambda d:d["additional_historical_anchors"][0].update(provenance=[]))
    def test_29_unknown_source(self):self.bad(lambda d:d["additional_historical_anchors"][0]["provenance"][0].update(source_id="NOT_IN_REGISTRY"))
    def test_30_false_precision(self):self.bad(lambda d:d["additional_historical_anchors"][0]["time_anchor"].update(precision="EXACT_DAY"))
    def test_31_bad_era_year(self):self.bad(lambda d:d["additional_historical_anchors"][0]["time_anchor"].update(reference_year=2265))
    def test_32_future_forced(self):self.bad(lambda d:d["additional_historical_anchors"][0].update(must_never_force_poststart=False))
    def test_33_poststart_runtime(self):self.bad(lambda d:d["additional_historical_anchors"][0].update(runtime_state_change=True))
    def test_34_omniscience(self):self.bad(lambda d:d["additional_historical_anchors"][0].update(knowledge_not_universal=False))
    def test_35_fake_entity_refs(self):self.bad(lambda d:d["additional_historical_anchors"][0]["historical_context"].update(subject_names_are_ids=True))
    def test_36_mandatory_story(self):self.bad(lambda d:d["additional_historical_anchors"][0].update(narrative_mandate=True))
    def test_37_event_hooks_invalid(self):self.bad(lambda d:d["additional_historical_anchors"][0].update(possible_consequence_hooks=["teleport_runtime"]))
    def test_38_no_precedents(self):self.bad(lambda d:d.update(historical_precedents=[]))
    def test_39_reservation_wolf(self):self.bad(lambda d:d["cross_reference_reservations"][0].update(status="RESOLVED_WITHOUT_EVIDENCE"))
    def test_40_backdated_valhalla(self):self.bad(lambda d:d["ship_temporal_reservations"][0].update(service_entry_year=2372))
    def test_41_backdated_odyssey(self):self.bad(lambda d:d["ship_temporal_reservations"][1].update(service_entry_year=2375))
    def test_42_sovereign_early(self):self.bad(lambda d:d["ship_temporal_reservations"][2].update(do_not_backdate=False))
    def test_43_inherited_event_promoted(self):
        copyd=copy.deepcopy(self.dipl)
        copyd["tzenkethi_false_coup_report"]["status"]="SCREEN_OR_OFFICIAL_ANCHOR"
        with self.assertRaises(AssertionError):
            validate_index(self.d,copyd,self.registry,self.eras)

if __name__=="__main__":
    unittest.main(verbosity=2)
