from langgraph.graph import StateGraph
from langgraph.constants import START

from src.state import AgentState
from src.nodes import (
    task_mAIstro,
    handle_profile,
    handle_preferences,
    handle_tasks,
    message_router,
)

builder = StateGraph(AgentState)

builder.add_node("task_mAIstro", task_mAIstro)
builder.add_node("handle_profile", handle_profile)
builder.add_node("handle_preferences", handle_preferences)
builder.add_node("handle_tasks", handle_tasks)

builder.add_edge(START, "task_mAIstro")
builder.add_conditional_edges("task_mAIstro", message_router)
builder.add_edge("handle_profile", "task_mAIstro")
builder.add_edge("handle_preferences", "task_mAIstro")
builder.add_edge("handle_tasks", "task_mAIstro")
