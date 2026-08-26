import json
import os
import oracledb
import pandas as pd
import streamlit as st
import uuid


class AssistenteIAView:

  def render(self, model=None):
    st.markdown(
        """
            <style>
                /* Trava o scroll da página inteira para cima */
                html, body, [data-testid="stAppViewContainer"] {
                    overflow-x: hidden !important;
                    overscroll-behavior-y: none !important;
                }

                /* Zera o cabeçalho nativo do Streamlit */
                header.stAppHeader {
                    background-color: transparent !important;
                    height: 0px !important;
                    visibility: hidden;
                }
                
                /* Elimina margem do container principal e centraliza com limite */
                .block-container, div.stMainBlockContainer {
                    padding-top: 0rem !important;
                    padding-bottom: 0.5rem !important;
                    max-width: 900px;
                    margin: 0 auto !important;
                }

                .vitta-header {
                    text-align: center;
                    padding-top: 40px;
                    padding-bottom: 4px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                    background-color: inherit;
                    z-index: 10;
                    margin-bottom: 8px;
                }

                .vitta-body {
                    flex-grow: 1;
                    padding: 5px;
                    margin-bottom: 10px;
                }

                .vitta-footer {
                    background-color: inherit;
                    padding-top: 5px;
                    border-top: 1px solid rgba(255, 255, 255, 0.05);
                    z-index: 10;
                    margin-top: auto;
                }

                div.stButton > button {
                    background-color: rgba(168, 85, 247, 0.08);
                    color: #e2e8f0;
                    border: 1px solid rgba(168, 85, 247, 0.25);
                    border-radius: 20px;
                    font-size: 11px;
                    font-weight: 500;
                    transition: all 0.3s ease;
                }
                div.stButton > button:hover {
                    background-color: rgba(168, 85, 247, 0.25);
                    border-color: rgba(168, 85, 247, 0.6);
                    color: #ffffff;
                }

                /* --- CHAT INPUT REFINADO E ÚNICO --- */
                [data-testid="stChatInput"] {
                    background-color: rgba(18, 24, 38, 0.95) !important;
                    border: 1px solid rgba(168, 85, 247, 0.4) !important;
                    border-radius: 30px !important;
                    padding: 4px 10px !important;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
                    max-width: 750px !important;
                    margin: 0 auto !important;
                    transition: all 0.3s ease;
                }

                [data-testid="stChatInput"] > div {
                    background-color: transparent !important;
                    border: none !important;
                    box-shadow: none !important;
                }

                [data-testid="stChatInput"]:focus-within {
                    border-color: rgba(168, 85, 247, 0.9) !important;
                    box-shadow: 0 0 15px rgba(168, 85, 247, 0.25) !important;
                }

                [data-testid="stChatInput"] textarea {
                    color: #f8fafc !important;
                    font-size: 13px !important;
                }

                [data-testid="stChatInput"] button {
                    background-color: #a855f7 !important;
                    color: #ffffff !important;
                    border-radius: 50% !important;
                    border: none !important;
                    width: 32px !important;
                    height: 32px !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    transition: transform 0.2s ease, background-color 0.2s ease;
                }

                [data-testid="stChatInput"] button:hover {
                    background-color: #9333ea !important;
                    transform: scale(1.08);
                }
            </style>
        """,
        unsafe_allow_html=True,
    )

    # --- INICIALIZAÇÃO DO ESTADO DE SESSÃO ÚNICA ---
    if "messages" not in st.session_state:
      st.session_state.messages = [{
          "role": "assistant",
          "content": (
              "Olá! Como posso ajudar você a analisar os dados do SUS"
              " hoje?\n\n*Quer explorar alguma métrica específica ou descobrir"
              " novos insights sobre a rede hospitalar?*"
          ),
      }]

    # Início da estrutura principal
    st.markdown('<div class="vitta-layout">', unsafe_allow_html=True)

    # 1. HEADER INTERNO DA IA
    st.markdown(
        """
            <div class="vitta-header">
                <div style="font-size: 20px; margin-bottom: 0px;">🩺</div>
                <h2 style="color: #f8fafc; font-weight: 800; margin: 0; letter-spacing: 1px; font-size: 14px;">
                    VITTA<span style="color: #c084fc;"> AI</span>
                </h2>
                <p style="color: #94a3b8; font-size: 9px; margin: 0px 0 0 0;">Assistente neural inteligente integrado ao Oracle Select AI.</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. BODY (Mensagens do Chat)
    st.markdown('<div class="vitta-body">', unsafe_allow_html=True)
    for message in st.session_state.messages:
      with st.chat_message(
          message["role"],
          avatar="🤖" if message["role"] == "assistant" else "👤",
      ):
        conteudo = message["content"]

        if isinstance(conteudo, (list, dict)):
          try:
            df = pd.DataFrame(conteudo)
          except Exception:
            df = None

          if df is not None and not df.empty:
            colunas_numericas = df.select_dtypes(
                include=["number"]
            ).columns.tolist()
            if colunas_numericas and len(df) == 1:
              col_nome = colunas_numericas[0]
              st.metric(
                  label=f"Indicador Principal ({col_nome})",
                  value=f"{df[col_nome].iloc[0]:,.0f}",
              )

            st.dataframe(df, use_container_width=True)

            if len(df.columns) >= 2 and len(df) > 1:
              try:
                col_cat = df.columns[0]
                col_val = colunas_numericas[0] if colunas_numericas else None
                if col_val:
                  chart_data = df.set_index(col_cat)[col_val]
                  st.bar_chart(chart_data)
              except Exception:
                pass

            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Baixar Dados em CSV",
                data=csv_data,
                file_name="vitta_relatorio_sus.csv",
                mime="text/csv",
                key=f"dl_{id(conteudo)}",
            )
          else:
            st.write(conteudo)
        else:
          st.markdown(conteudo)

    st.markdown("</div>", unsafe_allow_html=True)  # Fim do vitta-body

    # 3. FOOTER (Sugestões e Input centralizado)
    st.markdown('<div class="vitta-footer">', unsafe_allow_html=True)

    sugestao_clicada = None

    if len(st.session_state.messages) == 1:
      st.markdown(
          "<p style='color: #94a3b8; font-size: 10px; margin-bottom: 3px;"
          " text-align: center; text-transform: uppercase; letter-spacing:"
          " 0.5px;'>💡 Sugestões rápidas</p>",
          unsafe_allow_html=True,
      )

      col1, col2, col3 = st.columns(3)

      with col1:
        if st.button("📊 Maior nº de leitos", use_container_width=True):
          sugestao_clicada = (
              "Quais municípios possuem a maior quantidade de leitos SUS"
              " disponíveis?"
          )
      with col2:
        if st.button("📈 Internações 2024", use_container_width=True):
          sugestao_clicada = (
              "Quais municípios tiveram maior volume de internações em 2024?"
          )
      with col3:
        if st.button("🏥 Relação Pop. x Leitos", use_container_width=True):
          sugestao_clicada = (
              "Mostre a relação entre população e leitos existentes por"
              " município."
          )

    prompt_input = st.chat_input("Digite sua mensagem...")

    st.markdown("</div>", unsafe_allow_html=True)  # Fim do vitta-footer
    st.markdown("</div>", unsafe_allow_html=True)  # Fim do vitta-layout

    prompt_final = sugestao_clicada if sugestao_clicada else prompt_input
    if prompt_final:
      self._processar_pergunta(prompt_final)

  def _processar_pergunta(self, prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})

    prompt_limpo = prompt.strip().lower()
    saudacoes = [
        "oi",
        "olá",
        "ola",
        "tudo bem",
        "bom dia",
        "boa tarde",
        "boa noite",
        "eae",
        "hey",
    ]

    if prompt_limpo in saudacoes:
      resposta_ia = (
          "Olá! Tudo ótimo por aqui. Como posso ajudar você com os dados e"
          ' indicadores da saúde hoje? (Ex: "Quais municípios têm mais'
          ' leitos?")\n\n*Quer analisar alguma região ou indicador em'
          " específico?*"
      )
    elif len(prompt_limpo) < 3:
      resposta_ia = (
          "Por favor, digite uma pergunta completa sobre os dados do SUS (ex: "
          '"Quais municípios têm mais leitos?").\n\n*Fique à vontade para me'
          " perguntar sobre internações, leitos ou redes de saúde!*"
      )
    else:
      with st.spinner("Analisando dados..."):
        dados_ou_texto = self._gerar_resposta_inteligente(prompt)

      if isinstance(dados_ou_texto, (list, dict)):
        resposta_ia = dados_ou_texto
      else:
        gancho = (
            "\n\n---"
            "\n*💡 Análise concluída! Deseja cruzar esses dados com internações,"
            " comparar com outra região ou verificar a média populacional? O"
            " que gostaria de ver a seguir?*"
        )
        resposta_ia = str(dados_ou_texto) + gancho

    st.session_state.messages.append(
        {"role": "assistant", "content": resposta_ia}
    )

    if isinstance(resposta_ia, (list, dict)):
      st.session_state.messages.append({
          "role": "assistant",
          "content": (
              "*💡 Análise concluída! Deseja cruzar esses dados com internações,"
              " comparar com outra região ou verificar a média populacional?"
              " Estou à disposição para aprofundar!*"
          ),
      })

    st.rerun()

  def _gerar_resposta_inteligente(self, query):
    DB_USER = "ADMIN"
    DB_PASSWORD = "Databytes@123"
    DB_DSN = "DATABYTES_HIGH"
    WALLET_DIR = r"C:\Users\Jhona\Downloads\VittaVision\VittaVision\data\Wallet"

    try:
      with oracledb.connect(
          user=DB_USER,
          password=DB_PASSWORD,
          dsn=DB_DSN,
          config_dir=WALLET_DIR,
          wallet_location=WALLET_DIR,
          wallet_password="Databytes@123",
      ) as connection:

        with connection.cursor() as cursor:
          sql_select_ai = """
                    SELECT DBMS_CLOUD_AI.GENERATE(
                        prompt => :q,
                        profile_name => 'SUS_PROFILE',
                        action => 'runsql'
                    ) FROM dual
                """

          cursor.execute(sql_select_ai, {"q": query})
          resultado = cursor.fetchone()

          if resultado and resultado[0]:
            bruto = resultado[0]
            texto_resposta = (
                bruto.read().strip()
                if hasattr(bruto, "read")
                else str(bruto).strip()
            )

            try:
              if texto_resposta.startswith("[") or texto_resposta.startswith(
                  "{"
              ):
                return json.loads(texto_resposta)
            except json.JSONDecodeError:
              pass

            return texto_resposta
          else:
            return "⚠️ O Select AI não retornou dados para esta consulta."

    except Exception as e:
      return f"⚠️ **Erro técnico retornado pelo Oracle:** `{str(e)}`"