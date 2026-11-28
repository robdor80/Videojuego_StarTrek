#!/usr/bin/env python3
"""Enrich the *existing* F06 Aster fixture with derived physical Host truth.

The output is private to the build tree. F06's sensor-feed generator discards
all science_truth fields: an observer never sees a planet class just because
it exists in this file.
"""
from __future__ import annotations
import argparse
import copy
import json
import math
from pathlib import Path
from astro_physics_v1 import EARTH_RADIUS_AU, VERSION, planet_physics, star_from_mass, validate_planet

# The fixed F06 sensor positions are illustrative milli-AU, not an N-body simulation.
# Scientific planet types below are NOT supplied directly; they are DERIVED.
RECIPES = {
    201: ("desert", {"mass_earth": .8, "pressure_bar": .18, "greenhouse_k": 8}),
    202: ("rocky", {"mass_earth": 1.05, "pressure_bar": 1.0, "greenhouse_k": 65,
                   "water_inventory": .68}),
    203: ("ice_rock", {"mass_earth": .7, "pressure_bar": .6, "greenhouse_k": 12}),
    204: ("gas_giant", {"mass_earth": 170}),
    205: ("ice_rock", {"mass_earth": 1.8, "pressure_bar": .2, "greenhouse_k": 8}),
    206: ("ice_rock", {"mass_earth": .6, "pressure_bar": .03, "greenhouse_k": 1}),
}
# Stable and conservative orbit ratios; each moon has a physically plausible
# near-parent position instead of the oversized illustrative old offsets.
MOON_OFFSETS = {301:(2,1), 302:(12,4), 303:(-10,-6), 304:(3,1)}

def enrich(base: dict) -> dict:
    if base["scenario_id"]!="aster_f06_qa" or base["schema_version"]!=1:
        raise ValueError("Aster QA input only")
    result=copy.deepcopy(base)
    star=star_from_mass(1.0,4.6,"Aster")
    parents={}
    entities={e["key"]:e for e in result["entities"]}
    if set(RECIPES)!=set(k for k,e in entities.items() if e["kind"]=="planet"):
        raise ValueError("Aster planet roster changed without a reviewed recipe")
    if set(MOON_OFFSETS)!=set(k for k,e in entities.items() if e["kind"]=="moon"):
        raise ValueError("Aster moon roster changed")
    for e in result["entities"]:
        if e["kind"]=="star":
            e["science_truth"]={"physical_model":"trek_astro_physical_v1","stellar":star,
                                "composition":{"H2":.74,"He":.25,"metals":.01},
                                "biosphere":None,"planet_class":None}
        elif e["kind"]=="planet":
            key=e["key"]
            orbit=math.sqrt(sum((c/1000)**2 for c in e["position_milli_au"]))
            family,recipe=RECIPES[key]
            physics=planet_physics(1.0,1.0,4.6,orbit,family,f"aster|{key}",recipe)
            errors=validate_planet(physics,1.0,1.0,4.6)
            if errors:
                raise ValueError(f"{key}: {'; '.join(errors)}")
            parents[key]=physics
            e["science_truth"]={
                "physical_model":"trek_astro_physical_v1",
                "physical_planet":physics,
                "planet_class":physics["star_trek"]["class_candidate"],
                "planet_class_status":"provisional_gameplay_derived_not_sensor_confirmation",
                "generation_version":VERSION
            }
        elif e["kind"]=="moon":
            parent_key=e["parent_key"]
            if parent_key not in parents:
                raise ValueError("fixture must list planets before moons")
            parent=entities[parent_key]
            p=parents[parent_key]
            dx,dy=MOON_OFFSETS[e["key"]]
            distance=math.hypot(dx,dy)/1000
            min_dist=3*p["radius_earth"]*EARTH_RADIUS_AU
            max_dist=.30*p["orbit"]["hill_radius_au"]
            if not min_dist<distance<max_dist:
                raise ValueError(f"moon {e['key']} outside stable Hill/size band")
            e["position_milli_au"]=[
                parent["position_milli_au"][0]+dx,
                parent["position_milli_au"][1]+dy, 0]
            e["science_truth"]={
                "physical_model":"trek_astro_physical_v1",
                "parent_key":parent_key,"orbital_distance_au":distance,
                "parent_hill_radius_au":p["orbit"]["hill_radius_au"],
                "surface":{"exists":True,"biomes":["abiotic"]},
                "biosphere":{"stage":"none"},"planet_class":None
            }
    # Never masquerade as a real galactic persistence/runtime module.
    result["status"]="FIXTURE_NON_CANON_NOT_A_PERSISTENT_GALAXY"
    result["science_generation"]={
        "generator":"trek_astro_physical_v1","generator_version":VERSION,
        "host_truth_private":True,
        "validation":"6 planet profiles and 4 Hill-bounded moon offsets",
        "planet_classification":"derived_from_physics_not_direct_input",
        "planetary_orbits":"fixed_for_eight_hour_sensor_QA_not_n_body"
    }
    return result

def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    result=enrich(json.loads(a.source.read_text(encoding="utf-8")))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+"\n",
                        encoding="utf-8")

if __name__=="__main__":
    main()
