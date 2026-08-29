import re
import os
import oracledb
import pandas as pd


class OracleDatabase:

    def __init__(self):
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        default_wallet_path = os.path.join(
            base_dir,
            "data",
            "Wallet"
        )

        self.user = os.getenv(
            "DB_USER",
            "ADMIN"
        )

        self.password = os.getenv(
            "DB_PASSWORD",
            "Databytes@123"
        )

        self.dsn = os.getenv(
            "DB_DSN",
            "databytes_high"
        )

        self.wallet_path = os.getenv(
            "DB_WALLET_PATH",
            default_wallet_path
        )

        self.wallet_password = os.getenv(
            "DB_WALLET_PASSWORD",
            "Databytes@123"
        )

    # =========================================================
    # CONEXÃO
    # =========================================================

    def _conectar(self):

        return oracledb.connect(
            user=self.user,
            password=self.password,
            dsn=self.dsn,
            config_dir=self.wallet_path,
            wallet_location=self.wallet_path,
            wallet_password=self.wallet_password,
        )

    # =========================================================
    # CONSULTA GENÉRICA
    # =========================================================

    def fetch_data(self, query: str, params=None):

        connection = None

        try:

            connection = self._conectar()

            df = pd.read_sql(
                query,
                con=connection,
                params=params or {}
            )

            return df

        except Exception as e:

            print(f"Erro no fetch_data: {e}")

            return pd.DataFrame()

        finally:

            if connection:
                connection.close()

    # =========================================================
    # LOGIN
    # =========================================================

    def verificar_login(
        self,
        nm_login: str,
        ds_senha_hash: str
    ) -> bool:

        connection = None
        cursor = None

        try:

            connection = self._conectar()
            cursor = connection.cursor()

            sql = """
                SELECT ID_USUARIO
                FROM ALFA_USUARIO
                WHERE NM_LOGIN = :1
                  AND DS_SENHA = :2
                  AND FL_ATIVO = 'S'
            """

            cursor.execute(
                sql,
                [
                    nm_login,
                    ds_senha_hash
                ]
            )

            resultado = cursor.fetchone()

            return bool(resultado)

        except Exception as e:

            print(
                f"ERRO ao validar login: {e}"
            )

            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # =========================================================
    # LISTAR USUÁRIOS
    # =========================================================

    def listar_usuarios(self):

        connection = None

        try:

            connection = self._conectar()

            query = """
                SELECT
                    ID_USUARIO,
                    NM_LOGIN,
                    DS_EMAIL,
                    NM_COMPLETO,
                    FL_ATIVO,
                    DT_CRIACAO
                FROM ALFA_USUARIO
                ORDER BY ID_USUARIO DESC
            """

            df = pd.read_sql(
                query,
                con=connection
            )

            return df

        except Exception as e:

            print(
                f"Erro ao listar usuários: {e}"
            )

            return pd.DataFrame()

        finally:

            if connection:
                connection.close()

    # =========================================================
    # CADASTRAR USUÁRIO
    # =========================================================

    def cadastrar_usuario(
        self,
        nm_login: str,
        ds_email: str,
        ds_senha_hash: str,
        nm_completo: str,
        fl_ativo: str = "S"
    ) -> bool:

        connection = None
        cursor = None

        try:

            connection = self._conectar()
            cursor = connection.cursor()

            sql = """
                INSERT INTO ALFA_USUARIO
                (
                    NM_LOGIN,
                    DS_EMAIL,
                    DS_SENHA,
                    NM_COMPLETO,
                    FL_ATIVO,
                    DT_CRIACAO
                )
                VALUES
                (
                    :1,
                    :2,
                    :3,
                    :4,
                    :5,
                    SYSDATE
                )
            """

            cursor.execute(
                sql,
                [
                    nm_login,
                    ds_email,
                    ds_senha_hash,
                    nm_completo,
                    fl_ativo
                ]
            )

            connection.commit()

            return True

        except Exception as e:

            print(
                f"Erro ao cadastrar usuário: {e}"
            )

            if connection:
                connection.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # =========================================================
    # ALTERAR STATUS
    # =========================================================

    def alterar_status_usuario(
        self,
        id_usuario: int,
        novo_status: str
    ) -> bool:

        connection = None
        cursor = None

        try:

            connection = self._conectar()
            cursor = connection.cursor()

            sql = """
                UPDATE ALFA_USUARIO
                SET FL_ATIVO = :1
                WHERE ID_USUARIO = :2
            """

            cursor.execute(
                sql,
                [
                    novo_status,
                    id_usuario
                ]
            )

            connection.commit()

            return True

        except Exception as e:

            print(
                f"Erro ao alterar status: {e}"
            )

            if connection:
                connection.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # =========================================================
    # ATUALIZAR USUÁRIO
    # =========================================================

    def atualizar_usuario(
        self,
        id_usuario: int,
        nm_login: str,
        nm_completo: str,
        ds_email: str,
        fl_ativo: str,
        ds_senha_hash: str = None
    ) -> bool:

        connection = None
        cursor = None

        try:

            connection = self._conectar()
            cursor = connection.cursor()

            # -------------------------------------------------
            # COM NOVA SENHA
            # -------------------------------------------------

            if ds_senha_hash:

                sql = """
                    UPDATE ALFA_USUARIO
                    SET
                        NM_LOGIN = :1,
                        NM_COMPLETO = :2,
                        DS_EMAIL = :3,
                        FL_ATIVO = :4,
                        DS_SENHA = :5
                    WHERE ID_USUARIO = :6
                """

                cursor.execute(
                    sql,
                    [
                        nm_login,
                        nm_completo,
                        ds_email,
                        fl_ativo,
                        ds_senha_hash,
                        id_usuario
                    ]
                )

            # -------------------------------------------------
            # SEM ALTERAR SENHA
            # -------------------------------------------------

            else:

                sql = """
                    UPDATE ALFA_USUARIO
                    SET
                        NM_LOGIN = :1,
                        NM_COMPLETO = :2,
                        DS_EMAIL = :3,
                        FL_ATIVO = :4
                    WHERE ID_USUARIO = :5
                """

                cursor.execute(
                    sql,
                    [
                        nm_login,
                        nm_completo,
                        ds_email,
                        fl_ativo,
                        id_usuario
                    ]
                )

            connection.commit()

            return True

        except Exception as e:

            print(
                f"Erro ao atualizar usuário: {e}"
            )

            if connection:
                connection.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

    # =========================================================
    # EXCLUIR USUÁRIO
    # =========================================================

    def excluir_usuario(
        self,
        id_usuario: int
    ) -> bool:

        connection = None
        cursor = None

        try:

            connection = self._conectar()
            cursor = connection.cursor()

            sql = """
                DELETE FROM ALFA_USUARIO
                WHERE ID_USUARIO = :1
            """

            cursor.execute(
                sql,
                [id_usuario]
            )

            connection.commit()

            return True

        except Exception as e:

            print(
                f"Erro ao excluir usuário: {e}"
            )

            if connection:
                connection.rollback()

            return False

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()

        # =========================================================
    # DATABASE MANAGER
    # =========================================================

    def _validar_nome_oracle(self, nome: str) -> str:
        """
        Valida nomes de tabelas/colunas antes de utilizar SQL dinâmico.
        """

        nome = str(nome).strip().upper()

        if not re.match(r"^[A-Z][A-Z0-9_$#]*$", nome):
            raise ValueError(
                f"Nome Oracle inválido: {nome}"
            )

        return nome


    def listar_tabelas(self):
        """
        Lista todas as tabelas do schema atual.
        """

        connection = None

        try:

            connection = self._conectar()

            query = """
                SELECT
                    TABLE_NAME,
                    NUM_ROWS,
                    TABLESPACE_NAME,
                    STATUS
                FROM USER_TABLES
                ORDER BY TABLE_NAME
            """

            df = pd.read_sql(
                query,
                con=connection
            )

            return df

        except Exception as e:

            print(
                f"Erro ao listar tabelas: {e}"
            )

            return pd.DataFrame()

        finally:

            if connection:

                connection.close()


    def obter_estrutura_tabela(self, nome_tabela: str):
        """
        Retorna estrutura das colunas da tabela.
        """

        nome_tabela = self._validar_nome_oracle(
            nome_tabela
        )

        connection = None

        try:

            connection = self._conectar()

            query = """
                SELECT
                    COLUMN_ID,
                    COLUMN_NAME,
                    DATA_TYPE,
                    DATA_LENGTH,
                    DATA_PRECISION,
                    DATA_SCALE,
                    NULLABLE,
                    DATA_DEFAULT
                FROM USER_TAB_COLUMNS
                WHERE TABLE_NAME = :1
                ORDER BY COLUMN_ID
            """

            return pd.read_sql(
                query,
                con=connection,
                params=[nome_tabela]
            )

        except Exception as e:

            print(
                f"Erro ao obter estrutura: {e}"
            )

            return pd.DataFrame()

        finally:

            if connection:

                connection.close()


    def obter_constraints_tabela(self, nome_tabela: str):
        """
        Retorna PK, FK, UNIQUE e outras constraints.
        """

        nome_tabela = self._validar_nome_oracle(
            nome_tabela
        )

        connection = None

        try:

            connection = self._conectar()

            query = """
                SELECT
                    uc.CONSTRAINT_NAME,
                    uc.CONSTRAINT_TYPE,
                    ucc.COLUMN_NAME,
                    uc.R_CONSTRAINT_NAME
                FROM USER_CONSTRAINTS uc
                LEFT JOIN USER_CONS_COLUMNS ucc
                    ON uc.CONSTRAINT_NAME = ucc.CONSTRAINT_NAME
                WHERE uc.TABLE_NAME = :1
                ORDER BY
                    uc.CONSTRAINT_NAME,
                    ucc.POSITION
            """

            return pd.read_sql(
                query,
                con=connection,
                params=[nome_tabela]
            )

        except Exception as e:

            print(
                f"Erro ao obter constraints: {e}"
            )

            return pd.DataFrame()

        finally:

            if connection:

                connection.close()


    def consultar_tabela(
        self,
        nome_tabela: str,
        limite: int = 100
    ):
        """
        Consulta registros de uma tabela.
        """

        nome_tabela = self._validar_nome_oracle(
            nome_tabela
        )

        limite = int(limite)

        if limite < 1:

            limite = 100

        if limite > 10000:

            limite = 10000

        connection = None

        try:

            connection = self._conectar()

            query = f"""
                SELECT *
                FROM {nome_tabela}
                FETCH FIRST {limite} ROWS ONLY
            """

            return pd.read_sql(
                query,
                con=connection
            )

        except Exception as e:

            print(
                f"Erro ao consultar tabela: {e}"
            )

            raise

        finally:

            if connection:

                connection.close()


    def executar_query_sql(self, query: str):
        """
        Executa consultas SQL de leitura.
        """

        query_limpa = query.strip()

        if not query_limpa:

            raise ValueError(
                "A consulta SQL está vazia."
            )

        primeira_palavra = (
            query_limpa
            .split()[0]
            .upper()
        )

        permitidos = [
            "SELECT",
            "WITH",
            "EXPLAIN"
        ]

        if primeira_palavra not in permitidos:

            raise ValueError(
                "Apenas SELECT, WITH e EXPLAIN "
                "são permitidos."
            )

        connection = None

        try:

            connection = self._conectar()

            return pd.read_sql(
                query_limpa,
                con=connection
            )

        except Exception as e:

            print(
                f"Erro ao executar SQL: {e}"
            )

            raise

        finally:

            if connection:

                connection.close()


    def importar_dataframe(
        self,
        nome_tabela: str,
        df: pd.DataFrame
    ) -> int:
        """
        Importa um DataFrame para uma tabela Oracle existente.

        Os nomes das colunas do DataFrame devem corresponder
        às colunas existentes na tabela.
        """

        if df.empty:

            raise ValueError(
                "O arquivo não possui registros."
            )

        nome_tabela = self._validar_nome_oracle(
            nome_tabela
        )

        # ---------------------------------------------------------
        # Validação das colunas
        # ---------------------------------------------------------

        colunas = []

        for coluna in df.columns:

            coluna_validada = (
                self._validar_nome_oracle(
                    coluna
                )
            )

            colunas.append(
                coluna_validada
            )

        df = df.copy()

        df.columns = colunas

        connection = None
        cursor = None

        try:

            connection = self._conectar()

            cursor = connection.cursor()

            placeholders = ", ".join(
                [f":{i + 1}" for i in range(len(colunas))]
            )

            nomes_colunas = ", ".join(
                colunas
            )

            sql = f"""
                INSERT INTO {nome_tabela}
                ({nomes_colunas})
                VALUES ({placeholders})
            """

            dados = []

            for linha in df.itertuples(
                index=False,
                name=None
            ):

                dados.append(
                    tuple(
                        None if pd.isna(valor)
                        else valor
                        for valor in linha
                    )
                )

            cursor.executemany(
                sql,
                dados
            )

            connection.commit()

            return len(dados)

        except Exception as e:

            if connection:

                connection.rollback()

            print(
                f"Erro na importação: {e}"
            )

            raise

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()


    def criar_tabela(
        self,
        nome_tabela: str,
        colunas: list
    ):
        """
        Cria uma nova tabela Oracle.
        """

        nome_tabela = self._validar_nome_oracle(
            nome_tabela
        )

        if not colunas:

            raise ValueError(
                "Nenhuma coluna foi informada."
            )

        tipos_permitidos = {
            "VARCHAR2",
            "NUMBER",
            "DATE",
            "TIMESTAMP",
            "CLOB"
        }

        definicoes = []

        for coluna in colunas:

            nome_coluna = self._validar_nome_oracle(
                coluna["nome"]
            )

            tipo = str(
                coluna["tipo"]
            ).upper().strip()

            if tipo not in tipos_permitidos:

                raise ValueError(
                    f"Tipo Oracle não permitido: {tipo}"
                )

            if tipo == "VARCHAR2":

                tamanho = str(
                    coluna.get(
                        "tamanho",
                        "255"
                    )
                ).strip()

                if not tamanho.isdigit():

                    tamanho = "255"

                definicao = (
                    f"{nome_coluna} "
                    f"VARCHAR2({tamanho})"
                )

            elif tipo == "NUMBER":

                definicao = (
                    f"{nome_coluna} NUMBER"
                )

            elif tipo == "DATE":

                definicao = (
                    f"{nome_coluna} DATE"
                )

            elif tipo == "TIMESTAMP":

                definicao = (
                    f"{nome_coluna} TIMESTAMP"
                )

            elif tipo == "CLOB":

                definicao = (
                    f"{nome_coluna} CLOB"
                )

            definicoes.append(
                definicao
            )

        sql = f"""
            CREATE TABLE {nome_tabela}
            (
                {", ".join(definicoes)}
            )
        """

        connection = None
        cursor = None

        try:

            connection = self._conectar()

            cursor = connection.cursor()

            cursor.execute(sql)

            connection.commit()

        except Exception as e:

            if connection:

                connection.rollback()

            print(
                f"Erro ao criar tabela: {e}"
            )

            raise

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()


    def excluir_tabela(
        self,
        nome_tabela: str
    ):
        """
        Exclui uma tabela.

        Mantido como método separado para futuras telas
        de confirmação administrativa.
        """

        nome_tabela = self._validar_nome_oracle(
            nome_tabela
        )

        connection = None
        cursor = None

        try:

            connection = self._conectar()

            cursor = connection.cursor()

            cursor.execute(
                f"DROP TABLE {nome_tabela}"
            )

            connection.commit()

        except Exception as e:

            if connection:

                connection.rollback()

            print(
                f"Erro ao excluir tabela: {e}"
            )

            raise

        finally:

            if cursor:

                cursor.close()

            if connection:

                connection.close()


    def obter_info_banco(self):
        """
        Informações básicas do Oracle.
        """

        connection = None

        try:

            connection = self._conectar()

            query = """
                SELECT
                    SYS_CONTEXT(
                        'USERENV',
                        'DB_NAME'
                    ) AS DATABASE_NAME,

                    SYS_CONTEXT(
                        'USERENV',
                        'CURRENT_SCHEMA'
                    ) AS CURRENT_SCHEMA,

                    SYS_CONTEXT(
                        'USERENV',
                        'INSTANCE_NAME'
                    ) AS INSTANCE_NAME

                FROM DUAL
            """

            return pd.read_sql(
                query,
                con=connection
            )

        except Exception as e:

            print(
                f"Erro ao obter informações do banco: {e}"
            )

            return pd.DataFrame()

        finally:

            if connection:

                connection.close()