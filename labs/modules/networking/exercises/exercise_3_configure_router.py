# Networking Module - Exercise 3: Configure Router

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class ConfigureRouterExercise(Exercise):
    """Configure a router and attach it to a subnet."""

    @property
    def problem_statement(self) -> str:
        return "Configure a router and attach it to a subnet."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use network_manager to create a router named '{student_id}-net-router'.",
            "Attach the router to '{student_id}-net-subnet'.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "router", "name": "{student_id}-net-router", "status": "ACTIVE"}
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        router_name = f"{student_id}-net-router"
        subnet_name = f"{student_id}-net-subnet"
        net = self.managers.get("network_manager")
        if net is None:
            return {"error": self._handle_openstack_error(
                "configure router", "network_manager not available"
            )}
        try:
            router = net.create_router(name=router_name)
            net.add_router_interface(router_name=router_name, subnet_name=subnet_name)
            return {"router": router, "name": router_name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("configure router", exc)}
