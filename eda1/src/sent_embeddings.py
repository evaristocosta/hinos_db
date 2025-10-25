import streamlit as st
import pandas as pd
from pipeline import hinos_processados, similarity_matrices
import plotly.express as px
from collections import Counter

#    Sequence embeddings (eda1_part5):
st.markdown("# Embeddings de frases 🗒️")

hinos_analise: pd.DataFrame = hinos_processados()
hinos_analise["sent_cluster"] = hinos_analise["sent_cluster"].astype("category")
hinos_analise["BERT_topic"] = hinos_analise["BERT_topic"].astype("category")
_, similarity_sentence = similarity_matrices()

# - Hinos mais semelhantes
st.markdown("## Matriz de Similaridade entre Hinos (Sentence Embeddings)")

fig = px.imshow(
    similarity_sentence,
    labels=dict(x="Hinos", y="Hinos", color="Similaridade"),
)
st.plotly_chart(fig)


# - Hinos mais semelhantes
st.markdown("## Hinos mais semelhantes")
st.markdown(
    "Selecione um hino para ver os mais semelhantes com base nos embeddings de sentenças."
)

hymn_num = st.number_input(
    "Número do hino",
    min_value=int(hinos_analise.index.min()),
    max_value=int(hinos_analise.index.max()),
    value=106,  # um bom exemplo pra iniciar
)

similarities = list(enumerate(similarity_sentence.iloc[hymn_num]))
similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

st.markdown(
    "Mais parecidos com o hino "
    + str(hymn_num)
    + ": "
    + hinos_analise["nome"].iloc[hymn_num]
)
for idx, score in similarities[1:6]:
    st.markdown(
        f"Hino {idx}: {hinos_analise['nome'].iloc[idx]} → similaridade {score:.3f}"
    )


# - Clustering
st.markdown("## Clustering de Hinos com Embeddings de Sentenças")

fig = px.scatter(
    hinos_analise,
    x="sent_umap1",
    y="sent_umap2",
    color="sent_cluster",
    hover_data=["nome"],
    # title="Clustering de Hinos com Embeddings de Sentenças",
    labels={"sent_umap1": "", "sent_umap2": "", "sent_cluster": "Cluster"},
)
st.plotly_chart(fig)

# - Termos mais frequentes
st.markdown("## Termos mais frequentes por cluster")


for c in sorted(hinos_analise["sent_cluster"].unique()):
    cluster_tokens = hinos_analise.loc[
        hinos_analise["sent_cluster"] == c, "tokens_no_stops"
    ].sum()
    top_terms = Counter(cluster_tokens).most_common(10)
    st.markdown(f"\nCluster {c}:")
    st.markdown([t for t, _ in top_terms])


# - Tópicos
st.markdown("## Tópicos comuns entre os hinos")

"""
Tópicos extraídos:
Tópico 0:
['me', 'meu', 'senhor', 'ti', 'minha', 'eu', 'mim', 'jesus', 'és', 'de']

Tópico 1:
['eu', 'que', 'me', 'meu', 'ti', 'não', 'te', 'tudo', 'de', 'senhor']

Tópico 2:
['eu', 'em', 'me', 'meu', 'seu', 'jesus', 'amor', 'com', 'que', 'deus']

Tópico 3:
['deus', 'se', 'não', 'te', 'ele', 'que', 'em', 'teu', 'tu', 'tua']

Tópico 4:
['amor', 'cruz', 'por', 'me', 'jesus', 'que', 'mim', 'eu', 'meu', 'foi']

Tópico 5:
['nos', 'nosso', 'teu', 'em', 'que', 'louvor', 'vidas', 'nós', 'nossas', 'te']

Tópico 6:
['que', 'de', 'os', 'se', 'as', 'do', 'meu', 'deus', 'vem', 'com']

Tópico 7:
['senhor', 'nos', 'teu', 'santo', 'toda', 'tua', 'sobre', 'glória', 'de', 'vem']

Tópico 8:
['aleluia', 'glória', 'de', 'céu', 'oh', 'jesus', 'rei', 'do', 'da', 'no']

Tópico 9:
['me', 'fala', 'quero', 'te', 'em', 'tua', 'meu', 'ardendo', 'senhor', 'teu']

Tópico 10:
['areia', 'tantos', 'como', 'praia', 'maranata', 'voltará', 'rei', 'que', 'de', 'viva']
"""


# - Distribuição de tópicos
st.markdown("## Distribuição de Tópicos nos Hinos")

fig = px.scatter(
    hinos_analise,
    x="sent_umap1",
    y="sent_umap2",
    color="BERT_topic",
    hover_data=["nome"],
)
st.plotly_chart(fig)
