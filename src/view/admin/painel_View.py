import streamlit as st
from model.oracle_connection import OracleDatabase
from view.admin.usuarios_view import UsuariosView
from view.admin.database_view import DatabaseView


class PerfilView:
    """View dedicada para gerenciar os dados de login e perfil administrativo."""

    def render(self, db):
        if st.button("← Voltar ao Menu Principal", key="voltar_perfil"):
            st.session_state.admin_aba_ativa = "Menu Principal"
            st.rerun()

        st.markdown("### ⚙️ Meu Perfil e Credenciais")
        st.write("Gerencie as informações da sua sessão ativa e diretrizes de acesso.")
        st.write("")

        perfil_nome = st.session_state.get('admin_perfil', 'Administrador')
        usuario_email = st.session_state.get('admin_email', 'admin@vittavision.com')

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📋 Informações da Conta")
            st.text_input("Perfil de Acesso", value=perfil_nome, disabled=True)
            st.text_input("E-mail de Login", value=usuario_email, disabled=True)
            st.text_input("Banco de Dados Conectado", value="Oracle Database (ALFA)", disabled=True)

        with col2:
            st.markdown("#### 🔒 Segurança e Senha")
            with st.form("form_alterar_senha"):
                senha_atual = st.text_input("Senha Atual", type="password")
                nova_senha = st.text_input("Nova Senha", type="password")
                confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
                
                submitted = st.form_submit_button("Atualizar Senha")
                if submitted:
                    if not senha_atual or not nova_senha or not confirmar_senha:
                        st.error("Preencha todos os campos de senha.")
                    elif nova_senha != confirmar_senha:
                        st.error("A nova senha e a confirmação não coincidem.")
                    else:
                        st.success("Senha atualizada com sucesso no sistema!")

        st.divider()
        st.info("💡 **Dica de Segurança:** Nunca compartilhe suas credenciais de administrador com terceiros.")


class AdminPainelView:
    """Painel administrativo onde cada módulo abre em formato de página dedicada."""

    def render(self):
        db = OracleDatabase()

        if "admin_aba_ativa" not in st.session_state:
            st.session_state.admin_aba_ativa = "Menu Principal"

        if st.session_state.admin_aba_ativa != "Menu Principal":
            
            if st.session_state.admin_aba_ativa == "Módulo Acessos":
                if st.button("← Voltar ao Menu Principal", key="voltar_acessos"):
                    st.session_state.admin_aba_ativa = "Menu Principal"
                    st.rerun()
                UsuariosView().render(db)
                
            elif st.session_state.admin_aba_ativa == "Módulo de Tabelas":
                if st.button("← Voltar ao Menu Principal", key="voltar_tabelas"):
                    st.session_state.admin_aba_ativa = "Menu Principal"
                    st.rerun()
                DatabaseView().render(db)
                
            elif st.session_state.admin_aba_ativa == "Meu Perfil":
                PerfilView().render(db)
                
            return  

        # ---------------------------------------------------------
        # TELA INICIAL DO PAINEL (Apenas os cards 2x2)
        # ---------------------------------------------------------
        st.markdown(
            """
            <style>
                div.stButton > button {
                    background: linear-gradient(145deg, rgba(18, 24, 38, 0.95) 0%, rgba(26, 16, 47, 0.95) 100%);
                    border: 1px solid rgba(168, 85, 247, 0.25);
                    border-radius: 16px;
                    color: #ffffff;
                    padding: 30px 24px;
                    text-align: left;
                    width: 100%;
                    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
                    transition: all 0.3s ease;
                }
                div.stButton > button:hover {
                    background: linear-gradient(145deg, rgba(28, 36, 58, 1) 0%, rgba(40, 24, 71, 1) 100%);
                    border-color: rgba(168, 85, 247, 0.8);
                    box-shadow: 0 12px 40px rgba(168, 85, 247, 0.3);
                    transform: translateY(-3px);
                }
                div.stButton > button p {
                    margin: 0px !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("## 🔒 Painel Administrativo")
        st.write("")

        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            if st.button("👥 **Módulo Acessos**\n\nGerenciar acessos e cadastros.", key="card_acessos", use_container_width=True):
                st.session_state.admin_aba_ativa = "Módulo Acessos"
                st.rerun()

        with row1_col2:
            if st.button("🗄️ **Módulo de Tabelas**\n\nConsultas e status do Oracle.", key="card_tabelas", use_container_width=True):
                st.session_state.admin_aba_ativa = "Módulo de Tabelas"
                st.rerun()

        st.write("")  

        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            if st.button("⚙️ **Meu Perfil**\n\nVisualizar dados da conta ativa.", key="card_perfil", use_container_width=True):
                st.session_state.admin_aba_ativa = "Meu Perfil"
                st.rerun()

        with row2_col2:
            if st.button("🚪 **Sair do Sistema**\n\nEncerrar a sessão atual.", key="card_sair", use_container_width=True):
                st.session_state.admin_logado = False
                st.session_state.admin_perfil = ""
                st.session_state.admin_aba_ativa = "Menu Principal"
                st.rerun()