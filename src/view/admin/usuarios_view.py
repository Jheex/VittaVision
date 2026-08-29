import streamlit as st
import hashlib


# =========================================================
# HASH DE SENHA
# =========================================================

def gerar_hash_senha(senha_texto_plano: str) -> str:
    """
    Converte a senha em texto plano para SHA-256.
    O mesmo método é utilizado no login.
    """
    return hashlib.sha256(
        senha_texto_plano.encode("utf-8")
    ).hexdigest()


# =========================================================
# MODAL - NOVO USUÁRIO
# =========================================================

@st.dialog("➕ Cadastrar Novo Usuário")
def modal_novo_usuario(db):

    st.markdown("### 👤 Dados do novo usuário")

    st.caption(
        "Preencha os dados abaixo. "
        "A senha será armazenada de forma criptografada."
    )

    with st.form(
        "form_novo_usuario",
        clear_on_submit=False
    ):

        col1, col2 = st.columns(2)

        with col1:

            nm_completo = st.text_input(
                "Nome Completo",
                placeholder="Ex: Ana Silva"
            )

        with col2:

            nm_login = st.text_input(
                "Login de Acesso",
                placeholder="Ex: ana.silva"
            )

        ds_email = st.text_input(
            "E-mail Corporativo",
            placeholder="Ex: ana.silva@empresa.com.br"
        )

        col1, col2 = st.columns(2)

        with col1:

            senha_plana = st.text_input(
                "Senha Inicial",
                type="password",
                placeholder="Digite a senha"
            )

        with col2:

            confirmar_senha = st.text_input(
                "Confirmar Senha",
                type="password",
                placeholder="Repita a senha"
            )

        status = st.selectbox(
            "Status",
            [
                "S - Ativo",
                "N - Inativo"
            ]
        )

        st.write("")

        submit_button = st.form_submit_button(
            "💾 Salvar Usuário",
            type="primary",
            width="stretch"
        )

        if submit_button:

            # =================================================
            # VALIDAÇÕES
            # =================================================

            if not nm_completo.strip():

                st.error(
                    "O nome completo é obrigatório."
                )

                return

            if not nm_login.strip():

                st.error(
                    "O login é obrigatório."
                )

                return

            if not ds_email.strip():

                st.error(
                    "O e-mail é obrigatório."
                )

                return

            if not senha_plana:

                st.error(
                    "A senha é obrigatória."
                )

                return

            if not confirmar_senha:

                st.error(
                    "Confirme a senha."
                )

                return

            if senha_plana != confirmar_senha:

                st.error(
                    "As senhas não coincidem."
                )

                return

            if len(senha_plana) < 4:

                st.error(
                    "A senha deve possuir pelo menos 4 caracteres."
                )

                return

            # =================================================
            # GERAR HASH
            # =================================================

            senha_hash = gerar_hash_senha(
                senha_plana
            )

            status_limpo = status[0]

            # =================================================
            # CADASTRAR
            # =================================================

            sucesso = db.cadastrar_usuario(
                nm_login=nm_login.strip(),
                ds_email=ds_email.strip(),
                ds_senha_hash=senha_hash,
                nm_completo=nm_completo.strip(),
                fl_ativo=status_limpo
            )

            if sucesso:

                st.success(
                    "Usuário cadastrado com sucesso!"
                )

                st.rerun()

            else:

                st.error(
                    "Não foi possível cadastrar o usuário. "
                    "Verifique o terminal para mais detalhes."
                )


# =========================================================
# MODAL - EDITAR USUÁRIO
# =========================================================

@st.dialog("✏️ Editar Usuário")
def modal_editar_usuario(usuario, db):

    id_usr = usuario.get("ID_USUARIO")

    nome_atual = str(
        usuario.get(
            "NM_COMPLETO",
            ""
        )
    )

    login_atual = str(
        usuario.get(
            "NM_LOGIN",
            ""
        )
    )

    email_atual = str(
        usuario.get(
            "DS_EMAIL",
            ""
        )
    )

    status_atual = str(
        usuario.get(
            "FL_ATIVO",
            "S"
        )
    ).strip().upper()

    idx_status = (
        0
        if status_atual == "S"
        else 1
    )

    st.markdown(
        f"Alterando dados de **{nome_atual}**"
    )

    st.caption(
        "Altere apenas os dados necessários. "
        "A senha só será modificada se uma nova senha for informada."
    )

    with st.form(
        f"form_editar_{id_usr}",
        clear_on_submit=False
    ):

        # =================================================
        # DADOS DA CONTA
        # =================================================

        st.markdown("#### 👤 Dados da Conta")

        col1, col2 = st.columns(2)

        with col1:

            novo_nome = st.text_input(
                "Nome Completo",
                value=nome_atual
            )

        with col2:

            novo_login = st.text_input(
                "Login de Acesso",
                value=login_atual
            )

        novo_email = st.text_input(
            "E-mail Corporativo",
            value=email_atual
        )

        novo_status = st.selectbox(
            "Status",
            [
                "S - Ativo",
                "N - Inativo"
            ],
            index=idx_status
        )

        # =================================================
        # SENHA
        # =================================================

        st.divider()

        st.markdown("#### 🔐 Alterar Senha")

        st.caption(
            "Deixe os dois campos vazios para manter a senha atual."
        )

        nova_senha = st.text_input(
            "Nova Senha",
            type="password",
            placeholder="Digite somente se quiser alterar"
        )

        confirmar_nova_senha = st.text_input(
            "Confirmar Nova Senha",
            type="password",
            placeholder="Repita a nova senha"
        )

        st.write("")

        submit_button = st.form_submit_button(
            "💾 Salvar Alterações",
            type="primary",
            width="stretch"
        )

        if submit_button:

            # =================================================
            # VALIDAÇÕES DOS DADOS
            # =================================================

            if not novo_nome.strip():

                st.error(
                    "O nome não pode ficar vazio."
                )

                return

            if not novo_login.strip():

                st.error(
                    "O login não pode ficar vazio."
                )

                return

            if not novo_email.strip():

                st.error(
                    "O e-mail não pode ficar vazio."
                )

                return

            # =================================================
            # SENHA
            # =================================================

            senha_hash = None

            # Se um dos campos foi preenchido,
            # os dois precisam ser preenchidos.

            if nova_senha or confirmar_nova_senha:

                if not nova_senha:

                    st.error(
                        "Informe a nova senha."
                    )

                    return

                if not confirmar_nova_senha:

                    st.error(
                        "Confirme a nova senha."
                    )

                    return

                if nova_senha != confirmar_nova_senha:

                    st.error(
                        "As novas senhas não coincidem."
                    )

                    return

                if len(nova_senha) < 4:

                    st.error(
                        "A senha deve possuir pelo menos 4 caracteres."
                    )

                    return

                senha_hash = gerar_hash_senha(
                    nova_senha
                )

            # =================================================
            # ATUALIZAR BANCO
            # =================================================

            sucesso = db.atualizar_usuario(
                id_usuario=id_usr,
                nm_login=novo_login.strip(),
                nm_completo=novo_nome.strip(),
                ds_email=novo_email.strip(),
                fl_ativo=novo_status[0],
                ds_senha_hash=senha_hash
            )

            if sucesso:

                if senha_hash:

                    st.success(
                        "Usuário e senha atualizados com sucesso!"
                    )

                else:

                    st.success(
                        "Dados do usuário atualizados com sucesso!"
                    )

                st.rerun()

            else:

                st.error(
                    "Erro ao atualizar o usuário."
                )


# =========================================================
# MODAL - EXCLUIR USUÁRIO
# =========================================================

@st.dialog("🗑️ Confirmar Exclusão")
def modal_remover_usuario(usuario, db):

    nome = usuario.get(
        "NM_COMPLETO",
        "este usuário"
    )

    st.warning(
        f"Tem certeza que deseja remover permanentemente "
        f"o usuário **{nome}**?"
    )

    st.info(
        "⚠️ Esta ação não poderá ser desfeita."
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        excluir = st.button(
            "🗑️ Sim, Excluir",
            width="stretch",
            type="primary"
        )

    with col2:

        cancelar = st.button(
            "Cancelar",
            width="stretch"
        )

    if excluir:

        sucesso = db.excluir_usuario(
            usuario.get("ID_USUARIO")
        )

        if sucesso:

            st.success(
                "Usuário excluído com sucesso!"
            )

            st.rerun()

        else:

            st.error(
                "Erro ao excluir usuário."
            )

    if cancelar:

        st.rerun()


# =========================================================
# VIEW PRINCIPAL
# =========================================================

class UsuariosView:
    """
    View responsável pelo gerenciamento
    dos usuários do sistema.
    """

    def render(self, db):

        # =====================================================
        # CABEÇALHO
        # =====================================================

        col1, col2 = st.columns(
            [4, 1]
        )

        with col1:

            st.markdown(
                "## 👥 Acesso de Usuários"
            )

            st.caption(
                "Gerencie usuários, permissões de acesso "
                "e credenciais do sistema."
            )

        with col2:

            if st.button(
                "➕ Adicionar Usuário",
                type="primary",
                width="stretch"
            ):

                modal_novo_usuario(db)

        st.write("")

        # =====================================================
        # CARREGAR USUÁRIOS
        # =====================================================

        with st.spinner(
            "Carregando base de usuários..."
        ):

            df = db.listar_usuarios()

        if df.empty:

            st.info(
                "Nenhum usuário encontrado."
            )

            return

        # =====================================================
        # NORMALIZAR COLUNAS
        # =====================================================

        df.columns = [
            str(c).upper()
            for c in df.columns
        ]

        # =====================================================
        # PESQUISA
        # =====================================================

        st.markdown(
            "### 🔎 Pesquisar usuário"
        )

        pesquisa = st.text_input(
            "Pesquisar",
            placeholder=(
                "Digite nome, login ou e-mail..."
            ),
            label_visibility="collapsed"
        )

        pesquisa = pesquisa.strip().lower()

        if pesquisa:

            mask = (
                df["NM_COMPLETO"]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(
                    pesquisa,
                    na=False
                )
                |
                df["NM_LOGIN"]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(
                    pesquisa,
                    na=False
                )
                |
                df["DS_EMAIL"]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(
                    pesquisa,
                    na=False
                )
            )

            df_filtrado = df[mask]

        else:

            df_filtrado = df

        # =====================================================
        # CONTADOR
        # =====================================================

        total = len(df)
        encontrados = len(df_filtrado)

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Total de usuários",
                total
            )

        with col2:

            st.metric(
                "Encontrados",
                encontrados
            )

        st.write("")

        # =====================================================
        # NENHUM RESULTADO
        # =====================================================

        if df_filtrado.empty:

            st.warning(
                f"Nenhum usuário encontrado para "
                f'"{pesquisa}".'
            )

            return

        # =====================================================
        # CSS DA TABELA
        # =====================================================

        st.markdown(
            """
            <style>

            .cabecalho-usuarios {
                font-weight: 600;
                color: #94a3b8;
                font-size: 13px;
                margin-bottom: 8px;
                border-bottom: 1px solid
                    rgba(255,255,255,0.10);
                padding-bottom: 8px;
            }

            .linha-usuario {
                padding-top: 8px;
                padding-bottom: 8px;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

        # =====================================================
        # CABEÇALHO
        # =====================================================

        colunas_layout = [
            3,
            2,
            3,
            1,
            2,
            1,
            1
        ]

        hc = st.columns(
            colunas_layout
        )

        hc[0].markdown(
            "<div class='cabecalho-usuarios'>"
            "Nome Completo"
            "</div>",
            unsafe_allow_html=True
        )

        hc[1].markdown(
            "<div class='cabecalho-usuarios'>"
            "Login"
            "</div>",
            unsafe_allow_html=True
        )

        hc[2].markdown(
            "<div class='cabecalho-usuarios'>"
            "E-mail"
            "</div>",
            unsafe_allow_html=True
        )

        hc[3].markdown(
            "<div class='cabecalho-usuarios'>"
            "Status"
            "</div>",
            unsafe_allow_html=True
        )

        hc[4].markdown(
            "<div class='cabecalho-usuarios'>"
            "Criado em"
            "</div>",
            unsafe_allow_html=True
        )

        hc[5].markdown(
            "<div class='cabecalho-usuarios'>"
            "Editar"
            "</div>",
            unsafe_allow_html=True
        )

        hc[6].markdown(
            "<div class='cabecalho-usuarios'>"
            "Remover"
            "</div>",
            unsafe_allow_html=True
        )

        # =====================================================
        # LINHAS
        # =====================================================

        for idx, row in df_filtrado.iterrows():

            rc = st.columns(
                colunas_layout
            )

            # -------------------------------------------------
            # NOME
            # -------------------------------------------------

            rc[0].write(
                row.get(
                    "NM_COMPLETO",
                    "-"
                )
            )

            # -------------------------------------------------
            # LOGIN
            # -------------------------------------------------

            rc[1].write(
                row.get(
                    "NM_LOGIN",
                    "-"
                )
            )

            # -------------------------------------------------
            # E-MAIL
            # -------------------------------------------------

            rc[2].write(
                row.get(
                    "DS_EMAIL",
                    "-"
                )
            )

            # -------------------------------------------------
            # STATUS
            # -------------------------------------------------

            status_val = str(
                row.get(
                    "FL_ATIVO",
                    "S"
                )
            ).strip().upper()

            if status_val == "S":

                rc[3].markdown(
                    "🟢 **Ativo**"
                )

            else:

                rc[3].markdown(
                    "🔴 **Inativo**"
                )

            # -------------------------------------------------
            # DATA
            # -------------------------------------------------

            data_criacao = row.get(
                "DT_CRIACAO",
                "-"
            )

            if data_criacao != "-":

                try:

                    data_criacao = str(
                        data_criacao
                    )[:10]

                except Exception:

                    data_criacao = "-"

            rc[4].write(
                data_criacao
            )

            # -------------------------------------------------
            # EDITAR
            # -------------------------------------------------

            if rc[5].button(
                "✏️",
                key=f"edit_{idx}",
                help="Editar usuário"
            ):

                modal_editar_usuario(
                    row,
                    db
                )

            # -------------------------------------------------
            # EXCLUIR
            # -------------------------------------------------

            if rc[6].button(
                "🗑️",
                key=f"del_{idx}",
                help="Excluir usuário"
            ):

                modal_remover_usuario(
                    row,
                    db
                )

            # -------------------------------------------------
            # DIVISOR
            # -------------------------------------------------

            st.markdown(
                """
                <hr style="
                    margin: 0;
                    border: 0;
                    border-top:
                    1px solid
                    rgba(255,255,255,0.05);
                ">
                """,
                unsafe_allow_html=True
            )
