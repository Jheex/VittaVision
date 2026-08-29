import streamlit as st


class PerfilView:
    """Tela de perfil do usuário administrativo."""

    def render(self, db):

        # =========================================================
        # BOTÃO VOLTAR
        # =========================================================

        if st.button("← Voltar ao Menu Principal", key="voltar_perfil"):
            st.session_state.admin_aba_ativa = "Menu Principal"
            st.rerun()

        # =========================================================
        # ESTILOS DA PÁGINA
        # =========================================================

        st.markdown(
            """
            <style>

            /* Container principal */
            .perfil-container {
                max-width: 1050px;
                margin: 20px auto 0 auto;
            }

            /* Cabeçalho */
            .perfil-header {
                margin-bottom: 28px;
            }

            .perfil-title {
                font-size: 30px;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 6px;
            }

            .perfil-subtitle {
                font-size: 14px;
                color: #94a3b8;
            }

            /* Card principal */
            .perfil-card {
                background:
                    linear-gradient(
                        145deg,
                        rgba(18, 24, 38, 0.96),
                        rgba(27, 17, 48, 0.96)
                    );

                border: 1px solid rgba(168, 85, 247, 0.25);
                border-radius: 20px;

                padding: 30px;

                box-shadow:
                    0 15px 45px rgba(0, 0, 0, 0.35);

                margin-bottom: 22px;
            }

            /* Perfil superior */
            .perfil-topo {
                display: flex;
                align-items: center;
                gap: 22px;
                padding-bottom: 25px;
                border-bottom: 1px solid rgba(255,255,255,0.08);
                margin-bottom: 25px;
            }

            /* Avatar */
            .perfil-avatar {
                width: 76px;
                height: 76px;

                border-radius: 50%;

                display: flex;
                align-items: center;
                justify-content: center;

                background:
                    linear-gradient(
                        135deg,
                        #7c3aed,
                        #2563eb
                    );

                color: white;

                font-size: 30px;
                font-weight: 700;

                box-shadow:
                    0 8px 25px rgba(124, 58, 237, 0.35);
            }

            .perfil-nome {
                font-size: 25px;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 4px;
            }

            .perfil-funcao {
                font-size: 14px;
                color: #a78bfa;
            }

            /* Status */
            .status-badge {
                display: inline-flex;
                align-items: center;
                gap: 7px;

                background: rgba(34, 197, 94, 0.10);
                border: 1px solid rgba(34, 197, 94, 0.25);

                color: #4ade80;

                padding: 6px 12px;
                border-radius: 20px;

                font-size: 12px;
                font-weight: 600;
            }

            .status-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #22c55e;
                box-shadow: 0 0 8px rgba(34,197,94,0.8);
            }

            /* Informações */
            .info-label {
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.7px;
                color: #64748b;
                margin-bottom: 5px;
            }

            .info-value {
                font-size: 15px;
                color: #e2e8f0;
                font-weight: 500;
            }

            .info-box {
                background: rgba(255,255,255,0.025);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 12px;
                padding: 15px 17px;
                margin-bottom: 12px;
            }

            /* Segurança */
            .security-title {
                font-size: 20px;
                font-weight: 650;
                color: #ffffff;
                margin-bottom: 5px;
            }

            .security-description {
                font-size: 13px;
                color: #94a3b8;
                margin-bottom: 20px;
            }

            /* Ícone de segurança */
            .security-icon {
                width: 46px;
                height: 46px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 12px;

                background: rgba(168,85,247,0.12);
                border: 1px solid rgba(168,85,247,0.2);

                font-size: 21px;
                margin-bottom: 15px;
            }

            /* Rodapé */
            .perfil-footer {
                text-align: center;
                color: #475569;
                font-size: 12px;
                margin-top: 25px;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

        # =========================================================
        # DADOS DA SESSÃO
        # =========================================================

        perfil_nome = st.session_state.get(
            "admin_perfil",
            "Administrador"
        )

        usuario_email = st.session_state.get(
            "admin_email",
            "admin@vittavision.com"
        )

        usuario_login = st.session_state.get(
            "admin_usuario",
            "Administrador"
        )

        # Inicial do nome
        inicial = perfil_nome.strip()[0].upper() if perfil_nome else "A"

        # =========================================================
        # CABEÇALHO
        # =========================================================

        st.markdown(
            """
            <div class="perfil-container">
                <div class="perfil-header">
                    <div class="perfil-title">
                        Meu Perfil
                    </div>

                    <div class="perfil-subtitle">
                        Gerencie suas informações e credenciais de acesso.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # =========================================================
        # CARD DO PERFIL
        # =========================================================

        st.markdown(
            f"""
            <div class="perfil-container">
                <div class="perfil-card">

                    <div class="perfil-topo">

                        <div class="perfil-avatar">
                            {inicial}
                        </div>

                        <div style="flex:1">

                            <div class="perfil-nome">
                                {perfil_nome}
                            </div>

                            <div class="perfil-funcao">
                                Administrador do sistema
                            </div>

                        </div>

                        <div class="status-badge">
                            <span class="status-dot"></span>
                            Conta ativa
                        </div>

                    </div>

                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # =========================================================
        # INFORMAÇÕES DA CONTA
        # =========================================================

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                """
                <div class="perfil-card">

                    <div class="security-icon">
                        👤
                    </div>

                    <div class="security-title">
                        Informações da conta
                    </div>

                    <div class="security-description">
                        Dados vinculados à sua conta administrativa.
                    </div>

                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                    <div class="info-box">
                        <div class="info-label">
                            Nome
                        </div>

                        <div class="info-value">
                            {perfil_nome}
                        </div>
                    </div>

                    <div class="info-box">
                        <div class="info-label">
                            Login
                        </div>

                        <div class="info-value">
                            {usuario_login}
                        </div>
                    </div>

                    <div class="info-box">
                        <div class="info-label">
                            E-mail
                        </div>

                        <div class="info-value">
                            {usuario_email}
                        </div>
                    </div>

                    <div class="info-box">
                        <div class="info-label">
                            Banco de dados
                        </div>

                        <div class="info-value">
                            Oracle Database
                        </div>
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        # =========================================================
        # ALTERAÇÃO DE SENHA
        # =========================================================

        with col2:

            st.markdown(
                """
                <div class="perfil-card">

                    <div class="security-icon">
                        🔐
                    </div>

                    <div class="security-title">
                        Segurança
                    </div>

                    <div class="security-description">
                        Altere sua senha de acesso ao sistema.
                    </div>

                """,
                unsafe_allow_html=True,
            )

            with st.form("form_alterar_senha_perfil"):

                senha_atual = st.text_input(
                    "Senha atual",
                    type="password",
                    placeholder="Digite sua senha atual"
                )

                nova_senha = st.text_input(
                    "Nova senha",
                    type="password",
                    placeholder="Digite a nova senha"
                )

                confirmar_senha = st.text_input(
                    "Confirmar nova senha",
                    type="password",
                    placeholder="Digite novamente a nova senha"
                )

                alterar = st.form_submit_button(
                    "🔒 Atualizar senha",
                    type="primary",
                    width="stretch"
                )

                if alterar:

                    if not senha_atual:
                        st.error("Digite sua senha atual.")

                    elif not nova_senha:
                        st.error("Digite a nova senha.")

                    elif len(nova_senha) < 4:
                        st.error(
                            "A nova senha deve possuir pelo menos 4 caracteres."
                        )

                    elif nova_senha != confirmar_senha:
                        st.error(
                            "A confirmação da nova senha não coincide."
                        )

                    else:

                        # -------------------------------------------------
                        # Recupera o login atual
                        # -------------------------------------------------

                        login_atual = st.session_state.get(
                            "admin_usuario",
                            ""
                        )

                        if not login_atual:
                            login_atual = usuario_email

                        # -------------------------------------------------
                        # Importação local para evitar dependência circular
                        # -------------------------------------------------

                        import hashlib

                        senha_atual_hash = hashlib.sha256(
                            senha_atual.strip().encode()
                        ).hexdigest()

                        nova_senha_hash = hashlib.sha256(
                            nova_senha.strip().encode()
                        ).hexdigest()

                        try:

                            sucesso = db.alterar_senha_usuario(
                                login_atual,
                                senha_atual_hash,
                                nova_senha_hash
                            )

                            if sucesso:
                                st.success(
                                    "Senha atualizada com sucesso!"
                                )

                            else:
                                st.error(
                                    "Não foi possível alterar a senha. "
                                    "Verifique sua senha atual."
                                )

                        except AttributeError:

                            st.error(
                                "O método alterar_senha_usuario() "
                                "não foi encontrado no OracleDatabase."
                            )

            st.markdown(
                """
                    <div style="
                        margin-top: 12px;
                        font-size: 12px;
                        color: #64748b;
                    ">
                        🔒 Sua senha é armazenada utilizando hash
                        SHA-256.
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        # =========================================================
        # RODAPÉ
        # =========================================================

        st.markdown(
            """
            <div class="perfil-footer">
                Vitta Vision • Área administrativa
            </div>
            """,
            unsafe_allow_html=True,
        )


class AdminPainelView:
    """Painel administrativo."""

    def render(self):

        db = OracleDatabase()

        if "admin_aba_ativa" not in st.session_state:
            st.session_state.admin_aba_ativa = "Menu Principal"

        if st.session_state.admin_aba_ativa != "Menu Principal":

            if st.session_state.admin_aba_ativa == "Módulo Acessos":

                if st.button(
                    "← Voltar ao Menu Principal",
                    key="voltar_acessos"
                ):
                    st.session_state.admin_aba_ativa = "Menu Principal"
                    st.rerun()

                UsuariosView().render(db)

            elif st.session_state.admin_aba_ativa == "Módulo de Tabelas":

                if st.button(
                    "← Voltar ao Menu Principal",
                    key="voltar_tabelas"
                ):
                    st.session_state.admin_aba_ativa = "Menu Principal"
                    st.rerun()

                DatabaseView().render(db)

            elif st.session_state.admin_aba_ativa == "Meu Perfil":

                PerfilView().render(db)

            return

        # =========================================================
        # MENU PRINCIPAL
        # =========================================================

        st.markdown(
            """
            <style>

            div.stButton > button {
                background:
                    linear-gradient(
                        145deg,
                        rgba(18, 24, 38, 0.95),
                        rgba(26, 16, 47, 0.95)
                    );

                border: 1px solid rgba(168, 85, 247, 0.25);
                border-radius: 16px;

                color: #ffffff;

                padding: 30px 24px;

                text-align: left;
                width: 100%;

                box-shadow:
                    0 8px 30px rgba(0, 0, 0, 0.4);

                transition: all 0.3s ease;
            }

            div.stButton > button:hover {
                background:
                    linear-gradient(
                        145deg,
                        rgba(28, 36, 58, 1),
                        rgba(40, 24, 71, 1)
                    );

                border-color: rgba(168, 85, 247, 0.8);

                box-shadow:
                    0 12px 40px rgba(168, 85, 247, 0.3);

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

            if st.button(
                "👥 **Módulo Acessos**\n\n"
                "Gerenciar acessos e cadastros.",
                key="card_acessos",
                width="stretch"
            ):
                st.session_state.admin_aba_ativa = "Módulo Acessos"
                st.rerun()

        with row1_col2:

            if st.button(
                "🗄️ **Módulo de Tabelas**\n\n"
                "Consultas e status do Oracle.",
                key="card_tabelas",
                width="stretch"
            ):
                st.session_state.admin_aba_ativa = "Módulo de Tabelas"
                st.rerun()

        st.write("")

        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:

            if st.button(
                "⚙️ **Meu Perfil**\n\n"
                "Visualizar dados da conta ativa.",
                key="card_perfil",
                width="stretch"
            ):
                st.session_state.admin_aba_ativa = "Meu Perfil"
                st.rerun()

        with row2_col2:

            if st.button(
                "🚪 **Sair do Sistema**\n\n"
                "Encerrar a sessão atual.",
                key="card_sair",
                width="stretch"
            ):
                st.session_state.admin_logado = False
                st.session_state.admin_perfil = ""
                st.session_state.admin_usuario = ""
                st.session_state.admin_email = ""
                st.session_state.admin_aba_ativa = "Menu Principal"

                st.rerun()