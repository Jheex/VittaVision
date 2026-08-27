import pandas as pd
import streamlit as st
import os

@st.cache_data
def carregar_dados_ultimo_mes(nome_arquivo: str) -> pd.DataFrame:
    """
    Carrega qualquer CSV da pasta de dados mantendo apenas 
    a foto do registro/competência mais recente de cada entidade.
    """
    caminhos = [
        f"data/{nome_arquivo}",
        f"{nome_arquivo}",
        f"../data/{nome_arquivo}"
    ]
    
    df = pd.DataFrame()
    for caminho in caminhos:
        if os.path.exists(caminho):
            try:
                df = pd.read_csv(caminho, sep=";", encoding="latin1")
                if not df.empty:
                    break
            except Exception:
                try:
                    df = pd.read_csv(caminho, sep=",", encoding="utf-8")
                    if not df.empty:
                        break
                except Exception:
                    continue

    if df.empty:
        return df

    # 1. Identifica a coluna temporal de competência/data
    col_tempo = None
    cols_data_possiveis = ["COMPETENCIA", "COMP", "NU_COMP", "ANO_MES", "DATA", "DT_INTERNACAO"]
    for c in cols_data_possiveis:
        if c in df.columns:
            col_tempo = c
            break

    if col_tempo:
        # Ordena para garantir que a última competência fique por último
        df = df.sort_values(col_tempo, ascending=True)

    # 2. Identifica a chave primária/identificador do registro
    chave = None
    if "CO_CNES" in df.columns:
        chave = ["CO_CNES"]
    elif "CNES" in df.columns:
        chave = ["CNES"]
    elif "NOME_ESTABELECIMENTO" in df.columns and "MUNICIPIO" in df.columns:
        chave = ["NOME_ESTABELECIMENTO", "MUNICIPIO"]
    elif "NOME_ESTABELECIMENTO" in df.columns:
        chave = ["NOME_ESTABELECIMENTO"]

    # 3. Se encontrou uma chave, remove duplicatas mantendo o mês mais recente
    if chave:
        df = df.drop_duplicates(subset=chave, keep="last")

    return df