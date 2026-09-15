from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph,END
from typing import TypedDict,Annotated
import operator
from langchain_core.messages import AnyMessage, AIMessage, ToolMessage, HumanMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
import asyncio
from langgraph.checkpoint.memory import InMemorySaver

_=load_dotenv()

tool = TavilSearchReasults(max_results=2)
class AgentState(TypeDict):
  messages:Annotated[list[Anymessages],operator.add]

class Agent:
  def __init__(self,model,tools,system="",checkpointer=checkpointer):
    self.system = system
    graph = StateGraph(AgentState)
    graph.add_node("llm",self.call_openai)
    graph.add_node("action",self.take_action)
    graph.add_conditional_edges("llm",exists_acition,{True:"take_action,False:END}
    graph.set_entry_point("llm")

    self.model = model.bind_tools(tools)
    self.graph = graph.compile(checkpointer=checkpointer)
    self.tool = {t.name: t for t in tools}

  def call_openai(self,state:AgentState):
    messages = state['messages']
    if self.system:
      messages = [SystemMessages(content=self.system }) + messages
      message = self.model.invoke(messages)
      return {'messages':[message]}

  def exists_action(self,state:AgentState):
    result = state['messages'][-1]
    return len(results.tool_calls)>0
    
  def take_action(self,state:AgentState):
     tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling:{t}")
            result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'],name=t['name'],content=str(result)))
            print("Back to the model!")
        return{'messages':results}

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
abot = Agent(model,[tool],system=prompt,checkpointer=memory)

# ============================================================
# 示例1：多轮对话（通过相同 thread_id 保持上下文）
# ============================================================

# messages = [HumanMessages(content=""上海天气怎么样？")
# thread = {"configurable"={"thread_id":1}}
# for event in abot.graph.stream({"messages":message},thread)
#   for v in event values:
#   print(v['messages'])

# messages = [HumanMessage(content="那么，北京呢")]
# thread = {"configurable":{"thread_id":"1"}}
# for event in abot.graph.stream({"messages":messages},thread):
#     for v in event.values():
#         print(v['messages'])

# messages = [HumanMessage(content="哪个城市的天气更暖和")]
# thread = {"configurable":{"thread_id":"1"}}
# for event in abot.graph.stream({"messages":messages},thread):
#     for v in event.values():
#         print(v['messages'])


# ============================================================
# 示例2：流式输出（逐字打印模型响应）
# ============================================================

messages = [HumanMessages(content="上海天气怎么样？")
thread = {"configurable":{thread_id":4}}
async def stream_demo():
  async for event in abot.graph.stream({'messages":messages},thread):
      kind = event['event']
      if kind == "on_chat_model_stream":
      content = event['data']['chunk'].content
      if content:
      print(content,end="|")

asynico.run(stream_demo())
      
      



                          
                                        
  
