import streamlit as st
from pathlib import Path


def header_home():
    # Get project root directory
    project_root = Path(__file__).resolve().parents[3]

    # Local logo path (prefer transparent PNG, fallback to JPG)
    logo_path = project_root / "assets" / "logo_url.png"
    if not logo_path.exists():
        logo_path = project_root / "assets" / "logo_url.jpg"

    # Header styling to bring SNAP CLASS close to the logo and center both
    st.markdown(
        """
        <style>
            [data-testid="stImage"] {
                display: flex !important;
                justify-content: center !important;
                align-items: center !important;
                margin-bottom: 0px !important;
            }
            [data-testid="stImage"] > img {
                margin: 0 auto !important;
                display: block !important;
            }
            .snap-header-title {
                text-align: center !important;
                color: #FFFFFF !important;
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.2rem !important;
                line-height: 1.05 !important;
                letter-spacing: 0.02em !important;
                margin-top: -10px !important;
                margin-bottom: 24px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Horizontally centered logo container
    _, col_center, _ = st.columns([1.8, 1, 1.8])
    with col_center:
        if logo_path.exists():
            st.image(str(logo_path), width=100)
        else:
            st.error(f"Logo not found at: {logo_path}")

    # Display title directly below logo with reduced spacing
    st.markdown(
        """
        <h1 class="snap-header-title">
            SNAP<br>CLASS
        </h1>
        """,
        unsafe_allow_html=True,
    )