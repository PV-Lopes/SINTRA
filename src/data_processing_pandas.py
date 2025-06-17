# src/data_processing.py
import pandas as pd
import os
from datetime import datetime

INPUT = "data/raw/acidentes2025_todas_causas_tipos.csv"
OUTPUT = "data/processed/sinistros_processados.csv"
os.makedirs("data/processed", exist_ok=True)

# Carrega CSV bruto
df = pd.read_csv(INPUT, sep=';', encoding='latin-1')

# Converte datas
df['datahora'] = pd.to_datetime(df['data_inversa'] + ' ' + df['horario'], errors='coerce')
df['ano'] = df['datahora'].dt.year
df['mes'] = df['datahora'].dt.month

# Cria faixa etária personalizada
def faixa(idade):
    if idade <= 17: return '0-17'
    elif idade <= 25: return '18-25'
    elif idade <= 40: return '26-40'
    elif idade <= 60: return '41-60'
    elif idade <= 80: return '61-80'
    else: return '80+'

df['idade'] = pd.to_numeric(df['idade'], errors='coerce')
df = df[df['idade'].notna()]
df['faixa_idade'] = df['idade'].apply(faixa)

# Natureza do sinistro

def natureza(row):
    if row['mortos'] > 0 or row['feridos_graves'] > 0 or row['feridos_leves'] > 0:
        return 'Com Vítima'
    return 'Sem Vítima'

df['natureza_sinistro'] = df.apply(natureza, axis=1)

# Filtra colunas relevantes
colunas = [
    'datahora', 'dia_semana', 'horario', 'ano', 'mes', 'uf', 'municipio', 'br', 'km',
    'tipo_acidente', 'classificacao_acidente', 'natureza_sinistro', 'fase_dia', 'sentido_via',
    'condicao_metereologica', 'tipo_pista', 'tracado_via', 'uso_solo',
    'tipo_veiculo', 'tipo_envolvido', 'estado_fisico', 'idade', 'faixa_idade', 'sexo',
    'ilesos', 'feridos_leves', 'feridos_graves', 'mortos', 'latitude', 'longitude'
]
df_filtrado = df[colunas]

# Remove registros sem coordenada
df_filtrado = df_filtrado[df_filtrado['latitude'].notna() & df_filtrado['longitude'].notna()]

# Salva
df_filtrado.to_csv(OUTPUT, index=False, sep=';')
print(f"✅ Arquivo salvo em {OUTPUT} com {len(df_filtrado)} registros.")
