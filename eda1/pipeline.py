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
    # hinos = text_processing(hinos)
    # hinos = length_calc(hinos)

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

    return hinos_analise.sort_values("numero")


def text_processing(hinos_analise: pd.DataFrame) -> pd.DataFrame:
    hinos_texto = hinos_analise.copy()

    stopwords = nltk.corpus.stopwords.words("portuguese")
    texto_processado = []
    titulo_processado = []
    punctuations = string.punctuation.replace("-", "")

    for hino in hinos_texto.to_dict("records"):
        texto = hino["texto_limpo"].translate(str.maketrans("", "", punctuations))
        texto = " ".join([palavra.upper() for palavra in texto.split()])
        texto = " ".join(
            [palavra for palavra in texto.split() if palavra.lower() not in stopwords]
        )
        texto_processado.append(texto)

        titulo = hino["nome_limpo"].translate(str.maketrans("", "", punctuations))
        titulo = " ".join([palavra.upper() for palavra in titulo.split()])
        titulo = " ".join(
            [palavra for palavra in titulo.split() if palavra.lower() not in stopwords]
        )
        titulo_processado.append(titulo)

    hinos_texto["texto_processado"] = texto_processado
    hinos_texto["titulo_processado"] = titulo_processado

    return hinos_texto


def length_calc(hinos_texto: pd.DataFrame) -> pd.DataFrame:
    hinos_length = hinos_texto.copy()

    hinos_length["titulo_tam_char"] = hinos_length["nome_limpo"].str.len()
    hinos_length["titulo_tam_palavras"] = (
        hinos_length["nome_limpo"].str.split().str.len()
    )
    hinos_length["texto_tam_palavras"] = hinos_length["texto"].str.split().str.len()
    hinos_length["texto_processado_tam_palavras"] = (
        hinos_length["texto_processado"].str.split().str.len()
    )

    return hinos_length
