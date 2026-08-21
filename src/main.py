import streamlit as st
from view.sidebar_view import SidebarView
from view.dashboard_view import DashboardView
from view.assistente_ia_view import AssistenteIAView
from view.hospitais_view import HospitaisView
from view.generico_view import GenericoView

st.set_page_config(page_title="Vitta Vision", layout="wide")

# CSS Global limpo para o app inteiro
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
            border-right: 1px solid rgba(168, 85, 247, 0.2);
        }
        .metric-card {
            background: linear-gradient(145deg, #121826 0%, #1a102f 100%);
            border: 1px solid rgba(168, 85, 247, 0.3);
            padding: 20px;
            border-radius: 14px;
            box-shadow: 0 8px 24px rgba(139, 92, 246, 0.15);
        }
        h1, h2, h3 { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

class MainController:
    def __init__(self):
        # Instancie seu Model aqui se necessário
        self.model = self.carregar_model()

    def carregar_model(self):
        # Mock rápido apenas para exemplo caso precise
        class ModelMock:
            def get_kpis_ia(self): return {"perguntas": 142, "respostas": 138, "tempo": "0.8s", "precisao": "98.4%"}
            def get_internacoes_data(self):
                import pandas as pd
                return pd.DataFrame({"Data": ["Jan", "Fev", "Mar", "Abr"], "Valores": [120, 150, 110, 170]})
            def get_hospitais_data(self):
                import pandas as pd
                return pd.DataFrame({"Hospital": ["H. Central", "H. Norte"], "Leitos": [150, 80]})
        return ModelMock()

    def run(self):
        # Renderiza a Sidebar e pega a opção escolhida
        sidebar = SidebarView()
        pagina_atual = sidebar.render()

        # Faz o roteamento limpo para cada arquivo de view correspondente
        if pagina_atual == "Dashboard":
            DashboardView().render(self.model)
        elif pagina_atual == "Assistente IA":
            AssistenteIAView().render(self.model)
        elif pagina_atual == "Hospitais":
            HospitaisView().render(self.model)
        else:
            GenericoView().render(pagina_atual)

if __name__ == "__main__":
    app = MainController()
    app.run()