import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. Importa a função centralizada que pega apenas o último mês (ajustado sem 'src.')
from model.data_loader import carregar_dados_ultimo_mes


class LeitosView:

    def render(self, model=None):
        # =========================================================
        # CSS CUSTOMIZADO PARA REFINAR A TABELA E O DESIGN
        # =========================================================
        st.markdown(
            """
            <style>
            /* Customização do container do dataframe */
            [data-testid="stDataFrame"] {
                background: rgba(18, 24, 38, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 12px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        # =========================================================
        # CARREGAMENTO DOS DADOS (USANDO O DATA_LOADER PADRONIZADO)
        # =========================================================
        df = carregar_dados_ultimo_mes("leitos.csv")

        if df.empty:
            st.error(
                "⚠️ O arquivo `leitos.csv` não foi encontrado na pasta de dados."
            )
            return

        # =========================================================
        # CABEÇALHO DA TELA
        # =========================================================
        col_title, col_actions = st.columns([3, 1])
        with col_title:
            st.markdown(
                """
                <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: #ffffff;">Gestão de <span style="color: #3b82f6;">Leitos Hospitalares</span></h1>
                <p style="margin: 6px 0 0 0; font-size: 15px; color: #9ca3af;">Consulta avançada e interativa de infraestrutura hospitalar e redes credenciadas no SUS.</p>
            """,
                unsafe_allow_html=True,
            )

        with col_actions:
            st.markdown(
                "<div style='height: 12px;'></div>", unsafe_allow_html=True
            )
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Exportar Relatório",
                data=csv_data,
                file_name="leitos_hospitalares.csv",
                mime="text/csv",
                use_container_width=True,
                key="btn_exp_leitos",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # PAINEL DE FILTROS DEDICADO
        # =========================================================
        st.markdown(
            """
            <div style="background: rgba(18, 24, 38, 0.85); border: 1px solid rgba(168, 85, 247, 0.3); padding: 20px 24px; border-radius: 14px; margin-bottom: 24px;">
                <h3 style="margin: 0 0 14px 0; font-size: 17px; font-weight: 700; color: #a855f7; display: flex; align-items: center; gap: 8px;">
                    🎛️ Filtros da Base de Dados
                </h3>
            </div>
        """,
            unsafe_allow_html=True,
        )

        f_col1, f_col2, f_col3 = st.columns(3)

        ufs_disponiveis = (
            sorted(df["UF"].dropna().unique()) if "UF" in df.columns else []
        )
        uf_escolhida = f_col1.selectbox(
            "Selecione a UF:", options=["TODOS"] + ufs_disponiveis
        )

        df_filtrado = df.copy()
        if uf_escolhida != "TODOS":
            df_filtrado = df_filtrado[df_filtrado["UF"] == uf_escolhida]

        municipios_disponiveis = (
            sorted(df_filtrado["MUNICIPIO"].dropna().unique())
            if "MUNICIPIO" in df_filtrado.columns
            else []
        )
        mun_escolhido = f_col2.selectbox(
            "Selecione o Município:",
            options=["TODOS"] + municipios_disponiveis,
        )

        if mun_escolhido != "TODOS":
            df_filtrado = df_filtrado[
                df_filtrado["MUNICIPIO"] == mun_escolhido
            ]

        busca_estabelecimento = f_col3.text_input(
            "Nome do Estabelecimento:", placeholder="Digite para pesquisar..."
        )

        if (
            busca_estabelecimento
            and "NOME_ESTABELECIMENTO" in df_filtrado.columns
        ):
            df_filtrado = df_filtrado[
                df_filtrado["NOME_ESTABELECIMENTO"].str.contains(
                    busca_estabelecimento, case=False, na=False
                )
            ]

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # CARDS DE MÉTRICAS (KPIs)
        # =========================================================
        total_estabelecimentos = len(df_filtrado)
        total_leitos = (
            int(df_filtrado["LEITOS_EXISTENTES"].sum())
            if "LEITOS_EXISTENTES" in df_filtrado.columns
            else 0
        )
        total_sus = (
            int(df_filtrado["LEITOS_SUS"].sum())
            if "LEITOS_SUS" in df_filtrado.columns
            else 0
        )
        total_uti = (
            int(df_filtrado["UTI_TOTAL_EXIST"].sum())
            if "UTI_TOTAL_EXIST" in df_filtrado.columns
            else 0
        )

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.markdown(
                f"""
                <div class="metric-card" style="padding: 22px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <p style="color: #9ca3af; font-size: 14px; margin: 0; font-weight: 500;">Unidades Filtradas</p>
                            <h2 style="margin: 6px 0; font-size: 28px; font-weight: 800; color: #ffffff;">{total_estabelecimentos:,}</h2>
                            <p style="color: #9ca3af; font-size: 13px; margin: 0;">Unidades de saúde</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%); padding: 12px; border-radius: 12px; font-size: 20px;">🏥</div>
                    </div>
                </div>
            """.replace(
                    ",", "."
                ),
                unsafe_allow_html=True,
            )

        with m2:
            st.markdown(
                f"""
                <div class="metric-card" style="padding: 22px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <p style="color: #9ca3af; font-size: 14px; margin: 0; font-weight: 500;">Total de Leitos</p>
                            <h2 style="margin: 6px 0; font-size: 28px; font-weight: 800; color: #ffffff;">{total_leitos:,}</h2>
                            <p style="color: #9ca3af; font-size: 13px; margin: 0;">Capacidade cadastrada</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); padding: 12px; border-radius: 12px; font-size: 20px;">🛏️</div>
                    </div>
                </div>
            """.replace(
                    ",", "."
                ),
                unsafe_allow_html=True,
            )

        with m3:
            st.markdown(
                f"""
                <div class="metric-card" style="padding: 22px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <p style="color: #9ca3af; font-size: 14px; margin: 0; font-weight: 500;">Leitos SUS</p>
                            <h2 style="margin: 6px 0; font-size: 28px; font-weight: 800; color: #ffffff;">{total_sus:,}</h2>
                            <p style="color: #10b981; font-size: 13px; margin: 0; font-weight: 600;">{(total_sus/total_leitos*100 if total_leitos else 0):.1f}% da rede</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 12px; border-radius: 12px; font-size: 20px;">🤝</div>
                    </div>
                </div>
            """.replace(
                    ",", "."
                ),
                unsafe_allow_html=True,
            )

        with m4:
            st.markdown(
                f"""
                <div class="metric-card" style="padding: 22px;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <p style="color: #9ca3af; font-size: 14px; margin: 0; font-weight: 500;">Leitos UTI</p>
                            <h2 style="margin: 6px 0; font-size: 28px; font-weight: 800; color: #ffffff;">{total_uti:,}</h2>
                            <p style="color: #ef4444; font-size: 13px; margin: 0; font-weight: 600;">UTI Adulto/Pediátrico</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%); padding: 12px; border-radius: 12px; font-size: 20px;">🚨</div>
                    </div>
                </div>
            """.replace(
                    ",", "."
                ),
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # TABELA PRINCIPAL
        # =========================================================
        st.markdown(
            """
            <div style="margin-bottom: 16px;">
                <h3 style="margin: 0; font-size: 20px; font-weight: 700; color: #ffffff;">📋 Tabela Detalhada de Unidades Hospitalares</h3>
                <p style="margin: 4px 0 0 0; font-size: 14px; color: #9ca3af;">Exibição completa dos registros cadastrados de acordo com a seleção atual.</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

        colunas_exibir = [
            c
            for c in [
                "NOME_ESTABELECIMENTO",
                "MUNICIPIO",
                "UF",
                "LEITOS_EXISTENTES",
                "LEITOS_SUS",
                "UTI_TOTAL_EXIST",
                "UTI_TOTAL_SUS",
                "DS_TIPO_UNIDADE",
            ]
            if c in df_filtrado.columns
        ]

        if not df_filtrado.empty:
            # Ordena os dados em ordem decrescente pela coluna com a barra de progresso (LEITOS_EXISTENTES)
            df_tabela = df_filtrado[colunas_exibir].copy()
            if "LEITOS_EXISTENTES" in df_tabela.columns:
                df_tabela = df_tabela.sort_values(
                    by="LEITOS_EXISTENTES", ascending=False
                )

            st.dataframe(
                df_tabela,
                column_config={
                    "NOME_ESTABELECIMENTO": st.column_config.TextColumn(
                        "Hospital / Estabelecimento", width="large"
                    ),
                    "MUNICIPIO": st.column_config.TextColumn(
                        "Município", width="medium"
                    ),
                    "UF": st.column_config.TextColumn("UF", width="small"),
                    "LEITOS_EXISTENTES": st.column_config.ProgressColumn(
                        "Total de Leitos",
                        format="%d",
                        min_value=0,
                        max_value=(
                            int(df_filtrado["LEITOS_EXISTENTES"].max())
                            if "LEITOS_EXISTENTES" in df_filtrado.columns
                            else 100
                        ),
                    ),
                    "LEITOS_SUS": st.column_config.NumberColumn(
                        "Leitos SUS", format="%d"
                    ),
                    "UTI_TOTAL_EXIST": st.column_config.NumberColumn(
                        "UTI Total", format="%d"
                    ),
                    "UTI_TOTAL_SUS": st.column_config.NumberColumn(
                        "UTI SUS", format="%d"
                    ),
                    "DS_TIPO_UNIDADE": st.column_config.TextColumn(
                        "Tipo de Unidade", width="medium"
                    ),
                },
                use_container_width=True,
                hide_index=True,
                height=450,
            )
        else:
            st.warning(
                "⚠️ Nenhum estabelecimento encontrado com os filtros selecionados."
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # GRÁFICOS ANALÍTICOS (ABAIXO DA TABELA)
        # =========================================================
        if not df_filtrado.empty and total_leitos > 0:
            c_left, c_right = st.columns(2)

            outros_leitos = max(0, total_leitos - total_sus)

            # --- BARRAS HORIZONTAIS ---
            with c_left:
                categories = ["Leitos UTI", "Privado / Outros", "Leitos SUS"]
                values = [total_uti, outros_leitos, total_sus]
                percentages = [
                    (v / total_leitos * 100) if total_leitos else 0
                    for v in values
                ]

                labels = [
                    f"{v:,}".replace(",", ".") + f" ({p:.1f}%)"
                    for v, p in zip(values, percentages)
                ]

                fig_bar = go.Figure(
                    go.Bar(
                        x=values,
                        y=categories,
                        orientation="h",
                        text=labels,
                        textposition="inside",
                        insidetextanchor="start",
                        marker=dict(
                            color=["#ef4444", "#3b82f6", "#10b981"],
                            line=dict(color="rgba(0,0,0,0)", width=0),
                        ),
                    )
                )

                fig_bar.update_layout(
                    title=dict(
                        text="Distribuição Geral de Leitos",
                        font=dict(
                            color="#ffffff", size=16, family="sans-serif"
                        ),
                    ),
                    paper_bgcolor="rgba(18, 24, 38, 0.85)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ffffff", size=12),
                    margin=dict(l=20, r=20, t=50, b=20),
                    height=300,
                    xaxis=dict(showgrid=False, visible=False),
                    yaxis=dict(
                        showgrid=False,
                        tickfont=dict(color="#9ca3af", size=13),
                    ),
                )

                st.plotly_chart(fig_bar, use_container_width=True)

            # --- GRÁFICO DE ROSCA (DONUT) ---
            with c_right:
                df_pie = pd.DataFrame(
                    {
                        "Categoria": ["Leitos SUS", "Privado / Outros"],
                        "Quantidade": [total_sus, outros_leitos],
                    }
                )

                fig_pie = px.pie(
                    df_pie,
                    values="Quantidade",
                    names="Categoria",
                    hole=0.6,
                    color_discrete_sequence=["#10b981", "#3b82f6"],
                )

                fig_pie.update_layout(
                    title=dict(
                        text="Proporção SUS vs Privado",
                        font=dict(
                            color="#ffffff", size=16, family="sans-serif"
                        ),
                    ),
                    paper_bgcolor="rgba(18, 24, 38, 0.85)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ffffff", size=13),
                    margin=dict(l=20, r=20, t=50, b=20),
                    height=300,
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.1,
                        xanchor="center",
                        x=0.5,
                        font=dict(color="#9ca3af"),
                    ),
                )

                st.plotly_chart(fig_pie, use_container_width=True)