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
    "README.md", "DECISIONES_RATIFICADAS_20261123.md", "A01_AUDITORIA_PRECEDENCIAS.md", "A02_ENTERPRISE_D_VALHALLA.md",
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
    "C11_BIOGRAFIA_PROTAGONISTA.md": ("GAME_ADDITION", "Naveen Rise", "T'Ralis", "piano", "Suus Mahna"),
    "C12_LEGENDARIOS_ARCOS.md": ("vicealmirante", "Data", "Sisko", "2386", "comandante", "2393"),
    "C14_HISTORIA_VALHALLA.md": ("Galaxy", "flujo cuántico", "2387", "Defiant"),
    "C15_PROLOGO_ACADEMIA.md": ("Janeway", "Picard", "Riker", "F10"),
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
    identity = a.get("identity", {})
    parents = identity.get("parentage", {})
    if identity.get("surname") != "Rise" or identity.get("given_name_customizable") is not True:
        issues.append("fixed Rise surname and configurable given name")
    if identity.get("display_name_policy") != "CUSTOM_GIVEN_NAME_PLUS_RISE":
        issues.append("display name policy")
    if parents.get("mother", {}).get("species") != "vulcan" or parents.get("father", {}).get("ancestor") != "khan_noonien_singh":
        issues.append("parentage")
    if parents.get("mother", {}).get("name") != "T'Ralis" or parents.get("father", {}).get("name") != "Naveen Rise":
        issues.append("approved parents")
    if any(parents.get(p, {}).get("starfleet_service") is not False for p in ("mother", "father")):
        issues.append("civilian parents")
    for parent in ("mother", "father"):
        d = parents.get(parent, {}).get("death", {})
        if d.get("state") != "DECEASED_BEFORE_2383" or d.get("exact_year") is not None or d.get("protagonist_already_adult") is not True:
            issues.append("parent death temporal policy: " + parent)
    if parents.get("mother", {}).get("death", {}).get("cause") != "SUDDEN_FULMINANT_CARDIAC_DISEASE" or parents.get("father", {}).get("death", {}).get("cause") != "AGE_RELATED_NATURAL":
        issues.append("parent death causes")
    if a.get("lineage") != [] or a.get("lineage_policy", {}).get("verified") is not True or a.get("lineage_policy", {}).get("intermediate_ancestors") != "NOT_NAMED_NOT_REQUIRED":
        issues.append("no invented genealogy")
    if a.get("teachers") != [] or a.get("teachers_policy") != "NAMES_NOT_REQUIRED_BY_GAME":
        issues.append("no invented martial teachers")
    skills = a.get("skills", {})
    if skills.get("music") != ["piano"]:
        issues.append("piano only")
    if set(skills.get("martial", [])) != {"kung_fu", "karate", "aikido", "suus_mahna"} or skills.get("martial_mastery") != "ADVANCED_MASTER_ALL_FOUR" or skills.get("associated_blade_weapons_mastery") != "ADVANCED":
        issues.append("four arts and associated blades mastery")
    if len(a.get("genetic_traits", [])) != 9 or len(set(a["genetic_traits"])) != 9 or a.get("genetic_traits_require_starfleet_evaluation") is not True:
        issues.append("nine inherited traits and Flota evaluation")
    if a.get("blood_therapeutic_scope") != "INVESTIGABLE_NOT_UNIVERSAL_CURE_CONSENT_REQUIRED":
        issues.append("blood non-universal therapeutic scope")
    if a.get("academy_vocation", {}).get("since_childhood") is not True or a.get("academy_vocation", {}).get("entry_age_45_planned_voluntary") is not True:
        issues.append("lifetime Starfleet vocation")
    personality = a.get("initial_personality", {})
    if personality.get("player_choices_unrestricted") is not True or personality.get("mutable_by_gameplay") is not True or personality.get("no_genetic_moral_determinism") is not True:
        issues.append("player agency and evolving personality")
    if any(k in (root / OP / "C11_BIOGRAFIA_PROTAGONISTA.md").read_text(encoding="utf-8") for k in ("Naveen Vale", "Sorvek", "Mara Calder", "laúd vulcano")):
        issues.append("discarded biography details")
    intro = (root / OP / "C15_PROLOGO_ACADEMIA.md").read_text(encoding="utf-8")
    if "**PICARD:**" in intro or "**JANEWAY:**" in intro or "| S0 " in intro:
        issues.append("unapproved intro screenplay restored")
    val_doc = (root / OP / "C14_HISTORIA_VALHALLA.md").read_text(encoding="utf-8")
    if "| VAL-N" in val_doc:
        issues.append("invented Valhalla missions restored")
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
    print(f"PASS: {len(DOCUMENTS)} documentos, 20 semillas no aprobadas, 12 dossiers, 16 VAL-TEC, S04/Valhalla intactos.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
