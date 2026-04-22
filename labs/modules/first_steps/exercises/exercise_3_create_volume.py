# OpenStack First Steps Labs - Exercise 3: Create Volume

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class CreateVolumeExercise(Exercise):
    """Create a block storage volume using the Cinder API via volume_manager."""

    @property
    def problem_statement(self) -> str:
        return "Create a block storage volume using the Cinder API."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use volume_manager to create a volume.",
            "Name it '${STUDENT_ID}-first-volume'.",
            "Set the size to 1 GB.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {
                "type": "volume",
                "name": "${STUDENT_ID}-first-volume",
                "status": "available",
            }
        ]

    def run(self, **kwargs) -> dict:
        student_id = kwargs.get("student_id", "")
        name = f"${STUDENT_ID}-first-volume"
        volume_mgr = self.managers.get("volume_manager")
        if volume_mgr is None:
            return {"error": self._handle_openstack_error(
                "create volume", "volume_manager not available"
            )}
        try:
            volume = volume_mgr.create(name=name, size=kwargs.get("size", 1))
            return {"volume": volume, "name": name}
        except Exception as exc:
            return {"error": self._handle_openstack_error("create volume", exc)}
