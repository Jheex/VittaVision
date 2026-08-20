from model.dataframe_model import DataframeModel
from view.dashboard_view import DashboardView

class AppController:
    def __init__(self):
        self.model = DataframeModel()
        self.view = DashboardView()

    def run(self):
        self.view.render(self.model)