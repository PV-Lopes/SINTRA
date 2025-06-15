# Codigos com erros por favor não mexer 🦊


import os
import pandas as pd
import joblib
import dash
from dash import dcc, html, dash_table
import plotly.express as px

# Caminhos
PROCESSED_PATH = "data/processed/acidentes_processados.csv"
MODEL_PATH = "data/models/modelo_risco_acidente.pkl"

# Carrega dados e modelo
df = pd.read_csv(PROCESSED_PATH, sep=';')
df['datahora'] = pd.to_datetime(df['datahora'], errors='coerce')
model = joblib.load(MODEL_PATH)

# ======= PREPARAÇÃO DOS DADOS PARA PREDIÇÃO =======
features = [
    'hora', 'periodo', 'causa_acidente', 'tipo_acidente',
    'condicao_metereologica', 'tipo_pista', 'tracado_via',
    'sentido_via', 'uso_solo', 'populacao'
]

# Subconjunto com dados válidos e campos extra para visualização
df_predicao = df[
    features + ["latitude", "longitude", "datahora", "municipio_normalizado",
                "br", "km", "causa_acidente", "tipo_acidente"]
].dropna().copy()

# One-hot encoding
df_model_encoded = pd.get_dummies(df_predicao[features])

# Garante as colunas esperadas pelo modelo
model_cols = model.feature_names_in_
for col in model_cols:
    if col not in df_model_encoded.columns:
        df_model_encoded[col] = 0

# Reordena as colunas na mesma ordem do modelo
df_model_encoded = df_model_encoded[model_cols.tolist()]

# Faz predição
df_predicao["risco_predito"] = model.predict(df_model_encoded)

# ======= DASHBOARD COM DASH =======
app = dash.Dash(__name__)
app.title = "Sistema Inteligente de Prevenção de Acidentes"

app.layout = html.Div([
    html.H1("📊 Prevenção de Acidentes em Rodovias Federais", style={"textAlign": "center"}),

    html.Div([
        dcc.Graph(
            id="mapa-calor",
            figure=px.density_mapbox(
                df_predicao[df_predicao['risco_predito'] == 1],
                lat='latitude', lon='longitude', z='risco_predito',
                radius=10, center=dict(lat=-15.8, lon=-47.9), zoom=4,
                mapbox_style="carto-positron",
                title="🗺️ Mapa de Calor de Acidentes com Risco Alto"
            )
        )
    ], style={"margin": "30px"}),

    html.Div([
        dcc.Graph(
            id="grafico-horas",
            figure=px.histogram(
                df_predicao, x="hora", color="risco_predito", barmode="overlay",
                title="🕒 Acidentes por Hora do Dia (com risco predito)",
                labels={"hora": "Hora do Acidente"}
            )
        )
    ], style={"margin": "30px"}),

    html.Div([
        html.H3("🚨 Alertas Recentes de Alto Risco"),
        dash_table.DataTable(
            data=df_predicao[df_predicao["risco_predito"] == 1][[
                "datahora", "municipio_normalizado", "br", "km",
                "causa_acidente", "tipo_acidente"
            ]].sort_values("datahora", ascending=False).head(10).to_dict("records"),
            columns=[{"name": i, "id": i} for i in [
                "datahora", "municipio_normalizado", "br", "km",
                "causa_acidente", "tipo_acidente"
            ]],
            style_cell={"textAlign": "left", "padding": "5px"},
            style_header={"backgroundColor": "#444", "color": "white"},
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "#f5f5f5"}
            ],
        )
    ], style={"margin": "30px"}),

    html.Div([
        html.H3("📋 Tabela Geral de Acidentes com Predição"),
        dash_table.DataTable(
            data=df_predicao[[
                "datahora", "municipio_normalizado", "br", "km", "hora",
                "causa_acidente", "tipo_acidente", "risco_predito"
            ]].to_dict("records"),
            columns=[{"name": i, "id": i} for i in [
                "datahora", "municipio_normalizado", "br", "km", "hora",
                "causa_acidente", "tipo_acidente", "risco_predito"
            ]],
            page_size=10,
            style_cell={"textAlign": "left", "padding": "5px"},
            style_header={"backgroundColor": "#1f77b4", "color": "white"},
        )
    ], style={"margin": "30px"}),

], style={"fontFamily": "Arial"})


if __name__ == "__main__":
    app.run_server(debug=True)
