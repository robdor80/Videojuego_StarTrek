#!/usr/bin/env python3
"""Prueba obligatoria F04 -> F05 -> F06 tras fusionar sus PR anteriores.

SOLO referencia: no simula Core, persistencia o UE5. Si faltan los módulos
predecesores, las pruebas DEBEN FALLAR, nunca omitirse silenciosamente.
"""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / "tools" / "validation"
sys.path.insert(0, str(VALIDATION))
from test_f06_reference import f06, request, context, WORLD


class CrossPhaseContractTests(unittest.TestCase):
    def _evaluate_chain(self, allow=True):
        from f04_reference import issue_reference_binding
        from f05_reference import assess

        station = "station:sensors"
        officer = "cadet:1"
        authority = {
            "action": "sensor_scan", "actor_active": True, "actor_fit": True,
            "safety_interlock": "none", "technical_available": True,
            "station": "sensors", "on_duty": allow, "assignment_active": True,
            "qualified": True, "actor_id": officer, "station_id": station,
            "state_revision": 7,
        }
        proof = issue_reference_binding(
            authority, actor_id=officer, action_id="sensor_scan",
            station_id=station, state_revision=7, issued_tick=90, expires_tick=110)
        if not allow:
            self.assertIsNone(proof)
            return None
        self.assertIsNotNone(proof)
        decision = assess({
            "phase": "execute", "channel": "actor",
            "authority_verdict": "allow", "appointment_active": True,
            "medical_fit": True, "knowledge_visible": True,
            "duty_active": True, "executor_qualified": True,
            "executor_authorized": True, "capability_available": True,
            "resources_available": True, "temporal_conflict": False,
            "actor_id": officer, "action_id": "sensor_scan",
            "station_id": station, "state_revision": 7, "current_tick": 100,
            "authorization_binding": proof,
        })
        self.assertEqual(decision["verdict"], "ALLOW_REFERENCE")
        self.assertFalse(decision["authoritative"])
        return {
            "source": "F05_REFERENCE", "decision": decision["verdict"],
            "actor_id": officer, "action_id": "sensor_scan",
            "station_id": station, "ship_id": "ship:academy",
            "state_revision": 7, "issued_tick": 90, "expires_tick": 110,
        }

    def test_positive_reference_only(self):
        b = self._evaluate_chain()
        outcome = f06.run_reference_scan(
            WORLD, request(), context(authorization_binding=b))
        self.assertEqual(outcome["status"], "reference_completed")
        self.assertFalse(outcome["authoritative"])
        self.assertEqual(outcome["effects_applied"], 0)
        self.assertEqual(outcome["events"], [])

    def test_denied_watch_cannot_become_sensor_permission(self):
        self.assertIsNone(self._evaluate_chain(allow=False))

    def test_stale_grant_cannot_run_scan(self):
        b = self._evaluate_chain()
        outcome = f06.run_reference_scan(
            WORLD, request(), context(authorization_binding=b, current_tick=110))
        self.assertEqual(outcome["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
