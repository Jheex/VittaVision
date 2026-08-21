import streamlit as st
import pandas as pd

class DashboardView:
    def render(self, model):
        # =========================================================
        # CABEÇALHO DO DASHBOARD
        # =========================================================
        col_title, col_date, col_filter = st.columns([3, 1, 1])
        with col_title:
            st.markdown("""
                <h1 style="margin: 0; font-size: 24px; font-weight: 700; color: #ffffff;">Bem-vindo(a) ao <span style="color: #3b82f6;">VITTA VISION</span></h1>
                <p style="margin: 4px 0 0 0; font-size: 13px; color: #9ca3af;">Painel inteligente de monitoramento da capacidade hospitalar e demanda por internações no SUS.</p>
            """, unsafe_allow_html=True)
        with col_date:
            st.markdown("""
                <div style="background: rgba(18, 24, 38, 0.7); border: 1px solid rgba(168, 85, 247, 0.3); padding: 8px 12px; border-radius: 10px; text-align: center; font-size: 12px; color: #e2e8f0;">
                    📅 01/01/2024 - 30/04/2026
                </div>
            """, unsafe_allow_html=True)
        with col_filter:
            st.markdown("""
                <div style="background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%); padding: 8px 12px; border-radius: 10px; text-align: center; font-size: 12px; font-weight: 600; color: #ffffff; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);">
                    🎯 Filtros
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # CARDS DE MÉTRICAS SUPERIORES (KPIs)
        # =========================================================
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            st.markdown("""
                <div class="metric-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <p style="color: #9ca3af; font-size: 12px; margin: 0;">Internações</p>
                            <h3 style="margin: 4px 0; font-size: 20px; color: #ffffff;">3.246.781</h3>
                            <p style="color: #9ca3af; font-size: 11px; margin: 0;">Total no período</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); padding: 10px; border-radius: 10px; font-size: 16px;">🛏️</div>
                    </div>
                    <p style="color: #10b981; font-size: 11px; margin-top: 10px; font-weight: 600;">↑ 12,4% <span style="color: #9ca3af; font-weight: normal;">vs período anterior</span></p>
                </div>
            """, unsafe_allow_html=True)

        with kpi2:
            st.markdown("""
                <div class="metric-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <p style="color: #9ca3af; font-size: 12px; margin: 0;">Valor Pago (R$)</p>
                            <h3 style="margin: 4px 0; font-size: 20px; color: #ffffff;">4,82 Bi</h3>
                            <p style="color: #9ca3af; font-size: 11px; margin: 0;">Total no período</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); padding: 10px; border-radius: 10px; font-size: 16px;">💰</div>
                    </div>
                    <p style="color: #10b981; font-size: 11px; margin-top: 10px; font-weight: 600;">↑ 9,7% <span style="color: #9ca3af; font-weight: normal;">vs período anterior</span></p>
                </div>
            """, unsafe_allow_html=True)

        with kpi3:
            st.markdown("""
                <div class="metric-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <p style="color: #9ca3af; font-size: 12px; margin: 0;">Permanência Média</p>
                            <h3 style="margin: 4px 0; font-size: 20px; color: #ffffff;">5,6 dias</h3>
                            <p style="color: #9ca3af; font-size: 11px; margin: 0;">Média no período</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 10px; border-radius: 10px; font-size: 16px;">📅</div>
                    </div>
                    <p style="color: #ef4444; font-size: 11px; margin-top: 10px; font-weight: 600;">↓ 0,3 dia <span style="color: #9ca3af; font-weight: normal;">vs período anterior</span></p>
                </div>
            """, unsafe_allow_html=True)

        with kpi4:
            st.markdown("""
                <div class="metric-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <p style="color: #9ca3af; font-size: 12px; margin: 0;">Municípios Atendidos</p>
                            <h3 style="margin: 4px 0; font-size: 20px; color: #ffffff;">5.568</h3>
                            <p style="color: #9ca3af; font-size: 11px; margin: 0;">Total de municípios</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%); padding: 10px; border-radius: 10px; font-size: 16px;">🏢</div>
                    </div>
                    <p style="color: #10b981; font-size: 11px; margin-top: 10px; font-weight: 600;">100% <span style="color: #9ca3af; font-weight: normal;">do território nacional</span></p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # GRÁFICO DE LINHAS + MAPA DE PRESSÃO AO LADO
        # =========================================================
        col_grafico, col_mapa = st.columns([1.3, 1])

        with col_grafico:
            st.markdown("""
                <div class="metric-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <h3 style="margin: 0; font-size: 15px; color: #ffffff;">Internações por período</h3>
                        <span style="font-size: 12px; color: #9ca3af; background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 6px;">Mensal ▾</span>
                    </div>
            """, unsafe_allow_html=True)
            
            df_int = model.get_internacoes_data()
            st.line_chart(df_int.set_index("Data"), color="#a855f7", height=220)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_mapa:
            st.markdown("""
                <div class="metric-card">
                    <h3 style="margin: 0 0 10px 0; font-size: 15px; color: #ffffff;">Mapa de pressão assistencial</h3>
                    <div style="display: flex; gap: 15px; align-items: center;">
                        <div style="background: rgba(139, 92, 246, 0.1); border-radius: 10px; padding: 10px; text-align: center; flex: 1;">
                            <p style="font-size: 11px; color: #9ca3af; margin: 0;">Região Crítica</p>
                            <p style="font-size: 14px; font-weight: bold; color: #f43f5e; margin: 4px 0 0 0;">Sudeste (89%)</p>
                        </div>
                        <div style="font-size: 12px; color: #9ca3af; flex: 1;">
                            <p style="margin: 2px 0;">🔴 Sudeste — 89%</p>
                            <p style="margin: 2px 0;">🟣 Nordeste — 74%</p>
                            <p style="margin: 2px 0;">🔵 Sul — 72%</p>
                            <p style="margin: 2px 0;">🔵 Norte — 65%</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # RANKING DE MUNICÍPIOS + TAXA DE OCUPAÇÃO + CHATBOT DE IA
        # =========================================================
        col_top, col_taxa, col_ai = st.columns([1, 1, 1.2])

        # 1. Ranking de internações por municípios
        with col_top:
            st.markdown("""
                <div class="metric-card" style="height: 100%;">
                    <h3 style="margin: 0 0 10px 0; font-size: 14px; color: #ffffff;">Top 5 municípios por internações</h3>
                    <div style="font-size: 12px; color: #9ca3af;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>1. São Paulo - SP</span><strong style="color:#fff;">234.567</strong></div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>2. Rio de Janeiro - RJ</span><strong style="color:#fff;">156.892</strong></div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>3. Belo Horizonte - MG</span><strong style="color:#fff;">98.765</strong></div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span>4. Fortaleza - CE</span><strong style="color:#fff;">87.543</strong></div>
                        <div style="display: flex; justify-content: space-between;"><span>5. Salvador - BA</span><strong style="color:#fff;">76.321</strong></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # 2. Taxa de ocupação de leitos
        with col_taxa:
            st.markdown("""
                <div class="metric-card" style="height: 100%;">
                    <h3 style="margin: 0; font-size: 14px; color: #ffffff;">Taxa de ocupação de leitos (média)</h3>
                    <div style="text-align: center; margin: 15px 0;">
                        <span style="font-size: 28px; font-weight: bold; color: #3b82f6;">78%</span>
                        <p style="font-size: 11px; color: #9ca3af; margin: 0;">Taxa média geral</p>
                    </div>
                    <div style="background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.3); padding: 8px; border-radius: 8px; font-size: 11px; color: #f43f5e; text-align: center;">
                        🚨 15 regiões em alerta crítico (> 90%)
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # 3. Chatbot integrado de IA
        with col_ai:
            st.markdown("""
                <div class="metric-card" style="height: 100%;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <h3 style="margin: 0; font-size: 14px; color: #ffffff;">✨ Assistente IA</h3>
                        <span style="font-size: 10px; background: #8b5cf6; color: white; padding: 2px 6px; border-radius: 4px;">BETA</span>
                    </div>
                    <div style="background: rgba(139, 92, 246, 0.1); padding: 8px; border-radius: 8px; font-size: 11px; color: #e2e8f0; margin-bottom: 10px;">
                        🤖 <strong>Vitta IA:</strong> A região Sudeste registrou o maior número de internações, representando 39,2% do total nacional.
                    </div>
                    <div style="display: flex; gap: 5px;">
                        <input type="text" placeholder="Faça uma pergunta..." style="width: 100%; background: #070913; border: 1px solid rgba(168, 85, 247, 0.3); padding: 6px 10px; border-radius: 6px; color: white; font-size: 11px;" disabled>
                    </div>
                </div>
            """, unsafe_allow_html=True)