from workflow.orchestrator import yuanfa_workflow


def _build_workflow_input(data: dict) -> dict:
    return {
        "case_id": data.get("case_id", "case-local-001"),
        "title": data.get("title", "Untitled case"),
        "summary": data.get("query") or data.get("summary", ""),
        "severity": data.get("severity", "medium"),
        "emergency": bool(data.get("emergency", False)),
        "major": bool(data.get("major", False)),
        "requested_by": data.get("requested_by", "AION"),
        "query": data.get("query", ""),
        "data": data.get("data", {}),
        "timeline": [
            {
                "stage": "SUBMISSION",
                "actor": data.get("requested_by", "AION"),
                "detail": "case submitted to yuanfa orchestrator",
            }
        ],
        "step": "AION",
    }


def _wrap_response(result: dict) -> dict:
    return {
        "code": 0,
        "message": "success",
        "data": {
            "case_id": result["case_id"],
            "title": result["title"],
            "summary": result["summary"],
            "severity": result["severity"],
            "requested_by": result["requested_by"],
            "timeline": result["timeline"],
            "final_decision": result["final_decision"],
            "poca_contribution": result["poca_contribution"],
            "aion_warning": result["aion_warning"],
            "aegis_evidence": result["aegis_evidence"],
            "arbi_result": result["arbi_result"],
        },
    }


lead_agent = {
    "invoke": lambda data: _wrap_response(yuanfa_workflow.invoke(_build_workflow_input(data)))
}
