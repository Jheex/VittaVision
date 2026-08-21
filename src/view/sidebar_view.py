import streamlit as st
import importlib.util
from PIL import Image
import os

if importlib.util.find_spec("streamlit_option_menu") is not None:
    from streamlit_option_menu import option_menu

class SidebarView:
    def render(self):
        with st.sidebar:
            # CSS para Sidebar com gradiente imersivo e sem blocos travados
            st.markdown("""
                <style>
                    [data-testid="stSidebar"] {
                        height: 100vh;
                        display: flex;
                        flex-direction: column;
                        overflow-y: auto;
                        background: linear-gradient(180deg, #090d16 0%, #17102e 50%, #1e1b4b 100%) !important;
                        border-right: 1px solid rgba(139, 92, 246, 0.15);
                    }
                    /* Remove qualquer padding lateral excessivo do container padrão do Streamlit */
                    [data-testid="stSidebarUserContent"] {
                        padding-left: 10px;
                        padding-right: 10px;
                    }
                </style>
            """, unsafe_allow_html=True)

            # Logo Centralizada
            current_dir = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.abspath(os.path.join(current_dir, "..", "..", "Src", "assets", "logo.png"))
            
            if not os.path.exists(logo_path):
                logo_path = "Src/assets/logo.png"

            if os.path.exists(logo_path):
                image = Image.open(logo_path)
                st.image(image, use_container_width=True)
            else:
                st.markdown("""
                    <div style="background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%); padding: 15px; border-radius: 12px; text-align: center; color: white; font-weight: bold; font-size: 18px; box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);">
                        VITTA VISION
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

            # Menu Principal com container transparente e visual minimalista
            menu_selecionado = option_menu(
                menu_title=None,
                options=["Dashboard", "Internações", "Hospitais", "Leitos", "Indicadores", "Mapas", "Relatórios", "Assistente IA", "Configurações"],
                icons=['house-door', 'hospital', 'buildings', 'clipboard-plus', 'graph-up', 'map', 'file-earmark-text', 'robot', 'gear'],
                menu_icon=None,
                default_index=0,
                key="menu_principal",
                styles={
                    # Container transparente para sumir com o bloco retangular
                    "container": {"padding": "0px", "background-color": "transparent"},
                    "icon": {"color": "#a78bfa", "font-size": "17px"},
                    "nav-link": {
                        "font-size": "14px",
                        "margin": "4px 0px",
                        "background-color": "transparent",
                        "--hover-color": "rgba(139, 92, 246, 0.1)",
                        "padding": "11px 14px",
                        "border-radius": "10px",
                        "color": "#94a3b8",
                        "transition": "all 0.25s ease"
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(90deg, rgba(139, 92, 246, 0.25) 0%, rgba(139, 92, 246, 0.05) 100%)",
                        "color": "#f8fafc",
                        "border-left": "3px solid #8b5cf6",
                        "border-radius": "0 10px 10px 0",
                        "font-weight": "600",
                        "box-shadow": "inset 0 1px 0 rgba(255, 255, 255, 0.05)"
                    },
                }
            )

            # Espaçador Flexível: Empurra o perfil para o rodapé
            st.markdown('<div style="flex-grow: 1;"></div>', unsafe_allow_html=True)

            # Card de Usuário (Rodapé)
            st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.04); padding: 12px 14px; border-radius: 14px; margin: 15px 0;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%); color: white; width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px; box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);">JS</div>
                        <div>
                            <div style="color: #f8fafc; font-size: 13px; font-weight: 600;">Gestor de Saúde</div>
                            <div style="color: #64748b; font-size: 11px;">Secretaria Municipal</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            return menu_selecionado