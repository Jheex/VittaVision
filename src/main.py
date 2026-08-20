import streamlit as st
from controller.app_controller import AppController

def main():
    # Configuração inicial da página (deve ser a primeira chamada do Streamlit)
    st.set_page_config(
        page_title="VittaVision - Inteligência em Saúde",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inicializa e executa o controller
    controller = AppController()
    controller.run()

if __name__ == "__main__":
    main()