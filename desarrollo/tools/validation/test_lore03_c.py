#!/usr/bin/env python3
"""LORE-03C positive cases and deliberate mutations (documentary only)."""
import copy
import unittest
import validate_lore03_c as v

class Lore03CMemoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.refs=v.context()
        cls.book=v.load(v.CASEBOOK)
        cls.pats=v.load(v.PATTERNS)
    def mut_case(self, case_id, change):
        case=copy.deepcopy(next(x for x in self.book["cases"] if x["case_id"]==case_id))
        change(case)
        with self.assertRaises(v.InvalidLore03C):
            v.validate_case(case,self.refs)
    def mut_book(self, change):
        book=copy.deepcopy(self.book)
        change(book)
        with self.assertRaises(v.InvalidLore03C):
            v.validate_sets(book,self.pats,self.refs)
    def mut_pat(self, pattern_id, change):
        p=copy.deepcopy(next(x for x in self.pats["patterns"] if x["pattern_id"]==pattern_id))
        change(p)
        with self.assertRaises(v.InvalidLore03C):
            v.validate_pattern(p,self.refs)

    def test_01_full(self): self.assertEqual(v.validate()["cases"],13)
    def test_02_patterns(self): self.assertEqual(v.validate()["institutional_patterns"],6)
    def test_03_legacy_counts(self): self.assertEqual(len(self.refs["events"]),66)
    def test_04_prior_conflicts(self): self.assertEqual(len(self.refs["dossiers"]),22)
    def test_05_fake_tzenkethi(self): self.assertTrue(self.refs["events"][v.FALSE_REPORT]["false"])
    def test_06_wolf_two_memories(self):
        x=[a for a in self.book["cases"] if a["event_ref"]=="wolf_359_battle" and a["remembered_as"]=="firsthand"]
        self.assertEqual(len(x),2)
        self.assertNotEqual(x[0]["example_es"],x[1]["example_es"])
    def test_07_learning_after_birth(self):
        x=next(a for a in self.book["cases"] if a["case_id"]=="bajor_family_account")
        self.assertGreater(x["actor"]["birth_year"],self.refs["events"][x["event_ref"]]["year"])
        self.assertEqual(x["remembered_as"],"learned")
    def test_08_no_real_actor_instantiated(self):
        self.assertTrue(all(not x["actor"]["canonical_identity_asserted"] for x in self.book["cases"]))
    def test_09_no_installed_tech(self): self.assertNotIn("Sensores Rise",repr(self.book))
    def test_10_reject_unknown_event(self): self.mut_case("wolf_veteran_01",lambda x:x.update(event_ref="FAKE_WAR"))
    def test_11_reject_unknown_conflict(self): self.mut_case("wolf_veteran_01",lambda x:x.update(conflict_ref="not_a_conflict"))
    def test_12_reject_cross_conflict(self): self.mut_case("wolf_veteran_01",lambda x:x.update(conflict_ref="dominion_war"))
    def test_13_reject_birth_after_battle(self): self.mut_case("wolf_veteran_01",lambda x:x["actor"].update(birth_year=2370))
    def test_14_reject_birth_same_year(self): self.mut_case("wolf_veteran_01",lambda x:x["actor"].update(birth_year=2367))
    def test_15_reject_direct_no_service_evidence(self): self.mut_case("wolf_veteran_01",lambda x:x["actor"].update(assignment_provenance=None))
    def test_16_reject_direct_rumor(self): self.mut_case("wolf_veteran_01",lambda x:x["access"].update(channel="rumor"))
    def test_17_reject_family_as_witness(self): self.mut_case("bajor_family_account",lambda x:x.update(remembered_as="firsthand"))
    def test_18_reject_assigned_family_story(self): self.mut_case("bajor_family_account",lambda x:x["actor"].update(assignment_provenance="ILLUSTRATIVE_SERVICE_REQUIRES_VALIDATION"))
    def test_19_reject_false_report_worldfact(self): self.mut_case("tzenkethi_rumor",lambda x:x.update(world_event_claim="REFERENCES_SOURCE_FACT"))
    def test_20_reject_false_report_true_label(self): self.mut_case("tzenkethi_rumor",lambda x:x.update(claim_status="TRUE_EVENT_REPORTED"))
    def test_21_reject_false_report_direct_participation(self): self.mut_case("tzenkethi_rumor",lambda x:x.update(remembered_as="firsthand"))
    def test_22_reject_unauthorized_secret(self): self.mut_case("section31_restricted",lambda x:x["access"].update(authorization_evidence=None))
    def test_23_reject_secret_via_gossip(self): self.mut_case("section31_restricted",lambda x:x["access"].update(channel="rumor"))
    def test_24_reject_pretend_trauma(self): self.mut_case("dominion_resistance_veteran",lambda x:x.update(automatic_trauma=True))
    def test_25_reject_pretend_friendship(self): self.mut_case("wolf_veteran_02",lambda x:x.update(automatic_relationship=True))
    def test_26_reject_direct_world_mutation(self): self.mut_case("wolf_veteran_02",lambda x:x.update(runtime_state_mutation=True))
    def test_27_reject_automatic_consequence(self): self.mut_case("dominion_family_loss",lambda x:x.update(personal_consequence="TRAUMA_ALWAYS"))
    def test_28_reject_create_canon_npc(self): self.mut_case("wolf_veteran_02",lambda x:x["actor"].update(canonical_identity_asserted=True))
    def test_29_reject_book_bootstrap(self): self.mut_book(lambda x:x.update(auto_bootstrap_future=True))
    def test_30_reject_exact_D(self): self.mut_book(lambda x:x.update(campaign_start_exact_date="2383-01-01"))
    def test_31_reject_book_complete(self): self.mut_book(lambda x:x.update(status="COMPLETE_DOCUMENTARY"))
    def test_32_reject_duplicates(self): self.mut_book(lambda x:x["cases"][0].update(case_id=x["cases"][1]["case_id"]))
    def test_33_reject_new_world_true_event(self): self.mut_book(lambda x:x.update(creates_new_historical_events=True))
    def test_34_reject_memorial_instantiation(self):
        p=copy.deepcopy(self.pats);p["creates_memorials"]=True
        with self.assertRaises(v.InvalidLore03C):v.validate_sets(self.book,p,self.refs)
    def test_35_reject_false_coup_memorial(self):self.mut_pat("tzenkethi_report",lambda x:x.update(pattern_type="memorial_of_real_coup"))
    def test_36_reject_institutional_world_change(self):self.mut_pat("bajor_reconstruction",lambda x:x.update(runtime_state_mutation=True))
    def test_37_reject_institutional_no_permission(self):self.mut_pat("section31_sealed",lambda x:x.update(requires_authorized_institutional_event=False))
    def test_38_reject_missing_pattern_source(self):self.mut_pat("wolf_memorial",lambda x:x.update(event_ref="fake_memory"))
    def test_39_reject_false_coup_assertion(self):self.mut_pat("tzenkethi_report",lambda x:x.update(assert_tzenkethi_coup_happened=True))
    def test_40_reject_relabelled_real_event(self):self.mut_case("wolf_veteran_01",lambda x:x.update(claim_status="FALSE_REPORT_BELIEVED"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
