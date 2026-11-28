import streamlit as st
import requests
import pandas as pd

# vendo esse video para aprender mais sobre a API e tentar fazer o sistema
# https://youtu.be/vPMHgiN6row
# Video para o streamlit de forma Fácil https://youtu.be/zxA97KcUm1Q

# links da api do ibge
URL_NOMES = "https://servicodados.ibge.gov.br/api/v2/censos/nomes"
URL_ESTADOS = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"


def buscar_nome(nome):  # pega os dados do nome por decada
    try:
        resposta = requests.get(f"{URL_NOMES}/{nome}")
        if resposta.status_code == 200:  # 200 quer dizer q deu bom
            dados = resposta.json()
            if dados:
                return dados[0]["res"]
            st.warning(f"O nome {nome} não foi encontrado.")
        else:
            st.error("Erro ao conectar com a API do IBGE. Tente novamente.")
    except requests.exceptions.RequestException:  # se cair a internet ou a api der problema
        st.error("Erro ao conectar com a API do IBGE. Tente novamente.")
    return None


def buscar_por_estado(nome):  # mesma coisa mas separado por estado (uf)
    try:
        resposta = requests.get(f"{URL_NOMES}/{nome}?groupBy=uf")
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados:
                return dados
    except requests.exceptions.RequestException:
        st.error("Erro ao conectar com a API do IBGE. Tente novamente.")
    return None


def buscar_estados():  # pega a lista de estados pq a api de nomes so manda o codigo (ex: 35 = Sao Paulo)
    try:
        resposta = requests.get(URL_ESTADOS)
        if resposta.status_code == 200:
            dados = resposta.json()
            estados = {}
            for estado in dados:
                estados[str(estado["id"])] = estado["nome"]
            return estados
    except requests.exceptions.RequestException:
        st.error("Erro ao conectar com a API do IBGE. Tente novamente.")
    return {}


def montar_grafico_decadas(dados, nome):  # arruma a tabela pro grafico de linhas
    tabela = pd.DataFrame(dados)
    tabela = tabela[["periodo", "frequencia"]]
    tabela = tabela.rename(columns={"frequencia": nome})
    return tabela.set_index("periodo")


def montar_tabela_estados(dados_estados, estados, nome):  # arruma a tabela pro grafico de barras
    lista = []
    for item in dados_estados:
        codigo = str(item["localidade"])
        lista.append({
            "Estado": estados.get(codigo, codigo),  # troca o numero pelo nome do estado
            nome: item["res"][0]["frequencia"]
        })
    tabela = pd.DataFrame(lista)
    return tabela.set_index("Estado")


def mostrar_totais(nome1, dados1, nome2, dados2):
    # mostra os totais
    st.subheader("Total no Brasil")
    total1 = 0  # soma tudo pra saber o total no brasil
    for item in dados1:
        total1 += item["frequencia"]

    if dados2:
        total2 = 0
        for item in dados2:
            total2 += item["frequencia"]
        c1, c2 = st.columns(2)
        c1.metric(nome1, total1)
        c2.metric(nome2, total2)
    else:
        st.metric(nome1, total1)


def mostrar_decadas(nome1, dados1, nome2, dados2):
    # grafico por decada
    st.subheader("Frequência por década")
    grafico = montar_grafico_decadas(dados1, nome1)
    if dados2:
        grafico2 = montar_grafico_decadas(dados2, nome2)
        grafico = grafico.join(grafico2)  # junta os dois nomes no mesmo grafico
        st.line_chart(grafico, color=["#1f77b4", "#ff7f0e"])
    else:
        st.line_chart(grafico, color="#1f77b4")


def mostrar_estados(nome1, nome2, dados2):
    # grafico e tabela por estado
    st.subheader("Distribuição por estado")
    estados = buscar_estados()
    dados_est1 = buscar_por_estado(nome1)

    if dados_est1:
        tabela_estados = montar_tabela_estados(dados_est1, estados, nome1)
        cor_grafico = "#1f77b4"

        if dados2:
            dados_est2 = buscar_por_estado(nome2)
            if dados_est2:
                tabela_est2 = montar_tabela_estados(dados_est2, estados, nome2)
                tabela_estados = tabela_estados.join(tabela_est2).fillna(0).astype(int)  # se faltar estado em um nome, poe 0
                cor_grafico = ["#1f77b4", "#ff7f0e"]

        tabela_estados = tabela_estados.sort_values(by=nome1, ascending=False)  # ordena do maior pro menor
        st.bar_chart(tabela_estados, color=cor_grafico, horizontal=True)
        st.dataframe(tabela_estados)
    else:
        st.info("Sem dados por estado para esse nome.")


# parte visual do site
st.set_page_config(page_title="Nomes no Brasil", layout="centered")

# muda a fonte, o fundo e centraliza ( ESSA PARTE EU PRECISEI DE AJUDA DA IA, NAO SABIA MUDAR O FRONT NO STREAMLIT )
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=National+Park&display=swap');

.stApp {
    background-color: #111827;
    font-family: 'National Park', sans-serif;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("Nomes no Brasil - Trabalho Final Ciencia da Computação")
st.write("Consulta de nomes registrados no Brasil (Censo 2010 - IBGE).")

# caixinhas pra digitar os nomes
col1, col2 = st.columns(2)
with col1:
    nome1 = st.text_input("Primeiro nome", placeholder="Ex: Lucia Caminos")
with col2:
    nome2 = st.text_input("Comparar com outro nome", placeholder="Ex: Jason Duval")

if st.button("Pesquisar"):  # so roda quando clica no botao
    if not nome1.strip():
        st.warning("Digite um nome para pesquisar.")
    else:
        nome1 = nome1.strip().title()
        nome2 = nome2.strip().title()

        dados1 = buscar_nome(nome1)
        if dados1:
            dados2 = None
            if nome2:  # so busca o segundo se tiver alguma coisa escrita
                dados2 = buscar_nome(nome2)

            mostrar_totais(nome1, dados1, nome2, dados2)
            mostrar_decadas(nome1, dados1, nome2, dados2)
            st.divider()
            mostrar_estados(nome1, nome2, dados2)
