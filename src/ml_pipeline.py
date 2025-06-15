# funcionando porem estou testando ainda 🦊

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# Caminhos
PROCESSED_DIR = "data/processed"
MODEL_DIR = "data/models"
os.makedirs(MODEL_DIR, exist_ok=True)

# 1. Carrega os dados
df = pd.read_csv(os.path.join(PROCESSED_DIR, "acidentes_processados.csv"), sep=';')

# 2. Cria variável alvo: risco alto (1) se houve morto(s), risco baixo (0) caso contrário
df['risco_alto'] = df['mortos'].fillna(0).astype(int).apply(lambda x: 1 if x > 0 else 0)

# 3. Seleção de variáveis explicativas (features)
features = [
    'hora', 'periodo', 'causa_acidente', 'tipo_acidente',
    'condicao_metereologica', 'tipo_pista', 'tracado_via',
    'sentido_via', 'uso_solo', 'populacao'
]

df = df[features + ['risco_alto']].dropna()

# 4. One-hot encoding de variáveis categóricas
df_encoded = pd.get_dummies(df, columns=[
    'periodo', 'causa_acidente', 'tipo_acidente',
    'condicao_metereologica', 'tipo_pista', 'tracado_via',
    'sentido_via', 'uso_solo'
])

X = df_encoded.drop("risco_alto", axis=1)
y = df_encoded["risco_alto"]

# 5. Treina/testa modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Avaliação
y_pred = model.predict(X_test)
print("✅ Avaliação do Modelo (RandomForestClassifier):")
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 7. Salvar o modelo treinado
joblib.dump(model, os.path.join(MODEL_DIR, "modelo_risco_acidente.pkl"))
print("✅ Modelo salvo em data/models/modelo_risco_acidente.pkl")
