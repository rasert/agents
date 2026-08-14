# 🤖 Data Science, Machine Learning & AI Agents

> Repositório dedicado ao armazenamento, estudo e desenvolvimento de projetos práticos nas áreas de **Data Science**, **Machine Learning Engineering** e **Agentes de IA autônomos**.

---

## 📌 Sobre o Repositório

Este repositório funciona como um portfólio prático e diário de aprendizado. Aqui são desenvolvidos e documentados projetos focados em:
- **Inteligência Artificial Agêntica (AI Agents)** com arquiteturas de memória, roteamento de estado e chamadas de ferramentas.
- **Machine Learning & Deep Learning**: Modelagem preditiva, classificação, regressão, processamento de linguagem natural (NLP) e visão computacional.
- **Engenharia de Dados & ML Ops**: Processamento de dados, pipelines e integração de modelos em produção.

---

## 🛠️ Tecnologias & Ferramentas

- **Linguagem Principal:** Python 3.12+
- **Frameworks de IA & Agentes:** LangGraph, LangChain, Ollama
- **Modelagem & Dados:** Pydantic, NumPy, Pandas, Scikit-Learn, PyTorch *(em expansão)*
- **Ambiente de Desenvolvimento:** Jupyter Notebook, `uv`, `pip`, Virtualenv

---

## 📂 Projetos no Repositório

| Projeto | Descrição | Tecnologias Chave | Status |
| :--- | :--- | :--- | :---: |
| 🎯 [Task mAIstro](./Task%20mAIstro/) | Agente inteligente para gestão dinâmica de tarefas (*ToDo List*) com suporte a memória de longo prazo (perfil, tarefas e preferências) e ferramentas de atualização de estado. | LangGraph, LangChain Ollama, Pydantic, Jupyter | 🟢 Concluído |

---

## 🔍 Detalhes dos Projetos

### 1. Task mAIstro
- **Local:** [`/Task mAIstro/task_mAIstro.ipynb`](./Task%20mAIstro/task_mAIstro.ipynb)
- **Objetivo:** Construir um agente conversacional capaz de manter e atualizar dinamicamente o perfil do usuário, lista de tarefas e preferências de manipulação através de um grafo de estados (`StateGraph`).
- **Principais Funcionalidades:**
  - Reducer customizado para operações de `add`, `update` e `delete` em listas de tarefas estruturadas via Pydantic.
  - Roteamento condicional de mensagens (`message_router`) baseado na chamada de ferramentas do LLM.
  - Execução local com LLMs abertos através do `ChatOllama`.

---

## 💻 Como Executar os Projetos Localmente

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/rasert/agents.git
   cd agents
   ```

2. **Criar e ativar um ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar as dependências:**
   ```bash
   # Utilizando uv (recomendado por velocidade):
   uv pip install langgraph langchain-ollama langchain-core pydantic ipykernel grandalf

   # Ou utilizando pip convencional:
   pip install langgraph langchain-ollama langchain-core pydantic ipykernel grandalf
   ```

4. **Executar o Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

---

## 👤 Autor

Desenvolvido por **Jackson** ([@rasert](https://github.com/rasert)).

---
*Repositório mantido em constante evolução.*
