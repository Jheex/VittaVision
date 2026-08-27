import streamlit as st

class DatabaseView:
    """View responsável pelo status e testes de conexão com o banco de dados."""

    def render(self, db):
        st.subheader("🗄️ Módulo de Banco de Dados")
        st.write("Status da conexão com o Oracle Autonomous Database ativo.")
        if st.button("Testar Conexão com Oracle"):
            try:
                conn = db._conectar()
                conn.close()
                st.success("Conexão estabelecida com sucesso!")
            except Exception as e:
                st.error(f"Falha na conexão: {e}")