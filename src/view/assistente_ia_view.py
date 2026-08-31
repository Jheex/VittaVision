import json
import re
from io import BytesIO
from datetime import datetime

import pandas as pd
import streamlit as st

from model.oracle_connection import OracleDatabase


class AssistenteIAView:
    """Assistente VITTA AI integrado ao Oracle Select AI."""

    ORACLE_PROFILE = "SUS_PROFILE"

    # ================================================================
    # CONFIGURAÇÃO DAS TABELAS
    # ================================================================

    TABELAS = {
        "TB_LEITOS": {
            "descricao": "Dados de leitos, hospitais e UTIs.",
            "municipio": "MUNICIPIO",
            "codigo_municipio": "CO_IBGE",
            "campos": [
                "MUNICIPIO",
                "CO_IBGE",
                "LEITOS_EXISTENTES",
                "LEITOS_SUS",
                "UTI_TOTAL_EXIST",
                "UTI_TOTAL_SUS",
                "NOME_ESTABELECIMENTO",
                "CNES",
                "UF",
            ],
        },

        "TB_INTERNACOES": {
            "descricao": "Dados de internações hospitalares em 2025.",
            "municipio": "MUNICIPIO",
            "codigo_municipio": "CODIGO_MUNICIPIO",
            "campos": [
                "MUNICIPIO",
                "CODIGO_MUNICIPIO",
                "CODIGO_UF",
                "VL_JAN_2025",
                "VL_FEV_2025",
                "VL_MAR_2025",
                "VL_ABR_2025",
                "VL_MAI_2025",
                "VL_JUN_2025",
                "VL_JUL_2025",
                "VL_AGO_2025",
                "VL_SET_2025",
                "VL_OUT_2025",
                "VL_NOV_2025",
                "VL_DEZ_2025",
                "VL_TOTAL_2025",
            ],
        },

        "TB_POPULACAO": {
            "descricao": "Dados de população estimada dos municípios.",
            "municipio": "NOME_DO_MUNICIPIO",
            "codigo_municipio": "COD_MUNIC",
            "campos": [
                "COD_MUNIC",
                "NOME_DO_MUNICIPIO",
                "COD_UF",
                "UF",
                "POPULACAO_ESTIMADA",
            ],
        },
    }

    # ================================================================
    # RENDER
    # ================================================================

    def render(self, model=None):

        self._aplicar_estilo()
        self._inicializar_estado()

        with st.container(key="assistente_ia_view"):

            self._render_sidebar()
            self._render_header()
            self._render_conversa()
            self._render_input()

    # ================================================================
    # ESTILO
    # ================================================================

    def _aplicar_estilo(self):

        st.html(
            """
            <style>

            /* =====================================================
               VITTA AI - ÁREA PRINCIPAL
               ===================================================== */

            .vitta-ai-page {
                width: 100%;
                box-sizing: border-box;
            }

            /* =====================================================
               SIDEBAR FIXA
               ===================================================== */

            section[data-testid="stSidebar"] {
                background:
                    linear-gradient(
                        180deg,
                        #090c18 0%,
                        #0d1020 52%,
                        #090c17 100%
                    ) !important;

                border-right:
                    1px solid
                    rgba(124, 58, 237, 0.16) !important;
            }

            /* Espaçamento superior da sidebar */
            section[data-testid="stSidebar"] > div:first-child {
                padding-top: 58px !important;
            }

            section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
                gap: 0.3rem;
            }

            /* =====================================================
               ESCONDER CONTROLES DE FECHAMENTO DA SIDEBAR
               ===================================================== */

            section[data-testid="stSidebar"] button[aria-label*="Close"],
            section[data-testid="stSidebar"] button[aria-label*="close"],
            section[data-testid="stSidebar"] button[title*="Close"],
            section[data-testid="stSidebar"] button[title*="close"] {
                display: none !important;
            }

            /* Botão nativo de expandir/recolher */
            button[data-testid="stSidebarCollapseButton"] {
                display: none !important;
            }

            /* Alguns builds do Streamlit */
            [data-testid="stSidebarHeader"] button {
                display: none !important;
            }

            /* =====================================================
               CABEÇALHO SIDEBAR
               ===================================================== */

            section[data-testid="stSidebar"] .vitta-sidebar-logo {
                display: flex;
                align-items: center;
                gap: 12px;

                padding:
                    7px 8px 20px 8px;
            }

            section[data-testid="stSidebar"] .vitta-sidebar-icon {
                width: 43px;
                height: 43px;
                min-width: 43px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 13px;

                background:
                    linear-gradient(
                        135deg,
                        #7c3aed,
                        #6366f1
                    );

                box-shadow:
                    0 10px 28px
                    rgba(124, 58, 237, 0.30);

                color: #ffffff;

                font-size: 21px;
                font-weight: 700;
            }

            section[data-testid="stSidebar"] .vitta-sidebar-title {
                color: #ffffff;

                font-size: 20px;
                font-weight: 750;

                line-height: 1.1;
            }

            section[data-testid="stSidebar"] .vitta-sidebar-subtitle {
                margin-top: 5px;

                color: #64748b;

                font-size: 11px;

                line-height: 1.3;
            }

            /* =====================================================
               DIVISOR SIDEBAR
               ===================================================== */

            section[data-testid="stSidebar"] hr {
                border: none !important;

                border-top:
                    1px solid
                    rgba(148, 163, 184, 0.08) !important;

                margin-top: 8px !important;
                margin-bottom: 18px !important;
            }

            /* =====================================================
               BOTÕES SIDEBAR
               ===================================================== */

            section[data-testid="stSidebar"] .stButton {
                margin-bottom: 5px;
            }

            section[data-testid="stSidebar"] .stButton > button {
                min-height: 43px;

                border-radius: 11px !important;

                border:
                    1px solid
                    rgba(139, 92, 246, 0.16) !important;

                background:
                    rgba(124, 58, 237, 0.045) !important;

                color: #cbd5e1 !important;

                font-size: 13px;
                font-weight: 600;

                transition:
                    background 0.2s ease,
                    border 0.2s ease,
                    transform 0.2s ease;
            }

            section[data-testid="stSidebar"] .stButton > button:hover {
                background:
                    linear-gradient(
                        135deg,
                        rgba(124, 58, 237, 0.15),
                        rgba(99, 102, 241, 0.12)
                    ) !important;

                border-color:
                    rgba(139, 92, 246, 0.42) !important;

                color: #ffffff !important;

                transform: translateY(-1px);
            }

            /* =====================================================
               HISTÓRICO
               ===================================================== */

            section[data-testid="stSidebar"] .historico-titulo {
                color: #64748b;

                font-size: 10px;

                font-weight: 750;

                text-transform: uppercase;

                letter-spacing: 1.2px;

                margin-top: 23px;
                margin-bottom: 9px;

                padding-left: 3px;
            }

            section[data-testid="stSidebar"] .stButton button {
                white-space: nowrap;

                overflow: hidden;

                text-overflow: ellipsis;
            }

            /* =====================================================
               RODAPÉ
               ===================================================== */

            section[data-testid="stSidebar"] .vitta-sidebar-footer {
                padding:
                    8px 3px 4px 3px;

                color: #475569;

                font-size: 10px;

                line-height: 1.6;
            }

            section[data-testid="stSidebar"] .vitta-sidebar-footer strong {
                color: #64748b;

                font-weight: 700;
            }

            /* =====================================================
               HEADER VITTA AI
               ===================================================== */

            .vitta-ai-header {
                padding-top: 30px;

                margin-bottom: 4px;
            }

            .vitta-ai-header-title {
                display: flex;

                align-items: center;

                gap: 13px;

                color: #ffffff;

                font-size: 32px;

                font-weight: 750;

                letter-spacing: -1px;
            }

            .vitta-ai-header-icon {
                width: 45px;
                height: 45px;

                min-width: 45px;

                display: flex;

                align-items: center;
                justify-content: center;

                border-radius: 14px;

                background:
                    linear-gradient(
                        135deg,
                        #7c3aed,
                        #6366f1
                    );

                box-shadow:
                    0 10px 30px
                    rgba(124, 58, 237, 0.30);

                color: #ffffff;

                font-size: 22px;

                font-weight: 700;
            }

            .vitta-ai-header-subtitle {
                margin-top: 8px;

                margin-left: 58px;

                color: #64748b;

                font-size: 14px;

                line-height: 1.5;
            }

            .vitta-ai-header-divider {
                height: 1px;

                margin-top: 22px;

                margin-bottom: 12px;

                background:
                    rgba(148, 163, 184, 0.08);
            }

            /* =====================================================
               ÁREA DE CHAT
               ===================================================== */

            .vitta-chat-row {
                width: 100%;

                display: flex;

                align-items: flex-start;

                margin-top: 17px;

                margin-bottom: 17px;

                box-sizing: border-box;
            }

            /* =====================================================
               IA
               ===================================================== */

            .vitta-chat-row-ai {
                justify-content: flex-start;

                gap: 11px;
            }

            .vitta-ai-avatar {
                width: 34px;
                height: 34px;

                min-width: 34px;

                display: flex;

                align-items: center;
                justify-content: center;

                border-radius: 10px;

                background:
                    linear-gradient(
                        135deg,
                        #7c3aed,
                        #6366f1
                    );

                box-shadow:
                    0 6px 18px
                    rgba(124, 58, 237, 0.25);

                color: #ffffff;

                font-size: 16px;

                font-weight: 700;
            }

            .vitta-ai-bubble {
                max-width: 82%;

                padding:
                    13px 17px;

                border-radius:
                    6px 17px 17px 17px;

                background:
                    linear-gradient(
                        145deg,
                        rgba(17, 23, 40, 0.96),
                        rgba(21, 27, 46, 0.92)
                    );

                border:
                    1px solid
                    rgba(139, 92, 246, 0.13);

                color: #e2e8f0;

                box-shadow:
                    0 7px 25px
                    rgba(0, 0, 0, 0.14);

                font-size: 15px;

                line-height: 1.65;

                box-sizing: border-box;
            }

            .vitta-ai-bubble strong {
                color: #ffffff;

                font-weight: 700;
            }

            .vitta-ai-bubble code {
                background:
                    rgba(124, 58, 237, 0.12);

                border:
                    1px solid
                    rgba(124, 58, 237, 0.18);

                color: #c4b5fd;

                border-radius: 5px;

                padding: 2px 5px;
            }

            /* =====================================================
               USUÁRIO
               ===================================================== */

            .vitta-chat-row-user {
                justify-content: flex-end;

                gap: 11px;
            }

            .vitta-user-bubble {
                max-width: 78%;

                padding:
                    12px 16px;

                border-radius:
                    17px 6px 17px 17px;

                background:
                    linear-gradient(
                        135deg,
                        rgba(124, 58, 237, 0.18),
                        rgba(99, 102, 241, 0.12)
                    );

                border:
                    1px solid
                    rgba(139, 92, 246, 0.18);

                color: #e2e8f0;

                box-shadow:
                    0 8px 25px
                    rgba(0, 0, 0, 0.12);

                font-size: 15px;

                line-height: 1.6;

                box-sizing: border-box;
            }

            .vitta-user-bubble strong {
                color: #ffffff;

                font-weight: 700;
            }

            /* =====================================================
               AVATAR DO USUÁRIO
               ===================================================== */

            .vitta-user-avatar {
                width: 34px;
                height: 34px;

                min-width: 34px;

                display: flex;

                align-items: center;
                justify-content: center;

                border-radius: 10px;

                background:
                    linear-gradient(
                        145deg,
                        #f8fafc,
                        #dbe4f0
                    );

                color: #475569;

                box-shadow:
                    0 6px 18px
                    rgba(0, 0, 0, 0.20);

                font-size: 19px;

                line-height: 1;
            }

            /* =====================================================
               PARÁGRAFOS
               ===================================================== */

            .vitta-chat-text p {
                margin:
                    0 0 8px 0;
            }

            .vitta-chat-text p:last-child {
                margin-bottom: 0;
            }

            .vitta-chat-text br {
                line-height: 1.7;
            }

            /* =====================================================
               TABELAS
               ===================================================== */

            [data-testid="stDataFrame"] {
                border-radius: 14px;

                overflow: hidden;

                border:
                    1px solid
                    rgba(124, 58, 237, 0.18);

                box-shadow:
                    0 10px 35px
                    rgba(0, 0, 0, 0.18);

                margin-top: 8px;

                margin-bottom: 8px;
            }

            /* =====================================================
               EXPORTAÇÃO
               ===================================================== */

            .vitta-export-title {
                margin-top: 18px;

                margin-bottom: 10px;

                color: #64748b;

                font-size: 11px;

                font-weight: 700;

                letter-spacing: 0.5px;
            }

            [data-testid="stDownloadButton"] button {
                min-height: 42px;

                border-radius: 10px !important;

                background:
                    rgba(124, 58, 237, 0.07) !important;

                border:
                    1px solid
                    rgba(124, 58, 237, 0.22) !important;

                color: #c4b5fd !important;
            }

            [data-testid="stDownloadButton"] button:hover {
                background:
                    rgba(124, 58, 237, 0.16) !important;

                border-color:
                    rgba(139, 92, 246, 0.45) !important;

                color: #ffffff !important;
            }

            /* =====================================================
               SUGESTÕES
               ===================================================== */

            .vitta-sugestoes {
                margin-top: 30px;

                margin-bottom: 11px;
            }

            .vitta-sugestoes-title {
                color: #64748b;

                font-size: 11px;

                font-weight: 700;

                letter-spacing: 0.5px;

                margin-bottom: 11px;
            }

            /* =====================================================
               BOTÕES PRINCIPAIS
               ===================================================== */

            .main .stButton button {
                min-height: 47px;

                border-radius: 13px !important;

                border:
                    1px solid
                    rgba(139, 92, 246, 0.16) !important;

                background:
                    linear-gradient(
                        145deg,
                        rgba(17, 23, 40, 0.96),
                        rgba(21, 27, 46, 0.90)
                    ) !important;

                color: #cbd5e1 !important;

                font-size: 12px;

                font-weight: 600;

                box-shadow:
                    0 6px 20px
                    rgba(0, 0, 0, 0.16);
            }

            .main .stButton button:hover {
                transform:
                    translateY(-2px);

                border-color:
                    rgba(139, 92, 246, 0.42) !important;

                background:
                    linear-gradient(
                        135deg,
                        rgba(124, 58, 237, 0.13),
                        rgba(99, 102, 241, 0.13)
                    ) !important;

                color: #ffffff !important;
            }

            /* =====================================================
               CHAT INPUT
               ===================================================== */

            [data-testid="stChatInput"] {
                background: transparent;

                padding-bottom: 15px;
            }

            [data-testid="stChatInput"] > div {
                background:
                    #111728 !important;

                border:
                    1px solid
                    rgba(124, 58, 237, 0.28);

                border-radius: 18px;

                box-shadow:
                    0 8px 35px
                    rgba(0, 0, 0, 0.28);
            }

            [data-testid="stChatInput"] > div:focus-within {
                border-color:
                    rgba(139, 92, 246, 0.65);

                box-shadow:
                    0 0 0 3px
                    rgba(124, 58, 237, 0.08),
                    0 8px 35px
                    rgba(0, 0, 0, 0.28);
            }

            [data-testid="stChatInput"] textarea {
                color: #f8fafc !important;

                background: transparent !important;

                font-size: 14px;
            }

            [data-testid="stChatInput"] textarea::placeholder {
                color: #64748b !important;
            }

            [data-testid="stChatInput"] button {
                background:
                    linear-gradient(
                        135deg,
                        #7c3aed,
                        #6366f1
                    ) !important;

                border: none;

                border-radius: 10px;
            }

            /* =====================================================
               SCROLLBAR
               ===================================================== */

            ::-webkit-scrollbar {
                width: 7px;
            }

            ::-webkit-scrollbar-track {
                background: #080b16;
            }

            ::-webkit-scrollbar-thumb {
                background:
                    linear-gradient(
                        180deg,
                        #7c3aed,
                        #6366f1
                    );

                border-radius: 10px;
            }

            /* =====================================================
               RESPONSIVO
               ===================================================== */

            @media (max-width: 768px) {

                .vitta-ai-header {
                    padding-top: 18px;
                }

                .vitta-ai-header-title {
                    font-size: 26px;
                }

                .vitta-ai-header-subtitle {
                    margin-left: 0;
                }

                .vitta-ai-bubble {
                    max-width: 88%;
                }

                .vitta-user-bubble {
                    max-width: 88%;
                }
            }

            </style>
            """
        )

    # ================================================================
    # ESTADO
    # ================================================================

    def _inicializar_estado(self):

        if "vitta_conversations" not in st.session_state:

            st.session_state.vitta_conversations = {
                "Nova conversa": [
                    {
                        "role": "assistant",
                        "content": (
                            "Olá! Como posso ajudar você a consultar "
                            "os dados do SUS hoje?\n\n"
                            "Posso consultar **leitos, hospitais, "
                            "internações, UTIs e população**."
                        ),
                    }
                ]
            }

        if "vitta_current_conversation" not in st.session_state:

            st.session_state.vitta_current_conversation = (
                "Nova conversa"
            )

    # ================================================================
    # SIDEBAR
    # ================================================================

    def _render_sidebar(self):

        with st.sidebar:

            st.html(
                """
                <div class="vitta-sidebar-logo">

                    <div class="vitta-sidebar-icon">
                        ✦
                    </div>

                    <div>

                        <div class="vitta-sidebar-title">
                            VITTA AI
                        </div>

                        <div class="vitta-sidebar-subtitle">
                            Assistente de dados do SUS
                        </div>

                    </div>

                </div>
                """
            )

            st.divider()

            if st.button(
                "＋  Nova conversa",
                use_container_width=True,
                key="nova_conversa",
            ):

                nome = self._gerar_nome_conversa()

                st.session_state.vitta_conversations[nome] = [
                    {
                        "role": "assistant",
                        "content": (
                            "Olá! Como posso ajudar você a consultar "
                            "os dados do SUS hoje?\n\n"
                            "Posso consultar **leitos, hospitais, "
                            "internações, UTIs e população**."
                        ),
                    }
                ]

                st.session_state.vitta_current_conversation = nome

                st.rerun()

            st.html(
                """
                <div class="historico-titulo">
                    Histórico
                </div>
                """
            )

            nomes = list(
                st.session_state.vitta_conversations.keys()
            )

            for nome in nomes:

                col_conversa, col_remover = st.columns(
                    [5.5, 1]
                )

                ativo = (
                    nome
                    == st.session_state.vitta_current_conversation
                )

                label = (
                    f"●  {nome}"
                    if ativo
                    else f"　{nome}"
                )

                with col_conversa:

                    if st.button(
                        label,
                        key=f"conversation_{nome}",
                        use_container_width=True,
                    ):

                        st.session_state.vitta_current_conversation = (
                            nome
                        )

                        st.rerun()

                with col_remover:

                    if st.button(
                        "×",
                        key=f"delete_conversation_{nome}",
                        help="Remover conversa",
                    ):

                        del st.session_state.vitta_conversations[
                            nome
                        ]

                        if not st.session_state.vitta_conversations:

                            st.session_state.vitta_conversations[
                                "Nova conversa"
                            ] = [
                                {
                                    "role": "assistant",
                                    "content": (
                                        "Olá! Como posso ajudar você "
                                        "a consultar os dados do SUS hoje?\n\n"
                                        "Posso consultar **leitos, hospitais, "
                                        "internações, UTIs e população**."
                                    ),
                                }
                            ]

                        if (
                            st.session_state.vitta_current_conversation
                            == nome
                        ):

                            st.session_state.vitta_current_conversation = (
                                next(
                                    iter(
                                        st.session_state
                                        .vitta_conversations
                                    )
                                )
                            )

                        st.rerun()

            st.divider()

            st.html(
                """
                <div class="vitta-sidebar-footer">

                    <strong>
                        VITTA VISION
                    </strong>

                    <br>

                    Inteligência aplicada à saúde pública

                </div>
                """
            )

    # ================================================================
    # HEADER
    # ================================================================

    def _render_header(self):

        st.html(
            """
            <div class="vitta-ai-header">

                <div class="vitta-ai-header-title">

                    <div class="vitta-ai-header-icon">
                        ✦
                    </div>

                    <span>
                        VITTA AI
                    </span>

                </div>

                <div class="vitta-ai-header-subtitle">
                    Assistente inteligente para consulta
                    dos dados do SUS
                </div>

            </div>

            <div class="vitta-ai-header-divider"></div>
            """
        )

    # ================================================================
    # CONVERSA
    # ================================================================

    def _render_conversa(self):

        nome = st.session_state.vitta_current_conversation

        mensagens = st.session_state.vitta_conversations[nome]

        for indice, message in enumerate(mensagens):

            role = message["role"]

            conteudo = message["content"]

            self._render_conteudo(
                conteudo,
                indice,
                assistant=(role == "assistant"),
            )

    # ================================================================
    # CONTEÚDO
    # ================================================================

    def _render_conteudo(
        self,
        conteudo,
        indice,
        assistant=True,
    ):

        # ------------------------------------------------------------
        # RESULTADO ESTRUTURADO
        # ------------------------------------------------------------

        if isinstance(
            conteudo,
            (list, dict),
        ):

            dados = self._normalizar_resultado(
                conteudo
            )

            if dados:

                try:

                    df = pd.DataFrame(dados)

                except Exception:

                    df = None

                if (
                    df is not None
                    and not df.empty
                ):

                    self._render_resultado_visual(
                        df,
                        indice,
                        assistant,
                    )

                    return

        # ------------------------------------------------------------
        # TEXTO
        # ------------------------------------------------------------

        texto = str(conteudo)

        texto_html = self._texto_para_html(
            texto
        )

        if assistant:

            st.html(
                f"""
                <div class="vitta-chat-row vitta-chat-row-ai">

                    <div class="vitta-ai-avatar">
                        ✦
                    </div>

                    <div class="vitta-ai-bubble">

                        <div class="vitta-chat-text">
                            {texto_html}
                        </div>

                    </div>

                </div>
                """
            )

        else:

            st.html(
                f"""
                <div class="vitta-chat-row vitta-chat-row-user">

                    <div class="vitta-user-bubble">

                        <div class="vitta-chat-text">
                            {texto_html}
                        </div>

                    </div>

                    <div class="vitta-user-avatar">
                        ♙
                    </div>

                </div>
                """
            )

    # ================================================================
    # RESULTADO VISUAL
    # ================================================================

    def _render_resultado_visual(
        self,
        df,
        indice,
        assistant,
    ):

        if assistant:

            st.html(
                """
                <div class="vitta-chat-row vitta-chat-row-ai">

                    <div class="vitta-ai-avatar">
                        ✦
                    </div>

                    <div class="vitta-ai-bubble">
                        Resultado encontrado nos dados do SUS.
                    </div>

                </div>
                """
            )

        else:

            st.html(
                """
                <div class="vitta-chat-row vitta-chat-row-user">

                    <div class="vitta-user-bubble">
                        Consulta realizada.
                    </div>

                    <div class="vitta-user-avatar">
                        ♙
                    </div>

                </div>
                """
            )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        self._render_grafico(df)

        self._render_exportacoes(
            df,
            indice,
        )

    # ================================================================
    # CONVERTER TEXTO PARA HTML
    # ================================================================

    def _texto_para_html(
        self,
        texto,
    ):

        import html

        texto = html.escape(
            str(texto)
        )

        # Negrito
        texto = re.sub(
            r"\*\*(.+?)\*\*",
            r"<strong>\1</strong>",
            texto,
        )

        # Código inline
        texto = re.sub(
            r"`([^`]+)`",
            r"<code>\1</code>",
            texto,
        )

        # Quebras de linha
        blocos = texto.split("\n\n")

        resultado = []

        for bloco in blocos:

            bloco = bloco.replace(
                "\n",
                "<br>",
            )

            if bloco.strip():

                resultado.append(
                    f"<p>{bloco}</p>"
                )

        return "".join(
            resultado
        )

    # ================================================================
    # EXPORTAÇÕES
    # ================================================================

    def _render_exportacoes(
        self,
        df,
        indice,
    ):

        csv_data = self._gerar_csv(df)

        excel_data = self._gerar_excel(df)

        pdf_data = self._gerar_pdf(df)

        st.html(
            """
            <div class="vitta-export-title">
                📤 Exportar resultado
            </div>
            """
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.download_button(
                "📥  CSV",
                data=csv_data,
                file_name="vitta_relatorio_sus.csv",
                mime="text/csv",
                key=f"csv_{indice}",
                use_container_width=True,
            )

        with col2:

            st.download_button(
                "📊  Excel",
                data=excel_data,
                file_name="vitta_relatorio_sus.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument"
                    ".spreadsheetml.sheet"
                ),
                key=f"excel_{indice}",
                use_container_width=True,
            )

        with col3:

            st.download_button(
                "📄  PDF",
                data=pdf_data,
                file_name="vitta_relatorio_sus.pdf",
                mime="application/pdf",
                key=f"pdf_{indice}",
                use_container_width=True,
            )

    # ================================================================
    # CSV
    # ================================================================

    def _gerar_csv(
        self,
        df,
    ):

        return (
            df.to_csv(
                index=False
            )
            .encode(
                "utf-8-sig"
            )
        )

    # ================================================================
    # EXCEL
    # ================================================================

    def _gerar_excel(
        self,
        df,
    ):

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl",
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Dados SUS",
            )

            worksheet = writer.sheets["Dados SUS"]

            worksheet.freeze_panes = "A2"

            if len(df.columns) > 0:

                worksheet.auto_filter.ref = (
                    worksheet.dimensions
                )

            for coluna in worksheet.columns:

                maior_tamanho = 0

                letra = coluna[0].column_letter

                for celula in coluna:

                    try:

                        tamanho = len(
                            str(
                                celula.value
                            )
                        )

                        maior_tamanho = max(
                            maior_tamanho,
                            tamanho,
                        )

                    except Exception:

                        pass

                worksheet.column_dimensions[
                    letra
                ].width = min(
                    maior_tamanho + 3,
                    45,
                )

        output.seek(0)

        return output.getvalue()

    # ================================================================
    # PDF
    # ================================================================

    def _gerar_pdf(
        self,
        df,
    ):

        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import (
            getSampleStyleSheet,
            ParagraphStyle,
        )
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
        )

        output = BytesIO()

        documento = SimpleDocTemplate(
            output,
            pagesize=landscape(A4),
            rightMargin=10 * mm,
            leftMargin=10 * mm,
            topMargin=10 * mm,
            bottomMargin=10 * mm,
        )

        estilos = getSampleStyleSheet()

        estilo_titulo = ParagraphStyle(
            "TituloVitta",
            parent=estilos["Title"],
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            spaceAfter=6,
        )

        estilo_subtitulo = ParagraphStyle(
            "SubtituloVitta",
            parent=estilos["Normal"],
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.grey,
            spaceAfter=12,
        )

        estilo_celula = ParagraphStyle(
            "Celula",
            parent=estilos["Normal"],
            fontSize=6.5,
            leading=8,
        )

        estilo_cabecalho = ParagraphStyle(
            "Cabecalho",
            parent=estilos["Normal"],
            fontSize=6.5,
            leading=8,
            alignment=TA_CENTER,
            textColor=colors.white,
        )

        elementos = []

        elementos.append(
            Paragraph(
                "VITTA VISION",
                estilo_titulo,
            )
        )

        elementos.append(
            Paragraph(
                "Relatório de Dados do SUS",
                estilo_subtitulo,
            )
        )

        data_geracao = datetime.now().strftime(
            "%d/%m/%Y às %H:%M"
        )

        elementos.append(
            Paragraph(
                f"<b>Gerado em:</b> {data_geracao}"
                f" &nbsp;&nbsp;&nbsp; "
                f"<b>Registros:</b> {len(df)}"
                f" &nbsp;&nbsp;&nbsp; "
                f"<b>Colunas:</b> {len(df.columns)}",
                estilos["Normal"],
            )
        )

        elementos.append(
            Spacer(
                1,
                8,
            )
        )

        dados_pdf = []

        cabecalho = []

        for coluna in df.columns:

            cabecalho.append(
                Paragraph(
                    str(coluna),
                    estilo_cabecalho,
                )
            )

        dados_pdf.append(
            cabecalho
        )

        for _, linha in df.iterrows():

            linha_pdf = []

            for valor in linha:

                if pd.isna(valor):

                    texto = ""

                else:

                    texto = str(valor)

                if len(texto) > 100:

                    texto = texto[:97] + "..."

                texto = (
                    texto
                    .replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;")
                )

                linha_pdf.append(
                    Paragraph(
                        texto,
                        estilo_celula,
                    )
                )

            dados_pdf.append(
                linha_pdf
            )

        quantidade_colunas = len(
            df.columns
        )

        largura_disponivel = (
            landscape(A4)[0]
            - (20 * mm)
        )

        if quantidade_colunas > 0:

            largura_coluna = (
                largura_disponivel
                / quantidade_colunas
            )

            larguras = [
                largura_coluna
                for _ in range(
                    quantidade_colunas
                )
            ]

        else:

            larguras = None

        tabela = Table(
            dados_pdf,
            colWidths=larguras,
            repeatRows=1,
        )

        tabela.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#7C3AED"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.25,
                        colors.HexColor("#CBD5E1"),
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor("#F8FAFC"),
                        ],
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                ]
            )
        )

        elementos.append(
            tabela
        )

        documento.build(
            elementos
        )

        output.seek(0)

        return output.getvalue()

    # ================================================================
    # NORMALIZAR RESULTADO
    # ================================================================

    def _normalizar_resultado(
        self,
        conteudo,
    ):

        if isinstance(
            conteudo,
            dict,
        ):

            if "DADOS" in conteudo:

                dados = conteudo["DADOS"]

                if isinstance(
                    dados,
                    list,
                ):

                    return dados

            return [conteudo]

        if not isinstance(
            conteudo,
            list,
        ):

            return []

        resultado = []

        for item in conteudo:

            if isinstance(
                item,
                dict,
            ):

                if "DADOS" in item:

                    dados = item["DADOS"]

                    if isinstance(
                        dados,
                        list,
                    ):

                        resultado.extend(
                            dados
                        )

                else:

                    resultado.append(
                        item
                    )

        return resultado

    # ================================================================
    # GRÁFICO
    # ================================================================

    def _render_grafico(
        self,
        df,
    ):

        if len(df) < 2:
            return

        if len(df.columns) < 2:
            return

        colunas_numericas = (
            df.select_dtypes(
                include=["number"]
            )
            .columns
            .tolist()
        )

        if not colunas_numericas:
            return

        coluna_categoria = None

        for coluna in df.columns:

            if coluna not in colunas_numericas:

                coluna_categoria = coluna

                break

        if not coluna_categoria:
            return

        coluna_valor = colunas_numericas[0]

        try:

            chart = (
                df[
                    [
                        coluna_categoria,
                        coluna_valor,
                    ]
                ]
                .dropna()
                .set_index(
                    coluna_categoria
                )
            )

            if not chart.empty:

                st.bar_chart(
                    chart
                )

        except Exception:

            pass

    # ================================================================
    # INPUT
    # ================================================================

    def _render_input(self):

        nome = (
            st.session_state
            .vitta_current_conversation
        )

        mensagens = (
            st.session_state
            .vitta_conversations[nome]
        )

        if len(mensagens) == 1:

            st.html(
                """
                <div class="vitta-sugestoes">

                    <div class="vitta-sugestoes-title">
                        💡 Sugestões rápidas
                    </div>

                </div>
                """
            )

            col1, col2, col3 = st.columns(3)

            sugestao = None

            with col1:

                if st.button(
                    "📊  Municípios com mais leitos",
                    use_container_width=True,
                ):

                    sugestao = (
                        "Quais são os 10 municípios "
                        "com mais leitos existentes?"
                    )

            with col2:

                if st.button(
                    "📈  Ranking internações",
                    use_container_width=True,
                ):

                    sugestao = (
                        "Quais são os 10 municípios "
                        "com maior número de internações "
                        "em 2025?"
                    )

            with col3:

                if st.button(
                    "👥  Maior população",
                    use_container_width=True,
                ):

                    sugestao = (
                        "Quais são os 10 municípios "
                        "com maior população estimada?"
                    )

            if sugestao:

                self._processar_pergunta(
                    sugestao
                )

                return

        prompt = st.chat_input(
            "Pergunte qualquer coisa sobre os dados do SUS..."
        )

        if prompt:

            self._processar_pergunta(
                prompt
            )

    # ================================================================
    # PROCESSAR PERGUNTA
    # ================================================================

    def _processar_pergunta(
        self,
        prompt,
    ):

        nome = (
            st.session_state
            .vitta_current_conversation
        )

        mensagens = (
            st.session_state
            .vitta_conversations[nome]
        )

        mensagens.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        pergunta = (
            prompt
            .strip()
            .lower()
        )

        saudacoes = {
            "oi",
            "olá",
            "ola",
            "hey",
            "eae",
            "e aí",
            "bom dia",
            "boa tarde",
            "boa noite",
        }

        if pergunta in saudacoes:

            resposta = (
                "Olá! 😊\n\n"
                "Posso ajudar você a consultar "
                "os dados de saúde pública do VittaVision.\n\n"
                "Posso analisar **leitos, hospitais, "
                "internações, UTIs e população**."
            )

        elif len(pergunta) < 3:

            resposta = (
                "Digite uma pergunta mais completa "
                "sobre os dados do SUS."
            )

        else:

            with st.spinner(
                "Consultando o Oracle..."
            ):

                resposta = (
                    self._gerar_resposta_inteligente(
                        prompt
                    )
                )

        mensagens.append(
            {
                "role": "assistant",
                "content": resposta,
            }
        )

        if nome.startswith(
            "Nova conversa"
        ):

            primeiro_prompt = None

            for mensagem in mensagens:

                if mensagem["role"] == "user":

                    primeiro_prompt = (
                        mensagem["content"]
                    )

                    break

            if primeiro_prompt:

                novo_nome = (
                    self._criar_titulo_conversa(
                        primeiro_prompt
                    )
                )

                if (
                    novo_nome
                    in st.session_state.vitta_conversations
                ) and novo_nome != nome:

                    contador = 2

                    titulo_original = novo_nome

                    while (
                        novo_nome
                        in st.session_state.vitta_conversations
                    ):

                        novo_nome = (
                            f"{titulo_original} "
                            f"({contador})"
                        )

                        contador += 1

                if novo_nome != nome:

                    st.session_state.vitta_conversations[
                        novo_nome
                    ] = mensagens

                    del (
                        st.session_state
                        .vitta_conversations[nome]
                    )

                    st.session_state.vitta_current_conversation = (
                        novo_nome
                    )

        st.rerun()

    # ================================================================
    # IDENTIFICAR TABELA
    # ================================================================

    def _identificar_tabela(
        self,
        pergunta,
    ):

        pergunta = (
            pergunta
            .lower()
            .strip()
        )

        palavras_leitos = [
            "leito",
            "leitos",
            "hospital",
            "hospitais",
            "uti",
            "utis",
            "cnes",
            "estabelecimento",
        ]

        if any(
            palavra in pergunta
            for palavra in palavras_leitos
        ):

            return "TB_LEITOS"

        palavras_internacoes = [
            "internação",
            "internações",
            "internacao",
            "internacoes",
            "internado",
            "internados",
        ]

        if any(
            palavra in pergunta
            for palavra in palavras_internacoes
        ):

            return "TB_INTERNACOES"

        palavras_populacao = [
            "população",
            "populacao",
            "habitante",
            "habitantes",
            "populacional",
        ]

        if any(
            palavra in pergunta
            for palavra in palavras_populacao
        ):

            return "TB_POPULACAO"

        return None

    # ================================================================
    # CONSTRUIR PROMPT
    # ================================================================

    def _construir_prompt(
        self,
        pergunta,
        tabela,
    ):

        config = self.TABELAS[tabela]

        campos = ", ".join(
            config["campos"]
        )

        prompt = f"""
Você é o assistente de dados do VITTA VISION.

A pergunta do usuário deve ser respondida utilizando
SOMENTE a tabela {tabela}.

Descrição da tabela:
{config["descricao"]}

Tabela permitida:
{tabela}

Coluna de município:
{config["municipio"]}

Código do município:
{config["codigo_municipio"]}

Colunas disponíveis:
{campos}

REGRAS IMPORTANTES:

1. Use SOMENTE a tabela {tabela}.
2. NÃO faça JOIN com outras tabelas.
3. NÃO utilize outras tabelas do banco.
4. Para município, utilize a coluna
   {config["municipio"]}.
5. Para identificação municipal, utilize
   {config["codigo_municipio"]}.
6. Gere somente consultas SQL de leitura.
7. Não faça INSERT, UPDATE, DELETE, DROP ou ALTER.
8. Responda exatamente à pergunta do usuário.
9. Quando a pergunta pedir "10", limite o resultado
   aos 10 primeiros registros.
10. Quando houver uma quantidade numérica,
    ordene de forma decrescente quando isso fizer
    sentido para a pergunta.
11. Retorne somente JSON válido.
12. Não coloque explicações antes ou depois do JSON.

PERGUNTA DO USUÁRIO:

{pergunta}
"""

        return prompt.strip()

    # ================================================================
    # ORACLE SELECT AI
    # ================================================================

    def _gerar_resposta_inteligente(
        self,
        query,
    ):

        tabela = (
            self._identificar_tabela(
                query
            )
        )

        if not tabela:

            return (
                "🤔 Não consegui identificar qual conjunto "
                "de dados você deseja consultar.\n\n"
                "Tente mencionar **leitos, internações, "
                "UTIs ou população**."
            )

        prompt = (
            self._construir_prompt(
                query,
                tabela,
            )
        )

        connection = None
        cursor = None

        try:

            db = OracleDatabase()

            connection = db._conectar()

            cursor = connection.cursor()

            try:

                cursor.call_timeout = 30000

            except Exception:

                pass

            sql = """
                SELECT DBMS_CLOUD_AI.GENERATE(
                    prompt => :prompt,
                    profile_name => :profile_name,
                    action => 'runsql'
                )
                FROM dual
            """

            cursor.execute(
                sql,
                {
                    "prompt": prompt,
                    "profile_name": self.ORACLE_PROFILE,
                },
            )

            resultado = cursor.fetchone()

            if not resultado:

                return (
                    "Não consegui obter uma resposta "
                    "para essa consulta."
                )

            bruto = resultado[0]

            if bruto is None:

                return (
                    "Não consegui obter uma resposta "
                    "para essa consulta."
                )

            if hasattr(
                bruto,
                "read",
            ):

                texto = bruto.read()

            else:

                texto = str(bruto)

            texto = texto.strip()

            if not texto:

                return (
                    "Não consegui obter uma resposta "
                    "para essa consulta."
                )

            dados = self._tentar_json(
                texto
            )

            if dados is not None:

                return dados

            texto_lower = texto.lower()

            # --------------------------------------------------------
            # RESPOSTAS QUE NÃO DEVEM SER MOSTRADAS AO USUÁRIO
            # --------------------------------------------------------

            erros_ia = [
                "no valid response generated",
                "ora-20422",
                "http 422",
                "request failed with status",
                "bearer://api.cohere.ai",
                "try updating messages",
            ]

            if any(
                erro in texto_lower
                for erro in erros_ia
            ):

                return (
                    "🤔 Não consegui encontrar uma resposta "
                    "confiável para essa pergunta.\n\n"
                    "Tente reformular a consulta ou "
                    "especificar melhor o que deseja analisar."
                )

            if "max_tokens" in texto_lower:

                return (
                    "A consulta retornou dados demais "
                    "para serem exibidos de uma vez.\n\n"
                    "Tente solicitar uma quantidade menor "
                    "de resultados."
                )

            return texto

        except Exception as erro:

            erro_texto = str(
                erro
            )

            erro_lower = (
                erro_texto.lower()
            )

            # --------------------------------------------------------
            # TIMEOUT
            # --------------------------------------------------------

            if (
                "call timeout"
                in erro_lower
                or "dpi-1080"
                in erro_lower
            ):

                return (
                    "⏱️ A consulta demorou mais do que "
                    "o esperado.\n\n"
                    "Tente fazer uma consulta mais específica."
                )

            # --------------------------------------------------------
            # WALLET
            # --------------------------------------------------------

            if (
                "wallet"
                in erro_lower
                or "dp-4011"
                in erro_lower
                or "dpy-4011"
                in erro_lower
                or "dpy-4026"
                in erro_lower
            ):

                return (
                    "Não foi possível estabelecer conexão "
                    "com o banco de dados no momento."
                )

            # --------------------------------------------------------
            # ERROS DA IA / COHERE / ORA-20422
            # NÃO MOSTRAR ERRO TÉCNICO
            # --------------------------------------------------------

            erros_tecnicos = [
                "ora-20422",
                "no valid response generated",
                "http 422",
                "request failed with status",
                "api.cohere.ai",
                "bearer://",
                "ora-06512",
                "dbms_cloud_ai",
            ]

            if any(
                termo in erro_lower
                for termo in erros_tecnicos
            ):

                return (
                    "🤔 Não consegui gerar uma resposta "
                    "para essa pergunta.\n\n"
                    "Tente reformular sua consulta ou "
                    "deixe o pedido mais específico."
                )

            # --------------------------------------------------------
            # FALLBACK
            # --------------------------------------------------------

            return (
                "Não consegui concluir essa consulta "
                "neste momento.\n\n"
                "Tente novamente ou reformule a pergunta."
            )

        finally:

            if cursor:

                try:
                    cursor.close()

                except Exception:
                    pass

            if connection:

                try:
                    connection.close()

                except Exception:
                    pass

    # ================================================================
    # TENTAR JSON
    # ================================================================

    def _tentar_json(
        self,
        texto,
    ):

        texto = texto.strip()

        try:

            dados = json.loads(
                texto
            )

            if isinstance(
                dados,
                (list, dict),
            ):

                return dados

        except (
            json.JSONDecodeError,
            TypeError,
        ):

            pass

        inicio_lista = texto.find(
            "["
        )

        fim_lista = texto.rfind(
            "]"
        )

        if (
            inicio_lista >= 0
            and fim_lista > inicio_lista
        ):

            trecho = (
                texto[
                    inicio_lista:
                    fim_lista + 1
                ]
            )

            try:

                dados = json.loads(
                    trecho
                )

                if isinstance(
                    dados,
                    list,
                ):

                    return dados

            except (
                json.JSONDecodeError,
                TypeError,
            ):

                pass

        inicio_objeto = texto.find(
            "{"
        )

        fim_objeto = texto.rfind(
            "}"
        )

        if (
            inicio_objeto >= 0
            and fim_objeto > inicio_objeto
        ):

            trecho = (
                texto[
                    inicio_objeto:
                    fim_objeto + 1
                ]
            )

            try:

                dados = json.loads(
                    trecho
                )

                if isinstance(
                    dados,
                    dict,
                ):

                    return dados

            except (
                json.JSONDecodeError,
                TypeError,
            ):

                pass

        return None

    # ================================================================
    # TÍTULO DA CONVERSA
    # ================================================================

    def _criar_titulo_conversa(
        self,
        pergunta,
    ):

        texto = pergunta.strip()

        texto = " ".join(
            texto.split()
        )

        if len(texto) > 32:

            texto = (
                texto[:32]
                .rstrip()
                + "..."
            )

        return texto

    # ================================================================
    # NOVA CONVERSA
    # ================================================================

    def _gerar_nome_conversa(
        self,
    ):

        base = "Nova conversa"

        if (
            base
            not in st.session_state
            .vitta_conversations
        ):

            return base

        contador = 2

        while True:

            nome = (
                f"Nova conversa {contador}"
            )

            if (
                nome
                not in st.session_state
                .vitta_conversations
            ):

                return nome

            contador += 1