import pandas as pd


class HospitaisModel:
    """
    Model responsável pelo acesso aos dados hospitalares
    armazenados na tabela TB_GERAL do Oracle.
    """

    def __init__(self, db):
        self.db = db

    # =========================================================
    # DADOS PRINCIPAIS DO DASHBOARD
    # =========================================================

    def obter_dados_dashboard(self):
        """
        Retorna os dados hospitalares diretamente do Oracle.
        Não utiliza CSV nem dados fictícios.
        """

        query = """
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
                DT_IMPORTACAO,
                COMP_LEITOS
            FROM TB_GERAL
        """

        return self.db.fetch_data(query)

    # =========================================================
    # LISTAR HOSPITAIS
    # =========================================================

    def listar_hospitais(self):

        query = """
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
                DT_IMPORTACAO,
                COMP_LEITOS
            FROM TB_GERAL
            ORDER BY NOME_ESTABELECIMENTO
        """

        return self.db.fetch_data(query)

    # =========================================================
    # INDICADORES
    # =========================================================

    def obter_indicadores(self):

        query = """
            SELECT
                COUNT(DISTINCT CNES) AS TOTAL_HOSPITAIS,

                COUNT(
                    DISTINCT CASE
                        WHEN MOTIVO_DESABILITACAO IS NULL
                        THEN CNES
                    END
                ) AS HOSPITAIS_ATIVOS,

                NVL(SUM(LEITOS_EXISTENTES), 0)
                    AS LEITOS_TOTAIS,

                NVL(SUM(LEITOS_SUS), 0)
                    AS LEITOS_SUS,

                NVL(SUM(UTI_TOTAL_EXIST), 0)
                    AS UTI_TOTAL,

                NVL(SUM(UTI_TOTAL_SUS), 0)
                    AS UTI_TOTAL_SUS

            FROM TB_GERAL
        """

        df = self.db.fetch_data(query)

        if df.empty:
            return {
                "total_hospitais": 0,
                "hospitais_ativos": 0,
                "leitos_totais": 0,
                "leitos_sus": 0,
                "uti_total": 0,
                "uti_total_sus": 0,
            }

        linha = df.iloc[0]

        return {
            "total_hospitais": int(linha["TOTAL_HOSPITAIS"] or 0),
            "hospitais_ativos": int(linha["HOSPITAIS_ATIVOS"] or 0),
            "leitos_totais": int(linha["LEITOS_TOTAIS"] or 0),
            "leitos_sus": int(linha["LEITOS_SUS"] or 0),
            "uti_total": int(linha["UTI_TOTAL"] or 0),
            "uti_total_sus": int(linha["UTI_TOTAL_SUS"] or 0),
        }

    # =========================================================
    # HOSPITAIS POR REGIÃO
    # =========================================================

    def hospitais_por_regiao(self):

        query = """
            SELECT
                REGIAO,
                COUNT(DISTINCT CNES) AS TOTAL
            FROM TB_GERAL
            WHERE REGIAO IS NOT NULL
            GROUP BY REGIAO
            ORDER BY TOTAL DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # HOSPITAIS POR GESTÃO
    # =========================================================

    def hospitais_por_gestao(self):

        query = """
            SELECT
                TP_GESTAO,
                COUNT(DISTINCT CNES) AS TOTAL
            FROM TB_GERAL
            WHERE TP_GESTAO IS NOT NULL
            GROUP BY TP_GESTAO
            ORDER BY TOTAL DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # HOSPITAIS POR TIPO DE UNIDADE
    # =========================================================

    def hospitais_por_tipo(self):

        query = """
            SELECT
                DS_TIPO_UNIDADE,
                COUNT(DISTINCT CNES) AS TOTAL
            FROM TB_GERAL
            WHERE DS_TIPO_UNIDADE IS NOT NULL
            GROUP BY DS_TIPO_UNIDADE
            ORDER BY TOTAL DESC
        """

        return self.db.fetch_data(query)

    # =========================================================
    # HOSPITAIS POR PORTE
    # =========================================================

    def hospitais_por_porte(self):

        query = """
            SELECT
                PORTE,
                COUNT(*) AS TOTAL
            FROM
            (
                SELECT
                    CNES,

                    CASE
                        WHEN MAX(NVL(LEITOS_EXISTENTES, 0)) < 50
                            THEN 'Pequeno'

                        WHEN MAX(NVL(LEITOS_EXISTENTES, 0)) < 150
                            THEN 'Médio'

                        WHEN MAX(NVL(LEITOS_EXISTENTES, 0)) < 300
                            THEN 'Grande'

                        ELSE 'Extra-grande'
                    END AS PORTE

                FROM TB_GERAL

                WHERE CNES IS NOT NULL

                GROUP BY CNES
            )

            GROUP BY PORTE

            ORDER BY
                CASE PORTE
                    WHEN 'Pequeno' THEN 1
                    WHEN 'Médio' THEN 2
                    WHEN 'Grande' THEN 3
                    WHEN 'Extra-grande' THEN 4
                END
        """

        return self.db.fetch_data(query)

    # =========================================================
    # DADOS DO MAPA
    # =========================================================

    def dados_mapa(self):

        query = """
            SELECT
                CNES,
                NOME_ESTABELECIMENTO,
                MUNICIPIO,
                UF,
                REGIAO,
                LEITOS_EXISTENTES,
                LEITOS_SUS
            FROM TB_GERAL
            WHERE CNES IS NOT NULL
        """

        return self.db.fetch_data(query)

    # =========================================================
    # BUSCAR HOSPITAIS
    # =========================================================

    def buscar_hospitais(self, termo):

        if not termo:
            return self.listar_hospitais()

        termo = str(termo).strip()

        query = """
            SELECT
                CNES,
                NOME_ESTABELECIMENTO,
                MUNICIPIO,
                UF,
                DS_TIPO_UNIDADE,
                TP_GESTAO,
                LEITOS_EXISTENTES,
                LEITOS_SUS,
                UTI_TOTAL_EXIST,
                UTI_TOTAL_SUS,
                MOTIVO_DESABILITACAO
            FROM TB_GERAL

            WHERE
                UPPER(NOME_ESTABELECIMENTO)
                    LIKE '%' || UPPER(:1) || '%'

                OR UPPER(MUNICIPIO)
                    LIKE '%' || UPPER(:2) || '%'

                OR TO_CHAR(CNES)
                    LIKE '%' || :3 || '%'

            ORDER BY NOME_ESTABELECIMENTO
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
    # RESUMO POR ESTABELECIMENTO
    # =========================================================

    def resumo_estabelecimentos(self):

        query = """
            SELECT
                CNES,

                MAX(NOME_ESTABELECIMENTO)
                    AS NOME_ESTABELECIMENTO,

                MAX(MUNICIPIO)
                    AS MUNICIPIO,

                MAX(UF)
                    AS UF,

                MAX(REGIAO)
                    AS REGIAO,

                MAX(TP_GESTAO)
                    AS TP_GESTAO,

                MAX(DS_TIPO_UNIDADE)
                    AS DS_TIPO_UNIDADE,

                SUM(NVL(LEITOS_EXISTENTES, 0))
                    AS LEITOS_EXISTENTES,

                SUM(NVL(LEITOS_SUS, 0))
                    AS LEITOS_SUS,

                SUM(NVL(UTI_TOTAL_EXIST, 0))
                    AS UTI_TOTAL_EXIST,

                SUM(NVL(UTI_TOTAL_SUS, 0))
                    AS UTI_TOTAL_SUS

            FROM TB_GERAL

            WHERE CNES IS NOT NULL

            GROUP BY CNES

            ORDER BY NOME_ESTABELECIMENTO
        """

        return self.db.fetch_data(query)

    # =========================================================
    # ÚLTIMA IMPORTAÇÃO
    # =========================================================

    def obter_ultima_importacao(self):

        query = """
            SELECT
                MAX(DT_IMPORTACAO) AS ULTIMA_IMPORTACAO
            FROM TB_GERAL
        """

        df = self.db.fetch_data(query)

        if df.empty:
            return None

        return df.iloc[0]["ULTIMA_IMPORTACAO"]

    # =========================================================
    # TOTAL DE REGISTROS
    # =========================================================

    def total_registros(self):

        query = """
            SELECT COUNT(*) AS TOTAL
            FROM TB_GERAL
        """

        df = self.db.fetch_data(query)

        if df.empty:
            return 0

        return int(df.iloc[0]["TOTAL"] or 0)