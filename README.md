# 🦜 LangGraph 学习笔记

> 从零开始学习 LangGraph —— 构建可控、可扩展的 Agent 应用

本仓库采用 **Monorepo（单一仓库）** 结构，每个文件夹对应一个课时，互不干扰，方便随时回顾和复用。

---

## 📂 课程目录

| 课时 | 文件夹 | 内容 | 状态 |
| :---: | :--- | :--- | :---: |
| 01 | [01_hello_langgraph](./01_hello_langgraph) | 从零开始打造一个 Agent | ✅ 已完成 |
| 02 | 02_langgraph_components | LangGraph 组件 | 📅 待学习 |
| 03 | 03_agent_search_tool | Agent 搜索工具 | 📅 待学习 |
| 04 | 04_persistence_streaming | 持久化与流式传输 | 📅 待学习 |
| 05 | 05_human_in_loop | 人类在流程中 | 📅 待学习 |
| 06 | 06_paper_writer | 论文写手 | 📅 待学习 |
| 07 | 07_langchain_resources | LangChain 资源 | 📅 待学习 |

---

## 📂 项目结构
anggraph-learning/
├── README.md
├── .gitignore
├── LICENSE
├── requirements.txt
├── 01_hello_langgraph/ # ✅ 已完成
│ ├── main.py # 第一个 LangGraph 程序
│ └── README.md
├── 02_xxx/ # 📅 待学习
└── ...

text

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/langgraph-learning.git
cd langgraph-learning
2. 安装依赖

bash
pip install -r requirements.txt
3. 运行示例

bash
cd 01_hello_langgraph
python main.py
📄 许可证

MIT License

Happy Coding! 🦜

text

4. 提交信息写 `docs: 添加项目README`。


### 📄 第三步：创建 `.gitignore`

1. 点击 **"Add file"** → **"Create new file"**。
2. 文件名输入：`.gitignore`
3. 粘贴内容：

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
.coverage
htmlcov/
*.cover

# 环境变量
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# 生成的图片
*.png
*.jpg

# Distribution
dist/
build/
*.egg-info/
*.egg
提交信息写 chore: 添加gitignore。
📄 第四步：创建 LICENSE

点击 "Add file" → "Create new file"。
文件名输入：LICENSE
粘贴 MIT 协议内容（替换年份和名字）。
提交信息写 chore: 添加MIT许可证。
📄 第五步：创建 requirements.txt

点击 "Add file" → "Create new file"。
文件名输入：requirements.txt
粘贴内容：
txt
langgraph>=0.2.0
langchain-core>=0.3.0
提交信息写 chore: 添加依赖清单。
📄 第六步：创建第 1 课 main.py

点击 "Add file" → "Create new file"。
文件名输入：01_hello_langgraph/main.py
粘贴你的代码（修正了 draw_mermaid_png 的写法）：
python
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
提交信息写 feat: 添加第1课 从零开始打造Agent。
📄 第七步：创建第 1 课的 README.md

点击 "Add file" → "Create new file"。
文件名输入：01_hello_langgraph/README.md
粘贴内容：
markdown
# 第 1 课：从零开始打造一个 Agent

## 核心概念

| 概念 | 说明 | 类比 |
| :--- | :--- | :--- |
| **State（状态）** | 所有节点共享的数据容器 | 团队的"共享便签本" |
| **Node（节点）** | 执行具体任务的函数 | 流水线上的工人 |
| **Edge（边）** | 节点之间的连接 | 流水线上的传送带 |
| **Graph（图）** | 节点和边的编排 | 整条流水线 |

## 代码结构
01_hello_langgraph/
├── main.py # 主程序
└── README.md # 本说明文档

text

## 执行流程
START
↓
hello 节点 → 返回 {"text": "你好"}
↓
world 节点 → 返回 {"text": "你好,世界！"}
↓
END

text

## 运行

```bash
cd 01_hello_langgraph
python main.py
预期输出

text
{'text': '你好,世界！'}
流程图

运行程序后会自动生成 langgraph_graph.png，可视化展示节点和边的连接关系。

关键点

节点函数必须返回字典，用于更新 State
State 是只读+合并：每个节点读取当前 State，返回的字典会合并进去
START 和 END 是 LangGraph 内置的特殊节点
text

4. 提交信息写 `docs: 添加第1课README`。


### ✅ 最终仓库结构
langgraph-learning/
├── README.md
├── .gitignore
├── LICENSE
├── requirements.txt
├── 01_hello_langgraph/
│ ├── main.py
│ └── README.md
└── 02_xxx/ # 📅 待学习

text


### 🚀 运行测试

```bash
cd langgraph-learning/01_hello_langgraph
python main.py
预期输出：

text
{'text': '你好,世界！'}
✅ 流程图已保存为 langgraph_graph.png
📌 关于 draw_mermaid_png 的说明

如果生成流程图时报错，可能是缺少 Graphviz：

macOS：

bash
brew install graphviz
Ubuntu/Debian：

bash
sudo apt-get install graphviz
Windows：下载安装 Graphviz

📌 核心知识点总结

概念	代码	作用
定义状态	class State(TypedDict)	声明图的数据结构
创建图	StateGraph(State)	初始化图构建器
添加节点	add_node("name", func)	注册执行函数
添加边	add_edge("from", "to")	定义执行顺序
编译图	compile()	生成可执行的图
运行图	invoke({"text": ""})	执行并返回结果
🚀 下一步（第 2 课）

第 2 课的内容是 LangGraph 组件。准备好了随时发我代码！🚀
from dotenv import load_dotenv,find_dotenv
from langgraph.graph import StateGraph,END
from typing import TypedDict,Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
import os

_ = load_dotenv(find_dotenv())

tool = TavilySearchResults(max_results =2 )
print(type(tool))
print(tool.name)

class AgentState(TypedDict):
    messages:Annotated[list[AnyMessage],operator.add]
class Agent:

    def __init__(self,model,tools,system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm",self.call_openai)
        graph.add_node("action",self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True:"action",False:END}
        )
        graph.add_edge("action","llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools ={t.name:t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self,state:AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls)>0

    def call_openai(self,state:AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        messages = self.model.invoke(messages)
        return {'messages':[messages]}

    def take_action(self,state:AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling:{t}")
            result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'],name=t['name'],content=str(result)))
            print("Back to the model!")

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


# messages = [HumanMessage(content="上海天气怎么样？")]
# result = abot.graph.invoke({"messages":messages})
# re = result['messages'][-1].content
# print(re)

# messages = [HumanMessage(content="上海和北京的天气怎么样？")]
# result = abot.graph.invoke({"messages":messages})
# re = result['messages'][-1].content
# print(re)

query = "哪个国家获得了世界杯的冠军？中国2025年人均gdp为多少？"
messages = [HumanMessage(content=query)]
result = abot.graph.invoke({"messages":messages})
re = result['messages'][-1].content
print(re)
这是第二课的内容
好的，用户发来的是LangGraph学习的第二课代码，同时问"这是第二课的内容"。结合对话历史，用户一直在按课程目录学习LangGraph，之前已经建立了langgraph-learning仓库并录入了第一课。

我需要分析这段代码的内容，识别它对应课程目录中的哪一课。课程目录是：
从零开始打造一个Agent（已完成）
LangGraph组件
Agent搜索工具
持久化与流式传输
人类在流程中
论文写手
LangChain资源
这段代码确实包含了LangGraph的核心组件（StateGraph、节点、边、条件边），同时引入了工具调用（Tavily搜索）和Agent循环，符合"LangGraph组件"这一课的内容，所以应该作为第二课录入。

代码中有几个问题需要注意：
模型用的是DeepSeek，需要配置DEEPSEEK_API_KEY，而不是之前的DashScope
tavily_search工具需要TAVILY_API_KEY
需要安装tavily-python包
我需要帮用户：
创建02_langgraph_components文件夹
录入main.py
更新根目录README
创建该课的README.md
指导如何配置环境变量
由于用户用DeepSeek取代了OpenAI，这是合理的（国内用户更容易获取），但需要明确说明需要配置两个API Key。
收到！这是你的LangGraph 第 2 课——LangGraph 组件（含 Agent 搜索工具）。你的代码构建了一个支持工具调用的 ReAct Agent，并使用 Tavily 搜索引擎作为工具。

🔍 代码分析

课程对应：根据你的目录，"LangGraph组件"（第2课）和"Agent搜索工具"（第3课）在这段代码中都有涉及——代码既展示了 LangGraph 的核心组件，又集成了 Tavily 搜索工具。

模型选择：你用了 deepseek-chat（DeepSeek 模型），需要配置 DEEPSEEK_API_KEY。同时 Tavily 搜索需要 TAVILY_API_KEY。

导入路径：不需要修正（相对路径没问题），但需要确保安装 tavily-python。

✍️ 操作步骤（在仓库中录入练习 2）

第一步：创建 02_langgraph_components/main.py

进入你的仓库 langgraph-learning 主页。
点击 “Add file” → “Create new file”。
文件名输入：02_langgraph_components/main.py
粘贴你的代码（完全保持原样，只添加注释）：
python
"""
LangGraph 第 2 课：LangGraph 组件 + Agent 搜索工具

核心组件：
1. State（状态）：Annotated + operator.add 实现消息累加
2. 节点：llm（调用模型）、action（执行工具）
3. 条件边：根据是否有 tool_calls 决定下一步
4. 工具绑定：model.bind_tools(tools) 让模型知道有哪些工具可用
"""
from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
import os

_ = load_dotenv(find_dotenv())

# 创建 Tavily 搜索工具
tool = TavilySearchResults(max_results=2)
print(type(tool))
print(tool.name)


class AgentState(TypedDict):
    # Annotated + operator.add：新消息自动追加到列表中（而不是覆盖）
    messages: Annotated[list[AnyMessage], operator.add]


class Agent:
    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)

        # 添加节点
        graph.add_node("llm", self.call_openai)      # LLM 推理节点
        graph.add_node("action", self.take_action)   # 工具执行节点

        # 条件边：LLM 节点后判断是否调用工具
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )

        # 工具执行后回到 LLM（继续推理）
        graph.add_edge("action", "llm")

        # 设置入口
        graph.set_entry_point("llm")

        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        """判断最后一条消息是否包含 tool_calls"""
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        """LLM 推理节点"""
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        messages = self.model.invoke(messages)
        return {'messages': [messages]}

    def take_action(self, state: AgentState):
        """工具执行节点"""
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
            print("Back to the model!")
        return {'messages': results}


# 系统提示词
prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""

# 使用 DeepSeek 模型（兼容 OpenAI API）
model = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 创建 Agent
abot = Agent(model, [tool], system=prompt)

# 生成流程图
abot.graph.get_graph().draw_mermaid_png(output_file_path="abot图.png")

# 测试查询：两个独立问题，Agent 会调用多次搜索
query = "哪个国家获得了世界杯的冠军？中国2025年人均gdp为多少？"
messages = [HumanMessage(content=query)]
result = abot.graph.invoke({"messages": messages})
re = result['messages'][-1].content
print(re)
提交信息写 feat: 添加第2课 LangGraph组件与Agent搜索工具。
第二步：创建 requirements.txt（更新）

编辑根目录的 requirements.txt，补充依赖：
txt
langgraph>=0.2.0
langchain-core>=0.3.0
langchain-openai>=0.3.0
langchain-community>=0.3.0
tavily-python>=0.5.0
python-dotenv>=1.0.0
提交信息写 chore: 更新依赖清单，添加tavily和openai。
第三步：创建 .env.example

点击 “Add file” → “Create new file”。
文件名输入：.env.example
粘贴内容：
env
# DeepSeek API Key（兼容 OpenAI 接口）
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Tavily 搜索 API Key
TAVILY_API_KEY=your_tavily_api_key_here
提交信息写 chore: 添加环境变量模板。
第四步：创建该课的 README.md

点击 “Add file” → “Create new file”。
文件名输入：02_langgraph_components/README.md
粘贴内容：
markdown
# 第 2 课：LangGraph 组件 + Agent 搜索工具

## 核心概念

| 组件 | 说明 | 本课示例 |
| :--- | :--- | :--- |
| **State** | 状态管理 | `AgentState` + `Annotated` 累加消息 |
| **Node** | 执行节点 | `call_openai`、`take_action` |
| **Edge** | 固定边 | `action → llm`（工具执行后回到模型） |
| **Conditional Edge** | 条件边 | 判断是否调用工具 → 分支执行 |
| **Tool Binding** | 工具绑定 | `model.bind_tools(tools)` |
| **Entry Point** | 入口 | `set_entry_point("llm")` |

## 执行流程
START
↓
llm（调用模型，判断是否需要工具）
↓
存在 tool_calls？
├─ True → action（执行工具）→ llm（继续推理）
└─ False → END（输出最终答案）

text

## 环境变量

| 变量 | 说明 | 获取 |
| :--- | :--- | :--- |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | platform.deepseek.com |
| `TAVILY_API_KEY` | Tavily 搜索 API Key | app.tavily.com |

## 运行

```bash
cd 02_langgraph_components
python main.py
预期输出

text
<class 'tavily.TavilySearchResults'>
tavily_search_results_json
Calling: {'name': 'tavily_search_results_json', 'args': {'query': '世界杯冠军 2026'}, ...}
Back to the model!
Calling: {'name': 'tavily_search_results_json', 'args': {'query': '中国 2025 人均 GDP'}, ...}
Back to the model!
（最终答案）
与第1课的对比

对比项	第1课	第2课
State 类型	简单 TypedDict	Annotated + 累加器
边类型	固定边	固定边 + 条件边
节点数量	2 个	2 个（含循环）
工具调用	❌ 不支持	✅ 支持
循环执行	❌ 无	✅ 有（action → llm）
text

4. 提交信息写 `docs: 添加第2课README`。


#### 第五步：更新根目录 README（总导航）

1. 回到仓库根目录，点击 `README.md` 的 ✏️ 编辑。
2. 找到 **"课程目录"** 表格，更新为：

```markdown
| 课时 | 文件夹 | 内容 | 状态 |
| :---: | :--- | :--- | :---: |
| 01 | [01_hello_langgraph](./01_hello_langgraph) | 从零开始打造一个 Agent | ✅ 已完成 |
| 02 | [02_langgraph_components](./02_langgraph_components) | LangGraph 组件 + Agent 搜索工具 | ✅ 已完成 |
| 03 | 03_agent_search_tool | Agent 搜索工具（扩展） | 📅 待学习 |
| 04 | 04_persistence_streaming | 持久化与流式传输 | 📅 待学习 |
| 05 | 05_human_in_loop | 人类在流程中 | 📅 待学习 |
| 06 | 06_paper_writer | 论文写手 | 📅 待学习 |
| 07 | 07_langchain_resources | LangChain 资源 | 📅 待学习 |
更新 "项目结构" 部分：
text
├── 01_hello_langgraph/           # ✅ 已完成
├── 02_langgraph_components/      # ✅ 已完成
│   ├── main.py
│   └── README.md
├── 03_xxx/                       # 📅 待学习

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/langgraph-learning.git
cd langgraph-learning
