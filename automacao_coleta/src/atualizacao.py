from automacao_coleta.src.download import download_csv, convert_csv_to_parquet
from automacao_coleta.utils.paths import get_input_data_path, ensure_directory_exists
from automacao_coleta.utils.datas import get_ano_atual
from automacao_coleta.utils.logging_utils import setup_logging
import os
import logging

def atualizar_ano_corrente(modo: str):
    setup_logging()
    ano = get_ano_atual()
    base_dir = get_input_data_path()
    ensure_directory_exists(base_dir)

    filename_csv = f"{modo}_{ano}.csv"
    filename_parquet = f"{modo}_{ano}.parquet"
    url = f"https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/{modo}_{ano}.csv"

    csv_path = os.path.join(base_dir, filename_csv)
    parquet_path = os.path.join(base_dir, filename_parquet)

    logging.info(f"[ATUALIZAÇÃO] Atualizando {modo} {ano}...")
    download_csv(url, csv_path)
    convert_csv_to_parquet(csv_path, parquet_path)

if __name__ == "__main__":
    for modo in ["EXP", "IMP"]:
        atualizar_ano_corrente(modo)
