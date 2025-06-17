# dashboard.py
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from flask_login import current_user
from run_secure_app import server  # importa o Flask server autenticado

# Cria o app Dash
app = Dash(__name__,
    server=server,
    url_base_pathname="/dashboard/",
    suppress_callback_exceptions=True
)
app.title = "Dashboard SINTRA"

# Carrega os dados
df = pd.read_csv("data/processed/sinistros_processados.csv", sep=";")
df["datahora"] = pd.to_datetime(df["datahora"], errors="coerce")

# Layout protegido
def secure_layout():
    if not current_user.is_authenticated:
        return html.Div([
            html.H3("⛔ Acesso negado. Faça login em /login", style={"color": "crimson"})
        ])
    
    return html.Div([
        html.H1("📊 Dashboard de Sinistros", style={"textAlign": "center", "color": "#1976D2"}),
        dcc.Dropdown(df["uf"].dropna().unique(), id="filtro-uf", placeholder="Selecione o estado (UF)", style={"marginBottom": "20px"}),
        dcc.Graph(id="grafico-tipo"),
        dcc.Graph(id="grafico-sexo"),
        dcc.Graph(id="grafico-veiculo"),
        dcc.Graph(id="grafico-tendencia"),
        dcc.Graph(id="mapa"),
        html.Br(),
        html.A("🚪 Sair", href="/logout", style={"color": "red", "fontWeight": "bold"})
    ], style={"padding": "30px", "fontFamily": "Arial"})

app.layout = secure_layout

# Callback de visualização
@app.callback(
    Output("grafico-tipo", "figure"),
    Output("grafico-sexo", "figure"),
    Output("grafico-veiculo", "figure"),
    Output("grafico-tendencia", "figure"),
    Output("mapa", "figure"),
    Input("filtro-uf", "value"),
    prevent_initial_call=False
)
def atualizar_dashboard(uf):
    dff = df[df["uf"] == uf] if uf else df.copy()

    fig1 = px.histogram(dff, x="tipo_acidente", title="💥 Tipo de Sinistro")
    fig2 = px.histogram(dff, x="sexo", title="⚧️ Sexo da Vítima")
    fig3 = px.histogram(dff, x="tipo_veiculo", title="🚗 Tipo de Veículo")
    fig4 = px.histogram(dff, x="mes", title="📈 Tendência Mensal")
    fig5 = px.density_mapbox(
        dff.dropna(subset=["latitude", "longitude"]),
        lat="latitude", lon="longitude", z="km", radius=10, zoom=4,
        mapbox_style="carto-darkmatter", title="🗺️ Mapa de Calor"
    )

    for fig in [fig1, fig2, fig3, fig4, fig5]:
        fig.update_layout(template="plotly_dark")

    return fig1, fig2, fig3, fig4, fig5
