import streamlit as st
import pandas as pd
from pipeline import hinos_processados, similarity_matrices
import streamlit_vertical_slider as svs
from topsis_hamedbaziyad import TOPSIS


#    TOPSIS (eda1_part6):

st.markdown("# Seleção de similares ✅")
hinos_analise: pd.DataFrame = hinos_processados()
similarity_word, similarity_sent = similarity_matrices()


# - Funcionamento
# - Escolha do hino

st.markdown("## Escolha um hino para ver sugestões similares")
hymn_num = st.number_input(
    "Número do hino",
    min_value=int(hinos_analise.index.min()),
    max_value=int(hinos_analise.index.max()),
    value=106,  # um bom exemplo pra iniciar
)
hino_sample = hinos_analise.loc[hymn_num]


hinos_restantes = hinos_analise[hinos_analise.index != hino_sample.name].copy()
# se categoria_id é a mesma de sample, então 1, senão 0
hinos_restantes["categoria_id"] = (
    hinos_restantes["categoria_id"] == hino_sample["categoria_id"]
).astype(int)
hinos_restantes["word_cluster"] = (
    hinos_restantes["word_cluster"] == hino_sample["word_cluster"]
).astype(int)
hinos_restantes["NMF_topic"] = (
    hinos_restantes["NMF_topic"] == hino_sample["NMF_topic"]
).astype(int)
hinos_restantes["sent_cluster"] = (
    hinos_restantes["sent_cluster"] == hino_sample["sent_cluster"]
).astype(int)
hinos_restantes["BERT_topic"] = (
    hinos_restantes["BERT_topic"] == hino_sample["BERT_topic"]
).astype(int)
hinos_restantes = hinos_restantes[
    [
        "nome",
        "texto_limpo",
        "categoria_id",
        "word_cluster",
        "NMF_topic",
        "sent_cluster",
        "BERT_topic",
    ]
]

similarity_matrix_words_sample = similarity_word.loc[
    hino_sample.name, hinos_restantes.index
]
similarity_matrix_sent_sample = similarity_sent.loc[
    hino_sample.name, hinos_restantes.index
]
hinos_restantes["sim_word"] = similarity_matrix_words_sample.values
hinos_restantes["sim_sent"] = similarity_matrix_sent_sample.values

# - Escolha dos pesos
st.markdown("## Defina os pesos para cada critério")

categories = [
    "categoria_id",
    "word_cluster",
    "NMF_topic",
    "sent_cluster",
    "BERT_topic",
    "sim_word",
    "sim_sent",
]


(
    categoria_id_weight,
    word_cluster_weight,
    NMF_topic_weight,
    sent_cluster_weight,
    BERT_topic_weight,
    sim_word_weight,
    sim_sent_weight,
) = (0, 0, 0, 0, 0, 0, 0)

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    st.markdown("**Categoria ID**")
    categoria_id_weight = svs.vertical_slider(
        key="categoria_id",
        default_value=100,
        step=1,
        min_value=0,
        max_value=100,
    )
with col2:
    st.markdown("**Word Cluster**")
    word_cluster_weight = svs.vertical_slider(
        key="word_cluster",
        default_value=90,
        step=1,
        min_value=0,
        max_value=100,
    )

with col3:
    st.markdown("**NMF Topic**")
    NMF_topic_weight = svs.vertical_slider(
        key="NMF_topic",
        default_value=80,
        step=1,
        min_value=0,
        max_value=100,
    )
with col4:
    st.markdown("**Sent Cluster**")
    sent_cluster_weight = svs.vertical_slider(
        key="sent_cluster",
        default_value=70,
        step=1,
        min_value=0,
        max_value=100,
    )

with col5:
    st.markdown("**BERT Topic**")
    BERT_topic_weight = svs.vertical_slider(
        key="BERT_topic",
        default_value=60,
        step=1,
        min_value=0,
        max_value=100,
    )

with col6:
    st.markdown("**Similaridade Word Embeddings**")
    sim_word_weight = svs.vertical_slider(
        key="sim_word",
        default_value=50,
        step=1,
        min_value=0,
        max_value=100,
    )

with col7:
    st.markdown("**Similaridade Sentence Embeddings**")
    sim_sent_weight = svs.vertical_slider(
        key="sim_sent",
        default_value=40,
        step=1,
        min_value=0,
        max_value=100,
    )

weights = [
    categoria_id_weight,
    word_cluster_weight,
    NMF_topic_weight,
    sent_cluster_weight,
    BERT_topic_weight,
    sim_word_weight,
    sim_sent_weight,
]
weights = [w / sum(weights) for w in weights]
profit_cost = [1, 1, 1, 1, 1, 1, 1]


# - Resultados
st.markdown("## Resultados da seleção TOPSIS")

# BUG: tenta calcular antes dos sliders serem inicializados
output = TOPSIS(
    hinos_restantes[categories],
    weights,
    profit_cost,
)
scores = pd.DataFrame(output)
scores.columns = ["topsis_score"]
hinos_restantes = pd.concat([hinos_restantes, scores], axis=1).sort_values(
    by="topsis_score", ascending=False
)

st.markdown(
    "Sugestões para o hino: " + str(hino_sample.name) + " - " + str(hino_sample["nome"])
)
st.dataframe(
    hinos_restantes[["nome", "topsis_score", "texto_limpo"]].head(10),
    width="stretch",
    column_config={
        "nome": st.column_config.TextColumn("Nome", width="small", max_chars=25),
        "texto_limpo": st.column_config.TextColumn("Texto", width="medium"),
        "topsis_score": st.column_config.NumberColumn(
            "TOPSIS Score", format="%.2f", width=20
        ),
    },
)
