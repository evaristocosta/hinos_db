import streamlit as st


st.set_page_config(page_title="EDA da Coletânea", layout="wide")

st.markdown(
    """
    <style>
        /* Corpo geral */
        .main {
            background-color: #ffffff;
            font-family: 'Times New Roman', 'Georgia', serif;
            color: #1c1c1c;
            line-height: 1.6;
        }
        /* Títulos */
        h1, h2, h3 {
            color: #2E5A87;
            font-weight: 600;
        }
        /* Cards e caixas */
        .stMarkdown, .stDataFrame, .stPlotlyChart {
            border-radius: 8px;
            background-color: #f7f9fb;
            padding: 10px 15px;
            box-shadow: 0 0 4px rgba(0,0,0,0.05);
        }
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #f0f3f7;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# Define the pages
main = st.Page("main.py", title="Início - Estatísticas dos Hinos", icon="🏠")

# Tabela geral pra observação dos dados
tabela = st.Page("tabela.py", title="Tabela exploratória", icon="📆")
# Exploração das categorias dos louvores (eda1_part1)
categorias = st.Page("categorias.py", title="Categorias dos louvores", icon="📑")
# Exploração dos títulos (eda1_part2)
analise_titulo = st.Page("analise_titulo.py", title="Tamanho dos títulos", icon="🔢")
# Exploração dos textos (eda1_part3.1)
analise_texto = st.Page("analise_texto.py", title="Exploração de palavras", icon="🔡")
# Exploração dos textos (eda1_part3.2)
analise_palavras = st.Page("analise_palavras.py", title="Análise de palavras", icon="✒️")
# Tranformação de palavras em embeddings (eda1_part4)
word_embeddings = st.Page(
    "word_embeddings.py", title="Embeddings de palavras", icon="📝"
)
# Frases todas como embeddings (eda1_part5)
sent_embeddings = st.Page("sent_embeddings.py", title="Embeddings de frases", icon="🗒️")
# Seleção de similares usando TOPSIS (eda1_part6)
topsis_escolha = st.Page("topsis_escolha.py", title="Seleção de similares", icon="✅")
# Análise de emoções (eda1_part7)
emocoes = st.Page("emocoes.py", title="Análise de emoções", icon="🎭")

# Set up navigation
pg = st.navigation(
    [
        main,
        tabela,
        categorias,
        analise_titulo,
        analise_texto,
        analise_palavras,
        word_embeddings,
        sent_embeddings,
        topsis_escolha,
        emocoes,
    ]
)

# Run the selected page
pg.run()
