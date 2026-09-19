"""
LangGraph 第 5 课：人类在流程中（Human-in-the-loop）

核心知识点：
1. 自定义 Reducer：reduce_messages 实现消息替换（而非追加）
2. 中断机制：interrupt_before=["action"] 在执行工具前暂停
3. 人工干预：通过 update_state 修改状态后继续执行
4. 时间旅行：get_state_history 回放历史状态
5. 分支修改：从某个历史节点分叉，尝试不同路径
6. 插入消息：as_node="action" 模拟节点输出
"""
from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, ToolMessage, HumanMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from uuid import uuid4

_ = load_dotenv()
memory = InMemorySaver()

"""
说明：
之前的例子中，我们用 operator.add 或 "+" 作为 messages 的 reducer，
即永远追加新消息。

现在为了支持「替换已有消息」，我们自定义了 reducer 函数：
- 如果消息 id 相同，则替换
- 如果 id 不同，则追加
"""


def reduce_messages(left: list[AnyMessage], right: list[AnyMessage]) -> list[AnyMessage]:
    """自定义消息 reducer：按 id 替换，否则追加"""
    # 为没有 id 的消息分配 id
    for message in right:
        if not message.id:
            message.id = str(uuid4())

    # 合并新消息到已有消息
    merged = left.copy()
    for message in right:
        for i, existing in enumerate(merged):
            # 如果 id 相同，则替换
            if existing.id == message.id:
                merged[i] = message
                break
        else:
            # 否则追加到末尾
            merged.append(message)
    return merged


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], reduce_messages]


tool = TavilySearchResults(max_results=2)


class Agent:
    def __init__(self, model, tools, checkpointer, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges("llm", self.exists_action, {True: "action", False: END})
        graph.set_entry_point("llm")
        graph.add_edge("action", "llm")

        # 关键：在 action 节点前中断，等待人工确认
        self.graph = graph.compile(
            checkpointer=checkpointer,
            interrupt_before=["action"]
        )
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
            print("Back to the model!")
        return {'messages': results}


prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""

model = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

abot = Agent(model, [tool], system=prompt, checkpointer=memory)

# ============================================================
# 基础人工干预流程（含注释掉的初始示例）
# ============================================================
# messages = [HumanMessage(content="上海天气怎么样")]
# thread = {"configurable": {"thread_id": "1"}}
# for event in abot.graph.stream({"messages": messages}, thread):
#     for v in event.values():
#         print(v)
#
# print(abot.graph.get_state(thread))
#
# for event in abot.graph.stream(None, thread):
#     for v in event.values():
#         print(v)
# print(abot.graph.get_state(thread))

# ============================================================
# 主示例：中断 → 修改参数 → 继续执行
# ============================================================
messages = [HumanMessage(content="杭州天气怎么样")]
thread = {"configurable": {"thread_id": "3"}}

# 第1步：执行到 action 前中断
for event in abot.graph.stream({"messages": messages}, thread):
    for v in event.values():
        print(v)
print(abot.graph.get_state(thread))

# 第2步：获取当前状态，修改工具调用参数
current_values = abot.graph.get_state(thread)

_id = current_values.values['messages'][-1].tool_calls[0]['id']
current_values.values['messages'][-1].tool_calls = [
    {'name': 'tavily_search_results_json',
     'args': {'query': '北京现在的天气'},
     'id': _id}
]
print(abot.graph.update_state(thread, current_values.values))
print(abot.graph.get_state(thread))

# 第3步：继续执行（传入 None 表示从中断处继续）
for event in abot.graph.stream(None, thread):
    for v in event.values():
        print(v)

# ============================================================
# 时间旅行：获取所有历史状态
# ============================================================
states = []
for state in abot.graph.get_state_history(thread):
    print(state)
    print('--')
    states.append(state)

# 找到某个在 action 前的历史状态
to_replay = None
for state in states:
    if state.next == ("action",):
        to_replay = state

# ============================================================
# 分支执行1：从历史节点分叉，修改查询为"北京天气"
# ============================================================
for event in abot.graph.stream(None, to_replay.config):
    for k, v in event.items():
        print(v)

_id = to_replay.values['messages'][-1].tool_calls[0]['id']
to_replay.values['messages'][-1].tool_calls = [
    {'name': 'tavily_search_results_json',
     'args': {'query': '北京现在的天气,accweather'},
     'id': _id}]
branch_state = abot.graph.update_state(to_replay.config, to_replay.values)

for event in abot.graph.stream(None, branch_state):
    for k, v in event.items():
        if k != "__end__":
            print(v)

# ============================================================
# 分支执行2：直接插入 ToolMessage，模拟工具返回结果
# ============================================================
_id = to_replay.values['messages'][-1].tool_calls[0]['id']

state_update = {"messages": [ToolMessage(
    tool_call_id=_id,
    name="tavily_search_results_json",
    content="37度"
)]}

# as_node="action" 表示这个更新来自 action 节点
branch_and_add = abot.graph.update_state(
    to_replay.config,
    state_update,
    as_node="action")

for event in abot.graph.stream(None, branch_and_add):
    for k, v in event.items():
        print(v)
