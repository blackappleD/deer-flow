from langgraph.graph import StateGraph, END
from deerflow.tools.invoke_sub_agent import invoke_sub_agent

def stvb_workflow_node(state: dict):
    """
    M 元阀 / 调度中枢
    动态决定调用 S → T → V → B
    支持：条件、回退、循环
    """
    step = state.get("step", "S")

    # ========== S ==========
    if step == "S":
        res = invoke_sub_agent("s_agent", state)
        state.update(result=res, step="T")

    # ========== T ==========
    elif step == "T":
        res = invoke_sub_agent("t_agent", state)
        state.update(result=res, step="V")

    # ========== V ==========
    elif step == "V":
        res = invoke_sub_agent("v_agent", state)
        state["result"] = res
        # 条件判断：通过 → B，不通过 → 退回 S
        state["step"] = "B" if res.get("pass") else "S"

    # ========== B ==========
    elif step == "B":
        res = invoke_sub_agent("b_agent", state)
        state.update(result=res, step="END")

    return state

# 流程结束判断
def is_end(state):
    return state["step"] == "END"

# ================== 构建工作流 ==================
workflow = StateGraph(dict)
workflow.add_node("stvb_flow", stvb_workflow_node)
workflow.set_entry_point("stvb_flow")

workflow.add_conditional_edges(
    "stvb_flow",
    is_end,
    {True: END, False: "stvb_flow"}
)

# 编译成可运行的调度器
stvb_workflow = workflow.compile()