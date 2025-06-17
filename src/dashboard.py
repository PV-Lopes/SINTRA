# funcionando, porem em melhoria🦊

import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# --- IMPORTS ADICIONAIS PARA SEGURANÇA ---
from flask import request, redirect, session
# Adicionado 'login_required' para proteger a rota de logout
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import qrcode
import io
import base64
# --- FIM DOS IMPORTS DE SEGURANÇA ---


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

# App Dash
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Dashboard de Sinistros em Rodovias"


# --- INÍCIO DA CONFIGURAÇÃO DE SEGURANÇA ---
server = app.server
server.config['SECRET_KEY'] = 'outra-chave-secreta-muito-forte-e-aleatoria'

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'
# --- FIM DA CONFIGURAÇÃO DE SEGURANÇA ---


# --- INÍCIO DO MODELO DE USUÁRIO ---
class User(UserMixin):
    def __init__(self, id):
        self.id = id

users_db = {
    'aluno@exemplo.com': {
        'password': generate_password_hash('123', method='pbkdf2:sha256'),
        'otp_secret': pyotp.random_base32()
    }
}

@login_manager.user_loader
def load_user(user_id):
    if user_id in users_db:
        return User(user_id)
    return None
# --- FIM DO MODELO DE USUÁRIO ---


# --- INÍCIO DAS ROTAS DE AUTENTICAÇÃO (PÁGINAS DE LOGIN) ---
@server.route('/setup/mfa/<user_email>')
def setup_mfa(user_email):
    if user_email not in users_db:
        return "Usuário não encontrado.", 404
    secret = users_db[user_email]['otp_secret']
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=user_email, issuer_name='Dashboard SIPAT')
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f'''<body style="background-color:{theme_color}; color:{text_color}; text-align:center;">
                <h1>Configure seu App de Autenticação</h1>
                <p>Escaneie o QR Code abaixo com o Google Authenticator ou similar.</p>
                <img src="data:image/png;base64,{img_str}" style="border: 5px solid {accent_color};"/>
                <p>Depois de escanear, volte para a <a href="/login" style="color:{accent_color};">página de login</a>.</p>
            </body>'''

@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users_db and check_password_hash(users_db[email]['password'], password):
            session['email_for_mfa'] = email
            return redirect('/login/mfa')
        else:
            return f'<h1>Usuário ou senha inválidos.</h1><a href="/login">Tente novamente</a>'
    return f'''<body style="background-color:{theme_color}; color:{text_color};">
                <h1>Login - Passo 1 de 2</h1>
                <form method="post">
                    E-mail: <input type="email" name="email" required><br>
                    Senha: <input type="password" name="password" required><br>
                    <input type="submit" value="Próximo">
                </form>
                <p>Primeiro acesso? <a href="/setup/mfa/aluno@exemplo.com" style="color:{accent_color};">Configure seu MFA aqui</a>.</p>
            </body>'''

@server.route('/login/mfa', methods=['GET', 'POST'])
def login_mfa():
    email = session.get('email_for_mfa')
    if not email:
        return redirect('/login')
    if request.method == 'POST':
        otp_code = request.form['otp_code']
        totp = pyotp.TOTP(users_db[email]['otp_secret'])
        if totp.verify(otp_code):
            user = User(email)
            login_user(user)
            session.pop('email_for_mfa', None)
            return redirect('/dashboard')
        else:
            return f'<h1>Código MFA inválido.</h1><a href="/login/mfa">Tente novamente</a>'
    return f'''<body style="background-color:{theme_color}; color:{text_color};">
                <h1>Login - Passo 2 de 2 (MFA)</h1>
                <form method="post">
                    Abra seu app de autenticação e digite o código:<br>
                    <input type="text" name="otp_code" required><br>
                    <input type="submit" value="Verificar e Entrar">
                </form>
            </body>'''

@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')



# --- INÍCIO DA LÓGICA DE EXIBIÇÃO DE PÁGINA ---
def create_dashboard_layout():
    return html.Div([
        
        html.A(
            html.Button("Sair (Logout)", style={'color': 'white', 'backgroundColor': '#d9534f', 'border': 'none', 'padding': '10px', 'cursor': 'pointer'}),
            href='/logout',
            style={'position': 'absolute', 'top': '15px', 'right': '15px', 'textDecoration': 'none'}
        ),
        

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

    ], style={"backgroundColor": theme_color, "fontFamily": "Arial", "position": "relative"}) # Adicionado position: relative

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if current_user.is_authenticated:
        if pathname.startswith('/login'): # Se já está logado, não pode ver a página de login
            return dcc.Location(pathname="/dashboard", id="redirect-to-dash")
        return create_dashboard_layout()
    else: # Se não está logado
        if pathname.startswith('/dashboard'): # Se tentar acessar o dashboard, é redirecionado
            return dcc.Location(pathname="/login", id="redirect-to-login")
        # As rotas de login são cuidadas pelo Flask, aqui apenas retornamos um container vazio para o Dash
        # pois o Flask já está renderizando a página de login por trás.
        return html.Div()

# CALLBACK
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
    # Proteção para garantir que o callback não rode se o layout não estiver visível
    if not current_user.is_authenticated:
        return [px.scatter() for _ in range(5)] + [""] # Retorna figuras vazias

    df = df_original.copy()
    filtros = [
        (mes, 'mes'), (dia, 'dia_semana'), (uf, 'uf'),
        (municipio, 'municipio'), (natureza, 'natureza_sinistro'),
        (tipo, 'tipo_acidente'), (veiculo, 'tipo_veiculo'),
        (envolvido, 'tipo_envolvido'), (sexo, 'sexo'), (idade, 'faixa_idade')
    ]
    for val, col in filtros:
        if val: df = df[df[col].isin(val)]

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    feedback = ""
    if "btn-exportar" in changed_id:
        path = "data/processed/export_filtrado.csv"
        df.to_csv(path, sep=';', index=False)
        feedback = f"CSV exportado para {path}"

    mapa = px.density_mapbox(df, lat="latitude", lon="longitude", z="km", radius=10, zoom=4,
        center={"lat": -15.8, "lon": -47.9}, mapbox_style="carto-darkmatter", title="🗺️ Mapa de Sinistros")

    tipo_fig = px.histogram(df, x="tipo_acidente", title="💥 Tipo de Sinistro")
    veic_fig = px.histogram(df, x="tipo_veiculo", title="🚗 Tipo de Veículo")
    sexo_fig = px.histogram(df, x="sexo", title="⚧️ Sexo da Vítima")
    tendencia = px.histogram(df, x="mes", title="📈 Tendência Mensal de Sinistros")

    for fig in [mapa, tipo_fig, veic_fig, sexo_fig, tendencia]:
        fig.update_layout(template="plotly_dark", paper_bgcolor=theme_color, plot_bgcolor=theme_color, font_color=text_color)

    return mapa, tipo_fig, veic_fig, sexo_fig, tendencia, feedback


if __name__ == "__main__":
    app.run(debug=True)
