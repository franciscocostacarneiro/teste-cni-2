import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_core.messages import AIMessage, ToolMessage

from agente_rag import agente_corporativo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Assistente Corporativo com IA", version="1.0.0")

# Interface web (frontend estático)
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(STATIC_DIR / "index.html")


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    tools_used: list[str]
    chart: dict | None = None


@app.post("/agent/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    try:
        result = await agente_corporativo.ainvoke(
            {"messages": [{"role": "user", "content": request.question}]}
        )
    except Exception as e:
        logger.exception("Erro ao invocar o agente")
        raise HTTPException(status_code=500, detail=str(e))

    messages = result.get("messages", [])

    # coleta os nomes de todas as tools chamadas durante o ciclo ReAct
    tools_used: list[str] = []
    # captura o artifact (spec do gráfico) caso a tool gerar_grafico tenha sido usada
    chart: dict | None = None
    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc["name"] not in tools_used:
                    tools_used.append(tc["name"])
        if isinstance(msg, ToolMessage):
            if msg.name == "gerar_grafico" and msg.artifact:
                chart = msg.artifact

    answer = messages[-1].content if messages else "Sem resposta."
    return QueryResponse(answer=answer, tools_used=tools_used, chart=chart)
