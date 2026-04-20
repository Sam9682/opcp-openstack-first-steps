# Solution: Exercise 1 - Create Network

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    net = managers["network_manager"]
    name = f"{student_id}-net-network"
    network = net.create(name=name)
    return {"network": network, "name": name}
