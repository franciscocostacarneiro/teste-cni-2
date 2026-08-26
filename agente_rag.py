import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from tools import get_indicators, search_documents

load_dotenv()

_SYSTEM_PROMPT = """
Você é um assistente corporativo especializado em análise de indicadores de desempenho.

Você possui duas ferramentas:
- get_indicators: retorna valores numéricos dos indicadores (Produtividade, Retrabalho) por mês.
- search_documents: busca contexto explicativo nos documentos corporativos da empresa.

Regras obrigatórias:
- SEMPRE use as ferramentas antes de formular a resposta final.
- Use get_indicators quando a pergunta envolver números, valores ou evolução de indicadores.
- Use search_documents quando a pergunta envolver causas, explicações ou contexto.
- Combine as duas ferramentas quando necessário.
- Responda sempre em português, de forma clara e objetiva.
"""

# OpenRouter é compatível com o protocolo OpenAI; basta apontar base_url
model = ChatOpenAI(
    model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

agente_corporativo = create_agent(
    model=model,
    tools=[get_indicators, search_documents],
    system_prompt=_SYSTEM_PROMPT,
)
