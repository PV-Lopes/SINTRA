# gerar_hash.py
from werkzeug.security import generate_password_hash

# Peça ao usuário para digitar a senha de forma segura
password = input("Digite a senha que você quer usar no seu app: ")

# Gere o hash
hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

print("\nCopia e guarde este hash! Este é o valor que você deve usar como variável de ambiente.\n")
print(hashed_password)