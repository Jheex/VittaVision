import streamlit as st

class DashboardView:
    def render(self, menu_selecionado, model):
        st.sidebar.title("🏥 VittaVision")
        st.sidebar.markdown("---")

        # Menu lateral com as 4 funções solicitadas
        menu = st.sidebar.radio("Navegação", ["DASHBOARD", "IA", "HOSPITAIS", "MAPA"])
        
        st.sidebar.markdown("---")
        st.sidebar.info("Sistema MVC Ativo na Web 🚀")

        # Roteamento das telas
        if menu == "DASHBOARD":
            self.render_dashboard(model)
        elif menu == "IA":
            self.render_ia()
        elif menu == "HOSPITAIS":
            self.render_hospitais(model)
        elif menu == "MAPA":
            self.render_mapa(model)

    def render_dashboard(self, model):
        st.title("📊 VittaVision - Dashboard Executivo")
        
        categoria = st.selectbox("Filtrar Categoria", ["Todas", "Tecnologia", "Marketing", "Vendas"])
        df = model.get_dashboard_data(categoria)

        total_receita = df["Receita"].sum()
        total_clientes = df["Clientes"].sum()

        col1, col2 = st.columns(2)
        col1.metric("💰 Receita Total", f"R$ {total_receita:,.2f}")
        col2.metric("👥 Total de Clientes", f"{total_clientes}")

        st.markdown("---")
        st.subheader("Receita por Categoria")
        if not df.empty:
            st.bar_chart(df.groupby("Categoria")["Receita"].sum())
        
        st.dataframe(df, use_container_width=True)

    def render_ia(self):
        st.title("🤖 Assistente de IA - Insights")
        st.write("Aqui você poderá interagir com análises preditivas e relatórios gerados por inteligência artificial.")
        
        pergunta = st.text_input("Faça uma pergunta sobre os dados:")
        if st.button("Consultar IA"):
            if pergunta:
                st.success(f"Análise simulada para: '{pergunta}' -> Os indicadores apontam uma tendência de alta nas unidades de tecnologia.")
            else:
                st.warning("Digite uma pergunta para consultar a IA.")

    def render_hospitais(self, model):
        st.title("🏥 Gestão de Hospitais")
        st.write("Monitoramento de leitos, taxas de ocupação e status das unidades.")
        
        df_hosp = model.get_hospitais_data()
        st.dataframe(df_hosp, use_container_width=True)

    def render_mapa(self, model):
        st.title("🗺️ Mapa de Unidades")
        st.write("Localização geográfica das unidades ativas no sistema.")
        
        df_map = model.get_mapa_data()
        st.map(df_map)