# 第 3 课：Agent 搜索工具（Tavily 原生用法）

## 功能说明

本课直接使用 **Tavily Python SDK** 进行搜索，不依赖 LangChain 封装。

## 核心知识点

| 知识点 | 说明 |
| :--- | :--- |
| `TavilyClient` | Tavily 的原生 Python 客户端 |
| `client.search()` | 执行搜索查询 |
| `include_answer=True` | 让 Tavily 返回 AI 生成的答案摘要 |
| `result["answer"]` | 提取答案字段 |

## 代码结构
03_agent_search_tool/
├── main.py # 主程序
└── README.md # 本说明文档

## 运行

```bash
cd 03_agent_search_tool
python main.py
