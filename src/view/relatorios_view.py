import io
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

CACHE_TTL = 300

ALTURA_GRAFICO = 390
ALTURA_RANKING = 470
ALTURA_GRANDE = 520


# ==========================================================
# MAPA DE ESTADOS
# ==========================================================

MAPA_UF = {
    11: "Rondônia (RO)",
    12: "Acre (AC)",
    13: "Amazonas (AM)",
    14: "Roraima (RR)",
    15: "Pará (PA)",
    16: "Amapá (AP)",
    17: "Tocantins (TO)",
    21: "Maranhão (MA)",
    22: "Piauí (PI)",
    23: "Ceará (CE)",
    24: "Rio Grande do Norte (RN)",
    25: "Paraíba (PB)",
    26: "Pernambuco (PE)",
    27: "Alagoas (AL)",
    28: "Sergipe (SE)",
    29: "Bahia (BA)",
    31: "Minas Gerais (MG)",
    32: "Espírito Santo (ES)",
    33: "Rio de Janeiro (RJ)",
    35: "São Paulo (SP)",
    41: "Paraná (PR)",
    42: "Santa Catarina (SC)",
    43: "Rio Grande do Sul (RS)",
    50: "Mato Grosso do Sul (MS)",
    51: "Mato Grosso (MT)",
    52: "Goiás (GO)",
    53: "Distrito Federal (DF)",
}


# ==========================================================
# CONSULTA CACHEADA
# ==========================================================

@st.cache_data(
    ttl=CACHE_TTL,
    max_entries=30,
    show_spinner=False,
)
def executar_query_cache(
    query,
    _db,
):

    try:

        resultado = _db.executar_query_sql(
            query
        )

        if resultado is None:

            return pd.DataFrame()

        return resultado.copy()

    except Exception:

        return pd.DataFrame()


# ==========================================================
# VIEW
# ==========================================================

class RelatoriosView:

    # ======================================================
    # MESES
    # ======================================================

    MESES = [
        ("Jan", "VL_JAN_2025"),
        ("Fev", "VL_FEV_2025"),
        ("Mar", "VL_MAR_2025"),
        ("Abr", "VL_ABR_2025"),
        ("Mai", "VL_MAI_2025"),
        ("Jun", "VL_JUN_2025"),
        ("Jul", "VL_JUL_2025"),
        ("Ago", "VL_AGO_2025"),
        ("Set", "VL_SET_2025"),
        ("Out", "VL_OUT_2025"),
        ("Nov", "VL_NOV_2025"),
        ("Dez", "VL_DEZ_2025"),
    ]

    # ======================================================
    # RENDER
    # ======================================================

    def render(
        self,
        model=None,
    ):

        self._aplicar_estilos()

        if model is None:

            st.error(
                "Conexão com o banco de dados não foi inicializada."
            )

            return

        self.db = model

        # ==================================================
        # CABEÇALHO
        # ==================================================

        self._render_cabecalho()

        # ==================================================
        # FILTROS
        # ==================================================

        filtros = self._render_filtros()

        if filtros is None:

            return

        fonte = filtros["fonte"]

        # ==================================================
        # CARREGAMENTO INDEPENDENTE
        # ==================================================

        with st.spinner(
            f"Carregando {fonte.lower()}..."
        ):

            if fonte == "Internações":

                df = self._carregar_internacoes()

                df = self._normalizar_internacoes(
                    df
                )

            else:

                df = self._carregar_leitos()

                df = self._normalizar_leitos(
                    df
                )

        if df.empty:

            self._estado_vazio(
                "A fonte selecionada não possui dados disponíveis."
            )

            self._render_botao_download(
                filtros,
                pd.DataFrame(),
            )

            return

        # ==================================================
        # APLICA FILTROS
        # ==================================================

        df_filtrado = self._aplicar_filtros(
            df,
            filtros,
            fonte,
        )

        # ==================================================
        # BOTÃO DE DOWNLOAD
        # ==================================================

        self._render_botao_download(
            filtros,
            df_filtrado,
        )

        # ==================================================
        # CONTEXTO
        # ==================================================

        self._render_contexto(
            fonte,
            df_filtrado,
        )

        if df_filtrado.empty:

            self._estado_vazio(
                "Nenhum registro corresponde aos filtros selecionados."
            )

            return

        # ==================================================
        # RELATÓRIO
        # ==================================================

        if fonte == "Internações":

            self._render_internacoes(
                df_filtrado
            )

        else:

            self._render_leitos(
                df_filtrado
            )

    # ======================================================
    # CABEÇALHO PRINCIPAL
    # ======================================================

    def _render_cabecalho(
        self,
    ):

        st.html(
            """
            <div class="page-header">

                <div class="header-icon">
                    📊
                </div>

                <div class="header-content">

                    <div class="header-eyebrow">
                        VITTA VISION • CENTRAL DE RELATÓRIOS
                    </div>

                    <div class="header-title">
                        Gestão de <span>Relatórios Gerenciais</span>
                    </div>

                    <div class="header-description">
                        Analise as bases de internações e capacidade
                        hospitalar de forma independente, com
                        indicadores e visualizações específicas.
                    </div>

                </div>

                <div class="header-badge">

                    <div class="header-badge-title">
                        2
                    </div>

                    <div class="header-badge-label">
                        FONTES
                    </div>

                </div>

            </div>
            """
        )

    # ======================================================
    # FILTROS
    # ======================================================

    def _render_filtros(
        self,
    ):

        st.html(
            """
            <div class="section-header">

                <div class="section-icon">
                    ⚙️
                </div>

                <div>

                    <div class="section-title">
                        Filtros Avançados
                    </div>

                    <div class="section-subtitle">
                        Selecione a fonte, região e formato
                        desejado para o relatório.
                    </div>

                </div>

            </div>
            """
        )

        with st.container(
            border=True
        ):

            # ==================================================
            # QUATRO CAMPOS NA MESMA LINHA
            # ==================================================

            col1, col2, col3, col4 = st.columns(
                [1.15, 1.25, 1.70, 1.20],
                gap="medium",
            )

            # ==================================================
            # TIPO DE RELATÓRIO
            # ==================================================

            with col1:

                fonte = st.selectbox(
                    "Tipo de relatório",
                    [
                        "Internações",
                        "Leitos",
                    ],
                    key="relatorios_fonte",
                )

            # ==================================================
            # ESTADO / UF
            # ==================================================

            with col2:

                df_uf = self._obter_ufs(
                    fonte
                )

                opcoes_uf = [
                    "Todos os estados"
                ]

                mapa_uf_selecao = {}

                if fonte == "Internações":

                    if (
                        not df_uf.empty
                        and "CODIGO_UF"
                        in df_uf.columns
                    ):

                        codigos = (
                            pd.to_numeric(
                                df_uf[
                                    "CODIGO_UF"
                                ],
                                errors="coerce",
                            )
                            .dropna()
                            .astype(int)
                            .unique()
                            .tolist()
                        )

                        for codigo in sorted(
                            set(codigos)
                        ):

                            if codigo not in MAPA_UF:

                                continue

                            label = MAPA_UF[
                                codigo
                            ]

                            opcoes_uf.append(
                                label
                            )

                            mapa_uf_selecao[
                                label
                            ] = codigo

                else:

                    if (
                        not df_uf.empty
                        and "UF"
                        in df_uf.columns
                    ):

                        estados = (
                            df_uf[
                                "UF"
                            ]
                            .dropna()
                            .astype(str)
                            .str.strip()
                            .str.upper()
                            .unique()
                            .tolist()
                        )

                        for sigla in sorted(
                            set(estados)
                        ):

                            sigla = sigla[:2]

                            codigo = next(
                                (
                                    numero
                                    for numero, nome
                                    in MAPA_UF.items()
                                    if f"({sigla})"
                                    in nome
                                ),
                                None,
                            )

                            label = (
                                MAPA_UF[codigo]
                                if codigo
                                else sigla
                            )

                            opcoes_uf.append(
                                label
                            )

                            mapa_uf_selecao[
                                label
                            ] = sigla

                uf_label = st.selectbox(
                    "Estado / UF",
                    opcoes_uf,
                    key=(
                        f"relatorios_uf_"
                        f"{fonte}"
                    ),
                )

                uf = mapa_uf_selecao.get(
                    uf_label
                )

            # ==================================================
            # MUNICÍPIO
            # ==================================================

            with col3:

                df_municipios = (
                    self._obter_municipios(
                        fonte,
                        uf,
                    )
                )

                opcoes_municipio = [
                    "Todos os municípios"
                ]

                if (
                    not df_municipios.empty
                    and "MUNICIPIO"
                    in df_municipios.columns
                ):

                    valores = (
                        df_municipios[
                            "MUNICIPIO"
                        ]
                        .dropna()
                        .astype(str)
                        .str.strip()
                        .unique()
                        .tolist()
                    )

                    valores = [
                        valor
                        for valor in valores
                        if valor
                        and valor.lower()
                        != "nan"
                    ]

                    opcoes_municipio.extend(
                        sorted(
                            valores
                        )
                    )

                municipio = st.selectbox(
                    "Município",
                    opcoes_municipio,
                    key=(
                        f"relatorios_municipio_"
                        f"{fonte}"
                    ),
                )

            # ==================================================
            # FORMATO DE EXPORTAÇÃO
            # ==================================================

            with col4:

                formato = st.selectbox(
                    "Formato de exportação",
                    [
                        "Excel (.xlsx)",
                        "CSV (.csv)",
                        "PDF (.pdf)",
                    ],
                    key="relatorios_formato",
                )

            # ==================================================
            # DIVISOR
            # ==================================================

            st.html(
                """
                <div class="filter-divider"></div>
                """
            )

            # ==================================================
            # INFORMAÇÃO + BOTÃO
            # ==================================================

            col_info, col_button = st.columns(
                [2.15, 1],
                gap="medium",
            )

            # ==================================================
            # DESCRIÇÃO DO FORMATO
            # ==================================================

            with col_info:

                descricoes = {
                    "Excel (.xlsx)": (
                        "Ideal para análise, filtros e manipulação dos dados."
                    ),
                    "CSV (.csv)": (
                        "Ideal para integração, processamento e ciência de dados."
                    ),
                    "PDF (.pdf)": (
                        "Ideal para apresentação, impressão e compartilhamento."
                    ),
                }

                st.html(
                    f"""
                    <div class="export-info">

                        <div class="export-info-label">
                            FORMATO SELECIONADO
                        </div>

                        <div class="export-info-value">
                            {formato}
                        </div>

                        <div class="export-info-description">
                            {
                                descricoes.get(
                                    formato,
                                    ""
                                )
                            }
                        </div>

                    </div>
                    """
                )

            # ==================================================
            # BOTÃO
            # ==================================================

            with col_button:

                st.write("")

                download_slot = st.empty()

            # ==================================================
            # RESUMO DOS FILTROS
            # ==================================================

            st.html(
                f"""
                <div class="filter-summary">

                    <div class="summary-item">

                        <div class="summary-label">
                            RELATÓRIO
                        </div>

                        <div class="summary-value">
                            {fonte}
                        </div>

                    </div>

                    <div class="summary-item">

                        <div class="summary-label">
                            UF
                        </div>

                        <div class="summary-value">
                            {uf_label}
                        </div>

                    </div>

                    <div class="summary-item">

                        <div class="summary-label">
                            MUNICÍPIO
                        </div>

                        <div class="summary-value">
                            {municipio}
                        </div>

                    </div>

                    <div class="summary-item">

                        <div class="summary-label">
                            EXPORTAÇÃO
                        </div>

                        <div class="summary-value">
                            {formato}
                        </div>

                    </div>

                </div>
                """
            )

            return {
                "fonte": fonte,
                "uf": uf,
                "municipio": municipio,
                "formato": formato,
                "download_slot": download_slot,
            }

    # ======================================================
    # BOTÃO DE DOWNLOAD
    # ======================================================

    def _render_botao_download(
        self,
        filtros,
        df,
    ):

        slot = filtros.get(
            "download_slot"
        )

        if slot is None:

            return

        if df is None or df.empty:

            with slot:

                st.button(
                    "Gerar relatório",
                    type="primary",
                    width="stretch",
                    disabled=True,
                    key=(
                        "relatorios_download_disabled"
                    ),
                )

            return

        fonte = filtros[
            "fonte"
        ]

        formato = filtros[
            "formato"
        ]

        try:

            # ==============================================
            # EXCEL
            # ==============================================

            if formato.startswith(
                "Excel"
            ):

                arquivo = self._gerar_excel(
                    df
                )

                mime = (
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                )

                extensao = "xlsx"

            # ==============================================
            # CSV
            # ==============================================

            elif formato.startswith(
                "CSV"
            ):

                arquivo = (
                    df.to_csv(
                        index=False
                    )
                    .encode(
                        "utf-8-sig"
                    )
                )

                mime = "text/csv"

                extensao = "csv"

            # ==============================================
            # PDF
            # ==============================================

            else:

                arquivo = self._gerar_pdf(
                    df,
                    fonte,
                )

                if arquivo is None:

                    with slot:

                        st.button(
                            "Gerar relatório",
                            type="primary",
                            width="stretch",
                            disabled=True,
                            key=(
                                "relatorios_pdf_disabled"
                            ),
                        )

                    return

                mime = "application/pdf"

                extensao = "pdf"

            # ==============================================
            # NOME
            # ==============================================

            nome = self._nome_arquivo(
                fonte,
                extensao,
            )

            # ==============================================
            # DOWNLOAD
            # ==============================================

            with slot:

                st.download_button(
                    "Gerar relatório",
                    data=arquivo,
                    file_name=nome,
                    mime=mime,
                    type="primary",
                    width="stretch",
                    key=(
                        "relatorios_download_"
                        f"{fonte.lower()}_"
                        f"{extensao}"
                    ),
                )

        except Exception as e:

            with slot:

                st.error(
                    f"Erro ao preparar relatório: {e}"
                )

    # ======================================================
    # UFS
    # ======================================================

    def _obter_ufs(
        self,
        fonte,
    ):

        if fonte == "Internações":

            query = """
                SELECT DISTINCT
                    CODIGO_UF
                FROM TB_INTERNACOES
                WHERE CODIGO_UF IS NOT NULL
                ORDER BY CODIGO_UF
            """

        else:

            query = """
                SELECT DISTINCT
                    UF
                FROM TB_LEITOS
                WHERE UF IS NOT NULL
                ORDER BY UF
            """

        return executar_query_cache(
            query,
            self.db,
        )

    # ======================================================
    # MUNICÍPIOS
    # ======================================================

    def _obter_municipios(
        self,
        fonte,
        uf,
    ):

        if fonte == "Internações":

            tabela = "TB_INTERNACOES"

            coluna = "MUNICIPIO"

        else:

            tabela = "TB_LEITOS"

            coluna = "MUNICIPIO"

        where_uf = ""

        if uf is not None:

            if fonte == "Internações":

                where_uf = (
                    f"AND CODIGO_UF = "
                    f"{int(uf)}"
                )

            else:

                uf_sql = (
                    str(uf)
                    .replace(
                        "'",
                        "''",
                    )
                    .upper()
                )

                where_uf = (
                    f"AND UPPER(TRIM(UF)) = "
                    f"'{uf_sql}'"
                )

        query = f"""
            SELECT DISTINCT
                {coluna} AS MUNICIPIO
            FROM {tabela}
            WHERE {coluna} IS NOT NULL
            {where_uf}
            ORDER BY {coluna}
        """

        return executar_query_cache(
            query,
            self.db,
        )

    # ======================================================
    # CARREGAR INTERNAÇÕES
    # ======================================================

    def _carregar_internacoes(
        self,
    ):

        query = """
            SELECT

                ID_INTERNACAO,
                CODIGO_MUNICIPIO,
                MUNICIPIO,
                CODIGO_UF,

                VL_JAN_2025,
                VL_FEV_2025,
                VL_MAR_2025,
                VL_ABR_2025,
                VL_MAI_2025,
                VL_JUN_2025,
                VL_JUL_2025,
                VL_AGO_2025,
                VL_SET_2025,
                VL_OUT_2025,
                VL_NOV_2025,
                VL_DEZ_2025,

                VL_TOTAL_2025,

                DT_IMPORTACAO

            FROM TB_INTERNACOES

            ORDER BY
                CODIGO_UF,
                MUNICIPIO
        """

        try:

            return executar_query_cache(
                query,
                self.db,
            )

        except Exception as e:

            st.error(
                f"Erro ao carregar TB_INTERNACOES: {e}"
            )

            return pd.DataFrame()

    # ======================================================
    # CARREGAR LEITOS
    # ======================================================

    def _carregar_leitos(
        self,
    ):

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

                DT_IMPORTACAO

            FROM TB_LEITOS

            ORDER BY
                UF,
                MUNICIPIO,
                NOME_ESTABELECIMENTO
        """

        try:

            return executar_query_cache(
                query,
                self.db,
            )

        except Exception as e:

            st.error(
                f"Erro ao carregar TB_LEITOS: {e}"
            )

            return pd.DataFrame()

    # ======================================================
    # NORMALIZAÇÃO — INTERNAÇÕES
    # ======================================================

    def _normalizar_internacoes(
        self,
        df,
    ):

        if df.empty:

            return df

        df = df.copy()

        df.columns = (
            df.columns
            .astype(str)
            .str.replace(
                "ï»¿",
                "",
                regex=False,
            )
            .str.replace(
                '"',
                "",
                regex=False,
            )
            .str.strip()
            .str.upper()
        )

        numericas = [
            "ID_INTERNACAO",
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

        for coluna in numericas:

            if coluna in df.columns:

                df[coluna] = pd.to_numeric(
                    df[coluna],
                    errors="coerce",
                ).fillna(0)

        if "MUNICIPIO" in df.columns:

            df["MUNICIPIO"] = (
                df["MUNICIPIO"]
                .astype(str)
                .str.strip()
                .str.upper()
            )

        meses = [
            coluna
            for _, coluna in self.MESES
            if coluna in df.columns
        ]

        if (
            meses
            and "VL_TOTAL_2025"
            in df.columns
        ):

            calculado = (
                df[
                    meses
                ]
                .sum(
                    axis=1
                )
            )

            df[
                "VL_TOTAL_2025"
            ] = (
                df[
                    "VL_TOTAL_2025"
                ]
                .where(
                    df[
                        "VL_TOTAL_2025"
                    ] > 0,
                    calculado,
                )
            )

        return df

    # ======================================================
    # NORMALIZAÇÃO — LEITOS
    # ======================================================

    def _normalizar_leitos(
        self,
        df,
    ):

        if df.empty:

            return df

        df = df.copy()

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.upper()
        )

        numericas = [
            "ID_LEITO",
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

        for coluna in numericas:

            if coluna in df.columns:

                df[coluna] = pd.to_numeric(
                    df[coluna],
                    errors="coerce",
                ).fillna(0)

        textos = [
            "REGIAO",
            "UF",
            "MUNICIPIO",
            "MOTIVO_DESABILITACAO",
            "NOME_ESTABELECIMENTO",
            "RAZAO_SOCIAL",
            "TP_GESTAO",
            "DS_TIPO_UNIDADE",
            "DESC_NATUREZA_JURIDICA",
        ]

        for coluna in textos:

            if coluna in df.columns:

                df[coluna] = (
                    df[coluna]
                    .astype(str)
                    .str.strip()
                )

        # ==================================================
        # IMPORTANTE:
        # TB_LEITOS possui histórico por competência.
        #
        # Mantemos somente a competência mais recente
        # para evitar somar os mesmos leitos várias vezes.
        # ==================================================

        if "COMP" in df.columns and not df.empty:

            ultima_competencia = df[
                "COMP"
            ].max()

            df = df[
                df["COMP"]
                == ultima_competencia
            ].copy()

        return df

    # ======================================================
    # APLICAR FILTROS
    # ======================================================

    def _aplicar_filtros(
        self,
        df,
        filtros,
        fonte,
    ):

        resultado = df.copy()

        if resultado.empty:

            return resultado

        # ==================================================
        # UF
        # ==================================================

        if filtros["uf"] is not None:

            if fonte == "Internações":

                resultado = resultado[
                    resultado[
                        "CODIGO_UF"
                    ]
                    == filtros["uf"]
                ]

            else:

                resultado = resultado[
                    resultado[
                        "UF"
                    ]
                    .astype(str)
                    .str.strip()
                    .str.upper()
                    == str(
                        filtros["uf"]
                    )
                    .strip()
                    .upper()
                ]

        # ==================================================
        # MUNICÍPIO
        # ==================================================

        if (
            filtros["municipio"]
            != "Todos os municípios"
        ):

            resultado = resultado[
                resultado[
                    "MUNICIPIO"
                ]
                .astype(str)
                .str.strip()
                == str(
                    filtros["municipio"]
                ).strip()
            ]

        return resultado.reset_index(
            drop=True
        )

    # ======================================================
    # RELATÓRIO — INTERNAÇÕES
    # ======================================================

    def _render_internacoes(
        self,
        df,
    ):

        total = df[
            "VL_TOTAL_2025"
        ].sum()

        municipios = (
            df[
                "CODIGO_MUNICIPIO"
            ]
            .nunique()
        )

        media_municipal = (
            total / municipios
            if municipios
            else 0
        )

        mensal = self._dados_mensais(
            df
        )

        pico = (
            mensal[
                "Internações"
            ].max()
            if not mensal.empty
            else 0
        )

        mes_pico = "-"

        if not mensal.empty:

            indice = mensal[
                "Internações"
            ].idxmax()

            mes_pico = mensal.loc[
                indice,
                "Mês",
            ]

        self._cabecalho_relatorio(
            "🏥",
            "TB_INTERNACOES",
            "Relatório de Internações Hospitalares",
            (
                "Análise exclusiva da demanda assistencial "
                "registrada em 2025."
            ),
        )

        # ==================================================
        # KPIs
        # ==================================================

        c1, c2, c3, c4 = st.columns(
            4,
            gap="medium",
        )

        self._kpi(
            c1,
            "🏥",
            "Internações",
            self._numero(total),
            "Total de 2025",
            "purple",
        )

        self._kpi(
            c2,
            "📍",
            "Municípios",
            self._numero(municipios),
            "Municípios representados",
            "blue",
        )

        self._kpi(
            c3,
            "📊",
            "Média municipal",
            self._numero(
                media_municipal
            ),
            "Internações por município",
            "cyan",
        )

        self._kpi(
            c4,
            "📈",
            "Pico mensal",
            self._numero(pico),
            f"Maior volume: {mes_pico}",
            "violet",
        )

        # ==================================================
        # EVOLUÇÃO
        # ==================================================

        self._cabecalho_secao(
            "📈",
            "Evolução das Internações",
            "Comportamento da demanda ao longo de 2025.",
        )

        col1, col2 = st.columns(
            [1.55, 1],
            gap="medium",
        )

        # ==================================================
        # GRÁFICO 1
        # ==================================================

        with col1:

            self._titulo_grafico(
                "📈 Evolução mensal",
                "Volume total de internações por mês",
            )

            fig = px.line(
                mensal,
                x="Mês",
                y="Internações",
                markers=True,
            )

            fig.update_traces(
                line=dict(
                    color="#A855F7",
                    width=3,
                ),
                marker=dict(
                    color="#A855F7",
                    size=8,
                ),
            )

            self._plotly_padrao(
                fig,
                ALTURA_GRAFICO,
            )

            fig.update_layout(
                hovermode="x unified",
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # GRÁFICO 2
        # ==================================================

        with col2:

            self._titulo_grafico(
                "📊 Comparativo mensal",
                "Ordenação dos meses por volume",
            )

            mensal_ord = mensal.sort_values(
                "Internações",
                ascending=False,
            )

            fig = px.bar(
                mensal_ord,
                x="Mês",
                y="Internações",
                text="Internações",
            )

            fig.update_traces(
                marker_color="#7C3AED",
                texttemplate="%{text:,.0f}",
                textposition="outside",
            )

            self._plotly_padrao(
                fig,
                ALTURA_GRAFICO,
            )

            fig.update_layout(
                xaxis_title=None,
                yaxis_title=None,
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # DISTRIBUIÇÃO TERRITORIAL
        # ==================================================

        self._cabecalho_secao(
            "🌎",
            "Distribuição Territorial",
            "Concentração da demanda entre estados e municípios.",
        )

        col1, col2 = st.columns(
            [1.4, 1],
            gap="medium",
        )

        # ==================================================
        # GRÁFICO 3
        # ==================================================

        with col1:

            self._titulo_grafico(
                "🏆 Top 15 municípios",
                "Municípios com maior volume de internações",
            )

            ranking = (
                df[
                    [
                        "MUNICIPIO",
                        "VL_TOTAL_2025",
                    ]
                ]
                .groupby(
                    "MUNICIPIO",
                    as_index=False,
                )
                .sum()
                .nlargest(
                    15,
                    "VL_TOTAL_2025",
                )
                .sort_values(
                    "VL_TOTAL_2025"
                )
            )

            ranking[
                "MUNICIPIO"
            ] = (
                ranking[
                    "MUNICIPIO"
                ]
                .astype(str)
                .str.slice(
                    0,
                    35,
                )
            )

            fig = px.bar(
                ranking,
                x="VL_TOTAL_2025",
                y="MUNICIPIO",
                orientation="h",
                text="VL_TOTAL_2025",
            )

            fig.update_traces(
                marker_color="#A855F7",
                texttemplate="%{text:,.0f}",
                textposition="outside",
            )

            self._plotly_padrao(
                fig,
                ALTURA_GRANDE,
            )

            fig.update_layout(
                xaxis=dict(
                    showticklabels=False,
                    title=None,
                    showgrid=False,
                ),
                yaxis=dict(
                    title=None,
                ),
                margin=dict(
                    l=10,
                    r=65,
                    t=20,
                    b=20,
                ),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # GRÁFICO 4
        # ==================================================

        with col2:

            self._titulo_grafico(
                "🌎 Internações por UF",
                "Demanda agregada por estado",
            )

            por_uf = (
                df[
                    [
                        "CODIGO_UF",
                        "VL_TOTAL_2025",
                    ]
                ]
                .groupby(
                    "CODIGO_UF",
                    as_index=False,
                )
                .sum()
                .sort_values(
                    "VL_TOTAL_2025"
                )
            )

            por_uf["UF"] = (
                por_uf[
                    "CODIGO_UF"
                ]
                .astype(int)
                .map(MAPA_UF)
                .fillna(
                    por_uf[
                        "CODIGO_UF"
                    ].astype(str)
                )
            )

            fig = px.bar(
                por_uf,
                x="VL_TOTAL_2025",
                y="UF",
                orientation="h",
                text="VL_TOTAL_2025",
            )

            fig.update_traces(
                marker_color="#2563EB",
                texttemplate="%{text:,.0f}",
                textposition="outside",
            )

            self._plotly_padrao(
                fig,
                ALTURA_GRANDE,
            )

            fig.update_layout(
                xaxis=dict(
                    showticklabels=False,
                    title=None,
                    showgrid=False,
                ),
                yaxis=dict(
                    title=None,
                ),
                margin=dict(
                    l=15,
                    r=65,
                    t=20,
                    b=20,
                ),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # HEATMAP
        # ==================================================

        self._cabecalho_secao(
            "🔥",
            "Comportamento dos Municípios Líderes",
            "Evolução mensal dos municípios com maior demanda.",
        )

        principais = (
            df[
                [
                    "MUNICIPIO",
                    "VL_TOTAL_2025",
                ]
            ]
            .groupby(
                "MUNICIPIO",
                as_index=False,
            )
            .sum()
            .nlargest(
                8,
                "VL_TOTAL_2025",
            )[
                "MUNICIPIO"
            ]
            .tolist()
        )

        heatmap_data = []

        for municipio in principais:

            linha = {
                "Município": municipio
            }

            dados_municipio = df[
                df[
                    "MUNICIPIO"
                ] == municipio
            ]

            for mes, coluna in self.MESES:

                if coluna in df.columns:

                    linha[mes] = (
                        dados_municipio[
                            coluna
                        ].sum()
                    )

            heatmap_data.append(
                linha
            )

        heatmap_df = pd.DataFrame(
            heatmap_data
        )

        if not heatmap_df.empty:

            heatmap_plot = (
                heatmap_df
                .set_index(
                    "Município"
                )
            )

            fig = go.Figure(
                data=go.Heatmap(
                    z=heatmap_plot.values,
                    x=heatmap_plot.columns.tolist(),
                    y=heatmap_plot.index.tolist(),
                    colorscale=[
                        [0, "#111827"],
                        [0.35, "#581C87"],
                        [0.70, "#9333EA"],
                        [1, "#D8B4FE"],
                    ],
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "%{x}: %{z:,.0f}"
                        "<extra></extra>"
                    ),
                )
            )

            fig.update_layout(
                height=430,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#E5E7EB",
                ),
                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=35,
                ),
                xaxis=dict(
                    title=None,
                ),
                yaxis=dict(
                    title=None,
                ),
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # TABELA
        # ==================================================

        self._tabela_internacoes(
            df
        )

    # ======================================================
    # DADOS MENSAIS
    # ======================================================

    def _dados_mensais(
        self,
        df,
    ):

        if df is None or df.empty:

            return pd.DataFrame(
                columns=[
                    "Mês",
                    "Internações",
                ]
            )

        dados = []

        for mes, coluna in self.MESES:

            if coluna not in df.columns:

                continue

            valor = (
                pd.to_numeric(
                    df[
                        coluna
                    ],
                    errors="coerce",
                )
                .fillna(0)
                .sum()
            )

            dados.append(
                {
                    "Mês": mes,
                    "Internações": valor,
                }
            )

        return pd.DataFrame(
            dados
        )

    # ======================================================
    # TABELA INTERNAÇÕES
    # ======================================================

    def _tabela_internacoes(
        self,
        df,
    ):

        self._cabecalho_tabela(
            "📋",
            "Detalhamento das Internações",
            "Municípios e evolução mensal da demanda.",
        )

        colunas = [
            "MUNICIPIO",
            "CODIGO_UF",
            "VL_TOTAL_2025",
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
        ]

        colunas = [
            coluna
            for coluna in colunas
            if coluna in df.columns
        ]

        tabela = df[
            colunas
        ].copy()

        if "VL_TOTAL_2025" in tabela.columns:

            tabela = tabela.sort_values(
                "VL_TOTAL_2025",
                ascending=False,
            )

        tabela.insert(
            0,
            "Posição",
            range(
                1,
                len(tabela) + 1,
            ),
        )

        tabela = tabela.rename(
            columns={
                "MUNICIPIO": "Município",
                "CODIGO_UF": "UF",
                "VL_TOTAL_2025": "Total 2025",
                "VL_JAN_2025": "Jan",
                "VL_FEV_2025": "Fev",
                "VL_MAR_2025": "Mar",
                "VL_ABR_2025": "Abr",
                "VL_MAI_2025": "Mai",
                "VL_JUN_2025": "Jun",
                "VL_JUL_2025": "Jul",
                "VL_AGO_2025": "Ago",
                "VL_SET_2025": "Set",
                "VL_OUT_2025": "Out",
                "VL_NOV_2025": "Nov",
                "VL_DEZ_2025": "Dez",
            }
        )

        config = {
            "Posição": st.column_config.NumberColumn(
                "Rank",
                width="small",
                format="%d",
            ),
            "Município": st.column_config.TextColumn(
                "Município",
                width="medium",
            ),
        }

        if "UF" in tabela.columns:

            config[
                "UF"
            ] = st.column_config.NumberColumn(
                "UF",
                width="small",
                format="%02d",
            )

        if "Total 2025" in tabela.columns:

            maximo = max(
                int(
                    tabela[
                        "Total 2025"
                    ].max()
                ),
                1,
            )

            config[
                "Total 2025"
            ] = st.column_config.ProgressColumn(
                "Total 2025",
                width="medium",
                format="%d",
                min_value=0,
                max_value=maximo,
            )

        for coluna in [
            "Jan",
            "Fev",
            "Mar",
            "Abr",
            "Mai",
            "Jun",
            "Jul",
            "Ago",
            "Set",
            "Out",
            "Nov",
            "Dez",
        ]:

            if coluna in tabela.columns:

                config[
                    coluna
                ] = st.column_config.NumberColumn(
                    coluna,
                    width="small",
                    format="%d",
                )

        st.dataframe(
            tabela,
            width="stretch",
            hide_index=True,
            height=550,
            column_config=config,
        )

        self._rodape_tabela(
            len(tabela),
            "TB_INTERNACOES",
        )

    # ======================================================
    # RELATÓRIO — LEITOS
    # ======================================================

    def _render_leitos(
        self,
        df,
    ):

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

        estabelecimentos = (
            df[
                "CNES"
            ]
            .replace(
                0,
                pd.NA,
            )
            .nunique()
        )

        municipios = (
            df[
                "MUNICIPIO"
            ]
            .nunique()
        )

        percentual_sus = (
            leitos_sus / leitos * 100
            if leitos
            else 0
        )

        self._cabecalho_relatorio(
            "🛏️",
            "TB_LEITOS",
            "Relatório de Capacidade Hospitalar",
            (
                "Análise exclusiva da infraestrutura hospitalar "
                "registrada na base de leitos."
            ),
        )

        # ==================================================
        # KPIs
        # ==================================================

        c1, c2, c3, c4, c5 = st.columns(
            5,
            gap="medium",
        )

        self._kpi(
            c1,
            "🛏️",
            "Leitos",
            self._numero(leitos),
            "Capacidade existente",
            "purple",
        )

        self._kpi(
            c2,
            "🏥",
            "Leitos SUS",
            self._numero(leitos_sus),
            f"{percentual_sus:.1f}% do total",
            "blue",
        )

        self._kpi(
            c3,
            "🚑",
            "UTIs",
            self._numero(uti),
            "UTIs existentes",
            "cyan",
        )

        self._kpi(
            c4,
            "🏢",
            "Estabelecimentos",
            self._numero(
                estabelecimentos
            ),
            "Estabelecimentos identificados",
            "violet",
        )

        self._kpi(
            c5,
            "📍",
            "Municípios",
            self._numero(
                municipios
            ),
            "Municípios com registros",
            "purple",
        )

        # ==================================================
        # CAPACIDADE
        # ==================================================

        self._cabecalho_secao(
            "🛏️",
            "Capacidade Hospitalar",
            "Comparação entre capacidade total e oferta SUS.",
        )

        col1, col2 = st.columns(
            [1.45, 1],
            gap="medium",
        )

        # ==================================================
        # GRÁFICO 1
        # ==================================================

        with col1:

            self._titulo_grafico(
                "🛏️ Leitos existentes × SUS",
                "Comparação direta da capacidade",
            )

            capacidade = pd.DataFrame(
                {
                    "Categoria": [
                        "Leitos",
                        "Leitos SUS",
                    ],
                    "Quantidade": [
                        leitos,
                        leitos_sus,
                    ],
                }
            )

            fig = px.bar(
                capacidade,
                x="Categoria",
                y="Quantidade",
                text="Quantidade",
            )

            fig.update_traces(
                marker_color="#A855F7",
                texttemplate="%{text:,.0f}",
                textposition="outside",
            )

            self._plotly_padrao(
                fig,
                ALTURA_GRAFICO,
            )

            fig.update_layout(
                xaxis_title=None,
                yaxis_title=None,
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # GRÁFICO 2
        # ==================================================

        with col2:

            self._titulo_grafico(
                "📊 Leitos SUS × não SUS",
                "Distribuição da capacidade",
            )

            nao_sus = max(
                leitos - leitos_sus,
                0,
            )

            distribuicao = pd.DataFrame(
                {
                    "Categoria": [
                        "SUS",
                        "Não SUS",
                    ],
                    "Quantidade": [
                        leitos_sus,
                        nao_sus,
                    ],
                }
            )

            fig = px.bar(
                distribuicao,
                x="Categoria",
                y="Quantidade",
                text="Quantidade",
            )

            fig.update_traces(
                marker_color="#7C3AED",
                texttemplate="%{text:,.0f}",
                textposition="outside",
            )

            self._plotly_padrao(
                fig,
                ALTURA_GRAFICO,
            )

            fig.update_layout(
                xaxis_title=None,
                yaxis_title=None,
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # UTI
        # ==================================================

        self._cabecalho_secao(
            "🚑",
            "Estrutura de UTI",
            "Perfil das unidades de terapia intensiva disponíveis.",
        )

        col1, col2 = st.columns(
            [1.45, 1],
            gap="medium",
        )

        tipos_uti = pd.DataFrame(
            {
                "Tipo": [
                    "Adulto",
                    "Pediátrico",
                    "Neonatal",
                    "Queimado",
                    "Coronariana",
                ],
                "Total": [
                    df[
                        "UTI_ADULTO_EXIST"
                    ].sum(),
                    df[
                        "UTI_PEDIATRICO_EXIST"
                    ].sum(),
                    df[
                        "UTI_NEONATAL_EXIST"
                    ].sum(),
                    df[
                        "UTI_QUEIMADO_EXIST"
                    ].sum(),
                    df[
                        "UTI_CORONARIANA_EXIST"
                    ].sum(),
                ],
                "SUS": [
                    df[
                        "UTI_ADULTO_SUS"
                    ].sum(),
                    df[
                        "UTI_PEDIATRICO_SUS"
                    ].sum(),
                    df[
                        "UTI_NEONATAL_SUS"
                    ].sum(),
                    df[
                        "UTI_QUEIMADO_SUS"
                    ].sum(),
                    df[
                        "UTI_CORONARIANA_SUS"
                    ].sum(),
                ],
            }
        )

        tipos_uti = tipos_uti[
            tipos_uti[
                "Total"
            ] > 0
        ]

        # ==================================================
        # GRÁFICO 3
        # ==================================================

        with col1:

            self._titulo_grafico(
                "🚑 UTIs por especialidade",
                "Quantidade total por tipo de UTI",
            )

            ranking_uti = (
                tipos_uti[
                    [
                        "Tipo",
                        "Total",
                    ]
                ]
                .sort_values(
                    "Total"
                )
            )

            fig = px.bar(
                ranking_uti,
                x="Total",
                y="Tipo",
                orientation="h",
                text="Total",
            )

            fig.update_traces(
                marker_color="#06B6D4",
                texttemplate="%{text:,.0f}",
                textposition="outside",
            )

            self._plotly_padrao(
                fig,
                ALTURA_GRAFICO,
            )

            fig.update_layout(
                xaxis=dict(
                    showticklabels=False,
                    title=None,
                    showgrid=False,
                ),
                yaxis=dict(
                    title=None,
                ),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # GRÁFICO 4
        # ==================================================

        with col2:

            self._titulo_grafico(
                "📊 Oferta SUS nas UTIs",
                "Total existente comparado ao SUS",
            )

            fig = px.bar(
                tipos_uti,
                x="Tipo",
                y=[
                    "Total",
                    "SUS",
                ],
                barmode="group",
            )

            fig.update_layout(
                height=ALTURA_GRAFICO,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(
                    color="#E5E7EB",
                ),
                margin=dict(
                    l=40,
                    r=20,
                    t=20,
                    b=45,
                ),
                xaxis=dict(
                    title=None,
                    showgrid=False,
                ),
                yaxis=dict(
                    title=None,
                    showgrid=True,
                    gridcolor=(
                        "rgba(139,92,246,.10)"
                    ),
                ),
                legend=dict(
                    orientation="h",
                    y=-0.15,
                ),
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # DISTRIBUIÇÃO
        # ==================================================

        self._cabecalho_secao(
            "🌎",
            "Distribuição da Capacidade",
            "Concentração de leitos por estabelecimento, estado e tipo.",
        )

        col1, col2 = st.columns(
            [1.45, 1],
            gap="medium",
        )

        # ==================================================
        # GRÁFICO 5
        # ==================================================

        with col1:

            self._titulo_grafico(
                "🏆 Top 15 estabelecimentos",
                "Estabelecimentos com maior capacidade",
            )

            ranking_est = (
                df[
                    [
                        "NOME_ESTABELECIMENTO",
                        "LEITOS_EXISTENTES",
                    ]
                ]
                .groupby(
                    "NOME_ESTABELECIMENTO",
                    as_index=False,
                )
                .sum()
                .nlargest(
                    15,
                    "LEITOS_EXISTENTES",
                )
                .sort_values(
                    "LEITOS_EXISTENTES"
                )
            )

            ranking_est[
                "NOME_ESTABELECIMENTO"
            ] = (
                ranking_est[
                    "NOME_ESTABELECIMENTO"
                ]
                .astype(str)
                .str.slice(
                    0,
                    38,
                )
            )

            fig = px.bar(
                ranking_est,
                x="LEITOS_EXISTENTES",
                y="NOME_ESTABELECIMENTO",
                orientation="h",
                text="LEITOS_EXISTENTES",
            )

            fig.update_traces(
                marker_color="#A855F7",
                texttemplate="%{text:,.0f}",
                textposition="outside",
            )

            self._plotly_padrao(
                fig,
                ALTURA_GRANDE,
            )

            fig.update_layout(
                xaxis=dict(
                    showticklabels=False,
                    title=None,
                    showgrid=False,
                ),
                yaxis=dict(
                    title=None,
                ),
                margin=dict(
                    l=10,
                    r=65,
                    t=20,
                    b=20,
                ),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # GRÁFICO 6
        # ==================================================

        with col2:

            self._titulo_grafico(
                "🌎 Leitos por UF",
                "Capacidade hospitalar agrupada por estado",
            )

            por_uf = (
                df[
                    [
                        "UF",
                        "LEITOS_EXISTENTES",
                    ]
                ]
                .groupby(
                    "UF",
                    as_index=False,
                )
                .sum()
                .sort_values(
                    "LEITOS_EXISTENTES"
                )
            )

            fig = px.bar(
                por_uf,
                x="LEITOS_EXISTENTES",
                y="UF",
                orientation="h",
                text="LEITOS_EXISTENTES",
            )

            fig.update_traces(
                marker_color="#2563EB",
                texttemplate="%{text:,.0f}",
                textposition="outside",
            )

            self._plotly_padrao(
                fig,
                ALTURA_GRANDE,
            )

            fig.update_layout(
                xaxis=dict(
                    showticklabels=False,
                    title=None,
                    showgrid=False,
                ),
                yaxis=dict(
                    title=None,
                ),
                margin=dict(
                    l=15,
                    r=65,
                    t=20,
                    b=20,
                ),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                    "responsive": True,
                },
            )

        # ==================================================
        # GRÁFICO 7
        # ==================================================

        self._titulo_grafico(
            "🏥 Leitos por tipo de unidade",
            "Tipos de estabelecimento com maior capacidade",
        )

        tipos = (
            df[
                [
                    "DS_TIPO_UNIDADE",
                    "LEITOS_EXISTENTES",
                ]
            ]
            .groupby(
                "DS_TIPO_UNIDADE",
                as_index=False,
            )
            .sum()
            .nlargest(
                12,
                "LEITOS_EXISTENTES",
            )
            .sort_values(
                "LEITOS_EXISTENTES"
            )
        )

        tipos[
            "DS_TIPO_UNIDADE"
        ] = (
            tipos[
                "DS_TIPO_UNIDADE"
            ]
            .astype(str)
            .str.slice(
                0,
                35,
            )
        )

        fig = px.bar(
            tipos,
            x="LEITOS_EXISTENTES",
            y="DS_TIPO_UNIDADE",
            orientation="h",
            text="LEITOS_EXISTENTES",
        )

        fig.update_traces(
            marker_color="#7C3AED",
            texttemplate="%{text:,.0f}",
            textposition="outside",
        )

        self._plotly_padrao(
            fig,
            ALTURA_GRANDE,
        )

        fig.update_layout(
            xaxis=dict(
                showticklabels=False,
                title=None,
                showgrid=False,
            ),
            yaxis=dict(
                title=None,
            ),
            margin=dict(
                l=10,
                r=65,
                t=20,
                b=20,
            ),
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False,
                "responsive": True,
            },
        )

        # ==================================================
        # TABELA
        # ==================================================

        self._tabela_leitos(
            df
        )

    # ======================================================
    # TABELA LEITOS
    # ======================================================

    def _tabela_leitos(
        self,
        df,
    ):

        self._cabecalho_tabela(
            "📋",
            "Detalhamento da Capacidade",
            "Estabelecimentos, leitos e estrutura intensiva.",
        )

        tabela = df[
            [
                "UF",
                "MUNICIPIO",
                "CNES",
                "NOME_ESTABELECIMENTO",
                "DS_TIPO_UNIDADE",
                "TP_GESTAO",
                "LEITOS_EXISTENTES",
                "LEITOS_SUS",
                "UTI_TOTAL_EXIST",
                "UTI_TOTAL_SUS",
            ]
        ].copy()

        tabela = tabela.sort_values(
            [
                "LEITOS_EXISTENTES",
                "UTI_TOTAL_EXIST",
            ],
            ascending=False,
        )

        tabela.insert(
            0,
            "Posição",
            range(
                1,
                len(tabela) + 1,
            ),
        )

        tabela = tabela.rename(
            columns={
                "UF": "UF",
                "MUNICIPIO": "Município",
                "CNES": "CNES",
                "NOME_ESTABELECIMENTO": "Estabelecimento",
                "DS_TIPO_UNIDADE": "Tipo",
                "TP_GESTAO": "Gestão",
                "LEITOS_EXISTENTES": "Leitos",
                "LEITOS_SUS": "Leitos SUS",
                "UTI_TOTAL_EXIST": "UTIs",
                "UTI_TOTAL_SUS": "UTIs SUS",
            }
        )

        max_leitos = max(
            int(
                tabela[
                    "Leitos"
                ].max()
            )
            if not tabela.empty
            else 1,
            1,
        )

        st.dataframe(
            tabela,
            width="stretch",
            hide_index=True,
            height=560,
            column_config={
                "Posição": st.column_config.NumberColumn(
                    "Rank",
                    width="small",
                    format="%d",
                ),
                "UF": st.column_config.TextColumn(
                    "UF",
                    width="small",
                ),
                "Município": st.column_config.TextColumn(
                    "Município",
                    width="medium",
                ),
                "CNES": st.column_config.NumberColumn(
                    "CNES",
                    width="small",
                    format="%d",
                ),
                "Estabelecimento": st.column_config.TextColumn(
                    "Estabelecimento",
                    width="large",
                ),
                "Tipo": st.column_config.TextColumn(
                    "Tipo",
                    width="medium",
                ),
                "Gestão": st.column_config.TextColumn(
                    "Gestão",
                    width="small",
                ),
                "Leitos": st.column_config.ProgressColumn(
                    "Leitos",
                    format="%d",
                    min_value=0,
                    max_value=max_leitos,
                    width="medium",
                ),
                "Leitos SUS": st.column_config.NumberColumn(
                    "Leitos SUS",
                    format="%d",
                    width="small",
                ),
                "UTIs": st.column_config.NumberColumn(
                    "UTIs",
                    format="%d",
                    width="small",
                ),
                "UTIs SUS": st.column_config.NumberColumn(
                    "UTIs SUS",
                    format="%d",
                    width="small",
                ),
            },
        )

        self._rodape_tabela(
            len(tabela),
            "TB_LEITOS",
        )

    # ======================================================
    # CABEÇALHO RELATÓRIO
    # ======================================================

    def _cabecalho_relatorio(
        self,
        icone,
        fonte,
        titulo,
        descricao,
    ):

        st.html(
            f"""
            <div class="report-header-small">

                <div class="report-icon-small">
                    {icone}
                </div>

                <div>

                    <div class="report-eyebrow">
                        {fonte}
                    </div>

                    <div class="report-title-small">
                        {titulo}
                    </div>

                    <div class="report-description-small">
                        {descricao}
                    </div>

                </div>

            </div>
            """
        )

    # ======================================================
    # CABEÇALHO SEÇÃO
    # ======================================================

    def _cabecalho_secao(
        self,
        icone,
        titulo,
        descricao,
    ):

        st.html(
            f"""
            <div class="section-header">

                <div class="section-icon">
                    {icone}
                </div>

                <div>

                    <div class="section-title">
                        {titulo}
                    </div>

                    <div class="section-subtitle">
                        {descricao}
                    </div>

                </div>

            </div>
            """
        )

    # ======================================================
    # TÍTULO GRÁFICO
    # ======================================================

    def _titulo_grafico(
        self,
        titulo,
        subtitulo,
    ):

        st.html(
            f"""
            <div class="chart-heading">

                <div class="chart-title">
                    {titulo}
                </div>

                <div class="chart-subtitle">
                    {subtitulo}
                </div>

            </div>
            """
        )

    # ======================================================
    # CABEÇALHO TABELA
    # ======================================================

    def _cabecalho_tabela(
        self,
        icone,
        titulo,
        descricao,
    ):

        st.html(
            f"""
            <div class="table-header">

                <div class="table-icon">
                    {icone}
                </div>

                <div>

                    <div class="table-title">
                        {titulo}
                    </div>

                    <div class="table-description">
                        {descricao}
                    </div>

                </div>

            </div>
            """
        )

    # ======================================================
    # RODAPÉ TABELA
    # ======================================================

    def _rodape_tabela(
        self,
        quantidade,
        fonte,
    ):

        st.html(
            f"""
            <div class="table-footer">

                <div class="table-footer-source">

                    <span class="table-footer-dot">
                        ●
                    </span>

                    Fonte:
                    <strong>{fonte}</strong>

                </div>

                <div class="table-footer-count">
                    {self._numero(quantidade)}
                    registros
                </div>

            </div>
            """
        )

    # ======================================================
    # CONTEXTO
    # ======================================================

    def _render_contexto(
        self,
        fonte,
        df,
    ):

        st.html(
            f"""
            <div class="context-bar">

                <div class="context-left">

                    <div class="context-status">
                        ●
                    </div>

                    <div>

                        <div class="context-label">
                            RELATÓRIO ATIVO
                        </div>

                        <div class="context-name">
                            {fonte}
                        </div>

                    </div>

                </div>

                <div class="context-count">
                    {self._numero(len(df))}
                    registro(s)
                </div>

            </div>
            """
        )

    # ======================================================
    # KPI
    # ======================================================

    def _kpi(
        self,
        coluna,
        icone,
        titulo,
        valor,
        descricao,
        classe,
    ):

        with coluna:

            st.html(
                f"""
                <div class="kpi-card {classe}">

                    <div class="kpi-glow"></div>

                    <div class="kpi-top">

                        <div class="kpi-icon">
                            {icone}
                        </div>

                        <div class="kpi-dot">
                            ●
                        </div>

                    </div>

                    <div class="kpi-title">
                        {titulo}
                    </div>

                    <div class="kpi-value">
                        {valor}
                    </div>

                    <div class="kpi-description">
                        {descricao}
                    </div>

                    <div class="kpi-line"></div>

                </div>
                """
            )

    # ======================================================
    # NÚMERO
    # ======================================================

    def _numero(
        self,
        valor,
    ):

        try:

            return (
                f"{float(valor):,.0f}"
                .replace(
                    ",",
                    ".",
                )
            )

        except (
            TypeError,
            ValueError,
        ):

            return "0"

    # ======================================================
    # PLOTLY
    # ======================================================

    def _plotly_padrao(
        self,
        fig,
        altura=ALTURA_GRAFICO,
    ):

        fig.update_layout(
            height=altura,
            autosize=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#E5E7EB",
                size=12,
            ),
            margin=dict(
                l=50,
                r=50,
                t=25,
                b=45,
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor=(
                    "rgba(139,92,246,.10)"
                ),
                zeroline=False,
                automargin=True,
                tickfont=dict(
                    color="#94A3B8",
                ),
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                automargin=True,
                tickfont=dict(
                    color="#CBD5E1",
                ),
            ),
        )

    # ======================================================
    # ESTADO VAZIO
    # ======================================================

    def _estado_vazio(
        self,
        mensagem,
    ):

        st.html(
            f"""
            <div class="empty-state">

                <div class="empty-icon">
                    ◌
                </div>

                <div class="empty-title">
                    Nenhum resultado
                </div>

                <div class="empty-description">
                    {mensagem}
                </div>

            </div>
            """
        )

    # ======================================================
    # EXCEL
    # ======================================================

    def _gerar_excel(
        self,
        df,
    ):

        output = io.BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl",
        ) as writer:

            df.to_excel(
                writer,
                index=False,
                sheet_name="Relatorio",
            )

        output.seek(0)

        return output.getvalue()

    # ======================================================
    # PDF
    # ======================================================

    def _gerar_pdf(
        self,
        df,
        fonte,
    ):

        try:

            from reportlab.lib import colors

            from reportlab.lib.pagesizes import (
                A4,
                landscape,
            )

            from reportlab.lib.styles import (
                getSampleStyleSheet,
            )

            from reportlab.lib.units import mm

            from reportlab.platypus import (
                SimpleDocTemplate,
                Paragraph,
                Spacer,
                Table,
                TableStyle,
                Image,
            )

        except ImportError:

            return None

        output = io.BytesIO()

        documento = SimpleDocTemplate(
            output,
            pagesize=landscape(A4),
            rightMargin=8 * mm,
            leftMargin=8 * mm,
            topMargin=10 * mm,
            bottomMargin=10 * mm,
        )

        estilos = getSampleStyleSheet()

        elementos = []

        # ==================================================
        # LOGO
        # ==================================================

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        caminho_logo = os.path.join(
            base_dir,
            "assets",
            "logo.png",
        )

        if os.path.exists(
            caminho_logo
        ):

            try:

                logo = Image(
                    caminho_logo,
                    width=48 * mm,
                    height=16 * mm,
                    kind="proportional",
                )

                elementos.append(
                    logo
                )

                elementos.append(
                    Spacer(
                        1,
                        3 * mm,
                    )
                )

            except Exception:

                pass

        # ==================================================
        # TÍTULO
        # ==================================================

        elementos.append(
            Paragraph(
                f"Relatório Gerencial — {fonte}",
                estilos["Heading2"],
            )
        )

        elementos.append(
            Spacer(
                1,
                2 * mm,
            )
        )

        # ==================================================
        # DATA
        # ==================================================

        elementos.append(
            Paragraph(
                (
                    "Gerado em "
                    f"{datetime.now().strftime('%d/%m/%Y às %H:%M')}"
                ),
                estilos["Normal"],
            )
        )

        elementos.append(
            Spacer(
                1,
                5 * mm,
            )
        )

        # ==================================================
        # COLUNAS
        # ==================================================

        if fonte == "Internações":

            colunas = [
                "CODIGO_MUNICIPIO",
                "MUNICIPIO",
                "CODIGO_UF",
                "VL_TOTAL_2025",
            ]

        else:

            colunas = [
                "UF",
                "MUNICIPIO",
                "CNES",
                "NOME_ESTABELECIMENTO",
                "LEITOS_EXISTENTES",
                "LEITOS_SUS",
                "UTI_TOTAL_EXIST",
                "UTI_TOTAL_SUS",
            ]

        colunas = [
            coluna
            for coluna in colunas
            if coluna in df.columns
        ]

        dados_df = (
            df[
                colunas
            ]
            .head(500)
            .copy()
        )

        for coluna in dados_df.columns:

            if pd.api.types.is_datetime64_any_dtype(
                dados_df[coluna]
            ):

                dados_df[coluna] = (
                    dados_df[coluna]
                    .dt.strftime(
                        "%d/%m/%Y"
                    )
                    .fillna("")
                )

            else:

                dados_df[coluna] = (
                    dados_df[coluna]
                    .fillna("")
                    .astype(str)
                    .str.slice(
                        0,
                        40,
                    )
                )

        dados = [
            [
                str(coluna)
                for coluna
                in dados_df.columns
            ]
        ]

        dados.extend(
            dados_df.values.tolist()
        )

        tabela = Table(
            dados,
            repeatRows=1,
        )

        tabela.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor(
                            "#7C3AED"
                        ),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.25,
                        colors.HexColor(
                            "#CBD5E1"
                        ),
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor(
                                "#F8FAFC"
                            ),
                        ],
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                ]
            )
        )

        elementos.append(
            tabela
        )

        if len(df) > 500:

            elementos.append(
                Spacer(
                    1,
                    4 * mm,
                )
            )

            elementos.append(
                Paragraph(
                    (
                        "O PDF apresenta os primeiros "
                        "500 registros. CSV e Excel "
                        "contêm todos os "
                        f"{self._numero(len(df))} "
                        "registros filtrados."
                    ),
                    estilos["Normal"],
                )
            )

        documento.build(
            elementos
        )

        output.seek(0)

        return output.getvalue()

    # ======================================================
    # NOME DO ARQUIVO
    # ======================================================

    def _nome_arquivo(
        self,
        fonte,
        extensao,
    ):

        nomes = {
            "Internações": "internacoes",
            "Leitos": "leitos",
        }

        nome = nomes.get(
            fonte,
            "relatorio",
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M"
        )

        return (
            f"vitta_vision_"
            f"{nome}_"
            f"{timestamp}."
            f"{extensao}"
        )

    # ======================================================
    # CSS
    # ======================================================

    def _aplicar_estilos(
        self,
    ):

        st.html(
            """
            <style>

            .stApp {

                background:
                    radial-gradient(
                        circle at 10% 0%,
                        rgba(168,85,247,.08),
                        transparent 26%
                    ),
                    radial-gradient(
                        circle at 90% 100%,
                        rgba(37,99,235,.06),
                        transparent 25%
                    ),
                    #070910;

            }

            .page-header {

                position: relative;
                display: flex;
                align-items: center;
                gap: 22px;
                padding: 28px;
                margin-bottom: 24px;
                overflow: hidden;
                border-radius: 20px;

                background:
                    linear-gradient(
                        135deg,
                        rgba(126,34,206,.24),
                        rgba(168,85,247,.17),
                        rgba(15,23,42,.96)
                    );

                border:
                    1px solid
                    rgba(168,85,247,.22);

                box-shadow:
                    0 12px 40px
                    rgba(126,34,206,.12);

            }

            .page-header::after {

                content: "";
                position: absolute;
                width: 230px;
                height: 230px;
                right: -100px;
                top: -120px;
                border-radius: 50%;
                background: rgba(168,85,247,.16);
                filter: blur(6px);

            }

            .header-icon {

                position: relative;
                z-index: 1;
                width: 68px;
                height: 68px;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                border-radius: 18px;
                font-size: 34px;

                background:
                    linear-gradient(
                        135deg,
                        #7C3AED,
                        #A855F7
                    );

                box-shadow:
                    0 10px 30px
                    rgba(168,85,247,.35);

            }

            .header-content {

                position: relative;
                z-index: 1;
                min-width: 0;
                flex: 1;

            }

            .header-eyebrow {

                color: #C084FC;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1.5px;
                margin-bottom: 5px;

            }

            .header-title {

                color: #FFFFFF;
                font-size: 30px;
                line-height: 1.15;
                font-weight: 800;
                letter-spacing: -.7px;

            }

            .header-title span {

                color: #A855F7;

            }

            .header-description {

                margin-top: 8px;
                color: #C4B5FD;
                font-size: 14px;
                line-height: 1.5;
                max-width: 800px;

            }

            .header-badge {

                position: relative;
                z-index: 1;
                min-width: 100px;
                padding-left: 20px;
                text-align: center;

                border-left:
                    1px solid
                    rgba(255,255,255,.08);

            }

            .header-badge-title {

                color: #FFFFFF;
                font-size: 30px;
                font-weight: 850;
                line-height: 1;

            }

            .header-badge-label {

                color: #64748B;
                font-size: 9px;
                font-weight: 800;
                letter-spacing: 1.3px;
                margin-top: 5px;

            }

            .section-header {

                display: flex;
                align-items: center;
                gap: 13px;
                margin: 18px 0 15px 0;

            }

            .section-icon {

                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 12px;
                font-size: 19px;

                background:
                    linear-gradient(
                        135deg,
                        rgba(124,58,237,.15),
                        rgba(168,85,247,.12)
                    );

                border:
                    1px solid
                    rgba(168,85,247,.16);

            }

            .section-title {

                color: #F8FAFC;
                font-size: 18px;
                font-weight: 750;

            }

            .section-subtitle {

                color: #64748B;
                font-size: 11px;
                margin-top: 3px;

            }

            .filter-divider {

                height: 1px;
                background: rgba(148,163,184,.08);
                margin: 18px 0 12px 0;

            }

            .filter-summary {

                display: flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 24px;
                padding-top: 14px;
                margin-top: 8px;

                border-top:
                    1px solid
                    rgba(148,163,184,.08);

            }

            .summary-item {

                min-width: 120px;

            }

            .summary-label {

                color: #475569;
                font-size: 8px;
                font-weight: 850;
                letter-spacing: 1.1px;

            }

            .summary-value {

                margin-top: 3px;
                color: #CBD5E1;
                font-size: 11px;
                font-weight: 650;

            }

            .export-info {

                min-height: 68px;
                padding: 4px 2px;

            }

            .export-info-label {

                color: #475569;
                font-size: 8px;
                font-weight: 850;
                letter-spacing: 1.1px;

            }

            .export-info-value {

                color: #C084FC;
                font-size: 13px;
                font-weight: 750;
                margin-top: 3px;

            }

            .export-info-description {

                color: #64748B;
                font-size: 10px;
                line-height: 1.35;
                margin-top: 3px;

            }

            div[data-testid="stDownloadButton"] {

                width: 100%;

            }

            div[data-testid="stDownloadButton"] button {

                min-height: 42px !important;
                height: 42px !important;

                border:
                    1px solid
                    rgba(168,85,247,.65) !important;

                border-radius: 11px !important;

                background:
                    linear-gradient(
                        135deg,
                        #7C3AED,
                        #A855F7
                    ) !important;

                color: #FFFFFF !important;
                font-size: 12px !important;
                font-weight: 800 !important;

                box-shadow:
                    0 8px 22px
                    rgba(168,85,247,.22) !important;

                transition:
                    transform .18s ease,
                    box-shadow .18s ease;

            }

            div[data-testid="stDownloadButton"] button:hover {

                background:
                    linear-gradient(
                        135deg,
                        #6D28D9,
                        #9333EA
                    ) !important;

                box-shadow:
                    0 12px 28px
                    rgba(168,85,247,.32) !important;

                transform:
                    translateY(-1px);

            }

            div[data-testid="stButton"] button[kind="primary"] {

                min-height: 42px;

                border:
                    1px solid
                    rgba(168,85,247,.65);

                border-radius: 11px;

                background:
                    linear-gradient(
                        135deg,
                        #7C3AED,
                        #A855F7
                    );

                color: #FFFFFF;
                font-size: 12px;
                font-weight: 800;

                box-shadow:
                    0 8px 22px
                    rgba(168,85,247,.22);

            }

            .report-header-small {

                display: flex;
                align-items: center;
                gap: 14px;
                margin: 28px 0 20px 0;

            }

            .report-icon-small {

                width: 50px;
                height: 50px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 15px;
                font-size: 22px;

                background:
                    linear-gradient(
                        135deg,
                        rgba(124,58,237,.16),
                        rgba(168,85,247,.09)
                    );

                border:
                    1px solid
                    rgba(168,85,247,.16);

            }

            .report-eyebrow {

                color: #A855F7;
                font-size: 9px;
                font-weight: 850;
                letter-spacing: 1.2px;
                margin-bottom: 4px;

            }

            .report-title-small {

                color: #FFFFFF;
                font-size: 22px;
                font-weight: 820;

            }

            .report-description-small {

                color: #64748B;
                font-size: 12px;
                margin-top: 4px;

            }

            .context-bar {

                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 11px 15px;
                margin-top: 18px;
                border-radius: 12px;

                background:
                    rgba(15,23,42,.66);

                border:
                    1px solid
                    rgba(168,85,247,.10);

            }

            .context-left {

                display: flex;
                align-items: center;
                gap: 10px;

            }

            .context-status {

                color: #A855F7;
                font-size: 11px;

            }

            .context-label {

                color: #475569;
                font-size: 8px;
                font-weight: 850;
                letter-spacing: 1.1px;

            }

            .context-name {

                color: #CBD5E1;
                font-size: 11px;
                font-weight: 700;
                margin-top: 2px;

            }

            .context-count {

                color: #C084FC;
                font-size: 11px;
                font-weight: 750;

            }

            .kpi-card {

                position: relative;
                min-height: 180px;
                padding: 20px;
                overflow: hidden;
                border-radius: 18px;

                background:
                    linear-gradient(
                        145deg,
                        rgba(30,41,59,.98),
                        rgba(15,23,42,.98)
                    );

                border:
                    1px solid
                    rgba(255,255,255,.07);

                box-shadow:
                    0 10px 30px
                    rgba(0,0,0,.22);

                transition:
                    transform .2s ease,
                    box-shadow .2s ease;

            }

            .kpi-card:hover {

                transform:
                    translateY(-3px);

                box-shadow:
                    0 16px 40px
                    rgba(168,85,247,.15);

            }

            .kpi-card.purple {

                border-top:
                    3px solid
                    #A855F7;

            }

            .kpi-card.blue {

                border-top:
                    3px solid
                    #2563EB;

            }

            .kpi-card.cyan {

                border-top:
                    3px solid
                    #06B6D4;

            }

            .kpi-card.violet {

                border-top:
                    3px solid
                    #7C3AED;

            }

            .kpi-glow {

                position: absolute;
                width: 130px;
                height: 130px;
                right: -60px;
                top: -60px;
                border-radius: 50%;
                opacity: .16;
                filter: blur(3px);
                background: #A855F7;

            }

            .kpi-top {

                display: flex;
                align-items: center;
                justify-content: space-between;
                position: relative;
                z-index: 1;
                margin-bottom: 15px;

            }

            .kpi-icon {

                width: 43px;
                height: 43px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 12px;
                font-size: 21px;

                background:
                    rgba(168,85,247,.09);

                border:
                    1px solid
                    rgba(168,85,247,.10);

            }

            .kpi-dot {

                color: #334155;
                font-size: 8px;

            }

            .kpi-title {

                color: #CBD5E1;
                font-size: 13px;
                font-weight: 600;
                position: relative;
                z-index: 1;

            }

            .kpi-value {

                color: #FFFFFF;
                font-size: 31px;
                line-height: 1.1;
                font-weight: 850;
                letter-spacing: -1px;
                margin-top: 4px;
                position: relative;
                z-index: 1;

            }

            .kpi-description {

                color: #94A3B8;
                font-size: 10px;
                margin-top: 6px;
                position: relative;
                z-index: 1;

            }

            .kpi-line {

                position: absolute;
                left: 20px;
                right: 20px;
                bottom: 12px;
                height: 2px;
                border-radius: 10px;
                opacity: .45;

                background:
                    linear-gradient(
                        90deg,
                        #A855F7,
                        #7C3AED
                    );

            }

            .chart-heading {

                min-height: 39px;
                margin: 5px 0 6px 0;

            }

            .chart-title {

                color: #F1F5F9;
                font-size: 15px;
                font-weight: 750;
                line-height: 1.25;

            }

            .chart-subtitle {

                color: #64748B;
                font-size: 10px;
                margin-top: 3px;
                line-height: 1.3;

            }

            [data-testid="stPlotlyChart"] {

                width: 100% !important;
                border-radius: 16px;
                padding: 7px;

                background:
                    linear-gradient(
                        145deg,
                        rgba(15,23,42,.72),
                        rgba(30,41,59,.54)
                    );

                border:
                    1px solid
                    rgba(168,85,247,.10);

                box-shadow:
                    0 8px 30px
                    rgba(0,0,0,.13);

                box-sizing: border-box;

            }

            .table-header {

                display: flex;
                align-items: center;
                gap: 13px;
                margin: 28px 0 14px 0;

            }

            .table-icon {

                width: 43px;
                height: 43px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 12px;
                font-size: 20px;

                background:
                    linear-gradient(
                        135deg,
                        rgba(124,58,237,.17),
                        rgba(168,85,247,.10)
                    );

                border:
                    1px solid
                    rgba(168,85,247,.18);

            }

            .table-title {

                color: #F8FAFC;
                font-size: 17px;
                font-weight: 790;

            }

            .table-description {

                color: #64748B;
                font-size: 10px;
                margin-top: 3px;

            }

            [data-testid="stDataFrame"] {

                border-radius: 18px !important;
                overflow: hidden !important;

                border:
                    1px solid
                    rgba(168,85,247,.22) !important;

                background:
                    rgba(15,23,42,.70) !important;

                box-shadow:
                    0 14px 38px
                    rgba(0,0,0,.20) !important;

            }

            [data-testid="stDataFrame"] > div {

                border-radius: 18px !important;

            }

            [data-testid="stDataFrame"] ::-webkit-scrollbar {

                width: 8px;
                height: 8px;

            }

            [data-testid="stDataFrame"] ::-webkit-scrollbar-track {

                background:
                    rgba(15,23,42,.72);

            }

            [data-testid="stDataFrame"] ::-webkit-scrollbar-thumb {

                background:
                    linear-gradient(
                        180deg,
                        #A855F7,
                        #7C3AED
                    );

                border-radius: 20px;

            }

            [data-testid="stDataFrame"] ::-webkit-scrollbar-thumb:hover {

                background: #C084FC;

            }

            .table-footer {

                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
                padding: 10px 3px 0 3px;

            }

            .table-footer-source {

                color: #475569;
                font-size: 10px;

            }

            .table-footer-source strong {

                color: #94A3B8;
                font-weight: 700;

            }

            .table-footer-dot {

                color: #A855F7;
                font-size: 8px;
                margin-right: 4px;

            }

            .table-footer-count {

                color: #C084FC;
                font-size: 10px;
                font-weight: 750;
                padding: 5px 9px;
                border-radius: 8px;

                background:
                    rgba(168,85,247,.08);

                border:
                    1px solid
                    rgba(168,85,247,.12);

            }

            .empty-state {

                text-align: center;
                padding: 70px 20px;
                margin-top: 25px;
                border-radius: 18px;

                border:
                    1px dashed
                    rgba(148,163,184,.15);

                background:
                    rgba(15,23,42,.25);

            }

            .empty-icon {

                color: #475569;
                font-size: 34px;
                margin-bottom: 9px;

            }

            .empty-title {

                color: #E2E8F0;
                font-size: 18px;
                font-weight: 750;

            }

            .empty-description {

                color: #64748B;
                font-size: 12px;
                margin-top: 5px;

            }

            @media (max-width: 1100px) {

                .header-title {

                    font-size: 26px;

                }

            }

            @media (max-width: 900px) {

                .header-title {

                    font-size: 24px;

                }

                .header-badge {

                    display: none;

                }

                .page-header {

                    padding: 20px;

                }

            }

            </style>
            """
        )
