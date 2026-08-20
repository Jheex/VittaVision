import pandas as pd

class DataframeModel:
    def get_kpis_ia(self):
        return {
            "perguntas": "1.256",
            "respostas": "1.256",
            "tempo": "1,8s",
            "precisao": "96%"
        }

    def get_internacoes_data(self):
        data = {
            "Data": ["24/04", "25/04", "26/04", "27/04", "28/04", "29/04", "30/04"],
            "Internacoes": [1200, 1800, 2200, 2400, 2900, 2700, 3100]
        }
        return pd.DataFrame(data)

    def get_hospitais_data(self):
        data = {
            "Hospital": ["Hospital Central", "São Lucas", "Santa Maria", "Rede Vida", "Hospital Municipal"],
            "Leitos Disponíveis": [12, 5, 20, 8, 3],
            "Ocupação (%)": [85, 92, 65, 78, 95],
            "Status": ["Alerta", "Crítico", "Normal", "Estável", "Crítico"]
        }
        return pd.DataFrame(data)

    def get_mapa_data(self):
        data = {
            "lat": [-23.6821, -23.5505, -23.6000, -23.5200],
            "lon": [-46.6219, -46.6333, -46.5500, -46.6100],
            "Local": ["Unidade Centro", "Unidade Norte", "Unidade Sul", "Unidade Leste"]
        }
        return pd.DataFrame(data)