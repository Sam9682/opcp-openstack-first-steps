# Solution: Exercise 3 - Apply Security Group

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    sg = managers["security_group_manager"]
    sg_name = f"${STUDENT_ID}-sg-web"
    instance_name = f"${STUDENT_ID}-compute-instance"
    sg.apply_to_instance(sg_name=sg_name, instance_name=instance_name)
    return {"applied": True}
