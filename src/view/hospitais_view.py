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

        # Estilos
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

        # -----------------------------------------------------
        # TOTAL DE HOSPITAIS
        # -----------------------------------------------------
        with col1:

            st.markdown("""
<div class="card-indicador">

<div class="titulo-indicador">
🏥 Total de hospitais
</div>

<div class="valor-indicador">
1.642
</div>

<div class="variacao">

<span class="aumento">
↑ 3,6%
</span>

<span class="periodo">
 vs período anterior
</span>

</div>

</div>
""", unsafe_allow_html=True)


        # -----------------------------------------------------
        # HOSPITAIS ATIVOS
        # -----------------------------------------------------
        with col2:

            st.markdown("""
<div class="card-indicador">

<div class="titulo-indicador">
🛡️ Hospitais ativos
</div>

<div class="valor-indicador">
1.523
</div>

<div class="variacao">

<span class="aumento">
↑ 4,1%
</span>

<span class="periodo">
 vs período anterior
</span>

</div>

</div>
""", unsafe_allow_html=True)


        # -----------------------------------------------------
        # LEITOS TOTAIS
        # -----------------------------------------------------
        with col3:

            st.markdown("""
<div class="card-indicador">

<div class="titulo-indicador">
🛏️ Leitos totais
</div>

<div class="valor-indicador">
245.781
</div>

<div class="variacao">

<span class="aumento">
↑ 5,8%
</span>

<span class="periodo">
 vs período anterior
</span>

</div>

</div>
""", unsafe_allow_html=True)


        # -----------------------------------------------------
        # LEITOS SUS
        # -----------------------------------------------------
        with col4:

            st.markdown("""
<div class="card-indicador">

<div class="titulo-indicador">
➕ Leitos SUS
</div>

<div class="valor-indicador">
168.342
</div>

<div class="variacao">

<span class="aumento">
↑ 6,2%
</span>

<span class="periodo">
 vs período anterior
</span>

</div>

</div>
""", unsafe_allow_html=True)


        # -----------------------------------------------------
        # TAXA DE OCUPAÇÃO
        # -----------------------------------------------------
        with col5:

            st.markdown("""
<div class="card-indicador">

<div class="titulo-indicador">
📈 Taxa de ocupação média
</div>

<div class="valor-indicador">
78%
</div>

<div class="variacao">

<span class="queda">
↓ 0,7 p.p.
</span>

<span class="periodo">
 vs período anterior
</span>

</div>

</div>
""", unsafe_allow_html=True)


    # =========================================================
    # 3 GRÁFICOS
    # =========================================================
    def _render_graficos(self):

        grafico1, grafico2, grafico3 = st.columns(
            [1, 1.1, 1.8],
            gap="medium"
        )


        # =====================================================
        # GRÁFICO 1
        # HOSPITAIS POR TIPO DE GESTÃO
        # =====================================================
        with grafico1:

            st.markdown(
                "#### Hospitais por tipo de gestão"
            )

            fig_gestao = go.Figure()

            fig_gestao.add_trace(
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
        # GRÁFICO 2
        # HOSPITAIS POR REGIÃO
        # =====================================================
        with grafico2:

            st.markdown(
                "#### Hospitais por região"
            )

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

                    range=[
                        0,
                        750
                    ]
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
        # GRÁFICO 3
        # EVOLUÇÃO DO NÚMERO DE HOSPITAIS
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

                    [
                        "Mensal"
                    ],

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

                    range=[
                        0,
                        1800
                    ],

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

        coluna_tabela, coluna_lateral = st.columns(
            [3.2, 1.25],
            gap="medium"
        )


        # =====================================================
        # TABELA DE HOSPITAIS
        # =====================================================
        with coluna_tabela:

            st.markdown("""
<div style="
background-color:#071426;
border:1px solid #162840;
border-radius:10px;
padding:15px;
">

<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:15px;
">

<div style="
font-size:17px;
font-weight:600;
color:#FFFFFF;
">
Hospitais
</div>

<div style="
background:#050F1E;
border:1px solid #1B2A42;
border-radius:7px;
padding:7px 12px;
font-size:11px;
color:#8F9BAD;
width:280px;
">
🔍 Buscar hospital, CNES, município...
</div>

</div>


<div style="
overflow-x:auto;
">


<table style="
width:100%;
border-collapse:collapse;
font-size:11px;
color:#D7DCE5;
min-width:900px;
">

<thead>

<tr style="
border-bottom:1px solid #172840;
color:#FFFFFF;
">

<th style="padding:10px;text-align:left;">
Hospital
</th>

<th style="padding:10px;text-align:left;">
CNES
</th>

<th style="padding:10px;text-align:left;">
Município
</th>

<th style="padding:10px;text-align:left;">
UF
</th>

<th style="padding:10px;text-align:left;">
Gestão
</th>

<th style="padding:10px;text-align:left;">
Tipo
</th>

<th style="padding:10px;text-align:center;">
Leitos totais
</th>

<th style="padding:10px;text-align:center;">
Leitos SUS
</th>

<th style="padding:10px;text-align:center;">
UTI Adulto
</th>

<th style="padding:10px;text-align:center;">
Taxa de ocupação
</th>

</tr>

</thead>


<tbody>


<tr style="border-bottom:1px solid #14233A;">

<td style="padding:12px;">
Hospital das Clínicas
</td>

<td style="padding:12px;">
2078656
</td>

<td style="padding:12px;">
São Paulo
</td>

<td style="padding:12px;">
SP
</td>

<td style="padding:12px;">
Público
</td>

<td style="padding:12px;">
Geral
</td>

<td style="padding:12px;text-align:center;">
1.204
</td>

<td style="padding:12px;text-align:center;">
1.020
</td>

<td style="padding:12px;text-align:center;">
152
</td>

<td style="padding:12px;text-align:center;">
82%
</td>

</tr>


<tr style="border-bottom:1px solid #14233A;">

<td style="padding:12px;">
Santa Casa de Misericórdia
</td>

<td style="padding:12px;">
2098765
</td>

<td style="padding:12px;">
Rio de Janeiro
</td>

<td style="padding:12px;">
RJ
</td>

<td style="padding:12px;">
Filantrópico
</td>

<td style="padding:12px;">
Geral
</td>

<td style="padding:12px;text-align:center;">
890
</td>

<td style="padding:12px;text-align:center;">
720
</td>

<td style="padding:12px;text-align:center;">
90
</td>

<td style="padding:12px;text-align:center;">
76%
</td>

</tr>


<tr style="border-bottom:1px solid #14233A;">

<td style="padding:12px;">
Hospital Moinhos de Vento
</td>

<td style="padding:12px;">
2223344
</td>

<td style="padding:12px;">
Porto Alegre
</td>

<td style="padding:12px;">
RS
</td>

<td style="padding:12px;">
Privado
</td>

<td style="padding:12px;">
Geral
</td>

<td style="padding:12px;text-align:center;">
566
</td>

<td style="padding:12px;text-align:center;">
310
</td>

<td style="padding:12px;text-align:center;">
60
</td>

<td style="padding:12px;text-align:center;">
74%
</td>

</tr>


<tr style="border-bottom:1px solid #14233A;">

<td style="padding:12px;">
Hospital Geral de Fortaleza
</td>

<td style="padding:12px;">
2321123
</td>

<td style="padding:12px;">
Fortaleza
</td>

<td style="padding:12px;">
CE
</td>

<td style="padding:12px;">
Público
</td>

<td style="padding:12px;">
Geral
</td>

<td style="padding:12px;text-align:center;">
798
</td>

<td style="padding:12px;text-align:center;">
620
</td>

<td style="padding:12px;text-align:center;">
80
</td>

<td style="padding:12px;text-align:center;">
81%
</td>

</tr>


<tr>

<td style="padding:12px;">
Hospital Português
</td>

<td style="padding:12px;">
2675432
</td>

<td style="padding:12px;">
Salvador
</td>

<td style="padding:12px;">
BA
</td>

<td style="padding:12px;">
Privado
</td>

<td style="padding:12px;">
Geral
</td>

<td style="padding:12px;text-align:center;">
432
</td>

<td style="padding:12px;text-align:center;">
200
</td>

<td style="padding:12px;text-align:center;">
40
</td>

<td style="padding:12px;text-align:center;">
69%
</td>

</tr>


</tbody>

</table>

</div>


<div style="
display:flex;
justify-content:space-between;
align-items:center;
margin-top:18px;
">

<div style="
color:#A855F7;
font-size:12px;
">
Ver todos os hospitais →
</div>


<div style="
color:#9AA4B2;
font-size:11px;
white-space:nowrap;
">

1–5 de 1.642

&nbsp;&nbsp;

‹

&nbsp;

<span style="
background:#6525E8;
padding:5px 8px;
border-radius:5px;
color:#FFFFFF;
">
1
</span>

&nbsp; 2 &nbsp; 3 &nbsp; ... &nbsp; 329 &nbsp; ›

</div>

</div>

</div>
""", unsafe_allow_html=True)


        # =====================================================
        # HOSPITAIS POR PORTE
        # =====================================================
        with coluna_lateral:

            st.markdown(
                "#### Hospitais por porte (nº de leitos)"
            )

            portes = [
                "Pequeno (até 50)",
                "Médio (51 a 150)",
                "Grande (151 a 500)",
                "Extra-grande (> 500)"
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

                    range=[
                        0,
                        700
                    ]
                ),

                yaxis=dict(

                    autorange="reversed",

                    showgrid=False,

                    tickfont=dict(
                        size=10,
                        color="#D7DCE5"
                    )
                ),

                bargap=0.65,

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