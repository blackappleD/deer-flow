from workflow.orchestrator import stvb_workflow

lead_agent = {
    "invoke": lambda data: stvb_workflow.invoke({
        "query": data["query"],
        "data": data.get("data", {}),
        "step": "S",
        "result": {}
    })
}
