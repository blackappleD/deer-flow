"""Register the custom STVB stage agents."""

from __future__ import annotations

from registry.agent_registry import FunctionAgent, register_agent


def _run_s(state: dict) -> dict:
    query = state.get("query") or ""
    return {
        "stage": "S",
        "summary": f"Structured query: {query}".strip(),
        "query": query,
        "data": state.get("data", {}),
    }


def _run_t(state: dict) -> dict:
    previous = state.get("result", {})
    return {
        "stage": "T",
        "tasks": [
            "analyze user query",
            "validate intermediate result",
            "build final response",
        ],
        "previous": previous,
    }


def _run_v(state: dict) -> dict:
    query = (state.get("query") or "").strip()
    previous = state.get("result", {})
    passed = bool(query)
    return {
        "stage": "V",
        "pass": passed,
        "reason": "query is present" if passed else "query is empty",
        "previous": previous,
    }


def _run_b(state: dict) -> dict:
    query = state.get("query") or ""
    previous = state.get("result", {})
    return {
        "stage": "B",
        "final": {
            "message": f"STVB workflow completed for query: {query}".strip(),
            "query": query,
            "validation": previous,
            "data": state.get("data", {}),
        },
    }


register_agent("s_agent", FunctionAgent(_run_s))
register_agent("t_agent", FunctionAgent(_run_t))
register_agent("v_agent", FunctionAgent(_run_v))
register_agent("b_agent", FunctionAgent(_run_b))
