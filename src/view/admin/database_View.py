import pandas as pd
import streamlit as st


class DatabaseView:
    """
    Painel administrativo do Oracle Database.

    Funcionalidades:
    - Listagem de tabelas
    - Pesquisa
    - Estrutura das tabelas
    - Visualização dos dados
    - Importação de CSV
    - Criação de tabelas
    - Exclusão segura de tabelas
    - Consultas SQL
    - Diagnóstico da conexão
    """

    def render(self, db):

        # =========================================================
        # CSS
        # =========================================================

        st.markdown(
            """
            <style>

            .database-title {
                font-size: 28px;
                font-weight: 700;
                margin-bottom: 4px;
            }

            .database-subtitle {
                color: #94a3b8;
                font-size: 14px;
                margin-bottom: 25px;
            }

            .db-card {
                background: linear-gradient(
                    145deg,
                    rgba(18, 24, 38, 0.95),
                    rgba(26, 16, 47, 0.95)
                );

                border: 1px solid rgba(168, 85, 247, 0.20);
                border-radius: 14px;
                padding: 20px;
                min-height: 120px;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
            }

            .db-card-title {
                color: #94a3b8;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-bottom: 8px;
            }

            .db-card-value {
                color: white;
                font-size: 28px;
                font-weight: 700;
            }

            .db-danger-box {
                background: rgba(239, 68, 68, 0.08);
                border: 1px solid rgba(239, 68, 68, 0.30);
                border-radius: 14px;
                padding: 18px;
                margin: 15px 0;
            }

            .db-danger-title {
                color: #f87171;
                font-size: 16px;
                font-weight: 700;
                margin-bottom: 6px;
            }

            .db-danger-text {
                color: #cbd5e1;
                font-size: 13px;
                line-height: 1.5;
            }

            .db-success-box {
                background: rgba(34, 197, 94, 0.08);
                border: 1px solid rgba(34, 197, 94, 0.25);
                border-radius: 12px;
                padding: 15px;
            }

            .db-section {
                margin-top: 25px;
                margin-bottom: 10px;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

        # =========================================================
        # CABEÇALHO
        # =========================================================

        st.markdown(
            '<div class="database-title">🗄️ Database Manager</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="database-subtitle">
                Administração, inspeção e gerenciamento do Oracle Database
            </div>
            """,
            unsafe_allow_html=True,
        )

        # =========================================================
        # ABAS
        # =========================================================

        (
            aba_visao,
            aba_estrutura,
            aba_dados,
            aba_importacao,
            aba_criacao,
            aba_sql,
            aba_admin,
            aba_conexao,
        ) = st.tabs(
            [
                "🗂️ Tabelas",
                "🧱 Estrutura",
                "📊 Dados",
                "📥 Importar",
                "➕ Criar Tabela",
                "💻 SQL",
                "⚠️ Administração",
                "🔌 Conexão",
            ]
        )

        # =========================================================
        # ABA 1 - TABELAS
        # =========================================================

        with aba_visao:

            st.markdown("### 🗂️ Tabelas do Oracle")

            st.caption(
                "Visualize todas as tabelas disponíveis no schema conectado."
            )

            try:

                df_tabelas = db.listar_tabelas()

                if df_tabelas.empty:

                    st.warning(
                        "Nenhuma tabela encontrada."
                    )

                else:

                    total_tabelas = len(df_tabelas)

                    col1, col2, col3 = st.columns(3)

                    with col1:

                        st.markdown(
                            f"""
                            <div class="db-card">
                                <div class="db-card-title">
                                    Total de Tabelas
                                </div>

                                <div class="db-card-value">
                                    {total_tabelas}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with col2:

                        st.markdown(
                            """
                            <div class="db-card">
                                <div class="db-card-title">
                                    Schema
                                </div>

                                <div class="db-card-value">
                                    ALFA
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    with col3:

                        st.markdown(
                            """
                            <div class="db-card">
                                <div class="db-card-title">
                                    Banco
                                </div>

                                <div class="db-card-value">
                                    Oracle
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                    st.write("")

                    # -------------------------------------------------
                    # PESQUISA
                    # -------------------------------------------------

                    pesquisa = st.text_input(
                        "🔎 Pesquisar tabela",
                        placeholder="Digite o nome da tabela...",
                        key="database_pesquisa_tabela",
                    )

                    if pesquisa:

                        termo = pesquisa.strip().upper()

                        df_tabelas = df_tabelas[
                            df_tabelas["TABLE_NAME"]
                            .astype(str)
                            .str.contains(
                                termo,
                                na=False,
                                regex=False,
                            )
                        ]

                    if df_tabelas.empty:

                        st.info(
                            "Nenhuma tabela corresponde à pesquisa."
                        )

                    else:

                        st.write(
                            f"**{len(df_tabelas)} tabela(s) encontrada(s)**"
                        )

                        st.dataframe(
                            df_tabelas,
                            width="stretch",
                            hide_index=True,
                        )

            except Exception as e:

                st.error(
                    f"Erro ao carregar as tabelas: {e}"
                )

        # =========================================================
        # ABA 2 - ESTRUTURA
        # =========================================================

        with aba_estrutura:

            st.markdown(
                "### 🧱 Estrutura da Tabela"
            )

            try:

                df_tabelas = db.listar_tabelas()

                if df_tabelas.empty:

                    st.warning(
                        "Nenhuma tabela encontrada."
                    )

                else:

                    tabela = st.selectbox(
                        "Selecione uma tabela",
                        df_tabelas["TABLE_NAME"].tolist(),
                        key="estrutura_tabela",
                    )

                    if tabela:

                        st.markdown(
                            f"#### 📋 `{tabela}`"
                        )

                        estrutura = db.obter_estrutura_tabela(
                            tabela
                        )

                        if estrutura.empty:

                            st.warning(
                                "Não foi possível obter a estrutura."
                            )

                        else:

                            st.dataframe(
                                estrutura,
                                width="stretch",
                                hide_index=True,
                            )

                        st.divider()

                        st.markdown(
                            "#### 🔑 Chaves e relacionamentos"
                        )

                        constraints = (
                            db.obter_constraints_tabela(
                                tabela
                            )
                        )

                        if constraints.empty:

                            st.info(
                                "Nenhuma constraint encontrada."
                            )

                        else:

                            st.dataframe(
                                constraints,
                                width="stretch",
                                hide_index=True,
                            )

            except Exception as e:

                st.error(
                    f"Erro ao consultar estrutura: {e}"
                )

        # =========================================================
        # ABA 3 - DADOS
        # =========================================================

        with aba_dados:

            st.markdown(
                "### 📊 Dados da Tabela"
            )

            st.caption(
                "Visualize os registros armazenados diretamente no Oracle."
            )

            try:

                df_tabelas = db.listar_tabelas()

                if df_tabelas.empty:

                    st.warning(
                        "Nenhuma tabela encontrada."
                    )

                else:

                    tabela = st.selectbox(
                        "Tabela",
                        df_tabelas["TABLE_NAME"].tolist(),
                        key="dados_tabela",
                    )

                    col1, col2 = st.columns([3, 1])

                    with col1:

                        limite = st.number_input(
                            "Quantidade máxima de registros",
                            min_value=10,
                            max_value=10000,
                            value=100,
                            step=10,
                            key="database_limite",
                        )

                    with col2:

                        st.write("")

                        carregar = st.button(
                            "🔄 Carregar",
                            width="stretch",
                            type="primary",
                            key="database_carregar_dados",
                        )

                    if carregar:

                        with st.spinner(
                            "Consultando Oracle..."
                        ):

                            df = db.consultar_tabela(
                                tabela,
                                limite,
                            )

                        if df.empty:

                            st.info(
                                "A tabela não possui registros."
                            )

                        else:

                            st.success(
                                f"{len(df)} registro(s) carregado(s)."
                            )

                            st.dataframe(
                                df,
                                width="stretch",
                                height=500,
                                hide_index=True,
                            )

                            # -------------------------------------------------
                            # EXPORTAR
                            # -------------------------------------------------

                            csv = df.to_csv(
                                index=False
                            ).encode("utf-8")

                            st.download_button(
                                "📥 Exportar resultado CSV",
                                data=csv,
                                file_name=f"{tabela}.csv",
                                mime="text/csv",
                                width="stretch",
                            )

            except Exception as e:

                st.error(
                    f"Erro ao consultar dados: {e}"
                )

            # =========================================================
            # ABA 4 - IMPORTAÇÃO
            # =========================================================

            with aba_importacao:

                st.markdown(
                    "### 📥 Importar Arquivo"
                )

                st.info(
                    "Importe dados dos arquivos de Internações, Leitos, "
                    "População ou utilize a importação genérica."
                )

                try:

                    df_tabelas = db.listar_tabelas()

                    if df_tabelas.empty:

                        st.warning(
                            "Nenhuma tabela encontrada."
                        )

                    else:

                        # =========================================================
                        # SELEÇÃO DA TABELA
                        # =========================================================

                        tabelas_disponiveis = df_tabelas[
                            "TABLE_NAME"
                        ].tolist()

                        tabela_destino = st.selectbox(
                            "Tabela de destino",
                            tabelas_disponiveis,
                            key="import_tabela",
                        )

                        # =========================================================
                        # ARQUIVO
                        # =========================================================

                        arquivo = st.file_uploader(
                            "Selecione o arquivo CSV",
                            type=["csv"],
                            key="database_csv",
                        )

                        separador = st.selectbox(
                            "Separador",
                            [";", ",", "|"],
                            index=0,
                            key="database_separador",
                        )

                        if arquivo:

                            try:

                                # =================================================
                                # LEITURA DO CSV
                                # =================================================

                                df_import = pd.read_csv(
                                    arquivo,
                                    sep=separador,
                                    encoding="utf-8-sig",
                                )

                                # -------------------------------------------------
                                # LIMPAR NOMES DAS COLUNAS
                                # -------------------------------------------------

                                df_import.columns = [
                                    str(coluna).strip()
                                    for coluna in df_import.columns
                                ]

                                # =================================================
                                # IDENTIFICAR TABELA
                                # =================================================

                                tabela_upper = tabela_destino.upper()

                                # =================================================
                                # TB_INTERNACOES
                                # =================================================

                                if tabela_upper == "TB_INTERNACOES":

                                    st.markdown(
                                        "#### 🏥 Importação de Internações"
                                    )

                                    mapa_colunas = {

                                        "2025/Jan": "VL_JAN_2025",
                                        "2025/Fev": "VL_FEV_2025",
                                        "2025/Mar": "VL_MAR_2025",
                                        "2025/Abr": "VL_ABR_2025",
                                        "2025/Mai": "VL_MAI_2025",
                                        "2025/Jun": "VL_JUN_2025",
                                        "2025/Jul": "VL_JUL_2025",
                                        "2025/Ago": "VL_AGO_2025",
                                        "2025/Set": "VL_SET_2025",
                                        "2025/Out": "VL_OUT_2025",
                                        "2025/Nov": "VL_NOV_2025",
                                        "2025/Dez": "VL_DEZ_2025",

                                        "Total": "VL_TOTAL_2025",

                                    }

                                    df_import.rename(
                                        columns=mapa_colunas,
                                        inplace=True,
                                    )

                                    # -------------------------------------------------
                                    # CAMPOS GERADOS PELO ORACLE
                                    # -------------------------------------------------

                                    df_import.drop(
                                        columns=[
                                            "ID_INTERNACAO",
                                            "DT_IMPORTACAO",
                                        ],
                                        errors="ignore",
                                        inplace=True,
                                    )

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

                                        if coluna in df_import.columns:

                                            df_import[coluna] = pd.to_numeric(
                                                df_import[coluna],
                                                errors="coerce",
                                            )

                                    colunas_faltantes = [
                                        coluna
                                        for coluna in colunas_esperadas
                                        if coluna not in df_import.columns
                                    ]

                                    if colunas_faltantes:

                                        st.error(
                                            "O CSV não possui todas as colunas "
                                            "necessárias para a TB_INTERNACOES."
                                        )

                                        st.markdown(
                                            "#### ❌ Colunas faltantes"
                                        )

                                        for coluna in colunas_faltantes:

                                            st.write(
                                                f"- `{coluna}`"
                                            )

                                    else:

                                        df_import = df_import[
                                            colunas_esperadas
                                        ]

                                        st.success(
                                            "✅ Estrutura de Internações reconhecida."
                                        )

                                        col1, col2, col3 = st.columns(3)

                                        with col1:

                                            st.metric(
                                                "Registros",
                                                f"{len(df_import):,}"
                                            )

                                        with col2:

                                            st.metric(
                                                "Colunas",
                                                len(df_import.columns)
                                            )

                                        with col3:

                                            total_internacoes = (
                                                df_import[
                                                    "VL_TOTAL_2025"
                                                ].sum()
                                            )

                                            st.metric(
                                                "Internações 2025",
                                                f"{total_internacoes:,.0f}"
                                            )

                                        st.markdown(
                                            "#### 👁️ Pré-visualização"
                                        )

                                        st.dataframe(
                                            df_import.head(20),
                                            width="stretch",
                                            hide_index=True,
                                        )

                                        st.warning(
                                            "Confira os dados antes de importar. "
                                            "Os registros serão adicionados à "
                                            "TB_INTERNACOES."
                                        )

                                        confirmar = st.button(
                                            "🚀 Importar Internações",
                                            type="primary",
                                            width="stretch",
                                            key="importar_internacoes",
                                        )

                                        if confirmar:

                                            try:

                                                with st.spinner(
                                                    "Importando internações..."
                                                ):

                                                    quantidade = (
                                                        db.importar_dataframe(
                                                            tabela_destino,
                                                            df_import,
                                                        )
                                                    )

                                                st.success(
                                                    f"✅ {quantidade:,} registro(s) "
                                                    "de internações importado(s)!"
                                                )

                                                st.balloons()

                                            except Exception as e:

                                                st.error(
                                                    "Erro durante a importação."
                                                )

                                                st.exception(e)

                                # =================================================
                                # TB_LEITOS
                                # =================================================

                                elif tabela_upper == "TB_LEITOS":

                                    st.markdown(
                                        "#### 🛏️ Importação de Leitos"
                                    )

                                    # -------------------------------------------------
                                    # PADRONIZAÇÃO DOS NOMES
                                    # -------------------------------------------------

                                    mapa_colunas_leitos = {

                                        "UF": "UF",
                                        "COD_UF": "COD_UF",
                                        "COD_MUNIC": "COD_MUNIC",
                                        "NOME_DO_MUNICIPIO": "NOME_DO_MUNICIPIO",

                                    }

                                    df_import.rename(
                                        columns=mapa_colunas_leitos,
                                        inplace=True,
                                    )

                                    # -------------------------------------------------
                                    # VISUALIZAÇÃO
                                    # -------------------------------------------------

                                    st.success(
                                        "✅ Arquivo de Leitos reconhecido."
                                    )

                                    st.metric(
                                        "Registros",
                                        f"{len(df_import):,}"
                                    )

                                    st.markdown(
                                        "#### 👁️ Pré-visualização"
                                    )

                                    st.dataframe(
                                        df_import.head(20),
                                        width="stretch",
                                        hide_index=True,
                                    )

                                    st.warning(
                                        "Confira as colunas antes de importar. "
                                        "Os registros serão adicionados à "
                                        "TB_LEITOS."
                                    )

                                    confirmar = st.button(
                                        "🚀 Importar Leitos",
                                        type="primary",
                                        width="stretch",
                                        key="importar_leitos",
                                    )

                                    if confirmar:

                                        try:

                                            with st.spinner(
                                                "Importando dados de leitos..."
                                            ):

                                                quantidade = (
                                                    db.importar_dataframe(
                                                        tabela_destino,
                                                        df_import,
                                                    )
                                                )

                                            st.success(
                                                f"✅ {quantidade:,} registro(s) "
                                                "de leitos importado(s)!"
                                            )

                                            st.balloons()

                                        except Exception as e:

                                            st.error(
                                                "Erro durante a importação."
                                            )

                                            st.exception(e)

                                # =================================================
                                # TB_POPULACAO
                                # =================================================

                                elif tabela_upper == "TB_POPULACAO":

                                    st.markdown(
                                        "#### 👥 Importação de População"
                                    )

                                    # -------------------------------------------------
                                    # MAPA CSV → ORACLE
                                    # -------------------------------------------------

                                    mapa_colunas_populacao = {

                                        "UF": "UF",
                                        "COD_UF": "COD_UF",
                                        "COD_MUNIC": "COD_MUNIC",
                                        "NOME_DO_MUNICIPIO":
                                            "NOME_DO_MUNICIPIO",
                                        "POPULACAO_ESTIMADA":
                                            "POPULACAO_ESTIMADA",

                                    }

                                    df_import.rename(
                                        columns=mapa_colunas_populacao,
                                        inplace=True,
                                    )

                                    # -------------------------------------------------
                                    # COLUNAS ESPERADAS
                                    # -------------------------------------------------

                                    colunas_esperadas_populacao = [

                                        "UF",
                                        "COD_UF",
                                        "COD_MUNIC",
                                        "NOME_DO_MUNICIPIO",
                                        "POPULACAO_ESTIMADA",

                                    ]

                                    # -------------------------------------------------
                                    # VERIFICAR COLUNAS
                                    # -------------------------------------------------

                                    colunas_faltantes = [
                                        coluna
                                        for coluna
                                        in colunas_esperadas_populacao
                                        if coluna not in df_import.columns
                                    ]

                                    if colunas_faltantes:

                                        st.error(
                                            "O CSV não possui todas as colunas "
                                            "necessárias para a TB_POPULACAO."
                                        )

                                        st.markdown(
                                            "#### ❌ Colunas faltantes"
                                        )

                                        for coluna in colunas_faltantes:

                                            st.write(
                                                f"- `{coluna}`"
                                            )

                                    else:

                                        # -------------------------------------------------
                                        # CONVERTER CÓDIGOS E POPULAÇÃO
                                        # -------------------------------------------------

                                        colunas_numericas = [

                                            "COD_UF",
                                            "COD_MUNIC",
                                            "POPULACAO_ESTIMADA",

                                        ]

                                        for coluna in colunas_numericas:

                                            df_import[coluna] = pd.to_numeric(
                                                df_import[coluna],
                                                errors="coerce",
                                            )

                                        # -------------------------------------------------
                                        # ORGANIZAR
                                        # -------------------------------------------------

                                        df_import = df_import[
                                            colunas_esperadas_populacao
                                        ]

                                        st.success(
                                            "✅ Estrutura de População reconhecida."
                                        )

                                        # -------------------------------------------------
                                        # KPIs
                                        # -------------------------------------------------

                                        col1, col2, col3 = st.columns(3)

                                        with col1:

                                            st.metric(
                                                "Municípios",
                                                f"{len(df_import):,}"
                                            )

                                        with col2:

                                            st.metric(
                                                "Estados",
                                                df_import["UF"].nunique()
                                            )

                                        with col3:

                                            populacao_total = (
                                                df_import[
                                                    "POPULACAO_ESTIMADA"
                                                ].sum()
                                            )

                                            st.metric(
                                                "População",
                                                f"{populacao_total:,.0f}"
                                            )

                                        # -------------------------------------------------
                                        # PRÉ-VISUALIZAÇÃO
                                        # -------------------------------------------------

                                        st.markdown(
                                            "#### 👁️ Pré-visualização"
                                        )

                                        st.dataframe(
                                            df_import.head(20),
                                            width="stretch",
                                            hide_index=True,
                                        )

                                        st.write(
                                            f"**{len(df_import):,} município(s)** "
                                            "serão importados."
                                        )

                                        with st.expander(
                                            "🔎 Ver colunas que serão importadas"
                                        ):

                                            st.write(
                                                list(df_import.columns)
                                            )

                                        st.warning(
                                            "Confira os dados antes de continuar. "
                                            "Os registros serão adicionados à "
                                            "TB_POPULACAO."
                                        )

                                        confirmar = st.button(
                                            "🚀 Importar População",
                                            type="primary",
                                            width="stretch",
                                            key="importar_populacao",
                                        )

                                        if confirmar:

                                            try:

                                                with st.spinner(
                                                    "Importando população..."
                                                ):

                                                    quantidade = (
                                                        db.importar_dataframe(
                                                            tabela_destino,
                                                            df_import,
                                                        )
                                                    )

                                                st.success(
                                                    f"✅ {quantidade:,} registro(s) "
                                                    "de população importado(s)!"
                                                )

                                                st.balloons()

                                            except Exception as e:

                                                st.error(
                                                    "Erro durante a importação."
                                                )

                                                st.exception(e)

                                # =================================================
                                # IMPORTAÇÃO GENÉRICA
                                # =================================================

                                else:

                                    st.markdown(
                                        "#### 📄 Importação Genérica"
                                    )

                                    st.caption(
                                        "Esta tabela não possui tratamento específico. "
                                        "O arquivo será enviado utilizando os nomes "
                                        "das colunas presentes no CSV."
                                    )

                                    st.markdown(
                                        "#### 👁️ Pré-visualização"
                                    )

                                    st.dataframe(
                                        df_import.head(20),
                                        width="stretch",
                                        hide_index=True,
                                    )

                                    st.write(
                                        f"**{len(df_import):,} registro(s)** "
                                        "encontrado(s)."
                                    )

                                    with st.expander(
                                        "🔎 Ver colunas detectadas"
                                    ):

                                        st.write(
                                            list(df_import.columns)
                                        )

                                    st.warning(
                                        "Confira os nomes das colunas antes de "
                                        "importar. Eles devem corresponder às "
                                        "colunas da tabela Oracle."
                                    )

                                    confirmar = st.button(
                                        "🚀 Importar para o Oracle",
                                        type="primary",
                                        width="stretch",
                                        key="importar_generico",
                                    )

                                    if confirmar:

                                        try:

                                            with st.spinner(
                                                "Importando dados..."
                                            ):

                                                quantidade = (
                                                    db.importar_dataframe(
                                                        tabela_destino,
                                                        df_import,
                                                    )
                                                )

                                            st.success(
                                                f"✅ {quantidade:,} registro(s) "
                                                "importado(s) com sucesso!"
                                            )

                                        except Exception as e:

                                            st.error(
                                                "Erro durante a importação."
                                            )

                                            st.exception(e)

                            except Exception as e:

                                st.error(
                                    f"Erro ao ler o CSV: {e}"
                                )

                                st.exception(e)

                except Exception as e:

                    st.error(
                        f"Erro ao preparar importação: {e}"
                    )

                    st.exception(e)

        # =========================================================
        # ABA 5 - CRIAR TABELA
        # =========================================================

        with aba_criacao:

            st.markdown(
                "### ➕ Criar Nova Tabela"
            )

            st.warning(
                "A criação de tabelas altera permanentemente o schema."
            )

            nome_tabela = st.text_input(
                "Nome da tabela",
                placeholder="EX: TB_HOSPITAIS",
                key="database_nome_tabela",
            )

            st.markdown(
                "#### 🧱 Colunas"
            )

            if "db_colunas_nova_tabela" not in st.session_state:

                st.session_state.db_colunas_nova_tabela = [
                    {
                        "nome": "",
                        "tipo": "VARCHAR2",
                        "tamanho": "255",
                    }
                ]

            tipos_oracle = [
                "VARCHAR2",
                "NUMBER",
                "DATE",
                "TIMESTAMP",
                "CLOB",
            ]

            colunas_remover = []

            for i, coluna in enumerate(
                st.session_state.db_colunas_nova_tabela
            ):

                c1, c2, c3, c4 = st.columns(
                    [3, 2, 2, 1]
                )

                with c1:

                    coluna["nome"] = st.text_input(
                        "Nome",
                        value=coluna["nome"],
                        key=f"db_col_nome_{i}",
                    )

                with c2:

                    coluna["tipo"] = st.selectbox(
                        "Tipo",
                        tipos_oracle,
                        index=tipos_oracle.index(
                            coluna["tipo"]
                        ),
                        key=f"db_col_tipo_{i}",
                    )

                with c3:

                    coluna["tamanho"] = st.text_input(
                        "Tamanho",
                        value=coluna["tamanho"],
                        key=f"db_col_tamanho_{i}",
                    )

                with c4:

                    st.write("")

                    if st.button(
                        "🗑️",
                        key=f"db_col_del_{i}",
                    ):

                        colunas_remover.append(i)

            for i in reversed(colunas_remover):

                st.session_state.db_colunas_nova_tabela.pop(i)

                st.rerun()

            if st.button(
                "➕ Adicionar Coluna",
                width="stretch",
                key="database_adicionar_coluna",
            ):

                st.session_state.db_colunas_nova_tabela.append(
                    {
                        "nome": "",
                        "tipo": "VARCHAR2",
                        "tamanho": "255",
                    }
                )

                st.rerun()

            st.divider()

            if st.button(
                "🏗️ Criar Tabela",
                type="primary",
                width="stretch",
                key="database_criar_tabela",
            ):

                try:

                    if not nome_tabela.strip():

                        st.error(
                            "Informe o nome da tabela."
                        )

                    else:

                        colunas_validas = []

                        for coluna in (
                            st.session_state
                            .db_colunas_nova_tabela
                        ):

                            nome_coluna = (
                                coluna["nome"]
                                .strip()
                            )

                            if not nome_coluna:
                                continue

                            colunas_validas.append(
                                {
                                    "nome": nome_coluna,
                                    "tipo": coluna["tipo"],
                                    "tamanho": coluna["tamanho"],
                                }
                            )

                        if not colunas_validas:

                            st.error(
                                "Adicione pelo menos uma coluna."
                            )

                        else:

                            db.criar_tabela(
                                nome_tabela,
                                colunas_validas,
                            )

                            st.success(
                                f"Tabela `{nome_tabela.upper()}` "
                                "criada com sucesso!"
                            )

                            st.session_state.db_colunas_nova_tabela = [
                                {
                                    "nome": "",
                                    "tipo": "VARCHAR2",
                                    "tamanho": "255",
                                }
                            ]

                            st.rerun()

                except Exception as e:

                    st.error(
                        f"Erro ao criar tabela: {e}"
                    )

        # =========================================================
        # ABA 6 - SQL
        # =========================================================

        with aba_sql:

            st.markdown(
                "### 💻 SQL Explorer"
            )

            st.caption(
                "Execute consultas de leitura diretamente no Oracle."
            )

            sql = st.text_area(
                "Consulta SQL",
                height=220,
                placeholder="""SELECT *
FROM ALFA_USUARIO
FETCH FIRST 100 ROWS ONLY""",
                key="database_sql",
            )

            executar = st.button(
                "▶️ Executar Consulta",
                type="primary",
                width="stretch",
                key="database_executar_sql",
            )

            if executar:

                if not sql.strip():

                    st.warning(
                        "Digite uma consulta SQL."
                    )

                else:

                    sql_limpo = sql.strip().upper()

                    permitidos = (
                        sql_limpo.startswith("SELECT")
                        or sql_limpo.startswith("WITH")
                        or sql_limpo.startswith("EXPLAIN")
                    )

                    if not permitidos:

                        st.error(
                            "Por segurança, o SQL Explorer "
                            "permite apenas consultas de leitura "
                            "(SELECT, WITH e EXPLAIN)."
                        )

                    else:

                        try:

                            with st.spinner(
                                "Executando consulta..."
                            ):

                                resultado = (
                                    db.executar_query_sql(
                                        sql
                                    )
                                )

                            if resultado.empty:

                                st.info(
                                    "A consulta não retornou registros."
                                )

                            else:

                                st.success(
                                    f"{len(resultado)} "
                                    "registro(s) retornado(s)."
                                )

                                st.dataframe(
                                    resultado,
                                    width="stretch",
                                    height=500,
                                    hide_index=True,
                                )

                                csv = resultado.to_csv(
                                    index=False
                                ).encode("utf-8")

                                st.download_button(
                                    "📥 Exportar resultado",
                                    data=csv,
                                    file_name="resultado_sql.csv",
                                    mime="text/csv",
                                    width="stretch",
                                )

                        except Exception as e:

                            st.error(
                                f"Erro SQL: {e}"
                            )

        # =========================================================
        # ABA 7 - ADMINISTRAÇÃO
        # =========================================================

        with aba_admin:

            st.markdown(
                "### ⚠️ Administração do Banco"
            )

            st.caption(
                "Operações administrativas e potencialmente destrutivas."
            )

            st.markdown(
                """
                <div class="db-danger-box">

                    <div class="db-danger-title">
                        ⚠️ Cuidado!
                    </div>

                    <div class="db-danger-text">
                        As operações desta área podem alterar ou excluir
                        permanentemente objetos do banco de dados.
                        Certifique-se de que você realmente deseja
                        executar a operação antes de confirmar.
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            # -----------------------------------------------------
            # EXCLUSÃO DE TABELA
            # -----------------------------------------------------

            st.markdown(
                "#### 🗑️ Excluir tabela"
            )

            try:

                df_tabelas_admin = db.listar_tabelas()

                if df_tabelas_admin.empty:

                    st.info(
                        "Nenhuma tabela disponível para exclusão."
                    )

                else:

                    tabela_excluir = st.selectbox(
                        "Tabela que será excluída",
                        df_tabelas_admin[
                            "TABLE_NAME"
                        ].tolist(),
                        key="admin_tabela_excluir",
                    )

                    st.markdown(
                        f"""
                        <div class="db-danger-box">

                            <div class="db-danger-title">
                                🗑️ Exclusão permanente
                            </div>

                            <div class="db-danger-text">
                                Você selecionou a tabela
                                <strong style="color:white;">
                                    {tabela_excluir}
                                </strong>.
                                <br><br>
                                A exclusão removerá a tabela e seus
                                registros do Oracle.
                                <br>
                                <strong>
                                    Esta operação não poderá ser desfeita.
                                </strong>
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # -------------------------------------------------
                    # CONFIRMAÇÃO
                    # -------------------------------------------------

                    confirmar_exclusao = st.checkbox(
                        f"Eu entendo que a tabela {tabela_excluir} será excluída permanentemente.",
                        key="admin_confirmar_exclusao",
                    )

                    st.write("")

                    excluir = st.button(
                        "🗑️ Excluir Tabela Permanentemente",
                        type="primary",
                        width="stretch",
                        key="admin_excluir_tabela",
                    )

                    if excluir:

                        if not confirmar_exclusao:

                            st.error(
                                "Você precisa confirmar a exclusão "
                                "antes de continuar."
                            )

                        else:

                            # -------------------------------------------------
                            # SEGUNDA CONFIRMAÇÃO
                            # -------------------------------------------------

                            st.session_state[
                                "admin_exclusao_pendente"
                            ] = tabela_excluir

                            st.warning(
                                f"⚠️ Última confirmação: "
                                f"a tabela `{tabela_excluir}` será "
                                "excluída permanentemente."
                            )

                    # -----------------------------------------------------
                    # SEGUNDA CONFIRMAÇÃO
                    # -----------------------------------------------------

                    if (
                        "admin_exclusao_pendente"
                        in st.session_state
                    ):

                        tabela_pendente = (
                            st.session_state[
                                "admin_exclusao_pendente"
                            ]
                        )

                        st.markdown(
                            f"""
                            <div class="db-danger-box">

                                <div class="db-danger-title">
                                    🚨 CONFIRMAÇÃO FINAL
                                </div>

                                <div class="db-danger-text">

                                    Você está prestes a executar:

                                    <br><br>

                                    <strong style="color:#f87171;">
                                        DROP TABLE {tabela_pendente}
                                    </strong>

                                    <br><br>

                                    Todos os dados desta tabela serão
                                    removidos.

                                    <br><br>

                                    Essa operação é irreversível.

                                </div>

                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        c1, c2 = st.columns(2)

                        with c1:

                            cancelar = st.button(
                                "❌ Cancelar",
                                width="stretch",
                                key="admin_cancelar_exclusao",
                            )

                        with c2:

                            confirmar_final = st.button(
                                "🚨 CONFIRMAR EXCLUSÃO",
                                type="primary",
                                width="stretch",
                                key="admin_confirmar_final",
                            )

                        if cancelar:

                            del st.session_state[
                                "admin_exclusao_pendente"
                            ]

                            st.rerun()

                        if confirmar_final:

                            try:

                                with st.spinner(
                                    f"Excluindo {tabela_pendente}..."
                                ):

                                    db.excluir_tabela(
                                        tabela_pendente
                                    )

                                del st.session_state[
                                    "admin_exclusao_pendente"
                                ]

                                st.success(
                                    f"Tabela `{tabela_pendente}` "
                                    "excluída com sucesso."
                                )

                                st.rerun()

                            except Exception as e:

                                st.error(
                                    f"Erro ao excluir tabela: {e}"
                                )

            except Exception as e:

                st.error(
                    f"Erro ao carregar administração: {e}"
                )

        # =========================================================
        # ABA 8 - CONEXÃO
        # =========================================================

        with aba_conexao:

            st.markdown(
                "### 🔌 Diagnóstico do Oracle"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "🔌 Testar Conexão",
                    type="primary",
                    width="stretch",
                    key="database_testar_conexao",
                ):

                    try:

                        conn = db._conectar()

                        conn.close()

                        st.success(
                            "Oracle conectado com sucesso!"
                        )

                    except Exception as e:

                        st.error(
                            f"Falha na conexão: {e}"
                        )

            with col2:

                if st.button(
                    "🔄 Atualizar Metadados",
                    width="stretch",
                    key="database_atualizar_metadados",
                ):

                    st.cache_data.clear()

                    st.success(
                        "Metadados atualizados."
                    )

                    st.rerun()

            st.divider()

            try:

                info = db.obter_info_banco()

                if not info.empty:

                    st.dataframe(
                        info,
                        width="stretch",
                        hide_index=True,
                    )

            except Exception as e:

                st.error(
                    f"Erro ao obter informações do banco: {e}"
                )