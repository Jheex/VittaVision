import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. Importa a função centralizada que pega apenas o último mês
from model.data_loader import carregar_dados_ultimo_mes

# Função com cache para evitar travamentos ao interagir com filtros
@st.cache_data(show_spinner=False)
def converter_df_para_csv(df_export):
    return df_export.to_csv(index=False).encode("utf-8")


class LeitosView:

    def render(self, model=None):
        # =========================================================
        # CSS CUSTOMIZADO
        # =========================================================
        st.markdown(
            """
            <style>
            /* Customização da Tabela */
            [data-testid="stDataFrame"] {
                background: rgba(18, 24, 38, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 12px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            }
            /* Customização dos Gráficos (Padronização com a Tabela e Cards) */
            [data-testid="stPlotlyChart"] {
                background: rgba(18, 24, 38, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 16px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            }
            /* Refinamento dos Cards para garantir alinhamento perfeito */
            .metric-card {
                background: rgba(18, 24, 38, 0.85);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 20px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                display: flex;
                justify-content: space-between;
                align-items: center;
                height: 100%;
            }
            .metric-info {
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .metric-icon {
                padding: 14px;
                border-radius: 12px;
                font-size: 22px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # =========================================================
        # CARREGAMENTO DOS DADOS
        # =========================================================
        df = carregar_dados_ultimo_mes("leitos.csv")

        if df.empty:
            st.error("⚠️ O arquivo `leitos.csv` não foi encontrado na pasta de dados.")
            return

        # Constante global para não distorcer a barra visual da tabela ao filtrar
        max_leitos_global = int(df["LEITOS_EXISTENTES"].max()) if "LEITOS_EXISTENTES" in df.columns else 100

        # =========================================================
        # FILTROS NA SIDEBAR (Libera a tela central)
        # =========================================================
        with st.sidebar:
            st.header("🎛️ Filtros Avançados")
            
            df_filtrado = df.copy()

            if "REGIAO" in df_filtrado.columns:
                regioes = sorted(df_filtrado["REGIAO"].dropna().unique())
                regiao_escolhida = st.selectbox("Região:", options=["TODOS"] + regioes)
                if regiao_escolhida != "TODOS":
                    df_filtrado = df_filtrado[df_filtrado["REGIAO"] == regiao_escolhida]

            if "UF" in df_filtrado.columns:
                ufs = sorted(df_filtrado["UF"].dropna().unique())
                uf_escolhida = st.selectbox("UF:", options=["TODOS"] + ufs)
                if uf_escolhida != "TODOS":
                    df_filtrado = df_filtrado[df_filtrado["UF"] == uf_escolhida]

            if "MUNICIPIO" in df_filtrado.columns:
                municipios = sorted(df_filtrado["MUNICIPIO"].dropna().unique())
                mun_escolhido = st.selectbox("Município:", options=["TODOS"] + municipios)
                if mun_escolhido != "TODOS":
                    df_filtrado = df_filtrado[df_filtrado["MUNICIPIO"] == mun_escolhido]

            if "DESC_NATUREZA_JURIDICA" in df_filtrado.columns:
                esferas = sorted(df_filtrado["DESC_NATUREZA_JURIDICA"].dropna().unique())
                esfera_escolhida = st.selectbox("Esfera (Público/Privado):", options=["TODOS"] + esferas)
                if esfera_escolhida != "TODOS":
                    df_filtrado = df_filtrado[df_filtrado["DESC_NATUREZA_JURIDICA"] == esfera_escolhida]

            if "DS_TIPO_UNIDADE" in df_filtrado.columns:
                tipos = sorted(df_filtrado["DS_TIPO_UNIDADE"].dropna().unique())
                tipo_escolhido = st.selectbox("Tipo de Unidade:", options=["TODOS"] + tipos)
                if tipo_escolhido != "TODOS":
                    df_filtrado = df_filtrado[df_filtrado["DS_TIPO_UNIDADE"] == tipo_escolhido]

            busca_estabelecimento = st.text_input("Buscar Estabelecimento:", placeholder="Digite o nome...")
            if busca_estabelecimento and "NOME_ESTABELECIMENTO" in df_filtrado.columns:
                df_filtrado = df_filtrado[df_filtrado["NOME_ESTABELECIMENTO"].str.contains(busca_estabelecimento, case=False, na=False)]

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
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            # Utilizando a função em cache para exportar APENAS os dados filtrados
            csv_data = converter_df_para_csv(df_filtrado)
            st.download_button(
                label="📥 Exportar Dados Filtrados",
                data=csv_data,
                file_name="leitos_hospitalares_filtrados.csv",
                mime="text/csv",
                use_container_width=True,
                key="btn_exp_leitos",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # CARDS DE MÉTRICAS (KPIs)
        # =========================================================
        total_estabelecimentos = len(df_filtrado)
        total_leitos = int(df_filtrado["LEITOS_EXISTENTES"].sum()) if "LEITOS_EXISTENTES" in df_filtrado.columns else 0
        total_sus = int(df_filtrado["LEITOS_SUS"].sum()) if "LEITOS_SUS" in df_filtrado.columns else 0
        total_uti = int(df_filtrado["UTI_TOTAL_EXIST"].sum()) if "UTI_TOTAL_EXIST" in df_filtrado.columns else 0

        # Função auxiliar para gerar o HTML do Card alinhado
        def gerar_html_kpi(titulo, valor, subtitulo, cor_sub, icone, bg_gradiente):
            return f"""
            <div class="metric-card">
                <div class="metric-info">
                    <p style="color: #9ca3af; font-size: 14px; margin: 0; font-weight: 600;">{titulo}</p>
                    <h2 style="margin: 4px 0; font-size: 26px; font-weight: 800; color: #ffffff;">{valor}</h2>
                    <p style="color: {cor_sub}; font-size: 12px; margin: 0; font-weight: 600;">{subtitulo}</p>
                </div>
                <div class="metric-icon" style="background: {bg_gradiente};">
                    {icone}
                </div>
            </div>
            """

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.markdown(gerar_html_kpi("Unidades Filtradas", f"{total_estabelecimentos:,}".replace(",", "."), "Unidades de saúde", "#9ca3af", "🏥", "linear-gradient(135deg, #a855f7 0%, #7c3aed 100%)"), unsafe_allow_html=True)
        with m2:
            st.markdown(gerar_html_kpi("Total de Leitos", f"{total_leitos:,}".replace(",", "."), "Capacidade cadastrada", "#9ca3af", "🛏️", "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)"), unsafe_allow_html=True)
        with m3:
            perc_sus = (total_sus/total_leitos*100) if total_leitos else 0
            st.markdown(gerar_html_kpi("Leitos SUS", f"{total_sus:,}".replace(",", "."), f"{perc_sus:.1f}% da rede", "#10b981", "🤝", "linear-gradient(135deg, #10b981 0%, #059669 100%)"), unsafe_allow_html=True)
        with m4:
            st.markdown(gerar_html_kpi("Leitos UTI", f"{total_uti:,}".replace(",", "."), "UTI Geral Cadastrada", "#ef4444", "🚨", "linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # TABELA PRINCIPAL
        # =========================================================
        st.markdown(
            """
            <div style="margin-bottom: 12px;">
                <h3 style="margin: 0; font-size: 20px; font-weight: 700; color: #ffffff;">📋 Tabela Detalhada de Unidades Hospitalares</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        colunas_exibir = [
            c for c in ["NOME_ESTABELECIMENTO", "MUNICIPIO", "UF", "LEITOS_EXISTENTES", "LEITOS_SUS", "UTI_TOTAL_EXIST", "UTI_TOTAL_SUS", "DS_TIPO_UNIDADE"]
            if c in df_filtrado.columns
        ]

        if not df_filtrado.empty:
            df_tabela = df_filtrado[colunas_exibir].copy()
            if "LEITOS_EXISTENTES" in df_tabela.columns:
                df_tabela = df_tabela.sort_values(by="LEITOS_EXISTENTES", ascending=False)

            st.dataframe(
                df_tabela,
                column_config={
                    "NOME_ESTABELECIMENTO": st.column_config.TextColumn("Hospital / Estabelecimento", width="large"),
                    "MUNICIPIO": st.column_config.TextColumn("Município", width="medium"),
                    "UF": st.column_config.TextColumn("UF", width="small"),
                    "LEITOS_EXISTENTES": st.column_config.ProgressColumn(
                        "Total de Leitos",
                        format="%d",
                        min_value=0,
                        max_value=max_leitos_global,
                    ),
                    "LEITOS_SUS": st.column_config.NumberColumn("Leitos SUS", format="%d"),
                    "UTI_TOTAL_EXIST": st.column_config.NumberColumn("UTI Total", format="%d"),
                    "UTI_TOTAL_SUS": st.column_config.NumberColumn("UTI SUS", format="%d"),
                    "DS_TIPO_UNIDADE": st.column_config.TextColumn("Tipo de Unidade", width="medium"),
                },
                use_container_width=True,
                hide_index=True,
                height=350,
            )
        else:
            st.warning("⚠️ Nenhum estabelecimento encontrado com os filtros selecionados.")

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # GRÁFICOS ANALÍTICOS
        # =========================================================
        if not df_filtrado.empty and total_leitos > 0:
            c_left, c_right = st.columns(2)

            # --- GRÁFICO 1: RAIO-X DAS UTIS ---
            with c_left:
                colunas_uti = {
                    "UTI Adulto": "UTI_ADULTO_EXIST",
                    "UTI Pediátrica": "UTI_PEDIATRICO_EXIST",
                    "UTI Neonatal": "UTI_NEONATAL_EXIST",
                    "UTI Queimados": "UTI_QUEIMADO_EXIST",
                    "UTI Coronariana": "UTI_CORONARIANA_EXIST"
                }
                
                vals_uti = []
                nomes_uti = []
                for nome, col in colunas_uti.items():
                    if col in df_filtrado.columns:
                        soma = int(df_filtrado[col].sum())
                        if soma > 0:
                            vals_uti.append(soma)
                            nomes_uti.append(nome)

                if vals_uti:
                    fig_uti = go.Figure(go.Bar(
                        x=vals_uti,
                        y=nomes_uti,
                        orientation="h",
                        text=[f"{v:,}".replace(",", ".") for v in vals_uti],
                        textposition="auto",
                        marker_color="#ef4444"
                    ))
                    
                    fig_uti.update_layout(
                        title=dict(text="Raio-X: Perfil de Leitos de UTI", font=dict(color="#ffffff", size=16)),
                        # Background transparente para herdar o CSS do contêiner arredondado
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#ffffff", size=12),
                        margin=dict(l=20, r=20, t=50, b=20),
                        height=320,
                        xaxis=dict(showgrid=False, visible=False),
                        yaxis=dict(showgrid=False, autorange="reversed")
                    )
                    st.plotly_chart(fig_uti, use_container_width=True)
                else:
                    st.info("💡 Nenhum leito de UTI específico detalhado na seleção atual.")

            # --- GRÁFICO 2: PROPORÇÃO SUS VS PRIVADO ---
            with c_right:
                outros_leitos = max(0, total_leitos - total_sus)
                df_pie = pd.DataFrame({
                    "Categoria": ["Leitos SUS", "Privado / Outros"],
                    "Quantidade": [total_sus, outros_leitos],
                })

                fig_pie = px.pie(
                    df_pie,
                    values="Quantidade",
                    names="Categoria",
                    hole=0.65, # Ajuste leve para visual mais limpo (donut mais fino)
                    color_discrete_sequence=["#10b981", "#3b82f6"],
                )

                fig_pie.update_traces(textinfo='percent', textfont_size=14, textfont_color="white")

                fig_pie.update_layout(
                    title=dict(text="Proporção SUS vs Privado", font=dict(color="#ffffff", size=16)),
                    # Background transparente para herdar o CSS do contêiner arredondado
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ffffff", size=13),
                    margin=dict(l=20, r=20, t=50, b=20),
                    height=320,
                    showlegend=True,
                    legend=dict(
                        orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color="#9ca3af")
                    ),
                )
                st.plotly_chart(fig_pie, use_container_width=True)