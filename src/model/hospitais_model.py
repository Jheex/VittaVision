import pandas as pd


class HospitaisModel:
    """
    Model responsável pelo acesso aos dados hospitalares
    armazenados na tabela TB_GERAL do Oracle.

    IMPORTANTE:
    A TB_GERAL possui dados agregados por município.
    Não possui CNES, nome de hospital ou coordenadas geográficas.
    """

    def __init__(self, db):
        self.db = db

    # =========================================================
    # DADOS PRINCIPAIS
    # =========================================================

    def listar_dados(self):
        """
        Retorna os dados completos da TB_GERAL.
        """

        query = """
            SELECT
                ID_GERAL,
                COD_IBGE,
                COD_UF,
                UF,
                MUNICIPIO,
                POPULACAO_ESTIMADA,

                INTERNACOES_JAN_2025,
                INTERNACOES_FEV_2025,
                INTERNACOES_MAR_2025,
                INTERNACOES_ABR_2025,
                INTERNACOES_MAI_2025,
                INTERNACOES_JUN_2025,
                INTERNACOES_JUL_2025,
                INTERNACOES_AGO_2025,
                INTERNACOES_SET_2025,
                INTERNACOES_OUT_2025,
                INTERNACOES_NOV_2025,
                INTERNACOES_DEZ_2025,

                INTERNACOES_TOTAL_2025,

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

                COMP_LEITOS

            FROM TB_GERAL

            ORDER BY MUNICIPIO
        """

        return self.db.fetch_data(query)

    # =========================================================
    # INDICADORES
    # =========================================================

    def obter_indicadores(self):
        """
        Calcula os indicadores diretamente no Oracle.
        """

        query = """
            SELECT

                COUNT(DISTINCT COD_IBGE)
                    AS TOTAL_MUNICIPIOS,

                NVL(SUM(POPULACAO_ESTIMADA), 0)
                    AS POPULACAO_TOTAL,

                NVL(SUM(INTERNACOES_TOTAL_2025), 0)
                    AS INTERNACOES_TOTAL,

                NVL(SUM(LEITOS_EXISTENTES), 0)
                    AS LEITOS_TOTAIS,

                NVL(SUM(LEITOS_SUS), 0)
                    AS LEITOS_SUS,

                NVL(SUM(UTI_TOTAL_EXIST), 0)
                    AS UTI_TOTAL,

                NVL(SUM(UTI_TOTAL_SUS), 0)
                    AS UTI_SUS

            FROM TB_GERAL
        """

        df = self.db.fetch_data(query)

        if df.empty:
            return {
                "total_municipios": 0,
                "populacao_total": 0,
                "internacoes_total": 0,
                "leitos_totais": 0,
                "leitos_sus": 0,
                "uti_total": 0,
                "uti_sus": 0,
            }

        linha = df.iloc[0]

        return {
            "total_municipios": int(
                linha["TOTAL_MUNICIPIOS"] or 0
            ),

            "populacao_total": int(
                linha["POPULACAO_TOTAL"] or 0
            ),

            "internacoes_total": int(
                linha["INTERNACOES_TOTAL"] or 0
            ),

            "leitos_totais": int(
                linha["LEITOS_TOTAIS"] or 0
            ),

            "leitos_sus": int(
                linha["LEITOS_SUS"] or 0
            ),

            "uti_total": int(
                linha["UTI_TOTAL"] or 0
            ),

            "uti_sus": int(
                linha["UTI_SUS"] or 0
            ),
        }

    # =========================================================
    # MUNICÍPIOS POR UF
    # =========================================================

    def municipios_por_uf(self):
        """
        Retorna a quantidade de municípios por UF.
        """

        query = """
            SELECT
                UF,
                COUNT(DISTINCT COD_IBGE) AS TOTAL
            FROM TB_GERAL
            WHERE UF IS NOT NULL
            GROUP BY UF
            ORDER BY TOTAL DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # INTERNAÇÕES POR MÊS
    # =========================================================

    def internacoes_por_mes(self):
        """
        Retorna as internações mensais de 2025.

        Os dados são provenientes diretamente
        das colunas da TB_GERAL.
        """

        query = """
            SELECT
                NVL(SUM(INTERNACOES_JAN_2025), 0)
                    AS JAN,

                NVL(SUM(INTERNACOES_FEV_2025), 0)
                    AS FEV,

                NVL(SUM(INTERNACOES_MAR_2025), 0)
                    AS MAR,

                NVL(SUM(INTERNACOES_ABR_2025), 0)
                    AS ABR,

                NVL(SUM(INTERNACOES_MAI_2025), 0)
                    AS MAI,

                NVL(SUM(INTERNACOES_JUN_2025), 0)
                    AS JUN,

                NVL(SUM(INTERNACOES_JUL_2025), 0)
                    AS JUL,

                NVL(SUM(INTERNACOES_AGO_2025), 0)
                    AS AGO,

                NVL(SUM(INTERNACOES_SET_2025), 0)
                    AS SET,

                NVL(SUM(INTERNACOES_OUT_2025), 0)
                    AS OUT,

                NVL(SUM(INTERNACOES_NOV_2025), 0)
                    AS NOV,

                NVL(SUM(INTERNACOES_DEZ_2025), 0)
                    AS DEZ

            FROM TB_GERAL
        """

        return self.db.fetch_data(query)

    # =========================================================
    # LEITOS POR UF
    # =========================================================

    def leitos_por_uf(self):
        """
        Retorna leitos existentes e SUS por UF.
        """

        query = """
            SELECT
                UF,

                NVL(SUM(LEITOS_EXISTENTES), 0)
                    AS LEITOS_EXISTENTES,

                NVL(SUM(LEITOS_SUS), 0)
                    AS LEITOS_SUS

            FROM TB_GERAL

            WHERE UF IS NOT NULL

            GROUP BY UF

            ORDER BY LEITOS_EXISTENTES DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # UTIS POR UF
    # =========================================================

    def utis_por_uf(self):
        """
        Retorna quantidade de UTIs por UF.
        """

        query = """
            SELECT
                UF,

                NVL(SUM(UTI_TOTAL_EXIST), 0)
                    AS UTI_TOTAL,

                NVL(SUM(UTI_TOTAL_SUS), 0)
                    AS UTI_SUS

            FROM TB_GERAL

            WHERE UF IS NOT NULL

            GROUP BY UF

            ORDER BY UTI_TOTAL DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # BUSCA POR MUNICÍPIO
    # =========================================================

    def buscar_municipios(self, termo=""):
        """
        Busca municípios por nome, UF ou código IBGE.
        """

        termo = str(termo).strip()

        if not termo:
            return self.listar_dados()

        query = """
            SELECT
                ID_GERAL,
                COD_IBGE,
                COD_UF,
                UF,
                MUNICIPIO,
                POPULACAO_ESTIMADA,

                INTERNACOES_TOTAL_2025,

                LEITOS_EXISTENTES,
                LEITOS_SUS,

                UTI_TOTAL_EXIST,
                UTI_TOTAL_SUS,

                COMP_LEITOS

            FROM TB_GERAL

            WHERE
                UPPER(MUNICIPIO)
                    LIKE '%' || UPPER(:1) || '%'

                OR UPPER(UF)
                    LIKE '%' || UPPER(:2) || '%'

                OR TO_CHAR(COD_IBGE)
                    LIKE '%' || :3 || '%'

            ORDER BY MUNICIPIO
        """

        return self.db.fetch_data(
            query,
            [
                termo,
                termo,
                termo
            ]
        )

    # =========================================================
    # TOP MUNICÍPIOS POR INTERNAÇÕES
    # =========================================================

    def top_municipios_internacoes(self, limite=10):
        """
        Retorna os municípios com maior quantidade
        de internações em 2025.
        """

        limite = max(1, min(int(limite), 100))

        query = f"""
            SELECT *
            FROM
            (
                SELECT
                    MUNICIPIO,
                    UF,
                    INTERNACOES_TOTAL_2025,
                    LEITOS_EXISTENTES,
                    LEITOS_SUS,
                    UTI_TOTAL_EXIST,
                    UTI_TOTAL_SUS

                FROM TB_GERAL

                WHERE MUNICIPIO IS NOT NULL

                ORDER BY INTERNACOES_TOTAL_2025 DESC
            )

            FETCH FIRST {limite} ROWS ONLY
        """

        return self.db.fetch_data(query)

    # =========================================================
    # TOP MUNICÍPIOS POR LEITOS
    # =========================================================

    def top_municipios_leitos(self, limite=10):
        """
        Retorna os municípios com maior quantidade de leitos.
        """

        limite = max(1, min(int(limite), 100))

        query = f"""
            SELECT *
            FROM
            (
                SELECT
                    MUNICIPIO,
                    UF,
                    LEITOS_EXISTENTES,
                    LEITOS_SUS,
                    UTI_TOTAL_EXIST,
                    UTI_TOTAL_SUS,
                    INTERNACOES_TOTAL_2025

                FROM TB_GERAL

                WHERE MUNICIPIO IS NOT NULL

                ORDER BY LEITOS_EXISTENTES DESC
            )

            FETCH FIRST {limite} ROWS ONLY
        """

        return self.db.fetch_data(query)

    # =========================================================
    # ÚLTIMA INFORMAÇÃO DE COMPETÊNCIA
    # =========================================================

    def obter_competencia(self):
        """
        Retorna a competência dos dados disponíveis.
        """

        return "2025"

    # =========================================================
    # TOTAL DE REGISTROS
    # =========================================================

    def total_registros(self):
        """
        Retorna o total de registros da TB_GERAL.
        """

        query = """
            SELECT COUNT(*) AS TOTAL
            FROM TB_GERAL
        """

        df = self.db.fetch_data(query)

        if df.empty:
            return 0

        return int(df.iloc[0]["TOTAL"] or 0)