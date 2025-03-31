import os
import pandas as pd
import timeit

start = timeit.default_timer()

extract_dir = os.path.join(os.getcwd(), '..', 'automacao-coleta', 'data')
caminho_destino = 'delta/BALANÇA-COMERCIAL/BALANCA-COMERCIAL.parquet'

def ler_parquet(path):
    try:
        return pd.read_parquet(path)
    except Exception as e:
        print(f"[ERRO] Leitura falhou: {e}")

def filtrar_alagoas(df):
    df = df[df['SG_UF_MUN'] == 'AL']
    df = df.drop(columns=['SG_UF_MUN'])
    return df

def tratar_base(df, categoria):
    df['DATA'] = pd.to_datetime(df['CO_ANO'].astype(str) + '-' + df['CO_MES'].astype(str) + '-01')
    df['CATEGORIA'] = categoria
    df = df.drop(columns=['CO_ANO', 'CO_MES'])
    return df[['DATA', 'NO_MUN', 'NO_PAIS', 'NO_SH4_POR', 'CATEGORIA', 'VL_FOB']]

# Leitura dos arquivos principais
df_imp = filtrar_alagoas(ler_parquet(f'{extract_dir}/IMP_COMPLETA_MUN.parquet'))
df_exp = filtrar_alagoas(ler_parquet(f'{extract_dir}/EXP_COMPLETA_MUN.parquet'))

# Leitura dos arquivos de apoio
df_mun = ler_parquet(f'{extract_dir}/MUN.parquet')
df_pais = ler_parquet(f'{extract_dir}/PAIS.parquet')
df_sh4 = ler_parquet(f'{extract_dir}/SH4.parquet')

# Merges
for df in [df_imp, df_exp]:
    df.merge(df_mun, on='CO_MUN')\
      .merge(df_pais, on='CO_PAIS')\
      .merge(df_sh4, on='SH4')

# Limpeza
df_imp.drop(columns=['CO_MUN', 'CO_PAIS', 'SH4', 'KG_LIQUIDO'], inplace=True)
df_exp.drop(columns=['CO_MUN', 'CO_PAIS', 'SH4', 'KG_LIQUIDO'], inplace=True)

# Transformação final
df_imp = tratar_base(df_imp, 'IMPORTACAO')
df_exp = tratar_base(df_exp, 'EXPORTACAO')

# Combinação e salvamento
df = pd.concat([df_imp, df_exp])
df.to_parquet(caminho_destino)

print(f"[✅] Processo concluído com sucesso. Shape final: {df.shape}")
print(f"⏱️ Tempo total: {timeit.default_timer() - start:.2f} segundos")
