import os

# Os testes não chamam o LLM de verdade; a chave só precisa existir para o
# import de agente_rag não abortar.
os.environ.setdefault("OPENROUTER_API_KEY", "test-key")
