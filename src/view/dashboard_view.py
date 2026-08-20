import streamlit as st

class DashboardView:
    def render(self, df, on_slider_change):
        st.title("🚀 VittaVision - Teste de Tela MVC")
        st.write("Se você está vendo isso na web, a sua arquitetura MVC está funcionando perfeitamente!")
        
        # Barra lateral (Sidebar) para interação
        st.sidebar.header("Filtros do Dashboard")
        filtro_valor = st.sidebar.slider("Filtrar por Valor Mínimo (R$)", min_value=0, max_value=3000, value=0, step=100)
        
        # Métricas rápidas no topo
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Total de Registros", value=len(df))
        with col2:
            st.metric(label="Soma Total (R$)", value=f"R$ {df['Valor'].sum():,.2f}")

        # Tabela de dados
        st.subheader("📊 Dados Filtrados")
        st.dataframe(df, use_container_width=True)

        # Gráfico interativo
        st.subheader("📈 Desempenho por Categoria")
        if not df.empty:
            chart_data = df.groupby("Categoria")["Valor"].sum()
            st.bar_chart(chart_data)
        else:
            st.warning("Nenhum dado encontrado com esse filtro.")
            
        return filtro_valor