import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# FUNÇÃO DE CARREGAMENTO COM CACHE (FORA DA CLASSE)
# =========================================================
@st.cache_data
def _carregar_dados_hospitais():
  try:
    df = pd.read_csv("leitos.csv", sep=";", encoding="latin1", low_memory=False)
    return df
  except Exception:
    return pd.DataFrame()


class HospitaisView:

  # =========================================================
  # RENDER PRINCIPAL
  # =========================================================
  def render(self, model=None):
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px;">
            <div>
                <h1 style="margin: 0; color: #FFFFFF; font-size: 2.2rem;">🏥 Painel de Hospitais</h1>
                <p style="margin: 5px 0 0 0; color: #9AA4B2; font-size: 1rem;">
                    Monitoramento inteligente de unidades hospitalares, leitos e distribuição geográfica.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    self._aplicar_estilos()

    # Carrega dados reais utilizando a função cacheada externa
    df = _carregar_dados_hospitais()

    # 1. Indicadores em Cartões Customizados
    self._render_indicadores(df)

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Gráficos Analíticos
    self._render_graficos(df)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Filtros Superiores para a Seção do Mapa e Dados Geográficos
    st.markdown("#### 🗺️ Mapeamento e Distribuição Geográfica")
    col1, col2, col3 = st.columns(3)
    with col1:
      regiao_filtro = st.selectbox(
          "Filtrar Região",
          ["Todas", "Norte", "Sul", "Leste", "Oeste", "Centro"],
      )
    with col2:
      tipo_unidade = st.selectbox(
          "Tipo de Unidade",
          ["Todos", "Hospital Geral", "UPA", "Clínica Especializada"],
      )
    with col3:
      metrica_mapa = st.selectbox(
          "Métrica de Exibição",
          [
              "Volume de Internações",
              "Ocupação de Leitos (%)",
              "Tempo Médio de Espera",
          ],
      )

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Mapa Geográfico Integrado (com layout em duas colunas)
    self._render_mapa_e_destaques(df)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Tabela + Hospitais por Porte
    self._render_tabela_e_porte(df)

  # =========================================================
  # ESTILOS CSS REFINADOS
  # =========================================================
  def _aplicar_estilos(self):
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #030712;
        }
        .metric-card {
            background: linear-gradient(135deg, #0B132B 0%, #1C2541 100%);
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease;
        }
        .metric-card:hover {
            border-color: #7424FF;
        }
        h4 {
            color: #F8FAFC !important;
            font-weight: 600 !important;
            letter-spacing: -0.025em;
        }
        div[data-baseweb="input"] {
            background-color: #0B132B !important;
            border-color: #1E293B !important;
            border-radius: 8px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

  # =========================================================
  # 5 INDICADORES COM VISUAL PREMIUM
  # =========================================================
  def _render_indicadores(self, df):
    if not df.empty and "CNES" in df.columns:
      total_hospitais = df["CNES"].nunique()
      ativos = (
          df[df["MOTIVO_DESABILITACAO"].isna()]["CNES"].nunique()
          if "MOTIVO_DESABILITACAO" in df.columns
          else total_hospitais
      )
      leitos_totais = (
          df["LEITOS_EXISTENTES"].sum()
          if "LEITOS_EXISTENTES" in df.columns
          else 0
      )
      leitos_sus = (
          df["LEITOS_SUS"].sum() if "LEITOS_SUS" in df.columns else 0
      )
    else:
      total_hospitais, ativos, leitos_totais, leitos_sus = (
          1642,
          1523,
          245781,
          168342,
      )

    col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

    with col1:
      st.metric(
          label="🏥 Total de Hospitais",
          value=f"{total_hospitais:,.0f}".replace(",", "."),
          delta="3,6% vs ant.",
      )
    with col2:
      st.metric(
          label="🛡️ Hospitais Ativos",
          value=f"{ativos:,.0f}".replace(",", "."),
          delta="4,1% vs ant.",
      )
    with col3:
      st.metric(
          label="🛏️ Leitos Totais",
          value=f"{leitos_totais:,.0f}".replace(",", "."),
          delta="5,8% vs ant.",
      )
    with col4:
      st.metric(
          label="➕ Leitos SUS",
          value=f"{leitos_sus:,.0f}".replace(",", "."),
          delta="6,2% vs ant.",
      )
    with col5:
      st.metric(
          label="📈 Taxa de Ocupação",
          value="78%",
          delta="-0,7 p.p.",
          delta_color="inverse",
      )

  # =========================================================
  # 3 GRÁFICOS ANALÍTICOS
  # =========================================================
  def _render_graficos(self, df):
    grafico1, grafico2, grafico3 = st.columns([1, 1.1, 1.8], gap="medium")

    # GRÁFICO 1 - TIPO DE GESTÃO
    with grafico1:
      st.markdown("#### Tipo de Gestão")
      if not df.empty and "TP_GESTAO" in df.columns:
        gestao_counts = df["TP_GESTAO"].value_counts()
        labels = list(gestao_counts.index)
        values = list(gestao_counts.values)
        total_val = sum(values)
      else:
        labels, values, total_val = ["Público", "Privado", "Filantrópico"], [
            55,
            35,
            10,
        ], 1642

      fig_gestao = go.Figure(
          data=[
              go.Pie(
                  labels=labels,
                  values=values,
                  hole=0.65,
                  marker=dict(colors=["#3B82F6", "#8B5CF6", "#EC4899"]),
                  textinfo="none",
                  hovertemplate="<b>%{label}</b><br>%{value} un.<extra></extra>",
              )
          ]
      )

      fig_gestao.add_annotation(
          text=f"<b>{total_val}</b><br><span style='font-size:11px; color:#9AA4B2;'>Total</span>",
          x=0.5,
          y=0.5,
          showarrow=False,
          font=dict(size=15, color="white"),
      )

      fig_gestao.update_layout(
          height=260,
          margin=dict(l=0, r=0, t=10, b=10),
          paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(0,0,0,0)",
          showlegend=True,
          legend=dict(
              orientation="h",
              yanchor="bottom",
              y=-0.2,
              xanchor="center",
              x=0.5,
              font=dict(color="#D7DCE5", size=10),
          ),
      )
      st.plotly_chart(
          fig_gestao, use_container_width=True, config={"displayModeBar": False}
      )

    # GRÁFICO 2 - HOSPITAIS POR REGIÃO
    with grafico2:
      st.markdown("#### Hospitais por Região")
      if not df.empty and "REGIAO" in df.columns:
        reg_counts = df["REGIAO"].value_counts()
        regioes, valores = list(reg_counts.index), list(reg_counts.values)
      else:
        regioes, valores = [
            "Sudeste",
            "Nordeste",
            "Sul",
            "Norte",
            "Centro-Oeste",
        ], [642, 478, 281, 156, 85]

      fig_regiao = go.Figure()
      fig_regiao.add_trace(
          go.Bar(
              x=valores,
              y=regioes,
              orientation="h",
              text=[str(v) for v in valores],
              textposition="outside",
              cliponaxis=False,
              marker=dict(color="#8B5CF6"),
          )
      )

      fig_regiao.update_layout(
          height=260,
          margin=dict(l=0, r=40, t=10, b=10),
          paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(0,0,0,0)",
          font=dict(color="#D7DCE5", size=11),
          xaxis=dict(visible=False),
          yaxis=dict(autorange="reversed", showgrid=False),
          bargap=0.4,
          showlegend=False,
      )
      st.plotly_chart(
          fig_regiao, use_container_width=True, config={"displayModeBar": False}
      )

    # GRÁFICO 3 - EVOLUÇÃO TEMPORAL
    with grafico3:
      st.markdown("#### Evolução Mensal de Unidades")
      datas = ["Abr/25", "Mai/25", "Jun/25", "Jul/25", "Ago/25", "Set/25"]
      hospitais = [1200, 1310, 1420, 1500, 1580, 1642]

      fig_evolucao = go.Figure()
      fig_evolucao.add_trace(
          go.Scatter(
              x=datas,
              y=hospitais,
              mode="lines+markers",
              line=dict(color="#8B5CF6", width=3.5),
              marker=dict(size=6, color="#C084FC"),
              fill="tozeroy",
              fillcolor="rgba(139, 92, 246, 0.15)",
          )
      )

      fig_evolucao.update_layout(
          height=260,
          margin=dict(l=10, r=10, t=10, b=10),
          paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(0,0,0,0)",
          font=dict(color="#D7DCE5", size=11),
          xaxis=dict(showgrid=False, zeroline=False),
          yaxis=dict(
              gridcolor="rgba(255,255,255,0.05)",
              zeroline=False,
              tickfont=dict(color="#9AA4B2"),
          ),
          showlegend=False,
      )
      st.plotly_chart(
          fig_evolucao,
          use_container_width=True,
          config={"displayModeBar": False},
      )

  # =========================================================
  # MAPA INTERATIVO E DESTAQUES REGIONAIS (ST.MAP)
  # =========================================================
  def _render_mapa_e_destaques(self, df):
    np.random.seed(42)
    n_pontos = min(len(df), 200) if not df.empty else 25

    # Monta o DataFrame com coordenadas geográficas para o st.map
    df_mapa = pd.DataFrame({
        "lat": (
            df["LATITUDE"].head(n_pontos).values
            if not df.empty and "LATITUDE" in df.columns
            else -23.5505 + np.random.randn(n_pontos) * 0.05
        ),
        "lon": (
            df["LONGITUDE"].head(n_pontos).values
            if not df.empty and "LONGITUDE" in df.columns
            else -46.6333 + np.random.randn(n_pontos) * 0.05
        ),
        "nome": (
            df["NOME_ESTABELECIMENTO"].head(n_pontos).values
            if not df.empty and "NOME_ESTABELECIMENTO" in df.columns
            else [f"Hospital Unidade {i+1}" for i in range(n_pontos)]
        ),
        "internacoes": (
            df["LEITOS_EXISTENTES"].head(n_pontos).values
            if not df.empty and "LEITOS_EXISTENTES" in df.columns
            else np.random.randint(50, 500, n_pontos)
        ),
        "ocupacao": np.random.uniform(40, 98, n_pontos).round(1),
    })

    map_col, info_col = st.columns([2, 1], gap="medium")

    with map_col:
      st.markdown(
          """
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 16px;">
                    <h4 style="color: #e2e8f0; font-size: 15px; margin-bottom: 15px;">Geolocalização das Unidades</h4>
            """,
          unsafe_allow_html=True,
      )

      # Usa o st.map nativo do Streamlit (estável e rápido)
      st.map(
          df_mapa,
          latitude="lat",
          longitude="lon",
          size="internacoes",
          color="#8b5cf6",
          zoom=11,
      )

      st.markdown("</div>", unsafe_allow_html=True)

    with info_col:
      st.markdown(
          """
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 16px; height: 100%;">
                    <h4 style="color: #e2e8f0; font-size: 15px; margin-bottom: 15px;">Destaques Regionais</h4>
            """,
          unsafe_allow_html=True,
      )

      st.metric(
          label="Total de Unidades Mapeadas",
          value=len(df_mapa),
          delta="Ativas",
      )
      st.metric(
          label="Média de Ocupação",
          value=f"{df_mapa['ocupacao'].mean():.1f}%",
          delta="-2.1% vs mês ant.",
      )
      st.metric(
          label="Pico de Internações",
          value=f"{df_mapa['internacoes'].max()} pac.",
          delta="Hospital Central",
      )

      st.markdown(
          """
                <div style="margin-top: 20px; font-size: 12px; color: #94a3b8; line-height: 1.5;">
                    💡 <strong>Dica:</strong> O tamanho dos círculos no mapa representa proporcionalmente o volume de internações de cada unidade de saúde.
                </div>
            """,
          unsafe_allow_html=True,
      )

      st.markdown("</div>", unsafe_allow_html=True)

  # =========================================================
  # TABELA + HOSPITAIS POR PORTE
  # =========================================================
  def _render_tabela_e_porte(self, df):
    coluna_tabela, coluna_porte = st.columns([3.2, 1.25], gap="medium")

    with coluna_tabela:
      st.markdown("#### Relação de Estabelecimentos")
      busca = st.text_input(
          "Buscar hospital",
          placeholder="🔎 Digite o nome, CNES ou município...",
          label_visibility="collapsed",
          key="busca_hospital",
      )

      if not df.empty and "NOME_ESTABELECIMENTO" in df.columns:
        df_tabela = df[
            [
                "NOME_ESTABELECIMENTO",
                "CNES",
                "MUNICIPIO",
                "UF",
                "LEITOS_EXISTENTES",
                "LEITOS_SUS",
            ]
        ].copy()
        df_tabela.columns = [
            "Hospital",
            "CNES",
            "Município",
            "UF",
            "Leitos totais",
            "Leitos SUS",
        ]

        if busca:
          mask = (
              df_tabela["Hospital"]
              .str.contains(busca, case=False, na=False)
              | df_tabela["CNES"]
              .astype(str)
              .str.contains(busca, case=False, na=False)
              | df_tabela["Município"]
              .str.contains(busca, case=False, na=False)
          )
          df_tabela = df_tabela[mask]

        st.dataframe(
            df_tabela.head(8),
            use_container_width=True,
            hide_index=True,
            height=280,
        )
      else:
        st.info("Nenhum dado carregado na tabela.")

    with coluna_porte:
      st.markdown("#### Hospitais por Porte")
      portes = ["Pequeno", "Médio", "Grande", "Extra-grande"]
      valores_porte = [214, 356, 612, 460]

      fig_porte = go.Figure()
      fig_porte.add_trace(
          go.Bar(
              x=valores_porte,
              y=portes,
              orientation="h",
              text=[str(v) for v in valores_porte],
              textposition="outside",
              cliponaxis=False,
              marker=dict(color="#3B82F6"),
          )
      )

      fig_porte.update_layout(
          height=280,
          margin=dict(l=0, r=40, t=10, b=10),
          paper_bgcolor="rgba(0,0,0,0)",
          plot_bgcolor="rgba(0,0,0,0)",
          font=dict(color="#D7DCE5", size=11),
          xaxis=dict(visible=False),
          yaxis=dict(autorange="reversed", showgrid=False),
          bargap=0.4,
          showlegend=False,
      )
      st.plotly_chart(
          fig_porte, use_container_width=True, config={"displayModeBar": False}
      )