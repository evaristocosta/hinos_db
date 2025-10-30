import streamlit as st
import pandas as pd
from pipeline import hinos_processados, similarity_matrices
import plotly.express as px
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

#    Word embeddings (eda1_part4):

"""
# Embeddings de palavras 📝

Nesta seção, exploramos os embeddings de palavras gerados a partir dos textos dos hinos.
Utilizamos técnicas de processamento de linguagem natural para transformar os textos em representações 
vetoriais densas, que capturam o significado semântico das palavras. Esses embeddings permitem analisar 
similaridades entre hinos, realizar clustering e identificar tópicos comuns.
"""

hinos_analise: pd.DataFrame = hinos_processados()
hinos_analise["word_cluster"] = hinos_analise["word_cluster"].astype("category")
hinos_analise["NMF_topic"] = hinos_analise["NMF_topic"].astype("category")
# hinos_analise = hinos_analise.rename_axis("Nº")
similarity_word, _ = similarity_matrices()

st.sidebar.header("Filtros")
categorias_unicas = hinos_analise["categoria_abr"].unique()
categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as categorias",
    options=categorias_unicas,
    placeholder="Todas as categorias",
)
if categorias_selecionadas:
    hinos_analise = hinos_analise[
        hinos_analise["categoria_abr"].isin(categorias_selecionadas)
    ]

# - Matrizes de similaridade com heatmap
"""
## Matriz de Similaridade entre Hinos

Aqui, visualizamos a matriz de similaridade entre os hinos com base nos embeddings de palavras. Cada célula na matriz 
representa o grau de similaridade entre dois hinos, onde valores mais altos indicam maior similaridade semântica.

estratégia de peso: TF-IDF
"""

fig = px.imshow(
    similarity_word,
    labels=dict(x="Hinos", y="Hinos", color="Similaridade"),
    width=600,
    height=600,
)
st.plotly_chart(fig)

"""
Diferentemente da matriz de similaridade baseada em TF-IDF, que se concentra na frequência e importância das palavras 
nos documentos, a matriz de similaridade baseada em embeddings de palavras captura relações semânticas mais profundas 
entre os hinos. Isso significa que hinos com significados semelhantes, mesmo que usem palavras diferentes, podem ser 
identificados como similares, o que explica porque mais hinos aparecem como similares nesta matriz.

Dois hinos que chamam a atenção são 106 - "Pela fé somos salvos" e 179 - "Pela fé eu posso contemplar Jesus": ambos tem 
baixa similaridade com a maioria dos outros hinos, mas alta similaridade entre si. Isso sugere que, apesar de usarem 
palavras diferentes, eles compartilham um significado semântico semelhante, relacionado ao tema da fé e salvação.
"""

# - Hinos mais semelhantes
"""
## Hinos mais semelhantes

A seguir, selecione um hino para ver os mais semelhantes com base nos embeddings de palavras.
"""

hymn_num = st.number_input(
    "Número do hino",
    min_value=int(hinos_analise.index.min()),
    max_value=int(hinos_analise.index.max()),
    value=106,  # um bom exemplo pra iniciar
)
hymn_name = hinos_analise.loc[hymn_num, "nome"]
st.markdown(f"**🎵 Hino {hymn_num} — {hymn_name}:**")

similarities_tfidf = list(enumerate(similarity_word.iloc[hymn_num]))
similarities_tfidf = sorted(similarities_tfidf, key=lambda x: x[1], reverse=True)

rows = []
for idx, score in similarities_tfidf[1:11]:
    rows.append(
        {
            "Hino": int(idx),
            "Nome": hinos_analise["nome"].iloc[idx],
            "Similaridade": float(score),
        }
    )
df_sim = pd.DataFrame(rows).set_index("Hino")
st.dataframe(df_sim.style.format({"Similaridade": "{:.3f}"}))

# - Clustering
# Diminuição de dimensionalidade: UMAP
# Clustering: K-Means
# Definição de clusters: silhueta - 4º melhor valor, 10 clusters
"""
## Clustering de Hinos

Utilizando os embeddings de palavras, aplicamos técnicas de redução de dimensionalidade (UMAP) e clustering (K-Means) para 
agrupar os hinos com base em suas similaridades semânticas. A visualização abaixo mostra os hinos em um espaço bidimensional,
onde cores diferentes representam clusters distintos. 

Cada ponto representa um hino, e a proximidade entre os pontos indica similaridade semântica. Clusters próximos
sugerem temas ou estilos comuns entre os hinos agrupados. 

A definição dos clusters foi baseada na análise de silhueta, resultando em 10 clusters que capturam bem as variações 
nos temas dos hinos. 

"""

fig = px.scatter(
    hinos_analise,
    x="word_umap1",
    y="word_umap2",
    color="word_cluster",
    hover_data=["nome"],
    # title="Clustering de Hinos com Embeddings de Palavras",
    labels={"word_umap1": "", "word_umap2": "", "word_cluster": "Cluster"},
    width=600,
    height=600,
)
st.plotly_chart(fig)

# - Termos mais frequentes por cluster
"""
### Termos mais frequentes por cluster

A seguir, apresentamos os termos mais frequentes em cada cluster de hinos, conforme identificado pelo algoritmo de clustering.
Esses termos fornecem insights sobre os temas predominantes em cada grupo de hinos. 

"""


rows = []
for c in sorted(hinos_analise["word_cluster"].unique()):
    cluster_tokens = hinos_analise.loc[
        hinos_analise["word_cluster"] == c, "tokens_no_stops"
    ].sum()
    top_terms = [t for t, _ in Counter(cluster_tokens).most_common(10)]
    top_hinos = (
        hinos_analise.loc[hinos_analise["word_cluster"] == c, "nome"].head(3).tolist()
    )

    rows.append(
        {
            "Cluster": str(c),
            "Top terms": ", ".join(top_terms),
            "Top hinos": " | ".join(top_hinos),
        }
    )

df_clusters = pd.DataFrame(rows).set_index("Cluster")
st.dataframe(df_clusters)

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
