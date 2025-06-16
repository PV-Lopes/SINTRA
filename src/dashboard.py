# funcionando, porem em melhoria🦊

import os
import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output
import plotly.express as px

# Caminho do CSV
CSV_PATH = "data/processed/acidentes_processados.csv"
df_original = pd.read_csv(CSV_PATH, sep=';')
df_original['datahora'] = pd.to_datetime(df_original['datahora'], errors='coerce')

# Opções de filtros
ufs = sorted(df_original['uf'].dropna().unique())
brs = sorted(df_original['br'].dropna().unique())

# App Dash
app = Dash(__name__)
app.title = "Visualização de Acidentes"

app.layout = html.Div([
    html.H1("🚧 Dashboard de Sinistros de Trânsito em Rodovias Federais", style={"textAlign": "center"}),

    html.Div([
        html.Label("🗺️ UF (Estado):"),
        dcc.Dropdown(options=[{"label": uf, "value": uf} for uf in ufs], id="filtro-uf", multi=True),

        html.Label("🛣️ BR (Rodovia):", style={"marginTop": "10px"}),
        dcc.Dropdown(options=[{"label": f"BR-{int(br)}", "value": br} for br in brs], id="filtro-br", multi=True),

        html.Button("⬇️ Exportar CSV", id="btn-exportar", n_clicks=0, style={"marginTop": "10px"}),
        html.Div(id="export-feedback", style={"marginBottom": "20px", "color": "green"})
    ], style={"padding": "20px", "width": "30%", "display": "inline-block", "verticalAlign": "top"}),

    html.Div([
        dcc.Graph(id="mapa-calor"),
        dcc.Graph(id="grafico-horas"),
        dcc.Graph(id="grafico-tipo"),
        dcc.Graph(id="grafico-clima")
    ], style={"width": "68%", "display": "inline-block", "verticalAlign": "top"}),

    html.H3("📋 Últimos Sinistros Filtrados"),
    dash_table.DataTable(id="tabela-acidentes",
                         columns=[{"name": i, "id": i} for i in [
                             "datahora", "uf", "municipio_x", "br", "km",
                             "tipo_acidente", "causa_acidente", "condicao_metereologica"
                         ]],
                         page_size=10,
                         style_cell={"textAlign": "left", "padding": "5px"},
                         style_header={"backgroundColor": "#0074D9", "color": "white"}),
], style={"fontFamily": "Arial"})


@app.callback(
    Output("mapa-calor", "figure"),
    Output("grafico-horas", "figure"),
    Output("grafico-tipo", "figure"),
    Output("grafico-clima", "figure"),
    Output("tabela-acidentes", "data"),
    Output("export-feedback", "children"),
    Input("filtro-uf", "value"),
    Input("filtro-br", "value"),
    Input("btn-exportar", "n_clicks")
)
def atualizar_dashboard(ufs, brs, export_clicks):
    df = df_original.copy()

    if ufs:
        df = df[df["uf"].isin(ufs)]
    if brs:
        df = df[df["br"].isin(brs)]

    feedback = ""
    if export_clicks > 0:
        export_path = os.path.join("data", "processed", "export_acidentes_filtrados.csv")
        df.to_csv(export_path, index=False, sep=';')
        feedback = f"Arquivo exportado para: {export_path}"

    fig_mapa = px.density_mapbox(
        df.dropna(subset=["latitude", "longitude"]),
        lat="latitude", lon="longitude", z="km",
        radius=10, zoom=4, center={"lat": -15.8, "lon": -47.9},
        mapbox_style="carto-positron",
        title="🗺️ Mapa de Calor dos Sinistros"
    )

    fig_hora = px.histogram(df, x="hora", nbins=24, title="🕒 Sinistros por Hora")

    fig_tipo = px.histogram(df, x="tipo_acidente", title="💥 Tipos de Sinistros")

    fig_clima = px.histogram(df, x="condicao_metereologica", title="☁️ Sinistros por Condição Climática")

    tabela = df.sort_values("datahora", ascending=False).head(10).to_dict("records")

    return fig_mapa, fig_hora, fig_tipo, fig_clima, tabela, feedback


if __name__ == "__main__":
    app.run(debug=True)