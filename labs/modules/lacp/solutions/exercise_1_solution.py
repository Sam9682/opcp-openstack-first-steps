# Solution: Exercise 1 - Create LACP Bond

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    net = managers["network_manager"]

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
    return {"network": network, "port1": port1, "port2": port2, "bond": bond, "name": bond_name}
