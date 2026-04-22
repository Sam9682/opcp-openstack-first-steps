# LACP Module - Exercise 1: Create LACP Bond

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class CreateBondExercise(Exercise):
    """Create a LACP bond from two Neutron ports."""

    @property
    def problem_statement(self) -> str:
        return "Create two Neutron ports and bond them using LACP (802.3ad)."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use network_manager to create a network named '${STUDENT_ID}-lacp-network'.",
            "Create two ports: '${STUDENT_ID}-lacp-port-1' and '${STUDENT_ID}-lacp-port-2'.",
            "Create a bond named '${STUDENT_ID}-lacp-bond' with bond_mode '802.3ad'.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "network", "name": "${STUDENT_ID}-lacp-network", "status": "ACTIVE"},
            {"type": "port", "name": "${STUDENT_ID}-lacp-port-1", "status": "ACTIVE"},
            {"type": "port", "name": "${STUDENT_ID}-lacp-port-2", "status": "ACTIVE"},
            {"type": "bond", "name": "${STUDENT_ID}-lacp-bond", "bond_mode": "802.3ad"},
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        net = self.managers.get("network_manager")
        if net is None:
            return {"error": self._handle_openstack_error(
                "create bond", "network_manager not available"
            )}
        try:
            network_name = f"${STUDENT_ID}-lacp-network"
            network = net.create(name=network_name)

            port1_name = f"${STUDENT_ID}-lacp-port-1"
            port2_name = f"${STUDENT_ID}-lacp-port-2"
            port1 = net.create_port(network_name=network_name, name=port1_name)
            port2 = net.create_port(network_name=network_name, name=port2_name)

            bond_name = f"${STUDENT_ID}-lacp-bond"
            bond = net.create_bond(
                name=bond_name,
                port_names=[port1_name, port2_name],
                bond_mode="802.3ad",
            )
            return {
                "network": network,
                "port1": port1,
                "port2": port2,
                "bond": bond,
                "name": bond_name,
            }
        except Exception as exc:
            return {"error": self._handle_openstack_error("create bond", exc)}
