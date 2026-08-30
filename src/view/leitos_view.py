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


class LeitosView:

    # =====================================================
    # RENDER PRINCIPAL
    # =====================================================

    def render(self, model):

        self._aplicar_estilos()

        # =================================================
        # ORACLE
        # =================================================

        try:

            df = model.dados_para_view()

        except Exception as e:

            st.error(
                "Erro ao carregar os dados de leitos no Oracle."
            )

            st.exception(e)

            return

        if df is None or df.empty:

            st.warning(
                "Nenhum dado de leitos foi encontrado no Oracle."
            )

            return

        # =================================================
        # NORMALIZAÇÃO
        # =================================================

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.upper()
        )

        # =================================================
        # CONSOLIDAÇÃO
        # =================================================

        df = self._consolidar_hospitais(df)

        if df.empty:

            st.warning(
                "Nenhum estabelecimento hospitalar válido "
                "foi encontrado."
            )

            return

        # =================================================
        # PREPARAÇÃO
        # =================================================

        df_filtrado = df

        # =================================================
        # CABEÇALHO
        # =================================================

        self._render_cabecalho()

        # =================================================
        # KPIs
        # =================================================

        metricas = self._calcular_metricas(
            df_filtrado
        )

        self._render_kpis(
            metricas
        )

        st.write("")

        # =================================================
        # RESUMO UTI
        # =================================================

        self._render_resumo_uti(
            metricas
        )

        st.write("")

        # =================================================
        # GRÁFICOS
        # =================================================

        self._render_graficos(
            df_filtrado,
            metricas
        )

        st.write("")

        # =================================================
        # TABELA
        # =================================================

        self._render_tabela(
            df_filtrado
        )

    # =====================================================
    # CABEÇALHO
    # =====================================================

    def _render_cabecalho(self):

        st.html(
            """
            <div class="page-header">

                <div class="header-icon">
                    🏥
                </div>

                <div class="header-content">

                    <div class="header-eyebrow">
                        VITTA VISION • INFRAESTRUTURA DE SAÚDE
                    </div>

                    <div class="header-title">
                        Gestão de Leitos Hospitalares
                    </div>

                    <div class="header-description">
                        Monitoramento da infraestrutura hospitalar,
                        capacidade de atendimento e distribuição
                        dos leitos na rede de saúde.
                    </div>

                </div>

            </div>
            """
        )

    # =====================================================
    # CONSOLIDAÇÃO
    # =====================================================

    def _consolidar_hospitais(self, df):

        if df.empty:
            return df

        if "CNES" not in df.columns:
            return df

        return df.reset_index(
            drop=True
        )

    # =====================================================
    # MÉTRICAS
    # =====================================================

    def _calcular_metricas(self, df):

        total_estabelecimentos = len(df)

        total_leitos = self._soma(
            df,
            "LEITOS_EXISTENTES"
        )

        total_sus = self._soma(
            df,
            "LEITOS_SUS"
        )

        total_uti = self._soma(
            df,
            "UTI_TOTAL_EXIST"
        )

        total_uti_adulto = self._soma(
            df,
            "UTI_ADULTO_EXIST"
        )

        total_uti_pediatrica = self._soma(
            df,
            "UTI_PEDIATRICO_EXIST"
        )

        total_uti_neonatal = self._soma(
            df,
            "UTI_NEONATAL_EXIST"
        )

        total_uti_queimados = self._soma(
            df,
            "UTI_QUEIMADO_EXIST"
        )

        total_uti_coronariana = self._soma(
            df,
            "UTI_CORONARIANA_EXIST"
        )

        percentual_sus = (
            total_sus
            / total_leitos
            * 100
            if total_leitos > 0
            else 0
        )

        percentual_uti = (
            total_uti
            / total_leitos
            * 100
            if total_leitos > 0
            else 0
        )

        return {

            "total_estabelecimentos":
                total_estabelecimentos,

            "total_leitos":
                total_leitos,

            "total_sus":
                total_sus,

            "total_uti":
                total_uti,

            "total_uti_adulto":
                total_uti_adulto,

            "total_uti_pediatrica":
                total_uti_pediatrica,

            "total_uti_neonatal":
                total_uti_neonatal,

            "total_uti_queimados":
                total_uti_queimados,

            "total_uti_coronariana":
                total_uti_coronariana,

            "percentual_sus":
                percentual_sus,

            "percentual_uti":
                percentual_uti,
        }

    # =====================================================
    # KPIs
    # =====================================================

    def _render_kpis(self, metricas):

        total_estabelecimentos = (
            metricas["total_estabelecimentos"]
        )

        total_leitos = (
            metricas["total_leitos"]
        )

        total_sus = (
            metricas["total_sus"]
        )

        total_uti = (
            metricas["total_uti"]
        )

        percentual_sus = (
            metricas["percentual_sus"]
        )

        percentual_uti = (
            metricas["percentual_uti"]
        )

        col1, col2, col3, col4 = st.columns(
            4,
            gap="medium"
        )

        # =================================================
        # UNIDADES
        # =================================================

        with col1:

            self._render_kpi_card(
                icone="🏥",
                titulo="Unidades",
                valor=(
                    f"{total_estabelecimentos:,}"
                    .replace(",", ".")
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
                icone="🛏️",
                titulo="Total de Leitos",
                valor=(
                    f"{total_leitos:,}"
                    .replace(",", ".")
                ),
                descricao="Leitos cadastrados",
                detalhe="CAPACIDADE TOTAL",
                classe="cyan"
            )

        # =================================================
        # SUS
        # =================================================

        with col3:

            self._render_kpi_card(
                icone="🤝",
                titulo="Leitos SUS",
                valor=(
                    f"{total_sus:,}"
                    .replace(",", ".")
                ),
                descricao=f"{percentual_sus:.1f}% da rede",
                detalhe="ATENDIMENTO SUS",
                classe="purple"
            )

        # =================================================
        # UTI
        # =================================================

        with col4:

            self._render_kpi_card(
                icone="🚨",
                titulo="Leitos UTI",
                valor=(
                    f"{total_uti:,}"
                    .replace(",", ".")
                ),
                descricao=f"{percentual_uti:.1f}% dos leitos",
                detalhe="TERAPIA INTENSIVA",
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
    # RESUMO UTI
    # =====================================================

    def _render_resumo_uti(self, metricas):

        st.html(
            """
            <div class="section-heading">

                <div class="section-heading-icon">
                    🚨
                </div>

                <div>

                    <div class="section-heading-title">
                        Estrutura de Terapia Intensiva
                    </div>

                    <div class="section-heading-subtitle">
                        Distribuição dos leitos de UTI por especialidade
                    </div>

                </div>

            </div>
            """
        )

        dados = [

            (
                "Adulto",
                metricas["total_uti_adulto"],
                "🫀",
                "blue"
            ),

            (
                "Pediátrica",
                metricas["total_uti_pediatrica"],
                "👶",
                "cyan"
            ),

            (
                "Neonatal",
                metricas["total_uti_neonatal"],
                "🍼",
                "purple"
            ),

            (
                "Queimados",
                metricas["total_uti_queimados"],
                "🔥",
                "violet"
            ),

            (
                "Coronariana",
                metricas["total_uti_coronariana"],
                "❤️",
                "indigo"
            ),
        ]

        colunas = st.columns(
            5,
            gap="small"
        )

        for coluna, (
            nome,
            valor,
            icone,
            classe
        ) in zip(
            colunas,
            dados
        ):

            with coluna:

                st.html(
                    f"""
                    <div class="uti-card {classe}">

                        <div class="uti-glow"></div>

                        <div class="uti-icon">
                            {icone}
                        </div>

                        <div class="uti-name">
                            UTI {nome}
                        </div>

                        <div class="uti-value">
                            {valor:,}
                        </div>

                        <div class="uti-label">
                            LEITOS
                        </div>

                    </div>
                    """.replace(
                        ",",
                        "."
                    )
                )

    # =====================================================
    # GRÁFICOS
    # =====================================================

    def _render_graficos(
        self,
        df,
        metricas
    ):

        total_leitos = (
            metricas["total_leitos"]
        )

        if df.empty or total_leitos <= 0:

            st.info(
                "Não há dados suficientes para "
                "gerar os gráficos."
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
                        Distribuição e composição da infraestrutura hospitalar
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
        # PERFIL UTI
        # =================================================

        with col_esquerda:

            st.html(
                """
                <div class="chart-box">

                    <div class="chart-title">
                        Perfil de Leitos de UTI
                    </div>

                    <div class="chart-subtitle">
                        Distribuição por especialidade
                    </div>

                </div>
                """
            )

            nomes_uti = []
            valores_uti = []

            dados_uti = [

                (
                    "UTI Adulto",
                    metricas["total_uti_adulto"]
                ),

                (
                    "UTI Pediátrica",
                    metricas["total_uti_pediatrica"]
                ),

                (
                    "UTI Neonatal",
                    metricas["total_uti_neonatal"]
                ),

                (
                    "UTI Queimados",
                    metricas["total_uti_queimados"]
                ),

                (
                    "UTI Coronariana",
                    metricas["total_uti_coronariana"]
                ),
            ]

            for nome, valor in dados_uti:

                if valor > 0:

                    nomes_uti.append(nome)
                    valores_uti.append(valor)

            if valores_uti:

                fig_uti = go.Figure(
                    go.Bar(
                        x=valores_uti,
                        y=nomes_uti,
                        orientation="h",

                        text=[
                            f"{valor:,}".replace(
                                ",",
                                "."
                            )
                            for valor in valores_uti
                        ],

                        textposition="outside",

                        marker=dict(
                            color=[
                                "#3B82F6",
                                "#06B6D4",
                                "#8B5CF6",
                                "#A855F7",
                                "#6366F1",
                            ][:len(valores_uti)],

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

                fig_uti.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",

                    font=dict(
                        color="#E5E7EB",
                        size=12,
                    ),

                    margin=dict(
                        l=20,
                        r=55,
                        t=15,
                        b=20,
                    ),

                    height=330,

                    xaxis=dict(
                        showgrid=True,
                        gridcolor="rgba(99,102,241,0.10)",
                        zeroline=False,
                        showticklabels=False,
                    ),

                    yaxis=dict(
                        showgrid=False,
                        autorange="reversed",

                        tickfont=dict(
                            color="#C7D2FE",
                            size=12
                        ),
                    ),

                    showlegend=False,

                    bargap=0.35,
                )

                st.plotly_chart(
                    fig_uti,
                    width="stretch",
                    config={
                        "displayModeBar": False,
                        "responsive": True
                    }
                )

            else:

                st.info(
                    "Nenhum leito de UTI específico "
                    "foi detalhado."
                )

        # =================================================
        # SUS VS PRIVADO
        # =================================================

        with col_direita:

            st.html(
                """
                <div class="chart-box">

                    <div class="chart-title">
                        Proporção SUS vs Privado
                    </div>

                    <div class="chart-subtitle">
                        Composição do total de leitos cadastrados
                    </div>

                </div>
                """
            )

            total_sus = (
                metricas["total_sus"]
            )

            outros_leitos = max(
                0,
                total_leitos - total_sus
            )

            fig_pie = go.Figure(
                go.Pie(
                    labels=[
                        "Leitos SUS",
                        "Privado / Outros"
                    ],

                    values=[
                        total_sus,
                        outros_leitos
                    ],

                    hole=0.68,

                    textinfo="percent",

                    textfont=dict(
                        size=15,
                        color="#FFFFFF"
                    ),

                    marker=dict(

                        colors=[
                            "#6366F1",
                            "#2563EB"
                        ],

                        line=dict(
                            color="#0F172A",
                            width=3
                        )
                    ),

                    hovertemplate=(
                        "<b>%{label}</b>"
                        "<br>"
                        "Leitos: %{value:,}"
                        "<br>"
                        "Participação: %{percent}"
                        "<extra></extra>"
                    )
                )
            )

            fig_pie.update_layout(

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    color="#E5E7EB",
                    size=13
                ),

                margin=dict(
                    l=20,
                    r=20,
                    t=10,
                    b=45
                ),

                height=330,

                showlegend=True,

                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.08,
                    xanchor="center",
                    x=0.5,

                    font=dict(
                        color="#A5B4FC",
                        size=12
                    )
                )
            )

            st.plotly_chart(
                fig_pie,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True
                }
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
                        Detalhamento dos estabelecimentos e respectivos leitos
                    </div>

                </div>

            </div>
            """
        )

        if df.empty:

            st.warning(
                "Nenhum estabelecimento hospitalar encontrado."
            )

            return

        limite = 500

        colunas_exibir = [

            "NOME_ESTABELECIMENTO",
            "CNES",
            "MUNICIPIO",
            "UF",
            "LEITOS_EXISTENTES",
            "LEITOS_SUS",
            "UTI_TOTAL_EXIST",
            "UTI_TOTAL_SUS",
            "DS_TIPO_UNIDADE",
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
        # CONVERSÃO NUMÉRICA
        # =================================================

        colunas_numericas = [

            "CNES",
            "LEITOS_EXISTENTES",
            "LEITOS_SUS",
            "UTI_TOTAL_EXIST",
            "UTI_TOTAL_SUS",

        ]

        for coluna in colunas_numericas:

            if coluna in df_tabela.columns:

                df_tabela[coluna] = pd.to_numeric(
                    df_tabela[coluna],
                    errors="coerce"
                ).fillna(0)

        # =================================================
        # ORDENAÇÃO
        # =================================================

        if "LEITOS_EXISTENTES" in df_tabela.columns:

            df_tabela = df_tabela.sort_values(
                by="LEITOS_EXISTENTES",
                ascending=False
            )

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

        if "LEITOS_EXISTENTES" in df_tabela.columns:

            max_leitos = int(
                df_tabela[
                    "LEITOS_EXISTENTES"
                ].max() or 1
            )

            configuracao[
                "LEITOS_EXISTENTES"
            ] = st.column_config.ProgressColumn(
                "Total de Leitos",
                format="%d",
                min_value=0,
                max_value=max_leitos
            )

        if "LEITOS_SUS" in df_tabela.columns:

            configuracao[
                "LEITOS_SUS"
            ] = st.column_config.NumberColumn(
                "Leitos SUS",
                format="%d"
            )

        if "UTI_TOTAL_EXIST" in df_tabela.columns:

            configuracao[
                "UTI_TOTAL_EXIST"
            ] = st.column_config.NumberColumn(
                "UTI Total",
                format="%d"
            )

        if "UTI_TOTAL_SUS" in df_tabela.columns:

            configuracao[
                "UTI_TOTAL_SUS"
            ] = st.column_config.NumberColumn(
                "UTI SUS",
                format="%d"
            )

        if "DS_TIPO_UNIDADE" in df_tabela.columns:

            configuracao[
                "DS_TIPO_UNIDADE"
            ] = st.column_config.TextColumn(
                "Tipo de Unidade",
                width="medium"
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
                        maiores estabelecimentos por quantidade de leitos.
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
                        Exibindo todos os estabelecimentos encontrados.
                    </span>

                    <span class="table-total">
                        {total_registros:,} estabelecimento(s)
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
            serie.fillna(0).sum()
        )

    # =====================================================
    # ESTILOS
    # =====================================================

    def _aplicar_estilos(self):

        st.html(
            """
            <style>

            /* =================================================
               PALETA
               =================================================

               Azul:
               #2563EB
               #3B82F6
               #06B6D4

               Roxo:
               #6366F1
               #7C3AED
               #8B5CF6
               #A855F7

               ================================================= */


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
               UTI
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

            .uti-card.indigo::before {
                background: #6366F1;
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

            .uti-card.indigo .uti-glow {
                background: #6366F1;
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
               BOTÃO EXPORTAR
               ================================================= */

            [data-testid="stDownloadButton"] button {

                border-radius: 10px;

                border:
                    1px solid
                    rgba(99,102,241,0.35);

                background:
                    linear-gradient(
                        135deg,
                        rgba(37,99,235,0.12),
                        rgba(124,58,237,0.12)
                    );

                color: #A5B4FC;

                font-weight: 700;

                transition:
                    all 0.2s ease;

            }


            [data-testid="stDownloadButton"] button:hover {

                border-color:
                    rgba(129,140,248,0.70);

                background:
                    linear-gradient(
                        135deg,
                        rgba(37,99,235,0.22),
                        rgba(124,58,237,0.22)
                    );

                color: #FFFFFF;

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

            }


            </style>
            """
        )