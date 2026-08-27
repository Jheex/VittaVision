import streamlit as st
from model.oracle_connection import OracleDatabase
# Importando as views modulares solicitadas
from view.admin.usuarios_view import UsuariosView
from view.admin.database_view import DatabaseView


class AdminPainelView:
    """Painel administrativo modular com cards clicáveis para Usuários e Banco de Dados."""

    def render(self):
        # Inicializa a aba ativa no session_state se não existir
        if "admin_aba_ativa" not in st.session_state:
            st.session_state.admin_aba_ativa = "👥 Usuários"

        # CSS personalizado para estilizar os botões como cards profissionais com efeito hover
        st.markdown(
            """
            <style>
                div.stButton > button {
                    background: linear-gradient(145deg, rgba(18, 24, 38, 0.95) 0%, rgba(26, 16, 47, 0.95) 100%);
                    border: 1px solid rgba(168, 85, 247, 0.25);
                    border-radius: 16px;
                    color: #ffffff;
                    padding: 30px 20px;
                    text-align: left;
                    width: 100%;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    transition: all 0.3s ease;
                }
                div.stButton > button:hover {
                    background: linear-gradient(145deg, rgba(28, 36, 58, 1) 0%, rgba(40, 24, 71, 1) 100%);
                    border-color: rgba(168, 85, 247, 0.8);
                    box-shadow: 0 12px 40px rgba(168, 85, 247, 0.25);
                    transform: translateY(-3px);
                }
                div.stButton > button p {
                    font-size: 18px !important;
                    font-weight: 600 !important;
                    color: #ffffff !important;
                    margin: 0px !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Informações da sessão ativa
        st.info(f"Sessão ativa como **{st.session_state.get('admin_perfil', 'Administrador')}**.")
        st.write("")
        st.markdown("### 📊 Menu Principal")

        # ---------------------------------------------------------
        # CARDS CLICÁVEIS DE NAVEGAÇÃO E SAÍDA
        # ---------------------------------------------------------
        c1, c2, c3 = st.columns(3)

        with c1:
            if st.button("👥 Usuários\n\nGerenciar acessos e cadastros.", key="card_usuarios", use_container_width=True):
                st.session_state.admin_aba_ativa = "👥 Usuários"
                st.rerun()

        with c2:
            if st.button("🗄️ Banco de Dados\n\nConsultas e status do Oracle.", key="card_banco", use_container_width=True):
                st.session_state.admin_aba_ativa = "🗄️ Banco de Dados"
                st.rerun()

        with c3:
            if st.button("🚪 Sair\n\nEncerrar a sessão atual.", key="card_sair", use_container_width=True):
                st.session_state.admin_logado = False
                st.session_state.admin_perfil = ""
                st.session_state.admin_aba_ativa = "👥 Usuários"
                st.rerun()

        st.divider()

        # ---------------------------------------------------------
        # ROTEAMENTO PARA AS VIEWS ESPECÍFICAS
        # ---------------------------------------------------------
        modulo_atual = st.session_state.admin_aba_ativa

        if modulo_atual == "👥 Usuários":
            UsuariosView().render()
        elif modulo_atual == "🗄️ Banco de Dados":
            DatabaseView().render()