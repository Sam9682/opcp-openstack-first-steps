# Solution: Exercise 1 - Launch Instance

from __future__ import annotations


def solve(managers: dict, student_id: str, config: dict) -> dict:
    compute = managers["compute_manager"]
    name = f"{student_id}-compute-instance"
    instance = compute.create(
        name=name,
        flavor=config.get("default_flavor", "m1.small"),
        image=config.get("default_image", "ubuntu-22.04"),
    )
    return {"instance": instance, "name": name}
