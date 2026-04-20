# Authentication Module - Exercise 2: Token Management

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class TokenManagementExercise(Exercise):
    """List, validate, and revoke authentication tokens."""

    @property
    def problem_statement(self) -> str:
        return "Manage authentication tokens: list, validate, and revoke."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use auth_manager to list current tokens.",
            "Validate an existing token.",
            "Revoke a token you no longer need.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "token_action", "name": "list_tokens", "performed": True},
            {"type": "token_action", "name": "validate_token", "performed": True},
            {"type": "token_action", "name": "revoke_token", "performed": True},
        ]

    def run(self, **kwargs) -> dict:
        auth = self.managers.get("auth_manager")
        if auth is None:
            return {"error": self._handle_openstack_error(
                "token management", "auth_manager not available"
            )}
        results: dict = {}
        try:
            results["tokens"] = auth.list_tokens()
            results["validation"] = auth.validate_token(kwargs.get("token"))
            auth.revoke_token(kwargs.get("token"))
            results["revoked"] = True
        except Exception as exc:
            return {"error": self._handle_openstack_error("token management", exc)}
        return results
