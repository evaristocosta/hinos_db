import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from pipeline import hinos_processados

st.markdown("# Exploração de palavras ✒️")
# st.sidebar.markdown("# Page 3 ❄️")


# Exploração dos textos (eda1_part3.1):
# - Tokenização, remoção de stopwords
# - 10 maiores e menores
# - Boxplot por categoria
# - Histograma de frequência de tamanhos
# - Total de palavras únicas e mais longas
# - Bag-of-words com plot
# - Wordcloud

hinos_analise: pd.DataFrame = hinos_processados()
# renomeia index para Nº
hinos_analise = hinos_analise.rename_axis("Nº")

# Filtros:
# - Categoria
# - Número
# - Nome
st.sidebar.header("Filtros")
categorias_unicas = hinos_analise["categoria_abr"].unique()
categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as categorias", options=categorias_unicas
)
if categorias_selecionadas:
    hinos_analise = hinos_analise[
        hinos_analise["categoria_abr"].isin(categorias_selecionadas)
    ]

# texto explicativo sobre stopwords e tokenização

# texto explicando tamanho dos tokens com stopwords pra dizer os maiores

col1, col2 = st.columns(2)

with col1:
    st.markdown("Top 10 maiores louvores")

    st.dataframe(
        hinos_analise[["nome", "num_tokens"]]
        .sort_values("num_tokens", ascending=False)
        .head(10),
        column_config={
            "num_tokens": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do hino em palavras",
                max_value=int(hinos_analise["num_tokens"].max()),
                width="small",
            ),
            "nome": st.column_config.TextColumn("Nome", width="small", max_chars=25),
        },
    )
with col2:
    st.markdown("Top 10 menores louvores")

    st.dataframe(
        hinos_analise[["nome", "num_tokens"]]
        .sort_values("num_tokens", ascending=True)
        .head(10),
        column_config={
            "num_tokens": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do hino em palavras",
                max_value=int(hinos_analise["num_tokens"].max()),
                width="small",
            ),
            "nome": st.column_config.TextColumn("Nome", width="small", max_chars=25),
        },
    )


# boxplot
# Garantir que 'categoria_id' é tratado como uma variável categórica
hinos_analise["categoria_id"] = hinos_analise["categoria_id"].astype("category")

# Criar um mapeamento entre categoria_id e categoria
categoria_mapping = (
    hinos_analise[["categoria_id", "categoria_abr"]]
    .drop_duplicates()
    .set_index("categoria_id")["categoria_abr"]
)


# Gráfico interativo com Plotly
# Criar coluna com rótulos amigáveis de categoria
hinos_analise["categoria_label"] = hinos_analise["categoria_id"].map(categoria_mapping)

if hinos_analise.empty:
    st.warning(
        "Nenhuma categoria selecionada ou não há dados para as categorias escolhidas."
    )
else:
    fig = px.box(
        hinos_analise,
        x="categoria_abr",
        y="num_tokens",
        points="all",
        hover_data=["nome"],
        labels={"categoria_abr": "Categoria", "num_tokens": "Número de Tokens"},
        title="Relação Entre Número de Tokens e Categoria (Box Plot)",
    )
    fig.update_layout(xaxis_tickangle=-45, boxmode="group")
    st.plotly_chart(fig, use_container_width=True)


# - Total de palavras únicas e mais longas
st.markdown("### Estatísticas de Vocabulário")
palavras = hinos_analise["tokens_no_stops"].explode().tolist()
st.write(f"**Total de palavras:** {len(palavras)}")
# find the 10 largest words
palavras_unicas = list(set(palavras))
palavras_unicas.sort(key=len, reverse=True)

st.write(f"**Total de palavras únicas:** {len(palavras_unicas)}")
mais_longas = pd.DataFrame(
    {
        "palavra": palavras_unicas[:10],
        "tamanho": [len(palavra) for palavra in palavras_unicas[:10]],
    }
)
st.markdown("#### 10 Palavras Mais Longas")
st.bar_chart(
    data=mais_longas,
    x="palavra",
    y="tamanho",
    y_label="Tamanho da palavra",
    x_label="Palavra",
    horizontal=True,
    sort=False,
    use_container_width=True,
)


# - Histograma de frequência de tamanhos
# Histograma interativo: distribuição do tamanho das palavras (tokens sem stopwords)


# Extrair tamanhos das palavras (tratando casos vazios)
palavras_explodidas = hinos_analise["tokens_no_stops"].explode().dropna().tolist()
line_num_words = [
    len(p) for p in palavras_explodidas if isinstance(p, str) and p.strip() != ""
]

if len(line_num_words) == 0:
    st.info("Sem dados para o histograma de tamanhos de palavras.")
else:
    # DataFrame para Plotly
    df_lengths = pd.DataFrame({"length": line_num_words})

    # Estatísticas
    media = np.mean(line_num_words)
    mediana = np.median(line_num_words)
    total = len(line_num_words)

    # Gráfico interativo com Plotly
    max_len = int(max(line_num_words)) if line_num_words else 1
    fig = px.histogram(
        df_lengths,
        x="length",
        nbins=max_len,
        color_discrete_sequence=["#2a9d8f"],
        title="Distribuição dos tamanhos das palavras (tokens sem stopwords)",
        labels={
            "length": "Tamanho da palavra (número de caracteres)",
            "count": "Frequência",
        },
    )

    # Linhas de média e mediana
    fig.add_vline(
        x=media,
        line=dict(color="#e76f51", dash="dash"),
        annotation_text=f"Média: {media:.2f}",
        annotation_position="top right",
    )
    fig.add_vline(
        x=mediana,
        line=dict(color="#264653", dash="dashdot"),
        annotation_text=f"Mediana: {mediana:.0f}",
        annotation_position="top right",
    )

    # Caixa de anotação com total e média
    fig.add_annotation(
        x=0.97,
        y=0.95,
        xref="paper",
        yref="paper",
        text=f"Total palavras: {total}<br>Média: {media:.2f}",
        showarrow=False,
        align="right",
        # bgcolor="white",
        bordercolor="black",
    )

    fig.update_layout(xaxis=dict(dtick=1), bargap=0.05)
    fig.update_xaxes(tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)


# - Bag-of-words com plot
set_words_full = list(set(palavras))
count_words = [palavras.count(i) for i in set_words_full]

contagem_palav = pd.DataFrame(
    zip(set_words_full, count_words), columns=["palavra", "contagem"]
)
contagem_palav = contagem_palav.sort_values("contagem", ascending=False)
contagem_palav["percentual"] = contagem_palav["contagem"] / len(palavras) * 100

st.markdown("### Bag-of-Words")
st.markdown("#### Top 20 palavras mais frequentes (sem stopwords)")
st.bar_chart(
    contagem_palav.head(20),
    x="palavra",
    y="contagem",
    x_label="Palavra",
    y_label="Contagem",
    horizontal=True,
    sort=False,
    use_container_width=True,
)

# - Wordcloud
st.markdown("### Wordcloud")
word_freq_dict = dict(zip(contagem_palav["palavra"], contagem_palav["contagem"]))

from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    max_words=100,
    colormap="viridis",
    relative_scaling=0.5,
    random_state=42,
).generate_from_frequencies(word_freq_dict)

# Plot the word cloud (Streamlit-friendly)
fig, ax = plt.subplots(figsize=(12, 6))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
ax.set_title("Word Cloud - Palavras mais frequentes nos hinos", fontsize=16, pad=20)
plt.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)
