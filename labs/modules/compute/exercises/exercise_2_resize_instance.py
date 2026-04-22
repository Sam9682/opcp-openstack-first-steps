# Compute Module - Exercise 2: Resize Instance

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class ResizeInstanceExercise(Exercise):
    """Resize an existing compute instance."""

    @property
    def problem_statement(self) -> str:
        return "Resize an existing compute instance to a different flavor."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use compute_manager to resize '${STUDENT_ID}-compute-instance'.",
            "Change the flavor to the target flavor provided.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "instance", "name": "${STUDENT_ID}-compute-instance", "status": "ACTIVE"}
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        name = f"${STUDENT_ID}-compute-instance"
        compute = self.managers.get("compute_manager")
        if compute is None:
            return {"error": self._handle_openstack_error(
                "resize instance", "compute_manager not available"
            )}
        try:
            result = compute.resize(name=name, flavor=kwargs.get("target_flavor"))
            return {"result": result, "name": name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("resize instance", exc)}
