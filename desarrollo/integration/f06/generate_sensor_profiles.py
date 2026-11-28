#!/usr/bin/env python3
"""Generate tested Star Trek-only numeric sensor balance table, not canon."""
import argparse
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/"sistemas/gameplay/ship_operations/consoles/sensors/sensor_capability_profiles_f06.json"
FIELDS=["short_permille","long_permille","focus_permille","interference_resistance_permille","tracking_slots"]
def generate(source=SOURCE):
    data=json.loads(Path(source).read_text(encoding="utf-8"))
    rows=data["profiles"]
    if len(rows)!=5 or [r["id"] for r in rows]!=[1,2,3,4,5]:
        raise ValueError("Expected five stable profile IDs, ordered")
    for row in rows:
        if any(not isinstance(row.get(k),int) or isinstance(row[k],bool) for k in [*FIELDS,"tier"]):
            raise ValueError("Noninteger sensor balance fields")
        if any(not 0<=row[k]<=1000 for k in FIELDS[:4]) or not 1<=row["tracking_slots"]<=64:
            raise ValueError("Out-of-range sensor balance")
        if row["tier"]!=row["id"] or not row.get("ship_class"):
            raise ValueError("Invalid source class and tier")
    for key in FIELDS:
        if key=="tracking_slots": continue
        if any(rows[i][key]>=rows[i+1][key] for i in range(4)):
            raise ValueError(f"Profiles not strictly ordered: {key}")
    if rows[4].get("configuration")!="enterprise_d_geordi_refit" or not rows[4].get("independent_arrays"):
        raise ValueError("Galaxy refit identity not distinguished from class")
    result=["// GENERATED from sensor_capability_profiles_f06.json; DO NOT EDIT",
            "#pragma once",
            "struct F06ProfileNumbers { unsigned id,tier,short_permille,long_permille,focus_permille,interference_resistance_permille,tracking_slots; };",
            "static constexpr F06ProfileNumbers F06_PROFILE_NUMBERS[] = {"]
    for row in rows:
        result.append("  {"+",".join(str(row[k]) for k in ["id","tier",*FIELDS])+"},")
    result.append("};")
    return "\n".join(result)+"\n"
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",required=True,type=Path)
    args=p.parse_args()
    output=generate()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(output,encoding="utf-8")
    print("Generated 5 strictly ordered Star Trek sensor balance profiles")
if __name__=="__main__":
    main()
