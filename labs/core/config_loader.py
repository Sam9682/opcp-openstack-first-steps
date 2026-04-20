# OpenStack First Steps Labs - Configuration Loader

"""
Loads and validates lab_config.yaml.

Raises ConfigError with descriptive messages on missing file, invalid YAML,
or missing/wrong-type fields. Exits with non-zero code on configuration
errors (fail-fast for infrastructure errors).
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from labs.core import ConfigError, LabConfig, ResourceLimits


def load_config(config_path: str = "config/lab_config.yaml") -> LabConfig:
    """Load and validate lab configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        A validated LabConfig instance.

    Raises:
        ConfigError: If the file is missing, contains invalid YAML,
                     or fails validation.
    """
    path = Path(config_path)

    if not path.exists():
        raise ConfigError(f"Configuration file not found: {config_path}")

    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {config_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigError(
            f"Configuration file {config_path} must contain a YAML mapping, "
            f"got {type(raw).__name__}"
        )

    return validate_config(raw)


def _get_nested(data: dict, dotted_key: str) -> object:
    """Retrieve a value from a nested dict using a dotted key path.

    Args:
        data: The root dictionary.
        dotted_key: Key path like ``"openstack.endpoint"``.

    Returns:
        The value at the given path.

    Raises:
        ConfigError: If any segment of the path is missing.
    """
    keys = dotted_key.split(".")
    current = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            raise ConfigError(f"Missing required config field: {dotted_key}")
        current = current[key]
    return current


def _check_type(value: object, expected_type: type, field_name: str) -> None:
    """Assert *value* is an instance of *expected_type*.

    Raises:
        ConfigError: With a message naming the field and the expected type.
    """
    if not isinstance(value, expected_type):
        raise ConfigError(
            f"Config field '{field_name}' must be {expected_type.__name__}, "
            f"got {type(value).__name__}"
        )


def validate_config(raw: dict) -> LabConfig:
    """Validate a raw YAML dict and return a LabConfig instance.

    Required fields:
        - openstack.endpoint  (str)
        - openstack.default_flavor  (str)
        - openstack.default_image  (str)
        - modules.order  (list)
        - session.timeout_minutes  (int)
        - session.resource_limits.max_instances  (int)
        - session.resource_limits.max_networks  (int)
        - session.resource_limits.max_volumes  (int)
        - session.resource_limits.max_security_groups  (int)

    Raises:
        ConfigError: On missing or wrong-type fields.
    """
    # --- openstack section ---
    endpoint = _get_nested(raw, "openstack.endpoint")
    _check_type(endpoint, str, "openstack.endpoint")

    default_flavor = _get_nested(raw, "openstack.default_flavor")
    _check_type(default_flavor, str, "openstack.default_flavor")

    default_image = _get_nested(raw, "openstack.default_image")
    _check_type(default_image, str, "openstack.default_image")

    # --- modules section ---
    module_order = _get_nested(raw, "modules.order")
    _check_type(module_order, list, "modules.order")

    # --- session section ---
    timeout = _get_nested(raw, "session.timeout_minutes")
    _check_type(timeout, int, "session.timeout_minutes")

    # --- resource limits ---
    limits_fields = {
        "session.resource_limits.max_instances": "max_instances",
        "session.resource_limits.max_networks": "max_networks",
        "session.resource_limits.max_volumes": "max_volumes",
        "session.resource_limits.max_security_groups": "max_security_groups",
    }

    limits_kwargs: dict[str, int] = {}
    for dotted, attr in limits_fields.items():
        val = _get_nested(raw, dotted)
        _check_type(val, int, dotted)
        limits_kwargs[attr] = val

    resource_limits = ResourceLimits(**limits_kwargs)

    return LabConfig(
        openstack_endpoint=endpoint,
        default_flavor=default_flavor,
        default_image=default_image,
        module_order=module_order,
        resource_limits=resource_limits,
        session_timeout=timeout,
    )
