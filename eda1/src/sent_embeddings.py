import streamlit as st
import pandas as pd
from pipeline import hinos_processados, similarity_matrices
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import numpy as np

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


# modelo = SentenceTransformer("rufimelo/Legal-BERTimbau-sts-base")  # português brasileiro
# similaridade = cosine_similarity

"""
# Matriz de Similaridade entre Hinos

Como na análise de embeddings de palavras, aqui apresentamos a matriz de similaridade entre os hinos,
mas agora utilizando os embeddings de frases. 

Para gerar os embeddings de frases, utilizamos o modelo "[rufimelo/Legal-BERTimbau-sts-base](https://huggingface.co/rufimelo/Legal-BERTimbau-sts-base)", 
que é baseado na arquitetura BERT e foi ajustado para tarefas de similaridade semântica em português brasileiro.
A similaridade por sua vez, é calculada usando a similaridade do cosseno.

"""

fig = px.imshow(
    similarity_sentence,
    labels=dict(x="Hinos", y="Hinos", color="Similaridade"),
    width=600,
    height=600,
    color_continuous_scale="Viridis",
)
st.plotly_chart(fig)

"""
Comparando com a matriz de similaridade baseada em embeddings de palavras, podemos observar que a matriz
de embeddings de frases tende a apresentar valores de similaridade mais altos entre os hinos. Isso ocorre porque os 
embeddings de frases capturam o contexto completo das frases, levando em consideração a estrutura e o significado 
global, enquanto os embeddings de palavras focam em palavras individuais.
Essa característica dos embeddings de frases permite identificar similaridades semânticas mais profundas entre os 
hinos, mesmo quando eles utilizam palavras diferentes para expressar ideias semelhantes.

O que chama atenção, pela análise visual da matriz, são algumas linhas e colunas mais claras, indicando hinos que
não compartilham muita similaridade com os demais, como o hino 396 - "Abba Pai", ou 13 - "Vamos lavar as vestes". 
Esses hinos podem ser considerados mais únicos em termos de conteúdo e estilo, destacando-se na coleção.
A região dos corinhos (maiores que 731) também se destaca, mostrando hinos de menor similaridade com os demais, e
mesmo entre eles. De fato, são hinos característicos, com estruturas e temas próprios, o que justifica sua menor 
similaridade. O mesmo acontece com alguns hinos de clamor, e de invocação. No entanto, a faixa que mais chama atenção
é o intervalo entre os hinos 396 e 403, que apresentam uma similaridade muito baixa com o restante dos hinos. Um
fator que pode ser determinante, é que esses hinos são mais curtos, com menos versos, o que pode influenciar
na geração dos embeddings e na similaridade calculada.
"""


"""
## Relação de tamanho do hino e similaridade

Aqui, investigamos se existe alguma correlação entre o tamanho dos hinos (medido pelo número de tokens)
e a similaridade média com os demais hinos, utilizando os embeddings de frases.
"""


# restringe a matriz de similaridade aos hinos atualmente no dataframe (caso haja filtro)
idx = hinos_analise.index.tolist()
sim_sub = similarity_sentence.loc[idx, idx]

# média de similaridade com os demais (exclui a diagonal / self-similarity)
n = sim_sub.shape[0]
if n > 1:
    mean_sim = (sim_sub.sum(axis=1) - np.diag(sim_sub).astype(float)) / (n - 1)
else:
    mean_sim = pd.Series(0.0, index=sim_sub.index)


# conta número de tokens (compatível com listas ou strings)
def _count_tokens(x):
    try:
        return len(x)
    except Exception:
        if pd.isna(x):
            return 0
        return len(str(x).split())


size_series = hinos_analise["tokens_no_stops"].apply(_count_tokens)

plot_df = pd.DataFrame(
    {
        "hino": hinos_analise.index,
        "nome": hinos_analise["nome"],
        "tamanho": size_series,
        "similaridade_media": mean_sim.loc[hinos_analise.index].astype(float),
    }
).reset_index(drop=True)

# calcula correlação e ajuste linear
mask = np.isfinite(plot_df["tamanho"]) & np.isfinite(plot_df["similaridade_media"])
corr = np.corrcoef(
    plot_df.loc[mask, "tamanho"], plot_df.loc[mask, "similaridade_media"]
)[0, 1]
# reg_slope, reg_intercept = np.polyfit(
#     plot_df.loc[mask, "tamanho"], plot_df.loc[mask, "similaridade_media"], 1
# )

# scatter + linha de regressão
fig = px.scatter(
    plot_df,
    x="tamanho",
    y="similaridade_media",
    hover_data=["hino", "nome"],
    labels={
        "tamanho": "Número de tokens (tamanho do hino)",
        "similaridade_media": "Similaridade média",
    },
    title="Relação entre tamanho do hino e similaridade média",
    width=700,
    height=450,
)

# x_line = np.linspace(plot_df["tamanho"].min(), plot_df["tamanho"].max(), 100)
# y_line = reg_slope * x_line + reg_intercept
# fig.add_trace(
#     go.Scatter(
#         x=x_line,
#         y=y_line,
#         mode="lines",
#         name="Regressão linear",
#         line=dict(color="red"),
#     )
# )

st.plotly_chart(fig)


f"""
Fica claro que a afirmação anterior sobre hinos mais curtos terem menor similaridade se confirma aqui. Embora existam hinos
com baixo número de tokens que apresentam similaridade média alta, a tendência geral indica que hinos mais curtos tendem a ter
menor similaridade média com os demais hinos. Isso pode ser atribuído ao fato de que hinos mais curtos possuem menos conteúdo
semântico para capturar, o que pode resultar em embeddings menos informativos e, consequentemente, em menor similaridade 
com outros hinos.

A **Correlação (Pearson)** entre tamanho e similaridade média é igual a {corr:.3f}.
Isso indica uma correlação positiva moderada, sugerindo que, em geral, hinos maiores tendem a ter similaridade média mais alta
com os demais hinos, embora existam exceções individuais.
"""


# mostra amostra dos valores
# st.dataframe(plot_df.sort_values("tamanho").head(10).set_index("hino"))


"""
## Hinos mais semelhantes

Usando os dados de similaridade, a seguir você pode selecionar um hino para ver os mais semelhantes com base 
nos embeddings de sentenças.
"""

col1, col2 = st.columns(2)
with col1:
    hymn_num = st.number_input(
        "Selecione o número do hino:",
        min_value=int(hinos_analise.index.min()),
        max_value=int(hinos_analise.index.max()),
        value=495,  # um bom exemplo pra iniciar
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

Assim como na análise de embeddings de palavras, aplicamos técnicas de redução de dimensionalidade (UMAP)
e clustering (K-Means) para visualizar e agrupar os hinos com base em seus embeddings de frases. Levando em conta
resultados da análise de silhueta, optamos por 9 clusters para os embeddings de frases.
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
Na análise anterior, podíamos observar alguns hinos bem isolados em termos de similaridade. Aqui, vemos um agrupamento
mais coeso, com menos pontos isolados. Isso sugere que os embeddings de frases capturam melhor as semelhanças semânticas 
entre os hinos, permitindo uma formação de clusters mais definida.
"""


"""
## Termos mais frequentes por cluster

"""


rows = []
for c in sorted(hinos_analise["sent_cluster"].unique()):
    cluster_tokens = hinos_analise.loc[
        hinos_analise["sent_cluster"] == c, "tokens_no_stops"
    ].sum()
    top_terms = [t for t, _ in Counter(cluster_tokens).most_common(8)]
    cluster_series = hinos_analise.loc[hinos_analise["sent_cluster"] == c, "nome"]
    sampled = cluster_series.sample(n=min(3, cluster_series.shape[0]))
    top_hymns = [f"{idx} - {name}" for idx, name in sampled.items()]
    rows.append(
        {
            "Cluster": c,
            "Top termos": ", ".join(top_terms),
            "Top hinos": " | ".join(top_hymns),
        }
    )

df_terms = pd.DataFrame(rows).set_index("Cluster")
st.dataframe(df_terms)


# ## Relação entre Clusters e Categorias da Coletânea
st.subheader("Relação entre Clusters e Categorias da Coletânea")

# tabela de contingência: categorias x clusters
ct = pd.crosstab(
    hinos_analise["categoria_abr"], hinos_analise["sent_cluster"]
).sort_index()

# Heatmap (proporções por categoria) com anotações dentro dos quadrados
ct_counts = ct.copy()
ct_prop = ct_counts.div(
    ct_counts.sum(axis=1), axis=0
)  # normaliza por categoria (linha)
ct_prop_pct = ct_prop * 100  # em porcentagem

x = ct.index.tolist()  # categorias
y = [str(c) for c in ct.columns]  # clusters (string para rótulos)

fig_ct = px.imshow(
    ct_prop_pct.T.values,
    x=x,
    y=y,
    labels={
        "x": "Categoria da Coletânea",
        "y": "Cluster (sent_cluster)",
        "color": "Proporção (%)",
    },
    color_continuous_scale="Viridis",
    width=800,
    height=420,
)

# adicionar anotações com porcentagem e contagem
z = ct_prop_pct.T.values
counts = ct_counts.T.values
z_max = z.max() if z.size else 0
for i_y, y_label in enumerate(y):
    for i_x, x_label in enumerate(x):
        val_pct = z[i_y, i_x]
        cnt = int(counts[i_y, i_x])
        text = f"{val_pct:.1f}%\n({cnt})"
        # escolha de cor do texto para legibilidade
        text_color = "white" if val_pct > (z_max / 2 if z_max > 0 else 0.5) else "black"
        fig_ct.add_annotation(
            x=x_label,
            y=y_label,
            text=text,
            showarrow=False,
            font=dict(color=text_color, size=11),
            xanchor="center",
            yanchor="middle",
        )

fig_ct.update_layout(margin=dict(l=40, r=40, t=40, b=40))
st.plotly_chart(fig_ct)

# Stacked bar (proporção por categoria) — mostra composição de clusters dentro de cada categoria
# index_name = ct.index.name or "categoria_abr"
# ct_pct = (
#     ct.div(ct.sum(axis=1), axis=0)
#     .reset_index()
#     .melt(id_vars=index_name, var_name="Cluster", value_name="Proporção")
# )
# fig_bar = px.bar(
#     ct_pct,
#     x=index_name,
#     y="Proporção",
#     color="Cluster",
#     barmode="stack",
#     labels={
#         index_name: "Categoria da Coletânea",
#         "Proporção": "Proporção por Categoria",
#     },
#     width=800,
#     height=420,
# )
# fig_bar.update_layout(xaxis={"categoryorder": "array", "categoryarray": ct.index})
# st.plotly_chart(fig_bar)

# # Mostrar tabelas auxiliares (contagens e proporções)
# st.markdown("Contagens (Categoria × Cluster)")
# st.dataframe(ct)

# st.markdown("Proporções por Categoria (normalizado por categoria)")
# st.dataframe(ct.div(ct.sum(axis=1), axis=0).round(3))


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
