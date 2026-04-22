# Solution: Exercise 3 - Create Volume

"""
Reference solution for the first_steps create-volume exercise.
Uses volume_manager from the Automation Framework.
"""

from __future__ import annotations


def solve(managers: dict, student_id: str, **kwargs) -> dict:
    """Create a 1 GB block storage volume."""
    volume_mgr = managers["volume_manager"]
    name = f"${STUDENT_ID}-first-volume"
    volume = volume_mgr.create(name=name, size=1)
    return {"volume": volume, "name": name}
