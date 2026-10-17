#!/usr/bin/env python3
"""LORE-01 A v0.2: integridad de 25 monografías y anclajes a fuentes.

Solo valida el repositorio/documentación; NO verifica reproducción audiovisual
plano a plano, verdad histórica absoluta, CoreRPG, UE5 ni DLC ejecutable.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPECIES_OLD = {
 "human","vulcan","andorian","aenar","tellarite","klingon","romulan",
 "cardassian","bajoran","ferengi","trill","betazoid","changeling","vorta","jem_hadar"
}
SPECIES_MAIN_NEW = {"bolian","benzite","el_aurian","breen","pakled"}
SPECIES_DLC = {"kazon","ocampan","talaxian","vidiian","hirogen"}
ALL = SPECIES_OLD | SPECIES_MAIN_NEW | SPECIES_DLC
CANON_SOURCE_TYPES = {"SCREEN_CANON","OFFICIAL_REFERENCE","RELIABLE_SECONDARY"}
PERMITTED_SCREEN_PREFIXES = ("TNG_","DS9_","VOY_","TOS_")
UNKNOWN_FIELDS = ("unresolved_research","known_unknowns","unresolved_biology_and_research","missing_fields","unknown_information")
PROFILES = Path("lore/species/evidence")
MONOGRAPHS = Path("lore/species/monographs")

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def ledger_evidence(dossier: dict) -> list[dict]:
    return dossier.get("evidence", dossier.get("verified_claims", []))

def resolve_unknowns(dossier: dict) -> list[str]:
    return dossier.get("domains", {}).get("unknowns", [])

def validate_dossier(dossier: dict, species_id: str, sources: dict) -> list[str]:
    errs = []
    if dossier.get("species_id") != species_id:
        errs.append(f"{species_id}: ID del dossier no coincide")
    if dossier.get("schema_version") != "0.2.0":
        errs.append(f"{species_id}: schema_version distinto de 0.2.0")
    if dossier.get("status") not in {
        "DEEP_DOCUMENTARY_AUTHORING_NO_RUNTIME_CERTIFICATION",
        "DLC_DEEP_DOCUMENTARY_AUTHORING_NOT_INSTALLED",
    }:
        errs.append(f"{species_id}: estado no transparente")
    if dossier.get("legacy_profile_ref") != f"gameplay/species/profiles/{species_id}_v0.1.json":
        errs.append(f"{species_id}: ruta de ficha operativa incorrecta")
    if dossier.get("monograph_ref") != f"lore/species/monographs/{species_id}_v0.2.md" and dossier.get("narrative_profile_ref") != f"lore/species/monographs/{species_id}_v0.2.md":
        errs.append(f"{species_id}: ruta de monografía incorrecta")
    domains = dossier.get("domains", {})
    required = {"biology","lifecycle","culture","language","chronology","npc_scenarios","unknowns","canon_cautions"}
    if set(domains) != required:
        errs.append(f"{species_id}: esquema de ocho dominios incumplido")
    elif any(not domains[key] for key in required):
        errs.append(f"{species_id}: dominio fundamental vacío")
    if dossier.get("verification_status") != "EPISODE_OR_OFFICIAL_REFERENCE_ANCHORS_NOT_SCENE_BY_SCENE_VERIFIED":
        errs.append(f"{species_id}: verificación de escenas falsa")
    e = ledger_evidence(dossier)
    if len(e) < 3:
        errs.append(f"{species_id}: menos de tres anclajes de evidencia")
    ids = set()
    for item in e:
        claim_id, source_id = item.get("claim_id"), item.get("source_id")
        if not claim_id or claim_id in ids:
            errs.append(f"{species_id}: identificador de afirmación duplicado/ausente")
        ids.add(claim_id)
        if source_id not in sources:
            errs.append(f"{species_id}: fuente sin registrar: {source_id}")
        else:
            typ = sources[source_id]["source_type"]
            if typ not in CANON_SOURCE_TYPES:
                errs.append(f"{species_id}: fuente no apta para catalogación profunda: {source_id}")
            if item.get("authority") != typ:
                errs.append(f"{species_id}: tipo de autoridad contradictorio en {source_id}")
            if typ == "SCREEN_CANON" and not source_id.startswith(PERMITTED_SCREEN_PREFIXES):
                errs.append(f"{species_id}: pantalla fuera del alcance: {source_id}")
        if not str(item.get("claim_es", "")).strip() or len(item["claim_es"]) < 35:
            errs.append(f"{species_id}: evidencia demasiado vaga: {claim_id}")
        if str(source_id).startswith("ENT_"):
            errs.append(f"{species_id}: referencia ENT excluida de nuevas afirmaciones: {source_id}")
    unknown = resolve_unknowns(dossier)
    if not isinstance(unknown, list) or len(unknown) < 4:
        errs.append(f"{species_id}: incertidumbres insuficientes")
    if species_id == "aenar":
        if any(x.get("source_id", "").startswith(("TNG_", "DS9_", "VOY_")) for x in e):
            errs.append("aenar: evitar convertir una referencia a andorianos en prueba directa de Aenar")
    if species_id in SPECIES_DLC:
        if dossier.get("content_scope") != "DLC_DELTA_FUTURE_NO_MAIN_SPAWN":
            errs.append(f"{species_id}: perfil DLC sin protección correcta")
        if dossier.get("main_game_automatic_spawn_allowed") is not False and dossier.get("main_game_automatic_spawn_allowed") is not None:
            errs.append(f"{species_id}: permite spawn en base")
    elif dossier.get("content_scope", "").startswith("DLC_"):
        errs.append(f"{species_id}: especie base clasificada como DLC")
    return errs

def validate_repo(root: Path = ROOT) -> list[str]:
    errors = []
    source_registry = load_json(root / "sources/source_registry/source_registry.json")
    sources = {s["source_id"]: s for s in source_registry["sources"]}
    if len(sources) != len(source_registry["sources"]):
        errors.append("Source registry tiene duplicados")
    index = load_json(root / "lore/species/LORE01_TNG_species_coverage_audit_v0.1.json")
    rows = index["existing_species"] + index["approved_species_additions"]
    if {r["species_id"] for r in rows} != ALL or len(rows) != 25:
        errors.append("Cobertura del índice diferente a 25")
    for species_id in sorted(ALL):
        src_path = root / PROFILES / f"{species_id}_v0.2.json"
        md_path = root / MONOGRAPHS / f"{species_id}_v0.2.md"
        old_path = root / "gameplay/species/profiles" / f"{species_id}_v0.1.json"
        for file_path in (src_path, md_path, old_path):
            if not file_path.is_file():
                errors.append("Falta: " + str(file_path.relative_to(root)))
        if not src_path.is_file() or not md_path.is_file():
            continue
        try:
            dossier = load_json(src_path)
            monograph = md_path.read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            errors.append(f"{species_id}: archivo ilegible: {exc}")
            continue
        errors.extend(validate_dossier(dossier, species_id, sources))
        if len(monograph) < 2500:
            errors.append(f"{species_id}: monografía excesivamente corta")
        if f"`{species_id}`" not in monograph:
            errors.append(f"{species_id}: monografía sin su ID explícito")
        if "Incertidumbres" not in monograph and "Límites pendientes" not in monograph and "Lagunas conservadas" not in monograph:
            errors.append(f"{species_id}: monografía sin incertidumbres")
        if species_id in SPECIES_DLC and "No aparece" not in monograph and "DLC" not in monograph[:400]:
            errors.append(f"{species_id}: disponibilidad de DLC no clara")
    files = {x.stem.replace("_v0.2","") for x in (root / PROFILES).glob("*_v0.2.json")}
    if files != ALL:
        errors.append(f"Directorio de evidencias con IDs inesperados: {sorted(files ^ ALL)}")
    return errors

if __name__ == "__main__":
    errors = validate_repo()
    if errors:
        for e in errors:
            print("ERROR LORE01 DEPTH:", e, file=sys.stderr)
        sys.exit(1)
    print("LORE-01 A DEEP OK: 25 monografías; 25 libros de evidencia; referencias y reservas DLC coherentes.")
