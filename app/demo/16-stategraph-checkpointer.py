from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver # 内存检查点 checkpointer

from langchain_core.runnables import RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

# 表达状态：整个状态图的状态
class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]

def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}

# 构建状态图
workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

# 检查点管理器：
checkpointer = InMemorySaver()

# 配置
config: RunnableConfig = {
    "configurable": { "thread_id": "1" }
}

# 编译
graph = workflow.compile(checkpointer=checkpointer)

# 调用
results = graph.invoke({"foo": ""}, config)
print(results)
# {'foo': 'b', 'bar': ['a', 'b']}

## 状态查看
print(graph.get_state(config))
# StateSnapshot(
#     values={'foo': 'b', 'bar': ['a', 'b']}, 
#     next=(), 
#     config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f1af5ec-cfad-66a6-8002-ee7140b6df85'}}, 
#     metadata={'source': 'loop', 'step': 2, 'parents': {}}, 
#     created_at='2026-09-13T10:35:12.597362+00:00', 
#     parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f1af5ec-cfac-692c-8001-9867e5b6dfbe'}}, 
#     tasks=(), 
#     interrupts=()
# )

for checkpoint_tuple in checkpointer.list(config):
    print()
    print(checkpoint_tuple)
# CheckpointTuple(
#     config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f1af5f2-ac18-6a5a-8002-7fd761ba1e99'}}, 
#     checkpoint={
#         'v': 4, 
#         'ts': '2026-09-13T10:37:49.927684+00:00', 
#         'id': '1f1af5f2-ac18-6a5a-8002-7fd761ba1e99', 
#         'channel_versions': {
#             '__start__': '00000000000000000000000000000002.0.030622590859470944', 
#             'foo': '00000000000000000000000000000004.0.6429928770910645', 
#             'branch:to:node_a': '00000000000000000000000000000003.0.5195915875862472', 
#             'bar': '00000000000000000000000000000004.0.6429928770910645', 
#             'branch:to:node_b': '00000000000000000000000000000004.0.6429928770910645'
#         }, 
#         'versions_seen': {
#             '__input__': {}, 
#             '__start__': {
#                 '__start__': '00000000000000000000000000000001.0.0731044351276221'
#             }, 
#             'node_a': {
#                 'branch:to:node_a': '00000000000000000000000000000002.0.030622590859470944'
#             }, 
#             'node_b': {
#                 'branch:to:node_b': '00000000000000000000000000000003.0.5195915875862472'
#             }
#         }, 
#         'updated_channels': ['bar', 'foo'], 
#         'channel_values': {'foo': 'b', 'bar': ['a', 'b']}}, 
#         metadata={'source': 'loop', 'step': 2, 'parents': {}}, 
#         parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f1af5f2-ac17-6c68-8001-9f1826e1a225'}}, 
#         pending_writes=[]
# )