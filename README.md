

📌 **Introdução**

SINTRA é um sistema inteligente desenvolvido para análise de dados de trânsito e predição de riscos de acidentes. O projeto tem como objetivo auxiliar gestores públicos, pesquisadores e agentes de mobilidade urbana na identificação de padrões críticos, contribuindo com a formulação de políticas preventivas e com a melhoria da segurança viária.
Combinando dados reais de acidentes, população e infraestrutura urbana, o sistema utiliza modelos de aprendizado de máquina para prever áreas com maior risco e apresenta os resultados de forma acessível por meio de um dashboard interativo.

🚀 **Funcionalidades Principais**

* Coleta automatizada e pré-processamento de dados públicos (DATATRAN, IBGE, etc.)
* Predição do risco de acidentes com base em múltiplos fatores
* Visualização interativa de sinistros por região e por causa
* Relatórios analíticos em PDF
* Estrutura modular e expansível

📁 **Estrutura do Projeto**

SINTRA/
├── data/
│   ├── raw/                      # Dados brutos de entrada (DATATRAN, IBGE, etc.)
│   ├── processed/                # Dados limpos e tratados
│   └── models/                   # Modelos treinados (.pkl)
├── reports/
│   └── relatorio_sinistros.pdf   # Relatório final em PDF
├── src/
│   ├── data_collection.py        # Script de coleta de dados
│   ├── data_processing_pandas.py # Script de Limpeza de dados
│   ├── gerar_relatorio.py        # Gera o relatorio do /reports
│   └── dashboard.py              # Interface do dashboard com visualizações
├── run_secure_app.py             # Ponto de entrada da aplicação com camada de segurança
├── requirements.txt              # Dependências do projeto
├── Dockerfile                    # Configuração do contêiner para deploy
├── .env                          # Arquivo para variáveis de ambiente locais (NÃO ENVIAR PARA O GIT)
└── README.md                     # Documentação do projeto


🛠️ **Guia de Instalação**

✅ **Pré-requisitos**

* Python 3.9 ou superior
* pip ou ambiente virtual (recomendado)

🔧 **Passos para instalação**

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/PV-Lopes/SINTRA.git](https://github.com/PV-Lopes/SINTRA.git)
    cd SINTRA
    ```

2.  Crie um ambiente virtual (opcional):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  **[IMPORTANTE]** Crie o arquivo de ambiente para a chave secreta:
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Adicione o seguinte conteúdo a ele:
        ```
        SECRET_KEY="coloque_aqui_uma_string_longa_e_aleatoria_para_sua_seguranca"
        ```

5.  Execute a aplicação segura:
    ```bash
    python run_secure_app.py
    ```

6.  Acesse a aplicação:
    * Para configurar o MFA pela primeira vez, acesse `http://127.0.0.1:8050/setup/mfa/aluno@exemplo.com`.
    * Para fazer login, acesse `http://127.0.0.1:8050/login`.
    * O dashboard estará disponível em `http://127.0.0.1:8050/` após o login.

📊 **Desenvolvimento e Tecnologias**

* **Python:** linguagem principal
* **Pandas / NumPy:** manipulação de dados
* **Scikit-learn / Pickle:** criação e exportação dos modelos de ML
* **Plotly / Dash:** visualização de dados em dashboard
* **Flask / Flask-Login:** camada de segurança e autenticação
* **PyOTP:** geração de senhas de uso único para MFA
* **Gunicorn:** servidor de aplicação para produção

📈 **Modelo de Machine Learning**

O modelo `modelo_risco_acidente.pkl` utiliza regressão logística para prever o risco de acidentes com base em:
* Tipo de via
* Horário
* Condições climáticas
* População local
* Frequência histórica de acidentes

Os dados são padronizados e os modelos treinados usando validação cruzada, garantindo robustez nas previsões.

📃 **Relatórios e Saídas**

O projeto gera automaticamente:
* Arquivo `sinistros_processados.csv` com dados prontos para análise
* Arquivo `relatorio_sinistros.pdf` com gráficos e insights
* Dashboard interativo com filtros dinâmicos

🔐 **Segurança Implementada**

O acesso ao dashboard é protegido por uma camada de autenticação para garantir que apenas usuários autorizados possam visualizar os dados. As seguintes funcionalidades foram implementadas:
* **Autenticação de Usuário:** Sistema de login com e-mail e senha utilizando Flask-Login para gerenciar as sessões de forma segura.
* **Autenticação de Múltiplos Fatores (MFA):** Suporte para senhas de uso único baseadas em tempo (TOTP), compatível com aplicativos como Google Authenticator, utilizando a biblioteca `pyotp`.
* **Proteção de Rotas:** Acesso ao dashboard e suas funcionalidades internas é bloqueado para usuários não autenticados.
* **Uso de Variáveis de Ambiente:** A `SECRET_KEY`, utilizada para assinar as sessões de usuário, é carregada a partir de variáveis de ambiente e não está exposta no código-fonte, seguindo as melhores práticas de segurança.

☁️ **Implantação na Nuvem (Render)**

Esta aplicação está configurada para deploy na plataforma **Render**, uma alternativa moderna que não exige cartão de crédito para os planos gratuitos.
* **Containerização com Docker:** O projeto utiliza um `Dockerfile` para empacotar a aplicação e todas as suas dependências em um contêiner, garantindo um ambiente consistente e reprodutível da máquina local para a produção.
* **Deploy Contínuo:** O serviço no Render está conectado ao repositório do GitHub, permitindo que novas versões sejam implantadas automaticamente a cada `push` para a branch principal.
* **URL da Aplicação:** A aplicação está disponível publicamente no seguinte endereço:
    * [link-do-seu-dashboard.onrender.com](https://link-do-seu-dashboard.onrender.com) (substitua pelo seu link real)

📌 **Contribuição**

Contribuições são bem-vindas! Abra uma `issue` ou envie um `pull request`. Sugestões de novos modelos, fontes de dados e melhorias na visualização são especialmente encorajadas.
