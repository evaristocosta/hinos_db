import streamlit as st
from pipeline import hinos_processados

hinos = hinos_processados()
hinos["numero"] = hinos.index

categorias_count = (
    hinos[["categoria_abr", "numero"]]
    .groupby(["categoria_abr"])
    .count()
    .reset_index()
    .rename(columns={"numero": "contagem"})
)

st.markdown("# Categoria dos louvores")

sort_by = st.selectbox(
    "Ordenar por:",
    options=[
        "Nome da categoria",
        "Número de hinos (ascendente)",
        "Número de hinos (descendente)",
    ],
    index=0,
)

if sort_by == "Nome da categoria":
    categorias_count = categorias_count.sort_values("categoria_abr").reset_index()
elif sort_by == "Número de hinos (ascendente)":
    categorias_count = categorias_count.sort_values("contagem").reset_index()
elif sort_by == "Número de hinos (descendente)":
    categorias_count = categorias_count.sort_values(
        "contagem", ascending=False
    ).reset_index()

# exibir grafico de barras ordenadas de acordo com opcao
st.bar_chart(
    categorias_count,
    x="categoria_abr",
    y="contagem",
    x_label="Categoria",
    y_label="Número de hinos",
    sort=False,
    use_container_width=True,
    horizontal=True,
    height=500,
)
