import pandas as pd


class LeitosModel:
    """
    Model responsável pelas operações de dados
    relacionadas aos leitos hospitalares.
    """

    def __init__(self, db):
        self.db = db
        self.tabela = "TB_LEITOS"

    # =========================================================
    # LISTAR LEITOS
    # =========================================================

    def listar_leitos(self, limite=1000):

        return self.db.consultar_tabela(
            self.tabela,
            limite
        )

    # =========================================================
    # TOTAL DE REGISTROS
    # =========================================================

    def total_registros(self):

        query = f"""
            SELECT COUNT(*) AS TOTAL
            FROM {self.tabela}
        """

        df = self.db.executar_query_sql(query)

        if df.empty:
            return 0

        return int(df.iloc[0]["TOTAL"])

    # =========================================================
    # TOTAL DE LEITOS EXISTENTES
    # =========================================================

    def total_leitos(self):

        query = f"""
            SELECT
                NVL(SUM(LEITOS_EXISTENTES), 0) AS TOTAL
            FROM {self.tabela}
        """

        df = self.db.executar_query_sql(query)

        if df.empty:
            return 0

        return int(df.iloc[0]["TOTAL"])

    # =========================================================
    # TOTAL DE LEITOS SUS
    # =========================================================

    def total_leitos_sus(self):

        query = f"""
            SELECT
                NVL(SUM(LEITOS_SUS), 0) AS TOTAL
            FROM {self.tabela}
        """

        df = self.db.executar_query_sql(query)

        if df.empty:
            return 0

        return int(df.iloc[0]["TOTAL"])

    # =========================================================
    # TOTAL DE LEITOS UTI
    # =========================================================

    def total_leitos_uti(self):

        query = f"""
            SELECT
                NVL(SUM(UTI_TOTAL_EXIST), 0) AS TOTAL
            FROM {self.tabela}
        """

        df = self.db.executar_query_sql(query)

        if df.empty:
            return 0

        return int(df.iloc[0]["TOTAL"])

    # =========================================================
    # LEITOS POR UF
    # =========================================================

    def leitos_por_uf(self):

        query = f"""
            SELECT
                UF,
                NVL(SUM(LEITOS_EXISTENTES), 0) AS TOTAL
            FROM {self.tabela}
            GROUP BY UF
            ORDER BY TOTAL DESC
        """

        return self.db.executar_query_sql(query)

    # =========================================================
    # LEITOS POR MUNICÍPIO
    # =========================================================

    def leitos_por_municipio(self):

        query = f"""
            SELECT
                MUNICIPIO,
                NVL(SUM(LEITOS_EXISTENTES), 0) AS TOTAL
            FROM {self.tabela}
            GROUP BY MUNICIPIO
            ORDER BY TOTAL DESC
        """

        return self.db.executar_query_sql(query)

    # =========================================================
    # LEITOS POR REGIÃO
    # =========================================================

    def leitos_por_regiao(self):

        query = f"""
            SELECT
                REGIAO,
                NVL(SUM(LEITOS_EXISTENTES), 0) AS TOTAL
            FROM {self.tabela}
            GROUP BY REGIAO
            ORDER BY TOTAL DESC
        """

        return self.db.executar_query_sql(query)

    # =========================================================
    # DADOS PARA A VIEW
    # =========================================================

    def dados_para_view(self):
        """
        Retorna os dados já consolidados por CNES.

        OTIMIZAÇÃO:
        ---------------------------------------------------------
        A versão anterior buscava todos os registros da tabela
        e depois fazia o GROUP BY no Pandas.

        Agora a consolidação numérica é realizada pelo Oracle
        usando funções analíticas:

            SUM(...) OVER (PARTITION BY CNES)

        Dessa forma o Oracle calcula os totais por hospital
        durante uma única consulta.

        ROW_NUMBER() mantém somente um registro cadastral
        por CNES.

        Importante:
        ---------------------------------------------------------
        Não existe GROUP BY nesta consulta e não existe
        agregação dentro de outra agregação.

        Portanto não ocorre o ORA-00935:
        "group function is nested too deeply".
        """

        query = f"""
            SELECT
                REGIAO,
                UF,
                CO_IBGE,
                MUNICIPIO,
                CNES,
                NOME_ESTABELECIMENTO,
                RAZAO_SOCIAL,
                TP_GESTAO,
                CO_TIPO_UNIDADE,
                DS_TIPO_UNIDADE,
                NATUREZA_JURIDICA,
                DESC_NATUREZA_JURIDICA,

                LEITOS_EXISTENTES,
                LEITOS_SUS,

                UTI_TOTAL_EXIST,
                UTI_TOTAL_SUS,

                UTI_ADULTO_EXIST,
                UTI_ADULTO_SUS,

                UTI_PEDIATRICO_EXIST,
                UTI_PEDIATRICO_SUS,

                UTI_NEONATAL_EXIST,
                UTI_NEONATAL_SUS,

                UTI_QUEIMADO_EXIST,
                UTI_QUEIMADO_SUS,

                UTI_CORONARIANA_EXIST,
                UTI_CORONARIANA_SUS

            FROM
            (
                SELECT

                    REGIAO,
                    UF,
                    CO_IBGE,
                    MUNICIPIO,
                    CNES,
                    NOME_ESTABELECIMENTO,
                    RAZAO_SOCIAL,
                    TP_GESTAO,
                    CO_TIPO_UNIDADE,
                    DS_TIPO_UNIDADE,
                    NATUREZA_JURIDICA,
                    DESC_NATUREZA_JURIDICA,

                    SUM(
                        NVL(LEITOS_EXISTENTES, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS LEITOS_EXISTENTES,

                    SUM(
                        NVL(LEITOS_SUS, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS LEITOS_SUS,

                    SUM(
                        NVL(UTI_TOTAL_EXIST, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_TOTAL_EXIST,

                    SUM(
                        NVL(UTI_TOTAL_SUS, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_TOTAL_SUS,

                    SUM(
                        NVL(UTI_ADULTO_EXIST, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_ADULTO_EXIST,

                    SUM(
                        NVL(UTI_ADULTO_SUS, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_ADULTO_SUS,

                    SUM(
                        NVL(UTI_PEDIATRICO_EXIST, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_PEDIATRICO_EXIST,

                    SUM(
                        NVL(UTI_PEDIATRICO_SUS, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_PEDIATRICO_SUS,

                    SUM(
                        NVL(UTI_NEONATAL_EXIST, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_NEONATAL_EXIST,

                    SUM(
                        NVL(UTI_NEONATAL_SUS, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_NEONATAL_SUS,

                    SUM(
                        NVL(UTI_QUEIMADO_EXIST, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_QUEIMADO_EXIST,

                    SUM(
                        NVL(UTI_QUEIMADO_SUS, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_QUEIMADO_SUS,

                    SUM(
                        NVL(UTI_CORONARIANA_EXIST, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_CORONARIANA_EXIST,

                    SUM(
                        NVL(UTI_CORONARIANA_SUS, 0)
                    ) OVER (
                        PARTITION BY CNES
                    ) AS UTI_CORONARIANA_SUS,

                    ROW_NUMBER() OVER (
                        PARTITION BY CNES
                        ORDER BY CNES
                    ) AS RN

                FROM {self.tabela}

                WHERE CNES IS NOT NULL
            )

            WHERE RN = 1
        """

        return self.db.executar_query_sql(query)

    # =========================================================
    # BUSCAR MUNICÍPIO
    # =========================================================

    def buscar_municipio(self, municipio):

        if not municipio:
            return pd.DataFrame()

        connection = None

        try:

            connection = self.db._conectar()

            query = f"""
                SELECT *
                FROM {self.tabela}
                WHERE UPPER(MUNICIPIO) LIKE UPPER(:1)
                ORDER BY MUNICIPIO
            """

            return pd.read_sql(
                query,
                con=connection,
                params=[f"%{municipio}%"]
            )

        finally:

            if connection:
                connection.close()

    # =========================================================
    # BUSCAR ESTABELECIMENTO
    # =========================================================

    def buscar_estabelecimento(self, nome):

        if not nome:
            return pd.DataFrame()

        connection = None

        try:

            connection = self.db._conectar()

            query = f"""
                SELECT *
                FROM {self.tabela}
                WHERE UPPER(NOME_ESTABELECIMENTO)
                    LIKE UPPER(:1)
                ORDER BY NOME_ESTABELECIMENTO
            """

            return pd.read_sql(
                query,
                con=connection,
                params=[f"%{nome}%"]
            )

        finally:

            if connection:
                connection.close()

    # =========================================================
    # IMPORTAR CSV
    # =========================================================

    def importar_csv(self, arquivo):

        if arquivo is None:
            raise ValueError(
                "Nenhum arquivo foi enviado."
            )

        df = pd.read_csv(
            arquivo,
            sep=";"
        )

        if df.empty:
            raise ValueError(
                "O arquivo CSV está vazio."
            )

        df.columns = [
            str(coluna)
            .strip()
            .upper()
            for coluna in df.columns
        ]

        colunas_esperadas = [

            "COMP",
            "REGIAO",
            "UF",
            "CO_IBGE",
            "MUNICIPIO",
            "MOTIVO_DESABILITACAO",
            "CNES",
            "NOME_ESTABELECIMENTO",
            "RAZAO_SOCIAL",
            "TP_GESTAO",
            "CO_TIPO_UNIDADE",
            "DS_TIPO_UNIDADE",
            "NATUREZA_JURIDICA",
            "DESC_NATUREZA_JURIDICA",
            "NO_LOGRADOURO",
            "NU_ENDERECO",
            "NO_COMPLEMENTO",
            "NO_BAIRRO",
            "CO_CEP",
            "NU_TELEFONE",
            "NO_EMAIL",

            "LEITOS_EXISTENTES",
            "LEITOS_SUS",

            "UTI_TOTAL_EXIST",
            "UTI_TOTAL_SUS",

            "UTI_ADULTO_EXIST",
            "UTI_ADULTO_SUS",

            "UTI_PEDIATRICO_EXIST",
            "UTI_PEDIATRICO_SUS",

            "UTI_NEONATAL_EXIST",
            "UTI_NEONATAL_SUS",

            "UTI_QUEIMADO_EXIST",
            "UTI_QUEIMADO_SUS",

            "UTI_CORONARIANA_EXIST",
            "UTI_CORONARIANA_SUS",
        ]

        faltantes = [
            coluna
            for coluna in colunas_esperadas
            if coluna not in df.columns
        ]

        if faltantes:

            raise ValueError(
                "O CSV não possui todas as colunas esperadas: "
                + ", ".join(faltantes)
            )

        df = df[colunas_esperadas]

        colunas_numericas = [

            "COMP",
            "CO_IBGE",
            "CNES",
            "CO_TIPO_UNIDADE",
            "NATUREZA_JURIDICA",

            "LEITOS_EXISTENTES",
            "LEITOS_SUS",

            "UTI_TOTAL_EXIST",
            "UTI_TOTAL_SUS",

            "UTI_ADULTO_EXIST",
            "UTI_ADULTO_SUS",

            "UTI_PEDIATRICO_EXIST",
            "UTI_PEDIATRICO_SUS",

            "UTI_NEONATAL_EXIST",
            "UTI_NEONATAL_SUS",

            "UTI_QUEIMADO_EXIST",
            "UTI_QUEIMADO_SUS",

            "UTI_CORONARIANA_EXIST",
            "UTI_CORONARIANA_SUS",
        ]

        for coluna in colunas_numericas:

            df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce"
            )

        quantidade = self.db.importar_dataframe(
            self.tabela,
            df
        )

        return quantidade

    # =========================================================
    # LIMPAR TABELA
    # =========================================================

    def limpar_tabela(self):

        connection = None
        cursor = None

        try:

            connection = self.db._conectar()
            cursor = connection.cursor()

            cursor.execute(
                f"TRUNCATE TABLE {self.tabela}"
            )

            connection.commit()

        except Exception:

            if connection:
                connection.rollback()

            raise

        finally:

            if cursor:
                cursor.close()

            if connection:
                connection.close()