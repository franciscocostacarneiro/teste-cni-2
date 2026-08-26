# Assistente Corporativo com IA

API de assistente corporativo que responde perguntas em linguagem natural sobre
indicadores de desempenho (produtividade e retrabalho), combinando um agente de
IA (LangChain) com **tool calling** e integração com LLM via **OpenRouter**.

---

## 🧠 O que a aplicação faz

O assistente recebe uma pergunta e decide, de forma autônoma, quais ferramentas
usar para respondê-la:

| Ferramenta | Função |
|---|---|
| `get_indicators` | Consulta os valores numéricos dos indicadores por mês |
| `search_documents` | Busca contexto explicativo nos documentos corporativos |

As respostas são produzidas por um LLM usando o padrão **ReAct** (raciocina →
chama ferramentas → responde).

---

## 🚀 Como executar

### 1. Pré-requisitos

- Python 3.10 ou superior
- Uma chave de API da [OpenRouter](https://openrouter.ai/keys)

### 2. Clonar e entrar na pasta

```bash
git clone https://github.com/franciscocostacarneiro/teste-cni-2.git
cd teste-cni-2
```

### 3. Criar e ativar o ambiente virtual (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> Em Linux/macOS: `python -m venv .venv && source .venv/bin/activate`

### 4. Instalar as dependências

```powershell
pip install -r requirements.txt
```

### 5. Configurar a chave da API

```powershell
Copy-Item .env.example .env
```

Abra o arquivo `.env` e preencha sua chave real:

```
OPENROUTER_API_KEY=sk-or-v1-...sua_chave
OPENROUTER_MODEL=openai/gpt-4o-mini
```

### 6. Iniciar a aplicação

```powershell
python -m uvicorn main:app --port 8050
```

### 7. Abrir a interface

Acesse no navegador: **http://127.0.0.1:8050/**

A página exibe as 6 perguntas do estudo de caso, clicáveis, além de um campo
para perguntas livres.

---

## 🔌 API (endpoint)

### `POST /agent/query`

**Entrada:**

```json
{
  "question": "Por que a produtividade caiu em fevereiro?"
}
```

**Saída:**

```json
{
  "answer": "A produtividade caiu em fevereiro...",
  "tools_used": ["get_indicators", "search_documents"]
}
```

`tools_used` lista as ferramentas que o agente acionou para responder.

Documentação interativa (Swagger) disponível em `/docs`.

---

## 🧪 Como testar

As 6 perguntas do PRD podem ser testadas diretamente na interface web. Para testar
via terminal (usando `curl` ou PowerShell):

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8050/agent/query" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"question":"Qual foi a produtividade em fevereiro?"}'
```

---

## 🏗️ Decisões técnicas

- **Framework:** FastAPI para a API + LangChain (`create_agent`) para o agente.
- **Como funciona o agente:** usa o padrão ReAct. A cada pergunta, o LLM decide
  chamar uma ou mais ferramentas, observa os resultados e então gera a resposta final.
- **Seleção de ferramentas:** o prompt de sistema instrui o agente a usar
  `get_indicators` para valores numéricos e `search_documents` para contexto/causas.
  A decisão é feita pelo próprio LLM via tool calling (não há roteamento fixo).
- **Integração com o LLM:** via OpenRouter (`langchain-openai` com `base_url`),
  o que permite trocar o modelo apenas alterando `OPENROUTER_MODEL` no `.env`.
- **Dados:** armazenados como estruturas Python em `tools.py` (indicadores) e em
  memória (documentos) — sem banco de dados, visando simplicidade.
- **Busca em documentos:** por palavras-chave (com stop words), suficiente para o
  corpus pequeno; sem necessidade de embeddings ou banco vetorial.
- **Modelo padrão:** `openai/gpt-4o-mini` (tool calling confiável e rápido).
  Modelos pequenos como `llama-3.1-8b` não executam tools corretamente.

---

## 📁 Estrutura do projeto

```
.
├── agente_rag.py      # Agente corporativo (LangChain + OpenRouter)
├── tools.py           # As duas ferramentas (@tool get_indicators, search_documents)
├── main.py            # API FastAPI + rota do frontend
├── static/index.html  # Interface web com as perguntas clicáveis
├── requirements.txt   # Dependências
├── .env.example       # Exemplo de variáveis de ambiente
├── langgraph.json     # Configuração do grafo do agente
└── PRD.md             # Enunciado da prova técnica
```

---

## ⚠️ Limitações e melhorias futuras

- **Busca simples por palavras-chave** — poderia ser trocada por embeddings + banco
  vetorial (RAG) para corpora maiores ou buscas semânticas.
- **Sem memória de conversa** — cada requisição é independente (stateless); poderia
  usar `checkpointer` para manter histórico por sessão.
- **Sem testes automatizados** — uma suíte `pytest` (unitários nas tools e de
  integração no endpoint) deveria ser adicionada.
- **Tolerância a erros** — tratar timeouts/rate-limits do OpenRouter com retry.
- **Observabilidade** — logging estruturado e métricas de latência por tool call.
