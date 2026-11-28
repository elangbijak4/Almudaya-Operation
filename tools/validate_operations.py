#!/usr/bin/env python3
"""Static semantic validator and OBS PredicateExpr evaluator for Almudaya Operations."""

from __future__ import annotations

import json
import operator
import re
import sys
from pathlib import Path
from typing import Any

import jsonschema
from jsonschema import Draft202012Validator
import yaml


_OPS = {
    "eq": operator.eq,
    "neq": operator.ne,
    "gt": operator.gt,
    "gte": operator.ge,
    "lt": operator.lt,
    "lte": operator.le,
}


def _resolve_var(state: dict[str, Any], dotted_path: str) -> Any:
    current: Any = state
    for segment in dotted_path.split("."):
        if not isinstance(current, dict) or segment not in current:
            raise KeyError(f"State variable path not found: {dotted_path}")
        current = current[segment]
    return current


def evaluate_predicate(expr: dict[str, Any], state: dict[str, Any]) -> bool:
    """Evaluate a structured v0.3 OBS PredicateExpr AST against runtime state."""
    if "all" in expr:
        return all(evaluate_predicate(sub, state) for sub in expr["all"])
    if "any" in expr:
        return any(evaluate_predicate(sub, state) for sub in expr["any"])
    if "not" in expr:
        return not evaluate_predicate(expr["not"], state)

    op_name = expr["op"]
    lhs = _resolve_var(state, expr["var"])
    rhs = _resolve_var(state, expr["ref"]) if "ref" in expr else expr["value"]

    if op_name == "in":
        if not isinstance(rhs, (list, tuple, set, str)):
            raise TypeError(f"Right-hand side for 'in' operator must be a collection, got {type(rhs).__name__}")
        return lhs in rhs
    if op_name not in _OPS:
        raise ValueError(f"Unsupported predicate operator: {op_name}")
    return bool(_OPS[op_name](lhs, rhs))


def _parse_semver(version: str) -> tuple[int, int, int]:
    parts = version.strip().split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"Invalid semantic version: {version}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def _satisfies_semver(version: str, constraint: str) -> bool:
    v = _parse_semver(version)
    tokens = [t.strip() for t in constraint.split() if t.strip()]
    if not tokens:
        return True
    for tok in tokens:
        if tok == "*":
            continue
        if tok.endswith(".x"):
            major = int(tok[:-2])
            if v[0] != major:
                return False
            continue
        m = re.match(r"^(>=|<=|==|>|<)?(\d+\.\d+\.\d+)$", tok)
        if not m:
            raise ValueError(f"Unsupported version constraint token: {tok}")
        cmp_op = m.group(1) or "=="
        target = _parse_semver(m.group(2))
        if not _OPS[{"==": "eq", ">": "gt", ">=": "gte", "<": "lt", "<=": "lte"}[cmp_op]](v, target):
            return False
    return True


def _detect_cycle(adj: dict[str, list[str]]) -> list[str] | None:
    color: dict[str, int] = {node: 0 for node in adj}
    stack: list[str] = []

    def dfs(node: str) -> list[str] | None:
        color[node] = 1
        stack.append(node)
        for nxt in adj.get(node, []):
            if nxt not in color:
                continue
            if color[nxt] == 1:
                idx = stack.index(nxt)
                return stack[idx:] + [nxt]
            if color[nxt] == 0:
                cy = dfs(nxt)
                if cy:
                    return cy
        stack.pop()
        color[node] = 2
        return None

    for n in adj:
        if color[n] == 0:
            found = dfs(n)
            if found:
                return found
    return None


def _output_field_names(output_schema: dict[str, Any]) -> set[str]:
    props = output_schema.get("properties", {})
    names = set(props.keys())
    artifacts = props.get("artifacts", {})
    if isinstance(artifacts, dict):
        names.update(artifacts.get("properties", {}).keys())
    return names


def _load_yaml_or_json(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _validate_json_schema_file(schema_path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    if not schema_path.exists():
        errors.append(f"{label}: missing schema file '{schema_path}'")
        return None
    try:
        schema_obj = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema_obj)
        return schema_obj
    except Exception as exc:
        errors.append(f"{label}: invalid JSON schema '{schema_path}': {exc}")
        return None


def validate_v03_operation(
    op_dir: Path,
    op_schema: dict[str, Any] | None = None,
    registry: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    """Validate a single almudaya.operation/v0.3 directory."""
    errors: list[str] = []
    op_yaml = op_dir / "operation.yaml"
    if not op_yaml.exists():
        return [f"{op_dir}: missing operation.yaml"]

    op = _load_yaml_or_json(op_yaml)
    op_id = op.get("identity", {}).get("id", op_dir.name)

    if op_schema is None:
        default_schema_path = op_dir.parent / "schemas" / "operation.schema.json"
        if not default_schema_path.exists():
            default_schema_path = Path(__file__).resolve().parent.parent / "almudaya_operation_v0_3" / "schemas" / "operation.schema.json"
        op_schema = json.loads(default_schema_path.read_text(encoding="utf-8"))

    validator = Draft202012Validator(op_schema)
    for err in sorted(validator.iter_errors(op), key=lambda e: list(e.path)):
        loc = ".".join(str(p) for p in err.path) or "<root>"
        errors.append(f"[{op_id}] schema violation at '{loc}': {err.message}")
    if errors:
        return errors

    # 1. Input/Output schemas and sample-input.json
    in_schema = _validate_json_schema_file(op_dir / op["mission"]["input_schema"], f"[{op_id}] input_schema", errors)
    out_schema = _validate_json_schema_file(op_dir / op["mission"]["output_schema"], f"[{op_id}] output_schema", errors)

    sample_input = op_dir / "examples" / "sample-input.json"
    if sample_input.exists() and in_schema is not None:
        try:
            sample_data = json.loads(sample_input.read_text(encoding="utf-8"))
            jsonschema.validate(sample_data, in_schema)
        except Exception as exc:
            errors.append(f"[{op_id}] examples/sample-input.json failed input_schema: {exc}")

    # 2. Deliverable parity with output_schema
    if out_schema is not None:
        available_outputs = _output_field_names(out_schema)
        for item in op["mission"]["deliverables"]:
            if item not in available_outputs:
                errors.append(f"[{op_id}] deliverable '{item}' missing from output_schema properties/artifacts")

    # 3. Roles, lifecycle bounds, least privilege, and anti-affinity consistency
    roles = op["manifold"]["roles"]
    role_map: dict[str, dict[str, Any]] = {}
    for role in roles:
        rid = role["id"]
        if rid in role_map:
            errors.append(f"[{op_id}] duplicate role id '{rid}'")
        role_map[rid] = role
        card = role["lifecycle"]["cardinality"]
        if card["min"] > card["max"]:
            errors.append(f"[{op_id}] role '{rid}' cardinality min ({card['min']}) > max ({card['max']})")
        if role["default_access_mode"] == "REVIEW_ONLY":
            if role["allowed_path_globs"]:
                errors.append(f"[{op_id}] REVIEW_ONLY role '{rid}' must have empty allowed_path_globs")
            forbidden_caps = {"filesystem.write_external", "filesystem.delete_external"}
            overlap = forbidden_caps.intersection(role["acg_capabilities"])
            if overlap:
                errors.append(f"[{op_id}] REVIEW_ONLY role '{rid}' cannot grant write/delete ACG capabilities: {sorted(overlap)}")

    l1_fallback = op["manifold"]["continuity"]["l1_single_agent_fallback"]
    for rule in op["manifold"].get("anti_affinity", []):
        r1, r2 = rule["roles"]
        if r1 == r2:
            errors.append(f"[{op_id}] anti_affinity cannot pair role '{r1}' with itself")
        for rname in (r1, r2):
            if rname not in role_map:
                errors.append(f"[{op_id}] anti_affinity references unknown role '{rname}'")
        if (
            l1_fallback
            and rule["enforcement"] == "strict_distinct_bot"
            and r1 in role_map
            and r2 in role_map
            and role_map[r1]["lifecycle"]["cardinality"]["min"] >= 1
            and role_map[r2]["lifecycle"]["cardinality"]["min"] >= 1
        ):
            errors.append(
                f"[{op_id}] l1_single_agent_fallback=true conflicts with strict_distinct_bot anti_affinity "
                f"between mandatory roles '{r1}' and '{r2}'"
            )

    # 4. Role references across communication, resources, governance
    for acl in op["communication"].get("blackboard_acl", []):
        if acl["role_id"] not in role_map:
            errors.append(f"[{op_id}] blackboard_acl references unknown role '{acl['role_id']}'")

    resource_ids: set[str] = set()
    for res in op["resources"]["contracts"]:
        rid = res["id"]
        if rid in resource_ids:
            errors.append(f"[{op_id}] duplicate resource contract id '{rid}'")
        resource_ids.add(rid)
        for ar in res["authorized_roles"]:
            if ar not in role_map:
                errors.append(f"[{op_id}] resource '{rid}' authorizes unknown role '{ar}'")

    for gate in op["governance"].get("hitl_gates", []):
        if gate["approver_role"] not in role_map:
            errors.append(f"[{op_id}] hitl_gate '{gate['action']}' references unknown approver_role '{gate['approver_role']}'")

    # 5. Feedback sources distinguish roles from evaluator resources
    for loop in op["behavior"]["loops"]:
        for src in loop["feedback_sources"]:
            if src["kind"] == "role" and src["ref"] not in role_map:
                errors.append(f"[{op_id}] loop '{loop['id']}' feedback_source kind=role unknown: '{src['ref']}'")
            if src["kind"] == "resource_evaluator" and src["ref"] not in resource_ids:
                errors.append(f"[{op_id}] loop '{loop['id']}' feedback_source kind=resource_evaluator unknown: '{src['ref']}'")

    # 6. Sub-operations local DAG & budget checks
    sub_ops = op["manifold"].get("sub_operations", [])
    sub_map: dict[str, dict[str, Any]] = {}
    total_share = 0.0
    for sub in sub_ops:
        sid = sub["id"]
        if sid in sub_map:
            errors.append(f"[{op_id}] duplicate sub_operation id '{sid}'")
        sub_map[sid] = sub
        total_share += float(sub["budget_share_percent"])
    if total_share > 100.0 + 1e-9:
        errors.append(f"[{op_id}] sub_operations budget_share_percent sum ({total_share}) exceeds 100")

    sub_adj: dict[str, list[str]] = {}
    for sid, sub in sub_map.items():
        for dep in sub["depends_on"]:
            if dep not in sub_map:
                errors.append(f"[{op_id}] sub_operation '{sid}' depends_on unknown '{dep}'")
        sub_adj[sid] = list(sub["depends_on"])
    sub_cycle = _detect_cycle(sub_adj)
    if sub_cycle:
        errors.append(f"[{op_id}] sub_operations dependency cycle detected: {' -> '.join(sub_cycle)}")

    # 7. Workflow seed_stages checks
    regime = op["manifold"]["orchestration_regime"]
    stages = op["workflow"]["seed_stages"]
    if regime == "stage_gated" and not stages:
        errors.append(f"[{op_id}] stage_gated regime requires non-empty workflow.seed_stages")

    stage_ids: set[str] = set()
    stage_adj: dict[str, list[str]] = {}
    for st in stages:
        stid = st["id"]
        if stid in stage_ids:
            errors.append(f"[{op_id}] duplicate workflow stage id '{stid}'")
        stage_ids.add(stid)
        if st["owner_kind"] == "role" and st["owner_ref"] not in role_map:
            errors.append(f"[{op_id}] stage '{stid}' references unknown owner role '{st['owner_ref']}'")
        if st["owner_kind"] == "sub_operation" and st["owner_ref"] not in sub_map:
            errors.append(f"[{op_id}] stage '{stid}' references unknown sub_operation '{st['owner_ref']}'")

    for st in stages:
        stid = st["id"]
        for dep in st["depends_on"]:
            if dep not in stage_ids:
                errors.append(f"[{op_id}] stage '{stid}' depends_on unknown stage '{dep}'")
        stage_adj[stid] = list(st["depends_on"])
    stage_cycle = _detect_cycle(stage_adj)
    if stage_cycle:
        errors.append(f"[{op_id}] workflow stage dependency cycle detected: {' -> '.join(stage_cycle)}")

    # 8. Cross-operation contract validation against registry (if provided)
    if registry is not None and sub_ops:
        parent_in_props = set(in_schema.get("properties", {}).keys()) if in_schema else set()
        parent_out_props = _output_field_names(out_schema) if out_schema else set()
        for sid, sub in sub_map.items():
            ref = sub["operation_ref"]
            if ref not in registry:
                errors.append(f"[{op_id}] sub_operation '{sid}' references unregistered operation_ref '{ref}'")
                continue
            child_entry = registry[ref]
            child_op = child_entry["op"]
            child_ver = child_op["identity"]["version"]
            try:
                if not _satisfies_semver(child_ver, sub["version_constraint"]):
                    errors.append(
                        f"[{op_id}] sub_operation '{sid}' child version '{child_ver}' does not satisfy '{sub['version_constraint']}'"
                    )
            except ValueError as exc:
                errors.append(f"[{op_id}] sub_operation '{sid}': {exc}")

            child_in = child_entry["input_schema"]
            child_out = child_entry["output_schema"]
            if child_in is not None:
                req_fields = set(child_in.get("required", []))
                mapped_fields = set(sub["input_mapping"].keys())
                missing_req = req_fields - mapped_fields
                if missing_req:
                    errors.append(
                        f"[{op_id}] sub_operation '{sid}' input_mapping omits required child fields: {sorted(missing_req)}"
                    )
                for target_field, src_expr in sub["input_mapping"].items():
                    if src_expr.startswith("$.mission."):
                        field = src_expr[len("$.mission."):]
                        if field not in parent_in_props:
                            errors.append(
                                f"[{op_id}] sub_operation '{sid}' input_mapping '{target_field}' references missing parent input '{field}'"
                            )
                    elif src_expr.startswith("$.child_outputs."):
                        parts = src_expr[len("$.child_outputs."):].split(".")
                        sib_id = parts[0]
                        if sib_id not in sub_map:
                            errors.append(
                                f"[{op_id}] sub_operation '{sid}' input_mapping references unknown sibling '{sib_id}'"
                            )
                        elif len(parts) == 2 and sub_map[sib_id]["operation_ref"] in registry:
                            sib_out = registry[sub_map[sib_id]["operation_ref"]]["output_schema"]
                            if sib_out and parts[1] not in _output_field_names(sib_out):
                                errors.append(
                                    f"[{op_id}] sub_operation '{sid}' input_mapping references missing field '{parts[1]}' on sibling '{sib_id}'"
                                )

            if child_out is not None:
                child_out_fields = _output_field_names(child_out)
                for parent_field, child_expr in sub["output_mapping"].items():
                    if parent_field not in parent_out_props:
                        errors.append(
                            f"[{op_id}] sub_operation '{sid}' output_mapping target '{parent_field}' missing in parent output_schema"
                        )
                    if child_expr.startswith("$.outputs."):
                        cf = child_expr[len("$.outputs."):]
                        if cf not in child_out_fields:
                            errors.append(
                                f"[{op_id}] sub_operation '{sid}' output_mapping source '{cf}' missing in child '{ref}' output_schema"
                            )

    return errors


def validate_v03_registry(v03_root: Path) -> list[str]:
    """Validate all v0.3 Operations under v03_root including cross-operation DAG & nesting depth."""
    errors: list[str] = []
    op_schema_path = v03_root / "schemas" / "operation.schema.json"
    op_schema = _validate_json_schema_file(op_schema_path, "[v0.3 root]", errors)
    if op_schema is None:
        return errors

    registry: dict[str, dict[str, Any]] = {}
    op_dirs: list[Path] = []
    for yaml_path in sorted(v03_root.rglob("operation.yaml")):
        op_dir = yaml_path.parent
        op_dirs.append(op_dir)
        data = _load_yaml_or_json(yaml_path)
        oid = data.get("identity", {}).get("id")
        if not oid:
            errors.append(f"{yaml_path}: missing identity.id")
            continue
        if oid in registry:
            errors.append(f"Duplicate v0.3 operation id '{oid}' at {yaml_path}")
            continue
        in_path = op_dir / data.get("mission", {}).get("input_schema", "")
        out_path = op_dir / data.get("mission", {}).get("output_schema", "")
        in_s = json.loads(in_path.read_text(encoding="utf-8")) if in_path.exists() else None
        out_s = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else None
        registry[oid] = {"dir": op_dir, "op": data, "input_schema": in_s, "output_schema": out_s}

    # Check manifest.json completeness
    manifest_path = v03_root / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_ids = {entry["id"] for entry in manifest.get("operations", [])}
        missing_in_manifest = set(registry.keys()) - manifest_ids
        if missing_in_manifest:
            errors.append(f"v0.3 manifest.json missing operations: {sorted(missing_in_manifest)}")
    else:
        errors.append("Missing almudaya_operation_v0_3/manifest.json")

    for entry in registry.values():
        errors.extend(validate_v03_operation(entry["dir"], op_schema=op_schema, registry=registry))

    # Cross-operation cycle & max_nesting_depth check
    ref_adj: dict[str, list[str]] = {
        oid: [sub["operation_ref"] for sub in entry["op"]["manifold"].get("sub_operations", [])]
        for oid, entry in registry.items()
    }
    cycle = _detect_cycle(ref_adj)
    if cycle:
        errors.append(f"Cross-operation reference cycle detected: {' -> '.join(cycle)}")
    else:
        def depth(oid: str) -> int:
            children = [c for c in ref_adj.get(oid, []) if c in registry]
            return 1 + max((depth(c) for c in children), default=0)

        for oid, entry in registry.items():
            safety = entry["op"]["governance"].get("hierarchy_safety", {})
            max_d = safety.get("max_nesting_depth")
            if max_d is not None and depth(oid) > max_d:
                errors.append(f"[{oid}] nesting depth ({depth(oid)}) exceeds max_nesting_depth ({max_d})")

    return errors


def validate_v02_operation(
    op_dir: Path,
    op_schema: dict[str, Any],
    res_schema: dict[str, Any],
) -> list[str]:
    """Validate remediated almudaya.operation/v0.2 directories."""
    errors: list[str] = []
    op_yaml = op_dir / "operation.yaml"
    if not op_yaml.exists():
        return [f"{op_dir}: missing operation.yaml"]

    op = _load_yaml_or_json(op_yaml)
    op_id = op.get("identity", {}).get("id", op_dir.name)
    jsonschema.validate(op, op_schema)

    op_json = op_dir / "operation.json"
    if op_json.exists():
        json_data = json.loads(op_json.read_text(encoding="utf-8"))
        if json_data != op:
            errors.append(f"[{op_id}] operation.json and operation.yaml are out of sync")

    res_yaml = op_dir / "resources" / "resource-manifest.yaml"
    res_ids: set[str] = set()
    if res_yaml.exists():
        res_data = _load_yaml_or_json(res_yaml)
        jsonschema.validate(res_data, res_schema)
        res_ids = {r["id"] for r in res_data.get("resources", [])}

    in_path = op_dir / op["mission"].get("parameters_schema", "")
    in_schema = _validate_json_schema_file(in_path, f"[{op_id}] parameters_schema", errors)
    out_rel = op["mission"].get("output_schema")
    if not out_rel:
        errors.append(f"[{op_id}] mission.output_schema is missing")
        out_schema = None
    else:
        out_schema = _validate_json_schema_file(op_dir / out_rel, f"[{op_id}] output_schema", errors)

    sample_in = op_dir / "examples" / "sample-input.json"
    if sample_in.exists() and in_schema is not None:
        jsonschema.validate(json.loads(sample_in.read_text(encoding="utf-8")), in_schema)

    # Check skill-bindings.yaml parity
    sb_path = op_dir / "skills" / "skill-bindings.yaml"
    if sb_path.exists():
        sb = _load_yaml_or_json(sb_path)
        op_skills = {r["id"]: r.get("skills", []) for r in op["organization"]["roles"]}
        sb_skills = {b["role"]: b.get("skills", []) for b in sb.get("bindings", [])}
        for rid, skills in op_skills.items():
            if rid not in sb_skills:
                errors.append(f"[{op_id}] role '{rid}' missing from skills/skill-bindings.yaml")
            elif skills != sb_skills[rid]:
                errors.append(f"[{op_id}] skill parity mismatch for role '{rid}': {skills} != {sb_skills[rid]}")

    # Check deliverables vs output_schema
    if out_schema is not None:
        avail = _output_field_names(out_schema)
        aliases = {
            "paper.tex": "latex_source",
            "paper.pdf": "pdf",
            "references.bib": "bibliography",
            "quality_review.json": "quality_report",
        }
        for item in op["mission"].get("deliverables", []):
            key = aliases.get(item, item)
            if key not in avail and key.endswith(".json"):
                key = key[:-5]
            if key not in avail:
                errors.append(f"[{op_id}] deliverable '{item}' missing in output_schema")

    # Check feedback_from references roles, not resources
    role_ids = {r["id"] for r in op["organization"]["roles"]}
    for loop in op["behavior"]["loops"]:
        for fb in loop.get("feedback_from", []):
            if fb not in role_ids and fb in res_ids:
                errors.append(f"[{op_id}] loop '{loop['id']}' feedback_from conflates resource '{fb}' as a role")

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    all_errors: list[str] = []

    print("=== Validating almudaya_operation_v0_3 (Dynamic Swarm Manifold) ===")
    v03_root = repo_root / "almudaya_operation_v0_3"
    v03_errors = validate_v03_registry(v03_root)
    all_errors.extend(v03_errors)
    manifest = json.loads((v03_root / "manifest.json").read_text(encoding="utf-8"))
    print(f"  Checked {len(manifest.get('operations', []))} v0.3 Operations -> {len(v03_errors)} error(s)")

    print("=== Validating remediated almudaya.operation/v0.2 scaffolds ===")
    op_schema_v02 = json.loads((repo_root / "almudaya_operation_scaffold_v0_2" / "schemas" / "operation.schema.json").read_text(encoding="utf-8"))
    res_schema_v02 = json.loads((repo_root / "almudaya_operation_scaffold_v0_2" / "schemas" / "resource.schema.json").read_text(encoding="utf-8"))
    v02_dirs = [
        repo_root / "almudaya_operation_scaffold_v0_2" / "01_operation-looping",
        repo_root / "almudaya_operation_scaffold_v0_2" / "02_operation-multiHierarchyOperation",
        repo_root / "almudaya_operation_researchPipeline_v0_1",
    ]
    for d in v02_dirs:
        errs = validate_v02_operation(d, op_schema_v02, res_schema_v02)
        all_errors.extend(errs)
        print(f"  {d.name}: {len(errs)} error(s)")

    if all_errors:
        print("\nVALIDATION FAILED:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("\nALL VALIDATIONS PASSED (0 errors).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
