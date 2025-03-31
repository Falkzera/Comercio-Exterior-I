import os

def get_input_data_path():
    return os.path.abspath(os.path.join(os.getcwd(), 'etl-processamento', 'data', 'input'))

def ensure_directory_exists(path):
    os.makedirs(path, exist_ok=True)
