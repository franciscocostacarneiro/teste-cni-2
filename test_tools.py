from tools import get_indicators, search_documents
from chart_tool import gerar_grafico, SeriesDefinition


def test_get_indicators_por_indicador_e_mes():
    resultado = get_indicators.func(indicator="Produtividade", month="Fevereiro")
    assert "Fevereiro" in resultado
    assert "Produtividade" in resultado
    assert "82" in resultado


def test_get_indicators_somente_indicador():
    resultado = get_indicators.func(indicator="Produtividade")
    assert "Janeiro" in resultado
    assert "Fevereiro" in resultado
    assert "Março" in resultado
    assert "Retrabalho" not in resultado


def test_get_indicators_sem_filtro_retorna_todos():
    resultado = get_indicators.func()
    assert resultado.count("Produtividade") == 3
    assert resultado.count("Retrabalho") == 3


def test_get_indicators_filtro_inexistente():
    resultado = get_indicators.func(indicator="Qualidade")
    assert "Nenhum indicador encontrado" in resultado


def test_search_documents_encontra_contexto():
    resultado = search_documents.func(query="queda da produtividade em fevereiro")
    assert "Documento 2" in resultado


def test_search_documents_definicao():
    resultado = search_documents.func(query="o que significa produtividade")
    assert "Documento 1" in resultado


def test_search_documents_retorna_algo_quando_sem_match():
    resultado = search_documents.func(query="xyz abc qwerty")
    # fallback: retorna todos os documentos
    assert "Documento" in resultado


def test_gerar_grafico_monta_dados_wide():
    msg, spec = gerar_grafico.func(
        title="Evolução",
        xField="mes",
        series=[
            SeriesDefinition(yField="Produtividade", label="Produtividade"),
            SeriesDefinition(yField="Retrabalho", label="Retrabalho"),
        ],
        explanation="teste",
    )
    assert "teste" == msg
    # os dados são transformados: uma linha por mês, com coluna por indicador
    assert len(spec["data"]) == 3  # Janeiro, Fevereiro, Março
    assert spec["data"][0]["mes"] == "Janeiro"
    assert spec["data"][0]["Produtividade"] == 87
    assert spec["data"][0]["Retrabalho"] == 12
    assert spec["series"][0]["yField"] == "Produtividade"
