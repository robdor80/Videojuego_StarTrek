#!/usr/bin/env python3
"""Comparación ESTÁTICA entre el currículo fuente y un checkout de academiaflota.

No toca perfiles, Firebase, notas, usuarios, CoreRPG ni UE5.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from f10_academy_reference import ROOT, audit_sources


def _json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON no es objeto: {path}")
    return data


def check_web_parity(web_root: Path, game_root: Path = ROOT) -> dict:
    audit_sources(game_root)
    curriculum = game_root / "sistemas/gameplay/careers/academy_path/curriculum"
    game = _json(curriculum / "curriculum_manifest_v1_0.json")
    web = _json(web_root / "data/curriculum.json")
    if web.get("sourceRepository") != "robdor80/Videojuego_StarTrek":
        raise ValueError("La web no identifica la fuente autoritativa")
    expected_ref = "sistemas/gameplay/careers/academy_path/curriculum/curriculum_manifest_v1_0.json"
    if web.get("sourceManifest") != expected_ref:
        raise ValueError("El manifiesto publicado no apunta a la fuente")
    if len(web.get("years", [])) != 4:
        raise ValueError("Web: deben existir cuatro años")
    total = 0
    all_ids = []
    for index, (g, w) in enumerate(zip(game["years"], web["years"])):
        expected_web_id = ["4-clase", "3-clase", "2-clase", "1-clase"][index]
        if w.get("id") != expected_web_id:
            raise ValueError("El orden de clases en la web no coincide")
        ts = w.get("trimesters", [])
        if len(ts) != 3 or any(len(t.get("subjects", [])) != 5 for t in ts):
            raise ValueError("La web no publica 3 trimestres x 5 asignaturas")
        published = [sub for t in ts for sub in t["subjects"]]
        ids = [sub["courseId"] for sub in published]
        manifest = _json(curriculum / g["manifest_ref"])
        if ids != manifest["course_ids"]:
            raise ValueError(f"Desajuste o reordenación de IDs en {expected_web_id}")
        for sub in published:
            for ref_key in ("dataFile", "assessmentFile"):
                rel = sub.get(ref_key)
                if not isinstance(rel, str) or not rel.startswith("data/") or ".." in Path(rel).parts:
                    raise ValueError("Ruta web ausente o insegura")
                if not (web_root / rel).is_file():
                    raise ValueError(f"Archivo publicado no existe: {rel}")
        total += len(ids)
        all_ids.extend(ids)
    if total != 60 or len(set(all_ids)) != 60:
        raise ValueError("Las 60 asignaturas deben tener IDs únicos")
    branches = web.get("branchLibrary", [])
    ids = [x.get("branchId") for x in branches]
    if len(ids) != 7 or set(ids) != set(game["branch_ids"]) or len(set(ids)) != 7:
        raise ValueError("Las siete ramas web divergen del origen")
    for item in branches:
        for ref_key in ("dataFile", "assessmentFile"):
            rel = item.get(ref_key)
            if not isinstance(rel, str) or not rel.startswith("data/") or ".." in Path(rel).parts:
                raise ValueError("Ruta de rama insegura")
            if not (web_root / rel).is_file():
                raise ValueError(f"Rama publicada sin archivo: {rel}")
    return {
        "static_content_parity": "PASS", "years": 4, "trimesters": 12,
        "course_ids_matched": total, "branch_ids_matched": len(ids),
        "profiles_compared": False, "firebase_checked": False,
        "core_checked": False, "unreal_checked": False
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--web-root", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(check_web_parity(args.web_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
