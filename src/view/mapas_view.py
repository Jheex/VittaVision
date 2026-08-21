import streamlit as st
import pandas as pd
import numpy as np

class MapasView:
    def render(self, df_data=None):
        st.markdown("""
            <div style="margin-bottom: 25px;">
                <h2 style="color: #f8fafc; font-weight: 700; margin-bottom: 5px;">🗺️ Mapeamento de Saúde</h2>
                <p style="color: #94a3b8; font-size: 14px;">Visualização geográfica de hospitais, unidades de atendimento e distribuição de internações.</p>
            </div>
        """, unsafe_allow_html=True)

        # Filtros superiores para o mapa
        col1, col2, col3 = st.columns(3)
        with col1:
            regiao_filtro = st.selectbox("Filtrar Região", ["Todas", "Norte", "Sul", "Leste", "Oeste", "Centro"])
        with col2:
            tipo_unidade = st.selectbox("Tipo de Unidade", ["Todos", "Hospital Geral", "UPA", "Clínica Especializada"])
        with col3:
            metrica_mapa = st.selectbox("Métrica de Exibição", ["Volume de Internações", "Ocupação de Leitos (%)", "Tempo Médio de Espera"])

        st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

        # Gerando dados simulados de coordenadas geográficas (Exemplo centrado em São Paulo / região padrão)
        # Se você já tiver um DataFrame real com colunas 'lat' e 'lon', basta passá-lo para cá.
        if df_data is None or 'lat' not in df_data.columns or 'lon' not in df_data.columns:
            # Coordenadas fictícias para demonstração
            np.random.seed(42)
            n_pontos = 25
            df_mapa = pd.DataFrame({
                'lat': -23.5505 + np.random.randn(n_pontos) * 0.05,
                'lon': -46.6333 + np.random.randn(n_pontos) * 0.05,
                'nome': [f"Hospital Unidade {i+1}" for i in range(n_pontos)],
                'internacoes': np.random.randint(50, 500, n_pontos),
                'ocupacao': np.random.uniform(40, 98, n_pontos).round(1)
            })
        else:
            df_mapa = df_data

        # Layout em duas colunas: Mapa interativo à esquerda e Tabela/Detalhes à direita
        map_col, info_col = st.columns([2, 1])

        with map_col:
            st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 16px;">
                    <h4 style="color: #e2e8f0; font-size: 15px; margin-bottom: 15px;">Geolocalização das Unidades</h4>
            """, unsafe_allow_html=True)
            
            # Exibe o mapa nativo do Streamlit (otimizado e rápido)
            # Dica: O st.map busca automaticamente colunas 'lat'/'latitude' e 'lon'/'longitude'
            st.map(df_mapa, latitude='lat', longitude='lon', size='internacoes', color='#8b5cf6', zoom=11)
            
            st.markdown("</div>", unsafe_allow_html=True)

        with info_col:
            st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 16px; height: 100%;">
                    <h4 style="color: #e2e8f0; font-size: 15px; margin-bottom: 15px;">Destaques Regionais</h4>
            """, unsafe_allow_html=True)
            
            # Cards informativos resumidos dentro da coluna lateral
            st.metric(label="Total de Unidades Mapeadas", value=len(df_mapa), delta="Ativas")
            st.metric(label="Média de Ocupação", value=f"{df_mapa['ocupacao'].mean():.1f}%", delta="-2.1% vs mês ant.")
            st.metric(label="Pico de Internações", value=f"{df_mapa['internacoes'].max()} pac.", delta="Hospital Central")
            
            st.markdown("""
                <div style="margin-top: 20px; font-size: 12px; color: #94a3b8; line-height: 1.5;">
                    💡 <strong>Dica:</strong> O tamanho dos círculos no mapa representa proporcionalmente o volume de internações de cada unidade de saúde.
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

        # Tabela detalhada abaixo do mapa para consulta rápida
        st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 16px;">
                <h4 style="color: #e2e8f0; font-size: 15px; margin-bottom: 15px;">Detalhamento por Unidade</h4>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            df_mapa[['nome', 'internacoes', 'ocupacao']],
            column_config={
                "nome": "Unidade Hospitalar",
                "internacoes": "Total de Internações",
                "ocupacao": st.column_config.ProgressColumn(
                    "Taxa de Ocupação (%)",
                    format="%.1f%%",
                    min_value=0,
                    max_value=100,
                ),
            },
            use_container_width=True,
            hide_index=True
        )
        st.markdown("</div>", unsafe_allow_html=True)