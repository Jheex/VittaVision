import pandas as pd


class InternacoesModel:
    """
    Model responsável pelas operações de dados
    relacionadas às internações hospitalares.
    """

    def __init__(self, db):
        self.db = db
        self.tabela = "TB_INTERNACOES"

    # =========================================================
    # LISTAR INTERNAÇÕES
    # =========================================================

    def listar_internacoes(self, limite=1000):
        """
        Retorna os registros de internações.
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
    # TOTAL DE INTERNAÇÕES
    # =========================================================

    def total_internacoes(self):
        """
        Retorna o total de internações considerando
        a coluna VL_TOTAL_2025.
        """

        query = f"""
            SELECT
                NVL(SUM(VL_TOTAL_2025), 0) AS TOTAL
            FROM {self.tabela}
        """

        df = self.db.executar_query_sql(query)

        if df.empty:
            return 0

        return float(df.iloc[0]["TOTAL"])

    # =========================================================
    # INTERNAÇÕES POR MUNICÍPIO
    # =========================================================

    def internacoes_por_municipio(self):
        """
        Retorna o total de internações agrupado por município.
        """

        query = f"""
            SELECT
                MUNICIPIO,
                NVL(SUM(VL_TOTAL_2025), 0) AS TOTAL
            FROM {self.tabela}
            GROUP BY MUNICIPIO
            ORDER BY TOTAL DESC
        """

        return self.db.executar_query_sql(query)

    # =========================================================
    # INTERNAÇÕES POR UF
    # =========================================================

    def internacoes_por_uf(self):
        """
        Retorna o total de internações agrupado por UF.
        """

        query = f"""
            SELECT
                CODIGO_UF,
                NVL(SUM(VL_TOTAL_2025), 0) AS TOTAL
            FROM {self.tabela}
            GROUP BY CODIGO_UF
            ORDER BY TOTAL DESC
        """

        return self.db.executar_query_sql(query)

    # =========================================================
    # EVOLUÇÃO MENSAL
    # =========================================================

    def evolucao_mensal(self):
        """
        Retorna o total de internações por mês.
        """

        query = f"""
            SELECT
                NVL(SUM(VL_JAN_2025), 0) AS JAN_2025,
                NVL(SUM(VL_FEV_2025), 0) AS FEV_2025,
                NVL(SUM(VL_MAR_2025), 0) AS MAR_2025,
                NVL(SUM(VL_ABR_2025), 0) AS ABR_2025,
                NVL(SUM(VL_MAI_2025), 0) AS MAI_2025,
                NVL(SUM(VL_JUN_2025), 0) AS JUN_2025,
                NVL(SUM(VL_JUL_2025), 0) AS JUL_2025,
                NVL(SUM(VL_AGO_2025), 0) AS AGO_2025,
                NVL(SUM(VL_SET_2025), 0) AS SET_2025,
                NVL(SUM(VL_OUT_2025), 0) AS OUT_2025,
                NVL(SUM(VL_NOV_2025), 0) AS NOV_2025,
                NVL(SUM(VL_DEZ_2025), 0) AS DEZ_2025
            FROM {self.tabela}
        """

        df = self.db.executar_query_sql(query)

        if df.empty:
            return pd.DataFrame()

        meses = [
            "Jan/2025",
            "Fev/2025",
            "Mar/2025",
            "Abr/2025",
            "Mai/2025",
            "Jun/2025",
            "Jul/2025",
            "Ago/2025",
            "Set/2025",
            "Out/2025",
            "Nov/2025",
            "Dez/2025",
        ]

        valores = [
            df.iloc[0]["JAN_2025"],
            df.iloc[0]["FEV_2025"],
            df.iloc[0]["MAR_2025"],
            df.iloc[0]["ABR_2025"],
            df.iloc[0]["MAI_2025"],
            df.iloc[0]["JUN_2025"],
            df.iloc[0]["JUL_2025"],
            df.iloc[0]["AGO_2025"],
            df.iloc[0]["SET_2025"],
            df.iloc[0]["OUT_2025"],
            df.iloc[0]["NOV_2025"],
            df.iloc[0]["DEZ_2025"],
        ]

        return pd.DataFrame({
            "Mês": meses,
            "Internações": valores
        })

    # =========================================================
    # MAIORES MUNICÍPIOS
    # =========================================================

    def maiores_municipios(self, limite=10):
        """
        Retorna os municípios com maior número de internações.
        """

        limite = max(1, min(int(limite), 100))

        query = f"""
            SELECT
                MUNICIPIO,
                NVL(SUM(VL_TOTAL_2025), 0) AS TOTAL
            FROM {self.tabela}
            GROUP BY MUNICIPIO
            ORDER BY TOTAL DESC
            FETCH FIRST {limite} ROWS ONLY
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

        query = f"""
            SELECT *
            FROM {self.tabela}
            WHERE UPPER(MUNICIPIO) LIKE UPPER(:1)
            ORDER BY MUNICIPIO
        """

        # Como executar_query_sql atualmente não recebe parâmetros,
        # usamos diretamente o método de conexão.

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
    # IMPORTAR CSV
    # =========================================================

    def importar_csv(self, arquivo):
        """
        Importa um CSV diretamente para TB_INTERNACOES.
        """

        if arquivo is None:
            raise ValueError(
                "Nenhum arquivo foi enviado."
            )

        # -----------------------------------------------------
        # Leitura
        # -----------------------------------------------------

        df = pd.read_csv(
            arquivo,
            sep=";"
        )

        if df.empty:
            raise ValueError(
                "O arquivo CSV está vazio."
            )

        # -----------------------------------------------------
        # Padronização dos nomes
        # -----------------------------------------------------

        df.columns = [
            str(coluna)
            .strip()
            .upper()
            for coluna in df.columns
        ]

        # -----------------------------------------------------
        # Colunas esperadas
        # -----------------------------------------------------

        colunas_esperadas = [
            "CODIGO_MUNICIPIO",
            "MUNICIPIO",
            "CODIGO_UF",
            "VL_JAN_2025",
            "VL_FEV_2025",
            "VL_MAR_2025",
            "VL_ABR_2025",
            "VL_MAI_2025",
            "VL_JUN_2025",
            "VL_JUL_2025",
            "VL_AGO_2025",
            "VL_SET_2025",
            "VL_OUT_2025",
            "VL_NOV_2025",
            "VL_DEZ_2025",
            "VL_TOTAL_2025",
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

        # -----------------------------------------------------
        # Seleciona somente as colunas utilizadas
        # -----------------------------------------------------

        df = df[colunas_esperadas]

        # -----------------------------------------------------
        # Conversão dos campos numéricos
        # -----------------------------------------------------

        colunas_numericas = [
            "CODIGO_MUNICIPIO",
            "CODIGO_UF",
            "VL_JAN_2025",
            "VL_FEV_2025",
            "VL_MAR_2025",
            "VL_ABR_2025",
            "VL_MAI_2025",
            "VL_JUN_2025",
            "VL_JUL_2025",
            "VL_AGO_2025",
            "VL_SET_2025",
            "VL_OUT_2025",
            "VL_NOV_2025",
            "VL_DEZ_2025",
            "VL_TOTAL_2025",
        ]

        for coluna in colunas_numericas:

            df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce"
            )

        # -----------------------------------------------------
        # Importação
        # -----------------------------------------------------

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