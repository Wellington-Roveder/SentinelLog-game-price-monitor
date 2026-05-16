import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from database.db_manager import DBManager


load_dotenv()
db_manager = DBManager()





st.set_page_config(page_title="SentinelLog Dashboard", layout="wide")

def carregar_dados():
    db_dados = db_manager.buscar_tudo()
    df = pd.DataFrame(db_dados, columns=['id','produto', 'valor', 'data_verificacao', 'loja_barata'])
    return df

st.title("Sentinellog - Monitor de Preços")
st.markdown("Acompanhamento em tempo real dos preços monitorados via API")

df = carregar_dados()

if not df.empty:
    total_jogos = df['produto'].nunique()
    st.metric("Total de Jogos Monitorados", total_jogos)

    #filtrar por jogo
    jogo_selecionado = st.selectbox("Selecione um jogo para ver o historico:", df['produto'].unique())
    df_filtrado = df[df['produto'] == jogo_selecionado]
    df_filtrado['data_verificacao'] = pd.to_datetime(df_filtrado['data_verificacao'], dayfirst=True)
    

    # Graficos de Preços
    st.subheader(f"Historico de Preços: {jogo_selecionado}")
    st.line_chart(df_filtrado.set_index('data_verificacao')['valor'])

    #tabela de dados brutos
    st.subheader("Ultimos Registros")
    st.dataframe(df, width="stretch")
else:
    st.warning("O Banco de Dados ainda esta Vazio, Rode o monitor Primeiro")    