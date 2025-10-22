import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
from pathlib import Path

# import nltk

# nltk.download("stopwords")


@st.cache_data
def hinos_processados() -> pd.DataFrame:
    # hinos = load_data()
    # hinos = preprocessing(hinos)
    # pkl_path = Path(__file__).parent.parent / "assets" / "hinos_analise_com_emocoes.pkl"
    pkl_path = (
        Path(__file__).parent.parent / "assets" / "hinos_analise_word_embeddings.pkl"
    )
    hinos_processados = pd.read_pickle(pkl_path)

    return hinos_processados


@st.cache_data
def load_data() -> pd.DataFrame:
    database_path = Path(__file__).parent.parent / "assets" / "database.db"
    engine = create_engine(f"sqlite:///{database_path}")

    # Connect to the database
    connection = engine.connect()

    sql_query = """
    select
        numero,
        nome,
        texto,
        texto_limpo,
        categoria_id,
        c.descricao as categoria
    from 
        hino
        left join categoria c on c.id = categoria_id
    where
        coletanea_id = 1
    """

    hinos_analise = pd.read_sql_query(sql_query, connection)
    return hinos_analise


""" def preprocessing(hinos: pd.DataFrame) -> pd.DataFrame:
    hinos_analise = hinos.copy()
    hinos_analise.loc[hinos_analise["numero"] == "null", "numero"] = 0
    hinos_analise["numero_int"] = hinos_analise["numero"].astype(int)
    hinos_analise = hinos_analise.drop(columns=["numero"]).rename(
        columns={"numero_int": "numero"}
    )
    hinos_analise["categoria_abr"] = hinos_analise["categoria"].apply(
        lambda x: x[:13] + "..." if len(x) > 15 else x
    )

    return hinos_analise.sort_values("numero")
"""


@st.cache_data
def similarity_matrices():
    similarity_word = pd.read_pickle(
        "../assets/similarity_matrix_word_embeddings_tfidf.pkl"
    )
    similarity_sent = pd.read_pickle(
        "../assets/similarity_matrix_sentence_embeddings.pkl"
    )
    return similarity_word, similarity_sent
