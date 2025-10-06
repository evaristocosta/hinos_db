import streamlit as st
from pipeline import hinos_processados

hinos = hinos_processados()

# Widgets de filtro
st.sidebar.header("Filtros")  # Deixar os filtros na barra lateral

# Filtros
num_selecionado = st.sidebar.text_input("Filtrar por número:")
nome_filtro = st.sidebar.text_input("Filtrar por nome:")
texto_filtro = st.sidebar.text_input("Filtrar no texto:")

# Aplicar os filtros
hinos_filtrado = hinos.copy()
if num_selecionado:
    hinos_filtrado = hinos_filtrado[
        hinos_filtrado["numero"].astype(str).str.contains(num_selecionado)
    ]

if nome_filtro:
    hinos_filtrado = hinos_filtrado[
        hinos_filtrado["nome"].str.contains(nome_filtro, case=False, na=False)
    ]


if texto_filtro:
    hinos_filtrado = hinos_filtrado[
        hinos_filtrado["texto_limpo"].str.contains(texto_filtro, case=False, na=False)
    ]

# Filtro por categoria
categorias_unicas = hinos["categoria"].unique()
categorias_selecionadas = st.sidebar.multiselect(
    "Filtrar por categoria:", categorias_unicas, default=categorias_unicas
)
hinos_filtrado = hinos_filtrado[
    hinos_filtrado["categoria"].isin(categorias_selecionadas)
]


st.markdown("# Tabela de louvores")
st.dataframe(
    hinos_filtrado[
        [
            "numero",
            "nome",
            "categoria",
            "texto_limpo",
        ]
    ].rename(
        columns={
            "numero": "Número",
            "nome": "Título",
            "categoria": "Categoria",
            "texto_limpo": "Texto",
        }
    ),
    hide_index=True,
)
