# langchain 1.x 语法
from langchain.agents import create_agent
from dotenv import load_dotenv
from pathlib import Path

# 从项目根目录的 .env 加载环境变量（与当前工作目录无关）
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

agent = create_agent(
    model="deepseek:deepseek-chat"
)

# print(agent)

# 第一轮对话
# 问
results = agent.invoke({
    "messages": [
        { "role": "user", "content": "来一首宋词" }
    ]
})
# 答
messages = results["messages"]
print(f"历史小时：{len(messages)}条")
for message in messages:
    message.pretty_print()

# 手动保存历史对话记录
history_messages = messages

# 第二轮对话
# 问
message = { "role": "user", "content": "再来" }
history_messages.append(message)
results = agent.invoke({
    "messages": history_messages
})
# 答
messages = results["messages"]
print(f"历史小时：{len(messages)}条")
for message in messages:
    message.pretty_print()