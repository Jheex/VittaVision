import io

import pandas as pd
import streamlit as st

from model.oracle_connection import OracleDatabase


# ==============================================================
# CONFIGURAÇÕES
# ==============================================================

CACHE_TTL = 300
LIMITE_EXIBICAO = 5000


# ==============================================================
# CONSULTA ORACLE COM CACHE
# ==============================================================

@st.cache_data(
    ttl=CACHE_TTL,
    max_entries=20,
    show_spinner=False,
)
def _executar_query_cache(query, _db):

    try:

        if not hasattr(_db, "executar_query_sql"):
            return pd.DataFrame()

        resultado = _db.executar_query_sql(query)

        if resultado is None:
            return pd.DataFrame()

        return resultado.copy()

    except Exception as e:

        raise RuntimeError(
            f"Erro ao executar consulta Oracle: {e}"
        )


# ==============================================================
# CLASSE PRINCIPAL
# ==============================================================

class RelatoriosView:

    # ----------------------------------------------------------
    # AGORA UTILIZAMOS SOMENTE A TB_GERAL
    # ----------------------------------------------------------

    TABELA = "TB_GERAL"

    # ----------------------------------------------------------
    # MESES
    # ----------------------------------------------------------

    MESES = [
        ("JAN", "INTERNACOES_JAN_2025"),
        ("FEV", "INTERNACOES_FEV_2025"),
        ("MAR", "INTERNACOES_MAR_2025"),
        ("ABR", "INTERNACOES_ABR_2025"),
        ("MAI", "INTERNACOES_MAI_2025"),
        ("JUN", "INTERNACOES_JUN_2025"),
        ("JUL", "INTERNACOES_JUL_2025"),
        ("AGO", "INTERNACOES_AGO_2025"),
        ("SET", "INTERNACOES_SET_2025"),
        ("OUT", "INTERNACOES_OUT_2025"),
        ("NOV", "INTERNACOES_NOV_2025"),
        ("DEZ", "INTERNACOES_DEZ_2025"),
    ]

    # ==========================================================
    # RENDER
    # ==========================================================

    def render(self, model=None):

        self.db = self._resolver_banco(model)

        self._css()
        self._hero()

        if self.db is None:

            st.error(
                "Não foi possível estabelecer conexão com o banco Oracle."
            )

            return

        # ------------------------------------------------------
        # CARREGA SOMENTE A TB_GERAL
        # ------------------------------------------------------

        with st.spinner(
            "Carregando inteligência gerencial..."
        ):

            df = self._carregar_geral()

        # ------------------------------------------------------
        # NORMALIZAÇÃO
        # ------------------------------------------------------

        df = self._normalizar_geral(df)

        if df.empty:

            st.error(
                "Nenhum dado foi encontrado na TB_GERAL."
            )

            st.info(
                "Verifique se a tabela TB_GERAL possui registros."
            )

            return

        # ------------------------------------------------------
        # FILTROS
        # ------------------------------------------------------

        filtros = self._render_filtros(df)

        df_filtrado = self._aplicar_filtros(
            df,
            filtros,
        )

        # ------------------------------------------------------
        # ABAS
        # ------------------------------------------------------

        abas = st.tabs(
            [
                "🎯 Executivo",
                "🏥 Internações",
                "🛏️ Leitos",
                "👥 População",
                "🔎 Análise Cruzada",
                "🗃️ Dados",
                "📥 Exportar",
            ]
        )

        with abas[0]:

            self._aba_executivo(
                df_filtrado
            )

        with abas[1]:

            self._aba_internacoes(
                df_filtrado
            )

        with abas[2]:

            self._aba_leitos(
                df_filtrado
            )

        with abas[3]:

            self._aba_populacao(
                df_filtrado
            )

        with abas[4]:

            self._aba_analise(
                df_filtrado
            )

        with abas[5]:

            self._aba_dados(
                df_filtrado
            )

        with abas[6]:

            self._aba_exportacao(
                df_filtrado
            )

    # ==========================================================
    # BANCO
    # ==========================================================

    def _resolver_banco(self, model):

        if model is not None:

            if hasattr(
                model,
                "executar_query_sql",
            ):

                return model

            if hasattr(
                model,
                "consultar_tabela",
            ):

                return model

        try:

            return OracleDatabase()

        except Exception:

            return None

    # ==========================================================
    # CARREGAMENTO DA TB_GERAL
    # ==========================================================

    def _carregar_geral(self):

        query = f"""
            SELECT
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

            FROM {self.TABELA}

            ORDER BY
                COD_UF,
                MUNICIPIO
        """

        try:

            return _executar_query_cache(
                query,
                self.db,
            )

        except Exception as e:

            st.error(
                f"Erro ao carregar TB_GERAL: {e}"
            )

            return pd.DataFrame()

    # ==========================================================
    # NORMALIZAÇÃO
    # ==========================================================

    def _normalizar_geral(self, df):

        if df.empty:
            return df

        df = df.copy()

        # ------------------------------------------------------
        # Padroniza nomes das colunas
        # ------------------------------------------------------

        df.columns = [
            str(col).strip().upper()
            for col in df.columns
        ]

        # ------------------------------------------------------
        # Códigos geográficos
        # ------------------------------------------------------

        if "COD_IBGE" in df.columns:

            df["COD_IBGE"] = pd.to_numeric(
                df["COD_IBGE"],
                errors="coerce",
            ).astype("Int64")

        if "COD_UF" in df.columns:

            df["COD_UF"] = pd.to_numeric(
                df["COD_UF"],
                errors="coerce",
            ).astype("Int64")

        # ------------------------------------------------------
        # Texto
        # ------------------------------------------------------

        if "UF" in df.columns:

            df["UF"] = (
                df["UF"]
                .astype("string")
                .str.strip()
                .str.upper()
                .fillna("N/I")
            )

        if "MUNICIPIO" in df.columns:

            df["MUNICIPIO"] = (
                df["MUNICIPIO"]
                .astype("string")
                .str.strip()
                .str.upper()
                .fillna("N/I")
            )

        # ------------------------------------------------------
        # Colunas numéricas
        # ------------------------------------------------------

        colunas_numericas = [
            "POPULACAO_ESTIMADA",

            "INTERNACOES_JAN_2025",
            "INTERNACOES_FEV_2025",
            "INTERNACOES_MAR_2025",
            "INTERNACOES_ABR_2025",
            "INTERNACOES_MAI_2025",
            "INTERNACOES_JUN_2025",
            "INTERNACOES_JUL_2025",
            "INTERNACOES_AGO_2025",
            "INTERNACOES_SET_2025",
            "INTERNACOES_OUT_2025",
            "INTERNACOES_NOV_2025",
            "INTERNACOES_DEZ_2025",
            "INTERNACOES_TOTAL_2025",

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

            if coluna in df.columns:

                df[coluna] = pd.to_numeric(
                    df[coluna],
                    errors="coerce",
                ).fillna(0)

            else:

                df[coluna] = 0

        # ------------------------------------------------------
        # Caso o total de internações não esteja preenchido,
        # calculamos pelos meses.
        # ------------------------------------------------------

        if "INTERNACOES_TOTAL_2025" not in df.columns:

            df["INTERNACOES_TOTAL_2025"] = (
                df[
                    [
                        coluna
                        for _, coluna in self.MESES
                    ]
                ]
                .sum(axis=1)
            )

        # ------------------------------------------------------
        # Garante uma linha por município
        #
        # COD_IBGE é nossa chave geográfica oficial.
        # ------------------------------------------------------

        if "COD_IBGE" in df.columns:

            df = df.drop_duplicates(
                subset=["COD_IBGE"],
                keep="first",
            )

        return df.reset_index(
            drop=True
        )

    # ==========================================================
    # FILTROS
    # ==========================================================

    def _render_filtros(self, df):

        st.subheader(
            "🎛️ Filtros de análise"
        )

        st.caption(
            "Os filtros utilizam o código IBGE como chave oficial. "
            "Os nomes são utilizados apenas para exibição."
        )

        col1, col2 = st.columns(2)

        # ======================================================
        # UF
        # ======================================================

        ufs = []

        if "COD_UF" in df.columns:

            temp_ufs = (
                df[
                    [
                        "COD_UF",
                        "UF",
                    ]
                ]
                .dropna(
                    subset=["COD_UF"]
                )
                .drop_duplicates(
                    subset=["COD_UF"]
                )
                .sort_values("UF")
            )

            for _, row in temp_ufs.iterrows():

                codigo = int(
                    row["COD_UF"]
                )

                nome = str(
                    row["UF"]
                )

                ufs.append(
                    (
                        codigo,
                        nome,
                    )
                )

        opcoes_uf = ["TODOS"]

        mapa_uf = {
            "TODOS": None
        }

        for codigo, nome in ufs:

            label = (
                f"{codigo:02d} - {nome}"
            )

            opcoes_uf.append(label)

            mapa_uf[label] = codigo

        with col1:

            uf_label = st.selectbox(
                "🌎 Estado / UF",
                opcoes_uf,
                key="relatorios_uf_geral",
            )

        codigo_uf = mapa_uf[
            uf_label
        ]

        # ======================================================
        # MUNICÍPIO
        # ======================================================

        temp = df.copy()

        if codigo_uf is not None:

            temp = temp[
                temp["COD_UF"]
                == codigo_uf
            ]

        municipios = (
            temp[
                [
                    "COD_IBGE",
                    "MUNICIPIO",
                ]
            ]
            .dropna(
                subset=["COD_IBGE"]
            )
            .drop_duplicates(
                subset=["COD_IBGE"]
            )
            .sort_values(
                "MUNICIPIO"
            )
        )

        opcoes_municipio = ["TODOS"]

        mapa_municipio = {
            "TODOS": None
        }

        for _, row in municipios.iterrows():

            codigo = int(
                row["COD_IBGE"]
            )

            nome = str(
                row["MUNICIPIO"]
            )

            label = (
                f"{codigo} - {nome}"
            )

            opcoes_municipio.append(
                label
            )

            mapa_municipio[label] = codigo

        with col2:

            municipio_label = st.selectbox(
                "🏙️ Município",
                opcoes_municipio,
                key="relatorios_municipio_geral",
            )

        codigo_municipio = mapa_municipio[
            municipio_label
        ]

        st.divider()

        return {
            "uf": codigo_uf,
            "municipio": codigo_municipio,
        }

    # ==========================================================
    # APLICAR FILTROS
    # ==========================================================

    def _aplicar_filtros(
        self,
        df,
        filtros,
    ):

        if df.empty:
            return df

        resultado = df.copy()

        # ------------------------------------------------------
        # UF
        # ------------------------------------------------------

        if filtros["uf"] is not None:

            resultado = resultado[
                resultado["COD_UF"]
                == filtros["uf"]
            ]

        # ------------------------------------------------------
        # Município
        #
        # SEMPRE pelo COD_IBGE.
        # ------------------------------------------------------

        if filtros["municipio"] is not None:

            resultado = resultado[
                resultado["COD_IBGE"]
                == filtros["municipio"]
            ]

        return resultado

    # ==========================================================
    # CSS
    # ==========================================================

    def _css(self):

        st.markdown(
            """
            <style>

            .stApp {

                background:
                    radial-gradient(
                        circle at 15% 10%,
                        rgba(124, 58, 237, 0.10),
                        transparent 30%
                    ),
                    radial-gradient(
                        circle at 90% 80%,
                        rgba(37, 99, 235, 0.08),
                        transparent 30%
                    ),
                    #070913;
            }

            [data-testid="stMetric"] {

                background:
                    linear-gradient(
                        145deg,
                        rgba(17, 24, 39, 0.96),
                        rgba(30, 20, 52, 0.96)
                    );

                border:
                    1px solid rgba(139, 92, 246, 0.22);

                border-radius: 16px;

                padding: 18px;

                box-shadow:
                    0 10px 30px rgba(
                        0,
                        0,
                        0,
                        0.20
                    );
            }

            [data-testid="stMetricLabel"] {

                color: #94a3b8 !important;

                font-weight: 700 !important;
            }

            [data-testid="stMetricValue"] {

                color: #ffffff !important;

                font-weight: 800 !important;
            }

            [data-testid="stMetricDelta"] {

                color: #94a3b8 !important;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

    # ==========================================================
    # HERO
    # ==========================================================

    def _hero(self):

        st.title(
            "📊 Centro de Inteligência Gerencial"
        )

        st.caption(
            "Transforme os dados do Vitta Vision em indicadores "
            "claros para compreender demanda, capacidade hospitalar "
            "e distribuição populacional."
        )

        st.divider()

    # ==========================================================
    # CARD
    # ==========================================================

    def _card(
        self,
        coluna,
        titulo,
        valor,
        descricao,
    ):

        with coluna:

            st.metric(
                label=titulo,
                value=valor,
                help=descricao,
            )

    # ==========================================================
    # FORMATAÇÃO
    # ==========================================================

    def _numero(self, valor):

        try:

            return f"{float(valor):,.0f}".replace(
                ",",
                ".",
            )

        except Exception:

            return "0"

    def _decimal(self, valor):

        try:

            return (
                f"{float(valor):,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

        except Exception:

            return "0,00"

    # ==========================================================
    # MENSAL
    # ==========================================================

    def _mensal(self, df):

        if df.empty:
            return pd.DataFrame()

        valores = []

        for mes, coluna in self.MESES:

            valor = (
                pd.to_numeric(
                    df[coluna],
                    errors="coerce",
                )
                .fillna(0)
                .sum()
            )

            valores.append(
                {
                    "Mês": mes,
                    "Internações": valor,
                }
            )

        return pd.DataFrame(
            valores
        )

    # ==========================================================
    # RANKING INTERNAÇÕES
    # ==========================================================

    def _ranking_internacoes(self, df):

        if df.empty:
            return pd.DataFrame()

        ranking = df[
            [
                "COD_IBGE",
                "UF",
                "MUNICIPIO",
                "INTERNACOES_TOTAL_2025",
            ]
        ].copy()

        ranking = ranking.sort_values(
            "INTERNACOES_TOTAL_2025",
            ascending=False,
        )

        ranking.insert(
            0,
            "Posição",
            range(
                1,
                len(ranking) + 1,
            ),
        )

        return ranking.rename(
            columns={
                "COD_IBGE": "Código IBGE",
                "UF": "UF",
                "MUNICIPIO": "Município",
                "INTERNACOES_TOTAL_2025": "Internações 2025",
            }
        )

    # ==========================================================
    # ABA EXECUTIVO
    # ==========================================================

    def _aba_executivo(self, df):

        st.subheader(
            "🎯 Visão Executiva"
        )

        st.caption(
            "Os principais indicadores da área selecionada."
        )

        total_i = df[
            "INTERNACOES_TOTAL_2025"
        ].sum()

        total_l = df[
            "LEITOS_EXISTENTES"
        ].sum()

        total_uti = df[
            "UTI_TOTAL_EXIST"
        ].sum()

        total_pop = df[
            "POPULACAO_ESTIMADA"
        ].sum()

        c1, c2, c3, c4 = st.columns(4)

        self._card(
            c1,
            "🏥 Internações 2025",
            self._numero(total_i),
            "Volume anual",
        )

        self._card(
            c2,
            "🛏️ Leitos",
            self._numero(total_l),
            "Capacidade hospitalar",
        )

        self._card(
            c3,
            "🚑 UTIs",
            self._numero(total_uti),
            "Estrutura intensiva",
        )

        self._card(
            c4,
            "👥 População",
            self._numero(total_pop),
            "Área selecionada",
        )

        st.subheader(
            "📈 Evolução das internações"
        )

        mensal = self._mensal(df)

        if not mensal.empty:

            st.line_chart(
                mensal.set_index("Mês")[
                    "Internações"
                ],
                height=350,
            )

            pico = mensal.loc[
                mensal["Internações"].idxmax()
            ]

            menor = mensal.loc[
                mensal["Internações"].idxmin()
            ]

            with st.container(border=True):

                st.subheader(
                    "🧠 Leitura automática"
                )

                st.write(
                    f"O maior volume foi registrado em "
                    f"**{pico['Mês']}**, com "
                    f"**{self._numero(pico['Internações'])}** "
                    f"internações."
                )

                st.write(
                    f"O menor volume ocorreu em "
                    f"**{menor['Mês']}**, com "
                    f"**{self._numero(menor['Internações'])}** "
                    f"internações."
                )

        st.subheader(
            "🏆 Municípios com maior demanda"
        )

        ranking = self._ranking_internacoes(df)

        if ranking.empty:

            st.info(
                "Não existem dados suficientes para montar o ranking."
            )

        else:

            st.dataframe(
                ranking.head(15),
                width="stretch",
                hide_index=True,
            )

    # ==========================================================
    # ABA INTERNAÇÕES
    # ==========================================================

    def _aba_internacoes(self, df):

        st.subheader(
            "🏥 Internações"
        )

        st.caption(
            "Análise detalhada da demanda assistencial."
        )

        if df.empty:

            st.warning(
                "Nenhuma internação encontrada para os filtros."
            )

            return

        total = df[
            "INTERNACOES_TOTAL_2025"
        ].sum()

        municipios = df[
            "COD_IBGE"
        ].nunique()

        media = (
            total / municipios
            if municipios
            else 0
        )

        mensal = self._mensal(df)

        pico = (
            mensal["Internações"].max()
            if not mensal.empty
            else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        self._card(
            c1,
            "🏥 Internações",
            self._numero(total),
            "Total de 2025",
        )

        self._card(
            c2,
            "🏙️ Municípios",
            self._numero(municipios),
            "Municípios representados",
        )

        self._card(
            c3,
            "📊 Média municipal",
            self._numero(media),
            "Internações / município",
        )

        self._card(
            c4,
            "📈 Pico mensal",
            self._numero(pico),
            "Maior volume",
        )

        st.subheader(
            "📅 Evolução mensal"
        )

        if not mensal.empty:

            st.bar_chart(
                mensal.set_index("Mês")[
                    "Internações"
                ],
                height=330,
            )

        st.subheader(
            "🏆 Ranking"
        )

        ranking = self._ranking_internacoes(df)

        st.dataframe(
            ranking,
            width="stretch",
            hide_index=True,
        )

    # ==========================================================
    # ABA LEITOS
    # ==========================================================

    def _aba_leitos(self, df):

        st.subheader(
            "🛏️ Leitos e UTIs"
        )

        st.caption(
            "Panorama da capacidade hospitalar identificada."
        )

        if df.empty:

            st.warning(
                "Nenhum dado de leitos encontrado."
            )

            return

        leitos = df[
            "LEITOS_EXISTENTES"
        ].sum()

        leitos_sus = df[
            "LEITOS_SUS"
        ].sum()

        uti = df[
            "UTI_TOTAL_EXIST"
        ].sum()

        uti_sus = df[
            "UTI_TOTAL_SUS"
        ].sum()

        municipios = df[
            "COD_IBGE"
        ].nunique()

        percentual = (
            uti / leitos * 100
            if leitos
            else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        self._card(
            c1,
            "🛏️ Leitos",
            self._numero(leitos),
            "Leitos existentes",
        )

        self._card(
            c2,
            "🏥 Leitos SUS",
            self._numero(leitos_sus),
            "Leitos SUS",
        )

        self._card(
            c3,
            "🚑 UTIs",
            self._numero(uti),
            "UTIs existentes",
        )

        self._card(
            c4,
            "📊 % UTI",
            f"{percentual:.1f}%",
            "Participação das UTIs",
        )

        st.subheader(
            "🏥 Distribuição da capacidade"
        )

        ranking = df[
            [
                "COD_IBGE",
                "UF",
                "MUNICIPIO",
                "LEITOS_EXISTENTES",
                "LEITOS_SUS",
                "UTI_TOTAL_EXIST",
                "UTI_TOTAL_SUS",
            ]
        ].copy()

        ranking = ranking.sort_values(
            "LEITOS_EXISTENTES",
            ascending=False,
        )

        ranking = ranking.rename(
            columns={
                "COD_IBGE": "Código IBGE",
                "UF": "UF",
                "MUNICIPIO": "Município",
                "LEITOS_EXISTENTES": "Leitos",
                "LEITOS_SUS": "Leitos SUS",
                "UTI_TOTAL_EXIST": "UTIs",
                "UTI_TOTAL_SUS": "UTIs SUS",
            }
        )

        st.dataframe(
            ranking,
            width="stretch",
            hide_index=True,
        )

        if not ranking.empty:

            st.bar_chart(
                ranking.head(20).set_index(
                    "Município"
                )[
                    [
                        "Leitos",
                        "UTIs",
                    ]
                ],
                height=400,
            )

        st.caption(
            f"UTIs SUS identificadas: "
            f"{self._numero(uti_sus)}"
        )

    # ==========================================================
    # ABA POPULAÇÃO
    # ==========================================================

    def _aba_populacao(self, df):

        st.subheader(
            "👥 População"
        )

        st.caption(
            "Distribuição populacional utilizada nos indicadores."
        )

        if df.empty:

            st.warning(
                "Nenhum dado populacional encontrado."
            )

            return

        total = df[
            "POPULACAO_ESTIMADA"
        ].sum()

        municipios = df[
            "COD_IBGE"
        ].nunique()

        media = (
            total / municipios
            if municipios
            else 0
        )

        maior = (
            df[
                "POPULACAO_ESTIMADA"
            ].max()
        )

        maior_municipio = ""

        if not df.empty:

            indice = df[
                "POPULACAO_ESTIMADA"
            ].idxmax()

            maior_municipio = df.loc[
                indice,
                "MUNICIPIO",
            ]

        c1, c2, c3, c4 = st.columns(4)

        self._card(
            c1,
            "👥 População",
            self._numero(total),
            "População total",
        )

        self._card(
            c2,
            "🏙️ Municípios",
            self._numero(municipios),
            "Municípios analisados",
        )

        self._card(
            c3,
            "📊 Média municipal",
            self._numero(media),
            "População média",
        )

        self._card(
            c4,
            "🏆 Maior população",
            self._numero(maior),
            maior_municipio,
        )

        ranking = df[
            [
                "COD_IBGE",
                "UF",
                "MUNICIPIO",
                "POPULACAO_ESTIMADA",
            ]
        ].copy()

        ranking = ranking.sort_values(
            "POPULACAO_ESTIMADA",
            ascending=False,
        )

        ranking = ranking.rename(
            columns={
                "COD_IBGE": "Código IBGE",
                "UF": "UF",
                "MUNICIPIO": "Município",
                "POPULACAO_ESTIMADA": "População",
            }
        )

        st.subheader(
            "🏙️ Ranking populacional"
        )

        st.dataframe(
            ranking,
            width="stretch",
            hide_index=True,
        )

        if not ranking.empty:

            st.bar_chart(
                ranking.head(20).set_index(
                    "Município"
                )[
                    "População"
                ],
                height=400,
            )

    # ==========================================================
    # ANÁLISE CRUZADA
    # ==========================================================

    def _cruzar(self, df):

        if df.empty:
            return pd.DataFrame()

        resultado = df.copy()

        # ------------------------------------------------------
        # Indicadores
        # ------------------------------------------------------

        resultado[
            "LEITOS_POR_1000"
        ] = 0.0

        resultado[
            "INTERNACOES_POR_1000"
        ] = 0.0

        mascara = (
            resultado[
                "POPULACAO_ESTIMADA"
            ] > 0
        )

        resultado.loc[
            mascara,
            "LEITOS_POR_1000",
        ] = (
            resultado.loc[
                mascara,
                "LEITOS_EXISTENTES",
            ]
            /
            resultado.loc[
                mascara,
                "POPULACAO_ESTIMADA",
            ]
            * 1000
        )

        resultado.loc[
            mascara,
            "INTERNACOES_POR_1000",
        ] = (
            resultado.loc[
                mascara,
                "INTERNACOES_TOTAL_2025",
            ]
            /
            resultado.loc[
                mascara,
                "POPULACAO_ESTIMADA",
            ]
            * 1000
        )

        resultado[
            "UTI_POR_1000"
        ] = 0.0

        resultado.loc[
            mascara,
            "UTI_POR_1000",
        ] = (
            resultado.loc[
                mascara,
                "UTI_TOTAL_EXIST",
            ]
            /
            resultado.loc[
                mascara,
                "POPULACAO_ESTIMADA",
            ]
            * 1000
        )

        return resultado

    # ==========================================================
    # ABA ANÁLISE
    # ==========================================================

    def _aba_analise(self, df):

        st.subheader(
            "🔎 Análise Cruzada"
        )

        st.caption(
            "Relacionamento entre população, capacidade hospitalar "
            "e demanda assistencial."
        )

        dados = self._cruzar(df)

        if dados.empty:

            st.warning(
                "Dados insuficientes para realizar a análise."
            )

            return

        pop = dados[
            "POPULACAO_ESTIMADA"
        ].sum()

        leitos = dados[
            "LEITOS_EXISTENTES"
        ].sum()

        uti = dados[
            "UTI_TOTAL_EXIST"
        ].sum()

        internacoes = dados[
            "INTERNACOES_TOTAL_2025"
        ].sum()

        leitos_1000 = (
            leitos / pop * 1000
            if pop
            else 0
        )

        uti_1000 = (
            uti / pop * 1000
            if pop
            else 0
        )

        internacoes_1000 = (
            internacoes / pop * 1000
            if pop
            else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        self._card(
            c1,
            "🛏️ Leitos / 1.000",
            self._decimal(leitos_1000),
            "Cobertura hospitalar",
        )

        self._card(
            c2,
            "🚑 UTI / 1.000",
            self._decimal(uti_1000),
            "Disponibilidade de UTI",
        )

        self._card(
            c3,
            "🏥 Internações / 1.000",
            self._decimal(internacoes_1000),
            "Pressão assistencial",
        )

        self._card(
            c4,
            "👥 População",
            self._numero(pop),
            "Base populacional",
        )

        # ------------------------------------------------------
        # Ranking
        # ------------------------------------------------------

        ranking = dados[
            dados["POPULACAO_ESTIMADA"] > 0
        ].copy()

        ranking = ranking.sort_values(
            "INTERNACOES_POR_1000",
            ascending=False,
        )

        ranking = ranking.rename(
            columns={
                "COD_IBGE": "Código IBGE",
                "UF": "UF",
                "MUNICIPIO": "Município",
                "POPULACAO_ESTIMADA": "População",
                "LEITOS_EXISTENTES": "Leitos",
                "LEITOS_SUS": "Leitos SUS",
                "UTI_TOTAL_EXIST": "UTIs",
                "UTI_TOTAL_SUS": "UTIs SUS",
                "INTERNACOES_TOTAL_2025": "Internações 2025",
                "LEITOS_POR_1000": "Leitos / 1.000 hab.",
                "UTI_POR_1000": "UTI / 1.000 hab.",
                "INTERNACOES_POR_1000": "Internações / 1.000 hab.",
            }
        )

        colunas = [
            "Código IBGE",
            "UF",
            "Município",
            "População",
            "Leitos",
            "Leitos SUS",
            "UTIs",
            "UTIs SUS",
            "Internações 2025",
            "Leitos / 1.000 hab.",
            "UTI / 1.000 hab.",
            "Internações / 1.000 hab.",
        ]

        st.subheader(
            "🚨 Pressão assistencial"
        )

        st.dataframe(
            ranking[colunas].head(30),
            width="stretch",
            hide_index=True,
        )

        if not ranking.empty:

            primeiro = ranking.iloc[0]

            with st.container(border=True):

                st.subheader(
                    "🧠 Insight gerencial"
                )

                st.write(
                    f"Entre os municípios analisados, "
                    f"**{primeiro['Município']}** apresenta "
                    f"o maior índice de internações por "
                    f"1.000 habitantes."
                )

                st.write(
                    f"O indicador está em aproximadamente "
                    f"**{self._decimal(primeiro['Internações / 1.000 hab.'])}** "
                    f"internações por 1.000 habitantes."
                )

                st.caption(
                    "O indicador deve ser interpretado em conjunto "
                    "com capacidade hospitalar e características "
                    "demográficas da região."
                )

    # ==========================================================
    # ABA DADOS
    # ==========================================================

    def _aba_dados(self, df):

        st.subheader(
            "🗃️ Dados consolidados"
        )

        st.caption(
            f"A TB_GERAL possui {len(df):,} registro(s) "
            f"após aplicação dos filtros."
        )

        if df.empty:

            st.info(
                "Nenhum registro disponível."
            )

            return

        visualizacao = df.head(
            LIMITE_EXIBICAO
        )

        st.dataframe(
            visualizacao,
            width="stretch",
            height=560,
            hide_index=True,
        )

        if len(df) > LIMITE_EXIBICAO:

            st.info(
                f"Exibindo os primeiros "
                f"{LIMITE_EXIBICAO:,} registros."
            )

    # ==========================================================
    # EXPORTAÇÃO
    # ==========================================================

    def _aba_exportacao(self, df):

        st.subheader(
            "📥 Central de Exportação"
        )

        st.caption(
            "Baixe os dados consolidados utilizados na análise."
        )

        dados = self._cruzar(df)

        c1, c2 = st.columns(2)

        # ------------------------------------------------------
        # CSV
        # ------------------------------------------------------

        with c1:

            with st.container(border=True):

                st.subheader(
                    "📄 CSV"
                )

                st.write(
                    "Exporta a análise consolidada em CSV."
                )

                if not dados.empty:

                    csv = dados.to_csv(
                        index=False
                    ).encode(
                        "utf-8-sig"
                    )

                    st.download_button(
                        "⬇️ Baixar análise CSV",
                        data=csv,
                        file_name=(
                            "vitta_vision_analise.csv"
                        ),
                        mime="text/csv",
                        width="stretch",
                    )

                else:

                    st.info(
                        "Não existem dados para exportar."
                    )

        # ------------------------------------------------------
        # EXCEL
        # ------------------------------------------------------

        with c2:

            with st.container(border=True):

                st.subheader(
                    "📊 Excel"
                )

                st.write(
                    "Gere um relatório completo em Excel."
                )

                if st.button(
                    "⚙️ Preparar Excel",
                    width="stretch",
                    key="gerar_excel_relatorios",
                ):

                    output = io.BytesIO()

                    try:

                        with pd.ExcelWriter(
                            output,
                            engine="openpyxl",
                        ) as writer:

                            if not df.empty:

                                df.to_excel(
                                    writer,
                                    index=False,
                                    sheet_name="Geral",
                                )

                            if not dados.empty:

                                dados.to_excel(
                                    writer,
                                    index=False,
                                    sheet_name="Analise",
                                )

                        st.session_state[
                            "relatorios_excel"
                        ] = output.getvalue()

                    except ImportError:

                        st.error(
                            "O pacote openpyxl não está instalado."
                        )

                        st.code(
                            "pip install openpyxl"
                        )

                arquivo_excel = st.session_state.get(
                    "relatorios_excel"
                )

                if arquivo_excel:

                    st.download_button(
                        "⬇️ Baixar relatório Excel",
                        data=arquivo_excel,
                        file_name=(
                            "vitta_vision_relatorio.xlsx"
                        ),
                        mime=(
                            "application/vnd.openxmlformats-officedocument."
                            "spreadsheetml.sheet"
                        ),
                        width="stretch",
                        key="download_excel_relatorios",
                    )

        st.divider()

        st.subheader(
            "📋 Conteúdo do relatório"
        )

        st.write(
            "• 🗃️ TB_GERAL — dados consolidados"
        )

        st.write(
            "• 🔎 Análise cruzada"
        )

        st.write(
            "• 📊 Indicadores por município"
        )