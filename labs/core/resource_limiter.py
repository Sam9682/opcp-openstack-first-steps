# OpenStack First Steps Labs - Resource Limiter

"""
Enforces per-student resource caps and generates isolated resource names.
"""

from __future__ import annotations

from labs.core import ResourceLimitError, ResourceLimits


class ResourceLimiter:
    """Enforce configurable resource limits for a single student session."""

    def __init__(self, limits: ResourceLimits, student_id: str) -> None:
        self._limits = {
            "instances": limits.max_instances,
            "networks": limits.max_networks,
            "volumes": limits.max_volumes,
            "security_groups": limits.max_security_groups,
        }
        self._student_id = student_id

    def check_limit(self, resource_type: str, current_count: int) -> None:
        """Raise ``ResourceLimitError`` if *current_count* >= the limit.

        Args:
            resource_type: One of ``instances``, ``networks``, ``volumes``,
                ``security_groups``.
            current_count: How many resources of this type already exist.

        Raises:
            ResourceLimitError: With a message containing the limit and
                current usage.
        """
        limit = self._limits.get(resource_type)
        if limit is None:
            raise ResourceLimitError(
                f"Unknown resource type: {resource_type}"
            )
        if current_count >= limit:
            raise ResourceLimitError(
                f"Resource limit exceeded: {current_count}/{limit} "
                f"{resource_type}. Cannot create more."
            )

    def get_usage(self, resource_type: str) -> dict:
        """Return current limit for *resource_type*.

        The caller is responsible for supplying the actual current count
        when calling ``check_limit``; this helper exposes the configured
        ceiling so UIs can display it.
        """
        limit = self._limits.get(resource_type)
        if limit is None:
            raise ResourceLimitError(
                f"Unknown resource type: {resource_type}"
            )
        return {"limit": limit}

    def generate_name(self, base_name: str) -> str:
        """Return an isolated resource name prefixed with the student id."""
        return f"{self._student_id}-{base_name}"
