#!/usr/bin/env python3
"""LORE-01 B: integridad documental de civilizaciones, cronología y límites IA.

No constituye auditoría audiovisual escena a escena ni prueba de CoreRPG/UE5.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = Path("lore/factions/LORE01_B_civilizations_index_v0.1.json")
EXPECTED_IDS = {
    "united_federation_of_planets", "klingon_empire",
    "romulan_star_empire", "cardassian_union",
    "ferengi_alliance", "bajoran_provisional_government",
    "dominion", "breen_confederacy", "borg_collective",
    "maquis", "section_31", "orion_syndicate",
    "tholian_assembly", "gorn_hegemony", "tzenkethi_polity",
    "trill_symbiosis_commission",
}
DELTA = {"kazon", "ocampan", "talaxian", "vidiian", "hirogen"}
DOMAINS = {
    "identidad_historia", "gobierno_instituciones",
    "sociedad_ciudadania", "ley_justicia", "economia",
    "defensa_seguridad", "diplomacia", "conflictos_internos",
    "flota_estar", "videojuego",
}
AUTHORITY = {"SCREEN_CANON", "OFFICIAL_REFERENCE"}
SCREEN_SCOPE = ("TOS_", "TNG_", "DS9_", "VOY_", "ST1_", "ST2_",
                "ST3_", "ST4_", "ST5_", "ST6_", "ST7_", "ST8_", "ST9_", "ST10_")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_entry(entry: dict, data: dict, md: str, sources: dict) -> list[str]:
    errors = []
    cid = entry.get("civilization_id", "")
    def error(message: str) -> None:
        errors.append(f"{cid}: {message}")
    if data.get("civilization_id") != cid:
        error("ID del libro de evidencia no coincide con índice")
    if data.get("schema_version") != "0.1.0":
        error("versión de expediente no admitida")
    if data.get("authoring_status") != "DOCUMENTARY_NOT_RUNTIME":
        error("presenta contenido como runtime ejecutable")
    if data.get("core_mutations_allowed") is not False:
        error("concede mutación de estado político a contenido/IA")
    if data.get("content_scope") not in {"MAIN_GAME", "MAIN_GAME_CONTEXT_NOT_AUTOSPAWN"}:
        error("gate principal de investigación incorrecto")
    if data.get("verification_status") != "EPISODE_OR_OFFICIAL_REFERENCE_ANCHORS_NOT_SCENE_BY_SCENE_VERIFIED":
        error("afirma revisión de escenas no realizada")
    if data.get("monograph_ref") != entry.get("monograph_ref"):
        error("monografía mal vinculada")
    if len(data.get("identity_axes", [])) < 6:
        error("no separa especie, cultura, ciudadanía, organización y persona")
    domains = data.get("domains", {})
    if set(domains) != DOMAINS:
        error("faltan o sobran dominios documentales obligatorios")
    else:
        for key, value in domains.items():
            if not isinstance(value, str) or len(value.strip()) < 120:
                error("dominio insuficientemente documentado: " + key)
    if not isinstance(md, str) or len(md) < 3000:
        error("monografía ausente o demasiado breve")
    elif cid not in md or "Desconocidos" not in md:
        error("monografía no enlaza identidad o incertidumbres")
    unknowns = data.get("unknowns", [])
    if len(unknowns) < 4 or any(len(str(x)) < 15 for x in unknowns):
        error("ausencia o insuficiencia de incertidumbres expresas")
    evidence = data.get("evidence", [])
    if len(evidence) < 2:
        error("pocas anclas de evidencia")
    for i, ev in enumerate(evidence):
        source_id = ev.get("source_id")
        src = sources.get(source_id)
        if src is None:
            error(f"fuente no registrada en evidencia {i}: {source_id}")
            continue
        if src.get("source_type") not in AUTHORITY:
            error(f"fuente no apta: {source_id}")
        if ev.get("authority") != src.get("source_type"):
            error(f"autoridad discordante: {source_id}")
        if src["source_type"] == "SCREEN_CANON" and not source_id.startswith(SCREEN_SCOPE):
            error(f"episodio de serie excluida: {source_id}")
        if len(str(ev.get("claim_es", ""))) < 45:
            error(f"claim documental vago para {source_id}")
        if ev.get("verification") != "EPISODE_LEVEL_NOT_SCENE_BY_SCENE":
            error(f"certifica escena no comprobada: {source_id}")
    chronology = data.get("chronology", [])
    if not chronology:
        error("sin referencias cronológicas")
    previous = 0
    for n, item in enumerate(chronology):
        year = item.get("year")
        if not isinstance(year, int) or year < 2000 or year > 2500:
            error(f"fecha no validada en hito {n}")
        elif year < previous:
            error("hitos cronológicos no ordenados")
        else:
            previous = year
        if item.get("event_relation") != "PRE_CAMPAIGN_ONLY_IF_DATE_VALID":
            error("hito impone futuro de serie a la campaña")
        if not item.get("source_ids") or any(s not in sources for s in item["source_ids"]):
            error("hito temporal sin procedencia registrada")
    return errors


def validate_repo(root: Path = ROOT) -> list[str]:
    errors = []
    index = read_json(root / INDEX)
    rows = index.get("main_game_entries", [])
    ids = [row.get("civilization_id") for row in rows]
    if len(ids) != 16 or len(set(ids)) != 16 or set(ids) != EXPECTED_IDS:
        errors.append("Índice de 16 entidades incompleto, duplicado o alterado")
    if index.get("status") != "DOCUMENTARY_AUTHORING_NOT_INTEGRATED":
        errors.append("Índice confundido con programa ejecutable")
    if index.get("authority") != "CoreRPG_World_State_ONLY":
        errors.append("El índice no reserva autoridad de mundo a CoreRPG")
    registry = read_json(root / "sources/source_registry/source_registry.json")
    sources = {s["source_id"]: s for s in registry["sources"]}
    if len(sources) != len(registry["sources"]):
        errors.append("IDs duplicados en registro de fuentes")
    original_factions = read_json(root / "gameplay/diplomacy/major_faction_catalogue.json")["factions"]
    for row in rows:
        cid = row.get("civilization_id")
        mref, eref = row.get("monograph_ref", ""), row.get("evidence_ref", "")
        if mref != f"lore/factions/monographs/{cid}_v0.1.md" or eref != f"lore/factions/evidence/{cid}_v0.1.json":
            errors.append(f"{cid}: rutas de autoría inesperadas")
            continue
        if row.get("automatic_generation_enabled") is not False:
            errors.append(f"{cid}: generación activada antes de implementar gate")
        if row.get("availability") != "MAIN_GAME_LORE_CONTEXT":
            errors.append(f"{cid}: clasificación de ámbito incorrecta")
        if row.get("legacy_major_faction_id") != (cid if cid in original_factions else None):
            errors.append(f"{cid}: referencia al catálogo anterior incorrecta")
        try:
            data = read_json(root / eref)
            md = (root / mref).read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            errors.append(f"{cid}: archivos documentales inaccesibles: {exc}")
            continue
        errors.extend(validate_entry(row, data, md, sources))
    found_json = {p.stem.removesuffix("_v0.1") for p in (root / "lore/factions/evidence").glob("*_v0.1.json")}
    found_md = {p.stem.removesuffix("_v0.1") for p in (root / "lore/factions/monographs").glob("*_v0.1.md")}
    if found_json != EXPECTED_IDS or found_md != EXPECTED_IDS:
        errors.append("Ficheros documentales ausentes o inesperados")
    dlc = index.get("deliberately_not_main_game", [])
    if len(dlc) != 1 or set(dlc[0].get("species_ids", [])) != DELTA:
        errors.append("Cinco especies DLC Delta no protegidas en el índice")
    elif any(dlc[0].get(k) is not False for k in ("civilization_generation_enabled",
             "territory_generation_enabled", "encounter_generation_enabled")):
        errors.append("Generación no autorizada de civilizaciones Delta")
    baseline = read_json(root / "universe/generation/lore01_tng_content_availability_v0.1.json")
    if set(baseline["delta_dlc"]["species_ids"]) != DELTA or baseline["delta_dlc"]["planned_travel"]["borg_can_traverse_this_portal_toward_alpha"] is not False:
        errors.append("Incompatible con reserva aprobada en LORE-01 A")
    borg = index.get("borg_exception", {})
    if borg.get("classification") != "TECHNO_COLLECTIVE_NOT_BIOLOGICAL_SPECIES" or borg.get("borg_may_use_portal_to_enter_alpha") is not False or borg.get("idea_0011_portal_implemented") is not False:
        errors.append("Colectividad Borg equiparada a biología o portal DLC habilitado")
    context = read_json(root / "lore/factions/ai_npc_political_context_cases_v0.1.json")
    if len(context.get("cases", [])) < 7:
        errors.append("Insuficientes casos de identidades institucionales separadas")
    for case in context.get("cases", []):
        if case.get("core_controls_world_mutations") is not True:
            errors.append("Un ejemplo de IA se apropia de autoridad de mundo")
        if len(case.get("core_required", [])) < 3:
            errors.append("Ejemplo sin identidad, autorización y conocimiento contextual")
    if not any(c["id"] == "tzenkethi_false_coup" for c in context.get("cases", [])):
        errors.append("Falta caso de rumor tzenkethi desmentido")
    return errors


if __name__ == "__main__":
    problems = validate_repo()
    if problems:
        for problem in problems:
            print("LORE-01 B ERROR:", problem, file=sys.stderr)
        sys.exit(1)
    print("LORE-01 B OK: 16 entidades, 16 monografías, 16 libros de evidencia, fuentes, tiempo, IA y DLC.")
