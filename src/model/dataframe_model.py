import pandas as pd

class DataframeModel:
    def get_data(self, min_valor=0):
        data = {
            "Categoria": ["Tecnologia", "Marketing", "Vendas", "Tecnologia", "Vendas", "Marketing"],
            "Produto": ["Software A", "Campanha X", "Lead B", "Cloud Server", "Lead C", "Campanha Y"],
            "Valor": [1500, 800, 1200, 3000, 950, 600],
            "Qtd": [10, 5, 8, 15, 6, 4]
        }
        df = pd.DataFrame(data)
        df_filtered = df[df["Valor"] >= min_valor]
        return df_filtered