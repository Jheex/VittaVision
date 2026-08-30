import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# CONSOLIDAÇÃO DOS DADOS
# =========================================================

@st.cache_data(
    show_spinner="Processando dados hospitalares..."
)
def consolidar_dados_hospitais(df):

    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    # =====================================================
    # NORMALIZAÇÃO DAS COLUNAS
    # =====================================================

    df.columns = [
        str(col).strip().upper()
        for col in df.columns
    ]

    # =====================================================
    # CNES
    # =====================================================

    if "CNES" not in df.columns:
        return df

    df["CNES"] = pd.to_numeric(
        df["CNES"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["CNES"]
    )

    if df.empty:
        return pd.DataFrame()

    # =====================================================
    # COLUNAS IMPORTANTES PARA HOSPITAIS
    # =====================================================

    colunas_importantes = [

        "CNES",

        "UF",
        "MUNICIPIO",

        "NOME_ESTABELECIMENTO",
        "RAZAO_SOCIAL",

        "DS_TIPO_UNIDADE",

        "MOTIVO_DESABILITACAO",

        "NO_LOGRADOURO",
        "NU_ENDERECO",
        "NO_COMPLEMENTO",
        "NO_BAIRRO",
        "CO_CEP",
    ]

    colunas_existentes = [
        coluna
        for coluna in colunas_importantes
        if coluna in df.columns
    ]

    df = df[
        colunas_existentes
    ]

    # =====================================================
    # AGREGAÇÃO
    # =====================================================

    agregacoes = {}

    for coluna in df.columns:

        if coluna == "CNES":
            continue

        agregacoes[coluna] = "first"

    # =====================================================
    # CONSOLIDAÇÃO POR CNES
    # =====================================================

    df = (
        df
        .groupby(
            "CNES",
            as_index=False,
            sort=False
        )
        .agg(agregacoes)
    )

    # =====================================================
    # ORDENAÇÃO
    # =====================================================

    if "NOME_ESTABELECIMENTO" in df.columns:

        df = df.sort_values(
            by="NOME_ESTABELECIMENTO",
            na_position="last"
        )

    return df.reset_index(
        drop=True
    )


# =========================================================
# VIEW
# =========================================================

class HospitaisView:

    # =====================================================
    # RENDER PRINCIPAL
    # =====================================================

    def render(self, model):

        # =================================================
        # CSS
        # =================================================

        self._aplicar_estilos()

        # =================================================
        # ORACLE
        # =================================================

        try:

            df_bruto = model.listar_dados()

        except Exception as e:

            st.error(
                "Erro ao carregar os dados hospitalares no Oracle."
            )

            st.exception(e)

            return

        if df_bruto is None or df_bruto.empty:

            st.warning(
                "Nenhum dado hospitalar foi encontrado no Oracle."
            )

            return

        # =================================================
        # CONSOLIDAÇÃO
        # =================================================

        try:

            df = consolidar_dados_hospitais(
                df_bruto
            )

        except Exception as e:

            st.error(
                "Erro ao processar os dados hospitalares."
            )

            st.exception(e)

            return

        if df.empty:

            st.warning(
                "Nenhum hospital válido foi encontrado."
            )

            return

        # =================================================
        # CABEÇALHO
        # =================================================

        self._render_cabecalho(
            df
        )

        st.write("")

        # =================================================
        # INDICADORES
        # =================================================

        metricas = self._calcular_metricas(
            df
        )

        self._render_kpis(
            metricas
        )

        st.write("")

        # =================================================
        # GRÁFICOS
        # =================================================

        self._render_graficos(
            df
        )

        st.write("")

        # =================================================
        # TABELA
        # =================================================

        self._render_tabela(
            df
        )

    # =====================================================
    # CABEÇALHO
    # =====================================================

    def _render_cabecalho(self, df):

        quantidade = len(df)

        st.html(
            f"""
            <div class="page-header">

                <div class="header-icon">
                    🏥
                </div>

                <div class="header-content">

                    <div class="header-eyebrow">
                        VITTA VISION • REDE HOSPITALAR
                    </div>

                    <div class="header-title">
                        Painel de Hospitais
                    </div>

                    <div class="header-description">
                        Monitoramento dos estabelecimentos hospitalares
                        e distribuição da rede de atendimento.
                    </div>

                </div>

                <div class="header-counter">

                    <div class="header-counter-value">
                        {quantidade:,}
                    </div>

                    <div class="header-counter-label">
                        HOSPITAIS
                    </div>

                </div>

            </div>
            """.replace(",", ".")
        )

    # =====================================================
    # MÉTRICAS
    # =====================================================

    def _calcular_metricas(self, df):

        total_hospitais = len(df)

        # =================================================
        # HOSPITAIS ATIVOS
        # =================================================

        if "MOTIVO_DESABILITACAO" in df.columns:

            motivo = (
                df["MOTIVO_DESABILITACAO"]
                .fillna("")
                .astype(str)
                .str.strip()
            )

            hospitais_ativos = int(
                motivo.eq("").sum()
            )

        else:

            hospitais_ativos = total_hospitais

        # =================================================
        # MUNICÍPIOS
        # =================================================

        if "MUNICIPIO" in df.columns:

            municipios = (
                df["MUNICIPIO"]
                .dropna()
                .astype(str)
                .str.strip()
                .replace("", pd.NA)
                .nunique()
            )

        else:

            municipios = 0

        # =================================================
        # TIPOS DE UNIDADE
        # =================================================

        if "DS_TIPO_UNIDADE" in df.columns:

            tipos_unidade = (
                df["DS_TIPO_UNIDADE"]
                .dropna()
                .astype(str)
                .str.strip()
                .replace("", pd.NA)
                .nunique()
            )

        else:

            tipos_unidade = 0

        return {

            "total_hospitais":
                total_hospitais,

            "hospitais_ativos":
                hospitais_ativos,

            "municipios":
                municipios,

            "tipos_unidade":
                tipos_unidade,
        }

    # =====================================================
    # KPIs
    # =====================================================

    def _render_kpis(self, metricas):

        total_hospitais = (
            metricas["total_hospitais"]
        )

        hospitais_ativos = (
            metricas["hospitais_ativos"]
        )

        municipios = (
            metricas["municipios"]
        )

        tipos_unidade = (
            metricas["tipos_unidade"]
        )

        # =================================================
        # 4 CARDS
        # =================================================

        col1, col2, col3, col4 = st.columns(
            4,
            gap="medium"
        )

        # =================================================
        # HOSPITAIS
        # =================================================

        with col1:

            self._render_kpi_card(
                icone="🏥",
                titulo="Hospitais",
                valor=(
                    f"{total_hospitais:,}"
                    .replace(",", ".")
                ),
                descricao="Estabelecimentos cadastrados",
                detalhe="REDE HOSPITALAR",
                classe="blue"
            )

        # =================================================
        # HOSPITAIS ATIVOS
        # =================================================

        with col2:

            self._render_kpi_card(
                icone="🛡️",
                titulo="Hospitais Ativos",
                valor=(
                    f"{hospitais_ativos:,}"
                    .replace(",", ".")
                ),
                descricao="Estabelecimentos habilitados",
                detalhe="STATUS ATIVO",
                classe="cyan"
            )

        # =================================================
        # MUNICÍPIOS
        # =================================================

        with col3:

            self._render_kpi_card(
                icone="📍",
                titulo="Municípios",
                valor=(
                    f"{municipios:,}"
                    .replace(",", ".")
                ),
                descricao="Municípios com hospitais cadastrados",
                detalhe="ABRANGÊNCIA",
                classe="purple"
            )

        # =================================================
        # TIPOS DE UNIDADE
        # =================================================

        with col4:

            self._render_kpi_card(
                icone="🏨",
                titulo="Tipos de Unidade",
                valor=(
                    f"{tipos_unidade:,}"
                    .replace(",", ".")
                ),
                descricao="Categorias de estabelecimentos",
                detalhe="CLASSIFICAÇÃO",
                classe="violet"
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
        df
    ):

        if df.empty:

            st.info(
                "Não há dados suficientes para gerar os gráficos."
            )

            return

        # =================================================
        # TÍTULO
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
                        Distribuição e classificação dos hospitais
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
        # HOSPITAIS POR MUNICÍPIO
        # =================================================

        with col_esquerda:

            st.html(
                """
                <div class="chart-box">

                    <div class="chart-title">
                        Hospitais por Município
                    </div>

                    <div class="chart-subtitle">
                        Municípios com maior quantidade de hospitais
                    </div>

                </div>
                """
            )

            if "MUNICIPIO" in df.columns:

                dados_municipio = (
                    df["MUNICIPIO"]
                    .fillna("Não informado")
                    .astype(str)
                    .str.strip()
                    .replace("", "Não informado")
                    .value_counts()
                    .sort_values()
                    .tail(10)
                )

                fig_municipio = go.Figure(
                    go.Bar(
                        x=dados_municipio.values,
                        y=dados_municipio.index,
                        orientation="h",

                        text=[
                            f"{valor:,}".replace(
                                ",",
                                "."
                            )
                            for valor in dados_municipio.values
                        ],

                        textposition="outside",

                        marker=dict(
                            color="#8B5CF6",
                            line=dict(
                                width=0
                            )
                        ),

                        hovertemplate=(
                            "<b>%{y}</b>"
                            "<br>"
                            "Hospitais: %{x:,}"
                            "<extra></extra>"
                        )
                    )
                )

                fig_municipio.update_layout(

                    paper_bgcolor="rgba(0,0,0,0)",

                    plot_bgcolor="rgba(0,0,0,0)",

                    font=dict(
                        color="#E5E7EB",
                        size=12
                    ),

                    margin=dict(
                        l=20,
                        r=60,
                        t=15,
                        b=20
                    ),

                    height=330,

                    xaxis=dict(
                        showgrid=True,
                        gridcolor="rgba(99,102,241,0.10)",
                        zeroline=False,
                        showticklabels=False
                    ),

                    yaxis=dict(
                        showgrid=False,
                        autorange="reversed",

                        tickfont=dict(
                            color="#C7D2FE",
                            size=11
                        )
                    ),

                    showlegend=False,

                    bargap=0.35
                )

                st.plotly_chart(
                    fig_municipio,
                    width="stretch",
                    config={
                        "displayModeBar": False,
                        "responsive": True
                    }
                )

            else:

                st.info(
                    "Não há dados de município disponíveis."
                )

        # =================================================
        # HOSPITAIS POR TIPO
        # =================================================

        with col_direita:

            st.html(
                """
                <div class="chart-box">

                    <div class="chart-title">
                        Hospitais por Tipo de Unidade
                    </div>

                    <div class="chart-subtitle">
                        Principais categorias de estabelecimentos
                    </div>

                </div>
                """
            )

            if "DS_TIPO_UNIDADE" in df.columns:

                dados_tipo = (
                    df["DS_TIPO_UNIDADE"]
                    .fillna("Não informado")
                    .astype(str)
                    .str.strip()
                    .replace("", "Não informado")
                    .value_counts()
                    .sort_values()
                    .tail(10)
                )

                fig_tipo = go.Figure(
                    go.Bar(
                        x=dados_tipo.values,
                        y=dados_tipo.index,
                        orientation="h",

                        text=[
                            f"{valor:,}".replace(
                                ",",
                                "."
                            )
                            for valor in dados_tipo.values
                        ],

                        textposition="outside",

                        marker=dict(
                            color="#3B82F6",
                            line=dict(
                                width=0
                            )
                        ),

                        hovertemplate=(
                            "<b>%{y}</b>"
                            "<br>"
                            "Hospitais: %{x:,}"
                            "<extra></extra>"
                        )
                    )
                )

                fig_tipo.update_layout(

                    paper_bgcolor="rgba(0,0,0,0)",

                    plot_bgcolor="rgba(0,0,0,0)",

                    font=dict(
                        color="#E5E7EB",
                        size=12
                    ),

                    margin=dict(
                        l=20,
                        r=65,
                        t=15,
                        b=20
                    ),

                    height=330,

                    xaxis=dict(
                        showgrid=True,
                        gridcolor="rgba(99,102,241,0.10)",
                        zeroline=False,
                        showticklabels=False
                    ),

                    yaxis=dict(
                        showgrid=False,
                        autorange="reversed",

                        tickfont=dict(
                            color="#C7D2FE",
                            size=11
                        )
                    ),

                    showlegend=False,

                    bargap=0.35
                )

                st.plotly_chart(
                    fig_tipo,
                    width="stretch",
                    config={
                        "displayModeBar": False,
                        "responsive": True
                    }
                )

            else:

                st.info(
                    "Não há dados de tipo de unidade disponíveis."
                )

    # =====================================================
    # TABELA
    # =====================================================

    def _render_tabela(self, df):

        st.html(
            """
            <div class="section-heading">

                <div class="section-heading-icon">
                    📋
                </div>

                <div>

                    <div class="section-heading-title">
                        Unidades Hospitalares
                    </div>

                    <div class="section-heading-subtitle">
                        Detalhamento dos estabelecimentos hospitalares
                    </div>

                </div>

            </div>
            """
        )

        if df.empty:

            st.warning(
                "Nenhum hospital encontrado."
            )

            return

        # =================================================
        # LIMITE
        # =================================================

        limite = 500

        # =================================================
        # COLUNAS
        # =================================================

        colunas_exibir = [

            "NOME_ESTABELECIMENTO",

            "CNES",

            "MUNICIPIO",

            "UF",

            "DS_TIPO_UNIDADE",

            "NO_LOGRADOURO",

            "NU_ENDERECO",

            "NO_COMPLEMENTO",

            "NO_BAIRRO",

            "CO_CEP",
        ]

        colunas_exibir = [
            coluna
            for coluna in colunas_exibir
            if coluna in df.columns
        ]

        df_tabela = df[
            colunas_exibir
        ].copy()

        # =================================================
        # CONVERSÃO CNES
        # =================================================

        if "CNES" in df_tabela.columns:

            df_tabela["CNES"] = (
                pd.to_numeric(
                    df_tabela["CNES"],
                    errors="coerce"
                )
                .fillna(0)
                .astype(int)
            )

        # =================================================
        # ORDENAÇÃO
        # =================================================

        if "NOME_ESTABELECIMENTO" in df_tabela.columns:

            df_tabela = df_tabela.sort_values(
                by="NOME_ESTABELECIMENTO",
                na_position="last"
            )

        # =================================================
        # TOTAL
        # =================================================

        total_registros = len(
            df_tabela
        )

        df_tabela = df_tabela.head(
            limite
        )

        # =================================================
        # CONFIGURAÇÃO
        # =================================================

        configuracao = {}

        if "NOME_ESTABELECIMENTO" in df_tabela.columns:

            configuracao[
                "NOME_ESTABELECIMENTO"
            ] = st.column_config.TextColumn(
                "Hospital / Estabelecimento",
                width="large"
            )

        if "CNES" in df_tabela.columns:

            configuracao[
                "CNES"
            ] = st.column_config.NumberColumn(
                "CNES",
                format="%d"
            )

        if "MUNICIPIO" in df_tabela.columns:

            configuracao[
                "MUNICIPIO"
            ] = st.column_config.TextColumn(
                "Município",
                width="medium"
            )

        if "UF" in df_tabela.columns:

            configuracao[
                "UF"
            ] = st.column_config.TextColumn(
                "UF",
                width="small"
            )

        if "DS_TIPO_UNIDADE" in df_tabela.columns:

            configuracao[
                "DS_TIPO_UNIDADE"
            ] = st.column_config.TextColumn(
                "Tipo de Unidade",
                width="medium"
            )

        if "NO_LOGRADOURO" in df_tabela.columns:

            configuracao[
                "NO_LOGRADOURO"
            ] = st.column_config.TextColumn(
                "Logradouro",
                width="large"
            )

        if "NU_ENDERECO" in df_tabela.columns:

            configuracao[
                "NU_ENDERECO"
            ] = st.column_config.TextColumn(
                "Número",
                width="small"
            )

        if "NO_COMPLEMENTO" in df_tabela.columns:

            configuracao[
                "NO_COMPLEMENTO"
            ] = st.column_config.TextColumn(
                "Complemento",
                width="medium"
            )

        if "NO_BAIRRO" in df_tabela.columns:

            configuracao[
                "NO_BAIRRO"
            ] = st.column_config.TextColumn(
                "Bairro",
                width="medium"
            )

        if "CO_CEP" in df_tabela.columns:

            configuracao[
                "CO_CEP"
            ] = st.column_config.TextColumn(
                "CEP",
                width="small"
            )

        # =================================================
        # DATAFRAME
        # =================================================

        st.dataframe(
            df_tabela,
            column_config=configuracao,
            width="stretch",
            hide_index=True,
            height=520
        )

        # =================================================
        # RODAPÉ
        # =================================================

        if total_registros > limite:

            st.html(
                f"""
                <div class="table-footer">

                    <span>
                        Exibindo os
                        <strong>{limite}</strong>
                        primeiros hospitais.
                    </span>

                    <span class="table-total">
                        Total:
                        {total_registros:,}
                    </span>

                </div>
                """.replace(
                    ",",
                    "."
                )
            )

        else:

            st.html(
                f"""
                <div class="table-footer">

                    <span>
                        Exibindo todos os hospitais encontrados.
                    </span>

                    <span class="table-total">
                        {total_registros:,} hospital(is)
                    </span>

                </div>
                """.replace(
                    ",",
                    "."
                )
            )

    # =====================================================
    # SOMA SEGURA
    # =====================================================

    @staticmethod
    def _soma(
        df,
        coluna
    ):

        if coluna not in df.columns:
            return 0

        serie = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

        return int(
            serie
            .fillna(0)
            .sum()
        )

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
                        rgba(37, 99, 235, 0.22),
                        rgba(99, 102, 241, 0.20),
                        rgba(15, 23, 42, 0.96)
                    );

                border:
                    1px solid
                    rgba(99, 102, 241, 0.22);

                box-shadow:
                    0 12px 40px
                    rgba(37, 99, 235, 0.12);

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
                    rgba(124, 58, 237, 0.18);

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
                        #2563EB,
                        #7C3AED
                    );

                box-shadow:
                    0 10px 30px
                    rgba(79, 70, 229, 0.35);

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


            .header-description {

                margin-top: 8px;

                color: #A5B4FC;

                font-size: 14px;

                line-height: 1.5;

                max-width: 780px;

            }


            .header-counter {

                position: relative;

                z-index: 1;

                min-width: 110px;

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
                    rgba(37,99,235,0.15);

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


            .kpi-card.violet {

                border-top:
                    3px solid #A855F7;

            }


            .kpi-card.violet .kpi-glow {

                background: #A855F7;

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
                        rgba(37,99,235,0.15),
                        rgba(124,58,237,0.15)
                    );

                border:
                    1px solid
                    rgba(99,102,241,0.15);

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
               CARDS DE RESUMO
               ================================================= */

            .uti-card {

                min-height: 145px;

                padding: 18px;

                border-radius: 16px;

                background:
                    rgba(15,23,42,0.92);

                border:
                    1px solid
                    rgba(255,255,255,0.07);

                position: relative;

                overflow: hidden;

            }


            .uti-glow {

                position: absolute;

                width: 80px;

                height: 80px;

                right: -35px;

                bottom: -35px;

                border-radius: 50%;

                opacity: 0.13;

            }


            .uti-card::before {

                content: "";

                position: absolute;

                left: 0;

                top: 0;

                bottom: 0;

                width: 4px;

            }


            .uti-card.blue::before {
                background: #2563EB;
            }

            .uti-card.cyan::before {
                background: #06B6D4;
            }

            .uti-card.purple::before {
                background: #7C3AED;
            }

            .uti-card.violet::before {
                background: #A855F7;
            }


            .uti-card.blue .uti-glow {
                background: #2563EB;
            }

            .uti-card.cyan .uti-glow {
                background: #06B6D4;
            }

            .uti-card.purple .uti-glow {
                background: #7C3AED;
            }

            .uti-card.violet .uti-glow {
                background: #A855F7;
            }


            .uti-icon {

                position: relative;

                z-index: 1;

                font-size: 21px;

                margin-bottom: 12px;

            }


            .uti-name {

                position: relative;

                z-index: 1;

                color: #CBD5E1;

                font-size: 11px;

                font-weight: 700;

            }


            .uti-value {

                position: relative;

                z-index: 1;

                color: #FFFFFF;

                font-size: 27px;

                font-weight: 800;

                margin-top: 5px;

            }


            .uti-label {

                position: relative;

                z-index: 1;

                color: #64748B;

                font-size: 8px;

                font-weight: 800;

                letter-spacing: 1px;

                margin-top: 2px;

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
               TABELA
               ================================================= */

            [data-testid="stDataFrame"] {

                border-radius: 16px;

                overflow: hidden;

                border:
                    1px solid
                    rgba(99,102,241,0.13);

                box-shadow:
                    0 8px 30px
                    rgba(0,0,0,0.18);

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

                color: #818CF8;

                font-weight: 700;

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