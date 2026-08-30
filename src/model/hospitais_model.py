import pandas as pd


class HospitaisModel:
    """
    Model responsável pelo acesso aos dados hospitalares
    armazenados na tabela TB_LEITOS do Oracle.

    A consolidação dos registros por CNES é realizada
    diretamente no Oracle para reduzir o volume de dados
    transferido para o Python.
    """

    def __init__(self, db):
        self.db = db

    # =========================================================
    # DADOS PRINCIPAIS
    # =========================================================

    def listar_dados(self):
        """
        Retorna os estabelecimentos hospitalares consolidados
        diretamente no Oracle.

        Em vez de retornar todas as linhas da TB_LEITOS,
        o Oracle agrupa os registros por CNES e retorna
        somente um registro por estabelecimento.

        Isso reduz significativamente:
        - dados transferidos do Oracle;
        - processamento no Pandas;
        - tempo de consolidação na View.
        """

        query = """
            SELECT

                CNES,

                MAX(REGIAO)
                    AS REGIAO,

                MAX(UF)
                    AS UF,

                MAX(CO_IBGE)
                    AS CO_IBGE,

                MAX(MUNICIPIO)
                    AS MUNICIPIO,

                MAX(MOTIVO_DESABILITACAO)
                    AS MOTIVO_DESABILITACAO,

                MAX(NOME_ESTABELECIMENTO)
                    AS NOME_ESTABELECIMENTO,

                MAX(RAZAO_SOCIAL)
                    AS RAZAO_SOCIAL,

                MAX(TP_GESTAO)
                    AS TP_GESTAO,

                MAX(CO_TIPO_UNIDADE)
                    AS CO_TIPO_UNIDADE,

                MAX(DS_TIPO_UNIDADE)
                    AS DS_TIPO_UNIDADE,

                MAX(NATUREZA_JURIDICA)
                    AS NATUREZA_JURIDICA,

                MAX(DESC_NATUREZA_JURIDICA)
                    AS DESC_NATUREZA_JURIDICA,

                MAX(NO_LOGRADOURO)
                    AS NO_LOGRADOURO,

                MAX(NU_ENDERECO)
                    AS NU_ENDERECO,

                MAX(NO_COMPLEMENTO)
                    AS NO_COMPLEMENTO,

                MAX(NO_BAIRRO)
                    AS NO_BAIRRO,

                MAX(CO_CEP)
                    AS CO_CEP,

                MAX(NU_TELEFONE)
                    AS NU_TELEFONE,

                MAX(NO_EMAIL)
                    AS NO_EMAIL,

                NVL(
                    SUM(LEITOS_EXISTENTES),
                    0
                ) AS LEITOS_EXISTENTES,

                NVL(
                    SUM(LEITOS_SUS),
                    0
                ) AS LEITOS_SUS,

                NVL(
                    SUM(UTI_TOTAL_EXIST),
                    0
                ) AS UTI_TOTAL_EXIST,

                NVL(
                    SUM(UTI_TOTAL_SUS),
                    0
                ) AS UTI_TOTAL_SUS,

                NVL(
                    SUM(UTI_ADULTO_EXIST),
                    0
                ) AS UTI_ADULTO_EXIST,

                NVL(
                    SUM(UTI_ADULTO_SUS),
                    0
                ) AS UTI_ADULTO_SUS,

                NVL(
                    SUM(UTI_PEDIATRICO_EXIST),
                    0
                ) AS UTI_PEDIATRICO_EXIST,

                NVL(
                    SUM(UTI_PEDIATRICO_SUS),
                    0
                ) AS UTI_PEDIATRICO_SUS,

                NVL(
                    SUM(UTI_NEONATAL_EXIST),
                    0
                ) AS UTI_NEONATAL_EXIST,

                NVL(
                    SUM(UTI_NEONATAL_SUS),
                    0
                ) AS UTI_NEONATAL_SUS,

                NVL(
                    SUM(UTI_QUEIMADO_EXIST),
                    0
                ) AS UTI_QUEIMADO_EXIST,

                NVL(
                    SUM(UTI_QUEIMADO_SUS),
                    0
                ) AS UTI_QUEIMADO_SUS,

                NVL(
                    SUM(UTI_CORONARIANA_EXIST),
                    0
                ) AS UTI_CORONARIANA_EXIST,

                NVL(
                    SUM(UTI_CORONARIANA_SUS),
                    0
                ) AS UTI_CORONARIANA_SUS,

                MAX(DT_IMPORTACAO)
                    AS DT_IMPORTACAO

            FROM TB_LEITOS

            WHERE CNES IS NOT NULL

            GROUP BY CNES

            ORDER BY NOME_ESTABELECIMENTO
        """

        return self.db.fetch_data(query)

    # =========================================================
    # DADOS PARA A VIEW
    # =========================================================

    def dados_para_view(self):
        """
        Retorna os dados necessários para a tela de Hospitais.

        A consolidação já é realizada pelo Oracle.
        """

        return self.listar_dados()

    # =========================================================
    # INDICADORES
    # =========================================================

    def obter_indicadores(self):
        """
        Calcula os principais indicadores hospitalares
        diretamente no Oracle.

        A consulta consolida primeiro por CNES para garantir
        que os valores representem estabelecimentos únicos.
        """

        query = """
            SELECT

                COUNT(*) AS TOTAL_HOSPITAIS,

                SUM(
                    CASE
                        WHEN MOTIVO_DESABILITACAO IS NULL
                        THEN 1
                        ELSE 0
                    END
                ) AS HOSPITAIS_ATIVOS,

                NVL(
                    SUM(LEITOS_EXISTENTES),
                    0
                ) AS LEITOS_TOTAIS,

                NVL(
                    SUM(LEITOS_SUS),
                    0
                ) AS LEITOS_SUS,

                NVL(
                    SUM(UTI_TOTAL_EXIST),
                    0
                ) AS UTI_TOTAL,

                NVL(
                    SUM(UTI_TOTAL_SUS),
                    0
                ) AS UTI_SUS

            FROM (

                SELECT

                    CNES,

                    MAX(MOTIVO_DESABILITACAO)
                        AS MOTIVO_DESABILITACAO,

                    NVL(
                        SUM(LEITOS_EXISTENTES),
                        0
                    ) AS LEITOS_EXISTENTES,

                    NVL(
                        SUM(LEITOS_SUS),
                        0
                    ) AS LEITOS_SUS,

                    NVL(
                        SUM(UTI_TOTAL_EXIST),
                        0
                    ) AS UTI_TOTAL_EXIST,

                    NVL(
                        SUM(UTI_TOTAL_SUS),
                        0
                    ) AS UTI_TOTAL_SUS

                FROM TB_LEITOS

                WHERE CNES IS NOT NULL

                GROUP BY CNES
            )
        """

        df = self.db.fetch_data(query)

        if df.empty:

            return {
                "total_hospitais": 0,
                "hospitais_ativos": 0,
                "leitos_totais": 0,
                "leitos_sus": 0,
                "uti_total": 0,
                "uti_sus": 0,
            }

        linha = df.iloc[0]

        return {
            "total_hospitais": int(
                linha["TOTAL_HOSPITAIS"] or 0
            ),

            "hospitais_ativos": int(
                linha["HOSPITAIS_ATIVOS"] or 0
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
    # HOSPITAIS POR REGIÃO
    # =========================================================

    def hospitais_por_regiao(self):

        query = """
            SELECT
                REGIAO,
                COUNT(DISTINCT CNES) AS TOTAL

            FROM TB_LEITOS

            WHERE
                REGIAO IS NOT NULL
                AND CNES IS NOT NULL

            GROUP BY REGIAO

            ORDER BY TOTAL DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # HOSPITAIS POR UF
    # =========================================================

    def hospitais_por_uf(self):

        query = """
            SELECT
                UF,
                COUNT(DISTINCT CNES) AS TOTAL

            FROM TB_LEITOS

            WHERE
                UF IS NOT NULL
                AND CNES IS NOT NULL

            GROUP BY UF

            ORDER BY TOTAL DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # LEITOS POR REGIÃO
    # =========================================================

    def leitos_por_regiao(self):

        query = """
            SELECT
                REGIAO,

                NVL(
                    SUM(LEITOS_EXISTENTES),
                    0
                ) AS LEITOS_EXISTENTES,

                NVL(
                    SUM(LEITOS_SUS),
                    0
                ) AS LEITOS_SUS,

                NVL(
                    SUM(UTI_TOTAL_EXIST),
                    0
                ) AS UTI_TOTAL,

                NVL(
                    SUM(UTI_TOTAL_SUS),
                    0
                ) AS UTI_SUS

            FROM TB_LEITOS

            WHERE
                REGIAO IS NOT NULL
                AND CNES IS NOT NULL

            GROUP BY REGIAO

            ORDER BY LEITOS_EXISTENTES DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # LEITOS POR UF
    # =========================================================

    def leitos_por_uf(self):

        query = """
            SELECT
                UF,

                NVL(
                    SUM(LEITOS_EXISTENTES),
                    0
                ) AS LEITOS_EXISTENTES,

                NVL(
                    SUM(LEITOS_SUS),
                    0
                ) AS LEITOS_SUS,

                NVL(
                    SUM(UTI_TOTAL_EXIST),
                    0
                ) AS UTI_TOTAL,

                NVL(
                    SUM(UTI_TOTAL_SUS),
                    0
                ) AS UTI_SUS

            FROM TB_LEITOS

            WHERE
                UF IS NOT NULL
                AND CNES IS NOT NULL

            GROUP BY UF

            ORDER BY LEITOS_EXISTENTES DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # GESTÃO
    # =========================================================

    def hospitais_por_gestao(self):

        query = """
            SELECT
                TP_GESTAO,
                COUNT(DISTINCT CNES) AS TOTAL

            FROM TB_LEITOS

            WHERE
                TP_GESTAO IS NOT NULL
                AND CNES IS NOT NULL

            GROUP BY TP_GESTAO

            ORDER BY TOTAL DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # TIPO DE UNIDADE
    # =========================================================

    def hospitais_por_tipo(self):

        query = """
            SELECT
                DS_TIPO_UNIDADE,
                COUNT(DISTINCT CNES) AS TOTAL

            FROM TB_LEITOS

            WHERE
                DS_TIPO_UNIDADE IS NOT NULL
                AND CNES IS NOT NULL

            GROUP BY DS_TIPO_UNIDADE

            ORDER BY TOTAL DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # BUSCA DE HOSPITAIS
    # =========================================================

    def buscar_hospitais(self, termo=""):

        termo = str(termo).strip()

        if not termo:

            return self.listar_dados()

        query = """
            SELECT

                CNES,

                MAX(REGIAO)
                    AS REGIAO,

                MAX(UF)
                    AS UF,

                MAX(CO_IBGE)
                    AS CO_IBGE,

                MAX(MUNICIPIO)
                    AS MUNICIPIO,

                MAX(MOTIVO_DESABILITACAO)
                    AS MOTIVO_DESABILITACAO,

                MAX(NOME_ESTABELECIMENTO)
                    AS NOME_ESTABELECIMENTO,

                MAX(RAZAO_SOCIAL)
                    AS RAZAO_SOCIAL,

                MAX(TP_GESTAO)
                    AS TP_GESTAO,

                MAX(CO_TIPO_UNIDADE)
                    AS CO_TIPO_UNIDADE,

                MAX(DS_TIPO_UNIDADE)
                    AS DS_TIPO_UNIDADE,

                MAX(NATUREZA_JURIDICA)
                    AS NATUREZA_JURIDICA,

                MAX(DESC_NATUREZA_JURIDICA)
                    AS DESC_NATUREZA_JURIDICA,

                MAX(NO_LOGRADOURO)
                    AS NO_LOGRADOURO,

                MAX(NU_ENDERECO)
                    AS NU_ENDERECO,

                MAX(NO_COMPLEMENTO)
                    AS NO_COMPLEMENTO,

                MAX(NO_BAIRRO)
                    AS NO_BAIRRO,

                MAX(CO_CEP)
                    AS CO_CEP,

                MAX(NU_TELEFONE)
                    AS NU_TELEFONE,

                MAX(NO_EMAIL)
                    AS NO_EMAIL,

                NVL(
                    SUM(LEITOS_EXISTENTES),
                    0
                ) AS LEITOS_EXISTENTES,

                NVL(
                    SUM(LEITOS_SUS),
                    0
                ) AS LEITOS_SUS,

                NVL(
                    SUM(UTI_TOTAL_EXIST),
                    0
                ) AS UTI_TOTAL_EXIST,

                NVL(
                    SUM(UTI_TOTAL_SUS),
                    0
                ) AS UTI_TOTAL_SUS,

                NVL(
                    SUM(UTI_ADULTO_EXIST),
                    0
                ) AS UTI_ADULTO_EXIST,

                NVL(
                    SUM(UTI_ADULTO_SUS),
                    0
                ) AS UTI_ADULTO_SUS,

                NVL(
                    SUM(UTI_PEDIATRICO_EXIST),
                    0
                ) AS UTI_PEDIATRICO_EXIST,

                NVL(
                    SUM(UTI_PEDIATRICO_SUS),
                    0
                ) AS UTI_PEDIATRICO_SUS,

                NVL(
                    SUM(UTI_NEONATAL_EXIST),
                    0
                ) AS UTI_NEONATAL_EXIST,

                NVL(
                    SUM(UTI_NEONATAL_SUS),
                    0
                ) AS UTI_NEONATAL_SUS,

                NVL(
                    SUM(UTI_QUEIMADO_EXIST),
                    0
                ) AS UTI_QUEIMADO_EXIST,

                NVL(
                    SUM(UTI_QUEIMADO_SUS),
                    0
                ) AS UTI_QUEIMADO_SUS,

                NVL(
                    SUM(UTI_CORONARIANA_EXIST),
                    0
                ) AS UTI_CORONARIANA_EXIST,

                NVL(
                    SUM(UTI_CORONARIANA_SUS),
                    0
                ) AS UTI_CORONARIANA_SUS,

                MAX(DT_IMPORTACAO)
                    AS DT_IMPORTACAO

            FROM TB_LEITOS

            WHERE
                CNES IS NOT NULL

                AND (
                    UPPER(NOME_ESTABELECIMENTO)
                        LIKE '%' || UPPER(:1) || '%'

                    OR UPPER(MUNICIPIO)
                        LIKE '%' || UPPER(:2) || '%'

                    OR UPPER(UF)
                        LIKE '%' || UPPER(:3) || '%'

                    OR TO_CHAR(CNES)
                        LIKE '%' || :4 || '%'
                )

            GROUP BY CNES

            ORDER BY NOME_ESTABELECIMENTO
        """

        return self.db.fetch_data(
            query,
            [
                termo,
                termo,
                termo,
                termo,
            ]
        )

    # =========================================================
    # TOTAL DE REGISTROS
    # =========================================================

    def total_registros(self):

        query = """
            SELECT
                COUNT(*) AS TOTAL

            FROM TB_LEITOS
        """

        df = self.db.fetch_data(query)

        if df.empty:
            return 0

        return int(
            df.iloc[0]["TOTAL"] or 0
        )