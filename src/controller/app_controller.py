from src.model.dataframe_model import DataframeModel
from src.view.dashboard_view import DashboardView

class AppController:
    def __init__(self):
        self.model = DataframeModel()
        self.view = DashboardView()

    def run(self):
        # 1. Pede o valor do filtro para a View (slider)
        # Como o Streamlit executa o script de cima a baixo a cada interação, 
        # pegamos o valor inicial ou atual do componente renderizado.
        
        # Para simplificar na primeira chamada, definimos um valor padrão ou capturamos da View:
        # Vamos renderizar a view primeiro para pegar o input do usuário:
        
        # Abordagem reativa limpa:
        import streamlit as st
        
        st.sidebar.header("Painel de Controle MVC")
        min_valor = st.sidebar.slider("Valor Mínimo (R$)", 0, 3000, 0, 100)
        
        # 2. Busca os dados filtrados no Model
        df = self.model.get_data(min_valor=min_valor)
        
        # 3. Renderiza os componentes na View
        st.title("🚀 VittaVision - MVC com Streamlit")
        st.write("Arquitetura Model-View-Controller rodando com sucesso na web!")
        
        col1, col2 = st.columns(2)
        col1.metric("Registros Exibidos", len(df))
        col2.metric("Valor Acumulado", f"R$ {df['Valor'].sum():,.2f}")
        
        st.dataframe(df, use_container_width=True)
        
        if not df.empty:
            st.bar_chart(df.set_index("Produto")["Valor"])