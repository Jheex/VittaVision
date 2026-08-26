import streamlit as st
import pandas as pd

class RelatoriosView:
    def render(self, model=None):
        st.markdown("""
            <div style="margin-bottom: 25px;">
                <h2 style="color: #f8fafc; font-weight: 700; margin-bottom: 5px;">📊 Relatórios Gerenciais</h2>
                <p style="color: #94a3b8; font-size: 14px;">Central de consolidação de dados estratégicos, indicadores de desempenho e exportação.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 16px; margin-bottom: 20px;">
                <h4 style="color: #e2e8f0; font-size: 15px; margin-bottom: 15px;">Filtros de Emissão</h4>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Tipo de Relatório", ["Desempenho Geral de Leitos", "Fluxo de Internações", "Eficiência Operacional", "Auditoria de Atendimentos"])
        with col2:
            st.selectbox("Período de Análise", ["Último Trimestre", "Semestre Atual", "Ano Corrente (2026)", "Personalizado"])
        with col3:
            st.selectbox("Setor / Unidade", ["Todos os Hospitais", "Hospital Central", "Hospital Norte", "Hospital Sul"])

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 16px; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h4 style="color: #e2e8f0; font-size: 15px; margin: 0;">Pré-visualização do Sumário Executivo</h4>
                    <span style="background: rgba(168, 85, 247, 0.1); color: #c084fc; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">Status: Consolidado</span>
                </div>
        """, unsafe_allow_html=True)

        df_relatorio = pd.DataFrame({
            "Métrica Chave": ["Taxa Média de Ocupação", "Giro de Leitos", "Tempo Médio de Permanência", "Índice de Infecção Hospitalar", "Satisfação do Paciente (NPS)"],
            "Resultado Atual": ["84.5%", "4.2 por mês", "5.4 dias", "1.2%", "88.0"],
            "Meta Estabelecida": ["80.0%", "4.0 por mês", "5.0 dias", "< 1.5%", "85.0"],
            "Desvio / Avaliação": ["+4.5% (Acima)", "+0.2 (Ideal)", "+0.4d (Atenção)", "-0.3% (Bom)", "+3.0 (Excelente)"]
        })

        st.dataframe(df_relatorio, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 16px;">
                <h4 style="color: #e2e8f0; font-size: 15px; margin-bottom: 15px;">Exportar Documentação</h4>
        """, unsafe_allow_html=True)

        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            if st.button("📄 Baixar Relatório em PDF", use_container_width=True):
                st.success("Relatório PDF gerado com sucesso! (Simulação)")
        with col_btn2:
            if st.button("📊 Exportar Planilha (Excel)", use_container_width=True):
                st.success("Planilha Excel exportada com sucesso! (Simulação)")
        with col_btn3:
            if st.button("📧 Enviar por E-mail à Diretoria", use_container_width=True):
                st.info("E-mail disparado para o grupo de gestores.")

        st.markdown("</div>", unsafe_allow_html=True)