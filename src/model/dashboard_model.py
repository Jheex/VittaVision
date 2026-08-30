import pandas as pd


class DashboardModel:
    """
    Model responsável por centralizar os dados utilizados
    no Dashboard principal do VittaVision.

    Os dados são obtidos exclusivamente do Oracle Database
    através dos modelos existentes:
        - HospitaisModel
        - InternacoesModel
        - LeitosModel
    """

    def __init__(
        self,
        db,
        hospitais_model,
        internacoes_model,
        leitos_model
    ):
        self.db = db
        self.hospitais_model = hospitais_model
        self.internacoes_model = internacoes_model
        self.leitos_model = leitos_model

    # =========================================================
    # RESUMO GERAL
    # =========================================================

    def obter_resumo(self):
        """
        Retorna os principais indicadores do sistema.

        Nenhum valor é fixado manualmente.
        Todos os indicadores são obtidos do banco.
        """

        total_internacoes = (
            self.internacoes_model.total_internacoes()
        )

        total_municipios = self._contar_municipios()

        total_hospitais = self._obter_total_hospitais()

        total_leitos = (
            self.leitos_model.total_leitos()
        )

        total_leitos_sus = (
            self.leitos_model.total_leitos_sus()
        )

        total_uti = (
            self.leitos_model.total_leitos_uti()
        )

        return {
            "total_internacoes": total_internacoes,
            "total_municipios": total_municipios,
            "total_hospitais": total_hospitais,
            "total_leitos": total_leitos,
            "total_leitos_sus": total_leitos_sus,
            "total_uti": total_uti
        }

    # =========================================================
    # HOSPITAIS
    # =========================================================

    def obter_hospitais(self):
        """
        Retorna os dados consolidados de hospitais.
        """

        try:
            return self.hospitais_model.dados_para_view()

        except AttributeError:

            try:
                return self.hospitais_model.listar_hospitais()

            except AttributeError:
                return pd.DataFrame()

    # =========================================================
    # TOTAL DE HOSPITAIS
    # =========================================================

    def _obter_total_hospitais(self):
        """
        Obtém a quantidade de hospitais.

        Primeiro tenta utilizar um método existente no
        HospitaisModel.

        Caso não exista, utiliza CNES como identificador
        único diretamente através dos dados do modelo.
        """

        try:

            resultado = (
                self.hospitais_model.total_hospitais()
            )

            return int(resultado or 0)

        except AttributeError:

            df = self.obter_hospitais()

            if df.empty:
                return 0

            if "CNES" in df.columns:

                return int(
                    df["CNES"]
                    .dropna()
                    .nunique()
                )

            return len(df)

    # =========================================================
    # INTERNAÇÕES
    # =========================================================

    def obter_internacoes(self):
        """
        Retorna os registros de internações.
        """

        return self.internacoes_model.dados_para_view()

    # =========================================================
    # TOTAL DE INTERNAÇÕES
    # =========================================================

    def obter_total_internacoes(self):
        """
        Retorna o total geral de internações.
        """

        return (
            self.internacoes_model.total_internacoes()
        )

    # =========================================================
    # EVOLUÇÃO MENSAL
    # =========================================================

    def obter_evolucao_internacoes(self):
        """
        Retorna a evolução mensal das internações.
        """

        return (
            self.internacoes_model.evolucao_mensal()
        )

    # =========================================================
    # INTERNAÇÕES POR UF
    # =========================================================

    def obter_internacoes_por_uf(self):
        """
        Retorna internações agrupadas por UF.
        """

        return (
            self.internacoes_model.internacoes_por_uf()
        )

    # =========================================================
    # INTERNAÇÕES POR MUNICÍPIO
    # =========================================================

    def obter_internacoes_por_municipio(self):
        """
        Retorna internações agrupadas por município.
        """

        return (
            self.internacoes_model.internacoes_por_municipio()
        )

    # =========================================================
    # TOP MUNICÍPIOS
    # =========================================================

    def obter_top_municipios(self, limite=5):
        """
        Retorna os municípios com maior número
        de internações.
        """

        return (
            self.internacoes_model.maiores_municipios(
                limite
            )
        )

    # =========================================================
    # LEITOS
    # =========================================================

    def obter_leitos(self):
        """
        Retorna os dados consolidados de leitos.
        """

        return (
            self.leitos_model.dados_para_view()
        )

    # =========================================================
    # TOTAL DE LEITOS
    # =========================================================

    def obter_total_leitos(self):
        """
        Retorna o total de leitos existentes.
        """

        return (
            self.leitos_model.total_leitos()
        )

    # =========================================================
    # TOTAL DE LEITOS SUS
    # =========================================================

    def obter_total_leitos_sus(self):
        """
        Retorna o total de leitos SUS.
        """

        return (
            self.leitos_model.total_leitos_sus()
        )

    # =========================================================
    # TOTAL DE UTI
    # =========================================================

    def obter_total_uti(self):
        """
        Retorna o total de leitos de UTI.
        """

        return (
            self.leitos_model.total_leitos_uti()
        )

    # =========================================================
    # LEITOS POR UF
    # =========================================================

    def obter_leitos_por_uf(self):
        """
        Retorna leitos agrupados por UF.
        """

        return (
            self.leitos_model.leitos_por_uf()
        )

    # =========================================================
    # LEITOS POR MUNICÍPIO
    # =========================================================

    def obter_leitos_por_municipio(self):
        """
        Retorna leitos agrupados por município.
        """

        return (
            self.leitos_model.leitos_por_municipio()
        )

    # =========================================================
    # LEITOS POR REGIÃO
    # =========================================================

    def obter_leitos_por_regiao(self):
        """
        Retorna leitos agrupados por região.
        """

        return (
            self.leitos_model.leitos_por_regiao()
        )

    # =========================================================
    # MUNICÍPIOS
    # =========================================================

    def obter_municipios(self):
        """
        Retorna a lista de municípios existentes
        nas bases utilizadas pelo dashboard.
        """

        df = self.obter_internacoes()

        if df.empty:
            return []

        if "MUNICIPIO" not in df.columns:
            return []

        municipios = (
            df["MUNICIPIO"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        municipios = municipios[
            municipios != ""
        ]

        return sorted(
            municipios.unique().tolist()
        )

    # =========================================================
    # TOTAL DE MUNICÍPIOS
    # =========================================================

    def _contar_municipios(self):
        """
        Retorna a quantidade de municípios existentes
        na base de internações.
        """

        municipios = self.obter_municipios()

        return len(municipios)

    # =========================================================
    # UFS
    # =========================================================

    def obter_ufs(self):
        """
        Retorna as UFs existentes na base de leitos.
        """

        df = self.obter_leitos()

        if df.empty:
            return []

        if "UF" not in df.columns:
            return []

        ufs = (
            df["UF"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        ufs = ufs[
            ufs != ""
        ]

        return sorted(
            ufs.unique().tolist()
        )

    # =========================================================
    # MUNICÍPIOS POR UF
    # =========================================================

    def obter_municipios_por_uf(self, uf):
        """
        Retorna os municípios pertencentes à UF informada.
        """

        df = self.obter_leitos()

        if df.empty:
            return []

        if not uf:
            return self.obter_municipios()

        if "UF" not in df.columns:
            return []

        if "MUNICIPIO" not in df.columns:
            return []

        df_filtrado = df[
            df["UF"]
            .astype(str)
            .str.strip()
            .str.upper()
            == str(uf).strip().upper()
        ]

        municipios = (
            df_filtrado["MUNICIPIO"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        municipios = municipios[
            municipios != ""
        ]

        return sorted(
            municipios.unique().tolist()
        )

    # =========================================================
    # FILTRO GERAL
    # =========================================================

    def obter_dados_filtrados(
        self,
        uf=None,
        municipio=None
    ):
        """
        Retorna os principais dados filtrados por UF
        e município.

        O filtro é aplicado sobre os dados reais
        provenientes do Oracle.
        """

        hospitais = self.obter_hospitais()
        internacoes = self.obter_internacoes()
        leitos = self.obter_leitos()

        hospitais = self._filtrar_dataframe(
            hospitais,
            uf,
            municipio
        )

        internacoes = self._filtrar_dataframe(
            internacoes,
            uf,
            municipio
        )

        leitos = self._filtrar_dataframe(
            leitos,
            uf,
            municipio
        )

        return {
            "hospitais": hospitais,
            "internacoes": internacoes,
            "leitos": leitos
        }

    # =========================================================
    # FILTRAR DATAFRAME
    # =========================================================

    def _filtrar_dataframe(
        self,
        df,
        uf=None,
        municipio=None
    ):
        """
        Aplica UF e município em um DataFrame.
        """

        if df is None or df.empty:
            return pd.DataFrame()

        resultado = df.copy()

        # -----------------------------------------------------
        # UF
        # -----------------------------------------------------

        if uf and str(uf).upper() != "TODOS":

            if "UF" in resultado.columns:

                resultado = resultado[
                    resultado["UF"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == str(uf)
                    .strip()
                    .upper()
                ]

            elif "CODIGO_UF" in resultado.columns:

                codigo_uf = self._converter_uf_para_codigo(
                    uf
                )

                if codigo_uf is not None:

                    resultado = resultado[
                        pd.to_numeric(
                            resultado["CODIGO_UF"],
                            errors="coerce"
                        )
                        == codigo_uf
                    ]

        # -----------------------------------------------------
        # MUNICÍPIO
        # -----------------------------------------------------

        if (
            municipio
            and str(municipio).upper() != "TODOS"
        ):

            if "MUNICIPIO" in resultado.columns:

                resultado = resultado[
                    resultado["MUNICIPIO"]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == str(municipio)
                    .strip()
                    .upper()
                ]

        return resultado

    # =========================================================
    # MAPA UF
    # =========================================================

    def _converter_uf_para_codigo(self, uf):

        mapa = {

            "RO": 11,
            "AC": 12,
            "AM": 13,
            "RR": 14,
            "PA": 15,
            "AP": 16,
            "TO": 17,

            "MA": 21,
            "PI": 22,
            "CE": 23,
            "RN": 24,
            "PB": 25,
            "PE": 26,
            "AL": 27,
            "SE": 28,
            "BA": 29,

            "MG": 31,
            "ES": 32,
            "RJ": 33,
            "SP": 35,

            "PR": 41,
            "SC": 42,
            "RS": 43,

            "MS": 50,
            "MT": 51,
            "GO": 52,
            "DF": 53

        }

        return mapa.get(
            str(uf).strip().upper()
        )

    # =========================================================
    # DADOS PARA DOWNLOAD
    # =========================================================

    def obter_dados_download(
        self,
        uf=None,
        municipio=None
    ):
        """
        Prepara um DataFrame consolidado para exportação.
        """

        dados = self.obter_dados_filtrados(
            uf,
            municipio
        )

        internacoes = dados["internacoes"]

        if not internacoes.empty:
            return internacoes

        leitos = dados["leitos"]

        if not leitos.empty:
            return leitos

        hospitais = dados["hospitais"]

        return hospitais

    # =========================================================
    # STATUS DA BASE
    # =========================================================

    def obter_status_base(self):
        """
        Retorna informações simples sobre a disponibilidade
        das três bases.
        """

        hospitais = self.obter_hospitais()
        internacoes = self.obter_internacoes()
        leitos = self.obter_leitos()

        return {
            "hospitais_disponivel": not hospitais.empty,
            "internacoes_disponivel": not internacoes.empty,
            "leitos_disponivel": not leitos.empty
        }