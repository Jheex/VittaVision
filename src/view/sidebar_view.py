import streamlit as st
import importlib.util

if importlib.util.find_spec("streamlit_option_menu") is not None:
    from streamlit_option_menu import option_menu

class SidebarView:
    def render(self):
        with st.sidebar:
            st.markdown("""
                <div style="display: flex; align-items: center; gap: 12px; padding: 10px 5px 20px 5px; border-bottom: 1px solid rgba(168, 85, 247, 0.2); margin-bottom: 15px;">
                    <div style="background: linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%); width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);">💠</div>
                    <div>
                        <h2 style="margin: 0; font-size: 17px; font-weight: 700; color: #ffffff; letter-spacing: 0.5px;">VITTA VISION</h2>
                        <p style="margin: 0; font-size: 11px; color: #9ca3af;">Inteligência em Saúde</p>
                    </div>
                </div>
                <p style="color: #9ca3af; font-size: 11px; font-weight: 600; letter-spacing: 1px; margin-bottom: 8px; padding-left: 5px;">MENU PRINCIPAL</p>
            """, unsafe_allow_html=True)

            menu_selecionado = option_menu(
                menu_title=None,
                options=["Dashboard", "Internações", "Hospitais", "Leitos", "Indicadores", "Mapas", "Relatórios", "Assistente IA", "Configurações"],
                icons=['speedometer2', 'hospital', 'building', 'bed', 'graph-up-arrow', 'map', 'file-text', 'robot', 'gear'],
                menu_icon=None,
                default_index=0,
                key="menu_principal",  # <--- CHAVE ÚNICA PARA EVITAR O ERRO DO STREAMLIT
                styles={
                    "container": {"padding": "0px", "background-color": "transparent"},
                    "icon": {"color": "#a855f7", "font-size": "16px"}, 
                    "nav-link": {
                        "font-size": "14px",
                        "text-align": "left",
                        "margin": "4px 0px",
                        "--hover-color": "rgba(139, 92, 246, 0.15)",
                        "padding": "10px 14px",
                        "border-radius": "10px",
                        "background-color": "transparent",
                        "color": "#9ca3af"
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(135deg, #8b5cf6 0%, #3b82f6 100%)",
                        "color": "#ffffff",
                        "font-weight": "600",
                        "border": "1px solid rgba(255, 255, 255, 0.2)",
                        "box-shadow": "0 4px 15px rgba(139, 92, 246, 0.4)"
                    },
                }
            )

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div style="background: rgba(18, 24, 38, 0.7); border: 1px solid rgba(168, 85, 247, 0.3); padding: 12px 15px; border-radius: 12px; display: flex; align-items: center; gap: 10px;">
                    <div style="background-color: #8b5cf6; color: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 13px;">JS</div>
                    <div>
                        <h4 style="margin: 0; font-size: 13px; color: #ffffff;">Gestor de Saúde</h4>
                        <p style="margin: 0; font-size: 11px; color: #9ca3af;">Secretaria Municipal</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            return menu_selecionado