"""
LangGraph 第 1 课：从零开始打造一个 Agent

核心概念：
- State（状态）：图的共享"便签本"，所有节点共享
- Node（节点）：普通函数，接收 state 并返回更新
- Edge（边）：连接节点，定义执行流向
- Graph（图）：编排节点和边的执行流程
"""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ① 状态：图的共享便签本
class State(TypedDict):
    text: str


# ② 两个节点：就是两个普通函数
def node_hello(state):
    return {"text": "你好"}


def node_world(state):
    return {"text": state["text"] + ",世界！"}


# ③ 建图：加节点、加边
builder = StateGraph(State)
builder.add_node("hello", node_hello)
builder.add_node("world", node_world)
builder.add_edge(START, "hello")
builder.add_edge("hello", "world")
builder.add_edge("world", END)

# ④ 编译成机器，运行
graph = builder.compile()
result = graph.invoke({"text": ""})
print(result)

# 生成流程图（需要安装 graphviz 和 pydot）
try:
    graph.get_graph().draw_mermaid_png(output_file_path="langgraph_graph.png")
    print("\n✅ 流程图已保存为 langgraph_graph.png")
except Exception as e:
    print(f"\n⚠️ 生成流程图失败（可能需要安装 graphviz）: {e}")
