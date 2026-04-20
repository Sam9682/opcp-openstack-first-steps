# OpenStack First Steps Labs - Exercise 1: Create Compute Instance

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class CreateInstanceExercise(Exercise):
    """Create a compute instance using the Nova API via compute_manager."""

    @property
    def problem_statement(self) -> str:
        return "Create a compute instance using the Nova API."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use compute_manager to create an instance.",
            "Name it '{student_id}-first-instance'.",
            "Use the default flavor and image from config.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {
                "type": "instance",
                "name": "{student_id}-first-instance",
                "status": "ACTIVE",
            }
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        name = f"{student_id}-first-instance"
        compute = self.managers.get("compute_manager")
        if compute is None:
            return {"error": self._handle_openstack_error(
                "create instance", "compute_manager not available"
            )}
        try:
            instance = compute.create(
                name=name,
                flavor=kwargs.get("flavor"),
                image=kwargs.get("image"),
            )
            return {"instance": instance, "name": name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("create instance", exc)}
