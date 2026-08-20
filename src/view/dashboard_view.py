import streamlit as st
import importlib.util

# Verifica a biblioteca com segurança
if importlib.util.find_spec("streamlit_option_menu") is None:
    st.error("A biblioteca 'streamlit-option-menu' não está instalada. Rode: pip install streamlit-option-menu")
else:
    from streamlit_option_menu import option_menu

class DashboardView:
    def render(self, model):
        # 1. CSS Global do App e Cartões
        st.markdown("""
            <style>
                .stApp {
                    background: linear-gradient(135deg, #070913 0%, #0b0f19 50%, #110c24 100%);
                    color: #ffffff;
                }
                
                /* Estilo do fundo da barra lateral */
                [data-testid="stSidebar"] {
                    background: linear-gradient(180deg, #070913 0%, #0d061a 100%);
                    border-right: 1px solid rgba(168, 85, 247, 0.2);
                    padding-top: 0.5rem;
                }

                .metric-card {
                    background: linear-gradient(145deg, #121826 0%, #1a102f 100%);
                    border: 1px solid rgba(168, 85, 247, 0.3);
                    padding: 20px;
                    border-radius: 14px;
                    box-shadow: 0 8px 24px rgba(139, 92, 246, 0.15);
                }
                
                .stTextInput input, .stSelectbox select {
                    background-color: #121826 !important;
                    color: #ffffff !important;
                    border: 1px solid rgba(168, 85, 247, 0.3) !important;
                    border-radius: 10px !important;
                }
                .stAlert {
                    background-color: #121826 !important;
                    border: 1px solid rgba(168, 85, 247, 0.3) !important;
                    border-radius: 10px !important;
                    color: #ffffff !important;
                }
                h1, h2, h3 { color: #ffffff !important; }
            </style>
        """, unsafe_allow_html=True)

        # =========================================================
        # ESTRUTURA DA SIDEBAR COM BOTÕES MODERNOS E GRADIENTE
        # =========================================================
        with st.sidebar:
            # Logo / Topo da Sidebar
            st.markdown("""
                <div style="display: flex; align-items: center; gap: 12px; padding: 10px 5px 20px 5px; border-bottom: 1px solid rgba(168, 85, 247, 0.2); margin-bottom: 15px;">
                    <div style="background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%); width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);">💠</div>
                    <div>
                        <h2 style="margin: 0; font-size: 17px; font-weight: 700; color: #ffffff; letter-spacing: 0.5px;">VITTA VISION</h2>
                        <p style="margin: 0; font-size: 11px; color: #9ca3af;">Inteligência em Saúde</p>
                    </div>
                </div>
                <p style="color: #9ca3af; font-size: 11px; font-weight: 600; letter-spacing: 1px; margin-bottom: 8px; padding-left: 5px;">MENU PRINCIPAL</p>
            """, unsafe_allow_html=True)

            # MENU COM BOTÕES ESTILIZADOS
            menu = option_menu(
                menu_title=None,
                options=["Dashboard", "Internações", "Hospitais", "Leitos", "Indicadores", "Mapas", "Relatórios", "Assistente IA", "Configurações"],
                icons=['speedometer2', 'hospital', 'building', 'bed', 'graph-up-arrow', 'map', 'file-text', 'robot', 'gear'],
                menu_icon=None,
                default_index=0,
                styles={
                    "container": {"padding": "0px", "background-color": "transparent"},
                    "icon": {"color": "#a855f7", "font-size": "16px"}, 
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left",
                        "margin": "4px 0px",
                        "--hover-color": "rgba(139, 92, 246, 0.15)",
                        "padding": "10px 14px",
                        "border-radius": "10px",
                        "background-color": "#121826",
                        "color": "#9ca3af",
                        "border": "1px solid rgba(168, 85, 247, 0.15)"
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%)",
                        "color": "#ffffff",
                        "font-weight": "600",
                        "border": "1px solid rgba(255, 255, 255, 0.2)",
                        "box-shadow": "0 4px 15px rgba(139, 92, 246, 0.4)"
                    },
                }
            )

            # PERFIL DO USUÁRIO NO RODAPÉ DA SIDEBAR
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div style="background: rgba(18, 24, 38, 0.7); border: 1px solid rgba(168, 85, 247, 0.3); padding: 12px 15px; border-radius: 12px; display: flex; align-items: center; gap: 10px;">
                    <div style="background-color: #8b5cf6; color: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 13px;">JS</div>
                    <div>
                        <h4 style="margin: 0; font-size: 13px; color: #ffffff;">Gestor de Saúde</h4>
                        <p style="margin: 0; font-size: 11px; color: #9ca3af;">Secretaria Municipal</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # =========================================================
        # ROTEAMENTO DE TELAS
        # =========================================================
        if menu == "Assistente IA" or menu == "Dashboard":
            self.render_assistente_ia(model)
        elif menu == "Hospitais":
            self.render_hospitais(model)
        elif menu == "Mapas":
            self.render_mapas(model)
        else:
            self.render_generico(menu)

    def render_assistente_ia(self, model):
        col_title, col_date, col_btn = st.columns([3, 1, 1])
        with col_title:
            st.title("✨ Assistente IA")
            st.caption("Inteligência artificial que responde e analisa dados do SUS em linguagem natural.")
        with col_date:
            st.selectbox("Período", ["01/01/2024 - 30/04/2026"], label_visibility="collapsed")
        with col_btn:
            st.button("✨ Novo chat", key="btn_novo_chat")

        kpis = model.get_kpis_ia()
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""
                <div class="metric-card">
                    <p style="color: #9ca3af; font-size: 13px; margin-bottom: 4px;">Perguntas realizadas</p>
                    <h3 style="margin: 0; font-size: 22px;">{kpis['perguntas']}</h3>
                    <p style="color: #10b981; font-size: 12px; margin-top: 4px;">↑ 18,7% vs mês anterior</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <div class="metric-card">
                    <p style="color: #9ca3af; font-size: 13px; margin-bottom: 4px;">Respostas geradas</p>
                    <h3 style="margin: 0; font-size: 22px;">{kpis['respostas']}</h3>
                    <p style="color: #10b981; font-size: 12px; margin-top: 4px;">↑ 18,7% vs mês anterior</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
                <div class="metric-card">
                    <p style="color: #9ca3af; font-size: 13px; margin-bottom: 4px;">Tempo médio de resposta</p>
                    <h3 style="margin: 0; font-size: 22px;">{kpis['tempo']}</h3>
                    <p style="color: #10b981; font-size: 12px; margin-top: 4px;">↓ 0,4s vs mês anterior</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c4:
            st.markdown(f"""
                <div class="metric-card">
                    <p style="color: #9ca3af; font-size: 13px; margin-bottom: 4px;">Precisão das respostas</p>
                    <h3 style="margin: 0; font-size: 22px;">{kpis['precisao']}</h3>
                    <p style="color: #10b981; font-size: 12px; margin-top: 4px;">↑ 3% vs mês anterior</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_main, col_chat = st.columns([2, 1])

        with col_main:
            st.markdown("### Análises em destaque")
            st.radio("Filtro Gráfico", ["Internações", "Leitos", "Ocupação", "Mortalidade"], horizontal=True, label_visibility="collapsed")
            
            df_int = model.get_internacoes_data()
            st.line_chart(df_int.set_index("Data"), color="#a855f7")

            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.info("🚨 **Alerta de ocupação**\n15 regiões acima de 90%.")
            with mc2:
                st.info("📈 **Tendência**\nPermanência média aumentou.")
            with mc3:
                st.info("🔮 **Previsão IA**\nDemanda deve subir 12%.")

        with col_chat:
            st.markdown("### 🤖 Assistente Vitta IA")
            st.caption("BETA")
            
            st.chat_message("user").write("Quais regiões estão com maior taxa de ocupação de leitos no momento?")
            st.chat_message("assistant").write("Atualmente, as regiões com maior taxa de ocupação são:\n\n1. **Sudeste** — 89%\n2. **Nordeste** — 74%\n3. **Sul** — 72%")
            
            st.warning("⚠️ 15 regiões estão em nível crítico (acima de 90% de ocupação).")
            st.text_input("Faça uma pergunta...", placeholder="Digite aqui...", label_visibility="collapsed")

    def render_hospitais(self, model):
        st.title("🏥 Gestão de Hospitais")
        df = model.get_hospitais_data()
        st.dataframe(df, use_container_width=True)

    def render_mapas(self, model):
        st.title("🗺️ Mapas de Atendimento")
        df = model.get_mapa_data()
        st.map(df)

    def render_generico(self, nome):
        st.title(f"📁 Módulo: {nome}")
        st.write("Módulo em desenvolvimento.")