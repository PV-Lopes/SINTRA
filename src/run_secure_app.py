import os
from dotenv import load_dotenv
from flask import request, redirect, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import qrcode
import io
import base64
from .dashboard import app

load_dotenv()

# --- INÍCIO DA CONFIGURAÇÃO DE SEGURANÇA ---
server = app.server
server.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'uma-chave-padrao')

# 3. Configura o Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'

# 4. Define o modelo de usuário
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
# --- FIM DA CONFIGURAÇÃO DE SEGURANÇA ---


# --- ROTAS DE AUTENTICAÇÃO (LOGIN, MFA, LOGOUT) ---
@server.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users_db and check_password_hash(users_db[email]['password'], password):
            session['email_for_mfa'] = email
            return redirect('/login/mfa')
        else:
            return get_login_form_html(error="Usuário ou senha inválidos.")
            
    return get_login_form_html()

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
            return redirect('/')
        else:
            return get_mfa_form_html(error="Código MFA inválido.")
            
    return get_mfa_form_html()
    
@server.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@server.route('/setup/mfa/<user_email>')
def setup_mfa(user_email):
    
    if user_email not in users_db: return "Usuário não encontrado.", 404
    secret = users_db[user_email]['otp_secret']
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=user_email, issuer_name='Dashboard SIPAT')
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f'''<body style="text-align:center;">
                <h1>Configure seu App de Autenticação</h1><p>Escaneie o QR Code.</p>
                <img src="data:image/png;base64,{img_str}"/>
                <p>Depois, volte para a <a href="/login">página de login</a>.</p></body>'''
# --- FIM DAS ROTAS DE AUTENTICAÇÃO ---


# --- FUNÇÕES AUXILIARES PARA GERAR AS PÁGINAS DE LOGIN ---

LOGIN_STYLE = """
<style>
    body { font-family: Arial, sans-serif; background-color: #121212; color: #f0f0f0; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .login-container { background-color: #1e1e1e; padding: 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5); text-align: center; width: 100%; max-width: 400px; }
    h1 { color: #1976D2; margin-bottom: 30px; }
    form { display: flex; flex-direction: column; }
    input[type="email"], input[type="password"], input[type="text"] { background-color: #333; border: 1px solid #555; color: #f0f0f0; padding: 12px; margin-bottom: 20px; border-radius: 5px; font-size: 16px; }
    input[type="submit"] { background-color: #1976D2; color: white; border: none; padding: 12px; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background-color 0.3s; }
    input[type="submit"]:hover { background-color: #1565C0; }
    a { color: #1976D2; text-decoration: none; margin-top: 20px; display: inline-block; }
    a:hover { text-decoration: underline; }
    .error { color: #ff5252; margin-top: -10px; margin-bottom: 15px; font-weight: bold; }
</style>
"""
def get_login_form_html(error=None):
    error_html = f'<p style="color:red;">{error}</p>' if error else ""
    return f'''
        <h1>Login - Passo 1 de 2</h1>
        {error_html}
        <form method="post">
            E-mail: <input type="email" name="email" required><br>
            Senha: <input type="password" name="password" required><br>
            <input type="submit" value="Próximo">
        </form>
        <p>Primeiro acesso? <a href="/setup/mfa/aluno@exemplo.com">Configure seu MFA aqui</a>.</p>
    '''
def get_mfa_form_html(error=None):
    error_html = f'<p style="color:red;">{error}</p>' if error else ""
    return f'''
        <h1>Login - Passo 2 de 2 (MFA)</h1>
        {error_html}
        <form method="post">
            Código de Autenticação:<br>
            <input type="text" name="otp_code" required maxlength="6"><br>
            <input type="submit" value="Verificar e Entrar">
        </form>
    '''
# --- FIM DAS FUNÇÕES AUXILIARES ---


# --- O "GUARDA" DE SEGURANÇA ---
@server.before_request
def protect_routes():
    # Permite acesso livre às rotas de login, mfa, setup e arquivos estáticos do Dash
    public_paths = ['/login', '/login/mfa', '/logout']
    if request.path in public_paths or request.path.startswith('/setup/mfa') or request.path.startswith('/_dash'):
        return

    # redireciona para o login
    if not current_user.is_authenticated:
        return redirect('/login')
# --- FIM DO "GUARDA" ---

if __name__ == '__main__':
    app.run(debug=True)