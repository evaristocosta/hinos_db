import streamlit as st
import nltk
import pandas as pd
from pipeline import hinos_processados
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px
import altair as alt


st.title("Análise de palavras ✒️")
"""
Nesta seção, exploramos as palavras presentes nos hinos através de n-gramas e análise de similaridade utilizando TF-IDF. 
"""

hinos_analise: pd.DataFrame = hinos_processados()

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


# - N-gramas
"""
# N-gramas

Aqui, analisamos os n-gramas (bigramas e trigramas) mais frequentes nos hinos. N-gramas são sequências 
contíguas de 'n' itens (palavras, neste caso) em um texto. Bigramas são pares de palavras consecutivas, 
enquanto trigramas são trios de palavras consecutivas.
"""

explicacao_caption = """
**Importante:** o pré-processamento inclui transformar todas as palavras para minúsculas, remover pontuações e caracteres especiais.
Portanto, palavras como "Jesus", "Deus", "Cristo" e "Senhor" serão tratadas como "jesus", "deus", "cristo" e "senhor", meramente
por questões de análise textual.
"""
st.caption(explicacao_caption)


# Gerar bigramas do corpus inteiro
def get_bigrams(tokens):
    return list(nltk.ngrams(tokens, 2))  # 2 = bigramas


# Gerar trigramas do corpus inteiro
def get_trigrams(tokens):
    return list(nltk.ngrams(tokens, 3))  # 3 = trigrams


# Gerar bigramas para todos os hinos
hinos_analise["bigrams"] = hinos_analise["tokens_no_stops"].apply(get_bigrams)

# Contar bigramas mais frequentes no corpus inteiro
all_bigrams = [bigram for hino in hinos_analise["bigrams"] for bigram in hino]
bigram_freq = Counter(all_bigrams)
bigram_print = pd.DataFrame(
    bigram_freq.most_common(10), columns=["Bigrama", "Frequência"]
)
bigram_print["Bigrama"] = bigram_print["Bigrama"].apply(lambda x: " ".join(x))

# Gerar trigrams para todos os hinos
hinos_analise["trigrams"] = hinos_analise["tokens_no_stops"].apply(get_trigrams)

# Contar trigrams mais frequentes no corpus inteiro
all_trigrams = [trigram for hino in hinos_analise["trigrams"] for trigram in hino]
trigram_freq = Counter(all_trigrams)
trigram_print = pd.DataFrame(
    trigram_freq.most_common(10), columns=["Trigrama", "Frequência"]
)
trigram_print["Trigrama"] = trigram_print["Trigrama"].apply(lambda x: " ".join(x))


col1, col2 = st.columns(2)
with col1:
    st.markdown("**Top 10 bigramas mais frequentes**")
    st.dataframe(
        bigram_print[["Bigrama", "Frequência"]]
        .sort_values("Frequência", ascending=False)
        .head(10),
        hide_index=True,
        column_config={
            "Frequência": st.column_config.ProgressColumn(
                "Frequência",
                format="%f",
                help="Frequência do bigrama",
                max_value=int(bigram_print["Frequência"].max()),
                width="small",
            ),
            "Bigrama": st.column_config.TextColumn(
                "Bigrama", width="small", max_chars=25
            ),
        },
    )


with col2:
    st.markdown("**Top 10 trigramas mais frequentes**")
    st.dataframe(
        trigram_print[["Trigrama", "Frequência"]]
        .sort_values("Frequência", ascending=False)
        .head(10),
        hide_index=True,
        column_config={
            "Frequência": st.column_config.ProgressColumn(
                "Frequência",
                format="%f",
                help="Frequência do trigrama",
                max_value=int(trigram_print["Frequência"].max()),
                width="small",
            ),
            "Trigrama": st.column_config.TextColumn(
                "Trigrama", width="small", max_chars=25
            ),
        },
    )


"""
Os bigramas e trigramas mais frequentes mostram sequências recorrentes e temas predominantes nos hinos. 
Por exemplo, a repetição de termos como "vem senhor jesus", "grande amor", ou combinações semelhantes, sugere que 
determinadas mensagens, expressões ou nomes são centrais para o repertório.

Os n-gramas mais comuns indicam fórmulas linguísticas típicas dos textos analisados, como nomes ou declarações 
de fé que se repetem, tornando-se uma "marca registrada" do gênero.
A alta recorrência dos mesmos bigramas e trigramas ("gloria" e "santo" como bigramas e trigramas) evidencia uma 
padronização linguística. Isso pode ser sinal de tradição, estilo de composição ou limitação temática dos textos analisados.

"""


# - Matriz de similaridade TF-IDF
"""
# Matriz de similaridade TF-IDF

Aqui, utilizamos a técnica de TF-IDF (Term Frequency-Inverse Document Frequency) para transformar os 
textos dos hinos em vetores numéricos, considerando de unigramas a trigramas. Em seguida, calculamos a 
similaridade entre esses vetores usando a similaridade do cosseno. A matriz resultante mostra o quão 
semelhantes são os hinos entre si com base no conteúdo textual. Valores próximos de 1 indicam alta 
similaridade, enquanto valores próximos de 0 indicam baixa similaridade.
"""


# Juntar os tokens em strings
hinos_analise["tokens_str"] = hinos_analise["tokens_no_stops"].apply(
    lambda t: " ".join(t)
)

# TF-IDF: unigrams e bigrams
vectorizer = TfidfVectorizer(ngram_range=(1, 3), stop_words=None)
X_tfidf = vectorizer.fit_transform(hinos_analise["tokens_str"])

similarity_tfidf = cosine_similarity(X_tfidf)
similarity_df_tfidf = pd.DataFrame(
    similarity_tfidf, index=hinos_analise.index, columns=hinos_analise.index
)

fig = px.imshow(
    similarity_df_tfidf,
    labels=dict(x="Hinos", y="Hinos", color="Similaridade"),
    # title="Matriz de Similaridade TF-IDF",
    width=600,
    height=600,
    color_continuous_scale="viridis",
)
st.plotly_chart(fig)

"""
É possível notar que muitos hinos apresentam baixa similaridade entre si, refletindo a diversidade temática e linguística
da coletânea. No entanto, há grupos de hinos com alta similaridade, sugerindo temas ou expressões comuns. 
Em especial, hinos das categorias "VOLTA DE JESUS E ETERNIDADE", "LOUVOR" e "SALMOS DE LOUVOR" parecem formar agrupamentos 
mais coesos. Também é perceptível alguma similaridade entre os hinos da categoria de "CLAMOR", possivelmente devido
a compartilharem expressões sobre o clamor pelo sangue de Jesus.
Esses agrupamentos podem indicar subtemas ou estilos compartilhados entre certos hinos, o que pode ser útil para análises 
mais aprofundadas sobre padrões de composição ou conteúdo.
"""


# - Ranking de termos mais relevantes

"""
# Hinos mais similares e termos mais relevantes

A seguir, é possível selecionar um hino específico para ver quais termos (unigramas, bigramas e trigramas)
são mais relevantes para ele, de acordo com os pesos TF-IDF calculados anteriormente.
"""


# mais similares
def most_similar_hymns(hymn_num, similarity_df, top_n=5):
    similar_scores = similarity_df[hymn_num].sort_values(ascending=False)
    similar_scores = similar_scores.drop(hymn_num)  # remove self-similarity
    top_similar = similar_scores.head(top_n)
    return top_similar


# top terms
def top_terms_for_hymn(row, features, top_n=5):
    row_data = list(zip(features, row))
    row_data = sorted(row_data, key=lambda x: x[1], reverse=True)
    return row_data[:top_n]


features = vectorizer.get_feature_names_out()

hymn_num = st.number_input(
    "Escolha o número de um hino:",
    min_value=int(hinos_analise.index.min()),
    max_value=int(hinos_analise.index.max()),
    value=521,
)

hymn_name = hinos_analise.loc[hymn_num, "nome"]
st.markdown(f"**🎵 Hino {hymn_num} — {hymn_name}:**")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Hinos mais similares**")
    top_similar = most_similar_hymns(hymn_num, similarity_df_tfidf, top_n=5)
    similar_rows = [
        {
            "Hino": int(idx),
            "Nome": hinos_analise.loc[idx, "nome"],
            "Similaridade": round(score, 3),
        }
        for idx, score in top_similar.items()
    ]
    if similar_rows:
        st.dataframe(pd.DataFrame(similar_rows).set_index("Hino"))

with col2:
    st.markdown("**Termos mais relevantes (TF-IDF)**")
    row = X_tfidf[hymn_num].toarray().ravel()
    top_terms = top_terms_for_hymn(row, features, top_n=5)
    df_top = pd.DataFrame(top_terms, columns=["Termo", "Score"])
    df_top["Score"] = df_top["Score"].round(3)
    st.dataframe(df_top, hide_index=True)
