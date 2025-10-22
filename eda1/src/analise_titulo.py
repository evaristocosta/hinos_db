import streamlit as st
import pandas as pd
from pipeline import hinos_processados

hinos: pd.DataFrame = hinos_processados()

# separa dados de interesse
hinos["numero"] = hinos.index
hinos_analise = (
    hinos[["numero", "nome", "categoria_abr"]]
    .rename(columns={"numero": "Nº", "nome": "Nome", "categoria_abr": "Categoria"})
    .set_index("Nº")
)
# separa subtitulo do nome
hinos_analise["subtitulo"] = (
    hinos_analise["Nome"].str.extract(r"\((.*?)\)").squeeze().str.strip()
)
hinos_analise["Nome"] = hinos_analise["Nome"].str.replace(
    r"\s*\(.*?\)\s*", "", regex=True
)
# cria dataframe comparativo, considerando o subtitulo como um nome diferente
hinos_titulos = pd.concat(
    [
        hinos_analise[["subtitulo", "Categoria"]].rename(columns={"subtitulo": "Nome"}),
        hinos_analise[["Nome", "Categoria"]],
    ]
).dropna()
# calcula o tamanho do titulo
hinos_analise["titulo_tam_real"] = hinos_analise["Nome"].str.len()
hinos_titulos["titulo_tam_real"] = hinos_titulos["Nome"].str.len()


st.markdown("# Tamanho dos títulos")
st.sidebar.markdown("# Filtro")
# add filter by category
categorias = hinos_analise["Categoria"].unique()
categoria_selecionada = st.sidebar.selectbox(
    "Selecione uma categoria:", ["TODAS"] + list(categorias)
)
if categoria_selecionada != "TODAS":
    hinos_analise = hinos_analise.query(f"Categoria == '{categoria_selecionada}'")
    hinos_titulos = hinos_titulos.query(f"Categoria == '{categoria_selecionada}'")


col1, col2 = st.columns(2)


with col1:
    st.markdown("**Desconsiderando subtítulos**")
    st.markdown("Top 10 maiores títulos")
    st.dataframe(
        hinos_analise[["Nome", "titulo_tam_real"]]
        .sort_values(by="titulo_tam_real", ascending=False)
        .head(10),
        column_config={
            "titulo_tam_real": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do título em caracteres",
                max_value=int(hinos_analise["titulo_tam_real"].max()),
                width="small",
            ),
            "Nome": st.column_config.TextColumn(width="small", max_chars=25),
        },
    )
    st.markdown("Top 10 menores títulos")
    st.dataframe(
        hinos_analise[["Nome", "titulo_tam_real"]]
        .sort_values(by="titulo_tam_real")
        .head(10),
        column_config={
            "titulo_tam_real": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do título em caracteres",
                max_value=int(hinos_analise["titulo_tam_real"].max()),
                width="small",
            ),
            "Nome": st.column_config.TextColumn(width="small", max_chars=25),
        },
    )

with col2:
    st.markdown("**Considerando subtítulos**")
    st.markdown("Top 10 maiores títulos")
    st.dataframe(
        hinos_titulos[["Nome", "titulo_tam_real"]]
        .sort_values(by="titulo_tam_real", ascending=False)
        .head(10),
        column_config={
            "titulo_tam_real": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do título em caracteres",
                max_value=int(hinos_titulos["titulo_tam_real"].max()),
                width="small",
            ),
            "Nome": st.column_config.TextColumn(width="small", max_chars=25),
        },
    )
    st.markdown("Top 10 menores títulos")
    st.dataframe(
        hinos_titulos[["Nome", "titulo_tam_real"]]
        .sort_values(by="titulo_tam_real")
        .head(10),
        column_config={
            "titulo_tam_real": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do título em caracteres",
                max_value=int(hinos_titulos["titulo_tam_real"].max()),
                width="small",
            ),
            "Nome": st.column_config.TextColumn(width="small", max_chars=25),
        },
    )
