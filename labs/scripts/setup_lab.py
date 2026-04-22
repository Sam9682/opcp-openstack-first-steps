# OpenStack First Steps Labs - Lab Setup

"""
Provisions required OpenStack resources for a lab module.
Idempotent: running twice produces the same state without duplicates.
"""

from __future__ import annotations

import logging

from labs.core import LabConfig

logger = logging.getLogger(__name__)


class LabSetup:
    """Provision OpenStack resources for a lab module."""

    def __init__(self, config: LabConfig, managers: dict, student_id: str) -> None:
        self._config = config
        self._managers = managers
        self._student_id = student_id

    def setup_module(self, module_name: str) -> None:
        """Provision all required resources for *module_name*.

        Checks for existing resources first to ensure idempotency.
        """
        resources = self._module_resources(module_name)
        for resource in resources:
            rtype = resource["type"]
            rname = resource["name"].format(student_id=self._student_id)
            if self._resource_exists(rtype, rname):
                logger.info("Resource %s '%s' already exists — skipping.", rtype, rname)
                continue
            self._create_resource(rtype, rname, resource.get("params", {}))
            logger.info("Created %s '%s'.", rtype, rname)

    def _resource_exists(self, resource_type: str, name: str) -> bool:
        """Check if a resource already exists (for idempotency)."""
        manager = self._get_manager(resource_type)
        if manager is None:
            return False
        try:
            return manager.get(name) is not None
        except Exception:
            return False

    def _create_resource(self, resource_type: str, name: str, params: dict) -> None:
        """Create a resource via the appropriate framework manager."""
        manager = self._get_manager(resource_type)
        if manager is None:
            logger.warning("No manager for resource type: %s", resource_type)
            return
        manager.create(name=name, **params)

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

    @staticmethod
    def _module_resources(module_name: str) -> list[dict]:
        """Return the list of resources required for a module.

        Each entry is a dict with ``type``, ``name`` (may contain
        ``${STUDENT_ID}`` placeholder), and optional ``params``.
        """
        # Module-specific resource definitions.
        registry: dict[str, list[dict]] = {
            "first_steps": [
                {"type": "instance", "name": "${STUDENT_ID}-first-instance"},
                {"type": "network", "name": "${STUDENT_ID}-first-network"},
                {"type": "volume", "name": "${STUDENT_ID}-first-volume"},
            ],
            "authentication": [],
            "compute": [
                {"type": "snapshot", "name": "${STUDENT_ID}-compute-snapshot"},
                {"type": "instance", "name": "${STUDENT_ID}-compute-instance"},
                {"type": "network", "name": "${STUDENT_ID}-compute-network"},
            ],
            "networking": [],
            "storage": [
                {"type": "volume_snapshot", "name": "${STUDENT_ID}-storage-snapshot"},
                {"type": "volume", "name": "${STUDENT_ID}-storage-volume"},
                {"type": "network", "name": "${STUDENT_ID}-storage-network"},
            ],
            "security_groups": [
                {"type": "security_group", "name": "${STUDENT_ID}-sg-web"},
                {"type": "network", "name": "${STUDENT_ID}-sg-network"},
                {"type": "security_group", "name": "${STUDENT_ID}-default-sg"},
            ],
            "lacp": [
                {"type": "bond_attachment", "name": "${STUDENT_ID}-lacp-bond"},
                {"type": "instance", "name": "${STUDENT_ID}-lacp-instance"},
                {"type": "bond", "name": "${STUDENT_ID}-lacp-bond"},
                {"type": "port", "name": "${STUDENT_ID}-lacp-port-1"},
                {"type": "port", "name": "${STUDENT_ID}-lacp-port-2"},
                {"type": "network", "name": "${STUDENT_ID}-lacp-network"},
            ],
        }
        return registry.get(module_name, [])
