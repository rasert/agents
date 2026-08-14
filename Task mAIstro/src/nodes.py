from typing import Literal
from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langgraph.constants import END

from src.config import llm
from src.state import AgentState, Profile, Preferences, UpdateMemory, TaskUpdatePayload
from src.prompts import (
    SYSTEM_MESSAGE_TEMPLATE,
    PROFILE_MESSAGE_TEMPLATE,
    PREFERENCE_MESSAGE_TEMPLATE,
    TASK_MESSAGE_TEMPLATE,
)


def task_mAIstro(state: AgentState) -> dict:
    user_profile = state.get("profile", Profile())
    task_list = state.get("tasks", list())
    user_preferences = state.get("preferences", Preferences(info=dict()))

    system_msg = SYSTEM_MESSAGE_TEMPLATE.format(
        user_profile=user_profile,
        task_list=task_list,
        user_preferences=user_preferences,
    )

    response = (
        llm.bind_tools([UpdateMemory])
        .invoke([SystemMessage(content=system_msg)] + state["messages"])
    )

    return {"messages": [response]}


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


def handle_profile(state: AgentState) -> dict:
    user_profile = state.get("profile", Profile())
    profile_msg = PROFILE_MESSAGE_TEMPLATE.format(user_profile=user_profile)

    last_message = state["messages"][-1]
    tool_id = last_message.tool_calls[0]["id"]
    tool_message = ToolMessage(
        tool_call_id=tool_id, content="Perfil do usuário atualizado com sucesso."
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

    return {"profile": updated_profile, "messages": [tool_message]}


def handle_preferences(state: AgentState) -> dict:
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

    return {"preferences": updated_preferences, "messages": [tool_message]}


def handle_tasks(state: AgentState) -> dict:
    task_msg = TASK_MESSAGE_TEMPLATE.format(
        user_preferences=state.get("preferences", Preferences(info=dict())),
        task_list=state.get("tasks", list()),
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

    task_update_payload = llm.with_structured_output(
        schema=TaskUpdatePayload
    ).invoke([SystemMessage(content=task_msg)] + conversation_messages)

    return {"tasks": [task_update_payload], "messages": [tool_message]}
