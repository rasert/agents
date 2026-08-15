# 🤖 Data Science, Machine Learning & AI Agents

> Repositório dedicado ao armazenamento, estudo e desenvolvimento de projetos práticos nas áreas de **Data Science**, **Machine Learning Engineering** e **Agentes de IA autônomos**.

---

## 📌 Sobre o Repositório

Este repositório funciona como um portfólio prático e diário de aprendizado. Aqui são desenvolvidos e documentados projetos focados em:
- **Inteligência Artificial Agêntica (AI Agents)** com arquiteturas de memória, roteamento de estado e chamadas de ferramentas.
- **Machine Learning & Deep Learning**: Modelagem preditiva, classificação, regressão, processamento de linguagem natural (NLP) e visão computacional.
- **Engenharia de Dados & ML Ops**: Processamento de dados, pipelines e integração de modelos em produção.

---

## 🛠️ Tecnologias & Ferramentas Modernas (Rust-Powered DX)

O projeto utiliza um conjunto de ferramentas de última geração para alta performance e excelente **Developer Experience (DX)**:

- **Linguagem Principal:** Python 3.12+
- **Frameworks de IA & Agentes:** LangGraph, LangChain, Ollama, LangGraph Studio / Server
- **Validação de Dados:** **Pydantic v2** (com motor `pydantic-core` em Rust)
- **Gerenciador de Pacotes & Venv:** **`uv`** (Gerenciamento de dependências ultrarrápido em Rust)
- **Formatador & Linter:** **`Ruff`** (Linter e formatador PEP8 instantâneo em Rust)
- **Checagem de Tipos (Type Checking):** **`Pyrefly`** (Language Server estrito para verificação estática de tipos)

---

## 📂 Projetos no Repositório

| Projeto | Descrição | Tecnologias Chave | Status |
| :--- | :--- | :--- | :---: |
| 🎯 [Task mAIstro](./Task%20mAIstro/) | Agente inteligente para gestão dinâmica de tarefas (*ToDo List*) com suporte a memória de longo prazo (perfil, tarefas e preferências), interface visual via LangGraph Studio e arquitetura modular em Python. | LangGraph, LangChain Ollama, Pydantic, LangGraph Studio, Jupyter | 🟢 Concluído |

---

## 🔍 Detalhes dos Projetos

### 1. Task mAIstro
- **Local:** [`/Task mAIstro/`](./Task%20mAIstro/)
- **Objetivo:** Construir um agente conversacional capaz de manter e atualizar dinamicamente o perfil do usuário, lista de tarefas e preferências de manipulação através de um grafo de estados (`StateGraph`).
- **Principais Funcionalidades:**
  - Código modularizado em `src/` (`state.py`, `nodes.py`, `prompts.py`, `config.py`, `graph.py`).
  - Reducer customizado para operações de `add`, `update` e `delete` em listas de tarefas estruturadas via Pydantic.
  - Roteamento condicional de mensagens (`message_router`) baseado na chamada de ferramentas do LLM.
  - Execução interativa e visual via **LangGraph Studio** (`langgraph dev`) e testes síncronos via Jupyter Notebook.

---

## 💻 Como Executar os Projetos Localmente

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/rasert/agents.git
   cd agents
   ```

2. **Instalar dependências e ambiente virtual com `uv` (Recomendado):**
   ```bash
   uv sync
   ```

3. **Rodar o LangGraph Studio (Interface Visual Interativa):**
   ```bash
   cd "Task mAIstro"
   langgraph dev
   ```

4. **Ou executar via Jupyter Notebook:**
   ```bash
   source .venv/bin/activate
   jupyter notebook
   ```

---

## 👤 Autor

Desenvolvido por **Jackson** ([@rasert](https://github.com/rasert)).

---
*Repositório mantido em constante evolução.*
