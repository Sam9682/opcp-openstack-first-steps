# Solution: Exercise 1 - Authenticate

from __future__ import annotations


def solve(managers: dict, **kwargs) -> dict:
    auth = managers["auth_manager"]
    token = auth.authenticate(
        username=kwargs.get("username"),
        password=kwargs.get("password"),
    )
    return {"token": token}
