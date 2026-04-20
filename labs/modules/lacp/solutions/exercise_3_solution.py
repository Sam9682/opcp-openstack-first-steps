# Solution: Exercise 3 - Attach LACP Bond to Instance

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    net = managers["network_manager"]
    compute = managers["compute_manager"]

    instance_name = f"{student_id}-lacp-instance"
    instance = compute.create(
        name=instance_name,
        image="ubuntu-22.04",
        flavor="s1-4",
    )

    bond_name = f"{student_id}-lacp-bond"
    net.attach_bond_to_instance(bond_name=bond_name, instance_name=instance_name)
    return {"instance": instance, "bond": bond_name, "name": instance_name}
