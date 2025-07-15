import streamlit as st
from pipeline import hinos_processados

hinos = hinos_processados()
categorias_count = (
    hinos[["categoria_id", "categoria", "numero"]]
    .groupby(["categoria_id", "categoria"])
    .count()
    .reset_index()
    .rename(columns={"numero": "contagem"})
)


st.markdown("# Categoria dos louvores")
# st.sidebar.markdown("# Categoria dos louvores")


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
    categorias_count = categorias_count.sort_values("categoria").reset_index()
elif sort_by == "Número de hinos (ascendente)":
    categorias_count = categorias_count.sort_values("contagem").reset_index()
elif sort_by == "Número de hinos (descendente)":
    categorias_count = categorias_count.sort_values(
        "contagem", ascending=False
    ).reset_index()


# adicionar numero de ranking da nova ordenacao ao nome da categoria
categorias_count["categoria_abr"] = (
    (categorias_count.index + 1).astype(str).str.zfill(2)
    + ". "
    + categorias_count["categoria_abr"]
)


# exibir grafico de barras ordenadas de acordo com opcao
st.bar_chart(
    categorias_count.set_index("categoria_abr")["contagem"],
    use_container_width=True,
    horizontal=True,
    height=500,
)
