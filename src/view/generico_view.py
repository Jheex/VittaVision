import streamlit as st

class GenericoView:
    def render(self, nome_modulo):
        st.title(f"📁 Módulo: {nome_modulo}")
        st.info("Esta seção está em desenvolvimento ou aguardando integração de dados.")