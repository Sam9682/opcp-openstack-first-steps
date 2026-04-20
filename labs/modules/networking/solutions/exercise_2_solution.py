# Solution: Exercise 2 - Create Subnet

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    net = managers["network_manager"]
    name = f"{student_id}-net-subnet"
    network_name = f"{student_id}-net-network"
    subnet = net.create_subnet(network_name=network_name, name=name, cidr="10.0.0.0/24")
    return {"subnet": subnet, "name": name}
