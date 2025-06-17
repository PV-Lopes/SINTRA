# run_secure_app.py
from flask import Flask, redirect, request, render_template_string
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, UserMixin, current_user
)
import pyotp
import os

# Cria o servidor Flask
server = Flask(__name__)
server.secret_key = os.urandom(24)

# Flask-Login
login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(server)

# Usuário de teste
class User(UserMixin):
    def __init__(self, id):
        self.id = id

users = {"admin": User("admin")}
totp = pyotp.TOTP(pyotp.random_base32())
print("🔐 Código 2FA atual:", totp.now())

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Redireciona raiz para login
@server.route("/")
def index():
    return redirect("/login")

# Tela de login
@server.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        code = request.form.get("code")
        user = users.get(username)
        if user and code == totp.now():
            login_user(user)
            return redirect("/dashboard")  # sem barra final!
        return "Login ou código inválido."

    return render_template_string("""
        <h2>🔐 Login Seguro</h2>
        <form method="POST">
            <input name="username" placeholder="Usuário" required><br><br>
            <input name="code" placeholder="Código 2FA" required><br><br>
            <button type="submit">Entrar</button>
        </form>
        <p style="color: gray;">Usuário: admin<br>Código atual: {{ code }}</p>
    """, code=totp.now())

# Logout
@server.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# Protege /dashboard/
@server.route("/dashboard/")
@login_required
def dash_redirect():
    return redirect("/dashboard")

# Importa o app Dash protegido
import dashboard  # registra no server

# Inicia o servidor
if __name__ == "__main__":
    server.run(debug=True)
