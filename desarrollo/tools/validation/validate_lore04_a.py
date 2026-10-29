#!/usr/bin/env python3
"""LORE-04A: documentary integrity only, never a WorldState/UE5 runtime test."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DIR = "proyecto/docs/roadmap/lore_04_a/"
REGISTRY = "mundo/sources/source_registry/source_registry.json"
EVIDENCE = DIR + "lore04a_evidence_ledger_v0.1.json"
SCENARIOS = DIR + "lore04a_scenarios_v0.1.json"
INVARIANTS = "desarrollo/validation/consistency/lore04a_civil_society_invariants_v0.1.json"
MASTER = "proyecto/docs/roadmap/lore_04_master_plan_v0.1.md"
DOCS = {
    "A01": "A01_auditoria_reutilizacion.md",
    "A02": "A02_vida_civil_base_y_casos.md",
    "A03": "A03_educacion_profesiones_servicios.md",
    "A04": "A04_ocio_comunidades_rutinas_cotidianas.md",
    "A05": "A05_matriz_sociedades_y_diversidad.md",
    "A06": "A06_lod_rutinas_persistencia.md",
    "A07": "A07_casos_gameplay_npc.md",
    "A08": "A08_auditoria_pruebas_cierre.md",
}
REQUIRED_REUSE = {
    "sistemas/universe/generation/persistent_population_materialization_rules.json",
    "sistemas/gameplay/social/social_simulation_lod.json",
    "sistemas/gameplay/social/relationship_graph_model.json",
    "sistemas/universe/generation/settlement_infrastructure_contract.json",
    "sistemas/gameplay/economy/civilian_trade_operator_contract.json",
    "sistemas/gameplay/organizations/profiles/FEDERATION_INSTITUTIONS_v0.1.json",
}
NEEDED_TOKENS = {
    "A01": ("CoreRPG", "LORE-04", "reutiliz"),
    "A02": ("famil", "Bajor", "Ferengi", "CoreRPG"),
    "A03": ("Educación", "clínica", "Academia", "autoridad"),
    "A04": ("ocio", "horario", "social", "conocimiento"),
    "A05": ("Federación", "Klingon", "Romul", "Cardass", "Ferengi", "Bajor"),
    "A06": ("LOD", "WorldState", "CoreRPG", "fuera de pantalla"),
    "A07": ("CIV-01", "CIV-16", "CoreRPG", "conocimiento"),
    "A08": ("A01", "A08", "NO", "LORE-03", "CoreRPG"),
}
ALLOWED_CLAIM_CLASSES = {"SCREEN_CANON", "OFFICIAL_REFERENCE", "INFERRED", "GAME_ADDITION"}
REQUIRED_IDS = {"LA-E01", "LA-E02", "LA-E03", "LA-E05", "LA-E06", "LA-E07",
                "LA-E08", "LA-E09", "LA-E10", "LA-E11", "LA-E12", "LA-E13", "LA-E14"}
MANDATORY_SCENARIOS = {f"CIV-{i:02d}" for i in range(1, 17)}

def check(ok: bool, message: str):
    if not ok:
        raise AssertionError(message)

def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

def assert_doc_files(docs: dict[str, str], master: str, root=ROOT):
    check(set(docs) == set(DOCS), "Missing or extra A01–A08 package keys")
    check("LORE-04" in master and "04A" in master and "04E" in master, "Master incomplete")
    check("CoreRPG" in master and "LORE-04B" in master, "Authority/dependency not declared")
    for phase, content in docs.items():
        check(content.startswith("# LORE-04A / " + phase), "Package header mismatch " + phase)
        check(len(content.strip()) > 800, "Package underdeveloped " + phase)
        for token in NEEDED_TOKENS[phase]:
            check(token.lower() in content.lower(), f"Package {phase} missing {token}")
        check((root / (DIR + DOCS[phase])).is_file(), "Missing file " + phase)
    check((root / (DIR + "README.md")).is_file(), "Missing LORE-04A README")
    readme=(root / (DIR + "README.md")).read_text(encoding="utf-8")
    for path in DOCS.values():
        check(path in readme, "README missing package " + path)

def assert_reuse(root=ROOT):
    for path in REQUIRED_REUSE:
        check((root / path).is_file(), "Reused contract missing " + path)
    for path in ("proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md",
                 "proyecto/docs/roadmap/academy_life_final_closure_v1.0.md",
                 "proyecto/docs/decisions/lore03a_valhalla_2383_academy.md"):
        check((root / path).is_file(), "Master dependency missing " + path)
    block=(root/"proyecto/docs/roadmap/procedural_dynamic_universe_10_block_plan_v0.1.md").read_text(encoding="utf-8")
    check("READY_TO_RESUME" in block and "Block 4" in block, "Economy Block 4 state changed unexpectedly")
    academy=(root/"proyecto/docs/roadmap/academy_life_final_closure_v1.0.md").read_text(encoding="utf-8")
    check("20/20 COMPLETE" in academy, "Academy baseline changed")

def assert_evidence(ledger: dict, registry: dict):
    check(ledger.get("integration_owner", "CoreRPG") == "CoreRPG", "Wrong evidence owner")
    check(ledger.get("status") == "DOCUMENTARY_RESEARCH_WITH_SCREEN_SCENE_RECHECK_RESERVED",
          "Evidence falsely closed as full visual verification")
    check(ledger.get("source_registry_ref") == REGISTRY, "Source registry changed")
    sources=registry.get("sources", [])
    ids=[x.get("source_id") for x in sources]
    check(len(ids)==len(set(ids)) and len(ids)>=530, "Registry lost sources or contains duplicates")
    by_id={x["source_id"]:x for x in sources}
    claims=ledger.get("claims",[])
    cids=[x.get("id") for x in claims]
    check(len(claims)>=14 and len(cids)==len(set(cids)), "Evidence count or uniqueness")
    check(REQUIRED_IDS <= set(cids), "Missing key evidence claims")
    for c in claims:
        cl=c.get("classification")
        check(cl in ALLOWED_CLAIM_CLASSES, f"Bad claim class {cl}")
        check(c.get("confidence") in {"HIGH", "MEDIUM", "LOW"}, "Bad confidence " + c["id"])
        if cl=="SCREEN_CANON":
            sid=c.get("screen_source_id")
            check(sid in by_id and by_id[sid]["source_type"]=="SCREEN_CANON", "Invalid screen source")
            for sid2 in c.get("additional_screen_source_ids",[]):
                check(sid2 in by_id and by_id[sid2]["source_type"]=="SCREEN_CANON", "Invalid additional screen source")
            oid=c.get("official_source_id")
            check(oid in by_id and by_id[oid]["source_type"]=="OFFICIAL_REFERENCE",
                  "Official cross-check absent")
            check(c.get("screen_recheck")=="EPISODE_SCENE_TIMECODE_NOT_RECORDED",
                  "Scene incorrectly certified")
            check(c.get("limits"), "No limits on screen claim")
        elif cl=="OFFICIAL_REFERENCE":
            oid=c.get("official_source_id")
            check(oid in by_id and by_id[oid]["source_type"]=="OFFICIAL_REFERENCE",
                  "Official ref missing")
            check(c.get("screen_recheck")=="NOT_SCREEN_CLAIM", "Official article promoted to screen canon")
            check(c.get("limits"), "Official claim lacks limits")
        elif cl=="GAME_ADDITION":
            check(c.get("game_need") and c.get("constraints"), "Game addition lacks causal need")
            check(c.get("author_approval")=="NOT_REQUIRED_FOR_NONBINDING_TEST_SCENARIO",
                  "Unapproved world addition made binding")
        else:
            check(c.get("reasoning") and c.get("source_ids") and c.get("falsification_condition"),
                  "Inference must state premises, reasoning and invalidation")
    return by_id, {x["id"] for x in claims}

def assert_scenarios(fixture: dict, evidence_ids: set[str]):
    check(fixture.get("integration_owner")=="CoreRPG", "Bad runtime owner")
    check(fixture.get("status")=="DESIGN_FIXTURES_NOT_CORE_RUNTIME", "Runtime claim invented")
    cases=fixture.get("scenarios",[])
    ids=[s.get("scenario_id") for s in cases]
    check(len(cases)==16 and set(ids)==MANDATORY_SCENARIOS and len(ids)==len(set(ids)),
          "Missing/duplicate scenario")
    for item in cases:
        check(item.get("classification")=="GAME_ADDITION_NONBINDING_FIXTURE", "Case promoted to canon")
        check(item.get("simulation_executed") is False, "Unproven runtime claim")
        check(item.get("authority")=="CoreRPG_WorldState", "Non-CoreRPG authority")
        check(item.get("author_decision")=="NONE_FOR_TEST_HARNESS_ONLY", "Binding authored state")
        for field in ("preconditions","expected","forbidden"):
            check(isinstance(item.get(field),list) and len(item[field])>=1, "Missing " + field)
        check(set(item.get("evidence_ids",[])) <= evidence_ids, "Unknown evidence id")
    return len(cases)

def assert_invariants(inv: dict):
    check(inv.get("status")=="design_level_only_not_runtime_tested", "Runtime status falsified")
    check(inv.get("test_execution",{}).get("integration_CoreRPG_UE5")=="NOT_TESTED",
          "Runtime test falsely certified")
    check(inv.get("test_execution",{}).get("domain_cases")=="SPECIFIED_NOT_EXECUTED",
          "Domain cases falsely executed")
    cases=inv.get("cases",[])
    ids=[c.get("id") for c in cases]
    check(len(cases)>=14 and len(ids)==len(set(ids)), "Invariant count/duplicate")
    for c in cases:
        check(c.get("type") in {"positive","negative"}, "Invariant polarity")
        check(isinstance(c.get("expected"),list) and c["expected"], "Empty invariant")
    for p in inv.get("reference_docs",[])+inv.get("reuse_contracts",[]):
        check((ROOT/p).is_file(), "Invariant broken reference "+p)
    return len(cases)

def validate():
    master=(ROOT/MASTER).read_text(encoding="utf-8")
    docs={k:(ROOT/(DIR+v)).read_text(encoding="utf-8") for k,v in DOCS.items()}
    assert_doc_files(docs,master)
    assert_reuse()
    registry=load(REGISTRY)
    evidence_ids=assert_evidence(load(EVIDENCE), registry)[1]
    scenarios=assert_scenarios(load(SCENARIOS),evidence_ids)
    invariants=assert_invariants(load(INVARIANTS))
    return {"packages":len(docs),"sources":len(registry["sources"]),"claims":len(evidence_ids),
            "scenarios":scenarios,"invariants":invariants,"runtime":"NOT_TESTED"}
if __name__=="__main__":
    print("LORE-04A DOCUMENTARY VALIDATION:",validate())
