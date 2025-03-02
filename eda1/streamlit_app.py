import streamlit as st

# Define the pages
main = st.Page("main.py", title="Dados da Coletânea ICM", icon="🎈")
tabela = st.Page("tabela.py", title="Tabela exploratória", icon="📊")
categorias = st.Page("categorias.py", title="Categorias dos louvores", icon="📦")
ranking_titulo = st.Page("ranking_titulo.py", title="Ranking por título", icon="🏆")
ranking_texto = st.Page("ranking_texto.py", title="Ranking por texto", icon="🏆")
palavras = st.Page("palavras.py", title="Palavras mais frequentes", icon="📊")

# Set up navigation
pg = st.navigation([main, tabela, categorias, ranking_titulo, ranking_texto, palavras])

# Run the selected page
pg.run()
