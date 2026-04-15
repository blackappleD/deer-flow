"""Register AION/AEGIS/ARBI/M agents for yuanfa orchestration."""

from __future__ import annotations

from registry.agent_registry import FunctionAgent, register_agent


def _run_aion(state: dict) -> dict:
    severity = state.get("severity", "medium")
    case_id = state.get("case_id", "unknown-case")
    warning_level = {
        "low": "observe",
        "medium": "review",
        "high": "alert",
        "critical": "red-alert",
    }.get(severity, "review")
    return {
        "agent": "AION",
        "role_name": "灵哨",
        "stage": "AION_WARNING",
        "warning_level": warning_level,
        "risk_summary": f"AION detected {severity} risk for case {case_id}",
        "recommendation": "dispatch AEGIS for evidence collection",
    }


def _run_aegis(state: dict) -> dict:
    severity = state.get("severity", "medium")
    evidence_items = ["alert-trace", "event-log", "risk-snapshot"]
    if severity in {"high", "critical"}:
        evidence_items.append("forensics-package")
    return {
        "agent": "AEGIS",
        "role_name": "灵盾",
        "stage": "AEGIS_INVESTIGATION",
        "evidence_stage": "EVIDENCE_COLLECTION",
        "evidence_items": evidence_items,
        "finding": f"AEGIS collected {len(evidence_items)} evidence artifacts",
    }


def _run_arbi(state: dict) -> dict:
    severity = state.get("severity", "medium")
    outcome = "approve_remediation"
    if severity == "critical":
        outcome = "freeze_and_execute_emergency_plan"
    elif severity == "high":
        outcome = "temporary_restriction_and_remediation"

    requires_m_review = bool(state.get("emergency")) and bool(state.get("major"))
    return {
        "agent": "ARBI",
        "role_name": "灵治",
        "stage": "ARBI_ARBITRATION",
        "outcome": outcome,
        "reasoning": "ARBI completed arbitration based on AION warning and AEGIS evidence",
        "requires_m_review": requires_m_review,
    }


def _run_m(state: dict) -> dict:
    arbi_result = state.get("arbi_result", {})
    return {
        "decision_maker": "M",
        "mode": "centralized",
        "decision": "activate_emergency_command",
        "source": "M_EXECUTION",
        "based_on": arbi_result.get("outcome", "arbitration_result"),
    }


register_agent("aion_agent", FunctionAgent(_run_aion))
register_agent("aegis_agent", FunctionAgent(_run_aegis))
register_agent("arbi_agent", FunctionAgent(_run_arbi))
register_agent("m_agent", FunctionAgent(_run_m))
