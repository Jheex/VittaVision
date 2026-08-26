import os
import oracledb
import pandas as pd


class OracleDatabase:

    def __init__(self):
        # Defina suas credenciais ou use variáveis de ambiente (.env)
        self.user = os.getenv("DB_USER", "seu_usuario")
        self.password = os.getenv("DB_PASSWORD", "sua_senha")
        self.dsn = os.getenv(
            "DB_DSN", "sua_conexao_high"
        )  # Ex: "banco_high" do Oracle Autonomous Database
        self.wallet_path = os.getenv("DB_WALLET_PATH", "caminho/para/wallet")

    def executar_select_ai(self, prompt_usuario: str):
        """Envia uma pergunta em linguagem natural usando o perfil do Select AI configurado no Oracle"""
        try:
            # Conexão com Oracle Wallet (comum no OCI Autonomous Database)
            connection = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn,
                config_dir=self.wallet_path,
                wallet_location=self.wallet_path,
                wallet_password=os.getenv("WALLET_PASSWORD", "senha_wallet"),
            )

            # Exemplo de comando SQL chamando o Select AI da Oracle
            # Substitua 'NOME_DO_PERFIL_AI' pelo perfil que vocês criaram no banco (ex: 'openai_profile' ou 'cohere_profile')
            sql_query = f"""
                SELECT DBMS_CLOUD.GENERATE_TEXT(
                    prompt => :prompt,
                    profile_name => 'NOME_DO_PERFIL_AI'
                ) FROM DUAL
            """

            # Ou caso esteja rodando uma query direta via Select AI chat/run:
            # sql_query = "BEGIN DBMS_CLOUD_AI.CREATE_PROFILE(...); END;"

            df = pd.read_sql(sql_query, con=connection, params={"prompt": prompt_usuario})
            connection.close()
            return df
        except Exception as e:
            # Retorna o erro amigável para tratamento na tela caso o banco não esteja conectado
            return pd.DataFrame()