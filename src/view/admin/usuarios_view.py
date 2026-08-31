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
    st.caption("Preencha os dados abaixo. A senha será armazenada de forma criptografada.")

    with st.form("form_novo_usuario", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            nm_completo = st.text_input("Nome Completo", placeholder="Ex: Ana Silva")
        with col2:
            nm_login = st.text_input("Login de Acesso", placeholder="Ex: ana.silva")

        ds_email = st.text_input("E-mail Corporativo", placeholder="Ex: ana.silva@empresa.com.br")

        col1, col2 = st.columns(2)
        with col1:
            senha_plana = st.text_input("Senha Inicial", type="password", placeholder="Digite a senha")
        with col2:
            confirmar_senha = st.text_input("Confirmar Senha", type="password", placeholder="Repita a senha")

        status = st.selectbox("Status", ["S - Ativo", "N - Inativo"])
        st.write("")
        
        submit_button = st.form_submit_button("💾 Salvar Usuário", type="primary", use_container_width=True)

        if submit_button:
            if not nm_completo.strip():
                st.error("O nome completo é obrigatório.")
                return
            if not nm_login.strip():
                st.error("O login é obrigatório.")
                return
            if not ds_email.strip():
                st.error("O e-mail é obrigatório.")
                return
            if not senha_plana:
                st.error("A senha é obrigatória.")
                return
            if not confirmar_senha:
                st.error("Confirme a senha.")
                return
            if senha_plana != confirmar_senha:
                st.error("As senhas não coincidem.")
                return
            if len(senha_plana) < 4:
                st.error("A senha deve possuir pelo menos 4 caracteres.")
                return

            senha_hash = gerar_hash_senha(senha_plana)
            status_limpo = status[0]

            sucesso = db.cadastrar_usuario(
                nm_login=nm_login.strip(),
                ds_email=ds_email.strip(),
                ds_senha_hash=senha_hash,
                nm_completo=nm_completo.strip(),
                fl_ativo=status_limpo
            )

            if sucesso:
                st.success("Usuário cadastrado com sucesso!")
                st.rerun()
            else:
                st.error("Não foi possível cadastrar o usuário. Verifique o terminal para mais detalhes.")


# =========================================================
# MODAL - EDITAR USUÁRIO
# =========================================================
@st.dialog("✏️ Editar Usuário")
def modal_editar_usuario(usuario, db):
    id_usr = usuario.get("ID_USUARIO")
    nome_atual = str(usuario.get("NM_COMPLETO", ""))
    login_atual = str(usuario.get("NM_LOGIN", ""))
    email_atual = str(usuario.get("DS_EMAIL", ""))
    status_atual = str(usuario.get("FL_ATIVO", "S")).strip().upper()
    idx_status = 0 if status_atual == "S" else 1

    st.markdown(f"Alterando dados de **{nome_atual}**")
    st.caption("Altere apenas os dados necessários. A senha só será modificada se uma nova for informada.")

    with st.form(f"form_editar_{id_usr}", clear_on_submit=False):
        st.markdown("#### 👤 Dados da Conta")
        col1, col2 = st.columns(2)
        with col1:
            novo_nome = st.text_input("Nome Completo", value=nome_atual)
        with col2:
            novo_login = st.text_input("Login de Acesso", value=login_atual)

        novo_email = st.text_input("E-mail Corporativo", value=email_atual)
        novo_status = st.selectbox("Status", ["S - Ativo", "N - Inativo"], index=idx_status)

        st.divider()
        st.markdown("#### 🔐 Alterar Senha")
        st.caption("Deixe os dois campos vazios para manter a senha atual.")
        
        nova_senha = st.text_input("Nova Senha", type="password", placeholder="Digite somente se quiser alterar")
        confirmar_nova_senha = st.text_input("Confirmar Nova Senha", type="password", placeholder="Repita a nova senha")
        st.write("")

        submit_button = st.form_submit_button("💾 Salvar Alterações", type="primary", use_container_width=True)

        if submit_button:
            if not novo_nome.strip():
                st.error("O nome não pode ficar vazio.")
                return
            if not novo_login.strip():
                st.error("O login não pode ficar vazio.")
                return
            if not novo_email.strip():
                st.error("O e-mail não pode ficar vazio.")
                return

            senha_hash = None
            if nova_senha or confirmar_nova_senha:
                if not nova_senha:
                    st.error("Informe a nova senha.")
                    return
                if not confirmar_nova_senha:
                    st.error("Confirme a nova senha.")
                    return
                if nova_senha != confirmar_nova_senha:
                    st.error("As novas senhas não coincidem.")
                    return
                if len(nova_senha) < 4:
                    st.error("A senha deve possuir pelo menos 4 caracteres.")
                    return
                senha_hash = gerar_hash_senha(nova_senha)

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
                    st.success("Usuário e senha atualizados com sucesso!")
                else:
                    st.success("Dados do usuário atualizados com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao atualizar o usuário.")


# =========================================================
# MODAL - EXCLUIR USUÁRIO
# =========================================================
@st.dialog("🗑️ Confirmar Exclusão")
def modal_remover_usuario(usuario, db):
    nome = usuario.get("NM_COMPLETO", "este usuário")
    st.warning(f"Tem certeza que deseja remover permanentemente o usuário **{nome}**?")
    st.info("⚠️ Esta ação não poderá ser desfeita.")
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        excluir = st.button("🗑️ Sim, Excluir", use_container_width=True, type="primary")
    with col2:
        cancelar = st.button("Cancelar", use_container_width=True)

    if excluir:
        sucesso = db.excluir_usuario(usuario.get("ID_USUARIO"))
        if sucesso:
            st.success("Usuário excluído com sucesso!")
            st.rerun()
        else:
            st.error("Erro ao excluir usuário.")

    if cancelar:
        st.rerun()


# =========================================================
# VIEW PRINCIPAL
# =========================================================
class UsuariosView:
    """View responsável pelo gerenciamento dos usuários do sistema."""

    def render(self, db):
        # Injeção de CSS para padrão SaaS
        st.html(
            """
            <style>
                /* Botão Primário SaaS (Índigo) */
                .stButton button[kind="primary"] {
                    background-color: #6366f1 !important;
                    color: white !important;
                    border: none !important;
                    border-radius: 8px !important;
                    font-weight: 600 !important;
                    transition: all 0.3s ease !important;
                }
                .stButton button[kind="primary"]:hover {
                    background-color: #4f46e5 !important;
                    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
                }
                
                /* Estilização da Tabela Customizada */
                .cabecalho-usuarios {
                    font-weight: 700;
                    color: #94a3b8;
                    font-size: 11px;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    margin-bottom: 12px;
                    border-bottom: 1px solid rgba(255,255,255,0.1);
                    padding-bottom: 10px;
                }
                .linha-usuario {
                    font-size: 14px;
                    color: #f8fafc;
                    padding: 12px 0;
                    border-bottom: 1px solid rgba(255,255,255,0.03);
                    display: flex;
                    align-items: center;
                }
            </style>
            """
        )

        with st.spinner("Carregando base de usuários..."):
            df = db.listar_usuarios()

        if df.empty:
            st.info("Nenhum usuário encontrado.")
            return

        df.columns = [str(c).upper() for c in df.columns]

        # =====================================================
        # BARRA DE AÇÃO SUPERIOR (SaaS Pattern)
        # =====================================================
        
        # Função callback para limpar a busca antes de recarregar a tela
        def limpar_busca():
            if "pesquisa_usuario_input" in st.session_state:
                st.session_state["pesquisa_usuario_input"] = ""

        col_search, col_clear, col_btn = st.columns([6, 1, 2], gap="medium", vertical_alignment="bottom")

        with col_search:
            pesquisa = st.text_input(
                "🔎 Pesquisar usuário",
                placeholder="Busque por nome, login ou e-mail...",
                label_visibility="visible",
                key="pesquisa_usuario_input"
            )

        with col_clear:
            # O parâmetro on_click chama a função limpar_busca automaticamente
            st.button(
                "✖️ Limpar", 
                use_container_width=True, 
                help="Remover filtros",
                on_click=limpar_busca
            )

        with col_btn:
            if st.button("➕ Novo Usuário", type="primary", use_container_width=True):
                modal_novo_usuario(db)

        # Lógica de Filtro
        pesquisa = pesquisa.strip().lower()
        if pesquisa:
            mask = (
                df["NM_COMPLETO"].fillna("").astype(str).str.lower().str.contains(pesquisa, na=False) |
                df["NM_LOGIN"].fillna("").astype(str).str.lower().str.contains(pesquisa, na=False) |
                df["DS_EMAIL"].fillna("").astype(str).str.lower().str.contains(pesquisa, na=False)
            )
            df_filtrado = df[mask]
        else:
            df_filtrado = df

        # =====================================================
        # MÉTRICAS E RESULTADOS
        # =====================================================
        st.caption(f"Exibindo **{len(df_filtrado)}** de **{len(df)}** usuários cadastrados.")

        if df_filtrado.empty:
            st.warning(f'Nenhum usuário encontrado para "{pesquisa}".')
            return

        # =====================================================
        # TABELA DE USUÁRIOS
        # =====================================================
        with st.container(border=True):
            
            colunas_layout = [3, 2, 3, 1, 2, 1, 1]
            hc = st.columns(colunas_layout)

            # Cabeçalhos
            headers = ["Nome Completo", "Login", "E-mail", "Status", "Criado em", "Editar", "Remover"]
            for i, header_text in enumerate(headers):
                hc[i].markdown(f"<div class='cabecalho-usuarios'>{header_text}</div>", unsafe_allow_html=True)

            # Linhas de Dados
            for idx, row in df_filtrado.iterrows():
                rc = st.columns(colunas_layout, vertical_alignment="center")

                rc[0].markdown(f"<div class='linha-usuario'>{row.get('NM_COMPLETO', '-')}</div>", unsafe_allow_html=True)
                rc[1].markdown(f"<div class='linha-usuario'>{row.get('NM_LOGIN', '-')}</div>", unsafe_allow_html=True)
                
                # E-mail com formatação um pouco mais suave
                rc[2].markdown(f"<div class='linha-usuario' style='color: #cbd5e1;'>{row.get('DS_EMAIL', '-')}</div>", unsafe_allow_html=True)

                status_val = str(row.get("FL_ATIVO", "S")).strip().upper()
                if status_val == "S":
                    rc[3].markdown("<div class='linha-usuario'>🟢 Ativo</div>", unsafe_allow_html=True)
                else:
                    rc[3].markdown("<div class='linha-usuario'>🔴 Inativo</div>", unsafe_allow_html=True)

                data_criacao = row.get("DT_CRIACAO", "-")
                if data_criacao != "-":
                    try:
                        data_criacao = str(data_criacao)[:10]
                    except Exception:
                        data_criacao = "-"
                rc[4].markdown(f"<div class='linha-usuario'>{data_criacao}</div>", unsafe_allow_html=True)

                if rc[5].button("✏️", key=f"edit_{idx}", help="Editar usuário", use_container_width=True):
                    modal_editar_usuario(row, db)

                if rc[6].button("🗑️", key=f"del_{idx}", help="Excluir usuário", use_container_width=True):
                    modal_remover_usuario(row, db)