# Solution: Exercise 2 - Token Management

from __future__ import annotations


def solve(managers: dict, **kwargs) -> dict:
    auth = managers["auth_manager"]
    tokens = auth.list_tokens()
    validation = auth.validate_token(kwargs.get("token"))
    auth.revoke_token(kwargs.get("token"))
    return {"tokens": tokens, "validation": validation, "revoked": True}
