# Solution: Exercise 1 - Create Security Group

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    sg = managers["security_group_manager"]
    name = f"{student_id}-sg-web"
    group = sg.create(name=name, description="Web traffic security group")
    return {"security_group": group, "name": name}
