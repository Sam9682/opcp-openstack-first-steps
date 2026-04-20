# OpenStack First Steps Labs - Credential Handler

"""
Loads OpenStack credentials from environment variables or a secure config
file and provides masking utilities for safe logging.

Raises CredentialError when no source provides all required fields.
Never accepts credentials via command-line arguments.
"""

from __future__ import annotations

import os
from pathlib import Path

import yaml

from labs.core import CredentialError, Credentials

# Required environment variable names (and their Credentials field names).
_ENV_MAP: dict[str, str] = {
    "OS_AUTH_URL": "auth_url",
    "OS_USERNAME": "username",
    "OS_PASSWORD": "password",
    "OS_PROJECT_NAME": "project_name",
    "OS_DOMAIN_NAME": "domain_name",
}

_SECURE_FILE = Path.home() / ".openstack" / "credentials.yaml"


def load_credentials() -> Credentials:
    """Load credentials from environment variables, falling back to file.

    Priority:
        1. Environment variables (OS_AUTH_URL, OS_USERNAME, …)
        2. ``~/.openstack/credentials.yaml``

    Returns:
        A populated ``Credentials`` instance.

    Raises:
        CredentialError: If neither source provides all required fields.
    """
    creds = _load_from_env()
    if creds is not None:
        return creds

    creds = _load_from_file(_SECURE_FILE)
    if creds is not None:
        return creds

    raise CredentialError(
        "Credentials not found. Set OS_AUTH_URL, OS_USERNAME, OS_PASSWORD, "
        "OS_PROJECT_NAME, and OS_DOMAIN_NAME environment variables, or "
        "provide ~/.openstack/credentials.yaml."
    )


def mask_value(value: str) -> str:
    """Mask a credential value for safe logging.

    Args:
        value: The raw credential string.

    Returns:
        ``'****'`` for strings shorter than 4 characters, otherwise
        ``'****' + last 4 characters``.
    """
    if len(value) < 4:
        return "****"
    return "****" + value[-4:]


# ------------------------------------------------------------------
# Internal helpers
# ------------------------------------------------------------------

def _load_from_env() -> Credentials | None:
    """Attempt to build Credentials from environment variables.

    Returns ``None`` if any required variable is missing or empty.
    """
    values: dict[str, str] = {}
    for env_var, field in _ENV_MAP.items():
        val = os.environ.get(env_var)
        if not val:
            return None
        values[field] = val
    return Credentials(**values)


def _load_from_file(path: Path) -> Credentials | None:
    """Attempt to build Credentials from a YAML file.

    Expected file structure::

        auth_url: https://…
        username: …
        password: …
        project_name: …
        domain_name: …

    Returns ``None`` if the file does not exist or is missing fields.
    """
    if not path.exists():
        return None

    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
    except yaml.YAMLError:
        return None

    if not isinstance(raw, dict):
        return None

    required = {"auth_url", "username", "password", "project_name", "domain_name"}
    if not required.issubset(raw.keys()):
        return None

    values = {k: str(raw[k]) for k in required}
    return Credentials(**values)
