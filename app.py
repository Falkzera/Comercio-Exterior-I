import os
import streamlit as st
import pandas as pd
from automacao_coleta.utils.datas import get_range_historico
from automacao_coleta.src.historico import baixar_dados_historicos
from automacao_coleta.src.atualizacao import atualizar_ano_corrente
from utils.credits import display_credits

st.title("📦 Coletor de Dados")
st.subheader("Dados brutos de comércio exterior brasileiro")
st.write('---')
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
with st.expander("📊 Visualizar Dados", expanded=False):
    df_exp = concatall('EXP', 'Exportação')
    df_imp = concatall('IMP', 'Importação')
    df = pd.concat([df_exp, df_imp], ignore_index=True)

    if not df.empty:
        st.write('### Dados Carregados:')
        col1, col2 = st.columns(2)
        col1.metric(f"Total de linhas:", len(df), delta=None, help=None, label_visibility="visible", border=True)
        col2.metric(f"Total de colunas:", len(df.columns), delta=None, help=None, label_visibility="visible", border=True)

        st.write('Visualização das primeiras 100 linhas')
        linhas_por_pagina = 100
        total_paginas = (len(df) - 1) // linhas_por_pagina + 1
        pagina = st.number_input("📄 Página", min_value=1, max_value=total_paginas, value=1)

        inicio = (pagina - 1) * linhas_por_pagina
        fim = inicio + linhas_por_pagina
        st.write(f"Visualizando linhas {inicio + 1} a {min(fim, len(df))} de {len(df)}")
        st.data_editor(df.iloc[inicio:fim], use_container_width=True, height=400, num_rows='dynamic', hide_index=False)

        st.download_button(
            label="📥 Download do DataFrame completo",
            data=df.to_parquet(index=False),
            file_name='dados_comerciais.parquet',
            mime='application/octet-stream'
        , use_container_width=True, type='primary')
        st.caption('Download em Parquet. Para abrir, use o Pandas ou PyArrow.')
    else:
        st.warning("Nenhum dado foi carregado.")


display_credits()