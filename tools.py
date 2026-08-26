from langchain.tools import tool

# ---------------------------------------------------------------------------
# Dados estruturados dos indicadores corporativos
# ---------------------------------------------------------------------------
_INDICATORS = [
    {"month": "Janeiro",   "indicator": "Produtividade", "value": 87},
    {"month": "Fevereiro", "indicator": "Produtividade", "value": 82},
    {"month": "Março",     "indicator": "Produtividade", "value": 91},
    {"month": "Janeiro",   "indicator": "Retrabalho",    "value": 12},
    {"month": "Fevereiro", "indicator": "Retrabalho",    "value": 18},
    {"month": "Março",     "indicator": "Retrabalho",    "value": 10},
]

# ---------------------------------------------------------------------------
# Documentos corporativos em memória
# ---------------------------------------------------------------------------
_DOCUMENTS = [
    {
        "title": "Documento 1 – Janeiro",
        "content": (
            "O indicador de produtividade representa a relação entre as entregas realizadas "
            "e os recursos empregados. Valores acima de 85 são considerados dentro da faixa esperada."
        ),
    },
    {
        "title": "Documento 2 – Fevereiro",
        "content": (
            "Em fevereiro ocorreu uma redução temporária da produtividade em função da implantação "
            "de uma nova plataforma corporativa. Durante o período houve aumento do retrabalho e "
            "necessidade de adaptação das equipes."
        ),
    },
    {
        "title": "Documento 3 – Março",
        "content": (
            "Em março ocorreu recuperação da produtividade após estabilização da plataforma e "
            "capacitação das equipes. Também foi observada redução do retrabalho."
        ),
    },
]

_STOP_WORDS = {
    "de", "da", "do", "dos", "das", "em", "a", "o", "e", "que", "se",
    "os", "as", "por", "para", "com", "no", "na", "nos", "nas",
    "um", "uma", "foi", "ou", "ao", "ela", "ele",
}


@tool
def get_indicators(indicator: str = "", month: str = "") -> str:
    """Consulta os indicadores corporativos estruturados (Produtividade ou Retrabalho).

    Use quando o usuário perguntar sobre valores numéricos, evolução ou comparação
    entre meses dos indicadores.

    Args:
        indicator: Nome do indicador ('Produtividade' ou 'Retrabalho'). Deixe vazio para todos.
        month: Mês desejado ('Janeiro', 'Fevereiro', 'Março'). Deixe vazio para todos.
    """
    results = _INDICATORS
    if indicator:
        results = [r for r in results if indicator.lower() in r["indicator"].lower()]
    if month:
        results = [r for r in results if month.lower() in r["month"].lower()]
    if not results:
        return "Nenhum indicador encontrado para os filtros informados."
    return "\n".join(
        f"{r['month']} | {r['indicator']}: {r['value']}"
        for r in results
    )


@tool
def search_documents(query: str) -> str:
    """Pesquisa informações nos documentos corporativos da empresa.

    Use quando o usuário perguntar sobre contexto, explicações, causas ou eventos
    relacionados aos indicadores (ex: por que a produtividade caiu, o que significa
    um indicador, o que aconteceu em determinado período).

    Args:
        query: Pergunta ou palavras-chave a pesquisar nos documentos.
    """
    keywords = [
        w for w in query.lower().split()
        if len(w) > 3 and w not in _STOP_WORDS
    ]

    scored = [
        (doc, sum(1 for kw in keywords if kw in doc["content"].lower()))
        for doc in _DOCUMENTS
    ]
    # retorna documentos com pelo menos 1 match; se nenhum, retorna todos
    relevant = [doc for doc, score in scored if score > 0]
    if not relevant:
        relevant = _DOCUMENTS

    return "\n\n".join(
        f"[{doc['title']}]\n{doc['content']}"
        for doc in relevant
    )