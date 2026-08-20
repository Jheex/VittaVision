import streamlit as st

class DashboardView:
    def render(self, df):
        st.title("🚀 VittaVision - MVC com Streamlit")
        st.write("Arquitetura Model-View-Controller rodando com sucesso na web!")
        
        col1, col2 = st.columns(2)
        col1.metric("Registros Exibidos", len(df))
        col2.metric("Valor Acumulado", f"R$ {df['Valor'].sum():,.2f}")
        
        st.dataframe(df, use_container_width=True)
        
        if not df.empty:
            st.bar_chart(df.set_index("Produto")["Valor"])
        else:
            st.warning("Nenhum dado encontrado com esse filtro.")