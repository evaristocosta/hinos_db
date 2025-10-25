import streamlit as st
import pandas as pd
from pipeline import hinos_processados, similarity_matrices
import plotly.express as px
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

#    Word embeddings (eda1_part4):

st.markdown("# Embeddings de palavras 📝")

hinos_analise: pd.DataFrame = hinos_processados()
hinos_analise["word_cluster"] = hinos_analise["word_cluster"].astype("category")
hinos_analise["NMF_topic"] = hinos_analise["NMF_topic"].astype("category")
# hinos_analise = hinos_analise.rename_axis("Nº")
similarity_word, _ = similarity_matrices()

# - Matrizes de similaridade com heatmap
st.markdown("## Matriz de Similaridade entre Hinos (Word Embeddings)")

fig = px.imshow(
    similarity_word,
    labels=dict(x="Hinos", y="Hinos", color="Similaridade"),
)
st.plotly_chart(fig)

# - Hinos mais semelhantes
st.markdown("## Hinos mais semelhantes")
st.markdown(
    "Selecione um hino para ver os mais semelhantes com base nos embeddings de palavras."
)

hymn_num = st.number_input(
    "Número do hino",
    min_value=int(hinos_analise.index.min()),
    max_value=int(hinos_analise.index.max()),
    value=106,  # um bom exemplo pra iniciar
)

similarities_tfidf = list(enumerate(similarity_word.iloc[hymn_num]))
similarities_tfidf = sorted(similarities_tfidf, key=lambda x: x[1], reverse=True)

st.markdown(
    "Mais parecidos com o hino "
    + str(hymn_num)
    + ": "
    + hinos_analise["nome"].iloc[hymn_num]
)
for idx, score in similarities_tfidf[1:6]:
    st.markdown(
        f"Hino {idx}: {hinos_analise['nome'].iloc[idx]} → similaridade {score:.3f}"
    )

# - Clustering
st.markdown("## Clustering de Hinos com Embeddings de Palavras")

fig = px.scatter(
    hinos_analise,
    x="word_umap1",
    y="word_umap2",
    color="word_cluster",
    hover_data=["nome"],
    # title="Clustering de Hinos com Embeddings de Palavras",
    labels={"word_umap1": "", "word_umap2": "", "word_cluster": "Cluster"},
)
st.plotly_chart(fig)

# - Termos mais frequentes por cluster
st.markdown("## Termos mais frequentes por cluster")


for c in sorted(hinos_analise["word_cluster"].unique()):
    cluster_tokens = hinos_analise.loc[
        hinos_analise["word_cluster"] == c, "tokens_no_stops"
    ].sum()
    top_terms = Counter(cluster_tokens).most_common(10)

    st.markdown(f"\n**Cluster {c}:**")
    st.markdown([t for t, _ in top_terms])
    # st.markdown(hinos_analise.loc[hinos_analise["word_cluster"] == c, "nome"][:3])

# - Tópicos comuns
st.markdown("## Tópicos comuns entre os hinos")


n_topics = hinos_analise["word_cluster"].nunique()

# Criar TF-IDF apenas para análise de tópicos
vectorizer = TfidfVectorizer(
    max_features=500,
    stop_words=None,  # você já removeu as stopwords
    ngram_range=(1, 3),  # uni, bi e trigramas
    min_df=2,  # palavra deve aparecer em pelo menos 2 documentos
)

# Usar texto já limpo (sem stopwords)
texts_for_topics = [" ".join(tokens) for tokens in hinos_analise["tokens_no_stops"]]
X_tfidf = vectorizer.fit_transform(texts_for_topics)

# NMF também funciona com TF-IDF
nmf = NMF(n_components=n_topics, random_state=42, max_iter=100)
nmf_topics = nmf.fit_transform(X_tfidf)


def display_topics(model, feature_names, n_top_words=10):
    for idx, topic in enumerate(model.components_):
        st.markdown(f"\nTópico {idx+1}:")
        top_words = [feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
        st.markdown(f"Palavras-chave: {' | '.join(top_words)}")


feature_names = vectorizer.get_feature_names_out()

display_topics(nmf, feature_names)


# - Distribuição de tópicos
st.markdown("## Distribuição de Tópicos nos Hinos")

fig = px.scatter(
    hinos_analise,
    x="word_umap1",
    y="word_umap2",
    color="NMF_topic",
    hover_data=["nome"],
)
st.plotly_chart(fig)
