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

## 执行流程
START
↓
hello 节点 → 返回 {"text": "你好"}
↓
world 节点 → 返回 {"text": "你好,世界！"}
↓
END
## 运行

```bash
cd 01_hello_langgraph
python main.py
