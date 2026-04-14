from .app import app, create_app
from .config import GatewayConfig, get_gateway_config

# 注册 STVB Agent
from workflow  import stvb_agents

# 加载 Lead Agent
from workflow.lead_agent import lead_agent

__all__ = ["app", "create_app", "GatewayConfig", "get_gateway_config"]

from fastapi import FastAPI
import asyncio
from workflow.orchestrator import stvb_workflow

app = FastAPI()

@app.post("/stvb/run")
async def run_stvb(data: dict):
    # 同步运行 workflow（deer-flow 内部大多是同步）
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        stvb_workflow.invoke,
        {
            "query": data.get("query"),
            "data": data.get("data", {}),
            "step": "S",
            "result": {}
        }
    )
    return result