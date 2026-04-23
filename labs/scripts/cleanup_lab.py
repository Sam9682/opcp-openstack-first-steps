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
        if not resources:
            logger.info("[%s] No resources defined — nothing to clean.", module_name)
            return []

        logger.info("[%s] Found %d resource(s) to clean up.", module_name, len(resources))
        failures: list[str] = []
        deleted = 0
        skipped = 0
        # Delete in reverse order (dependents first).
        for i, resource in enumerate(reversed(resources), 1):
            rtype = resource["type"]
            rname = resource["name"].replace("${STUDENT_ID}", self._student_id)
            logger.info(
                "[%s] (%d/%d) Processing %s '%s'...",
                module_name, i, len(resources), rtype, rname,
            )
            try:
                manager = self._get_manager(rtype)
                if manager is None:
                    logger.warning(
                        "[%s] (%d/%d) No manager for type '%s' — skipped.",
                        module_name, i, len(resources), rtype,
                    )
                    skipped += 1
                    continue
                found = manager.get(rname)
                if found is None:
                    logger.info(
                        "[%s] (%d/%d) %s '%s' not found — already cleaned.",
                        module_name, i, len(resources), rtype, rname,
                    )
                    skipped += 1
                    continue
                manager.delete(rname)
                deleted += 1
                logger.info(
                    "[%s] (%d/%d) ✓ Deleted %s '%s'.",
                    module_name, i, len(resources), rtype, rname,
                )
            except Exception as exc:
                msg = f"Failed to delete {rtype} '{rname}': {exc}"
                logger.warning(
                    "[%s] (%d/%d) ✗ %s", module_name, i, len(resources), msg,
                )
                failures.append(msg)

        logger.info(
            "[%s] Done — %d deleted, %d skipped, %d failed.",
            module_name, deleted, skipped, len(failures),
        )
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
        logger.info("=" * 60)
        logger.info("Starting cleanup for %d module(s)...", len(all_modules))
        logger.info("=" * 60)
        for idx, module_name in enumerate(all_modules, 1):
            logger.info(
                "--- Module %d/%d: %s ---", idx, len(all_modules), module_name,
            )
            module_failures = self.cleanup_module(module_name)
            failures.extend(module_failures)
        logger.info("=" * 60)
        logger.info(
            "Cleanup complete — total failures: %d.", len(failures),
        )
        logger.info("=" * 60)
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


def main() -> None:
    """CLI entry point for lab cleanup."""
    import argparse
    import sys

    try:
        import openstack
    except ImportError:
        logger.error(
            "The 'openstacksdk' package is not installed. "
            "Install it with: pip install openstacksdk"
        )
        sys.exit(1)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        force=True,
    )
    # Ensure our module logger outputs to the console even if
    # openstacksdk or another library already configured the root logger.
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        _handler = logging.StreamHandler()
        _handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
        logger.addHandler(_handler)

    parser = argparse.ArgumentParser(
        description="Clean up OpenStack resources created during a lab session.",
    )
    parser.add_argument(
        "--student-id",
        required=True,
        help="Student identifier used as resource name prefix.",
    )
    parser.add_argument(
        "--module",
        default=None,
        help="Clean up a single module (e.g. compute, storage). "
             "If omitted, all modules are cleaned.",
    )
    args = parser.parse_args()

    logger.info("Connecting to OpenStack...")
    try:
        conn = openstack.connect()
        logger.info("Connected to OpenStack successfully.")
    except Exception as exc:
        logger.error("Failed to connect to OpenStack: %s", exc)
        sys.exit(1)

    # Build a lightweight managers dict that wraps the SDK connection.
    managers = {
        "compute_manager": _SdkManager(conn, "compute"),
        "network_manager": _SdkManager(conn, "network"),
        "volume_manager": _SdkManager(conn, "volume"),
        "security_group_manager": _SdkManager(conn, "network"),
    }

    cleanup = LabCleanup(managers=managers, student_id=args.student_id)

    if args.module:
        logger.info(
            "Cleaning module '%s' for student '%s'...",
            args.module, args.student_id,
        )
        failures = cleanup.cleanup_module(args.module)
    else:
        logger.info(
            "Cleaning ALL modules for student '%s'...", args.student_id,
        )
        failures = cleanup.cleanup_all()

    logger.info("Revoking session tokens...")
    cleanup.revoke_session_tokens()

    print()  # blank line before final summary
    if failures:
        logger.warning(
            "Completed with %d failure(s):", len(failures),
        )
        for i, f in enumerate(failures, 1):
            logger.warning("  %d. %s", i, f)
        print()
        logger.info(
            "Tip: re-run the command to retry failed deletions, or "
            "delete them manually with the OpenStack CLI."
        )
        sys.exit(1)
    else:
        logger.info("All resources for student '%s' cleaned up successfully.", args.student_id)


class _SdkManager:
    """Minimal wrapper around openstacksdk to satisfy LabCleanup.

    Provides ``delete(name)`` and ``get(name)`` for each resource type
    by searching resources whose name matches the student prefix.
    """

    _DELETE_MAP = {
        "compute": {
            "instance": "delete_server",
            "snapshot": "delete_image",
        },
        "network": {
            "network": "delete_network",
            "subnet": "delete_subnet",
            "router": "delete_router",
            "port": "delete_port",
            "bond": "delete_trunk",
            "bond_attachment": "delete_trunk",
            "security_group": "delete_security_group",
        },
        "volume": {
            "volume": "delete_volume",
            "volume_snapshot": "delete_volume_snapshot",
        },
    }

    def __init__(self, conn, service: str) -> None:
        self._conn = conn
        self._service = service

    def delete(self, name: str) -> None:
        """Best-effort delete a resource by name."""
        resource = self.get(name)
        if resource is None:
            logger.info("Resource '%s' not found — skipping.", name)
            return
        # Find the right delete method based on resource type
        proxy = getattr(self._conn, self._service)
        # Try common delete patterns
        for rtype, method_name in self._DELETE_MAP.get(self._service, {}).items():
            method = getattr(proxy, method_name, None)
            if method is not None:
                try:
                    method(resource["id"])
                    return
                except Exception:
                    continue
        logger.warning("No delete method found for resource '%s'.", name)

    def get(self, name: str):
        """Find a resource by name, return None if not found."""
        proxy = getattr(self._conn, self._service)
        # Search across common resource types for this service
        search_methods = {
            "compute": ["find_server", "find_image"],
            "network": [
                "find_network", "find_subnet", "find_router",
                "find_port", "find_security_group",
            ],
            "volume": ["find_volume", "find_volume_snapshot"],
        }
        for method_name in search_methods.get(self._service, []):
            method = getattr(proxy, method_name, None)
            if method is not None:
                try:
                    result = method(name, ignore_missing=True)
                    if result is not None:
                        return result
                except Exception:
                    continue
        return None


if __name__ == "__main__":
    main()
