import streamlit as st
import pandas as pd
import plotly.express as px

class LeitosView:
    def render(self, model):
        # Header e Ações
        col_title, col_actions = st.columns([2, 1])
        with col_title:
            st.title("Gestão de Leitos")
            st.caption("Monitoramento dinâmico de capacidade, ocupação e giro hospitalar em tempo real.")
        
        with col_actions:
            c1, c2 = st.columns([1, 1])
            with c1:
                st.button("⚙️ Filtros", use_container_width=True, key="btn_filtros_leitos")
            with c2:
                st.button("📥 Exportar", use_container_width=True, key="btn_exp_leitos")

        st.markdown("---")

        # 1. KPIs Superiores Rápidos
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Total de Leitos", "4.850", "+120 este mês")
        k2.metric("Ocupados", "3.783", "78% do total")
        k3.metric("Disponíveis", "742", "15% livres", delta_color="normal")
        k4.metric("Em Higienização", "325", "🚨 Alta Demanda", delta_color="inverse")
        k5.metric("Giro de Leito", "3,8", "pacientes/leito/mês")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. PAINEL SUPERIOR: Resumo Operacional x Gargalos & Alertas
        col_resumo, col_alertas = st.columns([1, 1])

        with col_resumo:
            st.subheader("📊 Resumo Operacional")
            m1, m2 = st.columns(2)
            m1.info("🟣 **3.783 Ocupados**\n\n78% da capacidade total")
            m2.success("🟢 **742 Livres**\n\nProntos para internação")
            
            m3, m4 = st.columns(2)
            m3.warning("🟡 **130 Higienização**\n\nTempo médio: 45 min")
            m4.error("🔴 **195 Manutenção**\n\n3 leitos em estado crítico")

        with col_alertas:
            st.subheader("🚨 Gargalos & Níveis de Alerta")
            st.warning("⚠️ **UTI Adulto - Hosp. Central**: Ocupação crítica em 92%. Risco de fila nas próximas 6h.")
            st.info("🕒 **Higienização**: Tempo médio de 45 min/leito. 12 leitos aguardando liberação rápida.")
            st.error("🚨 **Hospital Norte**: 3 leitos de isolamento indisponíveis por manutenção corretiva.")

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. MEIO: Detalhamento por Unidade Hospitalar (Largura Total)
        st.subheader("🏥 Detalhamento por Unidade Hospitalar")
        df_unidades = pd.DataFrame({
            "Hospital": ["Hospital Central", "Hospital do Norte", "Hospital Sul", "Hospital Leste", "Maternidade Municipal"],
            "Leitos Totais": [1200, 850, 950, 1100, 750],
            "Ocupados": [1020, 680, 712, 825, 546],
            "Disponíveis": [120, 130, 180, 205, 107],
            "Taxa Ocupação": [0.850, 0.800, 0.749, 0.750, 0.728],
            "Status": ["🔴 Crítico", "🟡 Atenção", "🟢 Normal", "🟡 Atenção", "🟢 Normal"]
        })

        st.dataframe(
            df_unidades,
            column_config={
                "Hospital": st.column_config.TextColumn("Unidade Hospitalar"),
                "Leitos Totais": st.column_config.NumberColumn("Total de Leitos", format="%d"),
                "Ocupados": st.column_config.NumberColumn("Leitos Ocupados", format="%d"),
                "Disponíveis": st.column_config.NumberColumn("Livres", format="%d"),
                "Taxa Ocupação": st.column_config.ProgressColumn(
                    "Taxa de Ocupação",
                    help="Percentual de ocupação atual da unidade",
                    format="%.1f%%",
                    min_value=0,
                    max_value=1,
                ),
                "Status": st.column_config.TextColumn("Situação")
            },
            use_container_width=True,
            hide_index=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # 4. BASE: Gráfico Grande de Ocupação por Especialidade (Vertical)
        st.subheader("📈 Taxa de Ocupação por Especialidade (%)")
        df_especialidades = pd.DataFrame({
            "Especialidade": ["UTI Adulto", "UTI Pediátrica", "Cirúrgicos", "Clínicos", "Pediatria", "Obstetrícia"],
            "Taxa": [92.3, 85.7, 82.7, 78.5, 76.0, 72.1]
        })

        fig_esp = px.bar(
            df_especialidades, 
            x="Especialidade", 
            y="Taxa", 
            text="Taxa",
            color="Taxa",
            color_continuous_scale=["#3b82f6", "#a855f7", "#ec4899"]
        )
        
        fig_esp.update_traces(
            texttemplate='%{text:.1f}%', 
            textposition='outside',
            marker_line_color='rgba(255,255,255,0.2)',
            marker_line_width=1.5
        )
        
        fig_esp.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff", size=13),
            xaxis=dict(showgrid=False, title=None),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', range=[0, 105], title="Ocupação (%)"),
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=30, b=10),
            height=340
        )
        
        st.plotly_chart(fig_esp, use_container_width=True)

        st.caption("🛡️ Monitoramento de leitos atualizado em tempo real via sistema de gestão hospitalar.")