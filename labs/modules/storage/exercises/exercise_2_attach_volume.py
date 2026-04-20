# Storage Module - Exercise 2: Attach Volume

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class AttachVolumeExercise(Exercise):
    """Attach a volume to a running instance."""

    @property
    def problem_statement(self) -> str:
        return "Attach a block storage volume to a running compute instance."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use volume_manager to attach '{student_id}-storage-volume' "
            "to '{student_id}-compute-instance'.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "volume", "name": "{student_id}-storage-volume", "status": "in-use"}
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        volume_name = f"{student_id}-storage-volume"
        instance_name = f"{student_id}-compute-instance"
        vol = self.managers.get("volume_manager")
        if vol is None:
            return {"error": self._handle_openstack_error(
                "attach volume", "volume_manager not available"
            )}
        try:
            result = vol.attach(volume_name=volume_name, instance_name=instance_name)
            return {"result": result, "volume": volume_name, "instance": instance_name}
        except Exception as exc:
            msg = str(exc)
            if "not found" in msg.lower() or "instance" in msg.lower():
                return {"error": f"Missing instance: {exc}"}
            return {"error": self._handle_openstack_error("attach volume", exc)}
