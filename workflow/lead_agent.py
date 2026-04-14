from deerflow.workflow.orchestrator import orchestrator

lead_agent = {
    "invoke": lambda data: orchestrator.invoke({
        "query": data["query"],
        "data": data.get("data", {}),
        "step": "S",
        "result": {}
    })
}