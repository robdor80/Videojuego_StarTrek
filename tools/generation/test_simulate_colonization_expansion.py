#!/usr/bin/env python3
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODULE_PATH = HERE / "simulate_colonization_expansion.py"
FIXTURES = ROOT / "validation" / "fixtures" / "colonization_expansion"
spec = importlib.util.spec_from_file_location("colx", MODULE_PATH)
colx = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = colx
spec.loader.exec_module(colx)

def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

class ColonizationExpansionTests(unittest.TestCase):
    def test_selects_causal_best_target(self):
        f=load("target_selection_v0.1.json"); r=colx.select_target(f["candidates"],f["policy"])
        self.assertEqual(r["selected_location_id"],f["expected"]["selected_location_id"])

    def test_prewarp_target_rejected(self):
        f=load("target_selection_v0.1.json"); protected=next(x for x in f["candidates"] if x["location_id"]=="sys:protected")
        r=colx.evaluate_candidate(protected,f["policy"])
        self.assertFalse(r["eligible"]); self.assertEqual(r["reason"],f["expected"]["protected_reason"])

    def test_existing_claim_warns_not_silently_transfers(self):
        f=load("target_selection_v0.1.json"); c=copy.deepcopy(f["candidates"][0]); c["existing_claimant_refs"]=["polity:other"]
        r=colx.evaluate_candidate(c,f["policy"]); self.assertTrue(r["eligible"]); self.assertIn("existing_claim_dispute_risk",r["warnings"])

    def test_overlap_creates_dispute_not_war(self):
        f=load("overlapping_claims_v0.1.json"); r=colx.resolve_claim_overlap(f["claims"]); self.assertEqual(r,f["expected"])

    def test_deterministic(self):
        f=load("viable_colony_25y_v0.1.json")
        self.assertEqual(colx.simulate_project(**f["input"]),colx.simulate_project(**f["input"]))

    def test_viable_colony_matures(self):
        f=load("viable_colony_25y_v0.1.json"); r=colx.simulate_project(**f["input"]); self.assertEqual(colx.validate(r),[])
        for k,v in f["expected"].items(): self.assertEqual(r["final_state"][k],v)

    def test_population_transfer_not_duplication(self):
        f=load("viable_colony_25y_v0.1.json"); r=colx.simulate_project(**f["input"]); s=r["final_state"]
        self.assertEqual(s["origin_population"]+s["colony_population"],f["input"]["initial"]["origin_population"]+s["natural_births_total"])

    def test_abandonment_ends_control_but_not_history(self):
        f=load("abandoned_colony_v0.1.json"); r=colx.simulate_project(**f["input"]); self.assertEqual(colx.validate(r),[])
        for k,v in f["expected"].items():
            if k!="evacuation_event": self.assertEqual(r["final_state"][k],v)
        self.assertTrue(any(e["event_id"]==f["expected"]["evacuation_event"] and e["type"]=="colony_abandoned" for e in r["history"]))

    def test_autonomy_candidate_is_not_independence(self):
        f=load("viable_colony_25y_v0.1.json"); inp=copy.deepcopy(f["input"]); inp["years"]=1; inp["initial"]["governance_maturity"]=70
        inp["scheduled_events"]=[{"year":1,"event_id":"evt:pressure","cause_refs":["politics:local"],"effects":{"autonomy_pressure_delta":90}}]
        r=colx.simulate_project(**inp); self.assertTrue(r["final_state"]["autonomy_candidate"]); self.assertEqual(r["final_state"]["governance_status"],"home_administered")

    def test_independence_preserves_civilization_id(self):
        f=load("viable_colony_25y_v0.1.json"); inp=copy.deepcopy(f["input"]); inp["years"]=1; inp["initial"]["governance_maturity"]=80; inp["initial"]["autonomy_pressure"]=90
        inp["scheduled_events"]=[{"year":1,"event_id":"evt:independence","cause_refs":["agreement:recognized"],"effects":{"independence_recognized":True,"new_polity_ref":"polity:haven"}}]
        r=colx.simulate_project(**inp); self.assertEqual(r["civilization_id"],inp["civilization_id"]); self.assertEqual(r["final_state"]["governance_status"],"independent_polity"); self.assertEqual(r["final_state"]["effective_controller_ref"],"polity:haven")

if __name__ == "__main__":
    unittest.main()
