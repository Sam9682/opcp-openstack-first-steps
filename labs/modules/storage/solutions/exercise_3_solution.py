# Solution: Exercise 3 - Manage Volume Snapshots

from __future__ import annotations


def solve(managers: dict, student_id: str) -> dict:
    vol = managers["volume_manager"]
    volume_name = f"{student_id}-storage-volume"
    snapshot_name = f"{student_id}-storage-snapshot"
    snapshot = vol.create_snapshot(volume_name=volume_name, snapshot_name=snapshot_name)
    return {"snapshot": snapshot, "name": snapshot_name}
