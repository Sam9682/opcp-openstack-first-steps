# LACP Module - Exercise 3: Attach LACP Bond to Instance

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class AttachBondExercise(Exercise):
    """Attach a LACP bond to a compute instance."""

    @property
    def problem_statement(self) -> str:
        return "Attach a LACP bond to a compute instance for aggregated bandwidth."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use compute_manager to create an instance named '${STUDENT_ID}-lacp-instance'.",
            "Use network_manager to attach '${STUDENT_ID}-lacp-bond' to the instance.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "instance", "name": "${STUDENT_ID}-lacp-instance", "status": "ACTIVE"},
            {"type": "bond_attachment", "bond": "${STUDENT_ID}-lacp-bond", "instance": "${STUDENT_ID}-lacp-instance"},
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        net = self.managers.get("network_manager")
        compute = self.managers.get("compute_manager")
        if net is None or compute is None:
            return {"error": self._handle_openstack_error(
                "attach bond", "network_manager or compute_manager not available"
            )}
        try:
            instance_name = f"${STUDENT_ID}-lacp-instance"
            instance = compute.create(
                name=instance_name,
                image="ubuntu-22.04",
                flavor="s1-4",
            )

            bond_name = f"${STUDENT_ID}-lacp-bond"
            net.attach_bond_to_instance(
                bond_name=bond_name,
                instance_name=instance_name,
            )
            return {"instance": instance, "bond": bond_name, "name": instance_name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("attach bond", exc)}
