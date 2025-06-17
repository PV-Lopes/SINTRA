from flask import Flask, session
import secrets

server = Flask(__name__)
server.secret_key = secrets.token_hex(16)

VALID_USER = "admin"
VALID_CODE = "123456"

def autenticar(usuario, codigo):
    if usuario == VALID_USER and codigo == VALID_CODE:
        session['logado'] = True
        return True
    return False

def deslogar():
    session.clear()
