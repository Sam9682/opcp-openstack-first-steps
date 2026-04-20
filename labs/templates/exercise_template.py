# OpenStack First Steps Labs - Exercise Base Class

"""
Standardized template that all lab exercises inherit from.

Subclasses must implement the abstract properties (``problem_statement``,
``instructions``, ``expected_outcomes``) and the ``run`` method.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Exercise(ABC):
    """Base class for all lab exercises."""

    def __init__(self, module_name: str, exercise_id: str, managers: dict) -> None:
        self.module_name = module_name
        self.exercise_id = exercise_id
        self.managers = managers

    # ------------------------------------------------------------------
    # Abstract interface — subclasses must implement
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def problem_statement(self) -> str:
        """Return the exercise problem statement."""

    @property
    @abstractmethod
    def instructions(self) -> list[str]:
        """Return step-by-step instructions."""

    @property
    @abstractmethod
    def expected_outcomes(self) -> list[dict]:
        """Return expected outcomes for assessment validation."""

    @abstractmethod
    def run(self, **kwargs) -> dict:
        """Execute the exercise. Subclasses implement this."""

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------

    def verify(self) -> "AssessmentResult":  # noqa: F821
        """Verify the exercise solution via the assessment engine.

        Delegates to the assessment engine attached to the managers dict.
        Returns an ``AssessmentResult``.
        """
        assessment_engine = self.managers.get("assessment_engine")
        if assessment_engine is None:
            from labs.core import AssessmentResult

            return AssessmentResult(
                passed=False,
                exercise_id=self.exercise_id,
                feedback="Assessment engine not available.",
                expected_outcomes=self.expected_outcomes,
                actual_outcomes=[],
            )
        return assessment_engine.validate_exercise(
            self.module_name, self.exercise_id, self.managers.get("student_id", "")
        )

    @staticmethod
    def _handle_openstack_error(operation: str, error: Exception | str) -> str:
        """Format a descriptive error message.

        Args:
            operation: The operation that was attempted (e.g. "create instance").
            error: The exception or error detail string.

        Returns:
            A human-readable message containing both *operation* and *error*.
        """
        return f"Operation '{operation}' failed: {error}"
