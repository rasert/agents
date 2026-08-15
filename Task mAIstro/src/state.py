from typing import Annotated, Literal, TypedDict
from uuid import uuid4

from langgraph.graph import MessagesState
from pydantic import BaseModel, Field


class Task(BaseModel, extra="allow"):
    """Tarefa do usuário com suporte a campos adicionais dinâmicos."""

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Identificador único da tarefa.",
    )
    description: str = Field(description="Descrição da tarefa.")


class TaskUpdatePayload(BaseModel):
    op: Literal["add", "update", "delete"] = Field(
        description="Operação a ser realizada: 'add', 'update' ou 'delete'."
    )
    tasks: list[Task] = Field(description="Lista de tarefas objeto da operação.")


def reduce_tasks(
    current_tasks: list[Task], update: TaskUpdatePayload | list[TaskUpdatePayload]
) -> list[Task]:
    updates = [update] if isinstance(update, TaskUpdatePayload) else update
    new_tasks = list(current_tasks) if current_tasks else []

    for item in updates:
        op = getattr(item, "op", None)
        tasks_item = getattr(item, "tasks", [])

        if op == "delete" and not tasks_item:
            new_tasks = []
        elif op == "delete":
            delete_ids = {getattr(t, "id", None) for t in tasks_item}
            new_tasks = [t for t in new_tasks if t.id not in delete_ids]
        elif op in ("add", "update"):
            for task_data in tasks_item:
                if any(t.id == task_data.id for t in new_tasks):
                    new_tasks = [
                        t if t.id != task_data.id else task_data for t in new_tasks
                    ]
                else:
                    new_tasks.append(task_data)

    return new_tasks


class Profile(BaseModel):
    """Perfil do usuário com suporte a campos adicionais dinâmicos."""

    name: str | None = Field(default=None, description="Nome do usuário")
    info: dict[str, str] = Field(
        default_factory=dict,
        description="Dicionário com informações arbitrárias sobre o usuário.",
    )


class Preferences(BaseModel):
    """Preferências do usuário sobre como manipular a lista de tarefas. É dinâmico e contém pares de chave e valor."""

    info: dict[str, str] = Field(
        description="Dicionário com informações arbitrárias sobre as preferências do usuário sobre como manipular a lista de tarefas, onde as chaves são a categoria/tipo da preferência e os valores são os detalhes."
    )


class AgentState(MessagesState):
    profile: Profile
    preferences: Preferences
    tasks: Annotated[list[Task], reduce_tasks]


class UpdateMemory(TypedDict):
    update_type: Literal["profile", "preferences", "tasks"]
