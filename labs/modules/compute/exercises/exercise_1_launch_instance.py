# Compute Module - Exercise 1: Launch Instance

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class LaunchInstanceExercise(Exercise):
    """Launch a compute instance with specified flavor and image."""

    @property
    def problem_statement(self) -> str:
        return "Launch a new compute instance with a specified flavor and image."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use compute_manager to launch an instance.",
            "Name it '{student_id}-compute-instance'.",
            "Specify the flavor and image from the config.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "instance", "name": "{student_id}-compute-instance", "status": "ACTIVE"}
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        name = f"{student_id}-compute-instance"
        compute = self.managers.get("compute_manager")
        if compute is None:
            return {"error": self._handle_openstack_error(
                "launch instance", "compute_manager not available"
            )}
        try:
            instance = compute.create(
                name=name,
                flavor=kwargs.get("flavor"),
                image=kwargs.get("image"),
            )
            return {"instance": instance, "name": name}
        except Exception as exc:
            msg = str(exc)
            if "flavor" in msg.lower() or "image" in msg.lower():
                return {"error": f"Missing resource: {exc}"}
            return {"error": self._handle_openstack_error("launch instance", exc)}
