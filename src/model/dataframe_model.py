import pandas as pd

class DataframeModel:
    def get_data(self, categoria_selecionada="Todas"):
        # Dados simulados mais ricos para o Dashboard
        data = {
            "Data": ["2026-08-01", "2026-08-02", "2026-08-03", "2026-08-04", "2026-08-05", "2026-08-06", "2026-08-07"],
            "Categoria": ["Tecnologia", "Marketing", "Vendas", "Tecnologia", "Vendas", "Marketing", "Tecnologia"],
            "Produto": ["Software Pro", "Campanha A", "Lead Direto", "Cloud Server", "Lead Premium", "Campanha B", "API Gateway"],
            "Receita": [4500, 1800, 3200, 7500, 2900, 1500, 6000],
            "Clientes": [15, 8, 12, 25, 10, 6, 20]
        }
        df = pd.DataFrame(data)
        df["Data"] = pd.to_datetime(df["Data"])

        # Aplicando filtro por categoria se houver seleção
        if categoria_selecionada != "Todas":
            df = df[df["Categoria"] == categoria_selecionada]
            
        return df