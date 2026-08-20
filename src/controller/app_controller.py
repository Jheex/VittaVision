import streamlit as st
from src.model.dataframe_model import DataframeModel
from src.view.dashboard_view import DashboardView

class AppController:
    def __init__(self):
        self.model = DataframeModel()
        self.view = DashboardView()

    def run(self):
        # 1. Painel lateral para o filtro
        st.sidebar.header("Painel de Controle")
        min_valor = st.sidebar.slider("Valor Mínimo (R$)", 0, 3000, 0, 100)
        
        # 2. Busca dados no Model
        df = self.model.get_data(min_valor=min_valor)
        
        # 3. Renderiza na View
        self.view.render(df)