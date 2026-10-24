import streamlit as st
import base64
from pathlib import Path


def _get_logo_base64():
    project_root = Path(__file__).resolve().parents[3]
    logo_path = project_root / "assets" / "logo_url.png"
    if not logo_path.exists():
        logo_path = project_root / "assets" / "logo_url.jpg"
    if logo_path.exists():
        b64 = base64.b64encode(logo_path.read_bytes()).decode()
        mime = "image/png" if logo_path.suffix.lower() == ".png" else "image/jpeg"
        return f"data:{mime};base64,{b64}"
    return None


def header_home():
    logo_src = _get_logo_base64()

    # Integrated single-section centered branding (Scholar logo on top, SNAP CLASS on 1 line below)
    st.markdown(
        f"""
        <style>
            .snap-home-brand {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                width: 100%;
                margin-top: 0px;
                margin-bottom: 24px;
            }}
            .snap-home-logo {{
                width: 130px;
                height: 130px;
                object-fit: contain;
                margin-bottom: 12px;
                display: block;
                filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.12));
            }}
            .snap-home-title {{
                color: #FFFFFF !important;
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: clamp(2.2rem, 5.2vw, 3.2rem) !important;
                line-height: 1.1 !important;
                letter-spacing: 0.04em !important;
                white-space: nowrap !important;
                margin: 0 !important;
                padding: 0 !important;
                text-align: center !important;
            }}
            .snap-home-brand a,
            .snap-home-brand .header-anchor,
            .snap-home-brand [data-testid="stHeaderActionElements"],
            .snap-home-brand a.anchor-link,
            .snap-home-title a,
            .snap-home-title .header-anchor,
            .snap-home-title a[href^="#"] {{
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                pointer-events: none !important;
                width: 0 !important;
                height: 0 !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
        </style>
        <div class="snap-home-brand">
            {'<img src="' + logo_src + '" class="snap-home-logo" alt="Scholar Cap Logo" />' if logo_src else ''}
            <h1 class="snap-home-title">SNAP CLASS</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )


def header_dashboard():
    logo_src = _get_logo_base64()

    st.markdown(
        f"""
        <style>
            .snap-dash-brand {{
                display: flex;
                align-items: center;
                gap: 12px;
                margin: 0;
                padding: 4px 0;
            }}
            .snap-dash-logo {{
                width: 44px;
                height: 44px;
                object-fit: contain;
                display: block;
            }}
            .snap-dash-title {{
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 1.6rem !important;
                color: #5865F2 !important;
                margin: 0 !important;
                line-height: 1 !important;
                white-space: nowrap !important;
            }}
        </style>
        <div class="snap-dash-brand">
            {'<img src="' + logo_src + '" class="snap-dash-logo" alt="Logo" />' if logo_src else ''}
            <span class="snap-dash-title">SNAP CLASS</span>
        </div>
        """,
        unsafe_allow_html=True,
    )