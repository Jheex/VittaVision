import streamlit as st

class AdminSidebar:
    """Componente isolado para padronização da Sidebar do Administrador."""
    
    def render(self):
        # Injeção do CSS exclusivo da Sidebar (aplicado em todas as telas)
        st.html("""
        <style>
            /* Esconde as bolinhas do Radio Button no Sidebar */
            [data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
                display: none !important;
            }
            /* Estiliza os itens do menu lateral */
            [data-testid="stSidebar"] div[role="radiogroup"] > label {
                background-color: transparent;
                border-radius: 8px;
                padding: 10px 15px;
                margin-bottom: 4px;
                transition: all 0.2s ease-in-out;
                border-left: 3px solid transparent;
            }
            /* Efeito ao passar o mouse e destaque do item ATIVO */
            [data-testid="stSidebar"] div[role="radiogroup"] > label:hover,
            [data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
                background-color: rgba(139, 92, 246, 0.1);
                border-left: 3px solid #8b5cf6;
            }
            /* Linha separadora do Sidebar */
            [data-testid="stSidebar"] hr {
                border-color: rgba(139, 92, 246, 0.2);
            }
        </style>
        """)

        with st.sidebar:
            st.title("Vitta Vision")
            
            # Puxa o nome real do administrador logado
            admin_nome = st.session_state.get("admin_perfil", "Administrador Master")
            st.markdown(f"Bem-vindo(a), **{admin_nome}**")
            
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
            
        return menu_selecionado