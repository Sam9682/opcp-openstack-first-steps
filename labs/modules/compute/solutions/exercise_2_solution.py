# Solution: Exercise 2 - Resize Instance

from __future__ import annotations


def solve(managers: dict, student_id: str, target_flavor: str) -> dict:
    compute = managers["compute_manager"]
    name = f"{student_id}-compute-instance"
    result = compute.resize(name=name, flavor=target_flavor)
    return {"result": result, "name": name}
