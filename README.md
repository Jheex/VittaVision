# 🏥 VittaVision

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Oracle](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white)

O **VittaVision** é uma aplicação interativa desenvolvida com [Streamlit](https://streamlit.io/) com foco na área da saúde. Seu principal objetivo é o monitoramento e a análise de dados do Sistema Único de Saúde (SUS), oferecendo uma visão clara sobre **internações** e **disponibilidade de leitos**.

A aplicação integra dados locais em arquivos CSV e também se conecta de forma segura a um banco de dados **Oracle Cloud** utilizando Oracle Wallet.

---

## ✨ Funcionalidades

- **Dashboard Interativo:** Visualização de dados médicos em tempo real através do Streamlit.
- **Análise de Leitos e Internações:** Cruzamento de dados de `leitos.csv`, `populacao.csv` e `internacoes.csv`.
- **Conexão Segura:** Integração com banco de dados Oracle utilizando configurações de Wallet (`cwallet.sso`, `ewallet.p12`, `tnsnames.ora`, etc.).
- **Ambiente de Desenvolvimento Preparado:** Configuração completa para uso com DevContainers (Docker) facilitando a padronização do ambiente.

---

## 📁 Estrutura do Projeto

```text
VittaVision_final/
├── .devcontainer/         # Configurações para desenvolvimento isolado (Docker/VS Code)
├── .streamlit/            # Configurações específicas de tema/layout do Streamlit
├── database/
│   └── setup_sus_db.sql   # Script SQL para criação das tabelas e carga inicial do banco (SUS)
├── VittaVision/           # Diretório principal da aplicação
│   └── data/
│       ├── Wallet/        # Arquivos de credenciais e segurança do Oracle Database
│       ├── internacoes.csv# Dataset contendo os registros de internações
│       ├── leitos.csv     # Dataset com informações sobre a ocupação de leitos
│       └── populacao.csv  # Dataset com conteudo sobre a populao
└── .gitignore             # Arquivos e pastas ignorados pelo controle de versão
```

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.8+
- Bibliotecas Python (ex: `streamlit`, `pandas`, `oracledb`)
- Oracle Client configurado (caso necessário para sua arquitetura)

### 1. Clonando e Preparando o Ambiente

Clone o repositório e acesse a pasta do projeto:
```bash
git clone <https://github.com/Jheex/VittaVision>
cd VittaVision_final
```

Crie e ative um ambiente virtual (recomendado):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências da aplicação:
```bash
pip install -r requirements.txt
```

### 2. Configurando o Banco de Dados (Oracle)

O projeto se conecta ao banco de dados utilizando a **Oracle Wallet**.
1. Certifique-se de que os arquivos da sua Wallet (como `cwallet.sso`, `tnsnames.ora`, `sqlnet.ora`) estejam devidamente localizados na pasta `VittaVision/data/Wallet/`.
2. Caso precise inicializar o banco de dados localmente ou em uma nova instância, execute o script SQL disponibilizado:
   ```bash
   database/setup_sus_db.sql
   ```

### 3. Rodando a Aplicação Streamlit

Com o ambiente ativado e as credenciais configuradas, inicie o dashboard:
```bash
streamlit run src/main.py
```
*(A aplicação será aberta automaticamente no seu navegador no endereço `http://localhost:8501`)*

---

## 🛠️ Usando DevContainers (VS Code)
Se você utiliza o VS Code e tem o Docker instalado, pode usar o recurso de **DevContainers** para rodar o projeto sem instalar nada na sua máquina local:
1. Abra a pasta do projeto no VS Code.
2. Quando solicitado, clique em **"Reopen in Container"** (ou use a paleta de comandos).
3. O ambiente será construído automaticamente com base no arquivo `.devcontainer/devcontainer.json`.

---

## 👨‍💻 Desenvolvedor
Desenvolvido para análise de indicadores do SUS [cite: 1].
