import json
from io import BytesIO
from datetime import datetime

import pandas as pd
import streamlit as st

from model.oracle_connection import OracleDatabase


class AssistenteIAView:
    """Assistente VITTA AI integrado ao Oracle Select AI."""

    # ================================================================
    # CONFIGURAÇÕES
    # ================================================================

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

        self._render_sidebar()
        self._render_header()
        self._render_conversa()
        self._render_input()

    # ================================================================
    # ESTILO
    # ================================================================

    def _aplicar_estilo(self):

        st.markdown(
            """
            <style>

            :root {
                --vitta-blue: #2563eb;
                --vitta-blue-light: #3b82f6;
                --vitta-purple: #7c3aed;
                --vitta-purple-light: #8b5cf6;

                --vitta-bg: #080b16;
                --vitta-bg-2: #0d1120;
                --vitta-sidebar: #090d19;

                --vitta-card: #111728;
                --vitta-card-2: #151b2e;

                --vitta-border:
                    rgba(139, 92, 246, 0.18);

                --vitta-text: #f8fafc;
                --vitta-muted: #94a3b8;
            }

            .stApp {
                background:
                    radial-gradient(
                        circle at 75% 10%,
                        rgba(37, 99, 235, 0.09),
                        transparent 30%
                    ),
                    radial-gradient(
                        circle at 45% 80%,
                        rgba(124, 58, 237, 0.07),
                        transparent 30%
                    ),
                    var(--vitta-bg);

                color: var(--vitta-text);
            }

            html,
            body,
            [data-testid="stAppViewContainer"],
            [data-testid="stHeader"],
            [data-testid="stToolbar"] {
                background-color: #080b16 !important;
            }

            [data-testid="stAppViewContainer"] {
                background:
                    radial-gradient(
                        circle at 75% 10%,
                        rgba(37, 99, 235, 0.09),
                        transparent 30%
                    ),
                    radial-gradient(
                        circle at 45% 80%,
                        rgba(124, 58, 237, 0.07),
                        transparent 30%
                    ),
                    #080b16 !important;
            }

            .main .block-container {
                max-width: 1050px;
                padding-top: 35px;
                padding-bottom: 120px;
            }

            header[data-testid="stHeader"] {
                background: transparent !important;
            }

            footer {
                visibility: hidden;
            }

            section[data-testid="stSidebar"] {
                background:
                    linear-gradient(
                        180deg,
                        #080b16 0%,
                        #0b0f1d 100%
                    ) !important;

                border-right:
                    1px solid
                    rgba(124, 58, 237, 0.18);
            }

            section[data-testid="stSidebar"] > div {
                padding-top: 25px;
            }

            section[data-testid="stSidebar"] * {
                color: #e2e8f0;
            }

            .vitta-logo {
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 5px;
            }

            .vitta-logo-icon {
                width: 42px;
                height: 42px;
                min-width: 42px;

                display: flex;
                align-items: center;
                justify-content: center;

                border-radius: 13px;

                background:
                    linear-gradient(
                        135deg,
                        #2563eb,
                        #7c3aed
                    );

                box-shadow:
                    0 8px 25px
                    rgba(79, 70, 229, 0.30);

                font-size: 21px;
            }

            .vitta-logo-title {
                font-size: 21px;
                font-weight: 750;
                color: #ffffff;
            }

            .vitta-logo-subtitle {
                font-size: 12px;
                color: #64748b;
                margin-top: -2px;
            }

            hr {
                border: none !important;

                border-top:
                    1px solid
                    rgba(148, 163, 184, 0.08)
                    !important;

                margin-top: 18px !important;
                margin-bottom: 18px !important;
            }

            section[data-testid="stSidebar"]
            .stButton {
                margin-bottom: 3px;
            }

            section[data-testid="stSidebar"]
            .stButton button {
                border-radius: 10px;

                border:
                    1px solid
                    rgba(139, 92, 246, 0.14);

                background:
                    rgba(255, 255, 255, 0.025);

                color: #cbd5e1 !important;

                transition:
                    background 0.2s ease,
                    border 0.2s ease,
                    transform 0.2s ease;
            }

            section[data-testid="stSidebar"]
            .stButton button:hover {
                background:
                    linear-gradient(
                        90deg,
                        rgba(37, 99, 235, 0.16),
                        rgba(124, 58, 237, 0.16)
                    );

                border-color:
                    rgba(139, 92, 246, 0.40);

                color: #ffffff !important;

                transform: translateY(-1px);
            }

            section[data-testid="stSidebar"]
            button[kind="secondary"] {
                min-height: 42px;
            }

            .historico-titulo {
                color: #64748b;

                font-size: 11px;

                font-weight: 700;

                text-transform: uppercase;

                letter-spacing: 1px;

                margin-top: 25px;

                margin-bottom: 8px;
            }

            section[data-testid="stSidebar"]
            .stButton button {
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }

            .vitta-header {
                margin-bottom: 20px;
            }

            .vitta-header-title {
                display: flex;
                align-items: center;
                gap: 13px;

                font-size: 32px;
                font-weight: 750;

                letter-spacing: -1px;

                color: #ffffff;
            }

            .vitta-header-icon {
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
                        #2563eb,
                        #7c3aed
                    );

                box-shadow:
                    0 10px 30px
                    rgba(79, 70, 229, 0.28);

                font-size: 22px;
            }

            .vitta-header-subtitle {
                margin-top: 7px;
                margin-left: 58px;

                color: #64748b;

                font-size: 14px;
                line-height: 1.5;
            }

            [data-testid="stChatMessage"] {
                background: transparent;
                border: none;

                padding-top: 18px;
                padding-bottom: 18px;
            }

            [data-testid="chatAvatarIcon-user"] {
                background:
                    linear-gradient(
                        135deg,
                        #2563eb,
                        #4f46e5
                    ) !important;
            }

            [data-testid="chatAvatarIcon-assistant"] {
                background:
                    linear-gradient(
                        135deg,
                        #7c3aed,
                        #2563eb
                    ) !important;
            }

            [data-testid="stChatMessage"]:has(
                [data-testid="chatAvatarIcon-user"]
            ) {
                background:
                    rgba(37, 99, 235, 0.045);

                border-top:
                    1px solid
                    rgba(37, 99, 235, 0.08);

                border-bottom:
                    1px solid
                    rgba(37, 99, 235, 0.08);
            }

            [data-testid="stChatMessage"]:has(
                [data-testid="chatAvatarIcon-assistant"]
            ) {
                background:
                    rgba(124, 58, 237, 0.025);
            }

            [data-testid="stChatMessage"] p {
                color: #e2e8f0;

                font-size: 15px;
                line-height: 1.65;
            }

            [data-testid="stChatMessage"] strong {
                color: #ffffff;
            }

            [data-testid="stChatMessage"] code {
                background:
                    rgba(124, 58, 237, 0.10);

                border:
                    1px solid
                    rgba(124, 58, 237, 0.16);

                color: #c4b5fd;

                border-radius: 5px;

                padding: 2px 5px;
            }

            [data-testid="stDataFrame"] {
                border-radius: 14px;
                overflow: hidden;

                border:
                    1px solid
                    rgba(124, 58, 237, 0.18);

                box-shadow:
                    0 10px 35px
                    rgba(0, 0, 0, 0.18);
            }

            [data-testid="stDownloadButton"] button {
                border-radius: 9px;

                background:
                    rgba(37, 99, 235, 0.08);

                border:
                    1px solid
                    rgba(37, 99, 235, 0.25);

                color: #93c5fd;

                transition: all 0.2s ease;
            }

            [data-testid="stDownloadButton"] button:hover {
                background:
                    rgba(124, 58, 237, 0.15);

                border-color:
                    rgba(139, 92, 246, 0.45);

                color: #ffffff;
            }

            .sugestoes-container {
                margin-top: 32px;
                margin-bottom: 12px;
            }

            .sugestoes-titulo {
                color: #64748b;

                font-size: 12px;
                font-weight: 700;

                letter-spacing: 0.4px;

                margin-bottom: 12px;
            }

            .main .stButton button {
                min-height: 48px;

                border-radius: 14px;

                border:
                    1px solid
                    rgba(139, 92, 246, 0.16);

                background:
                    linear-gradient(
                        145deg,
                        rgba(17, 23, 40, 0.95),
                        rgba(21, 27, 46, 0.85)
                    );

                color: #cbd5e1 !important;

                font-size: 13px;
                font-weight: 600;

                box-shadow:
                    0 6px 20px
                    rgba(0, 0, 0, 0.16);

                transition:
                    all 0.22s ease;

                position: relative;
                overflow: hidden;
            }

            .main .stButton button:hover {
                transform:
                    translateY(-3px);

                border-color:
                    rgba(139, 92, 246, 0.45);

                background:
                    linear-gradient(
                        135deg,
                        rgba(37, 99, 235, 0.13),
                        rgba(124, 58, 237, 0.16)
                    );

                color:
                    #ffffff !important;

                box-shadow:
                    0 10px 28px
                    rgba(79, 70, 229, 0.18);
            }

            .main .stButton button:active {
                transform:
                    translateY(-1px);

                box-shadow:
                    0 5px 15px
                    rgba(79, 70, 229, 0.15);
            }

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

                transition:
                    border 0.2s ease,
                    box-shadow 0.2s ease;
            }

            [data-testid="stChatInput"] > div:focus-within {
                border-color:
                    rgba(99, 102, 241, 0.65);

                box-shadow:
                    0 0 0 3px
                    rgba(99, 102, 241, 0.08),
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
                        #2563eb,
                        #7c3aed
                    ) !important;

                border: none;
                border-radius: 10px;

                transition:
                    transform 0.2s ease,
                    box-shadow 0.2s ease;
            }

            [data-testid="stChatInput"] button:hover {
                transform: scale(1.04);

                box-shadow:
                    0 5px 20px
                    rgba(124, 58, 237, 0.35);
            }

            [data-testid="stSpinner"] {
                color: #8b5cf6;
            }

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
                        #2563eb,
                        #7c3aed
                    );

                border-radius: 10px;
            }

            @media (max-width: 768px) {

                .main .block-container {
                    padding-left: 15px;
                    padding-right: 15px;
                }

                .vitta-header-title {
                    font-size: 26px;
                }

                .vitta-header-subtitle {
                    margin-left: 0;
                }
            }

            </style>
            """,
            unsafe_allow_html=True,
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
                <div class="vitta-logo">

                    <div class="vitta-logo-icon">
                        🤖
                    </div>

                    <div>

                        <div class="vitta-logo-title">
                            VITTA AI
                        </div>

                        <div class="vitta-logo-subtitle">
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

                if ativo:
                    label = f"🔵  {nome}"
                else:
                    label = f"　{nome}"

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
                <div style="
                    color:#475569;
                    font-size:11px;
                    line-height:1.6;
                    padding:4px 2px;
                ">

                    <strong style="
                        color:#64748b;
                        font-weight:700;
                    ">
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
            <div class="vitta-header">

                <div class="vitta-header-title">

                    <div class="vitta-header-icon">
                        🤖
                    </div>

                    <span>
                        VITTA AI
                    </span>

                </div>

                <div class="vitta-header-subtitle">
                    Assistente inteligente para consulta
                    dos dados do SUS
                </div>

            </div>
            """
        )

        st.divider()

    # ================================================================
    # CONVERSA
    # ================================================================

    def _render_conversa(self):

        nome = (
            st.session_state.vitta_current_conversation
        )

        mensagens = (
            st.session_state.vitta_conversations[nome]
        )

        for indice, message in enumerate(mensagens):

            role = message["role"]

            conteudo = message["content"]

            avatar = (
                "🤖"
                if role == "assistant"
                else "👤"
            )

            with st.chat_message(
                role,
                avatar=avatar,
            ):

                self._render_conteudo(
                    conteudo,
                    indice,
                )

    # ================================================================
    # CONTEÚDO
    # ================================================================

    def _render_conteudo(
        self,
        conteudo,
        indice,
    ):

        if isinstance(
            conteudo,
            (list, dict),
        ):

            dados = self._normalizar_resultado(
                conteudo
            )

            if dados:

                try:

                    df = pd.DataFrame(
                        dados
                    )

                except Exception:

                    df = None

                if (
                    df is not None
                    and not df.empty
                ):

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                    )

                    self._render_grafico(
                        df
                    )

                    # ====================================================
                    # EXPORTAÇÕES
                    # ====================================================

                    self._render_exportacoes(
                        df,
                        indice,
                    )

                    return

        st.markdown(
            str(conteudo)
        )

    # ================================================================
    # EXPORTAÇÕES
    # ================================================================

    def _render_exportacoes(
        self,
        df,
        indice,
    ):
        """
        Renderiza os botões para exportar os dados
        em CSV, Excel e PDF.
        """

        # ============================================================
        # PREPARAR ARQUIVOS
        # ============================================================

        csv_data = self._gerar_csv(
            df
        )

        excel_data = self._gerar_excel(
            df
        )

        pdf_data = self._gerar_pdf(
            df
        )

        # ============================================================
        # TÍTULO
        # ============================================================

        st.markdown(
            """
            <div style="
                margin-top:18px;
                margin-bottom:10px;
                color:#64748b;
                font-size:12px;
                font-weight:700;
                letter-spacing:0.4px;
            ">
                📤 Exportar resultado
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ============================================================
        # BOTÕES
        # ============================================================

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
    # GERAR CSV
    # ================================================================

    def _gerar_csv(
        self,
        df,
    ):
        """
        Gera o DataFrame em CSV UTF-8 com BOM,
        garantindo compatibilidade com Excel.
        """

        return (
            df
            .to_csv(
                index=False
            )
            .encode(
                "utf-8-sig"
            )
        )

    # ================================================================
    # GERAR EXCEL
    # ================================================================

    def _gerar_excel(
        self,
        df,
    ):
        """
        Gera um arquivo Excel .xlsx em memória.
        """

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

            workbook = writer.book

            worksheet = (
                writer.sheets["Dados SUS"]
            )

            # --------------------------------------------------------
            # Congelar cabeçalho
            # --------------------------------------------------------

            worksheet.freeze_panes = "A2"

            # --------------------------------------------------------
            # Filtro automático
            # --------------------------------------------------------

            if len(df.columns) > 0:

                worksheet.auto_filter.ref = (
                    worksheet.dimensions
                )

            # --------------------------------------------------------
            # Ajustar largura das colunas
            # --------------------------------------------------------

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

                        if tamanho > maior_tamanho:

                            maior_tamanho = tamanho

                    except Exception:

                        pass

                largura = min(
                    maior_tamanho + 3,
                    45,
                )

                worksheet.column_dimensions[
                    letra
                ].width = largura

        output.seek(0)

        return output.getvalue()

    # ================================================================
    # GERAR PDF
    # ================================================================

    def _gerar_pdf(
        self,
        df,
    ):
        """
        Gera um PDF contendo:
        - título do VITTA VISION
        - data/hora da geração
        - quantidade de registros
        - tabela de dados
        """

        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
        )

        output = BytesIO()

        # ============================================================
        # CONFIGURAÇÃO DA PÁGINA
        # ============================================================

        documento = SimpleDocTemplate(
            output,
            pagesize=landscape(A4),
            rightMargin=10 * mm,
            leftMargin=10 * mm,
            topMargin=10 * mm,
            bottomMargin=10 * mm,
        )

        # ============================================================
        # ESTILOS
        # ============================================================

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

        # ============================================================
        # TÍTULO
        # ============================================================

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

        # ============================================================
        # INFORMAÇÕES
        # ============================================================

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

        # ============================================================
        # PREPARAR DADOS
        # ============================================================

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

                    texto = str(
                        valor
                    )

                # Evitar conteúdo excessivamente grande
                if len(texto) > 100:

                    texto = (
                        texto[:97]
                        + "..."
                    )

                # Escapar caracteres HTML
                texto = (
                    texto
                    .replace(
                        "&",
                        "&amp;",
                    )
                    .replace(
                        "<",
                        "&lt;",
                    )
                    .replace(
                        ">",
                        "&gt;",
                    )
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

        # ============================================================
        # LARGURA DAS COLUNAS
        # ============================================================

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

        # ============================================================
        # TABELA
        # ============================================================

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
                        colors.HexColor(
                            "#2563EB"
                        ),
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
                        colors.HexColor(
                            "#CBD5E1"
                        ),
                    ),

                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor(
                                "#F8FAFC"
                            ),
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

        # ============================================================
        # GERAR
        # ============================================================

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

        coluna_valor = (
            colunas_numericas[0]
        )

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
                <div class="sugestoes-container">

                    <div class="sugestoes-titulo">
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

        # ============================================================
        # RENOMEAR PELO PRIMEIRO PROMPT
        # ============================================================

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
                    "profile_name": (
                        self.ORACLE_PROFILE
                    ),
                },
            )

            resultado = (
                cursor.fetchone()
            )

            if not resultado:

                return (
                    "⚠️ O Oracle Select AI não retornou "
                    "nenhum resultado."
                )

            bruto = resultado[0]

            if bruto is None:

                return (
                    "⚠️ O Oracle Select AI retornou "
                    "uma resposta vazia."
                )

            if hasattr(
                bruto,
                "read",
            ):

                texto = bruto.read()

            else:

                texto = str(
                    bruto
                )

            texto = texto.strip()

            if not texto:

                return (
                    "⚠️ O Oracle Select AI retornou "
                    "uma resposta vazia."
                )

            dados = (
                self._tentar_json(
                    texto
                )
            )

            if dados is not None:

                return dados

            texto_lower = (
                texto.lower()
            )

            if (
                "no valid response generated"
                in texto_lower
            ):

                return (
                    "⚠️ **O Oracle Select AI não conseguiu "
                    "gerar uma consulta válida.**\n\n"
                    "A pergunta foi direcionada para "
                    f"`{tabela}`.\n\n"
                    "Tente deixar a pergunta mais específica."
                )

            if "ora-20422" in texto_lower:

                return (
                    "⚠️ **O Oracle Select AI retornou "
                    "ORA-20422.**\n\n"
                    f"`{texto}`"
                )

            if "max_tokens" in texto_lower:

                return (
                    "⚠️ **A resposta ultrapassou o limite "
                    "de tokens.**\n\n"
                    "Tente solicitar menos resultados."
                )

            return texto

        except Exception as erro:

            erro_texto = str(
                erro
            )

            erro_lower = (
                erro_texto.lower()
            )

            if (
                "call timeout"
                in erro_lower
                or "dpi-1080"
                in erro_lower
            ):

                return (
                    "⏱️ **A consulta ultrapassou o limite "
                    "de 30 segundos.**\n\n"
                    "Tente fazer uma consulta mais específica."
                )

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
                    "⚠️ **Não foi possível acessar o Wallet "
                    "do Oracle.**\n\n"
                    "Verifique a configuração do Oracle."
                )

            return (
                "⚠️ **Erro ao consultar o Oracle.**\n\n"
                f"`{erro_texto}`"
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

        texto = (
            pergunta
            .strip()
        )

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
    # NOME DA NOVA CONVERSA
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