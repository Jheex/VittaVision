import hashlib

import pandas as pd
import streamlit as st

from model.oracle_connection import OracleDatabase

from view.admin.painel_view import AdminPainelView
from view.assistente_ia_view import AssistenteIAView
from view.dashboard_view import DashboardView
from view.header_component import HeaderComponent
from view.hospitais_view import HospitaisView
from view.internacoes_view import InternacoesView
from view.leitos_view import LeitosView
from view.relatorios_view import RelatoriosView


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Vitta Vision",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

if "admin_perfil" not in st.session_state:
    st.session_state.admin_perfil = ""


# ============================================================
# CSS GLOBAL
# ============================================================

st.markdown(
    """
    <style>

        .stApp {
            background:
                radial-gradient(
                    circle at top right,
                    rgba(90, 40, 150, 0.12),
                    transparent 35%
                ),
                linear-gradient(
                    135deg,
                    #070913 0%,
                    #0b0f19 50%,
                    #110c24 100%
                );

            color: #ffffff;
        }

        h1,
        h2,
        h3 {
            color: #ffffff !important;
        }

        .metric-card {
            background:
                linear-gradient(
                    145deg,
                    rgba(18, 24, 38, 0.85),
                    rgba(26, 16, 47, 0.85)
                );

            border:
                1px solid
                rgba(168, 85, 247, 0.20);

            padding: 20px;

            border-radius: 16px;

            box-shadow:
                0 8px 32px
                rgba(0, 0, 0, 0.30);

            margin-bottom: 16px;
        }

        .element-container {
            margin-bottom: 0 !important;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def gerar_hash_senha(senha: str) -> str:
    """
    Gera o mesmo SHA-256 utilizado no cadastro
    dos administradores.
    """

    return hashlib.sha256(
        senha.encode("utf-8")
    ).hexdigest()


# ============================================================
# ADMIN
# ============================================================

class AdminView:
    """
    Tela de login e painel administrativo.

    O login é validado diretamente no Oracle.
    """

    def render(self, db):

        st.title("🔒 Painel Administrativo")
        st.caption(
            "Gerenciamento administrativo do Vitta Vision."
        )

        # ====================================================
        # LOGIN
        # ====================================================

        if not st.session_state.admin_logado:

            st.markdown(
                """
                Faça login com suas credenciais cadastradas
                no banco Oracle para continuar.
                """
            )

            st.markdown("---")

            with st.form("form_login_admin"):

                usuario = st.text_input(
                    "Usuário",
                    placeholder="Digite seu usuário",
                )

                senha = st.text_input(
                    "Senha",
                    type="password",
                    placeholder="Digite sua senha",
                )

                submit_login = st.form_submit_button(
                    "🔐 Entrar",
                    use_container_width=True,
                )

                if submit_login:

                    if not usuario.strip() or not senha:

                        st.warning(
                            "Preencha o usuário e a senha."
                        )

                        return

                    senha_hash = gerar_hash_senha(
                        senha
                    )

                    try:

                        login_valido = db.verificar_login(
                            usuario.strip(),
                            senha_hash,
                        )

                    except Exception as e:

                        st.error(
                            "Erro ao validar o login no Oracle."
                        )

                        st.exception(e)

                        return

                    if login_valido:

                        st.session_state.admin_logado = True

                        st.session_state.admin_perfil = (
                            "Administrador Master"
                        )

                        st.success(
                            "Login realizado com sucesso!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Usuário ou senha incorretos, "
                            "ou conta inativa."
                        )

            return

        # ====================================================
        # PAINEL
        # ====================================================

        AdminPainelView().render()


# ============================================================
# CONTROLLER PRINCIPAL
# ============================================================

class MainController:

    def __init__(self):

        # ----------------------------------------------------
        # Banco Oracle
        # ----------------------------------------------------

        self.db = OracleDatabase()

        # ----------------------------------------------------
        # Model temporário utilizado pelas telas que ainda
        # trabalham com dados mockados.
        # ----------------------------------------------------

        self.model = self.carregar_model()

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        self.header = HeaderComponent()

    # ========================================================
    # MODEL MOCK
    # ========================================================

    def carregar_model(self):

        class ModelMock:

            def get_kpis_ia(self):

                return {
                    "perguntas": 142,
                    "respostas": 138,
                    "tempo": "0.8s",
                    "precisao": "98.4%",
                }

            # ------------------------------------------------

            def get_internacoes_data(self):

                return pd.DataFrame(
                    {
                        "Data": [
                            "Jan/24",
                            "Abr/24",
                            "Jul/24",
                            "Out/24",
                            "Jan/25",
                            "Abr/25",
                            "Jul/25",
                            "Out/25",
                            "Abr/26",
                        ],
                        "Valores": [
                            100,
                            115,
                            130,
                            125,
                            140,
                            160,
                            190,
                            175,
                            120,
                        ],
                    }
                )

            # ------------------------------------------------

            def get_hospitais_data(self):

                return pd.DataFrame(
                    {
                        "Hospital": [
                            "H. Central",
                            "H. Norte",
                            "H. Sul",
                            "H. Leste",
                        ],
                        "Leitos": [
                            150,
                            80,
                            120,
                            95,
                        ],
                    }
                )

        return ModelMock()

    # ========================================================
    # ROTEAMENTO
    # ========================================================

    def run(self):

        params = st.query_params

        pagina_atual = params.get(
            "page",
            "Dashboard",
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        self.header.render(
            pagina_atual
        )

        # ----------------------------------------------------
        # DASHBOARD
        # ----------------------------------------------------

        if pagina_atual == "Dashboard":

            DashboardView().render(
                self.model
            )

        # ----------------------------------------------------
        # ASSISTENTE IA
        # ----------------------------------------------------

        elif pagina_atual == "Assistente IA":

            AssistenteIAView().render(
                self.model
            )

        # ----------------------------------------------------
        # HOSPITAIS
        # ----------------------------------------------------

        elif pagina_atual == "Hospitais":

            HospitaisView().render(
                self.model
            )

        # ----------------------------------------------------
        # INTERNAÇÕES
        # ----------------------------------------------------

        elif pagina_atual == "Internações":

            InternacoesView().render(
                self.model
            )

        # ----------------------------------------------------
        # LEITOS
        # ----------------------------------------------------

        elif pagina_atual == "Leitos":

            LeitosView().render(
                self.model
            )

        # ----------------------------------------------------
        # RELATÓRIOS
        #
        # IMPORTANTE:
        # RelatoriosView recebe o OracleDatabase diretamente.
        # ----------------------------------------------------

        elif pagina_atual == "Relatórios":

            RelatoriosView().render(
                self.db
            )

        # ----------------------------------------------------
        # ADMIN
        # ----------------------------------------------------

        elif pagina_atual == "Admin":

            AdminView().render(
                self.db
            )

        # ----------------------------------------------------
        # PÁGINA DESCONHECIDA
        # ----------------------------------------------------

        else:

            st.warning(
                f"A página `{pagina_atual}` não existe."
            )

            st.info(
                "Volte para o Dashboard utilizando o menu superior."
            )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    app = MainController()

    app.run()