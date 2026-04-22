# Security Groups Module - Exercise 2: Manage Rules

from __future__ import annotations

from labs.core.validators import validate_sg_rule
from labs.templates.exercise_template import Exercise


class ManageRulesExercise(Exercise):
    """Add and remove ingress/egress rules on a security group."""

    @property
    def problem_statement(self) -> str:
        return "Add and remove ingress and egress rules on a security group."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use security_group_manager to add an ingress rule allowing TCP port 80.",
            "Add an ingress rule allowing TCP port 443.",
            "Remove the port 80 rule.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {
                "type": "security_group",
                "name": "${STUDENT_ID}-sg-web",
            }
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        sg_name = f"${STUDENT_ID}-sg-web"
        protocol = kwargs.get("protocol", "tcp")
        port_min = kwargs.get("port_range_min", 443)
        port_max = kwargs.get("port_range_max", 443)

        valid, err = validate_sg_rule(protocol, port_min, port_max)
        if not valid:
            return {"error": f"Validation failed: {err}"}

        sg = self.managers.get("security_group_manager")
        if sg is None:
            return {"error": self._handle_openstack_error(
                "manage rules", "security_group_manager not available"
            )}
        try:
            sg.add_rule(sg_name, protocol=protocol, port_min=port_min, port_max=port_max, direction="ingress")
            return {"sg_name": sg_name, "rule_added": True}
        except Exception as exc:
            return {"error": self._handle_openstack_error("manage rules", exc)}
