import os
import json
import requests
import pandas as pd
from datetime import datetime

# Diretórios
RAW_DATA_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

# 1. Coleta de dados de acidentes - PRF
def fetch_prf_data():
    url = "https://api.prf.gov.br/v1/acidentes"  # Link real pode ter parâmetros específicos
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        file_path = os.path.join(RAW_DATA_DIR, f"acidentes_prf_{datetime.now().date()}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[✓] Dados da PRF salvos em: {file_path}")
    except Exception as e:
        print(f"[Erro] Falha ao coletar dados da PRF: {e}")

# 2. Coleta de dados do IBGE - População e Frota
def fetch_ibge_data():
    # Exemplo: População estimada (cód. 2910) por município
    url = "https://servicodados.ibge.gov.br/api/v3/agregados"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        ibge_json = response.json()
        file_path = os.path.join(RAW_DATA_DIR, f"ibge_populacao_{datetime.now().date()}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(ibge_json, f, ensure_ascii=False, indent=2)
        print(f"[✓] Dados do IBGE (população) salvos em: {file_path}")
    except Exception as e:
        print(f"[Erro] Falha ao coletar dados do IBGE: {e}")

# Execução do script
if __name__ == "__main__":
    print("🔹 Iniciando coleta de dados...")
    fetch_prf_data()
    fetch_ibge_data()
    print("✅ Coleta finalizada.")
