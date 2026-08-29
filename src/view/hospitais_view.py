import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


class HospitaisView:

    # =========================================================
    # RENDER PRINCIPAL
    # =========================================================

    def render(self, model):

        # =====================================================
        # CSS
        # =====================================================

        self._aplicar_estilos()

        # =====================================================
        # CARREGAMENTO DOS DADOS
        # =====================================================

        try:
            df = model.listar_dados()

        except Exception as e:

            st.error(
                "Erro ao carregar os dados hospitalares do Oracle."
            )

            st.exception(e)

            return

        if df is None or df.empty:

            st.warning(
                "Nenhum dado hospitalar foi encontrado no Oracle."
            )

            return

        # =====================================================
        # NORMALIZAÇÃO DAS COLUNAS
        # =====================================================

        df.columns = [
            str(coluna).strip().upper()
            for coluna in df.columns
        ]

        # =====================================================
        # CONVERSÃO NUMÉRICA
        # =====================================================

        colunas_numericas = [
            "COD_IBGE",
            "COD_UF",
            "POPULACAO_ESTIMADA",

            "INTERNACOES_JAN_2025",
            "INTERNACOES_FEV_2025",
            "INTERNACOES_MAR_2025",
            "INTERNACOES_ABR_2025",
            "INTERNACOES_MAI_2025",
            "INTERNACOES_JUN_2025",
            "INTERNACOES_JUL_2025",
            "INTERNACOES_AGO_2025",
            "INTERNACOES_SET_2025",
            "INTERNACOES_OUT_2025",
            "INTERNACOES_NOV_2025",
            "INTERNACOES_DEZ_2025",

            "INTERNACOES_TOTAL_2025",

            "LEITOS_EXISTENTES",
            "LEITOS_SUS",

            "UTI_TOTAL_EXIST",
            "UTI_TOTAL_SUS",

            "UTI_ADULTO_EXIST",
            "UTI_ADULTO_SUS",

            "UTI_PEDIATRICO_EXIST",
            "UTI_PEDIATRICO_SUS",

            "UTI_NEONATAL_EXIST",
            "UTI_NEONATAL_SUS",

            "UTI_QUEIMADO_EXIST",
            "UTI_QUEIMADO_SUS",

            "UTI_CORONARIANA_EXIST",
            "UTI_CORONARIANA_SUS",
        ]

        for coluna in colunas_numericas:

            if coluna in df.columns:

                df[coluna] = pd.to_numeric(
                    df[coluna],
                    errors="coerce"
                ).fillna(0)

        # =====================================================
        # FILTROS
        # =====================================================

        df_filtrado = self._render_filtros(df)

        # =====================================================
        # CABEÇALHO
        # =====================================================

        self._render_cabecalho()

        # =====================================================
        # DOWNLOAD
        # =====================================================

        csv_data = df_filtrado.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="📥 Exportar Dados Filtrados",
            data=csv_data,
            file_name="dados_hospitalares_filtrados.csv",
            mime="text/csv",
            use_container_width=True,
            key="btn_exportar_hospitais",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================================================
        # INDICADORES
        # =====================================================

        self._render_indicadores(
            df_filtrado
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================================================
        # GRÁFICOS PRINCIPAIS
        # =====================================================

        self._render_graficos(
            df_filtrado
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================================================
        # DISTRIBUIÇÃO GEOGRÁFICA
        # =====================================================

        self._render_distribuicao_geografica(
            df_filtrado
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # =====================================================
        # TABELA DE MUNICÍPIOS
        # =====================================================

        self._render_tabela(
            df_filtrado
        )

    # =========================================================
    # CSS
    # =========================================================

    def _aplicar_estilos(self):

        st.markdown(
            """
            <style>

            .hospital-card {

                background:
                    linear-gradient(
                        145deg,
                        rgba(18, 24, 38, 0.92),
                        rgba(26, 16, 47, 0.92)
                    );

                border:
                    1px solid
                    rgba(168, 85, 247, 0.16);

                border-radius: 16px;

                padding: 20px;

                box-shadow:
                    0 8px 32px
                    rgba(0, 0, 0, 0.30);

                min-height: 125px;

            }

            .hospital-card-title {

                color: #9ca3af;

                font-size: 14px;

                font-weight: 600;

                margin-bottom: 5px;

            }

            .hospital-card-value {

                color: #ffffff;

                font-size: 27px;

                font-weight: 800;

                margin: 0;

            }

            .hospital-card-sub {

                color: #9ca3af;

                font-size: 12px;

                font-weight: 600;

                margin-top: 4px;

            }

            .hospital-section {

                color: #ffffff;

                font-size: 20px;

                font-weight: 700;

                margin-bottom: 12px;

            }

            </style>
            """,
            unsafe_allow_html=True,
        )

    # =========================================================
    # FILTROS
    # =========================================================

    def _render_filtros(self, df):

        with st.sidebar:

            st.header("🎛️ Filtros Avançados")

            df_filtrado = df.copy()

            # =================================================
            # REGIÃO
            # =================================================

            # A TB_GERAL não possui REGIAO.
            # Criamos a região a partir da UF.

            mapa_regioes = {

                "AC": "Norte",
                "AP": "Norte",
                "AM": "Norte",
                "PA": "Norte",
                "RO": "Norte",
                "RR": "Norte",
                "TO": "Norte",

                "AL": "Nordeste",
                "BA": "Nordeste",
                "CE": "Nordeste",
                "MA": "Nordeste",
                "PB": "Nordeste",
                "PE": "Nordeste",
                "PI": "Nordeste",
                "RN": "Nordeste",
                "SE": "Nordeste",

                "DF": "Centro-Oeste",
                "GO": "Centro-Oeste",
                "MT": "Centro-Oeste",
                "MS": "Centro-Oeste",

                "ES": "Sudeste",
                "MG": "Sudeste",
                "RJ": "Sudeste",
                "SP": "Sudeste",

                "PR": "Sul",
                "RS": "Sul",
                "SC": "Sul",
            }

            if "UF" in df_filtrado.columns:

                df_filtrado["_REGIAO"] = (
                    df_filtrado["UF"]
                    .astype(str)
                    .str.upper()
                    .map(mapa_regioes)
                )

                regioes = sorted(
                    df_filtrado["_REGIAO"]
                    .dropna()
                    .unique()
                )

                regiao = st.selectbox(
                    "Região:",
                    ["TODAS"] + regioes,
                    key="hospital_regiao",
                )

                if regiao != "TODAS":

                    df_filtrado = df_filtrado[
                        df_filtrado["_REGIAO"]
                        == regiao
                    ]

            # =================================================
            # UF
            # =================================================

            if "UF" in df_filtrado.columns:

                ufs = sorted(
                    df_filtrado["UF"]
                    .dropna()
                    .astype(str)
                    .unique()
                )

                uf = st.selectbox(
                    "UF:",
                    ["TODAS"] + ufs,
                    key="hospital_uf",
                )

                if uf != "TODAS":

                    df_filtrado = df_filtrado[
                        df_filtrado["UF"]
                        .astype(str)
                        == uf
                    ]

            # =================================================
            # MUNICÍPIO
            # =================================================

            if "MUNICIPIO" in df_filtrado.columns:

                municipios = sorted(
                    df_filtrado["MUNICIPIO"]
                    .dropna()
                    .astype(str)
                    .unique()
                )

                municipio = st.selectbox(
                    "Município:",
                    ["TODOS"] + municipios,
                    key="hospital_municipio",
                )

                if municipio != "TODOS":

                    df_filtrado = df_filtrado[
                        df_filtrado["MUNICIPIO"]
                        .astype(str)
                        == municipio
                    ]

            # =================================================
            # BUSCA
            # =================================================

            busca = st.text_input(
                "Buscar Município:",
                placeholder="Digite o nome do município...",
                key="hospital_busca",
            )

            if busca and "MUNICIPIO" in df_filtrado.columns:

                df_filtrado = df_filtrado[
                    df_filtrado["MUNICIPIO"]
                    .astype(str)
                    .str.contains(
                        busca,
                        case=False,
                        na=False,
                    )
                ]

            # =================================================
            # LIMPAR FILTROS
            # =================================================

            if st.button(
                "🔄 Recarregar dados",
                use_container_width=True,
            ):

                st.cache_data.clear()
                st.rerun()

        return df_filtrado

    # =========================================================
    # CABEÇALHO
    # =========================================================

    def _render_cabecalho(self):

        st.markdown(
            """
            <div style="
                margin-bottom: 20px;
            ">

                <h1 style="
                    margin: 0;
                    font-size: 32px;
                    font-weight: 800;
                    color: #ffffff;
                ">

                    🏥 Painel de
                    <span style="
                        color: #a855f7;
                    ">
                        Hospitais
                    </span>

                </h1>

                <p style="
                    margin: 6px 0 0 0;
                    font-size: 15px;
                    color: #9ca3af;
                ">

                    Monitoramento de infraestrutura
                    hospitalar, leitos, UTIs e
                    internações por município.

                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # =========================================================
    # INDICADORES
    # =========================================================

    def _render_indicadores(self, df):

        if df.empty:

            total_municipios = 0
            populacao = 0
            internacoes = 0
            leitos = 0
            leitos_sus = 0
            uti = 0

        else:

            total_municipios = (
                df["COD_IBGE"].nunique()
                if "COD_IBGE" in df.columns
                else len(df)
            )

            populacao = (
                int(df["POPULACAO_ESTIMADA"].sum())
                if "POPULACAO_ESTIMADA" in df.columns
                else 0
            )

            internacoes = (
                int(df["INTERNACOES_TOTAL_2025"].sum())
                if "INTERNACOES_TOTAL_2025" in df.columns
                else 0
            )

            leitos = (
                int(df["LEITOS_EXISTENTES"].sum())
                if "LEITOS_EXISTENTES" in df.columns
                else 0
            )

            leitos_sus = (
                int(df["LEITOS_SUS"].sum())
                if "LEITOS_SUS" in df.columns
                else 0
            )

            uti = (
                int(df["UTI_TOTAL_EXIST"].sum())
                if "UTI_TOTAL_EXIST" in df.columns
                else 0
            )

        col1, col2, col3, col4, col5, col6 = st.columns(
            6,
            gap="medium",
        )

        # =====================================================
        # MUNICÍPIOS
        # =====================================================

        with col1:

            self._card(
                "Municípios",
                total_municipios,
                "Municípios analisados",
                "🏙️",
                "#a855f7",
            )

        # =====================================================
        # POPULAÇÃO
        # =====================================================

        with col2:

            self._card(
                "População",
                populacao,
                "População estimada",
                "👥",
                "#3b82f6",
            )

        # =====================================================
        # INTERNAÇÕES
        # =====================================================

        with col3:

            self._card(
                "Internações",
                internacoes,
                "Total em 2025",
                "🏥",
                "#8b5cf6",
            )

        # =====================================================
        # LEITOS
        # =====================================================

        with col4:

            self._card(
                "Leitos Totais",
                leitos,
                "Capacidade cadastrada",
                "🛏️",
                "#06b6d4",
            )

        # =====================================================
        # LEITOS SUS
        # =====================================================

        with col5:

            percentual_sus = (
                leitos_sus / leitos * 100
                if leitos > 0
                else 0
            )

            self._card(
                "Leitos SUS",
                leitos_sus,
                f"{percentual_sus:.1f}% dos leitos",
                "🤝",
                "#10b981",
            )

        # =====================================================
        # UTI
        # =====================================================

        with col6:

            self._card(
                "UTIs",
                uti,
                "UTI total cadastrada",
                "🚨",
                "#ef4444",
            )

    # =========================================================
    # CARD
    # =========================================================

    def _card(
        self,
        titulo,
        valor,
        subtitulo,
        icone,
        cor,
    ):

        valor_formatado = (
            f"{int(valor):,}"
            .replace(",", ".")
        )

        st.markdown(
            f"""
            <div class="hospital-card">

                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                ">

                    <div>

                        <div class="hospital-card-title">
                            {titulo}
                        </div>

                        <div class="hospital-card-value">
                            {valor_formatado}
                        </div>

                        <div class="hospital-card-sub">
                            {subtitulo}
                        </div>

                    </div>

                    <div style="
                        background:
                            linear-gradient(
                                135deg,
                                {cor},
                                {cor}CC
                            );

                        border-radius: 12px;

                        padding: 10px;

                        font-size: 20px;
                    ">

                        {icone}

                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # =========================================================
    # GRÁFICOS
    # =========================================================

    def _render_graficos(self, df):

        col1, col2 = st.columns(
            [1, 1.4],
            gap="medium",
        )

        # =====================================================
        # GRÁFICO 1 — LEITOS SUS VS NÃO SUS
        # =====================================================

        with col1:

            st.markdown(
                '<div class="hospital-section">'
                '🛏️ Leitos SUS vs Não SUS'
                '</div>',
                unsafe_allow_html=True,
            )

            if df.empty:

                st.info(
                    "Nenhum dado disponível."
                )

            else:

                total_leitos = (
                    int(
                        df["LEITOS_EXISTENTES"].sum()
                    )
                    if "LEITOS_EXISTENTES" in df.columns
                    else 0
                )

                leitos_sus = (
                    int(
                        df["LEITOS_SUS"].sum()
                    )
                    if "LEITOS_SUS" in df.columns
                    else 0
                )

                leitos_outros = max(
                    0,
                    total_leitos - leitos_sus,
                )

                df_pie = pd.DataFrame(
                    {
                        "Categoria": [
                            "Leitos SUS",
                            "Não SUS",
                        ],
                        "Quantidade": [
                            leitos_sus,
                            leitos_outros,
                        ],
                    }
                )

                fig = go.Figure(
                    go.Pie(
                        labels=df_pie["Categoria"],
                        values=df_pie["Quantidade"],
                        hole=0.65,
                        marker=dict(
                            colors=[
                                "#10b981",
                                "#3b82f6",
                            ]
                        ),
                        textinfo="percent",
                        textfont=dict(
                            color="white",
                            size=13,
                        ),
                        hovertemplate=(
                            "<b>%{label}</b><br>"
                            "%{value:,} leitos"
                            "<extra></extra>"
                        ),
                    )
                )

                fig.update_layout(
                    height=320,
                    margin=dict(
                        l=10,
                        r=10,
                        t=10,
                        b=10,
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(
                        color="#ffffff"
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.15,
                        xanchor="center",
                        x=0.5,
                    ),
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False
                    },
                )

        # =====================================================
        # GRÁFICO 2 — TOP MUNICÍPIOS POR LEITOS
        # =====================================================

        with col2:

            st.markdown(
                '<div class="hospital-section">'
                '🏆 Municípios com Mais Leitos'
                '</div>',
                unsafe_allow_html=True,
            )

            if df.empty:

                st.info(
                    "Nenhum dado disponível."
                )

            else:

                ranking = (
                    df.groupby(
                        [
                            "MUNICIPIO",
                            "UF",
                        ],
                        as_index=False,
                    )[
                        "LEITOS_EXISTENTES"
                    ]
                    .sum()
                    .sort_values(
                        "LEITOS_EXISTENTES",
                        ascending=False,
                    )
                    .head(10)
                )

                ranking["LOCAL"] = (
                    ranking["MUNICIPIO"]
                    + " - "
                    + ranking["UF"]
                )

                fig = go.Figure()

                fig.add_trace(
                    go.Bar(
                        x=ranking[
                            "LEITOS_EXISTENTES"
                        ],
                        y=ranking["LOCAL"],
                        orientation="h",
                        text=[
                            f"{int(v):,}".replace(
                                ",",
                                ".",
                            )
                            for v in ranking[
                                "LEITOS_EXISTENTES"
                            ]
                        ],
                        textposition="outside",
                        cliponaxis=False,
                        marker=dict(
                            color="#8b5cf6"
                        ),
                    )
                )

                fig.update_layout(
                    height=320,
                    margin=dict(
                        l=10,
                        r=60,
                        t=10,
                        b=10,
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(
                        color="#ffffff"
                    ),
                    xaxis=dict(
                        visible=False
                    ),
                    yaxis=dict(
                        autorange="reversed",
                        showgrid=False,
                    ),
                    showlegend=False,
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={
                        "displayModeBar": False
                    },
                )

        # =====================================================
        # INTERNAÇÕES POR MÊS
        # =====================================================

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="hospital-section">'
            '📈 Evolução Mensal das Internações'
            '</div>',
            unsafe_allow_html=True,
        )

        meses = [
            ("JAN", "Janeiro"),
            ("FEV", "Fevereiro"),
            ("MAR", "Março"),
            ("ABR", "Abril"),
            ("MAI", "Maio"),
            ("JUN", "Junho"),
            ("JUL", "Julho"),
            ("AGO", "Agosto"),
            ("SET", "Setembro"),
            ("OUT", "Outubro"),
            ("NOV", "Novembro"),
            ("DEZ", "Dezembro"),
        ]

        valores = []
        nomes = []

        for abreviacao, nome in meses:

            coluna = (
                f"INTERNACOES_{abreviacao}_2025"
            )

            if coluna in df.columns:

                valores.append(
                    int(df[coluna].sum())
                )

                nomes.append(nome)

        if valores:

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=nomes,
                    y=valores,
                    mode="lines+markers",
                    line=dict(
                        color="#a855f7",
                        width=3,
                    ),
                    marker=dict(
                        size=7,
                        color="#c084fc",
                    ),
                    fill="tozeroy",
                    fillcolor=(
                        "rgba(168,85,247,0.12)"
                    ),
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Internações: %{y:,}"
                        "<extra></extra>"
                    ),
                )
            )

            fig.update_layout(
                height=330,
                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=20,
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#ffffff"
                ),
                xaxis=dict(
                    showgrid=False,
                ),
                yaxis=dict(
                    gridcolor=(
                        "rgba(255,255,255,0.05)"
                    ),
                    zeroline=False,
                ),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )

        else:

            st.info(
                "Não existem dados mensais disponíveis."
            )

    # =========================================================
    # DISTRIBUIÇÃO GEOGRÁFICA
    # =========================================================

    def _render_distribuicao_geografica(self, df):

        st.markdown(
            '<div class="hospital-section">'
            '🗺️ Distribuição Geográfica'
            '</div>',
            unsafe_allow_html=True,
        )

        if df.empty:

            st.info(
                "Nenhum dado disponível."
            )

            return

        mapa_regioes = {

            "AC": "Norte",
            "AP": "Norte",
            "AM": "Norte",
            "PA": "Norte",
            "RO": "Norte",
            "RR": "Norte",
            "TO": "Norte",

            "AL": "Nordeste",
            "BA": "Nordeste",
            "CE": "Nordeste",
            "MA": "Nordeste",
            "PB": "Nordeste",
            "PE": "Nordeste",
            "PI": "Nordeste",
            "RN": "Nordeste",
            "SE": "Nordeste",

            "DF": "Centro-Oeste",
            "GO": "Centro-Oeste",
            "MT": "Centro-Oeste",
            "MS": "Centro-Oeste",

            "ES": "Sudeste",
            "MG": "Sudeste",
            "RJ": "Sudeste",
            "SP": "Sudeste",

            "PR": "Sul",
            "RS": "Sul",
            "SC": "Sul",
        }

        df_geo = df.copy()

        df_geo["REGIAO"] = (
            df_geo["UF"]
            .astype(str)
            .str.upper()
            .map(mapa_regioes)
        )

        regiao = (
            df_geo.groupby(
                "REGIAO",
                as_index=False,
            )
            .agg(
                Municipios=(
                    "COD_IBGE",
                    "nunique",
                ),
                Leitos=(
                    "LEITOS_EXISTENTES",
                    "sum",
                ),
                Leitos_SUS=(
                    "LEITOS_SUS",
                    "sum",
                ),
                Internacoes=(
                    "INTERNACOES_TOTAL_2025",
                    "sum",
                ),
            )
            .sort_values(
                "Leitos",
                ascending=False,
            )
        )

        col1, col2 = st.columns(2)

        # =====================================================
        # LEITOS POR REGIÃO
        # =====================================================

        with col1:

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=regiao["REGIAO"],
                    y=regiao["Leitos"],
                    text=[
                        f"{int(v):,}".replace(
                            ",",
                            ".",
                        )
                        for v in regiao["Leitos"]
                    ],
                    textposition="outside",
                    marker=dict(
                        color="#3b82f6"
                    ),
                )
            )

            fig.update_layout(
                title=dict(
                    text="Leitos por Região",
                    font=dict(
                        color="#ffffff",
                        size=16,
                    ),
                ),
                height=330,
                margin=dict(
                    l=20,
                    r=20,
                    t=55,
                    b=20,
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#ffffff"
                ),
                yaxis=dict(
                    showgrid=False,
                    visible=False,
                ),
                xaxis=dict(
                    showgrid=False,
                ),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )

        # =====================================================
        # INTERNAÇÕES POR REGIÃO
        # =====================================================

        with col2:

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=regiao["REGIAO"],
                    y=regiao["Internacoes"],
                    text=[
                        f"{int(v):,}".replace(
                            ",",
                            ".",
                        )
                        for v in regiao[
                            "Internacoes"
                        ]
                    ],
                    textposition="outside",
                    marker=dict(
                        color="#10b981"
                    ),
                )
            )

            fig.update_layout(
                title=dict(
                    text="Internações por Região",
                    font=dict(
                        color="#ffffff",
                        size=16,
                    ),
                ),
                height=330,
                margin=dict(
                    l=20,
                    r=20,
                    t=55,
                    b=20,
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#ffffff"
                ),
                yaxis=dict(
                    showgrid=False,
                    visible=False,
                ),
                xaxis=dict(
                    showgrid=False,
                ),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                },
            )

    # =========================================================
    # TABELA
    # =========================================================

    def _render_tabela(self, df):

        st.markdown(
            '<div class="hospital-section">'
            '📋 Relação de Municípios'
            '</div>',
            unsafe_allow_html=True,
        )

        if df.empty:

            st.warning(
                "Nenhum município encontrado "
                "com os filtros selecionados."
            )

            return

        colunas = [
            "MUNICIPIO",
            "UF",
            "POPULACAO_ESTIMADA",
            "INTERNACOES_TOTAL_2025",
            "LEITOS_EXISTENTES",
            "LEITOS_SUS",
            "UTI_TOTAL_EXIST",
            "UTI_TOTAL_SUS",
        ]

        colunas = [
            coluna
            for coluna in colunas
            if coluna in df.columns
        ]

        tabela = df[colunas].copy()

        tabela = tabela.sort_values(
            by="LEITOS_EXISTENTES"
            if "LEITOS_EXISTENTES" in tabela.columns
            else tabela.columns[0],
            ascending=False,
        )

        nomes = {
            "MUNICIPIO":
                "Município",

            "UF":
                "UF",

            "POPULACAO_ESTIMADA":
                "População",

            "INTERNACOES_TOTAL_2025":
                "Internações 2025",

            "LEITOS_EXISTENTES":
                "Leitos Totais",

            "LEITOS_SUS":
                "Leitos SUS",

            "UTI_TOTAL_EXIST":
                "UTI Total",

            "UTI_TOTAL_SUS":
                "UTI SUS",
        }

        tabela = tabela.rename(
            columns=nomes
        )

        configuracao = {}

        if "Município" in tabela.columns:

            configuracao[
                "Município"
            ] = st.column_config.TextColumn(
                "Município",
                width="large",
            )

        if "UF" in tabela.columns:

            configuracao[
                "UF"
            ] = st.column_config.TextColumn(
                "UF",
                width="small",
            )

        for coluna in [
            "População",
            "Internações 2025",
            "Leitos Totais",
            "Leitos SUS",
            "UTI Total",
            "UTI SUS",
        ]:

            if coluna in tabela.columns:

                configuracao[
                    coluna
                ] = st.column_config.NumberColumn(
                    coluna,
                    format="%d",
                )

        st.dataframe(
            tabela,
            column_config=configuracao,
            use_container_width=True,
            hide_index=True,
            height=450,
        )

        st.caption(
            f"Exibindo {len(tabela):,} municípios."
            .replace(",", ".")
        )