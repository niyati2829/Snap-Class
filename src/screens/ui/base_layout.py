import streamlit as st


def style_background_home():
    st.markdown(
        """
        <style>
            .stApp,
            [data-testid="stAppViewContainer"] {
                background: #5865F2 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_background_dashboard():
    st.markdown(
        """
        <style>
            .stApp,
            [data-testid="stAppViewContainer"] {
                background: #E0E3FF !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_base_layout():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Montserrat:ital,wght@0,100..900;1,100..900&family=Outfit:wght@100..900&display=swap');
            #mainMenu, footer, header {
                visibility: hidden;
            }
            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 2rem !important;
                max-width: 900px !important;
            }
            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.2rem !important;
                line-height: 1.05 !important;
                margin-bottom: 0rem !important;
            }
            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2.5rem !important;
                line-height: 1.2 !important;
                margin-bottom: 0rem !important;
            }

            /* Portal Card Styling */
            [data-testid="stVerticalBlockBorderWrapper"] {
                background: #FFFFFF !important;
                border-radius: 28px !important;
                border: none !important;
                box-shadow: 0 12px 36px rgba(0, 0, 0, 0.18) !important;
                padding: 24px 20px 22px 20px !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                justify-content: space-between !important;
                min-height: 330px !important;
            }
            [data-testid="stVerticalBlockBorderWrapper"]:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 18px 44px rgba(0, 0, 0, 0.25) !important;
            }

            /* Portal Card Illustration */
            [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] {
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                height: 220px !important;
                width: 100% !important;
            }
            [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] img {
                max-height: 200px !important;
                max-width: 100% !important;
                width: auto !important;
                object-fit: contain !important;
                margin: 0 auto !important;
                display: block !important;
                border-radius: 12px !important;
            }

            /* Button Styling */
            button[kind="secondary"],
            button[kind="primary"],
            .stButton > button {
                border-radius: 2rem !important;
                background: #EB459E !important;
                color: #FFFFFF !important;
                font-family: 'Outfit', 'Montserrat', sans-serif !important;
                font-size: 1.15rem !important;
                font-weight: 700 !important;
                padding: 12px 24px !important;
                border: none !important;
                box-shadow: 0 4px 14px rgba(235, 69, 158, 0.4) !important;
                transition: all 0.25s ease-in-out !important;
                width: 100% !important;
            }
            button[kind="secondary"]:hover,
            button[kind="primary"]:hover,
            .stButton > button:hover {
                background: #d8358c !important;
                transform: scale(1.03) !important;
                box-shadow: 0 6px 20px rgba(235, 69, 158, 0.55) !important;
                color: #FFFFFF !important;
            }
            button[kind="secondary"]:active,
            button[kind="primary"]:active,
            .stButton > button:active {
                transform: scale(0.98) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )