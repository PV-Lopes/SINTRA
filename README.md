# SINTRA - Sistema Inteligente de Análise de Trânsito e Riscos de Acidentes

## 📌 Introdução

**SINTRA V4** é um sistema inteligente desenvolvido para análise de dados de trânsito e predição de riscos de acidentes. O projeto tem como objetivo auxiliar gestores públicos, pesquisadores e agentes de mobilidade urbana na identificação de padrões críticos, contribuindo com a formulação de políticas preventivas e com a melhoria da segurança viária.

Combinando dados reais de acidentes, população e infraestrutura urbana, o sistema utiliza **modelos de aprendizado de máquina** para prever áreas com maior risco e apresenta os resultados de forma acessível por meio de um **dashboard interativo**.

---

## 🚀 Funcionalidades Principais

* Coleta automatizada e pré-processamento de dados públicos (DATATRAN, IBGE, etc.)
* Predição do risco de acidentes com base em múltiplos fatores
* Visualização interativa de sinistros por região e por causa
* Relatórios analíticos em PDF
* Estrutura modular e expansível

---

## 📁 Estrutura do Projeto

```bash
SINTRA_V4/
├── data/
│   ├── raw/                  # Dados brutos de entrada (DATATRAN, IBGE, etc.)
│   ├── processed/            # Dados limpos e tratados
│   └── models/               # Modelos treinados (.pkl)
├── reports/
│   └── relatorio_sinistros.pdf  # Relatório final em PDF
├── src/
│   ├── data_collection.py    # Script de coleta e limpeza de dados
│   ├── dashboard.py          # Interface do dashboard com visualizações
│   └── model.py              # (opcional) Treinamento e avaliação dos modelos
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação do projeto
```

---

## 🛠️ Guia de Instalação

### ✅ Pré-requisitos

* Python 3.9 ou superior
* pip ou ambiente virtual (recomendado)

### 🔧 Passos para instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/SINTRA_V4.git
cd SINTRA_V4/SINTRA-SINTRA_V4
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o dashboard (opcional):

```bash
python src/dashboard.py
```

> Certifique-se de que os arquivos de modelo `.pkl` estejam na pasta correta (`/data/models`) para o funcionamento completo da aplicação.

---

## 📊 Desenvolvimento e Tecnologias

* **Python**: linguagem principal
* **Pandas / NumPy**: manipulação de dados
* **Scikit-learn / Pickle**: criação e exportação dos modelos de ML
* **Plotly / Dash**: visualização de dados em dashboard
* **Matplotlib / Seaborn**: geração de gráficos estatísticos
* **PDFKit**: exportação de relatórios

---

## 📈 Modelo de Machine Learning

O modelo `modelo_risco_acidente.pkl` utiliza regressão logística para prever o risco de acidentes com base em:

* Tipo de via
* Horário
* Condições climáticas
* População local
* Frequência histórica de acidentes

Os dados são padronizados e os modelos treinados usando validação cruzada, garantindo robustez nas previsões.

---

## 📃 Relatórios e Saídas

O projeto gera automaticamente:

* Arquivo `sinistros_processados.csv` com dados prontos para análise
* Arquivo `relatorio_sinistros.pdf` com gráficos e insights
* Dashboard interativo com filtros dinâmicos

---

## 📌 Contribuição

Contribuições são bem-vindas! Abra uma *issue* ou envie um *pull request*. Sugestões de novos modelos, fontes de dados e melhorias na visualização são especialmente encorajadas.

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** – veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

Se quiser, posso gerar esse arquivo `README.md` automaticamente dentro do projeto. Deseja que eu crie o arquivo diretamente no diretório extraído?
