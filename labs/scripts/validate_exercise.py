# OpenStack First Steps Labs - Exercise Validator CLI

"""
CLI entry point that loads config and credentials, then runs the
assessment engine for a given module/exercise.

Usage::

    python -m labs.scripts.validate_exercise <module_name> <exercise_id> <student_id>
"""

from __future__ import annotations

import sys


def main() -> None:
    if len(sys.argv) != 4:
        print(
            "Usage: python -m labs.scripts.validate_exercise "
            "<module_name> <exercise_id> <student_id>",
            file=sys.stderr,
        )
        sys.exit(1)

    module_name, exercise_id, student_id = sys.argv[1], sys.argv[2], sys.argv[3]

    from labs.core import ConfigError, CredentialError
    from labs.core.config_loader import load_config
    from labs.core.credential_handler import load_credentials
    from labs.core.progress import ProgressTracker
    from labs.core.assessment import AssessmentEngine

    try:
        config = load_config()
    except ConfigError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        credentials = load_credentials()
    except CredentialError as exc:
        print(f"Credential error: {exc}", file=sys.stderr)
        sys.exit(1)

    # In a full deployment the managers would be initialised from the
    # automation framework using the loaded credentials.  Here we provide
    # a placeholder dict — the real wiring happens in the Lab Runner.
    managers: dict = {}

    progress = ProgressTracker()
    engine = AssessmentEngine(managers, progress)
    result = engine.validate_exercise(module_name, exercise_id, student_id)

    print(result.feedback)
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
