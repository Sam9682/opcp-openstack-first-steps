# OpenStack First Steps Labs - Progress Tracker

"""
Records and persists per-student exercise/module completion status.
Data is stored as JSON so it survives container restarts via volume mount.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from labs.core import ExerciseStatus, ModuleProgress


class ProgressTracker:
    """Track student progress across lab modules and exercises."""

    def __init__(self, storage_path: str = "progress.json") -> None:
        self._path = Path(storage_path)
        self._data: dict = {"students": {}}
        self._load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def mark_complete(
        self, student_id: str, module_name: str, exercise_id: str
    ) -> None:
        """Mark an exercise as completed and persist."""
        student = self._ensure_student(student_id)
        module = student["modules"].setdefault(
            module_name, {"exercises": {}, "completed": False}
        )
        module["exercises"][exercise_id] = {
            "completed": True,
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }
        # Check module completion.
        if self._all_exercises_done(student_id, module_name):
            module["completed"] = True
        self._save()

    def get_progress(self, student_id: str) -> dict[str, ModuleProgress]:
        """Return progress summary for a student across all modules."""
        student = self._data["students"].get(student_id, {"modules": {}})
        result: dict[str, ModuleProgress] = {}
        for mod_name, mod_data in student["modules"].items():
            exercises: dict[str, ExerciseStatus] = {}
            for ex_id, ex_data in mod_data.get("exercises", {}).items():
                exercises[ex_id] = ExerciseStatus(
                    exercise_id=ex_id,
                    completed=ex_data.get("completed", False),
                    completed_at=ex_data.get("completed_at"),
                )
            result[mod_name] = ModuleProgress(
                module_name=mod_name,
                exercises=exercises,
                completed=mod_data.get("completed", False),
            )
        return result

    def is_module_complete(self, student_id: str, module_name: str) -> bool:
        """Return True only when all exercises in the module are marked complete."""
        student = self._data["students"].get(student_id)
        if student is None:
            return False
        module = student["modules"].get(module_name)
        if module is None:
            return False
        return module.get("completed", False)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _save(self) -> None:
        """Persist progress data to JSON file."""
        with open(self._path, "w", encoding="utf-8") as fh:
            json.dump(self._data, fh, indent=2)

    def _load(self) -> None:
        """Load progress data from JSON file if it exists."""
        if not self._path.exists():
            return
        try:
            with open(self._path, "r", encoding="utf-8") as fh:
                self._data = json.load(fh)
        except (json.JSONDecodeError, OSError):
            self._data = {"students": {}}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _ensure_student(self, student_id: str) -> dict:
        """Return (and lazily create) the student entry."""
        if student_id not in self._data["students"]:
            self._data["students"][student_id] = {"modules": {}}
        return self._data["students"][student_id]

    def _all_exercises_done(self, student_id: str, module_name: str) -> bool:
        """Check if every known exercise in a module is completed.

        Since we don't have a static registry of exercises per module,
        module completion is determined externally (e.g. by the Lab Runner
        after all exercises have been marked). This helper returns True
        when at least one exercise exists and all recorded exercises are
        completed.
        """
        student = self._data["students"].get(student_id, {})
        module = student.get("modules", {}).get(module_name, {})
        exercises = module.get("exercises", {})
        if not exercises:
            return False
        return all(ex.get("completed", False) for ex in exercises.values())
