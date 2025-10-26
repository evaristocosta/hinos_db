import streamlit as st
import pandas as pd
from pipeline import hinos_processados
import plotly.express as px

# Emoções (eda1_part7):
st.markdown("# Análise de emoções nos hinos 🎭")

hinos_analise: pd.DataFrame = hinos_processados()

# - Visualização e estatísticas
st.markdown("## Distribuição das emoções dominantes")

emocoes_dominantes = []
scores_dominantes = []

for emocoes in hinos_analise["emocoes"]:
    if emocoes:
        top_emocao = max(emocoes.items(), key=lambda x: x[1])
        emocoes_dominantes.append(top_emocao[0])
        scores_dominantes.append(top_emocao[1])
    else:
        emocoes_dominantes.append("unknown")
        scores_dominantes.append(0.0)

emocao_counts = pd.Series(emocoes_dominantes).value_counts().head(10)

st.bar_chart(
    emocao_counts,
    # x="emocoes",
    # y="contagem",
    y_label="Emoção",
    x_label="Número de hinos",
    sort=False,
    width="stretch",
    horizontal=True,
    # height=500,
    # title="Top 10 Emoções Dominantes nos Hinos",
)


fig = px.histogram(
    x=scores_dominantes,
    title="Distribuição dos Scores das Emoções Dominantes",
    labels={"x": "Score da Emoção", "y": "Número de Hinos"},
)

st.plotly_chart(fig)


# - Heatmap de emoções
st.markdown("## Heatmap das emoções nos hinos")

emocoes_expandidas = []
for idx, row in hinos_analise.iterrows():
    if row["emocoes"]:
        emocoes_expandidas.append(row["emocoes"])

if emocoes_expandidas:
    emo_df = pd.DataFrame(emocoes_expandidas)
    emocoes_principais = emo_df.mean().nlargest(10).index
    emo_df_filtrado = emo_df[emocoes_principais]
    # arredonda os valores para melhor visualização

    emo_df_filtrado = emo_df_filtrado.style.background_gradient(
        subset=emocoes_principais
    )
    # emo_df_filtrado["nome"] = hinos_analise["nome"].values
    # emo_df_filtrado.rename_axis("Nº")

    st.dataframe(
        emo_df_filtrado,
        column_config={
            "nome": st.column_config.TextColumn(
                "Nome do Hino", width="medium", max_chars=30
            )
        },
    )

# - Pesquisa de hinos e mostrar emoções
st.markdown("## Pesquisa de hinos por emoções")
