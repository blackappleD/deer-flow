"""Minimal in-process registry for custom STVB agents."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class FunctionAgent:
    """Adapter that gives plain callables an `.invoke()` method."""

    def __init__(self, fn: Callable[[dict[str, Any]], dict[str, Any]]):
        self._fn = fn

    def invoke(self, state: dict[str, Any]) -> dict[str, Any]:
        return self._fn(state)


_AGENTS: dict[str, Any] = {}


def register_agent(name: str, agent: Any) -> None:
    _AGENTS[name] = agent


def get_agent(name: str) -> Any:
    try:
        return _AGENTS[name]
    except KeyError as exc:
        raise KeyError(f"Agent '{name}' is not registered") from exc

