import base64
import os

import streamlit as st


class HeaderComponent:

    def render(self, pagina_atual="Dashboard"):

        # =========================================================
        # CSS
        # =========================================================

        st.html(
            """
            <style>

            /* =====================================================
               HEADER PRINCIPAL
               ===================================================== */

            .st-key-header_container {
                position: fixed !important;
                top: 0 !important;
                left: 0 !important;
                width: 100% !important;
                z-index: 999999 !important;

                box-sizing: border-box !important;

                background: rgba(7, 10, 18, 0.94) !important;

                backdrop-filter: blur(18px) !important;
                -webkit-backdrop-filter: blur(18px) !important;

                border-bottom: 1px solid
                    rgba(255, 255, 255, 0.08) !important;

                border-radius: 0 !important;

                padding: 10px 24px !important;

                margin: 0 !important;

                min-height: 86px !important;

                box-shadow:
                    0 10px 30px
                    rgba(0, 0, 0, 0.45) !important;
            }


            /* =====================================================
               ESPAÇO PARA O CONTEÚDO
               ===================================================== */

            .block-container {
                padding-top: 100px !important;
            }


            /* =====================================================
               CONTAINER INTERNO
               ===================================================== */

            .st-key-header_container
            [data-testid="stHorizontalBlock"] {

                align-items: center !important;

                gap: 6px !important;

                min-height: 62px !important;
            }


            .st-key-header_container
            [data-testid="column"] {

                display: flex !important;

                align-items: center !important;

                align-self: center !important;
            }


            /* =====================================================
               PRIMEIRA COLUNA - LOGO
               ===================================================== */

            .st-key-header_container
            [data-testid="column"]:first-child {

                align-items: center !important;

                justify-content: flex-start !important;
            }


            /* =====================================================
               ÁREA DA LOGO
               ===================================================== */

            .vitta-header-logo {

                display: flex;

                align-items: center;

                gap: 12px;

                width: fit-content;

                height: 62px;

                margin: 0;

                padding: 0;

                box-sizing: border-box;
            }


            /* =====================================================
               IMAGEM DA LOGO
               ===================================================== */

            .vitta-header-logo img {

                height: 62px;

                width: auto;

                max-width: 180px;

                object-fit: contain;

                display: block;

                flex-shrink: 0;

                margin: 0;

                padding: 0;
            }


            /* =====================================================
               BLOCO DA MARCA
               ===================================================== */

            .vitta-header-brand {

                display: flex;

                flex-direction: column;

                justify-content: center;

                align-items: flex-start;

                gap: 6px;

                min-width: 0;

                margin: 0;

                padding: 0;

                height: 100%;
            }


            /* =====================================================
               NOME DA MARCA
               ===================================================== */

            .vitta-header-logo-text {

                display: block;

                font-size: 25px;

                font-weight: 900;

                font-family: sans-serif;

                letter-spacing: -0.035em;

                line-height: 1;

                white-space: nowrap;

                margin: 0;

                padding: 0;

                filter:
                    drop-shadow(
                        0 0 8px
                        rgba(99, 102, 241, 0.25)
                    );
            }


            /* =====================================================
               VITTA
               ===================================================== */

            .vitta-brand-vitta {

                color: #ffffff;

                font-weight: 900;
            }


            /* =====================================================
               VISION
               ===================================================== */

            .vitta-brand-vision {

                background:
                    linear-gradient(
                        90deg,
                        #2563eb 0%,
                        #3b82f6 28%,
                        #7c3aed 65%,
                        #9333ea 100%
                    );

                -webkit-background-clip: text;

                -webkit-text-fill-color: transparent;

                background-clip: text;

                font-weight: 900;
            }


            /* =====================================================
               SUBTÍTULO
               ===================================================== */

            .vitta-header-subtitle {

                display: block;

                font-size: 11px;

                font-weight: 600;

                font-family: sans-serif;

                letter-spacing: 0.055em;

                line-height: 1.1;

                white-space: nowrap;

                text-transform: none;

                margin: 0;

                padding: 0;

                filter:
                    drop-shadow(
                        0 0 5px
                        rgba(129, 140, 248, 0.18)
                    );
            }


            /* =====================================================
               "INTELIGÊNCIA QUE"
               ===================================================== */

            .vitta-subtitle-white {

                color: #ffffff;

                font-weight: 600;
            }


            /* =====================================================
               "TRANSFORMA A SAÚDE"
               ===================================================== */

            .vitta-subtitle-gradient {

                background:
                    linear-gradient(
                        90deg,
                        #60a5fa 0%,
                        #818cf8 48%,
                        #c084fc 100%
                    );

                -webkit-background-clip: text;

                -webkit-text-fill-color: transparent;

                background-clip: text;

                font-weight: 700;
            }


            /* =====================================================
               LOGO CLICÁVEL

               IMPORTANTE:
               O LINK NÃO OCUPA MAIS A COLUNA INTEIRA.
               SOMENTE O CONTEÚDO DA LOGO É CLICÁVEL.
               ===================================================== */

            .vitta-header-link {

                display: flex !important;

                align-items: center !important;

                justify-content: flex-start !important;

                width: fit-content !important;

                height: 62px !important;

                text-decoration: none !important;

                color: inherit !important;

                cursor: pointer !important;

                border: none !important;

                box-shadow: none !important;

                margin: 0 !important;

                padding: 0 !important;
            }


            .vitta-header-link:hover {

                text-decoration: none !important;

                color: inherit !important;

                border: none !important;

                box-shadow: none !important;
            }


            .vitta-header-link:visited {

                text-decoration: none !important;

                color: inherit !important;
            }


            .vitta-header-link:active {

                text-decoration: none !important;

                color: inherit !important;
            }


            /* =====================================================
               LOGO ALTERNATIVA
               ===================================================== */

            .vitta-header-logo-fallback {

                display: flex;

                align-items: center;

                gap: 12px;

                width: fit-content;

                height: 62px;

                margin: 0;

                padding: 0;
            }


            .vitta-header-logo-icon {

                width: 40px;

                height: 40px;

                min-width: 40px;

                border-radius: 10px;

                display: flex;

                align-items: center;

                justify-content: center;

                background:
                    linear-gradient(
                        135deg,
                        #3b82f6,
                        #9333ea
                    );

                box-shadow:
                    0 0 16px
                    rgba(147, 51, 234, 0.35);
            }


            .vitta-header-logo-dot {

                width: 14px;

                height: 14px;

                background: #ffffff;

                border-radius: 50%;
            }


            .vitta-header-logo-fallback-text {

                display: block;

                font-size: 23px;

                font-weight: 800;

                font-family: sans-serif;

                letter-spacing: -0.03em;

                white-space: nowrap;

                margin: 0;

                padding: 0;
            }


            /* =====================================================
               FALLBACK - VITTA
               ===================================================== */

            .vitta-fallback-vitta {

                color: #ffffff;

                font-weight: 800;
            }


            /* =====================================================
               FALLBACK - VISION
               ===================================================== */

            .vitta-fallback-vision {

                background:
                    linear-gradient(
                        135deg,
                        #60a5fa 0%,
                        #c084fc 100%
                    );

                -webkit-background-clip: text;

                -webkit-text-fill-color: transparent;

                background-clip: text;

                font-weight: 800;
            }


            /* =====================================================
               BOTÕES NORMAIS
               ===================================================== */

            .st-key-header_container button {

                appearance: none !important;

                -webkit-appearance: none !important;

                width: auto !important;

                display: inline-flex !important;

                align-items: center !important;

                justify-content: center !important;

                height: 42px !important;

                min-height: 42px !important;

                padding: 0 13px !important;

                margin: 0 !important;

                background: transparent !important;

                border: 1px solid transparent !important;

                border-radius: 9px !important;

                box-shadow: none !important;

                outline: none !important;

                color: #cbd5e1 !important;

                font-size: 14px !important;

                font-weight: 500 !important;

                letter-spacing: -0.01em !important;

                transition:
                    all 0.2s ease-in-out !important;

                white-space: nowrap !important;
            }


            /* =====================================================
               TEXTO DOS BOTÕES
               ===================================================== */

            .st-key-header_container button p {

                color: inherit !important;

                font-size: 14px !important;

                font-weight: 500 !important;

                margin: 0 !important;

                padding: 0 !important;

                line-height: 1 !important;
            }


            /* =====================================================
               HOVER BOTÕES NORMAIS
               ===================================================== */

            .st-key-header_container button:hover {

                background:
                    rgba(255, 255, 255, 0.08) !important;

                backdrop-filter: blur(8px) !important;

                -webkit-backdrop-filter: blur(8px) !important;

                border:
                    1px solid
                    rgba(255, 255, 255, 0.15) !important;

                color: #ffffff !important;
            }


            /* =====================================================
               REMOVER HOVER DE FUNDO DA NAVEGAÇÃO
               ===================================================== */

            .st-key-header_dashboard button:hover,
            .st-key-header_leitos button:hover,
            .st-key-header_internacoes button:hover,
            .st-key-header_hospitais button:hover,
            .st-key-header_relatorios button:hover {

                background: transparent !important;

                border:
                    1px solid transparent !important;

                box-shadow: none !important;

                backdrop-filter: none !important;

                -webkit-backdrop-filter: none !important;

                transform: none !important;

                color: #ffffff !important;
            }


            /* =====================================================
               BOTÃO ATIVO
               ===================================================== */

            .header-active {

                display: flex !important;

                align-items: center !important;

                width: 100% !important;
            }


            .header-active button {

                background:
                    rgba(168, 85, 247, 0.15) !important;

                backdrop-filter: blur(8px) !important;

                -webkit-backdrop-filter: blur(8px) !important;

                border:
                    1px solid
                    rgba(168, 85, 247, 0.40) !important;

                box-shadow:
                    0 4px 15px
                    rgba(168, 85, 247, 0.10) !important;
            }


            .header-active button p {

                color: #e9d5ff !important;

                font-weight: 600 !important;
            }


            /* =====================================================
               BOTÃO NORMAL
               ===================================================== */

            .header-btn {

                display: flex !important;

                align-items: center !important;

                width: 100% !important;
            }


            /* =====================================================
               UNDERLINE
               ===================================================== */

            .st-key-header_dashboard button,
            .st-key-header_leitos button,
            .st-key-header_internacoes button,
            .st-key-header_hospitais button,
            .st-key-header_relatorios button {

                position: relative !important;

                overflow: visible !important;
            }


            /* =====================================================
               TRAÇO
               ===================================================== */

            .st-key-header_dashboard button::after,
            .st-key-header_leitos button::after,
            .st-key-header_internacoes button::after,
            .st-key-header_hospitais button::after,
            .st-key-header_relatorios button::after {

                content: "" !important;

                position: absolute !important;

                left: 12px !important;

                right: 12px !important;

                bottom: -2px !important;

                height: 3px !important;

                border-radius: 999px !important;

                background:
                    linear-gradient(
                        90deg,
                        #2563eb 0%,
                        #3b82f6 35%,
                        #7c3aed 70%,
                        #9333ea 100%
                    ) !important;

                box-shadow:
                    0 0 8px
                    rgba(59, 130, 246, 0.45),
                    0 0 12px
                    rgba(147, 51, 234, 0.35) !important;

                transform: scaleX(0) !important;

                transform-origin: left !important;

                opacity: 0 !important;

                transition:
                    transform 0.35s
                    cubic-bezier(0.4, 0, 0.2, 1),
                    opacity 0.20s ease !important;
            }


            /* =====================================================
               HOVER
               ===================================================== */

            .st-key-header_dashboard button:hover::after,
            .st-key-header_leitos button:hover::after,
            .st-key-header_internacoes button:hover::after,
            .st-key-header_hospitais button:hover::after,
            .st-key-header_relatorios button:hover::after {

                transform: scaleX(1) !important;

                opacity: 1 !important;
            }


            /* =====================================================
               ITEM ATIVO
               ===================================================== */

            .header-active button::after {

                transform: scaleX(1) !important;

                opacity: 1 !important;

                transform-origin: left !important;
            }


            /* =====================================================
               BRILHO EXTRA ITEM ATIVO
               ===================================================== */

            .header-active button {

                box-shadow:
                    0 4px 15px
                    rgba(124, 58, 237, 0.10) !important;
            }


            /* =====================================================
               VITTA AI
               ===================================================== */

            .st-key-header_assistente_ia button {

                background:
                    linear-gradient(
                        135deg,
                        #9333ea 0%,
                        #7c3aed 50%,
                        #6366f1 100%
                    ) !important;

                border:
                    1px solid
                    rgba(216, 180, 254, 0.80) !important;

                color: #ffffff !important;

                box-shadow:
                    0 4px 16px
                    rgba(124, 58, 237, 0.45) !important;
            }


            .st-key-header_assistente_ia button p {

                color: #ffffff !important;

                font-weight: 700 !important;

                font-size: 14px !important;
            }


            .st-key-header_assistente_ia button:hover {

                background:
                    linear-gradient(
                        135deg,
                        #a855f7 0%,
                        #8b5cf6 50%,
                        #6366f1 100%
                    ) !important;

                border:
                    1px solid
                    rgba(233, 213, 255, 0.95) !important;

                color: #ffffff !important;

                box-shadow:
                    0 7px 22px
                    rgba(139, 92, 246, 0.60) !important;

                transform: translateY(-1px) !important;
            }


            .st-key-header_assistente_ia button:active {

                transform: translateY(0) !important;

                box-shadow:
                    0 3px 10px
                    rgba(124, 58, 237, 0.40) !important;
            }


            /* =====================================================
               LOGIN
               ===================================================== */

            .st-key-header_admin_login button {

                background:
                    linear-gradient(
                        135deg,
                        #2563eb 0%,
                        #3b82f6 50%,
                        #06b6d4 100%
                    ) !important;

                border:
                    1px solid
                    rgba(147, 197, 253, 0.85) !important;

                color: #ffffff !important;

                box-shadow:
                    0 4px 16px
                    rgba(37, 99, 235, 0.45) !important;
            }


            .st-key-header_admin_login button p {

                color: #ffffff !important;

                font-weight: 700 !important;

                font-size: 14px !important;
            }


            .st-key-header_admin_login button:hover {

                background:
                    linear-gradient(
                        135deg,
                        #3b82f6 0%,
                        #2563eb 50%,
                        #0891b2 100%
                    ) !important;

                border:
                    1px solid
                    rgba(191, 219, 254, 1) !important;

                color: #ffffff !important;

                box-shadow:
                    0 7px 22px
                    rgba(37, 99, 235, 0.60) !important;

                transform: translateY(-1px) !important;
            }


            .st-key-header_admin_login button:active {

                transform: translateY(0) !important;

                box-shadow:
                    0 3px 10px
                    rgba(37, 99, 235, 0.40) !important;
            }


            /* =====================================================
               ADMIN LOGADO
               ===================================================== */

            .header-admin-online {

                display: flex !important;

                align-items: center !important;

                width: 100% !important;
            }


            .header-admin-online button {

                background:
                    linear-gradient(
                        135deg,
                        rgba(16, 185, 129, 0.25),
                        rgba(5, 150, 105, 0.25)
                    ) !important;

                border:
                    1px solid
                    rgba(52, 211, 153, 0.50) !important;

                box-shadow:
                    0 4px 12px
                    rgba(16, 185, 129, 0.20) !important;
            }


            .header-admin-online button:hover {

                background:
                    linear-gradient(
                        135deg,
                        rgba(16, 185, 129, 0.35),
                        rgba(5, 150, 105, 0.35)
                    ) !important;

                border:
                    1px solid
                    rgba(52, 211, 153, 0.70) !important;

                box-shadow:
                    0 6px 16px
                    rgba(16, 185, 129, 0.30) !important;
            }


            .header-admin-online button p {

                color: #34d399 !important;

                font-weight: 600 !important;

                font-size: 14px !important;
            }


            /* =====================================================
               RESPONSIVO
               ===================================================== */

            @media (max-width: 1200px) {

                .st-key-header_container {

                    padding: 9px 14px !important;
                }


                .vitta-header-logo-text {

                    font-size: 21px;
                }


                .vitta-header-logo img {

                    height: 38px;
                }


                .vitta-header-subtitle {

                    font-size: 9px;

                    letter-spacing: 0.045em;
                }


                .st-key-header_container button {

                    padding: 0 9px !important;

                    font-size: 13px !important;
                }


                .st-key-header_container button p {

                    font-size: 13px !important;
                }
            }


            @media (max-width: 900px) {

                .st-key-header_container {

                    padding: 7px 10px !important;

                    overflow-x: auto !important;
                }


                .block-container {

                    padding-top: 90px !important;
                }


                .vitta-header-logo-text {

                    font-size: 18px;
                }


                .vitta-header-logo img {

                    height: 34px;
                }


                .vitta-header-subtitle {

                    font-size: 8px;

                    letter-spacing: 0.035em;
                }


                .st-key-header_container
                [data-testid="stHorizontalBlock"] {

                    min-width: 900px !important;
                }
            }

            </style>
            """
        )

        # =========================================================
        # HEADER CONTAINER
        # =========================================================

        with st.container(key="header_container"):

            cols = st.columns(
                [
                    2.4,
                    0.42,
                    0.38,
                    0.48,
                    0.42,
                    0.48,
                    0.50,
                    0.48,
                ],
                gap="small",
            )

            (
                col0,
                col1,
                col2,
                col3,
                col4,
                col5,
                col6,
                col7,
            ) = cols

            # =====================================================
            # LOGO
            # =====================================================

            with col0:

                current_dir = os.path.dirname(
                    os.path.abspath(__file__)
                )

                possible_paths = [

                    os.path.join(
                        current_dir,
                        "..",
                        "assets",
                        "logotipo.png",
                    ),

                    os.path.join(
                        current_dir,
                        "src",
                        "assets",
                        "logotipo.png",
                    ),

                    os.path.join(
                        "src",
                        "assets",
                        "logotipo.png",
                    ),

                    "logotipo.png",
                ]

                logo_found = None

                for path in possible_paths:

                    if os.path.exists(path):

                        logo_found = path

                        break

                # =================================================
                # LOGO ENCONTRADA
                # =================================================

                if logo_found:

                    try:

                        with open(
                            logo_found,
                            "rb",
                        ) as image_file:

                            encoded_string = (
                                base64.b64encode(
                                    image_file.read()
                                ).decode()
                            )

                        img_src = (
                            f"data:image/png;base64,"
                            f"{encoded_string}"
                        )

                        st.html(
                            f"""
                            <a
                                href="?page=Dashboard"
                                class="vitta-header-link"
                            >

                                <div class="vitta-header-logo">

                                    <img
                                        src="{img_src}"
                                        alt="VITTA Vision"
                                    />

                                    <div class="vitta-header-brand">

                                        <span
                                            class="vitta-header-logo-text"
                                        >

                                            <span
                                                class="vitta-brand-vitta"
                                            >
                                                VITTΛ
                                            </span>

                                            <span
                                                class="vitta-brand-vision"
                                            >
                                                VISION
                                            </span>

                                        </span>

                                        <span
                                            class="vitta-header-subtitle"
                                        >

                                            <span
                                                class="vitta-subtitle-white"
                                            >
                                                Inteligência que
                                            </span>

                                            <span
                                                class="vitta-subtitle-gradient"
                                            >
                                                Transforma a Saúde
                                            </span>

                                        </span>

                                    </div>

                                </div>

                            </a>
                            """
                        )

                    except Exception:

                        st.html(
                            """
                            <div class="vitta-header-logo-fallback">

                                <div
                                    class="vitta-header-logo-icon"
                                >

                                    <div
                                        class="vitta-header-logo-dot"
                                    ></div>

                                </div>

                                <div class="vitta-header-brand">

                                    <span
                                        class="vitta-header-logo-fallback-text"
                                    >

                                        <span
                                            class="vitta-fallback-vitta"
                                        >
                                            VITTA
                                        </span>

                                        <span
                                            class="vitta-fallback-vision"
                                        >
                                            VISION
                                        </span>

                                    </span>

                                    <span
                                        class="vitta-header-subtitle"
                                    >

                                        <span
                                            class="vitta-subtitle-white"
                                        >
                                            Inteligência que
                                        </span>

                                        <span
                                            class="vitta-subtitle-gradient"
                                        >
                                            Transforma a Saúde
                                        </span>

                                    </span>

                                </div>

                            </div>
                            """
                        )

                # =================================================
                # FALLBACK
                # =================================================

                else:

                    st.html(
                        """
                        <div class="vitta-header-logo-fallback">

                            <div
                                class="vitta-header-logo-icon"
                            >

                                <div
                                    class="vitta-header-logo-dot"
                                ></div>

                            </div>

                            <div class="vitta-header-brand">

                                <span
                                    class="vitta-header-logo-fallback-text"
                                >

                                    <span
                                        class="vitta-fallback-vitta"
                                    >
                                        VITTA
                                    </span>

                                    <span
                                        class="vitta-fallback-vision"
                                    >
                                        VISION
                                    </span>

                                </span>

                                <span
                                    class="vitta-header-subtitle"
                                >

                                    <span
                                        class="vitta-subtitle-white"
                                    >
                                        Inteligência que
                                    </span>

                                    <span
                                        class="vitta-subtitle-gradient"
                                    >
                                        Transforma a Saúde
                                    </span>

                                </span>

                            </div>

                        </div>
                        """
                    )

            # =====================================================
            # FUNÇÃO DE NAVEGAÇÃO
            # =====================================================

            def navegar(nome, chave, coluna):

                with coluna:

                    is_ativo = (
                        pagina_atual == nome
                    )

                    wrapper_class = (
                        "header-active"
                        if is_ativo
                        else "header-btn"
                    )

                    st.html(
                        f"""
                        <div class="{wrapper_class}">
                        """
                    )

                    clicou = st.button(
                        nome,
                        key=chave,
                        use_container_width=True,
                    )

                    st.html(
                        """
                        </div>
                        """
                    )

                    if clicou:

                        st.query_params["page"] = nome

                        st.rerun()

            # =====================================================
            # MENU
            # =====================================================

            navegar(
                "Dashboard",
                "header_dashboard",
                col1,
            )

            navegar(
                "Leitos",
                "header_leitos",
                col2,
            )

            navegar(
                "Internações",
                "header_internacoes",
                col3,
            )

            navegar(
                "Hospitais",
                "header_hospitais",
                col4,
            )

            navegar(
                "Relatórios",
                "header_relatorios",
                col5,
            )

            # =====================================================
            # VITTA AI
            # =====================================================

            with col6:

                clicou_ai = st.button(
                    "✦ Vitta AI",
                    key="header_assistente_ia",
                    use_container_width=True,
                )

                if clicou_ai:

                    st.query_params["page"] = (
                        "Assistente IA"
                    )

                    st.rerun()

            # =====================================================
            # LOGIN / ADMIN
            # =====================================================

            with col7:

                is_admin_logado = (
                    st.session_state.get(
                        "admin_logado",
                        False,
                    )
                )

                is_ativo_admin = (
                    pagina_atual == "Admin"
                )

                # =================================================
                # ADMIN ATIVO
                # =================================================

                if is_ativo_admin:

                    texto_botao = (
                        "👤 Entrar"
                    )

                # =================================================
                # ADMIN LOGADO
                # =================================================

                elif is_admin_logado:

                    texto_botao = (
                        "👤 Painel"
                    )

                # =================================================
                # LOGIN
                # =================================================

                else:

                    texto_botao = (
                        "👤 Entrar"
                    )

                clicou_admin = st.button(
                    texto_botao,
                    key="header_admin_login",
                    use_container_width=True,
                )

                if clicou_admin:

                    st.query_params["page"] = "Admin"

                    st.rerun()