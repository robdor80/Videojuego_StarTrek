#!/usr/bin/env python3
"""LORE-03C: editorial integration integrity, never a CoreRPG runtime validator."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
CASEBOOK = "mundo/lore/historical_events/lore03c_memory_casebook_v0.1.json"
PATTERNS = "mundo/lore/historical_events/lore03c_institutional_patterns_v0.1.json"
DOCS = "proyecto/docs/roadmap/lore_03_c"
FIRSTHAND = {"direct_participation", "direct_observation"}
INDIRECT = {"explicit_disclosure", "formal_report", "authorized_record_access", "rumor", "trained", "group_conversation", "public_event"}
FALSE_REPORT = "tzenkethi_false_coup_report"

class InvalidLore03C(ValueError):
    pass

def check(value, reason):
    if not value:
        raise InvalidLore03C(reason)

def load(path, root=ROOT):
    return json.loads((root / path).read_text(encoding="utf-8"))

def context(root=ROOT):
    legacy = load("mundo/lore/diplomacy/historical_events_v0.1.json", root)["events"]
    anchors = load("mundo/lore/historical_events/lore03_a_chronology_index_v0.1.json", root)["additional_historical_anchors"]
    b = load("mundo/lore/conflicts/lore03b_dossier_index_v0.1.json", root)
    check(len(legacy) == 40 and len(anchors) == 26 and b["expected_dossiers"] == 22, "Prior lore coverage changed")
    events = {x["event_id"]: {"year": x["reference_year"], "false": x.get("status") == "FALSE_CLAIM_NOT_HISTORICAL_EVENT"} for x in legacy}
    for x in anchors:
        eid = x["event_id"]
        check(eid not in events, "LORE-03A event ID duplicates LORE-01D")
        events[eid] = {"year": x["time_anchor"]["reference_year"], "false": False}
    dossiers = {}
    for item in b["dossiers"]:
        d = load(item["ref"], root)
        check(d["conflict_id"] == item["conflict_id"], "LORE-03B dossier ID mismatch")
        dossiers[d["conflict_id"]] = set(d["major_event_refs"])
    check(events[FALSE_REPORT]["false"], "False tzenkethi report reclassified")
    return {"events": events, "dossiers": dossiers}

def validate_case(case, refs):
    ident = case.get("case_id")
    check(isinstance(ident, str) and ident, "Case has no stable ID")
    check(case.get("case_kind") == "DOCUMENTARY_HYPOTHETICAL_NOT_INSTANTIATED", ident + ": creates NPC")
    event = case.get("event_ref")
    check(event in refs["events"], ident + ": missing historical event")
    conflict = case.get("conflict_ref")
    check(conflict in refs["dossiers"] and event in refs["dossiers"][conflict],
          ident + ": event does not belong to cited conflict dossier")
    year = refs["events"][event]["year"]
    check(type(year) is int and year < 2383, ident + ": post-start/same-year event forced into history")
    actor = case.get("actor", {})
    birth = actor.get("birth_year")
    check(actor.get("identity_type") == "generated_hypothetical"
          and actor.get("canonical_identity_asserted") is False, ident + ": real person asserted")
    check(type(birth) is int and birth <= 2383, ident + ": invalid actor birth year")
    access = case.get("access", {})
    channel = access.get("channel")
    mode = case.get("remembered_as")
    check(channel in FIRSTHAND | INDIRECT and mode in {"firsthand", "learned"}, ident + ": invalid memory channel")
    if mode == "firsthand":
        check(channel in FIRSTHAND and birth < year, ident + ": implausible first-hand history")
        check(actor.get("assignment_provenance") == "ILLUSTRATIVE_SERVICE_REQUIRES_VALIDATION",
              ident + ": participation without provenance gate")
    else:
        check(channel in INDIRECT and actor.get("assignment_provenance") is None,
              ident + ": learned event misrepresented as direct service")
    classification = access.get("information_class")
    check(classification in {"public", "classified"}, ident + ": invalid classification")
    if classification == "classified":
        check(channel == "authorized_record_access" and
              access.get("authorization_evidence") == "HYPOTHETICAL_NEED_TO_KNOW_REQUIRES_CORE_VALIDATION",
              ident + ": secret leaks without need-to-know")
    else:
        check(access.get("authorization_evidence") is None, ident + ": fake clearance for public fact")
    false = refs["events"][event]["false"]
    allowed = {"FALSE_REPORT_BELIEVED", "FALSE_REPORT_CORRECTED"} if false else {"TRUE_EVENT_REPORTED", "TRUE_EVENT_PERSONAL_INTERPRETATION"}
    check(case.get("claim_status") in allowed, ident + ": false report promoted to fact or real fact denied")
    expected_world = "REPORT_NOT_ACTUAL_COUP" if false else "REFERENCES_SOURCE_FACT"
    check(case.get("world_event_claim") == expected_world, ident + ": world truth contamination")
    check(case.get("automatic_trauma") is False and case.get("automatic_relationship") is False
          and case.get("runtime_state_mutation") is False, ident + ": unapproved causal mutation")
    check(case.get("personal_consequence") == "CONDITIONAL_ON_AUTHORIZED_EVENTS", ident + ": forced consequence")
    check(len(case.get("example_es", "")) >= 55, ident + ": inadequate historical interpretation")
    return ident

def validate_pattern(p, refs):
    pid = p.get("pattern_id")
    check(isinstance(pid,str) and pid, "Institutional pattern missing ID")
    check(p.get("event_ref") in refs["events"], pid + ": unknown historical source")
    check(p.get("creation_status") == "CONDITIONAL_EDITORIAL_NOT_CREATED"
          and p.get("source_truth_preserved") is True
          and p.get("requires_authorized_institutional_event") is True
          and p.get("runtime_state_mutation") is False, pid + ": unapproved institution fact")
    check(p.get("access_policy") in {"institution_defined", "classified_need_to_know"}, pid + ": missing privacy")
    check(p.get("assert_tzenkethi_coup_happened") is False, pid + ": fictional coup was asserted")
    if p["event_ref"] == FALSE_REPORT:
        check(p.get("pattern_type") == "disinformation_review", pid + ": false coup commemorated")
    check(len(p.get("description_es","")) >= 70, pid + ": missing editorial explanation")
    return pid

def validate_sets(casebook, patterns, refs):
    check(casebook.get("status") == "NEEDS_REVIEW_DOCUMENTARY"
          and patterns.get("status") == "NEEDS_REVIEW_DOCUMENTARY", "Premature administrative COMPLETE")
    for obj in (casebook, patterns):
        check(obj.get("world_state_authority") == "CoreRPG_ONLY"
              and obj.get("gameplay_activated") is False, "Runtime/world authority breach")
    check(casebook.get("mode") == "NON_RUNTIME_DOCUMENTARY_EXAMPLES"
          and casebook.get("creates_canonical_characters") is False
          and casebook.get("creates_new_historical_events") is False
          and casebook.get("auto_bootstrap_future") is False, "Invented historical state")
    check(casebook.get("campaign_start_year_proposed") == 2383
          and casebook.get("campaign_start_exact_date") is None, "Campaign exact start date forged")
    check(patterns.get("mode") == "EDITORIAL_PATTERNS_NO_INSTANTIATION"
          and patterns.get("creates_memorials") is False
          and patterns.get("creates_policies") is False, "Institutional asset invented")
    cases = casebook.get("cases", [])
    pats = patterns.get("patterns", [])
    check(len(cases) >= 12 and len(pats) >= 6, "Insufficient cross-domain cases")
    ids = [validate_case(x,refs) for x in cases]
    pids = [validate_pattern(x,refs) for x in pats]
    check(len(ids)==len(set(ids)) and len(pids)==len(set(pids)), "Duplicated case or pattern ID")
    check(sum(x["remembered_as"]=="firsthand" for x in cases)>=3, "No veteran example")
    check(sum(x["remembered_as"]=="learned" for x in cases)>=6, "No second-hand examples")
    check(sum(x["access"]["information_class"]=="classified" for x in cases)>=1, "No classified example")
    check(any(x["event_ref"]==FALSE_REPORT and x["claim_status"]=="FALSE_REPORT_BELIEVED" for x in cases), "False rumor missing")
    check(any(x["event_ref"]==FALSE_REPORT and x["claim_status"]=="FALSE_REPORT_CORRECTED" for x in cases), "Correction missing")
    wolf = [x for x in cases if x["event_ref"]=="wolf_359_battle" and x["remembered_as"]=="firsthand"]
    check(len(wolf)>=2, "Shared event with different witnesses absent")
    return {"cases":len(cases),"institutional_patterns":len(pats),"historical_events_reused":len(refs["events"]),"conflict_dossiers_reused":len(refs["dossiers"]),"status":"NEEDS_REVIEW_DOCUMENTARY"}

def validate(root=ROOT):
    refs = context(root)
    book, patterns = load(CASEBOOK,root), load(PATTERNS,root)
    for key, value in book["source_references"].items():
        check((root/value).is_file(), "Missing reused reference " + key + ": " + value)
    for phase in ("C01_auditoria_arquitectura.md","C02_biografias_consecuencias.md",
                  "C03_conocimiento_recuerdos_secretos.md","C04_memoria_institucional_colectiva.md",
                  "C05_relaciones_veteranos_familias.md","C06_legado_cientifico_profesional.md",
                  "C07_integracion_npc_lod_ia.md","C08_auditoria_pruebas_cierre.md","README.md"):
        p = root / DOCS / phase
        check(p.is_file() and len(p.read_text(encoding="utf-8")) > 300, "Missing/empty subphase: " + phase)
    for ref in ("sistemas/gameplay/relationships/relationship_change_provenance_contract.json",
                "sistemas/gameplay/consequences/world_event_consequence_contract.json",
                "sistemas/gameplay/records_and_logs/access_and_privacy_rules.json",
                "mundo/lore/science/lore02_d_scientific_legacy_policy_v0.1.json"):
        check((root/ref).is_file(), "Existing owner contract missing: " + ref)
    return validate_sets(book,patterns,refs)

if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
