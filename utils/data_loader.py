import pandas as pd
import geopandas as gpd
from shapely import wkt
import requests
import streamlit as st

@st.cache_data(show_spinner="A extrair dados populacionais da API do IBGE...")
def obter_populacao_ibge():
    url = "https://servicodados.ibge.gov.br/api/v3/agregados/4709/periodos/2022/variaveis/93?localidades=N6[all]"
    resposta = requests.get(url)
    dados_json = resposta.json()

    registos = []
    for serie in dados_json[0]['resultados'][0]['series']:
        cod_ibge = serie['localidade']['id']
        populacao = serie['serie']['2022']
        registos.append({
            "co_ibge_join": str(cod_ibge)[:6],
            "populacao": int(populacao)
        })
    return pd.DataFrame(registos)


@st.cache_data
def carregar_dados():
    df = pd.read_csv('data/dataset.csv', sep=',')
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    df["co_ibge"] = df["co_ibge"].astype(int)
    df["nu_ocorrencias_internacoes"] = pd.to_numeric(df["nu_ocorrencias_internacoes"], errors='coerce').fillna(0)
    df["nu_ocorrencias_ambulatorio"] = pd.to_numeric(df["nu_ocorrencias_ambulatorio"], errors='coerce').fillna(0)

    df_pop = obter_populacao_ibge()
    df['co_ibge_join'] = df['co_ibge'].astype(str).str[:6]
    df = df.merge(df_pop, on='co_ibge_join', how='left')

    df['populacao'] = df['populacao'].fillna(df['populacao'].median())

    df["taxa_internacoes"] = (df["nu_ocorrencias_internacoes"] / df["populacao"]) * 100000
    df["taxa_ambulatorio"] = (df["nu_ocorrencias_ambulatorio"] / df["populacao"]) * 100000

    df['geometry'] = df['mp_municipio'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry').set_crs(epsg=4326, inplace=False)
    gdf["id"] = gdf.index.astype(str)

    return gdf


@st.cache_data
def converter_para_csv(_df):
    df_export = _df.drop(columns=['geometry'], errors='ignore')
    return df_export.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')