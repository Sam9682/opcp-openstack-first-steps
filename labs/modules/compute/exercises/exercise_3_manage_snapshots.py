# Compute Module - Exercise 3: Manage Instance Snapshots

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class ManageSnapshotsExercise(Exercise):
    """Create and manage instance snapshots."""

    @property
    def problem_statement(self) -> str:
        return "Create and manage snapshots of a compute instance."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use compute_manager to create a snapshot of '${STUDENT_ID}-compute-instance'.",
            "Name the snapshot '${STUDENT_ID}-compute-snapshot'.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "instance", "name": "${STUDENT_ID}-compute-snapshot", "status": "ACTIVE"}
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        instance_name = f"${STUDENT_ID}-compute-instance"
        snapshot_name = f"${STUDENT_ID}-compute-snapshot"
        compute = self.managers.get("compute_manager")
        if compute is None:
            return {"error": self._handle_openstack_error(
                "manage snapshots", "compute_manager not available"
            )}
        try:
            snapshot = compute.create_snapshot(
                instance_name=instance_name, snapshot_name=snapshot_name
            )
            return {"snapshot": snapshot, "name": snapshot_name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("manage snapshots", exc)}
