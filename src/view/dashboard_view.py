import streamlit as st

class DashboardView:
    def render(self, model):
        # 1. Injeção de CSS aprimorado para estilizar botões, inputs e rádios
        st.markdown("""
            <style>
                /* Fundo global escuro com gradiente */
                .stApp {
                    background: linear-gradient(135deg, #070913 0%, #0b0f19 50%, #110c24 100%);
                    color: #ffffff;
                }
                
                /* Barra lateral estilizada */
                [data-testid="stSidebar"] {
                    background: linear-gradient(180deg, #070913 0%, #0d061a 100%);
                    border-right: 1px solid rgba(168, 85, 247, 0.2);
                }

                /* Cards de Métricas */
                .metric-card {
                    background: linear-gradient(145deg, #121826 0%, #1a102f 100%);
                    border: 1px solid rgba(168, 85, 247, 0.3);
                    padding: 20px;
                    border-radius: 14px;
                    box-shadow: 0 8px 24px rgba(139, 92, 246, 0.15);
                    transition: all 0.3s ease;
                }
                .metric-card:hover {
                    border-color: rgba(168, 85, 247, 0.7);
                    box-shadow: 0 8px 30px rgba(139, 92, 246, 0.4);
                    transform: translateY(-2px);
                }

                /* BOTÕES MODERNOS (Substitui o visual padrão feio) */
                .stButton > button {
                    background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%) !important;
                    color: white !important;
                    border: none !important;
                    border-radius: 10px !important;
                    font-weight: 600 !important;
                    padding: 0.6rem 1.2rem !important;
                    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
                    transition: all 0.3s ease !important;
                }
                .stButton > button:hover {
                    background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
                    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6) !important;
                    transform: scale(1.02);
                }

                /* RÁDIOS E SELETORES EM FORMATO DE PÍLULA/BOTÃO */
                .stRadio > div {
                    background-color: #121826;
                    padding: 6px;
                    border-radius: 12px;
                    border: 1px solid rgba(168, 85, 247, 0.2);
                }
                .stRadio label {
                    color: #d1d5db !important;
                    font-weight: 500;
                }

                /* Caixas de Texto (Inputs do chat) estilizadas */
                .stTextInput input {
                    background-color: #121826 !important;
                    color: #ffffff !important;
                    border: 1px solid rgba(168, 85, 247, 0.3) !important;
                    border-radius: 10px !important;
                }
                .stTextInput input:focus {
                    border-color: #8b5cf6 !important;
                    box-shadow: 0 0 10px rgba(139, 92, 246, 0.3) !important;
                }

                /* Alertas e avisos modernos */
                .stAlert {
                    background-color: #121826 !important;
                    border: 1px solid rgba(168, 85, 247, 0.3) !important;
                    border-radius: 10px !important;
                    color: #ffffff !important;
                }

                h1, h2, h3 {
                    color: #ffffff !important;
                    font-family: 'Inter', sans-serif;
                }
            </style>
        """, unsafe_allow_html=True)

        # 2. Menu lateral (Sidebar)
        st.sidebar.markdown("### 💠 **VITTA VISION**")
        st.sidebar.caption("Inteligência que transforma a saúde")
        st.sidebar.markdown("---")

        menu = st.sidebar.radio(
            "Menu Principal",
            ["Dashboard", "Internações", "Hospitais", "Leitos", "Indicadores", "Mapas", "Relatórios", "Assistente IA", "Configurações"]
        )

        st.sidebar.markdown("---")
        st.sidebar.markdown("👤 **Gestor de Saúde**\n*Secretaria Municipal*")

        # 3. Roteamento de telas
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
            st.button("✨ Novo chat")

        # Cards de KPIs
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