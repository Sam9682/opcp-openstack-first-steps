# Security Groups Module - Exercise 3: Apply Security Group

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class ApplySecurityGroupExercise(Exercise):
    """Apply a security group to a running instance."""

    @property
    def problem_statement(self) -> str:
        return "Apply a security group to a running compute instance."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use security_group_manager to apply '{student_id}-sg-web' "
            "to '{student_id}-compute-instance'.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "instance", "name": "{student_id}-compute-instance"}
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        sg_name = f"{student_id}-sg-web"
        instance_name = f"{student_id}-compute-instance"
        sg = self.managers.get("security_group_manager")
        if sg is None:
            return {"error": self._handle_openstack_error(
                "apply security group", "security_group_manager not available"
            )}
        try:
            sg.apply_to_instance(sg_name=sg_name, instance_name=instance_name)
            return {"applied": True, "sg": sg_name, "instance": instance_name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("apply security group", exc)}
