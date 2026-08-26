Engenheiro(a) de Software – IA - Prova técnica
Tempo estimado: 3 a 4 horas
Modalidade: Individual
Foco principal: Codificação e resolução de problemas
________________________________________
1. Objetivo
O objetivo desta prova é avaliar sua capacidade de desenvolver uma aplicação funcional utilizando Engenharia de Software e Inteligência Artificial Generativa.
A avaliação terá ênfase principalmente em:
•	qualidade do código;
•	Python;
•	desenvolvimento de APIs;
•	integração com LLM;
•	construção de Agentes de IA;
•	Tool Calling;
•	tratamento de erros;
•	testes automatizados;
•	organização e clareza da solução.
Não é necessário desenvolver uma solução completa de produção.
________________________________________
2. Desafio
Desenvolva uma API para um Assistente Corporativo com IA.
O assistente deverá receber perguntas em linguagem natural e utilizar ferramentas disponíveis para consultar informações antes de produzir uma resposta.
A aplicação deverá utilizar preferencialmente:
•	Python;
•	FastAPI;
•	Claude ou Gemini.
Caso não possua acesso às APIs do Claude ou Gemini, poderá utilizar outro LLM ou realizar um mock da chamada.
________________________________________
3. Dados disponíveis
Considere os seguintes indicadores:
Mês	Indicador	Valor
Janeiro	Produtividade	87
Fevereiro	Produtividade	82
Março	Produtividade	91
Janeiro	Retrabalho	12
Fevereiro	Retrabalho	18
Março	Retrabalho	10
Esses dados poderão ser armazenados da maneira que considerar mais adequada, por exemplo:
•	JSON;
•	CSV;
•	SQLite;
•	estrutura Python.
Considere também as seguintes informações corporativas:
Documento 1 – Janeiro
O indicador de produtividade representa a relação entre as entregas realizadas e os recursos empregados. Valores acima de 85 são considerados dentro da faixa esperada.
Documento 2 – Fevereiro
Em fevereiro ocorreu uma redução temporária da produtividade em função da implantação de uma nova plataforma corporativa. Durante o período houve aumento do retrabalho e necessidade de adaptação das equipes.
Documento 3 – Março
Em março ocorreu recuperação da produtividade após estabilização da plataforma e capacitação das equipes. Também foi observada redução do retrabalho.
________________________________________
4. Implementação obrigatória
4.1 API
Desenvolva uma API utilizando preferencialmente FastAPI.
Implemente o endpoint:
POST /agent/query
Exemplo de entrada:
{
  "question": "Por que a produtividade caiu em fevereiro?"
}
Exemplo de resposta:
{
  "answer": "A produtividade caiu...",
  "tools_used": [
    "get_indicators",
    "search_documents"
  ]
}
A estrutura da resposta poderá ser adaptada.
________________________________________
4.2 Ferramentas
Implemente pelo menos duas ferramentas que possam ser utilizadas pelo assistente.
Tool 1 – get_indicators
Deverá consultar os dados estruturados dos indicadores.
Exemplo:
get_indicators(
    indicator="Produtividade",
    month="Fevereiro"
)
Resultado esperado:
{
  "indicator": "Produtividade",
  "month": "Fevereiro",
  "value": 82
}
________________________________________
Tool 2 – search_documents
Deverá pesquisar as informações corporativas disponibilizadas nesta prova.
Exemplo:
search_documents(
    query="queda da produtividade em fevereiro"
)
A implementação da busca fica a critério do candidato.
Pode ser utilizada:
•	busca textual;
•	busca por palavras-chave;
•	embeddings;
•	banco vetorial;
•	RAG;
•	outra estratégia justificável.
________________________________________
4.3 Agente de IA
Implemente uma lógica capaz de decidir quais ferramentas utilizar para responder às perguntas.
O agente deverá ser capaz, no mínimo, de:
a) consultar apenas indicadores quando necessário;
b) consultar apenas documentos quando necessário;
c) combinar indicadores e documentos;
d) utilizar o LLM para produzir a resposta final.
O agente poderá ser desenvolvido utilizando:
•	Claude;
•	Gemini;
•	LangChain;
•	LangGraph;
•	implementação própria;
•	outro framework equivalente.
O uso de framework de agentes não é obrigatório.
Será valorizada principalmente a clareza da implementação.
________________________________________
5. Perguntas que sua aplicação deverá responder
Utilize as seguintes perguntas para demonstrar o funcionamento da solução:
Pergunta 1
Qual foi a produtividade em fevereiro?
Pergunta 2
O que significa o indicador de produtividade?
Pergunta 3
Como evoluiu a produtividade entre janeiro e março?
Pergunta 4
Por que a produtividade caiu em fevereiro?
Pergunta 5
Existe alguma relação entre produtividade e retrabalho no período?
Pergunta 6
Considerando os dados disponíveis, quais recomendações você daria para a gestão?
O agente deverá selecionar as ferramentas de acordo com cada pergunta.
________________________________________
7. README
Inclua um README contendo:
Como executar
Explique como instalar as dependências e iniciar a aplicação.
Como testar
Explique como executar os testes automatizados.
Decisões técnicas
Explique brevemente:
•	como funciona o agente;
•	como ocorre a seleção das ferramentas;
•	como foi realizada a integração com o LLM;
•	principais decisões tomadas.
Limitações
Informe funcionalidades ou melhorias que seriam implementadas caso houvesse mais tempo.
________________________________________
8. Entrega
Entregue preferencialmente um repositório Git contendo:
1.	Realizar a apresentação das aplicações desenvolvidas;
2.	código-fonte;
3.	dados utilizados;
4.	testes;
5.	requirements.txt ou equivalente;
6.	.env.example;
7.	README.
A aplicação deverá possuir instruções suficientes para que o avaliador consiga executá-la.

