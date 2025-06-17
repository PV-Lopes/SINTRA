# funcionando, porem em melhoria🦊

# src/dashboard.py
import os
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output
import plotly.express as px

# Carrega dados
DATA_PATH = "data/processed/sinistros_processados.csv"
try:
    df_original = pd.read_csv(DATA_PATH, sep=';')
    df_original['datahora'] = pd.to_datetime(df_original['datahora'], errors='coerce')
except Exception as e:
    print(f"Erro ao carregar CSV: {e}")
    df_original = pd.DataFrame()

# Modo escuro
theme_color = "#121212"
text_color = "#f0f0f0"
accent_color = "#1976D2"

app = Dash(__name__)
app.title = "Dashboard de Sinistros em Rodovias"

app.layout = html.Div([
    html.H1("📊 Sinistros em Rodovias Federais", style={"textAlign": "center", "color": accent_color}),

    html.Div([
        dcc.Dropdown([{"label": str(m), "value": m} for m in sorted(df_original['mes'].dropna().unique())], id="filtro-mes", multi=True, placeholder="Mês"),
        dcc.Dropdown([{"label": d, "value": d} for d in sorted(df_original['dia_semana'].dropna().unique())], id="filtro-dia", multi=True, placeholder="Dia da Semana"),
        dcc.Dropdown([{"label": uf, "value": uf} for uf in sorted(df_original['uf'].dropna().unique())], id="filtro-uf", multi=True, placeholder="Estado (UF)"),
        dcc.Dropdown([{"label": m, "value": m} for m in sorted(df_original['municipio'].dropna().unique())], id="filtro-municipio", multi=True, placeholder="Município"),
        dcc.Dropdown([{"label": n, "value": n} for n in sorted(df_original['natureza_sinistro'].dropna().unique())], id="filtro-natureza", multi=True, placeholder="Natureza do Sinistro"),
        dcc.Dropdown([{"label": t, "value": t} for t in sorted(df_original['tipo_acidente'].dropna().unique())], id="filtro-tipo", multi=True, placeholder="Tipo de Sinistro"),
        dcc.Dropdown([{"label": v, "value": v} for v in sorted(df_original['tipo_veiculo'].dropna().unique())], id="filtro-veiculo", multi=True, placeholder="Tipo de Veículo"),
        dcc.Dropdown([{"label": t, "value": t} for t in sorted(df_original['tipo_envolvido'].dropna().unique())], id="filtro-envolvido", multi=True, placeholder="Tipo de Vítima"),
        dcc.Dropdown([{"label": s, "value": s} for s in sorted(df_original['sexo'].dropna().unique())], id="filtro-sexo", multi=True, placeholder="Sexo"),
        dcc.Dropdown([{"label": f, "value": f} for f in sorted(df_original['faixa_idade'].dropna().unique())], id="filtro-idade", multi=True, placeholder="Faixa Etária"),
        html.Button("⬇️ Exportar CSV", id="btn-exportar", n_clicks=0, style={"marginTop": "20px", "backgroundColor": accent_color, "color": "white"}),
        html.Div(id="export-feedback", style={"marginTop": "10px", "color": text_color})
    ], style={"width": "30%", "display": "inline-block", "padding": "20px", "verticalAlign": "top", "backgroundColor": theme_color}),

    html.Div([
        dcc.Graph(id="mapa"),
        dcc.Graph(id="grafico_tipo"),
        dcc.Graph(id="grafico_veiculo"),
        dcc.Graph(id="grafico_sexo"),
        dcc.Graph(id="grafico_tendencia")
    ], style={"width": "68%", "display": "inline-block", "verticalAlign": "top", "backgroundColor": theme_color})

], style={"backgroundColor": theme_color, "fontFamily": "Arial"})

@app.callback(
    Output("mapa", "figure"),
    Output("grafico_tipo", "figure"),
    Output("grafico_veiculo", "figure"),
    Output("grafico_sexo", "figure"),
    Output("grafico_tendencia", "figure"),
    Output("export-feedback", "children"),
    Input("filtro-mes", "value"), Input("filtro-dia", "value"),
    Input("filtro-uf", "value"), Input("filtro-municipio", "value"),
    Input("filtro-natureza", "value"), Input("filtro-tipo", "value"),
    Input("filtro-veiculo", "value"), Input("filtro-envolvido", "value"),
    Input("filtro-sexo", "value"), Input("filtro-idade", "value"),
    Input("btn-exportar", "n_clicks")
)
def atualizar(mes, dia, uf, municipio, natureza, tipo, veiculo, envolvido, sexo, idade, export_clicks):
    df = df_original.copy()
    filtros = [
        (mes, 'mes'), (dia, 'dia_semana'), (uf, 'uf'),
        (municipio, 'municipio'), (natureza, 'natureza_sinistro'),
        (tipo, 'tipo_acidente'), (veiculo, 'tipo_veiculo'),
        (envolvido, 'tipo_envolvido'), (sexo, 'sexo'), (idade, 'faixa_idade')
    ]
    for val, col in filtros:
        if val: df = df[df[col].isin(val)]

    if export_clicks:
        path = "data/processed/export_filtrado.csv"
        df.to_csv(path, sep=';', index=False)
        feedback = f"CSV exportado para {path}"
    else:
        feedback = ""

    mapa = px.density_mapbox(df, lat="latitude", lon="longitude", z="km", radius=10, zoom=4,
        center={"lat": -15.8, "lon": -47.9}, mapbox_style="carto-darkmatter", title="🗺️ Mapa de Sinistros")

    tipo_fig = px.histogram(df, x="tipo_acidente", title="💥 Tipo de Sinistro")
    veic_fig = px.histogram(df, x="tipo_veiculo", title="🚗 Tipo de Veículo")
    sexo_fig = px.histogram(df, x="sexo", title="⚧️ Sexo da Vítima")
    tendencia = px.histogram(df, x="mes", title="📈 Tendência Mensal de Sinistros")

    for fig in [mapa, tipo_fig, veic_fig, sexo_fig, tendencia]:
        fig.update_layout(template="plotly_dark")

    return mapa, tipo_fig, veic_fig, sexo_fig, tendencia, feedback

if __name__ == "__main__":
    app.run(debug=True)
