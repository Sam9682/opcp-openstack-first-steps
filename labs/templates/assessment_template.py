# OpenStack First Steps Labs - Assessment Helpers

"""
Helper functions used by the Assessment Engine to compare expected vs actual
OpenStack resource outcomes.
"""

from __future__ import annotations


def outcomes_match(expected: list[dict], actual: list[dict]) -> tuple[bool, list[str]]:
    """Compare expected outcomes against actual resource states.

    Args:
        expected: List of dicts describing expected resources, each with at
            least ``type`` and ``name`` keys plus optional property checks.
        actual: List of dicts describing actual resources found in OpenStack.

    Returns:
        A ``(passed, mismatches)`` tuple where *passed* is ``True`` when
        every expected outcome has a matching actual entry, and *mismatches*
        lists human-readable descriptions of unmet outcomes.
    """
    mismatches: list[str] = []
    actual_by_key = {(r.get("type"), r.get("name")): r for r in actual}

    for exp in expected:
        key = (exp.get("type"), exp.get("name"))
        found = actual_by_key.get(key)

        if found is None:
            mismatches.append(
                f"Expected {exp.get('type')} '{exp.get('name')}' not found"
            )
            continue

        # Check additional properties beyond type/name.
        for prop, expected_val in exp.items():
            if prop in ("type", "name"):
                continue
            actual_val = found.get(prop)
            if actual_val != expected_val:
                mismatches.append(
                    f"{exp.get('type')} '{exp.get('name')}': "
                    f"expected {prop}={expected_val!r}, got {actual_val!r}"
                )

    passed = len(mismatches) == 0
    return passed, mismatches
