# Networking Module - Exercise 2: Create Subnet

from __future__ import annotations

from labs.core.validators import validate_cidr
from labs.templates.exercise_template import Exercise


class CreateSubnetExercise(Exercise):
    """Create a subnet within a network."""

    @property
    def problem_statement(self) -> str:
        return "Create a subnet within an existing virtual network."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use network_manager to create a subnet in '{student_id}-net-network'.",
            "Name it '{student_id}-net-subnet'.",
            "Use CIDR 10.0.0.0/24.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "subnet", "name": "{student_id}-net-subnet", "cidr": "10.0.0.0/24"}
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        cidr = kwargs.get("cidr", "10.0.0.0/24")
        valid, err = validate_cidr(cidr)
        if not valid:
            return {"error": f"Validation failed: CIDR — {err}"}

        name = f"{student_id}-net-subnet"
        network_name = f"{student_id}-net-network"
        net = self.managers.get("network_manager")
        if net is None:
            return {"error": self._handle_openstack_error(
                "create subnet", "network_manager not available"
            )}
        try:
            subnet = net.create_subnet(
                network_name=network_name, name=name, cidr=cidr
            )
            return {"subnet": subnet, "name": name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("create subnet", exc)}
