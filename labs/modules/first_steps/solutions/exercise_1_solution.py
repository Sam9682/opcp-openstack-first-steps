# Solution: Exercise 1 - Create Compute Instance

"""
Reference solution for the first_steps create-instance exercise.
Uses compute_manager from the Automation Framework.
"""

from __future__ import annotations


def solve(managers: dict, student_id: str, config: dict) -> dict:
    """Create a compute instance with the default flavor and image."""
    compute = managers["compute_manager"]
    name = f"{student_id}-first-instance"
    instance = compute.create(
        name=name,
        flavor=config.get("default_flavor", "m1.small"),
        image=config.get("default_image", "ubuntu-22.04"),
    )
    return {"instance": instance, "name": name}
