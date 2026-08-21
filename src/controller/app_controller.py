import streamlit as st
from model.dataframe_model import DataframeModel
from view.sidebar_view import SidebarView
from view.dashboard_view import DashboardView
from view.mapas_view import MapasView
from view.internacoes_view import InternacoesView
from view.hospitais_view import HospitaisView
from view.leitos_view import LeitosView
from view.assistente_ia_view import AssistenteIAView

class AppController:
    def __init__(self):
        self.model = DataframeModel()
        self.sidebar = SidebarView()

    def run(self):
        # Renderiza a sidebar e captura qual aba o usuário clicou
        menu_selecionado = self.sidebar.render()

        # Direciona para a view correta com base na seleção
        if menu_selecionado == "Dashboard":
            DashboardView().render(self.model)
            
        elif menu_selecionado == "Mapas":
            MapasView().render()
            
        elif menu_selecionado == "Internações":
            InternacoesView().render()
            
        elif menu_selecionado == "Hospitais":
            Hospitais_View = HospitaisView() if 'HospitaisView' in globals() else None
            HospitaisView().render()
            
        elif menu_selecionado == "Leitos":
            LeitosView().render()
            
        elif menu_selecionado == "Indicadores":
            st.info("Tela de Indicadores em desenvolvimento.")
            
        elif menu_selecionado == "Relatórios":
            st.info("Tela de Relatórios em desenvolvimento.")
            
        elif menu_selecionado == "Assistente IA":
            AssistenteIAView().render()
            
        elif menu_selecionado == "Configurações":
            st.info("Tela de Configurações em desenvolvimento.")