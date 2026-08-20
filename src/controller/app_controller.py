from model.dataframe_model import DataframeModel
from view.dashboard_view import DashboardView

class AppController:
    def __init__(self):
        self.model = DataframeModel()
        self.view = DashboardView()

    def run(self):
        # O Controller delega a renderização principal para a View, 
        # que gerencia o menu lateral e a troca de telas (Dashboard, IA, Hospitais, Mapa).
        self.view.render(None, self.model)