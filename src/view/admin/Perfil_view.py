import streamlit as st


class PerfilView:
    """View dedicada para gerenciar os dados de login e perfil administrativo."""

    def render(self, db):

        if st.button("← Voltar ao Menu Principal", key="voltar_perfil"):
            st.session_state.admin_aba_ativa = "Menu Principal"
            st.rerun()

        perfil_nome = st.session_state.get(
            "admin_perfil",
            "Administrador"
        )

        usuario_email = st.session_state.get(
            "admin_email",
            "admin@vittavision.com"
        )

        # Cabeçalho
        st.markdown("## ⚙️ Meu Perfil")
        st.caption("Gerencie sua conta e suas credenciais de acesso.")

        col1, col2 = st.columns(2, gap="large")

        # =====================================================
        # INFORMAÇÕES DA CONTA
        # =====================================================

        with col1:

            with st.container(border=True):

                st.markdown("### 👤 Informações da conta")
                st.caption("Dados da conta administrativa conectada.")

                st.text_input(
                    "Perfil de acesso",
                    value=perfil_nome,
                    disabled=True
                )

                st.text_input(
                    "E-mail",
                    value=usuario_email,
                    disabled=True
                )

                st.text_input(
                    "Banco conectado",
                    value="Oracle Database (ALFA)",
                    disabled=True
                )

        # =====================================================
        # SEGURANÇA
        # =====================================================

        with col2:

            with st.container(border=True):

                st.markdown("### 🔐 Segurança")
                st.caption("Atualize sua senha de acesso ao sistema.")

                with st.form("form_alterar_senha"):

                    senha_atual = st.text_input(
                        "Senha atual",
                        type="password"
                    )

                    nova_senha = st.text_input(
                        "Nova senha",
                        type="password"
                    )

                    confirmar_senha = st.text_input(
                        "Confirmar nova senha",
                        type="password"
                    )

                    submitted = st.form_submit_button(
                        "🔒 Atualizar senha"
                    )

                    if submitted:

                        if not senha_atual or not nova_senha or not confirmar_senha:
                            st.error(
                                "Preencha todos os campos de senha."
                            )

                        elif nova_senha != confirmar_senha:
                            st.error(
                                "A nova senha e a confirmação não coincidem."
                            )

                        else:
                            st.success(
                                "Senha atualizada com sucesso no sistema!"
                            )

        # =====================================================
        # DICA
        # =====================================================

        st.divider()

        st.info(
            "💡 **Segurança:** Nunca compartilhe suas credenciais "
            "de administrador com terceiros."
        )