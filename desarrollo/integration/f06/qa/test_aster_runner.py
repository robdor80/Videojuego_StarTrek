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
    assert len(initial["attention_contacts"]) == initial["attention"], initial
    assert initial["interference_em"]==0,initial
    assert initial["config"][:3] == [1000, 1000, 0], initial
    assert initial["diagnostic"][0] == 1, initial
    assert all(len(c)==12 for c in initial["contacts"]),initial
    if len(initial["science"]) != 6:
        p.terminate()
        p.wait(timeout=5)
        diagnostics = p.stderr.read() if p.stderr else ""
        raise AssertionError((
            "Aster must have six real Core reports, no skipped planet",
            initial["science"], initial.get("science_issues"), diagnostics,
        ))
    assert any(r[1]==1 and r[3]==1 for r in initial["science"]), "provisional M class must come from Core"
    assert any(r[1]==3 for r in initial["science"]), "Core must report a measured gas giant as class J"
    assert all(r[0] in {c[0] for c in initial["contacts"]} for r in initial["science"])
    assert all(c[3]==0 for c in initial["contacts"] if c[1]==13),"planet class cannot occupy ship class field"
    assert all(c[3]!=0 for c in initial["contacts"] if c[1] in (1,2)), (
        "The Enterprise-D must classify every observable uncloaked ship at first detection",
        initial["contacts"])
    assert any(c[1]==1 and c[3]==18 for c in initial["contacts"]), (
        "The civilian transport must be identified without waiting for a long scan")
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
    planet = next(r[0] for r in initial["science"] if r[1] == 1)
    focused=say(p,f"FOCUS {planet}")
    assert any(r[0]==planet for r in focused["science"]),focused
    diagnostic=say(p,"DIAG")
    assert diagnostic["diagnostic"][0] == 1,diagnostic
    tuned=say(p,"CONFIG 2")
    assert tuned["config"][:4] == [700, 550, 400, 2],tuned
    normal=say(p,"CONFIG 0")
    assert normal["config"][:4] == [1000, 1000, 0, 0],normal
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
    assert len(ending["attention_contacts"]) == ending["attention"], ending
    assert all(any(c[0] == cid and c[2] == 1 and c[3] == 0
                   for c in ending["contacts"])
               for cid in ending["attention_contacts"]), ending
    finish(p)

    # Precisely the same input cadence produces the same complete Core result.
    p,repeat=start(runner)
    second_planet=next(r[0] for r in repeat["science"] if r[1]==1)
    assert second_planet==planet
    say(p,f"FOCUS {second_planet}")
    say(p,"DIAG")
    say(p,"CONFIG 2")
    say(p,"CONFIG 0")
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

    # Regression from the live human guard: requesting a detailed scan
    # while automatic Aster work is active must NOT require pausing time.
    p,running=start(runner)
    running=say(p,"STEP 15")
    auto_running=[j for j in running["scans"] if j[5]==1]
    assert auto_running, "fixture must exercise a busy computer"
    manual_contact=running["science"][0][0]
    active_ids={j[0] for j in running["scans"]}
    admitted=say(p,f"SCAN {manual_contact}")
    manual=[j for j in admitted["scans"]
            if j[0] not in active_ids and j[1]==manual_contact]
    assert len(manual)==1 and manual[0][5]==1,admitted
    assert manual[0][3]-manual[0][2] == 20, (
        "detailed sensor analysis must finish within 20 Core seconds")
    assert admitted["tick"]==running["tick"],(
        "an officer's order must not pause or advance the guard")
    finish(p)

    # An actual officer study must reserve a native Core timed job,
    # progress on the shared clock, and yield an observed result.
    p,study_initial=start(runner)
    planet_id=study_initial["science"][0][0]
    for _ in range(42):
        say(p,"STEP 30")
    before=say(p,"STATUS")
    known={j[0] for j in before["scans"]}
    scheduled=say(p,f"SCAN {planet_id}")
    manual=[j for j in scheduled["scans"] if j[0] not in known and j[1]==planet_id]
    assert len(manual)==1 and manual[0][5]==1,scheduled
    for _ in range(8):
        after=say(p,"STEP 30")
        current=next(j for j in after["scans"] if j[0]==manual[0][0])
        if current[5]!=1:
            break
    assert current[5]==2 and current[4]!=0,after
    # Recent comparisons are produced from Core's archived observations,
    # not differences invented in the Python window.
    row=next((r for r in after["comparisons"] if r[0]==planet_id),None)
    assert row is not None and row[1]>=2,row
    assert row[2]<=row[3],row
    saved_observations=say(p,"SAVE")["comparisons"]
    say(p,"STEP 30")
    loaded_observations=say(p,"LOAD")["comparisons"]
    assert loaded_observations==saved_observations,(
        loaded_observations,saved_observations)
    finish(p)

    # A Klingon cruiser arrives exactly at hour 1. Its classification must
    # be available in that *same* Core observation, with no timed scan.
    p,starting=start(runner)
    starting_naval={c[0] for c in starting["contacts"] if c[1]==1 and c[2]==1}
    incident=say(p,"STEP 3600")
    klingons=[c for c in incident["contacts"]
              if c[1]==1 and c[2]==1 and c[3]==16
              and c[0] not in starting_naval]
    assert len(klingons)==1,("new Klingon cruiser not identified immediately",incident)
    assert any(ev[0]==1 and ev[1]==klingons[0][0] for ev in incident["events"]), (
        "arrival notification missing", incident["events"])
    assert all(c[3]!=0 for c in incident["contacts"] if c[1]==1 and c[2]==1), (
        "uncloaked naval class still pending after acquisition",incident["contacts"])

    # New observations, not the hidden host route, drive motion. The first
    # change is closing without intercept; at 20 seconds Klingon alters its
    # actual course toward our own ship.
    t5=say(p,"STEP 5")
    tracked=next(row for row in t5["navigation"] if row[0]==klingons[0][0])
    assert tracked[2]==270 and tracked[3]==1 and tracked[4]==0,tracked
    t10=say(p,"STEP 5")
    tracked=next(row for row in t10["navigation"] if row[0]==klingons[0][0])
    assert tracked[3]==1 and tracked[4]==0,tracked
    t20=say(p,"STEP 10")
    tracked=next(row for row in t20["navigation"] if row[0]==klingons[0][0])
    assert tracked[3]==1 and tracked[4]==1,tracked
    assert any(e[0]==2 and e[1]==klingons[0][0] and e[2]==3620
               for e in t20["navigation_alerts"]), t20["navigation_alerts"]
    tactical=say(p,"TACTICAL")
    assert tactical["navigation"]==t20["navigation"],(
        "tactical must see the identical Core sensor snapshot")
    assert tactical["navigation_alerts"]==t20["navigation_alerts"],(
        "tactical must see the same maneuver alerts")
    assert tactical["contacts"]==t20["contacts"],(
        "sensor identity must not be reinterpreted by Tactical")
    saved=say(p,"SAVE")
    s30=say(p,"STEP 30")
    assert any(e[0]==1 and e[1]==klingons[0][0]
               for e in s30["navigation_alerts"]), (
        "new course change not announced")
    restored=say(p,"LOAD")
    assert restored["navigation"]==saved["navigation"]
    assert restored["navigation_alerts"]==saved["navigation_alerts"]
    finish(p)

    p,_=start(runner)
    change=say(p,"RESTART 2")
    assert change["mode"]==2
    change=say(p,"STEP 3600")
    assert change["tick"]==3600 and change["interference_em"]==550,change
    change=say(p,"STEP 3600")
    assert change["tick"]==7200 and change["interference_em"]==0,change
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
