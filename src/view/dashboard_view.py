import streamlit as st
import pandas as pd
import plotly.express as px

class DashboardView:
    def render(self, model):
      # =========================================================
        # CABEÇALHO DO DASHBOARD
        # =========================================================
        st.markdown("""
            <h1 style="margin: 0; font-size: 24px; font-weight: 700; color: #ffffff;">Bem-vindo(a) ao <span style="color: #3b82f6;">VITTA VISION</span></h1>
            <p style="margin: 4px 0 0 0; font-size: 13px; color: #9ca3af;">Painel inteligente de monitoramento da capacidade hospitalar e demanda por internações no SUS.</p>
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
        # GRÁFICO DE LINHAS + MAPA DE PRESSÃO ASSISTENCIAL
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
            fig_line = px.area(df_int, x="Data", y=df_int.columns[1], color_discrete_sequence=["#a855f7"])
            fig_line.update_traces(line_width=2.5, fillcolor='rgba(168, 85, 247, 0.15)')
            fig_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff", size=11),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False, color="#ffffff"),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)', color="#ffffff", title=None),
                height=265
            )
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_mapa:
            st.markdown("""
                <div class="metric-card">
                    <h3 style="margin: 0 0 10px 0; font-size: 15px; color: #ffffff;">Mapa de pressão assistencial</h3>
            """, unsafe_allow_html=True)
            
            df_mapa = pd.DataFrame({
                "lat": [-23.5505, -22.9068, -19.9167, -3.0031, -12.9714],
                "lon": [-46.6333, -43.1729, -43.9345, -60.0158, -38.5014]
            })
            st.map(df_mapa, zoom=3, height=265)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================
        # RANKING DE MUNICÍPIOS + TAXA DE OCUPAÇÃO + CHATBOT DE IA
        # =========================================================
        col_top, col_taxa, col_ai = st.columns([1, 1, 1])

        with col_top:
            st.markdown("""
                <div class="metric-card" style="display: flex; flex-direction: column; justify-content: space-between; height: 250px;">
                    <div>
                        <h3 style="margin: 0 0 16px 0; font-size: 14px; color: #ffffff;">Top 5 municípios por internações</h3>
                        <div style="display: flex; flex-direction: column; gap: 10px;">
                            <div>
                                <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                                    <span style="color: #e2e8f0;">1. São Paulo - SP</span>
                                    <strong style="color: #ffffff;">234.567</strong>
                                </div>
                                <div style="background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; width: 100%;">
                                    <div style="background: #3b82f6; width: 100%; height: 100%; border-radius: 4px;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                                    <span style="color: #e2e8f0;">2. Rio de Janeiro - RJ</span>
                                    <strong style="color: #ffffff;">156.892</strong>
                                </div>
                                <div style="background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; width: 100%;">
                                    <div style="background: #3b82f6; width: 67%; height: 100%; border-radius: 4px;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                                    <span style="color: #e2e8f0;">3. Belo Horizonte - MG</span>
                                    <strong style="color: #ffffff;">98.765</strong>
                                </div>
                                <div style="background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; width: 100%;">
                                    <div style="background: #3b82f6; width: 42%; height: 100%; border-radius: 4px;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                                    <span style="color: #e2e8f0;">4. Fortaleza - CE</span>
                                    <strong style="color: #ffffff;">87.543</strong>
                                </div>
                                <div style="background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; width: 100%;">
                                    <div style="background: #3b82f6; width: 37%; height: 100%; border-radius: 4px;"></div>
                                </div>
                            </div>
                            <div>
                                <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 3px;">
                                    <span style="color: #e2e8f0;">5. Salvador - BA</span>
                                    <strong style="color: #ffffff;">76.321</strong>
                                </div>
                                <div style="background: rgba(255,255,255,0.05); border-radius: 4px; height: 6px; width: 100%;">
                                    <div style="background: #3b82f6; width: 32%; height: 100%; border-radius: 4px;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col_taxa:
            st.markdown("""
                <div class="metric-card" style="display: flex; flex-direction: column; justify-content: space-between; height: 250px;">
                    <div>
                        <h3 style="margin: 0; font-size: 14px; color: #ffffff;">Taxa de ocupação de leitos (média)</h3>
                        <div style="text-align: center; margin-top: 35px;">
                            <span style="font-size: 48px; font-weight: 800; color: #3b82f6;">78%</span>
                            <p style="font-size: 12px; color: #9ca3af; margin: 4px 0 0 0;">Taxa média geral</p>
                        </div>
                    </div>
                    <div style="background: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.3); padding: 10px; border-radius: 8px; font-size: 11px; color: #f43f5e; text-align: center;">
                        🚨 15 regiões em alerta crítico (> 90%)
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col_ai:
            st.markdown("""
                <div class="metric-card" style="display: flex; flex-direction: column; justify-content: space-between; height: 250px;">
                    <div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <h3 style="margin: 0; font-size: 14px; color: #ffffff;">✨ Assistente IA</h3>
                            <span style="font-size: 10px; background: #8b5cf6; color: white; padding: 2px 6px; border-radius: 4px; font-weight: 600;">BETA</span>
                        </div>
                        <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.2); padding: 12px; border-radius: 8px; font-size: 11px; color: #e2e8f0; line-height: 1.5;">
                            🤖 <strong>Vitta IA:</strong> A região Sudeste registrou o maior número de internações, representando 39,2% do total nacional.
                        </div>
                    </div>
                    <input type="text" placeholder="Faça uma pergunta..." style="width: 100%; background: #070913; border: 1px solid rgba(168, 85, 247, 0.3); padding: 10px; border-radius: 6px; color: white; font-size: 11px; outline: none;" disabled>
                </div>
            """, unsafe_allow_html=True)