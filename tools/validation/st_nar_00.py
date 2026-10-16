#!/usr/bin/env python3
"""ST-NAR-00 offline reference: declarative pack lint, continuity checks and context ZIP.

This tool DOES NOT query CoreRPG, change saves, install packs or certify UE5/runtime.
Standard-library schema subset is deliberately restricted to the keywords used here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "schemas" / "authoring"
MAX_FILE = 2_000_000
MAX_BUNDLE = 12_000_000
STAMP = (2020, 1, 1, 0, 0, 0)

def load(path: Path):
    if not path.is_file() or path.stat().st_size > MAX_FILE:
        raise ValueError("missing_or_oversized_file")
    return json.loads(path.read_text(encoding="utf-8"))

def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")

def matches_type(value, expected):
    return {
        "object": lambda: isinstance(value, dict),
        "array": lambda: isinstance(value, list),
        "string": lambda: isinstance(value, str),
        "integer": lambda: type(value) is int,
        "boolean": lambda: type(value) is bool,
        "null": lambda: value is None,
    }[expected]()

def schema_errors(data, schema, at="$"):
    """Supported: type, required, additionalProperties=false, properties, items,
    enum, const, pattern, min/maxLength, min/maxItems, uniqueItems, minimum, oneOf.
    Not a claim of arbitrary JSON Schema Draft 2020-12 conformance.
    """
    errors = []
    if "oneOf" in schema:
        acceptable = sum(not schema_errors(data, s, at) for s in schema["oneOf"])
        if acceptable != 1:
            errors.append(at + ": oneOf expected exactly one match")
            return errors
    if "type" in schema:
        types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(matches_type(data, t) for t in types):
            return [at + ": invalid type"]
    if "const" in schema and data != schema["const"]:
        errors.append(at + ": const mismatch")
    if "enum" in schema and data not in schema["enum"]:
        errors.append(at + ": invalid enum")
    if isinstance(data, dict):
        for k in schema.get("required", []):
            if k not in data:
                errors.append(at + ": missing " + k)
        if schema.get("additionalProperties") is False:
            for k in data.keys() - schema.get("properties", {}).keys():
                errors.append(at + ": unexpected " + k)
        for key, subschema in schema.get("properties", {}).items():
            if key in data:
                errors.extend(schema_errors(data[key], subschema, at + "." + key))
    if isinstance(data, list):
        if len(data) < schema.get("minItems", 0) or len(data) > schema.get("maxItems", 10**9):
            errors.append(at + ": item count")
        if schema.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in data}) != len(data):
            errors.append(at + ": duplicate array item")
        if isinstance(schema.get("items"), dict):
            for i, item in enumerate(data):
                errors.extend(schema_errors(item, schema["items"], at + "[" + str(i) + "]"))
    if isinstance(data, str):
        if not schema.get("minLength", 0) <= len(data) <= schema.get("maxLength", 10**9):
            errors.append(at + ": string length")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], data):
            errors.append(at + ": invalid pattern")
    if type(data) is int and "minimum" in schema and data < schema["minimum"]:
        errors.append(at + ": below minimum")
    return errors

def verify_schema(value, name):
    return schema_errors(value, load(SCHEMAS / name))

def valid_timestamp(value):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S") == value
    except (ValueError, TypeError):
        return False

def inspect_pack(directory: Path):
    errors = []
    try:
        manifest = load(directory / "manifest.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, {}, ["manifest: " + str(exc)]
    errors += verify_schema(manifest, "st_nar_season_manifest_v0.1.schema.json")
    if errors:
        return manifest, {}, errors
    if manifest["season"]["era_start"] > manifest["season"]["era_end"]:
        errors.append("era interval inverted")
    for field in ("era_start", "era_end"):
        try:
            datetime.strptime(manifest["season"][field], "%Y-%m-%d")
        except ValueError:
            errors.append("invalid calendar date: " + field)
    activation = manifest["activation"]
    if activation["origin"] == "existing_world_event":
        if activation["authorization_capability"] is not None:
            errors.append("existing event must not declare seed authority")
    else:
        cap = activation["authorization_capability"]
        if cap != "authorized_world_seed_v1" or cap not in manifest["capability_ids"]:
            errors.append("authorized seed requires explicit registered capability declaration")
    known_events = set(load(ROOT / "narrative" / "events" / "world_event_state.json")["event_types"])
    if activation["event_hook_id"] not in known_events:
        errors.append("unregistered event hook")
    clauses = manifest["constraints"]
    for name in ("history", "current"):
        if set(clauses["require_" + name + "_fact_ids"]) & set(clauses["forbid_" + name + "_fact_ids"]):
            errors.append("contradictory " + name + " conditions")
    chapters = {}
    for rel in manifest["chapter_files"]:
        file = directory / rel
        if file.is_symlink() or not file.resolve().is_relative_to(directory.resolve()):
            errors.append("unsafe chapter path " + rel)
            continue
        try:
            value = load(file)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(rel + ": " + str(exc))
            continue
        errors.extend(rel + " " + x for x in verify_schema(value, "st_nar_chapter_v0.1.schema.json"))
        ident = value.get("chapter_id")
        if isinstance(ident, str):
            if ident in chapters:
                errors.append("duplicate chapter id: " + ident)
            chapters[ident] = value
        if rel != "chapters/" + str(ident) + ".json":
            errors.append("chapter file and id mismatch: " + rel)
        for t in value.get("event_types", []):
            if t not in known_events:
                errors.append("unregistered event type: " + str(t))
    if not chapters:
        errors.append("empty chapter graph")
    arcs = {key: set() for key in chapters}
    for ident, chapter in chapters.items():
        if ident in chapter.get("depends_on", []):
            errors.append("self dependency: " + ident)
        for dep in chapter.get("depends_on", []):
            if dep not in chapters:
                errors.append("missing dependency: " + str(dep))
            else:
                arcs[dep].add(ident)
        seen_outcomes = set()
        for out in chapter.get("outcomes", []):
            oid = out.get("outcome_id")
            if oid in seen_outcomes:
                errors.append("duplicate outcome in " + ident)
            seen_outcomes.add(oid)
            for nxt in out.get("next_chapter_ids", []):
                if nxt not in chapters:
                    errors.append("missing next chapter: " + str(nxt))
                elif ident not in chapters[nxt].get("depends_on", []):
                    errors.append("edge lacks dependency " + ident + " -> " + nxt)
    if chapters and not any(not c.get("depends_on") for c in chapters.values()):
        errors.append("no root chapter")
    visited, visiting = set(), set()
    def visit(node):
        if node in visiting:
            errors.append("cycle at " + node)
            return
        if node in visited:
            return
        visiting.add(node)
        for nxt in arcs[node]:
            visit(nxt)
        visiting.remove(node)
        visited.add(node)
    for node in arcs:
        visit(node)
    return manifest, chapters, sorted(set(errors))

def inspect_context(context):
    errors = verify_schema(context, "st_nar_campaign_context_v0.1.schema.json")
    if errors:
        return sorted(set(errors))
    coverage, history, campaign = context["coverage"], context["history"], context["campaign"]
    start, end = coverage["from_event_cursor"], coverage["to_event_cursor"]
    if not coverage["complete"]:
        errors.append("incomplete context coverage")
    if start > end or coverage["event_total"] < end:
        errors.append("invalid cursor range")
    if context["export_mode"] == "full":
        if start != 0 or coverage["base_snapshot_revision"] is not None:
            errors.append("full export must start at zero with no base")
        if coverage["event_total"] != end:
            errors.append("full export total does not match cursor")
    elif coverage["base_snapshot_revision"] is None or coverage["base_snapshot_revision"] >= campaign["snapshot_revision"]:
        errors.append("delta requires older base revision")
    if [e["sequence"] for e in history] != list(range(start + 1, end + 1)):
        errors.append("missing, duplicate or unordered history sequences")
    if len({e["event_id"] for e in history}) != len(history):
        errors.append("duplicate event id")
    if not valid_timestamp(campaign["world_time"]):
        errors.append("invalid world timestamp")
    for event in history:
        if not valid_timestamp(event["occurred_at"]) or event["occurred_at"] > campaign["world_time"]:
            errors.append("invalid or future event timestamp")
    if context["export_mode"] == "full":
        listed_facts = {f for event in history for f in event["fact_ids"]}
        if listed_facts != set(context["current"]["historical_fact_ids"]):
            errors.append("history facts diverge from complete event ledger")
    ids = [s["season_id"] for s in context["installed_seasons"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate installed season")
    foreground = campaign["foreground_main_season_id"]
    if foreground and foreground not in {s["season_id"] for s in context["installed_seasons"] if s["state"] == "in_progress"}:
        errors.append("foreground season not active")
    installed = {(s["season_id"], s["pack_id"], s["pack_version"]) for s in context["installed_seasons"]}
    for plan in context["pending_season_plans"]:
        if (plan["season_id"], plan["pack_id"], plan["pack_version"]) not in installed:
            errors.append("pending plan not backed by installed pack version")
    provenance = context["provenance"]
    if provenance["source_kind"] == "offline_fixture" and provenance["is_runtime_verified"]:
        errors.append("offline fixture cannot claim runtime verification")
    if provenance["is_runtime_verified"] and not provenance["evidence_ref"]:
        errors.append("runtime verification without evidence reference")
    return sorted(set(errors))

def assess_pack(directory, context, opt_in=False):
    manifest, chapters, problems = inspect_pack(directory)
    problems += inspect_context(context)
    outcome = {"status": "BLOCKED", "reasons": sorted(set(problems)), "runtime_certified": False,
               "installation_performed": False, "chapter_count": len(chapters)}
    if problems or not manifest:
        return outcome
    if manifest["publication_status"] != "approved_content":
        outcome["reasons"] = ["reference_only_not_installable"]
        return outcome
    if not opt_in:
        outcome["status"], outcome["reasons"] = "OPT_IN_REQUIRED", ["existing_campaign_default_disabled"]
        return outcome
    if context["knowledge_scope"] != "full_authoring":
        outcome["status"], outcome["reasons"] = "REVIEW_REQUIRED", ["incomplete_observer_knowledge"]
        return outcome
    if manifest["authoring_binding"]:
        binding = manifest["authoring_binding"]
        if binding["campaign_id"] != context["campaign"]["campaign_id"]:
            outcome["reasons"] = ["campaign_identity_mismatch"]
            return outcome
        if (binding["snapshot_revision"] != context["campaign"]["snapshot_revision"] or
                binding["catalog_revision"] != context["campaign"]["catalog_revision"]):
            outcome["status"], outcome["reasons"] = "REVIEW_REQUIRED", ["authoring_context_stale"]
            return outcome
    if not set(manifest["capability_ids"]) <= set(context["capability_ids"]):
        outcome["reasons"] = ["missing_runtime_capabilities"]
        return outcome
    history = set(context["current"]["historical_fact_ids"])
    current = set(context["current"]["current_fact_ids"])
    constraints = manifest["constraints"]
    if set(constraints["forbid_history_fact_ids"]) & history:
        outcome["reasons"] = ["contradicts_immutable_history"]
        return outcome
    if (not set(constraints["require_history_fact_ids"]) <= history or
            not set(constraints["require_current_fact_ids"]) <= current or
            set(constraints["forbid_current_fact_ids"]) & current):
        outcome["status"], outcome["reasons"] = "DORMANT_ELIGIBILITY", ["declared_eligibility_not_met"]
        return outcome
    outcome["status"], outcome["reasons"] = "REVIEW_REQUIRED", ["offline_checks_pass_runtime_authority_unverified"]
    return outcome

def build_bundle_files(context):
    camp = context["campaign"]
    warning = ("ALERTA: contiene información confidencial de autoría, posibles spoilers. "
               "No es un archivo de guardado y NO está verificado contra CoreRPG.")
    summary = ["# Contexto de campaña exportado", "", warning, "",
               "Campaña: " + camp["campaign_id"],
               "Fecha interna: " + camp["world_time"],
               "Revisión: " + str(camp["snapshot_revision"]),
               "Modalidad: " + context["export_mode"], "",
               "## Historial confirmado incluido"]
    for event in context["history"]:
        summary.append("- " + event["occurred_at"] + " | " + event["event_id"] +
                       " | " + event["summary_es"] + " [" + event["visibility"] + "]")
    summary += ["", "## Temporadas previstas", "Las previsiones NO son hechos canónicos futuros."]
    for plan in context["pending_season_plans"]:
        summary.append("- " + plan["season_id"] + ": " + ", ".join(plan["planned_chapter_ids"]))
    files = {
        "LEEME.md": ("# ST-NAR-00 — Paquete externo de contexto\n\n" + warning +
                     "\n\nValidar cobertura y versión. No reimportar como save.\n").encode("utf-8"),
        "RESUMEN_CAMPAÑA.md": ("\n".join(summary) + "\n").encode("utf-8"),
        "HISTORIA_REAL.json": encode(context["history"]),
        "ESTADO_ACTUAL.json": encode(context["current"]),
        "TEMPORADAS_INSTALADAS.json": encode(context["installed_seasons"]),
        "TEMPORADAS_PREVISTAS.json": encode(context["pending_season_plans"]),
        "CAPACIDADES.json": encode(context["capability_ids"]),
        "contexto.json": encode(context),
    }
    digests = {name: hashlib.sha256(payload).hexdigest() for name, payload in sorted(files.items())}
    files["MANIFEST.json"] = encode({
        "schema_version": "0.1.0", "campaign_id": camp["campaign_id"],
        "snapshot_revision": camp["snapshot_revision"], "sha256": digests,
        "runtime_certified": False
    })
    return files

def export_bundle(context, destination):
    errors = inspect_context(context)
    if errors:
        raise ValueError("; ".join(errors))
    files = build_bundle_files(context)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(name, STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            z.writestr(info, data)
    return {"status": "EXPORTED_OFFLINE_REFERENCE", "files": len(files),
            "runtime_certified": False, "destination": str(destination)}

def verify_bundle(destination):
    with zipfile.ZipFile(destination) as z:
        names = z.namelist()
        if len(names) != len(set(names)) or sum(x.file_size for x in z.infolist()) > MAX_BUNDLE:
            raise ValueError("duplicate entries or oversized bundle")
        if any(x.is_dir() or "/" in x.filename or "\\" in x.filename or
               (x.external_attr >> 16) & 0o170000 == 0o120000 for x in z.infolist()):
            raise ValueError("unsafe zip member")
        data = {name: z.read(name) for name in names}
    if "contexto.json" not in data or "MANIFEST.json" not in data:
        raise ValueError("missing context or manifest")
    context = json.loads(data["contexto.json"])
    errors = inspect_context(context)
    if errors:
        raise ValueError("; ".join(errors))
    expected = build_bundle_files(context)
    if set(data) != set(expected) or any(data[k] != expected[k] for k in expected):
        raise ValueError("bundle integrity or derived view mismatch")
    return {"status": "VALID_OFFLINE_REFERENCE_BUNDLE", "runtime_certified": False,
            "files": len(expected)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check-pack", "check-context", "assess-pack", "export-bundle", "verify-bundle"])
    parser.add_argument("--pack", type=Path)
    parser.add_argument("--context", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--opt-in", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "check-pack":
            if not args.pack: parser.error("--pack required")
            manifest, chapters, errors = inspect_pack(args.pack)
            result = {"status": "INVALID" if errors else "VALID_OFFLINE_REFERENCE",
                      "errors": errors, "chapters": len(chapters),
                      "publication_status": manifest.get("publication_status") if manifest else None}
        elif args.command == "check-context":
            if not args.context: parser.error("--context required")
            errors = inspect_context(load(args.context))
            result = {"status": "INVALID" if errors else "VALID_OFFLINE_REFERENCE", "errors": errors}
        elif args.command == "assess-pack":
            if not args.pack or not args.context: parser.error("--pack and --context required")
            result = assess_pack(args.pack, load(args.context), args.opt_in)
        elif args.command == "export-bundle":
            if not args.context or not args.output: parser.error("--context and --output required")
            result = export_bundle(load(args.context), args.output)
        else:
            if not args.bundle: parser.error("--bundle required")
            result = verify_bundle(args.bundle)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        result = {"status": "ERROR", "reasons": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if result["status"] in {
        "VALID_OFFLINE_REFERENCE", "EXPORTED_OFFLINE_REFERENCE", "VALID_OFFLINE_REFERENCE_BUNDLE",
        "REVIEW_REQUIRED", "DORMANT_ELIGIBILITY", "OPT_IN_REQUIRED",
    } else 2

if __name__ == "__main__":
    sys.exit(main())
