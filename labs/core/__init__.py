# OpenStack First Steps Labs - Core Package

"""
Core data models and exceptions for the OpenStack First Steps Labs platform.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------

class ConfigError(Exception):
    """Raised when lab configuration is missing, invalid, or contains wrong types."""


class CredentialError(Exception):
    """Raised when required credentials are missing or cannot be loaded."""


class ResourceLimitError(Exception):
    """Raised when a resource creation would exceed the configured limit."""


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ResourceLimits:
    """Per-student resource caps loaded from lab_config.yaml."""

    max_instances: int
    max_networks: int
    max_volumes: int
    max_security_groups: int


@dataclass
class LabConfig:
    """Immutable configuration loaded from lab_config.yaml."""

    openstack_endpoint: str
    default_flavor: str
    default_image: str
    module_order: list[str]
    resource_limits: ResourceLimits
    session_timeout: int


@dataclass
class Credentials:
    """OpenStack authentication credentials."""

    auth_url: str
    username: str
    password: str  # never logged
    project_name: str
    domain_name: str


@dataclass
class ExerciseStatus:
    """Completion status of a single exercise."""

    exercise_id: str
    completed: bool
    completed_at: str | None = None


@dataclass
class ModuleProgress:
    """Progress within a single lab module."""

    module_name: str
    exercises: dict[str, ExerciseStatus] = field(default_factory=dict)
    completed: bool = False


@dataclass
class AssessmentResult:
    """Result returned by the Assessment Engine after validating an exercise."""

    passed: bool
    exercise_id: str
    feedback: str
    expected_outcomes: list
    actual_outcomes: list
    mismatches: list[str] = field(default_factory=list)
