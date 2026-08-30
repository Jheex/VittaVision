import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# EXPORTAÇÃO CSV
# =========================================================

@st.cache_data(
    show_spinner=False,
    max_entries=3
)
def converter_df_para_csv(df_export):

    return (
        df_export
        .to_csv(index=False)
        .encode("utf-8")
    )


class DashboardView:

    # =====================================================
    # RENDER PRINCIPAL
    # =====================================================

    def render(self, model):

        self._aplicar_estilos()

        # =================================================
        # CABEÇALHO
        # =================================================

        self._render_cabecalho()

        # =================================================
        # SEM FILTROS
        # Dashboard sempre exibe toda a rede
        # =================================================

        uf_atual = None
        municipio_atual = None

        # =================================================
        # BUSCAR RESUMO
        # =================================================

        try:

            resumo = model.get_resumo(
                uf=uf_atual,
                municipio=municipio_atual
            )

        except Exception as e:

            st.error(
                "Não foi possível carregar o resumo do dashboard."
            )

            st.exception(e)

            return

        if resumo is None:

            resumo = {}

        # =================================================
        # INDICADORES
        # =================================================

        self._render_kpis(
            resumo
        )

        st.write("")

        # =================================================
        # GRÁFICOS
        # =================================================

        self._render_graficos(
            model,
            uf_atual,
            municipio_atual
        )

        st.write("")

        # =================================================
        # VITTA IA
        # =================================================

        self._render_chatbot(
            model,
            uf_atual,
            municipio_atual
        )

    # =====================================================
    # CABEÇALHO
    # =====================================================

    def _render_cabecalho(self):

        st.html(
            """
            <div class="page-header">

                <div class="header-icon">
                    ◈
                </div>

                <div class="header-content">

                    <div class="header-eyebrow">
                        VITTA VISION • INTELIGÊNCIA EM SAÚDE
                    </div>

                    <div class="header-title">
                        Dashboard <span>Hospitalar</span>
                    </div>

                    <div class="header-description">
                        Visão integrada da capacidade hospitalar,
                        infraestrutura, internações e indicadores
                        da rede de saúde.
                    </div>

                </div>

                <div class="header-status">

                    <div class="header-status-dot">
                        ●
                    </div>

                    <div class="header-status-text">
                        REDE MONITORADA
                    </div>

                </div>

            </div>
            """
        )

    # =====================================================
    # KPIs
    # =====================================================

    def _render_kpis(
        self,
        resumo
    ):

        col1, col2, col3, col4 = st.columns(
            4,
            gap="medium"
        )

        # =================================================
        # HOSPITAIS
        # =================================================

        with col1:

            self._render_kpi_card(
                icone="⌂",
                titulo="Hospitais",
                valor=self._formatar_numero(
                    resumo.get(
                        "hospitais",
                        0
                    )
                ),
                descricao="Estabelecimentos hospitalares",
                detalhe="REDE HOSPITALAR",
                classe="blue"
            )

        # =================================================
        # LEITOS
        # =================================================

        with col2:

            self._render_kpi_card(
                icone="▣",
                titulo="Leitos",
                valor=self._formatar_numero(
                    resumo.get(
                        "leitos",
                        0
                    )
                ),
                descricao="Capacidade hospitalar",
                detalhe="CAPACIDADE TOTAL",
                classe="cyan"
            )

        # =================================================
        # INTERNAÇÕES
        # =================================================

        with col3:

            self._render_kpi_card(
                icone="＋",
                titulo="Internações",
                valor=self._formatar_numero(
                    resumo.get(
                        "internacoes",
                        0
                    )
                ),
                descricao="Registros de internações",
                detalhe="ATENDIMENTO",
                classe="purple"
            )

        # =================================================
        # MUNICÍPIOS
        # =================================================

        with col4:

            self._render_kpi_card(
                icone="⌘",
                titulo="Municípios",
                valor=self._formatar_numero(
                    resumo.get(
                        "municipios",
                        0
                    )
                ),
                descricao="Municípios monitorados",
                detalhe="COBERTURA",
                classe="indigo"
            )

    # =====================================================
    # CARD KPI
    # =====================================================

    def _render_kpi_card(
        self,
        icone,
        titulo,
        valor,
        descricao,
        detalhe,
        classe
    ):

        st.html(
            f"""
            <div class="kpi-card {classe}">

                <div class="kpi-glow"></div>

                <div class="kpi-top">

                    <div class="kpi-icon">
                        {icone}
                    </div>

                    <div class="kpi-tag">
                        {detalhe}
                    </div>

                </div>

                <div class="kpi-title">
                    {titulo}
                </div>

                <div class="kpi-value">
                    {valor}
                </div>

                <div class="kpi-description">
                    {descricao}
                </div>

                <div class="kpi-line"></div>

            </div>
            """
        )

    # =====================================================
    # GRÁFICOS
    # =====================================================

    def _render_graficos(
        self,
        model,
        uf,
        municipio
    ):

        # =================================================
        # TÍTULO DA SEÇÃO
        # =================================================

        st.html(
            """
            <div class="section-heading">

                <div class="section-heading-icon">
                    📊
                </div>

                <div>

                    <div class="section-heading-title">
                        Visão Analítica
                    </div>

                    <div class="section-heading-subtitle">
                        Evolução das internações e capacidade da rede hospitalar
                    </div>

                </div>

            </div>
            """
        )

        col_esquerda, col_direita = st.columns(
            2,
            gap="medium"
        )

        # =================================================
        # INTERNAÇÕES
        # =================================================

        with col_esquerda:

            st.html(
                """
                <div class="chart-box">

                    <div class="chart-title">
                        📈 Evolução das Internações
                    </div>

                    <div class="chart-subtitle">
                        Distribuição das internações ao longo do período
                    </div>

                </div>
                """
            )

            try:

                df_internacoes = model.get_internacoes_data(
                    uf=uf,
                    municipio=municipio
                )

            except Exception as e:

                st.error(
                    "Erro ao carregar dados de internações."
                )

                st.exception(e)

                df_internacoes = pd.DataFrame()

            if (
                isinstance(
                    df_internacoes,
                    pd.DataFrame
                )
                and not df_internacoes.empty
            ):

                coluna_data = self._encontrar_coluna(
                    df_internacoes,
                    [
                        "DATA",
                        "Data",
                        "data",
                        "COMPETENCIA",
                        "competencia"
                    ]
                )

                coluna_valor = self._encontrar_coluna(
                    df_internacoes,
                    [
                        "VALOR",
                        "Valor",
                        "valor",
                        "INTERNACOES",
                        "Internacoes",
                        "internacoes",
                        "QUANTIDADE",
                        "quantidade"
                    ]
                )

                if coluna_data and coluna_valor:

                    df_grafico = (
                        df_internacoes.copy()
                    )

                    df_grafico[coluna_valor] = pd.to_numeric(
                        df_grafico[coluna_valor],
                        errors="coerce"
                    )

                    df_grafico = df_grafico.dropna(
                        subset=[
                            coluna_valor
                        ]
                    )

                    fig = go.Figure()

                    fig.add_trace(
                        go.Scatter(
                            x=df_grafico[
                                coluna_data
                            ],
                            y=df_grafico[
                                coluna_valor
                            ],
                            mode="lines+markers",
                            line=dict(
                                color="#6366F1",
                                width=3
                            ),
                            marker=dict(
                                color="#8B5CF6",
                                size=8
                            ),
                            fill="tozeroy",
                            fillcolor="rgba(99,102,241,0.10)",
                            hovertemplate=(
                                "<b>%{x}</b>"
                                "<br>"
                                "Internações: %{y:,}"
                                "<extra></extra>"
                            )
                        )
                    )

                    fig.update_layout(

                        height=350,

                        paper_bgcolor="rgba(0,0,0,0)",

                        plot_bgcolor="rgba(0,0,0,0)",

                        font=dict(
                            color="#E5E7EB",
                            size=12
                        ),

                        margin=dict(
                            l=20,
                            r=20,
                            t=15,
                            b=20
                        ),

                        xaxis=dict(
                            showgrid=False,
                            zeroline=False,
                            title=None,
                            tickfont=dict(
                                color="#94A3B8"
                            )
                        ),

                        yaxis=dict(
                            showgrid=True,
                            gridcolor="rgba(99,102,241,0.10)",
                            zeroline=False,
                            title=None,
                            tickfont=dict(
                                color="#94A3B8"
                            )
                        ),

                        hovermode="x unified",

                        showlegend=False

                    )

                    st.plotly_chart(
                        fig,
                        width="stretch",
                        config={
                            "displayModeBar": False,
                            "responsive": True
                        }
                    )

                else:

                    st.info(
                        "Os dados de internação não possuem "
                        "as colunas necessárias para o gráfico."
                    )

            else:

                st.info(
                    "Nenhum dado de internação encontrado."
                )

        # =================================================
        # HOSPITAIS / LEITOS
        # =================================================

        with col_direita:

            st.html(
                """
                <div class="chart-box">

                    <div class="chart-title">
                        🏥 Capacidade Hospitalar
                    </div>

                    <div class="chart-subtitle">
                        Hospitais com maior quantidade de leitos
                    </div>

                </div>
                """
            )

            try:

                df_hospitais = model.get_hospitais_data(
                    uf=uf,
                    municipio=municipio
                )

            except Exception as e:

                st.error(
                    "Erro ao carregar dados hospitalares."
                )

                st.exception(e)

                df_hospitais = pd.DataFrame()

            if (
                isinstance(
                    df_hospitais,
                    pd.DataFrame
                )
                and not df_hospitais.empty
            ):

                coluna_hospital = self._encontrar_coluna(
                    df_hospitais,
                    [
                        "HOSPITAL",
                        "Hospital",
                        "hospital",
                        "NOME",
                        "nome",
                        "NOME_ESTABELECIMENTO"
                    ]
                )

                coluna_leitos = self._encontrar_coluna(
                    df_hospitais,
                    [
                        "LEITOS",
                        "Leitos",
                        "leitos",
                        "QUANTIDADE_LEITOS",
                        "quantidade_leitos",
                        "LEITOS_EXISTENTES"
                    ]
                )

                if coluna_hospital and coluna_leitos:

                    df_grafico = (
                        df_hospitais.copy()
                    )

                    df_grafico[coluna_leitos] = pd.to_numeric(
                        df_grafico[coluna_leitos],
                        errors="coerce"
                    )

                    df_grafico = df_grafico.dropna(
                        subset=[
                            coluna_leitos
                        ]
                    )

                    df_grafico = (
                        df_grafico
                        .sort_values(
                            coluna_leitos,
                            ascending=False
                        )
                        .head(10)
                    )

                    fig = go.Figure()

                    fig.add_trace(
                        go.Bar(
                            x=df_grafico[
                                coluna_leitos
                            ],
                            y=df_grafico[
                                coluna_hospital
                            ],
                            orientation="h",
                            marker=dict(
                                color="#6366F1",
                                line=dict(
                                    width=0
                                )
                            ),
                            hovertemplate=(
                                "<b>%{y}</b>"
                                "<br>"
                                "Leitos: %{x:,}"
                                "<extra></extra>"
                            )
                        )
                    )

                    fig.update_layout(

                        height=350,

                        paper_bgcolor="rgba(0,0,0,0)",

                        plot_bgcolor="rgba(0,0,0,0)",

                        font=dict(
                            color="#E5E7EB",
                            size=12
                        ),

                        margin=dict(
                            l=20,
                            r=35,
                            t=15,
                            b=20
                        ),

                        xaxis=dict(
                            showgrid=True,
                            gridcolor="rgba(99,102,241,0.10)",
                            zeroline=False,
                            title=None,
                            tickfont=dict(
                                color="#94A3B8"
                            )
                        ),

                        yaxis=dict(
                            showgrid=False,
                            title=None,
                            categoryorder="total ascending",
                            tickfont=dict(
                                color="#C7D2FE",
                                size=11
                            )
                        ),

                        showlegend=False,

                        bargap=0.35

                    )

                    st.plotly_chart(
                        fig,
                        width="stretch",
                        config={
                            "displayModeBar": False,
                            "responsive": True
                        }
                    )

                else:

                    st.info(
                        "Os dados hospitalares não possuem "
                        "as colunas necessárias."
                    )

            else:

                st.info(
                    "Nenhum hospital encontrado."
                )

    # =====================================================
    # CHATBOT VITTA IA
    # =====================================================

    def _render_chatbot(
        self,
        model,
        uf,
        municipio
    ):

        # =================================================
        # TÍTULO
        # =================================================

        st.html(
            """
            <div class="section-heading chatbot-section-title">

                <div class="section-heading-icon ai-icon">
                    ✦
                </div>

                <div>

                    <div class="section-heading-title">
                        Vitta IA
                    </div>

                    <div class="section-heading-subtitle">
                        Assistente inteligente para análise dos dados hospitalares
                    </div>

                </div>

            </div>
            """
        )

        try:

            dados_ia = model.get_dados_ia(
                uf=uf,
                municipio=municipio
            )

        except Exception:

            dados_ia = None

        mensagem = ""

        if isinstance(
            dados_ia,
            dict
        ):

            mensagem = dados_ia.get(
                "mensagem",
                ""
            )

        # =================================================
        # CONTAINER PRINCIPAL
        # =================================================

        st.html(
            f"""
            <div class="chatbot-container">

                <div class="chatbot-background-glow"></div>

                <div class="chatbot-secondary-glow"></div>

                <div class="chatbot-top">

                    <div class="chatbot-brand">

                        <div class="chatbot-avatar">
                            ✦
                        </div>

                        <div>

                            <div class="chatbot-name">
                                Vitta IA
                            </div>

                            <div class="chatbot-status">
                                ● Inteligência hospitalar ativa
                            </div>

                        </div>

                    </div>

                    <div class="chatbot-badge">
                        IA
                    </div>

                </div>

                <div class="chatbot-body">

                    <div class="chatbot-message">

                        <div class="chatbot-message-avatar">
                            ✦
                        </div>

                        <div class="chatbot-message-content">

                            <div class="chatbot-message-name">
                                Vitta IA
                            </div>

                            <div class="chatbot-message-text">
                                {
                                    mensagem
                                    if mensagem
                                    else
                                    "Olá! Sou a Vitta IA. Estou pronta para analisar os indicadores hospitalares e ajudar você a interpretar os dados da rede de saúde."
                                }
                            </div>

                        </div>

                    </div>

                    <div class="chatbot-suggestions">

                        <div class="chatbot-suggestion">
                            Analisar capacidade hospitalar
                        </div>

                        <div class="chatbot-suggestion">
                            Identificar principais indicadores
                        </div>

                        <div class="chatbot-suggestion">
                            Resumir os dados hospitalares
                        </div>

                    </div>

                </div>

            </div>
            """
        )

        # =================================================
        # AÇÃO DA IA
        # =================================================

        st.html(
            """
            <div class="chatbot-action-wrapper">

                <div class="chatbot-action-content">

                    <div class="chatbot-action-text">
                        Continue sua análise diretamente com a Vitta IA.
                    </div>

                </div>

            </div>
            """
        )

        if st.button(
            "✦  Conversar com a Vitta IA",
            key="dashboard_abrir_vitta_ia",
            use_container_width=True
        ):

            st.session_state["pagina_atual"] = "Vitta IA"

            st.rerun()

    # =====================================================
    # FORMATAÇÃO DE NÚMEROS
    # =====================================================

    @staticmethod
    def _formatar_numero(valor):

        if valor is None:

            return "0"

        try:

            valor = float(valor)

            if valor.is_integer():

                return (
                    f"{int(valor):,}"
                    .replace(
                        ",",
                        "."
                    )
                )

            return (
                f"{valor:,.2f}"
                .replace(
                    ",",
                    "X"
                )
                .replace(
                    ".",
                    ","
                )
                .replace(
                    "X",
                    "."
                )
            )

        except (
            ValueError,
            TypeError
        ):

            return str(valor)

    # =====================================================
    # LOCALIZAR COLUNA
    # =====================================================

    @staticmethod
    def _encontrar_coluna(
        dataframe,
        possibilidades
    ):

        for coluna in dataframe.columns:

            if coluna in possibilidades:

                return coluna

        colunas_normalizadas = {
            str(coluna).upper(): coluna
            for coluna in dataframe.columns
        }

        for possibilidade in possibilidades:

            encontrada = (
                colunas_normalizadas.get(
                    possibilidade.upper()
                )
            )

            if encontrada:

                return encontrada

        return None

    # =====================================================
    # ESTILOS
    # =====================================================

    def _aplicar_estilos(self):

        st.html(
            """
            <style>

            /* =================================================
               CABEÇALHO
               ================================================= */

            .page-header {

                position: relative;

                display: flex;

                align-items: center;

                gap: 22px;

                padding: 28px;

                margin-bottom: 24px;

                overflow: hidden;

                border-radius: 20px;

                background:
                    linear-gradient(
                        135deg,
                        rgba(37,99,235,0.22),
                        rgba(99,102,241,0.20),
                        rgba(15,23,42,0.96)
                    );

                border:
                    1px solid
                    rgba(99,102,241,0.22);

                box-shadow:
                    0 12px 40px
                    rgba(37,99,235,0.12);

            }


            .page-header::after {

                content: "";

                position: absolute;

                width: 240px;

                height: 240px;

                right: -100px;

                top: -130px;

                border-radius: 50%;

                background:
                    rgba(124,58,237,0.18);

                filter: blur(5px);

            }


            .page-header::before {

                content: "";

                position: absolute;

                width: 160px;

                height: 160px;

                left: 25%;

                bottom: -130px;

                border-radius: 50%;

                background:
                    rgba(37,99,235,0.08);

                filter: blur(12px);

            }


            .header-icon {

                width: 68px;

                height: 68px;

                display: flex;

                align-items: center;

                justify-content: center;

                flex-shrink: 0;

                border-radius: 18px;

                font-size: 34px;

                color: #FFFFFF;

                background:
                    linear-gradient(
                        135deg,
                        #2563EB,
                        #7C3AED
                    );

                box-shadow:
                    0 10px 30px
                    rgba(79,70,229,0.35);

            }


            .header-content {

                position: relative;

                z-index: 1;

                min-width: 0;

                flex: 1;

            }


            .header-eyebrow {

                color: #818CF8;

                font-size: 11px;

                font-weight: 800;

                letter-spacing: 1.5px;

                margin-bottom: 5px;

            }


            .header-title {

                color: #FFFFFF;

                font-size: 30px;

                line-height: 1.15;

                font-weight: 800;

                letter-spacing: -0.7px;

            }


            .header-title span {

                color: #A78BFA;

                text-shadow:
                    0 0 24px
                    rgba(167,139,250,0.20);

            }


            .header-description {

                margin-top: 8px;

                color: #A5B4FC;

                font-size: 14px;

                line-height: 1.5;

                max-width: 780px;

            }


            .header-status {

                position: relative;

                z-index: 1;

                min-width: 130px;

                padding-left: 20px;

                text-align: right;

                border-left:
                    1px solid
                    rgba(255,255,255,0.08);

            }


            .header-status-dot {

                color: #6366F1;

                font-size: 13px;

                line-height: 1;

                text-shadow:
                    0 0 10px
                    rgba(99,102,241,0.65);

            }


            .header-status-text {

                color: #64748B;

                font-size: 9px;

                font-weight: 800;

                letter-spacing: 1.1px;

                margin-top: 5px;

            }


            /* =================================================
               SEÇÕES
               ================================================= */

            .section-heading {

                display: flex;

                align-items: center;

                gap: 13px;

                margin:
                    8px 0 15px 0;

            }


            .section-heading-icon {

                width: 38px;

                height: 38px;

                display: flex;

                align-items: center;

                justify-content: center;

                flex-shrink: 0;

                border-radius: 11px;

                background:
                    linear-gradient(
                        135deg,
                        rgba(37,58,235,0.15),
                        rgba(124,58,237,0.15)
                    );

                border:
                    1px solid
                    rgba(99,102,241,0.15);

                color: #A5B4FC;

                font-size: 19px;

            }


            .section-heading-title {

                color: #F8FAFC;

                font-size: 18px;

                font-weight: 750;

            }


            .section-heading-subtitle {

                color: #64748B;

                font-size: 11px;

                margin-top: 2px;

            }


            /* =================================================
               KPI
               ================================================= */

            .kpi-card {

                position: relative;

                min-height: 190px;

                padding: 20px;

                overflow: hidden;

                border-radius: 18px;

                background:
                    linear-gradient(
                        145deg,
                        rgba(30,41,59,0.98),
                        rgba(15,23,42,0.98)
                    );

                border:
                    1px solid
                    rgba(255,255,255,0.07);

                box-shadow:
                    0 10px 30px
                    rgba(0,0,0,0.22);

                transition:
                    transform 0.2s ease,
                    box-shadow 0.2s ease;

            }


            .kpi-card:hover {

                transform:
                    translateY(-3px);

                box-shadow:
                    0 16px 40px
                    rgba(99,102,241,0.15);

            }


            .kpi-glow {

                position: absolute;

                width: 120px;

                height: 120px;

                right: -55px;

                top: -55px;

                border-radius: 50%;

                opacity: 0.18;

                filter: blur(2px);

            }


            .kpi-card.blue {

                border-top:
                    3px solid #2563EB;

            }


            .kpi-card.blue .kpi-glow {

                background: #2563EB;

            }


            .kpi-card.cyan {

                border-top:
                    3px solid #06B6D4;

            }


            .kpi-card.cyan .kpi-glow {

                background: #06B6D4;

            }


            .kpi-card.purple {

                border-top:
                    3px solid #7C3AED;

            }


            .kpi-card.purple .kpi-glow {

                background: #7C3AED;

            }


            .kpi-card.indigo {

                border-top:
                    3px solid #6366F1;

            }


            .kpi-card.indigo .kpi-glow {

                background: #6366F1;

            }


            .kpi-top {

                position: relative;

                z-index: 1;

                display: flex;

                align-items: center;

                justify-content: space-between;

                margin-bottom: 15px;

            }


            .kpi-icon {

                width: 43px;

                height: 43px;

                display: flex;

                align-items: center;

                justify-content: center;

                border-radius: 12px;

                font-size: 22px;

                color: #C4B5FD;

                background:
                    rgba(99,102,241,0.10);

            }


            .kpi-tag {

                color: #64748B;

                font-size: 9px;

                font-weight: 800;

                letter-spacing: 1px;

            }


            .kpi-title {

                position: relative;

                z-index: 1;

                color: #CBD5E1;

                font-size: 13px;

                font-weight: 600;

            }


            .kpi-value {

                position: relative;

                z-index: 1;

                color: #FFFFFF;

                font-size: 32px;

                line-height: 1.1;

                font-weight: 850;

                margin-top: 4px;

                letter-spacing: -1px;

            }


            .kpi-description {

                position: relative;

                z-index: 1;

                color: #94A3B8;

                font-size: 11px;

                margin-top: 5px;

            }


            .kpi-line {

                position: absolute;

                left: 20px;

                right: 20px;

                bottom: 13px;

                height: 2px;

                border-radius: 10px;

                background:
                    linear-gradient(
                        90deg,
                        rgba(37,99,235,0.7),
                        rgba(139,92,246,0.7)
                    );

                opacity: 0.45;

            }


            /* =================================================
               GRÁFICOS
               ================================================= */

            .chart-box {

                margin-bottom: -3px;

            }


            .chart-title {

                color: #F1F5F9;

                font-size: 15px;

                font-weight: 750;

                margin-top: 5px;

            }


            .chart-subtitle {

                color: #64748B;

                font-size: 11px;

                margin-top: 2px;

            }


            [data-testid="stPlotlyChart"] {

                background:
                    linear-gradient(
                        145deg,
                        rgba(15,23,42,0.72),
                        rgba(30,41,59,0.60)
                    );

                border:
                    1px solid
                    rgba(99,102,241,0.10);

                border-radius: 16px;

                padding: 7px;

                box-shadow:
                    0 8px 30px
                    rgba(0,0,0,0.14);

            }


            /* =================================================
               CHATBOT
               ================================================= */

            .chatbot-section-title {

                margin-top: 10px;

            }


            .ai-icon {

                background:
                    linear-gradient(
                        135deg,
                        rgba(124,58,237,0.22),
                        rgba(37,99,235,0.18)
                    );

                color: #C4B5FD;

            }


            .chatbot-container {

                position: relative;

                min-height: 470px;

                overflow: hidden;

                border-radius: 22px;

                background:
                    linear-gradient(
                        145deg,
                        rgba(15,23,42,0.98),
                        rgba(30,27,75,0.97),
                        rgba(15,23,42,0.99)
                    );

                border:
                    1px solid
                    rgba(99,102,241,0.28);

                box-shadow:
                    0 18px 50px
                    rgba(0,0,0,0.28);

            }


            .chatbot-background-glow {

                position: absolute;

                width: 380px;

                height: 380px;

                right: -150px;

                top: -180px;

                border-radius: 50%;

                background:
                    rgba(124,58,237,0.13);

                filter: blur(15px);

            }


            .chatbot-secondary-glow {

                position: absolute;

                width: 240px;

                height: 240px;

                left: -120px;

                bottom: -140px;

                border-radius: 50%;

                background:
                    rgba(37,99,235,0.08);

                filter: blur(20px);

            }


            .chatbot-top {

                position: relative;

                z-index: 2;

                display: flex;

                align-items: center;

                justify-content: space-between;

                padding:
                    22px 25px;

                border-bottom:
                    1px solid
                    rgba(255,255,255,0.06);

            }


            .chatbot-brand {

                display: flex;

                align-items: center;

                gap: 13px;

            }


            .chatbot-avatar {

                width: 46px;

                height: 46px;

                display: flex;

                align-items: center;

                justify-content: center;

                border-radius: 14px;

                color: #FFFFFF;

                font-size: 22px;

                background:
                    linear-gradient(
                        135deg,
                        #6366F1,
                        #7C3AED
                    );

                box-shadow:
                    0 8px 25px
                    rgba(124,58,237,0.32);

            }


            .chatbot-name {

                color: #FFFFFF;

                font-size: 16px;

                font-weight: 800;

            }


            .chatbot-status {

                color: #64748B;

                font-size: 10px;

                margin-top: 3px;

            }


            .chatbot-status::first-letter {

                color: #8B5CF6;

            }


            .chatbot-badge {

                padding:
                    6px 11px;

                border-radius: 8px;

                color: #C4B5FD;

                background:
                    rgba(124,58,237,0.14);

                border:
                    1px solid
                    rgba(124,58,237,0.25);

                font-size: 9px;

                font-weight: 800;

                letter-spacing: 1px;

            }


            .chatbot-body {

                position: relative;

                z-index: 2;

                padding:
                    28px 25px;

                min-height: 290px;

            }


            .chatbot-message {

                display: flex;

                gap: 13px;

                max-width: 850px;

            }


            .chatbot-message-avatar {

                width: 36px;

                height: 36px;

                flex-shrink: 0;

                display: flex;

                align-items: center;

                justify-content: center;

                border-radius: 11px;

                color: #C4B5FD;

                background:
                    rgba(124,58,237,0.16);

                border:
                    1px solid
                    rgba(124,58,237,0.20);

            }


            .chatbot-message-content {

                padding:
                    14px 17px;

                border-radius:
                    5px 15px 15px 15px;

                background:
                    rgba(255,255,255,0.045);

                border:
                    1px solid
                    rgba(255,255,255,0.06);

            }


            .chatbot-message-name {

                color: #A78BFA;

                font-size: 10px;

                font-weight: 800;

                margin-bottom: 6px;

            }


            .chatbot-message-text {

                color: #CBD5E1;

                font-size: 13px;

                line-height: 1.6;

            }


            .chatbot-suggestions {

                display: flex;

                flex-wrap: wrap;

                gap: 9px;

                margin:
                    22px 0 0 49px;

            }


            .chatbot-suggestion {

                padding:
                    9px 13px;

                border-radius: 10px;

                color: #A5B4FC;

                background:
                    rgba(99,102,241,0.08);

                border:
                    1px solid
                    rgba(99,102,241,0.15);

                font-size: 10px;

                transition:
                    all 0.2s ease;

            }


            .chatbot-suggestion:hover {

                color: #FFFFFF;

                background:
                    rgba(99,102,241,0.16);

                border-color:
                    rgba(139,92,246,0.35);

            }


            /* =================================================
               AÇÃO DA IA
               ================================================= */

            .chatbot-action-wrapper {

                position: relative;

                z-index: 5;

                margin-top: -88px;

                padding:
                    0 25px 22px 25px;

                pointer-events: none;

            }


            .chatbot-action-content {

                display: flex;

                align-items: center;

                justify-content: center;

                min-height: 47px;

                text-align: center;

            }


            .chatbot-action-text {

                color: #64748B;

                font-size: 10px;

            }


            /* =================================================
               BOTÃO VITTA IA
               ================================================= */

            div[data-testid="stButton"] button {

                position: relative;

                z-index: 10;

                min-height: 42px !important;

                border-radius: 11px !important;

                border:
                    1px solid
                    rgba(124,58,237,0.42) !important;

                background:
                    linear-gradient(
                        135deg,
                        rgba(124,58,237,0.20),
                        rgba(79,70,229,0.16)
                    ) !important;

                color: #C4B5FD !important;

                font-size: 13px !important;

                font-weight: 800 !important;

                transition:
                    all 0.2s ease !important;

            }


            div[data-testid="stButton"] button:hover {

                border-color:
                    rgba(167,139,250,0.85) !important;

                background:
                    linear-gradient(
                        135deg,
                        rgba(124,58,237,0.34),
                        rgba(79,70,229,0.26)
                    ) !important;

                color: #FFFFFF !important;

                transform:
                    translateY(-1px);

                box-shadow:
                    0 8px 22px
                    rgba(124,58,237,0.18);

            }


            /* =================================================
               RESPONSIVIDADE
               ================================================= */

            @media (max-width: 900px) {

                .header-title {

                    font-size: 24px;

                }


                .page-header {

                    padding: 20px;

                }


                .header-status {

                    display: none;

                }


                .chatbot-container {

                    min-height: 500px;

                }

            }

            </style>
            """
        )