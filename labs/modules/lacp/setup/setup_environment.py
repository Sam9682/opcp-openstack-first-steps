# LACP Module - Environment Setup

from __future__ import annotations

from labs.core import LabConfig
from labs.scripts.setup_lab import LabSetup


def setup(config: LabConfig, managers: dict, student_id: str) -> None:
    lab_setup = LabSetup(config, managers, student_id)
    lab_setup.setup_module("lacp")
