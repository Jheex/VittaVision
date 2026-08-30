import streamlit as st

from model.oracle_connection import OracleDatabase
from view.admin.usuarios_view import UsuariosView
from view.admin.database_view import DatabaseView
from view.admin.perfil_view import PerfilView


class AdminPainelView:
    """
    Painel administrativo principal do Vitta Vision.

    Responsável por:
    - Navegação entre módulos administrativos
    - Gerenciamento de usuários
    - Acesso ao banco de dados
    - Visualização do perfil
    - Encerramento da sessão
    """

    def render(self):

        db = OracleDatabase()

        # =====================================================
        # CONTROLE DA ABA ATIVA
        # =====================================================

        if "admin_aba_ativa" not in st.session_state:
            st.session_state.admin_aba_ativa = "Menu Principal"

        # =====================================================
        # MÓDULOS INTERNOS
        # =====================================================

        if st.session_state.admin_aba_ativa != "Menu Principal":

            # =================================================
            # MÓDULO ACESSOS
            # =================================================

            if (
                st.session_state.admin_aba_ativa
                == "Módulo Acessos"
            ):

                st.html(
                    """
                    <style>

                        .admin-inner-header {
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            gap: 20px;
                            margin-bottom: 24px;
                            padding-bottom: 18px;
                            border-bottom: 1px solid
                                rgba(255,255,255,0.07);
                        }

                        .admin-inner-title {
                            font-family: Arial, sans-serif;
                            font-size: 25px;
                            font-weight: 800;
                            color: #f8fafc;
                            letter-spacing: -0.03em;
                        }

                        .admin-inner-subtitle {
                            margin-top: 5px;
                            font-family: Arial, sans-serif;
                            font-size: 13px;
                            color: #64748b;
                        }

                    </style>

                    <div class="admin-inner-header">

                        <div>

                            <div class="admin-inner-title">
                                👥 Gerenciamento de Acessos
                            </div>

                            <div class="admin-inner-subtitle">
                                Controle usuários, permissões e acessos
                                ao ambiente administrativo.
                            </div>

                        </div>

                    </div>
                    """
                )

                if st.button(
                    "← Voltar ao Menu Principal",
                    key="voltar_acessos",
                ):
                    st.session_state.admin_aba_ativa = (
                        "Menu Principal"
                    )
                    st.rerun()

                st.write("")

                UsuariosView().render(db)

            # =================================================
            # MÓDULO TABELAS
            # =================================================

            elif (
                st.session_state.admin_aba_ativa
                == "Módulo de Tabelas"
            ):

                st.html(
                    """
                    <style>

                        .admin-inner-header {
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            gap: 20px;
                            margin-bottom: 24px;
                            padding-bottom: 18px;
                            border-bottom: 1px solid
                                rgba(255,255,255,0.07);
                        }

                        .admin-inner-title {
                            font-family: Arial, sans-serif;
                            font-size: 25px;
                            font-weight: 800;
                            color: #f8fafc;
                            letter-spacing: -0.03em;
                        }

                        .admin-inner-subtitle {
                            margin-top: 5px;
                            font-family: Arial, sans-serif;
                            font-size: 13px;
                            color: #64748b;
                        }

                    </style>

                    <div class="admin-inner-header">

                        <div>

                            <div class="admin-inner-title">
                                🗄️ Banco de Dados
                            </div>

                            <div class="admin-inner-subtitle">
                                Consulte tabelas, estruturas e informações
                                do Oracle Database.
                            </div>

                        </div>

                    </div>
                    """
                )

                if st.button(
                    "← Voltar ao Menu Principal",
                    key="voltar_tabelas",
                ):
                    st.session_state.admin_aba_ativa = (
                        "Menu Principal"
                    )
                    st.rerun()

                st.write("")

                DatabaseView().render(db)

            # =================================================
            # MEU PERFIL
            # =================================================

            elif (
                st.session_state.admin_aba_ativa
                == "Meu Perfil"
            ):

                st.html(
                    """
                    <style>

                        .admin-inner-header {
                            margin-bottom: 24px;
                            padding-bottom: 18px;
                            border-bottom: 1px solid
                                rgba(255,255,255,0.07);
                        }

                        .admin-inner-title {
                            font-family: Arial, sans-serif;
                            font-size: 25px;
                            font-weight: 800;
                            color: #f8fafc;
                            letter-spacing: -0.03em;
                        }

                        .admin-inner-subtitle {
                            margin-top: 5px;
                            font-family: Arial, sans-serif;
                            font-size: 13px;
                            color: #64748b;
                        }

                    </style>

                    <div class="admin-inner-header">

                        <div class="admin-inner-title">
                            ⚙️ Meu Perfil
                        </div>

                        <div class="admin-inner-subtitle">
                            Informações da conta administrativa
                            atualmente autenticada.
                        </div>

                    </div>
                    """
                )

                PerfilView().render(db)

            return

        # =====================================================
        # CSS DO MENU PRINCIPAL
        # =====================================================

        st.html(
            """
            <style>

                /* =================================================
                   CONTAINER PRINCIPAL
                   ================================================= */

                .admin-page {

                    width: 100%;

                    max-width: 1250px;

                    margin: 0 auto;

                    padding:
                        28px 18px 45px 18px;

                    box-sizing: border-box;

                    font-family: Arial, sans-serif;

                    color: #ffffff;
                }


                /* =================================================
                   HEADER PRINCIPAL
                   ================================================= */

                .admin-main-header {

                    display: flex;

                    justify-content: space-between;

                    align-items: center;

                    gap: 30px;

                    padding:
                        30px 34px;

                    border-radius: 22px;

                    border:
                        1px solid
                        rgba(168, 85, 247, 0.18);

                    background:
                        linear-gradient(
                            135deg,
                            rgba(15, 23, 42, 0.96),
                            rgba(27, 17, 52, 0.96)
                        );

                    box-shadow:
                        0 20px 60px
                        rgba(0, 0, 0, 0.30);

                    position: relative;

                    overflow: hidden;

                    margin-bottom: 22px;
                }


                .admin-main-header::before {

                    content: "";

                    position: absolute;

                    width: 350px;

                    height: 350px;

                    top: -230px;

                    right: -100px;

                    border-radius: 50%;

                    background:
                        radial-gradient(
                            circle,
                            rgba(124, 58, 237, 0.20),
                            transparent 70%
                        );

                    pointer-events: none;
                }


                .admin-main-header::after {

                    content: "";

                    position: absolute;

                    width: 280px;

                    height: 280px;

                    bottom: -220px;

                    left: 25%;

                    border-radius: 50%;

                    background:
                        radial-gradient(
                            circle,
                            rgba(37, 99, 235, 0.12),
                            transparent 70%
                        );

                    pointer-events: none;
                }


                /* =================================================
                   HEADER ESQUERDO
                   ================================================= */

                .admin-header-left {

                    position: relative;

                    z-index: 2;

                    flex: 1;
                }


                .admin-eyebrow {

                    display: flex;

                    align-items: center;

                    gap: 9px;

                    color: #94a3b8;

                    font-size: 11px;

                    font-weight: 600;

                    text-transform: uppercase;

                    letter-spacing: 0.10em;

                    margin-bottom: 10px;
                }


                .admin-eyebrow-dot {

                    width: 7px;

                    height: 7px;

                    min-width: 7px;

                    border-radius: 50%;

                    background: #34d399;

                    box-shadow:
                        0 0 10px
                        rgba(52, 211, 153, 0.75);
                }


                .admin-title {

                    font-size: 32px;

                    line-height: 1.15;

                    font-weight: 800;

                    letter-spacing: -0.04em;

                    background:
                        linear-gradient(
                            90deg,
                            #f8fafc,
                            #dbeafe 45%,
                            #c4b5fd
                        );

                    -webkit-background-clip: text;

                    -webkit-text-fill-color: transparent;

                    background-clip: text;
                }


                .admin-description {

                    max-width: 650px;

                    margin-top: 10px;

                    color: #94a3b8;

                    font-size: 13px;

                    line-height: 1.7;
                }


                .admin-description strong {

                    color: #c4b5fd;

                    font-weight: 700;
                }


                /* =================================================
                   CARD DO USUÁRIO
                   ================================================= */

                .admin-user-card {

                    position: relative;

                    z-index: 2;

                    min-width: 230px;

                    display: flex;

                    align-items: center;

                    gap: 13px;

                    padding:
                        13px 17px;

                    border-radius: 15px;

                    background:
                        rgba(255,255,255,0.035);

                    border:
                        1px solid
                        rgba(255,255,255,0.08);

                    box-shadow:
                        inset 0 1px 0
                        rgba(255,255,255,0.03);
                }


                .admin-user-icon {

                    width: 42px;

                    height: 42px;

                    min-width: 42px;

                    border-radius: 12px;

                    display: flex;

                    align-items: center;

                    justify-content: center;

                    font-size: 18px;

                    background:
                        linear-gradient(
                            135deg,
                            rgba(59,130,246,0.20),
                            rgba(124,58,237,0.24)
                        );

                    border:
                        1px solid
                        rgba(168,85,247,0.22);
                }


                .admin-user-label {

                    color: #64748b;

                    font-size: 10px;

                    text-transform: uppercase;

                    letter-spacing: 0.08em;

                    margin-bottom: 3px;
                }


                .admin-user-name {

                    color: #e2e8f0;

                    font-size: 13px;

                    font-weight: 700;
                }


                /* =================================================
                   STATUS BAR
                   ================================================= */

                .admin-status-bar {

                    display: grid;

                    grid-template-columns:
                        repeat(3, 1fr);

                    gap: 12px;

                    margin-bottom: 28px;
                }


                .admin-status-item {

                    display: flex;

                    align-items: center;

                    gap: 12px;

                    padding:
                        15px 17px;

                    border-radius: 14px;

                    background:
                        rgba(15,23,42,0.68);

                    border:
                        1px solid
                        rgba(255,255,255,0.06);

                    box-shadow:
                        0 8px 25px
                        rgba(0,0,0,0.15);
                }


                .admin-status-icon {

                    width: 38px;

                    height: 38px;

                    min-width: 38px;

                    display: flex;

                    align-items: center;

                    justify-content: center;

                    border-radius: 11px;

                    background:
                        rgba(255,255,255,0.035);

                    font-size: 15px;
                }


                .admin-status-title {

                    color: #64748b;

                    font-size: 10px;

                    text-transform: uppercase;

                    letter-spacing: 0.07em;

                    margin-bottom: 3px;
                }


                .admin-status-value {

                    color: #cbd5e1;

                    font-size: 12px;

                    font-weight: 600;
                }


                .admin-status-online {

                    color: #34d399;
                }


                /* =================================================
                   CABEÇALHO DOS MÓDULOS
                   ================================================= */

                .admin-section-header {

                    display: flex;

                    justify-content: space-between;

                    align-items: flex-end;

                    gap: 20px;

                    margin-bottom: 15px;

                    padding-bottom: 14px;

                    border-bottom:
                        1px solid
                        rgba(255,255,255,0.06);
                }


                .admin-section-title {

                    color: #f8fafc;

                    font-size: 19px;

                    font-weight: 800;

                    letter-spacing: -0.025em;
                }


                .admin-section-description {

                    margin-top: 4px;

                    color: #64748b;

                    font-size: 12px;
                }


                .admin-section-badge {

                    padding:
                        7px 11px;

                    border-radius: 999px;

                    color: #c4b5fd;

                    background:
                        rgba(124,58,237,0.09);

                    border:
                        1px solid
                        rgba(124,58,237,0.18);

                    font-size: 10px;

                    font-weight: 600;

                    white-space: nowrap;
                }


                /* =================================================
                   CARDS DOS MÓDULOS
                   ================================================= */

                [class*="st-key-card_acessos"],
                [class*="st-key-card_tabelas"],
                [class*="st-key-card_perfil"],
                [class*="st-key-card_sair"] {

                    position: relative;

                    margin: 0 !important;

                    padding: 0 !important;
                }


                /* =================================================
                   BOTÕES DOS CARDS
                   ================================================= */

                [class*="st-key-card_acessos"] button,
                [class*="st-key-card_tabelas"] button,
                [class*="st-key-card_perfil"] button,
                [class*="st-key-card_sair"] button {

                    position: relative;

                    min-height: 128px !important;

                    height: 128px !important;

                    width: 100% !important;

                    padding:
                        20px 30px 20px 105px !important;

                    box-sizing: border-box !important;

                    border-radius: 18px !important;

                    border:
                        1px solid
                        rgba(168,85,247,0.13) !important;

                    background:
                        linear-gradient(
                            145deg,
                            rgba(15,23,42,0.94),
                            rgba(26,16,47,0.94)
                        ) !important;

                    color: #f8fafc !important;

                    box-shadow:
                        0 12px 35px
                        rgba(0,0,0,0.25) !important;

                    text-align: left !important;

                    overflow: hidden !important;

                    transition:
                        transform 0.22s ease,
                        border-color 0.22s ease,
                        box-shadow 0.22s ease,
                        background 0.22s ease !important;
                }


                /* =================================================
                   BRILHO INTERNO
                   ================================================= */

                [class*="st-key-card_acessos"] button::after,
                [class*="st-key-card_tabelas"] button::after,
                [class*="st-key-card_perfil"] button::after,
                [class*="st-key-card_sair"] button::after {

                    content: "";

                    position: absolute;

                    width: 180px;

                    height: 180px;

                    right: -100px;

                    bottom: -110px;

                    border-radius: 50%;

                    background:
                        radial-gradient(
                            circle,
                            rgba(124,58,237,0.15),
                            transparent 70%
                        );

                    pointer-events: none;
                }


                /* =================================================
                   ÍCONES
                   ================================================= */

                [class*="st-key-card_acessos"] button::before,
                [class*="st-key-card_tabelas"] button::before,
                [class*="st-key-card_perfil"] button::before,
                [class*="st-key-card_sair"] button::before {

                    position: absolute;

                    left: 30px;

                    top: 50%;

                    transform: translateY(-50%);

                    width: 52px;

                    height: 52px;

                    display: flex;

                    align-items: center;

                    justify-content: center;

                    border-radius: 15px;

                    background:
                        linear-gradient(
                            135deg,
                            rgba(59,130,246,0.16),
                            rgba(124,58,237,0.20)
                        );

                    border:
                        1px solid
                        rgba(168,85,247,0.22);

                    box-shadow:
                        0 8px 22px
                        rgba(0,0,0,0.20);

                    font-size: 21px;

                    z-index: 3;
                }


                /* =================================================
                   ÍCONE ACESSOS
                   ================================================= */

                [class*="st-key-card_acessos"] button::before {

                    content: "👥";
                }


                /* =================================================
                   ÍCONE TABELAS
                   ================================================= */

                [class*="st-key-card_tabelas"] button::before {

                    content: "🗄️";
                }


                /* =================================================
                   ÍCONE PERFIL
                   ================================================= */

                [class*="st-key-card_perfil"] button::before {

                    content: "⚙️";
                }


                /* =================================================
                   ÍCONE SAIR
                   ================================================= */

                [class*="st-key-card_sair"] button::before {

                    content: "🚪";

                    background:
                        linear-gradient(
                            135deg,
                            rgba(239,68,68,0.10),
                            rgba(220,38,38,0.17)
                        );

                    border-color:
                        rgba(248,113,113,0.20);
                }


                /* =================================================
                   TEXTO DOS CARDS
                   ================================================= */

                [class*="st-key-card_acessos"] button p,
                [class*="st-key-card_tabelas"] button p,
                [class*="st-key-card_perfil"] button p,
                [class*="st-key-card_sair"] button p {

                    margin: 0 !important;

                    padding: 0 !important;

                    line-height: 1.55 !important;

                    white-space: pre-line !important;

                    font-size: 12px !important;
                }


                /* =================================================
                   PRIMEIRA LINHA DO TEXTO
                   ================================================= */

                [class*="st-key-card_acessos"] button p:first-line,
                [class*="st-key-card_tabelas"] button p:first-line,
                [class*="st-key-card_perfil"] button p:first-line,
                [class*="st-key-card_sair"] button p:first-line {

                    font-size: 15px;
                }


                /* =================================================
                   HOVER
                   ================================================= */

                [class*="st-key-card_acessos"] button:hover,
                [class*="st-key-card_tabelas"] button:hover,
                [class*="st-key-card_perfil"] button:hover {

                    transform:
                        translateY(-3px) !important;

                    border-color:
                        rgba(168,85,247,0.42) !important;

                    background:
                        linear-gradient(
                            145deg,
                            rgba(21,31,52,0.98),
                            rgba(37,22,66,0.98)
                        ) !important;

                    box-shadow:
                        0 18px 45px
                        rgba(124,58,237,0.18) !important;
                }


                [class*="st-key-card_sair"] button {

                    border-color:
                        rgba(248,113,113,0.12) !important;
                }


                [class*="st-key-card_sair"] button:hover {

                    transform:
                        translateY(-3px) !important;

                    border-color:
                        rgba(248,113,113,0.35) !important;

                    background:
                        linear-gradient(
                            145deg,
                            rgba(25,20,38,0.98),
                            rgba(49,22,42,0.98)
                        ) !important;

                    box-shadow:
                        0 18px 45px
                        rgba(239,68,68,0.12) !important;
                }


                /* =================================================
                   HOVER DOS ÍCONES
                   ================================================= */

                [class*="st-key-card_acessos"] button:hover::before,
                [class*="st-key-card_tabelas"] button:hover::before,
                [class*="st-key-card_perfil"] button:hover::before {

                    border-color:
                        rgba(168,85,247,0.42);

                    box-shadow:
                        0 0 25px
                        rgba(124,58,237,0.18);
                }


                [class*="st-key-card_sair"] button:hover::before {

                    border-color:
                        rgba(248,113,113,0.40);

                    box-shadow:
                        0 0 25px
                        rgba(239,68,68,0.15);
                }


                /* =================================================
                   RODAPÉ
                   ================================================= */

                .admin-footer {

                    display: flex;

                    justify-content: space-between;

                    align-items: center;

                    gap: 20px;

                    margin-top: 26px;

                    padding-top: 18px;

                    border-top:
                        1px solid
                        rgba(255,255,255,0.06);

                    color: #475569;

                    font-size: 10px;
                }


                .admin-footer strong {

                    color: #94a3b8;

                    font-weight: 700;
                }


                .admin-footer-status {

                    display: flex;

                    align-items: center;

                    gap: 7px;
                }


                .admin-footer-dot {

                    width: 6px;

                    height: 6px;

                    border-radius: 50%;

                    background: #34d399;

                    box-shadow:
                        0 0 7px
                        rgba(52,211,153,0.65);
                }


                /* =================================================
                   RESPONSIVO
                   ================================================= */

                @media (max-width: 850px) {

                    .admin-main-header {

                        flex-direction: column;

                        align-items: flex-start;
                    }


                    .admin-user-card {

                        width: 100%;

                        box-sizing: border-box;
                    }


                    .admin-status-bar {

                        grid-template-columns: 1fr;
                    }


                    .admin-section-header {

                        align-items: flex-start;

                        flex-direction: column;
                    }


                    [class*="st-key-card_acessos"] button,
                    [class*="st-key-card_tabelas"] button,
                    [class*="st-key-card_perfil"] button,
                    [class*="st-key-card_sair"] button {

                        height: 120px !important;

                        min-height: 120px !important;

                        padding-left: 95px !important;
                    }


                    [class*="st-key-card_acessos"] button::before,
                    [class*="st-key-card_tabelas"] button::before,
                    [class*="st-key-card_perfil"] button::before,
                    [class*="st-key-card_sair"] button::before {

                        left: 25px;
                    }


                    .admin-footer {

                        flex-direction: column;

                        align-items: flex-start;
                    }

                }


                @media (max-width: 520px) {

                    .admin-page {

                        padding:
                            18px 10px 35px 10px;
                    }


                    .admin-main-header {

                        padding:
                            24px 20px;
                    }


                    .admin-title {

                        font-size: 27px;
                    }


                    .admin-description {

                        font-size: 12px;
                    }


                    [class*="st-key-card_acessos"] button,
                    [class*="st-key-card_tabelas"] button,
                    [class*="st-key-card_perfil"] button,
                    [class*="st-key-card_sair"] button {

                        height: 112px !important;

                        min-height: 112px !important;

                        padding:
                            18px 18px 18px 88px !important;
                    }


                    [class*="st-key-card_acessos"] button::before,
                    [class*="st-key-card_tabelas"] button::before,
                    [class*="st-key-card_perfil"] button::before,
                    [class*="st-key-card_sair"] button::before {

                        left: 20px;

                        width: 46px;

                        height: 46px;

                        font-size: 18px;
                    }

                }

            </style>
            """
        )

        # =====================================================
        # HEADER PRINCIPAL
        # =====================================================

        st.html(
            """
            <div class="admin-page">

                <div class="admin-main-header">

                    <div class="admin-header-left">

                        <div class="admin-eyebrow">

                            <span class="admin-eyebrow-dot"></span>

                            Ambiente administrativo

                        </div>


                        <div class="admin-title">
                            Painel Administrativo
                        </div>


                        <div class="admin-description">

                            Gerencie usuários, banco de dados e
                            configurações do ambiente administrativo
                            do <strong>Vitta Vision</strong>.

                        </div>

                    </div>


                    <div class="admin-user-card">

                        <div class="admin-user-icon">
                            👤
                        </div>

                        <div>

                            <div class="admin-user-label">
                                Sessão ativa
                            </div>

                            <div class="admin-user-name">
                                Administrador Master
                            </div>

                        </div>

                    </div>

                </div>


                <!-- =============================================
                     STATUS
                     ============================================= -->

                <div class="admin-status-bar">

                    <div class="admin-status-item">

                        <div class="admin-status-icon">
                            🟢
                        </div>

                        <div>

                            <div class="admin-status-title">
                                Sistema
                            </div>

                            <div class="admin-status-value
                                        admin-status-online">
                                Operacional
                            </div>

                        </div>

                    </div>


                    <div class="admin-status-item">

                        <div class="admin-status-icon">
                            🔐
                        </div>

                        <div>

                            <div class="admin-status-title">
                                Segurança
                            </div>

                            <div class="admin-status-value">
                                Acesso protegido
                            </div>

                        </div>

                    </div>


                    <div class="admin-status-item">

                        <div class="admin-status-icon">
                            🗄️
                        </div>

                        <div>

                            <div class="admin-status-title">
                                Banco de dados
                            </div>

                            <div class="admin-status-value">
                                Oracle Database
                            </div>

                        </div>

                    </div>

                </div>


                <!-- =============================================
                     CABEÇALHO ADMINISTRAÇÃO
                     ============================================= -->

                <div class="admin-section-header">

                    <div>

                        <div class="admin-section-title">
                            Administração
                        </div>

                        <div class="admin-section-description">
                            Selecione uma área para continuar.
                        </div>

                    </div>


                    <div class="admin-section-badge">
                        3 módulos disponíveis
                    </div>

                </div>

            </div>
            """
        )

        # =====================================================
        # PRIMEIRA LINHA
        # =====================================================

        row1_col1, row1_col2 = st.columns(
            2,
            gap="medium"
        )


        # =====================================================
        # MÓDULO ACESSOS
        # =====================================================

        with row1_col1:

            if st.button(
                "Módulo Acessos\n\n"
                "Gerencie usuários, cadastros e "
                "acessos ao sistema.",
                key="card_acessos",
                use_container_width=True,
            ):

                st.session_state.admin_aba_ativa = (
                    "Módulo Acessos"
                )

                st.rerun()


        # =====================================================
        # MÓDULO TABELAS
        # =====================================================

        with row1_col2:

            if st.button(
                "Módulo de Tabelas\n\n"
                "Consulte tabelas, estruturas e "
                "informações do Oracle.",
                key="card_tabelas",
                use_container_width=True,
            ):

                st.session_state.admin_aba_ativa = (
                    "Módulo de Tabelas"
                )

                st.rerun()


        # =====================================================
        # ESPAÇAMENTO
        # =====================================================

        st.write("")


        # =====================================================
        # SEGUNDA LINHA
        # =====================================================

        row2_col1, row2_col2 = st.columns(
            2,
            gap="medium"
        )


        # =====================================================
        # MEU PERFIL
        # =====================================================

        with row2_col1:

            if st.button(
                "Meu Perfil\n\n"
                "Visualize as informações da "
                "conta administrativa.",
                key="card_perfil",
                use_container_width=True,
            ):

                st.session_state.admin_aba_ativa = (
                    "Meu Perfil"
                )

                st.rerun()


        # =====================================================
        # SAIR DO SISTEMA
        # =====================================================

        with row2_col2:

            if st.button(
                "Sair do Sistema\n\n"
                "Encerrar a sessão administrativa "
                "com segurança.",
                key="card_sair",
                use_container_width=True,
            ):

                st.session_state.admin_logado = False

                st.session_state.admin_perfil = ""

                st.session_state.admin_aba_ativa = (
                    "Menu Principal"
                )

                st.rerun()


        # =====================================================
        # RODAPÉ
        # =====================================================

        st.html(
            """
            <div class="admin-page">

                <div class="admin-footer">

                    <div>

                        <strong>Vitta Vision</strong>

                        &nbsp;•&nbsp;

                        Painel Administrativo

                    </div>


                    <div class="admin-footer-status">

                        <span class="admin-footer-dot"></span>

                        Ambiente restrito a administradores

                    </div>

                </div>

            </div>
            """
        )