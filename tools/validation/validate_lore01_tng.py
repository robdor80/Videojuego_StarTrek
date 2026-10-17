#!/usr/bin/env python3
"""Validación documental LORE-01 A: TNG/DS9/VOY y reserva del DLC Delta.

No prueba integración con CoreRPG ni disponibilidad en UE5.
Ejecutar: python tools/validation/validate_lore01_tng.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IDX = "lore/species/LORE01_TNG_species_coverage_audit_v0.1.json"
GATE = "universe/generation/lore01_tng_content_availability_v0.1.json"
REGISTRY = "sources/source_registry/source_registry.json"
LANGS = "gameplay/languages/initial_language_catalogue.json"
EXISTING = {
 "human","vulcan","andorian","aenar","tellarite","klingon","romulan",
 "cardassian","bajoran","ferengi","trill","betazoid","changeling","vorta","jem_hadar"
}
MAIN_ADDED = {"bolian","benzite","el_aurian","breen","pakled"}
DLC = {"kazon","ocampan","talaxian","vidiian","hirogen"}
TOTAL = EXISTING | MAIN_ADDED | DLC

def read(root: Path, rel: str):
    path = root / rel
    if not path.is_file():
        raise FileNotFoundError(rel)
    return json.loads(path.read_text(encoding="utf-8"))

def validate_policy(gate: dict) -> list[str]:
    errors = []
    main = gate.get("main_game", {})
    delta = gate.get("delta_dlc", {})
    if set(main.get("species_ids_existing", [])) != EXISTING:
        errors.append("El inventario original de 15 especies ha cambiado")
    if set(main.get("species_ids_added", [])) != MAIN_ADDED:
        errors.append("Las cinco especies principales no coinciden")
    if set(delta.get("species_ids", [])) != DLC:
        errors.append("La reserva de las cinco especies Delta no coincide")
    if set(main.get("species_ids_existing", []) + main.get("species_ids_added", [])) & DLC:
        errors.append("FUGA DLC: especie Delta habilitada como principal")
    if delta.get("default_main_game_spawn_allowed") is not False:
        errors.append("FUGA DLC: spawn principal permitido")
    if delta.get("status") != "FUTURE_NOT_IMPLEMENTED":
        errors.append("El DLC no puede presentarse como implementado")
    travel = delta.get("planned_travel", {})
    if travel.get("kind") != "BORG_TRANSWARP_PORTAL" or travel.get("implementation_status") != "NOT_IN_THIS_PHASE":
        errors.append("Portal no está documentado como concepto futuro")
    if travel.get("approved_idea_ref") != "ideas/IDEA-0011_dlc_cuadrante_delta_portal_transwarp.md":
        errors.append("Falta enlace a la idea 0011 ya aprobada")
    if travel.get("borg_can_traverse_this_portal_toward_alpha") is not False:
        errors.append("Portal permite entrada Borg hacia Alfa")
    if travel.get("no_auto_borg_invasion_on_activation") is not True:
        errors.append("Activar DLC provoca invasión Borg")
    if travel.get("normal_return_via_same_portal") is not True:
        errors.append("No preserva la opción C de regreso")
    if travel.get("return_may_be_interrupted_only_by_caused_world_events") is not True:
        errors.append("Interrupciones de regreso no exigen causas")
    if not gate.get("exceptions", {}).get("el_aurian", {}).get("main_game_allowed"):
        errors.append("La diáspora el-auriana quedó bloqueada incorrectamente")
    if not gate.get("exceptions", {}).get("borg", {}).get("main_game_allowed"):
        errors.append("Los Borg quedaron bloqueados incorrectamente")
    if not gate.get("integration_boundary", {}).get("authoring_only"):
        errors.append("Falsa afirmación de integración runtime")
    return errors

def validate_repo(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        idx = read(root, IDX)
        gate = read(root, GATE)
        registry = read(root, REGISTRY)
        langs = read(root, LANGS)
    except (OSError, ValueError) as exc:
        return [f"Documento base ilegible: {exc}"]
    errors += validate_policy(gate)
    source_ids = {s["source_id"] for s in registry["sources"]}
    known_languages = {l["language_id"] for l in langs["languages"]}
    if len(known_languages) != len(langs["languages"]):
        errors.append("IDs de lenguas duplicados")
    if not {"breen","kazon","talaxian"} <= known_languages:
        errors.append("Faltan lenguas con evidencia explícita")
    rows = idx.get("existing_species", []) + idx.get("approved_species_additions", [])
    ids = [r["species_id"] for r in rows]
    if len(ids) != 25 or len(ids) != len(set(ids)) or set(ids) != TOTAL:
        errors.append("La cobertura no coincide con 25 especies únicas")
    states = idx.get("non_species_states", [])
    if len(states) != 1 or states[0].get("state_id") != "borg_assimilated_character":
        errors.append("Asimilación Borg mal catalogada como especie")
    for st in states:
        if not (root / st["profile_ref"]).is_file():
            errors.append("No existe estado Borg: " + st["profile_ref"])
    if idx.get("content_gate_ref") != GATE:
        errors.append("Índice apunta a un gate distinto")
    for row in rows:
        ident = row["species_id"]
        profile_path = row["profile_ref"]
        try:
            sp = read(root, profile_path)
        except (OSError, ValueError) as exc:
            errors.append(f"{ident}: ficha ilegible {exc}")
            continue
        if sp.get("species_id") != ident:
            errors.append(f"{ident}: species_id no corresponde a la ruta")
        culture_path = row.get("cultural_profile_ref")
        if culture_path is None:
            culture_list = row.get("contextual_culture_refs", [])
        else:
            culture_list = [culture_path]
        for rel in culture_list:
            try:
                culture = read(root, rel)
            except (OSError, ValueError) as exc:
                errors.append(f"{ident}: cultura ilegible {exc}")
                continue
            scope = culture.get("identity_and_scope", {})
            if isinstance(culture.get("profiles"), dict):
                scope = culture["profiles"].get(ident, {}).get("identity_and_scope", {})
            auto = scope.get("automatic_attachment_by_species")
            if auto is not False and scope.get("species_lock") is not False:
                errors.append(f"{ident}: cultura sin garantía explícita de no adjunción automática")
        for claim in sp.get("provenance", []):
            src = claim.get("source_id")
            if src not in source_ids:
                errors.append(f"{ident}: fuente desconocida {src}")
            if ident in MAIN_ADDED | DLC and str(src).startswith("ENT_"):
                errors.append(f"{ident}: nueva ficha cita Enterprise fuera del corpus")
        if ident in MAIN_ADDED | DLC:
            if not sp.get("provenance"):
                errors.append(f"{ident}: faltan fuentes")
            if not sp.get("unknowns"):
                errors.append(f"{ident}: faltan incertidumbres")
            if not sp.get("description_es"):
                errors.append(f"{ident}: falta descripción española")
            cult_ref = sp.get("culture_socialization", {}).get("contextual_profile_ref")
            if cult_ref != culture_path:
                errors.append(f"{ident}: ruta de cultura incongruente")
            lang = sp.get("language", {}).get("language_id")
            if lang is not None and lang not in known_languages:
                errors.append(f"{ident}: lengua no registrada {lang}")
            if ident in DLC:
                if sp.get("content_availability", {}).get("gameplay_spawn_in_main") is not False:
                    errors.append(f"{ident}: DLC expuesto a spawn principal")
                if sp.get("generation_constraints", {}).get("general_main_game_population_eligible") is not False:
                    errors.append(f"{ident}: población Delta no bloqueada")
                if row.get("content_scope") != "DLC_DELTA_FUTURE_NO_MAIN_GAME_SPAWN":
                    errors.append(f"{ident}: fila de índice sin reserva DLC")
            else:
                if sp.get("scope", {}).get("game_content") != "MAIN_GAME":
                    errors.append(f"{ident}: ficha principal no habilitada documentalmente")
                if row.get("content_scope") != "MAIN_GAME_TNG_CONTEXTUAL":
                    errors.append(f"{ident}: índice principal inconsistente")
    for lang in langs["languages"]:
        for species_id in lang.get("associated_species_ids", []):
            if species_id not in TOTAL:
                errors.append(f"Idioma {lang['language_id']}: especie inexistente {species_id}")
        for src in lang.get("source_refs", []):
            if src not in source_ids:
                errors.append(f"Idioma {lang['language_id']}: fuente inexistente {src}")
        if any(x in DLC for x in lang.get("associated_species_ids", [])):
            if lang.get("availability_scope") != "DLC_DELTA_FUTURE":
                errors.append(f"Idioma {lang['language_id']}: filtración de lengua DLC")
    return errors

if __name__ == "__main__":
    issues = validate_repo(ROOT)
    if issues:
        for err in issues:
            print("ERROR LORE01:", err, file=sys.stderr)
        sys.exit(1)
    print("LORE-01 A OK: 25 especies; 15 heredadas, 5 principales, 5 DLC; culturas, fuentes, idiomas y reserva Delta.")
