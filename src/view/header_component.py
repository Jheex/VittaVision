import base64
import os
import streamlit as st


class HeaderComponent:

    def render(self, pagina_atual="Dashboard"):

        # =========================================================
        # CSS APRIMORADO (Alinhamento Vertical Perfeito & Glassmorphism)
        # =========================================================

        st.markdown(
            """
        <style>

        /* =====================================================
            HEADER PRINCIPAL (Fixado com Glassmorphism)
            ===================================================== */

        .st-key-header_container {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            z-index: 999999 !important;
            box-sizing: border-box !important;
            background: rgba(7, 10, 18, 0.92) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 0 0 16px 16px !important;
            padding: 8px 24px !important;
            margin: 0 !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45) !important;
        }

        /* =====================================================
            ESPAÇO PARA O CONTEÚDO (Evita sobreposição)
            ===================================================== */

        .block-container {
            padding-top: 75px !important;
        }

        /* =====================================================
            ALINHAMENTO RIGOROSO DO CONTAINER E COLUNAS
            ===================================================== */

        .st-key-header_container [data-testid="stHorizontalBlock"] {
            align-items: center !important;
            gap: 6px !important;
        }

        .st-key-header_container [data-testid="column"] {
            display: flex !important;
            align-items: center !important;
            align-self: center !important;
        }

        /* =====================================================
            BOTÕES COMPACTOS COM FONTES MAIORES
            ===================================================== */

        .st-key-header_container button {
            appearance: none !important;
            -webkit-appearance: none !important;
            width: auto !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            height: 38px !important;
            min-height: 38px !important;
            padding: 0 12px !important;
            margin: 0 !important;
            background: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 8px !important;
            box-shadow: none !important;
            outline: none !important;
            color: #cbd5e1 !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            letter-spacing: -0.01em !important;
            transition: all 0.2s ease-in-out !important;
        }

        /* Efeito Glassmorphism no Hover */
        .st-key-header_container button:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            color: #ffffff !important;
        }

        .st-key-header_container button p {
            color: inherit !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
        }

        /* =====================================================
            ESTADO ATIVO
            ===================================================== */

        .header-active {
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
        }

        .header-active button {
            background: rgba(168, 85, 247, 0.15) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            border: 1px solid rgba(168, 85, 247, 0.4) !important;
        }

        .header-active button p {
            color: #e9d5ff !important;
            font-weight: 600 !important;
        }

        .header-btn {
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
        }

        /* =====================================================
            BOTÃO DE VITTA AI (Destaque)
            ===================================================== */

        .header-ai {
            display: flex !important;
            align-items: center !important;
            width: 100% !important;
        }

        .header-ai button {
            background: linear-gradient(135deg, rgba(147, 51, 234, 0.85), rgba(79, 70, 229, 0.85)) !important;
            border: 1px solid rgba(192, 132, 252, 0.5) !important;
            box-shadow: 0 4px 12px rgba(147, 51, 234, 0.3) !important;
        }

        .header-ai button:hover {
            background: linear-gradient(135deg, rgba(168, 85, 247, 0.95), rgba(99, 102, 241, 0.95)) !important;
            box-shadow: 0 6px 16px rgba(147, 51, 234, 0.45) !important;
        }

        .header-ai button p {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        /* =====================================================
            MOBILE RESPONSIVO
            ===================================================== */

        @media (max-width: 900px) {
            .st-key-header_container {
                padding: 6px 10px !important;
                overflow-x: auto !important;
            }
            .block-container {
                padding-top: 65px !important;
            }
        }

        </style>
        """,
            unsafe_allow_html=True,
        )

        # =========================================================
        # HEADER CONTAINER
        # =========================================================

        with st.container(key="header_container"):

            cols = st.columns(
                [
                    2.8,  # Logo + Texto Gradiente
                    0.45,  # Dashboard
                    0.38,  # Mapas
                    0.38,  # Leitos
                    0.48,  # Internações
                    0.42,  # Hospitais
                    0.48,  # Relatórios
                    0.55,  # Vitta AI
                ],
                gap="small",
            )

            col0, col1, col2, col3, col4, col5, col6, col7 = cols

            # =====================================================
            # RENDERIZAR LOGO E TEXTO COM ALINHAMENTO PERFEITO
            # =====================================================
            with col0:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                possible_paths = [
                    os.path.join(current_dir, "..", "assets", "logotipo.png"),
                    os.path.join(current_dir, "src", "assets", "logotipo.png"),
                    os.path.join("src", "assets", "logotipo.png"),
                    "logotipo.png",
                ]

                logo_found = None
                for path in possible_paths:
                    if os.path.exists(path):
                        logo_found = path
                        break

                if logo_found:
                    with open(logo_found, "rb") as image_file:
                        encoded_string = base64.b64encode(
                            image_file.read()
                        ).decode()
                    img_src = f"data:image/png;base64,{encoded_string}"

                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; gap: 12px; width: 100%; margin: 0; padding: 0;">
                            <img src="{img_src}" style="height: 38px; width: auto; object-fit: contain; display: block; margin: 0; padding: 0;" />
                            <span style="font-size: 25px; font-weight: 800; font-family: sans-serif; background: linear-gradient(135deg, #60a5fa 0%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.03em; line-height: 1; display: inline-block; margin: 0; padding: 0;">
                                VITTA VISION
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <div style="display: flex; align-items: center; gap: 10px; width: 100%; margin: 0; padding: 0;">
                            <div style="width: 34px; height: 34px; background: linear-gradient(135deg, #3b82f6, #9333ea); border-radius: 8px; display: flex; align-items: center; justify-content: center; box-shadow: 0 0 12px rgba(147, 51, 234, 0.4);">
                                <div style="width: 12px; height: 12px; background-color: #ffffff; border-radius: 50%;"></div>
                            </div>
                            <span style="font-size: 18px; font-weight: 800; font-family: sans-serif; background: linear-gradient(135deg, #60a5fa 0%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.03em; line-height: 1; display: inline-block; margin: 0; padding: 0;">
                                VITTA VISION
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            # =====================================================
            # FUNÇÃO DE NAVEGAÇÃO
            # =====================================================

            def navegar(nome, chave, coluna):
                with coluna:
                    is_ativo = pagina_atual == nome
                    wrapper_class = "header-active" if is_ativo else "header-btn"

                    st.markdown(
                        f'<div class="{wrapper_class}">', unsafe_allow_html=True
                    )
                    clicou = st.button(
                        nome,
                        key=chave,
                        use_container_width=True,
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

                    if clicou:
                        st.query_params["page"] = nome
                        st.rerun()

            # Chamadas dos menus na ordem exata solicitada
            navegar("Dashboard", "header_dashboard", col1)
            navegar("Mapas", "header_mapas", col2)
            navegar("Leitos", "header_leitos", col3)
            navegar("Internações", "header_internacoes", col4)
            navegar("Hospitais", "header_hospitais", col5)
            navegar("Relatórios", "header_relatorios", col6)

            # VITTA AI (Assistente IA)
            with col7:
                st.markdown('<div class="header-ai">', unsafe_allow_html=True)
                clicou_ai = st.button(
                    "Vitta AI", key="header_assistente_ia", use_container_width=True
                )
                st.markdown("</div>", unsafe_allow_html=True)

                if clicou_ai:
                    st.query_params["page"] = "Assistente IA"
                    st.rerun()