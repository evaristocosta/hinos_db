import streamlit as st
import pandas as pd
from pipeline import hinos_processados
import plotly.express as px
import numpy as np

# Emoções (eda1_part7):
st.title("Análise de emoções nos hinos 🎭")

hinos_analise: pd.DataFrame = hinos_processados()

# modelo usado: https://huggingface.co/pysentimiento/bert-pt-emotion
"""
Nesta página, exploramos as emoções expressas nos hinos utilizando análises quantitativas e 
visuais. As emoções foram classificadas usando o modelo [bert-pt-emotion](https://huggingface.co/pysentimiento/bert-pt-emotion), 
um modelo de  processamento de linguagem natural treinado para reconhecer emoções em textos 
em português. As principais emoções analisadas incluem alegria, tristeza, otimismo, luto,
entre outras.
"""



# top 10 emoções dominantes nos hinos (sem 'neutral')

"""
# Distribuição das emoções dominantes

No gráfico abaixo, visualizamos as 10 emoções dominantes mais frequentes nos hinos, 
excluindo a categoria 'neutral' (neutra). Isso nos ajuda a entender quais emoções são mais 
prevalentes na coletânea.
"""

st.caption("""
    Observação: o nome das emoções está em inglês por padrão, por conta do modelo utilizado.
""")

emocao_counts = pd.Series(hinos_analise["emocao_dominante_sem_neutral"].tolist()).value_counts().head(10)

# Calcular porcentagens
total_hinos = len(hinos_analise)
emocao_df = pd.DataFrame({
    'emocao': emocao_counts.index,
    'contagem': emocao_counts.values,
    'percentual': (emocao_counts.values / total_hinos * 100).round(2)
})

fig_bar = px.bar(
    emocao_df,
    x='contagem',
    y='emocao',
    orientation='h',
    labels={'contagem': 'Número de hinos', 'emocao': 'Emoção'},
    custom_data=['percentual'],
)

fig_bar.update_traces(
    hovertemplate='<b>%{y}</b><br>Contagem: %{x}<br>Percentual: %{customdata[0]:.2f}%<extra></extra>'
)

fig_bar.update_layout(
    height=400,
    yaxis={'categoryorder': 'total ascending'}
)

st.plotly_chart(fig_bar, use_container_width=True)

"""
Quase metade dos hinos expressam "amor", e quase um quarto expressam "otimismo", sendo essas
as emoções mais marcantes nos hinos analisados. Além disso, as oito primeiras emoções são positivas,
indicando uma tendência geral de otimismo e alegria na coletânea.
"""

# matriz de correlação
"""
## Matriz de correlação entre emoções

Como análise continuada, exploramos a correlação entre diferentes emoções expressas nos hinos. 
A matriz de correlação abaixo mostra como as emoções se relacionam entre si, indicando quais
emoções tendem a aparecer juntas nos hinos.
"""

emocoes_por_hino = []
for emocoes in hinos_analise["emocoes"]:
    if emocoes:
        emocoes_por_hino.append(emocoes)
    else:
        emocoes_por_hino.append({})

emo_df_completo = pd.DataFrame(emocoes_por_hino).fillna(0)

# Matriz de correlação entre emoções
correlacao_emocoes = emo_df_completo.corr()

# Visualizar matriz de correlação com Plotly

# Criar máscara para triângulo superior
mask = np.triu(np.ones_like(correlacao_emocoes, dtype=bool))
correlacao_masked = correlacao_emocoes.copy()
correlacao_masked = correlacao_masked.where(~mask)

# Criar matriz de texto, substituindo NaN por strings vazias
texto_correlacao = correlacao_masked.round(2).astype(str)
texto_correlacao = texto_correlacao.replace('nan', '')

fig_corr = px.imshow(
    correlacao_masked,
    color_continuous_scale='RdBu_r',
    color_continuous_midpoint=0,
    aspect='auto',
    labels=dict(color="Correlação"),
    # title="Matriz de Correlação entre Emoções<br>(Como as emoções se relacionam entre si)"
)
fig_corr.update_traces(text=texto_correlacao, texttemplate='%{text}')
fig_corr.update_layout(height=700)
st.plotly_chart(fig_corr, use_container_width=True)

"""
Quatro correlações notáveis emergem da análise: tristeza ("sadness") e luto ("grief") estão 
fortemente correlacionados -- a maior correlação observada -- sugerindo que hinos que 
expressam tristeza frequentemente também abordam temas de perda e luto. Segundo, confusão ("confusion")
e curiosidade ("curiosity") mostram uma correlação positiva significativa, seguido de
alegria ("joy") e alívio ("relief"), e medo ("fear") com nervosismo ("nervousness").

É possível notar algumas linhas também, indicando que certas emoções têm correlações mais fortes,
ou inversas entre si. É o caso de embaraço ("embarrassment"), que tem correlações positivas
com várias emoções negativas. Por outro lado, a emoção neutra ("neutral") mostra correlações
inversas com várias emoções, principalmente amor ("love") -- a emoção mais presente
nos hinos -- indicando que hinos neutros tendem a evitar expressar emoções fortes.
"""

# diversidade (shannon, concentração, exemplos)
"""
# Diversidade emocional nos hinos
"""

st.write("**Estatísticas de Diversidade Emocional**")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Entropia média", f"{hinos_analise['diversidade_emocional'].mean():.3f}")
with col2:
    st.metric("Entropia mínima", f"{hinos_analise['diversidade_emocional'].min():.3f}")
with col3:
    st.metric("Entropia máxima", f"{hinos_analise['diversidade_emocional'].max():.3f}")
with col4:
    st.metric("Concentração média", f"{hinos_analise['concentracao_emocional'].mean():.3f}")

# Visualizar distribuição
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Distribuição da Diversidade Emocional<br>(Entropia de Shannon)",
                    "Distribuição da Concentração Emocional<br>(Score máximo / Total)")
)

# Histograma de diversidade
fig.add_trace(
    go.Histogram(x=hinos_analise["diversidade_emocional"], nbinsx=30, 
                 marker_color='teal', opacity=0.7, name='Diversidade'),
    row=1, col=1
)
# Linha vertical da média
media_div = hinos_analise["diversidade_emocional"].mean()
fig.add_vline(x=media_div, line_dash="dash", line_color="red", 
              annotation_text=f"Média: {media_div:.3f}", row=1, col=1)

# Histograma de concentração
fig.add_trace(
    go.Histogram(x=hinos_analise["concentracao_emocional"], nbinsx=30,
                 marker_color='coral', opacity=0.7, name='Concentração'),
    row=1, col=2
)
# Linha vertical da média
media_conc = hinos_analise["concentracao_emocional"].mean()
fig.add_vline(x=media_conc, line_dash="dash", line_color="red",
              annotation_text=f"Média: {media_conc:.3f}", row=1, col=2)

fig.update_xaxes(title_text="Entropia", row=1, col=1)
fig.update_xaxes(title_text="Índice de Concentração", row=1, col=2)
fig.update_yaxes(title_text="Frequência", row=1, col=1)
fig.update_yaxes(title_text="Frequência", row=1, col=2)
fig.update_layout(height=500, showlegend=False)

st.plotly_chart(fig, use_container_width=True)

# Exemplos de hinos mais diversos vs. mais concentrados
st.write("### Hinos Mais DIVERSOS Emocionalmente (múltiplas emoções balanceadas)")
mais_diversos = hinos_analise.nlargest(5, "diversidade_emocional")
for i, row in enumerate(mais_diversos.iterrows(), 1):
    idx, hino = row
    st.write(f"**{i}. {hino['nome']}**")
    st.write(f"   Entropia: {hino['diversidade_emocional']:.3f}")
    if hino['emocoes']:
        top_3 = sorted(hino['emocoes'].items(), key=lambda x: x[1], reverse=True)[:3]
        st.write(f"   Top 3 emoções: {', '.join([f'{e[0]}({e[1]:.2f})' for e in top_3])}")

st.write("### Hinos Mais CONCENTRADOS Emocionalmente (emoção dominante forte)")
mais_concentrados = hinos_analise.nlargest(5, "concentracao_emocional")
for i, row in enumerate(mais_concentrados.iterrows(), 1):
    idx, hino = row
    st.write(f"**{i}. {hino['nome']}**")
    st.write(f"   Concentração: {hino['concentracao_emocional']:.3f}")
    if hino['emocoes']:
        top_emocao = max(hino['emocoes'].items(), key=lambda x: x[1])
        st.write(f"   Emoção dominante: {top_emocao[0]} ({top_emocao[1]:.3f})")


# distribuição de categorias emocionais
"""
# Distribuição das categorias emocionais nos hinos

"""
categoria_counts = hinos_analise['categoria_dominante'].value_counts()

col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(
        values=categoria_counts.values,
        names=categoria_counts.index,
        title="Distribuição de Categorias Emocionais",
        color_discrete_sequence=['lightgreen', 'lightcoral', 'lightgray']
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Relação entre positivas e negativas
"""
# Relação entre emoções positivas e negativas nos hinos
"""
with col2:
    fig_scatter = px.scatter(
        hinos_analise,
        x='score_positivas',
        y='score_negativas',
        color='score_neutras',
        color_continuous_scale='viridis',
        opacity=0.5,
        title='Relação entre Emoções Positivas e Negativas<br>(cor = score neutro)',
        labels={
            'score_positivas': 'Score Emoções Positivas',
            'score_negativas': 'Score Emoções Negativas',
            'score_neutras': 'Score Neutro'
        }
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

# Valência emocional geral (positivas - negativas)
st.write(f"**Valência emocional média:** {hinos_analise['valencia_emocional'].mean():.3f}")
st.caption("(Valores positivos = mais alegre/positivo, negativos = mais triste/negativo)")

# casos extremos
"""
# Casos extremos 
"""
emocoes_principais = hinos_analise['emocao_dominante_sem_neutral'].value_counts().head(8).index

for emocao in emocoes_principais:
    st.write(f"### EMOÇÃO: {emocao.upper()}")
    
    # Criar coluna temporária com score dessa emoção
    hinos_analise[f'score_{emocao}_temp'] = hinos_analise['emocoes'].apply(
        lambda x: x.get(emocao, 0.0) if x else 0.0
    )
    
    top_hinos = hinos_analise.nlargest(3, f'score_{emocao}_temp')
    
    for i, row in enumerate(top_hinos.iterrows(), 1):
        idx, hino = row
        st.write(f"**{i}. {hino['nome']}**")
        st.write(f"   Score {emocao}: {hino[f'score_{emocao}_temp']:.3f}")
        st.write(f"   Categoria: {hino['categoria_dominante']} | Score líquido: {hino['score_liquido']:.3f}")
    
    # Limpar coluna temporária
    hinos_analise.drop(columns=[f'score_{emocao}_temp'], inplace=True)


# Calcular distância do perfil emocional médio
from scipy.spatial.distance import euclidean
import numpy as np

# Criar vetor de emoções médias
emocoes_todas = set()
for emocoes in hinos_analise["emocoes"]:
    if emocoes:
        emocoes_todas.update(emocoes.keys())

vetor_medio = {}
for emocao in emocoes_todas:
    scores = [e.get(emocao, 0.0) for e in hinos_analise["emocoes"] if e]
    vetor_medio[emocao] = np.mean(scores) if scores else 0.0

# Calcular distância euclidiana de cada hino para a média
def calcular_distancia_media(emocoes):
    if not emocoes:
        return 0.0
    vetor_hino = [emocoes.get(emocao, 0.0) for emocao in sorted(vetor_medio.keys())]
    vetor_medio_sorted = [vetor_medio[emocao] for emocao in sorted(vetor_medio.keys())]
    return euclidean(vetor_hino, vetor_medio_sorted)

hinos_analise['distancia_perfil_medio'] = hinos_analise['emocoes'].apply(calcular_distancia_media)

st.write("### Hinos MAIS ATÍPICOS (perfil emocional único)")
mais_atipicos = hinos_analise.nlargest(5, 'distancia_perfil_medio')

for i, row in enumerate(mais_atipicos.iterrows(), 1):
    idx, hino = row
    st.write(f"**{i}. {hino['nome']}**")
    st.write(f"   Distância do perfil médio: {hino['distancia_perfil_medio']:.3f}")
    st.write(f"   Emoção dominante: {hino['emocao_dominante_sem_neutral']}")
    st.write(f"   Categoria: {hino['categoria_dominante']}")
    
    if hino['emocoes']:
        top_3 = sorted(hino['emocoes'].items(), key=lambda x: x[1], reverse=True)[:3]
        st.write(f"   Top 3 emoções: {', '.join([f'{e[0]}({e[1]:.2f})' for e in top_3])}")


st.write("### Hinos MAIS TÍPICOS (perfil emocional comum)")
mais_tipicos = hinos_analise.nsmallest(5, 'distancia_perfil_medio')

for i, row in enumerate(mais_tipicos.iterrows(), 1):
    idx, hino = row
    st.write(f"**{i}. {hino['nome']}**")
    st.write(f"   Distância do perfil médio: {hino['distancia_perfil_medio']:.3f}")
    st.write(f"   Emoção dominante: {hino['emocao_dominante_sem_neutral']}")
    st.write(f"   Categoria: {hino['categoria_dominante']}")



st.write("### Hinos MAIS NEGATIVOS")
hinos_negativos = hinos_analise.nlargest(3, 'score_negativas')

for i, row in enumerate(hinos_negativos.iterrows(), 1):
    idx, hino = row
    st.write(f"**{i}. {hino['nome']}**")
    st.write(f"   Score negativas: {hino['score_negativas']:.3f}")
    st.write(f"   Emoção dominante: {hino['emocao_dominante_sem_neutral']}")

st.write("### Hinos com PERFIL MAIS BALANCEADO (múltiplas emoções fortes)")
# Esses são os com maior diversidade mas baixa concentração
hinos_balanceados = hinos_analise.nsmallest(3, 'concentracao_emocional')

for i, row in enumerate(hinos_balanceados.iterrows(), 1):
    idx, hino = row
    st.write(f"**{i}. {hino['nome']}**")
    st.write(f"   Concentração: {hino['concentracao_emocional']:.3f} (baixo = balanceado)")
    st.write(f"   Diversidade: {hino['diversidade_emocional']:.3f}")
    
    if hino['emocoes']:
        top_5 = sorted(hino['emocoes'].items(), key=lambda x: x[1], reverse=True)[:5]
        st.write(f"   Top 5 emoções: {', '.join([f'{e[0]}({e[1]:.2f})' for e in top_5])}")



# distribuição da intensidade emocional
# distribuição da complexidade emocional
# relação entre valência e intensidade

"""
# Intensidade e Complexidade Emocional
"""

fig2 = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Distribuição da Intensidade Emocional<br>(Soma das emoções não-neutras)",
        "Distribuição da Complexidade Emocional<br>(Número de emoções fortes)",
        "",
        "Relação entre Valência e Intensidade<br>(cor = diversidade)"
    ),
    specs=[[{"type": "histogram"}, {"type": "histogram"}],
           [{"type": "xy"}, {"type": "scatter"}]]
)

# 1. Intensidade emocional
media_int = hinos_analise['intensidade_emocional'].mean()
fig2.add_trace(
    go.Histogram(x=hinos_analise['intensidade_emocional'], nbinsx=30,
                 marker_color='orange', opacity=0.7, name='Intensidade'),
    row=1, col=1
)
fig2.add_vline(x=media_int, line_dash="dash", line_color="red",
               annotation_text=f"Média: {media_int:.3f}", row=1, col=1)

# 2. Número de emoções fortes
media_num = hinos_analise['num_emocoes_fortes'].mean()
fig2.add_trace(
    go.Histogram(x=hinos_analise['num_emocoes_fortes'],
                 marker_color='purple', opacity=0.7, name='Complexidade'),
    row=1, col=2
)
fig2.add_vline(x=media_num, line_dash="dash", line_color="red",
               annotation_text=f"Média: {media_num:.1f}", row=1, col=2)

# 3. Scatter: valencia vs intensidade
fig2.add_trace(
    go.Scatter(
        x=hinos_analise['valencia_emocional'],
        y=hinos_analise['intensidade_emocional'],
        mode='markers',
        marker=dict(
            color=hinos_analise['diversidade_emocional'],
            colorscale='viridis',
            opacity=0.6,
            showscale=True,
            colorbar=dict(title="Diversidade", x=1.15)
        ),
        name='Hinos'
    ),
    row=2, col=2
)
fig2.add_vline(x=0, line_dash="dash", line_color="black", opacity=0.5, row=2, col=2)

fig2.update_xaxes(title_text="Intensidade", row=1, col=1)
fig2.update_xaxes(title_text="Número de Emoções (score ≥ 0.1)", row=1, col=2)
fig2.update_xaxes(title_text="Valência Emocional (positivas - negativas)", row=2, col=2)
fig2.update_yaxes(title_text="Frequência", row=1, col=1)
fig2.update_yaxes(title_text="Frequência", row=1, col=2)
fig2.update_yaxes(title_text="Intensidade Emocional (soma não-neutras)", row=2, col=2)

fig2.update_layout(height=800, showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

# Rankings - Top Hinos por Diferentes Métricas
"""
# Rankings - Top Hinos por Diferentes Métricas
"""

col1, col2 = st.columns(2)

with col1:
    st.write("### TOP 10 HINOS MAIS ALEGRES")
    top_alegres = hinos_analise.nlargest(10, 'alegria_liquida')[['nome', 'alegria_liquida']]
    top_alegres['rank'] = range(1, len(top_alegres) + 1)
    st.dataframe(top_alegres[['rank', 'nome', 'alegria_liquida']], hide_index=True, use_container_width=True)

with col2:
    st.write("### TOP 10 HINOS MAIS TRISTES")
    top_tristes = hinos_analise.nsmallest(10, 'alegria_liquida')[['nome', 'alegria_liquida']]
    top_tristes['rank'] = range(1, len(top_tristes) + 1)
    st.dataframe(top_tristes[['rank', 'nome', 'alegria_liquida']], hide_index=True, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.write("### TOP 10 HINOS MAIS INTENSOS")
    top_intensos = hinos_analise.nlargest(10, 'intensidade_emocional')[['nome', 'intensidade_emocional']]
    top_intensos['rank'] = range(1, len(top_intensos) + 1)
    st.dataframe(top_intensos[['rank', 'nome', 'intensidade_emocional']], hide_index=True, use_container_width=True)

with col4:
    st.write("### TOP 10 HINOS MAIS COMPLEXOS")
    top_complexos = hinos_analise.nlargest(10, 'num_emocoes_fortes')[['nome', 'num_emocoes_fortes']]
    top_complexos['rank'] = range(1, len(top_complexos) + 1)
    st.dataframe(top_complexos[['rank', 'nome', 'num_emocoes_fortes']], hide_index=True, use_container_width=True)

st.write("### TOP 10 HINOS MAIS POSITIVOS (maior valência)")
top_positivos = hinos_analise.nlargest(10, 'valencia_emocional')[['nome', 'valencia_emocional']]
top_positivos['rank'] = range(1, len(top_positivos) + 1)
st.dataframe(top_positivos[['rank', 'nome', 'valencia_emocional']], hide_index=True, use_container_width=True)

# resumo emocional
"""
# Resumo Emocional da Coletânea
"""

top_emocoes_geral = hinos_analise['emocao_dominante_sem_neutral'].value_counts().head(5)
cat_dist = hinos_analise['categoria_dominante'].value_counts()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de hinos", len(hinos_analise))
    st.metric("Valência média", f"{hinos_analise['valencia_emocional'].mean():.3f}",
              delta="POSITIVA" if hinos_analise['valencia_emocional'].mean() > 0 else "NEGATIVA")
with col2:
    st.metric("Intensidade média", f"{hinos_analise['intensidade_emocional'].mean():.3f}")
    st.metric("Diversidade média", f"{hinos_analise['diversidade_emocional'].mean():.3f}")
with col3:
    st.metric("Categoria mais comum", f"{cat_dist.index[0].upper()}", delta=f"{cat_dist.iloc[0]} hinos")
    st.metric("Emoção mais comum", f"{top_emocoes_geral.index[0].upper()}", delta=f"{top_emocoes_geral.iloc[0]} hinos")


# - Pesquisa de hinos e mostrar emoções
"""
# Pesquisa de hinos por emoções

"""
