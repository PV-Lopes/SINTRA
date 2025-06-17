# src/gerar_relatorio.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import os

CSV_PATH = "data/processed/sinistros_processados.csv"

try:
    df = pd.read_csv(CSV_PATH, sep=';')
    df['datahora'] = pd.to_datetime(df['datahora'], errors='coerce')
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    exit(1)

os.makedirs("reports", exist_ok=True)
pdf_path = "reports/relatorio_sinistros.pdf"

with PdfPages(pdf_path) as pdf:
    try:
        if 'mes' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x="mes", palette="Blues")
            plt.title("📈 Sinistros por Mês")
            pdf.savefig(); plt.close()

        if 'hora' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x="hora", palette="Oranges")
            plt.title("🕒 Distribuição por Hora")
            pdf.savefig(); plt.close()

        if 'tipo_acidente' in df.columns:
            plt.figure(figsize=(12, 6))
            sns.countplot(data=df, y="tipo_acidente", order=df['tipo_acidente'].value_counts().index)
            plt.title("💥 Tipos de Sinistro Mais Frequentes")
            pdf.savefig(); plt.close()

        if 'tipo_veiculo' in df.columns:
            plt.figure(figsize=(12, 6))
            sns.countplot(data=df, y="tipo_veiculo", order=df['tipo_veiculo'].value_counts().index)
            plt.title("🚗 Tipos de Veículos Envolvidos")
            pdf.savefig(); plt.close()

        if 'sexo' in df.columns:
            plt.figure(figsize=(8, 6))
            sns.countplot(data=df, x="sexo", palette="coolwarm")
            plt.title("⚧️ Sexo das Vítimas")
            pdf.savefig(); plt.close()

        if 'faixa_idade' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x="faixa_idade", order=["0-17","18-25","26-40","41-60","61-80","80+"])
            plt.title("🎂 Distribuição por Faixa Etária")
            pdf.savefig(); plt.close()

        if 'br' in df.columns:
            plt.figure(figsize=(12, 6))
            top_brs = df['br'].value_counts().head(10)
            sns.barplot(x=top_brs.index.astype(str), y=top_brs.values)
            plt.title("🛣️ BRs com Mais Sinistros")
            plt.xlabel("BR")
            plt.ylabel("Quantidade")
            pdf.savefig(); plt.close()

        if 'uf' in df.columns:
            plt.figure(figsize=(10, 6))
            sns.countplot(data=df, x="uf", palette="Spectral")
            plt.title("📍 Distribuição por Estado (UF)")
            pdf.savefig(); plt.close()

        if 'municipio' in df.columns:
            plt.figure(figsize=(12, 6))
            top_mun = df['municipio'].value_counts().head(10)
            sns.barplot(y=top_mun.index, x=top_mun.values)
            plt.title("🏙️ Municípios com Mais Sinistros")
            plt.xlabel("Quantidade")
            plt.ylabel("Município")
            pdf.savefig(); plt.close()

        # Página de texto/conclusão
        fig, ax = plt.subplots(figsize=(11.7, 8.3))
        ax.axis("off")

        total = len(df)
        com_coords = df[df['latitude'].notna() & df['longitude'].notna()]
        perc_coords = (len(com_coords) / total) * 100

        texto = (
            "Relatório Técnico - Sistema de Prevenção de Sinistros\n\n"
            "Análise exploratória com base nos dados de sinistros em rodovias federais no ano de 2025.\n\n"
            f"Total de registros analisados: {total}\n"
            f"Total com vítimas: {(df['natureza_sinistro'] == 'Com Vítima').sum() if 'natureza_sinistro' in df.columns else 'N/A'}\n"
            f"Total com mortes: {df['mortos'].sum() if 'mortos' in df.columns else 'N/A'}\n"
            f"Registros com coordenadas válidas: {len(com_coords)} ({perc_coords:.2f}%)\n"
            "\n"
            "Conclusões Preliminares:\n"
            "- A maior parte dos sinistros ocorre entre 7h e 19h.\n"
            "- Colisão é o tipo mais recorrente.\n"
            "- Motocicletas e carros lideram a estatística de envolvimento.\n"
            "- Homens jovens (18-40) são maioria entre as vítimas.\n"
            "- Estados mais populosos concentram maior número de casos.\n"
            "\nRecomendações:\n"
            "• Reforçar sinalização em BRs com alto volume.\n"
            "• Intensificar campanhas educativas para motociclistas.\n"
            "• Monitoramento inteligente em horários críticos.\n"
            f"• Considerar o baixo volume de coordenadas geográficas (apenas {perc_coords:.2f}%) ao interpretar mapas."
        )
        ax.text(0.01, 0.95, texto, va="top", ha="left", fontsize=12, wrap=True)
        pdf.savefig(); plt.close()

    except Exception as e:
        print(f"Erro ao gerar relatório: {e}")

print(f"✅ Relatório salvo em {pdf_path}")
