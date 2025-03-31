import os
import requests
import pyarrow.csv as pv
import pyarrow.parquet as pq
import logging

def download_csv(url, destination_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(destination_path, 'wb') as f:
            f.write(response.content)
        logging.info(f"Download completo: {destination_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao baixar {url}: {e}")

def convert_csv_to_parquet(csv_path, parquet_path):
    try:
        table = pv.read_csv(
            csv_path,
            read_options=pv.ReadOptions(encoding='latin1'),
            parse_options=pv.ParseOptions(delimiter=';')
        )
        pq.write_table(table, parquet_path)
        os.remove(csv_path)
        logging.info(f"Convertido para Parquet e CSV removido: {csv_path}")
    except Exception as e:
        logging.error(f"Erro na conversão: {e}")
