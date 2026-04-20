# Solution: Exercise 3 - Configure Router

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    net = managers["network_manager"]
    router_name = f"{student_id}-net-router"
    subnet_name = f"{student_id}-net-subnet"
    router = net.create_router(name=router_name)
    net.add_router_interface(router_name=router_name, subnet_name=subnet_name)
    return {"router": router, "name": router_name}
