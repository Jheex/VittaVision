import streamlit as st
import pandas as pd
import io

class RelatoriosView:
    def render(self, model=None):
        # Cabeçalho da Seção
        st.markdown("""
            <div style="margin-bottom: 25px;">
                <h2 style="color: #f8fafc; font-weight: 700; margin-bottom: 5px;">📊 Relatórios Gerenciais</h2>
                <p style="color: #94a3b8; font-size: 14px;">Central de consolidação de dados estratégicos, indicadores de desempenho e exportação.</p>
            </div>
        """, unsafe_allow_html=True)

        # Inicializa o estado no session_state para controlar se a consulta foi feita
        if "consultar_relatorio" not in st.session_state:
            st.session_state.consultar_relatorio = False

        # Bloco de Configuração de Filtros
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 16px; margin-bottom: 20px;">
                <h4 style="color: #e2e8f0; font-size: 15px; margin-bottom: 15px;">1. Configuração do Relatório</h4>
        """, unsafe_allow_html=True)

        # Carregamento prévio rápido para popular os selects
        try:
            df_internacoes = pd.read_csv('internacoes.csv', sep=';', encoding='latin1')
            df_internacoes = df_internacoes.rename(columns={df_internacoes.columns[0]: 'ID_MUN'})
        except Exception:
            df_internacoes = pd.DataFrame()

        col1, col2, col3 = st.columns(3)
        with col1:
            tipo_relatorio = st.selectbox("Tipo de Relatório", [
                "Fluxo de Internações (2025)", 
                "Panorama de Leitos e UTIs", 
                "Indicadores Populacionais"
            ])
        with col2:
            ufs_disponiveis = ["TODAS"] + sorted(df_internacoes['UF'].dropna().unique().tolist()) if not df_internacoes.empty else ["TODAS"]
            uf_selecionada = st.selectbox("Estado (UF)", options=ufs_disponiveis)
        with col3:
            if uf_selecionada != "TODAS" and not df_internacoes.empty:
                municipios_disponiveis = ["TODOS"] + sorted(df_internacoes[df_internacoes['UF'] == uf_selecionada]['MUNICIPIO'].dropna().unique().tolist())
            else:
                municipios_disponiveis = ["TODOS"]
            municipio_selecionado = st.selectbox("Setor / Unidade (Município)", options=municipios_disponiveis)

        # Botão de Consultar isolado
        col_btn_acao, _ = st.columns([1, 4])
        with col_btn_acao:
            if st.button("🔍 Consultar Dados", use_container_width=True, type="primary"):
                st.session_state.consultar_relatorio = True

        st.markdown("</div>", unsafe_allow_html=True)

        # Exibição dos resultados apenas após o clique em "Consultar Dados"
        if st.session_state.consultar_relatorio:
            
            # Carregamento completo dos arquivos conforme a escolha
            try:
                if tipo_relatorio == "Fluxo de Internações (2025)":
                    df_relatorio = pd.read_csv('internacoes.csv', sep=';', encoding='latin1')
                    df_relatorio = df_relatorio.rename(columns={df_relatorio.columns[0]: 'ID_MUN'})
                elif tipo_relatorio == "Panorama de Leitos e UTIs":
                    df_relatorio = pd.read_csv('leitos.csv', sep=';', encoding='latin1')
                    df_relatorio = df_relatorio.rename(columns={df_relatorio.columns[0]: 'COMP'})
                else:
                    df_relatorio = pd.read_csv('populacao.csv', sep=';', encoding='latin1')
                    df_relatorio = df_relatorio.rename(columns={df_relatorio.columns[0]: 'UF_SIGLA'})
            except Exception:
                df_relatorio = pd.DataFrame()

            # Aplicação dos filtros se aplicável ao dataframe carregado
            if not df_relatorio.empty:
                if uf_selecionada != "TODAS":
                    if 'UF' in df_relatorio.columns:
                        df_relatorio = df_relatorio[df_relatorio['UF'] == uf_selecionada]
                    elif 'UF_SIGLA' in df_relatorio.columns:
                        df_relatorio = df_relatorio[df_relatorio['UF_SIGLA'] == uf_selecionada]
                
                if municipio_selecionado != "TODOS" and 'MUNICIPIO' in df_relatorio.columns:
                    df_relatorio = df_relatorio[df_relatorio['MUNICIPIO'] == municipio_selecionado]

            # Bloco de Pré-visualização da Tabela
            st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 16px; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h4 style="color: #e2e8f0; font-size: 15px; margin: 0;">2. Resultado da Consulta e Sumário Executivo</h4>
                        <span style="background: rgba(168, 85, 247, 0.1); color: #c084fc; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;">Status: Pronto para Download</span>
                    </div>
            """, unsafe_allow_html=True)

            if not df_relatorio.empty:
                st.dataframe(df_relatorio.head(100), use_container_width=True, hide_index=True)
            else:
                st.warning("Nenhum registro encontrado para os parâmetros selecionados.")

            st.markdown("</div>", unsafe_allow_html=True)

            # Bloco de Opções de Download
            st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 16px;">
                    <h4 style="color: #e2e8f0; font-size: 15px; margin-bottom: 15px;">3. Exportar Documentação</h4>
            """, unsafe_allow_html=True)

            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                csv_bytes = df_relatorio.to_csv(index=False).encode('utf-8') if not df_relatorio.empty else b""
                st.download_button(
                    label="📄 Baixar Relatório (CSV)",
                    data=csv_bytes,
                    file_name="relatorio_vitta_vision.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_btn2:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df_relatorio.to_excel(writer, index=False, sheet_name='Relatorio')
                excel_bytes = output.getvalue()
                
                st.download_button(
                    label="📊 Exportar Planilha (Excel)",
                    data=excel_bytes,
                    file_name="relatorio_vitta_vision.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            with col_btn3:
                if st.button("📧 Enviar por E-mail à Diretoria", use_container_width=True):
                    st.success("Relatório sintetizado enviado com sucesso para a diretoria!")

            st.markdown("</div>", unsafe_allow_html=True)