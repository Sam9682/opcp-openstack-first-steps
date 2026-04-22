# Networking Module - Exercise 1: Create Network

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class CreateNetworkExercise(Exercise):
    """Create a virtual network."""

    @property
    def problem_statement(self) -> str:
        return "Create a virtual network using the Neutron API."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use network_manager to create a network.",
            "Name it '${STUDENT_ID}-net-network'.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "network", "name": "${STUDENT_ID}-net-network", "status": "ACTIVE"}
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        name = f"${STUDENT_ID}-net-network"
        net = self.managers.get("network_manager")
        if net is None:
            return {"error": self._handle_openstack_error(
                "create network", "network_manager not available"
            )}
        try:
            network = net.create(name=name)
            return {"network": network, "name": name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("create network", exc)}
