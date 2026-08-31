import base64
import hashlib
import os

import pandas as pd
import streamlit as st

from model.oracle_connection import OracleDatabase
from model.hospitais_model import HospitaisModel
from model.internacoes_model import InternacoesModel
from model.leitos_model import LeitosModel

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

if "admin_email" not in st.session_state:
    st.session_state.admin_email = ""

if "admin_id" not in st.session_state:
    st.session_state.admin_id = None


# ============================================================
# CSS GLOBAL
# ============================================================

st.html(
    """
    <style>

        /* =====================================================
           APLICAÇÃO
           ===================================================== */

        .stApp {

            background:
                radial-gradient(
                    circle at top right,
                    rgba(90, 40, 150, 0.12),
                    transparent 35%
                ),

                radial-gradient(
                    circle at bottom left,
                    rgba(37, 99, 235, 0.08),
                    transparent 35%
                ),

                linear-gradient(
                    135deg,
                    #070913 0%,
                    #0b0f19 50%,
                    #110c24 100%
                );

            color:
                #ffffff;
        }


        h1,
        h2,
        h3 {

            color:
                #ffffff !important;
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

            padding:
                20px;

            border-radius:
                16px;

            box-shadow:
                0 8px 32px
                rgba(0, 0, 0, 0.30);

            margin-bottom:
                16px;
        }


        .element-container {

            margin-bottom:
                0 !important;
        }


        /* =====================================================
           LOGIN CARD
           ===================================================== */

        .st-key-admin_login_card {

            width:
                calc(100% - 32px) !important;

            max-width:
                1120px !important;

            margin:
                32px auto !important;

            padding:
                0 !important;

            background:
                linear-gradient(
                    145deg,
                    rgba(15, 20, 34, 0.98),
                    rgba(21, 16, 39, 0.98)
                ) !important;

            border:
                1px solid
                rgba(255, 255, 255, 0.10) !important;

            border-radius:
                26px !important;

            overflow:
                hidden !important;

            box-shadow:
                0 30px 80px
                rgba(0, 0, 0, 0.48),

                0 0 50px
                rgba(124, 58, 237, 0.08);

            backdrop-filter:
                blur(20px);

            -webkit-backdrop-filter:
                blur(20px);
        }


        /* =====================================================
           LINHA PRINCIPAL
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stHorizontalBlock"] {

            width:
                100% !important;

            max-width:
                none !important;

            gap:
                0 !important;

            align-items:
                stretch !important;

            min-height:
                620px !important;

            margin:
                0 !important;

            padding:
                0 !important;
        }


        /* =====================================================
           COLUNAS
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stColumn"] {

            padding:
                0 !important;

            margin:
                0 !important;

            min-height:
                620px !important;

            width:
                50% !important;

            flex:
                1 1 50% !important;

            display:
                flex !important;

            flex-direction:
                column !important;

            box-sizing:
                border-box !important;
        }


        /* =====================================================
           PAINEL ESQUERDO
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stColumn"]:first-child {

            border-right:
                1px solid
                rgba(255, 255, 255, 0.08) !important;

            background:

                radial-gradient(
                    circle at 20% 20%,
                    rgba(37, 99, 235, 0.20),
                    transparent 38%
                ),

                radial-gradient(
                    circle at 80% 85%,
                    rgba(147, 51, 234, 0.18),
                    transparent 40%
                ),

                linear-gradient(
                    145deg,
                    rgba(13, 20, 38, 0.98),
                    rgba(20, 15, 42, 0.98)
                ) !important;
        }


        /* =====================================================
           PAINEL DIREITO
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stColumn"]:nth-child(2) {

            background:

                linear-gradient(
                    145deg,
                    rgba(10, 14, 25, 0.97),
                    rgba(17, 12, 31, 0.99)
                ) !important;

            padding:
                70px 76px 58px 76px !important;

            box-sizing:
                border-box !important;

            justify-content:
                center !important;
        }


        .st-key-admin_login_card
        [data-testid="stColumn"] > div {

            width:
                100% !important;

            max-width:
                none !important;

            padding:
                0 !important;

            margin:
                0 !important;

            box-sizing:
                border-box !important;
        }


        /* =====================================================
           CONTEÚDO ESQUERDO
           ===================================================== */

        .admin-login-left {

            min-height:
                620px;

            width:
                100%;

            box-sizing:
                border-box;

            padding:
                55px 60px;

            display:
                flex;

            flex-direction:
                column;

            justify-content:
                center;

            position:
                relative;

            overflow:
                hidden;
        }


        .admin-login-left::before {

            content:
                "";

            position:
                absolute;

            width:
                320px;

            height:
                320px;

            top:
                -170px;

            left:
                -170px;

            border-radius:
                50%;

            background:
                radial-gradient(
                    circle,
                    rgba(59, 130, 246, 0.24),
                    transparent 70%
                );

            pointer-events:
                none;
        }


        .admin-login-left::after {

            content:
                "";

            position:
                absolute;

            width:
                360px;

            height:
                360px;

            right:
                -210px;

            bottom:
                -210px;

            border-radius:
                50%;

            background:
                radial-gradient(
                    circle,
                    rgba(147, 51, 234, 0.24),
                    transparent 70%
                );

            pointer-events:
                none;
        }


        /* =====================================================
           LOGO
           ===================================================== */

        .admin-brand-logo-wrapper {

            display:
                flex;

            align-items:
                center;

            width:
                100%;

            margin-bottom:
                18px;

            position:
                relative;

            z-index:
                2;
        }


        .admin-brand-logo {

            height:
                78px;

            width:
                auto;

            max-width:
                230px;

            object-fit:
                contain;

            display:
                block;

            filter:
                drop-shadow(
                    0 8px 20px
                    rgba(37, 99, 235, 0.20)
                );
        }


        /* =====================================================
           VITTA VISION
           ===================================================== */

        .admin-brand-name {

            font-family:
                Arial, sans-serif;

            font-size:
                35px;

            font-weight:
                900;

            letter-spacing:
                -0.045em;

            line-height:
                1.05;

            color:
                #ffffff;

            position:
                relative;

            z-index:
                2;

            margin-bottom:
                16px;
        }


        .admin-brand-name .brand-vitta {

            color:
                #ffffff;
        }


        .admin-brand-name .brand-vision {

            background:
                linear-gradient(
                    90deg,
                    #3b82f6 0%,
                    #6366f1 42%,
                    #8b5cf6 72%,
                    #a855f7 100%
                );

            -webkit-background-clip:
                text;

            -webkit-text-fill-color:
                transparent;

            background-clip:
                text;

            filter:
                drop-shadow(
                    0 0 14px
                    rgba(124, 58, 237, 0.22)
                );
        }


        .admin-brand-line {

            width:
                82px;

            height:
                4px;

            border-radius:
                999px;

            background:
                linear-gradient(
                    90deg,
                    #2563eb,
                    #6366f1,
                    #7c3aed,
                    #9333ea
                );

            box-shadow:
                0 0 14px
                rgba(124, 58, 237, 0.40);

            margin-bottom:
                24px;

            position:
                relative;

            z-index:
                2;
        }


        /* =====================================================
           DESCRIÇÃO
           ===================================================== */

        .admin-brand-description {

            max-width:
                440px;

            color:
                #94a3b8;

            font-family:
                Arial, sans-serif;

            font-size:
                15px;

            line-height:
                1.75;

            position:
                relative;

            z-index:
                2;
        }


        .admin-brand-description strong {

            color:
                #e2e8f0;

            font-weight:
                700;
        }


        /* =====================================================
           FEATURES
           ===================================================== */

        .admin-features {

            display:
                flex;

            align-items:
                flex-start;

            justify-content:
                flex-start;

            gap:
                38px;

            margin-top:
                42px;

            position:
                relative;

            z-index:
                2;
        }


        .admin-feature {

            width:
                125px;

            min-width:
                125px;

            color:
                #94a3b8;

            font-family:
                Arial, sans-serif;

            font-size:
                12px;

            line-height:
                1.45;

            display:
                flex;

            flex-direction:
                column;

            align-items:
                center;

            text-align:
                center;

            gap:
                13px;
        }


        /* =====================================================
           ÍCONES
           ===================================================== */

        .admin-feature-icon {

            width:
                68px;

            height:
                68px;

            border-radius:
                18px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            font-family:
                Arial, sans-serif;

            font-size:
                32px;

            font-weight:
                400;

            line-height:
                1;

            color:
                #c4b5fd;

            background:

                linear-gradient(
                    145deg,
                    rgba(59, 130, 246, 0.15),
                    rgba(99, 102, 241, 0.12),
                    rgba(147, 51, 234, 0.20)
                );

            border:
                1px solid
                rgba(168, 85, 247, 0.25);

            box-shadow:

                0 10px 28px
                rgba(0, 0, 0, 0.24),

                inset 0 1px 0
                rgba(255, 255, 255, 0.06);

            transition:

                transform 0.25s ease,
                border-color 0.25s ease,
                box-shadow 0.25s ease;

            position:
                relative;
        }


        .admin-feature-icon::before {

            content:
                "";

            position:
                absolute;

            inset:
                -1px;

            border-radius:
                18px;

            background:

                linear-gradient(
                    135deg,
                    rgba(59, 130, 246, 0.18),
                    transparent 45%,
                    rgba(168, 85, 247, 0.18)
                );

            opacity:
                0;

            transition:
                opacity 0.25s ease;

            pointer-events:
                none;
        }


        .admin-feature:hover
        .admin-feature-icon {

            transform:
                translateY(-5px)
                scale(1.04);

            border-color:
                rgba(168, 85, 247, 0.48);

            box-shadow:

                0 15px 35px
                rgba(0, 0, 0, 0.28),

                0 0 28px
                rgba(124, 58, 237, 0.18);
        }


        .admin-feature:hover
        .admin-feature-icon::before {

            opacity:
                1;
        }


        .admin-feature-title {

            color:
                #cbd5e1;

            font-size:
                12px;

            font-weight:
                600;

            line-height:
                1.45;
        }


        /* =====================================================
           CABEÇALHO DA DIREITA
           ===================================================== */

        .admin-login-header {

            width:
                100%;

            margin-bottom:
                38px;

            text-align:
                left;
        }


        /* =====================================================
           ÍCONE DE SEGURANÇA
           ===================================================== */

        .admin-security-icon {

            width:
                64px;

            height:
                64px;

            border-radius:
                18px;

            display:
                flex;

            align-items:
                center;

            justify-content:
                center;

            font-size:
                27px;

            margin:
                0 0 28px 0;

            background:

                linear-gradient(
                    135deg,
                    rgba(59, 130, 246, 0.18),
                    rgba(147, 51, 234, 0.22)
                );

            border:
                1px solid
                rgba(168, 85, 247, 0.28);

            box-shadow:
                0 10px 30px
                rgba(124, 58, 237, 0.14);

            position:
                relative;
        }


        .admin-security-icon::after {

            content:
                "";

            position:
                absolute;

            inset:
                -6px;

            border-radius:
                23px;

            border:
                1px solid
                rgba(124, 58, 237, 0.08);

            pointer-events:
                none;
        }


        /* =====================================================
           TÍTULO DIREITA
           ===================================================== */

        .admin-login-title {

            font-family:
                Arial, sans-serif;

            font-size:
                31px;

            font-weight:
                800;

            color:
                #f8fafc;

            letter-spacing:
                -0.035em;

            line-height:
                1.2;

            margin-bottom:
                16px;
        }


        /* =====================================================
           SUBTÍTULO DIREITA
           ===================================================== */

        .admin-login-subtitle {

            max-width:
                430px;

            color:
                #94a3b8;

            font-family:
                Arial, sans-serif;

            font-size:
                14px;

            line-height:
                1.75;

            margin:
                0;
        }


        /* =====================================================
           FORMULÁRIO
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stForm"] {

            width:
                100% !important;

            margin:
                0 !important;

            padding:
                0 !important;

            border:
                none !important;

            outline:
                none !important;

            border-radius:
                0 !important;

            background:
                transparent !important;

            box-shadow:
                none !important;
        }


        .st-key-admin_login_card
        form {

            border:
                none !important;

            outline:
                none !important;

            box-shadow:
                none !important;

            background:
                transparent !important;
        }


        /* =====================================================
           ESPAÇAMENTO ENTRE OS CAMPOS
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stForm"]
        [data-testid="stTextInput"] {

            margin-bottom:
                22px !important;
        }


        .st-key-admin_login_card
        [data-testid="stForm"]
        [data-testid="stTextInput"]:last-of-type {

            margin-bottom:
                28px !important;
        }


        /* =====================================================
           LABELS
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stForm"]
        label {

            color:
                #cbd5e1 !important;

            font-size:
                13px !important;

            font-weight:
                600 !important;

            margin-bottom:
                7px !important;
        }


        /* =====================================================
           INPUTS
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stForm"]
        input {

            background:
                rgba(255, 255, 255, 0.055) !important;

            color:
                #f8fafc !important;

            border:
                1px solid
                rgba(255, 255, 255, 0.09) !important;

            border-radius:
                11px !important;

            min-height:
                48px !important;

            padding:
                0 14px !important;

            font-size:
                13px !important;

            transition:
                border-color 0.2s ease,
                box-shadow 0.2s ease,
                background 0.2s ease;
        }


        .st-key-admin_login_card
        [data-testid="stForm"]
        input::placeholder {

            color:
                #526078 !important;
        }


        .st-key-admin_login_card
        [data-testid="stForm"]
        input:hover {

            background:
                rgba(255, 255, 255, 0.065) !important;

            border-color:
                rgba(255, 255, 255, 0.14) !important;
        }


        .st-key-admin_login_card
        [data-testid="stForm"]
        input:focus {

            border-color:
                rgba(124, 58, 237, 0.65) !important;

            box-shadow:
                0 0 0 3px
                rgba(124, 58, 237, 0.10) !important;

            background:
                rgba(255, 255, 255, 0.07) !important;
        }


        /* =====================================================
           BOTÃO
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stFormSubmitButton"] {

            width:
                100% !important;

            margin-top:
                4px !important;
        }


        .st-key-admin_login_card
        [data-testid="stFormSubmitButton"]
        button {

            width:
                100% !important;

            min-height:
                50px !important;

            border-radius:
                11px !important;

            border:
                1px solid
                rgba(191, 219, 254, 0.40) !important;

            background:

                linear-gradient(
                    135deg,
                    #2563eb 0%,
                    #6366f1 45%,
                    #7c3aed 75%,
                    #9333ea 100%
                ) !important;

            color:
                #ffffff !important;

            font-size:
                14px !important;

            font-weight:
                700 !important;

            box-shadow:
                0 10px 28px
                rgba(99, 102, 241, 0.25) !important;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                filter 0.2s ease !important;
        }


        .st-key-admin_login_card
        [data-testid="stFormSubmitButton"]
        button:hover {

            transform:
                translateY(-2px) !important;

            filter:
                brightness(1.06) !important;

            box-shadow:
                0 14px 34px
                rgba(124, 58, 237, 0.40) !important;
        }


        .st-key-admin_login_card
        [data-testid="stFormSubmitButton"]
        button:active {

            transform:
                translateY(0) !important;
        }


        /* =====================================================
           ALERTAS
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stAlert"] {

            border-radius:
                11px !important;

            margin-top:
                18px !important;

            font-size:
                12px !important;
        }


        /* =====================================================
           FOOTER
           ===================================================== */

        .admin-login-footer {

            width:
                100%;

            margin-top:
                34px;

            padding-top:
                20px;

            border-top:
                1px solid
                rgba(255, 255, 255, 0.07);

            color:
                #64748b;

            font-family:
                Arial, sans-serif;

            font-size:
                10px;

            text-align:
                center;

            line-height:
                1.6;
        }


        .admin-login-footer span {

            color:
                #94a3b8;
        }


        /* =====================================================
           VERTICAL BLOCK
           ===================================================== */

        .st-key-admin_login_card
        [data-testid="stVerticalBlock"] {

            gap:
                0 !important;
        }


        /* =====================================================
           RESPONSIVIDADE
           ===================================================== */

        @media (max-width: 1000px) {

            .st-key-admin_login_card {

                width:
                    calc(100% - 30px) !important;

                margin:
                    25px auto !important;

                border-radius:
                    22px !important;
            }


            .st-key-admin_login_card
            [data-testid="stHorizontalBlock"] {

                min-height:
                    auto !important;
            }


            .st-key-admin_login_card
            [data-testid="stColumn"] {

                min-height:
                    auto !important;
            }


            .st-key-admin_login_card
            [data-testid="stColumn"]:nth-child(2) {

                padding:
                    58px 52px !important;
            }


            .admin-login-left {

                min-height:
                    560px;

                padding:
                    50px;
            }
        }


        @media (max-width: 800px) {

            .st-key-admin_login_card
            [data-testid="stHorizontalBlock"] {

                flex-direction:
                    column !important;
            }


            .st-key-admin_login_card
            [data-testid="stColumn"] {

                width:
                    100% !important;

                min-width:
                    100% !important;

                flex:
                    1 1 100% !important;
            }


            .st-key-admin_login_card
            [data-testid="stColumn"]:first-child {

                border-right:
                    none !important;

                border-bottom:
                    1px solid
                    rgba(255, 255, 255, 0.08) !important;
            }


            .st-key-admin_login_card
            [data-testid="stColumn"]:nth-child(2) {

                padding:
                    48px 40px !important;
            }


            .admin-login-left {

                min-height:
                    auto;

                padding:
                    48px 40px;
            }


            .admin-features {

                gap:
                    24px;
            }


            .admin-feature {

                width:
                    110px;

                min-width:
                    110px;
            }


            .admin-feature-icon {

                width:
                    62px;

                height:
                    62px;

                font-size:
                    29px;
            }
        }


        @media (max-width: 600px) {

            .admin-features {

                justify-content:
                    space-between;

                gap:
                    10px;
            }


            .admin-feature {

                width:
                    30%;

                min-width:
                    0;
            }


            .admin-feature-icon {

                width:
                    58px;

                height:
                    58px;

                font-size:
                    27px;
            }


            .admin-feature-title {

                font-size:
                    11px;
            }
        }


        @media (max-width: 520px) {

            .st-key-admin_login_card
            [data-testid="stColumn"]:nth-child(2) {

                padding:
                    38px 24px !important;
            }


            .admin-login-left {

                padding:
                    38px 24px;
            }


            .admin-features {

                flex-direction:
                    column;

                align-items:
                    flex-start;

                gap:
                    18px;
            }


            .admin-feature {

                width:
                    100%;

                min-width:
                    100%;

                flex-direction:
                    row;

                align-items:
                    center;

                justify-content:
                    flex-start;

                text-align:
                    left;

                gap:
                    14px;
            }


            .admin-feature-icon {

                flex-shrink:
                    0;
            }


            .admin-login-title {

                font-size:
                    25px;
            }
        }

    </style>
    """
)


# ============================================================
# HASH DE SENHA
# ============================================================

def gerar_hash_senha(senha: str) -> str:

    return hashlib.sha256(
        senha.encode("utf-8")
    ).hexdigest()


# ============================================================
# LOCALIZAR LOGO
# ============================================================

def localizar_logo():

    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    possible_paths = [

        os.path.join(
            current_dir,
            "..",
            "assets",
            "logotipo.png",
        ),

        os.path.join(
            current_dir,
            "assets",
            "logotipo.png",
        ),

        os.path.join(
            current_dir,
            "src",
            "assets",
            "logotipo.png",
        ),

        os.path.join(
            current_dir,
            "..",
            "..",
            "assets",
            "logotipo.png",
        ),

        os.path.join(
            "src",
            "assets",
            "logotipo.png",
        ),

        os.path.join(
            "assets",
            "logotipo.png",
        ),

        "logotipo.png",
    ]

    for path in possible_paths:

        if os.path.exists(path):

            return path

    return None


# ============================================================
# LOGO BASE64
# ============================================================

def carregar_logo_base64():

    logo_path = localizar_logo()

    if not logo_path:

        return None

    try:

        with open(
            logo_path,
            "rb",
        ) as image_file:

            encoded_string = (
                base64.b64encode(
                    image_file.read()
                ).decode("utf-8")
            )

        return (
            "data:image/png;base64,"
            f"{encoded_string}"
        )

    except Exception:

        return None


# ============================================================
# DASHBOARD MODEL
# ============================================================

class DashboardModel:
    """
    Model responsável exclusivamente pelos dados
    utilizados pelo Dashboard.

    Todos os dados são obtidos diretamente do Oracle.

    Fontes utilizadas:

    TB_LEITOS
    TB_INTERNACOES
    """

    def __init__(self, db):

        self.db = db

        self.tabela_leitos = "TB_LEITOS"

        self.tabela_internacoes = "TB_INTERNACOES"


    # ========================================================
    # AUXILIAR DE FILTRO
    # ========================================================

    def _where_filtros(
        self,
        uf=None,
        municipio=None,
        tabela_alias=None,
    ):

        prefixo = ""

        if tabela_alias:

            prefixo = f"{tabela_alias}."

        filtros = []

        parametros = {}

        if uf:

            filtros.append(
                f"UPPER({prefixo}UF) = UPPER(:uf)"
            )

            parametros["uf"] = uf


        if municipio:

            filtros.append(
                f"UPPER({prefixo}MUNICIPIO) = "
                f"UPPER(:municipio)"
            )

            parametros["municipio"] = municipio


        if not filtros:

            return "", parametros


        return (
            " WHERE " + " AND ".join(filtros),
            parametros,
        )


    # ========================================================
    # UFS
    # ========================================================

    def get_ufs(self):

        query = f"""
            SELECT DISTINCT
                TRIM(UF) AS UF
            FROM {self.tabela_leitos}
            WHERE UF IS NOT NULL
            ORDER BY UF
        """

        df = self.db.fetch_data(query)

        if df.empty:

            return []

        coluna = "UF"

        if coluna not in df.columns:

            coluna = df.columns[0]

        return (
            df[coluna]
            .dropna()
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .tolist()
        )


    # ========================================================
    # MUNICÍPIOS
    # ========================================================

    def get_municipios(
        self,
        uf=None,
    ):

        where = ""

        parametros = {}

        if uf:

            where = """
                WHERE UPPER(UF) = UPPER(:uf)
                  AND MUNICIPIO IS NOT NULL
            """

            parametros["uf"] = uf

        else:

            where = """
                WHERE MUNICIPIO IS NOT NULL
            """


        query = f"""
            SELECT DISTINCT
                TRIM(MUNICIPIO) AS MUNICIPIO
            FROM {self.tabela_leitos}
            {where}
            ORDER BY MUNICIPIO
        """

        df = self.db.fetch_data(
            query,
            parametros,
        )

        if df.empty:

            return []

        coluna = "MUNICIPIO"

        if coluna not in df.columns:

            coluna = df.columns[0]

        return (
            df[coluna]
            .dropna()
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .tolist()
        )


    # ========================================================
    # RESUMO
    # ========================================================

    def get_resumo(
        self,
        uf=None,
        municipio=None,
    ):

        where_leitos, params_leitos = (
            self._where_filtros(
                uf=uf,
                municipio=municipio,
                tabela_alias="L",
            )
        )


        where_internacoes, params_internacoes = (
            self._where_filtros(
                uf=uf,
                municipio=municipio,
                tabela_alias="I",
            )
        )


        query_leitos = f"""
            SELECT

                COUNT(
                    DISTINCT L.CNES
                ) AS HOSPITAIS,

                NVL(
                    SUM(L.LEITOS_EXISTENTES),
                    0
                ) AS LEITOS,

                COUNT(
                    DISTINCT L.MUNICIPIO
                ) AS MUNICIPIOS

            FROM {self.tabela_leitos} L

            {where_leitos}
        """


        df_leitos = self.db.fetch_data(
            query_leitos,
            params_leitos,
        )


        query_internacoes = f"""
            SELECT

                NVL(
                    SUM(I.VL_TOTAL_2025),
                    0
                ) AS INTERNACOES

            FROM {self.tabela_internacoes} I

            {where_internacoes}
        """


        df_internacoes = self.db.fetch_data(
            query_internacoes,
            params_internacoes,
        )


        resumo = {

            "hospitais": 0,

            "leitos": 0,

            "internacoes": 0,

            "populacao": 0,

            "municipios": 0,

        }


        if not df_leitos.empty:

            linha = df_leitos.iloc[0]

            resumo["hospitais"] = (
                linha.get("HOSPITAIS", 0)
                or 0
            )

            resumo["leitos"] = (
                linha.get("LEITOS", 0)
                or 0
            )

            resumo["municipios"] = (
                linha.get("MUNICIPIOS", 0)
                or 0
            )


        if not df_internacoes.empty:

            resumo["internacoes"] = (
                df_internacoes.iloc[0].get(
                    "INTERNACOES",
                    0,
                )
                or 0
            )


        resumo["populacao"] = 0


        return resumo


    # ========================================================
    # INTERNAÇÕES
    # ========================================================

    def get_internacoes_data(
        self,
        uf=None,
        municipio=None,
    ):

        meses = [

            ("Jan/2025", "VL_JAN_2025"),

            ("Fev/2025", "VL_FEV_2025"),

            ("Mar/2025", "VL_MAR_2025"),

            ("Abr/2025", "VL_ABR_2025"),

            ("Mai/2025", "VL_MAI_2025"),

            ("Jun/2025", "VL_JUN_2025"),

            ("Jul/2025", "VL_JUL_2025"),

            ("Ago/2025", "VL_AGO_2025"),

            ("Set/2025", "VL_SET_2025"),

            ("Out/2025", "VL_OUT_2025"),

            ("Nov/2025", "VL_NOV_2025"),

            ("Dez/2025", "VL_DEZ_2025"),

        ]


        blocos = []

        parametros = {}


        for indice, (mes, coluna) in enumerate(meses):

            condicoes = []


            if uf:

                nome_param = f"uf_{indice}"

                condicoes.append(
                    f"UPPER(I.UF) = UPPER(:{nome_param})"
                )

                parametros[nome_param] = uf


            if municipio:

                nome_param = f"municipio_{indice}"

                condicoes.append(
                    f"UPPER(I.MUNICIPIO) = "
                    f"UPPER(:{nome_param})"
                )

                parametros[nome_param] = municipio


            where_mes = ""


            if condicoes:

                where_mes = (
                    "WHERE "
                    + " AND ".join(condicoes)
                )


            bloco = f"""
                SELECT

                    '{mes}' AS DATA,

                    NVL(
                        SUM(I.{coluna}),
                        0
                    ) AS VALOR

                FROM {self.tabela_internacoes} I

                {where_mes}
            """

            blocos.append(bloco)


        query = "\nUNION ALL\n".join(
            blocos
        )


        df = self.db.fetch_data(
            query,
            parametros,
        )


        if df.empty:

            return pd.DataFrame(
                columns=[
                    "DATA",
                    "VALOR",
                ]
            )


        return df


    # ========================================================
    # HOSPITAIS
    # ========================================================

    def get_hospitais_data(
        self,
        uf=None,
        municipio=None,
    ):

        where, parametros = (
            self._where_filtros(
                uf=uf,
                municipio=municipio,
                tabela_alias="L",
            )
        )


        query = f"""
            SELECT

                L.CNES AS CNES,

                MAX(
                    L.NOME_ESTABELECIMENTO
                ) AS HOSPITAL,

                NVL(
                    SUM(
                        L.LEITOS_EXISTENTES
                    ),
                    0
                ) AS LEITOS

            FROM {self.tabela_leitos} L

            {where}

            GROUP BY L.CNES

            ORDER BY LEITOS DESC
        """


        return self.db.fetch_data(
            query,
            parametros,
        )


    # ========================================================
    # LEITOS
    # ========================================================

    def get_leitos_data(
        self,
        uf=None,
        municipio=None,
    ):

        condicoes_1 = []

        condicoes_2 = []

        condicoes_3 = []

        parametros = {}


        if uf:

            condicoes_1.append(
                "UPPER(L.UF) = UPPER(:uf_1)"
            )

            condicoes_2.append(
                "UPPER(L.UF) = UPPER(:uf_2)"
            )

            condicoes_3.append(
                "UPPER(L.UF) = UPPER(:uf_3)"
            )

            parametros["uf_1"] = uf
            parametros["uf_2"] = uf
            parametros["uf_3"] = uf


        if municipio:

            condicoes_1.append(
                "UPPER(L.MUNICIPIO) = "
                "UPPER(:municipio_1)"
            )

            condicoes_2.append(
                "UPPER(L.MUNICIPIO) = "
                "UPPER(:municipio_2)"
            )

            condicoes_3.append(
                "UPPER(L.MUNICIPIO) = "
                "UPPER(:municipio_3)"
            )

            parametros["municipio_1"] = municipio
            parametros["municipio_2"] = municipio
            parametros["municipio_3"] = municipio


        def montar_where(condicoes):

            if not condicoes:

                return ""

            return (
                "WHERE "
                + " AND ".join(condicoes)
            )


        query = f"""
            SELECT

                'Leitos existentes' AS TIPO,

                NVL(
                    SUM(
                        L.LEITOS_EXISTENTES
                    ),
                    0
                ) AS LEITOS

            FROM {self.tabela_leitos} L

            {montar_where(condicoes_1)}

            UNION ALL

            SELECT

                'Leitos SUS' AS TIPO,

                NVL(
                    SUM(
                        L.LEITOS_SUS
                    ),
                    0
                ) AS LEITOS

            FROM {self.tabela_leitos} L

            {montar_where(condicoes_2)}

            UNION ALL

            SELECT

                'UTI' AS TIPO,

                NVL(
                    SUM(
                        L.UTI_TOTAL_EXIST
                    ),
                    0
                ) AS LEITOS

            FROM {self.tabela_leitos} L

            {montar_where(condicoes_3)}
        """


        return self.db.fetch_data(
            query,
            parametros,
        )


    # ========================================================
    # MUNICÍPIOS PARA GRÁFICO
    # ========================================================

    def get_municipios_data(
        self,
        uf=None,
        municipio=None,
    ):

        where, parametros = (
            self._where_filtros(
                uf=uf,
                municipio=municipio,
                tabela_alias="L",
            )
        )


        query = f"""
            SELECT

                L.MUNICIPIO AS MUNICIPIO,

                NVL(
                    SUM(
                        L.LEITOS_EXISTENTES
                    ),
                    0
                ) AS QUANTIDADE

            FROM {self.tabela_leitos} L

            {where}

            GROUP BY L.MUNICIPIO

            ORDER BY QUANTIDADE DESC
        """


        return self.db.fetch_data(
            query,
            parametros,
        )


    # ========================================================
    # DADOS PARA IA
    # ========================================================

    def get_dados_ia(
        self,
        uf=None,
        municipio=None,
    ):

        resumo = self.get_resumo(
            uf=uf,
            municipio=municipio,
        )


        hospitais = resumo.get(
            "hospitais",
            0,
        )

        leitos = resumo.get(
            "leitos",
            0,
        )

        internacoes = resumo.get(
            "internacoes",
            0,
        )


        local = ""


        if municipio:

            local = (
                f" no município de {municipio}"
            )

        elif uf:

            local = (
                f" no estado de {uf}"
            )


        mensagem = (
            "Análise baseada nos dados reais "
            f"do Oracle{local}. "
            f"Foram encontrados {hospitais} "
            f"estabelecimentos hospitalares, "
            f"{leitos} leitos existentes e "
            f"{internacoes} internações "
            "registradas para os filtros atuais."
        )


        return {
            "mensagem": mensagem,
        }


    # ========================================================
    # DOWNLOAD
    # ========================================================

    def get_dados_download(
        self,
        uf=None,
        municipio=None,
    ):

        where_leitos, params_leitos = (
            self._where_filtros(
                uf=uf,
                municipio=municipio,
                tabela_alias="L",
            )
        )


        query = f"""
            SELECT

                L.CNES,

                MAX(
                    L.UF
                ) AS UF,

                MAX(
                    L.MUNICIPIO
                ) AS MUNICIPIO,

                MAX(
                    L.NOME_ESTABELECIMENTO
                ) AS NOME_ESTABELECIMENTO,

                NVL(
                    SUM(
                        L.LEITOS_EXISTENTES
                    ),
                    0
                ) AS LEITOS_EXISTENTES,

                NVL(
                    SUM(
                        L.LEITOS_SUS
                    ),
                    0
                ) AS LEITOS_SUS,

                NVL(
                    SUM(
                        L.UTI_TOTAL_EXIST
                    ),
                    0
                ) AS UTI_TOTAL_EXIST

            FROM {self.tabela_leitos} L

            {where_leitos}

            GROUP BY L.CNES

            ORDER BY
                NOME_ESTABELECIMENTO
        """


        return self.db.fetch_data(
            query,
            params_leitos,
        )


# ============================================================
# ADMIN VIEW
# ============================================================

class AdminView:

    def render(self, db):

        if not st.session_state.admin_logado:

            logo_src = carregar_logo_base64()


            with st.container(
                key="admin_login_card"
            ):

                col_left, col_right = st.columns(
                    [1, 1],
                    gap="small",
                )


                # =================================================
                # ESQUERDA
                # =================================================

                with col_left:

                    if logo_src:

                        logo_html = f"""
                        <img
                            class="admin-brand-logo"
                            src="{logo_src}"
                            alt="Vitta Vision"
                        />
                        """

                    else:

                        logo_html = """
                        <div
                            style="
                                font-size: 52px;
                                color: #a855f7;
                            "
                        >
                            ✦
                        </div>
                        """


                    st.html(
                        f"""
                        <div class="admin-login-left">

                            <div class="admin-brand-logo-wrapper">

                                {logo_html}

                            </div>


                            <div class="admin-brand-name">

                                <span class="brand-vitta">
                                    VITTA
                                </span>

                                <span class="brand-vision">
                                    VISION
                                </span>

                            </div>


                            <div class="admin-brand-line"></div>


                            <div class="admin-brand-description">

                                <strong>
                                    Inteligência de dados
                                </strong>

                                para uma saúde mais eficiente,
                                conectando informações,
                                tecnologia e decisões inteligentes.

                            </div>


                            <div class="admin-features">

                                <div class="admin-feature">

                                    <div class="admin-feature-icon">
                                        ◈
                                    </div>

                                    <div class="admin-feature-title">
                                        Dados<br>
                                        inteligentes
                                    </div>

                                </div>


                                <div class="admin-feature">

                                    <div class="admin-feature-icon">
                                        ◉
                                    </div>

                                    <div class="admin-feature-title">
                                        Informações<br>
                                        seguras
                                    </div>

                                </div>


                                <div class="admin-feature">

                                    <div class="admin-feature-icon">
                                        ✦
                                    </div>

                                    <div class="admin-feature-title">
                                        Tecnologia<br>
                                        em saúde
                                    </div>

                                </div>

                            </div>

                        </div>
                        """
                    )


                # =================================================
                # DIREITA
                # =================================================

                with col_right:

                    st.html(
                        """
                        <div class="admin-login-header">

                            <div class="admin-security-icon">
                                🔐
                            </div>


                            <div class="admin-login-title">
                                Acesso Administrativo
                            </div>


                            <div class="admin-login-subtitle">

                                Entre com suas credenciais para
                                acessar o painel administrativo
                                do Vitta Vision.

                            </div>

                        </div>
                        """
                    )


                    with st.form(
                        "admin_login_form",
                        clear_on_submit=False,
                    ):

                        usuario = st.text_input(
                            "Usuário",
                            placeholder="Digite seu usuário",
                        )


                        senha = st.text_input(
                            "Senha",
                            type="password",
                            placeholder="Digite sua senha",
                        )


                        submit_login = (
                            st.form_submit_button(
                                "Entrar no painel",
                                use_container_width=True,
                            )
                        )


                        if submit_login:

                            if (
                                not usuario.strip()
                                or not senha
                            ):

                                st.warning(
                                    "Preencha o usuário e a senha."
                                )

                            else:

                                senha_hash = (
                                    gerar_hash_senha(
                                        senha
                                    )
                                )


                                try:

                                    login_valido = (
                                        db.verificar_login(
                                            usuario.strip(),
                                            senha_hash,
                                        )
                                    )

                                except Exception as e:

                                    st.error(
                                        "Erro ao validar o login no Oracle."
                                    )

                                    st.exception(e)

                                    return


                                if login_valido:

                                    try:

                                        usuario_dados = (
                                            db.obter_usuario_login(
                                                usuario.strip()
                                            )
                                        )

                                    except Exception:

                                        usuario_dados = None


                                    st.session_state.admin_logado = True


                                    if usuario_dados:

                                        st.session_state.admin_id = (
                                            usuario_dados.get(
                                                "ID_USUARIO"
                                            )
                                        )

                                        st.session_state.admin_perfil = (
                                            usuario_dados.get(
                                                "NM_COMPLETO"
                                            )
                                            or "Administrador"
                                        )

                                        st.session_state.admin_email = (
                                            usuario_dados.get(
                                                "DS_EMAIL"
                                            )
                                            or ""
                                        )

                                    else:

                                        st.session_state.admin_perfil = (
                                            "Administrador"
                                        )

                                        st.session_state.admin_email = (
                                            usuario.strip()
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


                    st.html(
                        """
                        <div class="admin-login-footer">

                            Vitta Vision
                            &nbsp;•&nbsp;

                            <span>
                                Painel Administrativo
                            </span>

                        </div>
                        """
                    )

            return


        AdminPainelView().render()


# ============================================================
# CONTROLLER PRINCIPAL
# ============================================================

class MainController:

    def __init__(self):

        self.db = OracleDatabase()


        self.dashboard_model = DashboardModel(
            self.db
        )


        self.hospitais_model = HospitaisModel(
            self.db
        )


        self.internacoes_model = InternacoesModel(
            self.db
        )


        self.leitos_model = LeitosModel(
            self.db
        )


        self.header = HeaderComponent()


    # ========================================================
    # ROTEAMENTO
    # ========================================================

    def run(self):

        params = st.query_params


        pagina_atual = params.get(
            "page",
            "Dashboard",
        )


        self.header.render(
            pagina_atual
        )


        # ----------------------------------------------------
        # DASHBOARD
        # ----------------------------------------------------

        if pagina_atual == "Dashboard":

            try:

                DashboardView().render(
                    self.dashboard_model
                )

            except Exception as e:

                st.error(
                    "Erro ao carregar o Dashboard "
                    "a partir do Oracle."
                )

                st.exception(e)


        # ----------------------------------------------------
        # ASSISTENTE IA
        # ----------------------------------------------------

        elif pagina_atual == "Assistente IA":

            AssistenteIAView().render(
                self.dashboard_model
            )


        # ----------------------------------------------------
        # HOSPITAIS
        # ----------------------------------------------------

        elif pagina_atual == "Hospitais":

            HospitaisView().render(
                self.hospitais_model
            )


        # ----------------------------------------------------
        # INTERNAÇÕES
        # ----------------------------------------------------

        elif pagina_atual == "Internações":

            InternacoesView().render(
                self.internacoes_model
            )


        # ----------------------------------------------------
        # LEITOS
        # ----------------------------------------------------

        elif pagina_atual == "Leitos":

            LeitosView().render(
                self.leitos_model
            )


        # ----------------------------------------------------
        # RELATÓRIOS
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
                "Volte para o Dashboard utilizando "
                "o menu superior."
            )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":

    app = MainController()

    app.run()