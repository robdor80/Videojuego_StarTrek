#!/usr/bin/env python3
"""LORE-03D: independent editorial unit tests and hostile mutations; no game runtime."""
import copy
import unittest
import validate_lore03_d as v

class Lore03DTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack=v.load(v.CASEBOOK)
        cls.sc={x["id"]:x for x in cls.pack["scenarios"]}

    def decision(self, id, change=None):
        item=copy.deepcopy(self.sc[id])
        if change: change(item["input"])
        return v.judge(item)
    def reject_mutated_pack(self, mutation):
        pack=copy.deepcopy(self.pack)
        mutation(pack)
        with self.assertRaises(v.InvalidLore03D): v.validate_scenario(pack["scenarios"][0]) if not mutation else self.assert_pack_invariants(pack)
    def assert_pack_invariants(self, pack):
        for c in pack["scenarios"]: v.validate_scenario(c)
    def test_01_integrity(self):
        result=v.validate()
        self.assertEqual(result["status"],"NEEDS_REVIEW_DOCUMENTARY")
        self.assertGreaterEqual(result["cases"],30)
        self.assertIs(result["runtime_verified"],False)
    def test_02_canonical_eras_and_future(self):
        self.assertEqual(self.pack["era"],"tng_ds9_voyager")
        self.assertFalse(self.pack["auto_schedules_future_canon"])
    def test_03_temporal_cut(self):
        self.assertEqual(v.classification(2375),"PAST_YEAR")
        self.assertEqual(v.classification(2383),"UNRESOLVED_SAME_YEAR")
        self.assertEqual(v.classification(2387),"FUTURE_YEAR")
        self.assertEqual(v.classification(2383,order="BEFORE"),"BEFORE")
    def test_04_all_fixture_outcomes(self):
        for scenario in self.pack["scenarios"]:
            with self.subTest(scenario=scenario["id"]):
                self.assertEqual(v.validate_scenario(scenario),scenario["expected_decision"])
    def test_05_no_rewrite(self): self.assertEqual(self.decision("T01"),"REJECT")
    def test_06_no_fated_romulus(self): self.assertEqual(self.decision("T02"),"REJECT")
    def test_07_romulus_exists(self): self.assertEqual(self.decision("T21"),"ALLOW")
    def test_08_same_year_ambiguous(self): self.assertEqual(self.decision("T04"),"UNRESOLVED")
    def test_09_same_year_ordered(self): self.assertEqual(self.decision("T22"),"ALLOW")
    def test_10_offscreen_possible(self): self.assertEqual(self.decision("T15"),"ALLOW")
    def test_11_multi_save_segregation(self): self.assertEqual(self.decision("T08"),"REJECT")
    def test_12_unchanged_roundtrip(self): self.assertEqual(self.decision("T20"),"ALLOW")
    def test_13_lod_identity(self): self.assertEqual(self.decision("T26"),"ALLOW")
    def test_14_ai_cannot_authorize(self): self.assertEqual(self.decision("T06"),"REJECT")
    def test_15_ignorance_future(self): self.assertEqual(self.decision("T07"),"REJECT")
    def test_16_false_tzenkethi(self): self.assertEqual(self.decision("T16"),"REJECT")
    def test_17_no_auto_promotion(self): self.assertEqual(self.decision("T12"),"REJECT")
    def test_18_no_auto_valhalla(self): self.assertEqual(self.decision("T17"),"REJECT")
    def test_19_no_instant_rise(self): self.assertEqual(self.decision("T18"),"REJECT")
    def test_20_time_travel_refused(self): self.assertEqual(self.decision("T33"),"REJECT")
    def test_21_mutate_accepted_treaty_no_cause(self):
        self.assertEqual(self.decision("T13",lambda x:x.update(cause_refs=[])),"REJECT")
    def test_22_mutate_accepted_treaty_ai_authority(self):
        self.assertEqual(self.decision("T13",lambda x:x.update(authorizer="AI")),"REJECT")
    def test_23_mutate_accepted_treaty_no_resources(self):
        self.assertEqual(self.decision("T13",lambda x:x.update(resource_evidence=False)),"REJECT")
    def test_24_mutate_accepted_treaty_actor_missing(self):
        self.assertEqual(self.decision("T13",lambda x:x.update(actor_available=False)),"REJECT")
    def test_25_mutate_remote_player_presence(self):
        self.assertEqual(self.decision("T15",lambda x:x.update(requires_player_presence=True)),"REJECT")
    def test_26_mutate_valid_save_other_campaign(self):
        self.assertEqual(self.decision("T31",lambda x:x.update(source_campaign_id="S2")),"REJECT")
    def test_27_mutate_save_history(self):
        self.assertEqual(self.decision("T20",lambda x:x["history_prefix_after"].append("phantom")),"REJECT")
    def test_28_mutate_save_replay(self):
        self.assertEqual(self.decision("T20",lambda x:x.update(replays_effects=True)),"REJECT")
    def test_29_mutate_lod_identity(self):
        self.assertEqual(self.decision("T26",lambda x:x.update(entity_id_after="new-id")),"REJECT")
    def test_30_mutate_valid_promotion_no_merits(self):
        self.assertEqual(self.decision("T27",lambda x:x.update(performance_ref=None)),"REJECT")
    def test_31_mutate_valid_promotion_no_authority(self):
        self.assertEqual(self.decision("T27",lambda x:x.update(authority_ref=None)),"REJECT")
    def test_32_mutate_assigned_valhalla_guaranteed(self):
        self.assertEqual(self.decision("T28",lambda x:x.update(guaranteed_assignment=True)),"REJECT")
    def test_33_mutate_rise_without_research(self):
        self.assertEqual(self.decision("T29",lambda x:x.update(validated_research=False)),"REJECT")
    def test_34_mutate_rise_without_approval(self):
        self.assertEqual(self.decision("T29",lambda x:x.update(institutional_approval=False)),"REJECT")
    def test_35_mutate_news_before_event(self):
        self.assertEqual(self.decision("T14",lambda x:x.update(learned_year=2383)),"REJECT")
    def test_36_mutate_news_secret_without_clearance(self):
        self.assertEqual(self.decision("T14",lambda x:x.update(classified=True)),"REJECT")
    def test_37_mutate_death_forced_grief(self):
        self.assertEqual(self.decision("T30",lambda x:x.update(universal_grief=True)),"REJECT")
    def test_38_mutate_death_history_erased(self):
        self.assertEqual(self.decision("T30",lambda x:x.update(identity_retained=False)),"REJECT")
    def test_39_mutate_false_report_claim_true(self):
        self.assertEqual(self.decision("T32",lambda x:x.update(claims_actual_coup=True)),"REJECT")
    def test_40_mutate_canon_reference_forced(self):
        self.assertEqual(self.decision("T25",lambda x:x.update(mandatory=True)),"REJECT")
    def test_41_mutate_historical_reference_rewrite(self):
        self.assertEqual(self.decision("T24",lambda x:x.update(changes_verified_past=True)),"REJECT")
    def test_42_mutate_same_year_without_evidence(self):
        self.assertEqual(self.decision("T22",lambda x:x.update(order_evidence=False)),"UNRESOLVED")
    def test_43_missing_evidence_is_invalid(self):
        x=copy.deepcopy(self.sc["T13"]);del x["input"]["cause_refs"]
        with self.assertRaises(v.InvalidLore03D):v.validate_scenario(x)
    def test_44_duplicate_identity_is_invalid(self):
        x=copy.deepcopy(self.sc["T13"]);x["kind"]="not_a_kind"
        with self.assertRaises(v.InvalidLore03D):v.validate_scenario(x)
    def test_45_fake_status_is_invalid(self):
        x=copy.deepcopy(self.sc["T13"]);x["non_runtime_hypothetical"]=False
        with self.assertRaises(v.InvalidLore03D):v.validate_scenario(x)

if __name__ == "__main__":
    unittest.main(verbosity=2)
