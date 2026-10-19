#!/usr/bin/env python3
"""Audita LORE-01 C (documental). No modifica datos de runtime."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "lore/astrography/atlas"
MAP_IDS = {
    "CHAT_MAP_01_FEDERATION_PANELS",
    "CHAT_MAP_02_GALAXY_SCHEMATIC",
    "CHAT_MAP_03_SECTOR_FAN_GRID",
    "CHAT_MAP_04_SHAKAAR_ALPHA_BETA_V33",
}
QUADRANTS = {"ALPHA", "BETA", "GAMMA", "DELTA"}
DELTA_ANCHORS = {
    "delta_quadrant_caretaker_arrival_region",
    "borg_transwarp_network_reference",
}


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def validate():
    """Valida cruces, autoridad, no creación de runtime y cronología."""
    a = read("lore/astrography/systems/anchor_locations.json")["locations"]
    r = read("lore/astrography/spatial_regions/gameplay_regions.json")["regions"]
    e = read("gameplay/navigation/initial_reference_distance_edges.json")["entries"]
    graph = read("gameplay/navigation/anchor_route_graph.json")
    src = read("sources/source_registry/source_registry.json")["sources"]
    registry = {x["source_id"] for x in src}
    atlas = read("lore/astrography/atlas/anchor_atlas_v0.1.json")
    quadrant = read("lore/astrography/atlas/quadrants_regions_v0.1.json")
    routes = read("lore/astrography/atlas/route_reference_cases_v0.1.json")
    manifest = read("lore/astrography/atlas/map_reference_manifest_v0.1.json")
    leads = read("lore/astrography/atlas/cartographic_research_leads_v0.1.json")
    issues = read("lore/astrography/atlas/map_discrepancy_ledger_v0.1.json")
    cases = read("lore/astrography/atlas/knowledge_era_cases_v0.1.json")
    legacy = {x["location_id"]: x for x in a}
    locations = {x["location_id"]: x for x in atlas["locations"]}

    require(len(locations) == len(a) == atlas["location_count"], "Atlas y anclajes no coinciden")
    require(set(legacy) == set(locations), "No añadir/quitar anclajes al índice de C")
    require(atlas["authority"] == "CoreRPG_World_State_ONLY", "Autoridad no declarada")
    require(atlas["status"] == "DOCUMENTARY_AUTHORING_NOT_INTEGRATED", "Importación prematura")
    for loc_id, row in locations.items():
        old = legacy[loc_id]
        require(row["legacy_anchor_ref"].endswith("#" + loc_id), "Referencia a anclaje corrupta")
        require(row["location_type"] == old["location_type"], "Tipo de anclaje modificado")
        require(row["parent_location_id"] == old.get("parent_location_id"), "Padre de anclaje alterado")
        require(row["region_id"] == old.get("region_id"), "Región del anclaje alterada")
        require(row["quadrant"] is None or row["quadrant"] in QUADRANTS, "Cuadrante no válido")
        require(row["quadrant_basis"] != "FAN_MAP", "Prohibido ascender fan-map a base factual")
        coords = row["coordinates"]
        require(all(coords[x] is None for x in ("frame_id", "x_ly", "y_ly", "z_ly", "provenance")), "XYZ de mapa no calibrado")
        require(row["runtime_generation_enabled"] is False, "No se permite generación en C")
        require(row["world_state_owned"] is False, "C no asigna propietario del estado del mundo")
        require(row["source_refs"] == list(dict.fromkeys(old.get("source_refs", []))), "C debe preservar fuentes existentes")
        require(set(row["source_refs"]).issubset(registry), "Fuente no registrada en localización")
        require("political_owner_id" not in row and "controller_faction_id" not in row,
                "Soberanía física no permitida en atlas")
        expected = "DELTA_RESERVED_REFERENCE_ONLY" if loc_id in DELTA_ANCHORS else "MAIN_GAME_REFERENCE"
        require(row["documentary_availability"] == expected, "Se filtra DLC Delta al juego principal")
    require(locations["sol_system"]["quadrant"] is None, "Sol requiere resolución no arbitraria")
    require(locations["earth"]["quadrant"] is None, "Tierra requiere resolución no arbitraria")
    require(locations["bajoran_wormhole_alpha"]["quadrant"] == "ALPHA", "Boca Alfa perdida")
    require(locations["bajoran_wormhole_gamma"]["quadrant"] == "GAMMA", "Boca Gamma perdida")
    require(locations["delta_quadrant_caretaker_arrival_region"]["quadrant"] == "DELTA",
            "Caretaker fuera de Delta")

    qs = quadrant["quadrants"]
    require({q["quadrant_id"] for q in qs} == QUADRANTS and len(qs) == 4, "Cuadrantes incompletos")
    require(next(q for q in qs if q["quadrant_id"] == "DELTA")["availability"]
            == "FUTURE_DLC_REFERENCE_ONLY", "Cuadrante Delta desbloqueado")
    require(all(q["physical_polygon"] is None and q["exact_sector_grid"] is None for q in qs),
            "Polígonos/sectores extrapolados")
    require({v["region_id"] for v in quadrant["regions"]} == {v["region_id"] for v in r}
            and len(quadrant["regions"]) == len(r), "Regiones cambiadas")
    require(all(x["boundary_polygon"] is None and x["political_owner_id"] is None
                for x in quadrant["regions"]), "Territorio temporal fijado en la geografía")

    maps = manifest["maps"]
    require(manifest["original_images_in_public_repository"] is False, "No publicar imágenes")
    require(manifest["upload_policy"] == "METADATA_ONLY_UNTIL_RIGHTS_VERIFIED", "Permisos de copia no verificados")
    require({m["map_id"] for m in maps} == MAP_IDS and len(maps) == 4, "Faltan mapas del usuario")
    require(all(m["license_status"] == "UNVERIFIED" for m in maps), "Licencia atribuida sin pruebas")
    for m in maps:
        require(bool(re.fullmatch(r"[0-9a-f]{64}", m["sha256"])), "SHA256 inválido")
        require(m["pixel_size"][0] > 0 and m["pixel_size"][1] > 0 and m["byte_size"] > 0,
                "Metadatos imagen inválidos")
        require(m["reference_class"] != "SCREEN_CANON", "Un mapa no es episodio")
    require(not any(p.suffix.lower() in {".jpg", ".png", ".jpeg", ".pdf", ".webp", ".gif"}
                    for p in BASE.rglob("*")), "Atlas debe ser solo documentos y datos")

    ref_edges = {v["edge_id"]: v for v in e}
    edge_cases = [x for x in routes["cases"] if x["baseline_edge_id"] in ref_edges]
    require(len(edge_cases) == len(ref_edges), "Perdida cobertura de distancias")
    for row in edge_cases:
        old = ref_edges[row["baseline_edge_id"]]
        require(row["original_distance_ly"] == old["distance_ly"], "Distancia modificada por visual")
        require(row["origin_location_id"] == old["origin_location_id"]
                and row["destination_location_id"] == old["destination_location_id"], "Arista redirigida")
        require(row["map_image_used_to_calculate_distance"] is False, "Distancia falsa de píxeles")
        require(row["legacy_underlying_source"] == old["underlying_source"], "Procedencia de distancia alterada")
        require(row["legacy_underlying_source"] in registry or row["legacy_underlying_source"] in {"real_star", "40_eridani_reference"},
                "Fuente heredada de distancia desconocida")
    wormhole = next(x for x in routes["cases"] if x["case_id"] == "L01C_BAJORAN_WORMHOLE")
    require(wormhole["original_distance_ly"] is None
            and wormhole["interpretation"] == "NON_WARP_GATED_SPECIAL_CONNECTION", "Gusano no especial")
    require(any(g.get("edge_id") == "bajoran_wormhole_traversal"
                and g.get("ordinary_warp_edge") is False for g in graph["edges"]),
            "Grafo original de agujero de gusano ausente")
    require(len(routes["prohibited_edges"]) >= 2
            and all("DELTA" in row["reason"].upper() or "DLC" in row["reason"].upper()
                    or "IDEA-0011" in row["reason"] for row in routes["prohibited_edges"]),
            "Faltan rutas prohibidas a Delta")

    cand = leads["candidates"]
    require(len(cand) >= 20, "Lista de pistas demasiado escasa")
    require(len({x["candidate_id"] for x in cand}) == len(cand), "Pistas repetidas")
    for x in cand:
        require(x["map_id"] in MAP_IDS and x["validation_state"] == "RESEARCH_REQUIRED", "Pista elevada a canon")
        require(x["canonical_location_id"] is None and x["runtime_import_allowed"] is False,
                "Mapa fan importado a juego")
        require(all(x[y] is None for y in ("position_x_ly", "position_y_ly", "position_z_ly")),
                "Pista contiene coordenadas inventadas")

    require(len(issues["entries"]) >= 10 and len(cases["cases"]) >= 9, "Faltan conflictos/casos")
    require({x["issue_id"] for x in issues["entries"]}
            >= {"SOL_ALPHA_BETA", "SOURCE_COPYRIGHT", "DELTA_LOCK", "POLITICAL_MAP_UNDATED"},
            "Conflictos críticos omitidos")
    require(all(x["map_ids"] and set(x["map_ids"]).issubset(MAP_IDS)
                and x["canon_promotion_allowed"] is False
                for x in issues["entries"]), "Ascenso automático de mapas")
    require(all(x["subject_location_id"] in locations and x["ai_may_bypass_gates"] is False
                and x["changes_world_state"] is False
                and set(x["source_refs"]).issubset(registry)
                for x in cases["cases"]), "Caso IA rompe límites")
    require(any(x["case_id"] == "VOY_DELTA_NO_SHARED_OMNISCIENCE" and x["auto_visible"] is False
                for x in cases["cases"]), "Omnisciencia Voyager")
    require(any(x["case_id"] == "TNG_2364_WORMHOLE_UNKNOWN" and x["auto_visible"] is False
                for x in cases["cases"]), "Anacronismo agujero de gusano")

    status = (ROOT / "CONTENT_STATUS.md").read_text(encoding="utf-8")
    require("B — Civilizaciones/potencias | ✅ COMPLETE" in status, "LORE-01 B no regularizada")
    require(any(marker in status for marker in ("C — Cartografía/astrogeografía | 🟧 NEEDS_REVIEW", "C — Cartografía/astrogeografía | ✅ COMPLETE")), "Estado C incorrecto")
    require(any(marker in status for marker in ("D — Relaciones diplomáticas | ⬜ TODO", "D — Relaciones diplomáticas | 🟧 NEEDS_REVIEW", "D — Relaciones diplomáticas | ✅ COMPLETE")), "Estado D desconocido")
    require("E — Información operativa transversal | ⬜ TODO" in status, "No avanzar E")
    return {
        "anchors": len(a), "regions": len(r), "maps": len(maps),
        "routes": len(routes["cases"]), "leads": len(cand),
        "discrepancies": len(issues["entries"]), "knowledge_cases": len(cases["cases"]),
        "sources_registry": len(registry),
    }


def main():
    result = validate()
    print("LORE-01 C VALIDACIÓN OK:", result)


if __name__ == "__main__":
    main()
