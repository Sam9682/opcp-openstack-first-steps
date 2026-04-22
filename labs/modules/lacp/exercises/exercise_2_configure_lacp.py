# LACP Module - Exercise 2: Configure LACP Parameters

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class ConfigureLacpExercise(Exercise):
    """Configure LACP rate, hash policy, and activity mode on a bond."""

    @property
    def problem_statement(self) -> str:
        return "Configure LACP parameters on an existing bond."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use network_manager to update the bond '${STUDENT_ID}-lacp-bond'.",
            "Set lacp_rate to 'fast' (1-second interval).",
            "Set transmit_hash_policy to 'layer3+4' (IP + port hashing).",
            "Set lacp_activity to 'active' (send LACPDU frames).",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {
                "type": "bond",
                "name": "${STUDENT_ID}-lacp-bond",
                "lacp_rate": "fast",
                "transmit_hash_policy": "layer3+4",
                "lacp_activity": "active",
            }
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        net = self.managers.get("network_manager")
        if net is None:
            return {"error": self._handle_openstack_error(
                "configure lacp", "network_manager not available"
            )}
        try:
            bond_name = f"${STUDENT_ID}-lacp-bond"
            result = net.update_bond(
                bond_name=bond_name,
                lacp_rate="fast",
                transmit_hash_policy="layer3+4",
                lacp_activity="active",
            )
            return {"bond": result, "name": bond_name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("configure lacp", exc)}
