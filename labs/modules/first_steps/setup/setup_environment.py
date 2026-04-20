# First Steps Module - Environment Setup

"""
Provisions the baseline OpenStack resources needed for the first_steps
exercises. Delegates to LabSetup for idempotent resource creation.
"""

from __future__ import annotations

from labs.core import LabConfig
from labs.scripts.setup_lab import LabSetup


def setup(config: LabConfig, managers: dict, student_id: str) -> None:
    """Provision resources for the first_steps module."""
    lab_setup = LabSetup(config, managers, student_id)
    lab_setup.setup_module("first_steps")
