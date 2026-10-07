#!/usr/bin/env python3
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MODULE_PATH = HERE / "simulate_conflict_war.py"
FIXTURES = ROOT / "validation" / "fixtures" / "conflict_war"
spec = importlib.util.spec_from_file_location("cw", MODULE_PATH)
cw = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = cw
spec.loader.exec_module(cw)

def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))

class ConflictWarTests(unittest.TestCase):
    def test_same_crisis_context_changes_response(self):
        f=load("doctrine_context_comparison_v0.1.json")
        k=cw.assess_response(f["profiles"]["klingon_empire_context"],f["situation"])
        v=cw.assess_response(f["profiles"]["vulcan_mainstream_context"],f["situation"])
        self.assertEqual(k["recommended_action"],f["expected"]["klingon_action"])
        self.assertEqual(v["recommended_action"],f["expected"]["vulcan_action"])
        self.assertGreater(k["escalation_score"],v["escalation_score"])

    def test_species_aggression_field_is_forbidden(self):
        f=load("doctrine_context_comparison_v0.1.json"); p=copy.deepcopy(f["profiles"]["klingon_empire_context"]); p["species_aggression"]=100
        with self.assertRaises(ValueError): cw.assess_response(p,f["situation"])

    def test_weakened_klingon_context_can_avoid_war(self):
        f=load("weakened_klingon_restraint_v0.1.json"); r=cw.assess_response(f["profile"],f["situation"])
        self.assertEqual(r["recommended_action"],f["expected"]["recommended_action"]); self.assertEqual(r["escalation_score"],f["expected"]["escalation_score"])

    def test_severe_crisis_can_reach_war_candidate(self):
        f=load("doctrine_context_comparison_v0.1.json"); s=copy.deepcopy(f["situation"])
        s.update(relative_force_percent=145,military_readiness=90,logistics_support=90,war_exhaustion=0,expected_loss_risk=20,threat=95,stakes=95,grievance=90,honor_or_reputation_challenge=95,relation_tension=95,negotiation_opportunity=20)
        self.assertEqual(cw.assess_response(f["profiles"]["klingon_empire_context"],s)["recommended_action"],"war_declaration_candidate")

    def test_war_candidate_requires_authority(self):
        f=load("doctrine_context_comparison_v0.1.json"); s=copy.deepcopy(f["situation"])
        s.update(relative_force_percent=145,military_readiness=90,logistics_support=90,war_exhaustion=0,expected_loss_risk=20,threat=95,stakes=95,grievance=90,honor_or_reputation_challenge=95,relation_tension=95,negotiation_opportunity=20,war_authority_granted=False)
        self.assertEqual(cw.assess_response(f["profiles"]["klingon_empire_context"],s)["recommended_action"],"seek_war_authority")

    def test_strategic_operation_is_deterministic(self):
        f=load("strategic_operation_v0.1.json")
        self.assertEqual(cw.resolve_operation(**f["input"]),cw.resolve_operation(**f["input"]))

    def test_strategic_operation_spawns_no_forces(self):
        f=load("strategic_operation_v0.1.json"); r=cw.resolve_operation(**f["input"])
        self.assertEqual(cw.validate_operation(r),[]); self.assertEqual(r["spawned_unit_ids"],[])

    def test_strategic_operation_persistent_damage_matches_fixture(self):
        f=load("strategic_operation_v0.1.json"); r=cw.resolve_operation(**f["input"])
        ai={u["unit_id"]:u["integrity"] for u in r["attacker_after"]["units"]}; di={u["unit_id"]:u["integrity"] for u in r["defender_after"]["units"]}
        self.assertEqual(ai,f["expected"]["attacker_integrity"]); self.assertEqual(di,f["expected"]["defender_integrity"])

    def test_operation_does_not_change_sovereignty(self):
        f=load("strategic_operation_v0.1.json"); r=cw.resolve_operation(**f["input"])
        self.assertFalse(r["sovereignty_changed"]); self.assertTrue(r["control_change_candidate"])

    def test_war_declaration_requires_cause_objective_authority(self):
        f=load("war_lifecycle_v0.1.json"); bad=copy.deepcopy(f["events"][0]); bad["cause_refs"]=[]
        with self.assertRaises(ValueError): cw.apply_conflict_event(f["initial_state"],bad)

    def test_occupation_changes_control_not_sovereignty(self):
        f=load("war_lifecycle_v0.1.json"); s=cw.apply_conflict_event(f["initial_state"],f["events"][0]); s=cw.apply_conflict_event(s,f["events"][1])
        self.assertEqual(s["effective_control_ref"],f["expected"]["after_occupation_control"]); self.assertEqual(s["sovereignty_ref"],f["expected"]["sovereignty_ref"])

    def test_ceasefire_and_peace_do_not_erase_history_or_objectives(self):
        f=load("war_lifecycle_v0.1.json"); s=copy.deepcopy(f["initial_state"]); states=[]
        for event in f["events"]: s=cw.apply_conflict_event(s,event); states.append(copy.deepcopy(s))
        self.assertEqual(states[0]["conflict_state"],f["expected"]["after_war"]); self.assertEqual(states[2]["conflict_state"],f["expected"]["after_ceasefire"]); self.assertEqual(states[-1]["conflict_state"],f["expected"]["final_state"])
        self.assertEqual(states[-1]["war_objective_refs"],f["expected"]["war_objectives_preserved"]); self.assertEqual(states[-1]["grievance_refs"],f["expected"]["grievance_refs"])

    def test_player_presence_is_not_a_response_input(self):
        f=load("doctrine_context_comparison_v0.1.json"); base=cw.assess_response(f["profiles"]["klingon_empire_context"],f["situation"]); altered=copy.deepcopy(f["situation"]); altered["player_present"]=True
        self.assertEqual(base,cw.assess_response(f["profiles"]["klingon_empire_context"],altered))

if __name__ == "__main__":
    unittest.main()
