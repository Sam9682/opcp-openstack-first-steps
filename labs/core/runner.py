# OpenStack First Steps Labs - Lab Runner

"""
Top-level orchestrator that wires config, credentials, managers,
assessment, progress tracking, and resource limiting together.
"""

from __future__ import annotations

import importlib
import logging

from labs.core import LabConfig, Credentials
from labs.core.assessment import AssessmentEngine
from labs.core.progress import ProgressTracker
from labs.core.resource_limiter import ResourceLimiter
from labs.scripts.cleanup_lab import LabCleanup
from labs.scripts.setup_lab import LabSetup
from labs.templates.exercise_template import Exercise

logger = logging.getLogger(__name__)


class LabRunner:
    """Orchestrate the full lab lifecycle."""

    def __init__(self, config: LabConfig, credentials: Credentials) -> None:
        self._config = config
        self._credentials = credentials

        # Framework managers — in a real deployment these would be
        # initialised from the opcp-openstack-automation framework.
        self._managers: dict = self._init_managers(config, credentials)

        self._progress = ProgressTracker()
        self._assessment = AssessmentEngine(self._managers, self._progress)
        self._managers["assessment_engine"] = self._assessment

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start_module(self, module_name: str, student_id: str) -> None:
        """Setup module environment and present exercises."""
        limiter = self._limiter(student_id)
        self._managers["student_id"] = student_id
        setup = LabSetup(self._config, self._managers, student_id)
        setup.setup_module(module_name)
        logger.info("Module '%s' ready for student '%s'.", module_name, student_id)

    def run_exercise(
        self,
        module_name: str,
        exercise_id: str,
        student_id: str,
        **kwargs,
    ) -> dict:
        """Execute an exercise with resource limit checks."""
        limiter = self._limiter(student_id)
        exercise = self._load_exercise(module_name, exercise_id)
        kwargs.setdefault("student_id", student_id)
        try:
            return exercise.run(**kwargs)
        except Exception as exc:
            return {"error": Exercise._handle_openstack_error(
                f"run {exercise_id}", exc
            )}

    def assess_exercise(
        self, module_name: str, exercise_id: str, student_id: str
    ):
        """Validate exercise and update progress."""
        return self._assessment.validate_exercise(
            module_name, exercise_id, student_id
        )

    def end_session(self, student_id: str) -> None:
        """Cleanup resources and revoke tokens."""
        cleanup = LabCleanup(self._managers, student_id)
        failures = cleanup.cleanup_all()
        cleanup.revoke_session_tokens()
        if failures:
            logger.warning(
                "Session cleanup for '%s' had %d failures.", student_id, len(failures)
            )

    def get_progress(self, student_id: str) -> dict:
        """Return student progress summary."""
        return self._progress.get_progress(student_id)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _limiter(self, student_id: str) -> ResourceLimiter:
        return ResourceLimiter(self._config.resource_limits, student_id)

    def _load_exercise(self, module_name: str, exercise_id: str) -> Exercise:
        module_path = f"labs.modules.{module_name}.exercises.{exercise_id}"
        mod = importlib.import_module(module_path)
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, Exercise)
                and attr is not Exercise
            ):
                return attr(module_name, exercise_id, self._managers)
        raise ValueError(f"No Exercise subclass found in {module_path}")

    @staticmethod
    def _init_managers(config: LabConfig, credentials: Credentials) -> dict:
        """Initialise framework managers.

        In a full deployment this would import and instantiate the real
        managers from opcp-openstack-automation. Here we return a dict
        that exercises and the assessment engine can populate.
        """
        # Placeholder — real wiring depends on the automation framework.
        return {
            "auth_manager": None,
            "compute_manager": None,
            "network_manager": None,
            "volume_manager": None,
            "security_group_manager": None,
        }
