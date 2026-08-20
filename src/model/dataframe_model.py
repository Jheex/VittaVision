import pandas as pd

class DataframeModel:
    def get_dashboard_data(self, categoria_selecionada="Todas"):
        data = {
            "Data": ["2026-08-01", "2026-08-02", "2026-08-03", "2026-08-04", "2026-08-05", "2026-08-06", "2026-08-07"],
            "Categoria": ["Tecnologia", "Marketing", "Vendas", "Tecnologia", "Vendas", "Marketing", "Tecnologia"],
            "Produto": ["Software Pro", "Campanha A", "Lead Direto", "Cloud Server", "Lead Premium", "Campanha B", "API Gateway"],
            "Receita": [4500, 1800, 3200, 7500, 2900, 1500, 6000],
            "Clientes": [15, 8, 12, 25, 10, 6, 20]
        }
        df = pd.DataFrame(data)
        df["Data"] = pd.to_datetime(df["Data"])
        if categoria_selecionada != "Todas":
            df = df[df["Categoria"] == categoria_selecionada]
        return df

    def get_hospitais_data(self):
        data = {
            "Hospital": ["Hospital Central", "São Lucas", "Santa Maria", "Rede Vida"],
            "Leitos Disponíveis": [12, 5, 20, 8],
            "Ocupação (%)": [85, 92, 65, 78],
            "Status": ["Alerta", "Crítico", "Normal", "Estável"]
        }
        return pd.DataFrame(data)

    def get_mapa_data(self):
        # Coordenadas geográficas simuladas (ex: região de São Paulo/Diadema)
        data = {
            "lat": [-23.6821, -23.5505, -23.6000],
            "lon": [-46.6219, -46.6333, -46.5500],
            "Local": ["Unidade Centro", "Unidade Norte", "Unidade Sul"]
        }
        return pd.DataFrame(data)