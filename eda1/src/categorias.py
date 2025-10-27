import streamlit as st
import altair as alt
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

# calcular porcentagem e string formatada para tooltip
total = categorias_count["contagem"].sum()
if total > 0:
    categorias_count["porcentagem"] = categorias_count["contagem"] / total * 100
else:
    categorias_count["porcentagem"] = 0
categorias_count["porcentagem_str"] = categorias_count["porcentagem"].map(
    lambda v: f"{v:.2f}%"
)

# marcar barras maior / menor para color mapping
if not categorias_count.empty:
    max_val = categorias_count["contagem"].max()
    min_val = categorias_count["contagem"].min()

    def bar_type(v):
        if v == max_val:
            return "Maior"
        if v == min_val:
            return "Menor"
        return "Outro"

    categorias_count["bar_type"] = categorias_count["contagem"].apply(bar_type)
else:
    categorias_count["bar_type"] = []

st.markdown("# Categoria dos louvores")

descricao_pagina = """
Nesta seção, exploramos a distribuição de hinos por categoria da coletânea.
Tais categorias são definidas pela própria coletânea.
"""
st.markdown(descricao_pagina)

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
    categorias_count = categorias_count.sort_values("categoria_abr").reset_index(
        drop=True
    )
    y_order = categorias_count["categoria_abr"].tolist()
elif sort_by == "Número de hinos (ascendente)":
    categorias_count = categorias_count.sort_values("contagem").reset_index(drop=True)
    y_order = categorias_count["categoria_abr"].tolist()
elif sort_by == "Número de hinos (descendente)":
    categorias_count = categorias_count.sort_values(
        "contagem", ascending=False
    ).reset_index(drop=True)
    y_order = categorias_count["categoria_abr"].tolist()

# exibir grafico de barras ordenadas de acordo com opcao (Altair para controle de tooltip/ordenacao)
chart = (
    alt.Chart(categorias_count)
    .mark_bar()
    .encode(
        x=alt.X("contagem:Q", title="Número de hinos"),
        y=alt.Y("categoria_abr:N", title="Categoria", sort=y_order),
        tooltip=[
            alt.Tooltip("categoria_abr:N", title="Categoria"),
            alt.Tooltip("contagem:Q", title="Número de hinos"),
            alt.Tooltip("porcentagem_str:N", title="Porcentagem"),
        ],
        color=alt.Color(
            "bar_type:N",
            scale=alt.Scale(
                domain=["Maior", "Menor", "Outro"],
                range=["#a715c1", "#d7800d", "#4c78a8"],
            ),
            legend=None,
        ),
    )
    .properties(height=500)
)

st.altair_chart(chart, use_container_width=True)


# conclusões
# st.markdown("## Conclusões")
conclusao_texto = """
A análise dos dados indica o seguinte:

- A categoria "DEDICAÇÃO" é a maior em quantidade, com 104 hinos (13,08%), sendo a categoria mais representada.
- Outras categorias bastante presentes são "VOLTA DE JESUS E ETERNIDADE" e "MORTE, RESSURREIÇÃO E SALVAÇÃO", 
ambas com 94 hinos cada (11,82% cada), seguidas de "SANTIFICAÇÃO E DERRAMAMENTO DO ESPÍRITO SANTO" 
(92 hinos, 11,57%), "CONSOLO E ENCORAJAMENTO" (91 hinos, 11,45%) e "LOUVOR" (78 hinos, 9,81%).
- Categorias pequenas incluem "SALMOS DE LOUVOR" com apenas 16 hinos (2,01%), destacando-se como a menos representada.
- A distribuição geral não é uniforme: há predominância de categorias relacionados a dedicação, 
volta de Jesus, santificação e consolo, enquanto Salmos de Louvor e Invocação são menos frequentes.
- Ao analisar as porcentagens, notamos que pelo menos seis categorias têm números entre 8%--13%, sugerindo 
certa variedade, mas com clara concentração em algumas temáticas centrais da coletânea.

Essas conclusões indicam as ênfases temáticas da coletânea, com maior foco em dedicação e 
esperança, enquanto louvor de categorias de salmos e invocação têm menos destaque.
"""
st.markdown(conclusao_texto)
