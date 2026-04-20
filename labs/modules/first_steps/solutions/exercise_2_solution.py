# Solution: Exercise 2 - Create Network

"""
Reference solution for the first_steps create-network exercise.
Uses network_manager from the Automation Framework.
"""

from __future__ import annotations


def solve(managers: dict, student_id: str, **kwargs) -> dict:
    """Create a virtual network."""
    network_mgr = managers["network_manager"]
    name = f"{student_id}-first-network"
    network = network_mgr.create(name=name)
    return {"network": network, "name": name}
