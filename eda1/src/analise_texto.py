import streamlit as st
import pandas as pd
import plotly.express as px
from pipeline import hinos_processados

st.markdown("# Exploração de palavras ✒️")
# st.sidebar.markdown("# Page 3 ❄️")


# Exploração dos textos (eda1_part3.1):
# - Tokenização, remoção de stopwords
# - 10 maiores e menores
# - Boxplot por categoria
# - Histograma de frequência de tamanhos
# - Total de palavras únicas e mais longas
# - Bag-of-words com plot
# - Wordcloud

hinos_analise: pd.DataFrame = hinos_processados()
# renomeia index para Nº
hinos_analise = hinos_analise.rename_axis("Nº")

# texto explicativo sobre stopwords e tokenização

# texto explicando tamanho dos tokens com stopwords pra dizer os maiores

col1, col2 = st.columns(2)

with col1:
    st.markdown("Top 10 maiores louvores")

    st.dataframe(
        hinos_analise[["nome", "num_tokens"]]
        .sort_values("num_tokens", ascending=False)
        .head(10),
        column_config={
            "num_tokens": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do hino em palavras",
                max_value=int(hinos_analise["num_tokens"].max()),
                width="small",
            ),
            "nome": st.column_config.TextColumn("Nome", width="small", max_chars=25),
        },
    )
with col2:
    st.markdown("Top 10 menores louvores")

    st.dataframe(
        hinos_analise[["nome", "num_tokens"]]
        .sort_values("num_tokens", ascending=True)
        .head(10),
        column_config={
            "num_tokens": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do hino em palavras",
                max_value=int(hinos_analise["num_tokens"].max()),
                width="small",
            ),
            "nome": st.column_config.TextColumn("Nome", width="small", max_chars=25),
        },
    )


# boxplot
# Garantir que 'categoria_id' é tratado como uma variável categórica
hinos_analise["categoria_id"] = hinos_analise["categoria_id"].astype("category")

# Criar um mapeamento entre categoria_id e categoria
categoria_mapping = (
    hinos_analise[["categoria_id", "categoria_abr"]]
    .drop_duplicates()
    .set_index("categoria_id")["categoria_abr"]
)


# Gráfico interativo com Plotly (mais a cara do Streamlit)
# Criar coluna com rótulos amigáveis de categoria
hinos_analise["categoria_label"] = hinos_analise["categoria_id"].map(categoria_mapping)

if hinos_analise.empty:
    st.warning(
        "Nenhuma categoria selecionada ou não há dados para as categorias escolhidas."
    )
else:
    fig = px.box(
        hinos_analise,
        x="categoria_abr",
        y="num_tokens",
        points="all",
        hover_data=["nome"],
        labels={"categoria_abr": "Categoria", "num_tokens": "Número de Tokens"},
        title="Relação Entre Número de Tokens e Categoria (Box Plot)",
    )
    fig.update_layout(xaxis_tickangle=-45, boxmode="group")
    st.plotly_chart(fig, use_container_width=True)


# - Histograma de frequência de tamanhos
# - Total de palavras únicas e mais longas
# - Bag-of-words com plot
# - Wordcloud
