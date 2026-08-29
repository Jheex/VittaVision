import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# EXPORTAÇÃO CSV
# =========================================================

@st.cache_data(show_spinner=False)
def converter_df_para_csv(df_export):
    return df_export.to_csv(index=False).encode("utf-8")


class LeitosView:

    def render(self, model):

        # =====================================================
        # CSS
        # =====================================================

        st.markdown(
            """
            <style>

            /* Fundo dos cards de métricas */
            [data-testid="stMetric"] {
                background: rgba(18, 24, 38, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 18px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.20);
            }

            [data-testid="stMetricLabel"] {
                color: #9ca3af !important;
            }

            [data-testid="stMetricValue"] {
                color: #ffffff !important;
            }

            /* Dataframe */
            [data-testid="stDataFrame"] {
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                overflow: hidden;
            }

            /* Gráficos */
            [data-testid="stPlotlyChart"] {
                background: rgba(18, 24, 38, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 10px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

        # =====================================================
        # CARREGAR DADOS
        # =====================================================

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

        # =====================================================
        # NORMALIZAR COLUNAS
        # =====================================================

        df.columns = [
            str(coluna).strip().upper()
            for coluna in df.columns
        ]

        # =====================================================
        # CONVERTER COLUNAS NUMÉRICAS
        # =====================================================

        colunas_numericas = [
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

        with st.sidebar:

            st.header("🎛️ Filtros Avançados")

            df_filtrado = df.copy()

            # -------------------------------------------------
            # REGIÃO
            # -------------------------------------------------

            if "REGIAO" in df_filtrado.columns:

                regioes = sorted(
                    df_filtrado["REGIAO"]
                    .dropna()
                    .astype(str)
                    .unique()
                )

                regiao_escolhida = st.selectbox(
                    "Região:",
                    ["TODOS"] + regioes,
                    key="leitos_regiao",
                )

                if regiao_escolhida != "TODOS":

                    df_filtrado = df_filtrado[
                        df_filtrado["REGIAO"].astype(str)
                        == regiao_escolhida
                    ]

            # -------------------------------------------------
            # UF
            # -------------------------------------------------

            if "UF" in df_filtrado.columns:

                ufs = sorted(
                    df_filtrado["UF"]
                    .dropna()
                    .astype(str)
                    .unique()
                )

                uf_escolhida = st.selectbox(
                    "UF:",
                    ["TODOS"] + ufs,
                    key="leitos_uf",
                )

                if uf_escolhida != "TODOS":

                    df_filtrado = df_filtrado[
                        df_filtrado["UF"].astype(str)
                        == uf_escolhida
                    ]

            # -------------------------------------------------
            # MUNICÍPIO
            # -------------------------------------------------

            if "MUNICIPIO" in df_filtrado.columns:

                municipios = sorted(
                    df_filtrado["MUNICIPIO"]
                    .dropna()
                    .astype(str)
                    .unique()
                )

                mun_escolhido = st.selectbox(
                    "Município:",
                    ["TODOS"] + municipios,
                    key="leitos_municipio",
                )

                if mun_escolhido != "TODOS":

                    df_filtrado = df_filtrado[
                        df_filtrado["MUNICIPIO"].astype(str)
                        == mun_escolhido
                    ]

            # -------------------------------------------------
            # ESFERA
            # -------------------------------------------------

            if "DESC_NATUREZA_JURIDICA" in df_filtrado.columns:

                esferas = sorted(
                    df_filtrado["DESC_NATUREZA_JURIDICA"]
                    .dropna()
                    .astype(str)
                    .unique()
                )

                esfera_escolhida = st.selectbox(
                    "Esfera (Público/Privado):",
                    ["TODOS"] + esferas,
                    key="leitos_esfera",
                )

                if esfera_escolhida != "TODOS":

                    df_filtrado = df_filtrado[
                        df_filtrado[
                            "DESC_NATUREZA_JURIDICA"
                        ].astype(str)
                        == esfera_escolhida
                    ]

            # -------------------------------------------------
            # TIPO DE UNIDADE
            # -------------------------------------------------

            if "DS_TIPO_UNIDADE" in df_filtrado.columns:

                tipos = sorted(
                    df_filtrado["DS_TIPO_UNIDADE"]
                    .dropna()
                    .astype(str)
                    .unique()
                )

                tipo_escolhido = st.selectbox(
                    "Tipo de Unidade:",
                    ["TODOS"] + tipos,
                    key="leitos_tipo",
                )

                if tipo_escolhido != "TODOS":

                    df_filtrado = df_filtrado[
                        df_filtrado[
                            "DS_TIPO_UNIDADE"
                        ].astype(str)
                        == tipo_escolhido
                    ]

            # -------------------------------------------------
            # BUSCA
            # -------------------------------------------------

            busca_estabelecimento = st.text_input(
                "Buscar Estabelecimento:",
                placeholder="Digite o nome...",
                key="leitos_busca",
            )

            if (
                busca_estabelecimento
                and "NOME_ESTABELECIMENTO"
                in df_filtrado.columns
            ):

                df_filtrado = df_filtrado[
                    df_filtrado[
                        "NOME_ESTABELECIMENTO"
                    ]
                    .astype(str)
                    .str.contains(
                        busca_estabelecimento,
                        case=False,
                        na=False,
                    )
                ]

        # =====================================================
        # CABEÇALHO
        # =====================================================

        st.title("Gestão de Leitos Hospitalares")

        st.caption(
            "Consulta avançada e interativa de infraestrutura "
            "hospitalar e redes credenciadas no SUS."
        )

        # =====================================================
        # EXPORTAÇÃO
        # =====================================================

        csv_data = converter_df_para_csv(
            df_filtrado
        )

        st.download_button(
            label="📥 Exportar Dados Filtrados",
            data=csv_data,
            file_name="leitos_hospitalares_filtrados.csv",
            mime="text/csv",
            use_container_width=False,
            key="btn_exp_leitos",
        )

        st.markdown("")

        # =====================================================
        # KPIs
        # =====================================================

        total_estabelecimentos = len(
            df_filtrado
        )

        total_leitos = 0

        if "LEITOS_EXISTENTES" in df_filtrado.columns:

            total_leitos = int(
                df_filtrado[
                    "LEITOS_EXISTENTES"
                ].sum()
            )

        total_sus = 0

        if "LEITOS_SUS" in df_filtrado.columns:

            total_sus = int(
                df_filtrado[
                    "LEITOS_SUS"
                ].sum()
            )

        total_uti = 0

        if "UTI_TOTAL_EXIST" in df_filtrado.columns:

            total_uti = int(
                df_filtrado[
                    "UTI_TOTAL_EXIST"
                ].sum()
            )

        percentual_sus = (
            total_sus / total_leitos * 100
            if total_leitos > 0
            else 0
        )

        m1, m2, m3, m4 = st.columns(4)

        with m1:

            st.metric(
                label="🏥 Unidades Filtradas",
                value=f"{total_estabelecimentos:,}".replace(
                    ",", "."
                ),
                help="Quantidade de unidades de saúde encontradas.",
            )

        with m2:

            st.metric(
                label="🛏️ Total de Leitos",
                value=f"{total_leitos:,}".replace(
                    ",", "."
                ),
                help="Quantidade total de leitos cadastrados.",
            )

        with m3:

            st.metric(
                label="🤝 Leitos SUS",
                value=f"{total_sus:,}".replace(
                    ",", "."
                ),
                delta=f"{percentual_sus:.1f}% da rede",
                delta_color="normal",
            )

        with m4:

            st.metric(
                label="🚨 Leitos UTI",
                value=f"{total_uti:,}".replace(
                    ",", "."
                ),
                help="Quantidade total de leitos de UTI cadastrados.",
            )

        st.markdown("")

        # =====================================================
        # TABELA
        # =====================================================

        st.subheader(
            "📋 Tabela Detalhada de Unidades Hospitalares"
        )

        colunas_exibir = [
            coluna
            for coluna in [
                "NOME_ESTABELECIMENTO",
                "MUNICIPIO",
                "UF",
                "LEITOS_EXISTENTES",
                "LEITOS_SUS",
                "UTI_TOTAL_EXIST",
                "UTI_TOTAL_SUS",
                "DS_TIPO_UNIDADE",
            ]
            if coluna in df_filtrado.columns
        ]

        if not df_filtrado.empty:

            df_tabela = df_filtrado[
                colunas_exibir
            ].copy()

            if "LEITOS_EXISTENTES" in df_tabela.columns:

                df_tabela = df_tabela.sort_values(
                    by="LEITOS_EXISTENTES",
                    ascending=False,
                )

            configuracao_colunas = {}

            if "NOME_ESTABELECIMENTO" in df_tabela.columns:

                configuracao_colunas[
                    "NOME_ESTABELECIMENTO"
                ] = st.column_config.TextColumn(
                    "Hospital / Estabelecimento",
                    width="large",
                )

            if "MUNICIPIO" in df_tabela.columns:

                configuracao_colunas[
                    "MUNICIPIO"
                ] = st.column_config.TextColumn(
                    "Município",
                    width="medium",
                )

            if "UF" in df_tabela.columns:

                configuracao_colunas[
                    "UF"
                ] = st.column_config.TextColumn(
                    "UF",
                    width="small",
                )

            if "LEITOS_EXISTENTES" in df_tabela.columns:

                max_leitos = int(
                    df_tabela[
                        "LEITOS_EXISTENTES"
                    ].max()
                )

                if max_leitos <= 0:
                    max_leitos = 1

                configuracao_colunas[
                    "LEITOS_EXISTENTES"
                ] = st.column_config.ProgressColumn(
                    "Total de Leitos",
                    format="%d",
                    min_value=0,
                    max_value=max_leitos,
                )

            if "LEITOS_SUS" in df_tabela.columns:

                configuracao_colunas[
                    "LEITOS_SUS"
                ] = st.column_config.NumberColumn(
                    "Leitos SUS",
                    format="%d",
                )

            if "UTI_TOTAL_EXIST" in df_tabela.columns:

                configuracao_colunas[
                    "UTI_TOTAL_EXIST"
                ] = st.column_config.NumberColumn(
                    "UTI Total",
                    format="%d",
                )

            if "UTI_TOTAL_SUS" in df_tabela.columns:

                configuracao_colunas[
                    "UTI_TOTAL_SUS"
                ] = st.column_config.NumberColumn(
                    "UTI SUS",
                    format="%d",
                )

            if "DS_TIPO_UNIDADE" in df_tabela.columns:

                configuracao_colunas[
                    "DS_TIPO_UNIDADE"
                ] = st.column_config.TextColumn(
                    "Tipo de Unidade",
                    width="medium",
                )

            st.dataframe(
                df_tabela,
                column_config=configuracao_colunas,
                use_container_width=True,
                hide_index=True,
                height=400,
            )

        else:

            st.warning(
                "Nenhum estabelecimento encontrado "
                "com os filtros selecionados."
            )

        # =====================================================
        # GRÁFICOS
        # =====================================================

        if not df_filtrado.empty and total_leitos > 0:

            st.markdown("")

            col_esquerda, col_direita = st.columns(2)

            # =================================================
            # PERFIL DAS UTIs
            # =================================================

            with col_esquerda:

                st.subheader(
                    "🚨 Perfil de Leitos de UTI"
                )

                colunas_uti = {

                    "UTI Adulto":
                        "UTI_ADULTO_EXIST",

                    "UTI Pediátrica":
                        "UTI_PEDIATRICO_EXIST",

                    "UTI Neonatal":
                        "UTI_NEONATAL_EXIST",

                    "UTI Queimados":
                        "UTI_QUEIMADO_EXIST",

                    "UTI Coronariana":
                        "UTI_CORONARIANA_EXIST",
                }

                nomes_uti = []
                valores_uti = []

                for nome, coluna in colunas_uti.items():

                    if coluna in df_filtrado.columns:

                        valor = int(
                            df_filtrado[
                                coluna
                            ].sum()
                        )

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
                                    ",", "."
                                )
                                for valor in valores_uti
                            ],
                            textposition="auto",
                        )
                    )

                    fig_uti.update_layout(

                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",

                        font=dict(
                            color="#ffffff",
                            size=12,
                        ),

                        margin=dict(
                            l=20,
                            r=20,
                            t=20,
                            b=20,
                        ),

                        height=320,

                        xaxis=dict(
                            showgrid=False,
                            visible=False,
                        ),

                        yaxis=dict(
                            showgrid=False,
                            autorange="reversed",
                        ),
                    )

                    st.plotly_chart(
                        fig_uti,
                        use_container_width=True,
                    )

                else:

                    st.info(
                        "Nenhum leito de UTI específico "
                        "foi detalhado na seleção atual."
                    )

            # =================================================
            # SUS VS PRIVADO
            # =================================================

            with col_direita:

                st.subheader(
                    "🤝 Proporção SUS vs Privado"
                )

                outros_leitos = max(
                    0,
                    total_leitos - total_sus,
                )

                df_pie = pd.DataFrame(
                    {
                        "Categoria": [
                            "Leitos SUS",
                            "Privado / Outros",
                        ],
                        "Quantidade": [
                            total_sus,
                            outros_leitos,
                        ],
                    }
                )

                fig_pie = px.pie(
                    df_pie,
                    values="Quantidade",
                    names="Categoria",
                    hole=0.65,
                    color_discrete_sequence=[
                        "#10b981",
                        "#3b82f6",
                    ],
                )

                fig_pie.update_traces(
                    textinfo="percent",
                    textfont_size=14,
                    textfont_color="white",
                )

                fig_pie.update_layout(

                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",

                    font=dict(
                        color="#ffffff",
                        size=13,
                    ),

                    margin=dict(
                        l=20,
                        r=20,
                        t=20,
                        b=20,
                    ),

                    height=320,

                    showlegend=True,

                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.15,
                        xanchor="center",
                        x=0.5,
                        font=dict(
                            color="#9ca3af"
                        ),
                    ),
                )

                st.plotly_chart(
                    fig_pie,
                    use_container_width=True,
                )