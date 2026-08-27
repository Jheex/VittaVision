import pandas as pd
import streamlit as st
from model.oracle_connection import OracleDatabase
from view.admin.painel_View import AdminPainelView
from view.assistente_ia_view import AssistenteIAView
from view.dashboard_view import DashboardView
from view.header_component import HeaderComponent
from view.hospitais_view import HospitaisView
from view.internacoes_view import InternacoesView
from view.leitos_view import LeitosView
from view.relatorios_view import RelatoriosView

st.set_page_config(page_title="Vitta Vision", layout="wide")

# Força o estado da sidebar no session_state para evitar cache
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# Inicializa o estado de autenticação do admin globalmente para evitar perda de sessão
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False
if "admin_perfil" not in st.session_state:
    st.session_state.admin_perfil = ""

# CSS Global aprimorado
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #070913 0%, #0b0f19 50%, #110c24 100%);
            color: #ffffff;
        }
        .metric-card {
            background: linear-gradient(145deg, rgba(18, 24, 38, 0.8) 0%, rgba(26, 16, 47, 0.8) 100%);
            border: 1px solid rgba(168, 85, 247, 0.2);
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            margin-bottom: 16px;
        }
        h1, h2, h3 { color: #ffffff !important; }
        .element-container { margin-bottom: 0px !important; }
    </style>
""",
    unsafe_allow_html=True,
)


class AdminView:
    """View responsável pela tela de Login e Painel do Administrador integrado ao Oracle."""

    def render(self, model):
        st.title("🔒 Painel Administrativo - Vitta Vision")

        # Inicializa a conexão com o banco Oracle
        db = OracleDatabase()

        # Verifica se o admin já está logado
        if not st.session_state.admin_logado:
            st.markdown("Faça login com suas credenciais cadastradas no banco Oracle para continuar.")

            with st.form("form_login_admin"):
                usuario = st.text_input("Usuário")
                senha = st.text_input("Senha", type="password")
                submit_login = st.form_submit_button("Entrar", use_container_width=True)

                if submit_login:
                    if not usuario or not senha:
                        st.warning("Preencha o usuário e a senha.")
                    else:
                        # Validação real consultando o banco Oracle na tabela ALFA_USUARIO
                        if db.verificar_login(usuario, senha):
                            st.session_state.admin_logado = True
                            st.session_state.admin_perfil = "Administrador Master"
                            st.success("Login realizado com sucesso via banco de dados!")
                            st.rerun()
                        else:
                            st.error("Usuário ou senha incorretos, ou conta inativa.")
        else:
            # Se logado, renderiza o painel completo modularizado
            AdminPainelView().render()


class MainController:

    def __init__(self):
        self.model = self.carregar_model()
        self.header = HeaderComponent()

    def carregar_model(self):

        class ModelMock:

            def get_kpis_ia(self):
                return {
                    "perguntas": 142,
                    "respostas": 138,
                    "tempo": "0.8s",
                    "precisao": "98.4%",
                }

            def get_internacoes_data(self):
                return pd.DataFrame({
                    "Data": [
                        "Jan/24", "Abr/24", "Jul/24", "Out/24",
                        "Jan/25", "Abr/25", "Jul/25", "Out/25", "Abr/26"
                    ],
                    "Valores": [100, 115, 130, 125, 140, 160, 190, 175, 120],
                })

            def get_hospitais_data(self):
                return pd.DataFrame({
                    "Hospital": ["H. Central", "H. Norte", "H. Sul", "H. Leste"],
                    "Leitos": [150, 80, 120, 95],
                })

        return ModelMock()

    def run(self):
        params = st.query_params
        pagina_atual = params.get("page", "Dashboard")

        self.header.render(pagina_atual)

        # Roteamento de páginas, incluindo a página Admin
        if pagina_atual == "Dashboard":
            DashboardView().render(self.model)
        elif pagina_atual == "Assistente IA":
            AssistenteIAView().render(self.model)
        elif pagina_atual == "Hospitais":
            HospitaisView().render(self.model)
        elif pagina_atual == "Internações":
            InternacoesView().render(self.model)
        elif pagina_atual == "Leitos":
            LeitosView().render(self.model)
        elif pagina_atual == "Relatórios":
            RelatoriosView().render(self.model)
        elif pagina_atual == "Admin":
            AdminView().render(self.model)


if __name__ == "__main__":
    app = MainController()
    app.run()