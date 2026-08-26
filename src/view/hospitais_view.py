import streamlit as st
import plotly.graph_objects as go


class HospitaisView:

    # =========================================================
    # RENDER PRINCIPAL
    # =========================================================
    def render(self, model):

        st.title("🏥 Hospitais")

        st.caption(
            "Consulte e explore as unidades hospitalares cadastradas na plataforma."
        )

        self._aplicar_estilos()

        # 5 indicadores
        self._render_indicadores()

        st.write("")

        # 3 gráficos
        self._render_graficos()

        st.write("")

        # Tabela + hospitais por porte
        self._render_tabela_e_porte()


    # =========================================================
    # ESTILOS
    # =========================================================
    def _aplicar_estilos(self):

        st.markdown("""
        <style>

        .card-indicador {
            background-color: #071426;
            border: 1px solid #162840;
            border-radius: 10px;
            padding: 16px;
            min-height: 120px;
        }

        .titulo-indicador {
            font-size: 14px;
            color: #D7DCE5;
            margin-bottom: 5px;
            white-space: nowrap;
        }

        .valor-indicador {
            font-size: 28px;
            font-weight: 600;
            color: #FFFFFF;
            margin-bottom: 8px;
        }

        .variacao {
            font-size: 12px;
            white-space: nowrap;
        }

        .aumento {
            color: #00E676;
            font-weight: 600;
        }

        .queda {
            color: #FF3B5C;
            font-weight: 600;
        }

        .periodo {
            color: #9AA4B2;
            font-weight: 400;
        }

        </style>
        """, unsafe_allow_html=True)


    # =========================================================
    # 5 INDICADORES
    # =========================================================
    def _render_indicadores(self):

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                label="🏥 Total de hospitais",
                value="1.642",
                delta="3,6% vs período anterior"
            )

        with col2:
            st.metric(
                label="🛡️ Hospitais ativos",
                value="1.523",
                delta="4,1% vs período anterior"
            )

        with col3:
            st.metric(
                label="🛏️ Leitos totais",
                value="245.781",
                delta="5,8% vs período anterior"
            )

        with col4:
            st.metric(
                label="➕ Leitos SUS",
                value="168.342",
                delta="6,2% vs período anterior"
            )

        with col5:
            st.metric(
                label="📈 Taxa de ocupação média",
                value="78%",
                delta="-0,7 p.p. vs período anterior"
            )


    # =========================================================
    # 3 GRÁFICOS
    # =========================================================
    def _render_graficos(self):

        grafico1, grafico2, grafico3 = st.columns(
            [1, 1.1, 1.8],
            gap="medium"
        )

        # =====================================================
        # GRÁFICO 1 - TIPO DE GESTÃO
        # =====================================================
        with grafico1:

            st.markdown("#### Hospitais por tipo de gestão")

            fig_gestao = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "Público",
                            "Privado",
                            "Filantrópico"
                        ],
                        values=[
                            55,
                            35,
                            10
                        ],
                        hole=0.60,
                        marker=dict(
                            colors=[
                                "#006EFF",
                                "#6A18FF",
                                "#E73BAE"
                            ]
                        ),
                        textinfo="none",
                        hovertemplate=(
                            "<b>%{label}</b><br>"
                            "%{value}%"
                            "<extra></extra>"
                        )
                    )
                ]
            )

            fig_gestao.add_annotation(
                text="<b>1.642</b><br>Total",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(
                    size=16,
                    color="white"
                )
            )

            fig_gestao.update_layout(
                height=270,
                margin=dict(
                    l=0,
                    r=0,
                    t=5,
                    b=5
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="white"
                ),
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=0.92,
                    font=dict(
                        size=11,
                        color="#D7DCE5"
                    )
                ),
                showlegend=True
            )

            st.plotly_chart(
                fig_gestao,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

            st.markdown(
                """
                <span style="
                    color:#A855F7;
                    font-size:13px;
                ">
                    Ver detalhes →
                </span>
                """,
                unsafe_allow_html=True
            )

        # =====================================================
        # GRÁFICO 2 - HOSPITAIS POR REGIÃO
        # =====================================================
        with grafico2:

            st.markdown("#### Hospitais por região")

            regioes = [
                "Sudeste",
                "Nordeste",
                "Sul",
                "Norte",
                "Centro-Oeste"
            ]

            valores = [
                642,
                478,
                281,
                156,
                85
            ]

            textos = [
                "642 (39%)",
                "478 (29%)",
                "281 (17%)",
                "156 (9%)",
                "85 (5%)"
            ]

            fig_regiao = go.Figure()

            fig_regiao.add_trace(
                go.Bar(
                    x=valores,
                    y=regioes,
                    orientation="h",
                    text=textos,
                    textposition="outside",
                    cliponaxis=False,
                    marker=dict(
                        color="#7424FF"
                    ),
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Hospitais: %{x}"
                        "<extra></extra>"
                    )
                )
            )

            fig_regiao.update_layout(
                height=270,

                margin=dict(
                    l=0,
                    r=70,
                    t=5,
                    b=5
                ),

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    color="#D7DCE5"
                ),

                xaxis=dict(
                    visible=False,
                    range=[0, 750]
                ),

                yaxis=dict(
                    autorange="reversed",
                    showgrid=False,
                    tickfont=dict(
                        size=11,
                        color="#D7DCE5"
                    )
                ),

                bargap=0.60,
                showlegend=False
            )

            st.plotly_chart(
                fig_regiao,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

            st.markdown(
                """
                <span style="
                    color:#A855F7;
                    font-size:13px;
                ">
                    Ver todas as regiões →
                </span>
                """,
                unsafe_allow_html=True
            )

        # =====================================================
        # GRÁFICO 3 - EVOLUÇÃO
        # =====================================================
        with grafico3:

            titulo_col, periodo_col = st.columns(
                [4, 1.2]
            )

            with titulo_col:
                st.markdown(
                    "#### Evolução do número de hospitais"
                )

            with periodo_col:
                st.selectbox(
                    "Período",
                    ["Mensal"],
                    label_visibility="collapsed",
                    key="periodo_hospitais"
                )

            datas = [
                "01/04",
                "04/04",
                "07/04",
                "10/04",
                "13/04",
                "16/04",
                "19/04",
                "22/04",
                "25/04",
                "28/04",
                "01/05",
                "04/05",
                "07/05",
                "10/05",
                "13/05",
                "16/05",
                "19/05",
                "22/05",
                "25/05",
                "27/05",
                "29/05",
                "31/05",
                "03/06"
            ]

            hospitais = [
                350,
                430,
                420,
                470,
                550,
                540,
                590,
                720,
                770,
                820,
                860,
                900,
                950,
                1120,
                1160,
                1200,
                1250,
                1300,
                1280,
                1550,
                1650,
                1500,
                1380
            ]

            fig_evolucao = go.Figure()

            fig_evolucao.add_trace(
                go.Scatter(
                    x=datas,
                    y=hospitais,

                    mode="lines+markers",

                    line=dict(
                        color="#8A2EFF",
                        width=3
                    ),

                    marker=dict(
                        size=5,
                        color="#A855F7",
                        line=dict(
                            width=1,
                            color="#D8B4FE"
                        )
                    ),

                    fill="tozeroy",

                    fillcolor="rgba(124,22,255,0.22)",

                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Hospitais: %{y}"
                        "<extra></extra>"
                    )
                )
            )

            fig_evolucao.update_layout(
                height=270,

                margin=dict(
                    l=10,
                    r=10,
                    t=5,
                    b=5
                ),

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    color="#D7DCE5",
                    size=11
                ),

                xaxis=dict(
                    showgrid=False,
                    tickmode="array",

                    tickvals=[
                        "01/04",
                        "07/04",
                        "13/04",
                        "19/04",
                        "25/04",
                        "01/05",
                        "07/05",
                        "13/05",
                        "19/05",
                        "25/05",
                        "03/06"
                    ],

                    tickfont=dict(
                        color="#AAB2C0"
                    ),

                    zeroline=False
                ),

                yaxis=dict(
                    range=[0, 1800],

                    tickvals=[
                        0,
                        300,
                        600,
                        900,
                        1200,
                        1500,
                        1800
                    ],

                    ticktext=[
                        "0",
                        "300",
                        "600",
                        "900",
                        "1,2 mil",
                        "1,5 mil",
                        "1,8 mil"
                    ],

                    gridcolor="rgba(100,120,150,0.15)",

                    zeroline=False,

                    tickfont=dict(
                        color="#AAB2C0"
                    )
                ),

                showlegend=False
            )

            st.plotly_chart(
                fig_evolucao,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )


    # =========================================================
    # TABELA + HOSPITAIS POR PORTE
    # =========================================================
    def _render_tabela_e_porte(self):

        coluna_tabela, coluna_porte = st.columns(
            [3.2, 1.25],
            gap="medium"
        )

        # =====================================================
        # TABELA DE HOSPITAIS
        # =====================================================
        with coluna_tabela:

            st.markdown("#### Hospitais")

            # Busca visual
            busca = st.text_input(
                "Buscar hospital",
                placeholder="🔎 Buscar hospital, CNES ou município...",
                label_visibility="collapsed",
                key="busca_hospital"
            )

            # Dados fictícios para o protótipo
            hospitais_tabela = [
                {
                    "Hospital": "Hospital das Clínicas",
                    "CNES": "2078656",
                    "Município": "São Paulo",
                    "UF": "SP",
                    "Gestão": "Público",
                    "Tipo": "Geral",
                    "Leitos totais": 1204,
                    "Leitos SUS": 1020,
                    "UTI Adulto": 152,
                    "Taxa de ocupação": "82%"
                },
                {
                    "Hospital": "Santa Casa de Misericórdia",
                    "CNES": "2098765",
                    "Município": "Rio de Janeiro",
                    "UF": "RJ",
                    "Gestão": "Filantrópico",
                    "Tipo": "Geral",
                    "Leitos totais": 890,
                    "Leitos SUS": 720,
                    "UTI Adulto": 90,
                    "Taxa de ocupação": "76%"
                },
                {
                    "Hospital": "Hospital Moinhos de Vento",
                    "CNES": "2223344",
                    "Município": "Porto Alegre",
                    "UF": "RS",
                    "Gestão": "Privado",
                    "Tipo": "Geral",
                    "Leitos totais": 566,
                    "Leitos SUS": 310,
                    "UTI Adulto": 60,
                    "Taxa de ocupação": "74%"
                },
                {
                    "Hospital": "Hospital Geral de Fortaleza",
                    "CNES": "2321123",
                    "Município": "Fortaleza",
                    "UF": "CE",
                    "Gestão": "Público",
                    "Tipo": "Geral",
                    "Leitos totais": 798,
                    "Leitos SUS": 620,
                    "UTI Adulto": 80,
                    "Taxa de ocupação": "81%"
                },
                {
                    "Hospital": "Hospital Português",
                    "CNES": "2675432",
                    "Município": "Salvador",
                    "UF": "BA",
                    "Gestão": "Privado",
                    "Tipo": "Geral",
                    "Leitos totais": 432,
                    "Leitos SUS": 200,
                    "UTI Adulto": 40,
                    "Taxa de ocupação": "69%"
                }
            ]

            # Filtro simples para a busca funcionar
            if busca:

                busca_lower = busca.lower()

                hospitais_tabela = [
                    hospital
                    for hospital in hospitais_tabela
                    if (
                        busca_lower in hospital["Hospital"].lower()
                        or busca_lower in hospital["CNES"].lower()
                        or busca_lower in hospital["Município"].lower()
                    )
                ]

            st.dataframe(
                hospitais_tabela,
                use_container_width=True,
                hide_index=True,
                height=250
            )

            rodape1, rodape2 = st.columns([2, 1])

            with rodape1:
                st.markdown(
                    """
                    <span style="
                        color:#A855F7;
                        font-size:13px;
                    ">
                        Ver todos os hospitais →
                    </span>
                    """,
                    unsafe_allow_html=True
                )

            with rodape2:
                st.caption("1–5 de 1.642")


        # =====================================================
        # GRÁFICO PEQUENO - HOSPITAIS POR PORTE
        # =====================================================
        with coluna_porte:

            st.markdown(
                "#### Hospitais por porte"
            )

            st.caption(
                "Número de leitos"
            )

            portes = [
                "Pequeno",
                "Médio",
                "Grande",
                "Extra-grande"
            ]

            valores_porte = [
                214,
                356,
                612,
                460
            ]

            textos_porte = [
                "214 (13%)",
                "356 (22%)",
                "612 (37%)",
                "460 (28%)"
            ]

            fig_porte = go.Figure()

            fig_porte.add_trace(
                go.Bar(
                    x=valores_porte,
                    y=portes,

                    orientation="h",

                    text=textos_porte,
                    textposition="outside",

                    cliponaxis=False,

                    marker=dict(
                        color="#7424FF"
                    ),

                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Hospitais: %{x}"
                        "<extra></extra>"
                    )
                )
            )

            fig_porte.update_layout(
                height=285,

                margin=dict(
                    l=0,
                    r=75,
                    t=5,
                    b=5
                ),

                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    color="#D7DCE5"
                ),

                xaxis=dict(
                    visible=False,
                    range=[0, 700]
                ),

                yaxis=dict(
                    autorange="reversed",
                    showgrid=False,

                    tickfont=dict(
                        size=10,
                        color="#D7DCE5"
                    )
                ),

                bargap=0.60,

                showlegend=False
            )

            st.plotly_chart(
                fig_porte,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

            st.markdown(
                """
                <span style="
                    color:#A855F7;
                    font-size:13px;
                ">
                    Ver detalhes →
                </span>
                """,
                unsafe_allow_html=True
            )