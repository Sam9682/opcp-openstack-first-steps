# Solution: Exercise 1 - Create Volume

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    vol = managers["volume_manager"]
    name = f"${STUDENT_ID}-storage-volume"
    volume = vol.create(name=name, size=1)
    return {"volume": volume, "name": name}
