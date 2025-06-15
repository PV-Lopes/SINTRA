import os
import pandas as pd
from datetime import datetime

# Diretórios
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

# 1. Carrega CSV de acidentes
df = pd.read_csv(os.path.join(RAW_DIR, "datatran2025.csv"), sep=';', encoding='latin-1')

# 2. Converte data e hora
df['datahora'] = pd.to_datetime(df['data_inversa'] + ' ' + df['horario'], errors='coerce')
df['hora'] = df['datahora'].dt.hour

# 3. Cria período do dia
def definir_periodo(hora):
    if pd.isna(hora):
        return 'Indefinido'
    elif hora < 6:
        return 'Madrugada'
    elif hora < 12:
        return 'Manhã'
    elif hora < 18:
        return 'Tarde'
    else:
        return 'Noite'

df['periodo'] = df['hora'].apply(definir_periodo)

# 4. Simula dados populacionais do IBGE (erro com api provavelmente ele caio novamente ou não possue os dados que preciso, logo a arte do improviso🦊)
ibge_data = [
    {"municipio": "SÃO PAULO", "populacao": 12325232},
    {"municipio": "RIO DE JANEIRO", "populacao": 6748000},
    {"municipio": "BRASÍLIA", "populacao": 3055149},
    {"municipio": "BELO HORIZONTE", "populacao": 2523794},
    {"municipio": "SALVADOR", "populacao": 2675654},
    {"municipio": "CURITIBA", "populacao": 1963726},
    {"municipio": "PORTO ALEGRE", "populacao": 1484953},
    {"municipio": "RECIFE", "populacao": 1488920},
    {"municipio": "GOIÂNIA", "populacao": 1536097},
    {"municipio": "MANAUS", "populacao": 2219580}
]

df_ibge = pd.DataFrame(ibge_data)

# 5. Padroniza e faz merge
df['municipio_normalizado'] = df['municipio'].str.strip().str.upper()
df_merged = df.merge(df_ibge, how='left', left_on='municipio_normalizado', right_on='municipio')

# 6. Salva CSV processado
output_path = os.path.join(PROCESSED_DIR, "acidentes_processados.csv")
df_merged.to_csv(output_path, index=False, sep=';')

print(f"✅ Dados processados salvos em: {output_path}")
