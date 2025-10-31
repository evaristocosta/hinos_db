import streamlit as st
import pandas as pd
from pipeline import hinos_processados, similarity_matrices
import plotly.express as px
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

#    Word embeddings (eda1_part4):
st.title("Embeddings de Palavras 📝")

"""
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
# estratégia de peso: TF-IDF
"""
# Matriz de Similaridade entre Hinos

Aqui, visualizamos a matriz de similaridade entre os hinos com base nos embeddings de palavras, calculada a partir da 
estratégia de peso TF-IDF. Cada célula na matriz representa o grau de similaridade entre dois hinos, onde valores 
mais altos indicam maior similaridade semântica.

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
# Hinos mais semelhantes

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
# Clustering de Hinos

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

"""
O agrupamento resultante permite dividir claramente os hinos em diferentes categorias. No geral, todos os hinos partilham
de um espaço comum. No entanto, alguns clusters se destacam por sua separação mais clara, indicando temas ou estilos únicos.
Por exemplo, os clusters 8 e 6 tem parte no espaço comum, mas também possuem áreas distintas, sugerindo que embora
compartilhem algumas características com outros hinos, eles também possuem elementos únicos que os diferenciam. 
O cluster 9, por outro lado, está totalmente isolado no canto superior direito, indicando que os hinos nesse grupo 
são semanticamente distintos dos demais.

"""

# - Termos mais frequentes por cluster
"""
## Termos mais frequentes por cluster

A seguir, apresentamos os primeiros 8 termos mais frequentes em cada cluster de hinos, conforme identificado pelo 
algoritmo de clustering. Esses termos fornecem insights sobre os temas predominantes em cada grupo de hinos. 
"""


rows = []
for c in sorted(hinos_analise["word_cluster"].unique()):
    cluster_tokens = hinos_analise.loc[
        hinos_analise["word_cluster"] == c, "tokens_no_stops"
    ].sum()
    top_terms = [t for t, _ in Counter(cluster_tokens).most_common(8)]
    top_hinos = (
        hinos_analise.loc[hinos_analise["word_cluster"] == c, "nome"].sample(3).tolist()
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


"""
É notável que algumas palavras-chave, como "Senhor", "Jesus" e "Deus", aparecem frequentemente em múltiplos clusters,
indicando sua importância central nos temas dos hinos. Como vimos em análises anteriores, essas são as palavras
mais comuns em todo o corpus de hinos.

Interessantemente, os termos relativos ao cluster 9, que está isolado no espaço UMAP, não diferem muito dos termos 
dos outros clusters. Isso sugere que, apesar da separação visual, os hinos desse grupo compartilham semelhanças temáticas
com os demais.
"""


hinos_cluster9 = hinos_analise[hinos_analise["word_cluster"] == 9][
    ["nome", "categoria_abr"]
].rename_axis("Nº")
f"""
## Cluster 9 em perspectiva

O cluster 9 é composto por um total de {hinos_cluster9.shape[0]} hinos. A seguir, são apresentados os hinos 
pertencentes a este cluster, que se destaca por sua separação no espaço UMAP.

"""

st.dataframe(
    hinos_cluster9, column_config={"nome": "Nome do Hino", "categoria_abr": "Categoria"}
)

"""
Não há uma relação óbvia entre os hinos do cluster 9 em termos de categoria, sugerindo que a separação observada no espaço UMAP
pode ser atribuída a outros fatores semânticos ou estilísticos presentes nos textos dos hinos.
"""


# - Tópicos comuns
"""
# Tópicos comuns entre os hinos

Utilizando a técnica de Non-negative Matrix Factorization (NMF) aplicada à representação TF-IDF dos textos dos hinos,
identificamos tópicos comuns presentes nos hinos. Usamos o número de clusters previamente definido como o número de 
tópicos para garantir consistência na análise.
A seguir, apresentamos os principais tópicos e suas palavras-chave associadas.
"""


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
    rows = []
    for idx, topic in enumerate(model.components_):
        top_words = [feature_names[i] for i in topic.argsort()[: -n_top_words - 1 : -1]]
        rows.append({"Tópico": f"{idx+1}", "Palavras-chave": ", ".join(top_words)})
    df_topics = pd.DataFrame(rows).set_index("Tópico")
    return df_topics


feature_names = vectorizer.get_feature_names_out()
df_topics = display_topics(nmf, feature_names)
st.dataframe(df_topics)

"""
Diferentemente dos termos mais frequentes por cluster, os tópicos identificados pelo NMF consideram também bigramas e trigramas,
o que pode revelar temas mais específicos e contextuais presentes nos hinos. Por exemplo, o tópico 3 está diretamente
relacionado ao tema de "Volta de Jesus", enquanto que os tópicos 5 e 9 são de "Glória" e "Aleluia", respectivamente.
Ainda, o tópico 6 contém termos relacionados ao clamor pelo sangue de Jesus, e o tópico 10 indica hinos de serviço e adoração.
"""

# - Distribuição de tópicos
"""
## Distribuição de Tópicos nos Hinos

Podemos usar os tópicos identificados para analisar a distribuição dos hinos no espaço UMAP, colorindo-os de acordo com o tópico
dominante atribuído pelo NMF.
"""

fig = px.scatter(
    hinos_analise,
    x="word_umap1",
    y="word_umap2",
    labels={"word_umap1": "", "word_umap2": "", "NMF_topic": "Tópico NMF"},
    color="NMF_topic",
    hover_data=["nome"],
    width=600,
    height=600,
)
st.plotly_chart(fig)

"""
Diferente dos claros agrupamentos observados com o clustering baseado em K-Means, a distribuição dos tópicos NMF no espaço UMAP
é mais difusa. Isso sugere que os tópicos identificados pelo NMF capturam nuances semânticas que não se traduzem 
diretamente em clusters distintos, indicando uma sobreposição maior entre os temas dos hinos.

É possível observar algumas relações, no entanto. Por exemplo, os hinos do tópico 2 aparecem na mesma região do espaço UMAP
associada ao cluster 6, e o tópico 7 está presente em uma área próxima ao cluster 5. Mas o que chama mais atenção, é que o
tópico 4 está fortemente concentrado na região do cluster 9, sugerindo que os hinos desse tópico compartilham características
semânticas distintas dos demais, e similares entre si.
"""

hinos_topico4 = hinos_analise[hinos_analise["NMF_topic"] == 4][
    ["nome", "categoria_abr"]
].rename_axis("Nº")

f"""
## Hinos do Tópico 4

O tópico 4 é composto por um total de {hinos_topico4.shape[0]} hinos, mais do que o cluster 9 (que tem 
{hinos_cluster9.shape[0]} hinos). A seguir, apresentamos os hinos pertencentes ao tópico 4.
"""

st.dataframe(
    hinos_topico4, column_config={"nome": "Nome do Hino", "categoria_abr": "Categoria"}
)

# termos do cluster 9: glória, jesus, aleluia, sempre, senhor, deus, grande, vencendo
# tópico 4: senhor, louvor, senhor senhor, voz, senhor deus, terra, nome, misericórdia, alma, diante
"""
Observa-se que os hinos do tópico 4 abrangem diversas categorias, sendo que as mais marcantes são sobre volta de Jesus
e louvor. Me chamou a atenção o termo "vencendo" do cluster 9, e "terra" do tópico 4, como distintivos entre os demais grupos e 
tópicos. Talvez esses termos expliquem a separação observada no espaço UMAP do cluster 9: hinos que enfatizam
a vitória de Jesus e a abrangência de Seu reino na terra.
"""
