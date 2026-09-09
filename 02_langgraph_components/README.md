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
TART
↓
llm（调用模型，判断是否需要工具）
↓
存在 tool_calls？
├─ True → action（执行工具）→ llm（继续推理）
└─ False → END（输出最终答案）

## 环境变量

| 变量 | 说明 | 获取 |
| :--- | :--- | :--- |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | platform.deepseek.com |
| `TAVILY_API_KEY` | Tavily 搜索 API Key | app.tavily.com |

## 运行

```bash
cd 02_langgraph_components
python main.py
