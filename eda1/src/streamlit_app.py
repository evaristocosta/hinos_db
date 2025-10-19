import streamlit as st

# Define the pages
main = st.Page("main.py", title="Estatísticas dos Hinos", icon="🏠")

# Tabela geral pra observação dos dados
tabela = st.Page("tabela.py", title="Tabela exploratória", icon="📆")
# Exploração das categorias dos louvores (eda1_part1)
categorias = st.Page("categorias.py", title="Categorias dos louvores", icon="📑")
# Exploração dos títulos (eda1_part2)
analise_titulo = st.Page("analise_titulo.py", title="Tamanho dos títulos", icon="🔢")
# Exploração dos textos (eda1_part3.1)
analise_texto = st.Page("analise_texto.py", title="Estudo de palavras", icon="✒️")
# Exploração dos textos (eda1_part3.2)
analise_palavras = st.Page("analise_palavras.py", title="Análise de palavras", icon="✒️")
# Tranformação de palavras em embeddings (eda1_part4)
word_embeddings = st.Page("word_embeddings.py", title="Análise de texto", icon="✒️")
# Frases todas como embeddings (eda1_part5)
seq_embeddings = st.Page("seq_embeddings.py", title="Análise de texto", icon="✒️")
# Seleção de similares usando TOPSIS (eda1_part6)
topsis_escolha = st.Page("topsis_escolha.py", title="Análise de texto", icon="✒️")
# Análise de emoções (eda1_part7)
emocoes = st.Page("emocoes.py", title="Análise de texto", icon="✒️")

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
        seq_embeddings,
        topsis_escolha,
        emocoes,
    ]
)

# Run the selected page
pg.run()
