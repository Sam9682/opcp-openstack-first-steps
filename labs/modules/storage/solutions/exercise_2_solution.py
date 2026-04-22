# Solution: Exercise 2 - Attach Volume

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    vol = managers["volume_manager"]
    volume_name = f"${STUDENT_ID}-storage-volume"
    instance_name = f"${STUDENT_ID}-compute-instance"
    result = vol.attach(volume_name=volume_name, instance_name=instance_name)
    return {"result": result}
