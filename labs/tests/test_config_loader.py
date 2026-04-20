# Tests for core/config_loader.py

"""Unit tests for load_config and validate_config."""

from __future__ import annotations

import os
import textwrap

import pytest

from labs.core import ConfigError, LabConfig, ResourceLimits
from labs.core.config_loader import load_config, validate_config


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_RAW: dict = {
    "openstack": {
        "endpoint": "https://cloud.example.com:5000/v3",
        "default_flavor": "m1.small",
        "default_image": "ubuntu-22.04",
    },
    "modules": {
        "order": ["first_steps", "authentication", "compute"],
    },
    "session": {
        "timeout_minutes": 120,
        "resource_limits": {
            "max_instances": 3,
            "max_networks": 2,
            "max_volumes": 3,
            "max_security_groups": 5,
        },
    },
}


def _write_yaml(tmp_path, content: str, filename: str = "lab_config.yaml") -> str:
    """Write *content* to a YAML file and return its path."""
    p = tmp_path / filename
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return str(p)


# ---------------------------------------------------------------------------
# validate_config — happy path
# ---------------------------------------------------------------------------

class TestValidateConfigHappyPath:
    def test_returns_lab_config(self):
        result = validate_config(VALID_RAW)
        assert isinstance(result, LabConfig)

    def test_populates_openstack_fields(self):
        cfg = validate_config(VALID_RAW)
        assert cfg.openstack_endpoint == "https://cloud.example.com:5000/v3"
        assert cfg.default_flavor == "m1.small"
        assert cfg.default_image == "ubuntu-22.04"

    def test_populates_module_order(self):
        cfg = validate_config(VALID_RAW)
        assert cfg.module_order == ["first_steps", "authentication", "compute"]

    def test_populates_session_timeout(self):
        cfg = validate_config(VALID_RAW)
        assert cfg.session_timeout == 120

    def test_populates_resource_limits(self):
        cfg = validate_config(VALID_RAW)
        assert isinstance(cfg.resource_limits, ResourceLimits)
        assert cfg.resource_limits.max_instances == 3
        assert cfg.resource_limits.max_networks == 2
        assert cfg.resource_limits.max_volumes == 3
        assert cfg.resource_limits.max_security_groups == 5


# ---------------------------------------------------------------------------
# validate_config — missing fields
# ---------------------------------------------------------------------------

class TestValidateConfigMissingFields:
    @pytest.mark.parametrize(
        "remove_path",
        [
            "openstack.endpoint",
            "openstack.default_flavor",
            "openstack.default_image",
            "modules.order",
            "session.timeout_minutes",
            "session.resource_limits.max_instances",
            "session.resource_limits.max_networks",
            "session.resource_limits.max_volumes",
            "session.resource_limits.max_security_groups",
        ],
    )
    def test_missing_field_raises_config_error(self, remove_path: str):
        import copy

        raw = copy.deepcopy(VALID_RAW)
        keys = remove_path.split(".")
        target = raw
        for k in keys[:-1]:
            target = target[k]
        del target[keys[-1]]

        with pytest.raises(ConfigError, match="Missing required config field"):
            validate_config(raw)


# ---------------------------------------------------------------------------
# validate_config — wrong types
# ---------------------------------------------------------------------------

class TestValidateConfigWrongTypes:
    def test_endpoint_not_string(self):
        import copy

        raw = copy.deepcopy(VALID_RAW)
        raw["openstack"]["endpoint"] = 12345
        with pytest.raises(ConfigError, match="must be str"):
            validate_config(raw)

    def test_module_order_not_list(self):
        import copy

        raw = copy.deepcopy(VALID_RAW)
        raw["modules"]["order"] = "not-a-list"
        with pytest.raises(ConfigError, match="must be list"):
            validate_config(raw)

    def test_timeout_not_int(self):
        import copy

        raw = copy.deepcopy(VALID_RAW)
        raw["session"]["timeout_minutes"] = "two hours"
        with pytest.raises(ConfigError, match="must be int"):
            validate_config(raw)

    def test_max_instances_not_int(self):
        import copy

        raw = copy.deepcopy(VALID_RAW)
        raw["session"]["resource_limits"]["max_instances"] = "three"
        with pytest.raises(ConfigError, match="must be int"):
            validate_config(raw)


# ---------------------------------------------------------------------------
# load_config — file-level errors
# ---------------------------------------------------------------------------

class TestLoadConfig:
    def test_missing_file_raises_config_error(self, tmp_path):
        with pytest.raises(ConfigError, match="not found"):
            load_config(str(tmp_path / "nonexistent.yaml"))

    def test_invalid_yaml_raises_config_error(self, tmp_path):
        path = _write_yaml(tmp_path, "{{invalid yaml: [")
        with pytest.raises(ConfigError, match="Invalid YAML"):
            load_config(path)

    def test_non_mapping_yaml_raises_config_error(self, tmp_path):
        path = _write_yaml(tmp_path, "- just\n- a\n- list\n")
        with pytest.raises(ConfigError, match="must contain a YAML mapping"):
            load_config(path)

    def test_valid_file_returns_lab_config(self, tmp_path):
        content = """\
        openstack:
          endpoint: "https://cloud.example.com:5000/v3"
          default_flavor: "m1.small"
          default_image: "ubuntu-22.04"
        modules:
          order:
            - first_steps
        session:
          timeout_minutes: 60
          resource_limits:
            max_instances: 1
            max_networks: 1
            max_volumes: 1
            max_security_groups: 1
        """
        path = _write_yaml(tmp_path, content)
        cfg = load_config(path)
        assert isinstance(cfg, LabConfig)
        assert cfg.openstack_endpoint == "https://cloud.example.com:5000/v3"
        assert cfg.session_timeout == 60
