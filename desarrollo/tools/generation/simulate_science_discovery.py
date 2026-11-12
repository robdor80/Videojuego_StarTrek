#!/usr/bin/env python3
"""P2-B06: deterministic, OFFLINE reference. Never writes CoreRPG WorldState."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

VERSION = "0.1.0"
KINDS = {"start", "observe", "validate", "review", "engineer", "order_refit",
         "complete_refit", "trial", "recognize", "share"}
PROHIBITED_FIELDS = {"player_presence", "player_distance", "lod", "camera_distance",
                     "spawn", "world_delta", "tech_band_delta", "mission_id",
                     "route_creation", "crisis_trigger", "time_travel"}
CLEARANCE = {"public": 0, "restricted": 1, "classified": 2}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def ident(value, label):
    require(isinstance(value, str) and bool(value.strip()), label + " missing")
    return value


def valid_tick(value, label):
    require(type(value) is int and value >= 0, label + " invalid")
    return value


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def record_hash(record):
    return digest({k: v for k, v in record.items() if k != "digest"})


def stable_event_id(state, kind, project_id, source_ref, ordinal="0"):
    for name, val in (("kind", kind), ("project", project_id),
                      ("source", source_ref), ("ordinal", ordinal)):
        ident(val, name)
    return "science:" + digest([VERSION, state["campaign_id"], kind, project_id,
                                source_ref, ordinal])[:24]


def validate_state(state):
    require(isinstance(state, dict), "state invalid")
    for key in ("campaign_id", "cutoff_tick", "last_tick", "entities", "authorities",
                "allocations", "facts", "reserved_ids", "projects", "designs",
                "work_orders", "installations", "recognitions", "knowledge", "events"):
        require(key in state, "missing state field " + key)
    ident(state["campaign_id"], "campaign")
    valid_tick(state["cutoff_tick"], "cutoff")
    valid_tick(state["last_tick"], "last tick")
    require(state["last_tick"] >= state["cutoff_tick"], "clock before cutoff")
    for field in ("entities", "authorities", "allocations", "facts", "projects",
                  "designs", "work_orders", "installations", "recognitions"):
        require(isinstance(state[field], dict), "invalid " + field)
    for field in ("reserved_ids", "knowledge", "events"):
        require(isinstance(state[field], list), "invalid " + field)
    require(len(set(state["reserved_ids"])) == len(state["reserved_ids"]), "duplicate reservations")
    for eid, e in state["entities"].items():
        ident(eid, "entity ID")
        require(e.get("campaign_id") in (state["campaign_id"], "canonical"),
                "foreign campaign entity")
        valid_tick(e.get("exists_tick"), "entity tick")
    for aid, scopes in state["authorities"].items():
        ident(aid, "authority actor")
        require(aid in state["entities"], "authority actor must exist")
        require(isinstance(scopes, list) and set(scopes) <= KINDS, "invalid authority scopes")
    for fid, fact in state["facts"].items():
        ident(fid, "fact")
        require(fact.get("status") == "accepted", "non-accepted fact")
        require(fact.get("campaign_id") in (state["campaign_id"], "canonical"),
                "foreign campaign fact")
        valid_tick(fact.get("tick"), "fact tick")
    for alid, alloc in state["allocations"].items():
        ident(alid, "allocation")
        require(alloc.get("accepted") is True and alloc.get("campaign_id") == state["campaign_id"],
                "invalid allocation provenance")
        valid_tick(alloc.get("tick"), "allocation tick")
        require(type(alloc.get("units")) is int and alloc["units"] >= 0, "invalid allocation units")
    seen, previous_tick = set(), -1
    for record in state["events"]:
        require(isinstance(record, dict), "invalid event record")
        ident(record.get("event_id"), "event ID")
        t = valid_tick(record.get("tick"), "record tick")
        require(t >= previous_tick and t <= state["last_tick"], "event time order")
        require(record["event_id"] not in seen, "duplicate event ID")
        require(record.get("digest") == record_hash(record), "tampered science event")
        seen.add(record["event_id"])
        previous_tick = t
    return True


def _asset(state, ref, expected, event_tick):
    ident(ref, "entity ref")
    asset = state["entities"].get(ref)
    require(asset is not None, "unknown entity")
    require(asset.get("kind") == expected, "wrong entity kind")
    require(asset["exists_tick"] <= event_tick, "entity not yet existing")
    require(asset.get("active") is True, "inactive entity")
    return asset


def _allocation(state, ref, *, at_tick, facility_ref, minimum):
    alloc = state["allocations"].get(ref)
    require(alloc is not None, "unknown allocation")
    require(alloc["tick"] <= at_tick, "future allocation")
    require(alloc.get("facility_ref") == facility_ref, "allocation facility mismatch")
    require(alloc["units"] >= minimum, "insufficient allocation")
    return alloc


def apply_event(state, event):
    """Return a fresh snapshot or reject atomically. The input is never mutated."""
    validate_state(state)
    require(isinstance(event, dict), "event invalid")
    for field in ("event_id", "kind", "actor_ref", "trigger"):
        ident(event.get(field), field)
    kind, actor, eid = event["kind"], event["actor_ref"], event["event_id"]
    require(kind in KINDS, "unsupported or other-block operation")
    require(event["trigger"] == "world", "player cannot trigger world science by proximity")
    require(not (set(event) & PROHIBITED_FIELDS), "forbidden cross-block or LOD fields")
    require(eid not in state["reserved_ids"], "canon reservation collision")
    require(actor in state["authorities"] and kind in state["authorities"][actor],
            "scientific action not authorized")
    t = valid_tick(event.get("tick"), "event tick")
    original_payload = digest(event)
    for record in state["events"]:
        if record["event_id"] == eid:
            require(record["source_digest"] == original_payload,
                    "event ID reused with different payload")
            return copy.deepcopy(state)
    require(t >= state["cutoff_tick"], "sealed pre-campaign history")
    require(t >= state["last_tick"], "non-monotonic research time")
    require(state["entities"][actor]["exists_tick"] <= t, "actor not yet existing")
    next_state = copy.deepcopy(state)
    projects, designs = next_state["projects"], next_state["designs"]

    if kind == "start":
        pid = ident(event.get("project_id"), "project")
        require(pid not in projects and pid not in state["reserved_ids"], "project ID collision")
        subject = _asset(state, event.get("subject_ref"), "subject", t)
        _asset(state, event.get("facility_ref"), "laboratory", t)
        require(subject.get("category") in ("ordinary", "omega", "wormhole", "temporal"),
                "unknown science category")
        require(event.get("discipline") in ("sensors", "materials", "life_sciences", "subspace"),
                "unknown discipline")
        hypothesis = ident(event.get("hypothesis"), "hypothesis")
        alloc_ref = ident(event.get("allocation_ref"), "allocation ref")
        _allocation(state, alloc_ref, at_tick=t, facility_ref=event["facility_ref"], minimum=2)
        require(all(p["allocation_ref"] != alloc_ref for p in projects.values()),
                "allocation already claimed")
        projects[pid] = dict(subject_ref=event["subject_ref"], facility_ref=event["facility_ref"],
                             allocation_ref=alloc_ref, discipline=event["discipline"],
                             category=subject["category"], hypothesis=hypothesis,
                             lead_ref=actor, contributors=[actor], observations=[],
                             spent=0, stage="open", classification=event.get("classification", "restricted"))
        require(projects[pid]["classification"] in CLEARANCE, "invalid classification")

    elif kind == "observe":
        p = projects.get(event.get("project_id"))
        require(p is not None and p["stage"] == "open", "project not open")
        instrument = _asset(state, event.get("instrument_ref"), "instrument", t)
        require(instrument.get("facility_ref") == p["facility_ref"]
                and instrument.get("installed") is True
                and instrument.get("calibrated") is True, "instrument not available or calibrated")
        fact_ref = ident(event.get("fact_ref"), "observation fact")
        f = state["facts"].get(fact_ref)
        require(f is not None and f.get("domain") == "observation",
                "accepted observation source required")
        require(f["tick"] <= t, "future observation")
        for field, expected in (("subject_ref", p["subject_ref"]),
                                ("instrument_ref", event["instrument_ref"]),
                                ("hypothesis", p["hypothesis"]), ("actor_ref", actor)):
            require(f.get(field) == expected, "observation provenance mismatch")
        require(f.get("result") in ("supports", "contradicts", "unknown")
                and f.get("quality") in ("usable", "degraded"), "invalid observation")
        require(fact_ref not in {o["fact_ref"] for z in projects.values()
                               for o in z["observations"]}, "observation already spent")
        budget = state["allocations"][p["allocation_ref"]]["units"]
        require(p["spent"] + 1 <= budget, "research resources exhausted")
        p["spent"] += 1
        p["observations"].append(dict(fact_ref=fact_ref, instrument_ref=event["instrument_ref"],
                                       actor_ref=actor, result=f["result"], quality=f["quality"],
                                       tick=f["tick"]))
        if actor not in p["contributors"]:
            p["contributors"].append(actor)

    elif kind == "validate":
        p = projects.get(event.get("project_id"))
        require(p is not None and p["stage"] == "open", "project not open for validation")
        supports = [o for o in p["observations"] if o["result"] == "supports"
                    and o["quality"] == "usable"]
        require(len(supports) >= 2
                and len({o["instrument_ref"] for o in supports}) >= 2
                and len({o["actor_ref"] for o in supports}) >= 2,
                "independent corroboration missing")
        require(not any(o["result"] == "contradicts" and o["quality"] == "usable"
                        for o in p["observations"]),
                "unresolved contradictory evidence")
        p["stage"] = "validated"
        p["validated_tick"] = t

    elif kind == "review":
        p = projects.get(event.get("project_id"))
        require(p is not None and p["stage"] == "validated", "unvalidated research")
        require(event.get("decision") in ("approve", "reject"), "review decision required")
        p["stage"] = "approved" if event["decision"] == "approve" else "rejected"
        p["review_actor_ref"] = actor
        p["review_tick"] = t

    elif kind == "engineer":
        p = projects.get(event.get("project_id"))
        require(p is not None and p["stage"] == "approved", "review not approved")
        require(p["category"] == "ordinary", "exceptional phenomena cannot unlock normal technology")
        did = ident(event.get("design_id"), "design ID")
        require(did not in designs and did not in state["reserved_ids"], "design collision")
        classes = event.get("compatible_classes")
        require(isinstance(classes, list) and classes
                and all(isinstance(c, str) and c.strip() for c in classes)
                and len(classes) == len(set(classes)), "explicit class compatibility required")
        require(event.get("era_approved") is True, "technology not certified for era")
        require(event.get("safety_approved") is True, "technology safety not certified")
        designs[did] = dict(project_id=event["project_id"], compatible_classes=classes,
                            institution_ref=p["review_actor_ref"], ready_tick=t,
                            classification=p["classification"])
        p["stage"] = "engineered"

    elif kind == "order_refit":
        did = ident(event.get("design_id"), "design ID")
        d = designs.get(did)
        require(d is not None, "design missing")
        ship = _asset(state, event.get("ship_ref"), "ship", t)
        _asset(state, event.get("shipyard_ref"), "shipyard", t)
        require(ship.get("class_ref") in d["compatible_classes"], "incompatible ship class")
        require(event.get("work_order_id") not in next_state["work_orders"],
                "work order exists")
        wid = ident(event.get("work_order_id"), "work order ID")
        require(wid not in state["reserved_ids"], "work order reservation collision")
        duration = event.get("duration")
        require(type(duration) is int and duration >= 2, "real refit duration required")
        alloc_ref = ident(event.get("allocation_ref"), "refit allocation")
        _allocation(state, alloc_ref, at_tick=t, facility_ref=event["shipyard_ref"], minimum=2)
        require(all(w["allocation_ref"] != alloc_ref for w in next_state["work_orders"].values()),
                "refit allocation already claimed")
        require(not any(w["ship_ref"] == event["ship_ref"] and w["design_id"] == did
                        for w in next_state["work_orders"].values()), "duplicate ship refit")
        next_state["work_orders"][wid] = dict(design_id=did, ship_ref=event["ship_ref"],
                                               shipyard_ref=event["shipyard_ref"],
                                               allocation_ref=alloc_ref, due_tick=t + duration,
                                               status="in_progress")

    elif kind == "complete_refit":
        wid = event.get("work_order_id")
        w = next_state["work_orders"].get(wid)
        require(w is not None and w["status"] == "in_progress", "refit not in progress")
        require(t >= w["due_tick"], "refit cannot finish early")
        _asset(state, w["ship_ref"], "ship", t)
        _asset(state, w["shipyard_ref"], "shipyard", t)
        w["status"] = "installed"
        key = w["ship_ref"] + ":" + w["design_id"]
        require(key not in next_state["installations"], "installation already exists")
        next_state["installations"][key] = dict(ship_ref=w["ship_ref"],
                                                  design_id=w["design_id"],
                                                  work_order_id=wid,
                                                  installed_tick=t, active=False)

    elif kind == "trial":
        key = ident(event.get("installation_ref"), "installation ref")
        i = next_state["installations"].get(key)
        require(i is not None and not i["active"], "installation not awaiting trial")
        f = state["facts"].get(event.get("fact_ref"))
        require(f is not None and f.get("domain") == "trial"
                and f.get("installation_ref") == key and f["tick"] <= t,
                "accepted installation trial evidence required")
        require(f.get("result") in ("pass", "fail"), "invalid trial result")
        require(t > i["installed_tick"], "instant trials forbidden")
        i["last_trial_ref"] = event["fact_ref"]
        if f["result"] == "pass":
            i["active"] = True
            i["commissioned_tick"] = t

    elif kind == "recognize":
        p = projects.get(event.get("project_id"))
        require(p is not None and p["stage"] in ("validated", "approved", "engineered"),
                "recognition requires validated discovery")
        pid = event["project_id"]
        require(pid not in next_state["recognitions"], "recognition already granted")
        credited = event.get("contributors")
        require(isinstance(credited, list) and credited
                and set(credited) == set(p["contributors"])
                and len(credited) == len(set(credited)), "scientific credit must include full team")
        name = ident(event.get("official_name"), "official name")
        require(event.get("institutional_approval") is True, "naming requires formal approval")
        next_state["recognitions"][pid] = dict(official_name=name, contributors=credited,
                                                authority_ref=actor, tick=t)

    elif kind == "share":
        ref = event.get("object_ref")
        available = set(projects) | set(designs) | set(next_state["recognitions"])
        require(ref in available, "unknown shared science object")
        recipient = ident(event.get("recipient_ref"), "recipient")
        require(recipient in state["entities"], "unknown knowledge recipient")
        require(state["entities"][recipient]["exists_tick"] <= t, "future recipient")
        cls = event.get("classification")
        require(cls in CLEARANCE, "invalid knowledge classification")
        p = projects.get(ref) or projects.get(designs.get(ref, {}).get("project_id"))
        require(p is not None and CLEARANCE[cls] >= CLEARANCE[p["classification"]],
                "cannot downgrade classified science")
        require(CLEARANCE[state["entities"][recipient].get("clearance", "public")] >= CLEARANCE[cls],
                "recipient lacks clearance")
        require(not any(k["recipient_ref"] == recipient and k["object_ref"] == ref
                        for k in next_state["knowledge"]), "duplicate knowledge delivery")
        next_state["knowledge"].append(dict(recipient_ref=recipient, object_ref=ref,
                                              classification=cls, tick=t, source_ref=eid))

    record = copy.deepcopy(event)
    record["source_digest"] = original_payload
    record["digest"] = record_hash(record)
    next_state["events"].append(record)
    next_state["last_tick"] = t
    validate_state(next_state)
    return next_state


def replay(state, events):
    result = copy.deepcopy(state)
    for event in events:
        result = apply_event(result, event)
    return result


def visible_knowledge(state, recipient_ref, at_tick, clearance):
    validate_state(state)
    valid_tick(at_tick, "knowledge tick")
    require(clearance in CLEARANCE, "clearance invalid")
    return [copy.deepcopy(grant) for grant in state["knowledge"]
            if grant["recipient_ref"] == recipient_ref and grant["tick"] <= at_tick
            and CLEARANCE[grant["classification"]] <= CLEARANCE[clearance]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    fixture = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    result = replay(fixture["initial_state"], fixture["events"])
    print(canonical({"events": len(result["events"]),
                     "projects": len(result["projects"]),
                     "active_installations": sum(bool(x["active"])
                         for x in result["installations"].values()),
                     "sha256": digest(result)}))


if __name__ == "__main__":
    main()
