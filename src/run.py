import os
import sys
from streamlit.web import cli as stcli

if __name__ == "__main__":
    # Garante que a raiz e a pasta src estão no path do Python
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_dir)
    sys.path.append(os.path.join(current_dir, "src"))

    # Define o arquivo principal que o Streamlit vai rodar
    sys.argv = [
        "streamlit",
        "run",
        "main.py",
        "--server.runOnSave=true",
        "--server.fileWatcherType=auto",
    ]

    stcli.main()