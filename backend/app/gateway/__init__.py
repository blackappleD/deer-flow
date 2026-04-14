from .app import app, create_app
from .config import GatewayConfig, get_gateway_config

__all__ = ["app", "create_app", "GatewayConfig", "get_gateway_config"]

import asyncio
import sys
from pathlib import Path


def _ensure_repo_root_on_path() -> None:
    """Allow gateway startup to import repo-root custom modules like `workflow`."""
    repo_root = Path(__file__).resolve().parents[3]
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.append(repo_root_str)


_ensure_repo_root_on_path()

from workflow import stvb_agents as _stvb_agents  # noqa: F401
from workflow.orchestrator import stvb_workflow


@app.post("/stvb/run")
async def run_stvb(data: dict) -> dict:
    """Run the custom STVB workflow on top of the main DeerFlow gateway app."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None,
        stvb_workflow.invoke,
        {
            "query": data.get("query"),
            "data": data.get("data", {}),
            "step": data.get("step", "S"),
            "result": data.get("result", {}),
        },
    )
