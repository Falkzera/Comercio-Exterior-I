import streamlit as st
import pandas as pd
import os
from automacao_coleta.utils.datas import get_range_historico
from automacao_coleta.src.historico import baixar_dados_historicos
from automacao_coleta.src.atualizacao import atualizar_ano_corrente

st.title("📦 Coletor de Dados")
st.subheader("Coletor de dados de comércio exterior brasileiro")
st.write("Escolha abaixo a ação que deseja realizar:")


anos_disponiveis = get_range_historico()
anos_selecionados = st.multiselect(
    "📅 Selecione os anos dos dados históricos:",
    anos_disponiveis,
    default=[anos_disponiveis[-1]] 
)
col1, col2 = st.columns(2)

with col1:

    if st.button("📚 Baixar Dados Históricos (anos selecionados)", use_container_width=True, type='secondary'):
        if not anos_selecionados:
            st.warning("Selecione ao menos um ano!")
        else:
            with st.spinner("Baixando e convertendo dados históricos..."):
                for ano in anos_selecionados:
                    for modo in ["EXP", "IMP"]:
                        baixar_dados_historicos(modo, ano)
            st.success("Download dos dados históricos concluído!")

with col2:
    if st.button("♻️ Atualizar Ano Atual", use_container_width=True, type='secondary'):
        with st.spinner("Atualizando dados do ano atual..."):
            for modo in ["EXP", "IMP"]:
                atualizar_ano_corrente(modo)
        st.success("Atualização do ano atual concluída!")

st.write('---')

st.write("### 📊 Visualizar Dados")

def concatall(tipo, modo):
    # tipo: 'EXP' ou 'IMP'
    # modo: 'Exportação' ou 'Importação'

    pasta = 'etl-processamento/data/input/'
    
    try:
        arquivos = [arq for arq in os.listdir(pasta) if tipo in arq and arq.endswith('.parquet')]
        if not arquivos:
            st.warning(f"Nenhum arquivo encontrado para o tipo {tipo}")
            return pd.DataFrame()
        
        dfs = []
        for arquivo in arquivos:
            caminho = os.path.join(pasta, arquivo)
            df = pd.read_parquet(caminho)
            df['TIPO'] = modo
            dfs.append(df)

        return pd.concat(dfs, ignore_index=True)
    except Exception as e:
        st.error(f"Erro ao processar os arquivos: {e}")
        return pd.DataFrame()

# Botão Streamlit
if st.button("📊 Visualizar Dados", use_container_width=True, type='primary'):
    df_exp = concatall('EXP', 'Exportação')
    df_imp = concatall('IMP', 'Importação')
    df = pd.concat([df_exp, df_imp], ignore_index=True)

    if not df.empty:
        st.write('### Dados Carregados:')
        col1, col2 = st.columns(2)
        col1.metric(f"Total de linhas:", len(df), delta=None, help=None, label_visibility="visible", border=True)
        col2.metric(f"Total de colunas:", len(df.columns), delta=None, help=None, label_visibility="visible", border=True)

        visualizacao = df.head(100)
        st.write('Visualização das primeiras 100 linhas')
        st.data_editor(visualizacao, use_container_width=True, hide_index=True, num_rows="dynamic", height=500)
    else:
        st.warning("Nenhum dado foi carregado.")

