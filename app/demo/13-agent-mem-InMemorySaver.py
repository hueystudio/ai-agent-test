# langchain 1.x 语法
from langchain.agents import create_agent
from dotenv import load_dotenv
from pathlib import Path
from langgraph.checkpoint.memory import InMemorySaver

# 从项目根目录的 .env 加载环境变量（与当前工作目录无关）
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# 创建内存保存器
memory_saver = InMemorySaver()

agent = create_agent(
    model="deepseek:deepseek-chat",
    checkpointer=memory_saver
)

# print(agent)

config = {
    "configurable": {
        "thread_id": "1"
    }
}

# 第一轮对话
# 问
results = agent.invoke(
    {
        "messages": [
            { "role": "user", "content": "来一首宋词" }
        ]
    },
    config=config
)
# 答
messages = results["messages"]
print(f"历史小时：{len(messages)}条")
for message in messages:
    message.pretty_print()

# 第二轮对话
# 问
results = agent.invoke(
    {
        "messages": [
            { "role": "user", "content": "再来" }
        ]
    },
    config=config
)
# 答
messages = results["messages"]
print(f"历史小时：{len(messages)}条")
for message in messages:
    message.pretty_print()