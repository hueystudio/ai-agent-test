# langchain 1.x 语法
from langchain.agents import create_agent
from dotenv import load_dotenv
from pathlib import Path
from langgraph.checkpoint.postgres import PostgresSaver

# 从项目根目录的 .env 加载环境变量（与当前工作目录无关）
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

DB_URL = "postgresql://postgres:postgres@localhost:5432/postgres"

with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    # 获取所有 checkpoint
    checkpoints = checkpointer.list(
        {"configurable": {"thread_id": "1"}}
    )

    print(checkpoints)

    for checkpoint in checkpoints:
        messages = checkpoint[1]["channel_values"]["messages"]
        for message in messages:
            message.pretty_print()
        break