import pandas as pd
import plotly.express as px
import streamlit as st

# Import relativo mantendo o padrão da aplicação
from model.data_loader import carregar_dados_ultimo_mes

# ==========================================================
# FUNÇÃO COM CACHE PARA PROCESSAMENTO DE DADOS
# ==========================================================
@st.cache_data(show_spinner=False)
def preparar_dados(df_int):
    if df_int is None or df_int.empty:
        return pd.DataFrame()

    # Limpeza rigorosa nos nomes das colunas
    df_int.columns = (
        df_int.columns.astype(str)
        .str.replace("ï»¿", "", regex=False)
        .str.replace('"', "", regex=False)
        .str.strip()
    )

    # Mapeamento do Código IBGE para a Sigla da UF
    MAPA_CODIGO_UF = {
        11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
        21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL",
        28: "SE", 29: "BA", 31: "MG", 32: "ES", 33: "RJ", 35: "SP", 41: "PR",
        42: "SC", 43: "RS", 50: "MS", 51: "MT", 52: "GO", 53: "DF"
    }

    if "CODIGO_UF" in df_int.columns:
        df_int["CODIGO_UF_NUM"] = pd.to_numeric(df_int["CODIGO_UF"], errors="coerce").fillna(0).astype(int)
        df_int["UF"] = df_int["CODIGO_UF_NUM"].map(MAPA_CODIGO_UF).fillna("Outros")
    else:
        df_int["UF"] = "Outros"

    meses_cols = [
        "2025/Jan", "2025/Fev", "2025/Mar", "2025/Abr",
        "2025/Mai", "2025/Jun", "2025/Jul", "2025/Ago",
        "2025/Set", "2025/Out", "2025/Nov", "2025/Dez",
    ]
    cols_meses_presentes = [c for c in meses_cols if c in df_int.columns]

    # Tratamento numérico para meses e Total
    for col in cols_meses_presentes:
        df_int[col] = (
            df_int[col]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
            .replace("-", "0")
        )
        df_int[col] = pd.to_numeric(df_int[col], errors="coerce").fillna(0)

    if "Total" in df_int.columns:
        df_int["Total"] = (
            df_int["Total"]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .str.strip()
            .replace("-", "0")
        )
        df_int["Total"] = pd.to_numeric(df_int["Total"], errors="coerce").fillna(0)
    elif cols_meses_presentes:
        df_int["Total"] = df_int[cols_meses_presentes].sum(axis=1)

    return df_int, cols_meses_presentes


class InternacoesView:

    def render(self, model=None):
        # ==========================================================
        # 0. CSS CUSTOMIZADO (ATUALIZADO)
        # ==========================================================
        st.markdown(
            """
            <style>
            /* Fundo da Tabela */
            [data-testid="stDataFrame"] {
                background: rgba(18, 24, 38, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 12px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            }
            /* Forçar a cor roxa na ProgressColumn da Tabela */
            [data-testid="stProgress"] > div > div {
                background-color: #a855f7 !important;
            }
            /* Melhor contraste para os cartões KPI */
            .kpi-card {
                background: #1e293b; 
                border: 1px solid rgba(255, 255, 255, 0.15); 
                border-radius: 14px; 
                padding: 20px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            /* Bordas arredondadas e fundo padronizado para os Gráficos Plotly */
            [data-testid="stPlotlyChart"] {
                background: rgba(18, 24, 38, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 16px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            }
            </style>
        """,
            unsafe_allow_html=True,
        )

        # ==========================================================
        # 1. CARREGAMENTO E TRATAMENTO DOS DADOS (CACHE)
        # ==========================================================
        df_raw = carregar_dados_ultimo_mes("internacoes.csv")
        
        if df_raw is None or df_raw.empty:
            st.error("⚠️ O arquivo `internacoes.csv` não foi encontrado na pasta de dados ou está vazio.")
            return

        df_int, cols_meses_presentes = preparar_dados(df_raw)
        col_mun = "MUNICIPIO" if "MUNICIPIO" in df_int.columns else None

        UFS_BRASIL = [
            "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA",
            "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN",
            "RO", "RR", "RS", "SC", "SE", "SP", "TO"
        ]
        
        meses_nomes = {
            "2025/Jan": "Jan", "2025/Fev": "Fev", "2025/Mar": "Mar",
            "2025/Abr": "Abr", "2025/Mai": "Mai", "2025/Jun": "Jun",
            "2025/Jul": "Jul", "2025/Ago": "Ago", "2025/Set": "Set",
            "2025/Out": "Out", "2025/Nov": "Nov", "2025/Dez": "Dez",
        }

        # ==========================================================
        # 2. CABEÇALHO DA PÁGINA
        # ==========================================================
        col_title, col_export = st.columns([3, 1])

        with col_title:
            st.markdown(
                """
                <h1 style="margin: 0; font-size: 32px; font-weight: 800; color: #ffffff;">Gestão de <span style="color: #a855f7;">Internações Hospitalares</span></h1>
                <p style="margin: 6px 0 0 0; font-size: 15px; color: #9ca3af;">Acompanhe a distribuição e a evolução das internações hospitalares do SUS em 2025.</p>
            """,
                unsafe_allow_html=True,
            )

        with col_export:
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.download_button(
                "📥 Exportar dados",
                data=df_int.to_csv(index=False, sep=";", encoding="utf-8-sig"),
                file_name="internacoes_2025.csv",
                mime="text/csv",
                use_container_width=True,
                key="btn_exp_internacoes_v7",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ==========================================================
        # 3. FILTROS EXATOS (UFs DO BRASIL)
        # ==========================================================
        col_uf_filter, col_mun_filter = st.columns(2)

        with col_uf_filter:
            uf_selecionada = st.selectbox("Selecione a UF:", options=["TODOS"] + UFS_BRASIL, index=0, key="filtro_uf_v7")

        df_estado = df_int[df_int["UF"] == uf_selecionada].copy() if uf_selecionada != "TODOS" else df_int.copy()

        lista_municipios = []
        if col_mun:
            lista_municipios = sorted(df_estado[col_mun].dropna().astype(str).str.strip().unique().tolist())

        with col_mun_filter:
            municipio_selecionado = st.selectbox("Selecione o Município:", options=["TODOS"] + lista_municipios, index=0, key="filtro_mun_v7")

        df_filtrado = df_estado.copy()
        if municipio_selecionado != "TODOS" and col_mun:
            df_filtrado = df_filtrado[df_filtrado[col_mun].astype(str).str.strip() == municipio_selecionado]

        st.markdown("<br>", unsafe_allow_html=True)

        # ==========================================================
        # 4. KPIS E RESUMO
        # ==========================================================
        texto_selecao = "Brasil" if uf_selecionada == "TODOS" and municipio_selecionado == "TODOS" else (uf_selecionada if municipio_selecionado == "TODOS" else municipio_selecionado)
        st.caption(f"Exibindo dados de: **{texto_selecao}**")

        total_geral = df_filtrado["Total"].sum() if "Total" in df_filtrado.columns else 0
        total_municipios = len(df_filtrado)
        media_municipio = total_geral / total_municipios if total_municipios > 0 else 0

        k1, k2, k3 = st.columns(3)

        with k1:
            st.markdown(f"""
                <div class="kpi-card">
                    <p style="color: #9ca3af; font-size: 14px; margin: 0;">Internações em 2025</p>
                    <h2 style="margin: 6px 0; font-size: 28px; font-weight: 800; color: #ffffff;">{total_geral:,.0f}</h2>
                </div>
            """.replace(",", "."), unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
                <div class="kpi-card">
                    <p style="color: #9ca3af; font-size: 14px; margin: 0;">Municípios</p>
                    <h2 style="margin: 6px 0; font-size: 28px; font-weight: 800; color: #ffffff;">{total_municipios:,}</h2>
                </div>
            """.replace(",", "."), unsafe_allow_html=True)

        with k3:
            st.markdown(f"""
                <div class="kpi-card">
                    <p style="color: #9ca3af; font-size: 14px; margin: 0;">Média por Município</p>
                    <h2 style="margin: 6px 0; font-size: 28px; font-weight: 800; color: #ffffff;">{media_municipio:,.0f}</h2>
                </div>
            """.replace(",", "."), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ==========================================================
        # 5. GRÁFICOS ANALÍTICOS
        # ==========================================================
        col_evolucao, col_top = st.columns([1.6, 1])

        with col_evolucao:
            st.markdown("<h3 style='font-size: 18px; font-weight: 700; color: #ffffff; padding-left: 10px;'>📈 Evolução Mensal</h3>", unsafe_allow_html=True)

            if cols_meses_presentes:
                soma_meses = df_filtrado[cols_meses_presentes].sum().reset_index()
                soma_meses.columns = ["Mês", "Internações"]
                soma_meses["Mês"] = soma_meses["Mês"].map(meses_nomes)

                fig_line = px.line(soma_meses, x="Mês", y="Internações", markers=True)
                fig_line.update_traces(line=dict(color="#a855f7", width=3), marker=dict(size=7))
                
                # Fundo transparente no Plotly para o CSS do Streamlit aparecer
                fig_line.update_layout(
                    height=320, 
                    paper_bgcolor="rgba(0,0,0,0)", 
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ffffff"), 
                    margin=dict(l=15, r=15, t=20, b=15),
                    xaxis=dict(showgrid=False, title=None), 
                    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", title=None),
                    hovermode="x unified"
                )
                st.plotly_chart(fig_line, use_container_width=True)

        with col_top:
            st.markdown("<h3 style='font-size: 18px; font-weight: 700; color: #ffffff; padding-left: 10px;'>🏆 Top 5 Municípios</h3>", unsafe_allow_html=True)

            if not df_filtrado.empty and "Total" in df_filtrado.columns and col_mun:
                df_top = df_filtrado.nlargest(5, "Total").sort_values("Total")

                if len(df_top) >= 1:
                    fig_bar = px.bar(df_top, x="Total", y=col_mun, orientation="h", text="Total")
                    
                    # Alteração aqui: textfont color definido para preto (#000000)
                    fig_bar.update_traces(
                        marker_color="#a855f7", 
                        texttemplate="%{text:,.0f}", 
                        textposition="auto",
                        textfont=dict(color="#000000", size=13, weight="bold")
                    )
                    
                    # Fundo transparente para herdar o card arredondado do CSS
                    fig_bar.update_layout(
                        height=320, 
                        paper_bgcolor="rgba(0,0,0,0)", 
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#ffffff"), 
                        margin=dict(l=15, r=15, t=20, b=15),
                        xaxis=dict(showgrid=False, title=None), 
                        yaxis=dict(showgrid=False, title=None)
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Não existem dados para a seleção atual.")

        # ==========================================================
        # 6. TABELA DETALHADA
        # ==========================================================
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div style="margin-bottom: 16px;">
                <h3 style="margin: 0; font-size: 20px; font-weight: 700; color: #ffffff;">📑 Tabela Detalhada de Internações Hospitalares</h3>
                <p style="margin: 4px 0 0 0; font-size: 14px; color: #9ca3af;">Exibição completa dos registros cadastrados de acordo com a seleção atual.</p>
            </div>
        """, unsafe_allow_html=True)

        if "Total" in df_filtrado.columns and not df_filtrado.empty:
            df_filtrado = df_filtrado.sort_values(by="Total", ascending=False)

        max_total_val = int(df_filtrado["Total"].max()) if "Total" in df_filtrado.columns and not df_filtrado.empty and df_filtrado["Total"].max() > 0 else 100
        column_config_dict = {}

        if col_mun:
            column_config_dict[col_mun] = st.column_config.TextColumn("Município", width="medium")

        column_config_dict["UF"] = st.column_config.TextColumn("UF", width="small")

        if "Total" in df_filtrado.columns:
            column_config_dict["Total"] = st.column_config.ProgressColumn(
                "Total de Internações", format="%d", min_value=0, max_value=max_total_val, width="medium"
            )

        for col_m in cols_meses_presentes:
            nome_amigavel = meses_nomes.get(col_m, col_m)
            column_config_dict[col_m] = st.column_config.NumberColumn(nome_amigavel, format="%d", width="small")

        colunas_ordem = [col_mun] if col_mun else []
        colunas_ordem.extend(["UF"])
        if "Total" in df_filtrado.columns:
            colunas_ordem.append("Total")
        colunas_ordem.extend(cols_meses_presentes)

        tabela = df_filtrado[colunas_ordem].copy()

        if not tabela.empty:
            st.dataframe(tabela, column_config=column_config_dict, use_container_width=True, hide_index=True, height=480)
        else:
            st.warning("⚠️ Nenhum registro encontrado com os filtros selecionados.")

        # ==========================================================
        # 7. RODAPÉ
        # ==========================================================
        st.caption("Fonte: Ministério da Saúde — DATASUS/SIH-SUS. Dados referentes ao ano de 2025.")