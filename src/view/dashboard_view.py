import streamlit as st

class DashboardView:
    def render(self, df):
        # Cabeçalho principal
        st.title("📊 VittaVision - Dashboard Executivo")
        st.markdown("Visão geral de desempenho, receitas e métricas em tempo real.")
        st.markdown("---")

        # Verificação se há dados
        if df.empty:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")
            return

        # Métricas principais (KPIs) no topo
        total_receita = df["Receita"].sum()
        total_clientes = df["Clientes"].sum()
        ticket_medio = total_receita / total_clientes if total_clientes > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="💰 Receita Total", value=f"R$ {total_receita:,.2f}")
        with col2:
            st.metric(label="👥 Total de Clientes", value=f"{total_clientes}")
        with col3:
            st.metric(label="📈 Ticket Médio", value=f"R$ {ticket_medio:,.2f}")

        st.markdown("---")

        # Layout em duas colunas para os gráficos
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            st.subheader("Receita por Categoria")
            if not df.empty:
                receita_categoria = df.groupby("Categoria")["Receita"].sum()
                st.bar_chart(receita_categoria)

        with col_graf2:
            st.subheader("Clientes por Categoria")
            if not df.empty:
                clientes_categoria = df.groupby("Categoria")["Clientes"].sum()
                st.line_chart(clientes_categoria)

        # Seção da Tabela de Dados Detalhados
        st.markdown("---")
        st.subheader("📋 Detalhamento dos Registros")
        st.dataframe(df, use_container_width=True)