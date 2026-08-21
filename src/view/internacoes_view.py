import streamlit as st
import pandas as pd
import plotly.express as px

class InternacoesView:
    def render(self, model):
        # Header e Filtros Superiores
        col_title, col_actions = st.columns([2, 1])
        with col_title:
            st.title("Internações")
            st.caption("Acompanhe o volume de internações e sua evolução em tempo real.")
        
        with col_actions:
            c1, c2 = st.columns([1, 1])
            with c1:
                st.button("⚙️ Filtros", use_container_width=True)
            with c2:
                st.button("📥 Exportar", use_container_width=True)

        st.markdown("---")

        # 1. KPIs Superiores
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        
        kpi1.metric("Total de internações", "3.246.781", "+12,4% vs período anterior")
        kpi2.metric("Internações do dia", "12.458", "+8,7% vs ontem")
        kpi3.metric("Taxa de ocupação média", "78%", "+4,3% vs período anterior")
        kpi4.metric("Tempo médio de permanência", "5,6 dias", "-0,3 dia vs período anterior")
        kpi5.metric("Taxa de readmissão (30 dias)", "8,2%", "-0,8% vs período anterior")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Gráficos do Meio: Evolução + Tipo
        col_evolucao, col_tipo = st.columns([2, 1])

        with col_evolucao:
            st.subheader("Evolução das internações")
            df_evolucao = pd.DataFrame({
                "Data": ["01/04", "08/04", "15/04", "22/04", "29/04", "06/05", "13/05", "20/05", "27/05", "03/06"],
                "Internações": [12000, 14000, 11000, 15500, 13000, 16000, 14726, 17000, 18000, 19500]
            })
            fig_line = px.line(
                df_evolucao, x="Data", y="Internações", markers=True, 
                line_shape="spline", color_discrete_sequence=["#a855f7"]
            )
            fig_line.update_traces(fill='tozeroy', fillcolor='rgba(168, 85, 247, 0.15)')
            fig_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
                margin=dict(l=0, r=0, t=20, b=0),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            )
            st.plotly_chart(fig_line, use_container_width=True)

        with col_tipo:
            st.subheader("Internações por tipo")
            df_tipo = pd.DataFrame({
                "Tipo": ["Clínicas", "Cirúrgicas", "Pediátricas", "Obstétricas", "Psiquiátricas", "Outras"],
                "Qtd": [42, 26, 12, 9, 8, 3]
            })
            fig_donut = px.pie(df_tipo, values="Qtd", names="Tipo", hole=0.6,
                               color_discrete_sequence=["#a855f7", "#6366f1", "#3b82f6", "#ec4899", "#8b5cf6", "#64748b"])
            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
                showlegend=True,
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Bloco Inferior: Tabela + Faixa Etária (Esquerda) vs Ocupação + Causas (Direita)
        col_tabela, col_detalhes = st.columns([1.5, 1])

        with col_tabela:
            st.subheader("Internações por município")
            df_municipios = pd.DataFrame({
                "Município": ["São Paulo - SP", "Rio de Janeiro - RJ", "Belo Horizonte - MG", "Fortaleza - CE", "Salvador - BA"],
                "Internações": [234567, 158882, 98765, 87543, 76321],
                "% do total": ["7,2%", "4,8%", "3,0%", "2,7%", "2,3%"],
                "Variação (%)": ["+11,2%", "+9,3%", "+3,1%", "+6,8%", "+4,2%"],
                "Taxa Ocupação": ["81%", "76%", "72%", "74%", "70%"],
                "Tempo Médio": ["5,8 dias", "6,1 dias", "5,3 dias", "5,9 dias", "5,2 dias"]
            })
            st.dataframe(df_municipios, use_container_width=True, hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # NOVO ELEMENTO CLEAN: Internações por Faixa Etária
            st.subheader("Internações por faixa etária")
            df_faixa = pd.DataFrame({
                "Faixa Etária": ["0-17", "18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"],
                "Internações (mil)": [25, 40, 58, 72, 95, 110, 105, 85]
            })
            fig_faixa = px.bar(
                df_faixa, x="Faixa Etária", y="Internações (mil)", 
                color_discrete_sequence=["#8b5cf6"]
            )
            fig_faixa.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
                margin=dict(l=0, r=0, t=10, b=0),
                height=220
            )
            st.plotly_chart(fig_faixa, use_container_width=True)

        with col_detalhes:
            st.subheader("Taxa de ocupação por faixa")
            st.progress(0.92, text="UTI Adulto: 92%")
            st.progress(0.88, text="UTI Pediátrica: 88%")
            st.progress(0.76, text="Enfermaria: 76%")
            st.progress(0.72, text="Leitos Clínicos: 72%")

            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Principais causas de internação")
            df_causas = pd.DataFrame({
                "Causa": ["Doenças respiratórias", "Doenças circulatórias", "Doenças digestivas", "Lesões/Envenenamento", "Doenças infecciosas"],
                "%": [22.6, 17.9, 12.4, 9.7, 6.1]
            })
            fig_causas = px.bar(df_causas, x="%", y="Causa", orientation="h",
                                color_discrete_sequence=["#a855f7"])
            fig_causas.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff"),
                xaxis=dict(showgrid=False),
                yaxis=dict(autorange="reversed"),
                margin=dict(l=0, r=0, t=10, b=0),
                height=220
            )
            st.plotly_chart(fig_causas, use_container_width=True)

        st.caption("🛡️ Dados públicos do SUS integrados e atualizados periodicamente.")