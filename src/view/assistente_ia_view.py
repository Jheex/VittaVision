import streamlit as st

class AssistenteIAView:
    def render(self, model):
        col_title, col_btn = st.columns([4, 1])
        with col_title:
            st.title("✨ Assistente IA")
            st.caption("Inteligência artificial analítica baseada em dados do SUS.")
        with col_btn:
            st.button("✨ Novo chat", key="btn_novo_chat_ia")

        col_main, col_chat = st.columns([2, 1])

        with col_main:
            st.markdown("### Insights Automáticos")
            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                st.info("🚨 **Alerta**\n15 regiões críticas.")
            with mc2:
                st.info("📈 **Tendência**\nAlta demanda.")
            with mc3:
                st.info("🔮 **Previsão**\n+12% próximo mês.")

        with col_chat:
            st.markdown("### 🤖 Chat Vitta")
            st.chat_message("user").write("Qual a situação dos leitos?")
            st.chat_message("assistant").write("A ocupação média está em 82% nas principais unidades.")
            st.text_input("Pergunte algo...", placeholder="Digite aqui...", label_visibility="collapsed")