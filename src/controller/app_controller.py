import streamlit as st
from model.dataframe_model import DataframeModel
from view.dashboard_view import DashboardView

class AppController:
    def __init__(self):
        self.model = DataframeModel()
        self.view = DashboardView()

    def run(self):
        st.sidebar.header("Painel de Controle")
        min_valor = st.sidebar.slider("Valor Mínimo (R$)", 0, 3000, 0, 100)
        
        df = self.model.get_data(min_valor=min_valor)
        self.view.render(df)