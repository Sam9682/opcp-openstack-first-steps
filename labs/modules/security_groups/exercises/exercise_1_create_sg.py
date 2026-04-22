# Security Groups Module - Exercise 1: Create Security Group

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class CreateSecurityGroupExercise(Exercise):
    """Create a security group."""

    @property
    def problem_statement(self) -> str:
        return "Create a security group to control network access."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use security_group_manager to create a security group.",
            "Name it '${STUDENT_ID}-sg-web'.",
            "Add a description: 'Web traffic security group'.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "security_group", "name": "${STUDENT_ID}-sg-web"}
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        name = f"${STUDENT_ID}-sg-web"
        sg = self.managers.get("security_group_manager")
        if sg is None:
            return {"error": self._handle_openstack_error(
                "create security group", "security_group_manager not available"
            )}
        try:
            group = sg.create(name=name, description="Web traffic security group")
            return {"security_group": group, "name": name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("create security group", exc)}
