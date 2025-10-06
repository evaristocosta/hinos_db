import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import string
import nltk

nltk.download("stopwords")


@st.cache_data
def hinos_processados():
    hinos = load_data()
    hinos = preprocessing(hinos)

    return hinos


def load_data() -> pd.DataFrame:
    engine = create_engine("sqlite:///assets//database.db")

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


def preprocessing(hinos: pd.DataFrame) -> pd.DataFrame:
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
