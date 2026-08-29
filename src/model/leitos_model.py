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
        """
        Retorna os registros de leitos.
        """

        return self.db.consultar_tabela(
            self.tabela,
            limite
        )

    # =========================================================
    # TOTAL DE REGISTROS
    # =========================================================

    def total_registros(self):
        """
        Retorna a quantidade total de registros.
        """

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
        """
        Retorna o total de leitos existentes.
        """

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
        """
        Retorna o total de leitos SUS.
        """

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
        """
        Retorna o total de leitos de UTI existentes.
        """

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
        """
        Retorna o total de leitos agrupado por UF.
        """

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
        """
        Retorna o total de leitos agrupado por município.
        """

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
        """
        Retorna o total de leitos agrupado por região.
        """

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
        Retorna os dados de TB_LEITOS no formato
        esperado pela LeitosView.
        """

        query = f"""
            SELECT
                ID_LEITO,
                COMP,
                REGIAO,
                UF,
                CO_IBGE,
                MUNICIPIO,
                MOTIVO_DESABILITACAO,
                CNES,
                NOME_ESTABELECIMENTO,
                RAZAO_SOCIAL,
                TP_GESTAO,
                CO_TIPO_UNIDADE,
                DS_TIPO_UNIDADE,
                NATUREZA_JURIDICA,
                DESC_NATUREZA_JURIDICA,
                NO_LOGRADOURO,
                NU_ENDERECO,
                NO_COMPLEMENTO,
                NO_BAIRRO,
                CO_CEP,
                NU_TELEFONE,
                NO_EMAIL,
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
                UTI_CORONARIANA_SUS,
                DT_IMPORTACAO
            FROM {self.tabela}
            ORDER BY NOME_ESTABELECIMENTO
        """

        return self.db.executar_query_sql(query)

    # =========================================================
    # BUSCAR MUNICÍPIO
    # =========================================================

    def buscar_municipio(self, municipio):
        """
        Busca registros pelo nome do município.
        """

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
        """
        Busca registros pelo nome do estabelecimento.
        """

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
        """
        Importa um CSV diretamente para TB_LEITOS.
        """

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
        """
        Remove todos os registros da tabela.
        """

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