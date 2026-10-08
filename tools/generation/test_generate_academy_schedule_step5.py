#!/usr/bin/env python3
import copy, importlib.util, json, sys, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
MODULE=HERE/"generate_academy_schedule_step5.py"
FIXTURE=ROOT/"validation"/"fixtures"/"academy_life"/"schedule_baseline_v0.1.json"
spec=importlib.util.spec_from_file_location("academy_schedule_step5",MODULE);mod=importlib.util.module_from_spec(spec);assert spec and spec.loader;sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
def req(): return json.loads(FIXTURE.read_text(encoding="utf-8"))["request"]
def out(): return mod.build_schedules(req())
class AcademyScheduleStep5Tests(unittest.TestCase):
    def test_01_deterministic(self): self.assertEqual(out(),out())
    def test_02_input_order_independent(self):
        r=req(); x=copy.deepcopy(r); x["cadets"]=list(reversed(x["cadets"])); x["shared_commitments"]=list(reversed(x["shared_commitments"])); self.assertEqual(mod.build_schedules(r),mod.build_schedules(x))
    def test_03_every_slot_has_schedule(self): self.assertEqual(set(out()["schedules"]),{"cadet4:00","cadet4:01","cadet4:02"})
    def test_04_shared_class_synchronized(self):
        o=out(); vals={(e["day_index"],e["start_minute"],e["end_minute"],e["location_ref"]) for s in o["schedules"].values() for e in s if e.get("source_ref")=="CLS-NAV-01"}; self.assertEqual(len(vals),1)
    def test_05_no_conflicts_in_baseline(self): self.assertEqual(out()["schedule_conflicts"],[])
    def test_06_flexible_all_resolved(self): self.assertEqual(out()["unresolved_flexible_requirements"],[])
    def test_07_flexible_duration_preserved(self):
        o=out(); fs=[e for es in o["schedules"].values() for e in es if e["entry_type"] in ("formal_study","required_preparation")]; self.assertEqual(sorted(e["end_minute"]-e["start_minute"] for e in fs),[45,45,60])
    def test_08_flexible_inside_authored_windows(self):
        r=req(); o=mod.build_schedules(r); limits={x["requirement_id"]:x["allowed_windows"][0] for x in r["flexible_requirements"]}
        for es in o["schedules"].values():
            for e in es:
                if e["source_ref"] in limits:
                    w=limits[e["source_ref"]]; self.assertEqual(e["day_index"],w["day_index"]); self.assertGreaterEqual(e["start_minute"],w["start_minute"]); self.assertLessEqual(e["end_minute"],w["end_minute"])
    def test_09_transit_blocks_exist(self): self.assertTrue(any(e["entry_type"]=="transit" for es in out()["schedules"].values() for e in es))
    def test_10_transit_is_derived(self): self.assertTrue(all(e["derived"] for es in out()["schedules"].values() for e in es if e["entry_type"]=="transit"))
    def test_11_impossible_travel_is_conflict(self):
        r=req(); r["shared_commitments"].append({"commitment_id":"IMP","entry_type":"class","member_slot_refs":["cadet4:00"],"day_index":0,"start_minute":725,"end_minute":745,"location_ref":"medical_academy"})
        o=mod.build_schedules(r); self.assertTrue(any(c["type"] in ("insufficient_travel_time","overlap") for c in o["schedule_conflicts"]))
    def test_12_materialization_preserves_schedule(self):
        r=req(); a=mod.build_schedules(r); x=copy.deepcopy(r)
        for c in x["cadets"]: c["character_id"]="materialized:"+c["population_slot_ref"]
        self.assertEqual(a["schedules"],mod.build_schedules(x)["schedules"])
    def test_13_species_irrelevant(self):
        r=req(); x=copy.deepcopy(r)
        for c in x["cadets"]: c["species_id"]="changed_species"
        self.assertEqual(mod.build_schedules(r)["schedules"],mod.build_schedules(x)["schedules"])
    def test_14_personality_irrelevant(self):
        r=req(); x=copy.deepcopy(r)
        for c in x["cadets"]: c["personality_recipe_id"]="changed_personality"
        self.assertEqual(mod.build_schedules(r)["schedules"],mod.build_schedules(x)["schedules"])
    def test_15_player_presence_irrelevant(self):
        r=req(); x=copy.deepcopy(r); x["player_present"]=True; x["player_slot_ref"]="cadet4:00"; self.assertEqual(mod.build_schedules(r),mod.build_schedules(x))
    def test_16_uncommitted_not_filled(self):
        o=out(); self.assertTrue(any(o["uncommitted_intervals"].values())); self.assertTrue(all(i["classification"]=="uncommitted" for xs in o["uncommitted_intervals"].values() for i in xs)); self.assertEqual(o["future_step_state"]["free_time_activity_assignments"],[])
    def test_17_expected_not_actual_presence(self):
        o=out(); self.assertEqual(o["schedule_truth_semantics"],"expected_not_actual_presence"); self.assertFalse(any("current_location" in e for es in o["schedules"].values() for e in es))
    def test_18_invalid_identity_or_interval_rejected(self):
        r=req(); r["cadets"].append(copy.deepcopy(r["cadets"][0]))
        with self.assertRaises(ValueError): mod.build_schedules(r)
        r=req(); r["individual_commitments"][0]["end_minute"]=r["individual_commitments"][0]["start_minute"]
        with self.assertRaises(ValueError): mod.build_schedules(r)
if __name__=="__main__": unittest.main()
