
# modelo em teste não funcionado com eu queria🦊

import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Caminhos
PROCESSED_DIR = "data/processed"
MODEL_DIR = "data/models"
os.makedirs(MODEL_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(PROCESSED_DIR, "acidentes_processados.csv"), sep=';')
df['risco_alto'] = df['mortos'].fillna(0).astype(int).apply(lambda x: 1 if x > 0 else 0)

features = [
    'hora', 'periodo', 'causa_acidente', 'tipo_acidente',
    'condicao_metereologica', 'tipo_pista', 'tracado_via',
    'sentido_via', 'uso_solo', 'populacao'
]

df = df[features + ['risco_alto']].dropna()
X = pd.get_dummies(df[features])
y = df['risco_alto']

# Salva colunas para o dashboard usar
joblib.dump(X.columns.tolist(), os.path.join(MODEL_DIR, "modelo_columns.pkl"))

# Treina modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, os.path.join(MODEL_DIR, "modelo_risco_acidente.pkl"))
print("✅ Modelo simples treinado e salvo com sucesso.")