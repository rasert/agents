from src.state import reduce_tasks
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
from typing import Literal

from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langgraph.constants import END
from src.config import llm
from src.prompts import (
    PREFERENCE_MESSAGE_TEMPLATE,
    PROFILE_MESSAGE_TEMPLATE,
    SYSTEM_MESSAGE_TEMPLATE,
    TASK_MESSAGE_TEMPLATE,
)
from src.state import AgentState, Preferences, Profile, TaskUpdatePayload, UpdateMemory, Task


def task_mAIstro(state: AgentState, config: RunnableConfig, store: BaseStore) -> dict:
    loaded_data = load_data(state, config, store)
    
    user_profile = loaded_data["profile"]
    user_preferences = loaded_data["preferences"]
    task_list = loaded_data["tasks"]

    system_msg = SYSTEM_MESSAGE_TEMPLATE.format(
        user_profile=user_profile,
        task_list=task_list,
        user_preferences=user_preferences,
    )

    response = llm.bind_tools([UpdateMemory]).invoke(
        [SystemMessage(content=system_msg)] + state["messages"]
    )

    return { "messages": [response], **loaded_data }

def load_data(state: AgentState, config: RunnableConfig, store: BaseStore) -> dict:
    user_id = config.get("configurable", {}).get("user_id", "default_user")

    user_profile = state.get("profile")
    user_preferences = state.get("preferences")
    tasks = state.get("tasks")

    if not (user_profile or user_preferences or tasks):
        profile_item = store.get(namespace=("users", user_id), key="profile")
        user_profile = Profile(**profile_item.value) if profile_item else Profile()

        preferences_item = store.get(namespace=("users", user_id), key="preferences")
        user_preferences = Preferences(**preferences_item.value) if preferences_item else Preferences(info=dict())

        tasks_item = store.get(namespace=("users", user_id), key="tasks")
        tasks = [Task(**t) for t in tasks_item.value] if tasks_item else []

    return {
        "profile": user_profile,
        "preferences": user_preferences,
        "tasks": tasks,
    }

def message_router(
    state: AgentState,
) -> Literal["handle_profile", "handle_preferences", "handle_tasks", END]:
    last_message = state["messages"][-1]
    if len(last_message.tool_calls) == 0:
        return END

    update_type = last_message.tool_calls[0]["args"]["update_type"]

    match update_type:
        case "profile":
            return "handle_profile"
        case "preferences":
            return "handle_preferences"
        case "tasks":
            return "handle_tasks"
        case _:
            raise ValueError(f"Tipo de atualização desconhecido: {update_type}")


def handle_profile(state: AgentState, config: RunnableConfig, store: BaseStore) -> dict:
    user_id = config.get("configurable", {}).get("user_id", "default_user")
    user_profile = state.get("profile", Profile())
    profile_msg = PROFILE_MESSAGE_TEMPLATE.format(user_profile=user_profile)

    last_message = state["messages"][-1]
    tool_id = last_message.tool_calls[0]["id"]
    tool_message = ToolMessage(
        tool_call_id=tool_id, content=f"user:{user_id} Perfil atualizado com sucesso."
    )

    conversation_messages = [
        m
        for m in state["messages"][:-1]
        if not isinstance(m, ToolMessage)
        and not (isinstance(m, AIMessage) and m.tool_calls)
    ]

    updated_profile = llm.with_structured_output(Profile).invoke(
        [SystemMessage(content=profile_msg)] + conversation_messages
    )

    store.put(namespace=("users", user_id), key="profile", value=updated_profile.model_dump())

    return {"profile": updated_profile, "messages": [tool_message]}


def handle_preferences(state: AgentState, config: RunnableConfig, store: BaseStore) -> dict:
    user_id = config.get("configurable", {}).get("user_id", "default_user")
    user_preferences = state.get("preferences", Preferences(info=dict()))
    preference_msg = PREFERENCE_MESSAGE_TEMPLATE.format(
        user_preferences=user_preferences
    )

    last_message = state["messages"][-1]
    tool_id = last_message.tool_calls[0]["id"]
    tool_message = ToolMessage(
        tool_call_id=tool_id,
        content="Preferências do usuário atualizadas com sucesso.",
    )

    conversation_messages = [
        m
        for m in state["messages"][:-1]
        if not isinstance(m, ToolMessage)
        and not (isinstance(m, AIMessage) and m.tool_calls)
    ]

    updated_preferences = llm.with_structured_output(Preferences).invoke(
        [SystemMessage(content=preference_msg)] + conversation_messages
    )

    store.put(namespace=("users", user_id), key="preferences", value=updated_preferences.model_dump())

    return {"preferences": updated_preferences, "messages": [tool_message]}


def handle_tasks(state: AgentState, config: RunnableConfig, store: BaseStore) -> dict:
    user_id = config.get("configurable", {}).get("user_id", "default_user")
    current_tasks = state.get("tasks", list())
    task_msg = TASK_MESSAGE_TEMPLATE.format(
        user_preferences=state.get("preferences", Preferences(info=dict())),
        task_list=current_tasks,
    )

    last_message = state["messages"][-1]
    tool_id = last_message.tool_calls[0]["id"]
    tool_message = ToolMessage(
        tool_call_id=tool_id, content="Tarefa processada com sucesso."
    )

    conversation_messages = [
        m
        for m in state["messages"][:-1]
        if not isinstance(m, ToolMessage)
        and not (isinstance(m, AIMessage) and m.tool_calls)
    ]

    task_update_payload = llm.with_structured_output(schema=TaskUpdatePayload).invoke(
        [SystemMessage(content=task_msg)] + conversation_messages
    )

    updated_tasks = reduce_tasks(current_tasks, task_update_payload)
    store.put(
        namespace=("users", user_id),
        key="tasks",
        value=[t.model_dump() for t in updated_tasks]
    )

    return {"tasks": [task_update_payload], "messages": [tool_message]}
