import streamlit as st
import pandas as pd
import hashlib
import time

def gerar_hash_senha(senha_texto_plano: str) -> str:
    """Gera o hash SHA-256 para atualizar a senha no banco."""
    return hashlib.sha256(senha_texto_plano.encode("utf-8")).hexdigest()

class PerfilView:
    """View dedicada para gerenciar os dados de login e perfil administrativo no padrão SaaS, com design centralizado de cartão de perfil."""

    def render(self, db):

        # =====================================================
        # 1. BUSCAR DADOS DO USUÁRIO NO BANCO DE DADOS
        # =====================================================
        admin_id = st.session_state.get("admin_id")
        
        # O main.py salva o login do usuário nesta variável caso não consiga o ID
        login_salvo = st.session_state.get("admin_email", "") 
        
        usuario_dados = None
        try:
            df_usuarios = db.listar_usuarios()
            if not df_usuarios.empty:
                # 1ª Tentativa: Buscar pelo ID salvo na sessão
                if admin_id:
                    filtro = df_usuarios[df_usuarios['ID_USUARIO'] == admin_id]
                    if not filtro.empty:
                        usuario_dados = filtro.iloc[0]
                
                # 2ª Tentativa (Fallback): Se o ID estiver nulo, busca pelo Nome de Login
                if usuario_dados is None and login_salvo:
                    filtro = df_usuarios[df_usuarios['NM_LOGIN'].astype(str).str.strip().str.upper() == login_salvo.strip().upper()]
                    if not filtro.empty:
                        usuario_dados = filtro.iloc[0]
                        admin_id = int(usuario_dados['ID_USUARIO'])
                        # Salva o ID corrigido na sessão para não dar mais erro
                        st.session_state.admin_id = admin_id 
        except Exception as e:
            st.error("Erro ao buscar dados no banco Oracle.")

        # Se encontrou no banco, usa os dados reais. Se não, usa valores padrão.
        if usuario_dados is not None:
            perfil_nome = str(usuario_dados.get("NM_COMPLETO", "")).strip()
            usuario_email = str(usuario_dados.get("DS_EMAIL", "")).strip()
            usuario_login = str(usuario_dados.get("NM_LOGIN", "")).strip()
            usuario_status = str(usuario_dados.get("FL_ATIVO", "S")).strip()
            
            # Garante que o nome do perfil exibido na barra lateral fique correto
            st.session_state.admin_perfil = perfil_nome
        else:
            perfil_nome = st.session_state.get("admin_perfil", "Administrador")
            usuario_email = ""
            usuario_login = login_salvo
            usuario_status = "S"

        # =====================================================
        # 2. INJEÇÃO DE CSS
        # =====================================================
        st.html(
            """
            <style>
                /* Estilização para os botões de submit dos formulários */
                [data-testid="stFormSubmitButton"] button {
                    background-color: #6366f1 !important; /* Azul Índigo (Padrão SaaS) */
                    color: white !important;
                    border: none !important;
                    border-radius: 8px !important;
                    font-weight: 600 !important;
                    transition: all 0.3s ease !important;
                    min-height: 45px !important;
                }
                [data-testid="stFormSubmitButton"] button:hover {
                    background-color: #4f46e5 !important;
                    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4) !important;
                    transform: translateY(-2px) !important;
                }
                
                /* Deixa os inputs levemente mais arredondados e com bordas mais suaves */
                div[data-baseweb="input"] {
                    border-radius: 8px !important;
                    background-color: rgba(15, 23, 42, 0.6) !important;
                    border: 1px solid rgba(139, 92, 246, 0.2) !important;
                }
                
                /* Layout Centralizado do Perfil */
                .profile-header-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    padding: 40px 20px;
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.12) 100%);
                    border-radius: 20px;
                    margin-bottom: 25px;
                    border: 1px solid rgba(168, 85, 247, 0.2);
                }
                
                .profile-avatar {
                    width: 110px;
                    height: 110px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #6366f1, #a855f7);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 45px;
                    font-weight: 800;
                    color: white;
                    margin-bottom: 15px;
                    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4);
                    border: 4px solid #0f172a;
                }
                
                .profile-name {
                    font-size: 26px;
                    font-weight: 800;
                    color: white;
                    margin-bottom: 4px;
                    letter-spacing: -0.5px;
                }
                
                .profile-role {
                    font-size: 13px;
                    color: #a5b4fc;
                    font-weight: 700;
                    letter-spacing: 1px;
                }
                
                /* Container da tab de formulários */
                .stTabs [data-baseweb="tab-list"] {
                    gap: 15px;
                    justify-content: center;
                    margin-bottom: 15px;
                }
                
                .stTabs [data-baseweb="tab"] {
                    padding: 10px 20px;
                    border-radius: 8px 8px 0 0;
                    font-weight: 600;
                }
            </style>
            """
        )

        # =====================================================
        # 3. INTERFACE CENTRALIZADA
        # =====================================================
        # Container principal centralizado (usando colunas para restringir a largura na tela de PC)
        _, col_center, _ = st.columns([1, 2, 1])

        with col_center:
            # Header do Perfil (Avatar e Nome)
            inicial = perfil_nome[0].upper() if perfil_nome else "A"
            
            st.html(
                f"""
                <div class="profile-header-container">
                    <div class="profile-avatar">
                        {inicial}
                    </div>
                    <div class="profile-name">
                        {perfil_nome}
                    </div>
                    <div class="profile-role">
                        ADMINISTRADOR DO SISTEMA
                    </div>
                </div>
                """
            )
            
            # Corpo do Perfil - Separado por abas
            tab_info, tab_seguranca = st.tabs(["👤 Meus Dados", "🔐 Segurança"])
            
            # ABA 1: MEUS DADOS (EDITÁVEL)
            with tab_info:
                st.write("")
                st.caption("Gerencie as informações públicas da sua conta.")
                
                with st.form("form_meus_dados", border=False):
                    
                    novo_nome = st.text_input("Nome Completo", value=perfil_nome)
                    novo_login = st.text_input("Login de Acesso", value=usuario_login)
                    novo_email = st.text_input("E-mail Corporativo", value=usuario_email)
                    
                    st.text_input("Banco de Dados Conectado", value="Oracle Database (ALFA)", disabled=True)
                    st.write("")

                    submitted_dados = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)

                    if submitted_dados:
                        if not novo_nome.strip() or not novo_login.strip() or not novo_email.strip():
                            st.error("Todos os campos editáveis são obrigatórios.")
                        else:
                            if admin_id:
                                sucesso = db.atualizar_usuario(
                                    id_usuario=admin_id,
                                    nm_login=novo_login.strip(),
                                    nm_completo=novo_nome.strip(),
                                    ds_email=novo_email.strip(),
                                    fl_ativo=usuario_status
                                )
                                if sucesso:
                                    # Atualiza o cache da sessão
                                    st.session_state.admin_perfil = novo_nome.strip()
                                    st.session_state.admin_email = novo_email.strip()
                                    
                                    # Feedback Visual
                                    st.toast("✅ Perfil atualizado com sucesso!", icon="💾")
                                    st.success("Dados atualizados com sucesso no banco!")
                                    
                                    # Aguarda 1.5s para o usuário ler a mensagem antes de recarregar
                                    time.sleep(1.5)
                                    st.rerun()
                                else:
                                    st.error("Erro ao atualizar os dados no banco Oracle.")
                            else:
                                st.warning("Usuário não identificado no banco de dados.")

            # ABA 2: SEGURANÇA (SENHA)
            with tab_seguranca:
                st.write("")
                st.caption("Atualize sua senha de acesso ao sistema.")
                
                with st.form("form_alterar_senha", border=False):

                    nova_senha = st.text_input("Nova senha", type="password", placeholder="••••••••")
                    confirmar_senha = st.text_input("Confirmar nova senha", type="password", placeholder="••••••••")
                    st.write("")

                    submitted_senha = st.form_submit_button("🔒 Atualizar senha", use_container_width=True)

                    if submitted_senha:
                        if not nova_senha or not confirmar_senha:
                            st.error("Preencha os campos da nova senha e confirmação.")
                        elif nova_senha != confirmar_senha:
                            st.error("A nova senha e a confirmação não coincidem.")
                        elif len(nova_senha) < 4:
                            st.error("A senha deve possuir pelo menos 4 caracteres.")
                        else:
                            if admin_id:
                                senha_hash = gerar_hash_senha(nova_senha)
                                sucesso = db.atualizar_usuario(
                                    id_usuario=admin_id,
                                    nm_login=usuario_login,
                                    nm_completo=perfil_nome,
                                    ds_email=usuario_email,
                                    fl_ativo=usuario_status,
                                    ds_senha_hash=senha_hash
                                )
                                if sucesso:
                                    # Feedback Visual
                                    st.toast("✅ Senha atualizada com sucesso!", icon="🔒")
                                    st.success("Sua senha foi alterada no banco Oracle.")
                                    
                                    # Aguarda 1.5s antes de recarregar
                                    time.sleep(1.5)
                                    st.rerun()
                                else:
                                    st.error("Erro ao atualizar a senha no banco.")
                            else:
                                st.warning("Usuário não identificado.")
                            
            # Dica de segurança fora das abas, no final do card
            st.write("")
            st.info(
                "💡 **Segurança:** Nunca compartilhe suas credenciais "
                "de administrador com terceiros."
            )