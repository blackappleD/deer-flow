# 官方加载自定义 Agent（目录形式）
from deerflow.agent.factory import create_agent_from_dir

# 加载你自己生成的 4 个 Agent（目录路径）
s_agent = create_agent_from_dir("./agent/my_s_agent")
t_agent = create_agent_from_dir("./agent/my_t_agent")
v_agent = create_agent_from_dir("./agent/my_v_agent")
b_agent = create_agent_from_dir("./agent/my_b_agent")

# 注册到注册表
from agent.agent_registry import register_agent

register_agent("s_agent", s_agent)
register_agent("t_agent", t_agent)
register_agent("v_agent", v_agent)
register_agent("b_agent", b_agent)