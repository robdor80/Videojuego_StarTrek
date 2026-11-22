#!/usr/bin/env python3
"""Validación documental no destructiva de Operación LORE 2026-11-22.

No comprueba, simula ni certifica CoreRPG, HOST, Unreal, IA o guardados reales.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OP = "proyecto/docs/roadmap/operacion_lore_20261122"
DOCUMENTS = (
    "README.md", "A01_AUDITORIA_PRECEDENCIAS.md", "A02_ENTERPRISE_D_VALHALLA.md",
    "A04_TECNOLOGIA_MEDICINA_CIENCIA.md", "B03_CRONOLOGIA_2383_2387.md",
    "B05_MEDICINA_CIENCIA_ESPECIES.md", "B07_INSTITUCIONES_ASTROGRAFIA.md",
    "B09_ENCICLOPEDIA_PADD.md", "C11_BIOGRAFIA_PROTAGONISTA.md",
    "C12_LEGENDARIOS_ARCOS.md", "C14_HISTORIA_VALHALLA.md",
    "C15_PROLOGO_ACADEMIA.md", "D10_AUDITORIA_CIERRE.md",
)
LEGENDARY_FILES = (
    "starfleet/jean_luc_picard_lore05b_v0.1.md",
    "starfleet/kathryn_janeway_lore05b_v0.1.md",
    "starfleet/william_t_riker_lore05b_v0.1.md",
    "starfleet/beverly_crusher_lore05b_v0.1.md",
    "starfleet/geordi_la_forge_lore05b_v0.1.md",
    "starfleet/worf_lore05b_v0.1.md",
    "starfleet/data_lore05b_v0.1.md",
    "starfleet/deanna_troi_lore05b_v0.1.md",
    "starfleet/seven_of_nine_lore05b_v0.1.md",
    "starfleet/tuvok_lore05b_v0.1.md",
    "starfleet/benjamin_sisko_lore05b_v0.1.md",
    "federation_civilians/guinan_lore05b_v0.1.md",
)
CATALOGUE = "mundo/lore/knowledge/lore_2383_enciclopedia_editorial_v1.json"
ANNEX = "sistemas/gameplay/character_creation/s04_protagonist_narrative_annex_20261122.json"
S04 = "sistemas/gameplay/character_creation/s04_fixed_protagonist_contract_v2.json"
VALHALLA = "mundo/lore/starships/individual_ships/project_valhalla_enterprise_d_v0.1.json"
LEGACY_TECH = "mundo/lore/technology/valhalla_tech_decisions_v0.1.json"
CLASSES = {"SCREEN_CANON", "OFFICIAL_REFERENCE", "INFERRED", "GAME_ADDITION"}
VISIBILITIES = {"PUBLIC_REFERENCE", "PUBLIC_HISTORICAL", "CONTEXTUAL_KNOWLEDGE", "RESTRICTED_PERSONAL", "ROLE_RESTRICTED"}
DOC_RULES = {
    "C11_BIOGRAFIA_PROTAGONISTA.md": ("GAME_ADDITION", "Naveen Vale", "T'Ralis", "CONFIGUR"),
    "C12_LEGENDARIOS_ARCOS.md": ("vicealmirante", "Data", "Sisko"),
    "C14_HISTORIA_VALHALLA.md": ("Galaxy", "condicional", "2387"),
    "C15_PROLOGO_ACADEMIA.md": ("JANEWAY", "PICARD", "ROURKE", "Sisko", "F10"),
    "B09_ENCICLOPEDIA_PADD.md": ("CoreRPG", "PADD", "permiso"),
}

def read(root: Path = ROOT) -> dict:
    paths = [CATALOGUE, ANNEX, S04, VALHALLA, LEGACY_TECH]
    return {p: json.loads((root / p).read_text(encoding="utf-8")) for p in paths}

def problems(data: dict, root: Path = ROOT) -> list[str]:
    issues: list[str] = []
    c, a, s, v, l = (data[p] for p in (CATALOGUE, ANNEX, S04, VALHALLA, LEGACY_TECH))
    docs = {f:(root / OP / f) for f in DOCUMENTS}
    for name, path in docs.items():
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            issues.append("missing/empty document " + name)
    for name, keywords in DOC_RULES.items():
        if docs[name].exists():
            content = docs[name].read_text(encoding="utf-8")
            for kw in keywords:
                if kw.lower() not in content.lower() and not (name.startswith("C11") and kw == "CONFIGUR" and "configurable" in content.lower()):
                    issues.append("doc invariant " + name + ": " + kw)
    if len(LEGENDARY_FILES) != 12 or any(not (root / "mundo/lore/characters" / p).is_file() for p in LEGENDARY_FILES):
        issues.append("12 closed legendary dossiers")
    if c.get("runtime_import_allowed") is not False or c.get("core_rpg_authority") != "EXCLUSIVE":
        issues.append("catalogue falsely owns runtime")
    if c.get("fictional_knowledge_guard") is not True:
        issues.append("catalogue missing security boundary")
    entries = c.get("records", [])
    if len(entries) != 20 or len({r.get("entry_id") for r in entries}) != len(entries):
        issues.append("catalogue count/duplicate entry IDs")
    for r in entries:
        rid = r.get("entry_id", "?")
        if not rid or not r.get("title_es") or not r.get("summary_es"):
            issues.append("catalogue missing essential field " + rid)
        if r.get("claim_class") not in CLASSES or r.get("default_visibility") not in VISIBILITIES:
            issues.append("catalogue unsupported provenance/visibility " + rid)
        if r.get("auto_materialize") is not False or not str(r.get("release_gate", "")).startswith("QUERY_CORE_"):
            issues.append("catalogue leakage/materialization gate " + rid)
        for source in r.get("source_paths", []):
            if not source or not (root / source).is_file():
                issues.append("missing source " + rid + ": " + str(source))
    if a.get("provenance") != "GAME_ADDITION" or a.get("runtime_import_allowed") is not False or a.get("must_not_override_embedded_contract_v2") is not True:
        issues.append("annex boundary")
    if a.get("identity", {}).get("public_name") != "CUSTOMIZABLE_BY_PLAYER":
        issues.append("player name locked")
    if (a.get("identity", {}).get("species_id"), a.get("identity", {}).get("age_at_academy_entry"), a.get("identity", {}).get("academy_year")) != ("human_vulcan_hybrid", 45, 2383):
        issues.append("fixed protagonist identity")
    if a.get("identity", {}).get("exact_birth_date") is not None:
        issues.append("invented precise birth date")
    parents = a.get("identity", {}).get("parentage", {})
    if parents.get("mother", {}).get("species") != "vulcan" or parents.get("father", {}).get("ancestor") != "khan_noonien_singh":
        issues.append("parentage")
    lineage = a.get("lineage", [])
    if len(lineage) != 13 or [x.get("generation") for x in lineage] != list(range(13)):
        issues.append("genealogy count/order")
    if len({x.get("name") for x in lineage}) != len(lineage):
        issues.append("duplicate ancestor names")
    dates = [x.get("birth_year_approx") for x in lineage[1:]]
    if any(not isinstance(x, int) for x in dates) or dates != sorted(set(dates)):
        issues.append("genealogical chronology")
    if a.get("identity", {}).get("parentage", {}).get("father", {}).get("name") != lineage[-1].get("name") if lineage else True:
        issues.append("lineage father mismatch")
    if len(a.get("teachers", [])) != 4:
        issues.append("teacher count")
    if s.get("contract_id") != "s04_fixed_player_protagonist" or s.get("selection", {}).get("mode") != "SINGLE_FIXED_CANONICAL_PROTAGONIST":
        issues.append("locked S04 identity changed")
    if v.get("subject", {}).get("class_id") != "galaxy" or v.get("subject", {}).get("ship_id") != "uss_enterprise_ncc_1701_d":
        issues.append("Enterprise-D identity")
    if v.get("future", {}).get("readiness_2387_guaranteed") is not False:
        issues.append("Valhalla readiness guaranteed")
    decisions = l.get("decisions", [])
    if len(decisions) != 16 or {x.get("decision_id") for x in decisions} != {f"VAL-TEC-{i:02d}" for i in range(1,17)}:
        issues.append("VAL-TEC legacy loss")
    if l.get("class_identity") != "NEW_VALHALLA_CLASS_GALAXY_INSPIRED_NOT_GALAXY_REFIT":
        issues.append("legacy tech overwritten; migration must be explicit")
    return issues

def main() -> int:
    found = problems(read())
    if found:
        for problem in found:
            print("FAIL:", problem)
        return 1
    print(f"PASS: {len(DOCUMENTS)} documentos, 20 entradas, 12 dossiers, 16 VAL-TEC, S04/Valhalla sin importación runtime.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
