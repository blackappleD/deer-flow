from __future__ import annotations

try:
    from langgraph.graph import END, StateGraph
except ModuleNotFoundError:  # pragma: no cover - fallback for local envs without langgraph
    END = "__end__"
    StateGraph = None

from tools.invoke_sub_agent import invoke_sub_agent
from workflow import stvb_agents  # noqa: F401  # ensure agent registration side effects


def yuanfa_workflow_node(state: dict) -> dict:
    step = state.get("step", "AION")
    timeline = list(state.get("timeline", []))

    if step == "AION":
        res = invoke_sub_agent("aion_agent", state)
        timeline.append(
            {
                "stage": "AION_WARNING",
                "actor": "AION",
                "detail": res["risk_summary"],
            }
        )
        state.update(aion_warning=res, timeline=timeline, step="AEGIS")

    elif step == "AEGIS":
        res = invoke_sub_agent("aegis_agent", state)
        timeline.extend(
            [
                {
                    "stage": "AEGIS_INVESTIGATION",
                    "actor": "AEGIS",
                    "detail": "investigation dispatched by yuanfa orchestrator",
                },
                {
                    "stage": "EVIDENCE_COLLECTION",
                    "actor": "AEGIS",
                    "detail": res["finding"],
                },
            ]
        )
        state.update(aegis_evidence=res, timeline=timeline, step="ARBI")

    elif step == "ARBI":
        res = invoke_sub_agent("arbi_agent", state)
        timeline.append(
            {
                "stage": "ARBI_ARBITRATION",
                "actor": "ARBI",
                "detail": res["outcome"],
            }
        )
        next_step = "M" if res.get("requires_m_review") else "FINAL"
        state.update(arbi_result=res, timeline=timeline, step=next_step)

    elif step == "M":
        res = invoke_sub_agent("m_agent", state)
        timeline.append(
            {
                "stage": "M_EXECUTION",
                "actor": "M",
                "detail": "centralized decision applied for emergency major case",
            }
        )
        state.update(final_decision=res, timeline=timeline, step="FINAL")

    elif step == "FINAL":
        final_decision = state.get("final_decision") or {
            "decision_maker": "ARBI",
            "mode": "federated",
            "decision": state["arbi_result"]["outcome"],
            "source": "ARBI_ARBITRATION",
            "based_on": "arbitration_result",
        }
        state["final_decision"] = final_decision
        state["poca_contribution"] = build_poca_contribution(state, final_decision)
        state["step"] = "END"

    return state


def build_poca_contribution(state: dict, final_decision: dict) -> dict:
    severity = state.get("severity", "medium")
    severity_bonus = {
        "low": 0,
        "medium": 5,
        "high": 10,
        "critical": 20,
    }.get(severity, 5)
    weights = {"AION": 0.25, "AEGIS": 0.4, "ARBI": 0.35}
    if final_decision["decision_maker"] == "ARBI":
        weights = {"AION": 0.2, "AEGIS": 0.45, "ARBI": 0.35}

    breakdown = []
    for agent_code, weight in weights.items():
        breakdown.append(
            {
                "agent": agent_code,
                "role_name": {
                    "AION": "灵哨",
                    "AEGIS": "灵盾",
                    "ARBI": "灵治",
                }[agent_code],
                "contribution_type": "governance",
                "weight": weight,
                "poca_points": round((100 + severity_bonus) * weight, 2),
            }
        )

    return {
        "case_id": state["case_id"],
        "distribution_mode": "shapley-inspired",
        "excluded_agents": ["M"],
        "total_poca_points": round(sum(item["poca_points"] for item in breakdown), 2),
        "breakdown": breakdown,
    }


def is_end(state: dict) -> bool:
    return state.get("step") == "END"


if StateGraph is not None:
    workflow = StateGraph(dict)
    workflow.add_node("yuanfa_flow", yuanfa_workflow_node)
    workflow.set_entry_point("yuanfa_flow")
    workflow.add_conditional_edges("yuanfa_flow", is_end, {True: END, False: "yuanfa_flow"})
    yuanfa_workflow = workflow.compile()
else:
    class _FallbackWorkflow:
        def invoke(self, state: dict) -> dict:
            current = dict(state)
            while not is_end(current):
                current = yuanfa_workflow_node(current)
            return current

    yuanfa_workflow = _FallbackWorkflow()
