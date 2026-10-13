#!/usr/bin/env python3
"""F06 independent contract tests. No CoreRPG/UE5 is invoked."""
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "tools/simulation/f06_reference.py"
spec = importlib.util.spec_from_file_location("f06_reference", MODULE)
f06 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = f06
spec.loader.exec_module(f06)


def entity(entity_id, position, *, signature="subspace", strength="strong", masked=False):
    return {
        "entity_id": entity_id, "entity_type": "anomaly",
        "temporal_state": {"active": True},
        "spatial_state": {"sector_id": "041", "system_id": "test:alpha",
                          "position": {"unit": "AU", "xyz": position}},
        "ground_truth": {
            "classification": "rift",
            "properties": {"diameter_km": 12},
            "hidden_properties": {"cause": {"value": "classified_core_truth",
                "minimum_resolution": "high", "preferred_filter": "subspace"}},
        },
        "signatures": [{
            "signature_id": "sig:" + entity_id,
            "signature_type": signature, "strength": strength,
            "detectability_modifiers": {"masking": 0.1 if masked else 0},
        }],
        "environmental_modifiers": {
            "masking": ["subspace_noise"] if masked else [],
            "local_interference": [],
        },
    }


WORLD = {"entities": [
    entity("world-secret-1", [1.0, 0.0, 0.0]),
    entity("world-secret-2", [5.0, 0.0, 0.0], signature="warp", strength="moderate"),
    entity("world-secret-3", [8.0, 0.0, 0.0], masked=True),
]}


def request(**kw):
    r = {
        "scan_id": "scan:6-a", "observer_id": "ship:imperator-training",
        "operator_id": "cadet:1", "origin_position_au": [0, 0, 0],
        "sector_id": "041", "system_id": "test:alpha",
        "range_mode": "long", "scan_mode": "active",
        "resolution": "standard", "filters": ["subspace"],
        "priority": "subspace", "scan_duration_s": 45,
        "sensor_profile": {"capability": 1.0, "power": 1.0, "integrity": 1.0},
    }
    r.update(kw)
    return r


def context(**kw):
    c = {
        "authorization_decision": "ALLOW_REFERENCE",
        "authorization_ref": "f05:example-only",
        "station_id": "station:sensors", "occupied_station": True,
        "ship_id": "ship:academy", "campaign_time": "2372-03-14T10:42:18",
        "available_power": 1.0, "selected_array_state": "operational",
        "supported_range_modes": ["short", "long", "focused"],
        "known_contact_ids": [],
        "order_id": "order:42",
        "state_revision": 7, "current_tick": 100,
        "authorization_binding": {
            "source": "F05_REFERENCE", "decision": "ALLOW_REFERENCE",
            "actor_id": "cadet:1", "action_id": "sensor_scan",
            "station_id": "station:sensors", "ship_id": "ship:academy",
            "state_revision": 7, "issued_tick": 90, "expires_tick": 110,
        },
    }
    c.update(kw)
    return c


class F06Tests(unittest.TestCase):
    def test_01_ten_primary_branches_and_three_scan_modes(self):
        path = ROOT / "gameplay/ship_operations/consoles/sensors/sensor_menu_tree.json"
        menu = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(len(menu["root"]), 10)
        self.assertEqual({s["id"] for s in next(x for x in menu["root"] if x["id"] == "scans")["secondary"]},
                         {"short_range", "long_range", "focused"})

    def test_02_reuse_existing_engine_without_truth_mutation(self):
        w, r, c = copy.deepcopy(WORLD), request(), context()
        originals = copy.deepcopy((w, r, c))
        answer = f06.run_reference_scan(w, r, c)
        self.assertEqual((w, r, c), originals)
        self.assertEqual(answer["result"]["engine"]["engine_id"], f06.sensor.ENGINE_ID)
        self.assertFalse(answer["authoritative"])
        self.assertEqual(answer["effects_applied"], 0)

    def test_03_repeat_same_input_and_no_secret_ids(self):
        a = f06.run_reference_scan(WORLD, request(), context())
        self.assertEqual(a, f06.run_reference_scan(WORLD, request(), context()))
        output = json.dumps(a, ensure_ascii=False)
        self.assertNotIn("world-secret", output)
        self.assertNotIn("ground_truth", output)
        self.assertNotIn("entity_id", output)
        self.assertNotIn("classified_core_truth", output)

    def test_04_observer_relative_contact_identity(self):
        a = f06.run_reference_scan(WORLD, request(), context())
        b = f06.run_reference_scan(
            WORLD, request(observer_id="ship:other", scan_id="scan:6-b"), context())
        self.assertNotEqual(a["result"]["detections"][0]["contact_id"],
                            b["result"]["detections"][0]["contact_id"])

    def test_05_partial_readout_then_final_at_longer_duration(self):
        a = f06.run_reference_scan(WORLD, request(), context())
        self.assertEqual(a["resource_estimate"]["elapsed_game_seconds"], 45)
        self.assertFalse(a["resource_estimate"]["reservation_applied"])
        partial = {x["contact_id"]: x for x in a["partial_result"]["detections"]}
        final = {x["contact_id"]: x for x in a["result"]["detections"]}
        for cid in partial:
            self.assertIn(cid, final)
            self.assertLessEqual(partial[cid]["confidence"], final[cid]["confidence"])

    def test_06_wrong_sector_is_professional_error_not_impossible(self):
        a = f06.run_reference_scan(WORLD, request(sector_id="014"), context())
        self.assertEqual(a["status"], "reference_completed")
        self.assertEqual(a["result"]["detections"], [])

    def test_07_wrong_filter_hides_contact(self):
        a = f06.run_reference_scan(
            WORLD, request(filters=["biological"], priority="biological"), context())
        self.assertEqual(a["result"]["detections"], [])

    def test_08_modes_and_interference_observe_existing_engine(self):
        active = f06.run_reference_scan(WORLD, request(), context())
        passive = f06.run_reference_scan(WORLD, request(scan_mode="passive"), context())
        a = {x["contact_id"]: x for x in active["result"]["detections"]}
        p = {x["contact_id"]: x for x in passive["result"]["detections"]}
        for cid in p:
            self.assertIn(cid, a)
            self.assertGreaterEqual(a[cid]["confidence"], p[cid]["confidence"])

    def test_09_focused_requires_known_contact_and_only_yields_it(self):
        cid = f06.sensor.contact_id("ship:imperator-training", "world-secret-1")
        r = request(range_mode="focused", target_contact_id=cid,
                    filters=["subspace"], resolution="high", scan_duration_s=90)
        self.assertEqual(f06.run_reference_scan(WORLD, r, context())["reason"],
                         "focused_target_not_known")
        result = f06.run_reference_scan(WORLD, r, context(known_contact_ids=[cid]))
        self.assertTrue(all(x["contact_id"] == cid for x in result["result"]["detections"]))

    def test_10_damaged_array_and_insufficient_resources_block_atomically(self):
        for c in [context(selected_array_state="destroyed"),
                  context(available_power=0.1),
                  context(supported_range_modes=["short"])]:
            a = f06.run_reference_scan(WORLD, request(), c)
            self.assertEqual(a["status"], "blocked")
            self.assertEqual(a["events"], [])
            self.assertEqual(a["dossier_candidates"], [])
            self.assertIsNone(a["result"])

    def test_11_not_authorized_or_station_unoccupied_blocks(self):
        for c in [context(authorization_decision="REFUSE"),
                  context(authorization_ref=""), context(occupied_station=False)]:
            a = f06.run_reference_scan(WORLD, request(), c)
            self.assertEqual(a["effects_applied"], 0)
            self.assertEqual(a["status"], "blocked")

    def test_12_disallow_unknown_filters_and_missing_identity(self):
        for r in [request(filters=["secret_truth"]),
                  request(filters=["all", "warp"]),
                  request(scan_id=""),
                  request(scan_duration_s=0)]:
            self.assertEqual(f06.run_reference_scan(WORLD, r, context())["status"], "blocked")

    def test_13_order_result_event_chain_is_causal_and_non_authoritative(self):
        a = f06.run_reference_scan(WORLD, request(), context())
        self.assertEqual(a["events"], [])
        names = [e["event_type"] for e in a["event_candidates"]]
        self.assertEqual(names, ["ACTION_STARTED", "RESULT_CREATED"])
        self.assertTrue(all(e["candidate_only"] and e["requires_core_confirmation"]
                            for e in a["event_candidates"]))
        for prev, nxt in zip(a["event_candidates"], a["event_candidates"][1:]):
            self.assertEqual(nxt["causal_refs"], [prev["event_id"]])
        self.assertEqual(a["event_candidates"][-1]["subject_refs"]["result_id"], a["result_id"])
        self.assertEqual(a["report_pending"]["status"], "not_reported")
        self.assertNotIn("REPORT_MADE", names)

    def test_14_dossier_candidate_provenance(self):
        a = f06.run_reference_scan(WORLD, request(), context())
        self.assertEqual(len(a["dossier_candidates"]), len(a["result"]["detections"]))
        dossier = a["dossier_candidates"][0]
        obs = dossier["observations"][0]
        self.assertEqual(obs["source_system"], "sensors")
        self.assertEqual(obs["provenance"]["scan_id"], "scan:6-a")
        self.assertIn("confidence", obs)

    def test_15_science_transfer_uses_known_observations_only(self):
        a = f06.run_reference_scan(WORLD, request(), context())
        d = a["dossier_candidates"][0]
        obsid = d["observations"][0]["observation_id"]
        meta = {"ship_id": "ship:academy", "created_at": "2372-03-14T10:45:00",
                "operator_id": "cadet:1", "requested_analysis": "Interpretar firma"}
        before = copy.deepcopy(d)
        transfer = f06.science_handoff_candidate(d["contact_id"], [obsid], d, meta)
        self.assertEqual(d, before)
        self.assertEqual(transfer["target_system"], "science")
        self.assertEqual(transfer["status"], "queued")
        self.assertEqual(transfer["effects_applied"], 0)
        with self.assertRaises(ValueError):
            f06.science_handoff_candidate(d["contact_id"], ["unknown"], d, meta)

    def test_16_existing_reference_contracts_compatible(self):
        def contract(path):
            return json.loads((ROOT / path).read_text(encoding="utf-8"))
        scan = contract("gameplay/ship_operations/sensor_resolution/sensor_scan_request_contract.json")
        result = contract("gameplay/ship_operations/sensor_resolution/sensor_result_contract.json")
        handoff = contract("gameplay/ship_operations/interconsole/sensor_to_science_analysis_handoff.json")
        event = contract("gameplay/ship_operations/operational_event_log/operational_event_contract.json")
        a = f06.run_reference_scan(WORLD, request(), context())
        meta = {"ship_id": "ship:academy", "created_at": "2372-03-14T10:45:00",
                "operator_id": "cadet:1", "requested_analysis": "Firma"}
        d = a["dossier_candidates"][0]
        t = f06.science_handoff_candidate(d["contact_id"],
                                         [d["observations"][0]["observation_id"]], d, meta)
        self.assertTrue(set(scan["required"]).issubset(request()))
        self.assertTrue(set(result["required"]).issubset(a["result"]))
        self.assertTrue(set(handoff["required"]).issubset(t))
        self.assertTrue(set(event["required"]).issubset(a["event_candidates"][0]))
        self.assertEqual(t["included_observation_ids"],
                         [d["observations"][0]["observation_id"]])


    def test_17_player_does_not_learn_undetected_entity_count(self):
        a = f06.run_reference_scan(WORLD, request(filters=["biological"]), context())
        self.assertEqual(a["result"]["summary"], {"contacts_detected": 0})
        self.assertEqual(a["partial_result"]["summary"], {"contacts_detected": 0})
        self.assertNotIn("entities_in_scope", json.dumps(a))
        self.assertNotIn("signatures_evaluated", json.dumps(a))

    def test_18_invalid_inputs_refused_without_mutation(self):
        for r in [request(priority=[]), request(filters=[[]])]:
            a = f06.run_reference_scan(WORLD, r, context())
            self.assertEqual(a["status"], "blocked")
            self.assertEqual(a["events"], [])
        a = f06.run_reference_scan(WORLD, request(), context(available_power="NaN-payload"))
        self.assertEqual(a["status"], "blocked")
        regular = f06.run_reference_scan(WORLD, request(), context())
        d = regular["dossier_candidates"][0]
        with self.assertRaisesRegex(ValueError, "invalid_handoff_priority"):
            f06.science_handoff_candidate(
                d["contact_id"], [d["observations"][0]["observation_id"]], d,
                {"ship_id": "ship:academy", "created_at": "2372-03-14T10:45:00",
                 "operator_id": "cadet:1", "requested_analysis": "Interpretar",
                 "priority": "forged_priority"}
            )


    def test_19_nonfinite_numbers_and_booleans_rejected(self):
        for bad in [float("nan"), float("inf"), -float("inf"), True]:
            for r, cx in (
                (request(scan_duration_s=bad), context()),
                (request(origin_position_au=[bad, 0, 0]), context()),
                (request(sensor_profile={"capability": bad, "power": 1, "integrity": 1}), context()),
                (request(), context(available_power=bad)),
            ):
                self.assertEqual(f06.run_reference_scan(WORLD, r, cx)["status"], "blocked")

    def test_20_binding_not_self_certifying_authorization(self):
        for cx in (
            context(authorization_binding={}),
            context(current_tick=110),
            context(state_revision=8),
            context(station_id="station:elsewhere"),
            context(ship_id="ship:other"),
        ):
            a = f06.run_reference_scan(WORLD, request(), cx)
            self.assertEqual(a["status"], "blocked")
            self.assertEqual(a["reason"], "authorization_binding_invalid_or_stale")
        self.assertEqual(f06.run_reference_scan(
            WORLD, request(operator_id="attacker"), context())["status"], "blocked")

    def test_21_legacy_engine_cannot_export_undetected_counts(self):
        raw = f06.sensor.resolve_scan(WORLD, request(filters=["biological"],
                                                    priority="biological"))
        self.assertEqual(raw["summary"], {"contacts_detected": 0})
        self.assertNotIn("entities_in_scope", json.dumps(raw))
        self.assertNotIn("signatures_evaluated", json.dumps(raw))

    def test_22_bad_world_rejected_without_partial_events(self):
        malformed = copy.deepcopy(WORLD)
        malformed["entities"][0]["signatures"][0]["detectability_modifiers"]["masking"] = float("nan")
        for world in [malformed, {"entities": None}, {"entities": [None]}, None]:
            answer = f06.run_reference_scan(world, request(), context())
            self.assertEqual(answer["status"], "blocked")
            self.assertEqual(answer["events"], [])
            self.assertEqual(answer["event_candidates"], [])

    def test_23_scan_does_not_commit_order_or_report(self):
        outcome = f06.run_reference_scan(WORLD, request(), context())
        self.assertEqual(outcome["events"], [])
        self.assertEqual(outcome["effects_applied"], 0)
        self.assertFalse(outcome["authoritative"])
        self.assertNotIn("ACTION_COMPLETED",
                         [x["event_type"] for x in outcome["event_candidates"]])
        self.assertNotIn("REPORT_MADE",
                         [x["event_type"] for x in outcome["event_candidates"]])


    def test_24_nontext_identifiers_are_blocked_before_hashing(self):
        for field in ("scan_id", "observer_id", "operator_id"):
            for invalid in (True, 42, ["forged"], {"id": "forged"}):
                with self.subTest(field=field, invalid=repr(invalid)):
                    answer = f06.run_reference_scan(
                        WORLD, request(**{field: invalid}), context())
                    self.assertEqual(answer["status"], "blocked")
                    self.assertEqual(answer["events"], [])
                    self.assertEqual(answer["event_candidates"], [])

    def test_25_boolean_binding_revision_is_not_integer_one(self):
        cx = context()
        cx["state_revision"] = 1
        cx["authorization_binding"] = {
            **cx["authorization_binding"], "state_revision": True,
        }
        answer = f06.run_reference_scan(WORLD, request(), cx)
        self.assertEqual(answer["status"], "blocked")
        self.assertEqual(answer["reason"], "authorization_binding_invalid_or_stale")

    def test_26_focused_known_contacts_must_be_a_collection(self):
        cid = f06.sensor.contact_id("ship:imperator-training", "world-secret-1")
        r = request(range_mode="focused", target_contact_id=cid)
        for malformed in (cid, f"prefix:{cid}", {"id": cid}, True):
            with self.subTest(known=repr(malformed)):
                answer = f06.run_reference_scan(
                    WORLD, r, context(known_contact_ids=malformed))
                self.assertEqual(answer["status"], "blocked")
                self.assertEqual(answer["reason"], "focused_target_not_known")

    def test_27_nontext_campaign_time_and_ship_are_blocked(self):
        for changed in ({"campaign_time": ["stolen"]}, {"ship_id": True}):
            answer = f06.run_reference_scan(WORLD, request(), context(**changed))
            self.assertEqual(answer["status"], "blocked")
            self.assertEqual(answer["events"], [])


if __name__ == "__main__":
    unittest.main()
