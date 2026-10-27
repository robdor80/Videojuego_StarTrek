#!/usr/bin/env python3
"""LORE-01 A.1: comprobar integridad de 25 guías culturales de IA.

Valida estructura, referencias, gates, no estereotipos y trazabilidad.
NO prueba texto generado por modelos, canon escena a escena ni CoreRPG/UE5.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SUB = Path("mundo/lore/cultures/ai_behavior")
OLD = {"human","vulcan","andorian","aenar","tellarite","klingon","romulan",
       "cardassian","bajoran","ferengi","trill","betazoid","changeling","vorta","jem_hadar"}
NEW = {"bolian","benzite","el_aurian","breen","pakled"}
DELTA = {"kazon","ocampan","talaxian","vidiian","hirogen"}
ALL = OLD | NEW | DELTA
STRENGTH = {"STRONG_CONTEXTUAL_NORMS","CONTEXTUAL_NORMS","LIMITED_CONTEXTUAL",
            "UNKNOWN_NO_DEFAULT","NO_SPECIES_PRIOR"}
GUIDE_KEYS = {"communication_es","emotional_expression_es","disagreement_and_conflict_es",
              "authority_and_duty_es","relationships_and_daily_life_es"}
REQUIRED = {"schema_version","profile_id","species_index_key","display_name_es",
            "status","content_gate","culture_bindings","source_basis","prior_strength",
            "interpretation_scope_es","conditional_guidance","variation_axes_es",
            "distinct_individual_outcomes_es","anti_stereotype_warnings_es",
            "era_guard_es","ai_application"}
PROHIBITED_DERIVATION = {"hostilidad","honestidad","profesión","rango","ideología",
                         "fe","relación","secreto","culpabilidad","moralidad"}

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate_profile(profile: dict, species_id: str, sources: dict, root: Path = ROOT) -> list[str]:
    errors = []
    def fail(msg):
        errors.append(f"{species_id}: {msg}")
    if not REQUIRED.issubset(profile.keys()):
        fail("faltan campos de contrato: " + str(sorted(REQUIRED - set(profile))))
    if profile.get("species_index_key") != species_id:
        fail("species_index_key no coincide")
    if profile.get("profile_id") != f"lore01_a1_{species_id}_behavior":
        fail("profile_id incorrecto")
    if profile.get("schema_version") != "0.1.0":
        fail("versión no soportada")
    if profile.get("status") != "AUTHORING_CULTURAL_AI_GUIDANCE_NOT_PERSONALITY":
        fail("se presenta como personalidad/código de ejecución")
    gate = profile.get("content_gate")
    expected = "DLC_DELTA_ONLY" if species_id in DELTA else (
        "MAIN_GAME_WITH_STRICT_HISTORICAL_CAUSALITY" if species_id == "aenar" else "MAIN_GAME"
    )
    if gate != expected:
        fail("gate de contenido o cautela temporal incorrecta")
    if profile.get("prior_strength") not in STRENGTH:
        fail("prior_strength inválido")
    if species_id in {"aenar","breen","pakled"} and profile.get("prior_strength") != "UNKNOWN_NO_DEFAULT":
        fail("una especie poco documentada recibe tendencia colectiva")
    if species_id == "human" and profile.get("prior_strength") != "NO_SPECIES_PRIOR":
        fail("humanos no pueden recibir cultura universal")
    b = profile.get("culture_bindings", {})
    if b.get("species_auto_attachment") is not False:
        fail("autoadjuntar cultura por especie está prohibido")
    if b.get("allowed_for_other_species_when_socialized") is not True:
        fail("prohíbe culturas por crianza intercultural")
    if b.get("multiple_cultures_can_coexist") is not True:
        fail("prohíbe culturas mixtas")
    if b.get("attachment_policy") != "REQUIRES_EXPLICIT_CULTURE_REF_OR_DOCUMENTED_SOCIALIZATION":
        fail("no exige socialización demostrada")
    cref = b.get("profile_ref")
    if not isinstance(cref, str) or not (root / cref).is_file():
        fail("ruta cultural inexistente")
    elif b.get("profile_subkey") is not None:
        try:
            ctx = read_json(root / cref)
            if b["profile_subkey"] not in ctx.get("profiles", {}):
                fail("subperfil cultural inexistente")
        except (OSError, ValueError):
            fail("perfil cultural ilegible")
    s = profile.get("source_basis", {})
    ledger_ref = s.get("ledger_ref")
    if ledger_ref != f"mundo/lore/species/evidence/{species_id}_v0.2.json":
        fail("ledger_ref inválido")
    else:
        try:
            ledger = read_json(root / ledger_ref)
            if ledger.get("species_id") != species_id:
                fail("ledger ID no coincide")
            ledger_sources = {e["source_id"] for e in ledger.get("evidence", [])}
            anchors = s.get("anchors", [])
            if not isinstance(anchors, list) or len(anchors) < 2 or len(set(anchors)) != len(anchors):
                fail("anclajes de fuente insuficientes o duplicados")
            else:
                for src in anchors:
                    if src not in sources:
                        fail("fuente no registrada " + str(src))
                    if src not in ledger_sources:
                        fail("fuente no vinculada al expediente previo " + str(src))
                    if str(src).startswith(("ENT_","PIC_","DIS_")):
                        fail("fuente ajena al alcance TNG/DS9/VOY " + str(src))
        except (OSError, ValueError, TypeError, KeyError):
            fail("ledger ilegible")
    if s.get("research_status") != "EPISODE_LEVEL_ANCHORS_NOT_SCENE_BY_SCENE_VERIFIED":
        fail("grado de verificación engañoso")
    guidance = profile.get("conditional_guidance", {})
    if set(guidance) != GUIDE_KEYS:
        fail("dimensiones de comportamiento faltantes o inesperadas")
    for k in GUIDE_KEYS:
        lines = guidance.get(k, [])
        if not isinstance(lines, list) or len(lines) < 2 or any(len(x.strip()) < 25 for x in lines if isinstance(x, str)):
            fail(f"{k} debe aportar dos observaciones diferenciadas")
    for name,minimum in (("variation_axes_es",4),("distinct_individual_outcomes_es",2),("anti_stereotype_warnings_es",2)):
        v = profile.get(name, [])
        if not isinstance(v,list) or len(v) < minimum:
            fail(f"{name}: falta variación/contraste")
    ai = profile.get("ai_application", {})
    expected_ai = {
        "character_personality_source": "PERSISTENT_PERSONAL_PROFILE_NOT_SPECIES",
        "may_use_only_if_relevant_culture_confirmed": True,
        "no_default_trait_probabilities": True,
        "no_generated_personality_scores": True,
        "decision_authority": "CoreRPG / estado persistente",
        "dialogue_authority": "AI_INTERPRETATION_ONLY"
    }
    for key,value in expected_ai.items():
        if ai.get(key) != value:
            fail(f"regla IA inválida: {key}")
    if not PROHIBITED_DERIVATION.issubset(set(ai.get("invalid_inferences",[]))):
        fail("faltan prohibiciones de inferencia racial")
    return errors

def validate_repo(root: Path = ROOT) -> list[str]:
    errors=[]
    source_json = read_json(root / "mundo/sources/source_registry/source_registry.json")
    sources = {x["source_id"]:x for x in source_json["sources"]}
    if len(sources) != len(source_json["sources"]):
        errors.append("fuentes duplicadas")
    index = read_json(root / SUB / "species_behavior_index_v0.1.json")
    rows=index.get("profiles",[])
    ids={x["species_id"] for x in rows}
    if ids != ALL or len(rows) != 25:
        errors.append("índice: faltan o sobran perfiles")
    if index.get("no_personality_by_species") is not True or index.get("species_is_discovery_index_only") is not True:
        errors.append("índice: confunde especie con personalidad")
    if (index.get("count_main_game"),index.get("count_delta_dlc")) != (20,5):
        errors.append("índice: clasificación DLC incorrecta")
    found=set()
    for species_id in sorted(ALL):
        profile_path=root/SUB/"profiles"/f"{species_id}_behavior_v0.1.json"
        if not profile_path.is_file():
            errors.append(f"falta {species_id}")
            continue
        found.add(species_id)
        try:
            profile=read_json(profile_path)
            errors.extend(validate_profile(profile,species_id,sources,root))
        except (OSError,ValueError,TypeError,KeyError) as ex:
            errors.append(f"{species_id}: JSON inválido {ex}")
        row=next((x for x in rows if x["species_id"]==species_id),None)
        if row is not None:
            if row["profile_ref"] != str(profile_path.relative_to(root)):
                errors.append(f"{species_id}: vínculo índice equivocado")
            expected_gate="DLC_DELTA_ONLY" if species_id in DELTA else "MAIN_GAME"
            if row.get("content_gate") != expected_gate:
                errors.append(f"{species_id}: gate índice incorrecto")
    actual={p.name.removesuffix("_behavior_v0.1.json") for p in (root/SUB/"profiles").glob("*_behavior_v0.1.json")}
    if actual != ALL:
        errors.append(f"perfiles adicionales o ausentes: {sorted(actual ^ ALL)}")
    contract=read_json(root / SUB / "behavior_context_contract_v0.1.json")
    if contract.get("no_species_auto_attach_culture") is not True or contract.get("no_species_based_personality_weights") is not True:
        errors.append("contrato permite generar personalidad desde especie")
    if contract.get("content_policy",{}).get("main_game_spawn_allowed_for_delta") is not False:
        errors.append("contrato permite spawn Delta")
    fixtures=read_json(root / SUB / "npc_dialogue_context_examples_v0.1.json")
    scenarios=fixtures.get("scenarios",[])
    if len(scenarios)<8 or not all(x.get("case_id") and x.get("species_id") in ALL and x.get("forbidden") for x in scenarios):
        errors.append("fixtures editoriales incompletos")
    return errors

if __name__=="__main__":
    errors=validate_repo()
    if errors:
        for e in errors:
            print("ERROR LORE01 A1:",e,file=sys.stderr)
        sys.exit(1)
    print("LORE-01 A.1 OK: 25 contextos, 20 principales, 5 DLC, cultura contextual y trazabilidad validada.")
