#!/usr/bin/env python3
"""Independent negative-mutation tests for LORE-03E. Not tests of gameplay runtime."""
import copy
import unittest
import validate_lore03_e as v

class Lore03E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=v.read_json(v.A)
        cls.legacy=v.read_json(v.LEGACY)
        cls.b=v.read_json(v.B)
        cls.c=v.read_json(v.C)
        cls.p=v.read_json(v.PATTERNS)
        cls.d=v.read_json(v.D)
        cls.events=v.event_map(cls.legacy,cls.a)
        cls.conflicts={x["conflict_id"] for x in cls.b["dossiers"]}
        cls.eras={x:v.read_json(f"sistemas/universe/chronology/era_profiles/{x}/era_profile.json")
                  for x in ("pike","kirk","tng_ds9_voyager")}
        cls.status=(v.ROOT/"CONTENT_STATUS.md").read_text(encoding="utf-8")
        cls.closure=v.read_json(v.CLOSURE)

    def test_positive_gate(self):
        d=v.validate()
        self.assertEqual((d["events"],d["conflicts"],d["d_scenarios"]),(66,22,35))
        self.assertFalse(d["runtime_verified"])
        self.assertEqual(d["status"],"COMPLETE_DOCUMENTARY")
        self.assertTrue(d["merge_authorized"])
    def test_duplicate_history_id_rejected(self):
        a=copy.deepcopy(self.a)
        a["additional_historical_anchors"][0]["event_id"]=self.legacy["events"][0]["event_id"]
        with self.assertRaises(v.CrossAuditError):v.event_map(self.legacy,a)
    def test_missing_inherited_history_rejected(self):
        a=copy.deepcopy(self.a)
        a["reused_catalogues"][0]["retained_event_ids"].pop()
        with self.assertRaises(v.CrossAuditError):v.event_map(self.legacy,a)
    def test_missing_dossier_event_rejected(self):
        a=copy.deepcopy(self.c)
        a["cases"][0]["event_ref"]="ghost_event_id"
        with self.assertRaises(v.CrossAuditError):
            v.validate_memories(a,self.p,self.events,self.conflicts)
    def test_missing_conflict_for_memory_rejected(self):
        a=copy.deepcopy(self.c)
        a["cases"][0]["conflict_ref"]="unknown_conflict"
        with self.assertRaises(v.CrossAuditError):
            v.validate_memories(a,self.p,self.events,self.conflicts)
    def test_memory_unauthorized_rejected(self):
        a=copy.deepcopy(self.c)
        a["world_state_authority"]="AI"
        with self.assertRaises(v.CrossAuditError):
            v.validate_memories(a,self.p,self.events,self.conflicts)
    def test_institution_creates_world_rejected(self):
        a=copy.deepcopy(self.p)
        a["patterns"][0]["runtime_state_mutation"]=True
        with self.assertRaises(v.CrossAuditError):
            v.validate_memories(self.c,a,self.events,self.conflicts)
    def test_future_mandatory_rejected(self):
        d=copy.deepcopy(self.d)
        d["auto_schedules_future_canon"]=True
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(self.a,d,self.eras,self.status,self.closure)
    def test_ai_changes_authority_rejected(self):
        d=copy.deepcopy(self.d)
        d["world_state_authority"]="AI"
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(self.a,d,self.eras,self.status,self.closure)
    def test_pike_playable_rejected(self):
        eras=copy.deepcopy(self.eras)
        eras["pike"]["playable"]=True
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(self.a,self.d,eras,self.status,self.closure)
    def test_same_year_fake_date_rejected(self):
        a=copy.deepcopy(self.a)
        a["reference_window"]["campaign_start_date"]="2383-01-01"
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(a,self.d,self.eras,self.status,self.closure)
    def test_reopen_e_without_authorization_rejected(self):
        status=self.status.replace("| E — Auditoría global | ✅ COMPLETE |",
                                   "| E — Auditoría global | ⬜ TODO |")
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(self.a,self.d,self.eras,status,self.closure)
    def test_missing_merge_evidence_rejected(self):
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(self.a,self.d,self.eras,self.status,{})
    def test_wrong_merge_sha_rejected(self):
        bad=copy.deepcopy(self.closure)
        bad["merge_commit_sha"]="0"*40
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(self.a,self.d,self.eras,self.status,bad)
    def test_wrong_ci_run_sha_rejected(self):
        bad=copy.deepcopy(self.closure)
        bad["post_merge_checks"][0]["head_sha"]="0"*40
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(self.a,self.d,self.eras,self.status,bad)
    def test_failure_in_ci_rejected(self):
        bad=copy.deepcopy(self.closure)
        bad["post_merge_checks"][0]["conclusion"]="failure"
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(self.a,self.d,self.eras,self.status,bad)
    def test_false_runtime_claim_rejected(self):
        bad=copy.deepcopy(self.closure)
        bad["runtime_verified"]=True
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(self.a,self.d,self.eras,self.status,bad)
    def test_duplicate_d_scenario_rejected(self):
        d=copy.deepcopy(self.d)
        d["scenarios"][-1]["id"]=d["scenarios"][0]["id"]
        with self.assertRaises(v.CrossAuditError):
            v.validate_boundary(self.a,d,self.eras,self.status,self.closure)
    def test_memories_must_stay_hypothetical(self):
        a=copy.deepcopy(self.c)
        a["cases"][0]["case_kind"]="LIVE_NPC"
        with self.assertRaises(v.CrossAuditError):
            v.validate_memories(a,self.p,self.events,self.conflicts)

if __name__=="__main__":
    unittest.main(verbosity=2)
