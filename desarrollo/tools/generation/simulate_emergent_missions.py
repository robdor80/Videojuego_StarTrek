#!/usr/bin/env python3
"""P2-B09: misión emergente de referencia OFFLINE. No hay escritor CoreRPG/HOST ni scheduler."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

VERSION = "0.1.0"
CLEARANCE = {"public": 0, "restricted": 1, "classified": 2}
SCOPES = {"propose", "authorize", "assign", "complete", "cancel", "communicate", "grant_order"}
KINDS = {"propose", "authorize", "assign", "complete", "cancel", "communicate"}
MISSION_STATES = {"proposed", "authorized", "assigned", "completed", "cancelled"}
EVENT_FIELDS = {
    "propose": {"need_ref", "asset_ref"},
    "authorize": {"mission_ref", "order_ref", "policy_ref"},
    "assign": {"mission_ref", "order_ref", "reservation_ref", "policy_ref"},
    "complete": {"mission_ref", "outcome_ref", "resolution_ref"},
    "cancel": {"mission_ref", "cancel_ref"},
    "communicate": {"need_ref", "recipient_ref", "classification", "arrival_tick"},
}
COMMON = {"event_id", "kind", "actor_ref", "tick", "trigger"}
PROHIBITED = {"player_distance", "player_presence", "camera_distance", "lod",
              "mission_spawn_reason", "world_delta", "inventory_delta", "population_delta",
              "damage_delta", "sovereignty_delta", "technology_unlock", "war_declaration",
              "create_route", "create_need", "force_outcome", "reward_grant"}


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def ident(value, name):
    require(isinstance(value, str) and bool(value.strip()), "invalid_" + name)
    return value


def clock(value, name):
    require(type(value) is int and value >= 0, "invalid_" + name)
    return value


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def mission_id(campaign, need_ref, asset_ref):
    return "p2b09:" + ident(campaign, "campaign") + ":" + ident(need_ref, "need") + ":" + ident(asset_ref, "asset")


def validate(state):
    require(isinstance(state, dict), "invalid_state")
    for field in ("campaign_id", "cutoff_tick", "last_tick", "locations", "routes",
                  "actors", "assets", "facts", "missions", "messages", "events", "reserved_ids"):
        require(field in state, "missing_" + field)
    ident(state["campaign_id"], "campaign")
    clock(state["cutoff_tick"], "cutoff")
    clock(state["last_tick"], "last_tick")
    require(state["last_tick"] >= state["cutoff_tick"], "clock_before_cutoff")
    for field in ("locations", "routes", "actors", "assets", "facts", "missions"):
        require(isinstance(state[field], dict), "invalid_map_" + field)
    for field in ("messages", "events", "reserved_ids"):
        require(isinstance(state[field], list), "invalid_list_" + field)
    require(len(state["reserved_ids"]) == len(set(state["reserved_ids"])), "duplicate_reservation")
    for location, spec in state["locations"].items():
        ident(location, "location")
        require(isinstance(spec, dict) and type(spec.get("prewarp")) is bool
                and isinstance(spec.get("jurisdiction_ref"), str)
                and bool(spec["jurisdiction_ref"]), "invalid_location")
    for route, spec in state["routes"].items():
        ident(route, "route")
        require(isinstance(spec, dict)
                and spec.get("destination_ref") in state["locations"]
                and spec.get("origin_ref") in state["locations"]
                and spec.get("status") in {"open", "closed"}, "invalid_route")
    for actor, spec in state["actors"].items():
        ident(actor, "actor")
        require(isinstance(spec, dict) and spec.get("clearance") in CLEARANCE
                and isinstance(spec.get("scopes"), list)
                and set(spec["scopes"]) <= SCOPES
                and len(spec["scopes"]) == len(set(spec["scopes"]))
                and isinstance(spec.get("known_need_refs"), list)
                and len(spec["known_need_refs"]) == len(set(spec["known_need_refs"])),
                "invalid_actor")
    for asset, spec in state["assets"].items():
        ident(asset, "asset")
        require(isinstance(spec, dict) and spec.get("location_ref") in state["locations"]
                and isinstance(spec.get("owner_ref"), str) and bool(spec["owner_ref"])
                and type(spec.get("available")) is bool
                and isinstance(spec.get("capabilities"), list)
                and all(isinstance(v, str) and bool(v) for v in spec["capabilities"])
                and len(spec["capabilities"]) == len(set(spec["capabilities"])),
                "invalid_asset")
    for ref, fact in state["facts"].items():
        ident(ref, "fact")
        require(isinstance(fact, dict) and fact.get("status") == "accepted"
                and fact.get("campaign_id") in {state["campaign_id"], "canonical"},
                "unaccepted_or_foreign_fact")
        clock(fact.get("tick"), "fact_tick")
        kind = fact.get("kind")
        require(kind in {"consequence", "need", "need_resolved", "order", "reservation",
                         "policy_review", "outcome_report", "cancel_order"}, "invalid_fact_kind")
        if kind == "need":
            require(fact.get("location_ref") in state["locations"]
                    and fact.get("requested_by_ref") in state["actors"]
                    and fact.get("cause_ref") in state["facts"]
                    and state["facts"][fact["cause_ref"]].get("kind") == "consequence"
                    and state["facts"][fact["cause_ref"]].get("tick", 10**30) <= fact["tick"]
                    and isinstance(fact.get("required_capabilities"), list)
                    and len(fact["required_capabilities"]) > 0
                    and all(isinstance(v, str) and bool(v) for v in fact["required_capabilities"])
                    and len(set(fact["required_capabilities"])) == len(fact["required_capabilities"])
                    and fact.get("classification") in CLEARANCE
                    and fact.get("route_ref") in state["routes"], "invalid_need")
            require(state["routes"][fact["route_ref"]]["destination_ref"]
                    == fact["location_ref"], "need_route_destination_mismatch")
        if kind == "need_resolved":
            require(fact.get("need_ref") in state["facts"]
                    and state["facts"][fact["need_ref"]].get("kind") == "need", "invalid_resolution")
    for actor, spec in state["actors"].items():
        require(all(ref in state["facts"] and state["facts"][ref].get("kind") == "need"
                    for ref in spec["known_need_refs"]), "unknown_initial_knowledge")
    for mid, mission in state["missions"].items():
        ident(mid, "mission")
        require(isinstance(mission, dict) and mission.get("mission_id") == mid
                and mission.get("state") in MISSION_STATES
                and mission.get("need_ref") in state["facts"]
                and state["facts"][mission["need_ref"]].get("kind") == "need"
                and mission.get("asset_ref") in state["assets"]
                and mission.get("originator_ref") in state["actors"], "invalid_mission")
        require(mid == mission_id(state["campaign_id"], mission["need_ref"],
                                  mission["asset_ref"]), "unstable_mission_id")
    seen, last = set(), -1
    for entry in state["events"]:
        require(isinstance(entry, dict) and set(entry) == {"event_id", "tick", "request", "digest"},
                "invalid_event_record")
        ident(entry["event_id"], "event_id")
        t = clock(entry["tick"], "event_tick")
        require(last <= t <= state["last_tick"] and entry["event_id"] not in seen,
                "history_order_or_duplicate")
        require(isinstance(entry["request"], dict)
                and entry["request"].get("event_id") == entry["event_id"]
                and entry["request"].get("tick") == t
                and entry["digest"] == digest({k: v for k, v in entry.items() if k != "digest"}),
                "tampered_history")
        seen.add(entry["event_id"])
        last = t
    for message in state["messages"]:
        require(isinstance(message, dict)
                and message.get("sender_ref") in state["actors"]
                and message.get("recipient_ref") in state["actors"]
                and message.get("need_ref") in state["facts"]
                and state["facts"][message["need_ref"]].get("kind") == "need"
                and message.get("classification") in CLEARANCE, "invalid_message")
        require(clock(message.get("arrival_tick"), "arrival") >= clock(message.get("sent_tick"), "sent"),
                "negative_message_delay")
    return True


def source(state, ref, kind, at):
    fact = state["facts"].get(ident(ref, "source_ref"))
    require(fact is not None and fact.get("kind") == kind and fact.get("tick") <= at,
            "missing_or_future_" + kind)
    return fact


def open_need(state, ref, at):
    need = source(state, ref, "need", at)
    source(state, need["cause_ref"], "consequence", at)
    for fact in state["facts"].values():
        if fact.get("kind") == "need_resolved" and fact.get("need_ref") == ref and fact["tick"] <= at:
            return False
    return True


def known(state, actor, need_ref, at):
    if need_ref in state["actors"][actor]["known_need_refs"]:
        return state["facts"][need_ref]["tick"] <= at
    return any(msg["recipient_ref"] == actor and msg["need_ref"] == need_ref
               and msg["arrival_tick"] <= at and msg["classification"] in CLEARANCE
               and CLEARANCE[state["actors"][actor]["clearance"]] >= CLEARANCE[msg["classification"]]
               for msg in state["messages"])


def can_screen(state, actor_ref, need_ref, asset_ref, at):
    """Non-authoritative candidate: does not reserve, assign or mutate any world resources."""
    validate(state)
    clock(at, "screen_tick")
    reasons = []
    actor = state["actors"].get(actor_ref)
    need = state["facts"].get(need_ref)
    asset = state["assets"].get(asset_ref)
    if not actor or "propose" not in actor["scopes"]:
        reasons.append("no_proposal_authority")
    if not need or need.get("kind") != "need" or need.get("tick", 10**30) > at:
        reasons.append("no_accepted_need")
    else:
        if not open_need(state, need_ref, at):
            reasons.append("need_already_resolved")
        if not actor or not known(state, actor_ref, need_ref, at):
            reasons.append("need_not_known")
        elif CLEARANCE[actor["clearance"]] < CLEARANCE[need["classification"]]:
            reasons.append("insufficient_clearance")
        if not asset:
            reasons.append("asset_not_existing")
        else:
            if not asset["available"]:
                reasons.append("asset_unavailable")
            if set(need["required_capabilities"]) - set(asset["capabilities"]):
                reasons.append("missing_capabilities")
            if state["routes"][need["route_ref"]]["status"] != "open":
                reasons.append("existing_route_closed")
            if state["routes"][need["route_ref"]]["origin_ref"] != asset["location_ref"]:
                reasons.append("asset_not_on_route_origin")
            if any(m["need_ref"] == need_ref and m["state"] == "assigned"
                   for m in state["missions"].values()):
                reasons.append("need_already_assigned")
            if any(m["asset_ref"] == asset_ref and m["state"] == "assigned"
                   for m in state["missions"].values()):
                reasons.append("asset_already_assigned")
    return {"status": "CANDIDATE" if not reasons else "NO_MISSION",
            "reasons": reasons, "need_ref": need_ref, "asset_ref": asset_ref,
            "mission_id": mission_id(state["campaign_id"], need_ref, asset_ref)
            if need and need.get("kind") == "need" and asset else None}


def valid_order(state, ref, purpose, mission, actor, at):
    order = source(state, ref, "order", at)
    require(order.get("purpose") == purpose and order.get("mission_ref") == mission["mission_id"]
            and order.get("need_ref") == mission["need_ref"]
            and order.get("asset_ref") == mission["asset_ref"]
            and order.get("actor_ref") == actor and order.get("approved") is True,
            "order_scope_or_subject_mismatch")
    approver = order.get("approved_by_ref")
    require(approver in state["actors"] and approver != actor
            and "grant_order" in state["actors"][approver]["scopes"], "no_independent_order_issuer")
    need = state["facts"][mission["need_ref"]]
    loc = state["locations"][need["location_ref"]]
    require(order.get("jurisdiction_ref") == loc["jurisdiction_ref"], "wrong_jurisdiction")
    return order


def prime_gate(state, mission, at, policy_ref):
    location = state["locations"][state["facts"][mission["need_ref"]]["location_ref"]]
    if location["prewarp"]:
        require(policy_ref is not None, "prime_directive_exception_required")
        p = source(state, policy_ref, "policy_review", at)
        require(p.get("mission_ref") == mission["mission_id"]
                and p.get("decision") == "approved_exception"
                and p.get("jurisdiction_ref") == location["jurisdiction_ref"],
                "prime_directive_not_approved")
    else:
        require(policy_ref is None, "unnecessary_policy_reference")


def apply(state, request):
    """Atomic reducer: fixture facts are synthetic; no WorldState mutation or real mission start."""
    validate(state)
    require(isinstance(request, dict), "invalid_request")
    kind = request.get("kind")
    require(kind in KINDS and set(request) == COMMON | EVENT_FIELDS[kind],
            "invalid_event_fields")
    require(not (set(request) & PROHIBITED), "prohibited_player_or_world_input")
    eid = ident(request.get("event_id"), "event_id")
    actor = ident(request.get("actor_ref"), "actor")
    at = clock(request.get("tick"), "tick")
    require(request.get("trigger") == "world", "player_or_script_trigger_forbidden")
    history = next((item for item in state["events"] if item["event_id"] == eid), None)
    if history:
        require(history["request"] == request, "event_id_payload_conflict")
        return copy.deepcopy(state)
    require(at >= state["cutoff_tick"] and at >= state["last_tick"], "retroactive_event")
    require(actor in state["actors"] and kind in state["actors"][actor]["scopes"],
            "actor_scope_denied")
    new = copy.deepcopy(state)
    if kind == "propose":
        nid = ident(request["need_ref"], "need")
        aid = ident(request["asset_ref"], "asset")
        verdict = can_screen(new, actor, nid, aid, at)
        require(verdict["status"] == "CANDIDATE", "candidate_blocked:" + ",".join(verdict["reasons"]))
        mid = verdict["mission_id"]
        require(mid not in new["reserved_ids"], "reserved_mission_identity")
        require(mid not in new["missions"], "mission_already_exists")
        new["missions"][mid] = {"mission_id": mid, "need_ref": nid, "asset_ref": aid,
                                "originator_ref": actor, "opened_tick": at, "state": "proposed"}
    elif kind == "communicate":
        nid = ident(request["need_ref"], "need")
        recipient = ident(request["recipient_ref"], "recipient")
        require(recipient in new["actors"], "recipient_unknown")
        need = source(new, nid, "need", at)
        require(known(new, actor, nid, at), "sender_does_not_know_need")
        level = request["classification"]
        require(level in CLEARANCE and CLEARANCE[level] >= CLEARANCE[need["classification"]]
                and CLEARANCE[level] <= min(CLEARANCE[new["actors"][actor]["clearance"]],
                                            CLEARANCE[new["actors"][recipient]["clearance"]]),
                "confidentiality_violation")
        arrival = clock(request["arrival_tick"], "arrival")
        require(arrival >= at, "negative_delivery_delay")
        new["messages"].append({"sender_ref": actor, "recipient_ref": recipient,
                                "need_ref": nid, "classification": level, "sent_tick": at,
                                "arrival_tick": arrival, "reported_open": open_need(new, nid, at)})
    else:
        mid = ident(request["mission_ref"], "mission")
        require(mid in new["missions"], "unknown_mission")
        m = new["missions"][mid]
        if kind == "authorize":
            require(m["state"] == "proposed", "wrong_lifecycle_state")
            require(open_need(new, m["need_ref"], at), "need_no_longer_exists")
            valid_order(new, request["order_ref"], "authorize", m, actor, at)
            prime_gate(new, m, at, request["policy_ref"])
            m["authorization_ref"] = request["order_ref"]
            m["state"] = "authorized"
        elif kind == "assign":
            require(m["state"] == "authorized", "wrong_lifecycle_state")
            require(open_need(new, m["need_ref"], at), "need_no_longer_exists")
            valid_order(new, request["order_ref"], "assign", m, actor, at)
            prime_gate(new, m, at, request["policy_ref"])
            r = source(new, request["reservation_ref"], "reservation", at)
            require(r.get("purpose") == "mission_assignment"
                    and r.get("mission_ref") == mid and r.get("asset_ref") == m["asset_ref"]
                    and r.get("granted_by_ref") in new["actors"]
                    and "grant_order" in new["actors"][r["granted_by_ref"]]["scopes"]
                    and r["granted_by_ref"] != actor, "invalid_external_reservation")
            require(new["assets"][m["asset_ref"]]["available"], "asset_unavailable")
            require(new["routes"][new["facts"][m["need_ref"]]["route_ref"]]["status"] == "open",
                    "route_closed")
            require(new["routes"][new["facts"][m["need_ref"]]["route_ref"]]["origin_ref"]
                    == new["assets"][m["asset_ref"]]["location_ref"], "asset_not_on_route_origin")
            require(not any(x["need_ref"] == m["need_ref"] and x["state"] == "assigned"
                            for key, x in new["missions"].items() if key != mid),
                    "need_already_assigned")
            require(not set(new["facts"][m["need_ref"]]["required_capabilities"])
                    - set(new["assets"][m["asset_ref"]]["capabilities"]), "asset_unqualified")
            require(not any(x["asset_ref"] == m["asset_ref"] and x["state"] == "assigned"
                            for key, x in new["missions"].items() if key != mid),
                    "double_assignment")
            require(not any(x.get("reservation_ref") == request["reservation_ref"]
                            for x in new["missions"].values()), "reservation_reuse")
            m["reservation_ref"] = request["reservation_ref"]
            m["assignment_order_ref"] = request["order_ref"]
            m["state"] = "assigned"
        elif kind == "complete":
            require(m["state"] == "assigned", "wrong_lifecycle_state")
            outcome = source(new, request["outcome_ref"], "outcome_report", at)
            resolution = source(new, request["resolution_ref"], "need_resolved", at)
            require(outcome.get("mission_ref") == mid
                    and outcome.get("result") == "verified"
                    and resolution.get("need_ref") == m["need_ref"]
                    and resolution["tick"] >= m["opened_tick"], "unverified_completion")
            m["state"] = "completed"
            m["outcome_ref"] = request["outcome_ref"]
            m["resolution_ref"] = request["resolution_ref"]
        elif kind == "cancel":
            require(m["state"] in {"proposed", "authorized", "assigned"}, "wrong_lifecycle_state")
            cancellation = source(new, request["cancel_ref"], "cancel_order", at)
            require(cancellation.get("mission_ref") == mid
                    and cancellation.get("actor_ref") == actor
                    and cancellation.get("approved_by_ref") in new["actors"]
                    and "grant_order" in new["actors"][cancellation["approved_by_ref"]]["scopes"]
                    and cancellation["approved_by_ref"] != actor,
                    "unapproved_cancellation")
            m["state"] = "cancelled"
            m["cancel_ref"] = request["cancel_ref"]
    record = {"event_id": eid, "tick": at, "request": copy.deepcopy(request)}
    record["digest"] = digest(record)
    new["events"].append(record)
    new["last_tick"] = at
    validate(new)
    return new


def view(state, actor, at):
    """A delivered historical snapshot, never omniscient present-time mission knowledge."""
    validate(state)
    require(actor in state["actors"], "unknown_observer")
    clock(at, "view_tick")
    require(at <= state["last_tick"], "future_view_forbidden")
    notices = {}
    for ref in state["actors"][actor]["known_need_refs"]:
        need = state["facts"][ref]
        if need["tick"] <= at and CLEARANCE[state["actors"][actor]["clearance"]] >= CLEARANCE[need["classification"]]:
            notices[ref] = {"need_ref": ref, "as_of_tick": need["tick"], "reported_open": True}
    for msg in state["messages"]:
        if msg["recipient_ref"] == actor and msg["arrival_tick"] <= at:
            old = notices.get(msg["need_ref"])
            if old is None or msg["sent_tick"] >= old["as_of_tick"]:
                notices[msg["need_ref"]] = {"need_ref": msg["need_ref"],
                                             "as_of_tick": msg["sent_tick"],
                                             "reported_open": msg["reported_open"]}
    return {"observer_ref": actor, "at_tick": at, "delivered": sorted(notices.values(),
                                                                     key=lambda x: x["need_ref"])}


def run_fixture(fixture):
    require(fixture.get("kind") == "SYNTHETIC_NONCANONICAL", "real_world_claim_forbidden")
    initial = copy.deepcopy(fixture["state"])
    state = copy.deepcopy(initial)
    for request in fixture["events"]:
        state = apply(state, request)
    validate(state)
    return {"schema_version": VERSION, "classification": "OFFLINE_REFERENCE_ONLY",
            "campaign_id": state["campaign_id"], "mission_states": {
                k: v["state"] for k, v in sorted(state["missions"].items())},
            "event_count": len(state["events"]), "state_sha256": digest(state),
            "initial_unchanged": initial == fixture["state"],
            "views": {actor: view(state, actor, state["last_tick"])
                      for actor in fixture.get("views", [])}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True, type=Path)
    args = parser.parse_args()
    data = json.loads(args.fixture.read_text(encoding="utf-8"))
    print(json.dumps(run_fixture(data), indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
