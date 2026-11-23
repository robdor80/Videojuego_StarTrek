#!/usr/bin/env python3
"""LORE-05A: auditoría documental de la identidad Enterprise-D / Proyecto Valhalla.
No modifica archivos ni WorldState; sin dependencias externas.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
IDENTITY = "mundo/lore/starships/individual_ships/project_valhalla_enterprise_d_v0.1.json"
SOURCE_SHIPS = "mundo/lore/starships/individual_ships/core_canonical_ships.json"
SOURCE_CLASSES = "mundo/lore/starships/classes/core_starship_classes.json"
DECISION = "proyecto/docs/decisions/enterprise_d_proyecto_valhalla_2380_2387_2026-11-13.md"
INDEXES = [
    "proyecto/docs/decisions/README.md",
    "mundo/lore/technology/README.md",
    "mundo/lore/starships/individual_ships/README.md",
    "proyecto/docs/roadmap/README.md",
]

def problems_for_data(payload: dict, catalogue: dict, classes: dict) -> list[str]:
    issues = []
    subj = payload.get("subject") or {}
    proj = payload.get("project") or {}
    if payload.get("decision_id") != "DEC-0020":
        issues.append("missing DEC-0020")
    if payload.get("runtime_implemented") is not False or payload.get("authoritative_world_state") != "CoreRPG_ONLY":
        issues.append("invalid authority/runtime")
    if (subj.get("ship_id"), subj.get("registry"), subj.get("class_id")) != ("uss_enterprise_ncc_1701_d", "NCC-1701-D", "galaxy"):
        issues.append("wrong ship identity")
    if subj.get("ship_is_renamed") is not False:
        issues.append("ship name must not change")
    if (proj.get("project_id"), proj.get("kind")) != ("project_valhalla", "INDIVIDUAL_SHIP_RECOVERY_RECONSTRUCTION_AND_REFIT"):
        issues.append("project cannot be ship class")
    ships = [s for s in catalogue.get("ships", []) if s.get("ship_id") == subj.get("ship_id")]
    if len(ships) != 1 or ships[0].get("class_id") != "galaxy" or ships[0].get("registry") != "NCC-1701-D":
        issues.append("core canonical identity mismatch")
    ids = {c.get("class_id") for c in classes.get("classes", [])}
    if not {"galaxy", "valhalla"}.issubset(ids):
        issues.append("legacy classes were removed")
    timeline = payload.get("chronology") or []
    by_year = {e.get("year"): e for e in timeline}
    if sorted(by_year) != [2371, 2379, 2380, 2383, 2387, 2401] or len(timeline) != len(by_year):
        issues.append("chronology missing/out of order")
    if by_year.get(2371, {}).get("provenance") != "SCREEN_CANON":
        issues.append("veridian not canon")
    if any(by_year.get(y, {}).get("provenance") != "GAME_ADDITION" for y in [2379, 2380, 2383]):
        issues.append("game additions mislabeled")
    if by_year.get(2387, {}).get("provenance") != "GAME_ADDITION_TARGET":
        issues.append("2387 cannot be canon/guaranteed")
    if by_year.get(2401, {}).get("campaign_initialization") != "NON_MANDATORY_FUTURE_TV_REFERENCE":
        issues.append("TV future must not be forced")
    academy = payload.get("academy") or {}
    if (academy.get("start_year"), academy.get("duration_years"), academy.get("graduation_year_approx")) != (2383, 4, 2387):
        issues.append("academy timing")
    if academy.get("player_assignment_automatic") is not False or academy.get("captaincy_automatic") is not False:
        issues.append("automatic career")
    od = payload.get("odyssey") or {}
    if od.get("in_service_by_2383") is not True or od.get("enterprise_f_automatically_exists") is not False:
        issues.append("odyssey/Enterprise-F constraint")
    sl = payload.get("quantum_slipstream") or {}
    if sl.get("experimental_start_year") != 2383 or sl.get("installed_on_enterprise_d_by_default") is not False:
        issues.append("quantum installation")
    future = payload.get("future") or {}
    if future.get("readiness_2387_guaranteed") is not False or future.get("syracuse_donor_required_in_2387") is not False or future.get("post_2383_screen_future_forced") is not False:
        issues.append("future cannot be guaranteed")
    return issues

def validate(root: Path = ROOT) -> list[str]:
    issues = []
    try:
        payload = json.loads((root / IDENTITY).read_text(encoding="utf-8"))
        ships = json.loads((root / SOURCE_SHIPS).read_text(encoding="utf-8"))
        classes = json.loads((root / SOURCE_CLASSES).read_text(encoding="utf-8"))
        issues.extend(problems_for_data(payload, ships, classes))
        decision = (root / DECISION).read_text(encoding="utf-8")
        for token in ("Proyecto Valhalla", "NCC-1701-D", "2383", "2387", "2401", "GAME_ADDITION", "CoreRPG"):
            if token not in decision:
                issues.append("decision missing: " + token)
        for filename in INDEXES:
            content = (root / filename).read_text(encoding="utf-8")
            if "enterprise_d_proyecto_valhalla_2380_2387_2026-11-13.md" not in content:
                issues.append("index missing decision: " + filename)
        for filename in ["proyecto/docs/roadmap/lore_05_a/A01_INVENTARIO_PRECEDENCIAS.md", "proyecto/docs/roadmap/lore_05_a/A02_CRONOLOGIA_CANON_CAMPANA.md", "proyecto/docs/roadmap/lore_05_a/A03_MATRIZ_DEUDAS_CONSUMIDORES.md", "proyecto/docs/roadmap/lore_05_a/A04_VALIDACION_Y_CIERRE.md"]:
            if not (root / filename).is_file():
                issues.append("missing report: " + filename)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        issues.append("input error: " + str(exc))
    return issues

if __name__ == "__main__":
    faults = validate()
    if faults:
        print("LORE-05A: FAIL")
        for fault in faults:
            print(" - " + fault)
        raise SystemExit(1)
    print("LORE-05A: PASS (documentary only; not runtime)")
