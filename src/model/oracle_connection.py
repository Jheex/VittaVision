import os
import oracledb
import pandas as pd


class OracleDatabase:

    def __init__(self):
        # Caminho absoluto ou relativo para a pasta Wallet baseada na estrutura do projeto
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        default_wallet_path = os.path.join(base_dir, "data", "Wallet")

        # Credenciais configuradas diretamente para o projeto DataBytes / VittaVision
        self.user = os.getenv("DB_USER", "ADMIN")
        self.password = os.getenv("DB_PASSWORD", "Databytes@123")
        self.dsn = os.getenv("DB_DSN", "databytes_high")
        self.wallet_path = os.getenv("DB_WALLET_PATH", default_wallet_path)
        self.wallet_password = os.getenv("DB_WALLET_PASSWORD", "Databytes@123")

    def _conectar(self):
        """Método auxiliar para abrir a conexão com o Oracle Autonomous Database"""
        print(f"DEBUG: Tentando conectar no DSN '{self.dsn}' usando a Wallet em: {self.wallet_path}")
        return oracledb.connect(
            user=self.user,
            password=self.password,
            dsn=self.dsn,
            config_dir=self.wallet_path,
            wallet_location=self.wallet_path,
            wallet_password=self.wallet_password,
        )

    def verificar_login(self, nm_login: str, ds_senha: str) -> bool:
        """Verifica na tabela ALFA_USUARIO se o login e a senha conferem"""
        try:
            print("DEBUG: Iniciando processo de verificação de login...")
            connection = self._conectar()
            print("DEBUG: Conexão com o Oracle aberta com sucesso!")
            
            cursor = connection.cursor()

            sql = """
                SELECT id_usuario 
                FROM ALFA_USUARIO 
                WHERE nm_login = :1 AND ds_senha = :2 AND fl_ativo = 'S'
            """
            
            print(f"DEBUG: Executando query para o usuário: {nm_login}")
            cursor.execute(sql, [nm_login, ds_senha])
            resultado = cursor.fetchone()

            cursor.close()
            connection.close()

            if resultado:
                print("DEBUG: Usuário encontrado e senha válida!")
                return True
            
            print("DEBUG: Nenhum registro encontrado para esse usuário/senha (ou conta inativa).")
            return False

        except Exception as e:
            print(f"ERRO CRÍTICO ao tentar validar login no banco: {e}")
            return False

    def executar_select_ai(self, prompt_usuario: str):
        """Envia uma pergunta em linguagem natural usando o perfil do Select AI configurado no Oracle"""
        try:
            connection = self._conectar()

            # Exemplo de comando SQL chamando o Select AI da Oracle
            sql_query = f"""
                SELECT DBMS_CLOUD.GENERATE_TEXT(
                    prompt => :prompt,
                    profile_name => 'NOME_DO_PERFIL_AI'
                ) FROM DUAL
            """

            df = pd.read_sql(sql_query, con=connection, params={"prompt": prompt_usuario})
            connection.close()
            return df
        except Exception as e:
            print(f"Erro no Select AI: {e}")
            return pd.DataFrame()