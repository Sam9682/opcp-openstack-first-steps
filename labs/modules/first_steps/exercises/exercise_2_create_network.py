# OpenStack First Steps Labs - Exercise 2: Create Network

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class CreateNetworkExercise(Exercise):
    """Create a virtual network using the Neutron API via network_manager."""

    @property
    def problem_statement(self) -> str:
        return "Create a virtual network using the Neutron API."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use network_manager to create a network.",
            "Name it '${STUDENT_ID}-first-network'.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {
                "type": "network",
                "name": "${STUDENT_ID}-first-network",
                "status": "ACTIVE",
            }
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        name = f"${STUDENT_ID}-first-network"
        network_mgr = self.managers.get("network_manager")
        if network_mgr is None:
            return {"error": self._handle_openstack_error(
                "create network", "network_manager not available"
            )}
        try:
            network = network_mgr.create(name=name)
            return {"network": network, "name": name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("create network", exc)}
