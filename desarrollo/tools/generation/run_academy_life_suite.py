#!/usr/bin/env python3
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
MANIFEST=ROOT/"desarrollo/validation/consistency/academy_life_final_acceptance_manifest_v1.0.json"
def main():
 manifest=json.loads(MANIFEST.read_text(encoding="utf-8"));scripts=manifest["test_scripts"];failed=[];passed=0
 for rel in scripts:
  p=ROOT/rel
  cp=subprocess.run([sys.executable,str(p)],cwd=ROOT,text=True,capture_output=True)
  if cp.returncode==0:
   passed+=1;print(f"[PASS] {rel}")
  else:
   failed.append(rel);print(f"[FAIL] {rel}");print(cp.stdout);print(cp.stderr,file=sys.stderr)
 print(json.dumps({"test_scripts_total":len(scripts),"test_scripts_passed":passed,"test_scripts_failed":failed,"defined_tests_expected":manifest.get("total_defined_tests")},indent=2))
 return 1 if failed else 0
if __name__=="__main__":raise SystemExit(main())
