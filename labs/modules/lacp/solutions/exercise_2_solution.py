# Solution: Exercise 2 - Configure LACP Parameters

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    net = managers["network_manager"]
    bond_name = f"${STUDENT_ID}-lacp-bond"
    result = net.update_bond(
        bond_name=bond_name,
        lacp_rate="fast",
        transmit_hash_policy="layer3+4",
        lacp_activity="active",
    )
    return {"bond": result, "name": bond_name}
