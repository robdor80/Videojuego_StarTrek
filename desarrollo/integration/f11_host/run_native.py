#!/usr/bin/env python3
"""Build F11 Host reader against real product DLL and verify 17 native CTest cases.

Uses the exact pinned CoreRPG checkout. All temporary outputs must live under
the project's ignored laboratorios/ tree, never outside the repository.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[3]
EXPECTED={"f11."+name for name in (
    "promotion", "negatives", "authority", "identity", "idempotency",
    "atomic", "corrupt", "legacy", "history", "abi", "process_save",
    "process_load", "product_bridge", "host_before", "host_after",
    "host_access", "host_legacy"
)}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core-source",required=True,type=Path)
    parser.add_argument("--output",required=True,type=Path)
    parser.add_argument("--parallel",type=int,default=3)
    args=parser.parse_args()
    output=args.output.resolve()
    if not output.is_relative_to((ROOT/"laboratorios").resolve()):
        raise RuntimeError("All runtime artifacts must stay under ignored laboratorios/")
    output.mkdir(parents=True,exist_ok=False)
    sha=subprocess.check_output(["git","-C",str(args.core_source),"rev-parse","HEAD"],text=True).strip()
    expected=(ROOT/"desarrollo/integration/f05/core-revision.txt").read_text().strip()
    if sha!=expected or subprocess.check_output(["git","-C",str(args.core_source),"status","--porcelain"]):
        raise RuntimeError("Host reader requires clean approved F11/F05 Core pin")
    env={**os.environ,"PYTHONPYCACHEPREFIX":str(output/"pycache"),
         "F04_TEST_TEMP_ROOT":str(output/"reference-temp")}
    record={"phase":"F11-P05-A02-03","scope":"READ_ONLY_NATIVE_HOST_ADAPTER",
            "utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "platform":platform.platform(),"core_revision":sha,
            "result":"INCOMPLETE","commands":[]}

    def run(name,command):
        record["commands"].append(command)
        with (output/(name+".log")).open("w",encoding="utf-8") as log:
            result=subprocess.run(command,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"{name} failed ({result.returncode}); inspect {output / (name+'.log')}")
    try:
        run("configure",["cmake","-S",str(ROOT/"desarrollo/integration/f11_host"),
                          "-B",str(output/"build"),"-DCMAKE_BUILD_TYPE=Release",
                          "-DCORERPG_SOURCE_DIR="+str(args.core_source.resolve())])
        paths=list((output/"build/CMakeFiles").glob("*/CMakeCXXCompiler.cmake"))
        if len(paths)!=1:
            raise RuntimeError("No unambiguous compiler metadata")
        compiler=paths[0].read_text()
        match=re.search(r'set\(CMAKE_CXX_COMPILER_ID "([^"]+)"\)',compiler)
        if not match:
            raise RuntimeError("Unknown compiler")
        record["compiler_id"]=match.group(1)
        if os.name=="nt" and record["compiler_id"]!="MSVC":
            raise RuntimeError("Windows Host CI must use MSVC")
        run("build",["cmake","--build",str(output/"build"),"--config","Release",
                     "--parallel",str(args.parallel),"--target",
                     "f11_tests","f11_product_tests","f11_host_reader_tests"])
        run("tests",["ctest","--test-dir",str(output/"build"),"-C","Release",
                     "-R",r"^f11\.","--no-tests=error","--output-on-failure",
                     "--output-junit",str(output/"tests.xml")])
        cases=ET.parse(output/"tests.xml").getroot().findall(".//testcase")
        found={case.attrib.get("name") for case in cases}
        if len(cases)!=17 or found!=EXPECTED:
            raise RuntimeError("Missing/duplicated native cases: "+repr(sorted(EXPECTED-found)))
        if any(case.find(tag) is not None for case in cases for tag in ("failure","error","skipped")):
            raise RuntimeError("Failure, error or skipped native case")
        if any(case.attrib.get("status")!="run" for case in cases):
            raise RuntimeError("Native case not executed")
        record.update(result="PASS",tests=17,cases=sorted(found),
                      production_issuer_implemented=False,unreal_certified=False)
    finally:
        (output/"run.json").write_text(json.dumps(record,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"result":record["result"],"tests":record.get("tests",0),
                      "compiler":record.get("compiler_id","unknown")}))

if __name__=="__main__":
    main()
