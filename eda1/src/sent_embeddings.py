import streamlit as st
import pandas as pd
from pipeline import hinos_processados, similarity_matrices
import plotly.express as px
from collections import Counter

#    Sequence embeddings (eda1_part5):
st.title("Embeddings de frases 🗒️")
"""
Nesta seção, exploramos os embeddings de frases gerados a partir dos hinos. Os embeddings são representações 
vetoriais que capturam o significado semântico de frases inteiras ao invés de palavras isoladas, permitindo 
comparações e análises mais profundas.
"""

hinos_analise: pd.DataFrame = hinos_processados()
hinos_analise["sent_cluster"] = hinos_analise["sent_cluster"].astype("category")
hinos_analise["BERT_topic"] = hinos_analise["BERT_topic"].astype("category")
_, similarity_sentence = similarity_matrices()


"""
# Matriz de Similaridade entre Hinos

Como na análise de embeddings de palavras, aqui apresentamos a matriz de similaridade entre os hinos,
mas agora utilizando os embeddings de frases. A similaridade é calculada usando a similaridade do cosseno.

"""

fig = px.imshow(
    similarity_sentence,
    labels=dict(x="Hinos", y="Hinos", color="Similaridade"),
    width=600,
    height=600,
)
st.plotly_chart(fig)


"""
# Hinos mais semelhantes

Selecione um hino para ver os mais semelhantes com base nos embeddings de sentenças.
"""

col1, col2 = st.columns(2)
with col1:
    hymn_num = st.number_input(
        "Selecione o número do hino:",
        min_value=int(hinos_analise.index.min()),
        max_value=int(hinos_analise.index.max()),
        value=43,  # um bom exemplo pra iniciar
    )

similarities = list(enumerate(similarity_sentence.iloc[hymn_num]))
similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

with col2:
    st.markdown(f"**🎵 Hino {hymn_num} - {hinos_analise['nome'].iloc[hymn_num]}**")

results = [
    (idx, hinos_analise["nome"].iloc[idx], score) for idx, score in similarities[1:11]
]
df_sim = (
    pd.DataFrame(results, columns=["hino", "nome", "similaridade"])
    .set_index("hino")
    .rename_axis("Nº")
)
df_sim["similaridade"] = df_sim["similaridade"].round(3)
st.dataframe(
    df_sim,
    column_config={"nome": "Nome", "similaridade": "Similaridade"},
)


"""
# Clustering de Hinos com Embeddings de Sentenças

"""

fig = px.scatter(
    hinos_analise,
    x="sent_umap1",
    y="sent_umap2",
    color="sent_cluster",
    hover_data=["nome"],
    # title="Clustering de Hinos com Embeddings de Sentenças",
    labels={"sent_umap1": "", "sent_umap2": "", "sent_cluster": "Cluster"},
    width=600,
    height=600,
)
st.plotly_chart(fig)


"""
# Termos mais frequentes por cluster

"""


rows = []
for c in sorted(hinos_analise["sent_cluster"].unique()):
    cluster_tokens = hinos_analise.loc[
        hinos_analise["sent_cluster"] == c, "tokens_no_stops"
    ].sum()
    top_terms = [t for t, _ in Counter(cluster_tokens).most_common(10)]
    rows.append({"Cluster": c, "Top termos": ", ".join(top_terms)})

df_terms = pd.DataFrame(rows).set_index("Cluster")
st.dataframe(df_terms)


"""
# Tópicos comuns entre os hinos

"""

topics = {
    0: ["me", "meu", "senhor", "ti", "minha", "eu", "mim", "jesus", "és", "de"],
    1: ["eu", "que", "me", "meu", "ti", "não", "te", "tudo", "de", "senhor"],
    2: ["eu", "em", "me", "meu", "seu", "jesus", "amor", "com", "que", "deus"],
    3: ["deus", "se", "não", "te", "ele", "que", "em", "teu", "tu", "tua"],
    4: ["amor", "cruz", "por", "me", "jesus", "que", "mim", "eu", "meu", "foi"],
    5: ["nos", "nosso", "teu", "em", "que", "louvor", "vidas", "nós", "nossas", "te"],
    6: ["que", "de", "os", "se", "as", "do", "meu", "deus", "vem", "com"],
    7: ["senhor", "nos", "teu", "santo", "toda", "tua", "sobre", "glória", "de", "vem"],
    8: ["aleluia", "glória", "de", "céu", "oh", "jesus", "rei", "do", "da", "no"],
    9: ["me", "fala", "quero", "te", "em", "tua", "meu", "ardendo", "senhor", "teu"],
    10: [
        "areia",
        "tantos",
        "como",
        "praia",
        "maranata",
        "voltará",
        "rei",
        "que",
        "de",
        "viva",
    ],
}

rows = [
    {"Tópico": f"Tópico {k}", "Top termos": ", ".join(v)}
    for k, v in sorted(topics.items())
]
df_topics = pd.DataFrame(rows).set_index("Tópico")

st.table(df_topics)


# - Distribuição de tópicos
"""
# Distribuição de Tópicos nos Hinos

"""

fig = px.scatter(
    hinos_analise,
    x="sent_umap1",
    y="sent_umap2",
    color="BERT_topic",
    hover_data=["nome"],
    labels={"sent_umap1": "", "sent_umap2": "", "BERT_topic": "Tópico BERT"},
    width=600,
    height=600,
)
st.plotly_chart(fig)
