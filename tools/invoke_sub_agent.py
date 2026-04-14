from deerflow.registry.agent_registry import get_agent

def invoke_sub_agent(agent_name: str, state: dict) -> dict:
    agent = get_agent(agent_name)
    return agent.invoke(state)
