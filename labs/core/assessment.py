# OpenStack First Steps Labs - Assessment Engine

"""
Validates exercise solutions by querying actual OpenStack resource state
(not source code) and comparing against expected outcomes.
"""

from __future__ import annotations

from labs.core import AssessmentResult
from labs.templates.assessment_template import outcomes_match


class AssessmentEngine:
    """Automated exercise assessment via OpenStack state queries."""

    def __init__(self, managers: dict, progress_tracker) -> None:
        self._managers = managers
        self._progress = progress_tracker

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate_exercise(
        self, module_name: str, exercise_id: str, student_id: str
    ) -> AssessmentResult:
        """Validate an exercise by querying OpenStack resource state.

        Returns an ``AssessmentResult`` indicating pass/fail with feedback.
        """
        try:
            exercise_cls = self._load_exercise(module_name, exercise_id)
            expected = exercise_cls.expected_outcomes
        except Exception as exc:
            return AssessmentResult(
                passed=False,
                exercise_id=exercise_id,
                feedback=f"Assessment error: could not load exercise — {exc}",
                expected_outcomes=[],
                actual_outcomes=[],
            )

        try:
            actual = self._query_actual_state(expected, student_id)
        except Exception as exc:
            return AssessmentResult(
                passed=False,
                exercise_id=exercise_id,
                feedback=f"Assessment could not verify: {exc}",
                expected_outcomes=[e for e in expected],
                actual_outcomes=[],
            )

        passed, mismatches = outcomes_match(expected, actual)

        if passed:
            self._progress.mark_complete(student_id, module_name, exercise_id)
            feedback = "All expected outcomes met. Exercise complete."
        else:
            feedback = "Some expected outcomes were not met:\n" + "\n".join(
                f"  - {m}" for m in mismatches
            )

        return AssessmentResult(
            passed=passed,
            exercise_id=exercise_id,
            feedback=feedback,
            expected_outcomes=[e for e in expected],
            actual_outcomes=actual,
            mismatches=mismatches,
        )

    # ------------------------------------------------------------------
    # Resource checks
    # ------------------------------------------------------------------

    def _check_resource_exists(
        self, resource_type: str, resource_name: str
    ) -> bool:
        """Check if a named resource exists in OpenStack."""
        manager = self._get_manager(resource_type)
        if manager is None:
            return False
        try:
            resource = manager.get(resource_name)
            return resource is not None
        except Exception:
            return False

    def _check_resource_properties(
        self, resource_type: str, resource_name: str, expected: dict
    ) -> list[str]:
        """Check resource properties match expected values.

        Returns a list of human-readable mismatch descriptions.
        """
        mismatches: list[str] = []
        manager = self._get_manager(resource_type)
        if manager is None:
            mismatches.append(f"No manager for resource type: {resource_type}")
            return mismatches

        try:
            resource = manager.get(resource_name)
        except Exception as exc:
            mismatches.append(f"Could not query {resource_type} '{resource_name}': {exc}")
            return mismatches

        if resource is None:
            mismatches.append(f"{resource_type} '{resource_name}' not found")
            return mismatches

        for prop, expected_val in expected.items():
            actual_val = getattr(resource, prop, None) if not isinstance(resource, dict) else resource.get(prop)
            if actual_val != expected_val:
                mismatches.append(
                    f"{resource_type} '{resource_name}': "
                    f"expected {prop}={expected_val!r}, got {actual_val!r}"
                )

        return mismatches

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_manager(self, resource_type: str):
        """Map a resource type string to the appropriate framework manager."""
        mapping = {
            "instance": "compute_manager",
            "network": "network_manager",
            "subnet": "network_manager",
            "router": "network_manager",
            "volume": "volume_manager",
            "security_group": "security_group_manager",
        }
        manager_key = mapping.get(resource_type)
        if manager_key is None:
            return None
        return self._managers.get(manager_key)

    def _load_exercise(self, module_name: str, exercise_id: str):
        """Dynamically load an exercise class to read its expected_outcomes."""
        import importlib

        module_path = f"labs.modules.{module_name}.exercises.{exercise_id}"
        mod = importlib.import_module(module_path)

        # Convention: the exercise class is the first Exercise subclass found.
        from labs.templates.exercise_template import Exercise

        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, Exercise)
                and attr is not Exercise
            ):
                # Instantiate with managers to access expected_outcomes.
                return attr(module_name, exercise_id, self._managers)

        raise ValueError(f"No Exercise subclass found in {module_path}")

    def _query_actual_state(
        self, expected: list[dict], student_id: str
    ) -> list[dict]:
        """Query OpenStack for the actual state of expected resources."""
        actual: list[dict] = []
        for exp in expected:
            rtype = exp.get("type", "")
            rname = exp.get("name", "").format(student_id=student_id)
            manager = self._get_manager(rtype)
            if manager is None:
                continue
            try:
                resource = manager.get(rname)
                if resource is None:
                    continue
                if isinstance(resource, dict):
                    entry = dict(resource)
                else:
                    entry = {"type": rtype, "name": rname}
                    for prop in exp:
                        if prop not in ("type", "name"):
                            entry[prop] = getattr(resource, prop, None)
                actual.append(entry)
            except Exception:
                continue
        return actual
