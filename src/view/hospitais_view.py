import streamlit as st

class HospitaisView:
    def render(self, model):
        st.title("🏥 Gestão de Hospitais")
        st.caption("Lista detalhada das unidades de atendimento cadastradas.")
        
        df = model.get_hospitais_data()
        st.dataframe(df, use_container_width=True)