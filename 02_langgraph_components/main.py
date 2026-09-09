from dotenv import find_dotenv,load_dotenv
from langgraph.graph import StateGraph,END
from typing import TypedDict,Annotated
import operator
from langchain_core.messages import AnyMessage,SystemMessage,HumanMessage,ToolMessage
import os
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph组件 import messages

_=load_dotenv(find_dotenv())

tool = TavilySearchResults(max_results=2)
print(tool.name)
print(type(tool))

class AgentState(TypedDict):
    messages:Annotated[list[AnyMessage],operator.add]
class Agent:

    def __init__(self,model,tools,system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm",self.call_openai)
        graph.add_node("action",)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
        {True:"action",False:END},
        )
        graph.add_edge("action","llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.model = model.bind_tools(tools)
        self.tools = {t.name :t for t in tools}

    def exists_action(self,state:AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls)>0

    def call_openai(self,State:AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content= self.system),+messages]
            messages = self.model.invoke(messages)
            return {'messages':[messages]}

    def take_action(self,State:AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling:{t}")
            result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'],name=t['name'],content=str(result)))
            print("Back to model!")

        return {'messages':results}

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

abot = Agent(model,[tool],system=prompt)
abot.graph.get_graph().draw_mermaid_png(output_file_path="abot图.png")

messages = HumanMessage(content="上海今天天气怎么样？")
results = abot.graph.invoke({"messages":messages})
re = result['messages'][-1].content
print(re)







