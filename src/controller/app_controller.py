import streamlit as st
from model.dataframe_model import DataframeModel
from view.dashboard_view import DashboardView

class AppController:
    def __init__(self):
        self.model = DataframeModel()
        self.view = DashboardView()

    def run(self):
        # Configurações da Barra Lateral (Filtros do Dashboard)
        st.sidebar.header("🔍 Filtros Globais")
        
        # Opções de categorias baseadas nos dados
        categorias = ["Todas", "Tecnologia", "Marketing", "Vendas"]
        categoria_escolhida = st.sidebar.selectbox("Filtrar por Categoria", categorias)
        
        st.sidebar.markdown("---")
        st.sidebar.info("Dashboard atualizado via arquitetura MVC.")

        # Busca os dados filtrados no Model
        df_filtrado = self.model.get_data(categoria_selecionada=categoria_escolhida)
        
        # Renderiza a View passando os dados tratados
        self.view.render(df_filtrado)