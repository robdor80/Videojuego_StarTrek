#!/usr/bin/env python3
"""LORE-03E: audit of cross-package editorial references only. No runtime mutation."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
A = "mundo/lore/historical_events/lore03_a_chronology_index_v0.1.json"
LEGACY = "mundo/lore/diplomacy/historical_events_v0.1.json"
B = "mundo/lore/conflicts/lore03b_dossier_index_v0.1.json"
C = "mundo/lore/historical_events/lore03c_memory_casebook_v0.1.json"
PATTERNS = "mundo/lore/historical_events/lore03c_institutional_patterns_v0.1.json"
D = "proyecto/docs/roadmap/lore_03_d/D_escenarios_documentales_v0.1.json"
DOCS = "proyecto/docs/roadmap/lore_03_e"
SOURCE = "mundo/sources/source_registry/source_registry.json"
REQUIRED = [
    "proyecto/docs/decisions/playable_eras.md",
    "proyecto/docs/decisions/campaign_continuity.md",
    "proyecto/docs/decisions/lore03a_valhalla_2383_academy.md",
    "mundo/lore/historical_events/historical_event_contract.json",
    "mundo/lore/conflicts/conflict_definition_contract.json",
    "sistemas/gameplay/conflict/conflict_war_index_v0.1.json",
    "sistemas/ai/memory/character_memory_contract.json",
    "sistemas/gameplay/knowledge/character_knowledge_state.json",
    "sistemas/gameplay/consequences/world_event_consequence_contract.json",
    "sistemas/gameplay/persistence/persistent_state_roundtrip_contract.json",
    "sistemas/universe/generation/persistent_entity_identity_contract.json",
    "sistemas/gameplay/simulation/professional_offscreen_simulation_contract.json",
    "proyecto/docs/roadmap/lore_03_master_plan_v0.1.md",
]
for phase, names in {
    "b": ["B01_clasificacion_y_decisiones.md","B02_grandes_guerras_historicas.md","B03_crisis_regionales_y_politicas.md","B04_diplomacia_alianzas_y_paz.md","B05_horizonte_2383_consecuencias.md","B06_conflictos_emergentes_documental.md","B07_integracion_y_migracion_diferida.md","B08_auditoria_y_criterios.md"],
    "c": ["C01_auditoria_arquitectura.md","C02_biografias_consecuencias.md","C03_conocimiento_recuerdos_secretos.md","C04_memoria_institucional_colectiva.md","C05_relaciones_veteranos_familias.md","C06_legado_cientifico_profesional.md","C07_integracion_npc_lod_ia.md","C08_auditoria_pruebas_cierre.md"],
    "d": ["D01_auditoria_y_arquitectura.md","D02_estado_inicial_corte_temporal.md","D03_divergencia_futuro_abierto.md","D04_autonomia_galactica.md","D05_causalidad_y_consecuencias.md","D06_npc_naves_organizaciones.md","D07_historia_por_partida.md","D08_auditoria_y_cierre.md"],
}.items():
    REQUIRED += [f"proyecto/docs/roadmap/lore_03_{phase}/{n}" for n in names]
REQUIRED += [f"{DOCS}/E0{i}_{s}.md" for i,s in enumerate([
    "integridad_estructural","cronologia_canon","personajes_naves",
    "integracion_lore01_lore02","universo_dinamico","contratos_persistencia",
    "pruebas_y_regresiones","dictamen_y_cierre"], start=1)]
REQUIRED += [f"{DOCS}/README.md",f"{DOCS}/matriz_transversal.md"]

class CrossAuditError(AssertionError):
    pass

def need(ok, reason):
    if not ok:
        raise CrossAuditError(reason)

def read_json(path, root=ROOT):
    return json.loads((root/path).read_text(encoding="utf-8"))

def event_map(legacy, a):
    inherited=legacy["events"]
    anchors=a["additional_historical_anchors"]
    left=[e["event_id"] for e in inherited]
    right=[e["event_id"] for e in anchors]
    need(len(left)==40 and len(set(left))==40, "LORE-01D event count/IDs")
    need(len(right)==26 and len(set(right))==26, "LORE-03A anchor count/IDs")
    need(not(set(left)&set(right)), "Historical ID duplicated across LORE-01D/03A")
    need(set(a["reused_catalogues"][0]["retained_event_ids"])==set(left),
         "Inherited historical references lost")
    return set(left)|set(right)

def validate_dossiers(index, all_events, root=ROOT):
    need(index["status"]=="COMPLETE_DOCUMENTARY" and
         index["expected_dossiers"]==22 and len(index["dossiers"])==22,
         "B dossier coverage/status")
    ids=[d["conflict_id"] for d in index["dossiers"]]
    need(len(set(ids))==len(ids), "Duplicate conflict ID")
    for item in index["dossiers"]:
        path=item["ref"]
        need((root/path).is_file(), "Missing B dossier: "+path)
        need((root/item["document_ref"]).is_file(), "Missing B note")
        d=read_json(path,root)
        need(d["conflict_id"]==item["conflict_id"], "Mismatch dossier identity")
        need(set(d["major_event_refs"])<=all_events,"Dossier references absent event")
        need(d["world_state_authority"]=="CoreRPG_ONLY" and
             d["auto_bootstrap_future"] is False and
             d["runtime_state_mutation"] is False, "Live/unauthorized B dossier")
    return set(ids)

def validate_memories(casebook, patterns, events, conflicts):
    need(casebook["status"]=="COMPLETE_DOCUMENTARY" and
         len(casebook["cases"])==13 and len(patterns["patterns"])==6,
         "Memory case/pattern coverage")
    need(casebook["world_state_authority"]=="CoreRPG_ONLY" and
         casebook["gameplay_activated"] is False, "Memory controls WorldState")
    ids=[q["case_id"] for q in casebook["cases"]]
    need(len(set(ids))==len(ids),"Duplicate memory example")
    for case in casebook["cases"]:
        need(case["event_ref"] in events and case["conflict_ref"] in conflicts,
             "Memory case historical reference missing")
        need(case["case_kind"]=="DOCUMENTARY_HYPOTHETICAL_NOT_INSTANTIATED"
             and case["runtime_state_mutation"] is False,
             "Illustrative memory became a live NPC")
    for p in patterns["patterns"]:
        need(p["event_ref"] in events,"Institutional pattern event missing")
        need(p["runtime_state_mutation"] is False and
             p["requires_authorized_institutional_event"] is True,
             "Institutional pattern bypasses authority")

def validate_boundary(a, d, eras, status):
    w=a["reference_window"]
    need(a["status"]=="COMPLETE_DOCUMENTARY" and
         (w["start_year"],w["end_year"])==(2364,2383), "Invalid A baseline")
    need(w["campaign_start_year_proposed"]==2383 and
         w["expected_ensign_year"]==2387 and
         w["academy_duration_years"]==4 and
         w["campaign_start_date"] is None and
         w["date_is_author_approved"] is False, "2383 / 2387 or precise D fabricated")
    need(all(eras[era]["playable"] is (era=="tng_ds9_voyager")
             for era in ("pike","kirk","tng_ds9_voyager")), "Incorrect selectable eras")
    need(d["status"]=="COMPLETE_DOCUMENTARY" and
         d["campaign_start_year_proposed"]==2383 and
         d["campaign_start_exact_date"] is None and len(d["scenarios"])==35,
         "D baseline/scenario coverage")
    need(d["world_state_authority"]=="CoreRPG_ONLY" and
         all(d[x] is False for x in ("gameplay_activated","auto_schedules_future_canon",
               "creates_runtime_events","playable_time_travel")),
         "Automatic future or runtime authority leaked")
    ids=[s["id"] for s in d["scenarios"]]
    need(len(set(ids))==35, "Duplicate D scenario IDs")
    need("| E — Auditoría global | ⬜ TODO |" in status,
         "E must remain TODO until author-approved fusion/admin update")
    return len(ids)

def validate(root=ROOT):
    for path in REQUIRED+[A,B,C,PATTERNS,D,LEGACY,SOURCE,"CONTENT_STATUS.md"]:
        need((root/path).is_file(),"Missing cross-phase document: "+path)
    a,b,c,p,d=[read_json(f,root) for f in (A,B,C,PATTERNS,D)]
    events=event_map(read_json(LEGACY,root),a)
    conflicts=validate_dossiers(b,events,root)
    validate_memories(c,p,events,conflicts)
    eras={x:read_json(f"sistemas/universe/chronology/era_profiles/{x}/era_profile.json",root)
          for x in ("pike","kirk","tng_ds9_voyager")}
    text=(root/"CONTENT_STATUS.md").read_text(encoding="utf-8")
    count=validate_boundary(a,d,eras,text)
    need("Only one playable era" in (root/"mundo/sources/canon_policy.md").read_text(encoding="utf-8"),
         "Canon policy lost single-era priority")
    for phase in ["A — Cronología y acontecimientos", "B — Conflictos, guerras y crisis",
                  "C — Consecuencias y memoria histórica", "D — Continuidad/divergencia"]:
        need(f"| {phase} | ✅ COMPLETE |" in text, "LORE-03 predecessor incomplete: "+phase)
    return {"status":"AUDIT_DOCUMENTARY_IN_REVIEW","events":len(events),
            "conflicts":len(conflicts),"memory_cases":len(c["cases"]),
            "institutional_patterns":len(p["patterns"]),"d_scenarios":count,
            "runtime_verified":False,"merge_authorized":False}
if __name__=="__main__":
    print("LORE-03E EDITORIAL CROSS-PHASE AUDIT:",validate())
