"""Unit and semantic regression tests for Almudaya Operation validator and OBS PredicateExpr."""

from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

from validate_operations import (  # noqa: E402
    evaluate_predicate,
    validate_v02_operation,
    validate_v03_operation,
    validate_v03_registry,
)


class OperationValidatorTests(unittest.TestCase):
    def test_v03_registry_passes(self) -> None:
        errors = validate_v03_registry(REPO_ROOT / "almudaya_operation_v0_3")
        self.assertEqual(errors, [])

    def test_v02_remediated_scaffolds_pass(self) -> None:
        op_schema = json.loads(
            (REPO_ROOT / "almudaya_operation_scaffold_v0_2" / "schemas" / "operation.schema.json").read_text(encoding="utf-8")
        )
        res_schema = json.loads(
            (REPO_ROOT / "almudaya_operation_scaffold_v0_2" / "schemas" / "resource.schema.json").read_text(encoding="utf-8")
        )
        for d in [
            REPO_ROOT / "almudaya_operation_scaffold_v0_2" / "01_operation-looping",
            REPO_ROOT / "almudaya_operation_scaffold_v0_2" / "02_operation-multiHierarchyOperation",
            REPO_ROOT / "almudaya_operation_researchPipeline_v0_1",
        ]:
            self.assertEqual(validate_v02_operation(d, op_schema, res_schema), [], msg=f"Failed on {d.name}")

    def test_predicate_evaluator_paperorchestra_acceptance_and_rollback(self) -> None:
        rp = yaml.safe_load(
            (REPO_ROOT / "almudaya_operation_v0_3" / "04_research_pipeline" / "operation.yaml").read_text(encoding="utf-8")
        )
        loop = next(l for l in rp["behavior"]["loops"] if l["id"] == "manuscript_refinement_loop")
        acc = loop["acceptance_predicate"]
        rb = loop["rollback_predicate"]

        # Score increases -> accepted, no rollback
        s_improve = {
            "candidate": {"overall_score": 8.5, "net_subscore_delta": -0.1, "required_subscore_regression": False, "hard_constraint_violated": False},
            "accepted": {"overall_score": 8.0},
        }
        self.assertTrue(evaluate_predicate(acc, s_improve))
        self.assertFalse(evaluate_predicate(rb, s_improve))

        # Score ties, net subscore delta >= 0, no required regression -> accepted
        s_tie_ok = {
            "candidate": {"overall_score": 8.0, "net_subscore_delta": 0.2, "required_subscore_regression": False, "hard_constraint_violated": False},
            "accepted": {"overall_score": 8.0},
        }
        self.assertTrue(evaluate_predicate(acc, s_tie_ok))
        self.assertFalse(evaluate_predicate(rb, s_tie_ok))

        # Score ties, required subscore regresses -> rejected
        s_tie_reg = {
            "candidate": {"overall_score": 8.0, "net_subscore_delta": 0.1, "required_subscore_regression": True, "hard_constraint_violated": False},
            "accepted": {"overall_score": 8.0},
        }
        self.assertFalse(evaluate_predicate(acc, s_tie_reg))

        # Score decreases -> rejected, triggers rollback
        s_drop = {
            "candidate": {"overall_score": 7.4, "net_subscore_delta": -0.6, "required_subscore_regression": True, "hard_constraint_violated": False},
            "accepted": {"overall_score": 8.0},
        }
        self.assertFalse(evaluate_predicate(acc, s_drop))
        self.assertTrue(evaluate_predicate(rb, s_drop))

    def _copy_v03_fixture(self, tmp: Path) -> Path:
        dst = tmp / "v03"
        shutil.copytree(REPO_ROOT / "almudaya_operation_v0_3", dst)
        return dst

    def test_rejects_workflow_stage_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            v03 = self._copy_v03_fixture(Path(tmp))
            op_path = v03 / "02_iterative_quality_loop" / "operation.yaml"
            data = yaml.safe_load(op_path.read_text(encoding="utf-8"))
            data["workflow"]["seed_stages"][0]["depends_on"] = ["evaluate"]
            op_path.write_text(yaml.safe_dump(data), encoding="utf-8")
            errors = validate_v03_operation(op_path.parent)
            self.assertTrue(any("cycle detected" in e for e in errors), errors)

    def test_rejects_sub_operation_reference_cycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            v03 = self._copy_v03_fixture(Path(tmp))
            child_path = v03 / "03_multi_hierarchy_manifold" / "sub_operations" / "research_branch" / "operation.yaml"
            data = yaml.safe_load(child_path.read_text(encoding="utf-8"))
            data["manifold"]["sub_operations"] = [
                {
                    "id": "cyclic_parent",
                    "operation_ref": "almudaya.operation.multi-hierarchy",
                    "version_constraint": ">=0.3.0 <1.0.0",
                    "delegate_moderator": True,
                    "depends_on": [],
                    "execution_mode": "sequential",
                    "required": True,
                    "budget_share_percent": 10,
                    "input_mapping": {},
                    "output_mapping": {},
                }
            ]
            child_path.write_text(yaml.safe_dump(data), encoding="utf-8")
            errors = validate_v03_registry(v03)
            self.assertTrue(any("Cross-operation reference cycle" in e for e in errors), errors)

    def test_rejects_l1_fallback_with_strict_distinct_bot_anti_affinity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            v03 = self._copy_v03_fixture(Path(tmp))
            op_path = v03 / "02_iterative_quality_loop" / "operation.yaml"
            data = yaml.safe_load(op_path.read_text(encoding="utf-8"))
            data["manifold"]["continuity"]["l1_single_agent_fallback"] = True
            op_path.write_text(yaml.safe_dump(data), encoding="utf-8")
            errors = validate_v03_operation(op_path.parent)
            self.assertTrue(any("l1_single_agent_fallback=true conflicts" in e for e in errors), errors)

    def test_rejects_resource_id_labeled_as_role_feedback_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            v03 = self._copy_v03_fixture(Path(tmp))
            op_path = v03 / "04_research_pipeline" / "operation.yaml"
            data = yaml.safe_load(op_path.read_text(encoding="utf-8"))
            data["behavior"]["loops"][0]["feedback_sources"] = [{"kind": "role", "ref": "visual_critic"}]
            op_path.write_text(yaml.safe_dump(data), encoding="utf-8")
            errors = validate_v03_operation(op_path.parent)
            self.assertTrue(any("kind=role unknown: 'visual_critic'" in e for e in errors), errors)

    def test_rejects_missing_deliverable_in_output_schema(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            v03 = self._copy_v03_fixture(Path(tmp))
            op_path = v03 / "02_iterative_quality_loop" / "operation.yaml"
            data = yaml.safe_load(op_path.read_text(encoding="utf-8"))
            data["mission"]["deliverables"].append("undeclared_artifact")
            op_path.write_text(yaml.safe_dump(data), encoding="utf-8")
            errors = validate_v03_operation(op_path.parent)
            self.assertTrue(any("undeclared_artifact" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
