# =============================================================================
# chart_tool.py — Ferramenta de geração de gráficos para o agente corporativo
# =============================================================================
# Adaptada para os indicadores do projeto (que vivem em tools.py, em memória).
# Originalmente a ferramenta re-executava uma query SQL; aqui ela lê os dados
# estruturados (_INDICATORS) e devolve um spec JSON completo (config + dados)
# como artifact. O main.py captura o artifact e o devolve ao frontend, que
# renderiza o gráfico.
# =============================================================================
from __future__ import annotations

from typing import List, Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from tools import _INDICATORS


# ---------------------------------------------------------------------------
# Schemas Pydantic — definem os argumentos que o LLM preenche
# ---------------------------------------------------------------------------

class SeriesDefinition(BaseModel):
    yField: str = Field(description="Nome do campo do eixo Y desta série")
    label: str = Field(description="Rótulo da série para a legenda")
    color: Optional[str] = Field(
        default=None, description='Cor da linha/barra (ex: "#38bdf8")'
    )


class ChartInput(BaseModel):
    title: str = Field(description="Título do gráfico em português")
    chart_type: str = Field(
        default="line",
        description=(
            "Tipo de gráfico: 'line' (evolução temporal) ou 'bar' (comparação). "
            "Para os indicadores do projeto, use 'line' quando o eixo X for 'mes' "
            "e quiser mostrar a evolução; use 'bar' para comparar valores."
        ),
    )
    xField: str = Field(
        description="Campo do eixo X. Para os indicadores, use 'mes'."
    )
    xTitle: Optional[str] = Field(default=None, description="Título do eixo X")
    yTitle: Optional[str] = Field(default=None, description="Título do eixo Y")
    series: List[SeriesDefinition] = Field(
        description=(
            "Séries do gráfico. Cada indicador disponível em tools.py vira uma "
            "série (ex: {yField:'Produtividade', label:'Produtividade'})."
        )
    )
    explanation: str = Field(
        description="Breve explicação do que o gráfico mostra e por que."
    )


# ---------------------------------------------------------------------------
# Estruturação dos dados dos indicadores no formato de gráfico (long -> wide)
# ---------------------------------------------------------------------------

def _montar_dados_indicadores() -> list[dict]:
    """Converte _INDICATORS (uma linha por mês/indicador) em uma linha por mês,
    com uma coluna por indicador. Ex: {'mes': 'Janeiro', 'Produtividade': 87, ...}"""
    meses = []
    for ind in _INDICATORS:
        if ind["month"] not in meses:
            meses.append(ind["month"])

    rows = []
    for mes in meses:
        row = {"mes": mes}
        for ind in _INDICATORS:
            if ind["month"] == mes:
                row[ind["indicator"]] = ind["value"]
        rows.append(row)
    return rows


# ---------------------------------------------------------------------------
# A tool — registrada no agente LangGraph com @tool
# ---------------------------------------------------------------------------

@tool("gerar_grafico", args_schema=ChartInput, response_format="content_and_artifact")
def gerar_grafico(
    title: str,
    xField: str,
    series: List[SeriesDefinition],
    explanation: str,
    chart_type: str = "line",
    xTitle: Optional[str] = None,
    yTitle: Optional[str] = None,
) -> tuple[str, dict]:
    """
    Gera um gráfico a partir dos indicadores do projeto (produtividade e retrabalho).

    Use quando o usuário pedir para visualizar, plotar ou comparar os indicadores
    ao longo dos meses. O eixo X deve ser 'mes' e as séries devem ser os nomes dos
    indicadores ('Produtividade', 'Retrabalho').

    EXEMPLOS úteis:
    - Evolução da produtividade: xField="mes",
      series=[{yField:"Produtividade", label:"Produtividade"}]
    - Produtividade x Retrabalho: xField="mes",
      series=[{yField:"Produtividade", label:"Produtividade"},
              {yField:"Retrabalho", label:"Retrabalho"}]
    """
    data = _montar_dados_indicadores()

    if not data:
        return "Não foi possível obter os dados dos indicadores.", {}

    spec: dict = {
        "title": title,
        "chart_type": chart_type,
        "xField": xField,
        "xTitle": xTitle,
        "yTitle": yTitle,
        "series": [s.model_dump() for s in series] if series else [],
        "explanation": explanation,
        "data": data,
    }
    return explanation, spec
