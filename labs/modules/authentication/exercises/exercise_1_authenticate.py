# Authentication Module - Exercise 1: Authenticate

from __future__ import annotations

from labs.templates.exercise_template import Exercise


class AuthenticateExercise(Exercise):
    """Authenticate against Keystone and obtain a token."""

    @property
    def problem_statement(self) -> str:
        return "Authenticate against the Keystone identity service and obtain a token."

    @property
    def instructions(self) -> list[str]:
        return [
            "Use auth_manager to authenticate with your credentials.",
            "Retrieve and store the authentication token.",
        ]

    @property
    def expected_outcomes(self) -> list[dict]:
        return [
            {"type": "token", "name": "{student_id}-auth-token", "valid": True}
        ]

    def run(self, **kwargs) -> dict:
        auth = self.managers.get("auth_manager")
        if auth is None:
            return {"error": self._handle_openstack_error(
                "authenticate", "auth_manager not available"
            )}
        try:
            token = auth.authenticate(
                username=kwargs.get("username"),
                password=kwargs.get("password"),
            )
            return {"token": token}
        except Exception as exc:
            return {"error": self._handle_openstack_error("authenticate", exc)}
