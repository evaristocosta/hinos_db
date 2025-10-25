import streamlit as st
import nltk
import pandas as pd
from pipeline import hinos_processados
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import plotly.express as px

st.markdown("# Análise de palavras ✒️")

hinos_analise: pd.DataFrame = hinos_processados()


# - N-gramas
st.markdown("## N-gramas")


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
    st.markdown("### Top 10 bigramas mais frequentes")
    st.table(bigram_print)


with col2:
    st.markdown("### Top 10 trigramas mais frequentes")
    st.table(trigram_print)


# - Matriz de similaridade TF-IDF
# Juntar os tokens em strings
hinos_analise["tokens_str"] = hinos_analise["tokens_no_stops"].apply(
    lambda t: " ".join(t)
)

# TF-IDF: unigrams e bigrams
vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=None)
X_tfidf = vectorizer.fit_transform(hinos_analise["tokens_str"])

similarity_tfidf = cosine_similarity(X_tfidf)
similarity_df_tfidf = pd.DataFrame(
    similarity_tfidf, index=hinos_analise.index, columns=hinos_analise.index
)

st.markdown("## Matriz de similaridade TF-IDF")
fig = px.imshow(
    similarity_df_tfidf,
    labels=dict(x="Hinos", y="Hinos", color="Similaridade"),
    title="Matriz de Similaridade TF-IDF",
)
st.plotly_chart(fig)

# - Ranking de termos mais relevantes

st.markdown("## Ranking de termos mais relevantes (TF-IDF)")


def top_terms_for_hymn(row, features, top_n=5):
    row_data = list(zip(features, row))
    row_data = sorted(row_data, key=lambda x: x[1], reverse=True)
    return row_data[:top_n]


features = vectorizer.get_feature_names_out()
st.markdown("Escolha o número de um hino:")
hymn_num = st.number_input(
    "Número do hino",
    min_value=int(hinos_analise.index.min()),
    max_value=int(hinos_analise.index.max()),
    value=int(hinos_analise.index.min()),
)

row = X_tfidf[hymn_num].toarray().ravel()
top_terms = top_terms_for_hymn(row, features, top_n=5)
hymn_name = hinos_analise.loc[hymn_num, "nome"]
st.markdown(f"\n🎵 Hino {hymn_num} — {hymn_name}:")
for term, score in top_terms:
    st.markdown(f'-  "{term}": {score:.3f}')
