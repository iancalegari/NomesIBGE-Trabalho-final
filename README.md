# Nomes no Brasil (IBGE)

Aplicação web feita em Python com **Streamlit** para consultar e comparar a popularidade de nomes próprios no Brasil usando os dados do Censo Demográfico de 2010 através da API pública do IBGE.

## Funcionalidades

- Pesquisa de um nome ou comparação entre dois nomes.
- Exibição do total de registros no Brasil.
- Gráfico de linhas com a evolução da frequência por década.
- Gráfico de barras e tabela com a distribuição por estado (UF).
- Mensagens de aviso caso o nome não seja encontrado ou ocorra erro na conexão com a API.

## Funcionamento da aplicação

1. O usuário informa um nome no campo **Primeiro nome** (e, opcionalmente, um segundo nome em **Comparar com outro nome**) e clica em **Pesquisar**.
2. A função `buscar_nome(nome)` envia uma requisição HTTP `GET` para a API do IBGE e, quando o retorno é `200`, extrai os dados em JSON com as frequências por década; os valores são somados para exibir o total no Brasil com `st.metric`.
3. A função `montar_grafico_decadas(dados, nome)` organiza os dados em um `DataFrame` do `pandas` por período e exibe a evolução temporal com `st.line_chart` (juntando os dois nomes quando há comparação).
4. As funções `buscar_por_estado(nome)`, `buscar_estados()` e `montar_tabela_estados(dados_estados, estados, nome)` consultam as ocorrências por UF, convertem o código numérico para o nome do estado e exibem a distribuição geográfica com `st.bar_chart` e `st.dataframe`.
5. Caso o campo esteja vazio, o nome não seja encontrado na API ou ocorra falha de conexão, a aplicação exibe um aviso na tela sem travar.

## Endpoints utilizados (API do IBGE)

- `https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}` — busca a frequência do nome por década.
- `https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}?groupBy=uf` — busca a frequência do nome separada por estado (UF).
- `https://servicodados.ibge.gov.br/api/v1/localidades/estados` — busca a lista de estados para converter o código da UF no nome do estado.

## Como executar localmente

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o aplicativo:
```bash
streamlit run app.py
```

## Arquivos do projeto

- `app.py` — código principal da aplicação.
- `requirements.txt` — bibliotecas utilizadas (`streamlit`, `requests` e `pandas`).


## Referência

- Vídeo de estudo sobre a API: https://youtu.be/vPMHgiN6row , https://youtu.be/zxA97KcUm1Q
