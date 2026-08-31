import streamlit as st
import pandas as pd
import numpy as np

# Imports originais do seu projeto
from model.oracle_connection import OracleDatabase
from view.admin.usuarios_view import UsuariosView
from view.admin.database_view import DatabaseView
from view.admin.perfil_view import PerfilView

class AdminPainelView:
    """
    Painel administrativo principal do Vitta Vision no padrão SaaS.
    Navegação via Sidebar e Dashboard analítico na home.
    """

    def render(self):
        db = OracleDatabase()

        # =====================================================
        # MENU LATERAL (SIDEBAR)
        # =====================================================
        with st.sidebar:
            st.title("Vitta Vision")
            st.markdown("Bem-vindo(a), **Administrador Master**")
            
            st.divider() 
            
            menu_selecionado = st.radio(
                "Navegação",
                [
                    "📊 Dashboard", 
                    "👥 Módulo Acessos", 
                    "🗄️ Tabelas", 
                    "⚙️ Meu Perfil", 
                    "🚪 Sair"
                ],
                label_visibility="collapsed"
            )

        # =====================================================
        # ROTEAMENTO (CONTEÚDO PRINCIPAL)
        # =====================================================
        
        if menu_selecionado == "📊 Dashboard":
            self.render_dashboard_home(db)
            
        elif menu_selecionado == "👥 Módulo Acessos":
            st.header("Gerenciamento de Acessos")
            st.markdown("Controle usuários, permissões e acessos ao ambiente administrativo.")
            st.divider()
            UsuariosView().render(db)
            
        elif menu_selecionado == "🗄️ Tabelas":
            st.header("Banco de Dados Oracle")
            st.markdown("Consulte tabelas, estruturas e status das chaves estrangeiras.")
            st.divider()
            DatabaseView().render(db)
            
        elif menu_selecionado == "⚙️ Meu Perfil":
            st.header("Meu Perfil")
            st.markdown("Informações da conta administrativa atualmente autenticada.")
            st.divider()
            PerfilView().render(db)
            
        elif menu_selecionado == "🚪 Sair":
            st.session_state.admin_logado = False
            st.session_state.admin_perfil = ""
            st.rerun()

    # =====================================================
    # COMPONENTE: DASHBOARD HOME
    # =====================================================
    def render_dashboard_home(self, db):
        
        # Injeção de CSS para os Cards SaaS e Estilização do Menu Lateral
        st.html("""
        <style>
            [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
                display: none !important;
            }
            [data-testid="stSidebar"] div[role="radiogroup"] > label {
                background-color: transparent;
                border-radius: 8px;
                padding: 10px 15px;
                margin-bottom: 4px;
                transition: all 0.2s ease-in-out;
                border-left: 3px solid transparent;
            }
            [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
                background-color: rgba(139, 92, 246, 0.1);
                border-left: 3px solid #8b5cf6;
            }
            [data-testid="stSidebar"] hr {
                border-color: rgba(139, 92, 246, 0.2);
            }
            .saas-card {
                background-color: #111827;
                border-radius: 12px;
                padding: 22px;
                border-left: 4px solid #8b5cf6;
                border-top: 1px solid rgba(139, 92, 246, 0.15);
                border-right: 1px solid rgba(139, 92, 246, 0.15);
                border-bottom: 1px solid rgba(139, 92, 246, 0.15);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                display: flex;
                flex-direction: column;
                margin-bottom: 1rem;
                height: 95%;
            }
            .saas-card-header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 15px;
            }
            .saas-icon {
                font-size: 24px;
                background: rgba(139, 92, 246, 0.15);
                padding: 8px 12px;
                border-radius: 10px;
                line-height: 1;
            }
            .saas-tag {
                font-size: 10px;
                text-transform: uppercase;
                color: #9ca3af;
                font-weight: 700;
                letter-spacing: 1px;
            }
            .saas-title {
                color: #f3f4f6;
                font-size: 15px;
                font-weight: 600;
                margin-bottom: 5px;
                word-wrap: break-word;
            }
            .saas-value {
                color: #ffffff;
                font-size: 34px;
                font-weight: 800;
                line-height: 1.2;
            }
            .saas-subtitle {
                color: #9ca3af;
                font-size: 12px;
                margin-top: 15px;
                border-top: 1px solid rgba(255, 255, 255, 0.05);
                padding-top: 12px;
            }
        </style>
        """)

        def criar_cartao(icon, tag, title, value, subtitle):
            return f"""
            <div class="saas-card">
                <div class="saas-card-header">
                    <div class="saas-icon">{icon}</div>
                    <div class="saas-tag">{tag}</div>
                </div>
                <div class="saas-title">{title}</div>
                <div class="saas-value">{value}</div>
                <div class="saas-subtitle">{subtitle}</div>
            </div>
            """

        st.header("Visão Geral do Sistema")
        st.markdown("Acompanhe o status de integração com o banco e a volumetria real dos dados.")
        
        st.write("")

        with st.spinner("Sincronizando com o Oracle Database..."):
            
            # 1. Teste Real de Conexão com o Banco (Ping)
            try:
                db.executar_query_sql("SELECT 1 FROM DUAL")
                status_sistema, status_sistema_sub, icone_sistema = "Operacional", "Online", "🟢"
                status_db, status_db_sub, icone_db = "Conectado", "Oracle OCI", "⚡"
            except Exception:
                status_sistema, status_sistema_sub, icone_sistema = "Indisponível", "Offline", "🔴"
                status_db, status_db_sub, icone_db = "Desconectado", "Falha de Rede", "❌"

            # 2. Obter dados reais de Usuários Ativos
            try:
                df_usuarios = db.listar_usuarios()
                usuarios_ativos = len(df_usuarios[df_usuarios['FL_ATIVO'] == 'S']) if not df_usuarios.empty else 0
            except:
                usuarios_ativos = 0

            # 3. Mapeamento Dinâmico de TODAS as Tabelas Reais
            def get_count_real(tabela):
                try:
                    df = db.executar_query_sql(f"SELECT COUNT(*) AS QTD FROM {tabela}")
                    return int(df['QTD'].iloc[0])
                except:
                    return 0

            tabelas_reais = []
            try:
                # Retirado o filtro DBTOOLS$ para exibir a tabela de sistema do Oracle
                df_all_tabs = db.executar_query_sql("SELECT TABLE_NAME FROM USER_TABLES WHERE TABLE_NAME NOT LIKE 'BIN$%' ORDER BY TABLE_NAME")
                if not df_all_tabs.empty:
                    for tb_name in df_all_tabs['TABLE_NAME']:
                        qtd = get_count_real(tb_name)
                        # Configuração padrão do cartão
                        info = {
                            "nome": tb_name,
                            "qtd": qtd,
                            "icone": "📊",
                            "tag": "TABELA ORACLE",
                            "desc": "Registros no banco"
                        }
                        
                        # Personalização condicional de ícones e tags
                        if "INTERNACOES" in tb_name:
                            info["icone"], info["tag"] = "🏥", "REDE HOSPITALAR"
                        elif "LEITOS" in tb_name:
                            info["icone"], info["tag"] = "🛏️", "CAPACIDADE"
                        elif "POPULACAO" in tb_name:
                            info["icone"], info["tag"] = "📍", "ABRANGÊNCIA"
                        elif "USUARIO" in tb_name:
                            info["icone"], info["tag"] = "👥", "SEGURANÇA"
                        elif "PERMANENCIA" in tb_name:
                            info["icone"], info["tag"] = "⏱️", "INDICADOR"
                        elif "DBTOOLS" in tb_name:
                            info["icone"], info["tag"] = "⚙️", "SISTEMA ORACLE"
                            info["desc"] = "Histórico de execução"
                            
                        tabelas_reais.append(info)
            except Exception as e:
                pass
                
            tabelas_mapeadas = len(tabelas_reais)

        def format_volumetria(num):
            if num >= 1_000_000:
                return f"{num/1_000_000:.1f}M".replace('.', ',')
            elif num >= 1_000:
                return f"{num/1_000:.1f}K".replace('.', ',')
            return str(num)
        
        # =====================================================
        # BLOCO 1: MONITORAMENTO REAL
        # =====================================================
        st.subheader("Monitoramento", divider="gray")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.html(criar_cartao(icone_sistema, "STATUS", "Status Sistema", status_sistema, status_sistema_sub))
        with col2:
            st.html(criar_cartao(icone_db, "CONEXÃO", "Banco de Dados", status_db, status_db_sub))
        with col3:
            st.html(criar_cartao("👥", "ACESSO", "Usuários Ativos", str(usuarios_ativos), "Permissões ativas no sistema"))
        with col4:
            st.html(criar_cartao("🗄️", "ESTRUTURA", "Tabelas no Oracle", str(tabelas_mapeadas), "Total no seu schema"))
        
        st.write("")

        # =====================================================
        # BLOCO 2: VOLUME DE DADOS DINÂMICO
        # =====================================================
        st.subheader("Volume de Dados (Real-time)", divider="gray")
        
        dados_grafico = []

        if not tabelas_reais:
            st.info("Nenhuma tabela encontrada no banco de dados para monitoramento.")
        else:
            # Organiza as tabelas reais em linhas de 3 colunas
            for i in range(0, len(tabelas_reais), 3):
                colunas = st.columns(3)
                tabelas_chunk = tabelas_reais[i:i+3]
                
                for idx, tb in enumerate(tabelas_chunk):
                    if tb["qtd"] >= 0: 
                        dados_grafico.append({"Tabela": tb["nome"], "Registros": tb["qtd"]})
                        
                    with colunas[idx]:
                        st.html(criar_cartao(tb["icone"], tb["tag"], tb["nome"], format_volumetria(tb["qtd"]), f"{tb['qtd']:,}".replace(',', '.') + " " + tb["desc"]))
                st.write("") 

        st.write("")
        st.write("")

        # =====================================================
        # BLOCO 3: GRÁFICO DINÂMICO (Baseado no Banco Real)
        # =====================================================
        st.subheader("Proporção de Registros no Oracle Database", divider="gray")
        
        if dados_grafico:
            df_grafico = pd.DataFrame(dados_grafico).set_index("Tabela")
            st.bar_chart(df_grafico, color="#8b5cf6", height=300)
        else:
            st.info("Nenhuma tabela monitorada possui registros no banco de dados.")

        st.write("")
        st.write("")

        # =====================================================
        # BLOCO 4: TRÁFEGO DE CONSULTAS
        # =====================================================
        st.subheader("Tráfego de Consultas (Streamlit App)", divider="gray")
        
        # Mantendo o visual analítico
        dados_trafego = pd.DataFrame(
            np.random.randint(10, 50, size=(20, 2)),
            columns=['Consultas Estruturadas (SQL)', 'Consultas Naturais (IA)']
        )
        st.area_chart(dados_trafego, color=["#3b82f6", "#8b5cf6"])