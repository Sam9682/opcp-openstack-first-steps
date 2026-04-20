# OpenStack First Steps Labs - Lab Cleanup

"""
Tears down OpenStack resources created during a lab session.
Best-effort: individual failures are logged but do not stop remaining
deletions.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class LabCleanup:
    """Delete OpenStack resources for a student session."""

    def __init__(self, managers: dict, student_id: str) -> None:
        self._managers = managers
        self._student_id = student_id

    def cleanup_module(self, module_name: str) -> list[str]:
        """Delete all resources for *module_name*.

        Returns a list of failure descriptions for resources that could
        not be deleted.
        """
        from labs.scripts.setup_lab import LabSetup

        resources = LabSetup._module_resources(module_name)
        failures: list[str] = []
        # Delete in reverse order (dependents first).
        for resource in reversed(resources):
            rtype = resource["type"]
            rname = resource["name"].format(student_id=self._student_id)
            try:
                manager = self._get_manager(rtype)
                if manager is not None:
                    manager.delete(rname)
                    logger.info("Deleted %s '%s'.", rtype, rname)
            except Exception as exc:
                msg = f"Failed to delete {rtype} '{rname}': {exc}"
                logger.warning(msg)
                failures.append(msg)
        return failures

    def cleanup_all(self) -> list[str]:
        """Delete all student resources across all modules.

        Continues on individual failures and returns the full list of
        failure descriptions.
        """
        from labs.scripts.setup_lab import LabSetup

        all_modules = [
            "first_steps", "authentication", "compute",
            "networking", "storage", "security_groups", "lacp",
        ]
        failures: list[str] = []
        for module_name in all_modules:
            failures.extend(self.cleanup_module(module_name))
        return failures

    def revoke_session_tokens(self) -> None:
        """Revoke any session-scoped tokens created during the session."""
        auth_manager = self._managers.get("auth_manager")
        if auth_manager is None:
            logger.warning("No auth_manager available — cannot revoke tokens.")
            return
        try:
            auth_manager.revoke_token()
            logger.info("Session tokens revoked for student '%s'.", self._student_id)
        except Exception as exc:
            logger.warning(
                "Failed to revoke tokens for student '%s': %s",
                self._student_id, exc,
            )

    def _get_manager(self, resource_type: str):
        """Map resource type to framework manager."""
        mapping = {
            "instance": "compute_manager",
            "snapshot": "compute_manager",
            "network": "network_manager",
            "subnet": "network_manager",
            "router": "network_manager",
            "port": "network_manager",
            "bond": "network_manager",
            "bond_attachment": "network_manager",
            "volume": "volume_manager",
            "volume_snapshot": "volume_manager",
            "security_group": "security_group_manager",
        }
        key = mapping.get(resource_type)
        return self._managers.get(key) if key else None
