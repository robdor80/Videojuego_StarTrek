#!/usr/bin/env python3
"""P2-B10: deterministic offline scheduling PROPOSALS only; never writes WorldState."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

VERSION = "0.1.0"
DOMAINS = {f"B{i:02d}" for i in range(1, 10)}
PRIORITIES = {"urgent": 0, "normal": 1, "background": 2}
CLASSIFICATIONS = {"public": 0, "restricted": 1, "classified": 2}
STATE_FIELDS = {"schema_version", "campaign_id", "world_revision", "tick", "config",
                "facts", "tasks", "outbox", "receipts", "journal", "trace_head", "viewers"}
TASK_FIELDS = {"domain", "intent_ref", "source_refs", "due_tick", "priority",
               "classification"}
CONFIG_FIELDS = {"budget_per_tick", "per_domain_quota", "max_batch_ticks",
                 "max_pending_outbox", "aging_ticks"}
BANNED = {"player_distance", "camera_distance", "player_present", "interest_radius",
          "lod", "world_delta", "inventory_delta", "population_delta", "ships_delta",
          "sovereignty_delta", "mission_spawn", "random_seed_override",
          "real_wallclock_seconds", "simulation_speed_multiplier"}


def require(value, reason):
    if not value:
        raise ValueError(reason)


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def nat(value):
    return type(value) is int and 0 <= value <= 10000000


def positive(value):
    return type(value) is int and 1 <= value <= 10000000


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def sha(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def genesis(campaign_id):
    return sha({"schema_version": VERSION, "campaign_id": campaign_id, "trace": "genesis"})


def dispatch_id(campaign, task_id):
    return "p2b10:" + campaign + ":" + task_id


def accepted(state, ref, kind=None):
    fact = state["facts"].get(ref)
    require(isinstance(fact, dict) and fact.get("status") == "accepted"
            and fact.get("campaign_id") == state["campaign_id"]
            and fact.get("world_revision") == state["world_revision"]
            and nonblank(fact.get("issuer_ref")), "unaccepted_or_foreign_fact")
    if kind:
        require(fact.get("kind") == kind, "wrong_fact_kind")
    require(nat(fact.get("tick")), "invalid_fact_tick")
    return fact


def validate(state):
    """Strict reference-snapshot validation. Claim 'accepted' is NOT a real CoreRPG signature."""
    require(isinstance(state, dict) and set(state) == STATE_FIELDS,
            "invalid_state_shape")
    require(state["schema_version"] == VERSION, "schema_version")
    require(nonblank(state["campaign_id"]) and nonblank(state["world_revision"]),
            "invalid_campaign_or_revision")
    require(nat(state["tick"]), "invalid_tick")
    config = state["config"]
    require(isinstance(config, dict) and set(config) == CONFIG_FIELDS, "invalid_config")
    for field in CONFIG_FIELDS:
        require(positive(config[field]), "invalid_config_" + field)
    require(config["per_domain_quota"] <= config["budget_per_tick"],
            "domain_quota_exceeds_budget")
    for field in ("facts", "tasks", "viewers"):
        require(isinstance(state[field], dict), "invalid_" + field)
    for field in ("outbox", "receipts", "journal"):
        require(isinstance(state[field], list), "invalid_" + field)

    for ref, fact in state["facts"].items():
        require(nonblank(ref), "invalid_fact_ref")
        accepted(state, ref)
        require(fact.get("kind") in {"domain_intent", "need", "clock_advance",
                                      "dispatch_receipt", "delivery"},
                "invalid_fact_kind")
    for task_id, task in state["tasks"].items():
        require(nonblank(task_id) and ":" not in task_id and
                isinstance(task, dict) and set(task) == TASK_FIELDS, "invalid_task")
        require(task["domain"] in DOMAINS and task["priority"] in PRIORITIES
                and task["classification"] in CLASSIFICATIONS
                and nat(task["due_tick"]), "invalid_task_traits")
        refs = task["source_refs"]
        require(isinstance(refs, list) and refs == sorted(set(refs))
                and len(refs) > 0 and all(nonblank(x) for x in refs),
                "invalid_causal_refs")
        require(task["intent_ref"] in refs, "intent_missing_from_sources")
        intent = accepted(state, task["intent_ref"], "domain_intent")
        require(intent.get("domain") == task["domain"] and
                intent.get("owner_ref") == task["domain"] and
                intent["tick"] <= task["due_tick"], "unowned_or_future_intent")
        require(all(accepted(state, x)["tick"] <= task["due_tick"] for x in refs),
                "future_source_fact")
        if task["domain"] == "B09":
            need_ref = intent.get("need_ref")
            require(need_ref in refs, "b09_without_need")
            accepted(state, need_ref, "need")
    for viewer, entry in state["viewers"].items():
        require(nonblank(viewer) and isinstance(entry, dict) and
                set(entry) == {"clearance"} and
                entry["clearance"] in CLASSIFICATIONS, "invalid_viewer")
    emitted, last_tick = set(), -1
    for envelope in state["outbox"]:
        require(isinstance(envelope, dict) and
                set(envelope) == {"dispatch_id", "task_id", "tick", "domain",
                                  "intent_ref", "source_refs", "classification",
                                  "authority"}, "invalid_outbox_record")
        tid = envelope["task_id"]
        require(tid in state["tasks"] and tid not in emitted, "duplicate_or_unknown_dispatch")
        task = state["tasks"][tid]
        require(envelope["dispatch_id"] == dispatch_id(state["campaign_id"], tid)
                and envelope["domain"] == task["domain"]
                and envelope["intent_ref"] == task["intent_ref"]
                and envelope["source_refs"] == task["source_refs"]
                and envelope["classification"] == task["classification"]
                and envelope["authority"] == "PROPOSAL_ONLY"
                and nat(envelope["tick"])
                and task["due_tick"] <= envelope["tick"] <= state["tick"]
                and envelope["tick"] >= last_tick, "invalid_dispatch_envelope")
        emitted.add(tid)
        last_tick = envelope["tick"]
    dispatched = {x["dispatch_id"]: x for x in state["outbox"]}
    receipt_ids = set()
    for receipt in state["receipts"]:
        require(isinstance(receipt, dict) and set(receipt) ==
                {"dispatch_id", "fact_ref", "tick"}, "invalid_receipt")
        did = receipt["dispatch_id"]
        require(did in dispatched and did not in receipt_ids
                and nat(receipt["tick"]) and receipt["tick"] <= state["tick"]
                and dispatched[did]["tick"] <= receipt["tick"],
                "invalid_receipt_dispatch")
        fact = accepted(state, receipt["fact_ref"], "dispatch_receipt")
        require(fact["tick"] == receipt["tick"] and fact.get("dispatch_id") == did
                and fact.get("result") in {"accepted", "rejected"}
                and fact.get("issuer_ref") == "core_writer",
                "untrusted_receipt")
        receipt_ids.add(did)
    require(sum(x["dispatch_id"] not in receipt_ids for x in state["outbox"])
            <= config["max_pending_outbox"], "outbox_limit_exceeded")

    prev = genesis(state["campaign_id"])
    for record in state["journal"]:
        require(isinstance(record, dict) and set(record) ==
                {"previous", "action", "digest"} and
                record["previous"] == prev and isinstance(record["action"], dict)
                and record["digest"] == sha({"previous": prev,
                                            "action": record["action"]}),
                "trace_chain_tampered")
        prev = record["digest"]
    require(state["trace_head"] == prev, "trace_head_tampered")
    return True


def record(state, action):
    prev = state["trace_head"]
    entry = {"previous": prev, "action": copy.deepcopy(action)}
    entry["digest"] = sha(entry)
    state["journal"].append(entry)
    state["trace_head"] = entry["digest"]


def priority_key(task_id, task, at, aging_ticks):
    # Aging is bounded: finite urgent work cannot indefinitely starve old low-priority tasks.
    age_bonus = (at - task["due_tick"]) // aging_ticks
    effective = max(0, PRIORITIES[task["priority"]] - age_bonus)
    return (effective, task["due_tick"], task_id)


def advance(state, to_tick, clock_ref):
    """Authorized virtual-time advance; never uses machine wall time, frame rate or camera LOD."""
    validate(state)
    require(nat(to_tick), "invalid_target_tick")
    require(nonblank(clock_ref), "invalid_clock_ref")
    start = state["tick"]
    if to_tick == start:
        # Exact request replay is allowed, but not arbitrary clock reuse.
        if any(x["action"] == {"kind": "advance", "from_tick": start,
                                "to_tick": to_tick, "clock_ref": clock_ref,
                                "emitted": []} for x in state["journal"]):
            return copy.deepcopy(state)
        raise ValueError("zero_length_advance")
    require(to_tick > start, "clock_reversal")
    require(to_tick - start <= state["config"]["max_batch_ticks"], "catchup_batch_limit")
    clock = accepted(state, clock_ref, "clock_advance")
    require(clock["tick"] <= start and clock.get("start_tick") == start
            and clock.get("end_tick") == to_tick
            and clock.get("issuer_ref") == "core_clock",
            "clock_authority_mismatch")
    require(not any(e["action"].get("clock_ref") == clock_ref for e in state["journal"]),
            "clock_authority_reuse")
    result = copy.deepcopy(state)
    dispatched_tasks = {x["task_id"] for x in result["outbox"]}
    acknowledged = {x["dispatch_id"] for x in result["receipts"]}
    emitted_ids = []
    for at in range(start + 1, to_tick + 1):
        domain_usage = {}
        budget = result["config"]["budget_per_tick"]
        ready = sorted(((tid, t) for tid, t in result["tasks"].items()
                        if tid not in dispatched_tasks and t["due_tick"] <= at),
                       key=lambda pair: priority_key(pair[0], pair[1], at,
                                                     result["config"]["aging_ticks"]))
        for tid, task in ready:
            if budget == 0:
                break
            if domain_usage.get(task["domain"], 0) >= result["config"]["per_domain_quota"]:
                continue
            pending = len(result["outbox"]) - len(acknowledged)
            if pending >= result["config"]["max_pending_outbox"]:
                break
            envelope = {"dispatch_id": dispatch_id(result["campaign_id"], tid),
                        "task_id": tid, "tick": at, "domain": task["domain"],
                        "intent_ref": task["intent_ref"],
                        "source_refs": copy.deepcopy(task["source_refs"]),
                        "classification": task["classification"],
                        "authority": "PROPOSAL_ONLY"}
            result["outbox"].append(envelope)
            dispatched_tasks.add(tid)
            emitted_ids.append(envelope["dispatch_id"])
            budget -= 1
            domain_usage[task["domain"]] = domain_usage.get(task["domain"], 0) + 1
    result["tick"] = to_tick
    record(result, {"kind": "advance", "from_tick": start,
                    "to_tick": to_tick, "clock_ref": clock_ref,
                    "emitted": emitted_ids})
    validate(result)
    return result


def acknowledge(state, dispatch_ref, receipt_ref):
    """Only records an already accepted external receipt; does NOT execute a domain effect."""
    validate(state)
    require(nonblank(dispatch_ref) and nonblank(receipt_ref), "invalid_ack_ref")
    outgoing = {x["dispatch_id"]: x for x in state["outbox"]}
    require(dispatch_ref in outgoing, "dispatch_missing")
    previous = {x["dispatch_id"]: x for x in state["receipts"]}
    if dispatch_ref in previous:
        if previous[dispatch_ref]["fact_ref"] == receipt_ref:
            return copy.deepcopy(state)
        raise ValueError("conflicting_receipt")
    fact = accepted(state, receipt_ref, "dispatch_receipt")
    require(fact.get("dispatch_id") == dispatch_ref
            and fact["tick"] >= outgoing[dispatch_ref]["tick"]
            and fact["tick"] <= state["tick"]
            and fact.get("result") in {"accepted", "rejected"}
            and fact.get("issuer_ref") == "core_writer", "untrusted_receipt")
    result = copy.deepcopy(state)
    result["receipts"].append({"dispatch_id": dispatch_ref,
                               "fact_ref": receipt_ref, "tick": fact["tick"]})
    record(result, {"kind": "acknowledge", "dispatch_id": dispatch_ref,
                    "receipt_ref": receipt_ref})
    validate(result)
    return result


def view(state, observer_ref, at_tick):
    """Explicitly delivered/cleared dispatches only; no omniscient live UI."""
    validate(state)
    require(observer_ref in state["viewers"] and nat(at_tick)
            and at_tick <= state["tick"], "invalid_view")
    level = CLASSIFICATIONS[state["viewers"][observer_ref]["clearance"]]
    allowed = set()
    for ref, fact in state["facts"].items():
        if fact["kind"] != "delivery" or fact.get("recipient_ref") != observer_ref:
            continue
        require(nat(fact.get("arrival_tick")), "invalid_delivery_tick")
        if fact["arrival_tick"] <= at_tick:
            allowed.add(fact.get("dispatch_id"))
    return {"observer_ref": observer_ref, "as_of_tick": at_tick,
            "delivered": [copy.deepcopy(x) for x in state["outbox"]
                          if x["dispatch_id"] in allowed and
                          x["tick"] <= at_tick and
                          level >= CLASSIFICATIONS[x["classification"]]]}


def run_fixture(data):
    require(isinstance(data, dict) and data.get("kind") == "SYNTHETIC_NONCANONICAL",
            "real_world_claim_forbidden")
    original = copy.deepcopy(data["state"])
    state = copy.deepcopy(original)
    validate(state)
    for action in data["actions"]:
        require(isinstance(action, dict) and action.get("kind") in
                {"advance", "acknowledge"}, "invalid_action")
        if action["kind"] == "advance":
            require(set(action) == {"kind", "to_tick", "clock_ref"}, "invalid_advance")
            state = advance(state, action["to_tick"], action["clock_ref"])
        else:
            require(set(action) == {"kind", "dispatch_ref", "receipt_ref"},
                    "invalid_ack")
            state = acknowledge(state, action["dispatch_ref"], action["receipt_ref"])
    return {"schema_version": VERSION, "authority": "OFFLINE_REFERENCE_ONLY",
            "campaign_id": state["campaign_id"], "final_tick": state["tick"],
            "dispatches": copy.deepcopy(state["outbox"]),
            "receipts": len(state["receipts"]),
            "pending": len(state["outbox"]) - len(state["receipts"]),
            "journal_entries": len(state["journal"]),
            "snapshot_sha256": sha(state), "initial_unchanged": original == data["state"],
            "views": {x: view(state, x, state["tick"]) for x in data.get("views", [])}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", required=True, type=Path)
    options = parser.parse_args()
    fixture = json.loads(options.fixture.read_text(encoding="utf-8"))
    print(json.dumps(run_fixture(fixture), ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
