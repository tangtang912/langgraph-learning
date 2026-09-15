# 第 4 课：持久化与流式传输

## 功能说明

本课展示 LangGraph 的两个高级特性：

### 1. 持久化（Persistence）
- 使用 `InMemorySaver` 作为检查点（Checkpointer）
- 通过 `thread_id` 区分不同会话
- 相同 `thread_id` 的多次调用自动共享历史消息

### 2. 流式传输（Streaming）
- `stream()`：同步流式输出
- `astream_events()`：异步事件流，可获取每个 token

## 核心概念

| 概念 | 说明 |
| :--- | :--- |
| `InMemorySaver` | 内存检查点，保存每个会话的状态 |
| `thread_id` | 会话标识符，相同 ID 共享历史 |
| `checkpointer` | 编译图时传入，启用持久化 |
| `astream_events` | 异步事件流，逐 token 输出 |

## 多轮对话原理
第1轮：thread_id="1" → 保存消息 [Human, AI, ...]
↓
第2轮：thread_id="1" → 自动加载历史 + 新消息
↓
第3轮：thread_id="1" → 继续累加历史

## 文件结构
04_persistence_streaming/
├── main.py # 主程序
└── README.md # 本说明文档

## 运行

```bash
cd 04_persistence_streaming
python main.py
