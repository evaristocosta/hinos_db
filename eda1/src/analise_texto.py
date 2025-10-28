import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import altair as alt
from pipeline import hinos_processados


"""
# Exploração de palavras 🔡

Nesta seção, exploramos os textos dos hinos presentes na coletânea.

A primeira parte da análise foca no tamanho dos textos dos hinos, medido em número de palavras. Para 
essa análise, consideramos todas as palavras. Isso porque são textos de hinos, onde cada palavra
é cantada, o que influencia no tamanho percebido do hino.
"""

explicacao_filtros = """
Importante: as explicações deste texto se baseiam na coletânea como um todo, sem aplicação de filtros, já que estes
alteram os resultados ilustrados nos gráficos.
"""
st.caption(explicacao_filtros)

"""
As tabelas a seguir mostram os 10 hinos com maior e menor número de palavras, respectivamente.
"""


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


col1, col2 = st.columns(2)

with col1:
    st.markdown("**Top 10 maiores louvores**")

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
    st.markdown("**Top 10 menores louvores**")

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


"""
A diferença de quantidade de palavras entre os maiores hinos é pequena, com exceção do primeiro lugar -- Hino 459, 
com 72 palavras a mais que o segundo colocado. Entre os menores hinos, percebe-se pouca diferença entre os 10 primeiros. 
Interessantemente, o menor hino da coletânea, Hino 15, também contém 15 palavras, uma coincidência curiosa.

A análise continua com a visualização da relação entre o número de palavras e a categoria dos hinos.
"""

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
    # Boxplot com Altair + pontos sobrepostos
    # Garantir que todas as categorias apareçam no eixo X, com rotação de 90 graus
    categorias_todas = categoria_mapping.tolist()

    mean_tokens = float(hinos_analise["num_tokens"].mean())

    box = (
        alt.Chart(hinos_analise)
        .mark_boxplot()
        .encode(
            x=alt.X(
                "categoria_abr:N",
                title="Categoria",
                sort=categorias_todas,
                scale=alt.Scale(domain=categorias_todas),
                axis=alt.Axis(labelAngle=90),
            ),
            y=alt.Y("num_tokens:Q", title="Número de Palavras"),
        )
    )

    mean_df = pd.DataFrame({"mean": [mean_tokens]})

    # Linha pontilhada da média
    mean_rule = (
        alt.Chart(mean_df)
        .mark_rule(strokeDash=[6, 4], size=1)
        .encode(y=alt.Y("mean:Q"))
    )

    # Rótulo com o valor da média (colocado à esquerda da área do gráfico)
    mean_label = (
        alt.Chart(mean_df)
        .mark_text(align="left", dx=6, dy=-6)
        .encode(y=alt.Y("mean:Q"), text=alt.Text("mean:Q", format=".1f"))
        .encode(x=alt.value(0))
    )

    chart = (box + mean_rule + mean_label).properties(
        title="Relação Entre Número de Palavras e Categoria", width="container"
    )

    st.altair_chart(chart, use_container_width=True)


"""
A média de palavras por hino é de 100.5 palavras, indicada pela linha pontilhada 
azul no gráfico acima. Os hinos da categoria "GRUPO DE LOUVOR" são os que apresentam maior
média de palavras (116), enquanto que "CORINHOS" tem a menor média (45), muito embora 
tenha outliers que chegam a 261 palavras (Sequência de Louvores Nº 1). A categoria com maior
variação na quantia de palavras é a de "SANTIFICAÇÃO E DERRAMAMENTO DO ESPÍRITO SANTO", com
hinos de vão de 24 a 345 palavras, sendo este o maior hino da coletânea.

A seguir, pode pesquisar o número de palavras de um hino específico:

"""
col1, col2 = st.columns(2)
with col1:
    # pesquisa de numero de palavras por hino
    hymn_num = st.number_input(
        "Número do hino",
        min_value=int(hinos_analise.index.min()),
        max_value=int(hinos_analise.index.max()),
        value=int(hinos_analise.index.min()),
    )
with col2:
    hymn_title = hinos_analise.loc[hymn_num, "nome"]
    hymn_num_words = hinos_analise.loc[hymn_num, "num_tokens"]
    st.write(
        f"🎵 Hino {hymn_num} -- {hymn_title}:<br>**{hymn_num_words} palavras**",
        unsafe_allow_html=True,
    )

"""
Para prosseguir com a análise textual, precisamos realizar algumas etapas de 
pré-processamento nos dados. Isso inclui a *tokenização* e remoção de *stopwords*.

Uma breve explicação dos termos:
- **Tokenização**: processo de dividir o texto em unidades menores, chamadas tokens (geralmente palavras -- similar
ao que fizemos nas etapas anteriores).
- **Stopwords**: palavras comuns que geralmente não carregam muito significado (como "e", "o", "de" em português) 
e são removidas para focar nas palavras mais relevantes.
"""


# - Total de palavras únicas e mais longas
st.markdown("### Estatísticas de Vocabulário")
palavras = hinos_analise["tokens_no_stops"].explode().tolist()
palavras_unicas = list(set(palavras))
palavras_unicas.sort(key=len, reverse=True)

texto_se_filtro = (
    f" considerando as categorias selecionadas ({', '.join(categorias_selecionadas)}), "
    if categorias_selecionadas
    else ""
)
f"""
Na coletânea, {texto_se_filtro}existem um total de {len(palavras)} palavras, das quais {len(palavras_unicas)} 
são únicas, ou seja, aparecem apenas uma vez no conjunto de hinos.

As 10 maiores palavras são as seguintes:
"""


mais_longas = pd.DataFrame(
    {
        "palavra": palavras_unicas[:10],
        "tamanho": [len(palavra) for palavra in palavras_unicas[:10]],
    }
)

# Gráfico Altair das palavras mais longas
chart = (
    alt.Chart(mais_longas)
    .mark_bar()
    .encode(
        x=alt.X("tamanho:Q", title="Tamanho da palavra"),
        y=alt.Y(
            "palavra:N",
            sort=alt.EncodingSortField(field="tamanho", order="descending"),
            title="Palavra",
        ),
        tooltip=[
            alt.Tooltip("palavra:N", title="Palavra"),
            alt.Tooltip("tamanho:Q", title="Tamanho"),
        ],
    )
    .properties(title="Top 10 palavras mais longas", width="container", height=300)
)

st.altair_chart(chart, use_container_width=True)


# - Histograma de frequência de tamanhos
# Histograma interativo: distribuição do tamanho das palavras (tokens sem stopwords)
"""
Se analisarmos o tamanho das palavras (em número de caracteres), podemos observar a distribuição
desses tamanhos no histograma abaixo.
"""


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

    # Gráfico interativo com Plotly
    max_len = int(max(line_num_words)) if line_num_words else 1
    fig = px.histogram(
        df_lengths,
        x="length",
        nbins=max_len,
        # color_discrete_sequence=["#2a9d8f"],
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
        # annotation_text=f"Média: {media:.2f}",
        # annotation_position="top right",
    )
    fig.add_vline(
        x=mediana,
        line=dict(color="#264653", dash="dashdot"),
        # annotation_text=f"Mediana: {mediana:.0f}",
        # annotation_position="top right",
    )

    # Caixa de anotação com total e média
    fig.add_annotation(
        x=0.97,
        y=0.95,
        xref="paper",
        yref="paper",
        text=f"Média: {media:.2f}<br>Mediana: {mediana:.0f}",
        showarrow=False,
        align="right",
        # bgcolor="white",
        # bordercolor="black",
    )

    fig.update_layout(xaxis=dict(dtick=1), bargap=0.05)
    fig.update_xaxes(tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)


"""
Podemos notar que a maioria das palavras tem entre 3 e 7 caracteres, com picos em 5 e 6 caracteres.
"""

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
