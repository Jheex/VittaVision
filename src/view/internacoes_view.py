import pandas as pd
import plotly.express as px
import streamlit as st


# ==========================================================
# PREPARAÇÃO DOS DADOS
# ==========================================================

@st.cache_data(show_spinner="Processando dados de internações...")
def preparar_dados(df_int):

    if df_int is None or df_int.empty:
        return pd.DataFrame(), []

    df_int = df_int.copy()

    # ======================================================
    # NORMALIZAÇÃO DAS COLUNAS
    # ======================================================

    df_int.columns = (
        df_int.columns.astype(str)
        .str.replace("ï»¿", "", regex=False)
        .str.replace('"', "", regex=False)
        .str.strip()
    )

    # ======================================================
    # MAPA UF
    # ======================================================

    MAPA_CODIGO_UF = {
        11: "RO",
        12: "AC",
        13: "AM",
        14: "RR",
        15: "PA",
        16: "AP",
        17: "TO",
        21: "MA",
        22: "PI",
        23: "CE",
        24: "RN",
        25: "PB",
        26: "PE",
        27: "AL",
        28: "SE",
        29: "BA",
        31: "MG",
        32: "ES",
        33: "RJ",
        35: "SP",
        41: "PR",
        42: "SC",
        43: "RS",
        50: "MS",
        51: "MT",
        52: "GO",
        53: "DF",
    }

    if "CODIGO_UF" in df_int.columns:

        df_int["CODIGO_UF_NUM"] = (
            pd.to_numeric(
                df_int["CODIGO_UF"],
                errors="coerce"
            )
            .fillna(0)
            .astype(int)
        )

        df_int["UF"] = (
            df_int["CODIGO_UF_NUM"]
            .map(MAPA_CODIGO_UF)
            .fillna("Outros")
        )

    else:

        df_int["UF"] = "Outros"

    # ======================================================
    # MESES
    # ======================================================

    meses_cols = [
        "2025/Jan",
        "2025/Fev",
        "2025/Mar",
        "2025/Abr",
        "2025/Mai",
        "2025/Jun",
        "2025/Jul",
        "2025/Ago",
        "2025/Set",
        "2025/Out",
        "2025/Nov",
        "2025/Dez",
    ]

    cols_meses_presentes = [
        coluna
        for coluna in meses_cols
        if coluna in df_int.columns
    ]

    # ======================================================
    # TRATAMENTO DOS MESES
    # ======================================================

    for coluna in cols_meses_presentes:

        df_int[coluna] = (
            df_int[coluna]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
            .replace("-", "0")
        )

        df_int[coluna] = pd.to_numeric(
            df_int[coluna],
            errors="coerce"
        ).fillna(0)

    # ======================================================
    # TOTAL
    # ======================================================

    if "Total" in df_int.columns:

        df_int["Total"] = (
            df_int["Total"]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
            .replace("-", "0")
        )

        df_int["Total"] = pd.to_numeric(
            df_int["Total"],
            errors="coerce"
        ).fillna(0)

    elif cols_meses_presentes:

        df_int["Total"] = (
            df_int[cols_meses_presentes]
            .sum(axis=1)
        )

    return df_int, cols_meses_presentes


# ==========================================================
# VIEW
# ==========================================================

class InternacoesView:

    # ======================================================
    # RENDER
    # ======================================================

    def render(self, model=None):

        # ==================================================
        # CSS
        # ==================================================

        self._aplicar_estilos()

        # ==================================================
        # VALIDAÇÃO DO MODEL
        # ==================================================

        if model is None:

            st.error(
                "Modelo de Internações não foi inicializado."
            )

            return

        # ==================================================
        # CARREGAMENTO
        # ==================================================

        try:

            df_raw = model.dados_para_view()

        except Exception as e:

            st.error(
                "Erro ao carregar os dados de internações."
            )

            st.exception(e)

            return

        if df_raw is None or df_raw.empty:

            st.warning(
                "Não foram encontrados dados de internações no banco de dados."
            )

            return

        # ==================================================
        # PREPARAÇÃO
        # ==================================================

        try:

            df_int, cols_meses_presentes = preparar_dados(
                df_raw
            )

        except Exception as e:

            st.error(
                "Erro ao processar os dados de internações."
            )

            st.exception(e)

            return

        if df_int.empty:

            st.warning(
                "Nenhum dado válido de internação foi encontrado."
            )

            return

        # ==================================================
        # COLUNA MUNICÍPIO
        # ==================================================

        col_mun = (
            "MUNICIPIO"
            if "MUNICIPIO" in df_int.columns
            else None
        )

        # ==================================================
        # NOMES DOS MESES
        # ==================================================

        meses_nomes = {

            "2025/Jan": "Jan",
            "2025/Fev": "Fev",
            "2025/Mar": "Mar",
            "2025/Abr": "Abr",
            "2025/Mai": "Mai",
            "2025/Jun": "Jun",
            "2025/Jul": "Jul",
            "2025/Ago": "Ago",
            "2025/Set": "Set",
            "2025/Out": "Out",
            "2025/Nov": "Nov",
            "2025/Dez": "Dez",

        }

        # ==================================================
        # CABEÇALHO
        # ==================================================

        self._render_cabecalho(
            df_int
        )

        st.write("")

        # ==================================================
        # DADOS PARA ANÁLISE
        # ==================================================

        df_filtrado = df_int.copy()

        # ==================================================
        # KPIS
        # ==================================================

        self._render_kpis(
            df_filtrado
        )

        st.write("")

        # ==================================================
        # GRÁFICOS
        # ==================================================

        self._render_graficos(
            df_filtrado,
            cols_meses_presentes,
            meses_nomes,
            col_mun
        )

        st.write("")

        # ==================================================
        # TABELA
        # ==================================================

        self._render_tabela(
            df_filtrado,
            cols_meses_presentes,
            meses_nomes,
            col_mun
        )

        # ==================================================
        # RODAPÉ
        # ==================================================

        st.html(
            """
            <div class="data-source">

                <span class="data-source-icon">
                    ℹ️
                </span>

                <span>
                    Fonte: Ministério da Saúde — DATASUS/SIH-SUS.
                    Dados referentes ao ano de 2025.
                </span>

            </div>
            """
        )

    # ======================================================
    # CABEÇALHO
    # ======================================================

    def _render_cabecalho(
        self,
        df
    ):

        total = (
            df["Total"].sum()
            if "Total" in df.columns
            else 0
        )

        st.html(
            f"""
            <div class="page-header">

                <div class="header-icon">
                    🏥
                </div>

                <div class="header-content">

                    <div class="header-eyebrow">
                        VITTA VISION • INTERNAÇÕES HOSPITALARES
                    </div>

                    <div class="header-title">
                        Gestão de <span>Internações Hospitalares</span>
                    </div>

                    <div class="header-description">
                        Acompanhamento da distribuição e evolução
                        das internações hospitalares do SUS em 2025.
                    </div>

                </div>

                <div class="header-counter">

                    <div class="header-counter-value">
                        {total:,.0f}
                    </div>

                    <div class="header-counter-label">
                        INTERNAÇÕES
                    </div>

                </div>

            </div>
            """.replace(
                ",",
                "."
            )
        )

    # ======================================================
    # KPIS
    # ======================================================

    def _render_kpis(
        self,
        df
    ):

        total_internacoes = (
            df["Total"].sum()
            if "Total" in df.columns
            else 0
        )

        total_municipios = (
            df["MUNICIPIO"]
            .dropna()
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .nunique()
            if "MUNICIPIO" in df.columns
            else 0
        )

        media_municipio = (
            total_internacoes / total_municipios
            if total_municipios > 0
            else 0
        )

        total_registros = len(df)

        # ==================================================
        # 4 CARDS
        # ==================================================

        col1, col2, col3, col4 = st.columns(
            4,
            gap="medium"
        )

        # ==================================================
        # INTERNAÇÕES
        # ==================================================

        with col1:

            self._render_kpi_card(
                icone="🏥",
                titulo="Internações",
                valor=f"{total_internacoes:,.0f}".replace(
                    ",",
                    "."
                ),
                descricao="Total de internações registradas",
                detalhe="2025",
                classe="purple"
            )

        # ==================================================
        # MUNICÍPIOS
        # ==================================================

        with col2:

            self._render_kpi_card(
                icone="📍",
                titulo="Municípios",
                valor=f"{total_municipios:,}".replace(
                    ",",
                    "."
                ),
                descricao="Municípios presentes nos registros",
                detalhe="ABRANGÊNCIA",
                classe="blue"
            )

        # ==================================================
        # MÉDIA
        # ==================================================

        with col3:

            self._render_kpi_card(
                icone="📊",
                titulo="Média por Município",
                valor=f"{media_municipio:,.0f}".replace(
                    ",",
                    "."
                ),
                descricao="Média de internações por município",
                detalhe="INDICADOR",
                classe="cyan"
            )

        # ==================================================
        # REGISTROS
        # ==================================================

        with col4:

            self._render_kpi_card(
                icone="📋",
                titulo="Registros",
                valor=f"{total_registros:,}".replace(
                    ",",
                    "."
                ),
                descricao="Registros municipais disponíveis",
                detalhe="BASE DE DADOS",
                classe="violet"
            )

    # ======================================================
    # CARD KPI
    # ======================================================

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

    # ======================================================
    # GRÁFICOS
    # ======================================================

    def _render_graficos(
        self,
        df,
        cols_meses,
        meses_nomes,
        col_mun
    ):

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
                        Evolução e distribuição das internações hospitalares
                    </div>

                </div>

            </div>
            """
        )

        if df.empty:

            st.warning(
                "Não existem dados para a seleção atual."
            )

            return

        col_esquerda, col_direita = st.columns(
            [1.6, 1],
            gap="medium"
        )

        # ==================================================
        # EVOLUÇÃO
        # ==================================================

        with col_esquerda:

            st.html(
                """
                <div class="chart-box">

                    <div class="chart-title">
                        📈 Evolução Mensal
                    </div>

                    <div class="chart-subtitle">
                        Quantidade de internações ao longo de 2025
                    </div>

                </div>
                """
            )

            if cols_meses:

                soma_meses = (
                    df[cols_meses]
                    .sum()
                    .reset_index()
                )

                soma_meses.columns = [
                    "Mês",
                    "Internações"
                ]

                soma_meses["Mês"] = (
                    soma_meses["Mês"]
                    .map(meses_nomes)
                )

                fig = px.line(
                    soma_meses,
                    x="Mês",
                    y="Internações",
                    markers=True
                )

                fig.update_traces(
                    line=dict(
                        color="#A855F7",
                        width=3
                    ),
                    marker=dict(
                        size=8,
                        color="#A855F7"
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

                    hovermode="x unified"

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
                    "Não há dados mensais disponíveis."
                )

        # ==================================================
        # TOP MUNICÍPIOS
        # ==================================================

        with col_direita:

            st.html(
                """
                <div class="chart-box">

                    <div class="chart-title">
                        🏆 Top 5 Municípios
                    </div>

                    <div class="chart-subtitle">
                        Municípios com maior número de internações
                    </div>

                </div>
                """
            )

            if (
                col_mun
                and "Total" in df.columns
            ):

                df_top = (
                    df.nlargest(
                        5,
                        "Total"
                    )
                    .sort_values(
                        "Total"
                    )
                )

                if not df_top.empty:

                    fig = px.bar(
                        df_top,
                        x="Total",
                        y=col_mun,
                        orientation="h",
                        text="Total"
                    )

                    fig.update_traces(

                        marker_color="#A855F7",

                        texttemplate="%{text:,.0f}",

                        textposition="outside",

                        textfont=dict(
                            color="#E5E7EB",
                            size=12
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
                            r=55,
                            t=15,
                            b=20
                        ),

                        xaxis=dict(
                            showgrid=True,
                            gridcolor="rgba(99,102,241,0.10)",
                            zeroline=False,
                            showticklabels=False,
                            title=None
                        ),

                        yaxis=dict(
                            showgrid=False,
                            title=None,
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
                    "Não existem dados suficientes para gerar o ranking."
                )

    # ======================================================
    # TABELA
    # ======================================================

    def _render_tabela(
        self,
        df,
        cols_meses,
        meses_nomes,
        col_mun
    ):

        st.html(
            """
            <div class="section-heading">

                <div class="section-heading-icon">
                    📋
                </div>

                <div>

                    <div class="section-heading-title">
                        Tabela de Internações Hospitalares
                    </div>

                    <div class="section-heading-subtitle">
                        Detalhamento dos registros de internações por município
                    </div>

                </div>

            </div>
            """
        )

        if df.empty:

            st.warning(
                "Nenhum registro encontrado."
            )

            return

        # ==================================================
        # ORDENAÇÃO
        # ==================================================

        df_tabela = df.copy()

        if "Total" in df_tabela.columns:

            df_tabela = df_tabela.sort_values(
                by="Total",
                ascending=False
            )

        # ==================================================
        # COLUNAS
        # ==================================================

        colunas_ordem = []

        if col_mun:

            colunas_ordem.append(
                col_mun
            )

        if "UF" in df_tabela.columns:

            colunas_ordem.append(
                "UF"
            )

        if "Total" in df_tabela.columns:

            colunas_ordem.append(
                "Total"
            )

        colunas_ordem.extend(
            cols_meses
        )

        colunas_ordem = [
            coluna
            for coluna in colunas_ordem
            if coluna in df_tabela.columns
        ]

        tabela = df_tabela[
            colunas_ordem
        ].copy()

        # ==================================================
        # CONFIGURAÇÃO
        # ==================================================

        column_config_dict = {}

        if col_mun:

            column_config_dict[
                col_mun
            ] = st.column_config.TextColumn(
                "Município",
                width="medium"
            )

        if "UF" in tabela.columns:

            column_config_dict[
                "UF"
            ] = st.column_config.TextColumn(
                "UF",
                width="small"
            )

        # ==================================================
        # TOTAL
        # ==================================================

        if "Total" in tabela.columns:

            max_total = int(
                tabela["Total"].max()
            )

            if max_total <= 0:
                max_total = 100

            column_config_dict[
                "Total"
            ] = st.column_config.ProgressColumn(
                "Total de Internações",
                format="%d",
                min_value=0,
                max_value=max_total,
                width="medium"
            )

        # ==================================================
        # MESES
        # ==================================================

        for coluna in cols_meses:

            nome_amigavel = meses_nomes.get(
                coluna,
                coluna
            )

            column_config_dict[
                coluna
            ] = st.column_config.NumberColumn(
                nome_amigavel,
                format="%d",
                width="small"
            )

        # ==================================================
        # DATAFRAME
        # ==================================================

        st.dataframe(
            tabela,
            column_config=column_config_dict,
            width="stretch",
            hide_index=True,
            height=520
        )

        # ==================================================
        # RODAPÉ
        # ==================================================

        st.html(
            f"""
            <div class="table-footer">

                <span>
                    Exibindo os registros disponíveis.
                </span>

                <span class="table-total">
                    {len(tabela):,} registro(s)
                </span>

            </div>
            """.replace(
                ",",
                "."
            )
        )

    # ======================================================
    # CSS
    # ======================================================

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
                        rgba(126, 34, 206, 0.24),
                        rgba(168, 85, 247, 0.18),
                        rgba(15, 23, 42, 0.96)
                    );

                border:
                    1px solid
                    rgba(168, 85, 247, 0.22);

                box-shadow:
                    0 12px 40px
                    rgba(126, 34, 206, 0.12);

            }


            .page-header::after {

                content: "";

                position: absolute;

                width: 220px;

                height: 220px;

                right: -100px;

                top: -120px;

                border-radius: 50%;

                background:
                    rgba(168, 85, 247, 0.18);

                filter: blur(5px);

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

                background:
                    linear-gradient(
                        135deg,
                        #7C3AED,
                        #A855F7
                    );

                box-shadow:
                    0 10px 30px
                    rgba(168, 85, 247, 0.35);

            }


            .header-content {

                position: relative;

                z-index: 1;

                min-width: 0;

                flex: 1;

            }


            .header-eyebrow {

                color: #C084FC;

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

                color: #A855F7;

            }


            .header-description {

                margin-top: 8px;

                color: #C4B5FD;

                font-size: 14px;

                line-height: 1.5;

                max-width: 780px;

            }


            .header-counter {

                position: relative;

                z-index: 1;

                min-width: 120px;

                padding-left: 20px;

                text-align: right;

                border-left:
                    1px solid
                    rgba(255,255,255,0.08);

            }


            .header-counter-value {

                color: #FFFFFF;

                font-size: 26px;

                font-weight: 850;

                line-height: 1.1;

            }


            .header-counter-label {

                color: #64748B;

                font-size: 9px;

                font-weight: 800;

                letter-spacing: 1.2px;

                margin-top: 4px;

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

                border-radius: 11px;

                background:
                    linear-gradient(
                        135deg,
                        rgba(124,58,237,0.15),
                        rgba(168,85,247,0.15)
                    );

                border:
                    1px solid
                    rgba(168,85,247,0.15);

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
               SELEÇÃO
               ================================================= */

            .selection-info {

                display: inline-flex;

                align-items: center;

                gap: 8px;

                padding: 8px 13px;

                border-radius: 10px;

                background:
                    rgba(168,85,247,0.08);

                border:
                    1px solid
                    rgba(168,85,247,0.13);

                color: #94A3B8;

                font-size: 11px;

            }


            .selection-info strong {

                color: #C084FC;

            }


            .selection-icon {

                font-size: 14px;

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
                        rgba(30, 41, 59, 0.98),
                        rgba(15, 23, 42, 0.98)
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
                    rgba(168,85,247,0.15);

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


            .kpi-card.purple {

                border-top:
                    3px solid #A855F7;

            }


            .kpi-card.purple .kpi-glow {

                background: #A855F7;

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


            .kpi-card.violet {

                border-top:
                    3px solid #7C3AED;

            }


            .kpi-card.violet .kpi-glow {

                background: #7C3AED;

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

                background:
                    rgba(168,85,247,0.10);

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
                        rgba(168,85,247,0.7),
                        rgba(124,58,237,0.7)
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
                    rgba(168,85,247,0.10);

                border-radius: 16px;

                padding: 7px;

                box-shadow:
                    0 8px 30px
                    rgba(0,0,0,0.14);

            }


            /* =================================================
               TABELA
               ================================================= */

            [data-testid="stDataFrame"] {

                border-radius: 16px;

                overflow: hidden;

                border:
                    1px solid
                    rgba(168,85,247,0.13);

                box-shadow:
                    0 8px 30px
                    rgba(0,0,0,0.18);

            }


            [data-testid="stProgress"] > div > div {

                background-color:
                    #A855F7 !important;

            }


            .table-footer {

                display: flex;

                justify-content: space-between;

                align-items: center;

                gap: 10px;

                padding: 10px 3px;

                color: #64748B;

                font-size: 11px;

            }


            .table-total {

                color: #C084FC;

                font-weight: 700;

            }


            /* =================================================
               FONTE
               ================================================= */

            .data-source {

                display: flex;

                align-items: center;

                gap: 8px;

                margin-top: 15px;

                padding: 12px 4px;

                color: #64748B;

                font-size: 10px;

            }


            .data-source-icon {

                font-size: 13px;

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


                .header-counter {

                    display: none;

                }

            }

            </style>
            """
        )