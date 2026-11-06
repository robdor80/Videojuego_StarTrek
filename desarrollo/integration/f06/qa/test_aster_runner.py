#!/usr/bin/env python3
"""Headless CI smoke test of the actual native CoreRPG Aster runner protocol."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess

def start(runner: Path):
    p=subprocess.Popen([str(runner)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,encoding="utf-8",bufsize=1)
    assert p.stdout and p.stdin
    initial=json.loads(p.stdout.readline())
    assert initial["ok"] and initial["tick"]==0,initial
    assert initial["automatic"]==1 and initial["active"]>=15,initial
    assert initial["running"] in (1,2),initial
    return p,initial

def say(p,command: str):
    assert p.stdin and p.stdout
    p.stdin.write(command+"\n")
    p.stdin.flush()
    result=json.loads(p.stdout.readline())
    assert result["ok"],(command,result)
    return result

def finish(p):
    assert p.stdin
    p.stdin.close()
    rc=p.wait(timeout=20)
    assert rc==0,(rc,p.stderr.read() if p.stderr else "")

def run(runner: Path):
    p,initial=start(runner)
    first=say(p,"STEP 300")
    assert first["tick"]==300 and first["completed"]>=1,first
    saved=say(p,"SAVE")
    mid=say(p,"STEP 600")
    assert mid["tick"]==900
    restored=say(p,"LOAD")
    assert restored["tick"]==300
    repeated=say(p,"STEP 600")
    assert repeated["completed"]==mid["completed"]
    assert repeated["contacts"]==mid["contacts"]
    assert repeated["running"]==mid["running"]
    ending=say(p,"STEP 28800")
    assert ending["tick"]==28800 and ending["active"]>=15,ending
    finish(p)

    # Precisely the same input cadence produces the same complete Core result.
    p,repeat=start(runner)
    same=say(p,"STEP 300")
    say(p,"SAVE")
    copy=say(p,"STEP 600")
    final=say(p,"STEP 28800")
    assert initial["contacts"]==repeat["contacts"]
    assert same["completed"]==first["completed"]
    assert copy["contacts"]==mid["contacts"]
    assert final["completed"]==ending["completed"]
    assert final["contacts"]==ending["contacts"]
    finish(p)

    p,_=start(runner)
    change=say(p,"RESTART 2")
    assert change["mode"]==2
    change=say(p,"STEP 3600")
    assert change["tick"]==3600
    change=say(p,"STEP 3600")
    assert change["tick"]==7200
    finish(p)

    p,_=start(runner)
    say(p,"RESTART 3")
    fault=say(p,"STEP 7200")
    assert fault["tick"]==7200 and fault["offline"]==1,fault
    restored=say(p,"STEP 1800")
    assert restored["tick"]==9000 and restored["offline"]==0,restored
    finish(p)
    print("PASS native Aster GUI protocol: baseline/repeat, save/load, field, outage/recovery")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--runner",type=Path,required=True)
    a=parser.parse_args()
    run(a.runner.resolve())
if __name__=="__main__":
    main()
