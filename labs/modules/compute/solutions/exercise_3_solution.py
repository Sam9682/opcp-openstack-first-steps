# Solution: Exercise 3 - Manage Instance Snapshots

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    compute = managers["compute_manager"]
    instance_name = f"${STUDENT_ID}-compute-instance"
    snapshot_name = f"${STUDENT_ID}-compute-snapshot"
    snapshot = compute.create_snapshot(
        instance_name=instance_name, snapshot_name=snapshot_name
    )
    return {"snapshot": snapshot, "name": snapshot_name}
