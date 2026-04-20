# OpenStack First Steps Labs - Validation Utilities

"""
CIDR and security-group rule validators used by networking and
security_groups exercises.
"""

from __future__ import annotations


def validate_cidr(cidr_string: str) -> tuple[bool, str]:
    """Validate a CIDR notation string.

    Args:
        cidr_string: e.g. ``"10.0.0.0/24"``.

    Returns:
        ``(True, "")`` on success, ``(False, reason)`` on failure.
    """
    if "/" not in cidr_string:
        return False, f"Invalid CIDR '{cidr_string}': missing '/' separator"

    ip_part, prefix_part = cidr_string.rsplit("/", 1)

    # Validate prefix length.
    try:
        prefix = int(prefix_part)
    except ValueError:
        return False, f"Invalid CIDR '{cidr_string}': prefix '{prefix_part}' is not numeric"

    if prefix < 0 or prefix > 32:
        return False, f"Invalid CIDR '{cidr_string}': prefix {prefix} out of range 0-32"

    # Validate IP octets.
    octets = ip_part.split(".")
    if len(octets) != 4:
        return False, f"Invalid CIDR '{cidr_string}': expected 4 octets, got {len(octets)}"

    for i, octet in enumerate(octets):
        try:
            val = int(octet)
        except ValueError:
            return False, f"Invalid CIDR '{cidr_string}': octet {i+1} '{octet}' is not numeric"
        if val < 0 or val > 255:
            return False, f"Invalid CIDR '{cidr_string}': octet {i+1} value {val} out of range 0-255"

    return True, ""


_VALID_PROTOCOLS = {"tcp", "udp", "icmp"}


def validate_sg_rule(
    protocol: str, port_range_min: int, port_range_max: int
) -> tuple[bool, str]:
    """Validate a security group rule.

    Args:
        protocol: ``"tcp"``, ``"udp"``, or ``"icmp"``.
        port_range_min: Start of port range (1-65535).
        port_range_max: End of port range (1-65535).

    Returns:
        ``(True, "")`` on success, ``(False, reason)`` on failure.
    """
    if protocol.lower() not in _VALID_PROTOCOLS:
        return False, f"Unknown protocol '{protocol}'. Valid: {', '.join(sorted(_VALID_PROTOCOLS))}"

    # ICMP doesn't use port ranges in the traditional sense.
    if protocol.lower() == "icmp":
        return True, ""

    if not (1 <= port_range_min <= 65535):
        return False, f"port_range_min {port_range_min} outside valid range 1-65535"

    if not (1 <= port_range_max <= 65535):
        return False, f"port_range_max {port_range_max} outside valid range 1-65535"

    if port_range_min > port_range_max:
        return False, f"port_range_min ({port_range_min}) > port_range_max ({port_range_max})"

    return True, ""
