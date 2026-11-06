#!/usr/bin/env python3
"""Compile *test-only* Aster scientific instruments from authoritative Host truth.

This header is test-only and must never be installed as a production LCARS
interface. The real Sensor ABI still exposes ONLY observed contacts.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

def render(path: Path) -> str:
    world=json.loads(path.read_text(encoding="utf-8"))
    if world.get("science_generation",{}).get("generator")!="trek_astro_physical_v1":
        raise ValueError("requires validated scientific Aster host frame")
    out=[
        "// GENERATED TEST-ONLY instrument readings from Host truth.",
        "#pragma once",
        "#include <cstdint>",
        "struct F06AsterInstrument { uint32_t key,temp_k,pressure_mbar,water_permille,n2_permille,o2_permille,co2_permille,solid,bio; };",
        "inline constexpr F06AsterInstrument F06_ASTER_INSTRUMENTS[] = {",
    ]
    for e in world["entities"]:
        if e["kind"]!="planet":
            continue
        p=e["science_truth"]["physical_planet"]
        atm=p["atmosphere"]
        total=atm["mole_fraction"]
        pressure=round((atm["surface_pressure_bar"] or 0)*1000)
        temp=round(p["climate"]["surface_temperature_k"] or p["climate"]["equilibrium_temperature_k"])
        water=round(p["hydrosphere"]["surface_liquid_fraction"]*1000)
        vals=[e["key"],temp,pressure,water,*[round(total.get(k,0)*1000) for k in ("N2","O2","CO2")],
              int(atm["has_solid_surface"]),2 if p["biosphere"]["stage"]!="none" else 0]
        if sum(vals[4:7])>1000 or any(v<0 for v in vals):
            raise ValueError("invalid test scientific instrument calibration")
        out.append(" {" + ", ".join(map(str,vals)) + "},")
    if len(out)!=12:  # 6 planets plus 6 lines
        raise ValueError("expected six distinct planets")
    out.append("};")
    return "\n".join(out)+"\n"

def main() -> None:
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,type=Path)
    p.add_argument("--out",required=True,type=Path)
    a=p.parse_args()
    result=render(a.source)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(result,encoding="utf-8")

if __name__=="__main__":
    main()
