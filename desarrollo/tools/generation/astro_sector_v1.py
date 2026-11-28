#!/usr/bin/env python3
"""Bounded, lazy-compatible stellar-neighborhood catalogue over astro_physics_v1.

Does not create ships, civilizations, campaign events, missions or Core state.
Sector is fictional context, not a Milky Way stellar-population model.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path

from astro_physics_v1 import Rng, compact_object, environmental_region, generate_system, token, validate_system

def generate_sector(seed: str, sector: str, *,
                    era: str = "tng_ds9_voyager", date: str = "2383-01-01",
                    systems: int = 5, reserved_system_names: set[str] | None = None) -> dict:
    """Generate a small sector manifest with disjoint stars at least 1.5 ly apart.

    A canonical reservation is never rerolled. Caller must place known worlds
    separately, outside this generated-only namespace.
    """
    if not seed or not sector or not 1<=systems<=25:
        raise ValueError("1..25 systems and nonempty seed/sector required")
    rng=Rng(seed,sector,"sector-v1")
    systems_out=[]
    reserved_system_names=reserved_system_names or set()
    positions=[]
    for i in range(systems):
        name=f"PROC-{sector}-{i+1}"
        if name in reserved_system_names:
            raise ValueError("reserved canonical or user-authored system name")
        for attempt in range(500):
            x,y,z=(rng.between(-18,18) for _ in range(3))
            if all(math.dist([x,y,z],other)>=1.5 for other in positions):
                break
        else:
            raise ValueError("cannot place another independent stellar system")
        positions.append([x,y,z])
        world=generate_system(seed=f"{seed}|{sector}|{i+1}",
                              sector=f"{sector}-{i+1}",era=era,date=date,
                              profile="game")
        if validate_system(world):
            raise ValueError("one generated star system fails physics validation")
        systems_out.append({
            "catalogue_key":f"gen:sector_system:{token(seed,sector,i+1)}",
            "display_name":name,
            "position_light_years":[round(v,6) for v in (x,y,z)],
            "system":world,
            "status":"PERSISTENT_INITIAL_TRUTH_NOT_COMMITTED_TO_CORE",
        })
    # Compact remnants are independent anchors, not a gratuitous feature of
    # every star system. Probabilities are gameplay tuning, not astronomical rate.
    extras=[]
    if rng.u()<.15:
        kind=rng.weighted([("white_dwarf",6),("brown_dwarf",5),
                           ("neutron_star",2),("pulsar",1),("black_hole",1)])
        extras.append({
            "entity_id":f"gen:compact:{token(seed,sector,kind)}",
            "position_light_years":[round(rng.between(-24,24),6) for _ in range(3)],
            "ground_truth":compact_object(f"{seed}|{sector}",kind),
            "canonical_reserved":False,
        })
    if rng.u()<.08:
        extras.append({
            "entity_id":f"gen:region:{token(seed,sector,'nebula')}",
            "position_light_years":[round(rng.between(-24,24),6) for _ in range(3)],
            "ground_truth":environmental_region(f"{seed}|{sector}","nebula"),
            "canonical_reserved":False,
        })
    result={
        "schema_version":"1.0.0",
        "generator":{"id":"trek_astro_sector_v1","version":"1.0.0"},
        "region":{"sector":sector,"era":era,"date":date,
                  "seed_hash":token(seed,sector,length=32),
                  "reference_frame":"local_cartesian_light_years_approx",
                  "generated_systems":systems},
        "systems":systems_out,
        "standalone_objects":extras,
        "materialization_policy":"AUTHORITATIVE_INITIAL_STATE_ONLY; COMMIT/LOAD THROUGH CORERPG",
    }
    return result

def public_sector_index(sector: dict) -> dict:
    """No science truth in discovery-side index: even system names can be hidden."""
    return {
        "sector":sector["region"]["sector"],
        "system_positions":[x["position_light_years"] for x in sector["systems"]],
        "candidate_counts":{"stellar_anchors":len(sector["systems"])},
        "not_observer_knowledge":"host_only_locator; must pass through Sensors before UI",
    }

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--seed",required=True)
    p.add_argument("--sector",default="041")
    p.add_argument("--systems",type=int,default=5)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=generate_sector(a.seed,a.sector,systems=a.systems)
    data=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(data,encoding="utf-8")
    else:
        print(data)

if __name__=="__main__":
    main()
