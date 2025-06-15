
# problema no hadoop.
# por enquanto estou adaptando para pandas
# e apos tudo funcionar vejo a melhor solução

# usando o arquivo "data_processing_pandas.py" temporariamente

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, hour, when

# Inicializa a sessão Spark
spark = SparkSession.builder \
    .appName("Processamento de Acidentes") \
    .getOrCreate()

# Diretórios
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

# 1. Carrega o CSV de acidentes (gov.br)
df_acidentes = spark.read.option("header", True).option("delimiter", ";").csv(
    os.path.join(RAW_DIR, "datatran2025.csv")
)

# 2. Converte colunas para tipos adequados
df_acidentes = df_acidentes.withColumn("datahora", to_timestamp(col("data_inversa") + " " + col("horario"), "yyyy-MM-dd HH:mm"))
df_acidentes = df_acidentes.withColumn("hora", hour("datahora"))

# 3. Cria colunas de período do dia
df_acidentes = df_acidentes.withColumn("periodo",
    when((col("hora") >= 0) & (col("hora") < 6), "Madrugada")
    .when((col("hora") >= 6) & (col("hora") < 12), "Manhã")
    .when((col("hora") >= 12) & (col("hora") < 18), "Tarde")
    .otherwise("Noite")
)

# 4. Carrega JSON do IBGE (população/frota)
import json
import pandas as pd

with open(os.path.join(RAW_DIR, "ibge_populacao_2025-06-14.json"), encoding='utf-8') as f:
    ibge_json = json.load(f)

# Transforma para DataFrame Pandas
ibge_data = []
for item in ibge_json[0]['resultados'][0]['series']:
    municipio = item['localidade']['nome']
    valor = item['serie']['2022']
    ibge_data.append({'municipio': municipio, 'populacao': int(valor)})

df_ibge_pd = pd.DataFrame(ibge_data)
df_ibge = spark.createDataFrame(df_ibge_pd)

# 5. Junção com base no nome do município (com padronização para maiúsculas)
df_acidentes = df_acidentes.withColumn("municipio", col("municipio").alias("municipio_acidente"))
df_ibge = df_ibge.withColumn("municipio", col("municipio"))

df_final = df_acidentes.join(
    df_ibge.withColumn("municipio", col("municipio").upper()),
    df_acidentes["municipio"] == df_ibge["municipio"],
    how="left"
)

# 6. Salvar dados processados
df_final.write.mode("overwrite").parquet(os.path.join(PROCESSED_DIR, "acidentes_processados.parquet"))
print("✅ Dados processados salvos com sucesso.")
