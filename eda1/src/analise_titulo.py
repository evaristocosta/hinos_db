import streamlit as st
import pandas as pd
from pipeline import hinos_processados

hinos: pd.DataFrame = hinos_processados()

# separa dados de interesse
hinos["numero"] = hinos.index
hinos_analise = (
    hinos[["numero", "nome", "categoria_abr"]]
    .rename(columns={"numero": "Nº", "nome": "Nome", "categoria_abr": "Categoria"})
    .set_index("Nº")
)
# separa subtitulo do nome
hinos_analise["subtitulo"] = (
    hinos_analise["Nome"].str.extract(r"\((.*?)\)").squeeze().str.strip()
)
hinos_analise["Nome"] = hinos_analise["Nome"].str.replace(
    r"\s*\(.*?\)\s*", "", regex=True
)
# cria dataframe comparativo, considerando o subtitulo como um nome diferente
hinos_titulos = pd.concat(
    [
        hinos_analise[["subtitulo", "Categoria"]].rename(columns={"subtitulo": "Nome"}),
        hinos_analise[["Nome", "Categoria"]],
    ]
).dropna()
# calcula o tamanho do titulo
hinos_analise["titulo_tam_real"] = hinos_analise["Nome"].str.len()
hinos_titulos["titulo_tam_real"] = hinos_titulos["Nome"].str.len()


st.title("Tamanho dos títulos 🔢")

"""
Nesta seção, analisamos o tamanho dos títulos dos hinos na coletânea, tanto considerando
os títulos principais quanto os subtítulos. São considerados subtítulos aqueles que aparecem
entre parênteses no título. A coluna da esquerda mostra os resultados desconsiderando os subtítulos, 
enquanto a coluna da direita inclui os subtítulos. 
Na análise com subtítulos, o mesmo hino pode aparecer duas vezes,
uma vez com o título principal e outra com o subtítulo.

O tamanho aqui, é medido em número de caracteres, considerando espaços. 

É possível usar o filtro na barra lateral para restringir a análise a categorias específicas de hinos.
"""


st.sidebar.markdown("# Filtros")
# add filter by category
categorias = hinos_analise["Categoria"].unique()
categoria_selecionada = st.sidebar.multiselect(
    "Filtrar por categoria:", list(categorias), placeholder="Selecione categorias..."
)
if categoria_selecionada:
    hinos_analise_print = hinos_analise.query(
        f"Categoria in {categoria_selecionada}"
    ).copy()
    hinos_titulos = hinos_titulos.query(f"Categoria in {categoria_selecionada}")
else:
    hinos_analise_print = hinos_analise.copy()

col1, col2 = st.columns(2)


with col1:
    st.markdown("**Desconsiderando subtítulos**")
    st.markdown("Top 10 maiores títulos")
    st.dataframe(
        hinos_analise_print[["Nome", "titulo_tam_real"]]
        .sort_values(by="titulo_tam_real", ascending=False)
        .head(10),
        column_config={
            "titulo_tam_real": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do título em caracteres",
                max_value=int(hinos_analise_print["titulo_tam_real"].max()),
                width="small",
            ),
            "Nome": st.column_config.TextColumn(width="small", max_chars=25),
        },
    )
    st.markdown("Top 10 menores títulos")
    st.dataframe(
        hinos_analise_print[["Nome", "titulo_tam_real"]]
        .sort_values(by="titulo_tam_real")
        .head(10),
        column_config={
            "titulo_tam_real": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do título em caracteres",
                max_value=int(hinos_analise_print["titulo_tam_real"].max()),
                width="small",
            ),
            "Nome": st.column_config.TextColumn(width="small", max_chars=25),
        },
    )

with col2:
    st.markdown("**Considerando subtítulos**")
    st.markdown("Top 10 maiores títulos")
    st.dataframe(
        hinos_titulos[["Nome", "titulo_tam_real"]]
        .sort_values(by="titulo_tam_real", ascending=False)
        .head(10),
        column_config={
            "titulo_tam_real": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do título em caracteres",
                max_value=int(hinos_titulos["titulo_tam_real"].max()),
                width="small",
            ),
            "Nome": st.column_config.TextColumn(width="small", max_chars=25),
        },
    )
    st.markdown("Top 10 menores títulos")
    st.dataframe(
        hinos_titulos[["Nome", "titulo_tam_real"]]
        .sort_values(by="titulo_tam_real")
        .head(10),
        column_config={
            "titulo_tam_real": st.column_config.ProgressColumn(
                "Tamanho",
                format="%f",
                help="Tamanho do título em caracteres",
                max_value=int(hinos_titulos["titulo_tam_real"].max()),
                width="small",
            ),
            "Nome": st.column_config.TextColumn(width="small", max_chars=25),
        },
    )


"""
Observamos que a inclusão dos subtítulos altera a lista dos maiores e menores títulos. De forma geral,
os oito primeiros hinos com maiores títulos permanecem os mesmos, sendo que o maior título contém 46 caracteres, 
ocorrendo três vezes (hinos 323, 511 e 612).

Já na lista dos menores títulos, a inclusão dos subtítulos traz mudanças mais significativas, alterando significativamente
a composição dos dez menores títulos. O menor título absoluto, com apenas quatro caracteres, é o hino 475 ("Ageu").

Por fim, parece não haver uma correlação clara entre o tamanho do título e a categoria do hino, sugerindo que a 
extensão do título não está diretamente relacionada ao tema abordado.


## Medidor de título

Selecione um hino para ver o tamanho do seu título, e comparar com outros hinos com título de igual tamanho.
"""

col1, col2 = st.columns(2)

with col1:
    hymn_num = st.number_input(
        "Número do hino",
        min_value=int(hinos_analise.index.min()),
        max_value=int(hinos_analise.index.max()),
        value=int(hinos_analise.index.min()),
    )
    hymn_title = hinos_analise.loc[hymn_num, "Nome"]
    hymn_title_size = hinos_analise.loc[hymn_num, "titulo_tam_real"]

with col2:
    st.markdown(
        f"**🎵 Hino {hymn_num} — {hymn_title}:** <br>*{hymn_title_size} caracteres*",
        unsafe_allow_html=True,
    )

hinos_mesmo_tamanho = hinos_analise[
    hinos_analise["titulo_tam_real"] == hymn_title_size
].drop(index=hymn_num)
if not hinos_mesmo_tamanho.empty:
    st.markdown("Outros hinos com título de igual tamanho:")

    st.dataframe(
        hinos_mesmo_tamanho[["Nome", "Categoria"]],
        column_config={
            "Nome": st.column_config.TextColumn(width="large"),
            "Categoria": st.column_config.TextColumn(width="small", max_chars=25),
        },
    )
