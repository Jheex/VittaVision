import streamlit as st

class DashboardView:
    def render(self, model):
        # 1. Injeção de CSS personalizado para o tema Dark/Cyberpunk da VittaVision
        st.markdown("""
            <style>
                /* Fundo global escuro */
                .stApp {
                    background-color: #0b0f19;
                    color: #ffffff;
                }
                /* Barra lateral escura */
                [data-testid="stSidebar"] {
                    background-color: #070913;
                    border-right: 1px solid #1e1e2f;
                }
                /* Estilização dos blocos/cards */
                .metric-card {
                    background-color: #121826;
                    border: 1px solid #1f293d;
                    padding: 18px;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                }
                /* Ajuste de textos e títulos */
                h1, h2, h3 {
                    color: #ffffff !important;
                }
            </style>
        """, unsafe_allow_html=True)

        # 2. Menu lateral customizado (Sidebar)
        st.sidebar.markdown("### 💠 **VITTA VISION**")
        st.sidebar.caption("Inteligência que transforma a saúde")
        st.sidebar.markdown("---")

        menu = st.sidebar.radio(
            "Menu Principal",
            ["Dashboard", "Internações", "Hospitais", "Leitos", "Indicadores", "Mapas", "Relatórios", "Assistente IA", "Configurações"]
        )

        st.sidebar.markdown("---")
        st.sidebar.markdown("👤 **Gestor de Saúde**\n*Secretaria Municipal*")

        # 3. Roteamento das telas
        if menu == "Assistente IA" or menu == "Dashboard":
            self.render_assistente_ia(model)
        elif menu == "Hospitais":
            self.render_hospitais(model)
        elif menu == "Mapas":
            self.render_mapas(model)
        else:
            self.render_generico(menu)

    def render_assistente_ia(self, model):
        # Cabeçalho da página
        col_title, col_date, col_btn = st.columns([3, 1, 1])
        with col_title:
            st.title("✨ Assistente IA")
            st.caption("Inteligência artificial que responde e analisa dados do SUS em linguagem natural.")
        with col_date:
            st.selectbox("Período", ["01/01/2024 - 30/04/2026"])
        with col_btn:
            st.button("✨ Novo chat", type="primary")

        # Cards de KPIs no topo (Estilo da Imagem)
        kpis = model.get_kpis_ia()
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""
                <div class="metric-card">
                    <p style="color: #9ca3af; font-size: 14px; margin-bottom: 4px;">Perguntas realizadas</p>
                    <h3 style="margin: 0; font-size: 24px;">{kpis['perguntas']}</h3>
                    <p style="color: #10b981; font-size: 12px; margin-top: 4px;">↑ 18,7% vs mês anterior</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <div class="metric-card">
                    <p style="color: #9ca3af; font-size: 14px; margin-bottom: 4px;">Respostas geradas</p>
                    <h3 style="margin: 0; font-size: 24px;">{kpis['respostas']}</h3>
                    <p style="color: #10b981; font-size: 12px; margin-top: 4px;">↑ 18,7% vs mês anterior</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
                <div class="metric-card">
                    <p style="color: #9ca3af; font-size: 14px; margin-bottom: 4px;">Tempo médio de resposta</p>
                    <h3 style="margin: 0; font-size: 24px;">{kpis['tempo']}</h3>
                    <p style="color: #10b981; font-size: 12px; margin-top: 4px;">↓ 0,4s vs mês anterior</p>
                </div>
            """, unsafe_allow_html=True)
            
        with c4:
            st.markdown(f"""
                <div class="metric-card">
                    <p style="color: #9ca3af; font-size: 14px; margin-bottom: 4px;">Precisão das respostas</p>
                    <h3 style="margin: 0; font-size: 24px;">{kpis['precisao']}</h3>
                    <p style="color: #10b981; font-size: 12px; margin-top: 4px;">↑ 3% vs mês anterior</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Layout dividindo Gráficos à esquerda e Chat IA à direita
        col_main, col_chat = st.columns([2, 1])

        with col_main:
            st.markdown("### Análises em destaque")
            st.radio("Filtro Gráfico", ["Internações", "Leitos", "Ocupação", "Mortalidade"], horizontal=True)
            
            # Gráfico de internações
            df_int = model.get_internacoes_data()
            st.line_chart(df_int.set_index("Data"), color="#a855f7")

            # Mini cards inferiores
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
            
            # Caixa de chat simulada
            st.chat_message("user").write("Quais regiões estão com maior taxa de ocupação de leitos no momento?")
            st.chat_message("assistant").write("Atualmente, as regiões com maior taxa de ocupação são:\n\n1. **Sudeste** — 89%\n2. **Nordeste** — 74%\n3. **Sul** — 72%")
            
            st.warning("⚠️ 15 regiões estão em nível crítico (acima de 90% de ocupação).")
            
            # Input de chat na parte inferior
            st.text_input("Faça uma pergunta sobre os dados do SUS...", placeholder="Digite aqui...")

    def render_hospitais(self, model):
        st.title("🏥 Gestão de Hospitais")
        st.write("Listagem completa de leitos, status e unidades conectadas.")
        df = model.get_hospitais_data()
        st.dataframe(df, use_container_width=True)

    def render_mapas(self, model):
        st.title("🗺️ Mapas de Atendimento")
        df = model.get_mapa_data()
        st.map(df)

    def render_generico(self, nome):
        st.title(f"📁 Módulo: {nome}")
        st.write("Esta seção está sendo estruturada com novas visualizações em breve.")