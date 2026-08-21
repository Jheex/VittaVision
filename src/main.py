import streamlit as st
import pandas as pd
from view.sidebar_view import SidebarView
from view.dashboard_view import DashboardView
from view.assistente_ia_view import AssistenteIAView
from view.hospitais_view import HospitaisView
from view.internacoes_view import InternacoesView
from view.leitos_view import LeitosView
from view.generico_view import GenericoView

st.set_page_config(page_title="Vitta Vision", layout="wide", initial_sidebar_state="expanded")

# CSS Global aprimorado para o visual corporativo e moderno
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #070913 0%, #0b0f19 50%, #110c24 100%);
            color: #ffffff;
        }
        [data-testid="stSidebar"] {
            background-color: transparent !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(180deg, #070913 0%, #0d061a 100%) !important;
            border-right: 1px solid rgba(168, 85, 247, 0.15);
        }
        /* Cartões robustos e modernos */
        .metric-card {
            background: linear-gradient(145deg, rgba(18, 24, 38, 0.8) 0%, rgba(26, 16, 47, 0.8) 100%);
            border: 1px solid rgba(168, 85, 247, 0.2);
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            margin-bottom: 16px;
        }
        h1, h2, h3 { color: #ffffff !important; }
        .element-container { margin-bottom: 0px !important; }
    </style>
""", unsafe_allow_html=True)

class MainController:
    def __init__(self):
        self.model = self.carregar_model()

    def carregar_model(self):
        class ModelMock:
            def get_kpis_ia(self): 
                return {"perguntas": 142, "respostas": 138, "tempo": "0.8s", "precisao": "98.4%"}
            
            def get_internacoes_data(self):
                return pd.DataFrame({
                    "Data": ["Jan/24", "Abr/24", "Jul/24", "Out/24", "Jan/25", "Abr/25", "Jul/25", "Out/25", "Abr/26"],
                    "Valores": [100, 115, 130, 125, 140, 160, 190, 175, 120]
                })
            
            def get_hospitais_data(self):
                return pd.DataFrame({
                    "Hospital": ["H. Central", "H. Norte", "H. Sul", "H. Leste"], 
                    "Leitos": [150, 80, 120, 95]
                })
                
        return ModelMock()

    def run(self):
        # Renderiza a Sidebar e pega a opção escolhida
        sidebar = SidebarView()
        pagina_atual = sidebar.render()

        # Roteamento limpo para cada arquivo de view correspondente
        if pagina_atual == "Dashboard":
            DashboardView().render(self.model)
        elif pagina_atual == "Assistente IA":
            AssistenteIAView().render(self.model)
        elif pagina_atual == "Hospitais":
            HospitaisView().render(self.model)
        elif pagina_atual == "Internações":
            InternacoesView().render(self.model)
        elif pagina_atual == "Leitos":
            LeitosView().render(self.model)
        else:
            GenericoView().render(pagina_atual)

if __name__ == "__main__":
    app = MainController()
    app.run()