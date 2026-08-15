import os

from langchain_ollama import ChatOllama

ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

llm = ChatOllama(model="gemma4-ctx16k", temperature=0, base_url=ollama_base_url)
