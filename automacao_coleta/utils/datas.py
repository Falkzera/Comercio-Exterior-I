from datetime import datetime
import streamlit as st

def get_ano_atual():
    return datetime.now().year

def get_range_historico(ano_inicio=2025):
    return list(range(ano_inicio, get_ano_atual() + 1))  # até ano atual - 2
