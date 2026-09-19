# 第 5 课：人类在流程中（Human-in-the-loop）

## 功能说明

本课展示 LangGraph 最强特性之一：**人类可以在 Agent 执行过程中介入**，包括：

1. **中断执行**：在指定节点前暂停
2. **修改状态**：人工修改工具调用的参数
3. **继续执行**：从中断处继续运行
4. **时间旅行**：回放历史状态，从任意节点分叉
5. **插入消息**：模拟工具返回结果

## 核心知识点

| 知识点 | API | 说明 |
| :--- | :--- | :--- |
| **自定义 Reducer** | `reduce_messages` | 按 id 替换消息而非追加 |
| **中断点** | `interrupt_before=["action"]` | 工具执行前暂停 |
| **获取状态** | `graph.get_state(thread)` | 查看当前完整状态 |
| **修改状态** | `graph.update_state(...)` | 人工修改状态 |
| **历史回放** | `graph.get_state_history(thread)` | 获取所有历史状态 |
| **从历史分叉** | `to_replay.config` | 从某个历史节点继续执行 |
| **模拟节点** | `as_node="action"` | 假装某节点产生了更新 |

## 工作流程图
START
↓
llm（模型推理）
↓
【中断点】← 人类可修改工具调用参数
↓
action（执行工具）
↓
llm（继续推理）
↓
END


## 文件结构
05_human_in_loop/
├── main.py # 主程序
└── README.md # 本说明文档

## 运行

```bash
cd 05_human_in_loop
python main.py
