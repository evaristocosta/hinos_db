import streamlit as st

# Define the pages
main = st.Page("main.py", title="Estatísticas dos Hinos", icon="🏠")
tabela = st.Page("tabela.py", title="Tabela exploratória", icon="📆")
categorias = st.Page("categorias.py", title="Categorias dos louvores", icon="📑")
ranking_titulo = st.Page("ranking_titulo.py", title="Tamanho dos títulos", icon="🔢")
ranking_texto = st.Page("ranking_texto.py", title="Estudo de palavras", icon="✒️")

# Set up navigation
pg = st.navigation([main, tabela, categorias, ranking_titulo, ranking_texto])

# Run the selected page
pg.run()
