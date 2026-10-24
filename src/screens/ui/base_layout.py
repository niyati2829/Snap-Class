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

        /* Hide Streamlit default chrome */
        #MainMenu,
        footer,
        header {
            visibility: hidden;
        }

        /* Main page layout container */
        .block-container {
            padding-top: 1.2rem !important;
            padding-bottom: 1.5rem !important;
            max-width: 1050px !important;
        }

        /* Headings typography */
        h1 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3.2rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
        }

        h2 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2rem !important;
            line-height: 1.15 !important;
            margin-bottom: 0rem !important;
        }

        h3,
        h4,
        p,
        label {
            font-family: 'Outfit', 'Montserrat', sans-serif !important;
        }

        /* Scope span font so Material Symbols icons are preserved and not turned to raw text */
        span:not([data-testid*="Icon"]):not([class*="material"]):not([class*="icon"]) {
            font-family: 'Outfit', 'Montserrat', sans-serif !important;
        }

        /* Portal cards (Home Screen) */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: #E0E3FF !important;
            border-radius: 2.5rem !important;
            border: none !important;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08) !important;
            padding: 1.5rem !important;
            min-height: 380px !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: space-between !important;
            box-sizing: border-box !important;
        }

        /* Portal card images */
        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] {
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
            height: 220px !important;
            margin: 0 auto !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stImage"] img {
            max-width: 100% !important;
            max-height: 210px !important;
            width: auto !important;
            object-fit: contain !important;
            display: block !important;
            margin: 0 auto !important;
        }

        /* General action buttons scoped strictly to .stButton > button */
        .stButton > button {
            border-radius: 1.8rem !important;
            background-color: #5865F2 !important;
            color: white !important;
            font-family: 'Outfit', 'Montserrat', sans-serif !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            padding: 10px 22px !important;
            border: none !important;
            min-height: 46px !important;
            transition: all 0.2s ease-in-out !important;
            cursor: pointer !important;
            box-shadow: 0 4px 12px rgba(88, 101, 242, 0.25) !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(88, 101, 242, 0.35) !important;
        }

        /* Secondary buttons (Pink Accent) */
        .stButton > button[kind="secondary"] {
            background-color: #EB459E !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(235, 69, 158, 0.25) !important;
        }

        .stButton > button[kind="secondary"]:hover {
            box-shadow: 0 6px 16px rgba(235, 69, 158, 0.35) !important;
        }

        /* Tertiary buttons (Dark/Neutral Accent) */
        .stButton > button[kind="tertiary"] {
            background-color: #1e293b !important;
            color: white !important;
            box-shadow: 0 4px 10px rgba(30, 41, 59, 0.2) !important;
        }

        /* Text Input Fields styling */
        [data-testid="stTextInput"] input {
            border-radius: 1rem !important;
            min-height: 46px !important;
            font-family: 'Outfit', sans-serif !important;
            border: 1px solid #cbd5e1 !important;
            padding: 8px 14px !important;
        }

        [data-testid="stTextInput"] input:focus {
            border-color: #5865F2 !important;
            box-shadow: 0 0 0 2px rgba(88, 101, 242, 0.2) !important;
        }

        /* Streamlit Password Visibility Eye Toggle Button — Prevent distortion or clipping */
        [data-testid="stTextInputRootElement"] button {
            background: transparent !important;
            border: none !important;
            color: #64748b !important;
            box-shadow: none !important;
            padding: 0 10px !important;
            min-height: auto !important;
            width: auto !important;
            border-radius: 0 !important;
            transform: none !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        [data-testid="stTextInputRootElement"] button:hover {
            background: transparent !important;
            color: #5865F2 !important;
            transform: none !important;
            box-shadow: none !important;
        }

        [data-testid="stTextInputRootElement"] button svg {
            width: 18px !important;
            height: 18px !important;
        }

        /* Portal button alignment */
        [data-testid="stVerticalBlockBorderWrapper"] .stButton {
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
            width: 90% !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )