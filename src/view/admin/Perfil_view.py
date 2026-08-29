import streamlit as st


class PerfilView:
    """Tela de perfil do usuário administrativo."""

    def render(self, db):

        # =========================================================
        # ESTILOS
        # =========================================================

        st.markdown(
            """
            <style>

            /* =====================================================
               CONTAINER
            ===================================================== */

            .perfil-page {
                max-width: 1180px;
                margin: 0 auto;
                padding: 10px 0 40px 0;
            }

            /* =====================================================
               CABEÇALHO
            ===================================================== */

            .perfil-header {
                margin-top: 8px;
                margin-bottom: 22px;
            }

            .perfil-title-row {
                display: flex;
                align-items: center;
                gap: 14px;
                margin-bottom: 7px;
            }

            .perfil-title-icon {
                width: 42px;
                height: 42px;
                border-radius: 12px;

                display: flex;
                align-items: center;
                justify-content: center;

                background:
                    linear-gradient(
                        135deg,
                        rgba(124, 58, 237, 0.20),
                        rgba(37, 99, 235, 0.20)
                    );

                border: 1px solid rgba(168, 85, 247, 0.28);

                color: #c4b5fd;
                font-size: 21px;

                box-shadow:
                    0 6px 20px rgba(124, 58, 237, 0.12);
            }

            .perfil-title {
                color: #ffffff;
                font-size: 30px;
                font-weight: 750;
                letter-spacing: -0.5px;
                line-height: 1.1;
            }

            .perfil-subtitle {
                color: #94a3b8;
                font-size: 13px;
                margin-left: 56px;
            }

            /* =====================================================
               CARD DE IDENTIDADE
            ===================================================== */

            .identity-card {
                position: relative;
                overflow: hidden;

                background:
                    linear-gradient(
                        135deg,
                        rgba(18, 24, 38, 0.98),
                        rgba(27, 17, 48, 0.98)
                    );

                border: 1px solid rgba(168, 85, 247, 0.24);
                border-radius: 18px;

                padding: 24px 26px;

                margin-bottom: 20px;

                box-shadow:
                    0 12px 35px rgba(0, 0, 0, 0.28);
            }

            .identity-card::before {
                content: "";
                position: absolute;

                width: 220px;
                height: 220px;

                right: -90px;
                top: -120px;

                background: rgba(124, 58, 237, 0.12);

                border-radius: 50%;

                filter: blur(8px);
            }

            .identity-content {
                position: relative;

                display: flex;
                align-items: center;

                gap: 18px;
            }

            .perfil-avatar {
                flex-shrink: 0;

                width: 68px;
                height: 68px;

                border-radius: 18px;

                display: flex;
                align-items: center;
                justify-content: center;

                background:
                    linear-gradient(
                        135deg,
                        #7c3aed,
                        #2563eb
                    );

                color: #ffffff;

                font-size: 27px;
                font-weight: 750;

                box-shadow:
                    0 8px 25px rgba(124, 58, 237, 0.28);
            }

            .identity-info {
                flex: 1;
                min-width: 0;
            }

            .perfil-nome {
                color: #ffffff;
                font-size: 21px;
                font-weight: 700;
                margin-bottom: 3px;
            }

            .perfil-funcao {
                color: #a78bfa;
                font-size: 13px;
                margin-bottom: 5px;
            }

            .perfil-email {
                color: #64748b;
                font-size: 12px;
            }

            /* =====================================================
               STATUS
            ===================================================== */

            .status-area {
                display: flex;
                align-items: center;
                gap: 9px;

                padding: 9px 13px;

                background: rgba(34, 197, 94, 0.07);

                border: 1px solid rgba(34, 197, 94, 0.20);

                border-radius: 10px;

                white-space: nowrap;
            }

            .status-dot {
                width: 8px;
                height: 8px;

                border-radius: 50%;

                background: #22c55e;

                box-shadow:
                    0 0 9px rgba(34, 197, 94, 0.75);
            }

            .status-text {
                color: #4ade80;
                font-size: 12px;
                font-weight: 600;
            }

            /* =====================================================
               CARDS INFERIORES
            ===================================================== */

            .perfil-card {
                height: 100%;

                background:
                    linear-gradient(
                        145deg,
                        rgba(18, 24, 38, 0.96),
                        rgba(24, 18, 42, 0.96)
                    );

                border: 1px solid rgba(255,255,255,0.07);

                border-radius: 16px;

                padding: 23px;

                box-shadow:
                    0 10px 30px rgba(0,0,0,0.22);
            }

            .card-header {
                display: flex;
                align-items: center;
                gap: 12px;

                padding-bottom: 17px;

                border-bottom:
                    1px solid rgba(255,255,255,0.07);

                margin-bottom: 18px;
            }

            .card-icon {
                width: 40px;
                height: 40px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 11px;

                background:
                    linear-gradient(
                        135deg,
                        rgba(124,58,237,0.16),
                        rgba(37,99,235,0.12)
                    );

                border:
                    1px solid rgba(168,85,247,0.18);

                color: #c4b5fd;

                font-size: 18px;
            }

            .card-title {
                color: #ffffff;
                font-size: 17px;
                font-weight: 680;
                margin-bottom: 2px;
            }

            .card-description {
                color: #64748b;
                font-size: 11px;
            }

            /* =====================================================
               INFORMAÇÕES
            ===================================================== */

            .info-item {
                padding: 13px 14px;

                background:
                    rgba(255,255,255,0.025);

                border:
                    1px solid rgba(255,255,255,0.055);

                border-radius: 10px;

                margin-bottom: 9px;

                transition:
                    border-color 0.2s ease,
                    background 0.2s ease;
            }

            .info-item:hover {
                background:
                    rgba(168,85,247,0.035);

                border-color:
                    rgba(168,85,247,0.14);
            }

            .info-label {
                color: #64748b;

                font-size: 10px;

                text-transform: uppercase;

                letter-spacing: 0.8px;

                margin-bottom: 4px;
            }

            .info-value {
                color: #e2e8f0;

                font-size: 13px;

                font-weight: 500;
            }

            /* =====================================================
               FORMULÁRIO DE SENHA
            ===================================================== */

            div[data-testid="stForm"] {
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
            }

            div[data-testid="stForm"] label {
                color: #cbd5e1 !important;
                font-size: 12px !important;
                font-weight: 500 !important;
            }

            div[data-testid="stForm"] input {
                background: rgba(255,255,255,0.045) !important;

                border:
                    1px solid rgba(255,255,255,0.08) !important;

                border-radius: 9px !important;

                color: #ffffff !important;

                height: 42px !important;

                transition:
                    border-color 0.2s ease,
                    box-shadow 0.2s ease;
            }

            div[data-testid="stForm"] input:focus {
                border-color:
                    rgba(168,85,247,0.65) !important;

                box-shadow:
                    0 0 0 2px rgba(168,85,247,0.10) !important;
            }

            div[data-testid="stForm"] button[kind="primary"] {
                background:
                    linear-gradient(
                        135deg,
                        #7c3aed,
                        #2563eb
                    ) !important;

                border: none !important;

                border-radius: 9px !important;

                color: #ffffff !important;

                font-weight: 600 !important;

                min-height: 42px !important;

                box-shadow:
                    0 6px 18px rgba(124,58,237,0.22);

                transition:
                    transform 0.2s ease,
                    box-shadow 0.2s ease;
            }

            div[data-testid="stForm"] button[kind="primary"]:hover {
                transform: translateY(-1px);

                box-shadow:
                    0 8px 24px rgba(124,58,237,0.34);
            }

            /* =====================================================
               DICA DE SEGURANÇA
            ===================================================== */

            .security-tip {
                display: flex;
                align-items: center;
                gap: 12px;

                margin-top: 20px;

                padding: 13px 16px;

                background:
                    linear-gradient(
                        90deg,
                        rgba(37,99,235,0.13),
                        rgba(124,58,237,0.08)
                    );

                border:
                    1px solid rgba(59,130,246,0.18);

                border-radius: 11px;
            }

            .tip-icon {
                font-size: 17px;
            }

            .tip-text {
                color: #94a3b8;
                font-size: 11px;
                line-height: 1.5;
            }

            .tip-text strong {
                color: #60a5fa;
                font-weight: 600;
            }

            /* =====================================================
               RODAPÉ
            ===================================================== */

            .perfil-footer {
                text-align: center;

                color: #475569;

                font-size: 10px;

                margin-top: 25px;
            }

            /* =====================================================
               RESPONSIVO
            ===================================================== */

            @media (max-width: 800px) {

                .identity-content {
                    align-items: flex-start;
                }

                .status-area {
                    display: none;
                }

                .perfil-title {
                    font-size: 25px;
                }

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

        inicial = (
            perfil_nome.strip()[0].upper()
            if perfil_nome
            else "A"
        )

        # =========================================================
        # VOLTAR
        # =========================================================

        if st.button(
            "← Voltar ao Menu Principal",
            key="voltar_perfil"
        ):
            st.session_state.admin_aba_ativa = "Menu Principal"
            st.rerun()

        # =========================================================
        # PÁGINA
        # =========================================================

        st.markdown(
            f"""
            <div class="perfil-page">

                <!-- CABEÇALHO -->

                <div class="perfil-header">

                    <div class="perfil-title-row">

                        <div class="perfil-title-icon">
                            ⚙
                        </div>

                        <div class="perfil-title">
                            Meu Perfil
                        </div>

                    </div>

                    <div class="perfil-subtitle">
                        Gerencie suas informações e credenciais de acesso.
                    </div>

                </div>


                <!-- IDENTIDADE -->

                <div class="identity-card">

                    <div class="identity-content">

                        <div class="perfil-avatar">
                            {inicial}
                        </div>

                        <div class="identity-info">

                            <div class="perfil-nome">
                                {perfil_nome}
                            </div>

                            <div class="perfil-funcao">
                                Administrador do sistema
                            </div>

                            <div class="perfil-email">
                                {usuario_email}
                            </div>

                        </div>

                        <div class="status-area">

                            <div class="status-dot"></div>

                            <div class="status-text">
                                Conta ativa
                            </div>

                        </div>

                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        # =========================================================
        # CARDS
        # =========================================================

        col1, col2 = st.columns(
            [1, 1],
            gap="large"
        )

        # =========================================================
        # INFORMAÇÕES DA CONTA
        # =========================================================

        with col1:

            st.markdown(
                """
                <div class="perfil-card">

                    <div class="card-header">

                        <div class="card-icon">
                            ◉
                        </div>

                        <div>

                            <div class="card-title">
                                Informações da conta
                            </div>

                            <div class="card-description">
                                Dados vinculados à conta administrativa.
                            </div>

                        </div>

                    </div>

                    <div class="info-item">

                        <div class="info-label">
                            Perfil de acesso
                        </div>

                        <div class="info-value">
                            Administrador Master
                        </div>

                    </div>

                    <div class="info-item">

                        <div class="info-label">
                            Login
                        </div>

                        <div class="info-value">
                            {usuario_login}
                        </div>

                    </div>

                    <div class="info-item">

                        <div class="info-label">
                            E-mail
                        </div>

                        <div class="info-value">
                            {usuario_email}
                        </div>

                    </div>

                    <div class="info-item">

                        <div class="info-label">
                            Banco de dados conectado
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
        # SEGURANÇA
        # =========================================================

        with col2:

            st.markdown(
                """
                <div class="perfil-card">

                    <div class="card-header">

                        <div class="card-icon">
                            🔐
                        </div>

                        <div>

                            <div class="card-title">
                                Segurança
                            </div>

                            <div class="card-description">
                                Atualize sua senha de acesso.
                            </div>

                        </div>

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
                    "Atualizar senha",
                    type="primary",
                    width="stretch"
                )

                if alterar:

                    if not senha_atual:

                        st.error(
                            "Digite sua senha atual."
                        )

                    elif not nova_senha:

                        st.error(
                            "Digite a nova senha."
                        )

                    elif len(nova_senha) < 4:

                        st.error(
                            "A nova senha deve possuir pelo menos 4 caracteres."
                        )

                    elif nova_senha != confirmar_senha:

                        st.error(
                            "A confirmação da nova senha não coincide."
                        )

                    else:

                        login_atual = st.session_state.get(
                            "admin_usuario",
                            ""
                        )

                        if not login_atual:
                            login_atual = usuario_email

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
                                    "Senha atualizada com sucesso."
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
                    margin-top: 13px;
                    color: #475569;
                    font-size: 10px;
                ">
                    As credenciais são protegidas por hash SHA-256.
                </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        # =========================================================
        # DICA
        # =========================================================

        st.markdown(
            """
            <div class="perfil-page">

                <div class="security-tip">

                    <div class="tip-icon">
                        💡
                    </div>

                    <div class="tip-text">
                        <strong>Dica de segurança:</strong>
                        nunca compartilhe suas credenciais de administrador
                        com terceiros.
                    </div>

                </div>

                <div class="perfil-footer">
                    Vitta Vision • Área administrativa
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )