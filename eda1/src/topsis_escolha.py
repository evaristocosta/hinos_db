import streamlit as st
import pandas as pd
from pipeline import hinos_processados, similarity_matrices
import streamlit_vertical_slider as svs
from topsis_hamedbaziyad import TOPSIS


#    TOPSIS (eda1_part6):

st.title("Seleção de similares ✅")
hinos_analise: pd.DataFrame = hinos_processados()
similarity_word, similarity_sent, similarity_emocoes = similarity_matrices()

"""
Nesta seção, utilizamos o método TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) para 
selecionar hinos similares com base em múltiplos critérios, incluindo categorias, clusters e similaridades, calculados
nas análises anteriores. O TOPSIS é uma técnica de tomada de decisão multi-critério que classifica as alternativas 
com base na distância de uma solução ideal positiva e negativa. 

"""


# - Funcionamento
# - Escolha do hino

"""### 1. Escolha um hino para ver sugestões similares:"""
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
similarity_matrix_emocoes_sample = similarity_emocoes.loc[
    hino_sample.name, hinos_restantes.index
]
hinos_restantes["sim_word"] = similarity_matrix_words_sample.values
hinos_restantes["sim_sent"] = similarity_matrix_sent_sample.values
hinos_restantes["sim_emocao"] = similarity_matrix_emocoes_sample.values

# - Escolha dos pesos
"""### 2. Defina os pesos para cada critério"""

categories = [
    "categoria_id",
    "word_cluster",
    "NMF_topic",
    "sent_cluster",
    "BERT_topic",
    "sim_word",
    "sim_sent",
    "sim_emocao",
]


(
    categoria_id_weight,
    word_cluster_weight,
    NMF_topic_weight,
    sent_cluster_weight,
    BERT_topic_weight,
    sim_word_weight,
    sim_sent_weight,
    sim_emocao_weight,
) = (0, 0, 0, 0, 0, 0, 0, 0)

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
with col1:
    st.badge("Categoria")

    categoria_id_weight = svs.vertical_slider(
        key="categoria_id",
        default_value=100,
        step=1,
        min_value=0,
        max_value=100,
    )
    st.caption("Considerando as categorias da coletânea de hinos.")

with col2:
    st.badge("Similaridade (palavras)", color="orange")
    sim_word_weight = svs.vertical_slider(
        key="sim_word",
        default_value=50,
        step=1,
        min_value=0,
        max_value=100,
    )
    st.caption(
        "Considerando a similaridade entre os hinos com base em Word Embeddings."
    )

with col3:
    st.badge("Cluster (palavras)", color="orange")
    word_cluster_weight = svs.vertical_slider(
        key="word_cluster",
        default_value=90,
        step=1,
        min_value=0,
        max_value=100,
    )
    st.caption("Considerando os clusters de palavras dos hinos.")

with col4:
    st.badge("Tópico NMF", color="orange")
    NMF_topic_weight = svs.vertical_slider(
        key="NMF_topic",
        default_value=80,
        step=1,
        min_value=0,
        max_value=100,
    )
    st.caption("Considerando os tópicos NMF dos hinos.")

with col5:
    st.badge("Similaridade (sentenças)", color="green")
    sim_sent_weight = svs.vertical_slider(
        key="sim_sent",
        default_value=40,
        step=1,
        min_value=0,
        max_value=100,
    )
    st.caption(
        "Considerando a similaridade entre os hinos com base em Sentence Embeddings."
    )

with col6:
    st.badge("Cluster (sentenças)", color="green")
    sent_cluster_weight = svs.vertical_slider(
        key="sent_cluster",
        default_value=70,
        step=1,
        min_value=0,
        max_value=100,
    )
    st.caption("Considerando os clusters de sentenças dos hinos.")

with col7:
    st.badge("Tópico BERT", color="green")
    BERT_topic_weight = svs.vertical_slider(
        key="BERT_topic",
        default_value=60,
        step=1,
        min_value=0,
        max_value=100,
    )
    st.caption("Considerando os tópicos BERT dos hinos.")

with col8:
    st.badge("Similaridade (emoções)", color="red")
    sim_emocao_weight = svs.vertical_slider(
        key="sim_emocao",
        default_value=30,
        step=1,
        min_value=0,
        max_value=100,
    )
    st.caption(
        "Considerando a similaridade entre os hinos com base na análise de emoções."
    )

weights = [
    categoria_id_weight,
    word_cluster_weight,
    NMF_topic_weight,
    sent_cluster_weight,
    BERT_topic_weight,
    sim_word_weight,
    sim_sent_weight,
    sim_emocao_weight,
]

# - Resultados
"""
# Resultados da seleção TOPSIS

"""

# Valida se os sliders já retornaram valores (não são None)
if any(w is None for w in weights):
    st.warning(
        "Aguarde a inicialização dos sliders ou ajuste-os para prosseguir com a seleção TOPSIS."
    )
    st.stop()

# Evita divisão por zero: exige soma > 0
sum_w = sum(weights)
if sum_w == 0:
    st.warning(
        "A soma dos pesos é zero. Ajuste pelo menos um peso para um valor maior que zero."
    )
    st.stop()

# Normaliza os pesos
weights = [w / sum_w for w in weights]
if sum(weights) != 1:
    st.warning(
        "Aguarde a inicialização dos sliders ou ajuste-os para prosseguir com a seleção TOPSIS."
    )
    st.stop()

profit_cost = [1, 1, 1, 1, 1, 1, 1, 1]


# executa TOPSIS apenas após validações
# valida e prepara a matriz de critérios para evitar None dentro da função TOPSIS
X = hinos_restantes[categories].copy()
# força tipos numéricos; se houver valores não-convertíveis vira NaN -> substitui por 0
X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

# valida consistência de dimensões com os vetores de peso e profit_cost
if X.shape[1] != len(weights) or X.shape[1] != len(profit_cost):
    print("nem entrou")
    st.error(
        f"Número de critérios ({X.shape[1]}) diferente do tamanho de weights ({len(weights)}) "
        f"ou profit_cost ({len(profit_cost)}). Ajuste antes de prosseguir."
    )
    st.stop()

output = TOPSIS(
    X,
    weights,
    profit_cost,
)
scores = pd.DataFrame(output)
scores.columns = ["topsis_score"]
hinos_restantes = pd.concat([hinos_restantes, scores], axis=1).sort_values(
    by="topsis_score", ascending=False
)

st.markdown(f"Sugestões para o hino: **{hino_sample.name} - {hino_sample['nome']}**")
st.dataframe(
    hinos_restantes[["nome", "topsis_score"]].head(20).rename_axis("Nº"),
    width="stretch",
    column_config={
        "nome": st.column_config.TextColumn("Nome"),
        # "texto_limpo": st.column_config.TextColumn("Texto", width="medium"),
        "topsis_score": st.column_config.NumberColumn(
            "TOPSIS Score",
            format="%.2f",
        ),
    },
    height=500,
)
