# Solution: Exercise 2 - Manage Rules

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    sg = managers["security_group_manager"]
    sg_name = f"{student_id}-sg-web"
    sg.add_rule(sg_name, protocol="tcp", port_min=443, port_max=443, direction="ingress")
    return {"sg_name": sg_name, "rule_added": True}
