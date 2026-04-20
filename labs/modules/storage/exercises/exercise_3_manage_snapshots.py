# Storage Module - Exercise 3: Manage Volume Snapshots

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class ManageVolumeSnapshotsExercise(Exercise):
    """Create and manage volume snapshots."""

    @property
    def problem_statement(self) -> str:
        return "Create and manage snapshots of a block storage volume."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use volume_manager to create a snapshot of '{student_id}-storage-volume'.",
            "Name the snapshot '{student_id}-storage-snapshot'.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "volume", "name": "{student_id}-storage-snapshot", "status": "available"}
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        volume_name = f"{student_id}-storage-volume"
        snapshot_name = f"{student_id}-storage-snapshot"
        vol = self.managers.get("volume_manager")
        if vol is None:
            return {"error": self._handle_openstack_error(
                "manage snapshots", "volume_manager not available"
            )}
        try:
            snapshot = vol.create_snapshot(
                volume_name=volume_name, snapshot_name=snapshot_name
            )
            return {"snapshot": snapshot, "name": snapshot_name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("manage snapshots", exc)}
