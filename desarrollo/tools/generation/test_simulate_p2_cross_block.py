#!/usr/bin/env python3
"""P2 R3/R4 invariants over one synthetic cross-domain ledger; not native F13."""
import copy
import json
import unittest
from pathlib import Path

from p2_reference_reconciliation import verify_causal_bridge, verify_consistent_read
import simulate_colonization_expansion as colony

ROOT = Path(__file__).resolve().parents[3]
FIX = ROOT / "desarrollo/validation/fixtures"


def ledger():
    return json.loads((FIX / "p2_reconciliation/causal_bridge_v1.json").read_text(encoding="utf-8"))


def snapshot():
    return {"campaign_id":"campaign:p2-bridge-fixture",
            "read_token":"synthetic:read:7", "read_revision":7, "snapshot_tick":120,
            "facts":[
              {"fact_id":"fact:old", "campaign_id":"campaign:p2-bridge-fixture",
               "origin_revision":1,"version_revision":2,"tick":91,
               "status":"accepted","issuer_ref":"synthetic:core"},
              {"fact_id":"fact:new", "campaign_id":"campaign:p2-bridge-fixture",
               "origin_revision":6,"version_revision":7,"tick":116,
               "status":"accepted","issuer_ref":"synthetic:core"}]}


class P2CrossBlockReferenceGates(unittest.TestCase):
    def test_h15_complete_ten_domain_ledger(self):
        proof = verify_causal_bridge(ledger())
        self.assertEqual(len(proof["domains"]), 10)
        self.assertEqual(proof["population_transfers"], 1)
        self.assertEqual(proof["inventory_transfers"], 1)
        self.assertEqual(proof["unique_units"], 1)

    def test_h15_rejects_unpaired_population_and_duplicate_transfer(self):
        x = ledger()
        x["records"][0]["ledger"].pop()
        with self.assertRaisesRegex(ValueError, "unbalanced"):
            verify_causal_bridge(x)
        x = ledger()
        x["records"][0]["ledger"].append(copy.deepcopy(x["records"][0]["ledger"][0]))
        with self.assertRaisesRegex(ValueError, "unbalanced"):
            verify_causal_bridge(x)

    def test_h15_rejects_unbalanced_inventory(self):
        x = ledger()
        x["records"][1]["ledger"][1]["delta"] = 80
        with self.assertRaisesRegex(ValueError, "resource transfer"):
            verify_causal_bridge(x)

    def test_h15_rejects_duplicate_military_identity(self):
        x = ledger()
        x["records"][3]["ledger"].append({
            "kind":"unit_ownership","unit_id":"vessel:unique-001","owner_ref":"fleet:other"})
        with self.assertRaisesRegex(ValueError, "duplicate military"):
            verify_causal_bridge(x)

    def test_h15_rejects_retrocausality_and_forecast_write(self):
        x = ledger()
        x["records"][4]["tick"] = 1
        with self.assertRaisesRegex(ValueError, "clock regression"):
            verify_causal_bridge(x)
        x = ledger()
        x["records"][7]["ledger"].append({"kind":"population_transfer",
            "transfer_id":"fake","account_ref":"civ:x","delta":100})
        with self.assertRaisesRegex(ValueError, "cannot mutate"):
            verify_causal_bridge(x)
        x = ledger()
        x["records"][9]["ledger"].append({"kind":"inventory_transfer",
            "transfer_id":"fake","account_ref":"warehouse:x","delta":100})
        with self.assertRaisesRegex(ValueError, "cannot mutate"):
            verify_causal_bridge(x)

    def test_h15_rejects_improper_information_and_campaign(self):
        x = ledger()
        x["records"][4]["ledger"][0]["issuer_domain"] = "PADD"
        with self.assertRaisesRegex(ValueError, "disclosure"):
            verify_causal_bridge(x)
        x = ledger()
        x["records"][6]["campaign_id"] = "foreign"
        with self.assertRaisesRegex(ValueError, "cross-campaign"):
            verify_causal_bridge(x)
        x = ledger()
        x["records"][9]["source_refs"] = ["ref:unknown"]
        with self.assertRaisesRegex(ValueError, "missing causal"):
            verify_causal_bridge(x)

    def test_h14_multiple_origin_revisions_share_consistent_read(self):
        self.assertTrue(verify_consistent_read(snapshot()))
        x = snapshot()
        x["facts"][0]["version_revision"] = 8
        with self.assertRaisesRegex(ValueError, "beyond read"):
            verify_consistent_read(x)
        x = snapshot()
        x["facts"][0]["tick"] = 150
        with self.assertRaisesRegex(ValueError, "beyond read"):
            verify_consistent_read(x)
        x = snapshot()
        x["facts"][0]["fact_id"] = x["facts"][1]["fact_id"]
        with self.assertRaisesRegex(ValueError, "duplicate fact"):
            verify_consistent_read(x)

    def test_h15_b02_foundation_conserves_two_real_simulated_accounts(self):
        i = json.loads((FIX / "colonization_expansion/viable_colony_25y_v0.1.json").read_text())["input"]
        i["years"] = 0
        original = i["initial"]["origin_population"]
        out = colony.simulate_project(**i)
        self.assertEqual(out["snapshots"][0]["origin_population"] +
                         out["snapshots"][0]["colony_population"], original)
        self.assertEqual(out["snapshots"][0]["migrants_transferred_total"],
                         i["initial"]["founding_population"])
        self.assertEqual(colony.validate(out), [])

    def test_h15_ledger_independent_of_lod_metadata(self):
        a, b = ledger(), ledger()
        a["lod"] = "near"
        b["lod"] = "offscreen"
        self.assertEqual(verify_causal_bridge(a), verify_causal_bridge(b))


if __name__ == "__main__":
    unittest.main()
