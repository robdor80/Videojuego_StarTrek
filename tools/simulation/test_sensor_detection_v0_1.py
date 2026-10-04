#!/usr/bin/env python3
import importlib.util
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "resolve_sensor_scan.py"
spec = importlib.util.spec_from_file_location("sensor_resolution", MODULE_PATH)
sensor = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = sensor
spec.loader.exec_module(sensor)


def make_entity(
    entity_id,
    entity_type,
    position,
    *,
    strength="strong",
    signature_type="subspace",
    hidden=True,
    interference=False,
):
    return {
        "entity_id": entity_id,
        "entity_type": entity_type,
        "temporal_state": {"active": True},
        "spatial_state": {
            "sector_id": "041",
            "system_id": "sys:test",
            "position": {"unit": "AU", "xyz": position},
        },
        "ground_truth": {
            "classification": "subspace_distortion" if entity_type == "anomaly" else "unidentified_vessel",
            "properties": {"diameter_km": 18240},
            "hidden_properties": {
                "precise_nature": {
                    "value": "subspace_fracture",
                    "minimum_resolution": "high",
                    "preferred_filter": "subspace",
                }
            } if hidden else {},
        },
        "signatures": [{
            "signature_id": "sig:" + entity_id,
            "signature_type": signature_type,
            "strength": strength,
            "variability": "stable",
            "emission_mode": "passive",
            "source_property": "test",
            "detectability_modifiers": {"masking": 0.10 if interference else 0.0},
        }],
        "environmental_modifiers": {
            "masking": ["subspace_noise"] if interference else [],
            "local_interference": [],
        },
    }


WORLD = {
    "entities": [
        make_entity("e1", "anomaly", [2.0, 0.0, 0.0]),
        make_entity(
            "e2", "starship", [5.0, 0.0, 0.0],
            strength="moderate", signature_type="warp", hidden=False
        ),
        make_entity(
            "e3", "anomaly", [10.0, 0.0, 0.0],
            strength="moderate", interference=True
        ),
    ]
}


def request(**overrides):
    value = {
        "scan_id": "scan:test",
        "observer_id": "ship:academy",
        "operator_id": "cadet:dorado",
        "origin_position_au": [0.0, 0.0, 0.0],
        "sector_id": "041",
        "system_id": "sys:test",
        "range_mode": "long",
        "scan_mode": "active",
        "resolution": "standard",
        "filters": ["all"],
        "priority": "subspace",
        "scan_duration_s": 10,
        "sensor_profile": {
            "capability": 0.85,
            "power": 1.0,
            "integrity": 1.0
        },
    }
    value.update(overrides)
    return value


class SensorResolutionTests(unittest.TestCase):
    def test_same_input_is_deterministic(self):
        self.assertEqual(
            sensor.resolve_scan(WORLD, request()),
            sensor.resolve_scan(WORLD, request()),
        )

    def test_player_result_does_not_leak_entity_ids(self):
        result = sensor.resolve_scan(WORLD, request())
        rendered = str(result)
        self.assertNotIn("entity_id", rendered)
        self.assertNotIn("ground_truth", rendered)

    def test_high_focused_scan_can_reveal_eligible_hidden_truth(self):
        result = sensor.resolve_scan(
            WORLD,
            request(
                range_mode="focused",
                resolution="high",
                filters=["subspace"],
                priority="subspace",
                scan_duration_s=60,
            ),
        )
        detection = next(
            d for d in result["detections"] if d["distance_au"] == 2.0
        )
        self.assertEqual(detection["resolution_state"], "resolved")
        self.assertEqual(
            detection["observed"]["resolved_hidden_properties"]["precise_nature"],
            "subspace_fracture",
        )

    def test_standard_resolution_does_not_reveal_high_resolution_hidden_truth(self):
        result = sensor.resolve_scan(
            WORLD,
            request(
                filters=["subspace"],
                priority="subspace",
                resolution="standard"
            ),
        )
        detection = next(
            d for d in result["detections"] if d["distance_au"] == 2.0
        )
        self.assertNotIn(
            "resolved_hidden_properties",
            detection["observed"]
        )

    def test_wrong_filter_hides_subspace_only_contact(self):
        result = sensor.resolve_scan(
            WORLD,
            request(
                filters=["biological"],
                priority="biological"
            ),
        )
        self.assertFalse(
            any(d["distance_au"] == 2.0 for d in result["detections"])
        )

    def test_short_range_excludes_distant_contacts(self):
        result = sensor.resolve_scan(
            WORLD,
            request(range_mode="short")
        )
        self.assertTrue(
            all(d["distance_au"] <= 2.0 for d in result["detections"])
        )

    def test_interference_reduces_detection_score(self):
        normalized = sensor.normalized_request(request())
        clean = sensor.score_signature(
            WORLD["entities"][0],
            WORLD["entities"][0]["signatures"][0],
            normalized,
        )[0]
        noisy = sensor.score_signature(
            WORLD["entities"][2],
            WORLD["entities"][2]["signatures"][0],
            normalized,
        )[0]
        self.assertGreater(clean, noisy)

    def test_active_scan_outperforms_passive_for_same_signature(self):
        entity = WORLD["entities"][0]
        signature = entity["signatures"][0]
        active = sensor.score_signature(
            entity,
            signature,
            sensor.normalized_request(request(scan_mode="active"))
        )[0]
        passive = sensor.score_signature(
            entity,
            signature,
            sensor.normalized_request(request(scan_mode="passive"))
        )[0]
        self.assertGreater(active, passive)


if __name__ == "__main__":
    unittest.main()
