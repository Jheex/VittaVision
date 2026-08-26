import pandas as pd
import streamlit as st
from view.assistente_ia_view import AssistenteIAView
from view.dashboard_view import DashboardView
from view.generico_view import GenericoView
from view.header_component import HeaderComponent
from view.hospitais_view import HospitaisView
from view.internacoes_view import InternacoesView
from view.leitos_view import LeitosView
from view.mapas_view import MapasView
from view.relatorios_view import RelatoriosView

st.set_page_config(
    page_title="Vitta Vision", layout="wide", initial_sidebar_state="expanded"
)

# Força o estado da sidebar no session_state para evitar que fique presa no cache do navegador
if "sidebar_state" not in st.session_state:
  st.session_state.sidebar_state = "expanded"

# CSS Global aprimorado
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(135deg, #070913 0%, #0b0f19 50%, #110c24 100%);
            color: #ffffff;
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
""",
    unsafe_allow_html=True,
)


class MainController:

  def __init__(self):
    self.model = self.carregar_model()
    self.header = HeaderComponent()

  def carregar_model(self):

    class ModelMock:

      def get_kpis_ia(self):
        return {
            "perguntas": 142,
            "respostas": 138,
            "tempo": "0.8s",
            "precisao": "98.4%",
        }

      def get_internacoes_data(self):
        return pd.DataFrame({
            "Data": [
                "Jan/24",
                "Abr/24",
                "Jul/24",
                "Out/24",
                "Jan/25",
                "Abr/25",
                "Jul/25",
                "Out/25",
                "Abr/26",
            ],
            "Valores": [100, 115, 130, 125, 140, 160, 190, 175, 120],
        })

      def get_hospitais_data(self):
        return pd.DataFrame({
            "Hospital": ["H. Central", "H. Norte", "H. Sul", "H. Leste"],
            "Leitos": [150, 80, 120, 95],
        })

    return ModelMock()

  def run(self):
    params = st.query_params
    pagina_atual = params.get("page", "Dashboard")

    self.header.render(pagina_atual)

    # Roteamento de páginas
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
    elif pagina_atual == "Mapas":
      MapasView().render()
    elif pagina_atual == "Relatórios":
      RelatoriosView().render(self.model)
    else:
      GenericoView().render(pagina_atual)


if __name__ == "__main__":
  app = MainController()
  app.run()